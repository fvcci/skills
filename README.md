# skills

Felix's agent skills for Claude Code, Codex, OpenCode, and any other harness that reads the Agent Skills format.

## Layout

- `skills/<name>/SKILL.md`: skills written here. Each one is a single folder used by every harness, so a Claude skill always has its Codex counterpart.
- `third-party.txt`: skills written by other people, installed from their upstream repos.
- `install.sh`: links `skills/*` into `~/.claude/skills` (Claude Code) and `~/.agents/skills` (Codex, OpenCode, Copilot, Zed), then installs the third-party skills with `npx skills`.
- `check.py`: fails when a skill would load differently between harnesses.

## Install

```bash
git clone git@github.com:fvcci/skills.git ~/Code/skills
~/Code/skills/install.sh
```

Skills are symlinked, so editing a file in `skills/` changes it in every harness at once.

In a cloud machine or sandbox (Codex cloud, Claude Code on the web, a dev VM), put the same two commands in the environment's setup script. The repo is private, so clone with a GitHub token:

```bash
git clone https://x-access-token:$GITHUB_TOKEN@github.com/fvcci/skills.git ~/skills && ~/skills/install.sh
```

To install only the skills in `skills/`, without cloning: `npx skills add fvcci/skills --global --yes --agent claude-code codex opencode`.

## Rules `check.py` enforces

- `name` matches the folder name; `description` is 1-1024 characters.
- No hardcoded `~/.claude/skills`, `~/.codex/skills` or `~/.agents/skills` paths. Refer to files relative to the skill folder.
- Claude's `disable-model-invocation: true` and Codex's `agents/openai.yaml` `policy.allow_implicit_invocation: false` appear together or not at all.
- A skill is in `skills/` or `third-party.txt`, never both.

`./check.py --local` also compares against this machine. It reports skills installed but not tracked here, tracked skills that are not installed, and names in both `~/.codex/skills` and `~/.agents/skills`, which Codex loads twice.

`./check.py --project ~/Code/greptilia` reports names shared with a repo's own skills.

## Adding or removing a skill

1. Add `skills/<name>/SKILL.md`, or a line in `third-party.txt`.
2. Run `./install.sh --skip-third-party` (or `./install.sh` for third-party changes).
3. Run `./check.py --local`.

To remove one, delete it here, then delete its links in `~/.claude/skills` and `~/.agents/skills` (`npx skills remove -g <name>` for third-party skills).
