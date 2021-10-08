from brownie import (
    Contract,
    HarvestRestructure,
)
import pytest

# strategies deploy dictionary
strat_dictionary = {
    "native.renCrv": "0x6582a5b139fc1c6360846efdc4440d51aad4df7b",
    "native.sbtcCrv": "0xf1ded284e891943b3e9c657d7fc376b86164ffc2",
    "native.tbtcCrv": "0x522bb024c339a12be1a47229546f288c40b62d29",
}

# This strats are affected by this update atm
CRV_STRATS = ["native.renCrv", "native.sbtcCrv", "native.tbtcCrv"]

# helper to update strategy logic in test
def upgrade_strategy(devProxyAdmin, strategy_proxy, strategyLogic, governanceTimelock):
    devProxyAdmin.upgrade(
        strategy_proxy,
        strategyLogic,
        {"from": governanceTimelock},
    )


def get_strategy(key):
    return strat_dictionary[key]


@pytest.mark.parametrize(
    "strategy_key",
    CRV_STRATS,
)
def test_upgraded_crv_strats_storage(
    devProxyAdmin, strategy, governance_lock, strategy_key
):
    # as_proxy_for="0x01d10fdc6b484BE380144dF12EB6C75387EfC49B"
    strategy_proxy = Contract.from_explorer(get_strategy(strategy_key))

    with pytest.raises(AttributeError):
        strategy_proxy.metaPoolIndex()

    # TODO: There's probably a better way to do this
    baseRewardsPool = strategy_proxy.baseRewardsPool()
    pid = strategy_proxy.pid()
    badgerTree = strategy_proxy.badgerTree()
    cvxHelperVault = strategy_proxy.cvxHelperVault()
    cvxCrvHelperVault = strategy_proxy.cvxCrvHelperVault()
    curvePool = strategy_proxy.curvePool()
    autoCompoundingBps = strategy_proxy.autoCompoundingBps()
    autoCompoundingPerformanceFeeGovernance = (
        strategy_proxy.autoCompoundingPerformanceFeeGovernance()
    )
    autoCompoundingPerformanceFeeGovernance = (
        strategy_proxy.autoCompoundingPerformanceFeeGovernance()
    )

    upgrade_strategy(
        devProxyAdmin, strategy_proxy.address, strategy.address, governance_lock
    )

    print("\n ==== NOTE: Proxy logic has been upgraded! ==== ")

    proxy_updated = Contract.from_abi(
        "HarvestRestructure", strategy_proxy.address, HarvestRestructure.abi
    )

    # Check that it's upgraded (metaPoolIndex, ibBTCRetentionBps, thresholdThreeCrv...)
    assert proxy_updated.metaPoolIndex() == 2
    assert strategy_proxy.ibBTCRetentionBps() == 6000
    assert strategy_proxy.thresholdThreeCrv() == 250

    assert baseRewardsPool == strategy_proxy.baseRewardsPool()
    assert pid == strategy_proxy.pid()
    assert badgerTree == strategy_proxy.badgerTree()
    assert cvxHelperVault == strategy_proxy.cvxHelperVault()
    assert cvxCrvHelperVault == strategy_proxy.cvxCrvHelperVault()
    assert curvePool == strategy_proxy.curvePool()
    assert autoCompoundingBps == strategy_proxy.autoCompoundingBps()
    assert (
        autoCompoundingPerformanceFeeGovernance
        == strategy_proxy.autoCompoundingPerformanceFeeGovernance()
    )
    assert autoCompoundingPerformanceFeeGovernance == (
        strategy_proxy.autoCompoundingPerformanceFeeGovernance()
    )
