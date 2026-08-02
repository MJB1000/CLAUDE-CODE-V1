import json, glob
from math import sqrt, erf
from datetime import datetime
def wilson(k,n,zc=1.96):
    if n==0: return (0,0,0)
    p=k/n;d=1+zc**2/n;c=(p+zc**2/(2*n))/d;h=zc*sqrt(p*(1-p)/n+zc**2/(4*n**2))/d
    return p,c-h,c+h
def twoprop(k1,n1,k2,n2):
    p1,p2=k1/n1,k2/n2;pp=(k1+k2)/(n1+n2)
    se=sqrt(pp*(1-pp)*(1/n1+1/n2));z=(p1-p2)/se
    return p1,p2,z,2*(1-0.5*(1+erf(abs(z)/sqrt(2))))
IGN=["package protection","package insurance","return shipping","retrurn","custom sale","tip","donation"]
def is_ign(t):
    tl=t.strip().lower()
    if tl in("test","tip","donation"):return True
    return any(s in tl for s in IGN)
def cat(t):
    tl=t.lower().strip()
    if is_ign(t) or "gwp" in tl:return "ignore"
    if "coupler" in tl or "kajo" in tl or "grease" in tl or "cartridge" in tl:return "grease"
    if "mat" in tl or "hauler" in tl:return "portable"
    if ("cradle" in tl or "phone holder" in tl or "caddy" in tl or "coupling cap" in tl or "bottle opener" in tl or "wipes" in tl):return "accessory"
    if any(w in tl for w in ["beanie","hoodie","work tee"," tee","trucker cap","dighead"]) and "coupling cap" not in tl:return "merch"
    if any(w in tl for w in ["cover","enclosure","digger lid","diggershield","draw bar","quicky","meglodon","ghoti","lzr2","casex"]):return "covers"
    return "other"
def amt(li):return float(li["originalTotalSet"]["shopMoney"]["amount"])
def ot(o):return sum(amt(li) for li in o["lineItems"]["nodes"])
def real(o):
    it=o["lineItems"]["nodes"]
    if not it or ot(o)<=1.01:return False
    if all(li["title"].strip().lower()=="test" for li in it):return False
    return True
def firstcat(o):
    c=[(amt(li),cat(li["title"])) for li in o["lineItems"]["nodes"] if cat(li["title"])!="ignore"]
    c=[x for x in c if x[1]!="other"] or c
    if not c:return "other"
    c.sort(reverse=True);return c[0][1]
def ocats(o):return {cat(li["title"]) for li in o["lineItems"]["nodes"] if cat(li["title"]) not in("ignore","other")}
def hv(o):return any(amt(li)>100 for li in o["lineItems"]["nodes"] if cat(li["title"])!="ignore")
def dt(s):return datetime.strptime(s[:10],"%Y-%m-%d")

def analyze(pattern, target_cat, lo, hi, cap_days=None):
    custs={}
    for f in glob.glob(pattern):
        for n in json.load(open(f))["data"]["customers"]["nodes"]:
            custs[n["id"]]=n
    n_=rep=xs=hvr=0
    for node in custs.values():
        ords=[o for o in node["orders"]["nodes"] if real(o)]
        ords.sort(key=lambda o:o["createdAt"])
        if not ords: continue
        d=ords[0]["createdAt"][:10]
        if not(lo<=d<=hi): continue
        fc=firstcat(ords[0])
        if fc!=target_cat: continue
        n_+=1
        f0=dt(ords[0]["createdAt"])
        later=[o for o in ords[1:] if (cap_days is None or (dt(o["createdAt"])-f0).days<=cap_days)]
        rep+= (len(later)>0)
        xs += any(ocats(o)-{fc} for o in later)
        hvr+= any(hv(o) for o in later)
    return n_,rep,xs,hvr

def show(lab,n,rep,xs,hvr):
    def fm(k):
        p,l,h=wilson(k,n);return f"{p*100:4.1f}% [{l*100:.0f}-{h*100:.0f}]"
    print(f"{lab:34s} n={n:3d} | repurch {fm(rep):16s} | cross-sell {fm(xs):15s} | HV-repurch {fm(hvr):16s}")

# MATS: Dec cohort, natural obs (~5-8mo, Dec-heavy)
m=analyze("pages_dec/page*.json","portable","2025-11-28","2026-02-28",cap_days=None)
# COVERS capped to 240d (~8mo) to match mats
c8=analyze("pages/page*.json","covers","2025-08-01","2025-10-31",cap_days=240)
# COVERS uncapped (full 9-12mo) for reference
cu=analyze("pages/page*.json","covers","2025-08-01","2025-10-31",cap_days=None)
print("HORIZON-MATCHED (~8-month observation window):")
show("MATS (Dec25-Feb26 acq)",*m)
show("COVERS (Aug-Oct25, capped 8mo)",*c8)
print("\nreference:")
show("COVERS (Aug-Oct25, full 9-12mo)",*cu)
print("\nSignificance MATS vs COVERS(8mo-capped):")
for i,lab in [(1,"repurchase"),(2,"cross-sell"),(3,"HV-repurchase")]:
    p1,p2,z,pv=twoprop(m[i],m[0],c8[i],c8[0])
    print(f"  {lab:14s} mats {p1*100:4.1f}% vs covers {p2*100:4.1f}%  z={z:+.2f} p={pv:.4f} -> {'SIG' if pv<0.05 else 'ns'}")
