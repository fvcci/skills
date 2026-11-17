#!/usr/bin/env python3
"""Copy the skills listed in vendor.txt from their upstream repos into vendor/.

  ./vendor.py              refresh every skill
  ./vendor.py tdd handoff  refresh only these

Each copy keeps its upstream licence file. Review the diff before committing: it is what upstream changed.
"""
import pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent
DEST = ROOT / "vendor"


def sources():
    for line in (ROOT / "vendor.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            source, *skills = line.split()
            yield source, skills


def parse(source):
    """A vendor.txt source as (clone URL, ref, path inside the repo)."""
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/([^/]+)/?(.*)$", source)
    if m:
        return f"https://github.com/{m.group(1)}.git", m.group(2), m.group(3)
    return (source if "://" in source else f"https://github.com/{source}.git"), "HEAD", ""


def checkout(url, ref, into):
    """A shallow checkout of one ref. `fetch` takes a branch, a tag or a commit SHA, which `clone --branch` does not."""
    run = lambda *args: subprocess.run(["git", "-C", str(into), *args], check=True, capture_output=True)
    into.mkdir(parents=True)
    run("init", "-q")
    run("fetch", "-q", "--depth", "1", url, ref)
    run("checkout", "-q", "FETCH_HEAD")


def licence_files(skill_dir, repo_root):
    """The licence nearest the skill: its own folder first, then each parent up to the repo root."""
    for folder in [skill_dir, *skill_dir.parents]:
        found = [f for f in folder.iterdir() if f.is_file() and re.match(r"(?i)(licen[cs]e|notice|copying)", f.name)]
        if found or folder == repo_root:
            return found
    return []


def main(only):
    with tempfile.TemporaryDirectory() as tmp:
        checkouts = {}
        for source, skills in sources():
            url, ref, path = parse(source)
            for name in skills:
                if only and name not in only:
                    continue
                if (url, ref) not in checkouts:
                    checkouts[url, ref] = pathlib.Path(tmp) / str(len(checkouts))
                    checkout(url, ref, checkouts[url, ref])
                repo = checkouts[url, ref]
                base = repo / path
                # Some repos repeat their skills under dot-folders for other tools (.openclaw/skills/...). Skip those copies.
                found = [f.parent for f in base.rglob("SKILL.md")
                         if f.parent.name == name and not any(part.startswith(".") for part in f.relative_to(base).parts)]
                if len(found) != 1:
                    sys.exit(f"{name}: expected one {name}/SKILL.md under {source}, found {len(found)}")
                target = DEST / name
                shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(found[0], target)
                for licence in licence_files(found[0], repo):
                    if not (target / licence.name).exists():
                        shutil.copy(licence, target / licence.name)
                print(f"{name}: copied from {source}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
