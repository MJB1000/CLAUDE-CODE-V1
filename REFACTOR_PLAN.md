# Brand-Agnostic Refactor + Firecrawl Integration — Plan

## Goal
Rebuild the tool so ANY brand/product can be tracked, not just Wipertech wipers.
Input: Claude Code CLI. Output: Vercel dashboard + Google Sheet.

## Phase 1: Core Renames (mechanical)
- `territory_price` → `product_price` across all files (50+ refs)
- `wiper:` KV prefix → `intel:` (brand-neutral, shorter)  
- `WIPER_INTEL_SECRET` → `API_SECRET` in env vars
- `extract_territory_price()` → `extract_product_price()`

## Phase 2: Brand-Aware Architecture
- Scraper reads brand configs from API (`GET /api/brands`) instead of config.json
- KV keys become `intel:latest`, `intel:history:{date}` (shared namespace)
- Each brand's data stored under `brands:{id}` with its own price history
- Ingest accepts `brand_id` to tag which brand the scrape belongs to

## Phase 3: Firecrawl Integration
- Replace `fetch_url()` HTTP fetcher with Firecrawl `/v2/scrape`
- Replace Playwright browser rendering with Firecrawl (handles JS)
- Firecrawl returns markdown → better promo detection input
- Env var: `FIRECRAWL_API_KEY`
- Fallback: if no Firecrawl key, use existing HTTP fetcher

## Phase 4: Dashboard
- Rename `/wiper-intel` → `/dashboard` (brand-neutral route)
- Dashboard loads brand list, user selects which to view
- Price tracker already brand-aware

## Files Changed
- cloud-run-job/scraper.py (biggest change)
- cloud-run-job/agents.py
- cloud-run-job/config.json → becomes default/template
- dashboard/api/*.js (KV prefix + field renames)
- dashboard/wiper-intel.html → dashboard.html
- dashboard/__tests__/*.js
- All Python tests
- vercel.json, Makefile, .env.example, scripts/*
