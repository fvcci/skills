#!/usr/bin/env bash
# Wait for Greptile to respond on a PR after a given time.
#
# Usage: wait-for-greptile.sh <PR> <since-ISO-8601-UTC> [timeout-minutes] [start-grace-minutes]
#   Both limits count from <since>, so a late start does not extend them.
#   e.g. wait-for-greptile.sh 19031 2026-11-12T22:44:03Z 45 15
#
# Greptile counts as having responded when any of these happened after <since>:
#   - a Greptile check run on the PR head started (we then wait for it to complete)
#   - a Greptile review was submitted
#   - a Greptile issue comment was created OR edited (summaries are edited in place)
#   - a Greptile inline review comment was created
# Exit codes: 0 responded (activity printed), 2 nothing started within the grace period,
#             3 started but not finished by the timeout. Network errors are retried.
set -u
pr=$1 since=$2 timeout_min=${3:-45} grace_min=${4:-15}
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner) || exit 1
# Measure the grace period and timeout from the request, not from when this script started.
start=$(date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$since" +%s 2>/dev/null || date -u -d "$since" +%s) || exit 1
is_greptile='test("(?i)greptile")'

query() { # retry transient API failures instead of treating them as "no activity"
  local out
  for _ in 1 2 3; do out=$(gh api "$@" 2>/dev/null) && { printf '%s' "$out"; return 0; }; sleep 10; done
  return 1
}

while :; do
  elapsed=$((($(date +%s) - start) / 60))
  head=$(query "repos/$repo/pulls/$pr" -q .head.sha) || { sleep 60; continue; }

  runs=$(query "repos/$repo/commits/$head/check-runs" --paginate \
    -q ".check_runs[] | select((.name|$is_greptile) or (.app.slug|$is_greptile)) | select(.started_at > \"$since\") | \"\(.status) \(.conclusion // \"-\") \(.name) [\(.app.slug)] \(.html_url)\"") || runs=""
  reviews=$(query "repos/$repo/pulls/$pr/reviews" --paginate \
    -q ".[] | select(.user.login|$is_greptile) | select(.submitted_at > \"$since\") | \"review \(.state) \(.user.login) \(.submitted_at) \(.html_url)\"") || reviews=""
  comments=$(query "repos/$repo/issues/$pr/comments" --paginate \
    -q ".[] | select(.user.login|$is_greptile) | select(.created_at > \"$since\" or .updated_at > \"$since\") | \"comment \(.user.login) created=\(.created_at) updated=\(.updated_at) \(.html_url)\"") || comments=""
  inline=$(query "repos/$repo/pulls/$pr/comments" --paginate \
    -q ".[] | select(.user.login|$is_greptile) | select(.created_at > \"$since\") | \"inline \(.user.login) \(.path):\(.line // .original_line) \(.html_url)\"") || inline=""

  activity=$(printf '%s\n%s\n%s\n%s\n' "$runs" "$reviews" "$comments" "$inline" | sed '/^$/d')
  running=$(printf '%s\n' "$runs" | grep -v '^completed ' | sed '/^$/d')

  if [ -n "$activity" ] && [ -z "$running" ]; then
    echo "Greptile responded after $since (head $head):"; echo "$activity"; exit 0
  fi
  if [ -z "$activity" ] && [ "$elapsed" -ge "$grace_min" ]; then
    echo "No Greptile check run, review, or comment started within $grace_min min of $since ($elapsed min ago; head $head)."; exit 2
  fi
  if [ "$elapsed" -ge "$timeout_min" ]; then
    echo "Greptile started but did not finish within $timeout_min min:"; echo "$activity"; exit 3
  fi
  sleep 60
done
