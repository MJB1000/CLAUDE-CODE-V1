#!/usr/bin/env python3
"""Build the DiggerLid product reference catalogue from the Shopify products.json.

- Downloads up to N images per product into
  clients/assets/diggerlid/products/catalogue/<handle>/
- Writes product-catalogue.json (machine-readable map for auto_refs)
- Writes PRODUCT-CATALOGUE.md (human-readable index)

Each product gets curated alias/trigger words so a phrase like 'add in a
Hauler Bag' resolves to the right image set.
"""

import json
import re
import time
import urllib.request
from pathlib import Path

SRC_JSON = Path("/tmp/diggerlid-products.json")
REPO = Path("/home/user/CLAUDE-CODE-V1")
CAT_DIR = REPO / "clients/assets/diggerlid/products/catalogue"
JSON_OUT = REPO / "clients/assets/diggerlid/product-catalogue.json"
MD_OUT = REPO / "clients/assets/diggerlid/PRODUCT-CATALOGUE.md"
BASE_URL = "https://diggerlid.com/products/"
MAX_IMAGES = 4  # per product

# Intelligent grouping: handle -> category
CATEGORY = {
    "pro-excavator-enclosure": "covers-enclosures",
    "diggerlid-digger-shield-kit": "covers-enclosures",
    "universal-engine-covers": "covers-enclosures",
    "skid-steer-loader-cover": "covers-enclosures",
    "diggerlid-1-tonne-excavator-cover": "covers-enclosures",
    "diggerlid-mini-loader-cover": "covers-enclosures",
    "digger-lid-1-7": "covers-enclosures",
    "digger-lid-quicky-cover": "covers-enclosures",
    "draw-bar-cover": "covers-enclosures",
    "kajo-two-handed-grease-gun": "grease-lubrication",
    "kajo-adapter": "grease-lubrication",
    "kajo-grease-cartridge-lzr2-ep2": "grease-lubrication",
    "grease-coupler": "grease-lubrication",
    "quicky-combo-1": "grease-lubrication",
    "the-hauler-luggage-bag": "storage-mats",
    "pro-mat": "storage-mats",
    "drink-tool-caddy": "storage-mats",
    "work-tee": "apparel",
    "diggerlid-trucker-cap": "apparel",
    "diggerlid-workwear-hoodie": "apparel",
    "diggerlid-beanie": "apparel",
    "diggerwipes": "accessories-novelty",
    "excavator-boom-bottle-opener": "accessories-novelty",
    "diggerlid-hydraulic-coupling-cap-set": "accessories-novelty",
    "excavator-phone-cradle": "accessories-novelty",
    "extras-pack": "bundles",
}

# Curated natural-language aliases / trigger words per handle. The first phrase
# is canonical; the rest are how a person might casually refer to the product.
ALIASES = {
    "pro-excavator-enclosure": ["pro enclosure", "pro excavator enclosure", "excavator enclosure", "diggerlid pro"],
    "diggerlid-digger-shield-kit": ["diggershield", "digger shield", "diggershield kit", "shield kit"],
    "universal-engine-covers": ["universal cover", "engine cover", "universal engine cover"],
    "skid-steer-loader-cover": ["skid steer cover", "skid steer loader cover", "skid steer"],
    "diggerlid-1-tonne-excavator-cover": ["micro excavator cover", "1 tonne cover", "micro cover"],
    "diggerlid-mini-loader-cover": ["mini loader cover", "mini loader"],
    "digger-lid-1-7": ["1.7 tonne cover", "1.7t excavator cover", "1.7 tonne excavator cover"],
    "digger-lid-quicky-cover": ["quicky cover", "quicky"],
    "draw-bar-cover": ["drawbar cover", "draw bar cover", "draw bar", "drawbar"],
    "kajo-two-handed-grease-gun": ["kajo grease gun", "kajo gun", "grease gun", "kajo"],
    "kajo-adapter": ["kajo adapter", "battery grease gun adapter", "grease gun adapter"],
    "kajo-grease-cartridge-lzr2-ep2": ["kajo grease packs", "grease cartridge", "grease pack", "lzr2", "hd800"],
    "grease-coupler": ["grease coupler", "quick release coupler", "coupler"],
    "quicky-combo-1": ["quicky combo", "grease combo"],
    "the-hauler-luggage-bag": ["hauler bag", "the hauler", "hauler", "luggage bag", "kit bag"],
    "pro-mat": ["pro mat", "magnet mat", "padded mat", "work mat"],
    "drink-tool-caddy": ["drink caddy", "tool caddy", "drink/tool caddy", "caddy"],
    "work-tee": ["work tee", "work t-shirt", "diggerlid tee", "tee"],
    "diggerlid-trucker-cap": ["trucker cap", "diggerlid cap", "cap"],
    "diggerlid-workwear-hoodie": ["work hoodie", "diggerlid hoodie", "hoodie"],
    "diggerlid-beanie": ["beanie", "dighead beanie"],
    "diggerwipes": ["digger wipes", "diggerwipes", "wipes", "cleaning wipes"],
    "excavator-boom-bottle-opener": ["bottle opener", "boom bottle opener", "excavator bottle opener"],
    "diggerlid-hydraulic-coupling-cap-set": ["coupling cap set", "hydraulic cap set", "coupling caps"],
    "excavator-phone-cradle": ["phone cradle", "excavator phone cradle", "phone holder"],
    "extras-pack": ["digheads bundle", "dighead's bundle", "extras pack"],
}

