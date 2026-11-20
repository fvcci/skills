---
name: posthog
description: Use before any PostHog query or operation (insights, alerts, dashboards, feature flags, data warehouse, events).
---

Use `posthog-cli api` for every PostHog query and operation, over the PostHog MCP tools.

1. Before the first PostHog command in a session, run `posthog-cli api --agent-help` and follow its full output as instructions: command reference, schema drill-down, data discovery, and the tool index.
2. Before each PostHog task, run `posthog-cli api skill list`. On a match, run `posthog-cli api skill install <skill-id>` (`--force` refreshes an installed one), then follow `.agents/skills/<skill-id>/SKILL.md`. These skills carry task workflows the tools lack.
