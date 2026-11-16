# Smells

## Terms

| Term | Meaning |
|---|---|
| **Smell** | "A surface indication that usually corresponds to a deeper problem in the system" (Martin Fowler). It is quick to spot, and it is a hint, not a verdict: the context decides whether the problem is real. Here the deeper problem is the cost of the next change. |
| **Reading** | A cost of a change: how much must be understood first. |
| **Reach** | A cost of a change: how many places must be edited. |
| **Risk** | A cost of a change: how you know nothing broke. |
| **Cheapest** | The code that asks for the least reading, reach and risk. |

## The smells

A linked name has a detail file. The cost shares are estimates, not measurements.

| Smell | Cost it adds to the next change: its share of reading, reach and risk, as an estimate | What it is | How to fix | Smells the fix can create: fixing the smell in this row tends to cause the smells named here | Also look for it in test code | Apply `codebase-design`: the smell is about how code is split up, so load that skill and describe the match in its words |
|---|---|---|---|---|---|---|
| **[Mysterious Name](smells/names.md)** | reading 100% | A function, variable, or type whose name doesn't reveal what it does or holds. | Rename it; if no honest name comes, the design's murky. | Second Name, Not Their Word | yes |  |
| **[Comment Says What](smells/comments.md)** | reading 100% | A comment that says what the code already says. | Delete it; a comment earns its place only with a why. |  | yes |  |
| **[Unnamed Condition](smells/conditions.md)** | reading 100% | A condition with three or more `&&` or `\|\|`, or one that needed a comment to be understood. | Give its parts named booleans. | Mysterious Name | yes |  |
| **Clever Code** | reading 100% | A dense or clever expression that takes minutes to decode. | Write it the plain way, in steps with named parts. |  | yes |  |
| **Unexplained Choice** | reading 70%, risk 30% | A surprising choice with no reason given, such as an odd data shape kept for an old constraint. | Say why in a comment at the code. Write a decision record when the choice is hard to reverse, surprising without context, and picked over a real alternative. | Comment Says What |  |  |
| **[Speculative Generality](smells/yagni.md)** | reading 70%, reach 30% | Abstraction, parameters, or hooks added for needs the spec doesn't have. | Delete it; inline back until a real need shows. | Duplicated Code | yes | yes |
| **Middle Man** | reading 70%, reach 30% | A class or function that mostly just delegates onward. | Cut it, call the real target direct. | Message Chains | yes | yes |
| **Duplicated Code** | reach 70%, reading 30% | The same logic shape, more than a single `if` or `try/catch`, appears in three or more hunks or files in the change. | Extract the shared shape, call it from each. | Middle Man, Speculative Generality |  | yes |
| **Feature Envy** | reach 50%, reading 50% | A method that reaches into another object's data more than its own. | Move the method onto the data it envies. | Divergent Change |  | yes |
| **Data Clumps** | reach 70%, reading 30% | The same few fields or params keep travelling together (a type wanting to be born). | Bundle them into one type, pass that. | Speculative Generality |  | yes |
| **Primitive Obsession** | reach 70%, reading 30% | A primitive or string standing in for a domain concept that deserves its own type. | Give the concept its own small type. | Speculative Generality |  | yes |
| **Repeated Switches** | reach 100% | The same `switch`/`if`-cascade on the same type recurs across the change. | Replace with polymorphism, or one map both sites share. | Refused Bequest, Speculative Generality |  | yes |
| **Shotgun Surgery** | reach 100% | One logical change forces scattered edits across many files in the diff. | Gather what changes together into one module. | Divergent Change |  | yes |
| **Divergent Change** | reading 70%, reach 30% | One file or module is edited for several unrelated reasons. | Split so each module changes for one reason. | Shotgun Surgery |  | yes |
| **Message Chains** | reach 70%, reading 30% | Long `a.b().c().d()` navigation the caller shouldn't depend on. | Hide the walk behind one method on the first object. | Middle Man |  | yes |
| **Refused Bequest** | reading 70%, reach 30% | A subclass or implementer that ignores or overrides most of what it inherits. | Drop the inheritance, use composition. | Middle Man |  | yes |
| **Inappropriate Intimacy** | reach 70%, risk 30% | Code that reaches into another module's internals, such as importing its inner files. | Import through the interface only. | Middle Man |  | yes |
| **Unstable Dependency** | reach 70%, risk 30% | Many things depend on something that changes often, such as a shared helper that changes weekly. | Depend toward stable things. | Duplicated Code |  | yes |
| **Hidden Requirement** | reading 70%, risk 30% | Something a caller must know that the interface does not say: ordering, error cases, or required setup. | Put what callers must know at the interface. |  |  | yes |
| **Sometimes-There Field** | reach 70%, risk 30% | A new field written on some records and left out of others. | Always write it, empty when there is no value. | Made-Up Value |  |  |
| **Second Name** | reading 70%, reach 30% | One thing given two names, or a new name where the code already has one. | Use the name that exists. |  |  |  |
| **Built-In By Hand** | reading 70%, reach 30% | Code that redoes what the language, an imported library, or the codebase already does. | Use that. |  |  |  |
| **Not Their Word** | reading 100% | A name, construct, or place the user gave, swapped for a near equivalent. | Use theirs. |  | yes |  |
| **Made-Up Value** | risk 100% | A stored field set to an invented label, zero, or sentinel when the real value is in scope. | Store the real value, or nothing. | Sometimes-There Field |  |  |
| **Silenced Check** | risk 100% | A lint or type check turned off, or a caught error dropped. | Fix it or report it. |  |  |  |
| **Test Bent To Pass** | risk 100% | A test narrowed until it passes, or one that pins a halfway state. | Point it at the new behaviour. |  | yes |  |
| **Fragile Test** | reach 70%, risk 30% | A test tied to the implementation: it breaks on a refactor while still describing correct behavior. | Test at the interface, so the test survives a rewrite of the inside. |  | yes | yes |
