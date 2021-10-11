from brownie import Wei, Contract
import pytest

OPENZEPPELIN_CONTRACTS = "OpenZeppelin/openzeppelin-contracts@3.4.0"

crvRenWBTC_address = "0x49849C98ae39Fff122806C06791Fa73784FB3675"
tree_address = "0x660802Fc641b154aBA66a62137e71f331B6d787A"
cvxHelperVault = "0x53C8E199eb2Cb7c01543C137078a038937a68E40"
cvxCrvHelperVault = "0x2B5455aac8d64C14786c3a29858E43b5945819C0"
governanceLock = "0x21CF9b77F88Adf8F8C98d7E33Fe601DC57bC0893"
yieldDistributor = "0x55e4d16f9c3041EfF17Ca32850662f3e9Dddbce7"
badgerSettPeak = "0x41671BA1abcbA387b9b2B752c205e22e916BE6e3"
bTokenAddress = "0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545"

CRV_ADDR = "0xD533a949740bb3306d119CC777fa900bA034cd52"
CVX_ADDR = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"
CVXCRV_ADDR = "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7"
THREE_CRV_ADDR = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"
WBTC_ADDR = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
DEV_PROXY_ADMIN = "0x20Dce41Acca85E8222D6861Aa6D23B6C941777bF"


@pytest.fixture(scope="module")
def deployer(accounts):
    yield accounts.at("0xDA25ee226E534d868f0Dd8a459536b03fEE9079b", force=True)


@pytest.fixture(scope="module")
def governance(accounts):
    yield accounts.at("0xB65cef03b9B89f99517643226d76e286ee999e77", force=True)


@pytest.fixture(scope="module")
def strategist(accounts):
    yield accounts.at("0x55949F769d0aF7453881435612561D109fFF07B8", force=True)


@pytest.fixture(scope="module")
def controller(accounts):
    yield accounts.at("0x63cF44B2548e4493Fd099222A1eC79F3344D9682", force=True)


@pytest.fixture(scope="module")
def keeper(accounts):
    yield accounts.at("0x711A339c002386f9db409cA55b6A35a604aB6cF6", force=True)


@pytest.fixture(scope="module")
def guardian(accounts):
    yield accounts.at("0x29F7F8896Fb913CF7f9949C623F896a154727919", force=True)


@pytest.fixture(scope="module")
def yield_distributor_dummy(accounts):
    yield accounts.at(yieldDistributor, force=True)


@pytest.fixture(scope="module")
def governance_lock(accounts):
    yield accounts.at(governanceLock, force=True)


@pytest.fixture(scope="module")
def config_addresses(governance, strategist, controller, keeper, guardian):
    yield [governance, strategist, controller, keeper, guardian]


@pytest.fixture
def crv(interface):
    yield interface.ERC20(CRV_ADDR)


@pytest.fixture
def cvx(interface):
    yield interface.ERC20(CVX_ADDR)


@pytest.fixture
def cvxcrv(interface):
    yield interface.ERC20(CVXCRV_ADDR)


@pytest.fixture
def three_crv(interface):
    yield interface.ERC20(THREE_CRV_ADDR)


@pytest.fixture(scope="module")
def wbtc(interface):
    yield interface.ERC20(WBTC_ADDR)


@pytest.fixture(scope="module")
def devProxyAdmin(interface):
    yield interface.IDevProxyAdmin(DEV_PROXY_ADMIN)


@pytest.fixture(scope="module")
def proxyAdminTest(StrategyConvexStakingOptimizer, config_addresses, governance, pm):
    OPENZEPPELIN = pm(OPENZEPPELIN_CONTRACTS)

    old_strategy = governance.deploy(StrategyConvexStakingOptimizer)

    want_config = [crvRenWBTC_address, tree_address, cvxHelperVault, cvxCrvHelperVault]
    pid = 6
    fee_config = [2000, 0, 50]
    curve_pool = ["0x93054188d876f558f4a66B2EF1d97d16eDf0895B", 1, 2]

    encode_input = old_strategy.initialize.encode_input(
        config_addresses[0],
        config_addresses[1],
        config_addresses[2],
        config_addresses[3],
        config_addresses[4],
        want_config,
        pid,
        fee_config,
        curve_pool,
    )

    proxy_admin = governance.deploy(OPENZEPPELIN.ProxyAdmin)

    proxy = governance.deploy(
        OPENZEPPELIN.TransparentUpgradeableProxy,
        old_strategy.address,
        proxy_admin.address,
        encode_input,
    )

    proxy_strat = Contract.from_abi(
        "StrategyConvexStakingOptimizer", proxy.address, old_strategy.abi
    )

    yield proxy_strat, proxy_admin, proxy


