// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.8.0;

interface IDevProxyAdmin {
    function upgrade(address, address) external;
}
