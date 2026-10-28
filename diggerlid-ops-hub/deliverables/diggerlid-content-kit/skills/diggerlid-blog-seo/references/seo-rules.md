# SEO Rules

These rules are distilled from the open-source **claude-seo** toolkit (claude-seo.md, github.com/AgriciDaniel/claude-seo, MIT). Where that toolkit's files disagree, the strictest overlap is used. Two other inputs are layered on top:

- DiggerLid's own SEO audit (Apr 2026)
- the live Shopify theme

The toolkit's scores are triage heuristics, not Google ranking signals. Say so if you report a score.

## 1. Keyword research (run every time)

### Step 1. Seed from the source

- Pull the 3 to 5 phrases a searcher would type that the source actually answers.
- A transcript usually holds a how-to, a comparison, a problem or a product question.
- Check `keyword-bank.md` for planner data and the content map first.

### Step 2. Expand to 30 to 50 variants

Combine:

- **Modifiers:** best, how to, vs, for beginners, guide, checklist, mistakes, cost, worth it
- **Question words:** what, why, how, when, can, does
- **Commercial modifiers:** price, review, alternative, comparison
- **Australia:** australia, aus

Sources, in order of preference:

1. WebSearch the seeds and read the results, related searches and People Also Ask.
2. Fetch Google autocomplete:

   ```
   https://suggestqueries.google.com/complete/search?client=firefox&gl=au&hl=en-AU&q=<seed>
   ```

   If it's blocked, skip it.
3. AnswerThePublic-style question variants.

### Step 3. Classify intent

| Intent | Signal words |
|---|---|
| Informational | how, what, why, guide |
| Commercial | best, vs, review |
| Transactional | buy, price |
| Navigational | brand names. Exclude these. |

A blog targets **informational or commercial** intent.

### Step 4. SERP check the shortlist (top 10, Australia)

WebSearch has no region setting and returns mostly US results. Add "australia" to the queries, use autocomplete with `gl=au` for the AU signal, and label the competitor check "approximate".

**Page-type consensus.** If over 60% of results are product or category pages, the keyword is transactional. A blog is a **critical mismatch** there. Pick a different primary keyword, or note that the PDP should own it.

**Competitor filter.**

- Ignore marketplaces and aggregators: amazon.com.au, ebay.com.au, gumtree, kogan, whirlpool, productreview, finder, YouTube, Reddit, Wikipedia, .gov.au, .edu.au.
- Score the top 5 real competitors on Depth, Formatting, SEO and UX, each 1 to 10.
- Note their H2s and approximate word counts.

**Find the gaps.**

| Gap type | Meaning |
|---|---|
| Topic | subtopics they miss |
| Depth | subtopics they cover thinly |
| Quality | no first-hand experience, outdated, poorly formatted |

DiggerLid's edge is almost always first-hand operator experience, plus real numbers from its own products.

### Step 5. Pick the keyword set

| Set | Size | What goes in it |
|---|---|---|
| **Primary** | 1 keyword | Informational or commercial. Realistic to rank for. Not already targeted by another DiggerLid page (cannibalisation check: grep the blog and product titles). |
| **Secondary** | 5 to 8 terms | Close variants and sub-questions. Each one gets an H2, an H3 or a passage. |
| **Semantic** | 10 to 15 terms | Entities and related vocabulary used naturally. Examples: machine brands (Kubota, Yanmar, Kobelco), ROPS, canopy, NLGI, EP2, ripstop, condensation, BoM rain days. |
| **Questions** | 5 to 7 | From People Also Ask, reviews or the source. These become the FAQ. |

**Keyword cluster rules** (SERP overlap, when choosing between near-duplicate keywords):

| Shared top-10 URLs | Action |
|---|---|
| 7 to 10 | Same article. The higher-volume keyword becomes primary. |
| 4 to 6 | Same cluster. Interlink. |
| 0 to 3 | Separate articles |

## 2. On-page rules

