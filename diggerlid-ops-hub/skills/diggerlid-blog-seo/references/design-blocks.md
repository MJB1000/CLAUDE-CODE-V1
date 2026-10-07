# Design Blocks (paste-ready HTML)

The theme renders article content inside `.rte` and only styles basic tags. These blocks use **inline styles only**, because Shopify keeps `style` attributes in article HTML. They use the brand palette, look built-for-purpose, and still read as clean semantic HTML for SEO.

## Palette

| Name | Hex |
|---|---|
| Black | `#231f20` |
| Black 90% | `#3a3637` |
| Yellow | `#f5eb19` |
| Yellow 40% | `#fbf7a3` |
| White | `#ffffff` |
| Border grey | `#e6e3dc` |

Body text stays theme default. Don't set fonts. The theme already loads the brand fonts.

## Rules

- Use semantic tags first (`h2`, `h3`, `p`, `ul`, `table`, `figure`, `blockquote`). Styling sits on top.
- No `<h1>`. No `<script>`. No external CSS.
- Every `<img>` needs a descriptive `alt`, plus `width`, `height` and `loading="lazy"`. The exception is the first (hero) image, which takes `loading="eager" fetchpriority="high"`.
- Every link has descriptive anchor text. Never "click here" or a bare "Shop Now".
- Use 4 to 7 blocks per article. A page full of boxes is as bad as a wall of text.
- Mobile first: no fixed widths over 100%, and tables get a scroll wrapper.

## 1. Key takeaways (top of article, after the intro)

Answer-first summary. Good for skimmers and AI citation.

```html
<div style="background:#fbf7a3;border-left:6px solid #231f20;padding:18px 22px;margin:28px 0;border-radius:4px;">
  <p style="margin:0 0 8px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;">The short version</p>
  <ul style="margin:0;padding-left:20px;">
    <li>[Direct answer to the primary query in one line]</li>
    <li>[Key number or fact]</li>
    <li>[What to do next]</li>
  </ul>
</div>
```

## 2. Hero or inline figure

```html
<figure style="margin:28px 0;">
  <img src="[CDN URL]" alt="[What is in the shot, with the keyword only if natural]" width="1600" height="900" loading="eager" fetchpriority="high" style="width:100%;height:auto;border-radius:6px;">
  <figcaption style="font-size:.9em;opacity:.75;margin-top:6px;">[Caption that adds context, e.g. location or machine model]</figcaption>
</figure>
```

## 3. Video embed (when the source is a video)

Responsive 16:9. Use YouTube's privacy URL. Put a one-line text summary above it, because the transcript content lives in the article itself.

```html
<div style="position:relative;padding-top:56.25%;margin:28px 0;border-radius:6px;overflow:hidden;background:#231f20;">
  <iframe src="https://www.youtube-nocookie.com/embed/[VIDEO_ID]" title="[Descriptive video title]" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>
</div>
```

For a vertical (9:16) Reel or TikTok, use `padding-top:177.78%` with `max-width:380px;margin:28px auto;`. You can also link out to the post with a thumbnail image.

## 4. Product callout card (1 to 2 per article)

```html
<div style="display:flex;flex-wrap:wrap;gap:18px;align-items:center;border:2px solid #231f20;border-radius:8px;padding:18px;margin:32px 0;">
  <img src="[product image CDN URL]" alt="[Product name] [what it shows]" width="220" height="220" loading="lazy" style="width:160px;height:auto;border-radius:4px;">
  <div style="flex:1;min-width:220px;">
    <p style="margin:0 0 4px;font-weight:700;font-size:1.15em;">[Product name]</p>
    <p style="margin:0 0 10px;">[One-line benefit. Spec proof.]</p>
    <a href="https://diggerlid.com/products/[handle]" style="display:inline-block;background:#f5eb19;color:#231f20;font-weight:700;padding:10px 18px;border-radius:4px;text-decoration:none;">See the [product name] →</a>
  </div>
</div>
```

## 5. Spec or comparison table

```html
<div style="overflow-x:auto;margin:28px 0;">
<table style="width:100%;border-collapse:collapse;min-width:480px;">
  <thead><tr style="background:#231f20;color:#fff;"><th style="padding:10px;text-align:left;">[Col]</th><th style="padding:10px;text-align:left;">[Old way]</th><th style="padding:10px;text-align:left;">[DiggerLid way]</th></tr></thead>
  <tbody>
    <tr style="border-bottom:1px solid #e6e3dc;"><td style="padding:10px;">[Row]</td><td style="padding:10px;">[..]</td><td style="padding:10px;">[..]</td></tr>
  </tbody>
</table>
</div>
```

## 6. Pull quote (customer or founder voice)

```html
<blockquote style="margin:32px 0;padding:16px 22px;border-left:6px solid #f5eb19;background:#231f20;color:#fff;border-radius:4px;">
  <p style="margin:0;font-size:1.15em;">"[Verbatim quote]"</p>
  <p style="margin:8px 0 0;font-size:.9em;opacity:.8;">[Name or role, location, only with permission]</p>
</blockquote>
```

## 7. Numbered steps (how-to sections)

Use a plain `<ol>` with `<h3>` step headings when the steps are substantial. Don't use HowTo schema. It's deprecated for rich results.

## 8. FAQ section (end of article)

A visible FAQ helps both humans and AI answers. Google only shows FAQ rich results for authoritative government and health sites, so the FAQ is there for content value, not stars.

```html
<h2>[Primary keyword] FAQs</h2>
<h3>[Real question from People Also Ask, a review or support]</h3>
<p>[Direct answer in 40 to 60 words, first sentence answers it outright.]</p>
```

## 9. Closing CTA band

```html
<div style="background:#231f20;color:#fff;padding:26px 22px;border-radius:8px;margin:36px 0;text-align:center;">
  <p style="margin:0 0 6px;font-size:1.3em;font-weight:700;color:#f5eb19;">[Short punchy line in brand voice]</p>
  <p style="margin:0 0 16px;">[One sentence: what to do and why now. Fast shipping Australia wide.]</p>
  <a href="https://diggerlid.com/products/[handle]" style="display:inline-block;background:#f5eb19;color:#231f20;font-weight:700;padding:12px 22px;border-radius:4px;text-decoration:none;">Shop the [product name]</a>
</div>
```

## 10. Author byline box (E-E-A-T, top or bottom)

```html
<div style="display:flex;gap:14px;align-items:center;border-top:1px solid #e6e3dc;border-bottom:1px solid #e6e3dc;padding:14px 0;margin:28px 0;">
  <div><p style="margin:0;font-weight:700;">Written by [Name], [role]</p>
  <p style="margin:2px 0 0;font-size:.9em;opacity:.8;">[One line of real experience, e.g. "Landscaping tradie turned founder. Has run mini diggers in Aussie weather since 20XX."] Updated [D Month YYYY].</p></div>
</div>
```
