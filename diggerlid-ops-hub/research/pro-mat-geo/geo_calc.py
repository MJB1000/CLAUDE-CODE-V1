#!/usr/bin/env python3
"""PRO Mat geo index: share of units vs share of population. Aggregates from ShopifyQL (23 Mar to 12 Oct 2026)."""
import json
POP = {"NSW": 8670.1, "VIC": 7154.2, "QLD": 5739.5, "SA": 1916.8, "WA": 3096.2, "TAS": 580.7, "NT": 268.9, "ACT": 489.7}  # ABS ERP 31 Mar 2026 ('000)
CAP = {"NSW": 5638.83, "VIC": 5435.59, "QLD": 2833.524, "SA": 1491.015, "WA": 2452.765, "TAS": 255.25, "NT": 159.284, "ACT": 484.63}  # ABS GCCSA ERP 30 Jun 2025 ('000)
NAME = {"New South Wales": "NSW", "Victoria": "VIC", "Queensland": "QLD", "South Australia": "SA", "Western Australia": "WA", "Tasmania": "TAS", "Northern Territory": "NT", "Australian Capital Territory": "ACT"}
V = {"OG / Signature Grey": "OG", "PLUS / Safety Orange": "Orange", "PLUS / Signature Grey": "Grey", "PLUS / High Country Camo": "Camo", "PLUS / Safety Pink": "Pink"}
# (variant, state, orders, units) all AU
tot = [("OG / Signature Grey","Queensland",407,505),("OG / Signature Grey","New South Wales",401,488),("OG / Signature Grey","Victoria",326,396),("OG / Signature Grey","Western Australia",242,304),("OG / Signature Grey","South Australia",107,141),("PLUS / Safety Orange","Queensland",93,119),("PLUS / Safety Orange","New South Wales",69,85),("PLUS / Signature Grey","New South Wales",68,90),("PLUS / Signature Grey","Queensland",57,75),("PLUS / Safety Orange","Victoria",56,71),("PLUS / High Country Camo","Queensland",54,67),("OG / Signature Grey","Tasmania",41,44),("PLUS / Signature Grey","Western Australia",38,48),("PLUS / Safety Orange","Western Australia",36,43),("PLUS / High Country Camo","New South Wales",36,41),("PLUS / High Country Camo","Victoria",35,40),("PLUS / Signature Grey","Victoria",32,39),("PLUS / Safety Pink","New South Wales",29,35),("PLUS / Safety Pink","Queensland",29,37),("OG / Signature Grey","Northern Territory",25,33),("PLUS / Safety Orange","South Australia",25,31),("PLUS / High Country Camo","Western Australia",22,24),("PLUS / Safety Pink","Western Australia",17,19),("PLUS / Signature Grey","South Australia",14,16),("PLUS / Safety Pink","Victoria",13,17),("OG / Signature Grey","Australian Capital Territory",12,12),("PLUS / High Country Camo","South Australia",9,11),("PLUS / Signature Grey","Tasmania",5,5),("PLUS / Safety Pink","South Australia",5,5),("PLUS / Safety Pink","Northern Territory",4,6),("PLUS / High Country Camo","Northern Territory",4,4),("PLUS / Safety Orange","Northern Territory",3,3),("PLUS / Signature Grey","Northern Territory",3,3),("PLUS / Safety Orange","Australian Capital Territory",3,3),("PLUS / Safety Orange","Tasmania",3,4),("PLUS / Signature Grey","Australian Capital Territory",2,2),("PLUS / High Country Camo","Tasmania",2,2),("PLUS / High Country Camo","Australian Capital Territory",1,1),("PLUS / Safety Pink","Tasmania",1,1)]
metro = [("Victoria","OG / Signature Grey",153,180),("Western Australia","OG / Signature Grey",131,152),("New South Wales","OG / Signature Grey",113,127),("Queensland","OG / Signature Grey",96,114),("South Australia","OG / Signature Grey",43,48),("Victoria","PLUS / Safety Orange",23,27),("Western Australia","PLUS / Safety Orange",21,25),("Queensland","PLUS / Safety Orange",20,31),("Victoria","PLUS / High Country Camo",19,21),("Western Australia","PLUS / Signature Grey",16,20),("New South Wales","PLUS / Signature Grey",15,20),("New South Wales","PLUS / Safety Orange",14,18),("Australian Capital Territory","OG / Signature Grey",12,12),("Western Australia","PLUS / High Country Camo",12,14),("Northern Territory","OG / Signature Grey",12,16),("Western Australia","PLUS / Safety Pink",11,13),("New South Wales","PLUS / High Country Camo",10,13),("Victoria","PLUS / Signature Grey",10,11),("Queensland","PLUS / Signature Grey",9,11),("Queensland","PLUS / High Country Camo",9,11),("South Australia","PLUS / Safety Orange",9,11),("Tasmania","OG / Signature Grey",5,5),("Victoria","PLUS / Safety Pink",4,5),("New South Wales","PLUS / Safety Pink",4,5),("Queensland","PLUS / Safety Pink",3,3),("Australian Capital Territory","PLUS / Safety Orange",3,3),("South Australia","PLUS / Signature Grey",3,4),("Northern Territory","PLUS / High Country Camo",3,3),("Northern Territory","PLUS / Safety Orange",3,3),("Australian Capital Territory","PLUS / Signature Grey",2,2),("Tasmania","PLUS / Signature Grey",2,2),("Northern Territory","PLUS / Safety Pink",1,2),("Northern Territory","PLUS / Signature Grey",1,1),("South Australia","PLUS / High Country Camo",1,1),("Australian Capital Territory","PLUS / High Country Camo",1,1),("South Australia","PLUS / Safety Pink",1,1)]
brand = {"NSW": 3298, "QLD": 2976, "VIC": 2270, "WA": 1299, "SA": 826, "TAS": 308, "ACT": 113, "NT": 104}  # all DiggerLid AU orders same period