| Element | Rule |
|---|---|
| SEO title tag | **50 to 60 characters.** Primary keyword first, ending ` \| DiggerLid`. Unique. |
| Meta description | **130 to 150 characters.** Primary keyword included. Active voice. Ends on a reason to click or a CTA. No quotation marks, no hashtags, no brand name. Sharing the keyword with the title is fine, but don't copy the title wording. |
| H1 (article Title field) | Exactly one, set by the theme. 45 to 65 characters, with the keyword near the front. It may differ from the SEO title. |
| URL handle | 3 to 6 words, lowercase and hyphenated, primary keyword, no dates. Drop filler stop words (a, the, of, for, and), but keep a question word (how, what, why) when it is part of the keyword, e.g. `how-to-load-grease-gun`. Never change it after publishing. |
| Headings | H2 then H3, never skipping a level. Primary keyword in the H1 plus 1 to 2 H2s. Phrase H2s as questions where natural. |
| Keyword placement (required) | title tag, H1, slug, meta description, first 100 words, at least one image alt |
| Density | Natural, roughly 1 to 3%. Never optimise to a number. Spread evenly. Use synonyms freely. |
| Word count | **1,500 words minimum** for a blog post, as a coverage floor, not a target. 1,500 to 2,200 is typical. A pillar guide runs 2,500 to 4,000. |
| Readability | Sentences average 15 to 20 words. Paragraphs are 2 to 4 sentences. Flesch reading ease is 60 to 70. Use lists and tables generously. |
| Answer first | The intro is a 40 to 60 word paragraph that directly answers the primary query. |
| Section openers | Each H2 section answers its heading in its first 40 to 60 words, then expands. Self-contained passages run 130 to 170 words. |
| Internal links | **5 to 10** for 1,500+ words: product pages, the size guide, collections, other articles. Use descriptive, varied anchors. No single anchor text above 40%. |
| External links | 1 to 3 authoritative sources where a claim needs one, e.g. BoM rain data or manufacturer specs. Open in a new tab. |
| Images | 1 image per 300 to 400 words. Alt text 10 to 125 characters. File names descriptive. Width and height set. Hero loads eager with `fetchpriority="high"`. Others lazy. |
| Freshness | Show the publish date. Add "Updated [date]" when revised. Review evergreen posts every year. |

## 3. E-E-A-T

E-E-A-T stands for experience, expertise, authoritativeness and trust. Scoring weights (toolkit model): Experience 20, Expertise 25, Authority 25, Trust 30.

- **Who.** A named author with a real role, shown in a byline box. Default: the DiggerLid founders, who are landscaping tradies (founded 2018).
- **How.** Say where the content comes from, e.g. "From our video with...", "We tested this on our own machines".
- **Experience.**
  - Original shoot photos and the embedded source video.
  - Specific anecdotes from the transcript.
  - Real numbers.
  - Stock imagery doesn't count.
- **Expertise.** Accurate specs (verified on the PDP) and correct terminology.
- **Trust.**
  - Dated claims.
  - Cited sources.
  - Links to the warranty and returns pages.
  - Customer reviews quoted verbatim.
  - Corrections noted.
- **Information gain is non-negotiable.** Name the new value this article adds that the competitors lack. Examples:
  - first-hand operator testing
  - the rain maths
  - a model-fit list
  - a grease compatibility table

  "More detail" doesn't count.

## 4. AI search and GEO

- Put a "What is X?" or direct-answer sentence in the first 60 words. AI citations skew towards the first 30% of a page.
- Use definitions in the form "X is...". Give specific numbers with sources. Use question-led H2s. Put comparisons in tables and steps in lists.
- Embed the source video. Multi-modal pages earn more citations.
- Include a visible FAQ of 5 to 7 questions, each answered in 40 to 60 words. Don't use FAQPage schema: its rich results were retired for all sites on 7 May 2026.
- Never use HowTo schema. It's deprecated.
- No llms.txt work is needed per article.

## 5. Schema

- The theme already outputs `Article` JSON-LD. Fill the Excerpt and Featured image so it's complete.
- Don't paste JSON-LD into the body. The extra schema types belong in the theme upgrade:
  - BlogPosting with an https context and `author.url`
  - BreadcrumbList
  - VideoObject: name, description, thumbnailUrl, uploadDate, duration (ISO 8601), embedUrl, contentUrl, creator
- Don't put Product schema in articles. Link to the product pages, which carry their own Product schema.

## 6. Site-specific findings to respect (DiggerLid SEO audit, Apr 2026)

- Multiple H1s were a critical issue. Articles must contain **zero** H1s in the body.
- Generic anchors like "Shop Now" were flagged. Every link must describe its target.
- Image alt text and file names were weak. Every image in an article must be named and described properly.
- Content depth was thin, with no guides or FAQs. Each article should end with an FAQ and link to at least 2 products and 1 other guide (once more guides exist).
- Punny headlines like "Don't Go Topless" hurt clarity. Use a plain, descriptive H1 with the keyword. Keep the brand wit in the body.
