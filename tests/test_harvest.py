from brownie import chain
from pytest import approx

def test_harvest(strategy, governance, whale_crv, whale_cvx, whale_cvxcrv):
    strategy.tend({"from": governance})
    chain.mine(10)

    tx = strategy.harvest({"from": governance})

    events = tx.events

    perf_fee = strategy.performanceFeeGovernance() / strategy.MAX_FEE()
    
    assert (
        approx(strategy.cvxToGovernanceAccum())
        == events["HarvestCustom"]["cvxHarvested"] * perf_fee
    )
    assert (
        approx(strategy.cvxCrvToGovernanceAccum())
        == events["HarvestCustom"]["cvxCrvHarvested"] * perf_fee
    )
    assert strategy.wbtcTokenYieldAccum() > 0


# this just to get the high range on the gas profiling as it will add 2 tx extras
def test_harvest_swap_3crv(strategy, governance, whale_crv, whale_cvx, whale_cvxcrv, whale_three_crv):
    strategy.tend({"from": governance})
    chain.mine(10)

    strategy.harvest({"from": governance})
