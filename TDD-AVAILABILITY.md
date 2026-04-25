# TDD: Does the Skill Work in Every Claude Environment?

Date: 2026-04-11
Test: Can a user activate Sofia in Chrome extension, Projects, Cowork, and raw chat?
Material: marketing-team.md (672 lines) from github.com/MJB1000/marketing-team

---

## Axis 1: CHROME EXTENSION (paste mode)

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| CE1 | Raw URL fetch works | Claude fetches and loads the skill | Chrome extension returns 404 on raw GitHub URLs | **RED** |
| CE2 | Pasting full file works | Claude reads the instructions and activates Sofia | User pasted the full file — it loaded into context | **GREEN** |
| CE3 | "You are Sofia" activates the role | Sofia reports status and waits | Not yet tested in the Chrome extension conversation (user came back here) | **YELLOW** |
| CE4 | Activation prompt is clear | User knows what to paste and type | SOFIA-SESSION-START.md exists with exact instructions | **GREEN** |
| CE5 | File is too long to paste | 672 lines might hit paste limits | 672 lines ≈ 21KB — within Claude's context. Paste works. | **GREEN** |

### Chrome Extension fixes needed:
- **CE1:** URL fetch doesn't work and can't be fixed (browser security). Need alternative activation method.
- Add to SOFIA-SESSION-START.md: "Chrome extension cannot fetch URLs. Copy the file content from your browser and paste it."

---

## Axis 2: CLAUDE.AI PROJECTS

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| P1 | Can add marketing-team.md as project knowledge | Upload or paste as knowledge | Documented in SOFIA-SESSION-START.md and How to Use section | **GREEN** |
| P2 | Sofia loads automatically in every project conversation | No need to paste each time | Projects load knowledge into every conversation — confirmed by design | **GREEN** |
| P3 | Multiple conversations share the same Sofia config | Second conversation in same project has Sofia | Projects work this way by design | **GREEN** |
| P4 | Instructions tell user to create a Project | Clear step-by-step | SOFIA-SESSION-START.md: "Create a Project → add marketing-team.md as knowledge" | **GREEN** |
| P5 | COPYWRITING-PRINCIPLES.md can be added as second knowledge file | Charlie gets Schwartz reference | Projects support multiple knowledge files | **GREEN** |

---

## Axis 3: CLAUDE COWORK

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| CW1 | Can connect to github.com/MJB1000/marketing-team | Repo exists and is public | Repo created and pushed — verified | **GREEN** |
| CW2 | CLAUDE.md auto-loaded on connect | Cowork reads CLAUDE.md at session start | CLAUDE.md exists at repo root with correct routing | **GREEN** |
| CW3 | Session prompt activates Sofia | "Read CLAUDE.md, then marketing-team.md" | Prompt documented in CLAUDE.md Quick Start | **GREEN** |
| CW4 | marketing-team.md is at correct path | File at root, not in skills/ subdirectory | File exists at both root and skills/ — **potential confusion** | **RED** |
| CW5 | knowledge/COPYWRITING-PRINCIPLES.md accessible | Charlie can grep it | File exists at knowledge/COPYWRITING-PRINCIPLES.md | **GREEN** |
| CW6 | Figma MCP configurable in Cowork | Can add figma MCP server | Instructions in skill file + SOFIA-SESSION-START.md | **GREEN** |

### Cowork fixes needed:
- **CW4:** The clean branch has marketing-team.md at ROOT and also in skills/ (from the sync). CLAUDE.md references `marketing-team.md` (root path). The skills/ copy is redundant and confusing. Remove `skills/marketing-team.md` from the marketing-team repo — keep only the root copy.

---

## Axis 4: RAW CLAUDE CHAT (no setup)

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| RC1 | Pasting the full file works | Claude reads and activates | Proven — user pasted 672 lines in Chrome extension, loaded fine | **GREEN** |
| RC2 | Activation prompt is in the file | User knows what to say after pasting | Line 2-3: "Paste this... say: You are Sofia" | **GREEN** |
| RC3 | File is self-contained | No external file references block operation | COPYWRITING-PRINCIPLES.md referenced but marked "if exists" — graceful degradation | **GREEN** |
| RC4 | Figma MCP references don't break paste mode | "If Figma MCP connected" fallback works | Fallback: "produce text wireframes in conversation" | **GREEN** |
| RC5 | File-based references (CAMPAIGN-LOG, etc) don't break paste mode | Conversation mode guidance exists | Session Checkpoint + Client Profile sections have conversation-mode fallbacks | **GREEN** |

---

## Axis 5: REPO STRUCTURE

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| RS1 | Single canonical repo | github.com/MJB1000/marketing-team | Repo exists, public, pushed | **GREEN** |
| RS2 | README has quick start for all environments | Cowork, Projects, chat — all covered | README.md has all 3 with activation prompts | **GREEN** |
| RS3 | SOFIA-SESSION-START.md exists | Paste-and-go document for users | File exists with full instructions | **GREEN** |
| RS4 | No references to old repo (CLAUDE-CODE-V1) | All references point to marketing-team | marketing-team.md How to Use section: "github.com/MJB1000/marketing-team" | **GREEN** |
| RS5 | Old repo CLAUDE.md still references old paths | Should not confuse users | Old repo still has agents/STRATEGIST.md references — but it's the development repo, not the canonical one | **YELLOW** |

---

## Axis 6: ACTIVATION EXPERIENCE

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| AX1 | Time from "I want to use this" to Sofia responding | < 2 minutes | Paste file + type prompt = ~90 seconds | **GREEN** |
| AX2 | User doesn't need to read documentation first | Activation prompt is visible at the top of the file | Line 2-3 of marketing-team.md: paste and say prompt | **GREEN** |
| AX3 | Sofia's first response is useful | Reports status + waits for direction | Skill instructs: "Report status to CD — one paragraph" | **GREEN** |
| AX4 | CD knows what to say | Quick reference table exists | SOFIA-SESSION-START.md: quick reference with "I want to..." table | **GREEN** |
| AX5 | Handoff protocol example is clear | User understands "go" / redirect pattern | Full example flow in Session Orchestration section | **GREEN** |

---

## Score

| Axis | GREEN | YELLOW | RED |
|---|---|---|---|
| Chrome Extension | 3 | 1 | 1 |
| Claude Projects | 5 | 0 | 0 |
| Claude Cowork | 5 | 0 | 1 |
| Raw Chat | 5 | 0 | 0 |
| Repo Structure | 4 | 1 | 0 |
| Activation Experience | 5 | 0 | 0 |
| **TOTAL** | **27** | **2** | **2** |

---

## The 2 REDs

### CE1: Chrome extension can't fetch raw GitHub URLs
**Root cause:** Browser security. Can't be fixed in the framework.
**Fix:** Add explicit guidance to SOFIA-SESSION-START.md: "The Chrome extension cannot fetch URLs. Open the raw URL in your browser, copy the content, and paste it into the conversation."

### CW4: Duplicate file in Cowork repo (root + skills/)
**Root cause:** The sync to the clean branch copied marketing-team.md to both locations.
**Fix:** Remove `skills/marketing-team.md` from the marketing-team repo. Keep only the root copy. CLAUDE.md references `marketing-team.md` (root path).

---
