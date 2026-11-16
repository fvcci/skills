# A theory of code quality

## In short

Code quality is the cost of the next change. Good code keeps that cost low.

A change has three costs.

| Cost | Question | In this doc |
|---|---|---|
| Reading | How much must I understand first? | Covered |
| Reach | How many places must I edit? | Covered |
| Risk | How do I know I broke nothing? | Out of scope. Greptile reviews cover it. |

Reading and reach come from two causes. Each cause gives you one job, placement or clarity.

| Cause | Job | What it lowers |
|---|---|---|
| Things live in the wrong place | Placement: put things in the right place | Reach, and most of reading |
| A place is hard to follow | Clarity: make each place clear | The rest of reading |

## Principles

1. **A design is a trade-off, decided on what you know now.** Every boundary makes one kind of change cheap and another expensive. No architecture is correct. The module's context decides. Nobody knows the future, human or agent. So decide from today's facts. Only a choice that is hard to reverse is a real bet.
2. **A smell is a hint, and its fix is a trade-off too.** A smell marks a place to look, and the context decides whether there is a problem. A fix sets a boundary: extracting, inlining, splitting and merging all move where things sit. So a fix can remove one smell and create another, and the two have to be weighed against each other.
3. **Start small and expand when needed.** Keep code next to the one place that uses it, and keep things that change together in one place. Do this even when you expect reuse. Two call sites is a coincidence; three is a pattern. Duplicate until then, and move something into its own function or file at the third use. Before that, a separate piece is a guess about the future that costs reading today.
4. **Simple means simple for the caller.** A deep module gives callers a lot of behavior for little to learn. Its inside may be complex.
5. **Change rate draws the boundaries.** Things that change together sit together. Stable things sit apart.

## Placement: put things in the right place

Two forces set where things go.

- **Reach pulls things together.** Things that change together pull toward one place, like gravity.
- **Reading pushes both ways.** Too much in one place is hard to hold in your head. Too many small pieces is just as hard, because you must read all of them to follow one thing.

A deep module answers both forces. A lot of behavior sits inside it, and outsiders read only its small interface.

So split only when a caller can use one part without reading the other. If you must read both parts to understand either, merge them.

## Where each part is put to work

This document is the hub. The skills below repeat parts of it on purpose, each for one job:

- **The smells:** [SMELLS.md](SMELLS.md). Every named smell, with the cost it adds and its fix. The smells are listed there and not here.
- **`sniff`:** finds those smells at the end of a change and fixes or reports them.
- **`codebase-design`:** the words for modules, interfaces and depth, and the deletion test.

## Sources

The sources of this theory, and who contributed what, are in this folder's README.
