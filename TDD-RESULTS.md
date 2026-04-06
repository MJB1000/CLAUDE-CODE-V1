# TDD Test Suite — Marketing Team Framework v1

Date: 2026-04-06
Method: Red-Green-Refactor across 3 axes

---

## Axis 1: Ease of Use

### TEST-U1: Cold start — can a new user go from clone to first brief in under 3 minutes?
**Run:** Read CLAUDE.md → find the session start prompt → understand what to paste.
**Expected:** One clear, copy-paste-ready prompt in CLAUDE.md or linked from it.
**Result: RED** — CLAUDE.md has no session prompt. It has orchestration rules, file loading
instructions, and routing logic. A new user must find HOW-TO-GET-STARTED.md or
examples/session-start.md to know what to paste. The entry point is buried.

### TEST-U2: Does CLAUDE.md tell the user what this framework IS in the first 3 lines?
**Run:** Read lines 1-5 of CLAUDE.md.
**Expected:** A one-line description of what this is and who it's for.
**Result: RED** — Line 1 is "# Marketing Team — Session Router". Line 3 is "## Token Rules."
A new user opening this file has no idea what it does or why it exists. It jumps
straight into implementation rules. No welcome, no orientation, no "start here."

### TEST-U3: Can the user brief Sofia without knowing framework terminology?
**Run:** User says "I need a landing page for my product launch."
**Expected:** Sofia asks clarifying questions in plain language, not framework jargon.
**Result: GREEN** — Sofia's role file says "Do not ask the Creative Director to summarize.
Read the files." and "Report status... one paragraph." The brief-writing process is
conversational. No terminology leaks. Pass.

### TEST-U4: Does the user know where their finished content is?
**Run:** After a full cycle, where does the user find their publishable copy?
**Expected:** Clear, obvious output location.
**Result: RED** — deliverables/ exists but CLAUDE.md doesn't mention it until line 64
under a small "Deliverable Artifacts" section. The user's #1 question — "where is my
stuff?" — is answered 64 lines into a file they may not read. It should be prominent.

### TEST-U5: Can the user resume after a break without reading documentation?
**Run:** User returns after 3 days. What do they paste?
**Expected:** The checkpoint or a clear resume prompt.
**Result: RED** — SESSION-CHECKPOINT.md has the state, but the user needs to know to
spin up Sofia with the resume prompt. That prompt lives in examples/session-start.md
and HOW-TO-GET-STARTED.md. Nothing in the project root says "paste this to resume."

### TEST-U6: Is there one single file that tells a new user everything they need?
**Run:** Count how many files a new user might need to read before starting.
**Expected:** One file, under 2 minutes of reading.
**Result: RED** — There are 5 candidate files: README.md, HOW-TO-GET-STARTED.md,
WORKFLOW-GUIDE.md, INSTALL.md, examples/session-start.md. A new user doesn't know
which one to read. Analysis paralysis.

---

## Axis 2: Self-Learning

### TEST-L1: After one campaign, does the next brief automatically include learned patterns?
**Run:** Complete Deliverable 1. Start Deliverable 2. Does STRATEGY-BRIEF.md template
prompt Sofia to include patterns?
**Expected:** Yes — the template has a "Learned Patterns" section.
**Result: GREEN** — STRATEGY-BRIEF.md has "### Learned Patterns" that references
CAMPAIGN-LOG. Sofia is instructed to read PLAYBOOK.md at session start (step 4). Pass.

### TEST-L2: Can the framework distinguish high-confidence patterns from guesses?
**Run:** Check if patterns have confidence levels.
**Expected:** Yes — validated vs observed.
**Result: GREEN** — PLAYBOOK.md has validated/observed tagging with promotion at
30-day retro. Pass.

### TEST-L3: Does the framework learn from WHAT WORKED, not just what failed?
**Run:** Check RETRO.md template.
**Expected:** Captures both successes and failures.
**Result: GREEN** — RETRO.md has "What Designer Caught" AND "What Copywriter Got Right
First Time." Both populate the playbook. Pass.

