#!/usr/bin/env python3
"""Regional QLD PRO Mat breakdown: postcode clusters -> approx LGA populations (QGSO ERP 30 Jun 2025p).
Clusters are postcode approximations of LGA groups, so per-capita figures are indicative."""
import csv, json, sys
POPCSV = sys.argv[1]
pop = {}
for r in list(csv.reader(open(POPCSV, encoding="latin-1")))[6:]:
    if r and r[0] and r[-1]:
        try: pop[r[0]] = int(r[-1].replace(",", ""))
        except ValueError: pass

def rng(*spans):
    s = set()
    for a in spans:
        if isinstance(a, int): s.add(a)
        else: s.update(range(a[0], a[1] + 1))
    return s

CLUSTERS = [
 ("Mackay, Isaac & Whitsunday", rng((4737,4757),4721,(4798,4805)), ["Mackay (R)","Isaac (R)","Whitsunday (R)"], "Mackay 4740, Walkerston 4751, Sarina 4737, Moranbah 4744, Clermont 4721, Airlie/Proserpine 4800-4802"),
 ("Rockhampton, Livingstone, Gladstone & Banana", rng((4700,4716),(4718,4719),(4677,4699)), ["Rockhampton (R)","Livingstone (S)","Gladstone (R)","Banana (S)"], "Rockhampton 4700-4701, Gracemere 4702, Yeppoon 4703, Gladstone 4680, Biloela 4715"),
 ("Central Highlands", rng(4717,4720,(4722,4724)), ["Central Highlands (R)"], "Emerald 4720, Springsure 4722, Capella 4723, Blackwater 4717"),
 ("Darling Downs & South West", rng((4370,4499)), ["Western Downs (R)","Maranoa (R)","Goondiwindi (R)","Southern Downs (R)","Balonne (S)","Murweh (S)","Paroo (S)","Bulloo (S)","Quilpie (S)"], "Dalby 4405, Roma 4455, Wallumbilla 4428, Chinchilla 4413, Goondiwindi 4390, Warwick 4370, Charleville 4470"),
 ("Toowoomba & Lockyer", rng((4340,4365)), ["Toowoomba (R)","Lockyer Valley (R)"], "Toowoomba 4350, rural Toowoomba 4352, Laidley/Plainland 4341, Gatton 4343"),
 ("Wide Bay & Burnett", rng((4600,4676)), ["Bundaberg (R)","Fraser Coast (R)","South Burnett (R)","North Burnett (R)","Cherbourg (S)"], "Bundaberg 4670, Maryborough 4650, Hervey Bay 4655, Kingaroy 4610, Mundubbera 4626"),
 ("Gympie region", rng(4570,4580,4581), ["Gympie (R)"], "Gympie 4570, Tin Can Bay 4580"),
 ("Sunshine Coast & Noosa", rng((4550,4569),(4571,4575)), ["Sunshine Coast (R)","Noosa (S)"], "Caloundra 4551, Maleny 4552, Nambour 4560, Noosa 4566"),
 ("Townsville, Burdekin & Charters Towers", rng((4806,4824),(4849,4850)), ["Townsville (C)","Burdekin (S)","Charters Towers (R)","Hinchinbrook (S)"], "Townsville 4810-4818, Ayr 4807, Charters Towers 4820"),
 ("Cairns, Tablelands & Far North", rng((4851,4895)), ["Cairns (R)","Tablelands (R)","Mareeba (S)","Cassowary Coast (R)","Douglas (S)","Cook (S)","Weipa (T)","Yarrabah (S)"], "Cairns 4870, Atherton/Tolga 4882-4883, Mareeba 4880, Innisfail 4860"),
 ("Outback (Mt Isa, Longreach etc.)", rng((4725,4736),(4825,4830)), ["Mount Isa (C)","Longreach (R)","Winton (S)","Cloncurry (S)","Barcaldine (R)","Blackall-Tambo (R)","Boulia (S)","McKinlay (S)","Flinders (S)","Richmond (S)","Carpentaria (S)","Burke (S)","Diamantina (S)","Barcoo (S)"], "Mount Isa 4825, Longreach 4730, Winton 4735, Barcaldine 4725"),
 ("SEQ fringe: Scenic Rim, Somerset & rural Logan/Ipswich", rng((4270,4287),(4306,4314)), ["Scenic Rim (R)","Somerset (R)"], "Jimboomba 4280, Beaudesert 4285, Tamborine 4272, Fernvale/Lowood 4306-4312"),
 ("Gold Coast", rng((4208,4230)), ["Gold Coast (C)"], "Gold Coast 4208-4230"),
]
METRO = rng((4000,4207),(4300,4305),(4500,4519))

units = {}; orders = {}
for t in open("qld_units_since_mar.txt").read().split():
    pc, o, u = t.split(":"); units[int(pc)] = int(u); orders[int(pc)] = int(o)
mix = {}
for t in open("qld_variant_since_aug.txt").read().split():
    pc, v, u = t.split(":"); mix.setdefault(int(pc), {}).setdefault(v, 0); mix[int(pc)][v] += int(u)

QLD_POP = pop["Queensland"]; TOT = sum(units.values())
assigned = set(); out = []
for name, pcs, lgas, eg in CLUSTERS:
    u = sum(units.get(p, 0) for p in pcs); o = sum(orders.get(p, 0) for p in pcs)
    pp = sum(pop[l] for l in lgas)
    m = {k: sum(mix.get(p, {}).get(k, 0) for p in pcs) for k in "ORGCP"}; mt = sum(m.values())
    top = sorted(((units.get(p, 0), p) for p in pcs if units.get(p, 0)), reverse=True)[:5]
    out.append({"region": name, "units": u, "orders": o, "pop": pp, "per_100k": round(u * 1e5 / pp, 1),
                "share_of_qld_units": round(100 * u / TOT, 1), "share_of_qld_pop": round(100 * pp / QLD_POP, 1),
                "index_vs_qld": round((u / TOT) / (pp / QLD_POP) * 100),
                "mix_since_aug_n": mt, "mix_%": {k: round(100 * v / mt) if mt else 0 for k, v in m.items()},
                "top_postcodes": [f"{p} ({n})" for n, p in top], "towns": eg})
    assigned |= pcs
mu = sum(units.get(p, 0) for p in METRO)
mpop = pop["Brisbane (C)"] + pop["Moreton Bay (C)"] + pop["Logan (C)"] + pop["Ipswich (C)"] + pop["Redland (C)"]
out.append({"region": "Greater Brisbane (metro postcodes)", "units": mu, "pop": mpop, "per_100k": round(mu * 1e5 / mpop, 1),
            "share_of_qld_units": round(100 * mu / TOT, 1), "share_of_qld_pop": round(100 * mpop / QLD_POP, 1),
            "index_vs_qld": round((mu / TOT) / (mpop / QLD_POP) * 100)})
assigned |= METRO
other = sum(u for p, u in units.items() if p not in assigned)
print(json.dumps({"qld_units": TOT, "unassigned_units": other, "regions": sorted(out, key=lambda r: -r["per_100k"])}, indent=1))
