#!/usr/bin/env python3
"""SEO check for a DiggerLid blog article before it goes into Shopify.

Usage: python3 scripts/seo_check.py article.html seo-fields.json

Prints PASS / WARN / FAIL lines and exits 1 if any FAIL. Standard library only.
Thresholds match references/seo-rules.md exactly.
"""
import json, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse

BANNED = ["elevate", "unlock", "revolutionary", "game-changing", "game changing", "seamless", "solution",
          "ultimate", "cutting-edge", "innovative", "in today's fast-paced", "we're diggin", "were diggin"]
GENERIC_ANCHORS = {"click here", "here", "shop now", "read more", "learn more", "this", "link"}
STOP = {"a", "an", "the", "of", "for", "and", "to", "in", "on", "with", "is", "your", "my"}
EM, EN = chr(0x2014), chr(0x2013)
OWN_HOSTS = {"diggerlid.com", "www.diggerlid.com", "diggerlid.com.au", "www.diggerlid.com.au"}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.headings, self.imgs, self.links = [], [], [], []
        self._h = self._a = None
        self.scripts = 0
        self.boxes = 0  # styled div/blockquote/table blocks
        self.faq_h3 = []  # questions under the FAQ H2
        self.in_faq = False
        self.p_after = None  # collecting first paragraph after an FAQ h3
        self.faq_answers = []
        self.first_p = None
        self._p = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = [tag, ""]
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self._a = [a.get("href", ""), "", a.get("target")]
        elif tag == "script":
            self.scripts += 1
        elif tag == "p":
            self._p = ""
        if tag in ("div", "blockquote") and "background" in (a.get("style") or ""):
            self.boxes += 1
        if tag == "div" and "border:2px solid" in (a.get("style") or ""):
            self.boxes += 1
        if tag == "table":
            self.boxes += 1

    def handle_endtag(self, tag):
        if self._h and tag == self._h[0]:
            lvl, txt = self._h[0], self._h[1].strip()
            self.headings.append((lvl, txt))
            if lvl == "h2":
                self.in_faq = bool(re.search(r"faq|frequently asked", txt, re.I))
            elif lvl == "h3" and self.in_faq:
                self.faq_h3.append(txt)
                self.p_after = True
            self._h = None
        elif tag == "a" and self._a is not None:
            self.links.append(tuple(self._a))
            self._a = None
        elif tag == "p" and self._p is not None:
            if self.first_p is None and self._p.strip():
                self.first_p = self._p.strip()
            if self.p_after is True:
                self.faq_answers.append(self._p.strip())
                self.p_after = None
            self._p = None

    def handle_data(self, d):
        self.text.append(d)
        if self._h:
            self._h[1] += d
        if self._a is not None:
            self._a[1] += d
        if self._p is not None:
            self._p += d


