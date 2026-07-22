#!/usr/bin/env bash
set -euo pipefail

# Installs the skill pack for Claude Code, Codex CLI, Google Antigravity,
# OpenCode, GitHub Copilot, and Cursor. Tools that read the ~/.agents/skills
# interop path (Amp, Cline, and a growing list) are covered automatically.
#
# Cursor note: project scope is .cursor/skills OR .agents/skills per Cursor's
# docs, so --project already covers it via .agents/skills. The user-level
# ~/.cursor/skills target serves builds with personal-skill support; harmless
# if your build is project-only.
#
# Antigravity note: Google deprecated Gemini CLI for free/Pro/Ultra tiers on
# June 18, 2026; Antigravity CLI replaced it and kept Agent Skills support.
# Global skills for Antigravity live at ~/.gemini/config/skills (yes, still
# under ~/.gemini), which this installer now writes. ~/.gemini/skills is kept
# for enterprise Code Assist licenses still running legacy Gemini CLI; delete
# that line if you have no legacy use. Project scope for Antigravity is
# .agents/skills, which --project already covers.
#
# Default: symlinks each skill into your user-level skill directories, so
# editing the canonical copy updates every harness at once.
#
#   ./install.sh              user-level symlinks (recommended)
#   ./install.sh --copy       copy instead of symlink
#   ./install.sh --project    install into ./.claude/skills etc. of the
#                             current directory instead of your home dir
#
# GitHub Copilot note: Copilot is mainly REPO-SCOPED. Its canonical path is
# .github/skills in the repo root, which --project populates. Copilot also
# auto-reads a repo's .claude/skills. At user level it reads ~/.copilot/skills
# (VS 2026); for team-shared skills, prefer --project so they land in
# .github/skills and get committed with the repo.
#
# OpenCode needs no directory of its own: it natively reads the
# .claude/skills and .agents/skills paths installed below. For harnesses
# that only read AGENTS.md, copy the table from this repo's AGENTS.md into
# your project's AGENTS.md and vendor the skills/ folder into the repo.

MODE="link"
SCOPE="user"

for arg in "$@"; do
  case "$arg" in
    --copy)    MODE="copy" ;;
    --project) SCOPE="project" ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $arg (try --help)"; exit 1 ;;
  esac
done

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills" && pwd)"

if [ "$SCOPE" = "user" ]; then
  TARGETS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
    "$HOME/.gemini/config/skills"
    "$HOME/.gemini/skills"
    "$HOME/.agents/skills"
    "$HOME/.copilot/skills"
    "$HOME/.cursor/skills"
  )
else
  TARGETS=(
    ".claude/skills"
    ".codex/skills"
    ".agents/skills"
    ".github/skills"
  )
fi

installed=0
skipped=0

for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  for skill in "$SRC"/*/; do
    skill="${skill%/}"
    name="$(basename "$skill")"
    dest="$target/$name"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      echo "skip  $dest (already exists)"
      skipped=$((skipped + 1))
      continue
    fi
    if [ "$MODE" = "link" ]; then
      ln -s "$skill" "$dest"
      echo "link  $dest"
    else
      cp -r "$skill" "$dest"
      echo "copy  $dest"
    fi
    installed=$((installed + 1))
  done
done

echo ""
echo "Installed $installed, skipped $skipped."
echo "Start a fresh session in your agent so it rescans its skills."
echo "If a harness in this list is one you don't use, delete its directory; nothing else depends on it."
