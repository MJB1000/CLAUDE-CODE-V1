#!/usr/bin/env bash
# Bootstrap this folder into a fresh private GitHub repo under MJB1000.
#
# Run from INSIDE a standalone copy of this folder (not inside another git repo).
# Requires the GitHub CLI (`gh`) authenticated as the MJB1000 account.
#
# Usage:
#   ./bootstrap.sh                 # creates MJB1000/repo-radar (private)
#   ./bootstrap.sh youracct/name   # custom owner/name
set -euo pipefail

REPO="${1:-MJB1000/repo-radar}"

if [ -d .git ]; then
  echo "! This folder is already a git repo. Move it out of any parent repo first." >&2
  exit 1
fi

command -v gh >/dev/null || { echo "! GitHub CLI 'gh' not found: https://cli.github.com" >&2; exit 1; }

git init -q
git add .
git commit -qm "Initial commit — Repo Radar (scout + Claude curation routine)"
git branch -M main

# Creates the private repo, sets it as origin, and pushes main.
gh repo create "$REPO" --private --source=. --remote=origin --push

echo
echo "✅ Created and pushed: https://github.com/$REPO"
echo "Next:"
echo "  1. Add repo secrets GMAIL_USERNAME + GMAIL_APP_PASSWORD for email (see README.md)."
echo "  2. Set up the Claude curation routine (see ROUTINE.md)."
echo "  3. Trigger a first run: Actions tab → Repo Radar → Run workflow."
