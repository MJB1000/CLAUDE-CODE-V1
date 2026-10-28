#!/usr/bin/env python3
"""Build an accurate Queensland PRO Mat sales map (inline SVG, interactive HTML).

Usage: python3 -I build_map.py GEO_DIR OUT_HTML
GEO_DIR holds australian_postcodes.csv (matthewproctor/australianpostcodes) as postcodes.csv
and states.geojson (rowanhogan/australian-states). Both are open data.
Dots sit on each postcode's centroid (mean of its locality coordinates), area proportional to mats sold.
"""
import csv, json, math, os, sys, html
from collections import defaultdict

GEO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sales data ----
units, orders = {}, {}
for t in open(os.path.join(HERE, "qld_units_since_mar.txt")).read().split():
    pc, o, u = t.split(":"); units[pc] = int(u); orders[pc] = int(o)
mix = defaultdict(lambda: defaultdict(int))
for t in open(os.path.join(HERE, "qld_variant_since_aug.txt")).read().split():
    pc, v, u = t.split(":"); mix[pc][v] += int(u)
regions = json.load(open(os.path.join(HERE, "qld_regions.json")))["regions"]

# ---- postcode centroids (QLD, delivery localities) ----
pts = defaultdict(list); names = defaultdict(list)
with open(os.path.join(GEO, "postcodes.csv"), encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        if r["state"] != "QLD": continue
        pc = r["postcode"].zfill(4)
        try:
            la = float(r.get("Lat_precise") or r["lat"]); lo = float(r.get("Long_precise") or r["long"])
        except ValueError:
            continue
        if la == 0 or lo == 0: continue
        if not (137.9 <= lo <= 153.7 and -29.3 <= la <= -9.9):  # source has a few bad precise coords
            try: la, lo = float(r["lat"]), float(r["long"])
            except ValueError: continue
            if not (137.9 <= lo <= 153.7 and -29.3 <= la <= -9.9): continue
        if (r.get("type") or "").lower().startswith("post office box"): continue
        pts[pc].append((lo, la)); names[pc].append(r["locality"].title())

def centroid(pc):
    p = pts.get(pc)
    if not p: return None
    return (sum(a for a, _ in p) / len(p), sum(b for _, b in p) / len(p))

# ---- projection: equirectangular scaled at -21deg ----
LON0, LON1, LAT0, LAT1 = 137.9, 153.7, -29.3, -9.9
K = math.cos(math.radians(21))
W = 620
SX = W / ((LON1 - LON0) * K)
H = (LAT1 - LAT0) * SX

def proj(lo, la):
    return ((lo - LON0) * K * SX, (LAT1 - la) * SX)

# ---- QLD outline ----
gj = json.load(open(os.path.join(GEO, "states.geojson")))
qld = next(f for f in gj["features"] if f["properties"]["STATE_NAME"] == "Queensland")["geometry"]
polys = qld["coordinates"] if qld["type"] == "MultiPolygon" else [qld["coordinates"]]
paths = []
for poly in polys:
    ring = poly[0]
    if len(ring) < 12: continue  # drop specks
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (proj(lo, la) for lo, la in ring)) + " Z"
    paths.append(d)
outline = "".join(f'<path d="{d}" class="land"/>' for d in paths)

METRO = set(range(4000, 4208)) | set(range(4300, 4306)) | set(range(4500, 4520))
dots, missing = [], []
for pc, u in sorted(units.items(), key=lambda kv: -kv[1]):
    c = centroid(pc)
    if not c:
        missing.append(pc); continue
    x, y = proj(*c)
    r = 1.6 + 2.1 * math.sqrt(u)
    m = mix.get(pc, {})
    mixtxt = ", ".join(f"{lab} {m[k]}" for k, lab in (("O", "Original"), ("R", "Orange"), ("G", "Grey"), ("C", "Camo"), ("P", "Pink")) if m.get(k)) or "no sales since 6 Aug"
    town = ", ".join(sorted(set(names[pc]))[:3]) + ("…" if len(set(names[pc])) > 3 else "")
    cls = "metro" if int(pc) in METRO else "reg"
    dots.append((u, f'<circle class="dot {cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" tabindex="0" '
                    f'data-pc="{pc}" data-town="{html.escape(town)}" data-u="{u}" data-o="{orders[pc]}" data-mix="{html.escape(mixtxt)}"/>'))
dot_svg = "".join(d for _, d in sorted(dots, key=lambda t: -t[0]))  # big first, small on top

LABELS = {"4740": "Mackay", "4670": "Bundaberg", "4570": "Gympie", "4702": "Gracemere", "4680": "Gladstone",
          "4751": "Walkerston", "4405": "Dalby", "4455": "Roma",
          "4818": "Townsville", "4825": "Mount Isa", "4720": "Emerald", "4870": "Cairns"}
