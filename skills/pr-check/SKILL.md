---
name: pr-check
description: >
  Check a PR for unresolved review comments, T-Rex/G-Rex test failures, and CI status
  checks, then loop fixing issues until none remain and finish with a Greptile Apex
  review. Parses Greptile review bodies and
  follow-up comments for "Comments Outside Diff" suggestions that never appear as inline
  threads. Use when the user asks to check, triage, or clear a PR's review feedback, or
  says "pr-check".
disable-model-invocation: false
license: MIT
compatibility: Requires git and gh (GitHub CLI) authenticated against the repo.
metadata:
  author: greptileai
  version: '1.0'
---

# PR Check

Check a PR for review comments, test failures, and status checks — then iteratively fix issues until none remain.

## Inputs

- **PR number** (optional): if not given, resolve the PR for the current branch.

## Instructions

### 1. Identify the PR

If a PR number was passed, use it. Otherwise:

```bash
gh pr view --json number,headRefName -q '{number: .number, branch: .headRefName}'
```

### 2. Wait for checks, and act on what arrives

Review bot comments (Greptile, T-Rex) only exist once their checks finish. Wait with
[references/wait-for-ci.sh](references/wait-for-ci.sh), run in the background:

```bash
references/wait-for-ci.sh <PR> <since>
```

For the first run, `<since>` is the PR's creation time
(`gh pr view <PR> --json createdAt -q .createdAt`). After that it is the `next-since` the
script printed last, or the time recorded just before a push (`date -u +%FT%TZ`).

It returns as soon as there is something to act on, so you work on feedback while the
other checks run:

- **Exit 4**: a check failed, or a review or comment arrived from Greptile, T-Rex / G-Rex,
  or a person, and other checks are still running. Start steps 3–8 on what it printed,
  then run it again with the printed `next-since`.
- **Exit 0**: no check is pending. Continue with step 3.
- **Exit 3**: checks were still running after 45 minutes. Report which.

### 3. Fetch PR state

```bash
gh pr view <PR> --json title,body,state,reviews,comments,headRefName,statusCheckRollup
gh api --paginate repos/{owner}/{repo}/pulls/<PR>/comments
```

Read the full discussion, including replies and resolved threads, before acting on
Greptile feedback. Preserve comment authors, URLs, and timestamps so conflicting
requests can be attributed and shown to the user. Paginate reviews and general PR
comments as needed; the thread query's first comment alone is not enough.

### 4. Check each area

**A. Status checks** — all CI passing? For each failure, identify which check and why.

**B. PR description** — complete, follows team conventions, no leftover TODOs or placeholders.

**C. Inline review comments** — unresolved threads via the GraphQL query in
[references/graphql.md](references/graphql.md). Cover `greptile-apps[bot]`,
`greptile-apps-staging[bot]`, and human reviewers.

**D. Review body summaries** — `gh pr view <PR> --json reviews`. Greptile reviews carry a
confidence score (e.g. `3/5`) and often a collapsible
`<details><summary>Comments Outside Diff (N)</summary>` block. **Those comments contain
actionable `suggestion` blocks that are never posted as inline threads** — parse every
review body from both Greptile bots and extract file paths, line numbers, and suggested
changes.

**E. General PR comments** — `gh pr view <PR> --json comments`. Greptile also posts
follow-up *comments* (not reviews) with the same "Comments Outside Diff" format. Parse
those too, plus human discussion. Vercel and similar bot comments are informational.

**F. Generated test reports (T-Rex / G-Rex)** — find the **latest** "Generated Tests"
comment by timestamp; earlier ones are stale. Parse "Potential Issues" and "Failed tests
(root cause summary)". Treat "External Problems" as candidate real bugs. Distinguish
genuine code bugs from test-runner artifacts (e.g. a test importing a function that does
not exist).

### 5. Categorize every issue

- **Needs user decision** — Greptile feedback conflicts with a user comment or instruction
- **Actionable** — needs a code, test, or docs change
- **Informational** — verification note, question, FYI
- **False positive** — flagged incorrectly
- **Already addressed** — resolved by existing code

Before classifying Greptile feedback as actionable or dismissing it, compare its
requested change with user comments in the PR discussion, review threads, and current
conversation. A conflict exists when following Greptile would contradict a requested
behavior, constraint, or explicit decision to retain the existing code. Check replies
and comments outside the diff too, including feedback from the final Apex review.
If the intended behavior is ambiguous, ask the user rather than assuming agreement.

For each conflict:

