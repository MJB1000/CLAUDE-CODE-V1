"""Standard A4 storyboard PDF exporter.

Reads either:
  - A PDF config JSON (legacy) with a flat "frames" array
  - A unified storyboard manifest JSON with "beats" containing frames

…and renders A4 portrait pages — 3x2 grid of 9:16 cells per page —
with each frame's image, beat-ID badge, scene title, and one-line
caption beneath. When the input is beat-organised, each beat starts a
fresh page with its own section header (yellow accent + beat title +
optional description).

UNIFIED MANIFEST SCHEMA (preferred — same file the renderer uses)
  {
    "project": "<slug>",
    "title":   "<HEADER TEXT, ALL-CAPS>",        # PDF header
    "version": "v1",                              # PDF filename suffix
    "output_dir": "deliverables/<slug>/images",   # where rendered frames live
    "pdf_dir":   "deliverables/<slug>/pdf",       # OPTIONAL: where PDF lands
    "beats": [
      {
        "id":          "act-1-arrival",
        "title":       "ACT 1 — ARRIVAL",
        "description": "The hero machine arrives.",  # OPTIONAL
        "frames": [
          {
            "n": 1, "id": "A1", "slug": "pallet-stop",
            "title":   "PALLET STOP",
            "caption": "XE17U dragged to a stop.",
            # "image" optional — derived from output_dir + n/id/slug
          },
          ...
        ]
      }
    ]
  }

LEGACY PDF CONFIG (still supported)
  { "project": ..., "title": ..., "version": ...,
    "output_dir": "deliverables/<slug>-pdf",
    "frames": [{ "id": ..., "title": ..., "caption": ..., "image": ... }] }

USAGE
  python3 pdf-export.py --config <unified-or-legacy.json>
"""

import argparse
import json
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[4]

PAGE_W, PAGE_H = 2480, 3508
MARGIN = 80
HEADER_H_FLAT = 140         # legacy flat header
HEADER_H_BEAT = 280          # beat-sectioned header (project + beat + desc)
COLS, ROWS = 3, 2
LABEL_H = 180
H_GUTTER = 30
V_GUTTER = 60

usable_w = PAGE_W - 2 * MARGIN - (COLS - 1) * H_GUTTER
CELL_W = usable_w // COLS
CELL_H = CELL_W * 16 // 9

FONT_PATH = "/tmp/fonts/Outfit.ttf"
title_font = ImageFont.truetype(FONT_PATH, 56)
beat_header_font = ImageFont.truetype(FONT_PATH, 72)
beat_desc_font = ImageFont.truetype(FONT_PATH, 28)
beat_font = ImageFont.truetype(FONT_PATH, 44)
scene_font = ImageFont.truetype(FONT_PATH, 30)
caption_font = ImageFont.truetype(FONT_PATH, 24)
footer_font = ImageFont.truetype(FONT_PATH, 28)
small_title_font = ImageFont.truetype(FONT_PATH, 34)

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


def derive_image_path(frame, output_dir):
    """When a frame omits 'image', derive it from output_dir + n + id + slug."""
    if "image" in frame:
        return REPO / frame["image"]
    n = frame.get("n")
    fid = frame.get("id")
    slug = frame.get("slug", "")
    if n is None or fid is None:
        raise KeyError(f"frame missing 'image' and lacks n/id to derive path: {frame}")
    name = f"{int(n):02d}-{fid}-{slug}.png" if slug else f"{int(n):02d}-{fid}.png"
    return REPO / output_dir / name


