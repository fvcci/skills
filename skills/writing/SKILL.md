---
name: writing
description: Writing or rewriting docs for programmers (API design docs, architecture guides, Notion pages, Linear issues and milestones), definitions, glossaries, term tables. Also when Felix says "unslop" or asks to reword something.
---

# Writing

Goal: a programmer reads the doc once and knows what the thing is, why it exists and what to do with it. For Notion mechanics and page structure, follow `notion-doc-writing`. This skill covers the prose.

## Core habits

- **Lead with the point.** The first sentence of a doc, section or paragraph states the decision, fact or definition.
- **Plain words.** Use the word a programmer says aloud: "use" for utilize or leverage, "help" for facilitate, "many" for numerous, "if" for in the event that, "to" for in order to, "because" for due to the fact that.
- **Existing terms only.** Take labels from the code, the docs or the team's own conversations. When no word exists, describe the object in a plain phrase. Restate in one clause any ID or pointer to another doc the first time it appears: a requirement (F12), a decision ("decision 7"), a plan step ("step 5"), a table ("the hub's table"). The reader has only this doc.
- **One source per fact.** Before writing a count, a date, a caller or a list of items taken from a source doc, search the other source docs for the same noun and read every hit; with no hits, write it. When two docs give different values, leave the value out, show Felix both lines with their file paths and ask which doc wins, because a caveat in chat beside a saved claim leaves the wrong side in the doc. When a hit names a related item your list lacks (the hub says Create a review calls Publish a review), keep writing and ask Felix whether it belongs.
- **One name per quantity.** In design docs with equations, define each quantity once as a backticked variable in a code-fenced block, then use only that name in prose, tables and examples.
- **Positive phrasing.** Write what to do and what a thing is: "write one-line comments", "the parser exits with code 2". Quoted rules from external sources stay verbatim.
- **Current plan only.** A design doc, plan, milestone or ticket describes what gets built, why it has that shape and the real risks of that shape. Requirements and constraints that shaped it stay. Before saving, search the text for "replaces", "instead of", "previously", "no longer", "originally" and "not confirmed". Each hit is either plan history or an open question between Felix and the agent: cut it from the doc and say it in chat. The reader of the doc was not in the conversation and takes every sentence as the plan.
- **Own scope only.** A package or module doc describes that package. Leave out how other modules should call it.
- **Intended contract only.** An API reference documents the minimum surface a caller needs: the fields each mode uses, checked against the code. Report accepted-but-unused inputs and internal quirks to Felix in chat.

## Defining terms

Use this for glossaries, Terms sections and any sentence that defines a word.

1. **Start from the published definition.** Search online for the term's standard definition (Evans' DDD Reference, Fowler, Wikipedia, Martin, Cockburn). Write it as one plain sentence. Narrow it only as far as needed, and say so when the doc's meaning differs from the standard one. Skip quotes and inline citations. List the sources once, in a Sources section at the end.
2. **Test both sides.** Name the closest objects that are not the term (for an entity: a join row, and a value such as a date range). Then name three objects the doc already treats as the term, including one stored as part of another object (for an entity: Review, ReviewConfig and TenantMember from the hub's entity table). Word the definition so each near miss fails it and each member passes. When a member fails, the definition is too narrow: reword the definition and leave the member's classification alone. "An object with an identifier" fails, because every join row has an ID. Keep the one sentence from rule 1 and end it at the last exclusion. A clause that starts with "so", "because" or "which means" states a reason or a consequence, and goes in chat.
3. **Use the programmer's word.** Write "object", "function", "field", "caller". Words like "thing" and "item" force the reader to guess.
4. **Take any new example from the reader's own domain.** For Greptile that is a review, a repository or a merge request. The example shows the definition holding over time (the review's status changes from pending to completed and it stays the same review).
5. **Keep the table's existing columns.** Read the table before editing and change only the cell you were asked about. The Architecture guide's Terms table is Term | Meaning | Analogy, and its Analogy cells stay as they are. A new table uses Term | Definition | Example.
6. **Keep terms apart.** A definition never reuses another defined term in a different sense (for example "business rule" next to a defined Rule).

