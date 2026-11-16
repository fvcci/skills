# skills

Felix's agent skills for Claude Code, Codex, OpenCode, and any other harness that reads the Agent Skills format.

## Layout

- `skills/<name>/SKILL.md`: skills written here. Each one is a single folder used by every harness, so a Claude skill always has its Codex counterpart.
- `third-party.txt`: skills written by other people, and the upstream repo each comes from.
- `third-party/`: the one copy of each of those skills, refreshed from upstream by `./vendor.py`.
- `install.sh`: links `skills/*` and `third-party/*` into `~/.claude/skills` (Claude Code) and `~/.agents/skills` (Codex, OpenCode, Copilot, Zed, Devin).
- `check.py`: fails when a skill would load differently between harnesses.
- `.devin-plugin/plugin.json`: makes the repo a Devin plugin named `fvcci`.
- `skills/AGENTS.md`: the rules for an agent editing skills. It sits below the repo root on purpose: Devin injects a root `AGENTS.md` into every session of anyone who has the plugin.

## Install

```bash
git clone https://github.com/fvcci/skills.git ~/Code/skills
~/Code/skills/install.sh
```

Skills are symlinked, so editing a file here changes it in every harness at once.

In a cloud machine or sandbox (Codex cloud, Claude Code on the web, a dev VM), put the same two commands in the environment's setup script.

### Installing with an agent

An agent asked to install or set up these skills does the following and reports the result.

1. **Get the repo.** If you are not already inside a clone, clone it to `~/Code/skills`:
   `git clone https://github.com/fvcci/skills.git ~/Code/skills`.
2. **Check prerequisites:** `git` and `python3`. Install any that are missing with the system package manager, or ask the user.
3. **Install:** run `./install.sh` from the repo root. It:
   - symlinks each `skills/<name>` and `third-party/<name>` into `~/.claude/skills` and `~/.agents/skills`;
   - moves any existing folder with the same name into `~/.skills-backup/<timestamp>/` first.
4. **Handle failures.** If `install.sh` prints `could not move ... sudo rm -rf '<path>'`, that folder belongs to another user. Give the user that exact command to run, then rerun `./install.sh`. Do not run `sudo` yourself.
5. **Remove duplicates.** Codex loads both `~/.codex/skills` and `~/.agents/skills`. If `./check.py --local` reports a name in both, delete the copy in `~/.codex/skills` (never touch `~/.codex/skills/.system`).
6. **Verify:** `./check.py --local` must print `ok`. For anything else it reports, fix it or explain it to the user. Skills installed on the machine that are not tracked here are the user's call: list them and ask whether to keep or remove them.
7. **Finish:** tell the user to restart open Claude Code, Codex, and OpenCode sessions, which load skills at startup.

### Devin

On a machine where `install.sh` has run, Devin reads the skills from `~/.agents/skills` like the other harnesses. Cloud sessions have no such folder, so they load the repo as a plugin, where the skills show up as `/fvcci:<skill>`:

```bash
devin plugins install fvcci/skills
```

The plugin is set to load in cloud sessions only, so a local session does not list every skill twice.

### Without cloning

To install the skills with the `skills` tool: `npx skills add fvcci/skills --global --yes --agent claude-code codex opencode`.

## Rules `check.py` enforces

- `name` matches the folder name; `description` is 1-1024 characters.
- No hardcoded `~/.claude/skills`, `~/.codex/skills` or `~/.agents/skills` paths. Refer to files relative to the skill folder.
- Claude's `disable-model-invocation: true` and Codex's `agents/openai.yaml` `policy.allow_implicit_invocation: false` appear together or not at all.
- Every relative link in a skill's markdown points at a file that exists.
- No frontmatter value holds `: ` unquoted. Lenient loaders accept it, and a strict YAML parser drops the skill.
- A skill is in `skills/` or `third-party.txt`, never both.
- `third-party/` holds exactly the skills `third-party.txt` lists.

`./check.py --local` also compares against this machine. It reports skills installed but not tracked here, tracked skills that are not linked to this repo, and names in both `~/.codex/skills` and `~/.agents/skills`, which Codex loads twice.

`./check.py --project ~/Code/greptilia` reports names shared with a repo's own skills.

## Adding or removing a skill

1. Add `skills/<name>/SKILL.md`, or a line in `third-party.txt` followed by `./vendor.py <name>`.
2. Run `./install.sh`.
3. Run `./check.py --local`.

To remove one, delete it here (for a third-party skill, its line and its folder in `third-party/`), then delete its links in `~/.claude/skills` and `~/.agents/skills`.

## License

MIT, see [LICENSE](LICENSE). The skills under `third-party/` belong to their authors and keep their own licences: each folder carries its upstream licence file.

The smell wording in `skills/sniff/SMELLS.md` is adapted from the `code-review` skill in [mattpocock/skills](https://github.com/mattpocock/skills), which is MIT licensed, Copyright (c) 2026 Matt Pocock.
