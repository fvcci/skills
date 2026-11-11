---
name: new-greptilia
description: >
  Create a fresh greptilia clone as a sibling folder of an existing checkout.
  Copies the source repo (excluding node_modules/.turbo/logs/.next), symlinks
  the shared local env files, runs bun install + env:generate + Prisma
  db:generate, and validates the result. Use when the user wants a new
  greptilia worktree/clone, says "new-greptilia", or asks to spin up another
  greptilia dev checkout.
argument-hint: "<name>"
---

# new-greptilia

Creates a new greptilia clone next to an existing checkout, wired up with the
shared local env files and ready to run.

## Usage

```
python3 <this skill's directory>/new_greptilia.py <name>
```

- `<name>` is a sibling folder name, not a path (no slashes). A `greptilia-`
  prefix is added automatically if missing, so `foo` becomes `greptilia-foo`.
- The source checkout defaults to `~/Code/greptilia`. Override with the
  `GREPTILIA_ROOT` environment variable. The clone is created as a sibling of
  the source (same parent directory).

## What it does

1. Validates args and that the source repo + required local config exist
   (`config/config.development.yaml`, `config/.env`, `packages/db/.env`,
   `internal/cli/.env`, `.infisical.json`).
2. Checks `rsync` and `bun` are on PATH and the destination doesn't exist.
3. `rsync -a` copies the repo, excluding `node_modules`, `.turbo`, `logs`, and
   `apps/*/.next`.
4. Symlinks the shared env files (`config/.env`, `packages/db/.env`,
   `internal/cli/.env`) back to the source so all clones share them.
5. Runs `bun install && bun run env:generate`, then `bun run db:generate` in
   `packages/db`.
6. Validates the result (env symlinks, generated `apps/web/.env.local`,
   `node_modules`, Prisma client) and reports the new path.

## Notes

- Clones share the local Postgres/Redis and bind the same dev ports, so run
  `bun run dev` from one clone at a time.
- Exit codes: `2` for usage errors, `1` for environment/validation failures,
  otherwise the underlying `rsync`/`bun` exit code.