- Mark it **Needs user decision** and show the conflicting requests with authors and
  links. For a chat instruction, quote the relevant text instead of inventing a link.
- Explain what each choice would change and ask the user which direction to take.
- Pause changes, dismissal, and thread resolution for that item until the user decides.
  A general instruction to fix feedback does not settle a specific conflict. Continue
  independent, non-conflicting work while waiting.
- Apply the user's decision and carry it forward through later review iterations.
  Repeated Greptile feedback does not override that decision. Ask again only if new
  feedback creates a materially different conflict.

### 6. Report

| Area | Issue | Status | Action Needed |
| ---- | ----- | ------ | ------------- |

### 7. Fix

If actionable items exist: switch to the PR branch if not already on it, ask the user
whether to fix, and if yes make the fixes.
Exclude items awaiting a user decision from these fixes.

### 8. Resolve threads

Resolve threads that were fixed or deemed informational, using the mutation in
[references/graphql.md](references/graphql.md). Batch multiple resolutions into one
mutation with aliases (`t1`, `t2`, …).
Leave threads with an undecided conflict unresolved.

End every comment or reply you post on the PR with `<!-- agent -->` on its own line,
except the Apex request in step 10. Agents post under the user's login, and
`wait-for-ci.sh` treats an unmarked comment from that login as the user's own and stops
on it.

### 9. Loop — commit, push, re-check (max 5 iterations)

a. Commit and push the fixes:

```bash
git add <specific files>
git commit -m "fix: address review feedback (iteration N)"
git push
```

b. Wait for checks again as in step 2, with the time recorded just before the push as
`<since>`.

c. Re-run steps 4–8 against the new results — new Greptile comments, new T-Rex failures,
CI failures, remaining unresolved threads.

d. **Exit** when any of these holds:
- A conflict still needs a user decision after independent work is done: report it and
  wait for the user; do not proceed to Apex or declare the PR check complete
- Zero unresolved threads AND zero T-Rex failures AND all CI green: proceed to step 10
- 5 iterations reached
- Only informational items / false positives remain: proceed to step 10

e. If actionable issues remain, present them and ask whether to fix. Continue on yes, exit
on skip/stop.

### 10. Final Greptile Apex review

Once the ordinary check-and-fix loop is clear, make Apex the last review before
declaring the PR check complete. Record the current PR head SHA and post this exact
comment on the PR:

```bash
gh pr view <PR> --json headRefOid -q .headRefOid
gh pr comment <PR> --body '[greptile](greptile) run an apex review'
```

Record the request time (`date -u +%FT%TZ`) and wait as in step 2, also requiring a
Greptile response after that time:

```bash
references/wait-for-ci.sh <PR> <request-time> --greptile-since <request-time>
```

With `--greptile-since` it counts any Greptile response after that time: a check run
(waited on until it completes), a review, an inline comment, or an edit to an existing
comment. Greptile updates its summary comment in place, so watching only for new comments
misses a finished review. Exit 2 means nothing started within the 15-minute grace period:
report that Apex did not start instead of waiting longer. On exit 4, keep the same
`--greptile-since` when you run it again. Existing green checks or an older
Greptile review do not establish completion; verify that the new review follows this
request and covers the recorded head SHA. Read its review body, inline comments, and
follow-up comments, including "Comments Outside Diff", using steps 4–8.

If Apex finds actionable issues, handle them through the same fix-and-recheck loop.
After any new commits, wait for CI and ordinary reviews to clear, then request Apex
again on the new head so Apex remains the final review. Count these fix iterations
toward the same five-iteration cap. Apply the conflict gate in step 5 to Apex feedback
as well. If the cap is reached or Apex fails to complete,
report the remaining issues or incomplete review instead of declaring success.

### 11. PR chains

Check multiple PRs sequentially, one full pass including the final Apex review each.

## Output

After each iteration, summarize: PR title and state, iteration N of 5, status-check
summary, Greptile confidence score, unresolved threads remaining, T-Rex results, items
fixed this iteration, and items dismissed as informational or false positive (with
reasons).

Final summary when the loop exits:

| Field               | Value                   |
| ------------------- | ----------------------- |
| Iterations          | N                       |
| Greptile confidence | X/5                     |
| Final Apex review   | status, reviewed SHA, review link |
| Threads resolved    | N                       |
| T-Rex tests         | N passed, N failed      |
| CI checks           | all passing / N failing |
| Remaining issues    | N (if any)              |
| Needs user decision | N, with conflicting comment links and pending choices |

If the loop hit the iteration cap, list what is still unresolved and suggest next steps.
