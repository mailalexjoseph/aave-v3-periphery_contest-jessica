echo "Applying certora/tests/certora/bug1.patch"
git apply certora/tests/certora/bug1.patch
echo "Running jobs"
certoraRun certora/conf/default.conf --rule_sanity --msg certora/tests/certora/bug1.patch
echo "Reverting certora/tests/certora/bug1.patch"
git apply -R certora/tests/certora/bug1.patch