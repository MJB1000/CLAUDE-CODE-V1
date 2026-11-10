# Prompt: choose the keyword focus for a piece of content

Use the diggerlid-blog-seo skill's keyword method (`references/seo-rules.md` section 1, plus `references/keyword-bank.md`).

Topic or source: [paste or describe]

1. Seed 3 to 5 phrases the source actually answers. Expand to 30 to 50 variants using autocomplete (gl=au), People Also Ask and modifiers.
2. Classify the intent of each variant. SERP-check the top 8 candidates and note the share of results that are articles.
3. Score each candidate out of 100:

   | Factor | Points |
   |---|---|
   | source fit (under 15 disqualifies) | 25 |
   | intent fit (under 40% articles in the SERP is a mismatch) | 20 |
   | business value | 20 |
   | demand (planner volume where sourced, otherwise "unverified") | 15 |
   | winnability | 15 |
   | cluster gap | 5 |

4. Check for cannibalisation against existing DiggerLid titles and H2s (`site-crawl/inventory.md`).
5. Return a table of candidates with scores, the chosen primary keyword, 5 to 8 secondary terms, 10 to 15 semantic terms and 5 to 7 FAQ questions. Explain in 3 lines why the winner won.

Never invent search volumes.
