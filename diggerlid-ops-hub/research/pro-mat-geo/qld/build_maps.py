#!/usr/bin/env python3
"""Three Queensland PRO Mat maps on one page (inline SVG, interactive):
  1. Population-weighted: mats per 10k residents by ABS SA3 (QGSO SA2 ERP 2025p rolled up to SA3).
  2. Original vs Plus: postcode dots, same period (6 Aug to 12 Oct 2026), side by side.
  3. Colour: one dot per colour bought per postcode, drawn in the mat's colour.
Usage: python3 -I build_maps.py GEO_DIR QGSO_DIR OUT_HTML
GEO_DIR: postcodes.csv (matthewproctor/australianpostcodes), states.geojson (rowanhogan/australian-states).
QGSO_DIR: sa2.csv (QGSO ERP by SA2, 2001-2025p).
"""
import csv, json, math, os, sys, html
from collections import defaultdict, Counter

GEO, QG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
esc = html.escape

# ---------- sales ----------
units, orders = {}, {}
for t in open(os.path.join(HERE, "qld_units_since_mar.txt")).read().split():
    pc, o, u = t.split(":"); units[pc] = int(u); orders[pc] = int(o)
mix = defaultdict(lambda: defaultdict(int))
for t in open(os.path.join(HERE, "qld_variant_since_aug.txt")).read().split():
    pc, v, u = t.split(":"); mix[pc][v] += int(u)

