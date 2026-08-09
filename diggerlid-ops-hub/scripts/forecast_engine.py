#!/usr/bin/env python3
"""
DiggerLid weekly forecast engine.

The Scorekeeper runs this every Monday:
  1. Update INPUTS below — lock any finished month into ACTUALS, and refresh the
     in-progress month's month-to-date (net revenue, days elapsed) + ad spend.
  2. `python3 forecast_engine.py` → prints a Markdown forecast block.
  3. Save it to data/forecast/YYYY-Www.md and refresh data/FORECAST.md.

Model (EE baseline):  GPAM% = (1 - VCR) - MER ;  GPAM$ = rev * GPAM% ;  Net = GPAM$ - FIXED.
GPAM target = 26%.  MER target <= 25% (sale months <= 28%).

REVENUE BASIS — **ex-GST** (EE model row 8, "Revenue Ex GST"), AUD.
This is the basis the model's own P&L uses (Profit = Revenue Ex GST - Total Expenses), so MER
and VCR are computed on it too. NOTE: the model *displays* MER/VCR divided by GST-INCLUSIVE
revenue, which flatters both by ~9% (e.g. July shows MER 37.9% when the P&L basis is 41.1%).
Always reconcile on ex-GST. Shopify net_sales runs ~4.4% below ex-GST revenue (it excludes
shipping revenue) — bridge factor EXGST_PER_NETSALES below.

MER note: if the in-progress month's ad_spend_mtd is None (Meta not wired), MER falls back
to `assumed_mer` and is flagged. Once Meta is wired, pass real spend and MER becomes actual.
"""

FIXED = 74831
# VCR from 2026 actuals on the ex-GST basis (was 0.46/0.48 — both were optimistic):
#   BAU  months Jan/Feb/Mar/Jul: 47.3 / 44.8 / 47.6 / 47.3  -> ~46.8%
#   Sale months Apr/May/Jun:     50.1 / 50.7 / 50.0         -> ~50.3%
VCR_BAU, VCR_SALE = 0.468, 0.503
GPAM_TARGET = 0.26
EXGST_PER_NETSALES = 1.0437   # ex-GST revenue / Shopify net_sales (Jul: 335,475 / 321,436)

# --- finished months: (net_revenue_exGST, realized_MER_exGST) -----------------
# Source: EE model Accelerate_5, "2026 Monthly Totals" rows 8 (rev ex GST) and 31 (Meta spend).
ACTUALS = {
    'Jan': (241767, 0.1992), 'Feb': (306489, 0.2758), 'Mar': (311480, 0.3216),
    'Apr': (341520, 0.3168), 'May': (416322, 0.2952), 'Jun': (807148, 0.2447),
    # Jul locked: Shopify net_sales $366,852 x 1.0437 = $382,884 ex-GST;
    # realized MER = live Meta $162,325 / 382,884 = 0.424.
    'Jul': (382884, 0.4240),
}

# --- month in progress: refresh weekly ---------------------------------------
# Revenue: Shopify net_sales MTD x EXGST_PER_NETSALES -> ex-GST basis.
# Spend:   live Meta Graph API via /api/mer.
CURRENT = {
    'month': 'Aug', 'sale': True,   # promo month (Zip Mat launched 5 Aug + Father's Day 26 Aug)
    # Shopify net_sales, 9 completed days (Aug 1-9 = $96,824.16); Aug 10 partial excluded.
    'mtd_net': round(96824.16 * EXGST_PER_NETSALES), 'days_elapsed': 9, 'days_in_month': 31,
    'ad_spend_mtd': 38123,     # LIVE Meta Graph API via /api/campaigns (Aug 1-9)
    'assumed_mer': 0.34,       # fallback only — not used while spend is live
    'mer_note': 'ACTUAL — Meta API MTD (Aug 1-9), ex-GST basis',
}

