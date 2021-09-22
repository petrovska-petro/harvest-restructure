# Harvest ibBTC restructure

On each harvest: 

- DAO gets 20% of tokens (perf fee)
- 20% of tokens sold for WBTC
- ibbtc contract gets the smaller of 20% of the total harvest or 60% of the value of the tokens going to ibBTC redeposited as BTC yield (tokens sold)
- everything else distributed to vault depositors as normal

Gas profilling:

```
HarvestRestructure <Contract>
   ├─ constructor           -  avg: 5395404  avg (confirmed): 5395404  low: 5395404  high: 5395404
   ├─ harvest               -  avg: 1561230  avg (confirmed): 1561230  low: 1527720  high: 1594740
   ├─ initiliazed           -  avg:  875540  avg (confirmed):  875540  low:  875540  high:  875540
   └─ tend                  -  avg:  368742  avg (confirmed):  368742  low:  315186  high:  422298
ISettV4 <Contract>
   └─ approveContractAccess -  avg:   46281  avg (confirmed):   46281  low:   46281  high:   46281
```

Looking at some of the current ones which could use this harvest restructure are hovering around 1.8m of gas used. Then, say after 10 harvest executed at 63.88gwei using the new structure could represent savings on ETH burning rates:

- 10 * 1800000 * 0.000000063882838667 = 1.149 ETH (OLD)
- 10 * 1527720 * 0.000000063882838667 = 0.975 ETH (no 3crv swap)
- 10 * 1594740 * 0.000000063882838667 = 1.018 ETH (with 3crv swap)

At current ETH=3600USD, will represent in 10 harvest a saving of $626 on avg gas profilling and $471 while swapping thru 3CRV for all of the 10 harversts.

Harvest trace sample:

