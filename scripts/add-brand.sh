#!/usr/bin/env bash
set -euo pipefail

# ── Wiper Intel — Add Brand (CLI) ────────────────────────────────────────────
# Interactive brand onboarding tool. Run from Claude Code or terminal.
#
# Usage:
#   bash scripts/add-brand.sh                    # interactive mode
#   bash scripts/add-brand.sh --setup-sheets     # create Google Sheet first
#
# Environment:
#   WIPER_INTEL_SECRET   — API key (or will prompt)
#   VERCEL_URL           — base URL (default: https://dashboard-theta-five-15.vercel.app)

VERCEL_URL="${VERCEL_URL:-https://dashboard-theta-five-15.vercel.app}"
SECRET="${WIPER_INTEL_SECRET:-}"

if [[ -z "$SECRET" ]]; then
  read -rp "API key: " SECRET
fi

api() {
  local method="$1" path="$2" data="${3:-}"
  if [[ -n "$data" ]]; then
    curl -s -X "$method" "$VERCEL_URL$path" \
      -H "Content-Type: application/json" \
      -H "X-API-Key: $SECRET" \
      -d "$data"
  else
    curl -s -X "$method" "$VERCEL_URL$path" \
      -H "X-API-Key: $SECRET"
  fi
}

# ── Google Sheets setup ─────────────────────────────────────────────────────
if [[ "${1:-}" == "--setup-sheets" ]]; then
  echo ""
  echo "Setting up Google Sheet..."
  RESULT=$(api POST /api/sheets-setup)
  if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('url',''))" 2>/dev/null | grep -q "docs.google"; then
    URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['url'])")
    echo "  Google Sheet ready: $URL"
  else
    echo "  Result: $RESULT"
  fi
  exit 0
fi

# ── Brand onboarding ────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  Wiper Intel — Add New Brand                     ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Brand details
read -rp "Brand name: " BRAND_NAME
echo "Market options: AU, NZ, US, UK"
read -rp "Market [AU]: " MARKET
MARKET="${MARKET:-AU}"
read -rp "Website URL: " WEBSITE
read -rp "Product category [wiper blades]: " CATEGORY
CATEGORY="${CATEGORY:-wiper blades}"
read -rp "Reference product (for price comparison): " REF_PRODUCT

# Competitors
echo ""
echo "Now let's add competitors to track."
echo "(Enter at least 1. Leave name blank when done.)"
echo ""

COMPETITORS="["
COMP_NUM=0
while true; do
  COMP_NUM=$((COMP_NUM + 1))
  read -rp "Competitor $COMP_NUM name (or blank to finish): " COMP_NAME
  [[ -z "$COMP_NAME" ]] && break

  read -rp "  Website URL: " COMP_URL
  read -rp "  Product page URL (optional): " COMP_PRODUCT_URL
  echo "  Type options: specialist, retailer, oem"
  read -rp "  Type [specialist]: " COMP_TYPE
  COMP_TYPE="${COMP_TYPE:-specialist}"

  [[ "$COMP_NUM" -gt 1 ]] && COMPETITORS="$COMPETITORS,"
  COMPETITORS="$COMPETITORS{\"name\":\"$COMP_NAME\",\"url\":\"$COMP_URL\",\"product_url\":\"$COMP_PRODUCT_URL\",\"type\":\"$COMP_TYPE\"}"
done
COMPETITORS="$COMPETITORS]"

if [[ "$COMP_NUM" -le 1 ]]; then
  echo ""
  echo "ERROR: At least one competitor is required."
  exit 1
fi

# Confirm
echo ""
echo "────────────────────────────────────────────────────"
echo "  Brand:       $BRAND_NAME"
echo "  Market:      $MARKET"
echo "  Website:     $WEBSITE"
echo "  Category:    $CATEGORY"
echo "  Reference:   $REF_PRODUCT"
echo "  Competitors: $((COMP_NUM - 1))"
echo "────────────────────────────────────────────────────"
echo ""
read -rp "Create this brand? [Y/n]: " CONFIRM
CONFIRM="${CONFIRM:-Y}"
if [[ "$CONFIRM" != [Yy]* ]]; then
  echo "Cancelled."
  exit 0
fi

# Submit
PAYLOAD=$(python3 -c "
import json
print(json.dumps({
    'name': '$BRAND_NAME',
    'market': '$MARKET',
    'website': '$WEBSITE',
    'product_category': '$CATEGORY',
    'reference_product': '$REF_PRODUCT',
    'competitors': $COMPETITORS
}))
")

echo ""
echo "Creating brand..."
RESULT=$(api POST /api/brands "$PAYLOAD")

if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('ok') else 1)" 2>/dev/null; then
  BRAND_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['brand']['id'])")
  echo "  Brand created: $BRAND_ID"
  echo ""

  # Ask about periods
  read -rp "Define a sale/BAU period now? [Y/n]: " ADD_PERIOD
  ADD_PERIOD="${ADD_PERIOD:-Y}"

  while [[ "$ADD_PERIOD" == [Yy]* ]]; do
    read -rp "  Period label (e.g. 'Winter Sale 2026'): " PERIOD_LABEL
    echo "  Period type: sale or bau"
    read -rp "  Type [sale]: " PERIOD_TYPE
    PERIOD_TYPE="${PERIOD_TYPE:-sale}"
    read -rp "  Start date (YYYY-MM-DD): " PERIOD_START
    read -rp "  End date (YYYY-MM-DD): " PERIOD_END

    PERIOD_PAYLOAD=$(python3 -c "
import json
print(json.dumps({
    'brand_id': '$BRAND_ID',
    'label': '$PERIOD_LABEL',
    'type': '$PERIOD_TYPE',
    'start_date': '$PERIOD_START',
    'end_date': '$PERIOD_END'
}))
")
    PERIOD_RESULT=$(api POST /api/periods "$PERIOD_PAYLOAD")
    if echo "$PERIOD_RESULT" | python3 -c "import sys,json; exit(0 if json.load(sys.stdin).get('ok') else 1)" 2>/dev/null; then
      echo "  Period created."
    else
      echo "  Error: $PERIOD_RESULT"
    fi
    echo ""
    read -rp "Add another period? [y/N]: " ADD_PERIOD
    ADD_PERIOD="${ADD_PERIOD:-N}"
  done

  echo ""
  echo "════════════════════════════════════════════════════"
  echo "  Brand '$BRAND_NAME' is now being tracked."
  echo ""
  echo "  Dashboard: $VERCEL_URL/price-tracker"
  echo "  Brand ID:  $BRAND_ID"
  echo "════════════════════════════════════════════════════"
else
  echo "  Error: $RESULT"
  exit 1
fi
