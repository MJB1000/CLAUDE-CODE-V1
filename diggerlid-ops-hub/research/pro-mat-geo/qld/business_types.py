#!/usr/bin/env python3
"""PRO Mat buyers by likely business type, from a Shopify order export CSV.

Usage: python3 business_types.py orders_export.csv [STATE]   (STATE defaults to QLD)

Run it locally on the raw export. It prints aggregate counts only and writes nothing,
so no emails or names leave your machine. Classification priority per order:
  1. Shipping or billing Company field (primary)
  2. Business email domain (not gmail, bigpond etc.)
  3. Trade word in the email (e.g. derwentcivil@yahoo) -> "likely business"
"""
import csv, re, sys
from collections import Counter

PRO_SKUS = {"DLPROM1980", "DLPROM1984", "DLPROM1985", "DLPROM1986", "DLPROM1987"}
PERSONAL = ("gmail.", "hotmail.", "outlook.", "live.", "icloud.", "me.com", "yahoo.", "bigpond.", "optusnet.",
            "iinet.", "westnet.", "tpg.", "internode.", "dodo.", "aapt.", "msn.", "protonmail.", "skymesh.")
TRADES = [  # first match wins, so specific before generic
    ("Civil, earthmoving & excavation", r"civil|earthmov|excavat|bobcat|digger|dozer|grader|plant ?hire|haulage|quarr|demoli"),
    ("Mechanical, diesel & automotive", r"mech|diesel|hydraul|auto|motor|engine|truck|trailer|tyre|fitter|repair|service ?cent|power equip"),
    ("Farming, agriculture & turf", r"farm|agri|ag[ -]|crop|cattle|grazing|pastoral|station|turf|dairy|poultry|orchard|vine|seed|feed|rice|cotton|grain"),
    ("Plumbing, electrical & building trades", r"plumb|drain|electr|sparky|build|construct|carpent|roof|concret|fenc|weld|fabricat|steel|paint|tiling"),
    ("Landscaping & gardening", r"landscap|garden|tree|arbor|mow|lawn|irrigat|nursery"),
    ("Mining & resources", r"mining|mine|resource|drill|blast|minerals"),
    ("Transport & logistics", r"transport|logistic|freight|tow|courier"),
    ("Animal & equine", r"equine|canine|vet|horse|pet|kennel|stable"),
    ("Hospitality & retail", r"coffee|cafe|bean|bakery|food|store|shop|retail"),
]
GENERIC_BIZ = r"pty|ltd|p/l|industr|services|solutions|group|contract|enterpris|co\b|company|trading"

def kind(text):
    t = text.lower()
    for name, rx in TRADES:
        if re.search(rx, t): return name
    return None

def classify(email, company):
    email = (email or "").strip().lower()
    local, _, domain = email.partition("@")
    company = (company or "").strip()
    if company:
        return "company field", kind(company) or kind(domain) or "Other or unclear business"
    if domain and not domain.startswith(PERSONAL):
        return "business domain", kind(domain) or kind(local) or "Other or unclear business"
    k = kind(local)
    if k or re.search(GENERIC_BIZ, local):
        return "trade word in email", k or "Other or unclear business"
    return None, None

def main():
    path = sys.argv[1]; state = (sys.argv[2] if len(sys.argv) > 2 else "QLD").upper()
    orders = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            o = orders.setdefault(r["Name"], {"email": "", "co": "", "prov": "", "pro": False})
            o["email"] = o["email"] or r.get("Email", "")
            o["co"] = o["co"] or r.get("Shipping Company", "") or r.get("Billing Company", "")
            o["prov"] = o["prov"] or r.get("Shipping Province", "")
            if r.get("Lineitem sku", "").strip().upper() in PRO_SKUS: o["pro"] = True
    sel = [o for o in orders.values() if o["pro"] and o["prov"].upper() == state]
    src, typ = Counter(), Counter()
    for o in sel:
        s, t = classify(o["email"], o["co"])
        if s: src[s] += 1; typ[t] += 1
    n, b = len(sel), sum(src.values())
    print(f"{state} PRO Mat orders: {n}")
    print(f"Likely business buyers: {b} ({b / n * 100:.0f}%)" if n else "No orders matched")
    print("\nBy evidence:"); [print(f"  {k:24} {v}") for k, v in src.most_common()]
    print("\nBy business type:"); [print(f"  {k:40} {v:4}  {v / b * 100:4.0f}%") for k, v in typ.most_common()]

if __name__ == "__main__":
    main()