```
Initial call cost  [-410336 gas]
HarvestRestructure.harvest  0:93713  [120388 / 1444142 gas]
├── BaseStrategy.balanceOf  79:629  [69 / 7923 gas]
│   ├── HarvestRestructure.balanceOfPool  85:311  [1876 / 3786 gas]
│   │   │   
│   │   └── BaseRewardPool.balanceOf  [STATICCALL]  150:255  [1910 gas]
│   │           ├── address: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│   │           ├── input arguments:
│   │           │   └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           └── return value: 0
│   │           
│   ├── BaseStrategy.balanceOfWant  315:601  [1873 / 4009 gas]
│   │   │   
│   │   └── Vyper_contract.balanceOf  [STATICCALL]  380:545  [2136 gas]
│   │           ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│   │           ├── input arguments:
│   │           │   └── arg0: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           └── return value: 0
│   │           
│   └── SafeMathUpgradeable.add  605:623  [59 gas]
│   
├── BaseRewardPool.getReward  [CALL]  704:1816  [13336 / 31309 gas]
│   │   ├── address: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│   │   ├── value: 0
│   │   ├── input arguments:
│   │   │   ├── _account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │   │   └── _claimExtras: True
│   │   └── return value: True
│   │   
│   ├── BaseRewardPool.totalSupply  786:792  [816 gas]
│   ├── BaseRewardPool.totalSupply  801:807  [816 gas]
│   ├── BaseRewardPool.lastTimeRewardApplicable  819:846  [840 / 888 gas]
│   │   └── MathUtil.min  827:841  [48 gas]
│   ├── SafeMath.sub  850:869  [60 gas]
│   ├── SafeMath.mul  873:900  [100 gas]
│   ├── SafeMath.mul  904:931  [100 gas]
│   ├── SafeMath.div  935:956  [75 gas]
│   ├── SafeMath.add  962:980  [59 gas]
│   ├── MathUtil.min  999:1013  [48 gas]
│   ├── BaseRewardPool.rewardPerToken  1078:1258  [2581 / 5405 gas]
│   │   ├── BaseRewardPool.totalSupply  1083:1089  [816 gas]
│   │   ├── BaseRewardPool.totalSupply  1098:1104  [816 gas]
│   │   ├── BaseRewardPool.lastTimeRewardApplicable  1116:1143  [840 / 888 gas]
│   │   │   └── MathUtil.min  1124:1138  [48 gas]
│   │   ├── SafeMath.sub  1147:1166  [60 gas]
│   │   ├── SafeMath.mul  1170:1185  [55 gas]
│   │   ├── SafeMath.mul  1189:1204  [55 gas]
│   │   ├── SafeMath.div  1208:1229  [75 gas]
│   │   └── SafeMath.add  1235:1253  [59 gas]
│   ├── SafeMath.sub  1262:1281  [60 gas]
│   ├── BaseRewardPool.balanceOf  1286:1306  [899 gas]
│   ├── SafeMath.mul  1310:1325  [55 gas]
│   ├── SafeMath.div  1329:1350  [75 gas]
│   ├── SafeMath.add  1354:1372  [59 gas]
│   └── BaseRewardPool.earned  1421:1766  [1905 / 8458 gas]
│       ├── BaseRewardPool.rewardPerToken  1464:1644  [2581 / 5405 gas]
│       │   ├── BaseRewardPool.totalSupply  1469:1475  [816 gas]
│       │   ├── BaseRewardPool.totalSupply  1484:1490  [816 gas]
│       │   ├── BaseRewardPool.lastTimeRewardApplicable  1502:1529  [840 / 888 gas]
│       │   │   └── MathUtil.min  1510:1524  [48 gas]
│       │   ├── SafeMath.sub  1533:1552  [60 gas]
│       │   ├── SafeMath.mul  1556:1571  [55 gas]
│       │   ├── SafeMath.mul  1575:1590  [55 gas]
│       │   ├── SafeMath.div  1594:1615  [75 gas]
│       │   └── SafeMath.add  1621:1639  [59 gas]
│       ├── SafeMath.sub  1648:1667  [60 gas]
│       ├── BaseRewardPool.balanceOf  1672:1692  [899 gas]
│       ├── SafeMath.mul  1696:1711  [55 gas]
│       ├── SafeMath.div  1715:1736  [75 gas]
│       └── SafeMath.add  1740:1758  [59 gas]
├── BaseRewardPool.balanceOf  [STATICCALL]  1945:2050  [1910 gas]
│       ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       ├── input arguments:
│       │   └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       └── return value: 4608435068897912156758
│       
├── BaseRewardPool.withdraw  [CALL]  2154:10699  [32916 / 245809 gas]
│   │   ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── amount: 4608435068897912156758
│   │       └── claim: True
│   │   
│   ├── BaseRewardPool.totalSupply  2230:2236  [816 gas]
│   ├── BaseRewardPool.totalSupply  2245:2251  [816 gas]
│   ├── BaseRewardPool.lastTimeRewardApplicable  2263:2290  [840 / 888 gas]
│   │   └── MathUtil.min  2271:2285  [48 gas]
│   ├── SafeMath.sub  2294:2313  [60 gas]
│   ├── SafeMath.mul  2317:2344  [100 gas]
│   ├── SafeMath.mul  2348:2375  [100 gas]
│   ├── SafeMath.div  2379:2400  [75 gas]
│   ├── SafeMath.add  2406:2424  [59 gas]
│   ├── MathUtil.min  2443:2457  [48 gas]
│   ├── BaseRewardPool.rewardPerToken  2522:2702  [2581 / 5405 gas]
│   │   ├── BaseRewardPool.totalSupply  2527:2533  [816 gas]
│   │   ├── BaseRewardPool.totalSupply  2542:2548  [816 gas]
│   │   ├── BaseRewardPool.lastTimeRewardApplicable  2560:2587  [840 / 888 gas]
│   │   │   └── MathUtil.min  2568:2582  [48 gas]
│   │   ├── SafeMath.sub  2591:2610  [60 gas]
│   │   ├── SafeMath.mul  2614:2629  [55 gas]
│   │   ├── SafeMath.mul  2633:2648  [55 gas]
│   │   ├── SafeMath.div  2652:2673  [75 gas]
│   │   └── SafeMath.add  2679:2697  [59 gas]
│   ├── SafeMath.sub  2706:2725  [60 gas]
│   ├── BaseRewardPool.balanceOf  2730:2750  [899 gas]
│   ├── SafeMath.mul  2754:2781  [100 gas]
│   ├── SafeMath.div  2785:2806  [75 gas]
│   ├── SafeMath.add  2810:2828  [59 gas]
│   │   
│   ├── VirtualBalanceRewardPool.withdraw  [CALL]  2960:4476  [29697 / 52805 gas]
│   │   │   ├── address: 0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA
│   │   │   ├── value: 0
│   │   │   └── input arguments:
│   │   │       ├── _account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │   │       └── amount: 4608435068897912156758
│   │   │   
│   │   ├── VirtualBalanceWrapper.totalSupply  3047:3200  [1756 / 3523 gas]
│   │   │   │   
│   │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  3101:3173  [1767 gas]
│   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│   │   │           ├── input arguments: None
│   │   │           └── return value: 77566137274889979669119503
│   │   │           
│   │   ├── VirtualBalanceWrapper.totalSupply  3209:3362  [1750 / 3517 gas]
│   │   │   │   
│   │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  3263:3335  [1767 gas]
│   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│   │   │           ├── input arguments: None
│   │   │           └── return value: 77566137274889979669119503
│   │   │           
│   │   ├── VirtualBalanceRewardPool.lastTimeRewardApplicable  3374:3401  [840 / 888 gas]
│   │   │   └── MathUtil.min  3382:3396  [48 gas]
│   │   ├── SafeMath.sub  3405:3419  [49 gas]
│   │   ├── SafeMath.mul  3423:3450  [100 gas]
│   │   ├── SafeMath.mul  3454:3481  [100 gas]
│   │   ├── SafeMath.div  3485:3506  [75 gas]
│   │   ├── SafeMath.add  3512:3530  [59 gas]
│   │   ├── MathUtil.min  3549:3563  [48 gas]
│   │   ├── VirtualBalanceRewardPool.rewardPerToken  3628:4097  [2581 / 10796 gas]
│   │   │   ├── VirtualBalanceWrapper.totalSupply  3633:3786  [1750 / 3517 gas]
│   │   │   │   │   
│   │   │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  3687:3759  [1767 gas]
│   │   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│   │   │   │           ├── input arguments: None
│   │   │   │           └── return value: 77566137274889979669119503
│   │   │   │           
│   │   │   ├── VirtualBalanceWrapper.totalSupply  3795:3948  [1750 / 3517 gas]
│   │   │   │   │   
│   │   │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  3849:3921  [1767 gas]
│   │   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│   │   │   │           ├── input arguments: None
│   │   │   │           └── return value: 77566137274889979669119503
│   │   │   │           
│   │   │   ├── VirtualBalanceRewardPool.lastTimeRewardApplicable  3960:3987  [840 / 888 gas]
│   │   │   │   └── MathUtil.min  3968:3982  [48 gas]
│   │   │   ├── SafeMath.sub  3991:4005  [49 gas]
│   │   │   ├── SafeMath.mul  4009:4024  [55 gas]
│   │   │   ├── SafeMath.mul  4028:4043  [55 gas]
│   │   │   ├── SafeMath.div  4047:4068  [75 gas]
│   │   │   └── SafeMath.add  4074:4092  [59 gas]
│   │   ├── SafeMath.sub  4101:4115  [49 gas]
│   │   ├── VirtualBalanceWrapper.balanceOf  4120:4311  [1760 / 3670 gas]
│   │   │   │   
│   │   │   └── BaseRewardPool.balanceOf  [STATICCALL]  4179:4284  [1910 gas]
│   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│   │   │           ├── input arguments:
│   │   │           │   └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │   │           └── return value: 4608435068897912156758
│   │   │           
│   │   ├── SafeMath.mul  4315:4342  [100 gas]
│   │   ├── SafeMath.div  4346:4367  [75 gas]
│   │   └── SafeMath.add  4371:4389  [59 gas]
│   ├── SafeMath.sub  4511:4530  [60 gas]
│   ├── SafeMath.sub  4550:4569  [60 gas]
│   ├── SafeERC20.safeTransfer  4601:5281  [207 / 17174 gas]
│   │   └── SafeERC20._callOptionalReturn  4663:5276  [224 / 16967 gas]
│   │       └── Address.functionCall  4699:5245  [53 / 16743 gas]
│   │           └── Address.functionCallWithValue  4708:5237  [689 / 16690 gas]
│   │               ├── Address.isContract  4721:4727  [718 gas]
│   │               │   
│   │               ├── ERC20.transfer  [CALL]  4854:5161  [15223 gas]
│   │               │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│   │               │       ├── value: 0
│   │               │       └── input arguments:
│   │               │           ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │               │           └── _value: 4608435068897912156758
│   │               │       
│   │               └── Address._verifyCallResult  5209:5226  [60 gas]
│   ├── BaseRewardPool.getReward  5311:5497  [2602 / 5426 gas]
│   │   ├── BaseRewardPool.totalSupply  5322:5328  [816 gas]
│   │   ├── BaseRewardPool.totalSupply  5337:5343  [816 gas]
│   │   ├── BaseRewardPool.lastTimeRewardApplicable  5355:5382  [840 / 888 gas]
│   │   │   └── MathUtil.min  5363:5377  [48 gas]
│   │   ├── SafeMath.sub  5386:5405  [60 gas]
│   │   ├── SafeMath.mul  5409:5424  [55 gas]
│   │   ├── SafeMath.mul  5428:5443  [55 gas]
│   │   ├── SafeMath.div  5447:5468  [75 gas]
│   │   └── SafeMath.add  5474:5492  [59 gas]
│   ├── MathUtil.min  5511:5525  [48 gas]
│   ├── BaseRewardPool.rewardPerToken  5590:5770  [2581 / 5405 gas]
│   │   ├── BaseRewardPool.totalSupply  5595:5601  [816 gas]
│   │   ├── BaseRewardPool.totalSupply  5610:5616  [816 gas]
│   │   ├── BaseRewardPool.lastTimeRewardApplicable  5628:5655  [840 / 888 gas]
│   │   │   └── MathUtil.min  5636:5650  [48 gas]
│   │   ├── SafeMath.sub  5659:5678  [60 gas]
│   │   ├── SafeMath.mul  5682:5697  [55 gas]
│   │   ├── SafeMath.mul  5701:5716  [55 gas]
│   │   ├── SafeMath.div  5720:5741  [75 gas]
│   │   └── SafeMath.add  5747:5765  [59 gas]
│   ├── SafeMath.sub  5774:5793  [60 gas]
│   ├── BaseRewardPool.balanceOf  5798:5818  [899 gas]
│   ├── SafeMath.mul  5822:5837  [55 gas]
│   ├── SafeMath.div  5841:5862  [75 gas]
│   ├── SafeMath.add  5866:5884  [59 gas]
│   ├── BaseRewardPool.earned  5933:6278  [1905 / 8458 gas]
│   │   ├── BaseRewardPool.rewardPerToken  5976:6156  [2581 / 5405 gas]
│   │   │   ├── BaseRewardPool.totalSupply  5981:5987  [816 gas]
│   │   │   ├── BaseRewardPool.totalSupply  5996:6002  [816 gas]
│   │   │   ├── BaseRewardPool.lastTimeRewardApplicable  6014:6041  [840 / 888 gas]
│   │   │   │   └── MathUtil.min  6022:6036  [48 gas]
│   │   │   ├── SafeMath.sub  6045:6064  [60 gas]
│   │   │   ├── SafeMath.mul  6068:6083  [55 gas]
│   │   │   ├── SafeMath.mul  6087:6102  [55 gas]
│   │   │   ├── SafeMath.div  6106:6127  [75 gas]
│   │   │   └── SafeMath.add  6133:6151  [59 gas]
│   │   ├── SafeMath.sub  6160:6179  [60 gas]
│   │   ├── BaseRewardPool.balanceOf  6184:6204  [899 gas]
│   │   ├── SafeMath.mul  6208:6223  [55 gas]
│   │   ├── SafeMath.div  6227:6248  [75 gas]
│   │   └── SafeMath.add  6252:6270  [59 gas]
│   ├── SafeERC20.safeTransfer  6314:6904  [210 / 16835 gas]
│   │   └── SafeERC20._callOptionalReturn  6376:6899  [224 / 16625 gas]
│   │       └── Address.functionCall  6412:6868  [53 / 16401 gas]
│   │           └── Address.functionCallWithValue  6421:6860  [689 / 16348 gas]
│   │               ├── Address.isContract  6434:6440  [718 gas]
│   │               │   
│   │               ├── ERC20.transfer  [CALL]  6567:6784  [14881 gas]
│   │               │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │               │       ├── value: 0
│   │               │       └── input arguments:
│   │               │           ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │               │           └── _value: 337059847306858
│   │               │       
│   │               └── Address._verifyCallResult  6832:6849  [60 gas]
│   │   
│   ├── Booster.rewardClaimed  [CALL]  6978:7666  [4662 / 25859 gas]
│   │   │   ├── address: 0xF403C135812408BFbE8713b5A23a04b3D48AAE31
│   │   │   ├── value: 0
│   │   │   └── input arguments:
│   │   │       ├── _pid: 0
│   │   │       ├── _address: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │   │       └── _amount: 337059847306858
│   │   │   
│   │   │   
│   │   └── ERC20  [CALL]  7190:7629  [21197 gas]
│   │           ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│   │           ├── value: 0
│   │           └── calldata: 0x40c10f190000000000000000000000009fcc3bc8f0e63c5313c1d7b65eaf394b5be933ae0000000000000000000000000000000000000000000000000001328ddc777e6a
│   │           
│   └── VirtualBalanceRewardPool.getReward  [CALL]  7787:10633  [-1144 / 70055 gas]
│       │   ├── address: 0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA
│       │   ├── value: 0
│       │   └── input arguments:
│       │       └── _account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │   
│       ├── VirtualBalanceWrapper.totalSupply  7880:8033  [1756 / 3523 gas]
│       │   │   
│       │   └── BaseRewardPool.totalSupply  [STATICCALL]  7934:8006  [1767 gas]
│       │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │           ├── input arguments: None
│       │           └── return value: 77561528839821081756962745
│       │           
│       ├── VirtualBalanceWrapper.totalSupply  8042:8195  [1750 / 3517 gas]
│       │   │   
│       │   └── BaseRewardPool.totalSupply  [STATICCALL]  8096:8168  [1767 gas]
│       │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │           ├── input arguments: None
│       │           └── return value: 77561528839821081756962745
│       │           
│       ├── VirtualBalanceRewardPool.lastTimeRewardApplicable  8207:8234  [840 / 888 gas]
│       │   └── MathUtil.min  8215:8229  [48 gas]
│       ├── SafeMath.sub  8238:8252  [49 gas]
│       ├── SafeMath.mul  8256:8271  [55 gas]
│       ├── SafeMath.mul  8275:8290  [55 gas]
│       ├── SafeMath.div  8294:8315  [75 gas]
│       ├── SafeMath.add  8321:8339  [59 gas]
│       ├── MathUtil.min  8358:8372  [48 gas]
│       ├── VirtualBalanceRewardPool.rewardPerToken  8437:8906  [2581 / 10796 gas]
│       │   ├── VirtualBalanceWrapper.totalSupply  8442:8595  [1750 / 3517 gas]
│       │   │   │   
│       │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  8496:8568  [1767 gas]
│       │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │   │           ├── input arguments: None
│       │   │           └── return value: 77561528839821081756962745
│       │   │           
│       │   ├── VirtualBalanceWrapper.totalSupply  8604:8757  [1750 / 3517 gas]
│       │   │   │   
│       │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  8658:8730  [1767 gas]
│       │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │   │           ├── input arguments: None
│       │   │           └── return value: 77561528839821081756962745
│       │   │           
│       │   ├── VirtualBalanceRewardPool.lastTimeRewardApplicable  8769:8796  [840 / 888 gas]
│       │   │   └── MathUtil.min  8777:8791  [48 gas]
│       │   ├── SafeMath.sub  8800:8814  [49 gas]
│       │   ├── SafeMath.mul  8818:8833  [55 gas]
│       │   ├── SafeMath.mul  8837:8852  [55 gas]
│       │   ├── SafeMath.div  8856:8877  [75 gas]
│       │   └── SafeMath.add  8883:8901  [59 gas]
│       ├── SafeMath.sub  8910:8924  [49 gas]
│       ├── VirtualBalanceWrapper.balanceOf  8929:9120  [1760 / 3670 gas]
│       │   │   
│       │   └── BaseRewardPool.balanceOf  [STATICCALL]  8988:9093  [1910 gas]
│       │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │           ├── input arguments:
│       │           │   └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │           └── return value: 0
│       │           
│       ├── SafeMath.mul  9124:9139  [55 gas]
│       ├── SafeMath.div  9143:9164  [75 gas]
│       ├── SafeMath.add  9168:9186  [59 gas]
│       ├── VirtualBalanceRewardPool.earned  9233:10031  [1901 / 16602 gas]
│       │   ├── VirtualBalanceRewardPool.rewardPerToken  9276:9745  [2581 / 10796 gas]
│       │   │   ├── VirtualBalanceWrapper.totalSupply  9281:9434  [1750 / 3517 gas]
│       │   │   │   │   
│       │   │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  9335:9407  [1767 gas]
│       │   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │   │   │           ├── input arguments: None
│       │   │   │           └── return value: 77561528839821081756962745
│       │   │   │           
│       │   │   ├── VirtualBalanceWrapper.totalSupply  9443:9596  [1750 / 3517 gas]
│       │   │   │   │   
│       │   │   │   └── BaseRewardPool.totalSupply  [STATICCALL]  9497:9569  [1767 gas]
│       │   │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │   │   │           ├── input arguments: None
│       │   │   │           └── return value: 77561528839821081756962745
│       │   │   │           
│       │   │   ├── VirtualBalanceRewardPool.lastTimeRewardApplicable  9608:9635  [840 / 888 gas]
│       │   │   │   └── MathUtil.min  9616:9630  [48 gas]
│       │   │   ├── SafeMath.sub  9639:9653  [49 gas]
│       │   │   ├── SafeMath.mul  9657:9672  [55 gas]
│       │   │   ├── SafeMath.mul  9676:9691  [55 gas]
│       │   │   ├── SafeMath.div  9695:9716  [75 gas]
│       │   │   └── SafeMath.add  9722:9740  [59 gas]
│       │   ├── SafeMath.sub  9749:9763  [49 gas]
│       │   ├── VirtualBalanceWrapper.balanceOf  9768:9959  [1757 / 3667 gas]
│       │   │   │   
│       │   │   └── BaseRewardPool.balanceOf  [STATICCALL]  9827:9932  [1910 gas]
│       │   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │   │           ├── input arguments:
│       │   │           │   └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │   │           └── return value: True
│       │   │           
│       │   ├── SafeMath.mul  9963:9978  [55 gas]
│       │   ├── SafeMath.div  9982:10003  [75 gas]
│       │   └── SafeMath.add  10007:10025  [59 gas]
│       └── SafeERC20.safeTransfer  10066:10599  [210 / 31624 gas]
│           └── SafeERC20._callOptionalReturn  10128:10594  [224 / 31414 gas]
│               └── Address.functionCall  10164:10563  [53 / 31190 gas]
│                   └── Address.functionCallWithValue  10173:10555  [689 / 31137 gas]
│                       ├── Address.isContract  10186:10192  [718 gas]
│                       │   
│                       ├── ERC20.transfer  [CALL]  10319:10479  [29670 gas]
│                       │       ├── address: 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490
│                       │       ├── value: 0
│                       │       └── input arguments:
│                       │           ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│                       │           └── _value: 311025616534481
│                       │       
│                       └── Address._verifyCallResult  10527:10544  [60 gas]
├── cvxRewardPool.balanceOf  [STATICCALL]  10828:10947  [1975 gas]
│       ├── address: 0xCF50b810E57Ac33B91dCF525C6ddd9881B139332
│       └── input arguments:
│           └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       
├── cvxRewardPool.withdraw  [CALL]  11051:17203  [58592 / 83919 gas]
│   │   ├── address: 0xCF50b810E57Ac33B91dCF525C6ddd9881B139332
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── _amount: 1200000000000000000000
│   │       └── claim: True
│   │   
│   │   
│   ├── ERC20.transfer  [CALL]  12103:12422  [11069 gas]
│   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│   │       ├── value: 0
│   │       └── input arguments:
│   │           ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           └── _value: 1200000000000000000000
│   │       
│   ├── ERC20.approve  [CALL]  13795:13993  [-10953 gas]
│   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │       ├── value: 0
│   │       └── input arguments:
│   │           ├── _spender: 0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae
│   │           └── _value: 0
│   │       
│   ├── ERC20.allowance  [STATICCALL]  14193:14350  [2140 gas]
│   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │       └── input arguments:
│   │           ├── _owner: 0xCF50b810E57Ac33B91dCF525C6ddd9881B139332
│   │           └── _spender: 0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae
│   │       
│   ├── ERC20.approve  [CALL]  14627:14843  [4968 gas]
│   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │       ├── value: 0
│   │       └── input arguments:
│   │           ├── _spender: 0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae
│   │           └── _value: 189015816565200
│   │       
│   ├── CrvDepositor.deposit  [CALL]  15021:16256  [-8109 / 24390 gas]
│   │   │   ├── address: 0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae
│   │   │   ├── value: 0
│   │   │   └── input arguments:
│   │   │       ├── _amount: 189015816565200
│   │   │       └── _lock: False
│   │   │   
│   │   │   
│   │   ├── ERC20.transferFrom  [CALL]  15389:15665  [1742 gas]
│   │   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │   │       ├── value: 0
│   │   │       └── input arguments:
│   │   │           ├── _from: 0xCF50b810E57Ac33B91dCF525C6ddd9881B139332
│   │   │           ├── _to: 0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae
│   │   │           └── _value: 189015816565200
│   │   │       
│   │   └── ERC20  [CALL]  15985:16232  [30757 gas]
│   │           ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│   │           ├── value: 0
│   │           └── calldata: 0x40c10f19000000000000000000000000cf50b810e57ac33b91dcf525c6ddd9881b1393320000000000000000000000000000000000000000000000000000abe8ac9a71d0
│   │           
│   ├── ERC20.balanceOf  [STATICCALL]  16321:16421  [1890 gas]
│   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│   │       └── input arguments:
│   │           └── _owner: 0xCF50b810E57Ac33B91dCF525C6ddd9881B139332
│   │       
│   └── ERC20.transfer  [CALL]  16715:17022  [-8177 gas]
│           ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│           ├── value: 0
│           └── input arguments:
│               ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│               └── _value: 189015816565200
│           
├── ERC20.balanceOf  [STATICCALL]  17278:17378  [1890 gas]
│       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       └── input arguments:
│           └── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       
├── ERC20.balanceOf  [STATICCALL]  17496:17591  [1868 gas]
│       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       └── input arguments:
│           └── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       
├── ERC20.balanceOf  [STATICCALL]  17703:17863  [2116 gas]
│       ├── address: 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490
│       └── input arguments:
│           └── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       
├── SafeMathUpgradeable.mul  17946:17973  [100 gas]
├── SafeMathUpgradeable.div  17977:17998  [75 gas]
├── TokenSwapPathRegistry.getTokenSwapPath  18030:18210  [4670 gas]
├── UniswapSwapper._swapExactTokensForTokens  18213:18868  [39 / -8785 gas]
│   └── BaseSwapper._safeApproveHelper  18220:18863  [71 / -8824 gas]
│       └── SafeERC20Upgradeable.safeApprove  18233:18855  [326 / -8895 gas]
│           └── SafeERC20Upgradeable._callOptionalReturn  18324:18848  [293 / -9221 gas]
│               └── AddressUpgradeable.functionCall  18360:18797  [53 / -9514 gas]
│                   └── AddressUpgradeable.functionCallWithValue  18369:18789  [693 / -9567 gas]
│                       ├── AddressUpgradeable.isContract  18382:18388  [718 gas]
│                       │   
│                       ├── ERC20.approve  [CALL]  18524:18713  [-11038 gas]
│                       │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│                       │       ├── value: 0
│                       │       └── input arguments:
│                       │           ├── _spender: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│                       │           └── _value: 0
│                       │       
│                       └── AddressUpgradeable._verifyCallResult  18761:18778  [60 gas]
├── SafeERC20Upgradeable.safeApprove  18881:19755  [1395 / 9212 gas]
│   │   
│   ├── ERC20.allowance  [STATICCALL]  18956:19087  [2038 gas]
│   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│   │       └── input arguments:
│   │           ├── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           └── _spender: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│   │       
│   └── SafeERC20Upgradeable._callOptionalReturn  19224:19748  [293 / 5779 gas]
│       └── AddressUpgradeable.functionCall  19260:19697  [53 / 5486 gas]
│           └── AddressUpgradeable.functionCallWithValue  19269:19689  [693 / 5433 gas]
│               ├── AddressUpgradeable.isContract  19282:19288  [718 gas]
│               │   
│               ├── ERC20.approve  [CALL]  19424:19613  [3962 gas]
│               │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│               │       ├── value: 0
│               │       └── input arguments:
│               │           ├── _spender: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│               │           └── _value: 921687051582745744391
│               │       
│               └── AddressUpgradeable._verifyCallResult  19661:19678  [60 gas]
│   
├── UniswapV2Router02.swapExactTokensForTokens  [CALL]  20025:32319  [22700 / 173308 gas]
│   │   ├── address: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── amountIn: 921687051582745744391
│   │       ├── amountOutMin: 0
│   │       ├── path: [
│   │       │           "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7",
│   │       │           "0xD533a949740bb3306d119CC777fa900bA034cd52",
│   │       │           "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
│   │       │           "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
│   │       │       ]
│   │       ├── to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │       └── deadline: 1631795256
│   │   
│   │   
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  20680:20798  [1924 gas]
│   │       ├── address: 0x33F6DDAEa2a8a54062E021873bCaEE006CdF4007
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 5445172637320048038058782
│   │           ├── 5418802034328835722169488
│   │           └── 1631795246
│   │       
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  21468:21586  [1923 gas]
│   │       ├── address: 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 3017848167418673741277
│   │           ├── 3352181227150682152831142
│   │           └── 1631794718
│   │       
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  22257:22375  [1923 gas]
│   │       ├── address: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 681103659303
│   │           ├── 90233101132560367476978
│   │           └── 1631794962
│   │       
│   ├── ERC20.transferFrom  [CALL]  23211:23696  [91 gas]
│   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│   │       ├── value: 0
│   │       └── input arguments:
│   │           ├── _from: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           ├── _to: 0x33F6DDAEa2a8a54062E021873bCaEE006CdF4007
│   │           └── _value: 921687051582745744391
│   │       
│   ├── UniswapV2Pair.swap  [CALL]  24575:26602  [-186 / 42097 gas]
│   │   │   ├── address: 0x33F6DDAEa2a8a54062E021873bCaEE006CdF4007
│   │   │   ├── value: 0
│   │   │   └── input arguments:
│   │   │       ├── amount0Out: 0
│   │   │       ├── amount1Out: 914317414037596453253
│   │   │       ├── to: 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │   │       └── data: 0x
│   │   │   
│   │   ├── UniswapV2Pair.getReserves  24731:24761  [894 gas]
│   │   ├── UniswapV2Pair._safeTransfer  24860:25346  [924 / 15805 gas]
│   │   │   │   
│   │   │   └── ERC20.transfer  [CALL]  25050:25267  [14881 gas]
│   │   │           ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │   │           ├── value: 0
│   │   │           └── input arguments:
│   │   │               ├── _to: 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │   │               └── _value: 914317414037596453253
│   │   │           
│   │   │   
│   │   ├── ERC20.balanceOf  [STATICCALL]  25403:25503  [1890 gas]
│   │   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│   │   │       └── input arguments:
│   │   │           └── _owner: 0x33F6DDAEa2a8a54062E021873bCaEE006CdF4007
│   │   │       
│   │   ├── ERC20.balanceOf  [STATICCALL]  25580:25798  [2330 gas]
│   │   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │   │       └── input arguments:
│   │   │           └── _owner: 0x33F6DDAEa2a8a54062E021873bCaEE006CdF4007
│   │   │       
│   │   ├── SafeMathUniswap.mul  25892:25922  [108 gas]
│   │   ├── SafeMathUniswap.mul  25928:25958  [108 gas]
│   │   ├── SafeMathUniswap.sub  25962:25978  [54 gas]
│   │   ├── SafeMathUniswap.mul  25988:26018  [108 gas]
│   │   ├── SafeMathUniswap.mul  26024:26054  [108 gas]
│   │   ├── SafeMathUniswap.sub  26058:26074  [54 gas]
│   │   ├── SafeMathUniswap.mul  26093:26123  [108 gas]
│   │   ├── SafeMathUniswap.mul  26127:26157  [108 gas]
│   │   ├── SafeMathUniswap.mul  26163:26193  [108 gas]
│   │   └── UniswapV2Pair._update  26208:26539  [20236 / 20500 gas]
│   │       ├── UQ112x112.encode  26297:26310  [44 gas]
│   │       ├── UQ112x112.uqdiv  26320:26347  [88 gas]
│   │       ├── UQ112x112.encode  26376:26389  [44 gas]
│   │       └── UQ112x112.uqdiv  26399:26426  [88 gas]
│   ├── UniswapV2Pair.swap  [CALL]  27375:29468  [-186 / 43122 gas]
│   │   │   ├── address: 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │   │   ├── value: 0
│   │   │   └── input arguments:
│   │   │       ├── amount0Out: 820434590319788275
│   │   │       ├── amount1Out: 0
│   │   │       ├── to: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│   │   │       └── data: 0x
│   │   │   
│   │   ├── UniswapV2Pair.getReserves  27527:27557  [894 gas]
│   │   ├── UniswapV2Pair._safeTransfer  27651:28193  [924 / 16786 gas]
│   │   │   │   
│   │   │   └── WETH9.transfer  [CALL]  27841:28114  [15862 gas]
│   │   │           ├── address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
│   │   │           ├── value: 0
│   │   │           └── input arguments:
│   │   │               ├── dst: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│   │   │               └── wad: 820434590319788275
│   │   │           
│   │   │   
│   │   ├── WETH9.balanceOf  [STATICCALL]  28255:28365  [1934 gas]
│   │   │       ├── address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
│   │   │       └── input arguments:
│   │   │           └── : 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │   │       
│   │   ├── ERC20.balanceOf  [STATICCALL]  28442:28660  [2330 gas]
│   │   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│   │   │       └── input arguments:
│   │   │           └── _owner: 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │   │       
│   │   ├── SafeMathUniswap.mul  28758:28788  [108 gas]
│   │   ├── SafeMathUniswap.mul  28794:28824  [108 gas]
│   │   ├── SafeMathUniswap.sub  28828:28844  [54 gas]
│   │   ├── SafeMathUniswap.mul  28854:28884  [108 gas]
│   │   ├── SafeMathUniswap.mul  28890:28920  [108 gas]
│   │   ├── SafeMathUniswap.sub  28924:28940  [54 gas]
│   │   ├── SafeMathUniswap.mul  28959:28989  [108 gas]
│   │   ├── SafeMathUniswap.mul  28993:29023  [108 gas]
│   │   ├── SafeMathUniswap.mul  29029:29059  [108 gas]
│   │   └── UniswapV2Pair._update  29074:29405  [20236 / 20500 gas]
│   │       ├── UQ112x112.encode  29163:29176  [44 gas]
│   │       ├── UQ112x112.uqdiv  29186:29213  [88 gas]
│   │       ├── UQ112x112.encode  29242:29255  [44 gas]
│   │       └── UQ112x112.uqdiv  29265:29292  [88 gas]
│   └── UniswapV2Pair.swap  [CALL]  30028:32132  [-186 / 59528 gas]
│       │   ├── address: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│       │   ├── value: 0
│       │   └── input arguments:
│       │       ├── amount0Out: 6174225
│       │       ├── amount1Out: 0
│       │       ├── to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │       └── data: 0x
│       │   
│       ├── UniswapV2Pair.getReserves  30180:30210  [894 gas]
│       ├── UniswapV2Pair._safeTransfer  30304:30935  [924 / 33327 gas]
│       │   │   
│       │   └── WBTC.transfer  [CALL]  30494:30856  [2322 / 32403 gas]
│       │       │   ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│       │       │   ├── value: 0
│       │       │   ├── input arguments:
│       │       │   │   ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │       │   │   └── _value: 6174225
│       │       │   └── return value: True
│       │       │   
│       │       └── BasicToken.transfer  30650:30831  [29978 / 30081 gas]
│       │           ├── SafeMath.sub  30702:30716  [49 gas]
│       │           └── SafeMath.add  30752:30768  [54 gas]
│       │   
│       ├── WBTC.balanceOf  [STATICCALL]  30997:31137  [2195 gas]
│       │       ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│       │       ├── input arguments:
│       │       │   └── _owner: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│       │       └── return value: 681097485078
│       │       
│       ├── WETH9.balanceOf  [STATICCALL]  31214:31324  [1934 gas]
│       │       ├── address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
│       │       └── input arguments:
│       │           └── : 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│       │       
│       ├── SafeMathUniswap.mul  31422:31452  [108 gas]
│       ├── SafeMathUniswap.mul  31458:31488  [108 gas]
│       ├── SafeMathUniswap.sub  31492:31508  [54 gas]
│       ├── SafeMathUniswap.mul  31518:31548  [108 gas]
│       ├── SafeMathUniswap.mul  31554:31584  [108 gas]
│       ├── SafeMathUniswap.sub  31588:31604  [54 gas]
│       ├── SafeMathUniswap.mul  31623:31653  [108 gas]
│       ├── SafeMathUniswap.mul  31657:31687  [108 gas]
│       ├── SafeMathUniswap.mul  31693:31723  [108 gas]
│       └── UniswapV2Pair._update  31738:32069  [20236 / 20500 gas]
│           ├── UQ112x112.encode  31827:31840  [44 gas]
│           ├── UQ112x112.uqdiv  31850:31877  [88 gas]
│           ├── UQ112x112.encode  31906:31919  [44 gas]
│           └── UQ112x112.uqdiv  31929:31956  [88 gas]
├── SafeMathUpgradeable.mul  32616:32643  [100 gas]
├── SafeMathUpgradeable.div  32647:32668  [75 gas]
├── TokenSwapPathRegistry.getTokenSwapPath  32700:32857  [3800 gas]
├── UniswapSwapper._swapExactTokensForTokens  32860:33516  [39 / -8787 gas]
│   └── BaseSwapper._safeApproveHelper  32867:33511  [71 / -8826 gas]
│       └── SafeERC20Upgradeable.safeApprove  32880:33503  [322 / -8897 gas]
│           └── SafeERC20Upgradeable._callOptionalReturn  32971:33496  [294 / -9219 gas]
│               └── AddressUpgradeable.functionCall  33007:33445  [53 / -9513 gas]
│                   └── AddressUpgradeable.functionCallWithValue  33016:33437  [693 / -9566 gas]
│                       ├── AddressUpgradeable.isContract  33029:33035  [718 gas]
│                       │   
│                       ├── ERC20.approve  [CALL]  33171:33361  [-11037 gas]
│                       │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│                       │       ├── value: 0
│                       │       └── input arguments:
│                       │           ├── _spender: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│                       │           └── _value: 0
│                       │       
│                       └── AddressUpgradeable._verifyCallResult  33409:33426  [60 gas]
├── SafeERC20Upgradeable.safeApprove  33529:34404  [1395 / 9214 gas]
│   │   
│   ├── ERC20.allowance  [STATICCALL]  33604:33735  [2038 gas]
│   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│   │       └── input arguments:
│   │           ├── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           └── _spender: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│   │       
│   └── SafeERC20Upgradeable._callOptionalReturn  33872:34397  [294 / 5781 gas]
│       └── AddressUpgradeable.functionCall  33908:34346  [53 / 5487 gas]
│           └── AddressUpgradeable.functionCallWithValue  33917:34338  [693 / 5434 gas]
│               ├── AddressUpgradeable.isContract  33930:33936  [718 gas]
│               │   
│               ├── ERC20.approve  [CALL]  34072:34262  [3963 gas]
│               │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│               │       ├── value: 0
│               │       └── input arguments:
│               │           ├── _spender: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│               │           └── _value: 240000022583009769559
│               │       
│               └── AddressUpgradeable._verifyCallResult  34310:34327  [60 gas]
│   
├── UniswapV2Router02.swapExactTokensForTokens  [CALL]  34645:43030  [16295 / 78460 gas]
│   │   ├── address: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── amountIn: 240000022583009769559
│   │       ├── amountOutMin: 0
│   │       ├── path: [
│   │       │           "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",
│   │       │           "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
│   │       │           "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
│   │       │       ]
│   │       ├── to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │       └── deadline: 1631795256
│   │   
│   │   
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  35300:35418  [1923 gas]
│   │       ├── address: 0x05767d9EF41dC40689678fFca0608878fb3dE906
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 2602890977572167124970734
│   │           ├── 10409368253377261769228
│   │           └── 1631795175
│   │       
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  36088:36206  [1923 gas]
│   │       ├── address: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 681097485078
│   │           ├── 90233921567150687265253
│   │           └── 1631795256
│   │       
│   ├── ERC20.transferFrom  [CALL]  37042:37527  [91 gas]
│   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│   │       ├── value: 0
│   │       └── input arguments:
│   │           ├── _from: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │           ├── _to: 0x05767d9EF41dC40689678fFca0608878fb3dE906
│   │           └── _value: 240000022583009769559
│   │       
│   ├── UniswapV2Pair.swap  [CALL]  38406:40376  [-186 / 38460 gas]
│   │   │   ├── address: 0x05767d9EF41dC40689678fFca0608878fb3dE906
│   │   │   ├── value: 0
│   │   │   └── input arguments:
│   │   │       ├── amount0Out: 0
│   │   │       ├── amount1Out: 956830286448758927
│   │   │       ├── to: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│   │   │       └── data: 0x
│   │   │   
│   │   ├── UniswapV2Pair.getReserves  38562:38592  [894 gas]
│   │   ├── UniswapV2Pair._safeTransfer  38691:39233  [924 / 12586 gas]
│   │   │   │   
│   │   │   └── WETH9.transfer  [CALL]  38881:39154  [11662 gas]
│   │   │           ├── address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
│   │   │           ├── value: 0
│   │   │           └── input arguments:
│   │   │               ├── dst: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│   │   │               └── wad: 956830286448758927
│   │   │           
│   │   │   
│   │   ├── ERC20.balanceOf  [STATICCALL]  39290:39385  [1868 gas]
│   │   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│   │   │       └── input arguments:
│   │   │           └── _owner: 0x05767d9EF41dC40689678fFca0608878fb3dE906
│   │   │       
│   │   ├── WETH9.balanceOf  [STATICCALL]  39462:39572  [1934 gas]
│   │   │       ├── address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
│   │   │       └── input arguments:
│   │   │           └── : 0x05767d9EF41dC40689678fFca0608878fb3dE906
│   │   │       
│   │   ├── SafeMathUniswap.mul  39666:39696  [108 gas]
│   │   ├── SafeMathUniswap.mul  39702:39732  [108 gas]
│   │   ├── SafeMathUniswap.sub  39736:39752  [54 gas]
│   │   ├── SafeMathUniswap.mul  39762:39792  [108 gas]
│   │   ├── SafeMathUniswap.mul  39798:39828  [108 gas]
│   │   ├── SafeMathUniswap.sub  39832:39848  [54 gas]
│   │   ├── SafeMathUniswap.mul  39867:39897  [108 gas]
│   │   ├── SafeMathUniswap.mul  39901:39931  [108 gas]
│   │   ├── SafeMathUniswap.mul  39937:39967  [108 gas]
│   │   └── UniswapV2Pair._update  39982:40313  [20236 / 20500 gas]
│   │       ├── UQ112x112.encode  40071:40084  [44 gas]
│   │       ├── UQ112x112.uqdiv  40094:40121  [88 gas]
│   │       ├── UQ112x112.encode  40150:40163  [44 gas]
│   │       └── UQ112x112.uqdiv  40173:40200  [88 gas]
│   └── UniswapV2Pair.swap  [CALL]  40936:42862  [-186 / 19768 gas]
│       │   ├── address: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│       │   ├── value: 0
│       │   └── input arguments:
│       │       ├── amount0Out: 7200537
│       │       ├── amount1Out: 0
│       │       ├── to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │       └── data: 0x
│       │   
│       ├── UniswapV2Pair.getReserves  41088:41118  [894 gas]
│       ├── UniswapV2Pair._safeTransfer  41212:41843  [924 / 9927 gas]
│       │   │   
│       │   └── WBTC.transfer  [CALL]  41402:41764  [2322 / 9003 gas]
│       │       │   ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│       │       │   ├── value: 0
│       │       │   ├── input arguments:
│       │       │   │   ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │       │   │   └── _value: 7200537
│       │       │   └── return value: True
│       │       │   
│       │       └── BasicToken.transfer  41558:41739  [6578 / 6681 gas]
│       │           ├── SafeMath.sub  41610:41624  [49 gas]
│       │           └── SafeMath.add  41660:41676  [54 gas]
│       │   
│       ├── WBTC.balanceOf  [STATICCALL]  41905:42045  [2195 gas]
│       │       ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│       │       ├── input arguments:
│       │       │   └── _owner: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│       │       └── return value: 681090284541
│       │       
│       ├── WETH9.balanceOf  [STATICCALL]  42122:42232  [1934 gas]
│       │       ├── address: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
│       │       └── input arguments:
│       │           └── : 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│       │       
│       ├── SafeMathUniswap.mul  42330:42360  [108 gas]
│       ├── SafeMathUniswap.mul  42366:42396  [108 gas]
│       ├── SafeMathUniswap.sub  42400:42416  [54 gas]
│       ├── SafeMathUniswap.mul  42426:42456  [108 gas]
│       ├── SafeMathUniswap.mul  42462:42492  [108 gas]
│       ├── SafeMathUniswap.sub  42496:42512  [54 gas]
│       ├── SafeMathUniswap.mul  42531:42561  [108 gas]
│       ├── SafeMathUniswap.mul  42565:42595  [108 gas]
│       ├── SafeMathUniswap.mul  42601:42631  [108 gas]
│       └── UniswapV2Pair._update  42646:42799  [4140 gas]
├── WBTC.balanceOf  [STATICCALL]  43335:43475  [2195 gas]
│       ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│       ├── input arguments:
│       │   └── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       └── return value: 13374762
│       
├── HarvestRestructure._calcibBTCPortion  43544:45211  [802 / 24472 gas]
│   ├── HarvestRestructure._getibBTCHarvestShare  43551:44367  [4612 / 14275 gas]
│   │   │   
│   │   ├── AdminUpgradeabilityProxy.balanceOf  [STATICCALL]  43622:43868  [173230 / 4729 gas]
│   │   │   │   ├── address: 0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545
│   │   │   │   ├── input arguments:
│   │   │   │   │   └── account: 0x41671BA1abcbA387b9b2B752c205e22e916BE6e3
│   │   │   │   └── return value: 470159133167934246450
│   │   │   │   
│   │   │   └── Proxy._fallback  43665:43868  [45 / -168501 gas]
│   │   │       ├── AdminUpgradeabilityProxy._willFallback  43669:43706  [73 / 924 gas]
│   │   │       │   ├── AdminUpgradeabilityProxy._admin  43673:43688  [842 gas]
│   │   │       │   └── Proxy._willFallback  43702:43704  [9 gas]
│   │   │       ├── UpgradeabilityProxy._implementation  43711:43726  [842 gas]
│   │   │       └── Proxy._delegate  43729:43868  [-172265 / -170312 gas]
│   │   │           │   
│   │   │           └── SettV1.balanceOf  [DELEGATECALL]  43741:43855  [1054 / 1953 gas]
│   │   │               │   ├── address: 0x5c7AdB3Fd0DF2D1822a36922dd941e16D2bF4E51
│   │   │               │   ├── input arguments:
│   │   │               │   │   └── account: 0x41671BA1abcbA387b9b2B752c205e22e916BE6e3
│   │   │               │   └── return value: 470159133167934246450
│   │   │               │   
│   │   │               └── ERC20Upgradeable.balanceOf  43819:43839  [899 gas]
│   │   ├── AdminUpgradeabilityProxy.totalSupply  [STATICCALL]  43974:44188  [173128 / 4584 gas]
│   │   │   │   ├── address: 0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545
│   │   │   │   ├── input arguments: None
│   │   │   │   └── return value: 3639708149533738794861
│   │   │   │   
│   │   │   └── Proxy._fallback  44017:44188  [45 / -168544 gas]
│   │   │       ├── AdminUpgradeabilityProxy._willFallback  44021:44058  [73 / 924 gas]
│   │   │       │   ├── AdminUpgradeabilityProxy._admin  44025:44040  [842 gas]
│   │   │       │   └── Proxy._willFallback  44054:44056  [9 gas]
│   │   │       ├── UpgradeabilityProxy._implementation  44063:44078  [842 gas]
│   │   │       └── Proxy._delegate  44081:44188  [-172166 / -170355 gas]
│   │   │           │   
│   │   │           └── SettV1.totalSupply  [DELEGATECALL]  44093:44175  [996 / 1811 gas]
│   │   │               │   ├── address: 0x5c7AdB3Fd0DF2D1822a36922dd941e16D2bF4E51
│   │   │               │   ├── input arguments: None
│   │   │               │   └── return value: 3639708149533738794861
│   │   │               │   
│   │   │               └── ERC20Upgradeable.totalSupply  44154:44159  [815 gas]
│   │   ├── SafeMathUpgradeable.mul  44252:44279  [100 gas]
│   │   ├── SafeMathUpgradeable.div  44283:44304  [75 gas]
│   │   ├── SafeMathUpgradeable.mul  44308:44335  [100 gas]
│   │   └── SafeMathUpgradeable.div  44339:44360  [75 gas]
│   ├── HarvestRestructure._partnerTokenibBTCPortion  44376:44591  [1786 / 2360 gas]
│   │   ├── SafeMathUpgradeable.sub  44401:44415  [49 gas]
│   │   ├── SafeMathUpgradeable.mul  44420:44447  [100 gas]
│   │   ├── SafeMathUpgradeable.div  44451:44472  [75 gas]
│   │   ├── SafeMathUpgradeable.mul  44476:44503  [100 gas]
│   │   ├── SafeMathUpgradeable.div  44507:44528  [75 gas]
│   │   ├── SafeMathUpgradeable.mul  44532:44559  [100 gas]
│   │   └── SafeMathUpgradeable.div  44563:44584  [75 gas]
│   ├── HarvestRestructure._partnerTokenibBTCPortion  44600:44815  [1786 / 2360 gas]
│   │   ├── SafeMathUpgradeable.sub  44625:44639  [49 gas]
│   │   ├── SafeMathUpgradeable.mul  44644:44671  [100 gas]
│   │   ├── SafeMathUpgradeable.div  44675:44696  [75 gas]
│   │   ├── SafeMathUpgradeable.mul  44700:44727  [100 gas]
│   │   ├── SafeMathUpgradeable.div  44731:44752  [75 gas]
│   │   ├── SafeMathUpgradeable.mul  44756:44783  [100 gas]
│   │   └── SafeMathUpgradeable.div  44787:44808  [75 gas]
│   └── TokenSwapPathRegistry.getTokenSwapPath  44837:45017  [4675 gas]
│   
├── UniswapV2Router02.getAmountsOut  [STATICCALL]  45231:48004  [11040 / 16810 gas]
│   │   ├── address: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│   │   └── input arguments:
│   │       ├── amountIn: 285575516062397941442
│   │       └── path: [
│   │                   "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7",
│   │                   "0xD533a949740bb3306d119CC777fa900bA034cd52",
│   │                   "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
│   │                   "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
│   │               ]
│   │   
│   │   
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  45841:45959  [1924 gas]
│   │       ├── address: 0x33F6DDAEa2a8a54062E021873bCaEE006CdF4007
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 5446094324371630783803173
│   │           ├── 5417887716914798125716235
│   │           └── 1631795256
│   │       
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  46629:46747  [1923 gas]
│   │       ├── address: 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 3017027732828353953002
│   │           ├── 3353095544564719749284395
│   │           └── 1631795256
│   │       
│   └── UniswapV2Pair.getReserves  [STATICCALL]  47418:47536  [1923 gas]
│           ├── address: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│           ├── input arguments: None
│           └── return values:
│               ├── 681090284541
│               ├── 90234878397437136024180
│               └── 1631795256
│           
├── SafeMathUpgradeable.add  48294:48312  [59 gas]
├── TokenSwapPathRegistry.getTokenSwapPath  48333:48490  [3800 gas]
│   
├── UniswapV2Router02.getAmountsOut  [STATICCALL]  48675:50640  [7976 / 11822 gas]
│   │   ├── address: 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F
│   │   └── input arguments:
│   │       ├── amountIn: 74361606997119747000
│   │       └── path: [
│   │                   "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",
│   │                   "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
│   │                   "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
│   │               ]
│   │   
│   │   
│   ├── UniswapV2Pair.getReserves  [STATICCALL]  49285:49403  [1923 gas]
│   │       ├── address: 0x05767d9EF41dC40689678fFca0608878fb3dE906
│   │       ├── input arguments: None
│   │       └── return values:
│   │           ├── 2603130977594750134740293
│   │           ├── 10408411423090813010301
│   │           └── 1631795256
│   │       
│   └── UniswapV2Pair.getReserves  [STATICCALL]  50073:50191  [1923 gas]
│           ├── address: 0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58
│           ├── input arguments: None
│           └── return values:
│               ├── 681090284541
│               ├── 90234878397437136024180
│               └── 1631795256
│           
├── SafeMathUpgradeable.add  50907:50925  [59 gas]
├── SafeMathUpgradeable.add  50948:50966  [59 gas]
├── SafeMathUpgradeable.sub  50975:50989  [49 gas]
├── CurveSwapper._add_liquidity_single_coin  51023:51647  [39 / -7924 gas]
│   └── BaseSwapper._safeApproveHelper  51030:51642  [71 / -7963 gas]
│       └── SafeERC20Upgradeable.safeApprove  51043:51634  [323 / -8034 gas]
│           └── SafeERC20Upgradeable._callOptionalReturn  51134:51627  [294 / -8357 gas]
│               └── AddressUpgradeable.functionCall  51170:51576  [53 / -8651 gas]
│                   └── AddressUpgradeable.functionCallWithValue  51179:51568  [694 / -8704 gas]
│                       ├── AddressUpgradeable.isContract  51192:51198  [718 gas]
│                       │   
│                       ├── WBTC.approve  [CALL]  51334:51492  [1948 / -10176 gas]
│                       │   │   ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│                       │   │   ├── value: 0
│                       │   │   ├── input arguments:
│                       │   │   │   ├── _spender: 0x93054188d876f558f4a66B2EF1d97d16eDf0895B
│                       │   │   │   └── _value: 0
│                       │   │   └── return value: True
│                       │   │   
│                       │   └── StandardToken.approve  51405:51467  [-12124 gas]
│                       └── AddressUpgradeable._verifyCallResult  51540:51557  [60 gas]
├── SafeERC20Upgradeable.safeApprove  51660:52572  [1396 / 10509 gas]
│   │   
│   ├── WBTC.allowance  [STATICCALL]  51735:51935  [2470 gas]
│   │       ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│   │       ├── input arguments:
│   │       │   ├── _owner: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │       │   └── _spender: 0x93054188d876f558f4a66B2EF1d97d16eDf0895B
│   │       └── return value: 0
│   │       
│   └── SafeERC20Upgradeable._callOptionalReturn  52072:52565  [294 / 6643 gas]
│       └── AddressUpgradeable.functionCall  52108:52514  [53 / 6349 gas]
│           └── AddressUpgradeable.functionCallWithValue  52117:52506  [694 / 6296 gas]
│               ├── AddressUpgradeable.isContract  52130:52136  [718 gas]
│               │   
│               ├── WBTC.approve  [CALL]  52272:52430  [1948 / 4824 gas]
│               │   │   ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│               │   │   ├── value: 0
│               │   │   ├── input arguments:
│               │   │   │   ├── _spender: 0x93054188d876f558f4a66B2EF1d97d16eDf0895B
│               │   │   │   └── _value: 9232196
│               │   │   └── return value: True
│               │   │   
│               │   └── StandardToken.approve  52343:52405  [2876 gas]
│               └── AddressUpgradeable._verifyCallResult  52478:52495  [60 gas]
│   
├── Vyper_contract.add_liquidity  [CALL]  52764:70722  [55703 / 135110 gas]
│   │   ├── address: 0x93054188d876f558f4a66B2EF1d97d16eDf0895B
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── amounts: [0, 9232196]
│   │       └── min_mint_amount: 0
│   │   
│   ├── Vyper_contract._A  52952:52980  [1685 gas]
│   │   
│   ├── Vyper_contract.totalSupply  [STATICCALL]  53025:53078  [1701 gas]
│   │       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│   │       ├── input arguments: None
│   │       └── return value: 10896617294682678602590
│   │       
│   ├── Vyper_contract._rates  53399:53922  [4258 / 9594 gas]
│   │   │   
│   │   └── RenBTC.exchangeRateCurrent  [STATICCALL]  53515:53714  [168411 / 5336 gas]
│   │       │   ├── address: 0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D
│   │       │   ├── input arguments: None
│   │       │   └── return value: 1000000000000000000
│   │       │   
│   │       └── Proxy._fallback  53558:53714  [45 / -163075 gas]
│   │           ├── BaseAdminUpgradeabilityProxy._willFallback  53562:53597  [97 / 921 gas]
│   │           │   ├── BaseAdminUpgradeabilityProxy._admin  53566:53571  [815 gas]
│   │           │   └── Proxy._fallback  53593:53595  [9 gas]
│   │           ├── BaseUpgradeabilityProxy._implementation  53602:53607  [815 gas]
│   │           └── Proxy._delegate  53610:53714  [-167452 / -164856 gas]
│   │               │   
│   │               └── RenERC20LogicV1.exchangeRateCurrent  [DELEGATECALL]  53622:53702  [950 / 2596 gas]
│   │                   │   ├── address: 0xe2d6cCAC3EE3A21AbF7BeDBE2E107FfC0C037e80
│   │                   │   ├── input arguments: None
│   │                   │   └── return value: 1000000000000000000
│   │                   │   
│   │                   └── ERC20WithRate.exchangeRateCurrent  53671:53686  [1646 gas]
│   ├── Vyper_contract.get_D_mem  54774:58225  [6103 / 11591 gas]
│   │   ├── Vyper_contract._xp_mem  55641:55918  [922 gas]
│   │   └── Vyper_contract.get_D  56275:57691  [4566 gas]
│   ├── Vyper_contract.get_D_mem  59593:63044  [6087 / 11575 gas]
│   │   ├── Vyper_contract._xp_mem  60460:60737  [922 gas]
│   │   └── Vyper_contract.get_D  61094:62510  [4566 gas]
│   ├── Vyper_contract.get_D_mem  65362:68813  [6087 / 11575 gas]
│   │   ├── Vyper_contract._xp_mem  66229:66506  [922 gas]
│   │   └── Vyper_contract.get_D  66863:68279  [4566 gas]
│   │   
│   ├── WBTC.transferFrom  [CALL]  70002:70430  [2044 / 1180 gas]
│   │   │   ├── address: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
│   │   │   ├── value: 0
│   │   │   ├── input arguments:
│   │   │   │   ├── _from: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│   │   │   │   ├── _to: 0x93054188d876f558f4a66B2EF1d97d16eDf0895B
│   │   │   │   └── _value: 9232196
│   │   │   └── return value: True
│   │   │   
│   │   └── StandardToken.transferFrom  70094:70404  [-1016 / -864 gas]
│   │       ├── SafeMath.sub  70193:70207  [49 gas]
│   │       ├── SafeMath.add  70246:70262  [54 gas]
│   │       └── SafeMath.sub  70313:70327  [49 gas]
│   └── Vyper_contract.mint  [CALL]  70489:70668  [30506 gas]
│           ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│           ├── value: 0
│           └── input arguments:
│               ├── _to: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│               └── _value: 90698479504637086
│           
├── Vyper_contract.balanceOf  [STATICCALL]  70809:70974  [2136 gas]
│       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       ├── input arguments:
│       │   └── arg0: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       └── return value: 90698479504637086
│       
├── HarvestRestructure._deposit  71035:84683  [1905 / 281192 gas]
│   │   
│   └── Booster.deposit  [CALL]  71102:84622  [19603 / 279287 gas]
│       │   ├── address: 0xF403C135812408BFbE8713b5A23a04b3D48AAE31
│       │   ├── value: 0
│       │   └── input arguments:
│       │       ├── _pid: 6
│       │       ├── _amount: 90698479504637086
│       │       └── _stake: True
│       │   
│       │   
│       ├── Vyper_contract.transferFrom  [CALL]  71548:71767  [17327 gas]
│       │       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │       ├── value: 0
│       │       ├── input arguments:
│       │       │   ├── _from: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │       │   ├── _to: 0x989AEb4d175e16225E39E87d0D97A3360524AD80
│       │       │   └── _value: 90698479504637086
│       │       └── return value: True
│       │       
│       ├── CurveVoterProxy.deposit  [CALL]  71971:80984  [5871 / 190035 gas]
│       │   │   ├── address: 0x989AEb4d175e16225E39E87d0D97A3360524AD80
│       │   │   ├── value: 0
│       │   │   ├── input arguments:
│       │   │   │   ├── _token: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │   │   │   └── _gauge: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │   │   └── return value: True
│       │   │   
│       │   │   
│       │   ├── Vyper_contract.balanceOf  [STATICCALL]  72209:72374  [2136 gas]
│       │   │       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │   │       ├── input arguments:
│       │   │       │   └── arg0: 0x989AEb4d175e16225E39E87d0D97A3360524AD80
│       │   │       └── return value: 90698479504637086
│       │   │       
│       │   ├── SafeERC20.safeApprove  72432:72998  [249 / -8199 gas]
│       │   │   └── SafeERC20._callOptionalReturn  72506:72993  [256 / -8448 gas]
│       │   │       └── Address.functionCall  72538:72946  [56 / -8704 gas]
│       │   │           └── Address.functionCallWithValue  72547:72937  [692 / -8760 gas]
│       │   │               ├── Address.isContract  72560:72577  [747 gas]
│       │   │               │   
│       │   │               ├── Vyper_contract.approve  [CALL]  72706:72859  [-10262 gas]
│       │   │               │       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │   │               │       ├── value: 0
│       │   │               │       ├── input arguments:
│       │   │               │       │   ├── _spender: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │   │               │       │   └── _value: 0
│       │   │               │       └── return value: True
│       │   │               │       
│       │   │               └── Address._verifyCallResult  72907:72925  [63 gas]
│       │   ├── SafeERC20.safeApprove  73013:73772  [1225 / 9703 gas]
│       │   │   │   
│       │   │   ├── Vyper_contract.allowance  [STATICCALL]  73077:73176  [1926 gas]
│       │   │   │       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │   │   │       ├── input arguments:
│       │   │   │       │   ├── _owner: 0x989AEb4d175e16225E39E87d0D97A3360524AD80
│       │   │   │       │   └── _spender: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │   │   │       └── return value: 0
│       │   │   │       
│       │   │   └── SafeERC20._callOptionalReturn  73280:73767  [256 / 6552 gas]
│       │   │       └── Address.functionCall  73312:73720  [56 / 6296 gas]
│       │   │           └── Address.functionCallWithValue  73321:73711  [692 / 6240 gas]
│       │   │               ├── Address.isContract  73334:73351  [747 gas]
│       │   │               │   
│       │   │               ├── Vyper_contract.approve  [CALL]  73480:73633  [4738 gas]
│       │   │               │       ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │   │               │       ├── value: 0
│       │   │               │       ├── input arguments:
│       │   │               │       │   ├── _spender: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │   │               │       │   └── _value: 90698479504637086
│       │   │               │       └── return value: True
│       │   │               │       
│       │   │               └── Address._verifyCallResult  73681:73699  [63 gas]
│       │   │   
│       │   └── Vyper_contract.deposit  [CALL]  73818:80943  [23732 / 180524 gas]
│       │       │   ├── address: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │       │   ├── value: 0
│       │       │   └── input arguments:
│       │       │       └── _value: 90698479504637086
│       │       │   
│       │       ├── Vyper_contract._checkpoint  73934:78742  [73573 / 143981 gas]
│       │       │   │   
│       │       │   ├── ERC20  [CALL]  74020:74133  [1916 gas]
│       │       │   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│       │       │   │       ├── value: 0
│       │       │   │       └── calldata: 0xb26b238e
│       │       │   │       
│       │       │   ├── ERC20  [STATICCALL]  74159:74398  [2378 gas]
│       │       │   │       ├── address: 0xD533a949740bb3306d119CC777fa900bA034cd52
│       │       │   │       └── calldata: 0x2c4e722e
│       │       │   │       
│       │       │   ├── Vyper_contract.checkpoint_gauge  [CALL]  74439:77824  [1298 / 60545 gas]
│       │       │   │   │   ├── address: 0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB
│       │       │   │   │   ├── value: 0
│       │       │   │   │   └── input arguments:
│       │       │   │   │       └── addr: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │       │   │   │   
│       │       │   │   ├── Vyper_contract._get_weight  74571:74669  [2899 gas]
│       │       │   │   └── Vyper_contract._get_total  74687:77810  [22307 / 56348 gas]
│       │       │   │       ├── Vyper_contract._get_sum  74778:74881  [2895 gas]
│       │       │   │       ├── Vyper_contract._get_type_weight  74927:75008  [1968 gas]
│       │       │   │       ├── Vyper_contract._get_sum  75077:75180  [2895 gas]
│       │       │   │       ├── Vyper_contract._get_type_weight  75226:75307  [1968 gas]
│       │       │   │       ├── Vyper_contract._get_sum  75376:75479  [2895 gas]
│       │       │   │       ├── Vyper_contract._get_type_weight  75525:75606  [1968 gas]
│       │       │   │       ├── Vyper_contract._get_sum  75675:75778  [2895 gas]
│       │       │   │       ├── Vyper_contract._get_type_weight  75824:75905  [1968 gas]
│       │       │   │       ├── Vyper_contract._get_sum  75974:76077  [2895 gas]
│       │       │   │       ├── Vyper_contract._get_type_weight  76123:76204  [1968 gas]
│       │       │   │       ├── Vyper_contract._get_sum  76273:76376  [2895 gas]
│       │       │   │       ├── Vyper_contract._get_type_weight  76422:76503  [1968 gas]
│       │       │   │       ├── Vyper_contract._get_sum  76572:76675  [2895 gas]
│       │       │   │       └── Vyper_contract._get_type_weight  76721:76802  [1968 gas]
│       │       │   └── Vyper_contract.gauge_relative_weight  [STATICCALL]  78005:78408  [1390 / 5569 gas]
│       │       │       │   ├── address: 0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB
│       │       │       │   ├── input arguments:
│       │       │       │   │   ├── addr: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │       │       │   │   └── time: 1631750400
│       │       │       │   └── return value: 23202243585747131
│       │       │       │   
│       │       │       └── Vyper_contract._gauge_relative_weight  78175:78396  [4179 gas]
│       │       ├── Vyper_contract._update_liquidity_limit  79077:80426  [16465 / 29684 gas]
│       │       │   │   
│       │       │   ├── Vyper_contract.balanceOf  [STATICCALL]  79105:79486  [6265 gas]
│       │       │   │       ├── address: 0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2
│       │       │   │       ├── input arguments:
│       │       │   │       │   └── addr: 0x989AEb4d175e16225E39E87d0D97A3360524AD80
│       │       │   │       └── return value: 100933364081400210560599056
│       │       │   │       
│       │       │   └── Vyper_contract.totalSupply  [STATICCALL]  79512:80124  [6120 / 6954 gas]
│       │       │       │   ├── address: 0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2
│       │       │       │   ├── input arguments: None
│       │       │       │   └── return value: 279534202707825534301193088
│       │       │       │   
│       │       │       └── Vyper_contract.supply_at  79847:80102  [834 gas]
│       │       │   
│       │       └── Vyper_contract.transferFrom  [CALL]  80693:80912  [-16873 gas]
│       │               ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
│       │               ├── value: 0
│       │               ├── input arguments:
│       │               │   ├── _from: 0x989AEb4d175e16225E39E87d0D97A3360524AD80
│       │               │   ├── _to: 0xB1F2cdeC61db658F091671F5f199635aEF202CAC
│       │               │   └── _value: 90698479504637086
│       │               └── return value: True
│       │               
│       ├── DepositToken.mint  [CALL]  81081:81328  [1884 / 30757 gas]
│       │   │   ├── address: 0x74b79021Ea6De3f0D1731fb8BdfF6eE7DF10b8Ae
│       │   │   ├── value: 0
│       │   │   └── input arguments:
│       │   │       ├── _to: 0xF403C135812408BFbE8713b5A23a04b3D48AAE31
│       │   │       └── _amount: 90698479504637086
│       │   │   
│       │   └── ERC20._mint  81181:81322  [28740 / 28873 gas]
│       │       ├── ERC20._beforeTokenTransfer  81198:81203  [15 gas]
│       │       ├── SafeMath.add  81211:81229  [59 gas]
│       │       └── SafeMath.add  81256:81274  [59 gas]
│       ├── DepositToken.approve  [CALL]  81621:81810  [1004 / -11038 gas]
│       │   │   ├── address: 0x74b79021Ea6De3f0D1731fb8BdfF6eE7DF10b8Ae
│       │   │   ├── value: 0
│       │   │   ├── input arguments:
│       │   │   │   ├── spender: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│       │   │   │   └── amount: 0
│       │   │   └── return value: True
│       │   │   
│       │   └── ERC20.approve  81690:81792  [63 / -12042 gas]
│       │       ├── Context._msgSender  81696:81700  [14 gas]
│       │       └── ERC20._approve  81705:81784  [-12119 gas]
│       ├── DepositToken.allowance  [STATICCALL]  82010:82141  [1052 / 2038 gas]
│       │   │   ├── address: 0x74b79021Ea6De3f0D1731fb8BdfF6eE7DF10b8Ae
│       │   │   ├── input arguments:
│       │   │   │   ├── owner: 0xF403C135812408BFbE8713b5A23a04b3D48AAE31
│       │   │   │   └── spender: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│       │   │   └── return value: 0
│       │   │   
│       │   └── ERC20.allowance  82089:82125  [986 gas]
│       ├── DepositToken.approve  [CALL]  82420:82609  [1004 / 3962 gas]
│       │   │   ├── address: 0x74b79021Ea6De3f0D1731fb8BdfF6eE7DF10b8Ae
│       │   │   ├── value: 0
│       │   │   ├── input arguments:
│       │   │   │   ├── spender: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│       │   │   │   └── amount: 90698479504637086
│       │   │   └── return value: True
│       │   │   
│       │   └── ERC20.approve  82489:82591  [63 / 2958 gas]
│       │       ├── Context._msgSender  82495:82499  [14 gas]
│       │       └── ERC20._approve  82504:82583  [2881 gas]
│       └── BaseRewardPool.stakeFor  [CALL]  82788:84556  [29895 / 26603 gas]
│           │   ├── address: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│           │   ├── value: 0
│           │   ├── input arguments:
│           │   │   ├── _for: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│           │   │   └── _amount: 90698479504637086
│           │   └── return value: True
│           │   
│           ├── BaseRewardPool.totalSupply  82888:82894  [816 gas]
│           ├── BaseRewardPool.totalSupply  82903:82909  [816 gas]
│           ├── BaseRewardPool.lastTimeRewardApplicable  82921:82948  [840 / 888 gas]
│           │   └── MathUtil.min  82929:82943  [48 gas]
│           ├── SafeMath.sub  82952:82971  [60 gas]
│           ├── SafeMath.mul  82975:82990  [55 gas]
│           ├── SafeMath.mul  82994:83009  [55 gas]
│           ├── SafeMath.div  83013:83034  [75 gas]
│           ├── SafeMath.add  83040:83058  [59 gas]
│           ├── MathUtil.min  83077:83091  [48 gas]
│           ├── BaseRewardPool.rewardPerToken  83156:83336  [2581 / 5405 gas]
│           │   ├── BaseRewardPool.totalSupply  83161:83167  [816 gas]
│           │   ├── BaseRewardPool.totalSupply  83176:83182  [816 gas]
│           │   ├── BaseRewardPool.lastTimeRewardApplicable  83194:83221  [840 / 888 gas]
│           │   │   └── MathUtil.min  83202:83216  [48 gas]
│           │   ├── SafeMath.sub  83225:83244  [60 gas]
│           │   ├── SafeMath.mul  83248:83263  [55 gas]
│           │   ├── SafeMath.mul  83267:83282  [55 gas]
│           │   ├── SafeMath.div  83286:83307  [75 gas]
│           │   └── SafeMath.add  83313:83331  [59 gas]
│           ├── SafeMath.sub  83340:83359  [60 gas]
│           ├── BaseRewardPool.balanceOf  83364:83384  [899 gas]
│           ├── SafeMath.mul  83388:83403  [55 gas]
│           ├── SafeMath.div  83407:83428  [75 gas]
│           ├── SafeMath.add  83432:83450  [59 gas]
│           ├── SafeMath.add  83518:83536  [59 gas]
│           ├── SafeMath.add  83562:83580  [59 gas]
│           └── SafeERC20.safeTransferFrom  83613:84503  [245 / -12835 gas]
│               └── SafeERC20._callOptionalReturn  83682:84497  [224 / -13080 gas]
│                   └── Address.functionCall  83718:84466  [53 / -13304 gas]
│                       └── Address.functionCallWithValue  83727:84458  [774 / -13357 gas]
│                           ├── Address.isContract  83740:83746  [718 gas]
│                           │   
│                           ├── DepositToken.transferFrom  [CALL]  83897:84382  [1008 / -14909 gas]
│                           │   │   ├── address: 0x74b79021Ea6De3f0D1731fb8BdfF6eE7DF10b8Ae
│                           │   │   ├── value: 0
│                           │   │   ├── input arguments:
│                           │   │   │   ├── sender: 0xF403C135812408BFbE8713b5A23a04b3D48AAE31
│                           │   │   │   ├── recipient: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
│                           │   │   │   └── amount: 90698479504637086
│                           │   │   └── return value: True
│                           │   │   
│                           │   └── ERC20.transferFrom  83969:84364  [1177 / -15917 gas]
│                           │       ├── ERC20._transfer  83977:84176  [-5186 / -5056 gas]
│                           │       │   ├── ERC20._beforeTokenTransfer  84004:84009  [15 gas]
│                           │       │   ├── SafeMath.sub  84052:84069  [56 gas]
│                           │       │   └── SafeMath.add  84106:84124  [59 gas]
│                           │       ├── Context._msgSender  84182:84186  [14 gas]
│                           │       ├── Context._msgSender  84227:84231  [14 gas]
│                           │       ├── SafeMath.sub  84256:84273  [56 gas]
│                           │       └── ERC20._approve  84276:84355  [-12122 gas]
│                           └── Address._verifyCallResult  84430:84447  [60 gas]
├── SafeMathUpgradeable.mul  84726:84753  [100 gas]
├── SafeMathUpgradeable.div  84757:84778  [75 gas]
├── SafeMathUpgradeable.add  84789:84807  [59 gas]
│   
├── ISettV4.balanceOf  [STATICCALL]  84882:85101  [2743 / 4631 gas]
│   │   ├── address: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│   │   └── input arguments:
│   │       └── : 0x660802Fc641b154aBA66a62137e71f331B6d787A
│   │   
│   │   
│   └── SettV4.balanceOf  [DELEGATECALL]  84989:85089  [989 / 1888 gas]
│       │   ├── address: 0xBabAE0E133cd5a6836a63820284cCD8B14D9272a
│       │   ├── input arguments:
│       │   │   └── account: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│       │   └── return value: 207989068852744534088708
│       │   
│       └── ERC20Upgradeable.balanceOf  85053:85073  [899 gas]
├── SafeMathUpgradeable.mul  85171:85198  [100 gas]
├── SafeMathUpgradeable.div  85202:85223  [75 gas]
│   
├── ISettV4.depositFor  [CALL]  85300:88480  [2743 / 95457 gas]
│   │   ├── address: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── _recipient: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│   │       └── _amount: 2765061154748237233174
│   │   
│   │   
│   └── SettV4.depositFor  [DELEGATECALL]  85407:88468  [2046 / 92714 gas]
│       │   ├── address: 0xBabAE0E133cd5a6836a63820284cCD8B14D9272a
│       │   └── input arguments:
│       │       ├── _recipient: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│       │       └── _amount: 2765061154748237233174
│       │   
│       ├── SettAccessControlDefended._defend  85503:85527  [920 gas]
│       ├── SettV4._blockLocked  85532:85551  [899 gas]
│       ├── SettV4._lockForBlock  85556:85577  [5101 gas]
│       ├── SettV4._depositForWithAuthorization  85598:88299  [974 / 69878 gas]
│       │   ├── SettV4._depositFor  85616:88181  [4386 / 67013 gas]
│       │   │   ├── SettV4.balance  85621:86881  [4307 / 22438 gas]
│       │   │   │   │   
│       │   │   │   ├── AdminUpgradeabilityProxy.balanceOf  [STATICCALL]  85682:86656  [156739 / 16182 gas]
│       │   │   │   │   │   ├── address: 0x9b4efA18c0c6b4822225b81D150f3518160f8609
│       │   │   │   │   │   ├── input arguments:
│       │   │   │   │   │   │   └── _token: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │   │   │   └── return value: 3300370261130138765085299
│       │   │   │   │   │   
│       │   │   │   │   └── Proxy._fallback  85725:86656  [45 / -140557 gas]
│       │   │   │   │       ├── AdminUpgradeabilityProxy._willFallback  85729:85764  [97 / 921 gas]
│       │   │   │   │       │   ├── AdminUpgradeabilityProxy._admin  85733:85738  [815 gas]
│       │   │   │   │       │   └── Proxy._fallback  85760:85762  [9 gas]
│       │   │   │   │       ├── UpgradeabilityProxy._implementation  85769:85774  [815 gas]
│       │   │   │   │       └── Proxy._delegate  85777:86656  [-155777 / -142338 gas]
│       │   │   │   │           │   
│       │   │   │   │           └── Controller.balanceOf  [DELEGATECALL]  85789:86644  [2819 / 13439 gas]
│       │   │   │   │               │   ├── address: 0x6354E79F21B56C11f48bcD7c451BE456D7102A36
│       │   │   │   │               │   ├── input arguments:
│       │   │   │   │               │   │   └── _token: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │   │               │   └── return value: 3300370261130138765085299
│       │   │   │   │               │   
│       │   │   │   │               │   
│       │   │   │   │               └── AdminUpgradeabilityProxy.balanceOf  [STATICCALL]  85921:86601  [151823 / 10620 gas]
│       │   │   │   │                   │   ├── address: 0x826048381d65a65DAa51342C51d464428d301896
│       │   │   │   │                   │   ├── input arguments: None
│       │   │   │   │                   │   └── return value: 3300370261130138765085299
│       │   │   │   │                   │   
│       │   │   │   │                   └── Proxy._fallback  85964:86601  [45 / -141203 gas]
│       │   │   │   │                       ├── AdminUpgradeabilityProxy._willFallback  85968:86003  [97 / 921 gas]
│       │   │   │   │                       │   ├── AdminUpgradeabilityProxy._admin  85972:85977  [815 gas]
│       │   │   │   │                       │   └── Proxy._fallback  85999:86001  [9 gas]
│       │   │   │   │                       ├── UpgradeabilityProxy._implementation  86008:86013  [815 gas]
│       │   │   │   │                       └── Proxy._delegate  86016:86601  [-150864 / -142984 gas]
│       │   │   │   │                           │   
│       │   │   │   │                           └── StrategyCvxCrvHelper.balanceOf  [DELEGATECALL]  86028:86589  [1018 / 7880 gas]
│       │   │   │   │                               │   ├── address: 0xD2d68d896cc88ae75eEde5aC0ee109cecF2B6d72
│       │   │   │   │                               │   ├── input arguments: None
│       │   │   │   │                               │   └── return value: 3300370261130138765085299
│       │   │   │   │                               │   
│       │   │   │   │                               └── BaseStrategy.balanceOf  86087:86565  [69 / 6862 gas]
│       │   │   │   │                                   ├── StrategyCvxCrvHelper.balanceOfPool  86093:86312  [1061 / 2971 gas]
│       │   │   │   │                                   │   │   
│       │   │   │   │                                   │   └── BaseRewardPool.balanceOf  [STATICCALL]  86151:86256  [1910 gas]
│       │   │   │   │                                   │           ├── address: 0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e
│       │   │   │   │                                   │           ├── input arguments:
│       │   │   │   │                                   │           │   └── account: 0x826048381d65a65DAa51342C51d464428d301896
│       │   │   │   │                                   │           └── return value: 3300370261130138765085299
│       │   │   │   │                                   │           
│       │   │   │   │                                   ├── BaseStrategy.balanceOfWant  86316:86537  [1873 / 3763 gas]
│       │   │   │   │                                   │   │   
│       │   │   │   │                                   │   └── ERC20.balanceOf  [STATICCALL]  86381:86481  [1890 gas]
│       │   │   │   │                                   │           ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │   │                                   │           └── input arguments:
│       │   │   │   │                                   │               └── _owner: 0x826048381d65a65DAa51342C51d464428d301896
│       │   │   │   │                                   │           
│       │   │   │   │                                   └── SafeMathUpgradeable.add  86541:86559  [59 gas]
│       │   │   │   ├── ERC20.balanceOf  [STATICCALL]  86733:86833  [1890 gas]
│       │   │   │   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │   │       └── input arguments:
│       │   │   │   │           └── _owner: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│       │   │   │   │       
│       │   │   │   └── SafeMathUpgradeable.add  86858:86876  [59 gas]
│       │   │   │   
│       │   │   ├── ERC20.balanceOf  [STATICCALL]  86942:87042  [1890 gas]
│       │   │   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │       └── input arguments:
│       │   │   │           └── _owner: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│       │   │   │       
│       │   │   ├── SafeERC20Upgradeable.safeTransferFrom  87082:87949  [236 / 36279 gas]
│       │   │   │   └── SafeERC20Upgradeable._callOptionalReturn  87151:87943  [224 / 36043 gas]
│       │   │   │       └── AddressUpgradeable.functionCall  87187:87912  [53 / 35819 gas]
│       │   │   │           └── AddressUpgradeable._functionCallWithValue  87196:87904  [757 / 35766 gas]
│       │   │   │               ├── AddressUpgradeable.isContract  87202:87208  [718 gas]
│       │   │   │               │   
│       │   │   │               └── ERC20.transferFrom  [CALL]  87359:87844  [34291 gas]
│       │   │   │                       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │                       ├── value: 0
│       │   │   │                       └── input arguments:
│       │   │   │                           ├── _from: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │   │   │                           ├── _to: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│       │   │   │                           └── _value: 2765061154748237233174
│       │   │   │                       
│       │   │   │   
│       │   │   ├── ERC20.balanceOf  [STATICCALL]  88004:88104  [1890 gas]
│       │   │   │       ├── address: 0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7
│       │   │   │       └── input arguments:
│       │   │   │           └── _owner: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│       │   │   │       
│       │   │   └── SafeMathUpgradeable.sub  88133:88174  [130 gas]
│       │   ├── ERC20Upgradeable.totalSupply  88188:88193  [815 gas]
│       │   ├── ERC20Upgradeable.totalSupply  88203:88208  [815 gas]
│       │   ├── SafeMathUpgradeable.mul  88213:88240  [100 gas]
│       │   └── SafeMathUpgradeable.div  88244:88292  [161 gas]
│       └── ERC20Upgradeable._mint  88308:88449  [13737 / 13870 gas]
│           ├── SettV4.depositFor  88325:88330  [15 gas]
│           ├── SafeMathUpgradeable.add  88338:88356  [59 gas]
│           └── SafeMathUpgradeable.add  88382:88400  [59 gas]
├── ISettV4.balanceOf  [STATICCALL]  88558:88777  [2743 / 4631 gas]
│   │   ├── address: 0x2B5455aac8d64C14786c3a29858E43b5945819C0
│   │   └── input arguments:
│   │       └── : 0x660802Fc641b154aBA66a62137e71f331B6d787A
│   │   
│   │   
│   └── SettV4.balanceOf  [DELEGATECALL]  88665:88765  [989 / 1888 gas]
│       │   ├── address: 0xBabAE0E133cd5a6836a63820284cCD8B14D9272a
│       │   ├── input arguments:
│       │   │   └── account: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│       │   └── return value: 210436614629230217183937
│       │   
│       └── ERC20Upgradeable.balanceOf  88729:88749  [899 gas]
├── SafeMathUpgradeable.sub  88836:88850  [49 gas]
├── SafeMathUpgradeable.mul  88933:88960  [100 gas]
├── SafeMathUpgradeable.div  88964:88985  [75 gas]
├── SafeMathUpgradeable.add  88996:89014  [59 gas]
│   
├── ISettV4.balanceOf  [STATICCALL]  89089:89308  [2743 / 4631 gas]
│   │   ├── address: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│   │   └── input arguments:
│   │       └── : 0x660802Fc641b154aBA66a62137e71f331B6d787A
│   │   
│   │   
│   └── SettV4.balanceOf  [DELEGATECALL]  89196:89296  [989 / 1888 gas]
│       │   ├── address: 0xBabAE0E133cd5a6836a63820284cCD8B14D9272a
│       │   ├── input arguments:
│       │   │   └── account: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│       │   └── return value: 79639096726852467965978
│       │   
│       └── ERC20Upgradeable.balanceOf  89260:89280  [899 gas]
├── SafeMathUpgradeable.mul  89378:89405  [100 gas]
├── SafeMathUpgradeable.div  89409:89430  [75 gas]
│   
├── ISettV4.depositFor  [CALL]  89507:92681  [2743 / 80434 gas]
│   │   ├── address: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│   │   ├── value: 0
│   │   └── input arguments:
│   │       ├── _recipient: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│   │       └── _amount: 720000067749029308678
│   │   
│   │   
│   └── SettV4.depositFor  [DELEGATECALL]  89614:92669  [2046 / 77691 gas]
│       │   ├── address: 0xBabAE0E133cd5a6836a63820284cCD8B14D9272a
│       │   └── input arguments:
│       │       ├── _recipient: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│       │       └── _amount: 720000067749029308678
│       │   
│       ├── SettAccessControlDefended._defend  89710:89734  [920 gas]
│       ├── SettV4._blockLocked  89739:89758  [899 gas]
│       ├── SettV4._lockForBlock  89763:89784  [5101 gas]
│       ├── SettV4._depositForWithAuthorization  89805:92500  [974 / 54855 gas]
│       │   ├── SettV4._depositFor  89823:92382  [4386 / 51990 gas]
│       │   │   ├── SettV4.balance  89828:91092  [4307 / 22459 gas]
│       │   │   │   │   
│       │   │   │   ├── AdminUpgradeabilityProxy.balanceOf  [STATICCALL]  89889:90872  [154627 / 16225 gas]
│       │   │   │   │   │   ├── address: 0x9b4efA18c0c6b4822225b81D150f3518160f8609
│       │   │   │   │   │   ├── input arguments:
│       │   │   │   │   │   │   └── _token: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │   │   │   └── return value: 949091302475096858393204
│       │   │   │   │   │   
│       │   │   │   │   └── Proxy._fallback  89932:90872  [45 / -138402 gas]
│       │   │   │   │       ├── AdminUpgradeabilityProxy._willFallback  89936:89971  [97 / 921 gas]
│       │   │   │   │       │   ├── AdminUpgradeabilityProxy._admin  89940:89945  [815 gas]
│       │   │   │   │       │   └── Proxy._fallback  89967:89969  [9 gas]
│       │   │   │   │       ├── UpgradeabilityProxy._implementation  89976:89981  [815 gas]
│       │   │   │   │       └── Proxy._delegate  89984:90872  [-153665 / -140183 gas]
│       │   │   │   │           │   
│       │   │   │   │           └── Controller.balanceOf  [DELEGATECALL]  89996:90860  [2819 / 13482 gas]
│       │   │   │   │               │   ├── address: 0x6354E79F21B56C11f48bcD7c451BE456D7102A36
│       │   │   │   │               │   ├── input arguments:
│       │   │   │   │               │   │   └── _token: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │   │               │   └── return value: 949091302475096858393204
│       │   │   │   │               │   
│       │   │   │   │               │   
│       │   │   │   │               └── AdminUpgradeabilityProxy.balanceOf  [STATICCALL]  90128:90817  [149777 / 10663 gas]
│       │   │   │   │                   │   ├── address: 0xBCee2c6CfA7A4e29892c3665f464Be5536F16D95
│       │   │   │   │                   │   ├── input arguments: None
│       │   │   │   │                   │   └── return value: 949091302475096858393204
│       │   │   │   │                   │   
│       │   │   │   │                   └── Proxy._fallback  90171:90817  [45 / -139114 gas]
│       │   │   │   │                       ├── AdminUpgradeabilityProxy._willFallback  90175:90210  [97 / 921 gas]
│       │   │   │   │                       │   ├── AdminUpgradeabilityProxy._admin  90179:90184  [815 gas]
│       │   │   │   │                       │   └── Proxy._fallback  90206:90208  [9 gas]
│       │   │   │   │                       ├── UpgradeabilityProxy._implementation  90215:90220  [815 gas]
│       │   │   │   │                       └── Proxy._delegate  90223:90817  [-148818 / -140895 gas]
│       │   │   │   │                           │   
│       │   │   │   │                           └── StrategyCvxHelper.balanceOf  [DELEGATECALL]  90235:90805  [1018 / 7923 gas]
│       │   │   │   │                               │   ├── address: 0xc77Fa76d7F30fb10e2D39A47861bA1704092e86e
│       │   │   │   │                               │   ├── input arguments: None
│       │   │   │   │                               │   └── return value: 949091302475096858393204
│       │   │   │   │                               │   
│       │   │   │   │                               └── BaseStrategy.balanceOf  90294:90781  [69 / 6905 gas]
│       │   │   │   │                                   ├── StrategyCvxHelper.balanceOfPool  90300:90533  [1061 / 3036 gas]
│       │   │   │   │                                   │   │   
│       │   │   │   │                                   │   └── cvxRewardPool.balanceOf  [STATICCALL]  90358:90477  [1975 gas]
│       │   │   │   │                                   │           ├── address: 0xCF50b810E57Ac33B91dCF525C6ddd9881B139332
│       │   │   │   │                                   │           └── input arguments:
│       │   │   │   │                                   │               └── account: 0xBCee2c6CfA7A4e29892c3665f464Be5536F16D95
│       │   │   │   │                                   │           
│       │   │   │   │                                   ├── BaseStrategy.balanceOfWant  90537:90753  [1873 / 3741 gas]
│       │   │   │   │                                   │   │   
│       │   │   │   │                                   │   └── ERC20.balanceOf  [STATICCALL]  90602:90697  [1868 gas]
│       │   │   │   │                                   │           ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │   │                                   │           └── input arguments:
│       │   │   │   │                                   │               └── _owner: 0xBCee2c6CfA7A4e29892c3665f464Be5536F16D95
│       │   │   │   │                                   │           
│       │   │   │   │                                   └── SafeMathUpgradeable.add  90757:90775  [59 gas]
│       │   │   │   ├── ERC20.balanceOf  [STATICCALL]  90949:91044  [1868 gas]
│       │   │   │   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │   │       └── input arguments:
│       │   │   │   │           └── _owner: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│       │   │   │   │       
│       │   │   │   └── SafeMathUpgradeable.add  91069:91087  [59 gas]
│       │   │   │   
│       │   │   ├── ERC20.balanceOf  [STATICCALL]  91153:91248  [1868 gas]
│       │   │   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │       └── input arguments:
│       │   │   │           └── _owner: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│       │   │   │       
│       │   │   ├── SafeERC20Upgradeable.safeTransferFrom  91288:92155  [236 / 21279 gas]
│       │   │   │   └── SafeERC20Upgradeable._callOptionalReturn  91357:92149  [224 / 21043 gas]
│       │   │   │       └── AddressUpgradeable.functionCall  91393:92118  [53 / 20819 gas]
│       │   │   │           └── AddressUpgradeable._functionCallWithValue  91402:92110  [757 / 20766 gas]
│       │   │   │               ├── AddressUpgradeable.isContract  91408:91414  [718 gas]
│       │   │   │               │   
│       │   │   │               └── ERC20.transferFrom  [CALL]  91565:92050  [19291 gas]
│       │   │   │                       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │                       ├── value: 0
│       │   │   │                       └── input arguments:
│       │   │   │                           ├── _from: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
│       │   │   │                           ├── _to: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│       │   │   │                           └── _value: 720000067749029308678
│       │   │   │                       
│       │   │   │   
│       │   │   ├── ERC20.balanceOf  [STATICCALL]  92210:92305  [1868 gas]
│       │   │   │       ├── address: 0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B
│       │   │   │       └── input arguments:
│       │   │   │           └── _owner: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│       │   │   │       
│       │   │   └── SafeMathUpgradeable.sub  92334:92375  [130 gas]
│       │   ├── ERC20Upgradeable.totalSupply  92389:92394  [815 gas]
│       │   ├── ERC20Upgradeable.totalSupply  92404:92409  [815 gas]
│       │   ├── SafeMathUpgradeable.mul  92414:92441  [100 gas]
│       │   └── SafeMathUpgradeable.div  92445:92493  [161 gas]
│       └── ERC20Upgradeable._mint  92509:92650  [13737 / 13870 gas]
│           ├── SettV4.depositFor  92526:92531  [15 gas]
│           ├── SafeMathUpgradeable.add  92539:92557  [59 gas]
│           └── SafeMathUpgradeable.add  92583:92601  [59 gas]
├── ISettV4.balanceOf  [STATICCALL]  92759:92978  [2743 / 4631 gas]
│   │   ├── address: 0x53C8E199eb2Cb7c01543C137078a038937a68E40
│   │   └── input arguments:
│   │       └── : 0x660802Fc641b154aBA66a62137e71f331B6d787A
│   │   
│   │   
│   └── SettV4.balanceOf  [DELEGATECALL]  92866:92966  [989 / 1888 gas]
│       │   ├── address: 0xBabAE0E133cd5a6836a63820284cCD8B14D9272a
│       │   ├── input arguments:
│       │   │   └── account: 0x660802Fc641b154aBA66a62137e71f331B6d787A
│       │   └── return value: 80312449358278698986634
│       │   
│       └── ERC20Upgradeable.balanceOf  92930:92950  [899 gas]
├── SafeMathUpgradeable.sub  93037:93051  [49 gas]
└── BaseStrategy.balanceOf  93109:93659  [69 / 7914 gas]
    ├── HarvestRestructure.balanceOfPool  93115:93341  [1870 / 3780 gas]
    │   │   
    │   └── BaseRewardPool.balanceOf  [STATICCALL]  93180:93285  [1910 gas]
    │           ├── address: 0x8E299C62EeD737a5d5a53539dF37b5356a27b07D
    │           ├── input arguments:
    │           │   └── account: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
    │           └── return value: 90698479504637086
    │           
    ├── BaseStrategy.balanceOfWant  93345:93631  [1870 / 4006 gas]
    │   │   
    │   └── Vyper_contract.balanceOf  [STATICCALL]  93410:93575  [2136 gas]
    │           ├── address: 0x49849C98ae39Fff122806C06791Fa73784FB3675
    │           ├── input arguments:
    │           │   └── arg0: 0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae
    │           └── return value: 0
    │           
    └── SafeMathUpgradeable.add  93635:93653  [59 gas]
```

