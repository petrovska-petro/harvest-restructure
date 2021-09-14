// SPDX-License-Identifier: MIT

pragma solidity ^0.6.11;

import "@openzeppelin-upgradeable/contracts/token/ERC20/IERC20Upgradeable.sol";
import "@openzeppelin-upgradeable/contracts/math/SafeMathUpgradeable.sol";
import "@openzeppelin-upgradeable/contracts/utils/AddressUpgradeable.sol";
import "@openzeppelin-upgradeable/contracts/utils/PausableUpgradeable.sol";
import "@openzeppelin-upgradeable/contracts/token/ERC20/SafeERC20Upgradeable.sol";
import "interfaces/curve/ICurveFi.sol";

/*
    Expands swapping functionality over base strategy
    - ETH in and ETH out Variants
    - Sushiswap support in addition to Uniswap
*/
contract TokenSwapPathRegistry {
    mapping(address => mapping(address => address[])) public tokenSwapPaths;

    event TokenSwapPathSet(address tokenIn, address tokenOut, address[] path);

    function getTokenSwapPath(address tokenIn, address tokenOut) public view returns (address[] memory) {
        return tokenSwapPaths[tokenIn][tokenOut];
    }

    function _setTokenSwapPath(
        address tokenIn,
        address tokenOut,
        address[] memory path
    ) internal {
        tokenSwapPaths[tokenIn][tokenOut] = path;
        emit TokenSwapPathSet(tokenIn, tokenOut, path);
    }
}