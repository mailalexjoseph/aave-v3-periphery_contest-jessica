// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

import {RewardsController} from '../../contracts/rewards/RewardsController.sol';
import {ITransferStrategyBase} from '../../contracts/rewards/interfaces/ITransferStrategyBase.sol';
import {IEACAggregatorProxy} from '../../contracts/misc/interfaces/IEACAggregatorProxy.sol';
import {RewardsDataTypes} from '../../contracts/rewards/libraries/RewardsDataTypes.sol';
import {IScaledBalanceToken} from '@aave/core-v3/contracts/interfaces/IScaledBalanceToken.sol';

contract RewardsControllerHarness is RewardsController {
    
    constructor(address emissionManager) RewardsController(emissionManager) {}

    // Asset Data

    function getAssetRewardIndex(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].index;
    }

    function getAvailableRewardsCount(address asset) external view returns (uint256) {
        return _assets[asset].availableRewardsCount;
    }

    function getAvailableRewards(address asset, uint128 r) external view returns (address) {
        return _assets[asset].availableRewards[r];
    }
 
    // User's data

    function getUserIndex(address asset, address reward, address user) external view returns (uint256) {
        return _assets[asset].rewards[reward].usersData[user].index;
    }

    function getRewardAmount(address asset, address reward, address user) external view returns (uint256) {
        return _assets[asset].rewards[reward].usersData[user].accrued;
    }

    // User asset balances data

    function getUserAssetBalancesUserBalance(address[] calldata assets, address user, uint256 j) public view returns (uint256) {
        return _getUserAssetBalances(assets, user)[j].userBalance;
    }

    function getUserAssetBalancesTotalSupply(address[] calldata assets, address user, uint256 j) public view returns (uint256) {
        return _getUserAssetBalances(assets, user)[j].totalSupply;
    }

    function getUserAssetBalancesAsset(address[] calldata assets, address user, uint256 j) external view returns (address) {
        return _getUserAssetBalances(assets, user)[j].asset;
    }

    function getNewAssetIndex(address asset, address reward, uint256 totalSupply) external returns (uint256) {
        uint256 assetUnit = 10**_assets[asset].decimals;
        (uint256 newAssetIndex, bool rewardDataUpdated) = _updateRewardData(_assets[asset].rewards[reward], totalSupply, assetUnit);
        return newAssetIndex;
    }

    function getRewardsList(uint256 j) external view returns (address) {
        return _rewardsList[j];
    }

    function getRewards(uint256 userBalance, uint256 newAssetIndex, uint256 userIndex, uint256 assetUnit) external returns (uint256) {
        uint256 rewardsAccrued = _getRewards(userBalance, newAssetIndex, userIndex, assetUnit);
        return rewardsAccrued;
    }

    function getUserTotalSupplyAndBalance(address[] calldata assets, address user, uint256 i) public returns (uint256, uint256) {
        return IScaledBalanceToken(assets[i]).getScaledUserBalanceAndSupply(user);
    }

    // Internal functions

    function claimRewardsInternal(address[] calldata assets, uint256 amount, address claimer, address user, address to, address reward) public returns (uint256) {
        return _claimRewards(assets, amount, claimer, user, to, reward);
    }

    function claimAllRewardsInternal(address[] calldata assets, address claimer, address user, address to) external returns (address[] memory rewardsList, uint256[] memory claimedAmounts) {
        return _claimAllRewards(assets,claimer,user,to);
    }

    function installTransferStrategyInternal(address reward,  address transferStrategy) external {
        _installTransferStrategy(reward, ITransferStrategyBase(transferStrategy));
    }

    function setRewardOracleInternal(address reward,  address rewardOracle) external {
        _setRewardOracle(reward, IEACAggregatorProxy(rewardOracle));
    }

    function isContract(address account) external view returns (bool) {
        return _isContract(account);
    }

    function transferRewardsInternal(address to, address reward, uint256 amount) external {
        _transferRewards(to, reward,amount);
    }

    function getAssetUnit(address asset) public view returns (uint256) {
        return 10**_assets[asset].decimals;
    }

    function updateRewardData(address[] calldata assets, address reward, address user, uint256 j) public returns (uint256, bool) {
        address asset = assets[j];
        RewardsDataTypes.RewardData storage rewardData = _assets[asset].rewards[reward];
        uint256 assetUnit = getAssetUnit(asset);
        uint256 totalSupply = getUserAssetBalancesTotalSupply(assets, user, j);
        (uint256 newAssetIndex, bool rewardDataUpdated) = _updateRewardData(rewardData, totalSupply, assetUnit);
        return (newAssetIndex, rewardDataUpdated);
    }

    function updateUserData(address[] calldata assets, address reward, address user, uint256 j) public returns (uint256, bool) {
        address asset = assets[j];
        RewardsDataTypes.RewardData storage rewardData = _assets[asset].rewards[reward];
        uint256 userBalance = getUserAssetBalancesUserBalance(assets, user, j);
        uint256 totalSupply = getUserAssetBalancesTotalSupply(assets, user, j);
        uint256 assetUnit = getAssetUnit(asset);
        (uint256 newAssetIndex, bool rewardDataUpdated) = _updateRewardData(rewardData, totalSupply, assetUnit);
        (uint256 rewardsAccrued, bool userDataUpdated) = _updateUserData(rewardData,user,userBalance,newAssetIndex,assetUnit);
        return (rewardsAccrued, userDataUpdated);
    }
    
    // Storage variables

    function getClaimerHarness(address user) external view returns(address) {
        return _authorizedClaimers[user];
    }

    function getRevisionHarness() external view returns(uint256) {
        return REVISION;
    }

    function getRewardOracleHarness(address reward) external view returns(address) {
        return address(_rewardOracle[reward]);
    }

    function getTransferStrategyHarness(address reward) external view returns(address) {
        return address(_transferStrategy[reward]);
    }

    function getEmissionManagerHarness() external view returns(address) {
        return EMISSION_MANAGER;
    }

    function getRewardsListHarness() external view returns (address[] memory) {
        return _rewardsList;
    }

    // Misc

    function getRewardOracleLatestAnswer(address rewardOracle) external view returns (int256) {
        return IEACAggregatorProxy(rewardOracle).latestAnswer();
    }

   function isContractHarness(address account) external view returns (bool) {
    // This method relies on extcodesize, which returns 0 for contracts in
    // construction, since the code is only stored at the end of the
    // constructor execution.

    uint256 size;
    // solhint-disable-next-line no-inline-assembly
    assembly {
      size := extcodesize(account)
    }
    return size > 0;
   }

   // Configure assets functions

    function getRewardsDataHarness(address asset, address reward) public view returns (uint256,uint256,uint256,uint256) {
        return (
        _assets[asset].rewards[reward].index,
        _assets[asset].rewards[reward].emissionPerSecond,
        _assets[asset].rewards[reward].lastUpdateTimestamp,
        _assets[asset].rewards[reward].distributionEnd
        );
  }

  function getDistributionEndHarness(address asset, address reward) public view returns (uint256) {
    return _assets[asset].rewards[reward].distributionEnd;
  }

  function getAvailableRewardsAtIndex(address asset, uint128 i) public view returns (address) {
    return _assets[asset].availableRewards[i];
  }

  function getUserAssetIndexHarness(address user, address asset, address reward) public view returns (uint256) {
    return _assets[asset].rewards[reward].usersData[user].index;
  }

  function configureAssetsInternal(RewardsDataTypes.RewardsConfigInput[] memory rewardsInput) public {
    _configureAssets(rewardsInput);
  }

  function isRewardEnabled(address reward) public view returns (bool) {
    return _isRewardEnabled[reward];
  }
}