---
name: defining-api-resource
description: Define one resource (reviews, findings, merge requests, ...) for the refactor of Greptile's existing API. Turn today's endpoints into use cases that every interface (REST, RPC, MCP) calls, then write each use case's input, output and errors. Use when Felix asks to define a resource, work out its use cases, fill a "Defining <resource>" Notion page, or organize every use case, entity and module.
---

# Defining an API resource

Goal: each of today's operations on one resource becomes one use case. It is written once, on worker v2's types, and every interface calls it. Existing callers keep working on the new use case: the web app, the CLI, MCP tools, and customer scripts on today's `/v1` and `/v2` routes.

The result is a "Defining <resource>" page with:

- a use cases table, where each row is a caller's goal with its outcome, its callers and the interfaces that expose it
- the input, output and errors of each use case
- an Endpoint comparison table that maps every existing endpoint to its use case

The finished page follows the format of "Defining reviews": the same sections in the same order (Proposal, Use case definitions, DTOs, Errors, Full objects, Endpoint comparison), with the same table columns and the same layout for each definition. Fetch that page before writing and copy its structure.

Pages:

- **Parent:** "Refactoring the existing API" (https://app.notion.com/p/406cc82c39b6815da32cd6c8b3f6cbc9). Its FRs, use case rules and request steps apply.
- **Sibling:** "Public API" (https://app.notion.com/p/40fcc82c39b681dd888ee47226c60966). It holds the customer jobs, the best practices for public routes and the published spec. Use its jobs to decide which use cases get a public route.
- **Worked example:** "Defining reviews" (https://app.notion.com/p/409cc82c39b681ffb2dee773a51b7528).

Write pages with the notion-doc-writing skill.

## Every operation at once

When Felix asks for every use case, entity and module rather than one resource, the working doc is `/Users/felix/Downloads/greptile-api-spec/use-cases-and-modules.md` (sections: Summary, Modules, Entities, Use cases, Debate outcomes, Open decisions, Group pages). Edit it there, and push to Notion only when Felix asks. The Notion hub "Defining all use cases and entities" (https://app.notion.com/p/40fcc82c39b68129a9daeac95b7148a9) and its group pages G1–G11 hold the outcomes, rules and endpoint verdicts. Before each edit, copy the md to `run/outcomes/use-cases-and-modules.before-<change>.md`. Read code at the design commit `dba87ce797` (`/tmp/dba-src`, or `git show dba87ce797:<path>`) instead of the worktree checkout. Use case definitions, DTOs and Full objects come later, per resource.

Steps 1, 5 and 6 change:

- **Step 1** starts from all 132 operation rows (658 endpoints) in the reference bundle (`/Users/felix/Downloads/greptile-api-spec/greptile-api-spec-reference.md`, Part 2 "CRUD endpoints" and "Non-CRUD endpoints"), split into groups of operations that probably share entities. Every endpoint lands in exactly one group's Endpoint comparison. Orchestration brief: `run/BRIEF.md`.
- **Step 5** runs the other way: derive the entities from the use cases (steps A–C below).
- **Step 6** marks interfaces for every use case, including internal and deferred ones.

Then organize entities, modules and use cases:

A. **Define each entity.** An entity has its own identity, its own lifecycle (its own use cases create and delete it) and its own rules.
   - Merge into the host when a thing has no use cases of its own, is created only as a side effect of the host's use cases and is shown to users as the same thing (GitHubAppUserConnection merged into Account).
   - Split when two things over one table have different rules (Entitlement for org and user grants; RepositoryEntitlement for repository grants).
   - An entity that is exactly one table takes the table's name, even when it reads oddly (Tenant, Memory, PrChatConversation).
   - Write "What it is" without the entity's own name.
B. **Record each entity's storage type** in a Type column:

   | Type | Stored as |
   |---|---|
   | 1 | One table |
   | 2 | One table plus child tables only it writes |
   | 3 | Outside our database (Stripe, Orb, S3, auth sessions) |
   | 4 | Rows sharing a table with another entity's rows; a column says which entity each row is |
   | 5 | Columns or a JSON key inside another entity's row; mark the row's owner "5 host" |
   | 6 | One entity over several tables |
   | 7 | Mid-migration: an old table and a new one |

C. **Debate types 4–7.** For each entity of those types, a challenger (GPT-6.1-Sol) argues merge, split, rename or move, and a defender (Opus 5.5) answers. Run up to 3 rounds. The orchestrator decides and records the result under Debate outcomes. Brief template: `run/debate3/BRIEF.md`.
D. **Group entities into modules.**
   - A module owns the entities whose rules change together, plus the use cases that change them. Other modules keep its ids and call its use cases.
   - Name modules after worker v2 folders where one exists.
   - A module can own use cases with no entities (`deployment`, `cli`).
E. **Place each use case in a module (rule 8).** It lives in the module whose rules decide its outcome, usually the owner of its main entity. Reads don't move it.
   - A change to another module's entity goes through that module's interface.
   - A read lives with the entity it returns, or where the question belongs.
   - When several modules keep settings on one row (a "5 host" such as Tenant), the host module is the only writer. It exposes an interface (`tenant.updateSettings`) that lets each module write only its own keys. The use case stays in the module whose rules apply.
   - Cite the sources: Vernon's Effective Aggregate Design, Fowler's DDD Aggregate, GRASP Information Expert and Fowler's CQRS.
F. **Record every entity each outcome changes.**
   - Fan out subagents in batches. Brief template: `run/outcomes/BRIEF.md`, with a table → entity map.
   - Each subagent writes `batch-<n>.tsv` with changes, returns, `path:line` evidence and notes.
   - Fill Entity (the main entity) and Also changes from the TSVs.
   - Collect the notes in `flags.md` for Felix: wrong main entity, reads that write, tables with no entity, no code found.
G. **Keep today's tables.** Each module's data access maps its entities onto the existing tables: it filters shared tables by their type column, writes JSON one key at a time and reads several tables together.
   - List bugs the storage causes under "Required code fixes".
   - Schema changes go under "Optional schema changes, not planned", unless code can't prevent the bug.
H. **Check the shape, then write the summary.**
   - Each use case names one main entity. Flag rows that name two or none.
   - An entity that is never a main entity is a merge candidate.
   - Entities table, ranked by dependents: # | Entity | Module | Type | Entities that depend on it | Use cases that depend on it | What it is.
   - Use cases table: # | Use case | Module | Entity | Also changes | Interfaces | Endpoints today | Depended on by.
   - Summary: endpoint, use case and entity counts. Then one table per question over the endpoint rows:
     - How many use cases does each endpoint become? (keep / merge / split / remove)
     - Is its use case defined on the same group page, or did it move?
     - Who can call it? (stays public / made internal / made public / stays internal / removed)
   - Join endpoints to use cases by key, not by exact name.

## Definitions

- **Use case:** a goal the caller reaches through the system. Name it with a short verb phrase that also works as a function name.
- **Outcome:** the end state the caller sees when the use case succeeds, including side effects. Describe the state itself, apart from the input and the response body.
- **Same outcome, different input format:** one use case with input variants.
- **Different outcome or side effect:** separate use cases.
- **Interface:** how a caller reaches a use case. Public use cases get REST and MCP. Internal use cases get RPC (parent FR1).

## Steps

1. **List what exists.** Collect every endpoint for the resource across REST (`apps/api`), tRPC and Next.js routes (`apps/web`), MCP tools (`apps/api/src/controllers/mcp`) and the CLI commands that call the server through `tools/greptile-cli/src/api/`. Add production traffic for the last 30 days. Mark endpoints with no caller, and duplicates of a kept endpoint, for deletion (parent FR6).
   - Note any webhook, poller or Hatchet workflow that performs the same operation as a use case (for example, starting a review on a push). List it under Called by, so it calls the same use case.
   - Check every use case against every provider: GitHub, GitLab, Bitbucket, Perforce, Gerrit and Origin. Read each endpoint's provider allowlist, such as the `remote` check in `triggerCodeReview`, and record which providers have a path.
   - Compare against Haotian's v3 draft (`packages/api-contracts` at commit `90403f36e8`) for its error format, cursor pagination, status model and policy fields.
2. **Name each caller's goal.** For each endpoint, ask what the caller is trying to get done.
3. **Write the outcome.** One sentence describing the end state. Rewrite any outcome that reads like a description of the input.
4. **Merge or split by outcome.** Group endpoints with the same outcome. Split when the side effects differ, even if the response is the same (Fowler: separate methods when the caller chooses the behaviour; CQRS: commands capture intent). Use a flag only for a dry run with no side effects (AIP-163).
5. **Find the owning resource.** Start from the domain model: worker v2 types (`apps/worker-v2/src/flows/`) and `packages/db/prisma/schema.prisma`. Treat worker v2's types as a starting point and change them wherever a use case needs it (parent FR3). Then ask:
   - Can the thing exist without this resource? If yes, it may be its own resource.
   - Does another resource produce it too? If yes, it gets its own resource (findings: reviews and scans; artifacts: reviews and T-Rex).
   - Does it work for every variant of this resource? It belongs to the resource where it works for every variant (apply-suggestion needs a branch, which only merge request reviews have, so it moves to merge requests).
   - Which resource owns the action? The use case lives there, even when it calls other resources. A use case that reads across several resources, such as a usage report, gets its own group (Lesson 5 "Feature folders", `~/Code/teach-architecture/lessons/0005-feature-folders.html`).
   - Does it have rules? A use case with rules runs them in the domain layer; one without rules reads the data layer directly. Either way, every interface calls the same function (parent FR2).
6. **Pick each use case's interfaces.** Mark REST, RPC and MCP in the use cases table:
   - RPC for every use case the web app or the landing website needs. Webhooks, pollers and Hatchet workflows call the use case function directly.
   - REST and MCP for every use case that existing users call today (CLI, MCP tools, today's `/v1` and `/v2` routes) or that a customer job on the Public API page needs.
   - Mark a use case deferred when it has no caller yet. Keep its row and write the reason under its definition.
7. **Check standards.** Use the `api-design-guidelines` skill to find which source answers the question and how to research it. Cite the source in the row that relies on it. AIP-121 and AIP-132 (Get and List on every non-singleton resource) are the reason to bring back a deferred List once a caller needs it. For public routes, check OpenAPI limits: one operation per path and method, `security` per operation.
8. **Give each endpoint a verdict** in an Endpoint comparison table (Use case | Today | v3 | Verdict | Why): keep, merge, split, internal, move or remove. Link each endpoint to its code at a pinned commit and give its request count. For every removed endpoint with traffic, name the use case its callers move to.
9. **Name for code.** Use the database's terms ("merge request" rather than "pull request"). Pick verbs that read clearly next to HTTP methods ("publish" rather than "post").
10. **Fill the use cases table:** Use case | Outcome | Called by | REST | RPC | MCP. Put endpoint and implementation details in the Endpoint comparison section.
11. **Record open questions** under the table: where differing rules for permission, billing or rate limits keep two use cases apart, and what would merge them.
12. **Write the use case definitions** in a "Use case definitions" section, one use case at a time:
    - A heading with the use case name and a one-line description of what it does.
    - An **Input** table: Field | Type | Required | Description. Write nested fields as dot paths (`localChanges.files[].path`). Mark alternatives "one of". Put limits and defaults in the description, taken from the current request schemas (lengths, counts, byte caps).
    - An **Output** line naming the DTO it returns, plus the behaviour the DTO leaves implicit (initial status, what a repeat call returns).
    - An **Errors** table for errors specific to this use case: Code | REST status | When. Each interface maps the same code to its own format (parent FR4). Errors every use case can return go once in a common Errors section.
    - Describe inputs as tables and outputs as DTOs. The DTOs section holds response shapes. Leave input types and code signatures to the implementation.
    - Lists take `pageSize` (default 20, capped at 100) and `cursor`, and return a page DTO with the items and `nextCursor`, null on the last page (parent FR5).
    - Field names follow the database (see memory `api-entities-follow-db-names`). Every response field is present and null when unset.
13. **Check coverage against the Endpoint comparison.** Each use case should support everything the endpoints merged into it do today, so existing callers keep working. For every endpoint in its row:
    - Read the request schema. Every input it takes goes in the Input table, or gets a reason for dropping it (derived by the server, unused).
    - Read the response, then what its callers actually read: CLI render and `--json` code, MCP tool output, web app components. Every field a caller reads goes in the output DTO, or gets a reason for dropping it.
    - Check how the endpoint identifies things (database id, provider number, repository name and remote). The Input accepts every identifier callers have.
    - Report the gaps as a table (Use case | Endpoint | Missing | Read by | Proposal) before editing the doc.

## How to work with Felix

- Settle one row at a time. Propose the wording, wait for Felix's call, then edit the doc.
- Answer questions about the doc in chat. Edit the doc when Felix asks for an edit.
- Check every claim against code and traffic before writing it down, including what a subagent returns from worker v2 or Notion.
- When citing an earlier decision, say who made it: Felix, a debate or you.
- Keep chat answers short, in tables.
