# DiggerLid Content Kit

Two Claude skills, a prompt library, and the full research context for DiggerLid's Meta ad copy and blog SEO work. Built on 7 and 8 October 2026.

## What's inside

```
diggerlid-content-kit/
├── README.md                     you are here
├── skills/
│   ├── diggerlid-meta-copy.skill   upload to claude.ai (Settings > Capabilities > Skills)
│   ├── diggerlid-blog-seo.skill    upload to claude.ai
│   ├── diggerlid-meta-copy/        the same skill as editable files (for Claude Code: ~/.claude/skills/)
│   └── diggerlid-blog-seo/
├── prompts/                      ready-to-paste prompts, numbered by use
├── context/
│   ├── CONTEXT.md                everything learned: business, rules, facts, ad learnings, audit, decisions
│   ├── seo-blog-readiness-audit.html   the full audit (open in a browser)
│   ├── site-crawl/               inventory.md/.json (88 pages audited) + corpus.md (all site copy)
│   ├── data/keyword-planner-grease.md  146 Keyword Planner keywords (AU, grease/KAJO)
│   └── examples/how-to-load-grease-gun/  test article: html, fields, preview, checklist
└── tools/                        standalone scripts (Python 3, standard library only)
    ├── api-ads.js                Vercel function: top BAU ads + copy from Meta (deploy to diggerlid-mer)
    ├── analyse_top_ads.py        turns api/ads output into length/emoji/style stats
    ├── site_inventory.py         crawls diggerlid.com for the pre-write mini audit and TOV corpus
    ├── seo_check.py              25+ SEO checks on an article before publishing
    └── build_preview.py          branded article preview with Google snippet
```

## Install the skills

**claude.ai or the Claude apps.** Go to Settings > Capabilities > Skills > Upload, and add each `.skill` file.

**Claude Code.** Copy the two folders into `~/.claude/skills/`, or into the project's `.claude/skills/`.

**Claude Project.**
1. Paste `prompts/00-project-instructions.md` into the project instructions.
2. Add `context/CONTEXT.md` as project knowledge.

## Which prompt for which job

| Job | Prompt |
|---|---|
| Set up a project or session | 00, 12 |
| Meta ad copy from a video or brief | 01 |
| Refresh a tired ad | 02 |
| Blog article launching with a post | 03 |
| Pick a keyword | 04 |
| Monthly SEO health check | 05 |
| Check or rewrite copy for brand voice | 06 |
| Refresh the voice guide every quarter | 07 |
| Tune ad copy with real top-30 ad data | 08 |
| Developer: fix canonicals and llms.txt (critical) | 09 |
| Fix conflicting facts across the site | 10 |
| Move the 3 article pages into the blog | 11 |

## Before the first blog article goes live

These come from the audit. Details are in `prompts/09` and `context/CONTEXT.md` section 7.

1. **Canonicals.** Fix the canonical tags. Right now all 49 product and collection pages point Google at a 404.
2. **llms.txt.** Fix it or remove it. It currently describes the wrong business.
3. **Theme.** Turn on Show author, and hide the placeholder "You may also like" section on the blog.
4. **Open decisions:**
   - Is DeepLumen meant to be live?
   - Do you want to rename the blog?
   - Can I move the 3 article pages into the blog?
   - Can you give me Search Console access?
   - Should I build blog skill upgrades 1 to 6?

## Rules baked into everything

- No em dashes.
- Never use "we're diggin' it".
- Shipping copy is "Fast shipping Australia wide".
- Use exact product names.
- Never invent numbers.
- The live site wins over any reference file.
- No API keys or secrets anywhere in this kit. META_TOKEN stays in Vercel env.

## Credits

The SEO rules and method are distilled from the open-source claude-seo toolkit (MIT, github.com/AgriciDaniel/claude-seo). FLOW concepts are © Daniel Agrici, CC BY 4.0. The product facts are a snapshot from 7 October 2026, so verify them against the live site.
