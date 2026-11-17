# A theory of code quality

## In short

Code quality is the cost of the next change. Good code keeps that cost low.

A change has three costs.

| Cost | Question | In this doc |
|---|---|---|
| Reading | How much must I understand first? | Covered |
| Reach | How many places must I edit? | Covered |
| Risk | How do I know I broke nothing? | Covered. Greptile reviews catch much of it, and it is graded below. |

Reading and reach come from two causes. Each cause gives you one job, placement or clarity.

| Cause | Job | What it lowers |
|---|---|---|
| Things live in the wrong place | Placement: put things in the right place | Reach, and most of reading |
| A place is hard to follow | Clarity: make each place clear | The rest of reading |

## Principles

1. **A design is a trade-off, decided on what you know now.** Every boundary makes one kind of change cheap and another expensive. Event-driven, onion, hexagonal and clean architecture and domain-driven design each draw the boundaries a different way, and none is right everywhere. The work is knowing which one fits the current context. The module's context decides. Nobody knows the future, human or agent. So decide from today's facts. Only a choice that is hard to reverse is a real bet.
2. **A smell is a hint, and its fix is a trade-off too.** A smell marks a place to look, and the context decides whether there is a problem. A fix sets a boundary: extracting, inlining, splitting and merging all move where things sit. So a fix can remove one smell and create another, and the two have to be weighed against each other.
3. **Start small and expand when needed.** Keep code next to the one place that uses it, and keep things that change together in one place. Do this even when you expect reuse.
4. **Simple means simple for the caller.** A deep module gives callers a lot of behavior for little to learn. Its inside may be complex.
5. **Change rate draws the boundaries.** Things that change together sit together. Stable things sit apart.

## Placement: put things in the right place

Two forces set where things go.

- **Reach pulls things together.** Things that change together pull toward one place, like gravity.
- **Reading pushes both ways.** Too much in one place is hard to hold in your head. Too many small pieces is just as hard, because you must read all of them to follow one thing.

A deep module answers both forces. A lot of behavior sits inside it, and outsiders read only its small interface.

So split only when a caller can use one part without reading the other. If you must read both parts to understand either, merge them.

## How to grade code quality

Grade code from 1 to 10 by how cheap it makes the changes it will actually get. 10 is best.

1. Name the smells in the code.
2. Add up their cost shares of reading, reach and risk from [SMELLS.md](SMELLS.md).
3. Ask which kind of change this code gets, and how often. A cost only counts when that change happens.
4. Score each row of the rubric from 1 to 10. The shares are estimates and the context decides, so overrule the numbers when it calls for it, and say why.
5. The grade is the four scores, each multiplied by its weight, added up.

The rubric applies one rule to each cost: a cost is graded by whether it fits its context. A high cost is fine where it is rarely paid, and poor where it is paid often.

| Criterion | Weight | 10 | 5 | 1 |
|---|---|---|---|---|
| **Reading** | 30% | Code that is worked on often is obvious. What is hard to read is isolated where nobody works. | Code that is worked on often takes effort to follow. | Hard-to-read code sits where developers spend their time. |
| **Reach** | 25% | The changes this code really gets touch few places. | A common change touches several places, and they are easy to find. | A change this code often gets needs edits in many places. |
| **Risk** | 35% | What a developer must know to change the code safely can be found. | It can be found, but only by reading far from the change. | Something must be known and cannot be found, so a change breaks things with no warning. |
| **The trade is deliberate** | 10% | A high cost buys a lower one elsewhere, and the reason is written down. | A high cost buys something, and no reason is written down. | A high cost buys nothing. |

Notes for scoring:

- **Reach.** Abstract code has high reach, and pays for it in reading: a caller learns the abstraction and not what sits behind it. That is fine when the abstraction is stable. It is the Unstable Dependency smell when it changes often. Concrete code is the opposite: low reach, harder to read.
- **Reading.** John Ousterhout, in *A Philosophy of Software Design*: "Isolating complexity in a place where it will never be seen is almost as good as eliminating the complexity entirely." The reader decides what is hard, not the writer: "If you write a piece of code and it seems simple to you, but other people think it is complex, then it is complex."
- **Risk.** Trade it away last. Ousterhout: "Of the three manifestations of complexity, unknown unknowns are the worst."
- **Two versions.** Grade each against the same likely changes. The higher grade wins, and on a tie the higher Risk score wins.
- **Weights.** They are a judgement, not a measurement. Risk weighs most because it is the worst of the three costs. Reading and reach are close, and the last row weighs least because it only asks whether a cost was chosen.

## Where each part is put to work

This document is the hub. The skills below repeat parts of it on purpose, each for one job:

- **The smells:** [SMELLS.md](SMELLS.md). Every named smell, with the cost it adds and its fix. The smells are listed there and not here.
- **`sniff`:** finds those smells at the end of a change and fixes or reports them.
- **`codebase-design`:** the words for modules, interfaces and depth, and the deletion test.

## Sources

- John Ousterhout, *A Philosophy of Software Design*: the three costs, as change amplification, cognitive load and unknown unknowns. The two causes, as dependencies and obscurity. Deep modules. Weighting each part by how much time is spent working on it.
- Matt Pocock's skills repo, <https://github.com/mattpocock/skills>: depth as leverage and the deletion test, in `codebase-design`, and the form of the smell list.
- Martin Fowler: the definition of a smell, from his "Code Smell" article, and twelve of the smells, from *Refactoring*, as used in Pocock's review skill.
- Robert C. Martin, *Clean Architecture*: abstract and concrete.
- Adam Tornhill, *Your Code as a Crime Scene*: files that change together.
