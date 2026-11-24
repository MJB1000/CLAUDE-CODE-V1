#!/usr/bin/env python3
"""Build the 2-page PRO Mat customer & conversion report (HTML -> PDF via Playwright).

Usage: python3 build_report.py OUT_DIR
All figures are aggregates measured on 12 Oct 2026 (see README.md in this folder).
"""
import sys, html

OG, PLUS = "#2a78d6", "#eb6834"      # validated categorical pair (light surface)
INK, INK2, MUTED, GRID, SURF = "#1d1b1b", "#4a4643", "#77716b", "#e6e2dc", "#ffffff"
ACCENT = "#f5eb19"
FONT = "'Liberation Sans', Arial, Helvetica, sans-serif"


def esc(s):
    return html.escape(str(s))


def bars_v(data, w=330, h=150, color=OG, fmt="{}", title=""):
    """Single-series vertical bars. data = [(label, value)]"""
    pad_l, pad_b, pad_t = 8, 30, 18
    n = len(data); mx = max(v for _, v in data)
    bw = (w - pad_l * 2) / n
    ih = h - pad_b - pad_t
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(title)}">']
    out.append(f'<line x1="{pad_l}" y1="{h-pad_b}" x2="{w-pad_l}" y2="{h-pad_b}" stroke="{GRID}" stroke-width="1"/>')
    for i, (lab, v) in enumerate(data):
        bh = ih * v / mx; x = pad_l + i * bw + bw * 0.18; bwid = bw * 0.64; y = h - pad_b - bh
        out.append(f'<path d="M{x},{h-pad_b} V{y+3} Q{x},{y} {x+3},{y} H{x+bwid-3} Q{x+bwid},{y} {x+bwid},{y+3} V{h-pad_b} Z" fill="{color}"/>')
        out.append(f'<text x="{x+bwid/2}" y="{y-4}" text-anchor="middle" font-size="9.5" fill="{INK}" font-weight="700">{esc(fmt.format(v))}</text>')
        out.append(f'<text x="{x+bwid/2}" y="{h-pad_b+12}" text-anchor="middle" font-size="9" fill="{INK2}">{esc(lab)}</text>')
    out.append("</svg>")
    return "".join(out)


def grouped(data, w=330, h=150, fmt="{}%", mx=None, title="", legend=True):
    """Two-series grouped vertical bars. data = [(label, og, plus)]"""
    pad_l, pad_b, pad_t = 8, 30, 22 if legend else 14
    n = len(data); mx = mx or max(max(a, b) for _, a, b in data)
    gw = (w - pad_l * 2) / n; ih = h - pad_b - pad_t
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(title)}">']
    if legend:
        out.append(f'<rect x="{w-150}" y="2" width="9" height="9" rx="2" fill="{OG}"/><text x="{w-137}" y="10" font-size="9" fill="{INK2}">Original</text>'
                   f'<rect x="{w-85}" y="2" width="9" height="9" rx="2" fill="{PLUS}"/><text x="{w-72}" y="10" font-size="9" fill="{INK2}">Plus</text>')
    out.append(f'<line x1="{pad_l}" y1="{h-pad_b}" x2="{w-pad_l}" y2="{h-pad_b}" stroke="{GRID}"/>')
    for i, (lab, a, b) in enumerate(data):
        bw = gw * 0.34; x0 = pad_l + i * gw + gw * 0.14
        for j, (v, c) in enumerate(((a, OG), (b, PLUS))):
            x = x0 + j * (bw + 2); bh = ih * v / mx; y = h - pad_b - bh
            out.append(f'<path d="M{x},{h-pad_b} V{y+3} Q{x},{y} {x+3},{y} H{x+bw-3} Q{x+bw},{y} {x+bw},{y+3} V{h-pad_b} Z" fill="{c}"/>')
            out.append(f'<text x="{x+bw/2}" y="{y-3}" text-anchor="middle" font-size="8.5" fill="{INK}">{esc(fmt.format(v))}</text>')
        out.append(f'<text x="{x0+bw+1}" y="{h-pad_b+12}" text-anchor="middle" font-size="9" fill="{INK2}">{esc(lab)}</text>')
    out.append("</svg>")
    return "".join(out)