def draw_cell(page, draw, frame, x, y, output_dir):
    img_path = derive_image_path(frame, output_dir)
    im = Image.open(img_path).convert("RGB")
    im = im.resize((CELL_W, CELL_H), Image.LANCZOS)
    page.paste(im, (x, y))
    draw.rectangle([x, y, x + CELL_W, y + CELL_H], outline=BORDER, width=2)

    label_y = y + CELL_H + 18
    beat_id = frame["id"]
    scene_title = frame.get("title", "")
    caption = frame.get("caption", "")

    badge_w = max(70, 30 + len(beat_id) * 26)
    badge_h = 60
    draw.rectangle([x, label_y, x + badge_w, label_y + badge_h], fill=NAVY)
    bw, bh = measure(draw, beat_id, beat_font)
    draw.text((x + (badge_w - bw) // 2, label_y + (badge_h - bh) // 2 - 6),
              beat_id, fill=YELLOW, font=beat_font)

    title_x = x + badge_w + 16
    title_y = label_y + 6
    draw.text((title_x, title_y), scene_title, fill=NAVY, font=scene_font)

    caption_y = label_y + badge_h + 14
    for line in wrap(caption, caption_font, CELL_W, draw)[:2]:
        draw.text((x, caption_y), line, fill=GREY, font=caption_font)
        caption_y += 30


def draw_footer(draw, project_title, version, page_num, total_pages):
    footer_y = PAGE_H - MARGIN - 40
    draw.line([MARGIN, footer_y - 16, PAGE_W - MARGIN, footer_y - 16],
              fill=BORDER, width=1)
    draw.text((MARGIN, footer_y), f"{project_title.lower()} · {version}",
              fill=GREY, font=footer_font)
    page_text = f"Page {page_num} of {total_pages}"
    pw, _ = measure(draw, page_text, footer_font)
    draw.text((PAGE_W - MARGIN - pw, footer_y), page_text,
              fill=GREY, font=footer_font)


def render_flat_page(page_frames, page_num, total_pages, project_title, version, output_dir):
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    draw.rectangle([MARGIN, MARGIN, MARGIN + 80, MARGIN + 8], fill=YELLOW)
    draw.text((MARGIN, MARGIN + 30), project_title, fill=NAVY, font=title_font)

    grid_top = MARGIN + HEADER_H_FLAT
    for i, frame in enumerate(page_frames):
        col = i % COLS
        row = i // COLS
        x = MARGIN + col * (CELL_W + H_GUTTER)
        y = grid_top + row * (CELL_H + LABEL_H + V_GUTTER)
        draw_cell(page, draw, frame, x, y, output_dir)

    draw_footer(draw, project_title, version, page_num, total_pages)
    return page


def render_beat_page(beat, page_frames, beat_page_num, beat_total_pages,
                     page_num, total_pages, project_title, version,
                     output_dir, is_continuation=False):
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # Top strip: small project title on left, version tag on right
    draw.text((MARGIN, MARGIN), project_title, fill=GREY, font=small_title_font)
    vt = f"· {version} ·"
    vw, _ = measure(draw, vt, small_title_font)
    draw.text((PAGE_W - MARGIN - vw, MARGIN), vt, fill=GREY, font=small_title_font)

    # Beat section header: thick yellow accent bar + beat title + optional description
    beat_top = MARGIN + 60
    draw.rectangle([MARGIN, beat_top, MARGIN + 18, beat_top + 96], fill=YELLOW)
    beat_title = beat.get("title", beat.get("id", "").upper())
    if is_continuation:
        beat_title = f"{beat_title} (CONT.)"
    draw.text((MARGIN + 38, beat_top + 4), beat_title, fill=NAVY, font=beat_header_font)

    desc = beat.get("description", "")
    if desc and not is_continuation:
        draw.text((MARGIN + 38, beat_top + 96 + 6), desc, fill=GREY, font=beat_desc_font)

    # Pagination tag for multi-page beats
    if beat_total_pages > 1:
        ptag = f"{beat_page_num}/{beat_total_pages}"
        pw, _ = measure(draw, ptag, beat_desc_font)
        draw.text((PAGE_W - MARGIN - pw, beat_top + 40), ptag,
                  fill=GREY, font=beat_desc_font)

    grid_top = MARGIN + HEADER_H_BEAT
    for i, frame in enumerate(page_frames):
        col = i % COLS
        row = i // COLS
        x = MARGIN + col * (CELL_W + H_GUTTER)
        y = grid_top + row * (CELL_H + LABEL_H + V_GUTTER)
        draw_cell(page, draw, frame, x, y, output_dir)

    draw_footer(draw, project_title, version, page_num, total_pages)
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True,
                    help="Path to PDF config JSON or unified storyboard manifest JSON")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    project_title = cfg["title"]
    version = cfg.get("version", "v1")

    # Resolve output directories.
    # pdf_dir: where the PDF lands.  output_dir: where the rendered frames live
    # (used to derive image paths when frames omit "image").
    pdf_dir = REPO / cfg.get("pdf_dir", cfg["output_dir"])
    output_dir = REPO / cfg["output_dir"]
    pdf_dir.mkdir(parents=True, exist_ok=True)

    per_page = COLS * ROWS

    # Beat-sectioned PDF (unified manifest shape) — each beat gets its own page(s).
    if "beats" in cfg:
        # Plan pages: one entry per page, paginating beats with more than per_page frames.
        plan = []
        for beat in cfg["beats"]:
            beat_frames = beat.get("frames", [])
            if not beat_frames:
                continue
            chunks = [beat_frames[i:i + per_page]
                      for i in range(0, len(beat_frames), per_page)]
            for idx, chunk in enumerate(chunks, 1):
                plan.append({
                    "beat": beat,
                    "frames": chunk,
                    "beat_page_num": idx,
                    "beat_total_pages": len(chunks),
                    "is_continuation": idx > 1,
                })
        total_pages = len(plan)

        page_imgs = []
        for n, page in enumerate(plan, 1):
            img = render_beat_page(
                page["beat"], page["frames"],
                page["beat_page_num"], page["beat_total_pages"],
                n, total_pages, project_title, version,
                output_dir, is_continuation=page["is_continuation"],
            )
            png_path = pdf_dir / f"{version}-page-{n:02d}.png"
            img.save(png_path, "PNG", optimize=True)
            print(f"Wrote {png_path.relative_to(REPO)} ({png_path.stat().st_size:,} b)")
            page_imgs.append(img)

    # Legacy flat-frames PDF.
    else:
        frames = cfg["frames"]
        pages = [frames[i:i + per_page] for i in range(0, len(frames), per_page)]
        total_pages = len(pages)
        page_imgs = []
        for n, page_frames in enumerate(pages, 1):
            img = render_flat_page(page_frames, n, total_pages,
                                   project_title, version, output_dir)
            png_path = pdf_dir / f"{version}-page-{n:02d}.png"
            img.save(png_path, "PNG", optimize=True)
            print(f"Wrote {png_path.relative_to(REPO)} ({png_path.stat().st_size:,} b)")
            page_imgs.append(img)

    pdf_path = pdf_dir / f"{cfg['project']}-{version}.pdf"
    page_imgs[0].save(pdf_path, "PDF", resolution=300, save_all=True,
                      append_images=page_imgs[1:])
    print(f"Wrote {pdf_path.relative_to(REPO)} ({pdf_path.stat().st_size:,} b)")

    zip_path = pdf_dir.parent / f"{pdf_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(pdf_dir.iterdir()):
            z.write(p, arcname=p.name)
    print(f"Wrote {zip_path.relative_to(REPO)} ({zip_path.stat().st_size:,} b)")


if __name__ == "__main__":
    main()
