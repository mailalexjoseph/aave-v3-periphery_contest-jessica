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
      https://prover.certora.com/output/3960/97d88da0d2e448529e923e619444319b/?anonymousKey=2a4aa61a348efa949f8161bacc2b0a6cfc4b882b
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
  claimRewards(e, assets, amount, to, _DummyERC20_rewardToken);
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
    @Rule 5

    @title:
      Integrity of getRevision
    @methods:
      getRevision
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/ec6c3af3c9624262b8d36e124bb1a965/?anonymousKey=c91cb9773e30c6174c9f533c2c39ea0f8479c6da
    @status:
      COMPLETE
*/
rule integrity_of_getRevision(){
  env e;
  uint256 expectedRevision = getRevisionHarness(e);
  uint256 actualRevision = 1;
  assert expectedRevision == actualRevision;
}

/*
    @Rule 6

    @title:
      Integrity of getRewardOracle
    @methods:
      getRewardOracle
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/c751224e36f14502bc12219754b22034/?anonymousKey=8f65c8830ce83641705f3f86db58bb335b26c5c0
    @status:
      COMPLETE
*/
rule integrity_of_getRewardOracle(){
  env e;
  address reward;
  address expectedRewardOracle = getRewardOracleHarness(e, reward);
  address actualRewardOracle = getRewardOracle(e, reward);
  assert expectedRewardOracle == actualRewardOracle;
}

/*
    @Rule 7

    @title:
      Integrity of getTransferStrategy
    @methods:
      getTransferStrategy
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/2a570242837b4a07a7409e33d4b277de/?anonymousKey=6fa906ea8671d07f71c6d0a28ad807d142fa8e03
    @status:
      COMPLETE
*/
rule integrity_of_getTransferStrategy(){
  env e;
  address reward;
  address expectedTransferStrategy = getTransferStrategyHarness(e, reward);
  address actualTransferStrategy = getTransferStrategy(e, reward);
  assert expectedTransferStrategy == actualTransferStrategy;
}

/*
    @Rule 8

    @title:
      only emissionManager can configureAssets
    @methods:
      configureAssets
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/14e1fc3c54ef4dd2ab4d62b22d901d4a/?anonymousKey=21835fa2296ab6295f7c71975776afb0f3993946
    @status:
      COMPLETE
*/
rule only_emissionManager_can_configureAssets(){
  env e;
  calldataarg args;
  address emissionManager = getEmissionManagerHarness(e);

  configureAssets@withrevert(e, args);

  assert e.msg.sender != emissionManager => lastReverted;
}

/*
    @Rule 9

    @title:
      only emissionManager can setTransferStrategy
    @methods:
      setTransferStrategy
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/40984a07e25f4cedb3346097bc777b27/?anonymousKey=6e15d4f81ba88b8ed90de21caaf08684216fa9b4
    @status:
      COMPLETE
*/
rule only_emissionManager_can_setTransferStrategy(){
  env e;
  calldataarg args;
  address emissionManager = getEmissionManagerHarness(e);

  setTransferStrategy@withrevert(e, args);

  assert e.msg.sender != emissionManager => lastReverted;
}

/*
    @Rule 10

    @title:
      only emissionManager can setRewardOracle
    @methods:
      setRewardOracle
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/30312629fc5a453eb636da247113d4aa/?anonymousKey=9bc8b832ddef32c1b259d2dd859ef315bca7c882
    @status:
      COMPLETE
*/
rule only_emissionManager_can_setRewardOracle(){
  env e;
  calldataarg args;
  address emissionManager = getEmissionManagerHarness(e);

  setRewardOracle@withrevert(e, args);

  assert e.msg.sender != emissionManager => lastReverted;
}

/*
    @Rule 11

    @title:
      claimRewardsOnBehalf reverts when address "to" is zero 
    @methods:
      claimRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/358808e9945e4fcbb4f16ab3e5bdeb55/?anonymousKey=eabb1a8a9d768ab0ca58a3642905c0e30cc80447
    @status:
      COMPLETE
*/
rule claimRewardsOnBehalf_reverts_when_to_address_is_zero() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;
  address user;
  
  claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);
  
  assert to == 0 => lastReverted;
}

