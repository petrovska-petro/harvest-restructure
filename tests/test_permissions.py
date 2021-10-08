from brownie import reverts, ZERO_ADDRESS


def test_action_permissions(strategy, accounts):
    random_address = accounts[8]

    tendable = strategy.isTendable()

    with reverts("onlyAuthorizedActors"):
        strategy.harvest({"from": random_address})

    if tendable:
        with reverts("onlyAuthorizedActors"):
            strategy.tend({"from": random_address})

    with reverts("onlyController"):
        strategy.withdrawAll({"from": random_address})

    with reverts("onlyController"):
        strategy.withdraw(1, {"from": random_address})

    with reverts("onlyController"):
        strategy.withdrawOther(ZERO_ADDRESS, {"from": random_address})


# check config of new params
def test_config_permissions(strategy, governance, accounts):
    random_address = accounts[8]

    # Valid address should update
    strategy.setMetaPoolIndex(1, {"from": governance})
    assert strategy.metaPoolIndex() == 1

    strategy.setThresholdThreeCrv(350, {"from": governance})
    assert strategy.thresholdThreeCrv() == 350

    strategy.setibBTCRetentionBps(50, {"from": governance})
    assert strategy.ibBTCRetentionBps() == 50

    # Invalid address revert
    with reverts("onlyGovernance"):
        strategy.setMetaPoolIndex(0, {"from": random_address})

    with reverts("onlyGovernance"):
        strategy.setThresholdThreeCrv(0, {"from": random_address})

    with reverts("onlyGovernance"):
        strategy.setibBTCRetentionBps(0, {"from": random_address})


def test_pausing_permissions(strategy, accounts):
    random_address = accounts[8]

    authorizedPausers = [
        strategy.governance(),
        strategy.guardian(),
    ]

    authorizedUnpausers = [
        strategy.governance(),
    ]

    # pause onlyPausers
    for pauser in authorizedPausers:
        strategy.pause({"from": pauser})
        strategy.unpause({"from": authorizedUnpausers[0]})

    with reverts("onlyPausers"):
        strategy.pause({"from": random_address})

    # unpause onlyPausers
    for unpauser in authorizedUnpausers:
        strategy.pause({"from": unpauser})
        strategy.unpause({"from": unpauser})

    with reverts("onlyGovernance"):
        strategy.unpause({"from": random_address})

    strategy.pause({"from": strategy.guardian()})

    strategyKeeper = accounts.at(strategy.keeper(), force=True)

    with reverts("Pausable: paused"):
        strategy.harvest({"from": strategyKeeper})
    if strategy.isTendable():
        with reverts("Pausable: paused"):
            strategy.tend({"from": strategyKeeper})
