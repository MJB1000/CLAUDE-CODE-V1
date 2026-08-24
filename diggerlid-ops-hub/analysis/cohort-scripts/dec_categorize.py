import json, glob, sys
from math import sqrt, erf
files = sorted(glob.glob("pages_dec/page*.json"))
def wilson(k,n,zc=1.96):
    if n==0: return (0,0,0)
    p=k/n; d=1+zc**2/n
    c=(p+zc**2/(2*n))/d; h=zc*sqrt(p*(1-p)/n+zc**2/(4*n**2))/d
    return p,c-h,c+h
IGN=["package protection","package insurance","return shipping","retrurn","custom sale","tip","donation"]
def is_ign(t):
    tl=t.strip().lower()
    if tl in("test","tip","donation"): return True
    return any(s in tl for s in IGN)
def cat(t):
    tl=t.lower().strip()
    if is_ign(t): return "ignore"
    if "gwp" in tl: return "ignore"
    if "coupler" in tl or "kajo" in tl or "grease" in tl or "cartridge" in tl: return "grease"
    if "mat" in tl or "hauler" in tl: return "portable"
    if ("cradle" in tl or "phone holder" in tl or "caddy" in tl or "coupling cap" in tl or "bottle opener" in tl or "wipes" in tl): return "accessory"
    if any(w in tl for w in ["beanie","hoodie","work tee"," tee","trucker cap","dighead"]) and "coupling cap" not in tl: return "merch"
    if any(w in tl for w in ["cover","enclosure","digger lid","diggershield","draw bar","quicky","meglodon","ghoti","lzr2","casex"]): return "covers"
    return "other"
def amt(li): return float(li["originalTotalSet"]["shopMoney"]["amount"])
def ototal(o): return sum(amt(li) for li in o["lineItems"]["nodes"])
def real(o):
    it=o["lineItems"]["nodes"]
    if not it or ototal(o)<=1.01: return False
    if all(li["title"].strip().lower()=="test" for li in it): return False
    return True
def firstcat(o):
    c=[(amt(li),cat(li["title"])) for li in o["lineItems"]["nodes"] if cat(li["title"])!="ignore"]
    c=[x for x in c if x[1]!="other"] or c
    if not c: return "other"
    c.sort(reverse=True); return c[0][1]
def ocats(o):
    return {cat(li["title"]) for li in o["lineItems"]["nodes"] if cat(li["title"]) not in ("ignore","other")}
def has_over100(o):
    return any(amt(li)>100 for li in o["lineItems"]["nodes"] if cat(li["title"]) not in ("ignore",))
custs={}
for f in files:
    for n in json.load(open(f))["data"]["customers"]["nodes"]:
        custs[n["id"]]=n
LO,HI="2025-11-28","2026-02-28"
cats=["grease","covers","portable","accessory","merch","other"]
S={c:{"n":0,"rep":0,"xs":0,"hvr":0} for c in cats}
qual=0; integ_bad=0
for n in custs.values():
    ords=[o for o in n["orders"]["nodes"] if real(o)]
    ords.sort(key=lambda o:o["createdAt"])
    # integrity: returned order nodes vs numberOfOrders (cap 12)
    exp=min(int(n["numberOfOrders"]),12); got=len(n["orders"]["nodes"])
    if got!=exp: integ_bad+=1
    if not ords: continue
    d=ords[0]["createdAt"][:10]
    if not (LO<=d<=HI): continue
    qual+=1
    fc=firstcat(ords[0]); later=ords[1:]
    S[fc]["n"]+=1
    S[fc]["rep"]+= (len(later)>0)
    S[fc]["xs"]+= any(ocats(o)-{fc} for o in later)
    S[fc]["hvr"]+= any(has_over100(o) for o in later)
print(f"files={len(files)} unique_custs={len(custs)} qualifying={qual} integrity_mismatch={integ_bad}")
print(f"{'cat':10s}{'n':>5s}{'repurch':>18s}{'crosssell':>18s}{'HV-repurch':>18s}")
for c in cats:
    s=S[c]; n=s["n"]
    if n==0: continue
    def fm(k): 
        p,lo,hi=wilson(k,n); return f"{p*100:4.1f}% [{lo*100:.0f},{hi*100:.0f}]"
    print(f"{c:10s}{n:5d}{fm(s['rep']):>18s}{fm(s['xs']):>18s}{fm(s['hvr']):>18s}")