lab_svg = []
for pc, name in LABELS.items():
    c = centroid(pc)
    if not c: continue
    x, y = proj(*c)
    dx = -6 if pc in ("4306", "4280", "4352", "4670", "4680", "4720", "4405", "4570") else 7
    anchor = "end" if dx < 0 else "start"
    dy = {"4702": -5, "4720": 3, "4680": 10, "4751": 10, "4740": -4, "4306": -11, "4280": 12, "4352": 6, "4570": -4, "4405": -7}.get(pc, 3)
    lab_svg.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}" class="lab">{name} <tspan class="lv">{units[pc]}</tspan></text>')


# ---- SEQ inset ----
ILON0, ILON1, ILAT0, ILAT1 = 151.15, 153.75, -28.4, -25.95
IX, IY, IW = 8, 8, 580
ISX = IW / ((ILON1 - ILON0) * K)
IH = (ILAT1 - ILAT0) * ISX
def iproj(lo, la):
    return (IX + (lo - ILON0) * K * ISX, IY + (ILAT1 - la) * ISX)
ipaths = []
for poly in polys:
    ring = poly[0]
    if len(ring) < 12: continue
    ipaths.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (iproj(lo, la) for lo, la in ring)) + " Z")
idots = []
for pc, u in sorted(units.items(), key=lambda kv: -kv[1]):
    c = centroid(pc)
    if not c or not (ILON0 <= c[0] <= ILON1 and ILAT0 <= c[1] <= ILAT1): continue
    x, y = iproj(*c); r = 1.6 + 2.1 * math.sqrt(u)
    m = mix.get(pc, {})
    mixtxt = ", ".join(f"{lab} {m[k]}" for k, lab in (("O", "Original"), ("R", "Orange"), ("G", "Grey"), ("C", "Camo"), ("P", "Pink")) if m.get(k)) or "no sales since 6 Aug"
    town = ", ".join(sorted(set(names[pc]))[:3]) + ("…" if len(set(names[pc])) > 3 else "")
    cls = "metro" if int(pc) in METRO else "reg"
    idots.append(f'<circle class="dot {cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" tabindex="0" data-pc="{pc}" data-town="{html.escape(town)}" data-u="{u}" data-o="{orders[pc]}" data-mix="{html.escape(mixtxt)}"/>')
ILAB = {"4306": ("Fernvale", 0, -12), "4280": ("Jimboomba", -8, 14), "4352": ("Toowoomba rural", -10, -6), "4350": ("Toowoomba", -9, 14),
        "4570": ("Gympie", 10, 4), "4341": ("Laidley", 0, 17), "4207": ("Beenleigh", 10, 4), "4285": ("Beaudesert", -9, 6), "4405": ("Dalby", 9, 4), "4610": ("Kingaroy", 9, 4)}
ilabs = []
for pc, (nm, dx, dy) in ILAB.items():
    c = centroid(pc)
    if not c or pc not in units: continue
    x, y = iproj(*c)
    ilabs.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{"end" if dx < 0 else ("middle" if dx == 0 else "start")}" class="lab">{nm} <tspan class="lv">{units[pc]}</tspan></text>')
for nm, lo, la in (("Brisbane", 153.03, -27.47), ("Gold Coast", 153.40, -28.02), ("Sunshine Coast", 153.08, -26.62)):
    x, y = iproj(lo, la); ilabs.append(f'<text x="{x+7:.1f}" y="{y+3:.1f}" class="city">{nm}</text>')
iland = "".join('<path d="' + d + '" class="land"/>' for d in ipaths)
bx0, by0 = proj(ILON0, ILAT1); bx1, by1 = proj(ILON1, ILAT0)
ibox_svg = f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1-bx0:.1f}" height="{by1-by0:.1f}" class="ibox"/>'
inset_svg = (f'<svg viewBox="0 0 {IW+16:.0f} {IH+16:.0f}" role="img" aria-label="Zoomed map of south-east Queensland PRO Mat sales"><g>'
             f'<clipPath id="ic"><rect x="{IX}" y="{IY}" width="{IW}" height="{IH}"/></clipPath>'
             f'<g clip-path="url(#ic)">{iland}{"".join(idots)}{"".join(ilabs)}</g>'
             f'</g></svg>')

# size legend
leg = []
lx = 22
for i, u in enumerate((1, 5, 15, 29)):
    r = 1.6 + 2.1 * math.sqrt(u); cy = H - 28
    leg.append(f'<circle cx="{lx + r}" cy="{cy}" r="{r:.1f}" class="dot reg legend"/><text x="{lx + r}" y="{cy + 26}" text-anchor="middle" class="lg">{u}</text>')
    lx += 2 * r + 16
