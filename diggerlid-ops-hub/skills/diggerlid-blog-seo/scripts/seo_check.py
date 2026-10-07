#!/usr/bin/env python3
"""SEO check for a DiggerLid blog article before it goes into Shopify.

Usage: python3 scripts/seo_check.py article.html seo-fields.json

Prints PASS / WARN / FAIL lines and exits 1 if any FAIL. Standard library only.
Thresholds follow references/seo-rules.md.
"""
import json, re, sys
from html.parser import HTMLParser

BANNED = ["elevate", "unlock", "revolutionary", "game-changing", "game changing", "seamless",
          "cutting-edge", "innovative", "in today's fast-paced", "we're diggin", "were diggin"]
GENERIC_ANCHORS = {"click here", "here", "shop now", "read more", "learn more", "this", "link"}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text, self.headings, self.imgs, self.links = [], [], [], []
        self._h = None
        self._a = None
        self.tags = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = [tag, ""]
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self._a = [a.get("href", ""), ""]
        elif tag == "script":
            self.scripts += 1

    def handle_endtag(self, tag):
        if self._h and tag == self._h[0]:
            self.headings.append((self._h[0], self._h[1].strip()))
            self._h = None
        elif tag == "a" and self._a is not None:
            self.links.append((self._a[0], self._a[1].strip()))
            self._a = None

    def handle_data(self, d):
        self.text.append(d)
        if self._h:
            self._h[1] += d
        if self._a is not None:
            self._a[1] += d