/*
    @Rule 12

    @title:
      zero address balance does not change after claimRewardsOnBehalf
    @methods:
      claimRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/a40809fa97ab4145b57dd35cddeb4ac1/?anonymousKey=a593809f5d7cf921f910e0c91a46d2930f87e984
    @status:
      COMPLETE
*/
rule zero_address_cannot_claimRewardsOnBehalf() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;
  address user;

  uint256 balanceBefore = _DummyERC20_rewardToken.balanceOf(e, to);
  claimRewardsOnBehalf(e, assets, amount, user, to, _DummyERC20_rewardToken);
  uint256 balanceAfter = _DummyERC20_rewardToken.balanceOf(e, to);
  
  assert to == 0 => (balanceAfter == balanceBefore);
  assert balanceAfter >= balanceBefore;
}

/*
    @Rule 13

    @title:
      claimRewardsOnBehalf reverts when address "user" is zero 
    @methods:
      claimRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/81ff96fa662d4eae87088ece46033662/?anonymousKey=43328a28aeeeb69e663e7ed4a29422340d0671af
    @status:
      COMPLETE
*/
rule claimRewardsOnBehalf_reverts_when_user_address_is_zero() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;
  address user;
  
  claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);
  
  assert user == 0 => lastReverted;
}

/*
    @Rule 14

    @title:
      zero address balance does not change after claimRewardsOnBehalf
    @methods:
      claimRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/52c1cd89c54047f09fd7b142abf0cec0/?anonymousKey=b3dcf74a25e27b12c83370aa7c747a9b0337908b
    @status:
      COMPLETE
*/
rule zero_user_address_cannot_claimRewardsOnBehalf() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;
  address user;
  address asset;

  uint256 rewardAmountBefore = getRewardAmount(e, asset, reward, user);
  claimRewardsOnBehalf(e, assets, amount, user, to, reward);
  uint256 rewardAmountAfter = getRewardAmount(e, asset, reward, user);
  
  assert user == 0 => (rewardAmountAfter == rewardAmountBefore);
}

/*
    @Rule 15

    @title:
      claimRewardsOnBehalf reverts when claimer is not authorized
    @methods:
      claimRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/ce69559e95c443ef8c0fe34d33929908/?anonymousKey=b78eee460558fc624e11e62fc96446375b2ee070
    @status:
      COMPLETE
*/
rule claimRewardsOnBehalf_reverts_when_claimer_is_not_authorized() {
  env e;
  address[] assets;
  uint256 amount;
  address to;
  address reward;
  address user;

  address claimer = getClaimerHarness(e, user);
  
  claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);
  
  assert e.msg.sender != claimer => lastReverted;
}

/*
    @Rule 16

    @title:
      claimAllRewards reverts when address "to" is zero 
    @methods:
      claimAllRewards
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/95a40f26c0e94dd4b12c8c36998f470c/?anonymousKey=8ddda738ddcec5e5ae66607d9b2bde3eee1be5ec
    @status:
      COMPLETE
*/
rule claimAllRewards_reverts_when_to_address_is_zero() {
  env e;
  address[] assets;
  address to;
  
  claimAllRewards@withrevert(e, assets, to);
  
  assert to == 0 => lastReverted;
}

/*
    @Rule 17

    @title:
      zero address balance does not change after claimAllRewards
    @methods:
      claimAllRewards
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/38b59e77f5e64d87be94a739c4652a54/?anonymousKey=7ea417a2db7797f9fbfb1f0e94fffdb6230e4b4f
    @status:
      COMPLETE
*/
rule zero_address_cannot_claimAllRewards() {
  env e;
  address[] assets;
  address to;
  address[] rewards;

  rewards = getRewardsListHarness(e);

  require rewards.length == 1;
  require rewards[0] == _DummyERC20_rewardToken;

  uint256 balanceBefore = _DummyERC20_rewardToken.balanceOf(e, to);
  claimAllRewards(e, assets, to);
  uint256 balanceAfter = _DummyERC20_rewardToken.balanceOf(e, to);
  
  assert to == 0 => (balanceAfter == balanceBefore);
  assert balanceAfter >= balanceBefore;
}

