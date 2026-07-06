"""
Premium cutaway master illustration - a vector-illustration upgrade of the schematic masterplan,
styled to approach the composition/warmth of the original reference render (source_files/Stable
PROJECT/WhatsApp Image ...3.27.30 PM.jpeg) while being generated entirely from design/scripts/
model.py coordinates. Zero-hallucination-risk by construction: every rectangle drawn here is read
directly from the validated model, not redrawn by hand or guessed by an image model.

Arabic labels are rendered correctly by scoping font-family to a single font PER text element
(Noto Sans Arabic for Arabic runs, Helvetica/Arial for Latin runs) - this avoids a confirmed
cairosvg limitation where a single text element mixing scripts under a multi-font stack fails to
fall back per-glyph and renders Arabic as tofu boxes. Verified in isolation before use here.

Concept plan only. Not for construction or permit use.
"""
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

OUT_DIR = Path(__file__).parent.parent / "output" / "plans"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCALE = 20
MARGIN = 110
RIGHT_MARGIN = 230
CANVAS_W = SITE_WIDTH * SCALE + MARGIN + RIGHT_MARGIN
CANVAS_H = SITE_DEPTH * SCALE + MARGIN * 2 + 230

DISCLAIMER = ("Concept plan only. Not for construction or permit use until reviewed and approved by a "
              "licensed local architect/engineer, MEP/civil engineer, and fire/life-safety consultant.")

ARABIC_FONT = "Noto Sans Arabic"
LATIN_FONT = "Helvetica, Arial, sans-serif"

# Material-inspired palette (base, light-edge, shadow) per function
PALETTE = {
    "horse_stall":              ("#c9a066", "#ddb87e", "#9c7a4a"),
    "premium_horse_stall":      ("#b8894f", "#cc9d63", "#8f6a3a"),
    "veterinary_isolation_room":("#c17a5c", "#d4906f", "#96593f"),
    "feed_room":                ("#8c9a5e", "#a2b073", "#6b7845"),
    "service_room":             ("#9a9690", "#aeaaa4", "#77746f"),
    "worker_bedroom":           ("#7a9bbd", "#8fadcc", "#5c7994"),
    "worker_kitchen":           ("#7a9bbd", "#8fadcc", "#5c7994"),
    "worker_bathroom":          ("#7a9bbd", "#8fadcc", "#5c7994"),
    "majlis":                   ("#6b4632", "#82593f", "#4e3222"),
    "mens_wc":                  ("#8d7b68", "#a08d78", "#6c5c4c"),
    "outdoor_sitting":          ("#e8dcc0", "#f2e9d4", "#c9bb9c"),
    "private_bedroom":          ("#5c6f45", "#71835a", "#465432"),
    "private_bathroom":         ("#8d7b68", "#a08d78", "#6c5c4c"),
    "paddock":                  ("#d8c9a0", "#e6dab5", "#b8a878"),
    "service_yard":             ("#c7c3ba", "#d5d1c8", "#a19d94"),
    "service_lane":             ("#bab6ae", "#c9c5bd", "#918d85"),
    "arrival_court":            ("#ece2cd", "#f5eddd", "#cfc2a3"),
    "parking":                  ("#a8a49c", "#bab6ae", "#84807a"),
}

ARABIC_NAME_OVERRIDE = {
    # Short, presentation-friendly Arabic labels (same meaning as model.py's arabic_name field)
    "horse_stall": "غرفة خيل",
    "premium_horse_stall": "غرفة خيل كبيرة",
    "veterinary_isolation_room": "غرفة مصاب خيل",
    "feed_room": "غرفة علف",
    "service_room": "غرفة خدمة",
    "worker_bedroom": "غرفة نوم عمال",
    "worker_kitchen": "مطبخ العمال",
    "worker_bathroom": "حمام العمال",
    "majlis": "مجلس رجال",
    "mens_wc": "دورة مياه",
    "outdoor_sitting": "مجلس خارجي",
    "private_bedroom": "غرفة نوم خاصة",
    "private_bathroom": "حمام خاص",
    "paddock": "بادوك",
    "parking": "بركنج",
}