# ---------- geography ----------
BOX = (137.9, 153.7, -29.3, -9.9)
def inq(lo, la): return BOX[0] <= lo <= BOX[1] and BOX[2] <= la <= BOX[3]
pts = defaultdict(list); names = defaultdict(set); pc_sa3 = defaultdict(Counter); sa3_name = {}; sa3_pts = defaultdict(list)
with open(os.path.join(GEO, "postcodes.csv"), encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        if r["state"] != "QLD": continue
        if (r.get("type") or "").lower().startswith("post office box"): continue
        pc = r["postcode"].zfill(4)
        try: la, lo = float(r.get("Lat_precise") or r["lat"]), float(r.get("Long_precise") or r["long"])
        except ValueError: continue
        if not inq(lo, la):
            try: la, lo = float(r["lat"]), float(r["long"])
            except ValueError: continue
            if not inq(lo, la): continue
        pts[pc].append((lo, la)); names[pc].add(r["locality"].title())
        s3 = (r.get("SA3_CODE_2021") or "").strip()
        if s3:
            pc_sa3[pc][s3] += 1; sa3_name[s3] = r.get("SA3_NAME_2021") or s3; sa3_pts[s3].append((lo, la))

def cen(p):
    return (sum(a for a, _ in p) / len(p), sum(b for _, b in p) / len(p)) if p else None

# SA3 population from SA2 ERP 2025p
sa3_pop = Counter()
rows = list(csv.reader(open(os.path.join(QG, "sa2.csv"), encoding="latin-1")))
for r in rows:
    if r and r[0].strip().isdigit() and len(r[0].strip()) == 9 and r[-1].strip():
        try: sa3_pop[r[0].strip()[:5]] += int(r[-1].replace(",", ""))
        except ValueError: pass
QLD_POP = sum(sa3_pop.values())

# ---------- projection ----------
LON0, LON1, LAT0, LAT1 = BOX
K = math.cos(math.radians(21)); W = 620; SX = W / ((LON1 - LON0) * K); H = (LAT1 - LAT0) * SX
def proj(lo, la): return ((lo - LON0) * K * SX, (LAT1 - la) * SX)
SEQ = (151.15, 153.75, -28.4, -25.75)
sx0, sy0 = proj(SEQ[0], SEQ[3]); sx1, sy1 = proj(SEQ[1], SEQ[2])
SEQ_VB = f"{sx0:.1f} {sy0:.1f} {sx1-sx0:.1f} {sy1-sy0:.1f}"; ZOOM = W / (sx1 - sx0)

gj = json.load(open(os.path.join(GEO, "states.geojson")))
geom = next(f for f in gj["features"] if f["properties"]["STATE_NAME"] == "Queensland")["geometry"]
polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
LAND = "".join('<path class="land" d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in (proj(lo, la) for lo, la in poly[0])) + ' Z"/>'
               for poly in polys if len(poly[0]) >= 12)
SEQBOX = f'<rect class="seqbox q-only" x="{sx0:.1f}" y="{sy0:.1f}" width="{sx1-sx0:.1f}" height="{sy1-sy0:.1f}"/>'

def circle(x, y, r, cls, style, tip):
    return (f'<circle class="dot {cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" data-r="{r:.2f}" style="{style}" tabindex="0" '
            f'data-tip="{esc(tip)}"/>')

def label(x, y, text, val, dx, dy, seq=False, mid=False):
    fs_q, fs_s = 10.5, 10.5 / ZOOM * 1.25
    cls = "lab s-only" if seq else "lab q-only"
    fs = fs_s if seq else fs_q
    d = dx / ZOOM * 1.25 if seq else dx; e = dy / ZOOM * 1.25 if seq else dy
    anchor = "middle" if mid else ("end" if dx < 0 else "start")
    sw = 3 / ZOOM * 1.25 if seq else 3
    return (f'<text class="{cls}" x="{x+d:.2f}" y="{y+e:.2f}" text-anchor="{anchor}" style="font-size:{fs:.2f}px;stroke-width:{sw:.2f}px">'
            f'{esc(text)}<tspan class="lv"> {esc(str(val))}</tspan></text>')

def r_of(u): return 1.6 + 2.1 * math.sqrt(u)

def svg(inner, aria):
    return (f'<svg class="map" viewBox="0 0 {W:.0f} {H:.0f}" data-q="0 0 {W:.0f} {H:.0f}" data-s="{SEQ_VB}" role="img" aria-label="{esc(aria)}">'
            f'{LAND}{SEQBOX}{inner}</svg>')

# ---------- MAP 1: weighted by population (regions with QGSO council populations) ----------
REG = json.load(open(os.path.join(HERE, "qld_regions.json")))["regions"]
TOT = sum(units.values()); AVG10K = TOT / 5669764 * 1e4
BINS = [(0.5, "#fbe1d1", "under half the QLD rate"), (1.0, "#f6b48e", "0.5 to 1x"), (2.0, "#ee7c45", "1 to 2x"),
        (4.0, "#c4511c", "2 to 4x"), (1e9, "#7d2e0c", "4x or more")]
def bin_col(rel):
    for lim, col, _ in BINS:
        if rel < lim: return col
def rcen(rg):
    cps = [cen(pts[str(p).zfill(4)]) for p in rg["postcodes"] if str(p).zfill(4) in pts]
    return (sum(a for a, _ in cps) / len(cps), sum(b for _, b in cps) / len(cps))
m1 = []; labs1 = []; rank = []
for rg in sorted(REG, key=lambda r: -r["pop"]):
    lo, la = rcen(rg); x, y = proj(lo, la)
    rate = rg["units"] / rg["pop"] * 1e4; rel = rate / AVG10K
    r = 4 + 0.62 * math.sqrt(rg["pop"] / 1000)
    tip = f"{rg['region']}|{rg['pop']:,} residents, {rg['units']} mats|{rate:.1f} per 10k ({rel:.1f}x the QLD rate)"
    m1.append(circle(x, y, r, "w", f"fill:{bin_col(rel)}", tip))
    rank.append((rate, rg))
SHORT = {"SEQ fringe: Scenic Rim, Somerset & rural Logan/Ipswich": "SEQ acreage fringe", "Outback (Mt Isa, Longreach etc.)": "Outback",
         "Greater Brisbane (metro postcodes)": "Greater Brisbane", "Rockhampton, Livingstone, Gladstone & Banana": "Rockhampton & Gladstone",
         "Townsville, Burdekin & Charters Towers": "Townsville", "Cairns, Tablelands & Far North": "Cairns & Far North", "Darling Downs & South West": "Darling Downs & SW",
         "Mackay, Isaac & Whitsunday": "Mackay & Isaac"}
for rate, rg in rank:
    lo, la = rcen(rg); x, y = proj(lo, la); r = 4 + 0.62 * math.sqrt(rg["pop"] / 1000)
    nm = SHORT.get(rg["region"], rg["region"])
    inseq = SEQ[0] <= lo <= SEQ[1] and SEQ[2] <= la <= SEQ[3]
    POS = {"Central Highlands": (-1, 20), "Rockhampton & Gladstone": (-1, -12), "Wide Bay & Burnett": (-1, 4),
           "Darling Downs & SW": (-1, 4), "Mackay & Isaac": (1, 4), "Outback": (1, 4)}
    SPOS = {"Sunshine Coast & Noosa": (-1, 10), "Toowoomba & Lockyer": (0, None), "Gold Coast": (-1, 4),
            "Greater Brisbane": (0, 4), "SEQ acreage fringe": (1, 10), "Gympie region": (1, 4)}
    if not inseq:
        side, dy = POS.get(nm, (1, 4))
        labs1.append(label(x, y, nm, f"{rate:.1f}", side * (r + 7), dy))
    else:
        side, dy = SPOS.get(nm, (1, 4))
        if dy is None: dy = r * 2 / 1.25 + 14
        labs1.append(label(x, y, nm, f"{rate:.1f}", side * (r * 2 / 1.25 + 4), dy, seq=True, mid=(side == 0)))
leg1 = "".join(f'<span><i style="background:{c}"></i>{esc(t)}</span>' for _, c, t in BINS)
rank_rows = "".join(f'<tr><td>{esc(rg["region"])}</td><td class="n">{rg["units"]}</td><td class="n">{rg["pop"]:,}</td><td class="n hi">{rate:.1f}</td></tr>'
                    for rate, rg in sorted(rank, key=lambda t: -t[0]))

# ---------- MAP 2: Original vs Plus (since 6 Aug) ----------
def var_map(keys, cls, name):
    out, labs = [], []
    tot = 0
    for pc in sorted(mix, key=lambda p: -sum(mix[p][k] for k in keys)):
        u = sum(mix[pc][k] for k in keys)
        if not u or pc not in pts: continue
        tot += u
        x, y = proj(*cen(pts[pc]))
        tip = f"{pc} · {', '.join(sorted(names[pc])[:3])}|{u} {name} mats since 6 Aug"
        out.append(circle(x, y, r_of(u), cls, "", tip))
    return "".join(out), tot
og_svg, og_tot = var_map("O", "og", "Original")
pl_svg, pl_tot = var_map("RGCP", "plus", "Plus")

# ---------- MAP 3: colour of mat bought (since 6 Aug) ----------
COL = {"O": ("#3f4349", "Original (Signature Grey)"), "G": ("#a7adb4", "Plus Signature Grey"), "R": ("#f26b1f", "Plus Safety Orange"),
       "C": ("#5c7436", "Plus High Country Camo"), "P": ("#ef6fae", "Plus Safety Pink")}
m3 = []
for pc in sorted(mix, key=lambda p: -sum(mix[p].values())):
    if pc not in pts: continue
    x0, y0 = proj(*cen(pts[pc]))
    ks = [k for k in "ORGCP" if mix[pc].get(k)]
    for i, k in enumerate(ks):
        u = mix[pc][k]
        ang = 2 * math.pi * i / max(len(ks), 1) - math.pi / 2
        off = 0 if len(ks) == 1 else 2.2 + 0.9 * math.sqrt(u)
        x, y = x0 + off * math.cos(ang), y0 + off * math.sin(ang)
        tip = f"{pc} · {', '.join(sorted(names[pc])[:3])}|{COL[k][1]}: {u} mat{'s' if u > 1 else ''}"
        m3.append(circle(x, y, 1.3 + 1.9 * math.sqrt(u), "c3" + (" og" if k == "O" else ""), f"fill:{COL[k][0]}", tip))
leg3 = "".join(f'<span><i style="background:{c}"></i>{esc(t)}</span>' for c, t in COL.values())
colour_totals = {k: sum(mix[p].get(k, 0) for p in mix) for k in "ORGCP"}

# place-name labels shared by maps 2 and 3
PLACES = [("Mackay", 149.18, -21.14, 7, -4), ("Rockhampton", 150.51, -23.38, 7, 3), ("Gladstone", 151.26, -23.84, 7, 8),
          ("Bundaberg", 152.35, -24.87, 7, 3), ("Emerald", 148.16, -23.52, -7, 3), ("Dalby", 151.27, -27.18, -7, 3),
          ("Roma", 148.79, -26.57, -7, 3), ("Townsville", 146.82, -19.26, 7, 3), ("Cairns", 145.77, -16.92, 7, 3),
          ("Mount Isa", 139.49, -20.73, 7, 3), ("Toowoomba", 151.95, -27.56, -7, 3)]
SEQPLACES = [("Gympie", 152.66, -26.19, 7, 3), ("Brisbane", 153.03, -27.47, 7, 3), ("Gold Coast", 153.40, -28.02, 7, 3),
             ("Sunshine Coast", 153.07, -26.65, 7, 3), ("Toowoomba", 151.95, -27.56, -7, 3), ("Ipswich", 152.76, -27.61, -7, 3),
             ("Jimboomba", 152.98, -27.83, -7, 6), ("Dalby", 151.27, -27.18, 7, 3), ("Kingaroy", 151.84, -26.54, 7, 3)]
def place_labels():
    o = []
    for n, lo, la, dx, dy in PLACES:
        x, y = proj(lo, la); o.append(f'<text class="pl q-only" x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{"end" if dx<0 else "start"}">{n}</text>')
    for n, lo, la, dx, dy in SEQPLACES:
        x, y = proj(lo, la); f = 1.25 / ZOOM
        o.append(f'<text class="pl s-only" x="{x+dx*f:.2f}" y="{y+dy*f:.2f}" text-anchor="{"end" if dx<0 else "start"}" style="font-size:{10*f:.2f}px;stroke-width:{3*f:.2f}px">{n}</text>')
    return "".join(o)
PL = place_labels()

CSS = """
:root{--bg:#fbfaf6;--panel:#fff;--fg:#1d1b1b;--muted:#6d6761;--line:#e4e0d6;--land:#efece4;--edge:#b9b2a6;--og:#2a78d6;--plus:#eb6834;--tip:#1d1b1b;--tipfg:#fff;--ring:#ffffff;--zero:#b9b2a6;
--display:"Archivo Narrow","Arial Narrow",Arial,sans-serif;--body:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171515;--panel:#211e1e;--fg:#f1eee8;--muted:#b3ada4;--line:#38332f;--land:#2c2928;--edge:#5a544e;--og:#4b92e6;--plus:#f07a48;--tip:#f1eee8;--tipfg:#171515;--ring:#211e1e;--zero:#6d6761;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#171515;--panel:#211e1e;--fg:#f1eee8;--muted:#b3ada4;--line:#38332f;--land:#2c2928;--edge:#5a544e;--og:#4b92e6;--plus:#f07a48;--tip:#f1eee8;--tipfg:#171515;--ring:#211e1e;--zero:#6d6761;color-scheme:dark}
*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);font:15px/1.5 var(--body);margin:0}
.wrap{max-width:1180px;margin:0 auto;padding-inline:16px;padding-block:22px 48px}
.tag{display:inline-block;background:#f5eb19;color:#1d1b1b;font:700 11px/1 var(--display);letter-spacing:.12em;text-transform:uppercase;padding:5px 8px}
h1{font:800 clamp(26px,5vw,38px)/1.08 var(--display);margin:10px 0 4px;text-wrap:balance}
h2{font:800 22px/1.15 var(--display);margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 14px;max-width:75ch}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding:8px 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--line);margin-bottom:16px}
.bar button{font:600 13px var(--body);padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}
.bar button[aria-pressed="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.bar button:focus-visible{outline:2px solid var(--plus);outline-offset:2px}
.bar span{font-size:13px;color:var(--muted)}
section{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:18px}
.grid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:18px;align-items:start}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:860px){.grid,.pair{grid-template-columns:1fr}}
.mapwrap{position:relative;min-width:0}
svg.map{width:100%;height:auto;display:block;background:var(--panel)}
.land{fill:var(--land);stroke:var(--edge);stroke-width:.8;vector-effect:non-scaling-stroke}
.seqbox{fill:none;stroke:var(--fg);stroke-dasharray:3 2;stroke-width:1;vector-effect:non-scaling-stroke}
.dot{stroke:var(--ring);stroke-width:1;vector-effect:non-scaling-stroke;cursor:pointer}
.dot.og{fill:var(--og);fill-opacity:.8}.dot.plus{fill:var(--plus);fill-opacity:.8}
.dot.w{fill-opacity:.95}.dot.zero{fill:none;stroke:var(--zero);stroke-dasharray:2 2}
.dot.c3{fill-opacity:.92}.dot.c3.og{stroke:var(--ring)}
.dot:hover,.dot:focus{stroke:var(--fg);stroke-width:2;outline:none}
.lab,.pl{paint-order:stroke;stroke:var(--panel);fill:var(--fg)}
.lab{font:700 10.5px var(--body)}.lv{font-weight:400;fill:var(--muted)}
.pl{font:italic 10px var(--body);fill:var(--muted);stroke-width:3px}
.seq .q-only{display:none}.s-only{display:none}.seq .s-only{display:inline}
.key{display:flex;gap:12px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin-top:8px}
.key i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:5px;vertical-align:-1px;border:1px solid var(--line)}
.tip{position:absolute;pointer-events:none;background:var(--tip);color:var(--tipfg);font-size:12.5px;line-height:1.4;padding:7px 9px;border-radius:6px;max-width:250px;z-index:3;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px;min-width:320px}
th,td{text-align:left;padding:6px;border-bottom:1px solid var(--line)}th{font:700 11px var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
td.n{text-align:right;font-variant-numeric:tabular-nums}td.hi{font-weight:700}
.c3sec .mapwrap{max-width:680px}
svg.map{overflow:hidden}
.note{font-size:12px;color:var(--muted);margin-top:8px}
.stat{font:800 26px/1 var(--display)}.statl{font-size:12px;color:var(--muted)}
ul.ins{margin:10px 0 0;padding-left:18px;font-size:14px}ul.ins li{margin:5px 0}
"""

JS = """
(function(){
 var btns=document.querySelectorAll('.bar button');
 function setView(v){
  btns.forEach(function(b){b.setAttribute('aria-pressed', b.dataset.v===v?'true':'false');});
  document.querySelectorAll('svg.map').forEach(function(s){
   s.setAttribute('viewBox', v==='s'?s.dataset.s:s.dataset.q);
   s.classList.toggle('seq', v==='s');
   s.querySelectorAll('circle.dot').forEach(function(c){
     var r=parseFloat(c.dataset.r); c.setAttribute('r', v==='s'? (r/%ZOOM%*2.0).toFixed(2) : r);
   });
  });
  try{localStorage.setItem('qldmapview',v);}catch(e){}
 }
 btns.forEach(function(b){b.addEventListener('click',function(){setView(b.dataset.v);});});
 var saved='q'; try{saved=localStorage.getItem('qldmapview')||'q';}catch(e){}
 setView(saved);
 document.querySelectorAll('.mapwrap').forEach(function(w){
  var tip=w.querySelector('.tip');
  function show(e){var t=e.target; if(!t.classList||!t.classList.contains('dot')) return;
   var p=t.dataset.tip.split('|'); tip.innerHTML='<b>'+p[0]+'</b>'+(p[1]?'<br>'+p[1]:'')+(p[2]?'<br><span style="opacity:.8">'+p[2]+'</span>':'');
   tip.hidden=false; var b=w.getBoundingClientRect(), r=t.getBoundingClientRect();
   var x=r.left-b.left+r.width/2+10, y=r.top-b.top-10; if(x>b.width-255) x=Math.max(4,r.left-b.left-255);
   tip.style.left=x+'px'; tip.style.top=Math.max(4,y)+'px';}
  function hide(){tip.hidden=true;}
  w.addEventListener('mouseover',show); w.addEventListener('focusin',show); w.addEventListener('click',show);
  w.addEventListener('mouseout',hide); w.addEventListener('focusout',hide);
 });
})();
""".replace("%ZOOM%", f"{ZOOM:.3f}")

def mapwrap(s): return f'<div class="mapwrap">{s}<div class="tip" hidden></div></div>'

page = f"""<title>Queensland PRO Mat Maps</title><style>{CSS}</style>
<div class="wrap">
<span class="tag">DiggerLid · PRO Mat · Queensland</span>
<h1>Queensland PRO Mat maps</h1>
<p class="sub">Three views of where Queensland buys PRO Mats. Dots sit on real locations. Hover or tap any dot for details. Use the buttons to zoom every map into south-east Queensland.</p>
<div class="bar" role="group" aria-label="Map view"><button data-v="q" aria-pressed="true">All of Queensland</button><button data-v="s" aria-pressed="false">Zoom: south-east QLD</button><span>Dashed box marks the zoom area</span></div>

<section>
<h2>1 · Weighted by population: mats per 10,000 residents</h2>
<p class="sub">Each circle is a Queensland region (a group of councils). <b>Circle size = how many people live there. Colour = mats per 10,000 residents</b>, compared with the Queensland rate of {AVG10K:.1f}. Dashed outlines bought none. 803 mats, 23 Mar to 12 Oct 2026.</p>
<div class="grid">
 <div>{mapwrap(svg("".join(m1) + "".join(labs1) + PL, "Queensland PRO Mats per 10,000 residents by region"))}
 <div class="key">{leg1}</div></div>
 <div><h3 style="margin:0 0 6px;font:700 15px var(--body)">Regions ranked by mats per 10,000 residents</h3>
 <div class="tbl"><table><thead><tr><th>Region</th><th style="text-align:right">Mats</th><th style="text-align:right">Residents</th><th style="text-align:right">Per 10k</th></tr></thead><tbody>{rank_rows}</tbody></table></div>
 <ul class="ins"><li><b>Darker = more mats per person</b>, so this map removes the "big town" effect from the raw count map.</li>
 <li>Big pale circles in the south-east are Brisbane, the Gold Coast and the Sunshine Coast: lots of people, few mats per person.</li>
 <li>The dark small and medium circles inland and up the coast are where demand is genuinely strongest.</li></ul>
 <p class="note">Population: QGSO estimated resident population by council, 30 Jun 2025p. Regions are postcode groups matched to councils, so boundaries are approximate. The SEQ acreage fringe rate is overstated because Jimboomba and Fernvale sit partly in larger councils.</p></div>
</div>
</section>

<section>
<h2>2 · Original vs Plus</h2>
<p class="sub">Same period for both (6 Aug to 12 Oct 2026, since Plus launched). Dot area = mats sold in that postcode.</p>
<div class="pair">
 <div><div class="stat">{og_tot}</div><div class="statl">Original mats ($219, Signature Grey)</div>{mapwrap(svg(og_svg + PL, "Original PRO Mat sales by postcode"))}</div>
 <div><div class="stat">{pl_tot}</div><div class="statl">Plus mats ($299, four colours)</div>{mapwrap(svg(pl_svg + PL, "PRO Mat Plus sales by postcode"))}</div>
</div>
<p class="note">Since launch Plus outsells Original about 4 to 1 in Queensland. Plus spreads further into the inland and northern regions. Original is relatively stronger around Brisbane and Mackay.</p>
</section>

<section class="c3sec">
<h2>3 · By mat colour</h2>
<p class="sub">Each dot is drawn in the colour of the mat bought (6 Aug to 12 Oct 2026). Where a postcode bought several colours, the dots fan out around the postcode. Dot area = mats of that colour.</p>
{mapwrap(svg("".join(m3) + PL, "PRO Mat sales by colour by postcode"))}
<div class="key">{leg3}</div>
<p class="note">Queensland totals since 6 Aug: Orange {colour_totals['R']}, Grey Plus {colour_totals['G']}, Original {colour_totals['O']}, Camo {colour_totals['C']}, Pink {colour_totals['P']}.</p>
</section>

<p class="note">Sources: Shopify net items sold by shipping postcode. Postcode coordinates: Matthew Proctor Australian Postcodes (open data; a few bad coordinates outside Queensland are filtered out). Queensland outline: ABS-derived open GeoJSON. Population: Queensland Government Statistician's Office.</p>
</div>
<script>{JS}</script>"""
open(OUT, "w", encoding="utf-8").write(page)
print("ok", "avg/10k", round(AVG10K, 2), "zoom", round(ZOOM, 2), "OG", og_tot, "PLUS", pl_tot, "colours", colour_totals)
print("regions:", [(rg["region"][:22], round(r, 1)) for r, rg in sorted(rank, key=lambda t: -t[0])])
