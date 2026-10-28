#!/usr/bin/env python3
"""Variant/colour mix by state and metro vs regional, 6 Aug to 12 Oct 2026 (both variants on sale). Units (net items sold)."""
import json
V = ["OG", "Orange", "Grey", "Camo", "Pink"]
T = {"QLD": [73,119,75,67,37], "NSW": [89,85,90,41,35], "VIC": [65,71,39,40,17], "WA": [57,43,48,24,19],
     "SA": [30,31,16,11,5], "TAS": [7,4,5,2,1], "NT": [3,3,3,4,6], "ACT": [3,3,2,1,0]}
M = {"WA": [31,25,20,14,13], "QLD": [13,31,11,11,3], "VIC": [27,27,11,21,5], "NSW": [27,18,20,13,5],
     "SA": [12,11,4,1,1], "ACT": [3,3,2,1,0], "NT": [0,3,1,3,2], "TAS": [1,0,2,0,0]}
nat = [sum(T[s][i] for s in T) for i in range(5)]; N = sum(nat)
natmix = [x / N for x in nat]
def mix(row):
    t = sum(row); return [100 * x / t for x in row], t
out = {"national": {"units": N, "mix_%": dict(zip(V, [round(100 * x, 1) for x in natmix]))}}
for s in T:
    m, t = mix(T[s])
    out[s] = {"units": t, "mix_%": dict(zip(V, [round(x, 1) for x in m])),
              "index_vs_national": dict(zip(V, [round(m[i] / (100 * natmix[i]) * 100) for i in range(5)]))}
mt = [sum(M[s][i] for s in M) for i in range(5)]; rt = [nat[i] - mt[i] for i in range(5)]
for lab, row in (("capital", mt), ("regional", rt)):
    m, t = mix(row)
    out[lab] = {"units": t, "mix_%": dict(zip(V, [round(x, 1) for x in m])),
                "index_vs_national": dict(zip(V, [round(m[i] / (100 * natmix[i]) * 100) for i in range(5)]))}
for s in ["QLD", "NSW", "VIC", "WA", "SA"]:
    for lab, row in (("capital", M[s]), ("regional", [T[s][i] - M[s][i] for i in range(5)])):
        m, t = mix(row); out[f"{s} {lab}"] = {"units": t, "mix_%": dict(zip(V, [round(x) for x in m]))}
print(json.dumps(out, indent=1))
