#!/usr/bin/env python3
"""Create a fresh greptilia clone as a sibling folder.

Python port of the `new-greptilia` zsh function. Copies the source checkout
(minus build/dep artifacts), symlinks the shared local env files, installs
dependencies, regenerates the local env + Prisma client, and validates the
result.

Usage:
    new_greptilia.py <name>

The source repo defaults to ~/Code/greptilia and can be overridden with the
GREPTILIA_ROOT environment variable. <name> is a sibling folder name (not a
path); a "greptilia-" prefix is added automatically if missing.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def fail(msg: str, code: int = 1) -> int:
    print(f"new-greptilia: {msg}", file=sys.stderr)
    return code


def main(argv: list[str]) -> int:
    if len(argv) == 0 or not argv[0]:
        print("usage: new-greptilia <name>", file=sys.stderr)
        return 2

    if len(argv) != 1:
        return fail("expected exactly one sibling folder name", 2)

    name = argv[0]

    if "/" in name:
        return fail("name must be a sibling folder name, not a path", 2)

    src = Path(os.environ.get("GREPTILIA_ROOT") or (Path.home() / "Code" / "greptilia"))
    parent = src.parent

    folder_name = name if name.startswith("greptilia-") else f"greptilia-{name}"
    dest = parent / folder_name

    if not src.is_dir():
        return fail(f"source repo not found: {src}")

    required_files = [
        src / "config" / "config.development.yaml",
        src / "config" / ".env",
        src / "packages" / "db" / ".env",
        src / "internal" / "cli" / ".env",
        src / ".infisical.json",
    ]
    for required_file in required_files:
        if not required_file.is_file():
            return fail(
                f"source checkout is missing required local config: {required_file}"
            )

    if shutil.which("rsync") is None:
        return fail("rsync is required")

    if shutil.which("bun") is None:
        return fail("bun is required")

    if dest.exists() or dest.is_symlink():
        return fail(f"destination already exists: {dest}")

    print(f"Copying {src} -> {dest}")
    rsync = subprocess.run(
        [
            "rsync",
            "-a",
            "--exclude",
            "/node_modules/",
            "--exclude",
            "/.turbo/",
            "--exclude",
            "/logs/",
            "--exclude",
            "/apps/*/.next/",
            f"{src}/",
            f"{dest}/",
        ]
    )
    if rsync.returncode != 0:
        return rsync.returncode

    print("Linking shared local env files")
    (dest / "config").mkdir(parents=True, exist_ok=True)
    (dest / "packages" / "db").mkdir(parents=True, exist_ok=True)
    (dest / "internal" / "cli").mkdir(parents=True, exist_ok=True)

    links = {
        dest / "config" / ".env": src / "config" / ".env",
        dest / "packages" / "db" / ".env": src / "packages" / "db" / ".env",
        dest / "internal" / "cli" / ".env": src / "internal" / "cli" / ".env",
    }
    for link, target in links.items():
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(target)

    print("Installing dependencies and generating local env + Prisma client")
    setup = subprocess.run(
        "bun install && bun run env:generate && cd packages/db && bun run db:generate",
        shell=True,
        cwd=dest,
    )
    if setup.returncode != 0:
        return setup.returncode

    validations = [
        (dest / "config" / "config.development.yaml", "is_file",
         "missing config/config.development.yaml"),
        (dest / "config" / ".env", "is_symlink",
         "config/.env is not a symlink"),
        (dest / "packages" / "db" / ".env", "is_symlink",
         "packages/db/.env is not a symlink"),
        (dest / "internal" / "cli" / ".env", "is_symlink",
         "internal/cli/.env is not a symlink"),
        (dest / "apps" / "web" / ".env.local", "is_file",
         "missing apps/web/.env.local"),
        (dest / "node_modules", "is_dir",
         "missing node_modules"),
        (dest / "packages" / "db" / "generated" / "client", "is_dir",
         "missing packages/db/generated/client"),
    ]
    for path, check, message in validations:
        if not getattr(path, check)():
            return fail(f"validation failed: {message}")

    print(f"Created {dest}")
    print(
        "Note: clones share local Postgres/Redis and bind the same dev ports, "
        "so run bun run dev from one clone at a time."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