legend = f'<g><text x="22" y="{H - 58}" class="lgt">Mats sold per postcode</text>{"".join(leg)}</g>'

rows = "".join(
    f'<tr><td>{html.escape(r["region"])}</td><td class="n">{r["units"]}</td><td class="n">{r["per_100k"]:.0f}</td><td class="n {"hi" if r["index_vs_qld"] >= 200 else ("lo" if r["index_vs_qld"] < 100 else "")}">{r["index_vs_qld"]}</td></tr>'
    for r in regions)

page = f"""<title>Queensland PRO Mat Map</title>
<style>
:root {{ --bg:#fbfaf6; --panel:#ffffff; --fg:#1d1b1b; --muted:#6d6761; --line:#e4e0d6; --land:#efece4; --landedge:#b9b2a6;
  --reg:#eb6834; --metro:#2a78d6; --hi:#b8461b; --lo:#2a78d6; --tip:#1d1b1b; --tipfg:#ffffff;
  --display:"Archivo Narrow","Arial Narrow",Arial,sans-serif; --body:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#171515; --panel:#211e1e; --fg:#f1eee8; --muted:#b3ada4; --line:#38332f; --land:#2a2726; --landedge:#5a544e; --reg:#f07a48; --metro:#4b92e6; --hi:#f0a05a; --lo:#7fb2ef; --tip:#f1eee8; --tipfg:#171515; color-scheme:dark; }} }}
:root[data-theme="dark"] {{ --bg:#171515; --panel:#211e1e; --fg:#f1eee8; --muted:#b3ada4; --line:#38332f; --land:#2a2726; --landedge:#5a544e; --reg:#f07a48; --metro:#4b92e6; --hi:#f0a05a; --lo:#7fb2ef; --tip:#f1eee8; --tipfg:#171515; color-scheme:dark; }}
* {{ box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.5 var(--body); margin:0; }}
.wrap {{ max-width:1100px; margin:0 auto; padding-inline:16px; padding-block:22px 48px; }}
.tag {{ display:inline-block; background:#f5eb19; color:#1d1b1b; font:700 11px/1 var(--display); letter-spacing:.12em; text-transform:uppercase; padding:5px 8px; }}
h1 {{ font:800 clamp(26px,5vw,38px)/1.08 var(--display); margin:10px 0 4px; text-wrap:balance; }}
.sub {{ color:var(--muted); margin:0 0 16px; max-width:70ch; }}
.grid {{ display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr); gap:20px; align-items:start; }}
@media (max-width:820px) {{ .grid {{ grid-template-columns:1fr; }} }}
.mapbox {{ position:relative; background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:8px; }}
svg {{ width:100%; height:auto; display:block; }}
.land {{ fill:var(--land); stroke:var(--landedge); stroke-width:.8; }}
.dot {{ fill-opacity:.72; stroke:var(--panel); stroke-width:1; cursor:pointer; }}
.dot.reg {{ fill:var(--reg); }} .dot.metro {{ fill:var(--metro); }}
.dot:hover, .dot:focus {{ fill-opacity:1; stroke:var(--fg); stroke-width:1.5; outline:none; }}
.legend {{ cursor:default; }}
.ibox {{ fill:none; stroke:var(--fg); stroke-width:1; stroke-dasharray:3 2; }}
h3.ih {{ font:700 13px var(--body); margin:10px 4px 2px; }}
.iframe {{ fill:var(--panel); stroke:var(--line); stroke-width:1; }}
.lab {{ font:700 10.5px var(--body); fill:var(--fg); paint-order:stroke; stroke:var(--panel); stroke-width:3px; }}
.lv {{ font-weight:400; fill:var(--muted); }}
.city {{ font:italic 10px var(--body); fill:var(--muted); paint-order:stroke; stroke:var(--panel); stroke-width:3px; }}
.lg {{ font:10px var(--body); fill:var(--muted); }} .lgt {{ font:700 10.5px var(--body); fill:var(--fg); }}
.key {{ display:flex; gap:14px; flex-wrap:wrap; font-size:13px; color:var(--muted); margin:6px 4px 0; }}
.key i {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:5px; vertical-align:-1px; }}
#tip {{ position:absolute; pointer-events:none; background:var(--tip); color:var(--tipfg); font-size:12.5px; line-height:1.4; padding:7px 9px; border-radius:6px; max-width:240px; box-shadow:0 4px 14px rgba(0,0,0,.18); }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px 16px; min-width:0; }}
.panel h2 {{ font:700 18px/1.2 var(--display); margin:0 0 6px; }}
.tblwrap {{ overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; min-width:340px; }}
th, td {{ text-align:left; padding:6px 6px; border-bottom:1px solid var(--line); }}
th {{ font:700 11px var(--display); letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }}
td.n {{ text-align:right; font-variant-numeric:tabular-nums; }}
td.hi {{ color:var(--hi); font-weight:700; }} td.lo {{ color:var(--lo); }}
.note {{ font-size:12px; color:var(--muted); margin-top:10px; }}
ul.ins {{ margin:12px 0 0; padding-left:18px; font-size:14px; }} ul.ins li {{ margin:5px 0; }}
</style>
<div class="wrap">
<span class="tag">DiggerLid · PRO Mat · Queensland</span>
<h1>Where Queensland buys PRO Mats</h1>
<p class="sub">Every Queensland postcode that bought a PRO Mat, 23 Mar to 12 Oct 2026 (803 mats). Dots sit on the postcode's real location, and their area shows mats sold. Orange is regional, blue is Greater Brisbane. Hover or tap a dot for the town, mats and colour mix.</p>
<div class="grid">
 <div class="mapbox" id="mapbox">
  <svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Map of Queensland with PRO Mat sales by postcode">{outline}{dot_svg}{"".join(lab_svg)}{legend}{ibox_svg}</svg>
  <h3 class="ih">South-east Queensland, zoomed (dashed box)</h3>{inset_svg}
  <div class="key"><span><i style="background:var(--reg)"></i>Regional postcode</span><span><i style="background:var(--metro)"></i>Greater Brisbane postcode</span></div>
  <div id="tip" hidden></div>
 </div>
 <div class="panel">
  <h2>Regions ranked by mats per person</h2>
  <div class="tblwrap"><table><thead><tr><th>Region</th><th style="text-align:right">Mats</th><th style="text-align:right">Per 100k</th><th style="text-align:right">Index</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note">Index 100 = Queensland average. Populations are QGSO ERP 30 Jun 2025p, matched to postcode groups (approximate). The SEQ acreage fringe is overstated because Jimboomba and Fernvale sit partly in larger councils.</p>
  <ul class="ins">
   <li><b>The inland belt leads.</b> Darling Downs (Dalby, Roma, Chinchilla, Wallumbilla), Emerald and Mackay and Isaac buy 3 to 5 times the state average.</li>
   <li><b>Industrial coast is the volume.</b> Mackay 29, Bundaberg 24, Gracemere 19, Gladstone 17 and Rockhampton 12.</li>
   <li><b>Acreage fringe of SEQ.</b> Fernvale 17, Jimboomba 10, Gympie 21: lifestyle blocks and machines, and Camo's strongest pocket.</li>
   <li><b>Coastal cities lag.</b> The Gold Coast (4 per 100k), Brisbane (6) and the Sunshine Coast (8) are 70% of Queenslanders but a small share of mats.</li>
  </ul>
 </div>
</div>
<p class="note">Sources: Shopify net items sold by shipping postcode. Postcode coordinates: Matthew Proctor Australian Postcodes (open data). State outline: ABS-derived open GeoJSON. Population: Queensland Government Statistician's Office. {len(missing)} postcode(s) without coordinates were left off the map{(": " + ", ".join(missing)) if missing else ""}.</p>
</div>
<script>
(function(){{
  var box=document.getElementById('mapbox'), tip=document.getElementById('tip');
  function show(e){{
    var t=e.target; if(!t.classList.contains('dot')||t.classList.contains('legend')) return;
    tip.innerHTML='<b>'+t.dataset.pc+' · '+t.dataset.town+'</b><br>'+t.dataset.u+' mats from '+t.dataset.o+' orders<br><span style="opacity:.8">Since 6 Aug: '+t.dataset.mix+'</span>';
    tip.hidden=false;
    var b=box.getBoundingClientRect(), r=t.getBoundingClientRect();
    var x=r.left-b.left+r.width/2+10, y=r.top-b.top-8;
    if(x>b.width-250) x=r.left-b.left-250;
    tip.style.left=Math.max(4,x)+'px'; tip.style.top=Math.max(4,y)+'px';
  }}
  function hide(){{ tip.hidden=true; }}
  box.addEventListener('mouseover',show); box.addEventListener('focusin',show);
  box.addEventListener('mouseout',hide); box.addEventListener('focusout',hide);
  box.addEventListener('click',show);
}})();
</script>
"""
open(OUT, "w", encoding="utf-8").write(page)
print("written", OUT, "dots", len(dots), "missing", missing)
