# Prompt: tune the Meta copy skill with the top 30 BAU ads

Prerequisite: Matt has deployed `tools/api-ads.js` to the diggerlid-mer Vercel project as `api/ads.js` and saved the output:

`curl -s https://diggerlid-mer.vercel.app/api/ads > top-ads.json`

(Optional parameters: `?sort=purchases&top=50&min_spend=500`.)

Then:
1. Run `python3 scripts/analyse_top_ads.py top-ads.json`. This writes `references/bau-top-30.md` in the diggerlid-meta-copy skill.
2. Read it and compare it with the skill's current defaults: length tiers, emoji density, opener emojis, archetypes, headline style.
3. Update SKILL.md, `bau-copy-patterns.md` and the hook bank wherever the data disagrees with them. Cite the numbers.
4. Report the 5 biggest changes and anything surprising (e.g. long copy outperforming short, emoji-free winners).
5. Repackage the skill.
