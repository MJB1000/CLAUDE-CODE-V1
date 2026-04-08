#!/usr/bin/env python3
"""
Tests for Firecrawl integration and brand-aware scraping.
Run: pytest test_firecrawl.py -v
"""

import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))

from scraper import fetch_with_firecrawl, fetch_url_smart, html_to_text


class TestFirecrawlFetcher(unittest.TestCase):
    """Tests for the Firecrawl API integration."""

    @patch("scraper.urllib.request.urlopen")
    def test_firecrawl_returns_markdown_and_html(self, mock_urlopen):
        """Firecrawl should return (status, markdown, html) tuple."""
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({
            "success": True,
            "data": {
                "markdown": "# Test Page\n\n20% OFF everything",
                "html": "<h1>Test Page</h1><p>20% OFF everything</p>",
                "metadata": {"statusCode": 200},
            }
        }).encode()
        mock_resp.headers = MagicMock()
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        status, markdown, html = fetch_with_firecrawl("https://example.com", "fc-test-key")
        self.assertEqual(status, 200)
        self.assertIn("20% OFF", markdown)
        self.assertIn("20% OFF", html)

    @patch("scraper.urllib.request.urlopen")
    def test_firecrawl_failure_returns_empty(self, mock_urlopen):
        """On API failure, returns (0, '', '')."""
        mock_urlopen.side_effect = Exception("API down")
        status, markdown, html = fetch_with_firecrawl("https://example.com", "fc-test-key")
        self.assertEqual(status, 0)
        self.assertEqual(markdown, "")
        self.assertEqual(html, "")

    @patch("scraper.urllib.request.urlopen")
    def test_firecrawl_non_success_returns_error(self, mock_urlopen):
        """When Firecrawl returns success=false, return 0."""
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({
            "success": False,
            "error": "Blocked by robots.txt",
        }).encode()
        mock_resp.headers = MagicMock()
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        status, markdown, html = fetch_with_firecrawl("https://example.com", "fc-test-key")
        self.assertEqual(status, 0)


class TestSmartFetcher(unittest.TestCase):
    """Tests for fetch_url_smart which picks Firecrawl or HTTP."""

    @patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fc-test-key"})
    @patch("scraper.fetch_with_firecrawl")
    def test_uses_firecrawl_when_key_set(self, mock_fc):
        """Should use Firecrawl when FIRECRAWL_API_KEY is set."""
        mock_fc.return_value = (200, "# Page", "<h1>Page</h1>")
        status, text = fetch_url_smart("https://example.com")
        mock_fc.assert_called_once()
        self.assertEqual(status, 200)
        self.assertIn("Page", text)

    @patch.dict(os.environ, {"FIRECRAWL_API_KEY": ""})
    @patch("scraper.fetch_url")
    def test_falls_back_to_http_without_key(self, mock_http):
        """Should fall back to HTTP fetcher when no Firecrawl key."""
        mock_http.return_value = (200, "<h1>Page</h1>")
        status, text = fetch_url_smart("https://example.com")
        mock_http.assert_called_once()
        self.assertEqual(status, 200)

    @patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fc-test-key"})
    @patch("scraper.fetch_with_firecrawl")
    @patch("scraper.fetch_url")
    def test_falls_back_to_http_on_firecrawl_failure(self, mock_http, mock_fc):
        """If Firecrawl fails, fall back to HTTP."""
        mock_fc.return_value = (0, "", "")
        mock_http.return_value = (200, "<h1>Fallback</h1>")
        status, text = fetch_url_smart("https://example.com")
        self.assertEqual(status, 200)
        self.assertIn("Fallback", text)


if __name__ == "__main__":
    unittest.main()
