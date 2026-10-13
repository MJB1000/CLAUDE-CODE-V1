#!/usr/bin/env python3
"""Final QLD PRO Mat report: where mats sell (population-weighted) + who buys (business types).

Usage: python3 build_business_report.py GEO_DIR TEMPLATE OUT
  GEO_DIR  folder with postcodes.csv (matthewproctor australian_postcodes) and states.geojson
  TEMPLATE html with {{REGION}}, {{MAP}}, {{TRADES}} placeholders
Inputs are aggregates only: business_geo_qld.json (counts by region / postcode / type).
"""
import csv, json, math, os, sys
from collections import defaultdict

GEO, TPL, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "business_geo_qld.json")))

GROUP = {"Mechanical, diesel & automotive": "mec", "Civil, earthmoving & plant hire": "civ",
         "Farming, grazing & agriculture": "farm"}
def grp(t): return GROUP.get(t, "word" if t == "Trade word in email" else "oth")

# ---------- 1. regions: orders per 10k residents, business vs personal ----------
SHORT = {"SEQ fringe: Scenic Rim, Somerset & rural Logan/Ipswich": "SEQ acreage fringe",
         "Darling Downs & South West": "Darling Downs & SW", "Outback (Mt Isa, Longreach etc.)": "Outback",
         "Mackay, Isaac & Whitsunday": "Mackay & Isaac", "Rockhampton, Livingstone, Gladstone & Banana": "Rockhampton & Gladstone",
         "Townsville, Burdekin & Charters Towers": "Townsville", "Cairns, Tablelands & Far North": "Cairns & Far North",
         "Greater Brisbane (metro postcodes)": "Greater Brisbane", "Sunshine Coast & Noosa": "Sunshine Coast"}
CITY = {"Greater Brisbane", "Gold Coast", "Sunshine Coast"}
regs = [(SHORT.get(k, k), v) for k, v in D["regions"].items() if v["pop"]]
regs.sort(key=lambda kv: -kv[1]["orders_per_10k"])
W, L, R, rh, gap, top = 640, 168, 150, 18, 8, 22
span = W - L - R; mx = 7
H = top + len(regs) * (rh + gap) + 24
def X(v): return L + span * v / mx
o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="PRO Mat orders per 10,000 residents by Queensland region, split into business and personal buyers">']
o.append(f'<text x="{W-R+10}" y="12" class="colh">per 10k</text><text x="{W-6}" y="12" class="colh" text-anchor="end">business</text>')
for t in range(0, mx + 1):
    o.append(f'<line x1="{X(t):.1f}" y1="{top-6}" x2="{X(t):.1f}" y2="{H-20}" class="grid"/>')
    o.append(f'<text x="{X(t):.1f}" y="{H-5}" class="tick" text-anchor="middle">{t}</text>')
avg = D["total_orders"] / sum(v["pop"] for _, v in regs) * 1e4
o.append(f'<line x1="{X(avg):.1f}" y1="{top-8}" x2="{X(avg):.1f}" y2="{H-20}" class="avg"/>')
o.append(f'<text x="{X(avg)+4:.1f}" y="{top-10}" class="avgt">QLD average {avg:.1f}</text>')
for i, (n, v) in enumerate(regs):
    y = top + i * (rh + gap); p10 = v["orders_per_10k"]; b10 = v["biz"] / v["pop"] * 1e4
    city = n in CITY
    o.append(f'<text x="{L-10}" y="{y+rh/2+4.5}" text-anchor="end" class="lab{" city" if city else ""}">{n}</text>')
    o.append(f'<rect x="{L}" y="{y}" width="{X(b10)-L:.1f}" height="{rh}" class="rb"/>')
    o.append(f'<rect x="{X(b10)+1:.1f}" y="{y}" width="{max(X(p10)-X(b10)-1,0):.1f}" height="{rh}" class="rp"/>')
    o.append(f'<text x="{W-R+10}" y="{y+rh/2+4.5}" class="val">{p10:.1f}</text>')
    o.append(f'<text x="{W-6}" y="{y+rh/2+4.5}" class="val{" hi" if v["biz_pct"]>=30 else ""}" text-anchor="end">{v["biz_pct"]:.0f}%</text>')
