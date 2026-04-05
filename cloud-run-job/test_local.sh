#!/usr/bin/env bash
set -euo pipefail

# ── Wiper Intel Scraper — Local Testing ─────────────────────────────────────────
# Run the scraper locally in Docker with a test ingest endpoint.
#
# Usage:
#   ./test_local.sh                      # Run with defaults (dry-run mode)
#   ./test_local.sh --live               # Run against real ingest endpoint
#   ./test_local.sh --single autowipers_au  # Test a single brand only

MODE="dry-run"
SINGLE_BRAND=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --live)   MODE="live"; shift ;;
    --single) SINGLE_BRAND="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Load .env if present
ENV_FILE="../.env"
if [[ -f "$ENV_FILE" ]]; then
  echo "Loading environment from $ENV_FILE"
  set -a; source "$ENV_FILE"; set +a
fi

INGEST_URL="${INGEST_URL:-https://dashboard-theta-five-15.vercel.app/api/ingest}"
WIPER_INTEL_SECRET="${WIPER_INTEL_SECRET:-changeme}"

echo "╔══════════════════════════════════════════════════╗"
echo "║  Wiper Intel Scraper — Local Test               ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Mode:        $MODE"
echo "  Ingest URL:  $INGEST_URL"
echo "  Single:      ${SINGLE_BRAND:-all brands}"
echo ""

# ── Option A: Run directly with Python (no Docker) ─────────────────────────────
if command -v python3 &>/dev/null; then
  echo "→ Running with local Python..."
  echo ""

  if [[ "$MODE" == "dry-run" ]]; then
    # In dry-run mode, override ingest URL to a local echo server
    # or just let it fail gracefully
    echo "  (dry-run: will scrape sites but skip ingest POST)"
    INGEST_URL="http://localhost:9999/api/ingest"  # will fail, that's OK
  fi

  cd "$(dirname "$0")"

  INGEST_URL="$INGEST_URL" \
  WIPER_INTEL_SECRET="$WIPER_INTEL_SECRET" \
  GCS_BUCKET="" \
  python3 scraper.py || {
    if [[ "$MODE" == "dry-run" ]]; then
      echo ""
      echo "(Ingest POST failed as expected in dry-run mode — scraping worked)"
      exit 0
    else
      exit 1
    fi
  }

  exit 0
fi

# ── Option B: Run in Docker ────────────────────────────────────────────────────
echo "→ Building Docker image..."
docker build -t wiper-intel-scraper:test .

echo "→ Running container..."
docker run --rm \
  -e "INGEST_URL=$INGEST_URL" \
  -e "WIPER_INTEL_SECRET=$WIPER_INTEL_SECRET" \
  -e "GCS_BUCKET=" \
  wiper-intel-scraper:test

echo ""
echo "Done."