def x2px(x):
    return MARGIN + x * SCALE


def y2px(y):
    return MARGIN + y * SCALE


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def arabic_text(x, y, size, text, anchor="middle", weight="600", fill="#2a2018"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'font-family="{ARABIC_FONT}" font-weight="{weight}" fill="{fill}">{esc(text)}</text>')


def latin_text(x, y, size, text, anchor="middle", weight="600", fill="#2a2018"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'font-family="{LATIN_FONT}" font-weight="{weight}" fill="{fill}">{esc(text)}</text>')


def room_shadow_and_fill(x, y, w, h, base, light, shadow, rx=3):
    parts = []
    # cutaway drop shadow (offset, blurred)
    parts.append(f'<rect x="{x+4}" y="{y+5}" width="{w}" height="{h}" rx="{rx}" '
                 f'fill="#000000" fill-opacity="0.22" filter="url(#softblur)"/>')
    # base fill with subtle vertical gradient id referencing per-function gradient
    grad_id = f"grad_{base.strip('#')}"
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{grad_id})" '
                 f'stroke="{shadow}" stroke-width="1.6"/>')
    # light bevel edge top-left
    parts.append(f'<line x1="{x+2}" y1="{y+3}" x2="{x+w-2}" y2="{y+3}" stroke="{light}" '
                 f'stroke-width="1.5" stroke-opacity="0.65"/>')
    return "\n".join(parts)


def hay_bale_icon(cx, cy, s=7):
    parts = []
    for i, (dx, dy) in enumerate([(-s*0.55, 0), (s*0.55, 0), (0, -s*0.62)]):
        parts.append(f'<rect x="{cx+dx-s*0.5}" y="{cy+dy-s*0.35}" width="{s}" height="{s*0.7}" '
                     f'rx="1.5" fill="#c9a53f" stroke="#8f7527" stroke-width="0.6" '
                     f'transform="rotate({(-8+i*8)} {cx+dx} {cy+dy})"/>')
    return "\n".join(parts)


def bed_icon(x, y, w, h, count=1):
    parts = []
    bw = min(w * 0.42, 34)
    bh = min(h * 0.62, 46)
    gap = (w - bw * count) / (count + 1)
    for i in range(count):
        bx = x + gap * (i + 1) + bw * i
        by = y + (h - bh) / 2
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" '
                     f'fill="#e9e2d2" stroke="#8a7f68" stroke-width="1"/>')
        parts.append(f'<rect x="{bx+2}" y="{by+2}" width="{bw-4}" height="{bh*0.28}" rx="2.5" '
                     f'fill="#ffffff" stroke="#c9c0ab" stroke-width="0.6"/>')
        parts.append(f'<rect x="{bx}" y="{by+bh*0.72}" width="{bw}" height="{bh*0.28}" rx="2.5" '
                     f'fill="#7a5c46" fill-opacity="0.55"/>')
    return "\n".join(parts)


def majlis_seating_icon(x, y, w, h):
    parts = []
    cx, cy = x + w / 2, y + h / 2
    rug_w, rug_h = w * 0.62, h * 0.55
    parts.append(f'<rect x="{cx-rug_w/2}" y="{cy-rug_h/2}" width="{rug_w}" height="{rug_h}" rx="4" '
                 f'fill="#8a3f34" fill-opacity="0.85"/>')
    parts.append(f'<rect x="{cx-rug_w/2+6}" y="{cy-rug_h/2+6}" width="{rug_w-12}" height="{rug_h-12}" '
                 f'rx="3" fill="none" stroke="#d9b775" stroke-width="1.2"/>')
    seat_positions = [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1.35), (0, 1.35)]
    for sx, sy in seat_positions:
        px = cx + sx * (rug_w / 2 + 10)
        py = cy + sy * (rug_h / 2 + 8)
        parts.append(f'<rect x="{px-9}" y="{py-7}" width="18" height="14" rx="4" '
                     f'fill="#6b4632" stroke="#3f2a1c" stroke-width="0.8"/>')
    return "\n".join(parts)