/*
    @Rule 18

    @title:
      claimAllRewardsOnBehalf reverts when address "to" is zero 
    @methods:
      claimAllRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/c69d0faaaf814c9e951536d6ecb193b9/?anonymousKey=063d19282777fb33adfac8444458ddffe39e7ef3
    @status:
      COMPLETE
*/
rule claimAllRewardsOnBehalf_reverts_when_to_address_is_zero() {
  env e;
  address[] assets;
  address to;
  address user;
  
  claimAllRewardsOnBehalf@withrevert(e, assets, user, to);
  
  assert to == 0 => lastReverted;
}

/*
    @Rule 19

    @title:
      zero address balance does not change after claimAllRewardsOnBehalf
    @methods:
      claimAllRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/e0dd34c2e49f4fe2bf967b9aa77575bc/?anonymousKey=6f4e4d74f14643c1f32454ee653ca21480028a4e
    @status:
      COMPLETE
*/
rule zero_address_cannot_claimAllRewardsOnBehalf() {
  env e;
  address[] assets;
  address to;
  address user;

  address[] rewards;

  rewards = getRewardsListHarness(e);

  require rewards.length == 1;
  require rewards[0] == _DummyERC20_rewardToken;

  uint256 balanceBefore = _DummyERC20_rewardToken.balanceOf(e, to);
  claimAllRewardsOnBehalf(e, assets, user, to);
  uint256 balanceAfter = _DummyERC20_rewardToken.balanceOf(e, to);
  
  assert to == 0 => (balanceAfter == balanceBefore);
  assert balanceAfter >= balanceBefore;
}

/*
    @Rule 20

    @title:
      claimAllRewardsOnBehalf reverts when address "user" is zero 
    @methods:
      claimAllRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/d1799d8a745646a88420cc2d600d201c/?anonymousKey=f282ace513385ee1ecb43bd75892048360981e9d
    @status:
      COMPLETE
*/
rule claimAllRewardsOnBehalf_reverts_when_user_address_is_zero() {
  env e;
  address[] assets;
  address to;
  address user;
  
  claimAllRewardsOnBehalf@withrevert(e, assets, user, to);
  
  assert user == 0 => lastReverted;
}

/*
    @Rule 21

    @title:
      zero address balance does not change after claimAllRewardsOnBehalf
    @methods:
      claimAllRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/f2e3d00f1e1e4ba7837c5b9bf0fda63e/?anonymousKey=6d72e282d753362e281d184dfe91efe608f09a0f
    @status:
      COMPLETE
*/
rule zero_user_address_cannot_claimAllRewardsOnBehalf() {
  env e;
  address[] assets;
  address to;
  address reward;
  address user;
  address asset;

  address[] rewards;

  rewards = getRewardsListHarness(e);

  require rewards.length == 1;
  require rewards[0] == _DummyERC20_rewardToken;

  uint256 rewardAmountBefore = getRewardAmount(e, asset, reward, user);
  claimAllRewardsOnBehalf(e, assets, user, to);
  uint256 rewardAmountAfter = getRewardAmount(e, asset, reward, user);
  
  assert user == 0 => (rewardAmountAfter == rewardAmountBefore);
}

/*
    @Rule 22

    @title:
      claimAllRewardsOnBehalf reverts when claimer is not authorized
    @methods:
      claimAllRewardsOnBehalf
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/b6e165db9bc14d0786ccff431c04ea38/?anonymousKey=d4b4de4d4d73fb8762c8a00294b721c12885d5da
    @status:
      COMPLETE
*/
rule claimAllRewardsOnBehalf_reverts_when_claimer_is_not_authorized() {
  env e;
  address[] assets;
  address to;
  address user;

  address claimer = getClaimerHarness(e, user);
  
  claimAllRewardsOnBehalf@withrevert(e, assets, user, to);
  
  assert e.msg.sender != claimer => lastReverted;
}

/*
    @Rule 23

    @title:
      only emissionManager can setClaimer
    @methods:
      setClaimer
    @sanity:
      PASSES
    @outcome:
      PASSES
    @note:
    @link:
      https://prover.certora.com/output/3960/97ca7ee7366d4b7f87f458b31ce4d199/?anonymousKey=5cff1ab2477c66de62a623f923763db1bfe487f4
    @status:
      COMPLETE
*/
rule only_emissionManager_can_setClaimer(){
  env e;
  calldataarg args;
  address emissionManager = getEmissionManagerHarness(e);

  setClaimer@withrevert(e, args);

  assert e.msg.sender != emissionManager => lastReverted;
}