#!/usr/bin/env python3
"""Analyse PRO Mat conversion and purchase windows from the extracted order CSVs. Aggregates only."""
import csv, glob, json, statistics as st, sys
from collections import Counter, defaultdict
from datetime import datetime, date

src = sys.argv[1]
rows, seen = [], set()
for f in sorted(glob.glob(src + "/*.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if r["order"] in seen or float(r["total"] or 0) == 0:
            continue
        seen.add(r["order"])
        rows.append(r)

def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None

SALES = {  # sale windows (AEST dates, inclusive)
    "EOFY": (date(2026, 6, 15), date(2026, 6, 30)),
    "Fathers Day": (date(2026, 8, 23), date(2026, 9, 7)),
}
LAUNCH = ("PRO Mat Plus launch", date(2026, 8, 1), date(2026, 8, 19))

def period(d):
    for k, (a, b) in SALES.items():
        if a <= d <= b:
            return k
    if LAUNCH[1] <= d <= LAUNCH[2]:
        return LAUNCH[0]
    return "BAU"

def channel(r):
    s = (r["first_source"] or "").lower(); t = (r["first_source_type"] or "").lower()
    us = (r["first_utm_source"] or "").lower(); um = (r["first_utm_medium"] or "").lower()
    if us in ("facebook", "fb", "ig", "instagram", "meta") or "facebook" in s or "instagram" in s:
        return "Meta paid" if um in ("paid", "cpc", "paid_social", "ppc") else "Meta organic/other"
    if us == "klaviyo" or "klaviyo" in s or um == "email" or t == "email":
        return "Email (Klaviyo)"
    if "google" in s or us == "google":
        return "Google paid" if (t in ("sem", "paid") or um in ("cpc", "ppc", "paid")) else "Google organic"
    if t == "direct" or s in ("", "direct") and not us:
        return "Direct / unknown"
    return "Other referral"

for r in rows:
    c = dt(r["created_at"])
    r["_d"] = c.date()
    r["_period"] = period(c.astimezone().date() if False else c.date())
    r["_dtc"] = int(r["days_to_conversion"]) if r["days_to_conversion"] not in ("", "None", None) else None
    r["_mom"] = int(r["moments"]) if r["moments"] not in ("", "None", None) else None
    fo = dt(r.get("customer_first_order_at") or "")
    r["_returning"] = bool(fo and (c - fo).days >= 1)
    r["_gap"] = (c - fo).days if r["_returning"] else None
    og = int(r["pm_og_qty"] or 0); pl = int(r["pm_plus_qty"] or 0)
    r["_variant"] = "OG + PLUS" if og and pl else ("PLUS" if pl else "OG")
    r["_channel"] = channel(r)
    r["_multi"] = int(r["line_count"] or 1) > 1

def pct(xs, p):
    xs = sorted(xs)
    if not xs: return None
    k = (len(xs) - 1) * p; f = int(k); c = min(f + 1, len(xs) - 1)
    return round(xs[f] + (xs[c] - xs[f]) * (k - f), 1)

def summary(sub):
    d = [r["_dtc"] for r in sub if r["_dtc"] is not None]
    m = [r["_mom"] for r in sub if r["_mom"] is not None]
    n = len(d)
    if not n:
        return {"orders": len(sub), "with_journey": 0}
    return {
        "orders": len(sub), "with_journey": n,
        "same_day_%": round(100 * sum(x <= 1 for x in d) / n, 1),
        "within_2d_%": round(100 * sum(x <= 2 for x in d) / n, 1),
        "within_7d_%": round(100 * sum(x <= 7 for x in d) / n, 1),
        "within_14d_%": round(100 * sum(x <= 14 for x in d) / n, 1),
        "within_28d_%": round(100 * sum(x <= 28 for x in d) / n, 1),
        "over_28d_%": round(100 * sum(x > 28 for x in d) / n, 1),
        "median_days": pct(d, .5), "p75_days": pct(d, .75), "p90_days": pct(d, .9), "mean_days": round(st.mean(d), 1),
        "median_visits": pct(m, .5) if m else None, "p90_visits": pct(m, .9) if m else None,
        "single_visit_%": round(100 * sum(x == 1 for x in m) / len(m), 1) if m else None,
    }

out = {"total_orders": len(rows), "date_range": [str(min(r["_d"] for r in rows)), str(max(r["_d"] for r in rows))],
       "journey_missing": sum(r["_dtc"] is None for r in rows), "all": summary(rows)}
for key in ("_returning", "_variant", "_channel", "_period", "_multi"):
    g = defaultdict(list)
    for r in rows:
        g[r[key]].append(r)
    out[key.strip("_")] = {str(k): summary(v) for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))}
new = [r for r in rows if not r["_returning"]]
out["new_customers_only"] = summary(new)
g = defaultdict(list)
for r in new:
    g[r["_channel"]].append(r)
out["new_by_channel"] = {k: summary(v) for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))}
gaps = [r["_gap"] for r in rows if r["_returning"]]
if gaps:
    out["returning_gap_days_first_order_to_pro_mat"] = {
        "n": len(gaps), "median": pct(gaps, .5), "p25": pct(gaps, .25), "p75": pct(gaps, .75), "p90": pct(gaps, .9),
        "within_30d_%": round(100 * sum(x <= 30 for x in gaps) / len(gaps), 1),
        "within_90d_%": round(100 * sum(x <= 90 for x in gaps) / len(gaps), 1),
        "over_365d_%": round(100 * sum(x > 365 for x in gaps) / len(gaps), 1)}
# days-to-conversion histogram (all with journey)
buckets = [(1, 1, "same day"), (2, 2, "day 2"), (3, 7, "3-7"), (8, 14, "8-14"), (15, 28, "15-28"), (29, 60, "29-60"), (61, 9999, "61+")]
d = [r["_dtc"] for r in rows if r["_dtc"] is not None]
out["histogram"] = {lab: sum(a <= x <= b for x in d) for a, b, lab in buckets}
# monthly volume
out["orders_by_month"] = dict(sorted(Counter(r["_d"].strftime("%Y-%m") for r in rows).items()))
print(json.dumps(out, indent=1))
