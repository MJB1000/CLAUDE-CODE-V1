#!/usr/bin/env python3
"""
DiggerLid email holdout — deterministic assignment.

Reads a Klaviyo CSV export of the ACTIVE/mailable segment, assigns each profile
to control/treatment by a stable hash of its email, and writes a CSV you re-import
into Klaviyo (which sets the custom property, matched on email).

Deterministic: the same email always lands in the same bucket, so re-running is
safe and new signups self-assign when you re-export/re-import. No secrets used —
operates only on the local CSV.

Usage:
  python3 holdout_assign.py active_export.csv                # -> holdout_out.csv, 10% control
  python3 holdout_assign.py active_export.csv --pct 10 --prop ho_campaign --out holdout_out.csv

Then in Klaviyo: import holdout_out.csv, map the `<prop>` column to a custom
property, and build the segments described in the runbook.
"""
import csv, hashlib, argparse, sys

def bucket(email: str) -> int:
    e = (email or "").strip().lower()
    return int(hashlib.md5(e.encode("utf-8")).hexdigest(), 16) % 100

def find_email_col(header):
    for i, h in enumerate(header):
        if h and h.strip().lower() in ("email", "email address", "$email"):
            return i
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", help="Klaviyo CSV export of the ACTIVE segment (must contain an Email column)")
    ap.add_argument("--pct", type=int, default=10, help="control %% (default 10)")
    ap.add_argument("--prop", default="ho_campaign", help="property/column name (default ho_campaign)")
    ap.add_argument("--out", default="holdout_out.csv")
    a = ap.parse_args()

    with open(a.infile, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit("empty file")
    header = rows[0]
    ei = find_email_col(header)
    if ei is None:
        sys.exit("no Email column found in: " + ", ".join(header[:12]))

    n = c = t = dup = 0
    seen = set()
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Email", a.prop, "ho_bucket"])
        for r in rows[1:]:
            if len(r) <= ei:
                continue
            email = (r[ei] or "").strip().lower()
            if not email or "@" not in email:
                continue
            if email in seen:
                dup += 1
                continue
            seen.add(email)
            b = bucket(email)
            grp = "control" if b < a.pct else "treatment"
            w.writerow([email, grp, b])
            n += 1
            c += grp == "control"
            t += grp == "treatment"

    print(f"assigned {n} profiles  (dupes skipped: {dup})")
    print(f"  control   = {c}  ({c/n*100:.2f}%)")
    print(f"  treatment = {t}  ({t/n*100:.2f}%)")
    print(f"wrote -> {a.out}")

if __name__ == "__main__":
    main()
