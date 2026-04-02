# Simulation Report -- Full Campaign Sprint Stress Test
*Date: 2026-04-02*
*Scenario: SaaS landing page for AI-powered analytics feature targeting mid-market CFOs*

---

## Test Results Summary

| Test | Result | Notes |
|---|---|---|
| 1. Session start sequence | PASS with friction | See details below |
| 2. Brief template completeness | PASS | Captured everything Charlie needed |
| 3. Copywriter Plan approval flow | PASS with friction | See details below |
| 4. Review request format | PASS | Dana had enough to review |
| 5. Feedback loop (must-fix, should-fix, escalate) | PASS | Clean separation of severity levels |
| 6. Launch gate | PARTIAL PASS | Mechanics work, but external dependencies create ambiguity |
| 7. Friction points and gaps | Multiple found | See detailed analysis below |

---

## 1. Session Start Sequence

### What worked
- The three-step sequence (checkpoint -> role file -> reference files) is clear and unambiguous.
- The "do not ask the Creative Director to summarize" rule in STRATEGIST.md prevents a common antipattern.
- The routing logic in CLAUDE.md correctly directs each role to only the files they need.

### What broke or felt awkward
- **Token-optimizer skill does not exist.** Every role's Step 1 says "load token-optimizer skill if available." In a real session, this is a no-op that wastes a beat of attention. The framework should either ship with this skill or remove the reference. Currently it creates a "was I supposed to find something?" moment for every session start.
- **SESSION-CHECKPOINT.md vs. fresh start ambiguity.** The checkpoint template is in `handoff/` but the session start instructions say "check SESSION-CHECKPOINT.md" without specifying a path. In a project using the `templates/project-folder/` structure, the checkpoint could be in multiple locations. The router should specify: "check `handoff/SESSION-CHECKPOINT.md`" or "check the project root."
- **Strategist session start reads CAMPAIGN-LOG + STRATEGY-BRIEF on fresh start, but the brief may not exist yet.** If the Creative Director is starting a brand-new campaign, the Strategist reads an empty template. Not harmful, but the instructions could add: "If STRATEGY-BRIEF.md is a blank template, skip it."
- **Copywriter and Designer are spun up by Strategist, not self-starting.** This is good design -- prevents role confusion. But the spin-up prompt format in `examples/session-start.md` differs slightly from the spin-up prompt format in `agents/STRATEGIST.md`. The example says "Read CLAUDE.md, then STRATEGIST.md" but the agent file says "Load token-optimizer skill first. Then read COPYWRITER.md, then STRATEGY-BRIEF.md." Minor inconsistency -- the example includes CLAUDE.md as a first read, but the agent spin-up prompt does not.

---

## 2. Brief Template Completeness

### What worked
- The template in `handoff/STRATEGY-BRIEF.md` covers all critical fields: audience, objective, key message, tone, channel, constraints, deliverables, flags, definition of done.
- The Flags section was essential. Three of the four flags in this simulation directly prevented errors Charlie would have made (fabricated quotes, wrong product name spelling, AI-hype headline).
- Definition of Done as a checklist gave Dana a concrete verification list. This is the strongest part of the template.

### What is missing
- **No field for "what the audience already knows."** The brief describes who the audience is but not what they already believe about the product category or this specific vendor. For a mid-funnel audience, this matters. Charlie had to infer from "skeptical of AI hype" that the audience has seen similar pitches before.
- **No field for competitive context.** The brief says "no competitor names" but does not describe what competitors are saying. Charlie cannot differentiate effectively without knowing what the audience has already heard. This should be a brief field even if the constraint is "do not name competitors in copy."
- **No field for existing brand assets.** The brief flags "no approved customer quotes" but there is no standard field for "what approved assets exist" (logos, data, case studies, approved claims). Charlie had to discover through flags what was not available rather than seeing what was.
- **Copywriter Plan section placement is awkward.** The plan is appended to the bottom of STRATEGY-BRIEF.md, which means the brief is both a reference document and a conversation document. After Sofia approves, the brief now contains Charlie's working notes. Dana reads the brief at review time -- does she read the Copywriter Plan section? The framework does not say. In this simulation I created a separate `02-COPYWRITER-PLAN.md` to keep things clean, but the framework says to add it to STRATEGY-BRIEF.md.

