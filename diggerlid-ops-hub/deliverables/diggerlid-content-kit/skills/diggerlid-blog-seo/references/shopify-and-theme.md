# Shopify Blog and Theme Facts

Verified via the Shopify Admin API on 7 Oct 2026. Re-check before a launch if anything looks different.

## The blog

| Field | Value |
|---|---|
| Blog | **News**, handle `news`, URL `https://diggerlid.com/blogs/news` |
| Articles | **0** (7 Oct 2026). The first article you ship launches the blog. |
| Article URL | `https://diggerlid.com/blogs/news/<article-handle>` |
| Theme | Custom theme `DiggerLid-Web/main` |
| Template | `templates/article.json`, which renders `sections/article-template.liquid` and then the `blog-posts` section titled "You may also like" |

## What the template renders, and what that means for you

- **H1 = the article Title field.** The template prints `<h1>{{ article.title }}</h1>`.
  - **Never put an `<h1>` in the body HTML.** Start the body at `<h2>`.
  - The site audit flagged multiple H1s as a critical issue, so don't add another.
- **Body** is rendered as `{{ article.content }}` inside `.article__body.rte`.
  - The theme's rich-text styles apply to `h2`, `h3`, `p`, `ul`, `ol`, `table`, `blockquote` and `img`.
  - Custom blocks need inline styles. See `design-blocks.md`.
- **Breadcrumbs** render automatically via `render 'breadcrumbs'`.
- **Shown by default:**
  - Date (`blog_show_date` is true)
  - Tags, linked to `/blogs/news/tagged/<tag>`. Tags that start with `_` are hidden, so use `_hidden` tags for internal grouping.
  - Social sharing
- **Off by default:**
  - **Author** (`blog_show_author`). ⚠️ Recommend switching it on in the theme editor (Blog post > Show author). A visible author is an E-E-A-T signal.
  - **Hero image** (`image_hero`). When it's off, the featured image is not shown at the top of the article. So also place the hero image inside the body, after the intro paragraph.
- **Comments** follow the blog's comment setting.

### Built-in JSON-LD

The template already outputs `Article` schema from these fields:

| Schema property | Article field |
|---|---|
| headline | Title |
| description | Excerpt (summary) |
| image | Featured image |
| datePublished / dateModified | publish and update dates |
| author | Person name |
| publisher | Shop name |

So **fill the Excerpt and the Featured image every time**, or the schema is incomplete.

Known gaps you can't fix from article content:

- Uses `http://schema.org`
- No `author.url`
- No `BreadcrumbList`
- No `VideoObject`

The theme upgrade in the section below fixes these. Hand it to the developer once, not per article.

### "You may also like"

This section lists other blog posts. With 0 articles it currently shows **placeholder "Example collection" items**. ⚠️ Check how it renders before launch and turn the section off if it still shows placeholders.

## Fields to fill in Shopify Admin

Online Store > Blog posts > Add blog post.

| Admin field | What goes in | Limit and rule |
|---|---|---|
| Title | The H1. Primary keyword near the front, human and clickable. | 70 characters maximum. Aim for 45 to 65. |
| Content (Show HTML `<>`) | The body HTML from the output | Starts at `<h2>`. No `<h1>`, no `<script>`. |
| Excerpt | 1 to 2 sentences that answer the query | 160 characters maximum. It feeds the schema description and the blog cards. |
| Featured image | The hero image | At least 1200px wide, 16:9 or 1.91:1. Set alt text. |
| Author | A real person, e.g. "Joel, DiggerLid co-founder" | Must match the byline in the body |
| Tags | 2 to 4 topical tags, plus `_` internal tags | e.g. `Pro Enclosure`, `Machine Care`, `_bfcm-2026` |
| Search engine listing > Page title | SEO title tag | 50 to 60 characters, ending with ` \| DiggerLid` |
| Search engine listing > Meta description | Meta description | 130 to 150 characters, with the primary keyword and a reason to click. No quotes or hashtags. |
| Search engine listing > URL handle | Slug | 3 to 6 words, lowercase and hyphenated, primary keyword, no dates or stop words |
| Visibility | Set a date and time | Schedule it to match the social post or ad go-live (AEST/AEDT) |

## Publishing it alongside the post or ad

1. Set Visibility to **Visible on** the post's date and time. Shopify publishes it automatically.
2. Point the ad's or post's link at the article URL (with UTMs) **only if** the post is educational. For a sales ad, keep the PDP as the destination and link the article from the post's caption or comments.
3. After it publishes:
   - Request indexing in Google Search Console (URL Inspection).
   - Check `https://diggerlid.com/sitemap.xml` lists it. Shopify adds blog sitemaps automatically.
4. Share the article in the next Klaviyo newsletter for early signals.

## Optional theme upgrade (one-off, for the developer)

Add this to `sections/article-template.liquid` to emit richer schema. It reads optional article metafields.

- Switch the context to `https://schema.org` and the type to `BlogPosting`.
- Add `author.url` pointing to `/pages/about`, once that page exists.
- Add a `BreadcrumbList`: Home > News > Article.
- If metafield `custom.video_url` is set, add a `VideoObject` with these fields: name, description, thumbnailUrl, uploadDate, contentUrl/embedUrl, duration.
- Turn on Show author.

Until the developer does this, don't paste `<script type="application/ld+json">` into the article body. Shopify may strip it, and it duplicates the theme's Article schema.
