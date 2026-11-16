#!/usr/bin/env python3
"""Fail if a skill would not load the same way in every harness.

  ./check.py                     repo-only checks (what CI runs)
  ./check.py --local             also compare against what is installed on this machine
  ./check.py --project DIR       also fail on name clashes with DIR's repo skills
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SKILLS = ROOT / "skills"
HOME = pathlib.Path.home()
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HARNESS_PATH = re.compile(r"~/\.(claude|codex|agents)/skills|/Users/[^/\s]+/\.(claude|codex|agents)/skills")
LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
# Folders that hold skills managed by something else, not by this repo or `npx skills`.
NOT_OURS = {".system", "synced"}

errors = []


def frontmatter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return None
    block = text[4:text.find("\n---", 4)]
    fields, key = {}, None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2)
            fields[key] = "" if value in (">", "|", ">-", "|-") else value.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def broken_links(path):
    """Relative links in a markdown file that point at nothing. Code blocks and inline code are skipped."""
    text = re.sub(r"`[^`\n]*`", "", FENCE.sub("", path.read_text(errors="ignore")))
    for target in LINK.findall(text):
        target = target.split("#")[0]
        if target and not re.match(r"^[a-z][a-z0-9+.-]*:", target) and not (path.parent / target).exists():
            yield target


def third_party():
    names = {}
    for line in (ROOT / "third-party.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            source, *skills = line.split()
            names.update({s: source for s in skills})
    return names


def check_repo():
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill = d / "SKILL.md"
        if not skill.exists():
            errors.append(f"{d.name}: missing SKILL.md")
            continue
        fm = frontmatter(skill)
        if fm is None:
            errors.append(f"{d.name}: SKILL.md has no frontmatter")
            continue
        if fm.get("name") != d.name:
            errors.append(f"{d.name}: name '{fm.get('name')}' must match the folder name")
        if not NAME.match(d.name) or len(d.name) > 64:
            errors.append(f"{d.name}: name must be lowercase-hyphenated, at most 64 chars")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            errors.append(f"{d.name}: description must be 1-1024 chars (is {len(desc)})")

        for f in d.rglob("*"):
            if f.is_file() and f.suffix in (".md", ".py", ".sh", ".yaml", ".yml", ".ts", ".js"):
                for m in HARNESS_PATH.finditer(f.read_text(errors="ignore")):
                    errors.append(f"{d.name}: {f.relative_to(d)} hardcodes '{m.group(0)}'; use a path relative to the skill folder")

        for f in d.rglob("*.md"):
            for target in broken_links(f):
                errors.append(f"{d.name}: {f.relative_to(d)} links to '{target}', which does not exist")

        # Claude reads disable-model-invocation; Codex reads agents/openai.yaml. Keep them in step.
        manual_claude = fm.get("disable-model-invocation", "").lower() == "true"
        yaml = d / "agents" / "openai.yaml"
        manual_codex = yaml.exists() and re.search(r"allow_implicit_invocation:\s*false", yaml.read_text()) is not None
        if manual_claude and not manual_codex:
            errors.append(f"{d.name}: disable-model-invocation is true, so agents/openai.yaml needs policy.allow_implicit_invocation: false")
        if manual_codex and not manual_claude:
            errors.append(f"{d.name}: agents/openai.yaml disables implicit invocation, so SKILL.md needs disable-model-invocation: true")

    for name in third_party():
        if (SKILLS / name).exists():
            errors.append(f"{name}: listed in third-party.txt and also in skills/")


def installed(folder):
    if not folder.is_dir():
        return {}
    return {p.name: p for p in folder.iterdir() if p.name not in NOT_OURS and not p.name.startswith(".")}


def check_local():
    ours = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    known = ours | set(third_party())
    claude = installed(HOME / ".claude/skills")
    agents = installed(HOME / ".agents/skills")
    codex = installed(HOME / ".codex/skills")

    for name in sorted(ours):
        for label, folder in (("~/.claude/skills", claude), ("~/.agents/skills", agents)):
            p = folder.get(name)
            if p is None or p.resolve() != (SKILLS / name).resolve():
                errors.append(f"{name}: not linked from {label}; run ./install.sh")
    for name in sorted(set(third_party()) - set(agents)):
        errors.append(f"{name}: third-party skill not installed; run ./install.sh")
    for label, folder in (("~/.claude/skills", claude), ("~/.agents/skills", agents), ("~/.codex/skills", codex)):
        for name in sorted(set(folder) - known):
            errors.append(f"{name}: installed in {label} but not in this repo or third-party.txt; add it or remove it")
    # Codex loads both ~/.codex/skills and ~/.agents/skills, so a name in both shows up twice.
    for name in sorted(set(codex) & set(agents)):
        errors.append(f"{name}: in both ~/.codex/skills and ~/.agents/skills; Codex loads it twice")


def check_project(root):
    project = set()
    for sub in (".agents/skills", ".claude/skills", ".codex/skills"):
        project |= set(installed(pathlib.Path(root) / sub))
    for name in sorted(project & ({p.name for p in SKILLS.iterdir()} | set(third_party()))):
        errors.append(f"{name}: also a skill in {root}; inside that repo two skills share this name")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--project", action="append", default=[])
    args = ap.parse_args()
    check_repo()
    if args.local:
        check_local()
    for p in args.project:
        check_project(p)
    for e in errors:
        print(e, file=sys.stderr)
    print(f"{len(errors)} problem(s)" if errors else "ok")
    sys.exit(1 if errors else 0)
