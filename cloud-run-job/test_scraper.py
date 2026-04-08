#!/usr/bin/env python3
"""
Comprehensive tests for the Wiper Intel scraper.
Run: pytest test_scraper.py -v
"""

import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO

# Ensure scraper module is importable
sys.path.insert(0, os.path.dirname(__file__))

from scraper import (
    HTMLTextExtractor,
    html_to_text,
    detect_promos,
    calc_promotion_intensity,
    extract_product_price,
    upload_snapshot,
    scrape_brand,
    scrape_google_shopping,
    fetch_url,
    post_json,
    BRANDS,
    SALE_PATTERNS,
    PROMO_CODE_PATTERN,
    DISCOUNT_PCT_PATTERN,
    DOLLAR_OFF_PATTERN,
    GOOGLE_SHOPPING_QUERIES,
)


# ── HTMLTextExtractor Tests ──────────────────────────────────────────────────────

class TestHTMLTextExtractor(unittest.TestCase):

    def test_basic_html(self):
        html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
        result = html_to_text(html)
        assert "Hello" in result
        assert "World" in result

    def test_strips_script_tags(self):
        html = "<html><body><p>Visible</p><script>var x = 'hidden';</script><p>Also visible</p></body></html>"
        result = html_to_text(html)
        assert "Visible" in result
        assert "Also visible" in result
        assert "hidden" not in result
        assert "var x" not in result

    def test_strips_style_tags(self):
        html = "<body><style>.big{font-size:100px}</style><p>Content here</p></body>"
        result = html_to_text(html)
        assert "Content here" in result
        assert "font-size" not in result

    def test_strips_noscript_tags(self):
        html = "<body><noscript>Enable JavaScript</noscript><p>Main content</p></body>"
        result = html_to_text(html)
        assert "Main content" in result
        assert "Enable JavaScript" not in result

    def test_empty_html(self):
        result = html_to_text("")
        assert result == ""

    def test_plain_text(self):
        result = html_to_text("Just plain text no HTML")
        assert "Just plain text no HTML" in result

    def test_nested_tags(self):
        html = "<div><div><span>Deep</span> <em>nested</em></div></div>"
        result = html_to_text(html)
        assert "Deep" in result
        assert "nested" in result

    def test_multiple_script_blocks(self):
        html = "<script>a()</script><p>Between</p><script>b()</script><p>After</p>"
        result = html_to_text(html)
        assert "Between" in result
        assert "After" in result
        assert "a()" not in result
        assert "b()" not in result


# ── Promo Detection Tests ────────────────────────────────────────────────────────

class TestDetectPromos(unittest.TestCase):

    def test_percentage_off(self):
        text = "Get 25% off all wiper blades this weekend"
        promos = detect_promos(text)
        assert len(promos) >= 1
        assert any(p.get("discount_pct") == 25 for p in promos)

    def test_dollar_off(self):
        text = "Save $15 on premium wiper blades today"
        promos = detect_promos(text)
        assert len(promos) >= 1
        assert any(p.get("dollar_off") == 15.0 for p in promos)

    def test_promo_code_extraction(self):
        text = "Use code WINTER25 for 20% off all orders"
        promos = detect_promos(text)
        assert len(promos) >= 1
        assert any(p.get("promo_code") == "WINTER25" for p in promos)

    def test_sale_keyword(self):
        text = "Huge sale on all automotive accessories now"
        promos = detect_promos(text)
        assert len(promos) >= 1

    def test_clearance_keyword(self):
        text = "Clearance event — everything must go"
        promos = detect_promos(text)
        assert len(promos) >= 1

    def test_free_shipping(self):
        text = "Free shipping on orders over $50"
        promos = detect_promos(text)
        assert len(promos) >= 1

    def test_bogo(self):
        text = "Buy one get one free on all wiper blades"
        promos = detect_promos(text)
        assert len(promos) >= 1

    def test_no_promos(self):
        text = "Welcome to our wiper blade shop. We sell quality products."
        promos = detect_promos(text)
        assert len(promos) == 0

    def test_max_5_promos(self):
        text = ("sale event! clearance! discount! special offer! "
                "limited time! free shipping! coupon! bogo! "
                "save $10! 50% off! promo code ABC123!")
        promos = detect_promos(text)
        assert len(promos) <= 5

    def test_deduplication(self):
        text = "sale sale sale sale"
        promos = detect_promos(text)
        # Each "sale" match at the same context should deduplicate
        raw_texts = [p["raw_text"] for p in promos]
        assert len(raw_texts) == len(set(raw_texts))

    def test_promo_code_pattern_variants(self):
        texts = [
            "Use code SAVE20 at checkout",
            "Promo code: FALL2025",
            "Coupon code WIPERS10",
        ]
        for text in texts:
            promos = detect_promos(text)
            assert any(p.get("promo_code") for p in promos), f"Failed to extract code from: {text}"

    def test_discount_pct_pattern(self):
        assert DISCOUNT_PCT_PATTERN.search("30% off")
        assert DISCOUNT_PCT_PATTERN.search("5% OFF everything")
        assert not DISCOUNT_PCT_PATTERN.search("100 items")

    def test_dollar_off_pattern(self):
        assert DOLLAR_OFF_PATTERN.search("Save $25")
        assert DOLLAR_OFF_PATTERN.search("save $12.50")
        assert not DOLLAR_OFF_PATTERN.search("Costs $25")


