# Marketing Team — Simulation Results & Improvements

Based on a full end-to-end simulation: SaaS landing page for an AI analytics product
targeting mid-market CFOs.

---

## Simulation Verdict

**The framework works.** The handoff chain (Sofia → Charlie → Dana → Charlie → Dana → Sofia)
produced a credible landing page that improved across two review rounds. Dana caught real
issues (headline drift, malformed metrics, unsubstantiated claims). Charlie fixed them
without ego. Sofia's brief prevented at least three errors through Flags.

**But it has gaps.** Ten specific friction points surfaced during the simulation.

---

## What Works Well

1. **File-based handoffs prevent "I thought you said..."** — every decision is written
2. **Brief template Flags section** — caught 3 errors before any copy was written
3. **Definition of Done checklist** — gave the Designer concrete verification targets
4. **Must Fix / Should Fix / Escalate** — clean severity separation, no ambiguity
5. **Copywriter Plan step** — surfaced social proof format + brand guide gap before writing
6. **Anti-drift rules** — "one deliverable at a time" + Known Gaps prevent scope creep
7. **Role boundaries are clean** — no role bleeds into another

---

## Must Fix (framework breaks without these)

### 1. Re-submission flow after Must Fix
**Problem:** After Charlie fixes must-fix items, the framework says "re-submit" but doesn't
specify how. Does Charlie write a new REVIEW-REQUEST.md? Update the old one? Just signal "done"?

**Fix:** Add to COPYWRITER.md under "Handling Designer Feedback":
```
After fixing Must Fix items:
1. Update the deliverable file with fixes.
2. Add a "## Changes from Round N" section at the bottom of the deliverable.
3. Update REVIEW-REQUEST.md — change "Ready for Review: YES" header to "Ready for Re-Review: YES — Round [N+1]"
4. List only the changed sections in the Files Changed table.
```

### 2. Escalation file flow
**Problem:** If Dana escalates to Sofia, which files does Sofia read? Where does Sofia write
her decision? The escalation path is described in principle but not in file flow.

**Fix:** Add to STRATEGIST.md under a new "Handling Escalations" section:
```
When Designer escalates via REVIEW-FEEDBACK.md:
1. Read REVIEW-FEEDBACK.md Escalate to Strategist section.
2. Read the specific file/section cited.
3. Make the decision.
4. Write the decision back to STRATEGY-BRIEF.md under a new "## Escalation Decisions" section.
5. Signal Copywriter to proceed with the decision.
```

### 3. Copywriter Plan preservation
**Problem:** STRATEGY-BRIEF.md says "overwrite this file each deliverable." But the Copywriter
Plan is appended to it. When Deliverable 2 starts, the plan from Deliverable 1 is lost.

**Fix:** Move the Copywriter Plan to a separate section in CAMPAIGN-LOG.md under the
deliverable's history entry. The brief stays a clean brief; the plan is logged for posterity.

---

## Should Fix (recurring friction)

### 4. Deliverable artifact naming convention
Add to CLAUDE.md:
```
## Deliverable Artifacts
Store deliverable files in `deliverables/`:
  deliverables/01-landing-page.md
  deliverables/02-email-sequence.md
```

### 5. Definition of Done self-check in REVIEW-REQUEST.md
Add a section to the template:
```
## Definition of Done — Self-Check
- [x] Headline is 12 words or fewer (actual: 10)
- [x] Product name spelled "Clarifi Analytics" (4 occurrences, all correct)
- [ ] Social proof has real customer data (placeholder — logged as G1)
```

### 6. Copywriter Plan lightweight template
Add to COPYWRITER.md:
```
### Plan Format
## Approach
[What angle, what structure]

## Decisions Required
[What needs Strategist confirmation]

## Uncertainties
[What you are unsure about]
```

### 7. Publish with known gaps
Add to STRATEGIST.md under Launch Gate:
```
If the deliverable has [SOURCE NEEDED] or [PLACEHOLDER] tags:
- Present to Creative Director with a clear list of what is verified vs. unverified.
- Creative Director decides: hold for complete data, or publish with gaps removed.
- If publishing with gaps removed, log the removed content to CAMPAIGN-LOG for future insertion.
```

### 8. Known Gaps resolution tracking
Add "Status" and "Resolved" columns to CAMPAIGN-LOG Known Gaps:
```
| ID | Description | Logged | Status | Resolved |
|---|---|---|---|---|
| G1 | No customer quotes | 2026-04-02 | Open | — |
| G2 | No brand guide | 2026-04-02 | Closed | 2026-04-05 |
```

