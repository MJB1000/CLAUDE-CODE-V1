# Article Blueprint

## Blog voice (different from ads)

The blog voice is the same DiggerLid person as the ads, but sitting down for a yarn instead of yelling across the site.

**Tone**

- Plain Australian English: tyre, colour, metres, arvo, ute.
- Knowledgeable, practical, a bit of humour. One cheeky line per section, at most.
- Explain like an experienced operator talking to a newer one.

**Do**

- Use real numbers from the source and the product page.
- Write in first person plural ("we tested", "on our machines").
- Use short paragraphs.
- Use the operator's own words from the transcript as quotes.

**Don't**

- No em dashes.
- No corporate words: elevate, unlock, revolutionary, game-changing, seamless, solution, ultimate, cutting-edge, innovative, "in today's fast-paced world".
- Don't pad or repeat yourself. Don't write a conclusion that only summarises.
- Don't use the phrase "we're diggin' it".
- Don't use emoji in headings. Use them sparingly in the body, or not at all.

**Claims**

- Only use claims the product catalogue or the live product page supports.
- Shipping line: "Fast shipping Australia wide".
- Don't quote prices in evergreen articles, because prices change. Link to the product page instead.
- If a price really matters to the argument, add "(at time of writing, [Month YYYY])".

## Structure (default: a 1,500 to 2,200 word guide)

Every structural element maps to a rule in `seo-rules.md`.

| # | Element | Spec |
|---|---|---|
| 0 | H1 (Title field) | 45 to 65 characters. Primary keyword near the front. Plain and descriptive. |
| 1 | Intro | **40 to 60 words.** Directly answers the primary query and includes the primary keyword. Then 1 to 2 sentences on why to trust this: we're operators, from our video, tested on our machines. |
| 2 | Key takeaways box | 3 to 4 bullets (`design-blocks.md` #1) |
| 3 | Hero figure | The best shoot still, in the body (the theme hides the featured image) |
| 4 | Video embed | If the source is a video. One line above it: "Watch: [what happens in the video]". |
| 5 | H2 sections ×4 to 6 | Each answers a secondary keyword or People Also Ask question. Each opens with a 40 to 60 word direct answer, then detail. Mix in lists and tables, and put at least one image per 300 to 400 words. |
| 6 | Comparison or spec table | When the topic has options or "old vs new". (#5) |
| 7 | Product callout | 1 to 2 placements, inside the section where the product is the answer, not stacked at the end. (#4) |
| 8 | Real-world proof | Pull quote from the transcript or a verbatim review (#6) |
| 9 | Common mistakes | Numbered list. Great for snippets and very on-brand. |
| 10 | FAQ | H2 "[Topic] FAQs", 5 to 7 H3 questions, each answered in 40 to 60 words (#8) |
| 11 | CTA band | (#9) |
| 12 | Author box | Name, role, real experience line, updated date (#10) |

## Article types (choose to match intent)

| Intent | Type | Shape |
|---|---|---|
| How do I... | How-to guide | Numbered H2 or H3 steps, tools needed, mistakes, FAQ |
| X vs Y | Comparison | Verdict up top, comparison table, "choose X if / Y if", FAQ |
| Best... | Buyer's guide | Criteria first, then options, then "what we'd choose and why" (honest) |
| What is... | Explainer | Definition first, how it works, why it matters, FAQ |
| Problem (rain, wet seat, grease mess) | Problem and solution | Cost of the problem (the maths), causes, fixes ranked, product as one fix among them |
| Story (customer or founder video) | Case study | Situation, problem, what they did, result with numbers, lessons, FAQ |

## Turning a transcript into an article

1. **Clean it.** Remove fillers and fix brand and product names: KAJO, PRO Mat, Pro Enclosure, DiggerLid.
2. **Pull out the facts.** List every claim, number, tip, step, anecdote and quotable line, each with its timecode.
3. **Map facts to the outline.** Each H2 should be fed by the transcript. Fill gaps with verified product-page facts and research, never invention.
4. **Quote the talent.** Quote 1 to 3 lines verbatim. These are the experience signal.
5. **Expand, don't transcribe.** A 60-second video gives you the spine. The article adds context, how-to detail, comparison, mistakes and FAQs, using the keyword research and People Also Ask.
6. **Record timecodes.** Keep each section's timecode so the developer can add `hasPart` clips to VideoObject later.

## Other source types

| Source | How to handle it |
|---|---|
| Ad or social post copy | Use the post's angle as the hook, then expand the topic into a guide. Link the post's product. |
| Product description | Write a buyer's guide or explainer around the problem the product solves. Never just rewrite the product page, because that causes cannibalisation. |
| Brief or idea | Run keyword research first, then pick the article type. |
| Customer review or story | Case study, with permission. |
| Competitor article | Write a better, first-hand version. Never copy their structure word for word. |
