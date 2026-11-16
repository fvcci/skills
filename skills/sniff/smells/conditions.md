# Unnamed Condition

Two triggers, either one is enough:

- **Count**: 3 or more `&&`/`||` operators combined in one condition.
- **Comment**: the condition needed a comment to be understood.

Fix: assign parts of the condition to explicitly named boolean variables, so
the `if` reads as a sentence. If a comment was there, delete it — unless it
explains the *why* of the condition (rule 1), in which case keep the why and
drop the what.

```ts
// SMELL
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
