# TDD Final — Complete Framework Audit

Date: 2026-04-07
Framework: Marketing Team v3
Files: 41 framework files + 7 skills + 8 templates
Test: Does every piece work, connect, and produce execution-ready output?

---

## 1. EASE OF USE — Can a new user start without friction?

| # | Test | Result | Evidence |
|---|---|---|---|
| U1 | CLAUDE.md has session prompt in first 15 lines | **GREEN** | Lines 8-13: copy-paste new + resume prompts |
| U2 | One-line description of what this is | **GREEN** | Lines 3-4: "Three AI agents... You are the Creative Director" |
| U3 | Output location obvious | **GREEN** | Line 21: "Your output lives in: deliverables/" |
| U4 | Single "start here" document | **GREEN** | Line 23: "Need more help? HOW-TO-GET-STARTED.md — everything else is optional" |
| U5 | User can brief in plain language | **GREEN** | Strategist Pre-Brief is a conversation, not a form to fill |
| U6 | Resume after break is one prompt | **GREEN** | Line 16-19: resume prompt in Quick Start |

---

## 2. AGENT ROLES — Are roles clear, complete, non-overlapping?

| # | Test | Result | Evidence |
|---|---|---|---|
| R1 | Strategist owns planning + launch gate | **GREEN** | Session Start → Pre-Brief → Brief → Launch Gate → Post-Publish all in STRATEGIST.md |
| R2 | Copywriter owns writing only | **GREEN** | Reads brief, writes plan, writes copy, self-checks, submits. Does not review or publish. |
| R3 | Designer owns review + design production | **GREEN** | Review flow (Must Fix/Should Fix/Escalate/Locked) + Figma production workflow |
| R4 | No role bleeds into another | **GREEN** | Copywriter can't publish. Designer can't rewrite copy. Strategist can't skip review. |
| R5 | Escalation paths are clear | **GREEN** | Charlie → Sofia (via brief). Dana → Sofia (via feedback). Sofia → CD (verbally + logged). |

---

## 3. HANDOFF FILES — Does every handoff have a template and clear ownership?

| # | Test | Result | Evidence |
|---|---|---|---|
| H1 | STRATEGY-BRIEF.md — complete template | **GREEN** | Context Block, audience, assets, constraints, production specs, execution checklist, DoD (split), variants, approvals, plan, escalations |
| H2 | REVIEW-REQUEST.md — complete template | **GREEN** | What was created, files changed, DoD self-check (self-checkable only), creative choices, known gaps |
| H3 | REVIEW-FEEDBACK.md — versioned rounds | **GREEN** | Append-not-overwrite, Round N format, locked sections, cleared summary |
| H4 | CAMPAIGN-LOG.md — full tracking | **GREEN** | Status, history, pending external clearances, known gaps (with resolution), brand decisions, learned patterns |
| H5 | SESSION-CHECKPOINT.md — 200-word limit | **GREEN** | Compression guidance, state, active deliverable, decisions, next actions, open questions |
| H6 | RETRO.md — post-publish learning | **GREEN** | What was caught, what worked, brief gaps, carry-forward rules, A/B variant results, metrics (7-day + 30-day with CD interpretation) |
| H7 | DESIGN-BRIEF.md — complete template | **GREEN** | Design system ref, Figma workspace, channel specs, brand assets, layout direction, flags, DoD |
| H8 | DESIGN-REQUEST.md — complete template | **GREEN** | What was designed, Figma link, design decisions, assets used, known gaps |

---

## 4. SKILLS — Does every skill exist, load correctly, and serve a clear purpose?