---

## Nice to Have

### 9. Ship or remove token-optimizer skill reference
Every role file says "load token-optimizer skill if available." The skill doesn't exist
in this framework. Either create a minimal skill that embeds the 5 token rules, or change
the instruction to "apply the token rules in CLAUDE.md."

### 10. Add "what the audience already believes" to brief
```
### Audience Context
- [What they already know about this product category]
- [What competitors are saying that they have heard]
- [What objections or skepticism they bring]
```

### 11. Locked sections for multi-round reviews
After Round 1, Dana cleared Headline, VP1, VP3. In Round 2 she had to re-review everything.
Add to REVIEW-FEEDBACK.md:
```
## Locked (do not re-review unless changed)
- Headline — passed Round 1
- Value Prop 1 — passed Round 1
```

### 12. Clarify agents/ vs templates/ canonical source
Add to INSTALL.md:
```
## Which files to use
- `agents/` — the generic, customizable versions. Use these as your starting point.
- `templates/project-folder/` — pre-built personas (Sofia, Charlie, Dana). Copy INTO `agents/` to use.
- `templates/generic/` — same structure as agents/ but with CLAUDE.md template included.

The session router in CLAUDE.md always points to `agents/`. Templates are starting points, not runtime files.
```

---

## Context7 Integration — Cost/Benefit Analysis