Events emitted sample:

```
{'Withdrawn': [OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('amount', 4608435068897912156758)]), OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('amount', 4608435068897912156758)]), OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('amount', 1200000000000000000000)])], 'RewardPaid': [OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('reward', 337059847306858)]), OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('reward', 311025616534481)]), OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('reward', 189015816565200)])], 'Sync': [OrderedDict([('reserve0', 5446094324371630783803173), ('reserve1', 5417887716914798125716235)]), OrderedDict([('reserve0', 3017027732828353953002), ('reserve1', 3353095544564719749284395)]), OrderedDict([('reserve0', 681097485078), ('reserve1', 90233921567150687265253)]), OrderedDict([('reserve0', 2603130977594750134740293), ('reserve1', 10408411423090813010301)]), OrderedDict([('reserve0', 681090284541), ('reserve1', 90234878397437136024180)])], 'Swap': [OrderedDict([('sender', '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'), ('amount0In', 921687051582745744391), ('amount1In', 0), ('amount0Out', 0), ('amount1Out', 914317414037596453253), ('to', '0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009')]), OrderedDict([('sender', '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'), ('amount0In', 0), ('amount1In', 914317414037596453253), ('amount0Out', 820434590319788275), ('amount1Out', 0), ('to', '0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58')]), OrderedDict([('sender', '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'), ('amount0In', 0), ('amount1In', 820434590319788275), ('amount0Out', 6174225), ('amount1Out', 0), ('to', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae')]), OrderedDict([('sender', '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'), ('amount0In', 240000022583009769559), ('amount1In', 0), ('amount0Out', 0), ('amount1Out', 956830286448758927), ('to', '0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58')]), OrderedDict([('sender', '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'), ('amount0In', 0), ('amount1In', 956830286448758927), ('amount0Out', 7200537), ('amount1Out', 0), ('to', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae')])], 'Transfer': [OrderedDict([('src', '0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009'), ('dst', '0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58'), ('wad', 820434590319788275)]), OrderedDict([('from', '0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58'), ('to', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('value', 6174225)]), OrderedDict([('src', '0x05767d9EF41dC40689678fFca0608878fb3dE906'), ('dst', '0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58'), ('wad', 956830286448758927)]), OrderedDict([('from', '0xCEfF51756c56CeFFCA006cD410B03FFC46dd3a58'), ('to', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('value', 7200537)]), OrderedDict([('from', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('to', '0x93054188d876f558f4a66B2EF1d97d16eDf0895B'), ('value', 9232196)]), OrderedDict([('_from', '0x0000000000000000000000000000000000000000'), ('_to', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('_value', 90698479504637086)]), OrderedDict([('_from', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('_to', '0x989AEb4d175e16225E39E87d0D97A3360524AD80'), ('_value', 90698479504637086)]), OrderedDict([('_from', '0x989AEb4d175e16225E39E87d0D97A3360524AD80'), ('_to', '0xB1F2cdeC61db658F091671F5f199635aEF202CAC'), ('_value', 90698479504637086)]), OrderedDict([('from', '0x0000000000000000000000000000000000000000'), ('to', '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'), ('value', 90698479504637086)]), OrderedDict([('from', '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'), ('to', '0x8E299C62EeD737a5d5a53539dF37b5356a27b07D'), ('value', 90698479504637086)])], 'Approval': [OrderedDict([('owner', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('spender', '0x93054188d876f558f4a66B2EF1d97d16eDf0895B'), ('value', 0)]), OrderedDict([('owner', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('spender', '0x93054188d876f558f4a66B2EF1d97d16eDf0895B'), ('value', 9232196)]), OrderedDict([('_owner', '0x989AEb4d175e16225E39E87d0D97A3360524AD80'), ('_spender', '0xB1F2cdeC61db658F091671F5f199635aEF202CAC'), ('_value', 0)]), OrderedDict([('_owner', '0x989AEb4d175e16225E39E87d0D97A3360524AD80'), ('_spender', '0xB1F2cdeC61db658F091671F5f199635aEF202CAC'), ('_value', 90698479504637086)]), OrderedDict([('owner', '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'), ('spender', '0x8E299C62EeD737a5d5a53539dF37b5356a27b07D'), ('value', 0)]), OrderedDict([('owner', '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'), ('spender', '0x8E299C62EeD737a5d5a53539dF37b5356a27b07D'), ('value', 90698479504637086)]), OrderedDict([('owner', '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'), ('spender', '0x8E299C62EeD737a5d5a53539dF37b5356a27b07D'), ('value', 0)])], 'AddLiquidity': [OrderedDict([('provider', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('token_amounts', (0, 9232196)), ('fees', (869, 869)), ('invariant', 11089042514233750003626), ('token_supply', 10896707993162183239676)])], 'UpdateLiquidityLimit': [OrderedDict([('user', '0x989AEb4d175e16225E39E87d0D97A3360524AD80'), ('original_balance', 7267118777183603053205), ('original_supply', 10651571658627521720241), ('working_balance', 5214469869450626386934), ('working_supply', 6638362301659934759063)])], 'Deposit': [OrderedDict([('provider', '0x989AEb4d175e16225E39E87d0D97A3360524AD80'), ('value', 90698479504637086)])], 'Staked': [OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('amount', 90698479504637086)])], 'Deposited': [OrderedDict([('user', '0x9fcC3Bc8F0e63c5313C1D7B65eaf394b5be933Ae'), ('poolid', 6), ('amount', 90698479504637086)])], '(unknown)': [OrderedDict([('topic1', '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'), ('topic2', '0x0000000000000000000000000000000000000000000000000000000000000000'), ('topic3', '0x000000000000000000000000660802fc641b154aba66a62137e71f331b6d787a'), ('data', 0x000000000000000000000000000000000000000000000084ae855c0f78c2e6bd)]), OrderedDict([('topic1', '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'), ('topic2', '0x0000000000000000000000000000000000000000000000000000000000000000'), ('topic3', '0x000000000000000000000000660802fc641b154aba66a62137e71f331b6d787a'), ('data', 0x00000000000000000000000000000000000000000000002480a51ab4ff07ac70)])], 'TreeDistribution': [OrderedDict([('token', '0x2B5455aac8d64C14786c3a29858E43b5945819C0'), ('amount', 2447545776485683095229), ('blockNumber', 13236771), ('timestamp', 1631795256)]), OrderedDict([('token', '0x53C8E199eb2Cb7c01543C137078a038937a68E40'), ('amount', 673352631426231020656), ('blockNumber', 13236771), ('timestamp', 1631795256)])], 'HarvestCustom': [OrderedDict([('cvxCrvHarvested', 4608435257913728721958), ('cvxHarvested', 1200000112915048847797), ('blockNumber', 13236771)])]}
```