## Unslop

Scan the text for these patterns and rewrite. Keep the meaning and the intended tone. "Unslop" and "reword this" both run this pass.

**Content and language**
- Delete trailing "-ing" phrases ("highlighting...", "ensuring...", "showcasing...") or replace them with a real fact.
- Name the source for every attribution ("experts believe", "reports suggest"), or delete the sentence.
- Replace AI vocabulary with plain words: additionally, crucial, delve, enhance, foster, garner, interplay, intricate, landscape, pivotal, showcase, tapestry, testament, underscore, vibrant.
- Write "is" or "has" in place of "serves as", "stands as", "boasts", "features".
- State the point of "not just X, but Y" directly.
- Use the natural number of items in a list, whether that is two or four.
- Pick one name for a concept and repeat it. Synonym cycling makes readers wonder whether there are several concepts.
- Use "from X to Y" only for items on a real scale.

**Abstract and mannered words**
- Swap abstract metaphor nouns for the concrete word: substrate (base), wedge (add), vector (way), surface as in "API surface" (the endpoints), scaffolding, bedrock, paradigm, modality, primitive as a noun, harness as a metaphor, gold-plating (more than the job needs), ratchet, endgame (the last phase), north star, flywheel.
- Replace flourish with the literal phrase: aphorisms, rhetorical fragments, personified code ("the plan holds it"), figurative verbs ("rides along"). "A dial worth turning" becomes "a parameter worth varying".
- Name the mechanism or give a number in place of a feeling. "SQL you can read" becomes "`.toSQL()` returns the exact string sent to the database". When a sentence could appear unchanged in another project's docs, cut it.

**Sentences**
- One idea per sentence. Split any sentence the reader has to re-read.
- Use active voice and name the actor: "the compiler validates queries". Passive fits when the actor is unknown.
- Pick a stronger verb in place of an adverb, or give the measured delta ("p50 drops from 40 s to 12 s").
- Write whole sentences with articles and verbs, and spell out arrows and abbreviations. "Parser rejects bad date -> exit 2, no write" becomes "The parser rejects a bad date, exits with code 2 and writes nothing."
- Hedge once, with "may". Cut "it is important to note that" and other filler.
- End with the specific plan or fact. Cut generic conclusions ("the future looks bright").

**Formatting**
- Use periods or commas in place of em dashes.
- Use a colon before a list or an example, never as a mid-sentence connector.
- Write headings in sentence case.
- Bold only a lead-in that names an item and ends in a period, followed by new detail. A bold label that restates its line ("**Performance:** Performance improved...") becomes prose.
- Use straight quotes and no decorative emojis.

**Chat residue**
- Start with the answer. Cut "Certainly!", "Great question!", "I hope this helps" and "Let me know if...".

## Finish

Reread once and cut about 20%. Check each number for a unit, each definition against its near misses and its known members, and the title against the body's first sentence: every number and noun in the title (a Linear milestone or issue name, a page title, a heading) appears there with the same meaning. When they differ, change the title.

In a message Felix will send, run two checks before showing it. For each noun the recipient used first in the thread ("the PR", "this data"), write in your notes to Felix what it names: an existing repo, file, table or query, or, for work not yet done, which repo or file it would change. When the thread does not say, replace the noun in the message with a question that asks the recipient, because a copied word reads as if Felix knows its meaning. Then check each fact about a customer, a person or a deployment against the file, query result or message you read it in. An earlier answer from you or another agent is not a source. Cut a fact with no source, or turn it into a direct question to the recipient.

A Linear milestone is at most two sentences, then at most five goals of 25 words or fewer each. Count them before saving, and cut the longest clause from any goal over the limit. Leave out the owner: the project already names its lead. Explain only terms the team does not already use; "use case" needs no definition.