def stacked_h(rows, cats, colors, w=330, row_h=22, title=""):
    """100% stacked horizontal bars. rows = [(label, [v...])], values in %"""
    lab_w = 58; h = len(rows) * (row_h + 10) + 26
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(title)}">']
    lx = lab_w
    for c, col in zip(cats, colors):
        out.append(f'<rect x="{lx}" y="2" width="9" height="9" rx="2" fill="{col}"/><text x="{lx+12}" y="10" font-size="9" fill="{INK2}">{esc(c)}</text>')
        lx += 12 + len(c) * 5.2 + 12
    for i, (lab, vals) in enumerate(rows):
        y = 20 + i * (row_h + 10); x = lab_w; tot = sum(vals); span = w - lab_w - 4
        out.append(f'<text x="0" y="{y+row_h/2+3}" font-size="9.5" fill="{INK}" font-weight="700">{esc(lab)}</text>')
        for v, col in zip(vals, colors):
            ww = span * v / tot
            out.append(f'<rect x="{x}" y="{y}" width="{max(ww-2,0)}" height="{row_h}" rx="3" fill="{col}"/>')
            if ww > 26:
                tc = "#ffffff" if col not in ("#f2c8a8", "#c9dcf3", "#d9d4cd") else INK
                out.append(f'<text x="{x+ww/2-1}" y="{y+row_h/2+3.5}" text-anchor="middle" font-size="9" fill="{tc}" font-weight="700">{v:.0f}%</text>')
            x += ww
    out.append("</svg>")
    return "".join(out)


# ---------- data (measured 12 Oct 2026) ----------
hist = [("Same day", 1599), ("Day 2", 54), ("3-7", 158), ("8-14", 145), ("15-28", 195), ("29+", 13)]
checkpoints = [("Same day", 74.8, 71.9), ("≤7 days", 84.4, 82.0), ("≤14 days", 91.1, 88.8), ("≤28 days", 99.5, 99.3)]
visits = [("All buyers", [54.5, 20.2, 15.4, 9.8])]
source_mix = [("Original", [33, 28, 39]), ("Plus", [43, 28, 29])]
states = [("QLD", 24, 30), ("NSW", 25, 26), ("VIC", 21, 17), ("WA", 15, 14), ("SA", 9, 7), ("Other", 6, 6)]
tod = [("5-9am", 11, 20), ("9am-5pm", 55, 49), ("5-10pm", 26, 25), ("Late", 7, 6)]
colours = [("Orange", 300), ("Grey", 221), ("Camo", 166), ("Pink", 101)]

CSS = f"""
@page {{ size: A4; margin: 11mm 12mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: {FONT}; color: {INK}; font-size: 9.6pt; line-height: 1.38; margin: 0; background: {SURF}; }}
.page {{ page-break-after: always; }}
.page:last-child {{ page-break-after: auto; }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid {INK}; padding-bottom: 5px; margin-bottom: 8px; }}
header .tag {{ background: {ACCENT}; color: {INK}; font-weight: 700; font-size: 7.5pt; letter-spacing: .1em; padding: 3px 6px; text-transform: uppercase; }}
h1 {{ font-size: 17pt; margin: 4px 0 0; line-height: 1.1; }}
h2 {{ font-size: 11pt; margin: 10px 0 4px; }}
h3 {{ font-size: 9.5pt; margin: 0 0 3px; }}
.meta {{ font-size: 7.6pt; color: {MUTED}; text-align: right; }}
.lede {{ font-size: 10pt; margin: 0 0 8px; }}
.kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 6px 0 8px; }}
.kpi {{ border: 1px solid {GRID}; border-top: 3px solid {INK}; padding: 5px 7px; }}
.kpi b {{ display: block; font-size: 16pt; line-height: 1.05; }}
.kpi span {{ font-size: 7.8pt; color: {INK2}; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px 14px; }}
.card {{ min-width: 0; }}
.cap {{ font-size: 7.8pt; color: {MUTED}; margin-top: 1px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 8.4pt; }}
th, td {{ text-align: left; padding: 3px 5px; border-bottom: 1px solid {GRID}; vertical-align: top; }}
th {{ font-size: 7.4pt; text-transform: uppercase; letter-spacing: .05em; color: {INK2}; }}
td.n {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
.hi {{ font-weight: 700; }}
.dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 4px; vertical-align: 0; }}
.box {{ background: #fbf7d6; border-left: 4px solid {INK}; padding: 6px 9px; margin: 6px 0; }}
.box p {{ margin: 0; }}
ul.acts {{ margin: 3px 0 0; padding-left: 15px; }} ul.acts li {{ margin: 2px 0; }}
.foot {{ font-size: 7.2pt; color: {MUTED}; border-top: 1px solid {GRID}; margin-top: 8px; padding-top: 4px; }}
"""

def kpi(v, l):
    return f'<div class="kpi"><b>{v}</b><span>{l}</span></div>'

