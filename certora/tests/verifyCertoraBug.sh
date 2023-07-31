#!/bin/bash

BUG_NUM=$1
RULE=$2

FILE="bug$BUG_NUM.patch"
P="certora/tests/certora/$FILE"

echo "Applying $FILE"
git apply $P
certoraRun certora/conf/default.conf --send_only --rule $RULE --msg $FILE
echo "Reverting $FILE"
git apply -R $P