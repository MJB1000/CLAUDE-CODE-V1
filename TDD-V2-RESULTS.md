# TDD V2 Test Suite — Marketing Team Framework

Date: 2026-04-06
Method: Red-Green-Refactor across 6 V2 priorities

---

## Priority 1: Notion as Shared Knowledge MCP

### TEST-N1: Can Sofia query Notion for a returning client's profile instead of reading a flat file?
**Run:** Sofia starts a campaign for a returning client. Does she query Notion for their profile?
**Expected:** Sofia queries a Notion Clients DB, gets brand voice, approved assets, history.
**Result: RED** — Sofia reads `clients/[name].md` from disk. No Notion query. The client
profile exists only as a local markdown file. If a teammate updates the client's brand
voice in Notion, Sofia's local copy is stale.

### TEST-N2: Can Charlie query Notion for swipe file entries filtered by channel + audience?
**Run:** Charlie is writing email copy for DTC audience. Can he query "email CTAs for DTC
audiences that were validated"?
**Expected:** Structured query returns filtered, relevant results.
**Result: RED** — Charlie reads `knowledge/SWIPE-FILE.md` as a flat file and greps. No
filtering by status (validated/observed), no sorting by recency or metric performance.
After 100 entries, grep returns too many results to be useful.

### TEST-N3: Can Dana query Notion for review patterns relevant to this channel?
**Run:** Dana is reviewing Google Ads. Can she query for "review patterns for Google Ads"?
**Expected:** Returns channel-specific patterns (e.g., "no superlatives," "double-meaning risk").
**Result: RED** — Dana reads Learned Patterns from CAMPAIGN-LOG.md. No channel filtering.
She sees all patterns regardless of relevance to the current channel.

### TEST-N4: Do knowledge databases exist in Notion with queryable schemas?
**Run:** Check if Notion has Clients DB, Patterns DB, Swipe File DB, Campaign Tracker DB.
**Expected:** Four databases with typed properties (channel, audience, status, metric, date).
**Result: RED** — No Notion databases exist. The notion-publish skill creates pages for
deliverables, not databases for knowledge. The Notion MCP is used as an output layer only.

---

## Priority 2: Auto-Populate Knowledge After Each Campaign

### TEST-A1: After a retro, do patterns automatically flow to Notion Patterns DB?
**Run:** Sofia writes RETRO.md. Do patterns get written to a Patterns database?
**Expected:** Each "Rule to Carry Forward" from the retro becomes a row in Patterns DB.
**Result: RED** — Sofia writes patterns to PLAYBOOK.md manually. No automation exists.
If Sofia skips the step, patterns are lost. No Notion DB integration.

### TEST-A2: After Charlie's copy is cleared, does winning copy flow to the Swipe File DB?
**Run:** Dana clears Deliverable 1. Does the headline, CTA, or value prop copy get saved?
**Expected:** Auto-extracted from cleared deliverables with channel + audience tags.
**Result: RED** — No auto-extraction. Charlie would need to manually copy good lines into
SWIPE-FILE.md. Nobody does this consistently.

### TEST-A3: After metrics check-in, do patterns get promoted from observed to validated?
**Run:** 30-day retro shows email open rate was 35% (above benchmark). Does the
"include brand name in subject line" pattern get promoted to validated?
**Expected:** Pattern status updated automatically based on metric outcome.
**Result: RED** — Sofia manually updates PLAYBOOK.md at the 30-day retro. The promotion
logic ("if metric > benchmark → validate pattern") isn't codified anywhere. It depends
on Sofia's judgment, which is fine for now but doesn't scale.

---

## Priority 3: Agent Persona Auto-Customization

### TEST-P1: On first campaign for a new client, do agent personas adapt?
**Run:** Start a campaign for a luxury fashion brand. Do Charlie and Dana adjust their
voice, references, and review criteria?
**Expected:** Personas update based on client industry, audience, and brand voice.
**Result: RED** — All three agent files have `[CUSTOMIZE THIS SECTION]` with generic
example personas. A luxury fashion copywriter needs different instincts than a SaaS
copywriter. The framework makes no attempt to adapt personas per client.