| # | Test | Result | Evidence |
|---|---|---|---|
| S1 | token-optimizer.md | **GREEN** | 5 rules + file access rules + response rules. Referenced in every agent + CLAUDE.md. |
| S2 | notion-publish.md | **GREEN** | Per-deliverable-type format templates (email, LP, Google Ads, social). Workspace structure. Publishing workflow. |
| S3 | notion-knowledge.md | **GREEN** | 4 DB schemas, agent-specific queries, auto-populate post-retro, 30-day promotion, offline fallback. |
| S4 | brief-quality.md | **GREEN** | 10-point rubric (completeness 5 + safety 3 + structure 2). Must pass 8/10. Strategist self-checks. |
| S5 | research.md | **GREEN** | WebSearch/WebFetch for client, competitor, channel, audience research. Time-boxed. Stored to files. |
| S6 | design-systems.md | **GREEN** | DESIGN.md integration. 3 usage options (custom, reference, start-from-reference). Wired to DESIGN-BRIEF. |
| S7 | figma-production.md | **GREEN** | 10 critical use_figma rules, 6-step marketing workflow, channel dimensions, section-by-section build patterns, validation with screenshots. |
| S8 | All skills registered in CLAUDE.md | **GREEN** | Lines 107-121: all 7 skills listed with load-when guidance. |

---

## 5. KNOWLEDGE LAYER — Does knowledge compound across campaigns?

| # | Test | Result | Evidence |
|---|---|---|---|
| K1 | Client profiles persist | **GREEN** | clients/CLIENT-TEMPLATE.md with brand identity, audience psychology, competitive context, approved assets, campaign history, client-specific patterns. Strategist loads at session start. |
| K2 | Channel knowledge grows | **GREEN** | knowledge/CHANNELS.md with per-channel constraints + patterns + anti-patterns. Updated post-retro. |
| K3 | Swipe file grows | **GREEN** | knowledge/SWIPE-FILE.md with copy that worked, tagged by channel/audience/metric. Charlie queries at writing time. |
| K4 | Playbook scales | **GREEN** | PLAYBOOK.md with validated/observed tags, 30-cap, 100-line split rule, grep-based loading. |
| K5 | All agents read learned patterns directly | **GREEN** | Charlie step 3 (hard gate), Dana step 3 (proactive check). Not dependent on Sofia alone. |
| K6 | Notion DB schemas defined | **GREEN** | notion-knowledge.md: Clients DB, Patterns DB, Swipe File DB, Campaign Tracker DB with typed properties. |
| K7 | Offline fallback exists | **GREEN** | notion-knowledge.md: "If Notion is not connected, fall back to local markdown files." |

---

## 6. CONTEXT FLOW — Does the CD's context reach every agent?

| # | Test | Result | Evidence |
|---|---|---|---|
| C1 | Sofia pulls MCP data before asking questions | **GREEN** | Pre-Brief Step 1: pull from GA4, email, ads, Notion. Step 2: open with data + questions. |
| C2 | Sofia asks follow-up questions (not one-shot) | **GREEN** | Step 3: "Keep asking until the brief is clear." Example follow-ups provided. |
| C3 | Sofia confirms understanding before writing | **GREEN** | Step 4: "Summarize back to CD in 2-3 sentences. Get a yes." |
| C4 | Campaign Context block exists in brief | **GREEN** | STRATEGY-BRIEF.md: Performance data, CD interpretation, what worked, what didn't. |
| C5 | Charlie reads Context Block | **GREEN** | COPYWRITER.md step 2: "Read the Campaign Context block first. It tells you WHY." |
| C6 | Dana reads Context Block | **GREEN** | DESIGNER.md step 2: "Read the Campaign Context block in STRATEGY-BRIEF.md." |
| C7 | Dana reviews for differentiation (not just brief compliance) | **GREEN** | DESIGNER.md What You Review: "Differentiation — Does this say something competitors CAN'T say?" |

---

## 7. EXECUTION READINESS — Can output be deployed without a meeting?

| # | Test | Result | Evidence |
|---|---|---|---|
| E1 | Brief includes production specs per deliverable | **GREEN** | STRATEGY-BRIEF.md: Production Specs table (platform, image/visual, dimensions, technical notes). |
| E2 | Brief includes execution checklist per deliverable | **GREEN** | STRATEGY-BRIEF.md: Execution Checklist (platform → audience → schedule → tracking → test → go-live). |
| E3 | Strategist fills checklist at launch gate | **GREEN** | STRATEGIST.md launch gate step 8: "Fill the Execution Checklist for each deliverable." |
| E4 | Email deliverables are paste-ready | **GREEN** | Subject, preview, body, CTA — all fields present. Proven in WiperTech simulation. |
| E5 | Google Ads are upload-ready | **GREEN** | 15 headlines + 4 descriptions per ad group within limits. Proven in WiperTech simulation. |
| E6 | Landing pages have visual specs | **GREEN** | Production Specs table + DESIGN-BRIEF.md for Figma production. |
| E7 | Social ads have creative specs | **GREEN** | Production Specs table covers image style + dimensions per platform. |

