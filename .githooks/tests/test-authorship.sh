#!/bin/sh
# Regression tests for the authorship + identity git hooks.
# Builds a throwaway repo, installs the hooks, and asserts PASS/FAIL cases.
# Run: sh .githooks/tests/test-authorship.sh   (needs git + python)
set -u

HOOKS_DIR=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cd "$tmp"

git init -q
mkdir -p .githooks
cp "$HOOKS_DIR/pre-commit" "$HOOKS_DIR/commit-msg" .githooks/
chmod +x .githooks/pre-commit .githooks/commit-msg 2>/dev/null || true
git config core.hooksPath .githooks
git config user.name udonsari0101
git config user.email udonsari0101@users.noreply.github.com

rc=0
n=0
pass=0

# try_commit DESC EXPECT(ok|reject) -- commit-cmd...
# modifies a file, stages it, runs the commit, checks the result.
run_case() {
	desc="$1"; expect="$2"; shift 2
	n=$((n+1))
	printf 'x %s\n' "$n" >> f
	git add f
	before=$(git rev-list --count HEAD 2>/dev/null || echo 0)
	if "$@" >/dev/null 2>&1; then actual=ok; else actual=reject; fi
	after=$(git rev-list --count HEAD 2>/dev/null || echo 0)
	# a committed case must add exactly one commit; a rejected case must add none
	if [ "$expect" = ok ] && [ "$after" -le "$before" ]; then actual=reject; fi
	if [ "$expect" = reject ] && [ "$after" -gt "$before" ]; then actual=ok; fi
	if [ "$actual" = "$expect" ]; then
		pass=$((pass+1)); echo "PASS [$desc] expected=$expect"
	else
		rc=1; echo "FAIL [$desc] expected=$expect got=$actual"
		# clean a stuck staged change so later cases are independent
		git reset -q --hard >/dev/null 2>&1 || true
	fi
}

run_case "human author + clean message" ok \
	git commit -q -m "Map Sonoma IOAccelerator contract for custom Xe-LP device"

run_case "Claude as author" reject \
	git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -m "add thing"

run_case "Anthropic as committer (env)" reject \
	env GIT_COMMITTER_NAME=Anthropic GIT_COMMITTER_EMAIL=bot@anthropic.com git commit -q -m "add thing"

run_case "Co-authored-by: Claude trailer" reject \
	git commit -q -m "add thing

Co-authored-by: Claude <noreply@anthropic.com>"

run_case "Generated-by: AI trailer" reject \
	git commit -q -m "add thing

Generated-by: AI"

run_case "Assisted-by: Claude trailer" reject \
	git commit -q -m "add thing

Assisted-by: Claude"

run_case "Generated with Claude Code footer" reject \
	git commit -q -m "add thing

Generated with Claude Code"

echo "----"
echo "$pass/$n cases behaved as expected"
if [ "$rc" -eq 0 ]; then echo "AUTHORSHIP_HOOK_TESTS_OK"; else echo "AUTHORSHIP_HOOK_TESTS_FAILED"; fi
exit $rc
