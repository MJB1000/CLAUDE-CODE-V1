#!/usr/bin/env python3
"""1-page PRO Mat geo snapshot (HTML -> PDF). Usage: python3 build_onepager.py OUT_DIR"""
import sys, html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
geo = json.load(open(os.path.join(HERE, "geo_results.json")))
mix = json.load(open(os.path.join(HERE, "mix_results.json")))

INK, INK2, MUTED, GRID = "#1d1b1b", "#4a4643", "#77716b", "#e6e2dc"
BLUE, ORANGE = "#2a78d6", "#eb6834"
MIXC = {"OG": "#2a78d6", "Orange": "#eb6834", "Grey": "#6250d6", "Camo": "#008300", "Pink": "#e87ba4"}
MIXL = {"OG": "Original", "Orange": "Plus Orange", "Grey": "Plus Grey", "Camo": "Plus Camo", "Pink": "Plus Pink"}
FONT = "'Liberation Sans', Arial, Helvetica, sans-serif"
e = html.escape


def index_bars(w=340):
    """Horizontal bars of index vs population (100 = parity)."""
    idx = geo["All PRO Mat"]["index"]
    rows = sorted(idx.items(), key=lambda kv: -kv[1])
    lab, rh, gap, top = 34, 15, 6, 6
    mx = 200; span = w - lab - 34
    h = top + len(rows) * (rh + gap) + 16
    o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="PRO Mat index vs population by state">']
    x100 = lab + span * 100 / mx
    for i, (s, v) in enumerate(rows):
        y = top + i * (rh + gap); bw = span * min(v, mx) / mx
        col = ORANGE if v >= 100 else BLUE
        o.append(f'<text x="0" y="{y+rh-3}" font-size="9.5" font-weight="700" fill="{INK}">{s}</text>')
        o.append(f'<rect x="{lab}" y="{y}" width="{bw}" height="{rh}" rx="3" fill="{col}"/>')
        o.append(f'<text x="{lab+bw+4}" y="{y+rh-3}" font-size="9" fill="{INK}">{v}</text>')
    o.append(f'<line x1="{x100}" y1="2" x2="{x100}" y2="{h-14}" stroke="{INK}" stroke-dasharray="3 2" stroke-width="1"/>')
    o.append(f'<text x="{x100}" y="{h-3}" text-anchor="middle" font-size="8" fill="{MUTED}">100 = in line with population</text>')
    o.append("</svg>")
    return "".join(o)


def cap_reg(w=340, h=150):
    """Grouped bars: mats per 100k people, capital vs regional, by state."""
    st = ["WA", "SA", "QLD", "VIC", "NSW", "TAS"]
    d = geo["metro_vs_regional_by_state"]
    data = [(s, d[s]["metro_per_100k"], d[s]["regional_per_100k"]) for s in st]
    pad_b, pad_t, pad_l = 26, 20, 4; mx = 36; ih = h - pad_b - pad_t; gw = (w - pad_l * 2) / len(data)
    o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Mats per 100k people capital vs regional">']
    o.append(f'<rect x="{w-170}" y="2" width="9" height="9" rx="2" fill="{BLUE}"/><text x="{w-157}" y="10" font-size="9" fill="{INK2}">Capital city</text>'
             f'<rect x="{w-90}" y="2" width="9" height="9" rx="2" fill="{ORANGE}"/><text x="{w-77}" y="10" font-size="9" fill="{INK2}">Regional</text>')
    o.append(f'<line x1="{pad_l}" y1="{h-pad_b}" x2="{w-pad_l}" y2="{h-pad_b}" stroke="{GRID}"/>')
    for i, (s, a, b) in enumerate(data):
        bw = gw * 0.34; x0 = pad_l + i * gw + gw * 0.14
        for j, (v, c) in enumerate(((a, BLUE), (b, ORANGE))):
            x = x0 + j * (bw + 2); bh = ih * v / mx; y = h - pad_b - bh
            o.append(f'<path d="M{x},{h-pad_b} V{y+3} Q{x},{y} {x+3},{y} H{x+bw-3} Q{x+bw},{y} {x+bw},{y+3} V{h-pad_b} Z" fill="{c}"/>')
            o.append(f'<text x="{x+bw/2}" y="{y-3}" text-anchor="middle" font-size="8.5" fill="{INK}">{v:.0f}</text>')
        o.append(f'<text x="{x0+bw+1}" y="{h-pad_b+12}" text-anchor="middle" font-size="9.5" font-weight="700" fill="{INK}">{s}</text>')
    o.append("</svg>")
    return "".join(o)