units = {}; munits = {}
for v, s, o, u in tot: units[(V[v], NAME[s])] = u
for s, v, o, u in metro: munits[(V[v], NAME[s])] = u
groups = {"All PRO Mat": ["OG", "Orange", "Grey", "Camo", "Pink"], "Original": ["OG"], "Plus (all)": ["Orange", "Grey", "Camo", "Pink"],
          "Plus Orange": ["Orange"], "Plus Grey": ["Grey"], "Plus Camo": ["Camo"], "Plus Pink": ["Pink"]}
P = sum(POP.values()); states = list(POP)
out = {"population_share": {s: round(100 * POP[s] / P, 1) for s in states}}
for g, vs in groups.items():
    u = {s: sum(units.get((v, s), 0) for v in vs) for s in states}; T = sum(u.values())
    m = {s: sum(munits.get((v, s), 0) for v in vs) for s in states}; MT = sum(m.values())
    out[g] = {"units": T,
              "share": {s: round(100 * u[s] / T, 1) for s in states},
              "index": {s: round((u[s] / T) / (POP[s] / P) * 100) for s in states},
              "per_100k": {s: round(u[s] * 100 / POP[s], 1) for s in states},
              "metro_share_of_units": round(100 * MT / T, 1),
              "metro_index": round((MT / T) / (sum(CAP.values()) / P) * 100),
              "regional_index": round(((T - MT) / T) / (1 - sum(CAP.values()) / P) * 100)}
B = sum(brand.values())
out["brand_share"] = {s: round(100 * brand[s] / B, 1) for s in states}
out["brand_index"] = {s: round((brand[s] / B) / (POP[s] / P) * 100) for s in states}
# per-state metro vs regional for all PRO Mat
allv = groups["All PRO Mat"]; ms = {}
for s in states:
    u = sum(units.get((v, s), 0) for v in allv); m = sum(munits.get((v, s), 0) for v in allv)
    capshare = CAP[s] / POP[s]
    ms[s] = {"units": u, "metro_units": m, "metro_%units": round(100 * m / u, 1) if u else None, "metro_%pop": round(100 * capshare, 1),
             "metro_per_100k": round(m * 100 / CAP[s], 1), "regional_per_100k": round((u - m) * 100 / (POP[s] - CAP[s]), 1) if POP[s] > CAP[s] + 1 else None}
out["metro_vs_regional_by_state"] = ms
out["national_capital_pop_share"] = round(100 * sum(CAP.values()) / P, 1)
print(json.dumps(out, indent=1))