def main(html_path, fields_path):
    html = open(html_path, encoding="utf-8").read()
    f = json.load(open(fields_path, encoding="utf-8"))
    p = Parser()
    p.feed(html)
    text = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    words = text.split()
    low = text.lower()
    kw = (f.get("primary_keyword") or "").lower().strip()
    out = []

    def r(level, msg):
        out.append((level, msg))

    def rng(name, val, lo, hi, hard=True):
        n = len(val or "")
        if lo <= n <= hi:
            r("PASS", f"{name}: {n} chars")
        else:
            r("FAIL" if hard else "WARN", f"{name}: {n} chars (want {lo}-{hi})")

    # Fields
    rng("SEO title", f.get("seo_title"), 50, 60)
    rng("Meta description", f.get("meta_description"), 130, 150)
    rng("H1 / Title", f.get("title"), 45, 70, hard=False)
    rng("Excerpt", f.get("excerpt"), 70, 160, hard=False)
    md = f.get("meta_description") or ""
    if '"' in md or "#" in md:
        r("FAIL", "Meta description contains quotes or hashtags")
    handle = f.get("handle") or ""
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+){1,7}", handle):
        r("FAIL", f"Handle '{handle}' must be lowercase-hyphenated, 2-8 words")
    if not f.get("author"):
        r("FAIL", "Author missing")
    fi = f.get("featured_image") or {}
    if not fi.get("alt"):
        r("FAIL", "Featured image alt missing")
    if not f.get("publish_at"):
        r("WARN", "publish_at missing (schedule to match the post)")

    # Keyword placement
    if not kw:
        r("FAIL", "primary_keyword missing")
    else:
        first100 = " ".join(words[:100]).lower()
        checks = {
            "SEO title": kw in (f.get("seo_title") or "").lower(),
            "H1": kw in (f.get("title") or "").lower(),
            "meta description": kw in md.lower(),
            "first 100 words": kw in first100,
            "handle": all(w in handle for w in re.findall(r"[a-z0-9]+", kw) if len(w) > 2),
            "an image alt": any(kw in (i.get("alt") or "").lower() for i in p.imgs) or kw in (fi.get("alt") or "").lower(),
            "an H2": any(kw in t.lower() for h, t in p.headings if h == "h2"),
        }
        for k, ok in checks.items():
            r("PASS" if ok else ("FAIL" if k in ("SEO title", "H1", "first 100 words") else "WARN"),
              f"Primary keyword in {k}")
        count = low.count(kw)
        density = 100 * count * len(kw.split()) / max(len(words), 1)
        r("PASS" if 0.5 <= density <= 3 else "WARN", f"Keyword density {density:.1f}% ({count} uses)")

    # Structure
    n = len(words)
    r("PASS" if n >= 1500 else "FAIL", f"Word count {n} (min 1500)")
    h1s = [t for h, t in p.headings if h == "h1"]
    r("FAIL" if h1s else "PASS", f"H1 tags in body: {len(h1s)} (must be 0, theme prints the H1)")
    levels = [int(h[1]) for h, _ in p.headings]
    skipped = any(b - a > 1 for a, b in zip([1] + levels, levels))
    r("FAIL" if skipped else "PASS", "Heading levels do not skip" if not skipped else "Heading level skipped")
    h2 = sum(1 for h, _ in p.headings if h == "h2")
    r("PASS" if 4 <= h2 <= 10 else "WARN", f"H2 sections: {h2}")
    faq = any("faq" in t.lower() or "frequently asked" in t.lower() for h, t in p.headings if h == "h2")
    r("PASS" if faq else "WARN", "FAQ section present")
    if p.scripts:
        r("FAIL", f"{p.scripts} <script> tag(s) in body")

    # Links
    internal = [l for l in p.links if "diggerlid.com" in l[0] or l[0].startswith("/")]
    external = [l for l in p.links if l not in internal and l[0].startswith("http")]
    r("PASS" if 5 <= len(internal) <= 12 else "WARN", f"Internal links: {len(internal)} (want 5-10)")
    r("PASS" if len(external) <= 4 else "WARN", f"External links: {len(external)}")
    prod = {l[0] for l in internal if "/products/" in l[0]}
    r("PASS" if len(prod) >= 1 else "FAIL", f"Product pages linked: {len(prod)}")
    gen = [a for _, a in p.links if a.lower().strip(" →>.") in GENERIC_ANCHORS]
    if gen:
        r("FAIL", f"Generic anchor text: {gen}")

    # Images
    want = max(2, n // 400)
    r("PASS" if len(p.imgs) >= want else "WARN", f"Images in body: {len(p.imgs)} (want >= {want})")
    for i, im in enumerate(p.imgs, 1):
        alt = im.get("alt")
        if alt is None or not (10 <= len(alt) <= 125):
            r("FAIL", f"Image {i} alt missing or not 10-125 chars")
        if not (im.get("width") and im.get("height")):
            r("WARN", f"Image {i} missing width/height")
        src = im.get("src", "")
        if re.search(r"/(img|image|dsc|screenshot)[-_ ]?\d+", src, re.I):
            r("WARN", f"Image {i} filename looks generic: {src.rsplit('/', 1)[-1]}")
    if p.imgs and p.imgs[0].get("loading") == "lazy":
        r("WARN", "First (hero) image should not be lazy-loaded")
    pending = html.count("IMAGE NEEDED")
    if pending:
        r("WARN", f"{pending} IMAGE NEEDED placeholder(s), publishing blocked until filled")

    # Voice and claims
    EM = chr(0x2014)
    if EM in html or EM in json.dumps(f, ensure_ascii=False):
        r("FAIL", "Em dash found")
    hits = [b for b in BANNED if b in low]
    if hits:
        r("FAIL", f"Banned words: {hits}")
    if re.search(r"free (shipping|delivery)", low):
        r("FAIL", "Free shipping claim found. Use 'Fast shipping Australia wide'")
    if "[check]" in low:
        r("WARN", "[CHECK] claims remain, verify before publishing")
    sents = [s for s in re.split(r"[.!?]+\s", text) if len(s.split()) > 2]
    avg = sum(len(s.split()) for s in sents) / max(len(sents), 1)
    r("PASS" if avg <= 22 else "WARN", f"Average sentence length {avg:.0f} words")

    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    for lvl, msg in sorted(out, key=lambda x: order[x[0]]):
        print(f"{lvl:5} {msg}")
    fails = sum(1 for l, _ in out if l == "FAIL")
    warns = sum(1 for l, _ in out if l == "WARN")
    print(f"\n{fails} FAIL, {warns} WARN, {len(out) - fails - warns} PASS")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