---

## 3. Copywriter Plan Approval Flow

### What worked
- The requirement to write a plan before writing copy caught two important decisions early: (a) the social proof format choice and (b) the "no brand guide" uncertainty.
- Sofia's approval gave Charlie a clean mandate. No ambiguity about whether to proceed.
- The plan format (angle, structure, uncertainties) is lightweight enough that it does not feel like busywork.

### What broke or felt awkward
- **No explicit format for the plan.** COPYWRITER.md says "write your approach -- what angle you are taking, what decisions it requires, what you are uncertain about." But it does not give a template. Charlie's plan format was self-invented. In a multi-session campaign, plans from different sessions could look completely different. A lightweight template (even just three required headers: Approach, Decisions, Uncertainties) would help.
- **"Wait for Sofia to confirm or redirect. No copy until confirmed."** In a single-agent simulation, this handoff is instant. In a real multi-agent setup, this is a hard blocking wait. The framework does not address what happens if Sofia is unavailable or if the Strategist session ends between plan submission and approval. The checkpoint would need to capture "plan submitted, awaiting approval."
- **"For small changes -- skip the plan, write directly."** The boundary between "small" and "non-trivial" is undefined. A full landing page is clearly non-trivial. But what about a single headline revision? A CTA change? An A/B variant? This will cause inconsistency across sessions.

---

## 4. Review Request Format

### What worked
- The file-and-section table gave Dana precise targets. She did not have to read the whole landing page wondering what to focus on.
- Open Questions section was critical. Charlie's flag about the Value Prop 2 stat directly prompted Dana's most important Must Fix finding.
- Known Gaps Logged section kept scope clean -- Charlie logged the quote and brand guide gaps without trying to solve them.

### What is missing
- **No field for "Definition of Done checklist status."** The brief has a Definition of Done with checkboxes. The review request should include Charlie's self-assessment against that checklist. Currently, Dana has to mentally cross-reference the brief's DoD against the copy. Adding a "DoD self-check" section would reduce reviewer cognitive load and catch self-evident misses before review.
- **No field for "what changed since the brief."** If Charlie made any decisions not explicitly covered by the brief (e.g., choosing "Start satisfying the board" as a headline angle), those should be called out explicitly. The Open Questions section partially covers this, but it is framed as questions rather than declarations of creative choices.

---

## 5. Feedback Loop (Must-Fix, Should-Fix, Escalate)

### What worked
- The three-tier severity system is clear and unambiguous. Dana used all three categories (Must Fix, Should Fix, Escalate to Strategist) in the first round with no confusion about which items belonged where.
- "Must Fix blocks the deliverable" is a hard rule that prevents premature approval.
- "Describe the fix. Copywriter writes it." -- this rule prevented Dana from rewriting Charlie's copy. She described what was wrong and how to fix it, and Charlie executed. This preserved role boundaries cleanly.
- Charlie addressed all four items (2 must-fix, 2 should-fix) in one revision. The should-fix items were quick inline fixes per the framework rules.