### TEST-L4: Does the framework learn about the CLIENT, not just about marketing?
**Run:** After a campaign for WiperTech, does the framework store WiperTech-specific
knowledge (brand voice, audience insights, approved assets)?
**Expected:** Yes — client profile persists across campaigns.
**Result: RED** — No client profile mechanism exists. PLAYBOOK.md stores generic marketing
patterns. CAMPAIGN-LOG stores campaign-specific data but is overwritten per campaign.
If you run a second campaign for the same client 3 months later, Sofia knows generic
patterns but has lost all WiperTech-specific context (their tone, audience, what
claims are approved, what their competitors say, which stats are verified).

### TEST-L5: Does the framework learn about CHANNELS over time?
**Run:** After running 5 email campaigns, does the framework know what subject line
length works, what CTA formats convert, what tone resonates?
**Expected:** Channel-specific patterns accumulate.
**Result: YELLOW** — PLAYBOOK.md has a "Channel Patterns" section, but it requires
manual entry by Sofia. There's no structured way to capture channel-specific data
(e.g., "email open rates by subject line length"). It's freeform text in a table.
Partially passes — structure exists but is too loose.

### TEST-L6: Do the agents learn from EACH OTHER across campaigns?
**Run:** Dana catches superlatives twice. Does Charlie learn to avoid them without
Dana flagging it again?
**Expected:** Yes — the pattern feeds into the brief and Charlie's self-check.
**Result: YELLOW** — The pattern lands in PLAYBOOK.md and CAMPAIGN-LOG Learned Patterns,
which Sofia reads when writing the next brief. But Charlie doesn't read the Playbook
directly — he only sees what Sofia puts in the brief's Learned Patterns section.
If Sofia forgets to include it, Charlie repeats the mistake. The learning chain has
a single point of failure: Sofia's brief-writing diligence.

---

## Axis 3: Knowledge MCPs (Growing Knowledge Access)

### TEST-K1: Does Sofia have access to market/competitor intelligence that grows?
**Run:** Check what knowledge sources Sofia can access beyond the project files.
**Expected:** Web search, competitor monitoring, industry data.
**Result: RED** — Sofia reads project files only. No web search, no competitor
monitoring, no industry benchmarks. She cannot research a client's market, check
competitor campaigns, or access current industry data. She operates in a closed
file system. For a strategist, this is a critical gap.

### TEST-K2: Does Charlie have access to copy best practices that grow?
**Run:** Check what reference material Charlie can access.
**Expected:** Swipe files, tone references, channel-specific copy guides.
**Result: RED** — Charlie reads the brief and the token optimizer. No swipe file,
no copy reference library, no channel-specific writing guides. He relies entirely
on his training data + the brief. There's no mechanism to build a growing library
of "copy that worked" from past campaigns.

### TEST-K3: Does Dana have access to brand/design knowledge that grows?
**Run:** Check what reference material Dana can access.
**Expected:** Brand guidelines, competitor visual analysis, design system references.
**Result: YELLOW** — Dana has design-systems/ (DESIGN.md files) and the Figma MCP.
But she has no mechanism to store and recall brand-specific review patterns. She catches
the same superlative issue every campaign because her knowledge resets each session.
The Playbook helps (if Sofia includes it in the brief), but Dana doesn't read it directly.

### TEST-K4: Can agents access external knowledge sources (MCP) that compound?
**Run:** Check what MCP servers are configured and what knowledge they provide.
**Expected:** Each agent has access to relevant external knowledge.
**Result: RED** — Two MCPs registered (Notion, Figma) but both are OUTPUT tools, not
INPUT/knowledge tools. No agent has access to:
- Web search (for market research, competitor analysis)
- Industry databases (for benchmarks, trends)
- Content libraries (for swipe files, reference copy)
- Analytics platforms (for performance data to close the learning loop)
The MCP ecosystem is write-only. Agents cannot pull knowledge in.

