#!/usr/bin/env python3
"""Copy the skills listed in vendor.txt from their upstream repos into vendor/, merging upstream changes into local edits.

  ./vendor.py              refresh every skill
  ./vendor.py tdd handoff  refresh the lines that name these. A pin covers a whole line, so every skill on those lines is refreshed.

vendor.txt pins each line to the upstream commit its copies came from (`owner/repo@<sha>`). That commit is the base: the upstream
version your edits started from. Refreshing merges per file across base, your copy and the tracked ref (licence files included),
then moves the pin to the new commit. A line with no pin is copied over as is and gets one. A tree URL whose ref is a commit SHA
is your own pin: it is never moved, and with no base its copies are overwritten.

Where both sides changed a file, git merge-file leaves conflict markers in the copy. A file one side added or deleted and the
other changed keeps your version. Either way the file is listed and the exit status is 1.
Review the diff before committing: it is what upstream changed.
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
    """A vendor.txt source as (clone URL, ref, path inside the repo, base commit or None)."""
    source, _, base = source.partition("@")
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/([^/]+)/?(.*)$", source)
    if m:
        return f"https://github.com/{m.group(1)}.git", m.group(2), m.group(3), base or None
    return (source if "://" in source else f"https://github.com/{source}.git"), "HEAD", "", base or None


def checkout(url, ref, into):
    """A shallow checkout of one ref, returning its commit. `fetch` takes a branch, a tag or a commit SHA, which `clone --branch` does not."""
    run = lambda *args: subprocess.run(["git", "-C", str(into), *args], check=True, capture_output=True, text=True).stdout
    into.mkdir(parents=True)
    run("init", "-q")
    run("fetch", "-q", "--depth", "1", url, ref)
    run("checkout", "-q", "FETCH_HEAD")
    return run("rev-parse", "HEAD").strip()


def licence_files(skill_dir, repo_root):
    """The licence nearest the skill: its own folder first, then each parent up to the repo root."""
    for folder in [skill_dir, *skill_dir.parents]:
        found = [f for f in folder.iterdir() if f.is_file() and re.match(r"(?i)(licen[cs]e|notice|copying)", f.name)]
        if found or folder == repo_root:
            return found
    return []


def export(repo, path, name, source, into):
    """Copy one skill and its licence files out of a checkout into `into`. False if the checkout has no such skill."""
    base = repo / path
    # Some repos repeat their skills under dot-folders for other tools (.openclaw/skills/...). Skip those copies.
    found = [f.parent for f in base.rglob("SKILL.md")
             if f.parent.name == name and not any(part.startswith(".") for part in f.relative_to(base).parts)]
    if len(found) > 1:
        sys.exit(f"{name}: expected one {name}/SKILL.md under {source}, found {len(found)}")
    if not found:
        return False
    shutil.copytree(found[0], into)
    for licence in licence_files(found[0], repo):
        if not (into / licence.name).exists():
            shutil.copy(licence, into / licence.name)
    return True


def merge(name, ours, base, theirs):
    """Merge theirs into ours file by file, relative to base. Returns the files that conflicted."""
    files = lambda d: {f.relative_to(d) for f in d.rglob("*") if f.is_file()} if d.exists() else set()
    read = lambda d, f: (d / f).read_bytes() if (d / f).is_file() else None
    conflicts = []
    for f in sorted(files(ours) | files(base) | files(theirs)):
        o, b, t = read(ours, f), read(base, f), read(theirs, f)
        if o == b:
            if t is None:
                (ours / f).unlink()
            else:
                (ours / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(theirs / f, ours / f)
        elif t == b or o == t:
            continue
        elif None in (o, b, t):
            conflicts.append(f"{name}/{f}")
        else:
            merged = subprocess.run(["git", "merge-file", "-p", "-L", "ours", "-L", "base", "-L", "theirs",
                                     str(ours / f), str(base / f), str(theirs / f)], capture_output=True)
            if merged.returncode:
                conflicts.append(f"{name}/{f}")
            if merged.returncode < 127:  # 127 and up: git could not merge the file (binary), so ours stays
                (ours / f).write_bytes(merged.stdout)
    return conflicts


def main(only):
    lines = (ROOT / "vendor.txt").read_text().splitlines()
    conflicts = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        checkouts = {}
        for i, line in enumerate(lines):
            if not line.strip() or line.startswith("#"):
                continue
            source, *skills = line.split()
            if only and not only & set(skills):
                continue
            url, ref, path, pin = parse(source)
            if (url, ref) not in checkouts:
                into = tmp / f"theirs-{len(checkouts)}"
                checkouts[url, ref] = into, checkout(url, ref, into)
            repo, commit = checkouts[url, ref]
            base_repo = None
            if pin:
                base_repo = tmp / f"base-{i}"
                checkout(url, pin, base_repo)
            for name in skills:
                theirs = tmp / f"skill-theirs-{i}-{name}"
                if not export(repo, path, name, source, theirs):
                    sys.exit(f"{name}: expected one {name}/SKILL.md under {source}, found 0")
                target = DEST / name
                base = tmp / f"skill-base-{i}-{name}"
                if base_repo and target.exists() and export(base_repo, path, name, source, base):
                    conflicts += merge(name, target, base, theirs)
                    print(f"{name}: merged from {source}")
                else:
                    shutil.rmtree(target, ignore_errors=True)
                    shutil.copytree(theirs, target)
                    print(f"{name}: copied from {source}")
            # A tree URL whose ref is a commit SHA is the user's own pin; leave it.
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                lines[i] = line.replace(source, f"{source.partition('@')[0]}@{commit}", 1)
    (ROOT / "vendor.txt").write_text("\n".join(lines) + "\n")
    if conflicts:
        sys.exit("conflicts, see the markers in `git diff vendor/`:\n  " + "\n  ".join(conflicts))


if __name__ == "__main__":
    main(set(sys.argv[1:]))
