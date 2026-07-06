"""Assemble the render contact sheet from finished plan/render deliverables.

Reads finished PNGs from design/output/plans/ (produced by render_premium.py and render_3d.py)
and lays them out on one labeled sheet. Does not generate or alter any of the source images.

Fixed in the production-readiness pass: the previous version of this script listed
aerial_3d_render.png and sketchup_thumbnail.png as two separate numbered views ("2." and "3."),
but they are byte-identical duplicates (same file, saved under two names) - a real defect found
in FINAL_REPO_PRODUCTION_REVIEW.md §3.1. They are now shown once, clearly labeled as a superseded
legacy reference, and the new deterministic 3D render set (render_3d.py) is the featured gallery.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.join(HERE, "..", "output", "plans")
RENDERS_3D = os.path.join(PLANS, "renders_3d")

SHEET_W = 2500
MARGIN = 60
HEADER_H = 160
FOOTER_H = 130
LABEL_H = 46
GAP = 36
COLS = 3


def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def build():
    entries = [
        ("premium_cutaway_masterplan.png", "1. Premium Vector Cutaway Master Plan (primary deliverable)"),
        (os.path.join("renders_3d", "aerial_exterior.png"), "2. Aerial Exterior (deterministic 3D)"),
        (os.path.join("renders_3d", "stable_aisle.png"), "3. Stable Aisle Interior (deterministic 3D)"),
        (os.path.join("renders_3d", "paddock_courtyard.png"), "4. Paddock & Service Courtyard (deterministic 3D)"),
        (os.path.join("renders_3d", "guest_majlis.png"), "5. Guest & Majlis Zone (deterministic 3D)"),
        (os.path.join("renders_3d", "entry_parking.png"), "6. Entry & Parking Apron (deterministic 3D)"),
        (os.path.join("renders_3d", "twilight_hero.png"), "7. Twilight Hero View (deterministic 3D)"),
        ("plan_dimensioned.png", "8. Dimensioned Technical Plan"),
        ("masterplan_luxury.png", "9. Styled Masterplan (SVG render)"),
        ("aerial_3d_render.png", "10. Legacy SketchUp Massing Reference (superseded - see RENDER_FINALIZATION_REPORT.md)"),
    ]
    imgs = []
    for fname, label in entries:
        p = os.path.join(PLANS, fname)
        if os.path.exists(p):
            imgs.append((Image.open(p).convert("RGB"), label))

    cols = COLS
    rows = (len(imgs) + cols - 1) // cols
    cell_w = (SHEET_W - 2 * MARGIN - (cols - 1) * GAP) // cols
    cell_img_h = int(cell_w * 0.72)
    cell_h = cell_img_h + LABEL_H

    sheet_h = HEADER_H + rows * cell_h + (rows - 1) * GAP + FOOTER_H + 2 * MARGIN
    sheet = Image.new("RGB", (SHEET_W, sheet_h), (250, 249, 246))
    draw = ImageDraw.Draw(sheet)

    title_font = load_font(46, bold=True)
    sub_font = load_font(24)
    label_font = load_font(22, bold=True)
    footer_font = load_font(19)

    draw.text((MARGIN, 40), "Luxury Equestrian Stable — Render Contact Sheet", font=title_font, fill=(30, 30, 30))
    draw.text((MARGIN, 96), "Concept visualization package — not for construction or permit use", font=sub_font, fill=(90, 90, 90))
    draw.line([(MARGIN, HEADER_H - 10), (SHEET_W - MARGIN, HEADER_H - 10)], fill=(200, 195, 180), width=2)

    for i, (img, label) in enumerate(imgs):
        col = i % cols
        row = i // cols
        x = MARGIN + col * (cell_w + GAP)
        y = HEADER_H + row * (cell_h + GAP)

        w, h = img.size
        scale = min(cell_w / w, cell_img_h / h)
        new_w, new_h = int(w * scale), int(h * scale)
        thumb = img.resize((new_w, new_h), Image.LANCZOS)

        frame = Image.new("RGB", (cell_w, cell_img_h), (255, 255, 255))
        fx = (cell_w - new_w) // 2
        fy = (cell_img_h - new_h) // 2
        frame.paste(thumb, (fx, fy))
        sheet.paste(frame, (x, y))
        draw.rectangle([x, y, x + cell_w, y + cell_img_h], outline=(210, 205, 190), width=2)
        draw.text((x, y + cell_img_h + 8), label, font=label_font, fill=(40, 40, 40))

    footer_y = sheet_h - FOOTER_H
    draw.line([(MARGIN, footer_y), (SHEET_W - MARGIN, footer_y)], fill=(200, 195, 180), width=2)
    footer_lines = [
        "Item 1 and items 2-7 are all generated deterministically, directly from the validated coordinate model (design/scripts/model.py) - zero hallucination risk.",
        "Item 10 is kept only as a labeled historical reference to the original 3D-sync pass geometry check; it is not a current gallery view - see RENDER_FINALIZATION_REPORT.md.",
    ]
    ty = footer_y + 18
    for line in footer_lines:
        draw.text((MARGIN, ty), line, font=footer_font, fill=(110, 105, 95))
        ty += 28

    out_path = os.path.join(PLANS, "render_contact_sheet.png")
    sheet.save(out_path, "PNG")
    print("Wrote", out_path, sheet.size)


if __name__ == "__main__":
    build()
