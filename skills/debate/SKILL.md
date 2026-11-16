---
name: debate
description: Settle contested design decisions by running a structured debate between a challenger agent and a defender agent on different models, with a judge, over files on disk. Use when Felix asks to debate, stress-test, challenge, cut down or second-guess a list of decisions (use cases, entities, modules, API shapes, names), or says "debate".
---

# Debate

Goal: a list of design decisions, each with a verdict backed by evidence and a named winner, applied to the working doc.

Two agents argue on files: the **defender** is the session that made the change, and a **challenger** on a different model proposes changes. A **judge** on yet another model settles what they leave open. The challenger and the defender each know the other exists and that a judge will rule. Neither knows the criteria the judge rules by. You orchestrate: write the brief, launch rounds, track state, apply the result.

## 1. Set up

Make a folder next to the working doc: `run/debate<N>/`. Back up the doc before anything changes: `cp <doc> run/debate<N>/<doc>.before-debate<N>.md`.

Write `run/debate<N>/BRIEF.md`. Every agent reads it first, so it holds everything the challenger and the defender need:

- **Context:** what Felix is designing, where the working doc lives, and the rules already decided (with who decided them).
- **Question:** the one thing this debate decides, in one sentence.
- **Items:** a table with an id per item (E1, UC-12, ...), where it lives today, and the related item it might merge into or split from.
- **Verdicts:** a table of the verdicts allowed and what each means (keep, merge into X, split, rename, move, remove, defer, internal-only ...). Every non-keep verdict names where callers or rules go.
- **Evidence (read-only):** the doc, data files, schema, and code at a pinned commit (`git show <sha>:<path>`). Agents check every claim in code and cite `path:line`.
- **Roles and rounds** (below), and the **output format**. Name all three roles, and say that the judge rules by criteria the debaters are not shown.

Write `run/debate<N>/JUDGE.md`. Only the judge reads it. Never give its path or its content to the challenger or the defender:

- **The test:** the criteria that decide a verdict. Take them from a past decision when one exists ("Account was merged because it had no use cases of its own, was created only as a side effect, and users saw it as one thing").
- **What "good" means:** the priorities that break ties, for example customer benefit and simplicity first, best practices only when they actually separate the two options.

For more than ~40 items, split them into batches (A, B, C ...) of related items and run one debate per batch in parallel, each in its own subfolder.

## 2. Roles

| Role | Who | Job |
|---|---|---|
| Defender | The agent session that made the change. It knows why each choice was made. | Keeps the current design where the evidence supports it, concedes where it doesn't. Counter-proposals welcome. |
| Challenger | A different model from the defender's | Proposes a change for each item where the evidence supports one. Concedes items where the evidence supports the current design. |
| Judge | A model different from the defender's, the challenger's and the orchestrator's | Took no side. Reads `JUDGE.md` as well as the brief, and rules by it. Decides every item still open, and overrules an agreement the evidence contradicts. |

Picking them:

- **Defender:** when this session made the change, defend in a `fork` started before you write `JUDGE.md`, so the defender keeps this session's context and never sees the criteria. When a subagent or delegated task made it, continue that agent with `SendMessage`. Note the defender's model.
- **Challenger and judge:** the top of the line models, at high effort. Check `orchestrator_capabilities` for the current flagships (as of Nov 2026: `claude-fable-5-1`, `gpt-6.1-sol`, `claude-opus-5-5`), then give each role the strongest one the rules above allow. Launch each turn with `delegate_task` (`mode: "async"`, settings in `target.options`). Example with an Opus 5.5 defender and orchestrator: challenger `codex` / `gpt-6.1-sol` `{"reasoningEffort":"high","serviceTier":"priority"}`, judge `claudeAgent` / `claude-fable-5-1` `{"effort":"high"}`.
- Use one `clientRequestId` per turn, e.g. `d<N>-<batch>-c<round>` and `d<N>-<batch>-judge`.

## 3. Rounds

Run challenger, then defender, for up to 3 rounds: `c1 → d1 → c2 → d2 → c3 → d3`, then the judge.

- Round 1: the challenger contests as many items as warranted, strongest first.
- Rounds 2 and 3: answer only the other side's open items. No new targets.
- An item both sides agree on is settled and leaves the next round. Stop as soon as nothing is open.

Each agent writes only its own file in the debate folder and never edits the doc, Notion or git:

- Challenger: `r<n>-challenger.md`, one entry per item: **C<n>-<id>. <item>: <verdict>**, then evidence, then the change test (which future change would touch which item).
- Defender: `r<n>-defender.md`, one entry per open item: **D<n>-<id>: accept | defend | counter-proposal**, then evidence.
- Judge: `judge.md`, one line per contested item: **<id>. <item>: <final verdict>** · winner (challenger / defender / both partly) · one-line reason. Then totals before and after.

The final message from each agent is counts by verdict plus its file path, under 100 words, in plain text.

Keep `run/debate<N>/STATE.md` current: the topic, the models and request ids, and one line per finished turn with what it settled. A resumed session picks up from this file.

## 4. Apply

1. Read the judge file, or the last round when the sides agreed on everything. Spot-check the verdicts that change the most against the code.
2. Apply the verdicts to the working doc. When there are many, use a script you can rerun (`apply_judges.py`) instead of hand edits.
3. Record the outcome in the doc's "How we built this" section: the question, the counts before and after, and one line per merge, split, rename and removal.
4. Report to Felix in a short table: item, verdict, winner, and why. Name who decided each one (a debate, Felix, or you). Ask about anything the judge flagged for him.

## Working with Felix

- Felix decides what is debated and has the last word. A debate verdict can be overruled. When citing a decision later, say it came from a debate.
- Push to Notion only when Felix asks.
- Plain words, short sentences, numbers with units, positive phrasing.
