// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.8.0;

interface IibBTCV1Helper {
    function calcibBTCPortion(
        uint256 _cvxCrvAmount,
        uint256 _cvxAmount,
        uint256 _maxWbtc,
        address _strategy,
        address[] calldata _pathCrvWbtc,
        address[] calldata _pathCvxWbtc,
        uint256 _metaPoolIndex
    ) external returns (uint256);
}
