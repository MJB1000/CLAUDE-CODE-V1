"""Compose the 11 storyboard frames into A4 pages — 3x2 grid per page,
2 pages, labeled beats, multi-page PDF + per-page PNGs for download."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# A4 portrait at 300 DPI
PAGE_W, PAGE_H = 2480, 3508
MARGIN = 80
HEADER_H = 140
COLS, ROWS = 3, 2
LABEL_H = 100
H_GUTTER = 30
V_GUTTER = 50

usable_w = PAGE_W - 2*MARGIN - (COLS-1)*H_GUTTER
CELL_W = usable_w // COLS
CELL_H = CELL_W * 16 // 9  # 9:16 portrait frames

FRAME_DIR = Path("deliverables/diggerlid-pro-60s-storyboard")
OUT_DIR = Path("deliverables/diggerlid-pro-60s-storyboard-a4")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BEATS = [
    ("01-A-hero-hook.png",          "A",  "HERO HOOK"),
    ("02-B-problem-empty-box.png",  "B",  "PROBLEM"),
    ("03-C-villain-tarp-fails.png", "C",  "VILLAIN · TARP FAILS"),
    ("04-D-three-things.png",       "D",  "THREE THINGS"),
    ("05-E-diggerlid-born.png",     "E",  "DIGGERLID BORN"),
    ("06-F-feature-demo.png",       "F",  "FEATURE DEMO"),
    ("07-G-materials-nullarbor.png","G",  "MATERIALS · NULLARBOR"),
    ("08-H-ugc-heritage.png",       "H",  "HERITAGE · UGC"),
    ("09-I-track-test.png",         "I",  "TRACK TEST"),
    ("10-J-trojan-horse.png",       "J",  "TROJAN HORSE PIVOT"),
    ("11-K-finisher.png",           "K",  "FINISHER"),
]

PAGES = [BEATS[:6], BEATS[6:]]

FONT_PATH = "/tmp/fonts/Outfit.ttf"
title_font  = ImageFont.truetype(FONT_PATH, 56)
beat_font   = ImageFont.truetype(FONT_PATH, 44)
desc_font   = ImageFont.truetype(FONT_PATH, 32)
footer_font = ImageFont.truetype(FONT_PATH, 28)

YELLOW = (245, 235, 25)
NAVY = (20, 24, 38)
WHITE = (255, 255, 255)
PAPER = (252, 252, 248)
GREY = (90, 90, 100)
BORDER = (140, 140, 145)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


pages_imgs = []
for page_num, page_beats in enumerate(PAGES, 1):
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # Header: thin yellow accent bar + title
    draw.rectangle([MARGIN, MARGIN, MARGIN + 80, MARGIN + 8], fill=YELLOW)
    title = "DIGGERLID PRO · 60-SECOND STORYBOARD"
    draw.text((MARGIN, MARGIN + 30), title, fill=NAVY, font=title_font)

    # Place frames
    grid_top = MARGIN + HEADER_H
    for i, (fname, beat_id, beat_title) in enumerate(page_beats):
        col = i % COLS
        row = i // COLS
        x = MARGIN + col * (CELL_W + H_GUTTER)
        y = grid_top + row * (CELL_H + LABEL_H + V_GUTTER)

        # Frame image
        frame = Image.open(FRAME_DIR / fname).convert("RGB")
        frame = frame.resize((CELL_W, CELL_H), Image.LANCZOS)
        page.paste(frame, (x, y))
        draw.rectangle([x, y, x + CELL_W, y + CELL_H], outline=BORDER, width=2)

        # Label area below frame: navy badge for beat id + title text
        label_y = y + CELL_H + 20
        # Beat ID badge
        badge_w, badge_h = 70, 60
        draw.rectangle([x, label_y, x + badge_w, label_y + badge_h], fill=NAVY)
        bw, bh = measure(draw, beat_id, beat_font)
        draw.text((x + (badge_w - bw) // 2, label_y + (badge_h - bh) // 2 - 6),
                  beat_id, fill=YELLOW, font=beat_font)
        # Title next to badge
        draw.text((x + badge_w + 16, label_y + (badge_h - 30) // 2),
                  beat_title, fill=NAVY, font=desc_font)

    # Footer: project name + page number
    footer_y = PAGE_H - MARGIN - 40
    draw.line([MARGIN, footer_y - 16, PAGE_W - MARGIN, footer_y - 16], fill=BORDER, width=1)
    draw.text((MARGIN, footer_y), "diggerlid-pro-60s-storyboard", fill=GREY, font=footer_font)
    page_text = f"Page {page_num} of {len(PAGES)}"
    pw, _ = measure(draw, page_text, footer_font)
    draw.text((PAGE_W - MARGIN - pw, footer_y), page_text, fill=GREY, font=footer_font)

    png_path = OUT_DIR / f"page-{page_num}.png"
    page.save(png_path, "PNG", optimize=True)
    print(f"Wrote {png_path} ({png_path.stat().st_size:,} bytes)")
    pages_imgs.append(page)

# Multi-page PDF
pdf_path = OUT_DIR / "diggerlid-pro-60s-storyboard.pdf"
pages_imgs[0].save(pdf_path, "PDF", resolution=300, save_all=True, append_images=pages_imgs[1:])
print(f"Wrote {pdf_path} ({pdf_path.stat().st_size:,} bytes)")

# Also bundle a zip of the page PNGs + PDF
import zipfile
zip_path = OUT_DIR.parent / "diggerlid-pro-60s-storyboard-a4.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT_DIR.iterdir()):
        z.write(p, arcname=p.name)
print(f"Wrote {zip_path} ({zip_path.stat().st_size:,} bytes)")
