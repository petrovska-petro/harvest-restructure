//  SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

interface ICurveRegistryAddressProvider {
    function get_address(uint256 id) external view returns (address);
}