---

## 8. LEARNING LOOP — Does the framework get smarter?

| # | Test | Result | Evidence |
|---|---|---|---|
| L1 | Retro captures what worked + what didn't | **GREEN** | RETRO.md: Designer catches, Copywriter successes, brief gaps, carry-forward rules. |
| L2 | Metrics check-ins pull real data | **GREEN** | RETRO.md 7-day + 30-day: data pulled from MCPs, specific question asked to CD, CD's answer captured. |
| L3 | Patterns promoted by data + human judgment | **GREEN** | 30-day retro: "if metric confirms → validated. If contradicts → invalidated." CD interprets, not Sofia. |
| L4 | A/B variants tracked through to winner | **GREEN** | STRATEGY-BRIEF.md: Variants section. RETRO.md: Variant Results table with winner flag. |
| L5 | Learning feeds back into next brief | **GREEN** | Strategist step 4: reads Playbook. Brief template: Learned Patterns section. |
| L6 | Charlie's self-check is a hard gate on patterns | **GREEN** | COPYWRITER.md step 3: "verify your copy against every pattern. This is a hard gate, not a suggestion." |

---

## 9. DESIGN PRODUCTION — Is Figma integration complete?

| # | Test | Result | Evidence |
|---|---|---|---|
| D1 | Figma MCP registered | **GREEN** | figma-remote-mcp registered at https://mcp.figma.com/mcp |
| D2 | Production skill has official Figma rules | **GREEN** | figma-production.md: 10 critical use_figma rules from official docs |
| D3 | Marketing-specific build patterns exist | **GREEN** | LP, email, social ad section-by-section tables with what to build per call |
| D4 | Channel dimensions documented | **GREEN** | Table: LP 1440/375, email 600, FB feed 1080x1080, stories 1080x1920, etc. |
| D5 | Design system integration exists | **GREEN** | design-systems.md: DESIGN.md format, 55+ references from awesome-design-md |
| D6 | Figma auth is pending (user action required) | **YELLOW** | MCP registered but not authenticated. User must `/mcp → figma → Authenticate`. Cannot be fixed in framework — requires user's Figma credentials. |

---

## 10. MULTI-STAKEHOLDER — Does the framework support teams?

| # | Test | Result | Evidence |
|---|---|---|---|
| M1 | Multiple approvers supported | **GREEN** | STRATEGY-BRIEF.md: Approvals Required table (stakeholder, role, status, date). |
| M2 | Approvals persist across sessions | **GREEN** | Approval table lives in STRATEGY-BRIEF.md file, not conversation. |
| M3 | Launch gate checks all approvals | **GREEN** | STRATEGIST.md step 2: "All stakeholders must show Approved before publish." |

---

## FINAL SCORE

| Axis | Tests | GREEN | YELLOW | RED |
|---|---|---|---|---|
| Ease of Use | 6 | 6 | 0 | 0 |
| Agent Roles | 5 | 5 | 0 | 0 |
| Handoff Files | 8 | 8 | 0 | 0 |
| Skills | 8 | 8 | 0 | 0 |
| Knowledge Layer | 7 | 7 | 0 | 0 |
| Context Flow | 7 | 7 | 0 | 0 |
| Execution Readiness | 7 | 7 | 0 | 0 |
| Learning Loop | 6 | 6 | 0 | 0 |
| Design Production | 6 | 5 | 1 | 0 |
| Multi-Stakeholder | 3 | 3 | 0 | 0 |
| **TOTAL** | **63** | **62** | **1** | **0** |

**62 GREEN. 1 YELLOW (Figma auth — user action, not framework gap). 0 RED.**

The YELLOW is your Figma authentication — that's a credential handoff, not a framework fix.
The framework is structurally complete.

---
