// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

import {RewardsController} from '../../contracts/rewards/RewardsController.sol';

contract RewardsControllerHarness is RewardsController {
    
    constructor(address emissionManager) RewardsController(emissionManager) {}

    // returns an asset's reward index
    function getAssetRewardIndex(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].index;
    }

    // User's data

    function getUserIndex(address asset, address reward, address user) external view returns (uint256) {
        return _assets[asset].rewards[reward].usersData[user].index;
    }

    function getRewardAmount(address asset, address reward, address user) external view returns (uint256) {
        return _assets[asset].rewards[reward].usersData[user].accrued;
    }

    // User asset balances data

    function getUserAssetBalancesUserBalance(address[] calldata assets, address user, uint256 j) external view returns (uint256) {
        return _getUserAssetBalances(assets, user)[j].userBalance;
    }

    function getUserAssetBalancesTotalSupply(address[] calldata assets, address user, uint256 j) external view returns (uint256) {
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

    function getAssetUnit(address asset) external view returns (uint256) {
        return 10**_assets[asset].decimals;
    }

    // Internal functions

    function claimAllRewardsInternal(address[] calldata assets, address claimer, address user, address to) external returns (address[] memory rewardsList, uint256[] memory claimedAmounts) {
        return _claimAllRewards(assets,claimer,user,to);
    }

    // Storage variables

    function getClaimerHarness(address user) external view returns(address) {
        return _authorizedClaimers[user];
    }
}