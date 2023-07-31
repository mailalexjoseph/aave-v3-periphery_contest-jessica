/*
    @Rule 

    @title:
      claimAllRewardsInternal updates user data
    @methods:
      claimAllRewardsInternal
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
      FAILS on bug1.patch
    @link:
      
    @status:
      TODO
*/
rule claimAllRewardsInternal_updates_data(){
  env e;
  address reward;
  address user;
  address[] assets;

  address claimer;
  address to;

  address[] rewardsList;
  uint256[] claimedAmounts;

  uint256 userBalance = getUserAssetBalancesUserBalance(e, assets, user, 0);
  uint256 totalSupply = getUserAssetBalancesTotalSupply(e, assets, user, 0);
  address asset = getUserAssetBalancesAsset(e, assets, user, 0);

  uint256 userIndex = getUserIndex(e, asset, reward, user);
  uint256 assetUnit = getAssetUnit(e, asset);
  uint256 newAssetIndex = getNewAssetIndex(e, asset, reward, totalSupply);

  uint256 rewardAmountBefore = getRewardAmount(e, asset, reward, user);

  uint256 rewardsAccrued = getRewards(e, userBalance, newAssetIndex, userIndex, assetUnit);

  rewardsList, claimedAmounts = claimAllRewardsInternal(e, assets, claimer, user, to);

  uint256 rewardAmountAfter = getRewardAmount(e, asset, reward, user); 

  assert rewardAmountAfter == assert_uint256(rewardAmountBefore + rewardsAccrued);
}