### What broke or felt awkward
- **Round 2 review request is not specified.** After Charlie fixes Must Fix items, the framework says "Re-submit when done." But re-submit how? Does Charlie write a new REVIEW-REQUEST.md? Does Charlie just update the landing page file and tell Dana to re-review? In this simulation, I had Dana review the updated file directly. The framework should specify: after fixes, does Charlie write a new review request or just signal "fixes complete, re-review file X"?
- **The Escalate to Strategist path was not exercised in Round 1.** I deliberately avoided triggering an escalation because the framework is vague on the mechanics. If Dana escalates, does Sofia read REVIEW-FEEDBACK.md? Does she read the original brief and the copy? Does she make a decision and write it back to REVIEW-FEEDBACK.md, or to STRATEGY-BRIEF.md, or to a new file? The escalation path is described in principle but not in file flow.
- **"Cleared" section wording.** Dana's template says "One sentence: what was reviewed and passed." In practice, Dana needed to list multiple sections that passed. The "one sentence" constraint is too tight for a multi-section deliverable. It should say "Brief summary of what passed."
- **No "partially cleared" state.** In Round 1, Dana cleared the headline, VP1, VP3, subhead, and CTAs, but not VP2 and the social proof stat. The framework has no way to signal "these sections are locked, only review the changed sections in Round 2." Dana had to re-review the entire deliverable. A "locked sections" concept would save review time.

---

## 6. Launch Gate

### What worked
- The seven-step launch gate in STRATEGIST.md is thorough: tell CD what was created, get go-ahead, commit, push, confirm, update log, update checkpoint.
- "Nothing goes live without steps 1 and 2" is a hard guardrail that prevents accidental publish.
- The separation between "Dana clears" and "Sofia presents to CD" is correct -- the strategist contextualizes the work before the CD sees it.

### What broke or felt awkward
- **External dependencies are not modeled.** The launch gate assumes: Dana clears -> Sofia tells CD -> CD says go -> publish. But this deliverable has three external blockers: (1) data team stat verification, (2) customer quote sourcing, (3) CD sign-off. The framework has no mechanism for tracking external blockers or for partial publish (e.g., "publish with qualitative-only social proof while stats are verified"). Sofia had to improvise by putting this in Open Questions for Creative Director.
- **Step 3 says "commit to version control."** In a marketing context, this is appropriate for teams using git-based workflows. But many marketing teams publish through CMS platforms without version control. The framework should generalize: "Save the final version to your team's record of truth" or similar.
- **Step 5 says "confirm the publish landed."** How? For a landing page, this means checking the live URL. For email, it means confirming send. For social, it means confirming the post went live. The step is correct but so generic it provides no guardrails. Teams would benefit from a channel-specific publish checklist template.
- **The launch gate does not address "publish with known gaps."** This deliverable has [SOURCE NEEDED] tags and [PLACEHOLDER] tags. Can it publish in this state? The framework does not say. In practice, Sofia would need to decide whether to hold for complete data or publish a qualitative version. This is a common real-world scenario that the framework should address.

---

## 7. Comprehensive Friction Points and Missing Elements

### Structural Issues

1. **File overwrite vs. append problem.** STRATEGY-BRIEF.md says "overwrite this file each deliverable -- it is not a log." But the Copywriter Plan section gets appended to it. If Deliverable 2 starts, the brief is overwritten and the Copywriter Plan from Deliverable 1 is lost. The plan should either live in CAMPAIGN-LOG or in a separate file. The current design loses planning history.

2. **No file naming convention for deliverable artifacts.** The framework specifies handoff files (STRATEGY-BRIEF.md, REVIEW-REQUEST.md, etc.) but not deliverable files. Where does the landing page copy live? Charlie had to create a file with a self-chosen name. For multi-deliverable campaigns, this will get messy fast. A convention like `deliverables/01-landing-page.md` would help.

3. **Handoff files are singular, not versioned.** REVIEW-FEEDBACK.md gets overwritten each round. Round 1 feedback is lost when Round 2 feedback is written. For audit trails or post-campaign learning, the team loses the history of what was caught and fixed. Consider `REVIEW-FEEDBACK-R1.md`, `REVIEW-FEEDBACK-R2.md` or a single file with dated sections.

