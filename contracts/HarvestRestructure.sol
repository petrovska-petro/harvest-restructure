// SPDX-License-Identifier: MIT
pragma solidity ^0.6.11;
pragma experimental ABIEncoderV2;

import "@openzeppelin-upgradeable/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@openzeppelin-upgradeable/contracts/token/ERC20/SafeERC20Upgradeable.sol";

import "interfaces/badger/ISettV4.sol";
import "interfaces/convex/IBaseRewardsPool.sol";
import "interfaces/convex/ICvxRewardsPool.sol";
import "interfaces/convex/IBaseRewardsPool.sol";
import "interfaces/convex/IBooster.sol";

import "./deps/BaseStrategy.sol";
import "./deps/CurveSwapper.sol";
import "./deps/UniswapSwapper.sol";
import "./deps/TokenSwapPathRegistry.sol";

contract HarvestRestructure is
    BaseStrategy,
    CurveSwapper,
    UniswapSwapper,
    TokenSwapPathRegistry
{
    event WithdrawState(
        uint256 toWithdraw,
        uint256 preWant,
        uint256 postWant,
        uint256 withdrawn
    );

    event TreeDistribution(
        address indexed token,
        uint256 amount,
        uint256 indexed blockNumber,
        uint256 timestamp
    );

    event TendState(uint256 crvTended, uint256 cvxTended, uint256 cvxCrvTended);

    event PerformanceFeeGovernance(
        address indexed destination,
        address indexed token,
        uint256 amount,
        uint256 indexed blockNumber,
        uint256 timestamp
    );

    event DistributeWbtcYield(uint256 amount, uint256 indexed blockNumber);

    event HarvestCustom(
        uint256 cvxCrvHarvested,
        uint256 cvxHarvested,
        uint256 indexed blockNumber
    );

    struct HarvestData {
        uint256 cvxCrvHarvested;
        uint256 cvxHarvested;
    }

    struct TendData {
        uint256 crvTended;
        uint256 cvxTended;
        uint256 cvxCrvTended;
    }

    struct CurvePoolConfig {
        address swap;
        uint256 wbtcPosition;
        uint256 numElements;
    }

    // ===== threshold params for swaps =====
    uint256 public thresholdThreeCrv = 200 ether;

    // ===== strategy params =====
    uint256 public autoCompoundingBps = 2000;
    uint256 public ibBTCRetentionBps = 6000;
    uint256 public treeBps = 6000;

    // ===== accum variables =====
    uint256 public wbtcTokenYieldAccum;
    uint256 public cvxCrvToGovernanceAccum;
    uint256 public cvxToGovernanceAccum;

    // ===== Token Registry =====
    address public constant wbtc = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599;
    address public constant weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address public constant crv = 0xD533a949740bb3306d119CC777fa900bA034cd52;
    address public constant cvx = 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B;
    address public constant cvxCrv = 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7;
    address public constant usdc = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address public constant threeCrv =
        0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;

    IERC20Upgradeable public constant wbtcToken =
        IERC20Upgradeable(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    IERC20Upgradeable public constant crvToken =
        IERC20Upgradeable(0xD533a949740bb3306d119CC777fa900bA034cd52);
    IERC20Upgradeable public constant cvxToken =
        IERC20Upgradeable(0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B);
    IERC20Upgradeable public constant cvxCrvToken =
        IERC20Upgradeable(0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7);
    IERC20Upgradeable public constant usdcToken =
        IERC20Upgradeable(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    IERC20Upgradeable public constant threeCrvToken =
        IERC20Upgradeable(0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490);

    // ===== Convex Registry =====
    IBaseRewardsPool public baseRewardsPool;
    IBooster public constant booster =
        IBooster(0xF403C135812408BFbE8713b5A23a04b3D48AAE31);
    IBaseRewardsPool public constant cvxCrvRewardsPool =
        IBaseRewardsPool(0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e);
    ICvxRewardsPool public constant cvxRewardsPool =
        ICvxRewardsPool(0xCF50b810E57Ac33B91dCF525C6ddd9881B139332);
    address public constant threeCrvSwap =
        0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;

    uint256 public constant MAX_UINT_256 = uint256(-1);
    uint256 public constant WBTC_INDEX_OUTPUT = 3;

    uint256 public pid;
    address public badgerTree;
    address public yieldDistributor;
    address public bTokenAddress;
    address public badgerSettPeak;
    ISettV4 public cvxHelperVault;
    ISettV4 public cvxCrvHelperVault;
    CurvePoolConfig public curvePool;

    function initiliazed(
        address _governance,
        address _strategist,
        address _controller,
        address _keeper,
        address _guardian,
        address[7] memory _wantConfig,
        uint256 _pid,
        uint256[3] memory _feeConfig,
        CurvePoolConfig memory _curvePool
    ) public initializer whenNotPaused {
        __BaseStrategy_init(
            _governance,
            _strategist,
            _controller,
            _keeper,
            _guardian
        );

        want = _wantConfig[0];
        badgerTree = _wantConfig[1];

        cvxHelperVault = ISettV4(_wantConfig[2]);
        cvxCrvHelperVault = ISettV4(_wantConfig[3]);

        yieldDistributor = _wantConfig[4];
        badgerSettPeak = _wantConfig[5];
        bTokenAddress = _wantConfig[6];

        pid = _pid;

        IBooster.PoolInfo memory poolInfo = booster.poolInfo(pid);
        baseRewardsPool = IBaseRewardsPool(poolInfo.crvRewards);

        performanceFeeGovernance = _feeConfig[0];
        performanceFeeStrategist = _feeConfig[1];
        withdrawalFee = _feeConfig[2];

        // Approvals: Staking Pools
        IERC20Upgradeable(want).approve(address(booster), MAX_UINT_256);
        cvxToken.approve(address(cvxRewardsPool), MAX_UINT_256);
        cvxCrvToken.approve(address(cvxCrvRewardsPool), MAX_UINT_256);

        curvePool = CurvePoolConfig(
            _curvePool.swap,
            _curvePool.wbtcPosition,
            _curvePool.numElements
        );

        // Set Swap Paths - fix some that are suffering
        address[] memory path = new address[](4);
        path[0] = usdc;
        path[1] = weth;
        path[2] = crv;
        path[3] = cvxCrv;
        _setTokenSwapPath(usdc, cvxCrv, path);

        path = new address[](4);
        path[0] = cvxCrv;
        path[1] = crv;
        path[2] = weth;
        path[3] = wbtc;
        _setTokenSwapPath(cvxCrv, wbtc, path);

        path = new address[](3);
        path[0] = cvx;
        path[1] = weth;
        path[2] = wbtc;
        _setTokenSwapPath(cvx, wbtc, path);

        path = new address[](2);
        path[0] = crv;
        path[1] = cvxCrv;
        _setTokenSwapPath(crv, cvxCrv, path);

        _initializeApprovals();
    }

    /// ===== View Functions =====
    function getName() external pure override returns (string memory) {
        return "StrategyConvexStakingOptimizer-Restructure";
    }

    /// ===== Internal Core Implementations =====
    function _onlyNotProtectedTokens(address _asset) internal override {
        require(address(want) != _asset, "want");
        require(address(crv) != _asset, "crv");
        require(address(cvx) != _asset, "cvx");
        require(address(cvxCrv) != _asset, "cvxCrv");
    }

    function _initializeApprovals() internal {
        cvxToken.approve(address(cvxHelperVault), MAX_UINT_256);
        cvxCrvToken.approve(address(cvxCrvHelperVault), MAX_UINT_256);
    }

    function _deposit(uint256 _want) internal override {
        // Deposit all want in core staking pool
        booster.deposit(pid, _want, true);
    }

    /// @dev Unroll from all strategy positions, and transfer non-core tokens to controller rewards
    function _withdrawAll() internal override {
        baseRewardsPool.withdrawAndUnwrap(balanceOfPool(), false);
        // Note: All want is automatically withdrawn outside this "inner hook" in base strategy function
    }

    /// @dev Withdraw want from staking rewards, using earnings first
    function _withdrawSome(uint256 _amount)
        internal
        override
        returns (uint256)
    {
        // Get idle want in the strategy
        uint256 _preWant = IERC20Upgradeable(want).balanceOf(address(this));

        // If we lack sufficient idle want, withdraw the difference from the strategy position
        if (_preWant < _amount) {
            uint256 _toWithdraw = _amount.sub(_preWant);
            baseRewardsPool.withdrawAndUnwrap(_toWithdraw, false);
        }

        // Confirm how much want we actually end up with
        uint256 _postWant = IERC20Upgradeable(want).balanceOf(address(this));

        // Return the actual amount withdrawn if less than requested
        uint256 _withdrawn = MathUpgradeable.min(_postWant, _amount);
        emit WithdrawState(_amount, _preWant, _postWant, _withdrawn);

        return _withdrawn;
    }

    function balanceOfPool() public view override returns (uint256) {
        return baseRewardsPool.balanceOf(address(this));
    }

    function getProtectedTokens()
        public
        view
        override
        returns (address[] memory)
    {
        address[] memory protectedTokens = new address[](4);
        protectedTokens[0] = want;
        protectedTokens[1] = crv;
        protectedTokens[2] = cvx;
        protectedTokens[3] = cvxCrv;
        return protectedTokens;
    }

    function _tendGainsFromPositions() internal {
        // Harvest CRV, CVX, cvxCRV, 3CRV, and extra rewards tokens from staking positions
        // Note: Always claim extras
        baseRewardsPool.getReward(address(this), true);

        if (cvxCrvRewardsPool.earned(address(this)) > 0) {
            cvxCrvRewardsPool.getReward(address(this), true);
        }

        if (cvxRewardsPool.earned(address(this)) > 0) {
            cvxRewardsPool.getReward(false);
        }
    }

    /// @notice The more frequent the tend, the higher returns will be
    function tend() external whenNotPaused returns (TendData memory) {
        _onlyAuthorizedActors();

        TendData memory tendData;

        // 1. Harvest gains from positions
        _tendGainsFromPositions();

        // Track harvested coins, before conversion
        tendData.crvTended = crvToken.balanceOf(address(this));

        // 2. Convert CRV -> cvxCRV
        if (tendData.crvTended > 0) {
            _swapExactTokensForTokens(
                sushiswap,
                crv,
                tendData.crvTended,
                getTokenSwapPath(crv, cvxCrv)
            );
        }

        // Track harvested + converted coins
        tendData.cvxCrvTended = cvxCrvToken.balanceOf(address(this));
        tendData.cvxTended = cvxToken.balanceOf(address(this));

        // 3. Stake all cvxCRV
        if (tendData.cvxCrvTended > 0) {
            cvxCrvRewardsPool.stake(tendData.cvxCrvTended);
        }

        // 4. Stake all CVX
        if (tendData.cvxTended > 0) {
            cvxRewardsPool.stake(cvxToken.balanceOf(address(this)));
        }

        emit Tend(0);
        emit TendState(
            tendData.crvTended,
            tendData.cvxTended,
            tendData.cvxCrvTended
        );
        return tendData;
    }

    function harvest() external {
        HarvestData memory harvestData;

        uint256 totalWantBefore = balanceOf();

        // 1. grab rewards
        baseRewardsPool.getReward(address(this), true);
        cvxCrvRewardsPool.withdraw(
            cvxCrvRewardsPool.balanceOf(address(this)),
            true
        );
        cvxRewardsPool.withdraw(cvxRewardsPool.balanceOf(address(this)), true);

        harvestData.cvxCrvHarvested = cvxCrvToken.balanceOf(address(this));
        harvestData.cvxHarvested = cvxToken.balanceOf(address(this));

        // 2. convert 3CRV to USDC and USDC to cvxCRV, only if amount is above treshold due to the tx costs
        uint256 threeCrvBalance = threeCrvToken.balanceOf(address(this));
        if (threeCrvBalance > thresholdThreeCrv) {
            _remove_liquidity_one_coin(threeCrvSwap, threeCrvBalance, 1, 0);
            _swapExactTokensForTokens(
                sushiswap,
                usdc,
                usdcToken.balanceOf(address(this)),
                getTokenSwapPath(usdc, cvxCrv)
            );
            // note: here we get a bit extra of cvxCrv perhaps worthy to update `harvestData.cvxCrvHarvested`
            harvestData.cvxCrvHarvested = cvxCrvToken.balanceOf(address(this));
        }

        // 3. Sell 20% of partner tokens for wbtc
        if (harvestData.cvxCrvHarvested > 0) {
            uint256 cvxCrvToSell = harvestData
                .cvxCrvHarvested
                .mul(autoCompoundingBps)
                .div(MAX_FEE);
            _swapExactTokensForTokens(
                sushiswap,
                cvxCrv,
                cvxCrvToSell,
                getTokenSwapPath(cvxCrv, wbtc)
            );
        }

        if (harvestData.cvxHarvested > 0) {
            uint256 cvxToSell = harvestData
                .cvxHarvested
                .mul(autoCompoundingBps)
                .div(MAX_FEE);
            _swapExactTokensForTokens(
                sushiswap,
                cvx,
                cvxToSell,
                getTokenSwapPath(cvx, wbtc)
            );
        }

        // 4. check value of wbtc and divide between yield distributor and autocompound
        uint256 wbtcBalance = wbtcToken.balanceOf(address(this));

        if (wbtcBalance > 0) {
            // 4.1 find out amount to be sent to yield-distributor and accumulate
            uint256 wbtcToYieldDistr = _calcibBTCPortion(
                harvestData.cvxCrvHarvested,
                harvestData.cvxHarvested
            );
            wbtcTokenYieldAccum = wbtcTokenYieldAccum.add(wbtcToYieldDistr);
            // 4.2 the rest is autocompounded
            uint256 wbtcToCompound = wbtcBalance.sub(wbtcToYieldDistr);
            _add_liquidity_single_coin(
                curvePool.swap,
                want,
                wbtc,
                wbtcToCompound,
                curvePool.wbtcPosition,
                curvePool.numElements,
                0
            );
            uint256 wantToDeposited = IERC20Upgradeable(want).balanceOf(
                address(this)
            );
            if (wantToDeposited > 0) {
                _deposit(wantToDeposited);
            }
        }

        // 5. Split the rest of partner tokens between the tree for depositors and DAO, DAO will accum and call at agreed freq or whenever needed
        if (harvestData.cvxCrvHarvested > 0) {
            // 5.1 accum for cvxCrvToGovernanceAccum
            if (performanceFeeGovernance > 0) {
                uint256 cvxCrvToGovernance = harvestData
                    .cvxCrvHarvested
                    .mul(performanceFeeGovernance)
                    .div(MAX_FEE);
                cvxCrvToGovernanceAccum = cvxCrvToGovernanceAccum.add(
                    cvxCrvToGovernance
                );
            }

            // 5.2 depositFor tree at cvxCrvHelperVault
            uint256 treeHelperVaultBefore = cvxCrvHelperVault.balanceOf(
                badgerTree
            );

            uint256 cvxCrvToTree = harvestData.cvxCrvHarvested.mul(treeBps).div(
                MAX_FEE
            );

            cvxCrvHelperVault.depositFor(badgerTree, cvxCrvToTree);

            uint256 treeHelperVaultAfter = cvxCrvHelperVault.balanceOf(
                badgerTree
            );
            uint256 treeVaultPositionGained = treeHelperVaultAfter.sub(
                treeHelperVaultBefore
            );

            emit TreeDistribution(
                address(cvxCrvHelperVault),
                treeVaultPositionGained,
                block.number,
                block.timestamp
            );
        }

        if (harvestData.cvxHarvested > 0) {
            // 5.1 accum for cvxToGovernanceAccum
            if (performanceFeeGovernance > 0) {
                uint256 cvxToGovernance = harvestData
                    .cvxHarvested
                    .mul(performanceFeeGovernance)
                    .div(MAX_FEE);
                cvxToGovernanceAccum = cvxToGovernanceAccum.add(
                    cvxToGovernance
                );
            }

            // 5.2 depositFor tree at cvxHelperVault
            uint256 treeHelperVaultBefore = cvxHelperVault.balanceOf(
                badgerTree
            );

            uint256 cvxToTree = harvestData.cvxHarvested.mul(treeBps).div(
                MAX_FEE
            );

            cvxHelperVault.depositFor(badgerTree, cvxToTree);

            uint256 treeHelperVaultAfter = cvxHelperVault.balanceOf(badgerTree);
            uint256 treeVaultPositionGained = treeHelperVaultAfter.sub(
                treeHelperVaultBefore
            );

            emit TreeDistribution(
                address(cvxHelperVault),
                treeVaultPositionGained,
                block.number,
                block.timestamp
            );
        }

        uint256 totalWantAfter = balanceOf();
        require(
            totalWantAfter >= totalWantBefore,
            "harvest-total-want-must-not-decrease"
        );

        emit HarvestCustom(harvestData.cvxCrvHarvested, harvestData.cvxHarvested, block.number);
    }

    function _calcibBTCPortion(uint256 _cvxCrvAmount, uint256 _cvxAmount)
        internal
        returns (uint256)
    {
        uint256 totalWbtc = 0;
        // this approach may not be the most "secure" perhaps, but only use for estimation of portion
        uint256 ibBTCHarvestShareBps = _getibBTCHarvestShare();

        uint256 cvxToWbtc = _partnerTokenibBTCPortion(
            _cvxAmount,
            ibBTCHarvestShareBps
        );
        uint256 cvxCrvToWbtc = _partnerTokenibBTCPortion(
            _cvxCrvAmount,
            ibBTCHarvestShareBps
        );

        // get wbtc rates
        uint256[] memory minOuts = IUniswapRouterV2(sushiswap).getAmountsOut(
            cvxCrvToWbtc,
            getTokenSwapPath(cvxCrv, wbtc)
        );
        // 3rd index is the wbtc amount estimation
        totalWbtc = totalWbtc.add(minOuts[WBTC_INDEX_OUTPUT]);

        minOuts = IUniswapRouterV2(sushiswap).getAmountsOut(
            cvxToWbtc,
            getTokenSwapPath(cvx, wbtc)
        );
        // it has one index less than cvxCrv -> wbtc
        totalWbtc = totalWbtc.add(minOuts[WBTC_INDEX_OUTPUT - 1]);

        return totalWbtc;
    }

    function _partnerTokenibBTCPortion(
        uint256 _tokenAmount,
        uint256 _ibBTCHarvestShareBps
    ) internal returns (uint256) {
        return
            _tokenAmount
                .mul(MAX_FEE.sub(autoCompoundingBps))
                .div(MAX_FEE)
                .mul(ibBTCRetentionBps)
                .div(MAX_FEE)
                .mul(_ibBTCHarvestShareBps)
                .div(MAX_FEE);
    }

    function _getibBTCHarvestShare() internal returns (uint256) {
        uint256 peakShare = IERC20Upgradeable(bTokenAddress).balanceOf(
            badgerSettPeak
        );
        uint256 totalSupply = IERC20Upgradeable(bTokenAddress).totalSupply();

        return
            peakShare.mul(1 ether).div(totalSupply).mul(MAX_FEE).div(1 ether);
    }

    function transferWbtcTokenYield() external {
        uint256 _fee = wbtcTokenYieldAccum;
        require(_fee > 0, "NO_ACCUM");
        wbtcTokenYieldAccum = 0;
        wbtcToken.transfer(yieldDistributor, _fee);
        emit DistributeWbtcYield(_fee, block.number);
    }

    function collectPerformanceFees() external {
        uint256 _fee = cvxCrvToGovernanceAccum;
        require(_fee > 0, "NO_ACCUM_CVXCRV");
        cvxCrvToGovernanceAccum = 0;
        cvxCrvHelperVault.depositFor(IController(controller).rewards(), _fee);

        emit PerformanceFeeGovernance(
            IController(controller).rewards(),
            cvxCrv,
            _fee,
            block.number,
            block.timestamp
        );

        _fee = cvxToGovernanceAccum;
        require(_fee > 0, "NO_ACCUM_CVX");
        cvxToGovernanceAccum = 0;
        cvxHelperVault.depositFor(IController(controller).rewards(), _fee);

        emit PerformanceFeeGovernance(
            IController(controller).rewards(),
            cvx,
            _fee,
            block.number,
            block.timestamp
        );
    }

    /// ===== Permissioned Actions: Governance =====
    function setibBTCRetentionBps(uint256 _ibBTCRetentionBps) external {
        _onlyGovernance();
        require(
            ibBTCRetentionBps <= MAX_FEE,
            "excessive-governance-ibBTC-retention-bps"
        );
        ibBTCRetentionBps = _ibBTCRetentionBps;
    }

    function setAutoCompoundingBps(uint256 _bps) external {
        _onlyGovernance();
        autoCompoundingBps = _bps;
    }

    function setTreeBps(uint256 _treeBps) external {
        _onlyGovernance();
        treeBps = _treeBps;
    }

    function setPid(uint256 _pid) external {
        _onlyGovernance();
        pid = _pid; // LP token pool ID
    }
}