page1 = f"""
<section class="page">
<header><div><span class="tag">DiggerLid · PRO Mat insights</span><h1>PRO Mat: how long people take to buy, and who buys Plus</h1></div>
<div class="meta">12 Oct 2026 · Shopify orders &amp; sessions<br>23 Mar to 12 Oct 2026 · 2,249 paid PRO Mat orders</div></header>
<p class="lede"><b>The short version:</b> PRO Mat is a fast decision. Three in four buyers purchase the same day they first arrive, about 2 visits over about 4 days on average. Plus buyers decide the same way as Original buyers, but they come more from Meta, live more in Queensland, buy earlier in the day and spend about $160 more per order.</p>
<div class="kpis">{kpi("74%", "buy on the same day as their first visit")}{kpi("84%", "buy within 7 days · 90% within 14")}{kpi("2.2 · 4 days", "average visits and days to purchase")}{kpi("91%", "of PRO Mat buyers are new to DiggerLid")}</div>

<h2>1. Conversion window</h2>
<div class="grid2">
 <div class="card"><h3>Days from first visit to purchase (all PRO Mat orders)</h3>{bars_v(hist, title="Days to purchase histogram")}
 <div class="cap">Orders with tracking data (n = 2,164). A second cluster at 15 to 28 days (195 orders) is larger than days 8 to 14: the "think about it, come back" group.</div></div>
 <div class="card"><h3>Share bought by each checkpoint: Original vs Plus</h3>{grouped(checkpoints, mx=110, title="Cumulative share bought by checkpoint")}
 <div class="cap">Plus buyers take about half a day longer on average (4.3 vs 3.8 days). 90% have bought by day 15 for Plus and day 13 for Original.</div></div>
 <div class="card"><h3>Number of visits before buying</h3>{stacked_h(visits, ["1 visit", "2 visits", "3-4", "5+"], ["#1d1b1b", "#4a4643", "#77716b", "#b5afa8"], title="Visits before purchase")}
 <div class="cap">Buyers who come back more than once (45%) average 3.7 visits over about a week. Original and Plus are near identical (2.2 visits each).</div></div>
 <div class="card"><h3>New customers, by first traffic source</h3>
 <table><tr><th>Source</th><th>Orders</th><th>Same day</th><th>≤7 days</th><th>90% by day</th></tr>
 <tr><td>Meta paid</td><td class="n">724</td><td class="n">70%</td><td class="n">80%</td><td class="n hi">18</td></tr>
 <tr><td>Google organic</td><td class="n">603</td><td class="n">79%</td><td class="n">89%</td><td class="n">9</td></tr>
 <tr><td>Meta organic / other</td><td class="n">330</td><td class="n">72%</td><td class="n">83%</td><td class="n">13</td></tr>
 <tr><td>Direct / unknown</td><td class="n">241</td><td class="n">77%</td><td class="n">83%</td><td class="n">14</td></tr>
 <tr><td>Email (Klaviyo)</td><td class="n">85</td><td class="n">74%</td><td class="n">87%</td><td class="n">9</td></tr></table>
 <div class="cap">Meta buyers have the longest tail. Sale periods run longer too: Father's Day 68% same day and 90% by day 18, against 76% and day 14 in normal trading.</div></div>
</div>

<h2>2. Purchase window for returning customers</h2>
<div class="grid2">
 <div class="card"><table><tr><th>Days from first DiggerLid order to buying a PRO Mat (n = 205)</th><th></th></tr>
 <tr><td>Median</td><td class="n hi">269 days</td></tr><tr><td>Middle half</td><td class="n">75 to 545 days</td></tr>
 <tr><td>Within 30 days</td><td class="n">13%</td></tr><tr><td>Over a year</td><td class="n">37%</td></tr></table></div>
 <div class="card box"><p><b>Read:</b> PRO Mat is mostly a new-customer product (91%). For existing customers it's a slow-burn cross-sell, typically 9 months after their first order, not a 30-day post-purchase add-on. Target past customers 3 to 18 months after their first order.</p></div>
</div>
</section>"""

