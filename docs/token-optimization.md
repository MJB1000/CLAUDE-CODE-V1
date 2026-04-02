# Token Optimization for Marketing Teams

## Why This Matters

Marketing content generation can burn through tokens fast — especially when agents re-read
briefs, restate objectives, or speculatively generate content variations nobody asked for.
The five rules in CLAUDE.md eliminate the most common waste patterns.

## The Five Rules

### 1. Trust Skills and Memory
If information is in a loaded skill or already in the session context, do not re-read the source file.
This saves a file read on every reference.

### 2. Kill Speculative Calls
Do not generate "alternative headlines" or "optional variations" unless the brief explicitly asks for them.
One version, done right, reviewed, iterated. Not five drafts hoping one lands.

### 3. Parallelize Independent Operations
If you need to read the brand voice guide and the audience persona doc, read both in parallel.
Sequential reads when parallel is possible waste time and context.

### 4. Route Verbose Output to Subagents
Competitive analysis, long-form research, extensive brainstorm lists — anything over 20 lines
that the primary agent will not use directly should be routed to a subagent that returns a summary.

### 5. Never Restate
Do not begin a response with "Based on the brief, which asks us to create a landing page for..."
The Strategist knows what they wrote. The Creative Director knows what they asked for. Start with the work.

## Marketing-Specific Savings

| Pattern | Waste | Fix |
|---|---|---|
| Re-reading brand guide every deliverable | ~500 tokens/read | Load once, trust context |
| Generating 5 headline options unprompted | ~300 tokens wasted | Write the best one. Iterate if asked. |
| Summarizing the brief back to Strategist | ~200 tokens/handoff | Skip it. Start with the deliverable. |
| Reading entire content files to find one section | ~1000 tokens | Grep to the section. Read only what you need. |
| Restating feedback before fixing it | ~150 tokens/fix | Fix it. The diff shows what changed. |

## Supporting Strategies

### Checkpoint-First Loading

SESSION-CHECKPOINT.md replaces reading CAMPAIGN-LOG and the full campaign spec when it
is current. If the checkpoint is dated within 7 days, it covers decisions, open items,
and the resume prompt. Skip everything else.

### Lean CLAUDE.md

Keep your session router under ~50 lines. Every token in CLAUDE.md is paid on every
session start for every role. The cost compounds. Add project-specific references to
the table, but do not add prose or explanation.

### Role-Based Loading

Each team member loads only their job-specific files:
- Strategist loads checkpoint + campaign log + brief
- Copywriter loads brief + feedback (when iterating)
- Designer loads review request + only the files listed

Nobody loads everything. The structure prevents it.

### Targeted File Access

Grep before Read. If you need one section of a brand guide, grep for the section heading,
then read with offset and limit. Never read a 500-line style guide to find the CTA guidelines.

### RTK for CLI Sessions

For sessions that involve heavy bash output (file listings, search results, build logs),
[RTK](https://github.com/rtk-ai/rtk) compresses command output by 50-70% before it hits
context. Not required, but pairs with token-optimizer for significant additional savings.