def mix_stack(w=720):
    """100% stacked bars: variant/colour mix by state + national, capital, regional."""
    rows = [("Australia", "national"), ("QLD", "QLD"), ("NSW", "NSW"), ("VIC", "VIC"), ("WA", "WA"), ("SA", "SA"),
            ("Capitals", "capital"), ("Regional", "regional")]
    lab, rh, gap = 64, 17, 5; top = 22; span = w - lab - 44
    h = top + len(rows) * (rh + gap) + 2
    o = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Variant and colour mix by state">']
    lx = lab
    for k in MIXC:
        o.append(f'<rect x="{lx}" y="3" width="9" height="9" rx="2" fill="{MIXC[k]}"/><text x="{lx+12}" y="11" font-size="9" fill="{INK2}">{MIXL[k]}</text>')
        lx += 12 + len(MIXL[k]) * 5.0 + 16
    for i, (name, key) in enumerate(rows):
        y = top + i * (rh + gap); x = lab; m = mix[key]["mix_%"]; n = mix[key]["units"]
        bold = "700" if key in ("national",) else "700"
        o.append(f'<text x="0" y="{y+rh-4}" font-size="9.5" font-weight="{bold}" fill="{INK}">{name}</text>')
        for k in MIXC:
            ww = span * m[k] / 100
            o.append(f'<rect x="{x}" y="{y}" width="{max(ww-2,0)}" height="{rh}" rx="2" fill="{MIXC[k]}"/>')
            if ww > 22:
                tc = INK if k == "Pink" else "#ffffff"
                o.append(f'<text x="{x+ww/2-1}" y="{y+rh-5}" text-anchor="middle" font-size="8.5" font-weight="700" fill="{tc}">{m[k]:.0f}%</text>')
            x += ww
        o.append(f'<text x="{lab+span+4}" y="{y+rh-5}" font-size="8" fill="{MUTED}">n={n}</text>')
        if key == "SA":
            o.append(f'<line x1="0" y1="{y+rh+gap/2}" x2="{w}" y2="{y+rh+gap/2}" stroke="{GRID}"/>')
    o.append("</svg>")
    return "".join(o)


g = geo["All PRO Mat"]; ps = geo["population_share"]
CSS = f"""@page {{ size: A4; margin: 10mm 12mm; }} * {{ box-sizing: border-box; }}
body {{ font-family: {FONT}; color: {INK}; font-size: 9.4pt; line-height: 1.35; margin: 0; background: #fff; }}
header {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:3px solid {INK}; padding-bottom:5px; margin-bottom:8px; }}
.tag {{ background:#f5eb19; font-weight:700; font-size:7.5pt; letter-spacing:.1em; padding:3px 6px; text-transform:uppercase; }}
h1 {{ font-size:17pt; margin:4px 0 0; line-height:1.1; }} h3 {{ font-size:9.8pt; margin:0 0 3px; }}
.meta {{ font-size:7.6pt; color:{MUTED}; text-align:right; }}
.kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:6px; margin:4px 0 10px; }}
.kpi {{ border:1px solid {GRID}; border-top:3px solid {INK}; padding:5px 7px; }} .kpi b {{ display:block; font-size:16pt; line-height:1.05; }} .kpi span {{ font-size:7.8pt; color:{INK2}; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:10px 16px; }} .card {{ min-width:0; }}
.cap {{ font-size:7.8pt; color:{MUTED}; margin-top:2px; }}
.box {{ background:#fbf7d6; border-left:4px solid {INK}; padding:7px 10px; margin-top:10px; }}
.box ul {{ margin:3px 0 0; padding-left:15px; }} .box li {{ margin:2.5px 0; }}
.foot {{ font-size:7pt; color:{MUTED}; border-top:1px solid {GRID}; margin-top:8px; padding-top:4px; }}"""

