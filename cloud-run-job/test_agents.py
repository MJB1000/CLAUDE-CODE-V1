#!/usr/bin/env python3
"""Tests for the agent architecture and config loading."""

import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))

from agents import ResearcherAgent, AnalystAgent
from scraper import load_config


class TestConfigLoading(unittest.TestCase):

    def test_loads_config_json(self):
        config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
        assert "target_brand" in config
        assert "competitors" in config
        assert "google_shopping" in config

    def test_config_has_target_brand(self):
        config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
        tb = config["target_brand"]
        assert "name" in tb
        assert "market" in tb
        assert "product_category" in tb

    def test_config_competitors_valid(self):
        config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
        for comp in config["competitors"]:
            assert "id" in comp
            assert "name" in comp
            assert "url" in comp
            assert comp["url"].startswith("https://")

    def test_config_competitor_ids_unique(self):
        config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
        ids = [c["id"] for c in config["competitors"]]
        assert len(ids) == len(set(ids))

    def test_fallback_when_no_config(self):
        config = load_config("/nonexistent/path/config.json")
        assert "competitors" in config
        assert "target_brand" in config


class TestResearcherAgent(unittest.TestCase):

    def setUp(self):
        self.config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
        self.agent = ResearcherAgent(self.config)

    @patch("agents.fetch_url")
    @patch("agents.upload_snapshot")
    def test_research_success(self, mock_upload, mock_fetch):
        mock_fetch.return_value = (200, "<html><body><p>autowipers store open</p></body></html>")
        comp = self.config["competitors"][0]
        result = self.agent.research_competitor(comp, "2025-04-05")

        assert result["id"] == comp["id"]
        assert result["http_status"] == 200
        assert isinstance(result["promos"], list)
        assert isinstance(result["promotion_intensity"], int)

    @patch("agents.fetch_url")
    @patch("agents.upload_snapshot")
    def test_research_with_promo(self, mock_upload, mock_fetch):
        mock_fetch.return_value = (200, "<html><body><h1>autowipers 30% OFF SALE!</h1></body></html>")
        comp = self.config["competitors"][0]
        result = self.agent.research_competitor(comp, "2025-04-05")

        assert result["is_on_sale"] is True
        assert result["promotion_intensity"] >= 15

    @patch("agents.fetch_url")
    @patch("agents.upload_snapshot")
    def test_research_failure(self, mock_upload, mock_fetch):
        mock_fetch.return_value = (503, "")
        comp = self.config["competitors"][0]
        result = self.agent.research_competitor(comp, "2025-04-05")

        assert result["http_status"] == 503
        assert result["is_on_sale"] is False
        assert "error" in result

    @patch("agents.fetch_url")
    @patch("agents.upload_snapshot")
    def test_research_canary_check(self, mock_upload, mock_fetch):
        mock_fetch.return_value = (200, "<html><body><p>Unrelated page</p></body></html>")
        comp = self.config["competitors"][0]
        result = self.agent.research_competitor(comp, "2025-04-05")

        assert result["canary_pass"] is False


class TestAnalystAgent(unittest.TestCase):

    def setUp(self):
        self.config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
        self.agent = AnalystAgent(self.config)

    def test_analyze_empty(self):
        result = self.agent.analyze_landscape([], "2025-04-05")
        assert "sites" in result
        assert "landscape_summary" in result
        assert "market_stats" in result
        assert result["market_stats"]["total_competitors"] == 0

    def test_analyze_with_sites(self):
        sites = [
            {"id": "a", "name": "Brand A", "market": "AU", "is_on_sale": True,
             "promotion_intensity": 40, "promos": [{"raw_text": "20% off", "discount_pct": 20}],
             "territory_price": {"price": 29.95}},
            {"id": "b", "name": "Brand B", "market": "AU", "is_on_sale": False,
             "promotion_intensity": 0, "promos": [],
             "territory_price": {"price": 39.95}},
        ]
        result = self.agent.analyze_landscape(sites, "2025-04-05")

        assert result["market_stats"]["total_competitors"] == 2
        assert result["market_stats"]["on_sale_count"] == 1
        assert result["market_stats"]["lowest_price"] == 29.95
        assert result["market_stats"]["price_leader"] == "Brand A"

    def test_rule_based_summary_no_sales(self):
        sites = [
            {"id": "a", "name": "Brand A", "is_on_sale": False, "promotion_intensity": 0, "promos": []},
        ]
        result = self.agent.analyze_landscape(sites, "2025-04-05")
        assert "low competitive pressure" in result["landscape_summary"].lower() or \
               "no competitors" in result["landscape_summary"].lower()

    def test_rule_based_summary_high_pressure(self):
        sites = [
            {"id": "a", "name": "A", "is_on_sale": True, "promotion_intensity": 60, "promos": [{"raw_text": "sale"}]},
            {"id": "b", "name": "B", "is_on_sale": True, "promotion_intensity": 55, "promos": [{"raw_text": "sale"}]},
        ]
        result = self.agent.analyze_landscape(sites, "2025-04-05")
        assert "high" in result["landscape_summary"].lower() or "2 of 2" in result["landscape_summary"]

    def test_site_summary_with_promo(self):
        site = {
            "id": "a", "name": "A", "is_on_sale": True,
            "promotion_intensity": 40,
            "promos": [{"raw_text": "25% off everything", "discount_pct": 25, "promo_code": "SAVE25"}],
        }
        summary = self.agent._summarize_site(site)
        assert "25%" in summary or "SAVE25" in summary

    def test_site_summary_no_sale(self):
        site = {"id": "a", "name": "A", "is_on_sale": False, "promos": []}
        summary = self.agent._summarize_site(site)
        assert summary == ""


class TestConfigSchema(unittest.TestCase):
    """Validate the config.json schema is complete and correct."""

    def test_config_json_is_valid_json(self):
        path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(path) as f:
            config = json.load(f)
        assert isinstance(config, dict)

    def test_required_top_level_keys(self):
        path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(path) as f:
            config = json.load(f)
        for key in ["project", "target_brand", "competitors", "markets", "google_shopping", "dashboard", "alerts"]:
            assert key in config, f"Missing top-level key: {key}"

    def test_dashboard_config(self):
        path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(path) as f:
            config = json.load(f)
        dash = config["dashboard"]
        assert "title" in dash
        assert "logo_text" in dash
        assert "accent_color" in dash

    def test_markets_match_competitors(self):
        path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(path) as f:
            config = json.load(f)
        markets = set(config["markets"])
        comp_markets = set(c.get("market", "AU") for c in config["competitors"])
        assert comp_markets.issubset(markets), f"Competitors use markets {comp_markets} but only {markets} defined"


if __name__ == "__main__":
    unittest.main()
