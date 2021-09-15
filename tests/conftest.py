from brownie import Wei
import pytest

crvRenWBTC_address = "0x49849C98ae39Fff122806C06791Fa73784FB3675"
tree_address = "0x660802Fc641b154aBA66a62137e71f331B6d787A"
cvxHelperVault = "0x53C8E199eb2Cb7c01543C137078a038937a68E40"
cvxCrvHelperVault = "0x2B5455aac8d64C14786c3a29858E43b5945819C0"
yieldDistributor = "0xB65cef03b9B89f99517643226d76e286ee999e77"
badgerSettPeak = "0x41671BA1abcbA387b9b2B752c205e22e916BE6e3"
bTokenAddress = "0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545"

CRV_ADDR = "0xD533a949740bb3306d119CC777fa900bA034cd52"
CVX_ADDR = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"
CVXCRV_ADDR = "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7"


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


@pytest.fixture(scope="module")
def strategy(HarvestRestructure, config_addresses, deployer):
    strategy = deployer.deploy(HarvestRestructure)

    # crvRenWBTC test
    want_config = [
        crvRenWBTC_address,
        tree_address,
        cvxHelperVault,
        cvxCrvHelperVault,
        yieldDistributor,
        badgerSettPeak,
        bTokenAddress,
    ]
    pid = 6
    fee_config = [2000, 0, 50]
    curve_pool = ["0x93054188d876f558f4a66B2EF1d97d16eDf0895B", 1, 2]

    strategy.initiliazed(
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
