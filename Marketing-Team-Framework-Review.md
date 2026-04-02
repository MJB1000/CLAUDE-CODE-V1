# Marketing Team Framework — Review Summary

**Date:** 2026-04-02 | **Source:** three-man-team by russelleNVy | **PR:** MJB1000/CLAUDE-CODE-V1#1

---

## Framework Overview

Three AI agents with structured file-based handoffs:

| Role | Job | Flow |
|---|---|---|
| **Strategist** (Sofia) | Plans campaigns, writes briefs, owns launch gate | Brief → |
| **Copywriter** (Charlie) | Writes content from briefs | → Draft → |
| **Designer** (Dana) | Brand guardian, quality gate | → Review → Launch |

**Creative Director (you)** makes brand/business decisions. Strategist manages everything else.

**Core principle:** Handoffs through files, not conversation. Each agent reads only what it needs. Token waste is structural — fix the structure, fix the behavior.

---

## Simulation: SaaS Landing Page for Mid-Market CFOs

**Product:** Clarifi Analytics (AI-powered analytics)
**Deliverable:** Landing page — headline, 3 value props, CTA, social proof

### Sprint Flow

| Step | Who | What Happened |
|---|---|---|
| 1 | Sofia | Wrote brief with 4 flags (no real quotes, exact spelling, no AI hype, no unapproved ROI claims) |
| 2 | Charlie | Submitted plan — lead with CFO pain, not product. Mixed social proof format. Sofia approved. |
| 3 | Charlie | Wrote draft: "Stop chasing the numbers. Start acting on them." + 3 value props + CTA |
| 4 | Dana | **Round 1 — 2 Must Fix, 2 Should Fix, 1 Escalation** |
| 5 | Charlie | Fixed all 4 items in one pass |
| 6 | Dana | **Round 2 — All clear.** |
| 7 | Sofia | Logged to Campaign Log. Checkpoint written. Awaiting CD sign-off. |

### What Dana Caught

| Severity | Issue | Resolution |
|---|---|---|
| **Must Fix** | "3x more forecast accuracy" — not a coherent metric | Rewritten to qualitative language with [SOURCE NEEDED] |
| **Must Fix** | "without adding headcount" — drift from brief (brief says speed-to-insight, not cost) | Removed. Replaced with brief-aligned messaging |
| **Should Fix** | Placeholder quote had specific fabricated numbers — could be mistaken for real data | Replaced with clearly templated placeholder |
| **Should Fix** | CTA title case inconsistency | Flagged for brand guide decision |
| **Escalate** | "See Clarifi With Your Data" implies personalized demo — does sales team deliver that? | Deferred to CD. CTA changed to "Book a Demo" |

### Simulation Verdict

**The framework works.** The handoff chain produced a credible landing page that improved across two review rounds. Brief Flags prevented 3 errors before any copy was written. The feedback severity system (Must Fix / Should Fix / Escalate) separated cleanly.

---

## 10 Issues Found & Fixed

### Must Fix (framework broke without these)

| # | Problem | Fix |
|---|---|---|
| 1 | No re-submission flow after Must Fix | Added 4-step re-submission process to Copywriter role |
| 2 | Escalation path had no file flow | Added Handling Escalations section to Strategist role |
| 3 | Copywriter Plan lost when brief is overwritten | Plans now logged to Campaign Log for preservation |

### Should Fix (recurring friction)

| # | Problem | Fix |
|---|---|---|
| 4 | No deliverable file naming convention | Added `deliverables/01-name.md` convention to CLAUDE.md |
| 5 | No DoD self-check in review request | Added self-check section to Review Request template |
| 6 | No Copywriter Plan template | Added Approach / Decisions / Uncertainties format |
| 7 | No guidance on publishing with [SOURCE NEEDED] tags | Added publish-with-gaps section to launch gate |
| 8 | Known Gaps just accumulate, never close | Added Status / Resolved columns |
| 9 | Re-review covers already-cleared sections | Added Locked Sections concept to Review Feedback |
| 10 | No way to dispute a Must Fix | Added escalation path for disputed items |

---

## Context7 Evaluation

**Verdict: Skip for v1.**

| Factor | Assessment |
|---|---|
| What it does | Injects live library docs into LLM context via MCP server |
| Potential benefit | Could keep brand/style knowledge current from central source |
| Why not now | Built for code docs, not marketing content. Parsing engine indexes APIs, not brand guides. |
| Token cost | Injects docs into context — conflicts with framework's "skip the read" philosophy |
| Dependency risk | Adds network latency + third-party service to every reference lookup |
| Rate limits | Free tier limited; multi-agent framework could hit bottleneck |

**Revisit when:** Context7 supports Notion/Google Docs/Confluence, or team manages 10+ brand assets that change frequently.

---

## Continuous Learning Strategy

### Built into the framework now

| Mechanism | How It Works |
|---|---|
| **Learned Patterns** | Section in Campaign Log. Accumulates what Dana catches and what works. Sofia reads before writing each brief. |
| **Audience Context** | New brief field: what the audience already believes, what competitors say, what objections they bring. |
| **Brief Expiry** | Briefs older than 14 days must be reconfirmed. Markets change fast. |
| **Checkpoint Compression** | 200-word limit prevents context bloat while preserving essential state. |
| **Gap Resolution Tracking** | Known Gaps now have Status/Resolved columns — they close, not just accumulate. |

### Recommended for later

| Mechanism | What It Does |
|---|---|
| **PLAYBOOK.md** | Cross-campaign memory. Audience patterns, review patterns, channel patterns. Survives across projects. |
| **Campaign Retrospective** | Post-publish review: what was caught, what worked first time, what the brief should have included. |

---

## File Structure (38 files)

```
marketing-team/
├── agents/                        # Role definitions
│   ├── STRATEGIST.md              #   Plans, briefs, launch gate
│   ├── COPYWRITER.md              #   Writes content
│   └── DESIGNER.md                #   Reviews for brand/quality
├── handoff/                       # Inter-agent communication
│   ├── STRATEGY-BRIEF.md          #   Strategist → Copywriter
│   ├── REVIEW-REQUEST.md          #   Copywriter → Designer
│   ├── REVIEW-FEEDBACK.md         #   Designer → Copywriter
│   ├── CAMPAIGN-LOG.md            #   Shared record + learned patterns
│   └── SESSION-CHECKPOINT.md      #   State persistence (200-word limit)
├── templates/
│   ├── project-folder/            #   Named personas (Sofia, Charlie, Dana)
│   └── generic/                   #   Blank [CUSTOMIZE] placeholders
├── examples/
│   ├── session-start.md           #   Copy-paste session prompts
│   └── campaign-walkthrough.md    #   Full sprint example
├── simulation/                    #   Stress test outputs (10 files)
├── CLAUDE.md                      #   Session router + token rules
├── METHODOLOGY.md                 #   Why this works
├── IMPROVEMENTS.md                #   Full analysis + Context7 eval
├── INSTALL.md                     #   Setup guide
├── CHANGELOG.md                   #   v1.0.0
└── setup                          #   Install script
```

---

## Next Steps

1. **Review this PR** — MJB1000/CLAUDE-CODE-V1#1
2. **Customize personas** — edit Who You Are sections in agents/ or copy from templates/project-folder/
3. **Run a real campaign** — pick a deliverable and spin up the Strategist
4. **Build the Playbook** — after 3-5 deliverables, create PLAYBOOK.md from accumulated Learned Patterns
