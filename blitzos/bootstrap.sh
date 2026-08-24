#!/usr/bin/env bash
#
# BlitzOS bootstrap — initialize member repos as gitlinks using a fine-grained
# token, in the cloud or locally. Source code and history stay in the member
# repos; this context monorepo only holds pointers, the map, and the work log.
#
# Usage:
#   BLITZOS_GIT_TOKEN=github_pat_xxx ./bootstrap.sh
#
# The token needs read access (contents) to the member repos under owner MJB1000.
# It is used only to fetch the pinned submodule tips; it is never written to disk
# in this repo. See CLOUD-SETUP.md for creating the token.

set -euo pipefail

umask 077

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
cd "$repo_dir"

owner="MJB1000"

# --- refuse to run if this context repo is carrying credentials ------------------
# The whole security model is: no secrets in the context monorepo. Fail loudly
# rather than push a token into shared history.
secret_pattern='-----BEGIN [A-Z ]*PRIVATE KEY-----|github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|(?i)(secret|api[_-]?key|password|token)\s*[:=]\s*["'\''][^"'\'' ]{12,}'
if git ls-files -z 2>/dev/null | grep -zvE '(^|/)(bootstrap\.sh|CLOUD-SETUP\.md)$' | \
   xargs -0 -r grep -HInaoP "$secret_pattern" 2>/dev/null; then
  printf 'blitzos: refusing to bootstrap — credential-like content found above. Remove it first.\n' >&2
  exit 1
fi

if [ -z "${BLITZOS_GIT_TOKEN:-}" ]; then
  cat >&2 <<'MSG'
blitzos: BLITZOS_GIT_TOKEN is not set.
  In Claude cloud, prefer launching via Anthropic's native GitHub rail (no token).
  For "power mode" (bootstrapping submodules yourself), export a fine-grained token:
    BLITZOS_GIT_TOKEN=github_pat_xxx ./bootstrap.sh
  See CLOUD-SETUP.md.
MSG
  exit 1
fi

# Use the token only for this process's fetches, via an ephemeral credential helper.
# Never persisted to the repo config on disk in a readable form.
auth_header="Authorization: Bearer ${BLITZOS_GIT_TOKEN}"

git submodule sync --recursive

# init + update each pinned gitlink with the token supplied inline.
git -c http.https://github.com/.extraheader="$auth_header" \
    submodule update --init --recursive --depth 1 --jobs 4

printf 'blitzos: %s member repos initialized under repos/ (owner: %s)\n' \
  "$(git config --file .gitmodules --get-regexp path | wc -l | tr -d ' ')" "$owner"
printf 'blitzos: read CLAUDE.md, then the latest file in sessions/, before you start.\n'