# --- forward scenario: revenue (ex-GST) + MER per scenario --------------------
# Revenue = calendar-driven scenario, converted to the ex-GST basis. NOT a prediction.
# 'mer_current' now reflects the July-actual trajectory (~41% ex-GST), not the old 30% guess.
FORWARD = {
    'Sep': {'rev': 354858, 'sale': False, 'mer_current': 0.36, 'mer_target': 0.25},
    'Oct': {'rev': 344421, 'sale': False, 'mer_current': 0.36, 'mer_target': 0.25},
    'Nov': {'rev': 605346, 'sale': True,  'mer_current': 0.32, 'mer_target': 0.26},
    'Dec': {'rev': 448791, 'sale': True,  'mer_current': 0.34, 'mer_target': 0.26},
}

def vcr(sale): return VCR_SALE if sale else VCR_BAU
def gpam_pct(mer, sale): return (1 - vcr(sale)) - mer
def line(rev, mer, sale):
    gp = gpam_pct(mer, sale); g = rev * gp
    return gp, g, g - FIXED

def complete_current():
    c = CURRENT
    full_rev = round(c['mtd_net'] / c['days_elapsed'] * c['days_in_month'])
    if c['ad_spend_mtd']:
        mer = c['ad_spend_mtd'] / c['mtd_net']; mer_src = 'actual (MTD)'
    else:
        mer = c['assumed_mer']; mer_src = c.get('mer_note', 'ASSUMED — Meta not wired')
    return full_rev, mer, mer_src

def flags(gp, net):
    f = []
    if gp < GPAM_TARGET: f.append('GPAM<26%')
    if net < 0: f.append('LOSS')
    return ' '.join(f)

def render():
    out = []
    full_rev, cmer, mer_src = complete_current()
    csale = CURRENT['sale']
    cgp, cg, cnet = line(full_rev, cmer, csale)
    out.append(f"**In-progress month — {CURRENT['month']}** "
               f"(MTD net ${CURRENT['mtd_net']:,} over {CURRENT['days_elapsed']}/"
               f"{CURRENT['days_in_month']} days → completed ~${full_rev:,})")
    out.append(f"- MER: {cmer:.0%} ({mer_src}) · GPAM {cgp:.1%} · net ${cnet:,.0f} {flags(cgp,cnet)}")
    out.append("")
    for scen, key, label in [('current','mer_current','CURRENT TRAJECTORY'),
                             ('target','mer_target','TARGET DISCIPLINE')]:
        out.append(f"**Forward — {label}**")
        out.append("| Mon | Rev (net) | MER | GPAM% | GPAM$ | Net | flags |")
        out.append("|---|--:|--:|--:|--:|--:|---|")
        tr = tg = tn = 0
        # current month first (same in both, but shown for a full H2 view)
        out.append(f"| {CURRENT['month']} | ${full_rev:,} | {cmer:.0%} | {cgp:.1%} | "
                   f"${cg:,.0f} | ${cnet:,.0f} | {flags(cgp,cnet)} |")
        tr += full_rev; tg += cg; tn += cnet
        for m, d in FORWARD.items():
            gp, g, net = line(d['rev'], d[key], d['sale'])
            out.append(f"| {m} | ${d['rev']:,} | {d[key]:.0%} | {gp:.1%} | "
                       f"${g:,.0f} | ${net:,.0f} | {flags(gp,net)} |")
            tr += d['rev']; tg += g; tn += net
        out.append(f"| **H2** | **${tr:,.0f}** | | **{tg/tr:.1%}** | **${tg:,.0f}** | **${tn:,.0f}** | |")
        out.append("")
    fy_rev = sum(v[0] for v in ACTUALS.values()) + full_rev + sum(d['rev'] for d in FORWARD.values())
    out.append(f"Full-year 2026 net revenue (H1 actual + {CURRENT['month']} completed + forward): "
               f"**~${fy_rev:,.0f}**")
    out.append(f"\n*GPAM target {GPAM_TARGET:.0%}. Forward revenue = calendar scenario, not a "
               f"prediction. MER is the lever: the two tables differ only on spend discipline.*")
    return "\n".join(out)

if __name__ == '__main__':
    print(render())
