#!/usr/bin/env bash
# Install every skill in this repo for Claude Code, Codex, OpenCode and other harnesses.
#   ./install.sh                    link own skills, then install third-party ones from upstream
#   ./install.sh --skip-third-party only (re)link own skills
#
# Own skills are symlinked, so editing them here updates every harness at once:
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
for dir in "$repo"/skills/*/; do
  name="$(basename "$dir")"
  link "${dir%/}" "$HOME/.agents/skills/$name" || failed=1
  link "${dir%/}" "$HOME/.claude/skills/$name" || failed=1
done
echo "linked own skills from $repo/skills"

[ "${1:-}" = "--skip-third-party" ] && exit "$failed"

grep -vE '^\s*(#|$)' "$repo/third-party.txt" | while read -r source skills; do
  # shellcheck disable=SC2086
  npx -y skills add "$source" --global --yes --agent claude-code codex opencode --skill $skills </dev/null
done
exit "$failed"