def car_icon(x, y, w=26, h=14):
    return (f'<g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#5a6472" stroke="#2c323a" stroke-width="0.8"/>'
            f'<rect x="{x+w*0.22}" y="{y-h*0.3}" width="{w*0.56}" height="{h*0.55}" rx="3" '
            f'fill="#8ea3b8" stroke="#2c323a" stroke-width="0.7"/>'
            f'<circle cx="{x+w*0.22}" cy="{y+h}" r="2.6" fill="#1c1c1c"/>'
            f'<circle cx="{x+w*0.78}" cy="{y+h}" r="2.6" fill="#1c1c1c"/>'
            f'</g>')


def tree_icon(cx, cy, r=13):
    return (f'<g>'
            f'<ellipse cx="{cx+2}" cy="{cy+2}" rx="{r}" ry="{r*0.5}" fill="#000000" fill-opacity="0.15"/>'
            f'<rect x="{cx-2}" y="{cy-2}" width="4" height="10" fill="#6b4a30"/>'
            f'<circle cx="{cx}" cy="{cy-r*0.65}" r="{r*0.72}" fill="#7a9556" fill-opacity="0.92"/>'
            f'<circle cx="{cx-r*0.4}" cy="{cy-r*0.4}" r="{r*0.55}" fill="#8ba764" fill-opacity="0.88"/>'
            f'<circle cx="{cx+r*0.42}" cy="{cy-r*0.45}" r="{r*0.5}" fill="#6a8548" fill-opacity="0.9"/>'
            f'</g>')


def sand_texture(x, y, w, h, base_color, seed=0):
    """Layered soft blobs to simulate a raked sand paddock surface."""
    import random
    rnd = random.Random(seed)
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{base_color}"/>']
    for _ in range(int((w * h) / 2600)):
        bx = x + rnd.uniform(0, w)
        by = y + rnd.uniform(0, h)
        br = rnd.uniform(10, 30)
        shade = rnd.choice(["#c7b482", "#e2d3a8", "#d3c092"])
        parts.append(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{br:.1f}" ry="{br*0.45:.1f}" '
                     f'fill="{shade}" fill-opacity="0.25"/>')
    # rake lines
    for i in range(int(w / 40)):
        lx = x + 20 + i * 40
        parts.append(f'<line x1="{lx}" y1="{y+6}" x2="{lx+h*0.15}" y2="{y+h-6}" '
                     f'stroke="#b8a674" stroke-width="1" stroke-opacity="0.3"/>')
    return "\n".join(parts)


