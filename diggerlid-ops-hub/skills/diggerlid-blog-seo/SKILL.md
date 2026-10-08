---
name: diggerlid-blog-seo
description: Turn any DiggerLid source (a video transcript, social post, ad, product description, review or brief) into an extremely SEO-friendly, on-brand Shopify blog article ready to go live alongside the post. Runs live keyword research and SERP checks, verifies every fact against diggerlid.com, sources images from Frame.io or asks for them, designs the page with paste-ready branded HTML blocks, and outputs the Shopify fields (title, meta, handle, excerpt, tags, alt text), a launch checklist and an automated SEO check. Use whenever the user asks for a blog, article, blog post, SEO content, guide or "turn this into a blog" for DiggerLid or its products (Pro Enclosure, PRO Mat, KAJO grease, DiggerShield, covers, Draw Bar Cover, Hauler, Digger Wipes).
---

# DiggerLid Blog SEO

Turn one piece of content into one blog article that ranks, gets cited by AI answers, sells the product without being a hard sell, and launches on the same day as the post.

The blog is `https://diggerlid.com/blogs/news`, and it had **0 articles** as of Oct 2026. Every article sets the standard for the ones after it.

## Workflow

### 1. Intake

Gather six things. Ask only for what is missing, in **one** message.

1. **Source.** A transcript, post copy, product, review or brief. If it's a video, ask for the video URL (YouTube, Instagram or TikTok) for the embed. If there's no URL yet, leave a marked `<!-- VIDEO EMBED NEEDED -->` comment and an empty `video_url`, and carry on.
2. **Go-live date and time** of the matching post or ad. The article is scheduled to match.
3. **Product or products** the content is about. Infer them if you can.
4. **Images.** A Frame.io folder link, exported stills or attachments (see `references/image-sourcing.md`).
5. **Author.** Default to "Joel, DiggerLid co-founder" or "Luke, DiggerLid co-founder" when they're on camera. Otherwise ask.
6. **Any keyword the user already wants.**

### 2. Mine the source

Follow the transcript steps in `references/article-blueprint.md`. Extract:

- every fact, number, tip and step
- the quotable lines
- the timecodes
- the core question the content answers

### 3. Verify facts on the live site (mandatory)

- Grep `references/product-catalogue.md` and `references/usp-bank.md` for the product.
- **WebFetch every product page you will mention or link** (`https://diggerlid.com/products/<handle>`) and confirm the specs, names, variants and warranty.
- The site wins over the catalogue. Flag any mismatch.
- If the source makes a claim the site doesn't support (e.g. a spec said on camera), either soften it to what's verified or mark it `[CHECK]` and list it for the user.
- Facts the catalogue marks as **owner-supplied** count as verified. Examples: the 1966 spring-plunger patent, and the founders being landscaping tradies. Attribute them in the text, e.g. "the spring-plunger design dates back to 1966".
- Use "Fast shipping Australia wide". Never use free-shipping claims or thresholds.
- Before linking any internal URL, confirm it returns a page.

### 4. Keyword research

Follow `references/seo-rules.md` §1 exactly.

1. Seed the keywords and check `references/keyword-bank.md` (real planner data covers grease and KAJO).
2. Expand to 30 to 50 variants with WebSearch, People Also Ask and autocomplete.
3. Classify intent.
4. SERP-check the shortlist in Australia: page-type consensus and the top 5 competitors.
5. Pick the keyword set:
   - 1 primary keyword
   - 5 to 8 secondary terms
   - 10 to 15 semantic terms
   - 5 to 7 FAQ questions
6. Check for cannibalisation against existing DiggerLid product titles and articles.
7. Write down the **information gain**: what this article has that the top 5 don't.

### 5. Brief (show the user, then continue)

Post a compact brief:

- primary and secondary keywords, with volumes where sourced and "unverified" otherwise
- intent and article type
- H1
- slug
- H2 outline
- information gain
- image shot list

If the user is around, give them a moment to redirect. If the request says "just do it", carry straight on.

### 6. Images

Run `references/image-sourcing.md`:

1. Frame.io (connector, or ask for the link or stills)
2. Attachments
3. Google Drive
4. Shopify product images

Send the shot list for anything missing. Build with `<!-- IMAGE NEEDED -->` placeholders so nothing waits on images.

### 7. Write and design the article

- Follow `references/article-blueprint.md` for structure and voice.
- Use `references/design-blocks.md` for the HTML.
- Use 4 to 7 **styled boxes**: takeaways, product callout, table, pull quote, CTA band. Figures, the video embed, the FAQ and the author box don't count towards that.
- One H1 only (the Title field). Start the body at `<h2>`.
- **Hero while stills are pending.** Use the best real product image from Shopify as a temporary eager hero, and keep an `IMAGE NEEDED` comment beside it for the shoot still.

