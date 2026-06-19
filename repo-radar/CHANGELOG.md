# Changelog

## v1.0.0 — 2026-06-20

First packaged release. A self-running GitHub trend radar that scouts new,
fast-rising repos in your interest areas and emails you a digest.

### Features
- **Daily scout** — a GitHub Action runs `radar.py` every day at 08:00 AEST
  (22:00 UTC), commits a dated digest to `digests/`, and emails it.
- **14 interest lanes** — AI agents, multimodal, marketing/analytics, web stack,
  self-development, Claude/agent craft, community/social, customer-service AI,
  Meta inbox & omnichannel, wildcard, ads & paid growth, short-form video,
  e-commerce & Shopify, and brand systems. Edit `interests.yml` to retune.
- **5 picks per lane:**
  - **🚀 Top momentum** — top `per_theme` (3) by stars/day since creation.
  - **🌱 Rising fast** — 2 *small* repos (≤ `rising_max_stars`) gaining stars over
    a ~7-day window, from the `stars.json` rolling history. A cold-start proxy
    surfaces brand-new small repos until 7 days of history accrue.
- **Branded digest** — banner image header, momentum/7-day labels, one-line
  blurbs (lean, skimmable email + markdown).
- **De-duped** — `seen.json` ensures each digest shows only repos you haven't
  been shown before.
- **Optional curation routine** — a Claude Code session (see `ROUTINE.md`) trims
  each digest to the handful that matter and drafts the email.
- **Dependency-free** — Python stdlib + PyYAML only.

### Config (`interests.yml` → `settings`)
`created_within_days`, `min_stars` (+ per-lane override), `per_theme`,
`rising_count`, `rising_max_stars`, `rising_within_days`, `header_image`,
`languages`, `exclude_owners`, `exclude_keywords`.

### State files (owned by the Action — don't hand-edit)
`seen.json` (de-dupe memory) · `stars.json` (7-day star history) · `digests/`.
