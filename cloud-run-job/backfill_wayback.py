#!/usr/bin/env python3
"""
Backfill historical data from the Wayback Machine.

Fetches archived snapshots of competitor sites and runs the same promo
detection pipeline, then POSTs each day's results to the ingest endpoint.
This populates the dashboard with historical data for trend analysis.

Usage:
  python backfill_wayback.py                          # Last 90 days
  python backfill_wayback.py --days 30                # Last 30 days
  python backfill_wayback.py --start 2025-01-01 --end 2025-03-01
  python backfill_wayback.py --brand autowipers_au    # Single brand
  python backfill_wayback.py --dry-run                # Don't POST, just print

Environment variables:
  WIPER_INTEL_SECRET  — API key for ingest endpoint
  INGEST_URL          — Full URL of ingest endpoint
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

# Import scraper functions
sys.path.insert(0, os.path.dirname(__file__))
from scraper import (
    BRANDS, AEST, SECRET, INGEST_URL,
    html_to_text, detect_promos, calc_promotion_intensity,
    extract_territory_price, post_json,
)

WAYBACK_CDX_API = "https://web.archive.org/cdx/search/cdx"
WAYBACK_RAW = "https://web.archive.org/web"

USER_AGENT = "WiperIntel-Backfill/1.0 (contact: matthew@wipertech.com.au)"


def get_wayback_snapshots(url, start_date, end_date):
    """Query Wayback Machine CDX API for available snapshots of a URL."""
    params = (
        f"?url={urllib.request.quote(url)}"
        f"&from={start_date.strftime('%Y%m%d')}"
        f"&to={end_date.strftime('%Y%m%d')}"
        f"&output=json"
        f"&fl=timestamp,statuscode,original"
        f"&filter=statuscode:200"
        f"&collapse=timestamp:8"  # One per day
    )
    req_url = WAYBACK_CDX_API + params

    try:
        req = urllib.request.Request(req_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            if len(data) <= 1:
                return []
            # First row is headers: ["timestamp", "statuscode", "original"]
            return [{"timestamp": row[0], "status": row[1], "url": row[2]} for row in data[1:]]
    except Exception as e:
        print(f"  [WARN] CDX query failed for {url}: {e}", file=sys.stderr)
        return []


def fetch_wayback_snapshot(timestamp, url):
    """Fetch a specific Wayback Machine snapshot."""
    wb_url = f"{WAYBACK_RAW}/{timestamp}id_/{url}"
    try:
        req = urllib.request.Request(wb_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        print(f"  [WARN] Failed to fetch wayback {wb_url}: {e}", file=sys.stderr)
        return 0, ""


def process_snapshot(brand, html, date_str):
    """Run promo detection on a wayback snapshot."""
    text = html_to_text(html)
    canary_pass = brand["canary"].lower() in text.lower() if brand.get("canary") else True

    promos = detect_promos(text)
    intensity = calc_promotion_intensity(promos, text)
    is_on_sale = intensity >= 15 and len(promos) > 0

    return {
        "id": brand["id"],
        "name": brand["name"],
        "market": brand["market"],
        "type": brand["type"],
        "url": brand["url"],
        "http_status": 200,
        "canary_pass": canary_pass,
        "is_on_sale": is_on_sale,
        "promotion_intensity": intensity,
        "promos": promos,
        "territory_price": None,
        "source": "wayback",
    }


def main():
    parser = argparse.ArgumentParser(description="Backfill historical data from Wayback Machine")
    parser.add_argument("--days", type=int, default=90, help="Number of days to look back (default: 90)")
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--brand", type=str, help="Only backfill a specific brand ID")
    parser.add_argument("--dry-run", action="store_true", help="Don't POST to ingest, just print results")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between Wayback requests (seconds)")
    args = parser.parse_args()

    now = datetime.now(AEST)
    if args.start and args.end:
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
        end_date = datetime.strptime(args.end, "%Y-%m-%d")
    else:
        end_date = now
        start_date = now - timedelta(days=args.days)

    brands = BRANDS
    if args.brand:
        brands = [b for b in BRANDS if b["id"] == args.brand]
        if not brands:
            print(f"ERROR: Brand '{args.brand}' not found. Available:", file=sys.stderr)
            for b in BRANDS:
                print(f"  {b['id']}", file=sys.stderr)
            sys.exit(1)

    print("╔══════════════════════════════════════════════════╗")
    print("║  Wiper Intel — Wayback Machine Backfill         ║")
    print("╚══════════════════════════════════════════════════╝")
    print()
    print(f"  Period:  {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"  Brands:  {len(brands)}")
    print(f"  Mode:    {'DRY RUN' if args.dry_run else 'LIVE (posting to ingest)'}")
    print(f"  Ingest:  {INGEST_URL}")
    print()

    # Step 1: Query CDX for all available snapshots
    print("Step 1: Querying Wayback Machine for available snapshots...")
    brand_snapshots = {}
    for brand in brands:
        snapshots = get_wayback_snapshots(brand["url"], start_date, end_date)
        brand_snapshots[brand["id"]] = snapshots
        print(f"  {brand['name']}: {len(snapshots)} snapshots")
        time.sleep(0.5)

    # Step 2: Group by date
    date_sites = {}  # date_str -> list of site dicts
    total_snapshots = sum(len(v) for v in brand_snapshots.values())
    print(f"\nStep 2: Fetching and processing {total_snapshots} snapshots...")

    processed = 0
    for brand in brands:
        snapshots = brand_snapshots.get(brand["id"], [])
        for snap in snapshots:
            ts = snap["timestamp"]
            date_str = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"

            print(f"  [{processed + 1}/{total_snapshots}] {brand['name']} @ {date_str}...", end=" ")
            status, html = fetch_wayback_snapshot(ts, brand["url"])

            if not html:
                print("SKIP (no content)")
                processed += 1
                continue

            site = process_snapshot(brand, html, date_str)
            print(f"intensity={site['promotion_intensity']}, on_sale={site['is_on_sale']}")

            if date_str not in date_sites:
                date_sites[date_str] = []
            date_sites[date_str].append(site)

            processed += 1
            time.sleep(args.delay)

    # Step 3: POST each date's data to ingest
    dates_sorted = sorted(date_sites.keys())
    print(f"\nStep 3: Posting {len(dates_sorted)} days of data to ingest...")

    success = 0
    failed = 0
    for date_str in dates_sorted:
        sites = date_sites[date_str]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        payload = {
            "date": date_str,
            "day_of_week": dt.weekday(),
            "is_weekend": dt.weekday() >= 5,
            "sites": sites,
        }

        if args.dry_run:
            print(f"  [DRY RUN] {date_str}: {len(sites)} brands, "
                  f"avg_intensity={sum(s['promotion_intensity'] for s in sites) // max(len(sites), 1)}")
            success += 1
        else:
            status, resp = post_json(INGEST_URL, payload, SECRET)
            if status == 200 and resp.get("ok"):
                print(f"  {date_str}: OK — {resp.get('brands_processed', 0)} brands, "
                      f"{resp.get('new_alerts', 0)} alerts")
                success += 1
            else:
                print(f"  {date_str}: FAILED (HTTP {status})", file=sys.stderr)
                failed += 1
            time.sleep(0.5)

    # Summary
    print()
    print("═" * 50)
    print(f"  Backfill complete!")
    print(f"  Days processed:  {success}")
    print(f"  Days failed:     {failed}")
    print(f"  Total snapshots: {processed}")
    print("═" * 50)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