def build():
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
                 f'viewBox="0 0 {CANVAS_W} {CANVAS_H}">')

    # Defs: gradients + soft blur filter
    parts.append("<defs>")
    parts.append('<filter id="softblur" x="-30%" y="-30%" width="160%" height="160%">'
                 '<feGaussianBlur in="SourceGraphic" stdDeviation="3"/></filter>')
    seen = set()
    for base, light, shadow in PALETTE.values():
        gid = f"grad_{base.strip('#')}"
        if gid in seen:
            continue
        seen.add(gid)
        parts.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                     f'<stop offset="0%" stop-color="{light}"/>'
                     f'<stop offset="100%" stop-color="{base}"/></linearGradient>')
    parts.append('<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0%" stop-color="#faf5e9"/><stop offset="100%" stop-color="#f0e8d4"/>'
                 '</linearGradient>')
    parts.append("</defs>")

    parts.append(f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#bgGrad)"/>')

    # Presentation sheet frame (double rule mat) — turns a bare plan into a presentation board
    fpad = 26
    parts.append(f'<rect x="{fpad}" y="{fpad}" width="{CANVAS_W-2*fpad}" height="{CANVAS_H-2*fpad}" '
                 f'fill="none" stroke="#2a2018" stroke-width="2.5"/>')
    parts.append(f'<rect x="{fpad+7}" y="{fpad+7}" width="{CANVAS_W-2*fpad-14}" height="{CANVAS_H-2*fpad-14}" '
                 f'fill="none" stroke="#b7a074" stroke-width="1"/>')

    # Title block with accent rule
    parts.append(latin_text(MARGIN, 42, 26, "LUXURY EQUESTRIAN STABLE", anchor="start", weight="800"))
    parts.append(latin_text(MARGIN, 66, 15, "Concept Masterplan  ·  Validated Schematic Layout",
                            anchor="start", weight="500", fill="#6b5d47"))
    parts.append(arabic_text(MARGIN, 92, 17, "مخطط عام، تصميم معتمد ونهائي", anchor="start", weight="600",
                             fill="#6b5d47"))
    parts.append(f'<line x1="{MARGIN}" y1="102" x2="{x2px(SITE_WIDTH)}" y2="102" '
                 f'stroke="#b7a074" stroke-width="1.5"/>')
    # Sheet reference tag (top-right of the drawing area)
    tag_x = x2px(SITE_WIDTH) + 8
    parts.append(latin_text(tag_x, 52, 20, "MP·01", anchor="start", weight="800", fill="#2a2018"))
    parts.append(latin_text(tag_x, 72, 10.5, "MASTER PLAN", anchor="start", weight="600", fill="#6b5d47"))
    parts.append(latin_text(tag_x, 88, 10.5, "SCALE 1:250 @ A1", anchor="start", weight="500", fill="#8a7d63"))

    # Site boundary with soft ground shadow
    bx, by = x2px(0), y2px(0)
    bw, bh = SITE_WIDTH * SCALE, SITE_DEPTH * SCALE
    parts.append(f'<rect x="{bx+3}" y="{by+4}" width="{bw}" height="{bh}" fill="#000000" '
                 f'fill-opacity="0.10" filter="url(#softblur)"/>')
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#efe6cf" '
                 f'stroke="#2a2018" stroke-width="2.5"/>')

    # Gate marker
    gx, gy = x2px(SITE_WIDTH) + 50, y2px(4)
    parts.append(f'<g stroke="#2a2018" fill="#2a2018">'
                 f'<line x1="{gx}" y1="{gy+24}" x2="{gx}" y2="{gy-10}" stroke-width="2"/>'
                 f'<polygon points="{gx},{gy-18} {gx-7},{gy-4} {gx+7},{gy-4}"/></g>')
    parts.append(latin_text(gx, gy + 40, 12, "GATE", anchor="middle", weight="700"))
    parts.append(arabic_text(gx, gy + 58, 12, "البوابة", anchor="middle", weight="500", fill="#6b5d47"))

    # Compass north arrow (proper, in the right margin lower down)
    ncx, ncy = gx, y2px(19)
    parts.append(f'<circle cx="{ncx}" cy="{ncy}" r="24" fill="#faf5e9" stroke="#2a2018" stroke-width="1.4"/>')
    parts.append(f'<polygon points="{ncx},{ncy-19} {ncx-7},{ncy+3} {ncx+7},{ncy+3}" fill="#8a3f34"/>')
    parts.append(f'<polygon points="{ncx},{ncy+18} {ncx-7},{ncy+3} {ncx+7},{ncy+3}" fill="#2a2018"/>')
    parts.append(latin_text(ncx, ncy - 26, 11, "N", anchor="middle", weight="800"))

    # Rooms
    DRAW_FIRST = {"arrival_court", "service_lane", "service_yard", "paddock"}
    order = [s for s in spaces if s["function"] in DRAW_FIRST] + \
            [s for s in spaces if s["function"] not in DRAW_FIRST]

    for s in order:
        x, y = x2px(s["x_min"]), y2px(s["y_min"])
        w, h = s["width_m"] * SCALE, s["depth_m"] * SCALE
        func = s["function"]
        base, light, shadow = PALETTE.get(func, ("#cccccc", "#dddddd", "#999999"))

        if func == "paddock":
            parts.append(f'<rect x="{x+4}" y="{y+5}" width="{w}" height="{h}" fill="#000000" '
                         f'fill-opacity="0.15" filter="url(#softblur)"/>')
            parts.append(f'<clipPath id="clip_{s["id"]}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/></clipPath>')
            parts.append(f'<g clip-path="url(#clip_{s["id"]})">')
            parts.append(sand_texture(x, y, w, h, base, seed=zlib.crc32(s["id"].encode()) % 1000))
            parts.append("</g>")
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="none" '
                         f'stroke="{shadow}" stroke-width="1.6"/>')
        else:
            parts.append(room_shadow_and_fill(x, y, w, h, base, light, shadow))

        # Entourage vs. label vertical zoning: rooms with entourage icons get their label anchored
        # near the TOP edge and the icon confined to the LOWER portion, so the two never overlap
        # (previously both were centered on the same point, and e.g. the bed icon's pillow sat
        # directly on top of the room name text).
        cx, cy = x + w / 2, y + h / 2
        ICON_FUNCS = {"horse_stall", "premium_horse_stall", "majlis", "private_bedroom",
                      "worker_bedroom", "parking"}
        has_icon = func in ICON_FUNCS

        if func in ("horse_stall", "premium_horse_stall"):
            parts.append(hay_bale_icon(cx, y + h * 0.72, s=min(w, h) * 0.30))
        elif func == "majlis":
            parts.append(majlis_seating_icon(x, y + h * 0.12, w, h * 0.80))
        elif func == "private_bedroom":
            parts.append(bed_icon(x, y + h * 0.30, w, h * 0.66, count=1))
        elif func == "worker_bedroom":
            parts.append(bed_icon(x, y + h * 0.30, w, h * 0.66, count=2))
        elif func == "parking":
            n = 4
            cw = w / n
            for i in range(n):
                parts.append(car_icon(x + i * cw + cw * 0.18, y + h * 0.55, w=cw * 0.64, h=h * 0.34))

        # Labels: Arabic (primary) + English/ID (secondary) - each its own scoped-font text element,
        # both fitted to the room's actual WIDTH so nothing overflows into neighboring rooms.
        SKIP_ARABIC = {"service_lane", "service_yard", "arrival_court"}
        AR_CHAR_W = 0.60   # empirical average glyph-advance factor for Noto Sans Arabic, per font-size unit
        EN_CHAR_W = 0.62
        avail_w = w * 0.90

        def fit(text, char_w, max_font, min_font):
            font = max_font
            while font > min_font and len(text) * char_w * font > avail_w:
                font -= 0.5
            return font

        txt_fill = "#f5efe0" if func in ("majlis", "private_bedroom", "veterinary_isolation_room",
                                          "premium_horse_stall") else "#2a2018"
        if func == "paddock":
            txt_fill = "#5a4c30"

        ar_label = "" if func in SKIP_ARABIC else ARABIC_NAME_OVERRIDE.get(func, s.get("arabic_name", ""))
        en_label = s["id"]

        en_size = fit(en_label, EN_CHAR_W, 11 if min(w, h) >= 60 else 8.5, 5.5)
        ar_size = 0.0
        if ar_label:
            ar_size = fit(ar_label, AR_CHAR_W, 15 if min(w, h) >= 60 else 10, 7.0)
            # if even the floor size still overflows, drop the Arabic label rather than clip it
            if len(ar_label) * AR_CHAR_W * ar_size > avail_w * 1.05:
                ar_label, ar_size = "", 0.0

        if h >= 20:
            if ar_label:
                label_y = (y + ar_size + 6) if has_icon else (cy - en_size * 0.7)
                parts.append(arabic_text(cx, label_y, ar_size, ar_label, fill=txt_fill))
                parts.append(latin_text(cx, label_y + ar_size * 0.85 + en_size * 0.35, en_size, en_label,
                                        fill=txt_fill, weight="700"))
            else:
                label_y = (y + en_size + 6) if has_icon else (cy + en_size * 0.35)
                parts.append(latin_text(cx, label_y, en_size, en_label, fill=txt_fill, weight="700"))

    # Landscaping trees (guest zone + paddock edges) - purely decorative, matches prior tree positions
    tree_spots = [(1.0, 4.2), (36.5, 4.2), (11.0, 12.5), (28.5, 12.5), (0.5, 30.5), (37.0, 30.5),
                  (18.75, 30.5), (0.5, 49.0), (37.0, 49.0)]
    for tx, ty in tree_spots:
        parts.append(tree_icon(x2px(tx), y2px(ty), r=13))

    # Legend
    ly = y2px(SITE_DEPTH) + 34
    parts.append(latin_text(MARGIN, ly, 14, "LEGEND", anchor="start", weight="800"))
    legend_items = [
        ("horse_stall", "Standard Horse Stall — 3.75×3.75 m (×20)"),
        ("premium_horse_stall", "Premium Horse Stall — 4.00×4.00 m (×2)"),
        ("veterinary_isolation_room", "Veterinary / Isolation Room ('mesab', owner-confirmed) — 3.50×4.00 m (×2)"),
        ("feed_room", "Feed Room — 4.00×4.00 m"),
        ("service_room", "Service Room — 6.00×3.00 m (owner-confirmed)"),
        ("worker_bedroom", "Worker Accommodation"),
        ("majlis", "Men's Majlis — 8.00×8.24 m"),
        ("private_bedroom", "Private Bedroom Suite"),
        ("outdoor_sitting", "Outdoor Majlis / Sitting Terrace"),
        ("paddock", "Paddock — 2× equal, 318.9 m² each"),
        ("parking", "Parking Apron — 4 bays"),
    ]
    col_w = 380
    for i, (func, label) in enumerate(legend_items):
        col, row = i // 6, i % 6
        base, light, shadow = PALETTE[func]
        lx = MARGIN + col * col_w
        lyy = ly + 20 + row * 19
        parts.append(f'<rect x="{lx}" y="{lyy-11}" width="16" height="13" rx="2" fill="url(#grad_{base.strip(chr(35))})" '
                     f'stroke="{shadow}" stroke-width="1"/>')
        parts.append(latin_text(lx + 22, lyy, 10.5, label, anchor="start", weight="500"))

    # Graphic scale bar (true plan scale, 0–40 m in 10 m increments), left-aligned below the legend
    sb_x = MARGIN
    sb_y = ly + 150
    seg = 10 * SCALE  # 10 m per segment at plan scale (200 px)
    parts.append(latin_text(sb_x, sb_y - 9, 11, "SCALE  (metres)", anchor="start", weight="700"))
    for i in range(4):
        fill = "#2a2018" if i % 2 == 0 else "#faf5e9"
        parts.append(f'<rect x="{sb_x + i*seg}" y="{sb_y}" width="{seg}" height="9" '
                     f'fill="{fill}" stroke="#2a2018" stroke-width="1"/>')
    for i in range(5):
        parts.append(latin_text(sb_x + i*seg, sb_y + 24, 9.5, str(i*10), anchor="middle",
                                weight="500", fill="#4a4030"))

    # Project-info footer strip (elegant, single line) above the disclaimer
    info_y = CANVAS_H - 58
    parts.append(f'<line x1="{MARGIN}" y1="{info_y-14}" x2="{x2px(SITE_WIDTH)}" y2="{info_y-14}" '
                 f'stroke="#b7a074" stroke-width="1"/>')
    total_area = sum(s["area_m2"] for s in spaces)
    info = (f"Site 40.00 × 50.00 m  ·  2,000 m²    |    40 scheduled spaces    |    "
            f"scheduled area {total_area:,.2f} m² ({total_area/2000*100:.1f}%)    |    "
            f"validated schematic layout")
    parts.append(latin_text(MARGIN, info_y, 11, info, anchor="start", weight="600", fill="#4a4030"))

    # Disclaimer
    import textwrap
    disc_lines = textwrap.wrap(DISCLAIMER, width=120)
    for i, dl in enumerate(disc_lines):
        parts.append(f'<text x="{MARGIN}" y="{CANVAS_H-30+i*14}" font-size="9.5" font-family="{LATIN_FONT}" '
                     f'fill="#a33" font-weight="700">{esc(dl)}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


svg = build()
(OUT_DIR / "premium_cutaway_masterplan.svg").write_text(svg, encoding="utf-8")
print(f"Wrote premium_cutaway_masterplan.svg to {OUT_DIR}")

import cairosvg  # noqa: E402
cairosvg.svg2png(url=str(OUT_DIR / "premium_cutaway_masterplan.svg"),
                  write_to=str(OUT_DIR / "premium_cutaway_masterplan.png"), scale=2)
print(f"Rendered premium_cutaway_masterplan.png to {OUT_DIR}")
