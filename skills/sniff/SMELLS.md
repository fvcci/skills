# Smells

## Terms

| Term | Meaning |
|---|---|
| **Smell** | "A surface indication that usually corresponds to a deeper problem in the system" (Martin Fowler). It is quick to spot, and it is a hint, not a verdict: the context decides whether the problem is real. Here the deeper problem is the cost of the next change. |
| **Reading** | A cost of a change: how much must be understood first. |
| **Reach** | A cost of a change: how many places must be edited. |
| **Risk** | A cost of a change: how you know nothing broke. |
| **Cheapest** | The code that asks for the least reading, reach and risk. |

## Check effort

A match is a hint until a second check rules it real. Each smell's row gives the tier of that check.

| Tier | A ruling on the match needs | The second check |
|---|---|---|
| **Low** | Only the quoted lines | One agent on the other model family, at medium effort, takes every low match together |
| **Medium** | Code beyond the diff, or the request | One agent on the other model family, at high effort, for each match |
| **High** | A library fact, or a judgement about a boundary | A debate, run with the `debate` skill, its challenger and judge at high effort |

## The smells

A linked name has a detail file. The cost shares are estimates, not measurements.

| Smell | Cost it adds to the next change: its share of reading, reach and risk, as an estimate | What it is | Check effort: its tier in the table above, as an estimate | Usual fix: a starting point, since the right fix depends on the code | Smells the fix can create: fixing the smell in this row tends to cause the smells named here | Also look for it in test code | Apply `codebase-design`: the smell is about how code is split up, so load that skill and describe the match in its words |
|---|---|---|---|---|---|---|---|
| **[Mysterious Name](smells/mysterious-name.md)** | reading 100% | A function, variable, or type whose name doesn't reveal what it does or holds. | low | Rename it; if no honest name comes, the design's murky. | Second Name, Not Their Word | yes |  |
| **[Comment Says What](smells/comment-says-what.md)** | reading 100% | A comment that says what the code already says. | low | Delete it; a comment earns its place only with a why. |  | yes |  |
| **[Unnamed Condition](smells/unnamed-condition.md)** | reading 100% | A condition with three or more `&&` or `\|\|`, or one that needed a comment to be understood. | low | Give its parts named booleans. | Mysterious Name | yes |  |
| **[Deep Nesting](smells/deep-nesting.md)** | reading 70%, reach 30% | A function four blocks deep or more: its body is one, and each `if`, loop or other block inside a block adds one. | low | Invert conditions and return early. Then extract an inner block into its own function. | Speculative Generality, Mysterious Name |  |  |
| **Clever Code** | reading 100% | A dense or clever expression that takes minutes to decode. | low | Write it the plain way, in steps with named parts. |  | yes |  |
| **Unexplained Choice** | reading 70%, risk 30% | A surprising choice with no reason given, such as an odd data shape kept for an old constraint. | medium | Say why in a comment at the code. Write a decision record when the choice is hard to reverse, surprising without context, and picked over a real alternative. | Comment Says What |  |  |
| **[Speculative Generality](smells/speculative-generality.md)** | reading 70%, reach 30% | Abstraction, parameters, or hooks added for needs the spec doesn't have. | medium | Delete it; inline back until a real need shows. | Duplicated Code | yes | yes |
| **Middle Man** | reading 70%, reach 30% | A class or function that mostly just delegates onward. | medium | Cut it, call the real target direct. | Message Chains | yes | yes |
| **Duplicated Code** | reach 70%, reading 30% | The same definition, value, rule or logic, more than a single `if` or `try/catch`, written in two or more places, counting a place the codebase already has it. | high | Keep one copy and have the others use it or derive from it. | Middle Man, Speculative Generality |  | yes |
| **[Feature Envy](smells/feature-envy.md)** | reach 50%, reading 50% | A method that reaches into another object's data more than its own. Or a caller that does setup another module owns, such as building its client, fetching its URL or writing its config, and then hands the result over. | high | Move the work to its owner: the method onto the data it envies, the setup into the module. | Divergent Change, Middle Man |  | yes |
| **Data Clumps** | reach 70%, reading 30% | The same few fields or params keep travelling together (a type wanting to be born). | medium | Bundle them into one type, pass that. | Speculative Generality |  | yes |
| **Primitive Obsession** | reach 70%, reading 30% | A primitive or string standing in for a domain concept that deserves its own type. | medium | Give the concept its own small type. | Speculative Generality |  | yes |
| **Repeated Switches** | reach 100% | The same `switch`/`if`-cascade on the same type recurs across the change. | medium | Replace with polymorphism, or one map both sites share. | Refused Bequest, Speculative Generality |  | yes |
| **Shotgun Surgery** | reach 100% | One logical change forces scattered edits across many files in the diff. | high | Gather what changes together into one module. | Divergent Change |  | yes |
| **Divergent Change** | reading 70%, reach 30% | One file or module is edited for several unrelated reasons. | high | Split so each module changes for one reason. | Shotgun Surgery |  | yes |
| **Message Chains** | reach 70%, reading 30% | Long `a.b().c().d()` navigation the caller shouldn't depend on. | medium | Hide the walk behind one method on the first object. | Middle Man |  | yes |
| **Refused Bequest** | reading 70%, reach 30% | A subclass or implementer that ignores or overrides most of what it inherits. | medium | Drop the inheritance, use composition. | Middle Man |  | yes |
| **Inappropriate Intimacy** | reach 70%, risk 30% | Code that reaches into another module's internals, such as importing its inner files. | high | Import through the interface only. | Middle Man |  | yes |
| **Unstable Dependency** | reach 70%, risk 30% | Many things depend on something that changes often, such as a shared helper that changes weekly. | high | Depend toward stable things. | Duplicated Code |  | yes |
| **Hidden Requirement** | reading 70%, risk 30% | Something a caller must know that the interface does not say: ordering, error cases, or required setup. | medium | Put what callers must know at the interface. |  |  | yes |
| **Sometimes-There Field** | reach 70%, risk 30% | A new field written on some records and left out of others. | medium | Always write it, empty when there is no value. | Made-Up Value |  |  |
| **Second Name** | reading 70%, reach 30% | One thing given two names, or a new name where the code already has one. | medium | Use the name that exists. |  |  |  |
| **Built-In By Hand** | reading 70%, reach 30% | Code that does by hand, or the long way round, what the language, a library already in use, or the codebase has a feature or a simpler way for. | high | Use the feature or the simpler way. |  |  |  |
| **Not Their Word** | reading 100% | A name, construct, or place the user gave, swapped for a near equivalent. | medium | Use theirs. |  | yes |  |
| **Made-Up Value** | risk 100% | A stored field set to an invented label, zero, or sentinel when the real value is in scope. | medium | Store the real value, or nothing. | Sometimes-There Field |  |  |
| **Silenced Check** | risk 100% | A lint or type check turned off, or a caught error dropped. | low | Fix it or report it. |  |  |  |
| **Test Bent To Pass** | risk 100% | A test narrowed until it passes, or one that pins a halfway state. | medium | Point it at the new behaviour. |  | yes |  |
| **Fragile Test** | reach 70%, risk 30% | A test tied to the implementation: it asserts private state, internal call order, or which helper ran, so it breaks on a refactor while still describing correct behavior. | medium | Test at the interface, so the test survives a rewrite of the inside. |  | yes | yes |
| **[Test Guards Nothing](smells/test-guards-nothing.md)** | risk 100% | A test no regression can fail: it asserts removed code is gone, mocks the unit under test, checks what the type system or the platform guarantees, or computes its expected value with the code's own logic. | medium | Delete it. Where it also covers behavior something relies on, rewrite it against that behavior. |  | yes |  |
| **Duplicate Test** | reach 70%, reading 30% | A test that guards behavior another test already guards. | medium | Delete the copy. |  | yes |  |
| **Test-Only Production Code** | reading 70%, risk 30% | Production code that exists only for tests, such as a reset hook or a getter that exposes internals. | medium | Delete it with the test that used it, or have the test go through the interface. |  |  |  |