# ── Promotion Intensity Tests ────────────────────────────────────────────────────

class TestCalcPromotionIntensity(unittest.TestCase):

    def test_no_promos_returns_zero(self):
        assert calc_promotion_intensity([], "some text") == 0

    def test_base_score_15(self):
        promos = [{"raw_text": "sale"}]
        score = calc_promotion_intensity(promos, "some text about products")
        assert score >= 15

    def test_promo_code_adds_15(self):
        promos = [{"raw_text": "code SAVE10", "promo_code": "SAVE10"}]
        score = calc_promotion_intensity(promos, "some text")
        assert score >= 30  # base 15 + promo code 15

    def test_high_discount_pct(self):
        promos = [{"raw_text": "60% off", "discount_pct": 60}]
        score = calc_promotion_intensity(promos, "some text")
        assert score >= 40  # base 15 + 25 for 50%+

    def test_moderate_discount_pct(self):
        promos = [{"raw_text": "35% off", "discount_pct": 35}]
        score = calc_promotion_intensity(promos, "some text")
        assert score >= 35  # base 15 + 20 for 30-49%

    def test_low_discount_pct(self):
        promos = [{"raw_text": "10% off", "discount_pct": 10}]
        score = calc_promotion_intensity(promos, "some text")
        assert score >= 23  # base 15 + 8 for <15%

    def test_multiple_promos_adds_points(self):
        promos = [
            {"raw_text": "sale one"},
            {"raw_text": "sale two"},
            {"raw_text": "sale three"},
        ]
        score = calc_promotion_intensity(promos, "some text")
        assert score >= 25  # base 15 + 10 for 3+

    def test_urgency_keywords(self):
        promos = [{"raw_text": "flash sale"}]
        text = "Limited time flash sale ends soon! Last chance to save!"
        score = calc_promotion_intensity(promos, text)
        assert score >= 25  # base 15 + 10 urgency

    def test_sale_in_first_500_chars(self):
        promos = [{"raw_text": "sale"}]
        text = "SALE on now! " + "x" * 1000
        score = calc_promotion_intensity(promos, text)
        assert score >= 25  # base 15 + 10 prominent

    def test_free_shipping(self):
        promos = [{"raw_text": "free shipping"}]
        text = "Free shipping on all orders"
        score = calc_promotion_intensity(promos, text)
        assert score >= 20  # base 15 + 5 shipping

    def test_max_score_capped_at_100(self):
        promos = [
            {"raw_text": "70% off", "discount_pct": 70, "promo_code": "MEGA"},
            {"raw_text": "clearance"},
            {"raw_text": "bogo"},
        ]
        text = "SALE clearance limited time ends soon flash sale free shipping " + "x" * 1000
        score = calc_promotion_intensity(promos, text)
        assert score <= 100

    def test_full_intensity_scenario(self):
        promos = [
            {"raw_text": "Use code MEGA60 for 60% off!", "discount_pct": 60, "promo_code": "MEGA60"},
            {"raw_text": "Free shipping sitewide"},
            {"raw_text": "Flash sale clearance event"},
        ]
        text = "SALE! Flash sale clearance! Use code MEGA60 for 60% off! Free shipping! Limited time! Hurry!"
        score = calc_promotion_intensity(promos, text)
        # base(15) + code(15) + 50%+(25) + 3promos(10) + urgency(10) + prominent(10) + shipping(5) = 90
        assert score >= 80


# ── Territory Price Extraction Tests ─────────────────────────────────────────────

