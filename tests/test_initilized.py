crvRenWBTC_address = "0x49849C98ae39Fff122806C06791Fa73784FB3675"
tree_address = "0x660802Fc641b154aBA66a62137e71f331B6d787A"
cvxHelperVault = "0x53C8E199eb2Cb7c01543C137078a038937a68E40"
cvxCrvHelperVault = "0x2B5455aac8d64C14786c3a29858E43b5945819C0"
yieldDistributor = "0xB65cef03b9B89f99517643226d76e286ee999e77"
badgerSettPeak = "0x41671BA1abcbA387b9b2B752c205e22e916BE6e3"
bTokenAddress = "0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545"


def test_initiliazed(strategy, config_addresses):
    # config addresses
    assert strategy.governance() == config_addresses[0]
    assert strategy.strategist() == config_addresses[1]
    assert strategy.controller() == config_addresses[2]
    assert strategy.keeper() == config_addresses[3]
    assert strategy.guardian() == config_addresses[4]
    # config want
    assert strategy.want() == crvRenWBTC_address
    assert strategy.badgerTree() == tree_address
    assert strategy.cvxHelperVault() == cvxHelperVault
    assert strategy.cvxCrvHelperVault() == cvxCrvHelperVault
    assert strategy.yieldDistributor() == yieldDistributor
    assert strategy.badgerSettPeak() == badgerSettPeak
    assert strategy.bTokenAddress() == bTokenAddress
    # pid
    assert strategy.pid() == 6
    # config fee
    assert strategy.performanceFeeGovernance() == 2000
    assert strategy.performanceFeeStrategist() == 0
    assert strategy.withdrawalFee() == 50
    # curve pools checks
    curve_pool_struct = strategy.curvePool()
    assert curve_pool_struct[0] == "0x93054188d876f558f4a66B2EF1d97d16eDf0895B"
    assert curve_pool_struct[1] == 1
    assert curve_pool_struct[2] == 2
