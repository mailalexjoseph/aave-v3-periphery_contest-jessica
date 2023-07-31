import "methods/Methods_base.spec";

///////////////// Properties ///////////////////////

// Property: Reward index monotonically increase
rule index_keeps_growing(address asset, address reward, method f) filtered { f -> !f.isView } {
    uint256 _index = getAssetRewardIndex(asset, reward);

    env e; calldataarg args;
    f(e, args);

    uint256 index_ = getAssetRewardIndex(asset, reward);
    
    assert index_ >= _index;
}

/*
    @Rule 1

    @title:
      claimRewards reverts when address "to" is zero 
    @methods:
      claimRewards
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
      FAILS on bug2.patch 
      https://prover.certora.com/output/3960/a5d8b3f0d77445ed994986453b58fbdd/?anonymousKey=2739620fafed4be2853fb4673a47cee32954b0d9
    @link:
      https://prover.certora.com/output/3960/bae8d6830fd24ccb9c31863053075bf8/?anonymousKey=8b9316f3deebfd3c00625fbaad3ec1a10c458588
    @status:
      COMPLETE
*/
rule claimRewards_reverts_when_to_address_is_zero() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;
  
  claimRewards@withrevert(e, assets, amount, to, reward);
  
  assert to == 0 => lastReverted;
}

/*
    @Rule 2

    @title:
      zero address balance does not change after claimRewards
    @methods:
      claimRewards
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
      FAILS on bug2.patch 
      https://prover.certora.com/output/3960/172329e980904c3da85fc82b3cd96479/?anonymousKey=a85221a0b21dc7054aaa36d696c3f9812b61dbe4
    @link:
      https://prover.certora.com/output/3960/993fcd817d1d47f6b03ffe9157476f27/?anonymousKey=ee36e03f91f4256c35013ffc0e24918fca020d96
    @status:
      COMPLETE
*/
rule zero_address_cannot_claimRewards() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;

  uint256 balanceBefore = _DummyERC20_rewardToken.balanceOf(e, to);
  claimRewards(e, assets, amount, to, reward);
  uint256 balanceAfter = _DummyERC20_rewardToken.balanceOf(e, to);
  
  assert to == 0 => (balanceAfter == balanceBefore);
  assert balanceAfter >= balanceBefore;
}

/*
    @Rule 3

    @title:
      claimAllRewardsInternal updates the claimedAmounts
    @methods:
      claimAllRewardsInternal
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
      FAILS on bug3.patch 
      https://prover.certora.com/output/3960/e11e7940b002465288af7b8d39ed0ca4/?anonymousKey=a065d3d80390584f938f5820b04f96ad17933ba7
    @link:
      https://prover.certora.com/output/3960/074e99b6aa2347e8818254f3cfc254c0/?anonymousKey=e9c1bc25ae55efa053b1a17857559b5e29a48475
    @status:
      COMPLETE
*/
rule claimAllRewardsInternal_updates_claimedAmounts(){
  env e;
  address[] assets;
  address claimer;
  address user;
  address to;

  address asset;
  address reward;

  address[] rewardsList;
  uint256[] claimedAmounts;

  require assets[0] == asset;
  require reward == _DummyERC20_rewardToken; 
  require getRewardsList(e, 0) == reward;

  uint256 rewardAmount = getRewardAmount(e, asset, reward, user);

  rewardsList, claimedAmounts = claimAllRewardsInternal(e, assets, claimer, user, to);

  assert rewardAmount > 0 => claimedAmounts[0] > 0;
}

/*
    @Rule 4

    @title:
      Integrity of getClaimer
    @methods:
      getClaimer
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/812e68b13de34f18afe1e52a3eed28ca/?anonymousKey=e4de21f025d4ab59e71455795e0bc7edefff4e43
    @status:
      COMPLETE
*/
rule integrity_of_getClaimer(){
  env e;
  address user;
  address expectedClaimer = getClaimerHarness(e, user);
  address actualClaimer = getClaimer(e, user);
  assert expectedClaimer == actualClaimer;
}

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