### What Context7 Does
[Context7](https://github.com/upstash/context7) is an MCP server that injects live,
version-specific library documentation into LLM prompts. It solves the problem of AI
generating code based on stale training data.

### Where It Could Help This Framework

**Potential benefit: keeping brand/style knowledge current.**
Context7's pattern (fetch live docs → inject into context) could theoretically be adapted
for marketing knowledge — brand guidelines, style guides, audience personas, competitive
intel. Instead of reading a local brand-voice.md file that may be outdated, Context7 could
fetch the current version from a central source.

**Potential benefit: channel-specific best practices.**
Marketing channels evolve fast (email deliverability rules, social platform character limits,
SEO ranking factors). Context7 could inject current best practices per channel, preventing
the framework from producing content based on stale assumptions.

### Why It's Not a Clear Win (Yet)

1. **Context7 is built for code documentation, not marketing content.**
   Its parsing engine indexes library APIs, not brand guidelines or audience research.
   The crawling engine targets GitHub repos and docs sites, not Notion, Google Docs,
   or marketing platforms where brand assets actually live. Significant adaptation needed.

2. **Token cost is real.**
   Context7 injects documentation into the context window. The framework's entire
   philosophy is token discipline — read only what you need, when you need it. Adding
   a tool that dumps documentation into context on every query contradicts Rule #1
   ("Is this in a skill or memory? Trust it. Skip the file read.").

3. **The framework already solves this problem with files.**
   Brand voice guide, style guide, and audience personas are referenced in config/team.yml
   and loaded on demand. Context7 adds a network dependency and a third-party service
   to solve a problem that local file reads already handle.

4. **Latency and reliability.**
   Context7 requires an API call to an external service. In a token-optimized workflow
   where every unnecessary operation is eliminated, adding network latency to every
   reference lookup is counterproductive. Local files are instant.

5. **The free tier has rate limits.**
   For a multi-agent framework that may spin up 3+ agents per deliverable, rate limits
   could become a bottleneck. The paid tier pricing is unclear.

### Verdict: Not Now, But Watch It

**Skip Context7 for v1.** The framework's local file-based knowledge management is simpler,
faster, and more aligned with its token discipline philosophy.

**Revisit when:**
- Context7 adds support for non-code knowledge sources (Notion, Google Docs, Confluence)
- The framework grows to manage 10+ brand assets that change frequently
- A team needs to sync brand knowledge across multiple projects in real time
- Context7 ships a marketing-specific plugin or content type

**Alternative: build a lightweight knowledge refresh step.**
Instead of Context7, add a "Brand Knowledge Refresh" step to the Strategist's session start:
```
5. If brand assets have changed since last checkpoint, re-read only the changed files.
   Trust the checkpoint for everything else.
```
This achieves the "current knowledge" goal without a third-party dependency.

---

## Continuous Learning & Context Window Management

### The Core Problem
Each agent session starts fresh. There is no memory across sessions except what is
written to handoff files. The framework's learning is limited to what humans write
into CAMPAIGN-LOG and SESSION-CHECKPOINT.

### How to Build Continuous Learning

#### 1. Campaign Retrospective File (new handoff file)
After each deliverable is published, Strategist writes `RETRO.md`:
```
# Retrospective — Deliverable [N]

## What Dana Caught
- [Pattern: issue type, how it was caught, how it was fixed]

## What Charlie Got Right First Time
- [Pattern: what worked, why]

## What the Brief Should Have Included
- [Gap that caused friction]

## Rule to Add
- [New constraint or flag for future briefs]
```

Over time, RETRO.md becomes a learning log. Strategist reads it at session start
(added to the checkpoint flow) and incorporates patterns into future briefs.

#### 2. Brief Evolution Through Known Patterns
Add a "## Learned Patterns" section to STRATEGY-BRIEF.md template:
```
### Learned Patterns (from previous deliverables)
- Always mark social proof as [PLACEHOLDER] — Dana will catch fabricated specifics
- Avoid industry-level stats without attribution — use product-specific language
- CFO audience rejects AI hype — lead with outcomes
```

This is the cheapest form of learning: Sofia reads past patterns before writing
the next brief. No external tools required.

#### 3. Context Window Management Strategy

The framework already handles this well through role-based loading. But it can improve:

**a. Tiered context loading**
```
Tier 1 (always loaded, <50 tokens): CLAUDE.md token rules
Tier 2 (loaded at session start, <500 tokens): role file + checkpoint
Tier 3 (loaded on demand, variable): brief, review files, brand assets
Tier 4 (routed to subagent, never in main context): research, competitive analysis, long-form reference
```

**b. Checkpoint compression**
SESSION-CHECKPOINT.md should have a max word count (200 words). If the campaign
grows complex, the checkpoint should summarize rather than enumerate. Add to template:
```
Keep this file under 200 words. Summarize decisions, do not list them.
If the full history is needed, read CAMPAIGN-LOG.md.
```

**c. Brief expiry**
Add a date field to STRATEGY-BRIEF.md. If the brief is older than 14 days, Strategist
must review and reconfirm before Copywriter proceeds. Markets change fast.

**d. Known Gaps as a priority queue**
Instead of a flat table, order Known Gaps by impact. When starting a new deliverable,
Strategist checks if any high-impact gaps can be addressed. This turns passive logging
into active learning.

#### 4. Cross-Campaign Memory (advanced)
For teams running multiple campaigns, create a `PLAYBOOK.md` in the project root:
```
# Marketing Playbook
*Accumulated lessons across all campaigns. Read by Strategist at project start only.*

## Audience Patterns
- Mid-market CFOs: lead with outcomes, not technology. Avoid "AI-powered" in headlines.

## Review Patterns
- Dana consistently flags unsubstantiated claims. Always use [SOURCE NEEDED] proactively.

## Channel Patterns
- Landing pages: headline under 10 words converts better than 12.
- Email: subject lines under 45 chars outperform (not 50 as commonly assumed).
```

This is the closest analog to "continuous learning" without external infrastructure.
The playbook grows with each campaign and survives across projects.

---

## Summary of All Changes Needed

| Priority | Change | Effort |
|---|---|---|
| Must | Re-submission flow after Must Fix | Small — template update |
| Must | Escalation file flow | Small — add section to STRATEGIST.md |
| Must | Copywriter Plan preservation | Small — move to CAMPAIGN-LOG |
| Should | Deliverable naming convention | Small — add to CLAUDE.md |
| Should | DoD self-check in REVIEW-REQUEST | Small — template update |
| Should | Copywriter Plan template | Small — add to COPYWRITER.md |
| Should | Publish with known gaps guidance | Small — add to STRATEGIST.md |
| Should | Known Gaps resolution tracking | Small — add columns |
| Nice | Token-optimizer skill (ship or remove) | Medium — create skill or update refs |
| Nice | Audience context field in brief | Small — template update |
| Nice | Locked sections for multi-round reviews | Medium — new concept |
| Nice | agents/ vs templates/ clarification | Small — docs update |
| Learning | Campaign retrospective file | Small — new template |
| Learning | Learned patterns in brief template | Small — template update |
| Learning | Checkpoint compression (200 word limit) | Small — template update |
| Learning | Brief expiry (14-day review) | Small — add date field |
| Learning | Cross-campaign PLAYBOOK.md | Medium — new concept |
| Eval | Context7 integration | Skip for v1, revisit later |
