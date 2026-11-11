---
name: pr-check-incremental
description: Address review feedback and failing CI checks on the pull request associated with the current chat. Implement and verify fixes, post GitHub replies, resolve addressed Greptile-only threads, and leave human review threads unresolved. Use for /pr-check-incremental or requests to address PR comments and CI failures.
---

# Address PR comments and CI checks

Fix actionable feedback and failing CI checks on the PR associated with this conversation. Resolve addressed Greptile-only threads; human reviewers decide when to resolve their threads.

## Find the PR and feedback

- Prefer the PR explicitly identified in the current request or established by this conversation. Otherwise, inspect the current repository and branch and find its open PR. For GitHub, use `gh pr view --json number,url,headRefName,baseRefName`.
- Confirm that the checkout matches the PR's repository and head branch before editing. Preserve unrelated local changes. If multiple PRs are plausible or none can be identified, ask for the target instead of guessing.
- Fetch inline review threads, their replies and resolution status, review bodies, and general PR discussion. Paginate every collection. On GitHub, `gh pr view --comments` alone does not provide a complete inventory of inline threads; use the API for those.
- Include actionable feedback embedded in bot review summaries, including comments outside the diff. Record links so each finding can be traced to its source.

## Address the feedback

- Focus on unresolved feedback. Read each discussion in full and check the current code before deciding whether a change is needed. An outdated diff location does not mean the concern is fixed. Leave already-resolved threads alone unless the user explicitly includes them.
- Group duplicate requests and implement the smallest correct fix for each valid finding. Follow the repository's instructions and run checks appropriate to the affected behavior.
- Before patching a bug, ask whether a small architectural change would remove it at the root: moving a responsibility to the module that owns the data, deleting a duplicated code path, deriving a value instead of syncing it, or narrowing a type so the bad state can't be expressed. Be especially suspicious when several comments are variations of the same bug. If such a change is simpler than the patch (similar or smaller diff, fewer special cases), prompt the user with both options, each with a one-line sketch and the files it touches, and wait for their choice before changing that code. If no such change is clearly simpler, patch as normal and say nothing.
- If feedback is already addressed, incorrect, blocked, or needs a product decision, explain the evidence or missing decision. Do not change correct behavior merely to satisfy a comment. Continue with independent fixes while a question is pending.
- Honor existing authorization to commit and push. Otherwise, leave verified changes in the workspace and clearly report that they have not been pushed. Do not merge the PR or start a recurring monitoring loop as part of this skill.

## Address CI checks

- Inspect checks for the PR's current head commit. On GitHub, use `gh pr checks` and inspect failed job logs with `gh run view --log-failed`; follow external check links when the logs live elsewhere.
- Diagnose each failure before editing. Fix code, tests, or configuration responsible for the failure and run the relevant checks locally. Do not weaken checks or disable tests to make CI pass.
- Distinguish code failures from infrastructure, credentials, or transient runner problems. Retry a transient failure when authorized and useful; report blockers that require external action.
- After authorized pushes, recheck CI on the new head commit and address failures caused by the changes. Do not report older successful runs as validation of the current commit. Report pending or blocked checks explicitly, and stop retrying when the same external blocker persists without new evidence.

## Preserve reviewer control

- Resolve a thread only when it was opened by Greptile (`greptile-apps` or `greptile-apps-staging`, with or without the API’s `[bot]` suffix), contains no human reviewer comments, and every finding is verified as fixed, already addressed, or a false positive. An assistant-authored status reply posted through the user account does not count as human reviewer feedback when its provenance is known.
- Leave threads opened by humans, and Greptile threads containing human reviewer feedback, unresolved even after fixing them. If authorship is uncertain, leave the thread unresolved.
- Before resolving a Greptile-only thread, post or verify an evidence-based reply explaining its disposition. Never resolve a thread with pending work or an unverified fix.
- Never minimize, hide, or delete review comments or threads. Do not reopen already-resolved threads.
- Always post a GitHub reply on each review thread you address, including when no code change is needed. A request to address PR feedback authorizes these replies; do not ask for separate permission. Keep each reply specific: what changed or why no change is needed, code links, and verification results. Do not claim a fix is available on the PR until it has been pushed.
- When rechecking feedback, avoid duplicate fixes and replies. Finish after addressing the fetched feedback and validating the changes; report newly discovered blockers without waiting indefinitely for reviewers.

## Report back

Use concise jot notes with the PR link, addressed feedback linked to changes and posted replies, verification results, current CI status, and any deferred findings or failing checks with reasons. Identify the affected components and their responsibilities. State whether changes are local or pushed, which Greptile-only threads were resolved, and confirm that human review threads remain unresolved.
