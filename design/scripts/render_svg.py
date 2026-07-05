"""
Generate two SVG drawings from the validated model:
  1. plan_dimensioned.svg  - clean technical dimensioned plan (line-drawing CAD style)
  2. masterplan_luxury.svg - styled illustrative top-down color masterplan (same geometry)

Both are strictly derived from design/scripts/model.py coordinates - no invented
geometry. Concept plan only. Not for construction or permit use.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

OUT_DIR = Path(__file__).parent.parent / "output" / "plans"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCALE = 16  # px per meter
MARGIN = 90  # px canvas margin for dimensions/title block
RIGHT_MARGIN = 210  # extra room for north arrow + annotation
CANVAS_W = SITE_WIDTH * SCALE + MARGIN + RIGHT_MARGIN
CANVAS_H = SITE_DEPTH * SCALE + MARGIN * 2 + 190  # extra bottom for title block/legend


def text_color_for(hexcolor):
    h = hexcolor.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "#f5f0e6" if luminance < 130 else "#1a1a1a"

DISCLAIMER = ("Concept plan only. Not for construction or permit use until reviewed and approved by a "
              "licensed local architect/engineer, MEP/civil engineer, and fire/life-safety consultant.")

FUNC_COLOR = {
    "horse_stall": "#c9a875",
    "premium_horse_stall": "#b8894f",
    "special_horse_room_UNCONFIRMED": "#d94f4f",
    "feed_room": "#8a9a5b",
    "service_room": "#9a9a9a",
    "worker_bedroom": "#7fa7c9",
    "worker_kitchen": "#7fa7c9",
    "worker_bathroom": "#7fa7c9",
    "majlis": "#5b3a29",
    "mens_wc": "#8d7b68",
    "outdoor_sitting": "#e8dcc4",
    "private_bedroom": "#4a5a3a",
    "private_bathroom": "#8d7b68",
    "paddock": "#dfe8d0",
    "service_yard": "#cccccc",
    "service_lane": "#bfbfbf",
    "arrival_court": "#efe6d8",
    "parking": "#b8b8b0",
}

FUNC_COLOR_LUX = {
    "horse_stall": "#d9b98c",
    "premium_horse_stall": "#c79a5b",
    "special_horse_room_UNCONFIRMED": "#e07a5f",
    "feed_room": "#9caf6b",
    "service_room": "#a8a8a8",
    "worker_bedroom": "#8fb4d9",
    "worker_kitchen": "#8fb4d9",
    "worker_bathroom": "#8fb4d9",
    "majlis": "#6b4a35",
    "mens_wc": "#a08d78",
    "outdoor_sitting": "#f2e9d8",
    "private_bedroom": "#5c6f47",
    "private_bathroom": "#a08d78",
    "paddock": "#c9dba8",
    "service_yard": "#d8d8d8",
    "service_lane": "#c4c4c4",
    "arrival_court": "#f6efe0",
    "parking": "#bdbdb2",
}


def x2px(x):
    return MARGIN + x * SCALE


def y2px(y):
    return MARGIN + y * SCALE


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_svg(title, colors, styled=False):
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
                 f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="Helvetica, Arial, sans-serif">')
    bg = "#fbf7ef" if styled else "#ffffff"
    parts.append(f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{bg}"/>')

    # Title block
    parts.append(f'<text x="{MARGIN}" y="30" font-size="19" font-weight="bold" fill="#1a1a1a">{esc(title)}</text>')
    parts.append(f'<text x="{MARGIN}" y="52" font-size="12" fill="#444">Site: {SITE_WIDTH:.2f} m (W) x '
                  f'{SITE_DEPTH:.2f} m (D) = {SITE_WIDTH*SITE_DEPTH:.2f} m2  |  Scale 1:{int(1000/SCALE*10)/10} '
                  f'(schematic, not print-scale)  |  Units: meters</text>')

    # Coordinate grid every 5m
    grid_color = "#e6ded0" if styled else "#dddddd"
    for gx in range(0, int(SITE_WIDTH) + 1, 5):
        x = x2px(gx)
        parts.append(f'<line x1="{x}" y1="{MARGIN}" x2="{x}" y2="{y2px(SITE_DEPTH)}" stroke="{grid_color}" stroke-width="1"/>')
        parts.append(f'<text x="{x+2}" y="{MARGIN-6}" font-size="9" fill="#888">{gx}</text>')
    for gy in range(0, int(SITE_DEPTH) + 1, 5):
        y = y2px(gy)
        parts.append(f'<line x1="{MARGIN}" y1="{y}" x2="{x2px(SITE_WIDTH)}" y2="{y}" stroke="{grid_color}" stroke-width="1"/>')
        parts.append(f'<text x="{MARGIN-26}" y="{y+3}" font-size="9" fill="#888">{gy}</text>')

    # Site boundary
    parts.append(f'<rect x="{x2px(0)}" y="{y2px(0)}" width="{SITE_WIDTH*SCALE}" height="{SITE_DEPTH*SCALE}" '
                 f'fill="none" stroke="#111" stroke-width="2.5"/>')

    # Gate/entrance arrow (Y=0 confirmed as the entrance edge by the source hand sketch;
    # true compass north was not given in any source file, so this marks site-front, not North)
    ax, ay = x2px(SITE_WIDTH) + 45, y2px(4)
    parts.append(f'<g stroke="#111" fill="#111">'
                 f'<line x1="{ax}" y1="{ay+22}" x2="{ax}" y2="{ay-10}" stroke-width="1.5"/>'
                 f'<polygon points="{ax},{ay-16} {ax-6},{ay-4} {ax+6},{ay-4}"/>'
                 f'</g>')
    parts.append(f'<text x="{ax-16}" y="{ay+36}" font-size="10">GATE</text>')
    for i, line in enumerate(["confirmed on this edge", "by source hand sketch;", "compass North not given"]):
        parts.append(f'<text x="{ax-45}" y="{ay+50+i*11}" font-size="8" fill="#666">{esc(line)}</text>')

    # Rooms (draw large open zones first so nested markings like the parking apron sit on top)
    DRAW_FIRST = {"arrival_court", "service_lane", "service_yard"}
    draw_order = [s for s in spaces if s["function"] in DRAW_FIRST] + \
                 [s for s in spaces if s["function"] not in DRAW_FIRST]
    for s in draw_order:
        x, y = x2px(s["x_min"]), y2px(s["y_min"])
        w, h = s["width_m"] * SCALE, s["depth_m"] * SCALE
        fill = colors.get(s["function"], "#eeeeee")
        stroke = "#e0703f" if "UNCONFIRMED" in s["function"] else ("#1a1a1a" if not styled else "#5a4a3a")
        dash = ' stroke-dasharray="4,2"' if "UNCONFIRMED" in s["function"] else ""
        opacity = "0.95" if styled else "1"
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" fill-opacity="{opacity}" '
                     f'stroke="{stroke}" stroke-width="1.4"{dash}/>')

        txt_color = text_color_for(fill)
        label_font = 8.5 if s["width_m"] < 4.2 else 10
        label = s["id"]
        parts.append(f'<text x="{x + w/2}" y="{y + h/2 - 2}" font-size="{label_font}" text-anchor="middle" '
                     f'fill="{txt_color}" font-weight="600">{esc(label)}</text>')
        if s["width_m"] >= 4.2 or styled is False:
            dim = f'{s["width_m"]:.2f}x{s["depth_m"]:.2f}m'
            parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 10}" font-size="7" text-anchor="middle" '
                         f'fill="{txt_color}">{esc(dim)}</text>')

    # Legend (bottom strip)
    ly = y2px(SITE_DEPTH) + 26
    parts.append(f'<text x="{MARGIN}" y="{ly}" font-size="12" font-weight="bold">LEGEND</text>')
    legend_items = [
        ("horse_stall", "Standard Horse Stall (3.75x3.75m) - 20 no."),
        ("premium_horse_stall", "Premium Horse Stall (4.00x4.00m) - 2 no."),
        ("special_horse_room_UNCONFIRMED", "Special Room (3.50x4.00m) - LABEL UNCONFIRMED (dashed) - 2 no."),
        ("feed_room", "Feed Room (4.00x4.00m)"),
        ("service_room", "Service Room (3.00x3.00m per brief; CAD shows 6.00x3.00 - conflict)"),
        ("worker_bedroom", "Worker Accommodation (bedroom/kitchen/bath)"),
        ("majlis", "Men's Majlis (8.00x8.24m, CAD-sourced)"),
        ("private_bedroom", "Private Bedroom Suite (4.83x3.76m, CAD-sourced)"),
        ("outdoor_sitting", "Outdoor Majlis / Sitting Terrace (open-air)"),
        ("paddock", "Paddock (2 no., equal 318.9 m2 each - was unequal in source)"),
        ("service_lane", "Perimeter Service / Fire Lane"),
        ("parking", "Parking Apron (4 bays) - OPTIONAL, found in render only"),
    ]
    lx, lyy = MARGIN, ly + 14
    col_w = 350
    for i, (func, label) in enumerate(legend_items):
        col = i // 6
        row = i % 6
        cx = lx + col * col_w
        cy = lyy + row * 15
        fill = colors.get(func, "#eee")
        parts.append(f'<rect x="{cx}" y="{cy-9}" width="12" height="10" fill="{fill}" stroke="#333" stroke-width="0.8"/>')
        parts.append(f'<text x="{cx+18}" y="{cy}" font-size="8.5" fill="#222">{esc(label)}</text>')

    # Disclaimer (wrapped across two lines, full width)
    import textwrap
    disc_lines = textwrap.wrap(DISCLAIMER, width=118)
    for i, dl in enumerate(disc_lines):
        parts.append(f'<text x="{MARGIN}" y="{CANVAS_H-30+i*14}" font-size="9.5" fill="#b33" '
                     f'font-weight="bold">{esc(dl)}</text>')

    parts.append('</svg>')
    return "\n".join(parts)


dimensioned = build_svg("LUXURY EQUESTRIAN STABLE - DIMENSIONED CONCEPT MASTER PLAN", FUNC_COLOR, styled=False)
(OUT_DIR / "plan_dimensioned.svg").write_text(dimensioned, encoding="utf-8")

luxury = build_svg("LUXURY EQUESTRIAN STABLE - ILLUSTRATIVE TOP-DOWN MASTERPLAN",
                    FUNC_COLOR_LUX, styled=True)
(OUT_DIR / "masterplan_luxury.svg").write_text(luxury, encoding="utf-8")

print(f"Wrote plan_dimensioned.svg and masterplan_luxury.svg to {OUT_DIR}")
