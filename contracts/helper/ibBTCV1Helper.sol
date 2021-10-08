// SPDX-License-Identifier: MIT
pragma solidity ^0.6.11;

import "@openzeppelin-upgradeable/contracts/math/SafeMathUpgradeable.sol";
import "@openzeppelin-upgradeable/contracts/math/MathUpgradeable.sol";
import "@openzeppelin-upgradeable/contracts/token/ERC20/IERC20Upgradeable.sol";

import "../deps/CurveSwapper.sol";
import "../deps/UniswapSwapper.sol";

import "interfaces/badger/IStrategy.sol";

// Contains some math for ibBTC harvest restructuring due to EIP-170
contract ibBTCV1Helper is CurveSwapper, UniswapSwapper {
    using SafeMathUpgradeable for uint256;

    // ===== Token Registry for helper =====
    address public constant crv = 0xD533a949740bb3306d119CC777fa900bA034cd52;
    address public constant cvxCrv = 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7;

    // ===== Constant during this helper logic =====
    uint256 public constant MAX_FEE = 10000;
    uint256 public constant WBTC_INDEX_OUTPUT = 2;

    /**
     * @dev Calculates the amount of wbtc to deduct from the amount acquired from selling 20% of the partner tokens, accum in `wbtcTokenYieldAccum`
     * @param _cvxCrvAmount harvested amount of CVXCRV on this round of harvest
     * @param _cvxAmount harvested amount of CVX on this round of harvest
     **/
    function calcibBTCPortion(
        uint256 _cvxCrvAmount,
        uint256 _cvxAmount,
        uint256 _maxWbtc,
        address _strategy,
        address[] calldata _pathCrvWbtc,
        address[] calldata _pathCvxWbtc,
        uint256 _metaPoolIndex
    ) public returns (uint256 totalWbtc) {
        uint256 ibBTCHarvestShareBps = _getibBTCHarvestShare(_strategy);

        uint256 cvxToWbtc = _partnerTokenibBTCPortion(
            _cvxAmount,
            ibBTCHarvestShareBps,
            _strategy
        );
        uint256 cvxCrvToWbtc = _partnerTokenibBTCPortion(
            _cvxCrvAmount,
            ibBTCHarvestShareBps,
            _strategy
        );

        // get wbtc rates
        uint256[] memory minOuts = IUniswapRouterV2(sushiswap).getAmountsOut(
            _getDy(cvxCrv, crv, _metaPoolIndex, cvxCrvToWbtc),
            _pathCrvWbtc
        );

        // 3rd index is the wbtc amount estimation
        totalWbtc = totalWbtc.add(minOuts[WBTC_INDEX_OUTPUT]);
        minOuts = IUniswapRouterV2(sushiswap).getAmountsOut(
            cvxToWbtc,
            _pathCvxWbtc
        );

        // it has one index less than cvxCrv -> wbtc
        totalWbtc = totalWbtc.add(minOuts[WBTC_INDEX_OUTPUT]);

        //totalWbtc = MathUpgradeable.min(_maxWbtc, totalWbtc);
    }

    /// @dev Calculates the % of harvest share comparing what is on the peak and the total supply of its appropiate bToken
    function _getibBTCHarvestShare(address _strategy)
        internal
        returns (uint256)
    {
        uint256 peakShare = IERC20Upgradeable(
            IStrategy(_strategy).bTokenAddress()
        ).balanceOf(IStrategy(_strategy).badgerSettPeak());

        uint256 totalSupply = IERC20Upgradeable(
            IStrategy(_strategy).bTokenAddress()
        ).totalSupply();

        return peakShare.mul(MAX_FEE).div(totalSupply);
    }

    /// @dev Calculates the amount of partnet token, which will be used to be converted for WBTC
    function _partnerTokenibBTCPortion(
        uint256 _tokenAmount,
        uint256 _ibBTCHarvestShareBps,
        address _strategy
    ) internal returns (uint256) {
        return
            _tokenAmount
                .mul(MAX_FEE.sub(IStrategy(_strategy).autoCompoundingBps()))
                .div(MAX_FEE)
                .mul(_ibBTCHarvestShareBps)
                .div(MAX_FEE)
                .mul(IStrategy(_strategy).ibBTCRetentionBps())
                .div(MAX_FEE);
    }
}
