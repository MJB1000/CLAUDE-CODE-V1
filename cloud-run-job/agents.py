#!/usr/bin/env python3
"""
Sub-agents for competitive intelligence pipeline.

Agent 1 — Researcher: Fetches competitor sites, extracts raw data
  (promos, prices, HTML snapshots). Pure data gathering, no interpretation.

Agent 2 — Analyst: Takes researcher output + target brand context,
  produces strategic summaries and competitive position assessments.

Both agents use Claude API when ANTHROPIC_API_KEY is set.
Falls back to rule-based logic when API key is not available.
"""

import json
import os
import sys
import time as _time
import urllib.request
from scraper import (
    html_to_text, detect_promos, calc_promotion_intensity,
    extract_territory_price, fetch_url, upload_snapshot,
)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", os.path.join(os.path.dirname(__file__) or ".", "output", "screenshots"))

# Playwright availability — lazy import
_playwright_available = None

def is_playwright_available():
    global _playwright_available
    if _playwright_available is None:
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401
            _playwright_available = True
        except ImportError:
            _playwright_available = False
    return _playwright_available


def fetch_with_browser(url, screenshot_path=None, timeout_ms=30000):
    """
    Fetch a URL using Playwright headless Chromium.
    Returns (http_status, rendered_html, screenshot_bytes_or_None).
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        try:
            response = page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            status = response.status if response else 0

            # Wait a beat for late-loading JS content
            page.wait_for_timeout(2000)

            # Get fully rendered HTML
            html = page.content()

            # Screenshot (best-effort, don't fail the whole fetch)
            screenshot = None
            if screenshot_path:
                try:
                    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                    screenshot = page.screenshot(full_page=True, path=screenshot_path, timeout=10000)
                except Exception:
                    pass  # Screenshot is optional — don't fail the scrape

            return status, html, screenshot

        except Exception as e:
            print(f"    [BROWSER] Error fetching {url}: {e}", file=sys.stderr)
            return 0, "", None
        finally:
            context.close()
            browser.close()


def call_claude(system_prompt, user_prompt, max_tokens=500):
    """Call Claude API. Returns response text or empty string on failure."""
    if not ANTHROPIC_API_KEY:
        return ""

    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", ANTHROPIC_API_KEY)
    req.add_header("anthropic-version", "2023-06-01")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get("content", [{}])[0].get("text", "")
    except Exception as e:
        print(f"  [AGENT] Claude API error: {e}", file=sys.stderr)
        return ""


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 1: RESEARCHER
# Pure data gathering — no interpretation, no strategy
# ═══════════════════════════════════════════════════════════════════════════════

class ResearcherAgent:
    """Fetches and extracts raw competitive data from competitor websites."""

    def __init__(self, config):
        self.config = config
        self.target = config["target_brand"]

    def research_competitor(self, competitor, date_str):
        """
        Fetch a competitor's site and extract all available data.
        Uses Playwright for renderer:"browser" sites, urllib for renderer:"http".
        Returns a raw data dict — no interpretation applied.
        """
        renderer = competitor.get("renderer", "http")
        use_browser = renderer == "browser" and is_playwright_available()

        method_label = "BROWSER" if use_browser else "HTTP"
        print(f"  [RESEARCHER/{method_label}] Scraping {competitor['name']} ({competitor.get('market', 'AU')})...")

        # ── Fetch page ──────────────────────────────────────────────────────
        t0 = _time.monotonic()
        screenshot_path = None
        if use_browser:
            screenshot_path = os.path.join(
                SCREENSHOT_DIR, date_str, f"{competitor['id']}.png"
            )
            status, html, _screenshot = fetch_with_browser(
                competitor["url"], screenshot_path=screenshot_path
            )
        else:
            status, html = fetch_url(competitor["url"])
        fetch_duration_ms = round((_time.monotonic() - t0) * 1000)

        if not html:
            return self._error_result(competitor, status, fetch_duration_ms)

        text = html_to_text(html)

        # Canary check
        canary = competitor.get("canary", "")
        canary_pass = canary.lower() in text.lower() if canary else True

        # Extract promos (rule-based)
        promos = detect_promos(text)
        intensity = calc_promotion_intensity(promos, text)
        is_on_sale = intensity >= 15 and len(promos) > 0

        # ── Product-specific price ──────────────────────────────────────────
        product_price = None
        product_url = competitor.get("product_url")
        if product_url:
            if use_browser:
                p_status, p_html, _ = fetch_with_browser(product_url)
            else:
                p_status, p_html = fetch_url(product_url)
            if p_html:
                price = extract_territory_price(p_html)
                if price:
                    product_price = {
                        "price": price,
                        "url": product_url,
                        "http_status": p_status,
                    }

        # AI-enhanced promo extraction (if API key available)
        ai_raw_extract = ""
        if ANTHROPIC_API_KEY and promos:
            ai_raw_extract = call_claude(
                system_prompt=(
                    "You are a data extraction agent. Extract ONLY factual information "
                    "from the competitor webpage text. Do NOT interpret or strategize. "
                    "List: discount percentages, promo codes, sale dates, product names, prices."
                ),
                user_prompt=(
                    f"Competitor: {competitor['name']}\n"
                    f"Category: {self.target.get('product_category', 'products')}\n\n"
                    f"Page text (first 2000 chars):\n{text[:2000]}\n\n"
                    "Extract all promotional facts as bullet points:"
                ),
                max_tokens=300,
            )

        # Upload snapshot
        upload_snapshot(competitor["id"], date_str, html)

        result = {
            "id": competitor["id"],
            "name": competitor["name"],
            "market": competitor.get("market", "AU"),
            "type": competitor.get("type", ""),
            "url": competitor["url"],
            "http_status": status,
            "canary_pass": canary_pass,
            "is_on_sale": is_on_sale,
            "promotion_intensity": intensity,
            "promos": promos,
            "territory_price": product_price,
            "raw_text_length": len(text),
            "ai_raw_extract": ai_raw_extract,
            "renderer": method_label.lower(),
            "fetch_duration_ms": fetch_duration_ms,
            "screenshot": screenshot_path if screenshot_path and os.path.exists(screenshot_path) else None,
        }

        print(f"    → intensity={intensity}, on_sale={is_on_sale}, promos={len(promos)}, renderer={method_label}, {fetch_duration_ms}ms")
        return result

    def _error_result(self, competitor, status, fetch_duration_ms=0):
        return {
            "id": competitor["id"],
            "name": competitor["name"],
            "market": competitor.get("market", "AU"),
            "type": competitor.get("type", ""),
            "url": competitor["url"],
            "http_status": status,
            "is_on_sale": False,
            "promotion_intensity": 0,
            "promos": [],
            "fetch_duration_ms": fetch_duration_ms,
            "error": f"Failed to fetch (HTTP {status})",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 2: ANALYST
# Interprets researcher data in context of the target brand
# ═══════════════════════════════════════════════════════════════════════════════

class AnalystAgent:
    """Analyzes competitor data relative to the target brand's position."""

    def __init__(self, config):
        self.config = config
        self.target = config["target_brand"]

    def analyze_landscape(self, sites, date_str):
        """
        Analyze the full competitive landscape for the target brand.
        Takes all researcher outputs and produces strategic summaries.
        """
        print(f"  [ANALYST] Analyzing {len(sites)} competitors for {self.target['name']}...")

        on_sale = [s for s in sites if s.get("is_on_sale")]
        priced = [s for s in sites if s.get("territory_price")]
        avg_intensity = (
            sum(s.get("promotion_intensity", 0) for s in sites) / len(sites)
            if sites else 0
        )

        # Per-site summaries (AI or rule-based)
        for site in sites:
            site["claude_summary"] = self._summarize_site(site)

        # Overall landscape analysis
        landscape_summary = self._analyze_overall(sites, on_sale, priced, avg_intensity)

        return {
            "sites": sites,
            "landscape_summary": landscape_summary,
            "market_stats": {
                "total_competitors": len(sites),
                "on_sale_count": len(on_sale),
                "avg_intensity": round(avg_intensity),
                "price_leader": priced[0]["name"] if priced else None,
                "lowest_price": min(s["territory_price"]["price"] for s in priced) if priced else None,
            },
        }

    def _summarize_site(self, site):
        """Generate a one-line summary for a single competitor."""
        if not site.get("is_on_sale"):
            return ""

        promo = (site.get("promos") or [{}])[0]
        raw_text = promo.get("raw_text", "")

        if ANTHROPIC_API_KEY and raw_text:
            return call_claude(
                system_prompt=(
                    f"You are a competitive analyst for {self.target['name']}, "
                    f"a {self.target.get('product_category', '')} company in {self.target.get('market', 'AU')}. "
                    "Summarize this competitor's promotion in ONE line (max 80 chars). "
                    "Focus on: what discount, what's included, urgency level, threat to our brand."
                ),
                user_prompt=(
                    f"Competitor: {site['name']} ({site.get('market', 'AU')})\n"
                    f"Promo text: {raw_text[:300]}\n"
                    f"Intensity: {site.get('promotion_intensity', 0)}/100\n"
                    f"AI extract: {site.get('ai_raw_extract', '')[:200]}\n\n"
                    "One-line competitive summary:"
                ),
                max_tokens=100,
            ).strip()

        # Fallback: rule-based summary
        parts = []
        if promo.get("discount_pct"):
            parts.append(f"{promo['discount_pct']}% off")
        if promo.get("promo_code"):
            parts.append(f"code {promo['promo_code']}")
        if promo.get("dollar_off"):
            parts.append(f"save ${promo['dollar_off']:.0f}")
        return " — ".join(parts) if parts else raw_text[:60]

    def _analyze_overall(self, sites, on_sale, priced, avg_intensity):
        """Generate overall competitive landscape analysis."""
        if not ANTHROPIC_API_KEY:
            return self._rule_based_analysis(sites, on_sale, priced, avg_intensity)

        site_summaries = "\n".join(
            f"- {s['name']} [{s.get('market','AU')}]: "
            f"{'ON SALE' if s.get('is_on_sale') else 'no sale'}, "
            f"intensity={s.get('promotion_intensity',0)}, "
            f"{'price=$'+str(s['territory_price']['price']) if s.get('territory_price') else 'no price'}"
            f"{', ' + s.get('claude_summary','') if s.get('claude_summary') else ''}"
            for s in sites
        )

        return call_claude(
            system_prompt=(
                f"You are the competitive intelligence analyst for {self.target['name']}, "
                f"a {self.target.get('product_category', '')} company based in {self.target.get('market', 'AU')}. "
                "Provide a brief (3-4 sentence) strategic assessment of today's competitive landscape. "
                "Focus on: threat level, pricing position, recommended actions."
            ),
            user_prompt=(
                f"Date: {sites[0].get('date', 'today') if sites else 'today'}\n"
                f"Competitors tracked: {len(sites)}\n"
                f"Currently on sale: {len(on_sale)} of {len(sites)}\n"
                f"Average promotion intensity: {avg_intensity:.0f}/100\n\n"
                f"Individual competitor status:\n{site_summaries}\n\n"
                "Strategic assessment:"
            ),
            max_tokens=300,
        ).strip()

    def _rule_based_analysis(self, sites, on_sale, priced, avg_intensity):
        """Fallback analysis when Claude API is not available."""
        parts = []
        if len(on_sale) == 0:
            parts.append("No competitors currently running sales — low competitive pressure.")
        elif len(on_sale) >= len(sites) * 0.5:
            parts.append(f"High competitive pressure: {len(on_sale)} of {len(sites)} competitors on sale.")
        else:
            parts.append(f"Moderate activity: {len(on_sale)} of {len(sites)} competitors on sale.")

        if avg_intensity >= 50:
            parts.append("Average promotion intensity is high — consider competitive response.")
        elif avg_intensity >= 25:
            parts.append("Moderate promotion intensity across the market.")

        if priced:
            lowest = min(s["territory_price"]["price"] for s in priced)
            leader = next(s["name"] for s in priced if s["territory_price"]["price"] == lowest)
            parts.append(f"Price leader: {leader} at ${lowest:.2f}.")

        return " ".join(parts)
