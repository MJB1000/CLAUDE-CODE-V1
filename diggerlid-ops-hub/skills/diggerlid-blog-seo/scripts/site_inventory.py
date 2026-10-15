#!/usr/bin/env python3
"""Crawl diggerlid.com via its sitemap and build a site inventory for the pre-write mini audit.

Usage:
  python3 scripts/site_inventory.py OUT_DIR [--base https://diggerlid.com] [--max 400] [--types products,pages,collections,blogs,metaobject_pages]

Writes to OUT_DIR:
  inventory.json   one record per URL: type, title, meta, canonical, h1s, h2s, words, links out, inbound count,
                   images, images missing alt, robots noindex
  inventory.md     audit tables: issues per page, link targets, keyword-ish titles (for cannibalisation checks)
  corpus.md        the visible main-content copy of every page (input for the tone-of-voice guide)

Standard library only. Polite: one request at a time with a short delay. Read-only.
"""
import json, re, sys, time, urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; DiggerLid-SiteInventory/1.0)"
SKIP_TAGS = {"script", "style", "noscript", "svg", "template"}
CHROME_TAGS = {"header", "footer", "nav"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-AU"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def sitemap_urls(base, types):
    idx = get(base.rstrip("/") + "/sitemap.xml")
    out = []
    for sm in re.findall(r"<loc>([^<]+)</loc>", idx):
        sm = sm.replace("&amp;", "&")
        kind = next((t for t in types if f"sitemap_{t}" in sm), None)
        if not kind:
            continue
        xml = get(sm)
        for loc in re.findall(r"<url>\s*<loc>([^<]+)</loc>", xml):
            out.append((kind, loc.replace("&amp;", "&")))
    return out


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.meta, self.canonical, self.robots = "", "", "", ""
        self.h, self.links, self.imgs = [], [], []
        self.main_text, self.all_text = [], []
        self._skip = 0
        self._chrome = 0
        self._main = 0
        self._cur_h = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP_TAGS:
            self._skip += 1
        if tag in CHROME_TAGS:
            self._chrome += 1
        if tag == "main" or a.get("id") == "MainContent":
            self._main += 1
        if tag == "title" and not self.title and not self._skip:
            self._in_title = True
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.meta = (a.get("content") or "").strip()
        elif tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots = (a.get("content") or "").lower()
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href") or ""
        elif tag in ("h1", "h2", "h3"):
            self._cur_h = [tag, ""]
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img" and not self._chrome:
            self.imgs.append(a)

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self._skip:
            self._skip -= 1
        if tag in CHROME_TAGS and self._chrome:
            self._chrome -= 1
        if tag == "main" and self._main:
            self._main -= 1
        if tag == "title":
            self._in_title = False
        if self._cur_h and tag == self._cur_h[0]:
            t = re.sub(r"\s+", " ", self._cur_h[1]).strip()
            if t:
                self.h.append((self._cur_h[0], t))
            self._cur_h = None

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._skip:
            return
        if self._cur_h is not None:
            self._cur_h[1] += d
        if not self._chrome:
            self.all_text.append(d)
            if self._main:
                self.main_text.append(d)


def norm(base, href):
    u = urljoin(base, href.split("#")[0])
    p = urlparse(u)
    if p.netloc.replace("www.", "") != urlparse(base).netloc.replace("www.", ""):
        return None
    path = re.sub(r"/+$", "", p.path) or "/"
    if any(path.startswith(x) for x in ("/cart", "/account", "/search", "/checkout", "/cdn", "/policies")):
        return None
    return path


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    out_dir = args[0]
    opt = dict(zip(args[1::2], args[2::2])) if len(args) > 1 else {}
    base = opt.get("--base", "https://diggerlid.com")
    mx = int(opt.get("--max", 400))
    types = opt.get("--types", "products,pages,collections,blogs,metaobject_pages").split(",")
    import os
    os.makedirs(out_dir, exist_ok=True)

    urls = ([("home", base.rstrip("/") + "/")] + sitemap_urls(base, types))[:mx]
    recs, inbound = [], Counter()
    corpus = []
    for i, (kind, url) in enumerate(urls, 1):
        try:
            html = get(url)
        except Exception as e:  # keep going on one bad page
            recs.append({"url": url, "type": kind, "error": str(e)})
            continue
        p = Page()
        p.feed(html)
        text = re.sub(r"\s+", " ", " ".join(p.main_text or p.all_text)).strip()
        out_links = sorted({n for n in (norm(base, l) for l in p.links) if n})
        path = norm(base, url) or url
        for l in out_links:
            if l != path:
                inbound[l] += 1
        rec = {
            "url": url, "path": path, "type": kind,
            "title": re.sub(r"\s+", " ", p.title).strip(), "meta": p.meta, "canonical": p.canonical,
            "noindex": "noindex" in p.robots,
            "h1": [t for h, t in p.h if h == "h1"], "h2": [t for h, t in p.h if h == "h2"][:25],
            "words": len(text.split()), "links_out": out_links,
            "images": len(p.imgs), "images_no_alt": sum(1 for im in p.imgs if not (im.get("alt") or "").strip()),
        }
        recs.append(rec)
        corpus.append(f"\n\n## {rec['title']}\n{url}\n\n{text}")
        print(f"[{i}/{len(urls)}] {kind:11} {rec['words']:5}w h1={len(rec['h1'])} {path}", file=sys.stderr)
        time.sleep(0.4)

    for r in recs:
        if "path" in r:
            r["inbound"] = inbound.get(r["path"], 0)
    json.dump(recs, open(f"{out_dir}/inventory.json", "w"), indent=1)
    open(f"{out_dir}/corpus.md", "w").write(f"# Site copy corpus ({base}, {time.strftime('%d %b %Y')})" + "".join(corpus))

    ok = [r for r in recs if "path" in r]
    L = [f"# Site inventory: {base} ({time.strftime('%d %b %Y')})\n",
         f"{len(ok)} pages crawled ({', '.join(f'{k} {v}' for k, v in Counter(r['type'] for r in ok).items())}). "
         f"{len(recs) - len(ok)} errors.\n",
         "## Issues by page\n", "| Page | Type | Title len | Meta len | H1s | Words | Imgs no alt | Inbound | Flags |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(ok, key=lambda r: (r["type"], r["path"])):
        flags = []
        tl, ml = len(r["title"]), len(r["meta"])
        if not 30 <= tl <= 60: flags.append("title length")
        if not 120 <= ml <= 160: flags.append("meta length" if ml else "no meta")
        if len(r["h1"]) != 1: flags.append(f"{len(r['h1'])} H1s")
        if r["type"] in ("products", "collections") and r["words"] < 300: flags.append("thin")
        if r["images_no_alt"]: flags.append("alt missing")
        if r["inbound"] < 3: flags.append("weakly linked")
        if r["noindex"]: flags.append("noindex")
        L.append(f"| {r['path']} | {r['type']} | {tl} | {ml} | {len(r['h1'])} | {r['words']} | {r['images_no_alt']} | {r['inbound']} | {', '.join(flags)} |")
    L += ["\n## Link targets (use for interlinking)\n", "| Path | Title | H1 | Type |", "|---|---|---|---|"]
    for r in sorted(ok, key=lambda r: (r["type"], r["path"])):
        L.append(f"| {r['path']} | {r['title'][:70]} | {(r['h1'] or [''])[0][:60]} | {r['type']} |")
    L += ["\n## Headings per page (for cannibalisation and topic gaps)\n"]
    for r in ok:
        if r["h2"]:
            L.append(f"- **{r['path']}**: " + " / ".join(r["h2"][:12]))
    open(f"{out_dir}/inventory.md", "w").write("\n".join(L) + "\n")
    print(f"Wrote {out_dir}/inventory.json, inventory.md, corpus.md ({len(ok)} pages)", file=sys.stderr)


if __name__ == "__main__":
    main()