o.append("</svg>")
REGION = "".join(o)

# ---------- 2. map: business buyers by postcode, coloured by trade group ----------
BOX = (137.9, 153.7, -29.3, -9.9)
def inq(lo, la): return BOX[0] <= lo <= BOX[1] and BOX[2] <= la <= BOX[3]
pts = defaultdict(list)
with open(os.path.join(GEO, "postcodes.csv"), encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        if r["state"] != "QLD" or (r.get("type") or "").lower().startswith("post office box"): continue
        try: la, lo = float(r.get("Lat_precise") or r["lat"]), float(r.get("Long_precise") or r["long"])
        except ValueError: continue
        if not inq(lo, la):
            try: la, lo = float(r["lat"]), float(r["long"])
            except ValueError: continue
            if not inq(lo, la): continue
        pts[r["postcode"].zfill(4)].append((lo, la))
def cen(p): return (sum(a for a, _ in p) / len(p), sum(b for _, b in p) / len(p))
LON0, LON1, LAT0, LAT1 = BOX
K = math.cos(math.radians(21)); MW = 620; SX = MW / ((LON1 - LON0) * K); MH = (LAT1 - LAT0) * SX
def proj(lo, la): return ((lo - LON0) * K * SX, (LAT1 - la) * SX)
gj = json.load(open(os.path.join(GEO, "states.geojson")))
geom = next(f for f in gj["features"] if f["properties"]["STATE_NAME"] == "Queensland")["geometry"]
polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
LANDD = "".join("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (proj(lo, la) for lo, la in poly[0])) + "Z"
                for poly in polys if len(poly[0]) >= 12)
SEQ = (151.6, 153.6, -28.25, -26.35)
sx0, sy0 = proj(SEQ[0], SEQ[3]); sx1, sy1 = proj(SEQ[1], SEQ[2])
IX, IY, IW = 350, 14, 255; Z = IW / (sx1 - sx0); IH = (sy1 - sy0) * Z
def ip(x, y): return (IX + (x - sx0) * Z, IY + (y - sy0) * Z)
ORDER = ["mec", "civ", "farm", "oth", "word"]
OFF = {"mec": (-1, -1), "civ": (1, -1), "farm": (-1, 1), "oth": (1, 1), "word": (0, 0)}
def dots(xy_fn, scale, clip=None):
    out = []
    for pc, c in D["pc_business"].items():
        if pc not in pts: continue
        x, y = xy_fn(*proj(*cen(pts[pc])))
        if clip and not (clip[0] <= x <= clip[2] and clip[1] <= y <= clip[3]): continue
        g = defaultdict(int)
        for t, k in c.items(): g[grp(t)] += k
        multi = len(g) > 1
        for key in ORDER:
            if key not in g: continue
            r = (2.6 + 2.0 * math.sqrt(g[key])) * scale
            dx, dy = OFF[key] if multi else (0, 0)
            out.append(f'<circle cx="{x+dx*r*0.75:.1f}" cy="{y+dy*r*0.75:.1f}" r="{r:.1f}" class="d {key}"/>')
    return "".join(out)
m = [f'<svg viewBox="0 0 {MW} {MH:.0f}" role="img" aria-label="Map of Queensland showing PRO Mat business buyers by postcode, coloured by trade">',
     f'<defs><clipPath id="ic"><rect x="{IX}" y="{IY}" width="{IW}" height="{IH:.1f}"/></clipPath></defs>',
     f'<path d="{LANDD}" class="land"/>',
     f'<rect x="{sx0:.1f}" y="{sy0:.1f}" width="{sx1-sx0:.1f}" height="{sy1-sy0:.1f}" class="sbox"/>',
     f'<line x1="{sx1:.1f}" y1="{sy0:.1f}" x2="{IX+IW/2:.1f}" y2="{IY+IH:.1f}" class="lead"/>',
     dots(lambda x, y: (x, y), 1.0, clip=None if False else None).replace('class="d', 'class="d m'),
     f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH:.1f}" class="inset"/>',
     f'<g clip-path="url(#ic)"><path d="{LANDD}" class="land" transform="translate({IX-sx0*Z:.2f},{IY-sy0*Z:.2f}) scale({Z:.4f})"/>',
     dots(ip, 1.0, clip=(IX - 20, IY - 20, IX + IW + 20, IY + IH + 20)), "</g>",
     f'<text x="{IX+8}" y="{IY+IH-10:.1f}" class="itl">South East QLD, enlarged</text>']