@pytest.fixture(scope="module")
def bCVX(interface):
    yield interface.ISettV4(cvxHelperVault)


@pytest.fixture(scope="module")
def bCVXCRV(interface):
    yield interface.ISettV4(cvxCrvHelperVault)


@pytest.fixture(scope="module")
def helper(ibBTCV1Helper, deployer):
    helper = deployer.deploy(ibBTCV1Helper)
    print(f" === ibBTCV1Helper address={helper.address} === ")
    yield helper


@pytest.fixture(scope="module")
def strategy(HarvestRestructure, config_addresses, deployer, bCVX, bCVXCRV, helper):
    strategy = deployer.deploy(HarvestRestructure)
    print(f" === HarvestRestructure address={strategy.address} === ")
    # crvRenWBTC test
    want_config = [crvRenWBTC_address, tree_address, cvxHelperVault, cvxCrvHelperVault]
    pid = 6
    fee_config = [2000, 0, 50]
    curve_pool = ["0x93054188d876f558f4a66B2EF1d97d16eDf0895B", 1, 2]

    strategy.initialize(
        config_addresses[0],
        config_addresses[1],
        config_addresses[2],
        config_addresses[3],
        config_addresses[4],
        want_config,
        pid,
        fee_config,
        curve_pool,
    )

    # call patches for swapping route
    strategy.patchPaths({"from": config_addresses[0]})
    # config for BIP-68
    strategy.setConfigibBTC(
        yieldDistributor,
        badgerSettPeak,
        bTokenAddress,
        helper.address,
        Wei("250 ether"), # it can be tinker, but a min of 200-250 will make sense due to the cost of operation involved
        6000,
        {"from": config_addresses[0]},
    )

    # whitelist strat for the deposits
    bCVX.approveContractAccess(strategy.address, {"from": config_addresses[0]})
    bCVXCRV.approveContractAccess(strategy.address, {"from": config_addresses[0]})

    yield strategy


@pytest.fixture
def whale_crv(accounts, crv, strategy):
    crv_amount = Wei("3400 ether")
    whale_crv = accounts.at("0x687F7A828f3bb959F76BEAFfd34E998D63FEEe72", force=True)
    crv.transfer(strategy, crv_amount, {"from": whale_crv})
    yield whale_crv


@pytest.fixture
def whale_cvx(accounts, cvx, strategy):
    cvx_amount = Wei("1200 ether")
    whale_cvx = accounts.at("0xa6cf13Fa4df69F09A518e2F4419f7Ae1Cae71eC6", force=True)
    cvx.transfer(strategy, cvx_amount, {"from": whale_cvx})
    yield whale_cvx


@pytest.fixture
def whale_cvxcrv(accounts, cvxcrv, strategy):
    cvxcrv_amount = Wei("1200 ether")
    whale_cvxcrv = accounts.at("0xB65cef03b9B89f99517643226d76e286ee999e77", force=True)
    cvxcrv.transfer(strategy, cvxcrv_amount, {"from": whale_cvxcrv})
    yield whale_cvx


@pytest.fixture
def whale_three_crv(accounts, three_crv, strategy):
    threee_crv_amount = Wei("200 ether")
    whale_three_crv = accounts.at(
        "0x99459A327E2e1f7535501AFF6A1Aada7024C45FD", force=True
    )
    three_crv.transfer(strategy, threee_crv_amount, {"from": whale_three_crv})
    yield whale_three_crv