page2 = f"""
<section class="page">
<header><div><span class="tag">DiggerLid · PRO Mat insights</span><h1>Original vs Plus customers</h1></div>
<div class="meta">Same period for both: 6 Aug (Plus launch) to 12 Oct 2026<br>Original 291 orders · Plus 788 orders</div></header>

<div class="grid2">
 <div class="card"><h3>Side by side</h3>
 <table><tr><th></th><th><span class="dot" style="background:{OG}"></span>Original $219</th><th><span class="dot" style="background:{PLUS}"></span>Plus $299</th></tr>
 <tr><td>Spend per order</td><td class="n">$294</td><td class="n hi">$456</td></tr>
 <tr><td>Orders with 2+ mats</td><td class="n">8%</td><td class="n hi">32%</td></tr>
 <tr><td>Mat-only orders</td><td class="n">43%</td><td class="n hi">12%</td></tr>
 <tr><td>New to DiggerLid</td><td class="n">93%</td><td class="n">90%</td></tr>
 <tr><td>First-time buyers who ordered again*</td><td class="n">1.5%</td><td class="n hi">3.7%</td></tr>
 <tr><td>Visits / days to buy</td><td class="n">2.7 / 4.8</td><td class="n">2.2 / 4.3</td></tr>
 <tr><td>Used a discount code</td><td class="n">32%</td><td class="n">30%</td></tr>
 <tr><td>Discount as % of gross</td><td class="n">4%</td><td class="n">9-12%</td></tr></table>
 <div class="cap">*Small numbers (4 vs 23 customers), so treat as early signal. Original visits are measured since Plus launched. Before Plus, Original buyers averaged 2.2 visits over 3.8 days.</div></div>

 <div class="card"><h3>Where orders come from (order referrer)</h3>{stacked_h(source_mix, ["Social / Meta", "Search", "Direct / none"], [PLUS, OG, "#77716b"], title="Referrer mix")}
 <div class="cap">Plus leans on Meta creative (43% social). Original sells more on reputation, with 39% arriving direct.</div>
 <h3 style="margin-top:6px">Time of day orders are placed</h3>{grouped(tod, h=128, mx=62, title="Orders by time of day")}
 <div class="cap">One in five Plus orders lands between 5 and 9am, nearly double Original's 11%.</div></div>

 <div class="card"><h3>Orders by state</h3>{grouped(states, h=140, mx=33, title="Orders by state")}
 <div class="cap">Plus over-indexes in Queensland. Orange and Camo are about one third QLD. Other includes TAS, ACT, NT and NZ (NZ about 2 to 4%).</div></div>

 <div class="card"><h3>Plus orders by colour</h3>{bars_v(colours, h=128, color=PLUS, title="Plus orders by colour")}
 <div class="cap">Pink has the biggest basket ($552 per order), likely gift-led. Grey is evenly spread across states.</div></div>
</div>

<h2>The product page since Plus launched</h2>
<table><tr><th>Sessions landing on /products/pro-mat</th><th>Before Plus (23 Mar to 5 Aug)</th><th>After Plus (6 Aug to 12 Oct)</th><th>Change</th></tr>
<tr><td>Sessions</td><td class="n">68,351</td><td class="n">92,152</td><td class="n">+35%</td></tr>
<tr><td>Add to cart</td><td class="n">1.9%</td><td class="n">1.1%</td><td class="n hi">-41%</td></tr>
<tr><td>Cart to purchase</td><td class="n">52%</td><td class="n">44%</td><td class="n hi">-8 pts</td></tr>
<tr><td>Session conversion</td><td class="n">0.97%</td><td class="n">0.49%</td><td class="n hi">-49%</td></tr></table>
<div class="cap">Shopify can't split the funnel by variant, because both live on one page. Part of the drop is likely colder Father's Day and broad-audience traffic, but it lines up with Original buyers now taking more visits to choose.</div>

<div class="box" style="margin-top:7px"><h3>What to do</h3><ul class="acts">
<li><b>Fix the choice on the product page.</b> Add a clear Original vs Plus comparison ("Plus = zips + reflective + 4 colours") and default the selector to the bestseller. The page now converts at half its old rate.</li>
<li><b>Attribution and retargeting.</b> Keep 7-day click (about 80% of Meta buyers). Run 28-day retargeting with a fresh proof creative at days 10 to 14 to catch the 15 to 28 day cluster.</li>
<li><b>Sell Plus as a system.</b> 32% already buy 2+ mats, so lead Plus ads with "zip two together" and test a 2-mat bundle.</li>
<li><b>Targeting.</b> Test Queensland-weighted Orange and Camo creative, and early-morning (5 to 9am) delivery for Plus. Use gift framing for Pink.</li>
<li><b>Past customers.</b> Cross-sell PRO Mat to customers 3 to 18 months after their first order, not in the first 30 days.</li></ul></div>

<div class="foot">Sources: Shopify order customer journeys (2,249 paid PRO Mat orders, $0 orders excluded), ShopifyQL sales and sessions. "Days to purchase" counts from the first tracked visit (day 1 = same day). Shopify tracks journeys for about 30 days on one device, so longer and cross-device journeys are undercounted. Gift-buyer share was not measured. Original = SKU DLPROM1980; Plus = DLPROM1984 to 1987. No customer personal data was stored.</div>
</section>"""

out = sys.argv[1]
doc = f"<!doctype html><html lang='en-AU'><head><meta charset='utf-8'><title>PRO Mat Insights</title><style>{CSS}</style></head><body>{page1}{page2}</body></html>"
open(f"{out}/pro-mat-insights-2026-10.html", "w", encoding="utf-8").write(doc)
print("html written")