### 8. Package for Shopify

Fill every field in `references/shopify-and-theme.md`:

- Title (H1)
- SEO title
- meta description
- handle
- excerpt
- tags
- author
- featured image and alt text
- scheduled publish date and time

### 9. Check, then fix, then deliver

1. Save the body as `article.html` and the fields as `seo-fields.json`. See the output contract below for the keys.
2. Run `python3 scripts/seo_check.py article.html seo-fields.json`.
3. Fix every FAIL. Fix each WARN, or explain it.
4. Run `python3 scripts/build_preview.py article.html seo-fields.json preview.html` to make a branded preview page the user can open.

## Output contract

Deliver these files. Use the user's chosen folder, otherwise a `blog/<handle>/` folder in the working directory.

| File | Contents |
|---|---|
| `article.html` | Paste-ready body HTML for Shopify's "Show HTML" mode |
| `seo-fields.json` | See the keys below |
| `preview.html` | Branded preview of the full article page, including the Google snippet preview |
| `launch-checklist.md` | The checklist below, with items ticked or flagged |

`seo-fields.json` keys:

```json
{
  "title": "",
  "seo_title": "",
  "meta_description": "",
  "handle": "",
  "excerpt": "",
  "tags": [],
  "author": "",
  "publish_at": "YYYY-MM-DDTHH:MM+11:00",
  "featured_image": {"file": "", "alt": ""},
  "primary_keyword": "",
  "secondary_keywords": [],
  "semantic_terms": [],
  "faq_questions": [],
  "source": "",
  "video_url": "",
  "information_gain": ""
}
```

`publish_at` offset: use `+11:00` during daylight saving (AEDT, first Sunday in October to first Sunday in April). Use `+10:00` otherwise (AEST, or Queensland all year).

Then reply in chat with:

- the keyword set
- the SEO check summary
- open items: images needed, `[CHECK]` claims, theme fixes

Keep the reply short. The files carry the detail.

## Launch checklist

- [ ] Scheduled to go live with the post at [date and time AEST/AEDT].
- [ ] No `IMAGE NEEDED` placeholders remain. All images are uploaded to Shopify Files and renamed, with alt text.
- [ ] The featured image and its alt text are set. The excerpt is filled in. Both feed the theme's Article schema.
- [ ] The author is set, and "Show author" is on in the theme editor.
- [ ] Every product fact was verified on the live product page today. No `[CHECK]` items remain.
- [ ] All internal links resolve (product pages, size guide, other articles).
- [ ] The "You may also like" section is not showing placeholder "Example collection" items.
- [ ] After it goes live:
  - Request indexing in Search Console.
  - Confirm the article appears in `sitemap.xml`.
  - Link to it from the social post or ad caption.
  - Add it to the next Klaviyo newsletter.
- [ ] Log the primary keyword in the content map (keyword bank) so future articles don't cannibalise it.

## Hard rules

- No `<h1>` or `<script>` in the body. No em dashes anywhere. Never use the phrase "we're diggin' it".
- Never invent search volumes, stats, reviews, customer names or specs. Unsourced means "unverified" or `[CHECK]`.
- No FAQPage or HowTo schema. The FAQ is visible content only.
- Every link has descriptive anchor text. Never "click here" or a bare "Shop Now".
- Never change the handle after publishing.
- Product facts in this skill are a snapshot from 7 Oct 2026. The live site always wins.

## Reference files

| File | Read when |
|---|---|
| `references/seo-rules.md` | Always. Keyword method, on-page numbers, E-E-A-T, GEO, schema. |
| `references/article-blueprint.md` | Always. Voice, structure, article types, transcript method. |
| `references/tov-guide.md` | Always. Measured brand voice, vocabulary, site inconsistencies to avoid repeating, and the 30-point TOV rubric. Self-score every draft: pass is 24/30 with no dimension below 3. |
| `references/design-blocks.md` | Writing the HTML |
| `references/shopify-and-theme.md` | Packaging fields, theme behaviour, launch timing |
| `references/image-sourcing.md` | Finding or requesting images |
| `references/keyword-bank.md` | Keyword research (grep it) |
| `references/product-catalogue.md` | Product facts (grep the product) |
| `references/usp-bank.md` | Proof points and customer quotes (grep) |
| `examples/how-to-load-grease-gun/` | Worked example from the Grease VS Clone brief (2,168 words, 0 FAIL). Read it once to calibrate quality and structure. |
