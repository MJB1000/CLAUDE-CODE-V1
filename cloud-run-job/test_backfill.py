#!/usr/bin/env python3
"""
Tests for the Wayback Machine backfill script.
Run: pytest test_backfill.py -v
"""

import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from backfill_wayback import (
    get_wayback_snapshots,
    fetch_wayback_snapshot,
    process_snapshot,
    WAYBACK_CDX_API,
    WAYBACK_RAW,
)
from scraper import BRANDS


# ── Wayback CDX API Tests ────────────────────────────────────────────────────────

class TestGetWaybackSnapshots(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_successful_query(self, mock_urlopen):
        response_data = json.dumps([
            ["timestamp", "statuscode", "original"],
            ["20250101120000", "200", "https://www.autowipers.com.au/"],
            ["20250102120000", "200", "https://www.autowipers.com.au/"],
            ["20250103120000", "200", "https://www.autowipers.com.au/"],
        ]).encode()

        mock_resp = MagicMock()
        mock_resp.read.return_value = response_data
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 31)
        snapshots = get_wayback_snapshots("https://www.autowipers.com.au/", start, end)

        assert len(snapshots) == 3
        assert snapshots[0]["timestamp"] == "20250101120000"
        assert snapshots[0]["status"] == "200"

    @patch("urllib.request.urlopen")
    def test_empty_response(self, mock_urlopen):
        response_data = json.dumps([
            ["timestamp", "statuscode", "original"],
        ]).encode()

        mock_resp = MagicMock()
        mock_resp.read.return_value = response_data
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 31)
        snapshots = get_wayback_snapshots("https://www.autowipers.com.au/", start, end)

        assert len(snapshots) == 0

    @patch("urllib.request.urlopen")
    def test_network_error_returns_empty(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network timeout")

        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 31)
        snapshots = get_wayback_snapshots("https://www.autowipers.com.au/", start, end)

        assert snapshots == []


# ── Wayback Snapshot Fetch Tests ─────────────────────────────────────────────────

class TestFetchWaybackSnapshot(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_successful_fetch(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"<html><body>Archived page</body></html>"
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        status, html = fetch_wayback_snapshot("20250101120000", "https://www.autowipers.com.au/")
        assert status == 200
        assert "Archived page" in html

    @patch("urllib.request.urlopen")
    def test_constructs_correct_url(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b""
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        fetch_wayback_snapshot("20250315120000", "https://example.com/")

        call_args = mock_urlopen.call_args
        req = call_args[0][0]
        assert "20250315120000id_" in req.full_url
        assert "example.com" in req.full_url

    @patch("urllib.request.urlopen")
    def test_http_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://web.archive.org/web/20250101id_/x", 404, "Not Found", {}, None
        )

        status, html = fetch_wayback_snapshot("20250101120000", "https://example.com/")
        assert status == 404
        assert html == ""

    @patch("urllib.request.urlopen")
    def test_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection reset")

        status, html = fetch_wayback_snapshot("20250101120000", "https://example.com/")
        assert status == 0
        assert html == ""


# ── Process Snapshot Tests ───────────────────────────────────────────────────────

class TestProcessSnapshot(unittest.TestCase):

    def test_basic_snapshot_processing(self):
        brand = BRANDS[0]  # autowipers_au
        html = "<html><body><p>Welcome to autowipers, quality wipers.</p></body></html>"
        result = process_snapshot(brand, html, "2025-01-15")

        assert result["id"] == brand["id"]
        assert result["name"] == brand["name"]
        assert result["market"] == brand["market"]
        assert result["source"] == "wayback"
        assert result["http_status"] == 200
        assert isinstance(result["promos"], list)
        assert isinstance(result["promotion_intensity"], int)

    def test_snapshot_with_promo(self):
        brand = BRANDS[0]
        html = "<html><body><h1>autowipers 30% OFF SALE!</h1><p>Limited time offer</p></body></html>"
        result = process_snapshot(brand, html, "2025-01-15")

        assert result["is_on_sale"] is True
        assert result["promotion_intensity"] >= 15
        assert len(result["promos"]) >= 1

    def test_snapshot_canary_check(self):
        brand = BRANDS[0]  # canary = "autowipers"
        html = "<html><body><p>Some unrelated content</p></body></html>"
        result = process_snapshot(brand, html, "2025-01-15")

        assert result["canary_pass"] is False

    def test_snapshot_canary_pass(self):
        brand = BRANDS[0]
        html = "<html><body><p>Welcome to AutoWipers store</p></body></html>"
        result = process_snapshot(brand, html, "2025-01-15")

        assert result["canary_pass"] is True

    def test_snapshot_territory_price_is_none(self):
        brand = BRANDS[0]
        html = "<html><body><p>autowipers test</p></body></html>"
        result = process_snapshot(brand, html, "2025-01-15")

        # Backfill doesn't fetch territory pages
        assert result["territory_price"] is None

    def test_all_brands_processable(self):
        """Verify process_snapshot works for every brand definition."""
        html = "<html><body><p>Test content {canary}</p></body></html>"
        for brand in BRANDS:
            test_html = html.replace("{canary}", brand.get("canary", ""))
            result = process_snapshot(brand, test_html, "2025-01-15")
            assert result["id"] == brand["id"]
            assert result["source"] == "wayback"


# ── Constants Tests ──────────────────────────────────────────────────────────────

class TestBackfillConstants(unittest.TestCase):

    def test_cdx_api_url(self):
        assert "web.archive.org" in WAYBACK_CDX_API
        assert "cdx" in WAYBACK_CDX_API

    def test_wayback_raw_url(self):
        assert "web.archive.org" in WAYBACK_RAW
        assert "web" in WAYBACK_RAW


if __name__ == "__main__":
    unittest.main()
