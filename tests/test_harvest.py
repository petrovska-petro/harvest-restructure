from brownie import chain

def test_harvest(strategy, governance, whale_crv, whale_cvx, whale_cvxcrv):
    strategy.tend({"from": governance})
    chain.mine(10)
    # pendant of whitelisting the strat to test properly the harvest flow...
    strategy.harvest({"from": governance})