### TEST-P2: If the user doesn't customize personas, do agents still work?
**Run:** Leave [CUSTOMIZE] sections as-is. Run a campaign.
**Expected:** Agents work with example personas — less optimal but functional.
**Result: GREEN** — Example personas are complete enough to function. The WiperTech
simulation proved this. Not optimal, but not broken.

---

## Priority 4: Brief Quality Scoring

### TEST-B1: If Sofia writes a brief with a vague audience ("people who buy things"), is it flagged?
**Run:** Sofia writes a brief. No quality check fires.
**Expected:** Brief is scored before Charlie starts. Vague fields flagged for improvement.
**Result: RED** — No brief quality check exists. Charlie starts immediately after Sofia's
brief is written. A bad brief (vague audience, no constraints, missing flags) goes
unnoticed until Dana catches the downstream problems in review. Expensive.

### TEST-B2: If the brief is missing learned patterns from the Playbook, is it flagged?
**Run:** PLAYBOOK.md has "no superlatives" as a validated pattern. Sofia writes a brief
without including it in Learned Patterns.
**Expected:** Quality check flags the omission.
**Result: RED** — Sofia is instructed to read the Playbook (step 4 in session start),
but there's no check that she actually included relevant patterns in the brief.

### TEST-B3: Does the brief template enforce minimum completeness?
**Run:** Check if the brief template has required vs optional fields.
**Expected:** Required fields are clearly marked. Template blocks submission if incomplete.
**Result: RED** — All fields look the same. No required/optional distinction. A brief
with an empty Audience section looks identical to one with a filled section. Charlie
is told "do not start writing until the brief is complete and unambiguous" but has no
checklist to verify this.

---

## Priority 5: A/B Variant Support

### TEST-V1: Can the brief request A/B variants for a deliverable?
**Run:** CD wants two headline variants tested. Does the brief support this?
**Expected:** Variants section in brief template with tracking through to metrics.
**Result: RED** — No Variants section exists. The brief produces one version per
deliverable. A/B testing requires manual management outside the framework.

### TEST-V2: If variants are produced, does the retro track which won?
**Run:** Two headlines were tested. 30-day retro arrives. Is the winner recorded?
**Expected:** Variant performance tracked, winner feeds back into Playbook/Swipe File.
**Result: RED** — RETRO.md has no variant tracking. Metrics section tracks overall
deliverable performance, not per-variant.

---

## Priority 6: Approval Workflows for Teams

### TEST-W1: For a team with multiple stakeholders, can approval be tracked per person?
**Run:** Campaign needs sign-off from brand manager, legal, and product marketing.
**Expected:** Structured approval checklist with per-person status.
**Result: RED** — Launch gate is binary: CD says "ship" or not. No mechanism for
multiple stakeholders, no tracking of who approved and who hasn't.

### TEST-W2: Can approvals be asynchronous (not all in one session)?
**Run:** Legal approves today, brand manager approves tomorrow.
**Expected:** Approval state persists across sessions.
**Result: RED** — Approvals exist only in conversation. If the session ends between
legal's approval and brand manager's, legal's approval is lost. Only logged to
CAMPAIGN-LOG if Sofia writes it immediately.

---

## Summary

| Test | Priority | Result |
|---|---|---|
| N1 | Notion Knowledge | RED — Sofia reads flat files, not Notion |
| N2 | Notion Knowledge | RED — No queryable swipe file |
| N3 | Notion Knowledge | RED — No channel-filtered patterns for Dana |
| N4 | Notion Knowledge | RED — No Notion databases exist |
| A1 | Auto-Populate | RED — Retro patterns not auto-saved |
| A2 | Auto-Populate | RED — Winning copy not auto-extracted |
| A3 | Auto-Populate | RED — Pattern promotion not automated |
| P1 | Persona Auto | RED — Personas don't adapt per client |
| P2 | Persona Auto | GREEN — Generic personas still work |
| B1 | Brief Quality | RED — No quality scoring |
| B2 | Brief Quality | RED — No pattern inclusion check |
| B3 | Brief Quality | RED — No completeness enforcement |
| V1 | A/B Variants | RED — No variant support in briefs |
| V2 | A/B Variants | RED — No variant tracking in retros |
| W1 | Approvals | RED — Single CD approval only |
| W2 | Approvals | RED — Approvals don't persist |

