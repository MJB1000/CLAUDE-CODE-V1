#!/usr/bin/env python3
"""
DiggerLid weekly forecast engine.

The Scorekeeper runs this every Monday:
  1. Update INPUTS below — lock any finished month into ACTUALS, and refresh the
     in-progress month's month-to-date (net revenue, days elapsed) + ad spend.
  2. `python3 forecast_engine.py` → prints a Markdown forecast block.
  3. Save it to data/forecast/YYYY-Www.md and refresh data/FORECAST.md.

Model (EE baseline):  GPAM% = (1 - VCR) - MER ;  GPAM$ = rev * GPAM% ;  Net = GPAM$ - FIXED.
Revenue = Shopify net_sales (after discounts/returns, before GST), AUD.
GPAM target = 26%.  MER target <= 25% (sale months <= 28%).

MER note: if the in-progress month's ad_spend_mtd is None (Meta not wired), MER falls back
to `assumed_mer` and is flagged. Once Meta is wired, pass real spend and MER becomes actual.
"""

FIXED = 74831
VCR_BAU, VCR_SALE = 0.46, 0.48
GPAM_TARGET = 0.26

# --- finished months: (net_revenue, realized_MER) -----------------------------
ACTUALS = {
    'Jan': (239596, 0.20), 'Feb': (298749, 0.28), 'Mar': (301354, 0.32),
    'Apr': (331418, 0.32), 'May': (400329, 0.30), 'Jun': (778275, 0.25),
}

# --- month in progress: refresh weekly ---------------------------------------
CURRENT = {
    'month': 'Jul', 'sale': False,
    'mtd_net': 176383, 'days_elapsed': 15, 'days_in_month': 31,
    'ad_spend_mtd': None,      # set to real Meta spend when wired; None -> use assumed_mer
    'assumed_mer': 0.43,       # recent EE-model level; replace with actual when spend known
}

# --- forward scenario: revenue + MER per scenario ----------------------------
FORWARD = {
    'Aug': {'rev': 420000, 'sale': True,  'mer_current': 0.32, 'mer_target': 0.27},
    'Sep': {'rev': 340000, 'sale': False, 'mer_current': 0.30, 'mer_target': 0.25},
    'Oct': {'rev': 330000, 'sale': False, 'mer_current': 0.30, 'mer_target': 0.25},
    'Nov': {'rev': 580000, 'sale': True,  'mer_current': 0.28, 'mer_target': 0.26},
    'Dec': {'rev': 430000, 'sale': True,  'mer_current': 0.30, 'mer_target': 0.26},
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
        mer = c['assumed_mer']; mer_src = 'ASSUMED — Meta not wired'
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
