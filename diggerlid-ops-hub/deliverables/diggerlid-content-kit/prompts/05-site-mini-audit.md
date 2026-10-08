# Prompt: pre-write mini audit / monthly SEO check

Run `python3 scripts/site_inventory.py ./site` (from the diggerlid-blog-seo skill) to crawl diggerlid.com via the sitemap. Then report:

1. **Canonicals:** any canonical that doesn't match its own URL. Fetch each one and report its status code. Watch for `/a/shop/` and the DeepLumen `dl-bc-v2` block.
2. **H1s:** pages with 0 or more than 1 H1.
3. **Titles:** titles outside 30 to 60 characters, and duplicate titles.
4. **Metas:** missing meta descriptions, or ones outside 120 to 160 characters.
5. **Junk pages:** test, old or placeholder pages present in the sitemap.
6. **Weak linking:** pages with fewer than 3 inbound links.
7. **Alt text:** missing alt text, totals by page type.
8. **llms.txt:** does `/llms.txt` describe the business correctly?
9. **Blog:** article count, author shown, placeholder sections.
10. **Change since last time:** compare with `context/site-crawl/inventory.md` from the kit.

Give a prioritised table (Critical / High / Medium / Low) with owner and fix. Use real numbers only.