4. **No mechanism for the Copywriter to re-submit after fixes.** The framework says "Re-submit when done" but does not specify what re-submission looks like. Does Charlie update REVIEW-REQUEST.md? Write a new one? Just tell Dana "done"? This gap forced an improvisation in this simulation.

### Process Issues

5. **The "one deliverable at a time" rule is correct but creates a bottleneck.** For a campaign with 10 deliverables, each must go through the full brief -> plan -> write -> review -> fix -> re-review -> launch gate cycle sequentially. This is safe but slow. The framework could benefit from a "batch deliverable" pattern for closely related items (e.g., landing page + 3 paid ads that share messaging).

6. **No role for the Creative Director in the file system.** The CD is referenced throughout but never reads or writes handoff files. Sofia reports to them verbally (in the conversation), and the CD responds verbally. This means the CD's decisions are not captured in files unless Sofia transcribes them to CAMPAIGN-LOG. If Sofia's session ends before logging, the decision is lost.

7. **No conflict resolution between Dana and Charlie.** If Charlie disagrees with a Must Fix, the framework says Must Fix must be fixed. There is no appeal path. In practice, a talented copywriter may have a valid reason for a choice Dana flagged. The framework should allow Charlie to escalate a disputed Must Fix to Sofia, who arbitrates.

8. **Session boundaries are unclear for multi-agent work.** Does Sofia's session stay open while Charlie writes? Does Charlie's session stay open while Dana reviews? The framework implies separate sessions (spin up Charlie, spin up Dana) but does not address whether they can be concurrent or must be sequential. For a single-operator playing all roles, this is moot. For actual multi-agent deployment, it matters.

### Template Issues

9. **The `templates/project-folder/` versions of role files are nearly identical to `agents/` versions but with customizable persona sections.** It is unclear when to use which. If a team copies templates into their project folder, do the `agents/` versions still get read? The router in CLAUDE.md points to `agents/` but the templates exist in `templates/project-folder/`. This creates confusion about the canonical source.

10. **CAMPAIGN-LOG Known Gaps has no workflow for resolution.** Gaps are logged but there is no process for reviewing them, assigning them, or closing them. They accumulate. The template should include a "Resolved" column or a separate "Resolved Gaps" section.

---

## What the Framework Gets Right

1. **File-based handoffs are the core innovation.** Forcing all communication through structured files prevents the "I thought you said..." problem. Every decision is written down.
2. **Role boundaries are clean.** Sofia strategizes, Charlie writes, Dana reviews. No role bleeds into another.
3. **The brief template is strong.** Flags, constraints, and Definition of Done caught multiple issues before they became copy problems.
4. **The feedback severity system works.** Must Fix / Should Fix / Escalate is simple and effective.
5. **Anti-drift rules are practical.** "One deliverable at a time" and "out-of-scope items go to Known Gaps" prevent scope creep.
6. **The Copywriter Plan step catches strategic misalignment early.** In this simulation, it surfaced the social proof format decision and the brand guide gap before any copy was written.

---

## Priority Recommendations

### Must address (framework does not work correctly without these)
1. Define the re-submission flow after Must Fix items are resolved.
2. Define the file flow for Escalate to Strategist (which files does Sofia read/write?).
3. Clarify whether STRATEGY-BRIEF.md Copywriter Plan section persists or is lost on overwrite.

### Should address (framework works but with recurring friction)
4. Add a deliverable artifact naming convention.
5. Add a "Definition of Done self-check" section to REVIEW-REQUEST.md template.
6. Add a Copywriter Plan lightweight template (Approach, Decisions, Uncertainties).
7. Address "publish with known gaps" in the launch gate.
8. Add a "Resolved" column to Known Gaps in CAMPAIGN-LOG.

### Nice to have (polish)
9. Ship or remove the token-optimizer skill reference.
10. Add a "what the audience already believes" field to the brief template.
11. Add a "locked sections" concept for multi-round reviews.
12. Clarify `agents/` vs. `templates/project-folder/` canonical source.

---
