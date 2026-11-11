---
name: notion-doc-writing
description: House style for writing or rewriting Notion docs (product scopes, design docs, proposals, how-tos). Use whenever creating or editing a Notion page someone else will read.
---

# Notion doc writing

Goal: a reader gets the point in 10 seconds and can act on it without asking questions.

## Voice
- Write as the owner of the doc ("we", "our"), not as an assistant reporting back.
- State decisions and facts directly. No hedging, no "I think", no "it seems".
- No process commentary: no "per Slack thread", "after investigating", "X suggested", audit notes or research history. The doc is the outcome, not the story of how you got there.

## Density
- Lead with the point: first 1-3 lines say what this is, what we're doing, and why.
- Cut filler, repetition, and restated context. If a sentence can go without losing information, delete it.
- Prefer short headings, concrete bullets, and compact tables/comparisons over paragraphs.
- One idea per bullet. Use numbers, names, and examples instead of adjectives ("p50 drops 40s to 12s", not "much faster").
- Keep it short. If it runs past a screen or two, split details into a child page or a toggle.

## Structure (pick what fits, drop empty sections)
- **Product/scope:** Problem -> Goal (measurable) -> Scope (in / out) -> Approach -> Open questions.
- **Design doc:** Problem -> Functional Requirements -> Non Functional Requirements -> Non Requirements -> Design -> Open Questions.
- **How-to:** Prereqs -> numbered steps -> how to verify.
- Open questions and risks are bullets with an owner, not prose.

## Visuals
- Add a diagram or mock when it explains faster than text (architecture, flows, UI ideas). Embed it near the top of the relevant section.
- Use tables for any comparison of 2+ options.

## Notion mechanics
- Search for an existing page first; update it rather than creating a duplicate. Confirm the parent before creating.
- Use real Notion blocks (headings, bullets, tables, toggles, callouts), not one big markdown blob.
- Link related pages, PRs, and dashboards inline instead of describing them.
- After writing, reread once and cut ~20%.
