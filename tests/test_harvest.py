from brownie import chain
from pytest import approx


def test_harvest(strategy, governance, whale_crv, whale_cvx, whale_cvxcrv):
    strategy.tend({"from": governance})
    chain.mine(10)

    tx = strategy.harvest({"from": governance})

    print(f"wbtcTokenYieldAccum={strategy.pendingWbtcAccumForPpfsZapper()}")

    events = tx.events

    print(f" ==== Harvest event -> {events['Harvest']['harvested'] } ==== ")
    
    assert strategy.cvxToGovernanceAccum() > 0
    assert strategy.cvxCrvToGovernanceAccum() > 0
    assert strategy.pendingWbtcAccumForPpfsZapper() > 0
    assert events['Harvest']['harvested'] > 0


# this just to get the high range on the gas profiling as it will add 2 tx extras
def test_harvest_swap_3crv(
    strategy, governance, whale_crv, whale_cvx, whale_cvxcrv, whale_three_crv
):
    strategy.tend({"from": governance})
    chain.mine(10)

    strategy.harvest({"from": governance})