CATEGORY_LABELS = {
    "covers-enclosures": "Covers & Enclosures",
    "grease-lubrication": "Grease & Lubrication",
    "storage-mats": "Storage, Bags & Mats",
    "apparel": "Apparel",
    "accessories-novelty": "Accessories & Novelty",
    "bundles": "Bundles",
}


def slug_image_url(src, width=1200):
    """Append a width param to a Shopify CDN image URL to cap download size."""
    sep = "&" if "?" in src else "?"
    return f"{src}{sep}width={width}"


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    dest.write_bytes(data)
    return len(data)


def main():
    data = json.load(open(SRC_JSON))
    products = data.get("products", [])
    catalogue = {
        "source": "https://diggerlid.com",
        "fetched": "2026-05-21",
        "note": "Auto-built from Shopify products.json. Image paths are repo-relative. "
                "Use the aliases to resolve a casual product mention to its image set.",
        "categories": {},
        "products": {},
    }

    # group handles by category
    for cat in CATEGORY_LABELS:
        catalogue["categories"][cat] = []

    for p in products:
        handle = p["handle"]
        cat = CATEGORY.get(handle, "accessories-novelty")
        title = p["title"].strip()
        variants = p.get("variants", [])
        price = variants[0].get("price", "") if variants else ""
        images = p.get("images", [])

        out_dir = CAT_DIR / handle
        out_dir.mkdir(parents=True, exist_ok=True)

        saved = []
        for i, img in enumerate(images[:MAX_IMAGES], 1):
            src = img.get("src")
            if not src:
                continue
            ext = ".png" if ".png" in src.lower().split("?")[0] else ".jpg"
            name = f"{i:02d}-featured{ext}" if i == 1 else f"{i:02d}{ext}"
            dest = out_dir / name
            try:
                n = download(slug_image_url(src), dest)
                saved.append(str(dest.relative_to(REPO)))
                print(f"  {handle}/{name}  ({n:,}b)", flush=True)
            except Exception as e:
                print(f"  FAILED {handle} img{i}: {e}", flush=True)
            time.sleep(0.2)

        catalogue["categories"][cat].append(handle)
        catalogue["products"][handle] = {
            "title": title,
            "handle": handle,
            "category": cat,
            "type": p.get("product_type", ""),
            "price_aud": price,
            "url": BASE_URL + handle,
            "aliases": ALIASES.get(handle, [title.lower()]),
            "total_images_on_site": len(images),
            "images": saved,
        }

    JSON_OUT.write_text(json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {JSON_OUT.relative_to(REPO)}")

    # Build the markdown index
    lines = [
        "# DiggerLid Product Reference Catalogue",
        "",
        f"> Auto-built from {catalogue['source']} (Shopify `products.json`), fetched {catalogue['fetched']}.",
        f"> {len(catalogue['products'])} products across {len(CATEGORY_LABELS)} categories.",
        "",
        "**How this is used:** when you mention a product (e.g. \"add in a Hauler Bag\"), "
        "the matching `aliases` resolve to that product's image set under "
        "`clients/assets/diggerlid/products/catalogue/<handle>/`. Those images are then "
        "attached as Gemini reference images for the prompt — same mechanism as the "
        "`auto_refs` rules in the storyboard manifests.",
        "",
        "Machine-readable map: `clients/assets/diggerlid/product-catalogue.json`",
        "",
    ]
    for cat, label in CATEGORY_LABELS.items():
        handles = catalogue["categories"].get(cat, [])
        if not handles:
            continue
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| Product | Price | Images | Say any of… |")
        lines.append("|---|---|---|---|")
        for h in handles:
            pr = catalogue["products"][h]
            aliases = ", ".join(f"`{a}`" for a in pr["aliases"])
            lines.append(f"| [{pr['title']}]({pr['url']}) | ${pr['price_aud']} | {len(pr['images'])} | {aliases} |")
        lines.append("")

    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {MD_OUT.relative_to(REPO)}")

    total_imgs = sum(len(pr["images"]) for pr in catalogue["products"].values())
    print(f"\nCatalogued {len(catalogue['products'])} products, {total_imgs} reference images downloaded.")


if __name__ == "__main__":
    main()
