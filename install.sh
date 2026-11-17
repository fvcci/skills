#!/usr/bin/env bash
# Install every skill in this repo for Claude Code, Codex, OpenCode and other harnesses.
#   ./install.sh    link every skill in skills/ and vendor/
#
# Skills are symlinked, so editing them here updates every harness at once:
#   ~/.agents/skills  read by Codex, OpenCode, Copilot, Zed, ...
#   ~/.claude/skills  read by Claude Code (it does not read ~/.agents)
set -euo pipefail

repo="$(cd "$(dirname "$0")" && pwd)"
backup="$HOME/.skills-backup/$(date +%Y%m%d-%H%M%S)"

link() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [ -L "$dest" ]; then
    rm "$dest"
  elif [ -e "$dest" ]; then
    mkdir -p "$backup/$(basename "$(dirname "$dest")")"
    if ! mv "$dest" "$backup/$(basename "$(dirname "$dest")")/"; then
      echo "could not move $dest out of the way (owned by another user?): sudo rm -rf '$dest'" >&2
      return 1
    fi
    echo "moved existing $dest to $backup"
  fi
  ln -s "$src" "$dest"
}

failed=0
for dir in "$repo"/skills/*/ "$repo"/vendor/*/; do
  name="$(basename "$dir")"
  link "${dir%/}" "$HOME/.agents/skills/$name" || failed=1
  link "${dir%/}" "$HOME/.claude/skills/$name" || failed=1
done
echo "linked skills from $repo/skills and $repo/vendor"
exit "$failed"
