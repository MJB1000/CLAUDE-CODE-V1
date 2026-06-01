"""Standard A4 storyboard PDF exporter.

Reads a JSON config describing the export (project title, frames with id +
title + caption + image path) and renders A4 portrait pages — 3x2 grid per
page — with image, beat ID badge, scene title, and one-line caption beneath
each frame. Outputs page PNGs, a multi-page PDF, and a bundled zip.

Standard schema (re-use this shape for every future PDF export):

    {
      "project": "<slug>",
      "title":   "<HEADER TEXT, ALL-CAPS, NAVY>",
      "version": "v1",
      "output_dir": "deliverables/<slug>-pdf",
      "frames": [
        {"id": "A",  "title": "HERO HOOK",
         "caption": "XE17U lands clean. Shutter-click cuts.",
         "image":   "deliverables/.../01-A-hero-hook.png"},
        ...
      ]
    }

Usage:
    python3 pdf-export.py --config <config.json>
"""

import argparse
import json
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[4]

PAGE_W, PAGE_H = 2480, 3508
MARGIN = 80
HEADER_H = 140
COLS, ROWS = 3, 2
LABEL_H = 180
H_GUTTER = 30
V_GUTTER = 60

usable_w = PAGE_W - 2 * MARGIN - (COLS - 1) * H_GUTTER
CELL_W = usable_w // COLS
CELL_H = CELL_W * 16 // 9

FONT_PATH = "/tmp/fonts/Outfit.ttf"
title_font = ImageFont.truetype(FONT_PATH, 56)
beat_font = ImageFont.truetype(FONT_PATH, 44)
scene_font = ImageFont.truetype(FONT_PATH, 30)
caption_font = ImageFont.truetype(FONT_PATH, 24)
footer_font = ImageFont.truetype(FONT_PATH, 28)

YELLOW = (245, 235, 25)
NAVY = (20, 24, 38)
PAPER = (252, 252, 248)
GREY = (90, 90, 100)
BORDER = (140, 140, 145)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        tw, _ = measure(draw, trial, font)
        if tw <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_page(page_frames, page_num, total_pages, project_title, version):
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    draw.rectangle([MARGIN, MARGIN, MARGIN + 80, MARGIN + 8], fill=YELLOW)
    draw.text((MARGIN, MARGIN + 30), project_title, fill=NAVY, font=title_font)

    grid_top = MARGIN + HEADER_H
    for i, frame in enumerate(page_frames):
        col = i % COLS
        row = i // COLS
        x = MARGIN + col * (CELL_W + H_GUTTER)
        y = grid_top + row * (CELL_H + LABEL_H + V_GUTTER)

        img_path = REPO / frame["image"]
        im = Image.open(img_path).convert("RGB")
        im = im.resize((CELL_W, CELL_H), Image.LANCZOS)
        page.paste(im, (x, y))
        draw.rectangle([x, y, x + CELL_W, y + CELL_H], outline=BORDER, width=2)

        label_y = y + CELL_H + 18
        beat_id = frame["id"]
        scene_title = frame["title"]
        caption = frame.get("caption", "")

        badge_w = max(70, 30 + len(beat_id) * 26)
        badge_h = 60
        draw.rectangle([x, label_y, x + badge_w, label_y + badge_h], fill=NAVY)
        bw, bh = measure(draw, beat_id, beat_font)
        draw.text(
            (x + (badge_w - bw) // 2, label_y + (badge_h - bh) // 2 - 6),
            beat_id, fill=YELLOW, font=beat_font,
        )

        title_x = x + badge_w + 16
        title_y = label_y + 6
        draw.text((title_x, title_y), scene_title, fill=NAVY, font=scene_font)

        caption_y = label_y + badge_h + 14
        cap_lines = wrap(caption, caption_font, CELL_W, draw)
        for line in cap_lines[:2]:
            draw.text((x, caption_y), line, fill=GREY, font=caption_font)
            caption_y += 30

    footer_y = PAGE_H - MARGIN - 40
    draw.line([MARGIN, footer_y - 16, PAGE_W - MARGIN, footer_y - 16],
              fill=BORDER, width=1)
    draw.text((MARGIN, footer_y), f"{project_title.lower()} · {version}",
              fill=GREY, font=footer_font)
    page_text = f"Page {page_num} of {total_pages}"
    pw, _ = measure(draw, page_text, footer_font)
    draw.text((PAGE_W - MARGIN - pw, footer_y), page_text,
              fill=GREY, font=footer_font)
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to PDF export config JSON")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    project_title = cfg["title"]
    version = cfg.get("version", "v1")
    out_dir = REPO / cfg["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = cfg["frames"]

    per_page = COLS * ROWS
    pages = [frames[i : i + per_page] for i in range(0, len(frames), per_page)]
    total_pages = len(pages)

    page_imgs = []
    for n, page_frames in enumerate(pages, 1):
        img = render_page(page_frames, n, total_pages, project_title, version)
        png_path = out_dir / f"{version}-page-{n}.png"
        img.save(png_path, "PNG", optimize=True)
        print(f"Wrote {png_path.relative_to(REPO)} ({png_path.stat().st_size:,} b)")
        page_imgs.append(img)

    pdf_path = out_dir / f"{cfg['project']}-{version}.pdf"
    page_imgs[0].save(pdf_path, "PDF", resolution=300, save_all=True,
                      append_images=page_imgs[1:])
    print(f"Wrote {pdf_path.relative_to(REPO)} ({pdf_path.stat().st_size:,} b)")

    zip_path = out_dir.parent / f"{out_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out_dir.iterdir()):
            z.write(p, arcname=p.name)
    print(f"Wrote {zip_path.relative_to(REPO)} ({zip_path.stat().st_size:,} b)")


if __name__ == "__main__":
    main()
