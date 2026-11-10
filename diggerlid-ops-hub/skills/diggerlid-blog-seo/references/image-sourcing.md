# Image Sourcing

Every article needs:

- 1 featured or hero image
- 1 image per 300 to 400 words, for 3 to 6 body images in total
- 1 product image per product callout

Real photos from shoots beat stock every time, because they're an E-E-A-T "experience" signal.

## Where to look, in order

1. **Frame.io (the "frame folder").** Shoot stills and video frames live in the Frame.io project for the shoot.
   - If a Frame.io connector or tool is available in the session, search the project or folder named for the shoot or video. Pull stills, or grab frames at the timecodes that match each section.
   - If there's no connector, **ask the user** for one of these:
     - the Frame.io share link to the folder
     - exported stills (JPG or PNG, at least 1600px wide)
     - timecodes they're happy to screenshot

     When asking, list the exact shots you need (see the shot list below).
2. **Files the user attached in the chat.** Look at every one and describe what's in it before using it.
3. **Google Drive.** Search for the shoot name, product or date.
4. **Shopify.** Existing product and lifestyle images are already on the CDN with stable URLs.
   - Existing CDN file names can't be changed. The renaming rule applies to new uploads only, so write good alt text for these.
   - Skip any image that looks AI-generated. The Earthmovers Bundle's product image is one.
   - This query is pre-validated, so run it directly:

   
   `products(query:"handle:<handle>"){ nodes{ media(first:10){ nodes{ ... on MediaImage{ image{ url altText width height } } } } } }`
   Use these for product callout cards.
5. **Never** use AI-generated images of real products presented as real photos. Don't hotlink images from other sites.

## Shot list template (send this when asking)

```
For "[Article title]" I need:
1. HERO (16:9, 1600px+): [e.g. Pro Enclosure fitted on a mini digger in rain, operator inside]
2. [Section H2]: [e.g. close-up of YKK zip and 490 GSM fabric]
3. [Section H2]: [e.g. wide shot on site at the worksite location]
4. [Section H2]: [e.g. before/after or old-way vs new-way frame]
5. PRODUCT: [pulled from Shopify, no action needed]
Frame.io link or exported stills work. Timecodes are fine too.
```

## Image SEO rules

- **File name:** descriptive, lowercase, hyphenated, ideally with the keyword. Rename before uploading.
  - Good: `pro-enclosure-mini-excavator-rain-kubota-u17.jpg`
  - Bad: `IMG_4821.jpg` or `Universal-Cover.png`. The site audit flagged names like these.
- **Alt text:** describe what's actually in the image, in under 125 characters. Use the keyword at most once across the article's alt texts, and only where it's true. No "image of".
- **Format and size:**
  - Upload JPG or PNG at 1600 to 2000px wide. Shopify's CDN serves WebP and AVIF automatically.
  - Targets: content images under 200KB, hero under 300KB (500KB / 700KB are hard limits). Compress first, because the site audit flagged heavy images as a speed issue.
- **Dimensions:** always put `width` and `height` on the `<img>` tag to prevent layout shift.
- **Loading:** first image `loading="eager" fetchpriority="high"`, all others `loading="lazy"`.
- **Upload path:** Shopify Admin > Content > Files. Copy the CDN URL into the article HTML.
- **Featured image:** set it separately in the article's Featured image field, with alt text. It feeds the schema, social share cards and blog listing cards.

## While images are pending

Put a clear placeholder in the HTML, so the article can be built and approved in parallel:

```html
<!-- IMAGE NEEDED: [shot description] | file: [suggested-file-name.jpg] | alt: "[suggested alt]" -->
```

The launch checklist blocks publishing while any `IMAGE NEEDED` comment remains.