def words_of(s):
    return re.findall(r"[a-z0-9]+", s.lower())


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
    r = lambda lvl, msg: out.append((lvl, msg))

    def rng(name, val, lo, hi, hard=True):
        n = len(val or "")
        r("PASS" if lo <= n <= hi else ("FAIL" if hard else "WARN"), f"{name}: {n} chars (want {lo}-{hi})")

    # Fields
    rng("SEO title", f.get("seo_title"), 50, 60)
    rng("Meta description", f.get("meta_description"), 130, 150)
    rng("H1 / Title", f.get("title"), 45, 65, hard=False)
    rng("Excerpt", f.get("excerpt"), 70, 160, hard=False)
    md = f.get("meta_description") or ""
    if re.search(r"[\"#“”]", md):
        r("FAIL", "Meta description contains quotes or hashtags")
    if "diggerlid" in md.lower():
        r("WARN", "Meta description contains the brand name")
    if md.strip().lower() == (f.get("title") or "").strip().lower():
        r("FAIL", "Meta description copies the title")
    handle = f.get("handle") or ""
    hw = handle.split("-")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", handle) or not 3 <= len(hw) <= 6:
        r("FAIL", f"Handle '{handle}' must be lowercase-hyphenated, 3-6 words")
    if not f.get("author"):
        r("FAIL", "Author missing")
    if not (f.get("featured_image") or {}).get("alt"):
        r("FAIL", "Featured image alt missing")
    pub = f.get("publish_at") or ""
    if not pub:
        r("WARN", "publish_at missing (schedule to match the post)")
    elif not re.search(r"\+1[01]:00$", pub):
        r("WARN", "publish_at offset should be +11:00 (AEDT) or +10:00 (AEST)")

    # Keyword placement
    if not kw:
        r("FAIL", "primary_keyword missing")
    else:
        kws = [w for w in words_of(kw) if w not in STOP]
        first100 = " ".join(words[:100]).lower()
        fi_alt = ((f.get("featured_image") or {}).get("alt") or "").lower()
        checks = {
            "SEO title": kw in (f.get("seo_title") or "").lower(),
            "H1": kw in (f.get("title") or "").lower(),
            "meta description": kw in md.lower(),
            "first 100 words": kw in first100,
            "handle": all(w in hw for w in kws),
            "an image alt": any(kw in (i.get("alt") or "").lower() for i in p.imgs) or kw in fi_alt,
            "an H2": any(kw in t.lower() for h, t in p.headings if h == "h2"),
        }
        for k, ok in checks.items():
            r("PASS" if ok else ("FAIL" if k in ("SEO title", "H1", "first 100 words", "handle") else "WARN"),
              f"Primary keyword in {k}")
        count = low.count(kw)
        density = 100 * count * len(kw.split()) / max(len(words), 1)
        r("PASS" if 0.5 <= density <= 3 else "WARN", f"Keyword density {density:.1f}% ({count} uses)")

    # Structure
    n = len(words)
    r("PASS" if n >= 1500 else "FAIL", f"Word count {n} (min 1500)")
    if p.first_p:
        iw = len(p.first_p.split())
        r("PASS" if 40 <= iw <= 60 else "WARN", f"Intro paragraph {iw} words (want 40-60, answer first)")
    h1s = [t for h, t in p.headings if h == "h1"]
    r("FAIL" if h1s else "PASS", f"H1 tags in body: {len(h1s)} (must be 0, theme prints the H1)")
    levels = [int(h[1]) for h, _ in p.headings]
    skipped = any(b - a > 1 for a, b in zip([1] + levels, levels))
    r("FAIL" if skipped else "PASS", "Heading level skipped" if skipped else "Heading levels do not skip")
    h2 = sum(1 for h, _ in p.headings if h == "h2")
    r("PASS" if 4 <= h2 <= 10 else "WARN", f"H2 sections: {h2}")
    nq = len(p.faq_h3)
    r("PASS" if 5 <= nq <= 7 else "WARN", f"FAQ questions: {nq} (want 5-7)")
    bad = [q for q, a in zip(p.faq_h3, p.faq_answers) if not 40 <= len(a.split()) <= 60]
    if bad:
        r("WARN", f"{len(bad)} FAQ answer(s) outside 40-60 words: {bad[:3]}")
    r("PASS" if 4 <= p.boxes <= 7 else "WARN", f"Styled design boxes: {p.boxes} (want 4-7)")
    if p.scripts:
        r("FAIL", f"{p.scripts} <script> tag(s) in body")

    # Links
    def host(u):
        if u.startswith("/") and not u.startswith("//"):
            return "diggerlid.com"
        return urlparse(u if "//" in u else "https://" + u).netloc.lower()
    internal = [l for l in p.links if host(l[0]) in OWN_HOSTS]
    external = [l for l in p.links if l not in internal and l[0].startswith(("http", "//"))]
    r("PASS" if 5 <= len(internal) <= 10 else "WARN", f"Internal links: {len(internal)} (want 5-10)")
    r("PASS" if 1 <= len(external) <= 3 else "WARN", f"External links: {len(external)} (want 1-3)")
    nt = [l[0] for l in external if l[2] != "_blank"]
    if nt:
        r("WARN", f"External links without target=_blank: {nt}")
    prod = {l[0] for l in internal if "/products/" in l[0]}
    r("PASS" if prod else "FAIL", f"Product pages linked: {len(prod)}")
    gen = [a for _, a, _ in p.links if a.lower().strip(" →>.") in GENERIC_ANCHORS]
    if gen:
        r("FAIL", f"Generic anchor text: {gen}")

    # Images
    pending = html.count("IMAGE NEEDED")
    want = max(2, n // 400)
    have = len(p.imgs) + pending
    r("PASS" if have >= want else "WARN", f"Images: {len(p.imgs)} placed + {pending} pending (want >= {want})")
    if pending:
        r("WARN", f"{pending} IMAGE NEEDED placeholder(s): publishing blocked until filled")
    for i, im in enumerate(p.imgs, 1):
        alt = im.get("alt")
        if alt is None or not (10 <= len(alt) <= 125):
            r("FAIL", f"Image {i} alt missing or not 10-125 chars")
        if not (im.get("width") and im.get("height")):
            r("WARN", f"Image {i} missing width/height")
        if i > 1 and im.get("loading") != "lazy":
            r("WARN", f"Image {i} should be loading=lazy")
    if p.imgs:
        hero = p.imgs[0]
        if hero.get("loading") == "lazy" or hero.get("fetchpriority") != "high":
            r("WARN", "Hero (first) image should be loading=eager fetchpriority=high")
    if "VIDEO EMBED NEEDED" in html:
        r("WARN", "Video embed placeholder remains")

    # Voice and claims (parsed text, so entities like &mdash; are caught)
    blob = text + " " + json.dumps(f, ensure_ascii=False)
    if EM in blob:
        r("FAIL", "Em dash found")
    if re.search(rf"\s{EN}\s", blob):
        r("WARN", "Spaced en dash used as a dash, use a full stop or comma")
    hits = [b for b in BANNED if re.search(rf"\b{re.escape(b)}\b", low)]
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