def kpi(v, l): return f'<div class="kpi"><b>{v}</b><span>{l}</span></div>'

body = f"""<header><div><span class="tag">DiggerLid · PRO Mat geo snapshot</span><h1>Where PRO Mats sell, and in which colour</h1></div>
<div class="meta">12 Oct 2026 · Shopify units vs ABS population<br>Australia only · 2,870 mats since 23 Mar · colour mix since Plus launch (6 Aug, 1,274 mats)</div></header>
<div class="kpis">{kpi("4.2×", "regional Australians buy per person vs capital cities (21.1 vs 5.0 per 100k)")}{kpi("67%", "of mats go regional, from 33% of the population")}{kpi("QLD 28%", "of mats from 21% of people (index 136). WA index 138")}{kpi("Orange 28%", "national bestseller. Plus = 74% of mats since launch")}</div>
<div class="grid2">
 <div class="card"><h3>Index vs population share, by state</h3>{index_bars()}
 <div class="cap">Share of mats ÷ share of population × 100. NT {g['index']['NT']} and ACT {g['index']['ACT']} are small bases ({g['units']} mats total).</div></div>
 <div class="card"><h3>Mats per 100k people: capital city vs regional</h3>{cap_reg()}
 <div class="cap">Every state's regions out-buy its capital by 3.6 to 7.4 times. Regional WA and SA lead at about 33 per 100k.</div></div>
</div>
<h3 style="margin-top:8px">Variant and colour mix (share of mats sold, 6 Aug to 12 Oct)</h3>{mix_stack()}
<div class="cap">TAS, NT and ACT are left out because each has fewer than 20 mats. Capitals and regional are classified by postcode ranges (approximate).</div>
<div class="box"><b>Standouts</b><ul>
<li><b>Regional is the market.</b> Two thirds of mats ship outside the capitals. Sydney (3.2 per 100k) and Melbourne (4.5) barely buy, and Perth is the best capital (9.1).</li>
<li><b>Queensland is Plus country.</b> Only 20% Original. Orange is 32% (45% in Brisbane) and Camo is 18%, the highest of any big state.</li>
<li><b>Grey Plus wins NSW (27%) and regional WA (32%).</b> Orange is weakest in WA (23%).</li>
<li><b>Original holds in SA (32%), WA (30%) and Sydney (33%).</b> These markets need the Original vs Plus comparison most.</li>
<li><b>Pink is regional</b> (10% regional vs 7% capitals), strongest in regional NSW and QLD. It's weak in SA (5%).</li>
<li><b>Meta:</b> weight spend to regional postcodes in QLD, WA, SA and NT. Lead QLD with Orange and Camo, NSW and WA with Grey, and test gift-framed Pink in regional NSW and QLD.</li></ul></div>
<div class="foot">Sources: Shopify net items sold by shipping state and postcode (ShopifyQL). ABS National, state and territory population, Mar 2026. ABS Regional population 2024-25 (Greater Capital City ERP, Jun 2025). Index = % of mats ÷ % of population × 100. Capital-city split uses standard metro postcode ranges and is approximate. Cells under 20 mats are indicative only.</div>"""

out = sys.argv[1]
open(os.path.join(out, "pro-mat-geo-snapshot-2026-10.html"), "w", encoding="utf-8").write(
    f"<!doctype html><html lang='en-AU'><head><meta charset='utf-8'><title>PRO Mat Geo Snapshot</title><style>{CSS}</style></head><body>{body}</body></html>")
print("ok")
