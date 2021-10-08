from brownie import (
    Contract,
    HarvestRestructure,
)
import pytest

# helper to update strategy logic in test
def upgrade_strategy(proxyAdmin, strategy_proxy, strategyLogic, governance):
    proxyAdmin.upgrade(
        strategy_proxy,
        strategyLogic,
        {"from": governance},
    )


def test_upgraded_crv_strats_storage(strategy, proxyAdminTest, governance):
    strategy_proxy = proxyAdminTest[0]
    proxy_admin = proxyAdminTest[1]
    proxy_strat_address = proxyAdminTest[2]

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

    proxy_strat_updated = Contract.from_abi(
        "HarvestRestructure", proxy_strat_address, HarvestRestructure.abi
    )

    upgrade_strategy(proxy_admin, proxy_strat_address, strategy, governance)

    print("\n ==== NOTE: Proxy logic has been upgraded! ==== ")

    # Check that it's upgraded (metaPoolIndex, ibBTCRetentionBps, thresholdThreeCrv...)
    assert proxy_strat_updated.metaPoolIndex() == 2
    assert proxy_strat_updated.ibBTCRetentionBps() == 6000
    assert proxy_strat_updated.thresholdThreeCrv() == 250

    assert baseRewardsPool == proxy_strat_updated.baseRewardsPool()
    assert pid == proxy_strat_updated.pid()
    assert badgerTree == proxy_strat_updated.badgerTree()
    assert cvxHelperVault == proxy_strat_updated.cvxHelperVault()
    assert cvxCrvHelperVault == proxy_strat_updated.cvxCrvHelperVault()
    assert curvePool == proxy_strat_updated.curvePool()
    assert autoCompoundingBps == proxy_strat_updated.autoCompoundingBps()
    assert (
        autoCompoundingPerformanceFeeGovernance
        == proxy_strat_updated.autoCompoundingPerformanceFeeGovernance()
    )
    assert autoCompoundingPerformanceFeeGovernance == (
        proxy_strat_updated.autoCompoundingPerformanceFeeGovernance()
    )
