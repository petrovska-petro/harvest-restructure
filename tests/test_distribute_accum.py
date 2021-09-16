from brownie import chain


def test_collect_to_governance(
    strategy, governance, whale_crv, whale_cvx, whale_cvxcrv, bCVX, bCVXCRV
):
    strategy.tend({"from": governance})
    chain.mine(10)
    strategy.harvest({"from": governance})

    balance_bCVX_before = bCVX.balanceOf(governance)
    balance_bCVXCRV_before = bCVXCRV.balanceOf(governance)

    strategy.collectPerformanceFees()

    balance_bCVX_after = bCVX.balanceOf(governance)
    balance_bCVXCRV_after = bCVXCRV.balanceOf(governance)

    assert balance_bCVX_after > balance_bCVX_before
    assert balance_bCVXCRV_after > balance_bCVXCRV_before


def test_collect_to_yield_distributor(
    strategy,
    governance,
    yield_distributor_dummy,
    wbtc,
):
    wbtc_balance_strat_before = wbtc.balanceOf(strategy)
    print(f"Strat wbtc={wbtc_balance_strat_before}")

    wbtc_balance_distributor_before = wbtc.balanceOf(yield_distributor_dummy)

    strategy.transferWbtcTokenYield({"from": governance})

    wbtc_balance_strat_after = wbtc.balanceOf(strategy)
    wbtc_balance_distributor_after = wbtc.balanceOf(yield_distributor_dummy)

    assert wbtc_balance_strat_after == 0
    assert wbtc_balance_distributor_after > wbtc_balance_distributor_before
