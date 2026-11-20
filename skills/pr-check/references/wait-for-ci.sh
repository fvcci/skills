#!/usr/bin/env bash
# Wait on a PR until there is something to act on, or until its checks are done.
#
# Usage: wait-for-ci.sh <PR> <since> [--timeout MIN] [--greptile-since TIME [--grace MIN]]
#   <since>           ISO-8601 UTC. Only activity after it is reported.
#   --timeout MIN     stop after MIN minutes of waiting (default 45)
#   --greptile-since  also require a Greptile response after TIME, e.g. the time an Apex
#                     review was requested. A late start does not extend the grace period.
#   --grace MIN       minutes after --greptile-since for Greptile to start (default 15)
#   e.g. wait-for-ci.sh 19031 2026-11-12T22:44:03Z --greptile-since 2026-11-12T22:44:03Z
#
# Activity is anything after <since> that you can act on:
#   - a check that failed
#   - a Greptile review, inline comment, or comment that was created OR edited
#     (Greptile edits its summary in place)
#   - a "Generated Tests" comment (T-Rex / G-Rex)
#   - a review or comment from a person; the gh user's own count unless they end
#     with <!-- agent -->, because agents post under that login
# Exit codes: 0 no check is pending (and Greptile responded, when required)
#             4 activity arrived while other checks still run: act on it, then run again
#               with the printed next-since
#             2 Greptile started nothing within the grace period
#             3 checks still running at the timeout
#             1 bad arguments or gh failed. Network errors are retried.
set -u
[ $# -ge 2 ] || { echo "usage: wait-for-ci.sh <PR> <since> [--timeout MIN] [--greptile-since TIME [--grace MIN]]" >&2; exit 1; }
pr=$1 since=$2 timeout_min=45 greptile_since="" grace_min=15
shift 2
while [ $# -gt 0 ]; do
  case $1 in
    --timeout) timeout_min=$2 ;;
    --greptile-since) greptile_since=$2 ;;
    --grace) grace_min=$2 ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
  shift 2
done
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner) || exit 1
me=$(gh api user -q .login 2>/dev/null) || me=""
epoch() { date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$1" +%s 2>/dev/null || date -u -d "$1" +%s; }
greptile_start=""
if [ -n "$greptile_since" ]; then greptile_start=$(epoch "$greptile_since") || exit 1; fi

is_greptile='test("(?i)greptile")'
who="(if (.user.login|$is_greptile) then \"greptile\" else \"other\" end)"
# Greptile, the generated-test bots, and people. Other bots (Vercel and the like) are informational.
# Agents post as the gh user, so that login's comments count unless an agent marked them.
# Its empty-bodied reviews only wrap inline comments, which the inline query reports.
agent_wrote="((.body // \"\") as \$b | \$b == \"\" or (\$b | test(\"<!-- agent -->|run an apex review\")))"
can_act="((.user.login|$is_greptile) or ((.body // \"\")|test(\"Generated Tests\")) or (.user.type == \"User\" and ((.user.login == \"$me\" and $agent_wrote) | not)))"

query() { # retry transient API failures instead of treating them as "no activity"
  local out
  for _ in 1 2 3; do out=$(gh api "$@" 2>/dev/null) && { printf '%s' "$out"; return 0; }; sleep 10; done
  return 1
}
after() { awk -v t="$1" '$1 > t'; } # lines start with an ISO time, which sorts as text
finish() { echo "next-since: $now"; exit "$1"; }

SECONDS=0
while :; do
  now=$(date -u +%FT%TZ)
  head=$(query "repos/$repo/pulls/$pr" -q .head.sha) || { sleep 60; continue; }

  # `gh pr checks` covers check runs and commit statuses. It exits non-zero while checks are pending or failed.
  checks=$(gh pr checks "$pr" --json bucket,completedAt,name,link \
    -q '.[] | "\(.completedAt // "-") \(.bucket) \(.name) \(.link)"' 2>/dev/null)
  pending=$(printf '%s\n' "$checks" | awk '$2 == "pending"')
  failed=$(printf '%s\n' "$checks" | awk '$2 == "fail"')

  runs=$(query "repos/$repo/commits/$head/check-runs" --paginate \
    -q ".check_runs[] | select((.name|$is_greptile) or (.app.slug|$is_greptile)) | select(.started_at != null) | \"\(.started_at) greptile check \(.status) \(.conclusion // \"-\") \(.name) [\(.app.slug)] \(.html_url)\"") || runs=""
  reviews=$(query "repos/$repo/pulls/$pr/reviews" --paginate \
    -q ".[] | select(.submitted_at != null) | select($can_act) | \"\(.submitted_at) \($who) review \(.state) \(.user.login) \(.html_url)\"") || reviews=""
  comments=$(query "repos/$repo/issues/$pr/comments" --paginate \
    -q ".[] | select($can_act) | \"\([.created_at, .updated_at] | max) \($who) comment \(.user.login) created=\(.created_at) updated=\(.updated_at) \(.html_url)\"") || comments=""
  inline=$(query "repos/$repo/pulls/$pr/comments" --paginate \
    -q ".[] | select($can_act) | \"\(.created_at) \($who) inline \(.user.login) \(.path):\(.line // .original_line) \(.html_url)\"") || inline=""

  # What can be acted on now: feedback and failed checks since <since>. A check run that only started is not.
  activity=$(printf '%s\n%s\n%s\n%s\n' "$reviews" "$comments" "$inline" "$failed" | sed '/^$/d' | after "$since" | sort)

  greptile_done=yes
  if [ -n "$greptile_since" ]; then
    responded=$(printf '%s\n%s\n%s\n%s\n' "$runs" "$reviews" "$comments" "$inline" | after "$greptile_since" | awk '$2 == "greptile"')
    running=$(printf '%s\n' "$runs" | after "$greptile_since" | awk '$4 != "completed"')
    if [ -z "$responded" ] || [ -n "$running" ]; then greptile_done=no; fi
  fi
  # Checks take a moment to register after a push, so an empty list counts only once it has had time to fill.
  checks_done=no
  if [ -z "$pending" ] && { [ -n "$checks" ] || [ "$SECONDS" -ge 120 ]; }; then checks_done=yes; fi

  if [ "$checks_done" = yes ] && [ "$greptile_done" = yes ]; then
    echo "No check is pending (head $head)."
    if [ -n "$failed" ]; then echo "Failed checks:"; echo "$failed"; fi
    if [ -n "$activity" ]; then echo "Activity after $since:"; echo "$activity"; fi
    finish 0
  fi
  if [ -n "$activity" ]; then
    echo "Activity after $since, while other checks still run (head $head):"; echo "$activity"
    if [ -n "$pending" ]; then echo "Still running:"; echo "$pending"; fi
    finish 4
  fi
  if [ -n "$greptile_since" ] && [ -z "$responded" ] && [ $((($(date +%s) - greptile_start) / 60)) -ge "$grace_min" ]; then
    echo "No Greptile check run, review, or comment started within $grace_min min of $greptile_since (head $head)."
    finish 2
  fi
  if [ $((SECONDS / 60)) -ge "$timeout_min" ]; then
    echo "Still running after $timeout_min min (head $head):"; echo "$pending"
    finish 3
  fi
  sleep 60
done