LBL = [("Cairns", 145.77, -16.92, 1), ("Townsville", 146.82, -19.26, 1), ("Mackay", 149.19, -21.14, 1),
       ("Rockhampton", 150.51, -23.38, 1), ("Emerald", 148.16, -23.53, -1), ("Mount Isa", 139.49, -20.73, 1),
       ("Longreach", 144.25, -23.44, 1), ("Bundaberg", 152.35, -24.87, 1), ("Roma", 148.79, -26.57, -1),
       ("Dalby", 151.27, -27.18, -1), ("Charleville", 146.24, -26.40, 1)]
for n, lo, la, s in LBL:
    x, y = proj(lo, la)
    m.append(f'<text x="{x+s*9:.1f}" y="{y+4:.1f}" class="pl" text-anchor="{"start" if s > 0 else "end"}">{n}</text>')
for n, lo, la, s in [("Brisbane", 153.03, -27.47, 1), ("Gold Coast", 153.40, -28.0, 1), ("Sunshine Coast", 153.07, -26.65, -1),
                     ("Toowoomba", 151.95, -27.56, -1), ("Ipswich", 152.76, -27.61, -1), ("Gympie", 152.67, -26.19, -1)]:
    x, y = ip(*proj(lo, la))
    if IY < y < IY + IH: m.append(f'<text x="{x+s*10:.1f}" y="{y+4:.1f}" class="pl" text-anchor="{"start" if s > 0 else "end"}">{n}</text>')
m.append("</svg>")
MAP = "".join(m)

# ---------- 3. trades ----------
T = D["types"]; E = D["types_estimated_part"]; N = D["business_orders"]
rows = sorted(T.items(), key=lambda kv: -kv[1])
SH = {"Mechanical, diesel & automotive": "Mechanical, diesel & auto", "Other services": "Other services & sole traders",
      "Government, education & corporate": "Govt, education & corporate", "Farming, grazing & agriculture": "Farming & grazing",
      "Engineering, fabrication & industrial": "Engineering & fabrication", "Mining, resources & energy": "Mining & resources"}
W2, L2, R2, rh2, g2 = 640, 200, 82, 20, 8; sp2 = W2 - L2 - R2; mx2 = 40
H2 = 6 + len(rows) * (rh2 + g2) + 22
def X2(v): return L2 + sp2 * v / mx2
t = [f'<svg viewBox="0 0 {W2} {H2}" role="img" aria-label="Business buyers by trade">']
for k in range(0, mx2 + 1, 10):
    t.append(f'<line x1="{X2(k):.1f}" y1="2" x2="{X2(k):.1f}" y2="{H2-20}" class="grid"/><text x="{X2(k):.1f}" y="{H2-5}" class="tick" text-anchor="middle">{k}</text>')
for i, (n, v) in enumerate(rows):
    y = 6 + i * (rh2 + g2); e = E.get(n, 0); c = v - e; key = GROUP.get(n, "oth")
    core = key != "oth"
    t.append(f'<text x="{L2-10}" y="{y+rh2/2+4.5}" text-anchor="end" class="lab{" city" if core else ""}">{SH.get(n, n)}</text>')
    t.append(f'<rect x="{L2}" y="{y}" width="{X2(c)-L2:.1f}" height="{rh2}" class="b {key}"/>')
    if e: t.append(f'<rect x="{X2(c)+1:.1f}" y="{y}" width="{X2(v)-X2(c)-1:.1f}" height="{rh2}" class="b {key} est"/>')
    t.append(f'<text x="{X2(v)+8:.1f}" y="{y+rh2/2+4.5}" class="val">{v} <tspan class="pct">{v/N*100:.0f}%</tspan></text>')
t.append("</svg>")
TRADES = "".join(t)

page = open(TPL).read().replace("{{REGION}}", REGION).replace("{{MAP}}", MAP).replace("{{TRADES}}", TRADES)
open(OUT, "w", encoding="utf-8").write(page)
print("ok", N, round(avg, 2))
