---
name: unslop-code
description: >
  Strips AI slop out of code: comments explain only WHY, names alone tell
  you WHAT, long or comment-needing conditions become named booleans, and
  YAGNI. Use on ANY coding task: writing new code, editing, refactoring, or
  reviewing. Also use whenever the user says "unslop-code" or "unslop code".
license: MIT
---

# Unslop code

Slop is code that describes itself instead of reading clearly. Every comment
restating the next line, every `data`/`result`/`handle()` name, every
five-clause `if`, every "might need this later" parameter — that's slop.
Delete it or name it.

## Persistence

ACTIVE EVERY RESPONSE once invoked. Applies to code you write and code you
touch. Off only on "stop unslop-code".

Scope: when editing existing code, unslop what you write plus what you
already have your hands in. Do not sweep an untouched file unless asked.

## The four rules

### 1. Comments express only WHY

A comment earns its place by carrying information the code cannot: a reason,
a constraint, a link, a rejected alternative, a bug it works around, a
non-obvious consequence.

Delete on sight:
- Comments that restate the line below them.
- Section banners (`// --- helpers ---`) and step narration (`// Step 3: ...`).
- Docstrings that repeat the signature in prose.
- Changelog comments (`// added retry`, `// was 5, now 10`) — git owns that.
- `// TODO` you invented yourself and don't intend to do.

```ts
// SLOP: says what the code says
// Loop through users and add active ones to the list
for (const user of users) if (user.active) active.push(user)

// GOOD: says what the code can't
// Trials count as active until the grace period ends — billing reconciles nightly.
for (const user of users) if (isActive(user)) active.push(user)
```

Keep comments that a reader would otherwise ask "why is it like this?" about.
If you can't articulate the why, there wasn't one — delete the comment.

### 2. Names alone tell you WHAT

A reader must be able to tell what a class, function, or variable is from its
name, without opening the body or tracing the assignment. If a name needs a
comment to explain it, the name is wrong — fix the name, drop the comment.

- No `data`, `info`, `result`, `temp`, `obj`, `val`, `x` for anything with meaning.
- No `handle*`, `process*`, `manage*`, `doWork` — say what happens:
  `retryFailedWebhooks`, `parsePriceRow`.
- Booleans read as assertions: `isExpired`, `hasWriteAccess`, `shouldRetry`.
- Units and currency belong in the name: `timeoutMs`, `priceUsdCents`.
- Names claim exactly what the code does. A `validateX` that also writes to
  the DB is a lie — rename it or split it.
- Short loop indices and `i`/`j` in tight scopes are fine. Scope length is the
  budget: the further a name travels, the more it has to say.

If a function needs a comment to describe what it does, either the name is too
vague or the function does too many things.

### 3. Conditions get named

Two triggers, either one is enough:

- **Count**: 3 or more `&&`/`||` operators combined in one condition.
- **Comment**: the condition needed a comment to be understood.

Fix: assign parts of the condition to explicitly named boolean variables, so
the `if` reads as a sentence. If a comment was there, delete it — unless it
explains the *why* of the condition (rule 1), in which case keep the why and
drop the what.

```ts
// SLOP
// only charge if they're on a paid plan, not in trial, and past due
if (user.plan !== 'free' && !user.trialEndsAt && user.balanceCents > 0 && !user.dunningPaused) {

// GOOD
const isPaidPlan = user.plan !== 'free' && !user.trialEndsAt
const owesMoney = user.balanceCents > 0 && !user.dunningPaused
if (isPaidPlan && owesMoney) {
```

The extracted names must be meaningful (`isPaidPlan`, not `cond1`/`checkA`).
Extract along semantic seams, not arbitrary halves. Same rule applies to
ternaries, `while`, and filter/guard predicates.

Watch for short-circuit side effects and cost: only hoist into a variable
when the operands are pure and cheap. If one is expensive or has effects,
extract it as a named function or nested guard instead of eagerly evaluating.

### 4. YAGNI

Build what was asked. Nothing for the imagined next requirement.

Cut:
- Options, flags, and config knobs with one call site passing the default.
- Abstract base classes, interfaces, and registries with one implementation.
- Generic type parameters used at one concrete type.
- `try/catch` that logs and rethrows unchanged.
- Defensive checks for states the type system or caller already rules out.
- Wrappers that only forward arguments.
- Exports nothing imports.

Two call sites is a coincidence; three is a pattern. Duplicate until then —
inline duplication is cheaper to read and delete than the wrong abstraction.

If you genuinely think something extra is needed, say it in one line and let
the user decide. Don't build it preemptively.

## Working method

When writing new code, apply all four rules as you go — do not write slop
and clean it after.

When applying unslop-code to existing code, work file by file:

1. Read the code, then delete every comment that fails rule 1.
2. Rename anything that fails rule 2, following the codebase's naming idiom.
3. Extract every condition that trips rule 3.
4. Cut every unused knob, layer, and wrapper that fails rule 4.
5. Verify behavior is unchanged — run the tests, typecheck, or lint the file.

Unslop-code edits are behavior-preserving. Renames and extractions must not change
semantics. If a fix requires a behavior change, stop and flag it separately
instead of folding it in.

## Boundaries

Leave alone:
- Public API docs, generated code, vendored files, and license headers.
- Comments that link a ticket, spec, RFC, or CVE.
- Explanations of genuinely non-obvious algorithms, invariants, or math.
- The codebase's established conventions — unslopped code still has to look
  like it belongs. Match the surrounding style.

## Reporting

Fix silently. Don't narrate the cleanup line by line and don't leave a
comment explaining what you removed. If something notable was cut — a whole
abstraction layer, a config option that looked intentional — mention it in
one sentence at the end.
