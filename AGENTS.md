# Installing these skills

When asked to install or set up these skills, do the following and report the result.

1. **Get the repo.** If you are not already inside a clone, clone it to `~/Code/skills`:
   `git clone git@github.com:fvcci/skills.git ~/Code/skills`.
   The repo is private. If SSH fails and `GITHUB_TOKEN` is set, use
   `https://x-access-token:$GITHUB_TOKEN@github.com/fvcci/skills.git`. If neither works, ask the user to run `gh auth login`.
2. **Check prerequisites:** `git`, `python3`, and `node` (for `npx`). Install any that are missing with the system package manager, or ask the user.
3. **Install:** run `./install.sh` from the repo root. It:
   - symlinks each `skills/<name>` into `~/.claude/skills` and `~/.agents/skills`;
   - moves any existing folder with the same name into `~/.skills-backup/<timestamp>/` first;
   - installs the skills in `third-party.txt` from upstream with `npx skills add`.
4. **Handle failures.** If `install.sh` prints `could not move ... sudo rm -rf '<path>'`, that folder belongs to another user. Give the user that exact command to run, then rerun `./install.sh --skip-third-party`. Do not run `sudo` yourself.
5. **Remove duplicates.** Codex loads both `~/.codex/skills` and `~/.agents/skills`. If `./check.py --local` reports a name in both, delete the copy in `~/.codex/skills` (never touch `~/.codex/skills/.system`).
6. **Verify:** `./check.py --local` must print `ok`. For anything else it reports, fix it or explain it to the user. Skills installed on the machine that are not tracked here are the user's call: list them and ask whether to keep or remove them.
7. **Finish:** tell the user to restart open Claude Code, Codex, and OpenCode sessions, which load skills at startup.

# Changing skills

- Edit skills in `skills/` in this repo, never through `~/.claude/skills` or `~/.agents/skills`; those are links to here.
- After any change, run `./check.py` and keep it passing. Follow the rules in `README.md`: one folder per skill for every harness, paths relative to the skill folder, and `disable-model-invocation` paired with `agents/openai.yaml`.
- Third-party skills are only listed in `third-party.txt`; do not copy them into `skills/`.
