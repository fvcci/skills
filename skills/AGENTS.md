# Changing skills

- Edit skills here, in `skills/` of this repo, never through `~/.claude/skills` or `~/.agents/skills`; those are links to here.
- After any change, run `./check.py` from the repo root and keep it passing. Follow the rules in `README.md`: one folder per skill for every harness, paths relative to the skill folder, and `disable-model-invocation` paired with `agents/openai.yaml`.
- Third-party skills are listed in `third-party.txt` and copied into `third-party/` by `./vendor.py`. Do not edit the copies or put them in `skills/`.