class TestExtractTerritoryPrice(unittest.TestCase):

    def test_basic_price(self):
        html = '<span class="price">$29.95</span>'
        assert extract_product_price(html) == 29.95

    def test_multiple_prices_returns_lowest(self):
        html = '<span>$49.95</span><span>$29.95</span><span>$39.95</span>'
        assert extract_product_price(html) == 29.95

    def test_ignores_prices_outside_range(self):
        html = '$3.00 $29.95 $999.99'
        assert extract_product_price(html) == 29.95

    def test_no_prices(self):
        html = '<p>No prices here</p>'
        assert extract_product_price(html) is None

    def test_prices_at_boundaries(self):
        html = '$5.00 $5.01 $499.99 $500.00'
        result = extract_product_price(html)
        assert result == 5.01  # 5.00 excluded (not >5), 500 excluded (not <500)

    def test_integer_prices(self):
        html = '$25 $30 $45'
        assert extract_product_price(html) == 25.0

    def test_price_in_complex_html(self):
        html = '''
        <div class="product-price">
            <span class="was">$49.95</span>
            <span class="now">$34.95</span>
            <span class="save">Save $15.00!</span>
        </div>
        '''
        assert extract_product_price(html) == 15.0  # lowest valid


# ── Brand Definitions Tests ──────────────────────────────────────────────────────

class TestBrandDefinitions(unittest.TestCase):

    def test_all_brands_have_required_fields(self):
        required = ["id", "name", "market", "type", "url"]
        for brand in BRANDS:
            for field in required:
                assert field in brand, f"Brand {brand.get('id', '?')} missing '{field}'"

    def test_brand_ids_unique(self):
        ids = [b["id"] for b in BRANDS]
        assert len(ids) == len(set(ids)), "Duplicate brand IDs found"

    def test_markets_valid(self):
        for brand in BRANDS:
            assert brand["market"] in ("AU", "NZ"), f"Invalid market for {brand['id']}"

    def test_types_valid(self):
        valid_types = ("specialist", "retailer", "oem")
        for brand in BRANDS:
            assert brand["type"] in valid_types, f"Invalid type for {brand['id']}"

    def test_urls_are_https(self):
        for brand in BRANDS:
            assert brand["url"].startswith("https://"), f"Non-HTTPS URL for {brand['id']}"
            if brand.get("territory_url"):
                assert brand["territory_url"].startswith("https://"), \
                    f"Non-HTTPS territory URL for {brand['id']}"

    def test_au_brands_present(self):
        au_brands = [b for b in BRANDS if b["market"] == "AU"]
        assert len(au_brands) >= 3

    def test_nz_brands_present(self):
        nz_brands = [b for b in BRANDS if b["market"] == "NZ"]
        assert len(nz_brands) >= 1

    def test_canary_strings_present(self):
        for brand in BRANDS:
            assert "canary" in brand, f"Missing canary for {brand['id']}"
            assert isinstance(brand["canary"], str) and len(brand["canary"]) > 0


# ── Google Shopping Config Tests ─────────────────────────────────────────────────

class TestGoogleShoppingConfig(unittest.TestCase):

    def test_au_config_exists(self):
        assert "AU" in GOOGLE_SHOPPING_QUERIES

    def test_nz_config_exists(self):
        assert "NZ" in GOOGLE_SHOPPING_QUERIES

    def test_configs_have_required_fields(self):
        for market, config in GOOGLE_SHOPPING_QUERIES.items():
            assert "query" in config, f"Missing query for {market}"
            assert "domain" in config, f"Missing domain for {market}"
            assert "currency" in config, f"Missing currency for {market}"

    def test_currencies_valid(self):
        assert GOOGLE_SHOPPING_QUERIES["AU"]["currency"] == "AUD"
        assert GOOGLE_SHOPPING_QUERIES["NZ"]["currency"] == "NZD"


# ── Scrape Brand Tests (mocked) ─────────────────────────────────────────────────

