from brownie import chain

def test_harvest(strategy, governance, whale_crv, whale_cvx, whale_cvxcrv):
    strategy.tend({"from": governance})
    chain.mine(10)
    tx = strategy.harvest({"from": governance})
