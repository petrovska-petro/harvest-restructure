from brownie import Contract, HarvestRestructure, Wei
import pytest

# config values ibBTC
yieldDistributor = "0x55e4d16f9c3041EfF17Ca32850662f3e9Dddbce7"
badgerSettPeak = "0x41671BA1abcbA387b9b2B752c205e22e916BE6e3"
bTokenAddress = "0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545"

# helper to update strategy logic in test
def upgrade_strategy(proxyAdmin, strategy_proxy, strategyLogic, governance):
    proxyAdmin.upgrade(
        strategy_proxy,
        strategyLogic,
        {"from": governance},
    )


def test_upgraded_crv_strats_storage(strategy, proxyAdminTest, helper, governance):
    strategy_proxy = proxyAdminTest[0]
    proxy_admin = proxyAdminTest[1]

    with pytest.raises(AttributeError):
        strategy_proxy.crvCvxCrvPoolIndex()

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

    upgrade_strategy(proxy_admin, strategy_proxy, strategy.address, governance)

    strategy_proxy = Contract.from_abi(
        "HarvestRestructure", strategy_proxy.address, HarvestRestructure.abi
    )

    print("\n ==== NOTE: Proxy logic has been upgraded! ==== ")

    # call setConfigibBTC
    strategy_proxy.setConfigibBTC(
        yieldDistributor,
        badgerSettPeak,
        bTokenAddress,
        helper.address,
        Wei("250 ether"), # it can be tinker, but a min of 200-250 will make sense due to the cost of operation involved
        6000,
        {"from": governance},
    )

    # Check that it's upgraded (metaPoolIndex, ibBTCRetentionBps, thresholdThreeCrv...)
    assert strategy_proxy.crvCvxCrvPoolIndex() == 2
    assert strategy_proxy.ibBTCRetentionBps() == 6000
    assert strategy_proxy.thresholdThreeCrv() == Wei("250 ether")

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
