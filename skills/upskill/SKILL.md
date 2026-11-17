---
name: upskill
description: >
  Turn a workflow that misfired into a durable change in the skill that governs it.
  Proposes exact wording, waits for approval, applies it, then replays the task in a
  subagent until the mistake is gone. Use when Felix says
  "upskill" or asks what a skill should have told you, and offer it after a skill is
  followed faithfully and still produces a bad result.
---

# upskill

## Why

- A skill is executed, not consulted. A missing step does not read as a gap, it reads as
  nothing at all, so the failure looks like judgement rather than instruction.
- The moment after a workflow goes wrong is the only time its cause is visible. Later
  there is a bad outcome and a procedure that still looks sound.
- Skills are obeyed more literally than preferences, so a wrong step does more damage
  than a wrong preference. Hence approval before applying.

## Goal

A skill that fires correctly more often, not a longer skill.

- Sharpening an existing step beats adding one.
- Deleting a step that caused the problem is a complete result.
- "The skill already said this" is a successful run, and the most common one.
- Length is a real cost here. Every step competes for attention with every other step at
  the moment of execution.

## Budget

- Each round: under 400 words of output, including the proposed wording.
- One step per round, two at most.
- Read the section you would change plus its neighbours. Not the whole skill.
- If you cannot point at the step that should have caught it, stop and say so.

## First, is it the skill's fault?

Ask before anything else, because this is where skills get bloated.

Quote the line that should have prevented the outcome. If such a line exists and was
simply not followed, **the skill is fine** — say so and stop. Restating an instruction
louder does not make it more likely to be followed the third time; it makes the skill
longer and every other instruction weaker.

A skill defect looks like one of these:

| Symptom | Change |
| --- | --- |
| Step named an intent, not an observable signal | Name the exact field, command, or value |
| Step was right but fired too late to matter | Move it earlier; ordering is the fix |
| Two steps could both apply and disagree | Say which wins |
| Step assumed a precondition that was not checked | Add the check, not a warning |
| Step existed only for a case that never happens | Delete it |

## Process

1. Name the decision that went wrong, and when it was made. Skills fail at a moment.
2. Apply the test above. Most runs end here.
3. Find the section that executes at that moment. A correct rule in the wrong section
   fires after the damage.
4. Check it does not contradict a neighbouring step. Skills are followed in order, so a
   contradiction is a coin flip, not a judgement call.
5. Write the exact wording, show it, stop. In a replay round (step 9), show it and
   continue.
6. Apply with Edit, one hunk. Keep the file's existing voice and heading style.
7. Read back the whole section, not just the hunk.
8. Replay the moment in a fresh subagent. Give it the task and the source files as they
   stood when the decision was made, tell it to read the edited skill, and have it write
   its result to a scratch file and send nothing outside. The brief states only the task,
   so a clean result comes from the skill. If those inputs cannot be reproduced, say so
   and skip the replay.
9. Search the scratch file for the mistake. Present: return to step 1 with the subagent's
   output as the new moment. Felix's first approval covers these rounds. Absent, or
   still present after 3 rounds: stop and report each hunk applied, the rounds run and
   what the replay left untested.

## Writing the step

- Give the signal to key on, not the goal to achieve. "Confirm it finished" is not a
  step; "confirm the footer's commit matches your head" is.
- Say what to do when the signal is absent, or the step stalls the run.
- Encode the failure mode in a clause, so the next reader knows what it is defending
  against and can tell when it stops applying.
- Explicit, not terse. This is the opposite of a preferences file: it is read once, under
  load, and executed without interpretation.
- One to three sentences. A paragraph means two steps.

## Avoid

- Applying anything unapproved.
- Adding a step for a one-off, an external outage, or a tool that was simply down.
- A rule whose real content is "be more careful".
- Duplicating a global CLAUDE.md rule into a skill. If it is true everywhere, it belongs
  there and `reflect` is the right tool.
- Growing a checklist that is already long. Ask what to remove in the same run.
