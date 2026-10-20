# Prompt: blog article from a video or post (launches alongside it)

Use the diggerlid-blog-seo skill. Follow its full workflow:

1. Pre-write mini audit (run `scripts/site_inventory.py` if the inventory is older than 7 days).
2. Mine the source.
3. Verify facts on the live site.
4. Keyword research and scoring.
5. Brief.
6. Images.
7. Write and design.
8. TOV self-score (24/30 minimum).
9. Shopify fields.
10. `seo_check.py` (0 FAIL).
11. Preview.

Inputs:
- Source: [paste transcript / post copy, or attach]
- Video URL for the embed: [YouTube / IG / TikTok URL, or "none yet"]
- Go-live date and time (match the post): [e.g. 2026-10-22 12:00 AEDT]
- Author: [e.g. "Luke, DiggerLid co-founder"]
- Images: [Frame.io folder link / attached stills / "send me a shot list"]
- Keyword wish (optional): [keyword, or "you choose"]
- Mode: [show me the brief first / just do it]

Deliver `article.html`, `seo-fields.json`, `preview.html` and `launch-checklist.md`. Also list the inbound link edits (the existing pages to update, with the exact sentence and anchor), plus open items: images, [CHECK] claims, theme fixes.