### TEST-K5: Is there a mechanism for knowledge to compound across sessions?
**Run:** After 10 campaigns, is agent #11 meaningfully smarter than agent #1?
**Expected:** Yes — accumulated knowledge makes each campaign faster and better.
**Result: YELLOW** — PLAYBOOK.md grows, but it's a flat markdown table. After 30+
patterns it becomes unwieldy. No indexing, no relevance filtering, no automatic
retrieval. Sofia reads the whole thing at session start and manually picks what's
relevant. This doesn't scale. Campaign #50 has the same cold-start problem as #1
if the Playbook is too long to load in context.

---

## Summary

| Test | Axis | Result |
|---|---|---|
| U1 | Ease of use | RED — no session prompt in CLAUDE.md |
| U2 | Ease of use | RED — no orientation in first 3 lines |
| U3 | Ease of use | GREEN |
| U4 | Ease of use | RED — output location buried |
| U5 | Ease of use | RED — no resume guidance at project root |
| U6 | Ease of use | RED — too many starting documents |
| L1 | Self-learning | GREEN |
| L2 | Self-learning | GREEN |
| L3 | Self-learning | GREEN |
| L4 | Self-learning | RED — no client profiles |
| L5 | Self-learning | YELLOW — channel learning is freeform |
| L6 | Self-learning | YELLOW — learning chain depends on Sofia |
| K1 | Knowledge MCP | RED — no market intelligence access |
| K2 | Knowledge MCP | RED — no copy reference library |
| K3 | Knowledge MCP | YELLOW — design refs exist, no review memory |
| K4 | Knowledge MCP | RED — MCPs are output-only, no input |
| K5 | Knowledge MCP | YELLOW — playbook doesn't scale |

**Score: 3 GREEN, 4 YELLOW, 10 RED**

---

# Re-Run After Fixes

## Ease of Use — Re-Test

| Test | Before | After | Fix |
|---|---|---|---|
| U1 | RED | **GREEN** | Quick Start block with copy-paste prompt added to top of CLAUDE.md |
| U2 | RED | **GREEN** | One-line description + "You are the Creative Director" in first 3 lines |
| U3 | GREEN | GREEN | No change needed |
| U4 | RED | **GREEN** | "Your output lives in: `deliverables/`" in Quick Start block |
| U5 | RED | **GREEN** | Resume prompt in Quick Start block |
| U6 | RED | **GREEN** | Quick Start says "Need more help? Read HOW-TO-GET-STARTED.md — everything else is optional" |

## Self-Learning — Re-Test

| Test | Before | After | Fix |
|---|---|---|---|
| L1 | GREEN | GREEN | No change needed |
| L2 | GREEN | GREEN | No change needed |
| L3 | GREEN | GREEN | No change needed |
| L4 | RED | **GREEN** | Client profiles in `clients/[name].md` — persist across campaigns, updated post-retro |
| L5 | YELLOW | **GREEN** | Structured `knowledge/CHANNELS.md` with per-channel constraints + patterns |
| L6 | YELLOW | **GREEN** | Charlie reads Learned Patterns + CHANNELS.md + SWIPE-FILE.md directly. Dana reads Learned Patterns directly. Learning no longer depends solely on Sofia's brief. |

## Knowledge MCPs — Re-Test

| Test | Before | After | Fix |
|---|---|---|---|
| K1 | RED | **GREEN** | `skills/research.md` — Sofia uses WebSearch/WebFetch for market/competitor intelligence |
| K2 | RED | **GREEN** | `knowledge/SWIPE-FILE.md` — Charlie's growing copy reference library |
| K3 | YELLOW | **GREEN** | Dana reads Learned Patterns directly + has design-systems/ |
| K4 | RED | **YELLOW** | Research skill uses WebSearch/WebFetch (input). Notion/Figma (output). Still no analytics API integration for automated metrics. Upgrade path: add GA4/Klaviyo/Meta MCPs. |
| K5 | YELLOW | **GREEN** | Playbook grep-based loading (not full read), 100-line split rule, category-based scaling |

## Final Score: 14 GREEN, 1 YELLOW, 0 RED

The remaining YELLOW (K4 — analytics MCPs) requires external API integrations that
depend on the user's specific tech stack. The framework now has the mechanism (retro
metrics sections, playbook promotion) — it just needs the data pipes connected.

---
