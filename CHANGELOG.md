# Changelog

## v1.0.0 — 2026-04-02

Production-ready release — marketing adaptation of Three Man Team.
Stress-tested with two full simulations (SaaS landing page + DTC email sequence).

### Core Framework
- Three-agent team: Strategist, Copywriter, Designer
- Session router (CLAUDE.md) with token rules, session orchestration, CD decision capture
- Token-optimizer skill (`skills/token-optimizer.md`) — 5 behavioral rules
- Generic agents in `agents/` with [CUSTOMIZE] placeholders
- Named personas in `templates/project-folder/` (Sofia, Charlie, Dana)
- Blank-slate templates in `templates/generic/`

### Handoff System
- STRATEGY-BRIEF.md — audience context, brand assets, brief expiry (14-day), learned patterns, split DoD (self-checkable vs review-dependent), batch per-item criteria, escalation decisions
- REVIEW-REQUEST.md — DoD self-check (mechanical only), creative choices section
- REVIEW-FEEDBACK.md — versioned rounds (append, not overwrite), locked sections
- CAMPAIGN-LOG.md — resolution tracking, pending external clearances, learned patterns
- SESSION-CHECKPOINT.md — 200-word compression limit
- RETRO.md — post-publish retrospective with 7-day and 30-day metrics check-ins

### Agent Capabilities
- Strategist: batch deliverables, escalation handling, publish-with-gaps, post-publish retro, metrics check-ins, CD decision capture
- Copywriter: structured plan template, re-submission flow, disputed Must Fix path, brief expiry enforcement
- Designer: versioned review rounds, locked sections, append-not-overwrite feedback

### Learning System
- PLAYBOOK.md — cross-campaign memory with validated/observed pattern tags, pruning rules (30-cap, quarterly)
- Learned Patterns in CAMPAIGN-LOG — per-campaign memory
- Metrics feedback loop — 7-day and 30-day check-ins promote or invalidate patterns
- Pending External Clearances — [SOURCE NEEDED] signal-back tracking

### Documentation
- METHODOLOGY.md — framework philosophy and research basis
- INSTALL.md — agents/ vs templates/ canonical source clarification
- Examples: session start prompts, full campaign walkthrough
- Customization guide: personas, domains, brand assets, skills, file renaming
- Token optimization guide: checkpoint-first, lean CLAUDE.md, RTK reference
- Setup script

### Simulations (in repo for reference)
- `simulation/` — SaaS landing page for mid-market CFOs (identified 10 gaps, all fixed)
- `simulation-dtc/` — DTC skincare email sequence (validated all 9 improvements)

Adapted from [Three Man Team](https://github.com/russelleNVy/three-man-team) v1.0.0
