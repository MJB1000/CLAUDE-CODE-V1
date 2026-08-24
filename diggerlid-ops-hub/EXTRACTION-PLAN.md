# Extraction Plan — `diggerlid-ops-hub` → its own repo

**Why:** tighter access control (teammates see only the BI system, not the unrelated
marketing-team templates / repo-radar / simulations), a clean root `CLAUDE.md` (already
written — this folder's `CLAUDE.md` becomes the repo root), simpler mental model.

## Steps (run from any machine with git + GitHub access)

```bash
# 1. Create the new PRIVATE repo on GitHub first (empty, no README):  <org-or-user>/diggerlid-ops-hub

# 2. Clone the source repo and split the subfolder with full history
git clone https://github.com/MJB1000/CLAUDE-CODE-V1.git
cd CLAUDE-CODE-V1
git checkout claude/blitzos-build-qhutfl
git subtree split --prefix=diggerlid-ops-hub -b ops-hub-only

# 3. Push the split branch into the new repo as main
git push https://github.com/<org-or-user>/diggerlid-ops-hub.git ops-hub-only:main
```

(`git subtree split` preserves the folder's commit history. For a no-history fresh start,
just copy the folder into a new repo instead.)

## Post-extraction checklist
- [ ] New repo default branch = `main`; branch protection on `main` (PR-based writes).
- [ ] Invite teammates: read = analysts/brief readers · write = CoS + Scorekeeper owners.
- [ ] Each teammate connects the new repo via GitHub connector in their Claude account.
- [ ] Rebuild automations per `AUTOMATIONS.md` (they point at repo paths, which are unchanged).
- [ ] Update the Vercel dashboard note + any hard links that referenced `CLAUDE-CODE-V1`.
- [ ] In the OLD repo: replace `diggerlid-ops-hub/` with a pointer README ("moved to <new repo>")
      to avoid two-sources-of-truth drift. Do NOT run two live copies.
- [ ] Verify bootstrap: fresh Claude session + `CLAUDE.md` session-start → status report works.

## Decision needed
- Which GitHub org/user owns the new repo (personal vs company org — org recommended for
  team permissions).
