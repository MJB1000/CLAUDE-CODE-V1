#!/usr/bin/env bash
set -euo pipefail

# ── Wiper Intel — Production Smoke Test ────────────────────────────────��─────────
# Tests all API endpoints and the dashboard are responding correctly.
#
# Usage:
#   bash scripts/smoke_test.sh                                    # default prod
#   bash scripts/smoke_test.sh https://wt-dashboards.vercel.app   # custom base
#   WIPER_INTEL_SECRET=key bash scripts/smoke_test.sh             # with auth

BASE_URL="${1:-https://dashboard-theta-five-15.vercel.app}"
SECRET="${WIPER_INTEL_SECRET:-}"
PASS=0
FAIL=0
WARN=0

check() {
  local label="$1" url="$2" expected_status="${3:-200}" auth="${4:-}"
  local headers=()
  if [[ -n "$auth" && -n "$SECRET" ]]; then
    headers=(-H "X-API-Key: $SECRET")
  fi

  local status
  status=$(curl -sf -o /dev/null -w "%{http_code}" "${headers[@]}" "$url" 2>/dev/null || echo "000")

  if [[ "$status" == "$expected_status" ]]; then
    printf "  %-35s %s\n" "$label" "OK ($status)"
    PASS=$((PASS + 1))
  elif [[ "$status" == "000" ]]; then
    printf "  %-35s %s\n" "$label" "UNREACHABLE"
    FAIL=$((FAIL + 1))
  else
    printf "  %-35s %s (expected %s)\n" "$label" "FAIL ($status)" "$expected_status"
    FAIL=$((FAIL + 1))
  fi
}

check_content() {
  local label="$1" url="$2" expected_text="$3"
  local body
  body=$(curl -sf "$url" 2>/dev/null || echo "")

  if echo "$body" | grep -qi "$expected_text"; then
    printf "  %-35s %s\n" "$label" "OK (contains '$expected_text')"
    PASS=$((PASS + 1))
  else
    printf "  %-35s %s\n" "$label" "FAIL (missing '$expected_text')"
    FAIL=$((FAIL + 1))
  fi
}

echo "╔══════════════════════════════════════════════════╗"
echo "║  Wiper Intel — Production Smoke Test             ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Base URL:  $BASE_URL"
echo "  Auth key:  ${SECRET:+set}${SECRET:-NOT SET (skipping auth endpoints)}"
echo ""

# ── Public endpoints ───────────────────────��───────────────────────────────────��
echo "Public endpoints:"
check "GET  /api/health"              "$BASE_URL/api/health"
check "GET  /api/data"                "$BASE_URL/api/data"
check "GET  /api/openapi"             "$BASE_URL/api/openapi"
check "GET  /wiper-intel (dashboard)" "$BASE_URL/wiper-intel"

# Health endpoint deep check
echo ""
echo "Health check details:"
health_body=$(curl -sf "$BASE_URL/api/health" 2>/dev/null || echo "{}")
if echo "$health_body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"  Status: {d.get('status','?')}, KV: {d.get('kv','?')}, Brands: {d.get('brands_tracked','?')}, Hours since scrape: {d.get('hours_since_scrape','?')}\")" 2>/dev/null; then
  true
else
  echo "  Could not parse health response"
  WARN=$((WARN + 1))
fi

# ── Dashboard content ────────────────────────────���─────────────────────────────
echo ""
echo "Dashboard content:"
check_content "Dashboard has table"     "$BASE_URL/wiper-intel" "brandsTable"
check_content "Dashboard has auth"      "$BASE_URL/wiper-intel" "authOverlay"
check_content "Dashboard has export"    "$BASE_URL/wiper-intel" "exportCsv"

# ── Security headers ──────────────────────────────────────────────────────────
echo ""
echo "Security headers:"
sec_headers=$(curl -sI "$BASE_URL/wiper-intel" 2>/dev/null || echo "")
for header in "x-content-type-options" "x-frame-options" "referrer-policy"; do
  if echo "$sec_headers" | grep -qi "$header"; then
    printf "  %-35s %s\n" "$header" "OK"
    PASS=$((PASS + 1))
  else
    printf "  %-35s %s\n" "$header" "MISSING"
    FAIL=$((FAIL + 1))
  fi
done

# ── Authenticated endpoints (if key provided) ──────────────────────────────────
if [[ -n "$SECRET" ]]; then
  echo ""
  echo "Authenticated endpoints:"
  check "GET  /api/export?format=json"  "$BASE_URL/api/export?format=json&key=$SECRET"
  check "GET  /api/export?format=csv"   "$BASE_URL/api/export?format=csv&key=$SECRET"
  check "GET  /api/wipertech-own"       "$BASE_URL/api/wipertech-own"
  # POST with auth but no valid body should return 400
  ingest_status=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    -H "X-API-Key: $SECRET" -H "Content-Type: application/json" \
    -d '{}' "$BASE_URL/api/ingest" 2>/dev/null)
  if [[ "$ingest_status" == "400" ]]; then
    printf "  %-35s %s\n" "POST /api/ingest (no body)" "OK ($ingest_status)"
    PASS=$((PASS + 1))
  else
    printf "  %-35s %s (expected 400)\n" "POST /api/ingest (no body)" "FAIL ($ingest_status)"
    FAIL=$((FAIL + 1))
  fi

  # Check rate limit headers
  rl_headers=$(curl -sI -X POST -H "X-API-Key: $SECRET" -H "Content-Type: application/json" \
    -d '{}' "$BASE_URL/api/ingest" 2>/dev/null || echo "")
  if echo "$rl_headers" | grep -qi "x-ratelimit"; then
    printf "  %-35s %s\n" "Rate limit headers" "OK"
    PASS=$((PASS + 1))
  else
    printf "  %-35s %s\n" "Rate limit headers" "NOT PRESENT"
    WARN=$((WARN + 1))
  fi
else
  echo ""
  echo "Skipping authenticated endpoints (set WIPER_INTEL_SECRET to test)"
fi

# ── OpenAPI spec validation ──────────────────────────────────────────────────
echo ""
echo "OpenAPI spec:"
openapi_body=$(curl -sf "$BASE_URL/api/openapi" 2>/dev/null || echo "{}")
paths_count=$(echo "$openapi_body" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('paths',{})))" 2>/dev/null || echo "0")
if [[ "$paths_count" -ge 5 ]]; then
  printf "  %-35s %s\n" "Endpoint count" "OK ($paths_count paths)"
  PASS=$((PASS + 1))
else
  printf "  %-35s %s\n" "Endpoint count" "FAIL ($paths_count paths, expected 5+)"
  FAIL=$((FAIL + 1))
fi

# ── Summary ─────────────────────────────────────────────────────��────────────
echo ""
echo "══════════════════════════════���═════════════════════"
echo "  Results: $PASS passed, $FAIL failed, $WARN warnings"
echo "════════════════════════════════════════════════════"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
