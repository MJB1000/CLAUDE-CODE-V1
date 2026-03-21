#!/usr/bin/env python3
"""
Wiper Intel Scraper — Cloud Run Job
Scrapes competitor wiper blade sites (AU + NZ), detects promotions,
and POSTs structured data to the Vercel ingest endpoint.

Environment variables:
  WIPER_INTEL_SECRET   — API key for the ingest endpoint
  INGEST_URL           — Full URL of the ingest endpoint
  GCS_BUCKET           — (optional) GCS bucket for HTML snapshots
  ANTHROPIC_API_KEY    — (optional) Claude API key for AI summaries
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser

# ── Config ──────────────────────────────────────────────────────────────────────

INGEST_URL = os.environ.get("INGEST_URL", "https://wt-dashboards.vercel.app/api/ingest")
SECRET = os.environ.get("WIPER_INTEL_SECRET", "changeme")
GCS_BUCKET = os.environ.get("GCS_BUCKET", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

AEST = timezone(timedelta(hours=10))
USER_AGENT = "WiperIntel/2.0 (competitive-intel; contact: matthew@wipertech.com.au)"

# ── Brand definitions ───────────────────────────────────────────────────────────

BRANDS = [
    # AU brands
    {
        "id": "autowipers_au", "name": "AutoWipers AU", "market": "AU",
        "type": "specialist", "url": "https://www.autowipers.com.au/",
        "territory_url": "https://www.autowipers.com.au/ford-territory-wiper-blades",
        "canary": "autowipers",
    },
    {
        "id": "wiperblades_au", "name": "WiperBlades.com.au", "market": "AU",
        "type": "specialist", "url": "https://www.wiperblades.com.au/",
        "territory_url": "https://www.wiperblades.com.au/ford-territory",
        "canary": "wiper",
    },
    {
        "id": "repco_au", "name": "Repco", "market": "AU",
        "type": "retailer", "url": "https://www.repco.com.au/",
        "territory_url": None,
        "canary": "repco",
    },
    {
        "id": "supercheap_au", "name": "Supercheap Auto", "market": "AU",
        "type": "retailer", "url": "https://www.supercheapauto.com.au/",
        "territory_url": None,
        "canary": "supercheap",
    },
    {
        "id": "bosch_au", "name": "Bosch AU", "market": "AU",
        "type": "oem", "url": "https://www.boschwiperblades.com.au/",
        "territory_url": None,
        "canary": "bosch",
    },
    # NZ brands
    {
        "id": "wiperblades_nz", "name": "WiperBlades NZ", "market": "NZ",
        "type": "specialist", "url": "https://www.wiperblades.co.nz/",
        "territory_url": "https://www.wiperblades.co.nz/ford-territory",
        "canary": "wiper",
    },
    {
        "id": "repco_nz", "name": "Repco NZ", "market": "NZ",
        "type": "retailer", "url": "https://www.repco.co.nz/",
        "territory_url": None,
        "canary": "repco",
    },
]


# ── HTML text extractor ─────────────────────────────────────────────────────────

class HTMLTextExtractor(HTMLParser):
    """Simple HTML-to-text extractor."""
    def __init__(self):
        super().__init__()
        self._text = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self):
        return " ".join(self._text)


def html_to_text(html):
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()


# ── HTTP helpers ────────────────────────────────────────────────────────────────

def fetch_url(url, timeout=30):
    """Fetch a URL with retries and return (status_code, html_text)."""
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.status, raw.decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  [ERROR] Failed to fetch {url}: {e}", file=sys.stderr)
                return 0, ""
    return 0, ""


def post_json(url, data, api_key):
    """POST JSON to a URL."""
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", api_key)

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, json.loads(resp.read().decode())
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  [ERROR] Failed to POST to {url}: {e}", file=sys.stderr)
                return 0, {"error": str(e)}
    return 0, {}


# ── Promo detection ─────────────────────────────────────────────────────────────

# Patterns that indicate a sale or promotion
SALE_PATTERNS = [
    r"(\d{1,3})%\s*off",
    r"save\s*\$?(\d+)",
    r"sale\b",
    r"clearance",
    r"discount",
    r"special\s*offer",
    r"limited\s*time",
    r"free\s*shipping",
    r"buy\s*one\s*get\s*one",
    r"bogo",
    r"coupon",
    r"promo\s*code",
    r"use\s*code\s*(\w+)",
]

PROMO_CODE_PATTERN = re.compile(
    r"(?:use\s+code|promo\s*code|coupon\s*code|code|voucher)[:\s]+([A-Z0-9]{3,20})",
    re.IGNORECASE,
)

DISCOUNT_PCT_PATTERN = re.compile(r"(\d{1,3})%\s*off", re.IGNORECASE)
DOLLAR_OFF_PATTERN = re.compile(r"save\s*\$(\d+(?:\.\d{2})?)", re.IGNORECASE)

PRICE_PATTERNS = [
    re.compile(r"\$(\d+(?:\.\d{2})?)", re.IGNORECASE),
]


def detect_promos(text):
    """Detect promotions in page text. Returns list of promo dicts."""
    promos = []
    text_lower = text.lower()

    for pattern_str in SALE_PATTERNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        for match in pattern.finditer(text):
            start = max(0, match.start() - 80)
            end = min(len(text), match.end() + 80)
            context = text[start:end].strip()

            promo = {"raw_text": context}

            # Extract promo code
            code_match = PROMO_CODE_PATTERN.search(context)
            if code_match:
                promo["promo_code"] = code_match.group(1).upper()

            # Extract discount percentage
            pct_match = DISCOUNT_PCT_PATTERN.search(context)
            if pct_match:
                promo["discount_pct"] = int(pct_match.group(1))

            # Extract dollar-off
            dollar_match = DOLLAR_OFF_PATTERN.search(context)
            if dollar_match:
                promo["dollar_off"] = float(dollar_match.group(1))

            # Avoid duplicates
            if not any(p.get("raw_text") == promo["raw_text"] for p in promos):
                promos.append(promo)

    return promos[:5]  # Max 5 promos per site


def calc_promotion_intensity(promos, text):
    """Calculate a 0-100 promotion intensity score."""
    if not promos:
        return 0

    score = 0
    text_lower = text.lower()

    # Base: has any promo
    score += 15

    # Has promo code
    if any(p.get("promo_code") for p in promos):
        score += 15

    # Has percentage discount
    max_pct = max((p.get("discount_pct") or 0 for p in promos), default=0)
    if max_pct >= 50:
        score += 25
    elif max_pct >= 30:
        score += 20
    elif max_pct >= 15:
        score += 12
    elif max_pct > 0:
        score += 8

    # Multiple promos
    if len(promos) >= 3:
        score += 10
    elif len(promos) >= 2:
        score += 5

    # Urgency keywords
    urgency = ["limited time", "ends soon", "today only", "last chance", "hurry", "flash sale"]
    if any(u in text_lower for u in urgency):
        score += 10

    # Sale / clearance in prominent positions (first 500 chars)
    first_chunk = text_lower[:500]
    if "sale" in first_chunk or "clearance" in first_chunk:
        score += 10

    # Free shipping
    if "free shipping" in text_lower or "free delivery" in text_lower:
        score += 5

    return min(score, 100)


def extract_territory_price(html_text):
    """Try to extract a product price from a territory-specific page."""
    prices = []
    for pattern in PRICE_PATTERNS:
        for match in pattern.finditer(html_text):
            try:
                p = float(match.group(1))
                if 5 < p < 500:  # Reasonable wiper blade price range
                    prices.append(p)
            except ValueError:
                pass
    if prices:
        return min(prices)  # Usually the sale or lowest price
    return None


# ── GCS snapshot upload ─────────────────────────────────────────────────────────

def upload_snapshot(brand_id, date_str, html):
    """Upload HTML snapshot to GCS if configured."""
    if not GCS_BUCKET:
        return
    try:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        blob = bucket.blob(f"snapshots/{date_str}/{brand_id}.html")
        blob.upload_from_string(html, content_type="text/html")
        print(f"  [GCS] Uploaded snapshot for {brand_id}")
    except Exception as e:
        print(f"  [GCS] Failed to upload {brand_id}: {e}", file=sys.stderr)


# ── Main scraper ────────────────────────────────────────────────────────────────

def scrape_brand(brand, date_str):
    """Scrape a single brand and return a site dict."""
    print(f"  Scraping {brand['name']} ({brand['market']})...")

    status, html = fetch_url(brand["url"])
    if not html:
        return {
            "id": brand["id"], "name": brand["name"], "market": brand["market"],
            "type": brand["type"], "url": brand["url"],
            "http_status": status, "is_on_sale": False,
            "promotion_intensity": 0, "promos": [],
            "error": f"Failed to fetch (HTTP {status})",
        }

    text = html_to_text(html)

    # Canary check — verify we got the real page
    canary_pass = brand["canary"].lower() in text.lower() if brand.get("canary") else True

    # Detect promos
    promos = detect_promos(text)
    intensity = calc_promotion_intensity(promos, text)
    is_on_sale = intensity >= 15 and len(promos) > 0

    # Territory price
    territory_price = None
    if brand.get("territory_url"):
        t_status, t_html = fetch_url(brand["territory_url"])
        if t_html:
            price = extract_territory_price(t_html)
            if price:
                territory_price = {
                    "price": price,
                    "url": brand["territory_url"],
                    "http_status": t_status,
                }

    # Upload snapshot
    upload_snapshot(brand["id"], date_str, html)

    site = {
        "id": brand["id"],
        "name": brand["name"],
        "market": brand["market"],
        "type": brand["type"],
        "url": brand["url"],
        "http_status": status,
        "canary_pass": canary_pass,
        "is_on_sale": is_on_sale,
        "promotion_intensity": intensity,
        "promos": promos,
        "territory_price": territory_price,
    }

    print(f"    → intensity={intensity}, on_sale={is_on_sale}, promos={len(promos)}")
    return site


def main():
    now = datetime.now(AEST)
    date_str = now.strftime("%Y-%m-%d")
    day_of_week = now.weekday()  # 0=Monday
    is_weekend = day_of_week >= 5

    print(f"=== Wiper Intel Scraper — {date_str} (day={day_of_week}, weekend={is_weekend}) ===")
    print(f"Ingest URL: {INGEST_URL}")
    print(f"Brands to scrape: {len(BRANDS)}")
    print()

    sites = []
    for brand in BRANDS:
        try:
            site = scrape_brand(brand, date_str)
            sites.append(site)
        except Exception as e:
            print(f"  [ERROR] {brand['name']}: {e}", file=sys.stderr)
            sites.append({
                "id": brand["id"], "name": brand["name"],
                "market": brand["market"], "type": brand["type"],
                "url": brand["url"], "http_status": 0,
                "is_on_sale": False, "promotion_intensity": 0,
                "promos": [], "error": str(e),
            })
        # Be polite — delay between requests
        time.sleep(2)

    # Build payload
    payload = {
        "date": date_str,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "sites": sites,
    }

    # POST to ingest
    print()
    print(f"Posting {len(sites)} brands to ingest endpoint...")
    status, resp = post_json(INGEST_URL, payload, SECRET)

    if status == 200 and resp.get("ok"):
        print(f"SUCCESS — {resp.get('brands_processed', 0)} brands, {resp.get('new_alerts', 0)} new alerts")
        if resp.get("alerts"):
            for alert in resp["alerts"]:
                print(f"  ALERT: [{alert.get('type')}] {alert.get('brand')} — {alert.get('message')}")
    else:
        print(f"FAILED — HTTP {status}: {json.dumps(resp)}", file=sys.stderr)
        sys.exit(1)

    print()
    print("Done.")


if __name__ == "__main__":
    main()
