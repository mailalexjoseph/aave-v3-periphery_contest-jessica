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
  address asset;
  address[] assets = [asset];

  address claimer;
  address to;

  address[] rewardsList;
  uint256[] claimedAmounts;

  uint256 availableRewardsCount = getAvailableRewardsCount(e, asset);
  address availableReward = getAvailableRewards(e, asset, 0);

  require reward == availableReward;

  uint256 userBalance = getUserAssetBalancesUserBalance(e, assets, user, 0);
  uint256 totalSupply = getUserAssetBalancesTotalSupply(e, assets, user, 0);
  address userAsset = getUserAssetBalancesAsset(e, assets, user, 0);

  require userAsset == asset;

  uint256 userIndex = getUserIndex(e, asset, reward, user);
  uint256 assetUnit = getAssetUnit(e, asset);
  uint256 newAssetIndex = getNewAssetIndex(e, asset, reward, totalSupply);

  uint256 rewardAmountBefore = getRewardAmount(e, asset, reward, user);

  uint256 rewardsAccrued = getRewards(e, userBalance, newAssetIndex, userIndex, assetUnit);

  rewardsList, claimedAmounts = claimAllRewardsInternal(e, assets, claimer, user, to);

  uint256 rewardAmountAfter = getRewardAmount(e, asset, reward, user); 

  assert rewardAmountAfter == assert_uint256(rewardAmountBefore + rewardsAccrued);
}

/*
    @Rule 44

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
/* rule claimAllRewardsInternal_updates_data(){
  env e;
  address asset;
  address[] assets = [asset];
  address claimer;
  address user;
  address to;

  address reward = getRewardsList(e,0);
  require reward == _DummyERC20_rewardToken;

  uint256 rewardsAccrued;
  bool userDataUpdated;

  uint256 rewardsAmountBefore = getRewardAmount(e, asset, reward, user);
  rewardsAccrued, userDataUpdated = updateUserData(e, assets, reward, user, 0);

  claimAllRewardsInternal(e, assets, claimer, user, to);
  uint256 rewardsAmountAfter = getRewardAmount(e, asset, reward, user);

  assert rewardsAmountAfter == assert_uint256(rewardsAmountBefore + rewardsAccrued);
} */

/*
    @Rule 44

    @title:
      Integrity of configureAssets
    @methods:
      configureAssets
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/5d55563b6fb847e4ad6770e837f4ecca/?anonymousKey=97778a9f6536939fedf863a47951c57a4ed8ce85
    @status:
      COMPLETE
*/
/* rule integrity_of_configureAssets {
  env e;
  RewardsDataTypes.RewardsConfigInput[] config;
  configureAssets(e, config);
  assert true;
} */


/*
    @Rule 44

    @title:
      Integrity of constructor
    @methods:
      constructor
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      
    @status:
      COMPLETE
*/
rule integrity_of_constructor() {
  env e;
  address emissionManager;
  currentContract.constructor(emissionManager);
  address actualEmissionManager = getEmissionManagerHarness(e);
  assert emissionManager == actualEmissionManager;
}