class TestScrapeBrand(unittest.TestCase):

    @patch("scraper.upload_snapshot")
    @patch("scraper.fetch_url")
    def test_successful_scrape_no_promos(self, mock_fetch, mock_upload):
        mock_fetch.return_value = (200, "<html><body><p>Welcome to autowipers shop</p></body></html>")
        brand = BRANDS[0]  # autowipers_au
        result = scrape_brand(brand, "2025-03-21")

        assert result["id"] == brand["id"]
        assert result["http_status"] == 200
        assert result["canary_pass"] is True
        assert result["is_on_sale"] is False
        assert result["promotion_intensity"] == 0
        assert result["promos"] == []
        mock_upload.assert_called_once()

    @patch("scraper.upload_snapshot")
    @patch("scraper.fetch_url")
    def test_successful_scrape_with_promo(self, mock_fetch, mock_upload):
        html = "<html><body><h1>autowipers SALE!</h1><p>25% off all wiper blades!</p></body></html>"
        mock_fetch.return_value = (200, html)
        brand = BRANDS[0]
        result = scrape_brand(brand, "2025-03-21")

        assert result["is_on_sale"] is True
        assert result["promotion_intensity"] >= 15
        assert len(result["promos"]) >= 1

    @patch("scraper.upload_snapshot")
    @patch("scraper.fetch_url")
    def test_failed_fetch(self, mock_fetch, mock_upload):
        mock_fetch.return_value = (503, "")
        brand = BRANDS[0]
        result = scrape_brand(brand, "2025-03-21")

        assert result["http_status"] == 503
        assert result["is_on_sale"] is False
        assert "error" in result
        mock_upload.assert_not_called()

    @patch("scraper.upload_snapshot")
    @patch("scraper.fetch_url")
    def test_canary_failure(self, mock_fetch, mock_upload):
        # Page loads but doesn't contain canary text
        mock_fetch.return_value = (200, "<html><body><p>Some totally different site</p></body></html>")
        brand = BRANDS[0]  # canary = "autowipers"
        result = scrape_brand(brand, "2025-03-21")

        assert result["canary_pass"] is False

    @patch("scraper.upload_snapshot")
    @patch("scraper.fetch_url")
    def test_product_price_extraction(self, mock_fetch, mock_upload):
        # First call: main page, Second call: territory page
        mock_fetch.side_effect = [
            (200, "<html><body><p>Welcome to autowipers</p></body></html>"),
            (200, "<html><body><span class='price'>$34.95</span></body></html>"),
        ]
        brand = BRANDS[0]  # has territory_url
        result = scrape_brand(brand, "2025-03-21")

        assert result["product_price"] is not None
        assert result["product_price"]["price"] == 34.95

    @patch("scraper.upload_snapshot")
    @patch("scraper.fetch_url")
    def test_no_territory_url(self, mock_fetch, mock_upload):
        mock_fetch.return_value = (200, "<html><body><p>repco store</p></body></html>")
        brand = BRANDS[2]  # repco_au, territory_url=None
        result = scrape_brand(brand, "2025-03-21")

        assert result["product_price"] is None
        mock_fetch.assert_called_once()  # Only main page, no territory fetch


# ── Google Shopping Scraper Tests (mocked) ───────────────────────────────────────

class TestScrapeGoogleShopping(unittest.TestCase):

    @patch("scraper.fetch_url")
    def test_successful_shopping_scrape(self, mock_fetch):
        html = '''<html><body>
        <div class="product">Bosch Aerotwin $29.95</div>
        <div class="product">Trico Flex $34.50</div>
        <div class="product">SCA Standard $19.99</div>
        </body></html>'''
        mock_fetch.return_value = (200, html)

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        assert result is not None
        assert result["market"] == "AU"
        assert result["listing_count"] >= 1
        assert result["min_price"] is not None
        assert result["max_price"] is not None
        assert result["min_price"] <= result["max_price"]

    @patch("scraper.fetch_url")
    def test_shopping_no_results(self, mock_fetch):
        mock_fetch.return_value = (200, "<html><body><p>No results found</p></body></html>")

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        assert result is not None
        assert result["listing_count"] == 0
        assert result["min_price"] is None

    @patch("scraper.fetch_url")
    def test_shopping_fetch_failure(self, mock_fetch):
        mock_fetch.return_value = (403, "")

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        assert result is None

    @patch("scraper.fetch_url")
    def test_shopping_deduplication(self, mock_fetch):
        # Same price appearing multiple times
        html = '<div>$29.95</div><span>$29.95</span><p>$29.95</p><div>$39.95</div>'
        mock_fetch.return_value = (200, html)

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        # After dedup, should have at most 2 unique prices
        prices = [l["price"] for l in result["listings"]]
        assert len(prices) == len(set(prices))

    @patch("scraper.fetch_url")
    def test_shopping_max_15_listings(self, mock_fetch):
        # Generate 20 unique prices
        price_html = "".join(f'<span>${10 + i}.99</span>' for i in range(20))
        mock_fetch.return_value = (200, f"<html><body>{price_html}</body></html>")

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        assert result["listing_count"] <= 15

    @patch("scraper.fetch_url")
    def test_shopping_price_range_filter(self, mock_fetch):
        html = '<div>$2.00</div><div>$25.00</div><div>$600.00</div>'
        mock_fetch.return_value = (200, html)

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        # Only $25.00 should be in range (5-500 exclusive)
        prices = [l["price"] for l in result["listings"]]
        for p in prices:
            assert 5 < p < 500

    @patch("scraper.fetch_url")
    def test_shopping_sorted_by_price(self, mock_fetch):
        html = '<span>$49.95</span><span>$19.95</span><span>$34.95</span>'
        mock_fetch.return_value = (200, html)

        config = GOOGLE_SHOPPING_QUERIES["AU"]
        result = scrape_google_shopping("AU", config)

        prices = [l["price"] for l in result["listings"]]
        assert prices == sorted(prices)


