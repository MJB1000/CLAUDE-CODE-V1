#!/usr/bin/env python3
"""Build a branded preview of a DiggerLid blog article, plus a Google snippet preview.

Usage: python3 scripts/build_preview.py article.html seo-fields.json preview.html

Approximates the live theme (breadcrumbs, date, H1, narrow body) so the user can review
layout and design blocks before pasting into Shopify. Standard library only.
"""
import html as h
import json, sys
from datetime import datetime

TEMPLATE = """<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{seo_title}</title><meta name="description" content="{meta}">
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@600;800&display=swap" rel="stylesheet">
<style>
:root{{--black:#231f20;--yellow:#f5eb19;--y40:#fbf7a3;--line:#e6e3dc;--bg:#fff;--fg:#231f20}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#1a1718;--fg:#f3f1ec;--line:#3a3637}}}}
:root[data-theme=dark]{{--bg:#1a1718;--fg:#f3f1ec;--line:#3a3637}}
body{{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
.bar{{background:var(--black);color:var(--yellow);font:800 14px League Spartan,sans-serif;letter-spacing:.06em;padding:10px 16px;text-align:center}}
.snippet{{max-width:720px;margin:20px auto;padding:16px;border:1px dashed var(--line);border-radius:8px;font-family:arial,sans-serif}}
.snippet .u{{font-size:13px;opacity:.7}} .snippet .t{{color:#1a0dab;font-size:20px;margin:4px 0}} .snippet .d{{font-size:14px;opacity:.85}}
@media (prefers-color-scheme:dark){{.snippet .t{{color:#8ab4f8}}}}
.wrap{{max-width:760px;margin:0 auto;padding:0 16px 60px}}
.crumbs{{font-size:13px;opacity:.7;margin:24px 0 6px}} .date{{font-size:13px;opacity:.7}}
h1{{font:800 clamp(28px,5vw,42px)/1.15 League Spartan,sans-serif;margin:6px 0 4px}}
.rte h2{{font:800 26px/1.2 League Spartan,sans-serif;margin:40px 0 10px}} .rte h3{{font:600 20px/1.3 League Spartan,sans-serif;margin:26px 0 8px}}
.rte img{{max-width:100%;height:auto}} .rte a{{color:inherit;text-decoration-color:var(--yellow);text-decoration-thickness:3px}}
.rte table{{font-size:15px}} .note{{font-size:13px;opacity:.7;text-align:center;margin-top:40px}}
</style></head><body>
<div class="bar">PREVIEW · NOT LIVE · {publish}</div>
<div class="snippet"><div class="u">diggerlid.com › blogs › news › {handle}</div><div class="t">{seo_title}</div><div class="d">{meta}</div></div>
<div class="wrap">
<div class="crumbs">Home › News › {title}</div>
<div class="date">{tags}{date}</div>
<h1>{title}</h1>
<div class="date">by {author}</div>
<div class="rte">{body}</div>
<p class="note">Featured image (set in Shopify): {fimg} · alt: "{falt}"</p>
</div></body></html>"""


def main(a, b, out):
    body = open(a, encoding="utf-8").read()
    f = json.load(open(b, encoding="utf-8"))
    pub = f.get("publish_at") or ""
    try:
        d = datetime.fromisoformat(pub)
        date = f"{d.day} {d:%B %Y}"
    except ValueError:
        date = "Unscheduled"
    fi = f.get("featured_image") or {}
    page = TEMPLATE.format(
        seo_title=h.escape(f.get("seo_title", "")), meta=h.escape(f.get("meta_description", "")),
        handle=h.escape(f.get("handle", "")), title=h.escape(f.get("title", "")),
        author=h.escape(f.get("author", "")), publish=h.escape(pub or "unscheduled"), date=date,
        tags="".join(h.escape(t) + " · " for t in f.get("tags", []) if not t.startswith("_")),
        body=body, fimg=h.escape(fi.get("file", "")), falt=h.escape(fi.get("alt", "")))
    open(out, "w", encoding="utf-8").write(page)
    print("Wrote", out)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