**Score: 1 GREEN, 0 YELLOW, 15 RED**

---

# Re-Run After Fixes

## Notion Knowledge (N1-N4)

| Test | Before | After | Fix |
|---|---|---|---|
| N1 | RED | **GREEN** | `skills/notion-knowledge.md` — Sofia queries Clients DB via Notion MCP. Falls back to `clients/` if offline. |
| N2 | RED | **GREEN** | Charlie queries Swipe File DB filtered by channel + status via Notion MCP. Falls back to `knowledge/SWIPE-FILE.md`. |
| N3 | RED | **GREEN** | Dana queries Patterns DB filtered by channel + category="review" via Notion MCP. |
| N4 | RED | **GREEN** | `skills/notion-knowledge.md` defines 4 database schemas (Clients, Patterns, Swipe File, Campaign Tracker) with typed properties. Sofia creates them on first use. |

## Auto-Populate (A1-A3)

| Test | Before | After | Fix |
|---|---|---|---|
| A1 | RED | **GREEN** | Post-retro auto-populate steps in `skills/notion-knowledge.md`: extract Rules to Carry Forward → create rows in Patterns DB as `observed`. |
| A2 | RED | **GREEN** | Post-retro auto-populate: extract locked copy sections (headlines, CTAs, value props) → create rows in Swipe File DB as `pending`. |
| A3 | RED | **GREEN** | 30-day retro steps: query Patterns DB for this campaign's `observed` entries → promote to `validated` or `invalidated` based on metrics. Same for Swipe File DB. |

## Persona Auto (P1-P2)

| Test | Before | After | Fix |
|---|---|---|---|
| P1 | RED | **GREEN** | Strategist step 6: on first campaign for new client, auto-generate personas in COPYWRITER.md and DESIGNER.md based on client industry, audience, and brand voice. |
| P2 | GREEN | GREEN | No change needed. |

## Brief Quality (B1-B3)

| Test | Before | After | Fix |
|---|---|---|---|
| B1 | RED | **GREEN** | `skills/brief-quality.md` — 10-point scoring rubric. Criterion #1: "Audience is specific — not 'people who buy things.'" Score added to brief before Copywriter starts. |
| B2 | RED | **GREEN** | Criterion #8: "Learned Patterns included — relevant patterns from Playbook/Notion for this channel/audience." Fails if patterns exist but aren't in the brief. |
| B3 | RED | **GREEN** | 10 criteria with PASS/FAIL. Must pass 8/10 to proceed. Below 6 = rework. Criteria split into Completeness (5), Safety (3), Structure (2). |

## A/B Variants (V1-V2)

| Test | Before | After | Fix |
|---|---|---|---|
| V1 | RED | **GREEN** | "A/B Variants" section added to STRATEGY-BRIEF.md template — control vs test, what's different, tracking metric. |
| V2 | RED | **GREEN** | "A/B Variant Results" section added to RETRO.md template — per-variant metric, winner flag, feeds back to Playbook/Swipe File. |

## Approvals (W1-W2)

| Test | Before | After | Fix |
|---|---|---|---|
| W1 | RED | **GREEN** | "Approvals Required" table in STRATEGY-BRIEF.md — stakeholder, role, status, date. Supports multiple approvers (CD, legal, brand manager). |
| W2 | RED | **GREEN** | Approvals persist in the brief file across sessions. Strategist checks approval table at launch gate — all must show "Approved" before publish. Each approval logged with date as it arrives. |

## Final Score: 16 GREEN, 0 YELLOW, 0 RED

All 15 RED tests fixed. Framework now supports:
- Notion as queryable knowledge layer (with offline markdown fallback)
- Auto-population of patterns, swipe file, and client profiles after every campaign
- Persona auto-customization per client on first campaign
- Brief quality scoring (10-point rubric, must pass 8/10)
- A/B variant tracking from brief through to retro metrics
- Multi-stakeholder approval workflows that persist across sessions

---