# ── Upload Snapshot Tests ────────────────────────────────────────────────────────

class TestUploadSnapshot(unittest.TestCase):

    @patch("scraper.GCS_BUCKET", "")
    def test_no_upload_without_bucket(self):
        # Should return silently without error
        upload_snapshot("test_brand", "2025-03-21", "<html>test</html>")

    @patch("scraper.GCS_BUCKET", "my-bucket")
    def test_upload_handles_import_error(self, ):
        # google.cloud.storage may not be installed — should handle gracefully
        upload_snapshot("test_brand", "2025-03-21", "<html>test</html>")
        # No exception raised = pass


# ── HTTP Helper Tests ────────────────────────────────────────────────────────────

class TestFetchUrl(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_successful_fetch(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"<html>Hello</html>"
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        status, html = fetch_url("https://example.com")
        assert status == 200
        assert "Hello" in html

    @patch("urllib.request.urlopen")
    def test_http_error(self, mock_urlopen):
        import urllib.error as ue
        mock_urlopen.side_effect = ue.HTTPError(
            "https://example.com", 404, "Not Found", {}, None
        )
        status, html = fetch_url("https://example.com")
        assert status == 404
        assert html == ""


class TestPostJson(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_successful_post(self, mock_urlopen):
        response_data = json.dumps({"ok": True}).encode()
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = response_data
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        status, data = post_json("https://example.com/api", {"test": True}, "key123")
        assert status == 200
        assert data["ok"] is True


# ── Regex Pattern Tests ──────────────────────────────────────────────────────────

class TestRegexPatterns(unittest.TestCase):

    def test_all_sale_patterns_compile(self):
        import re
        for pattern_str in SALE_PATTERNS:
            try:
                re.compile(pattern_str, re.IGNORECASE)
            except re.error as e:
                self.fail(f"Pattern '{pattern_str}' failed to compile: {e}")

    def test_promo_code_pattern_matches(self):
        cases = [
            ("use code SAVE20", "SAVE20"),
            ("Promo code: WINTER", "WINTER"),
            ("coupon code ABC123", "ABC123"),
            ("code HELLO", "HELLO"),
            ("voucher DEAL50", "DEAL50"),
        ]
        for text, expected in cases:
            match = PROMO_CODE_PATTERN.search(text)
            assert match is not None, f"No match for: {text}"
            assert match.group(1).upper() == expected

    def test_promo_code_pattern_rejects_short_codes(self):
        match = PROMO_CODE_PATTERN.search("code AB")
        assert match is None  # Too short (< 3 chars)


# ── Edge Case Tests ──────────────────────────────────────────────────────────────

class TestEdgeCases(unittest.TestCase):

    def test_detect_promos_with_unicode(self):
        text = "SALE! Save 20% — use code SPRING25 for déals"
        promos = detect_promos(text)
        assert len(promos) >= 1

    def test_detect_promos_with_very_long_text(self):
        text = "sale " + "x" * 100000
        promos = detect_promos(text)
        assert isinstance(promos, list)

    def test_intensity_with_empty_text(self):
        promos = [{"raw_text": "sale"}]
        score = calc_promotion_intensity(promos, "")
        assert score >= 15

    def test_extract_price_with_malformed_html(self):
        html = '<div class="price">$29.95</div><<<<>>>not valid $19.99'
        price = extract_product_price(html)
        assert price == 19.99

    def test_html_to_text_with_entities(self):
        html = "<p>Price &amp; quality &lt; matters &gt;</p>"
        result = html_to_text(html)
        assert "Price" in result


if __name__ == "__main__":
    unittest.main()
