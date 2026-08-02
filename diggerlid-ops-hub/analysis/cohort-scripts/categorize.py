import json, glob, collections
from math import sqrt, erf
files = sorted(glob.glob("pages/page*.json"))

def wilson(k,n,zc=1.96):
    if n==0: return (0,0,0)
    p=k/n; d=1+zc**2/n
    c=(p+zc**2/(2*n))/d
    h=zc*sqrt(p*(1-p)/n+zc**2/(4*n**2))/d
    return p,(c-h),(c+h)

IGNORE_SUBSTR = ["package protection","package insurance","return shipping","retrurn","custom sale","tip","donation"]
def is_ignored(t):
    tl=t.strip().lower()
    if tl in ("test","tip","donation"): return True
    return any(s in tl for s in IGNORE_SUBSTR)

def category(t):
    tl=t.lower().strip()
    if is_ignored(t): return "ignore"
    if "gwp" in tl: return "ignore"          # free gift-with-purchase, not intent
    # GREASE
    if "coupler" in tl or "kajo" in tl or "grease" in tl or "cartridge" in tl: return "grease"
    # PORTABLE (mats / hauler)
    if "mat" in tl or "hauler" in tl: return "portable"
    # ACCESSORIES
    if ("cradle" in tl or "phone holder" in tl or "caddy" in tl or "coupling cap" in tl
        or "bottle opener" in tl or "wipes" in tl): return "accessory"
    # APPAREL / MERCH
    if any(w in tl for w in ["cap","beanie","hoodie"," tee","work tee","dighead"]) and "coupling cap" not in tl: return "merch"
    # COVERS (fitted covers/enclosures + machine-code SKUs)
    if any(w in tl for w in ["cover","enclosure","digger lid","diggershield","draw bar",
                              "quicky","meglodon","ghoti","lzr2","casex"]): return "covers"
    return "other"

def order_lines(o): return o["lineItems"]["nodes"]
def line_amt(li): return float(li["originalTotalSet"]["shopMoney"]["amount"])
def order_total(o): return sum(line_amt(li) for li in order_lines(o))

def order_is_real(o):
    items=order_lines(o)
    if not items: return False
    if order_total(o)<=1.01: return False
    if all(li["title"].strip().lower()=="test" for li in items): return False
    return True

def first_cat(o):
    # primary intent = highest-value non-ignored line
    cand=[(line_amt(li),category(li["title"])) for li in order_lines(o) if category(li["title"])!="ignore"]
    cand=[c for c in cand if c[1] not in ("other",)] or cand
    if not cand: return "other"
    cand.sort(reverse=True)
    return cand[0][1]

def order_cats(o, exclude_ignore=True):
    s=set()
    for li in order_lines(o):
        c=category(li["title"])
        if exclude_ignore and c in ("ignore","other"): continue
        s.add(c)
    return s
def order_cats_over100(o):
    s=set()
    for li in order_lines(o):
        c=category(li["title"])
        if c in ("ignore","other"): continue
        if line_amt(li)>100.0: s.add(c)
    return s

# load unique customers
custs={}
for f in files:
    for node in json.load(open(f))["data"]["customers"]["nodes"]:
        custs[node["id"]]=node

WIN_LO,WIN_HI="2025-08-01","2025-10-31"
cats=["grease","covers","portable","accessory","merch","other"]
stat={c:{"n":0,"repurch":0,"xsell":0,"xsell100":0} for c in cats}
qual=0
for node in custs.values():
    orders=[o for o in node["orders"]["nodes"] if order_is_real(o)]
    orders.sort(key=lambda o:o["createdAt"])
    if not orders: continue
    first=orders[0]
    d=first["createdAt"][:10]
    if not (WIN_LO<=d<=WIN_HI): continue
    qual+=1
    fc=first_cat(first)
    later=orders[1:]
    repurch = len(later)>0
    # cross-sell: later order containing a DIFFERENT category than first
    xsell = any((order_cats(o)-{fc}) for o in later)
    xsell100 = any((order_cats_over100(o)-{fc}) for o in later)
    st=stat[fc]
    st["n"]+=1; st["repurch"]+=repurch; st["xsell"]+=xsell; st["xsell100"]+=xsell100

print(f"QUALIFYING COHORT: {qual}   (sum of categories = {sum(stat[c]['n'] for c in cats)})\n")
hdr="first-cat    n  |      repurchase        |   cross-sell(diff cat)   |  x-sell over100 diff | power"
print(hdr); print("-"*len(hdr))
def fmt(k,n):
    p,lo,hi=wilson(k,n); return f"{p*100:5.1f}%  [{lo*100:4.1f},{hi*100:4.1f}]"
for c in cats:
    s=stat[c]; n=s["n"]
    if n==0: continue
    power = "well-powered" if n>=100 else ("directional" if n>=30 else "UNDERPOWERED")
    print(f"{c:10s} {n:4d} | {fmt(s['repurch'],n)} | {fmt(s['xsell'],n)} | {fmt(s['xsell100'],n)} | {power}")

# pairwise: repurchase grease vs covers; xsell grease vs covers
def twoprop(k1,n1,k2,n2):
    p1,p2=k1/n1,k2/n2; pp=(k1+k2)/(n1+n2)
    se=sqrt(pp*(1-pp)*(1/n1+1/n2)); z=(p1-p2)/se
    pv=2*(1-0.5*(1+erf(abs(z)/sqrt(2))))
    return p1,p2,z,pv
print("\nKey significance tests:")
for lab,a,b in [("repurchase","repurch","repurch"),("cross-sell diff-cat","xsell","xsell"),("x-sell >$100","xsell100","xsell100")]:
    g,c=stat["grease"],stat["covers"]
    p1,p2,z,pv=twoprop(g[a],g["n"],c[b],c["n"])
    print(f"  {lab:20s} grease {p1*100:.1f}% vs covers {p2*100:.1f}%  z={z:+.2f} p={pv:.4f} {'SIG' if pv<0.05 else 'ns'}")
