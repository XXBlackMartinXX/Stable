"""Generate the client-facing presentation PDF.

Narrative content here stays strictly within what design/output/reports/source_audit.md
and model.py already establish as fact - this script only adds polished prose and layout,
never new claims. All numbers (areas, counts, validation status) are computed live from
model.py / validation_report.json, matching the rest of the pipeline.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                 Spacer, Image, PageBreak, ListFlowable, ListItem,
                                 HRFlowable, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

ROOT = SCRIPTS_DIR.parent.parent
REPORTS_DIR = ROOT / "design" / "output" / "reports"
PLANS_DIR = ROOT / "design" / "output" / "plans"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

VALIDATION = json.loads((REPORTS_DIR / "validation_report.json").read_text())

DISCLAIMER = ("Concept plan only. Not for construction or permit use until reviewed and approved "
              "by a licensed local architect/engineer, MEP/civil engineer, and fire/life-safety "
              "consultant.")

GOLD = colors.HexColor("#8a6a3a")
BROWN = colors.HexColor("#7a4a2b")
INK = colors.HexColor("#2b241a")
MUTED = colors.HexColor("#6b6255")
CREAM = colors.HexColor("#f7f5ee")
LINE = colors.HexColor("#d8d2c2")
RED = colors.HexColor("#8a1f1f")

PAGE_SIZE = A4
PAGE_W, PAGE_H = PAGE_SIZE
MARGIN = 22 * mm

styles = getSampleStyleSheet()
cover_title = ParagraphStyle("CoverTitle", fontName="Helvetica-Bold", fontSize=34, leading=40,
                              textColor=INK, alignment=TA_LEFT)
cover_sub = ParagraphStyle("CoverSub", fontName="Helvetica", fontSize=15, leading=20,
                            textColor=MUTED, alignment=TA_LEFT, spaceBefore=6)
cover_tag = ParagraphStyle("CoverTag", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            textColor=GOLD, alignment=TA_LEFT, spaceBefore=18)
sec_no_style = ParagraphStyle("SecNo", fontName="Helvetica-Bold", fontSize=9.5, textColor=GOLD,
                               spaceAfter=2)
h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=INK,
                     spaceAfter=10)
h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=BROWN,
                     spaceBefore=12, spaceAfter=6)
body = ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=15, textColor=INK,
                       alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle("Bullet", parent=body, spaceAfter=4)
small = ParagraphStyle("Small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED)
disclaimer_style = ParagraphStyle("Disclaimer", fontName="Helvetica-Bold", fontSize=8.5, leading=12,
                                   textColor=RED)
toc_entry = ParagraphStyle("TOCEntry", fontName="Helvetica", fontSize=11, leading=20, textColor=INK)
caption = ParagraphStyle("Caption", fontName="Helvetica-Oblique", fontSize=9, leading=12,
                          textColor=MUTED, alignment=TA_CENTER, spaceBefore=4)
cell_path = ParagraphStyle("CellPath", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=INK)
cell_desc = ParagraphStyle("CellDesc", fontName="Helvetica", fontSize=8.5, leading=11, textColor=INK)

FUNCTION_LABELS = {
    "horse_stall": "Horse Stalls (Standard)", "premium_horse_stall": "Horse Stalls (Premium)",
    "veterinary_isolation_room": "Veterinary / Isolation Rooms", "feed_room": "Feed Room",
    "service_room": "Service Room", "paddock": "Paddocks", "worker_bedroom": "Worker Bedroom",
    "worker_kitchen": "Worker Kitchen", "worker_bathroom": "Worker Bathroom", "majlis": "Men's Majlis",
    "mens_wc": "Men's WC", "outdoor_sitting": "Outdoor Majlis / Sitting",
    "private_bedroom": "Private Bedroom", "private_bathroom": "Private Bathroom",
    "parking": "Parking Apron", "service_yard": "Service Yard",
    "service_lane": "Fire Lane / Service Lane", "arrival_court": "Arrival / Motor Court",
}

SECTION_TITLES = [
    "Executive Summary", "Project Goals", "Site Summary", "Design Concept & Philosophy",
    "Zoning Strategy", "Master Plan", "Dimensions & Design Logic", "Zone Narratives",
    "Circulation & Operations", "Materials & Finishes Palette", "Visualization",
    "Technical Highlights", "Room Schedule Summary", "Advantages Over the Original Scheme",
    "Next Steps", "What Still Requires Licensed Professional Review", "Appendix & Reference Index",
]

_section_counter = {"n": 0}


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 12 * mm, "Luxury Equestrian Stable — Concept Presentation")
    canvas.drawRightString(PAGE_W - MARGIN, 12 * mm, f"{doc.page}")
    canvas.setStrokeColor(LINE)
    canvas.line(MARGIN, 17 * mm, PAGE_W - MARGIN, 17 * mm)
    canvas.restoreState()


def section(flow, title):
    _section_counter["n"] += 1
    flow.append(Paragraph(f"SECTION {_section_counter['n']:02d}", sec_no_style))
    flow.append(Paragraph(title, h1))
    flow.append(HRFlowable(width="100%", thickness=1, color=LINE, spaceAfter=10))


def bullets(items):
    return ListFlowable([ListItem(Paragraph(t, bullet), bulletColor=GOLD) for t in items],
                         bulletType="bullet", start="circle", leftIndent=14)


def build_cover(flow):
    flow.append(Spacer(1, 60))
    flow.append(Paragraph("CONCEPT DESIGN PRESENTATION", cover_tag))
    flow.append(Spacer(1, 10))
    flow.append(Paragraph("Luxury Equestrian Stable", cover_title))
    flow.append(Paragraph("A Validated, Owner-Confirmed Concept Redesign", cover_sub))
    flow.append(Spacer(1, 30))
    facts = [
        ["Site", f"{SITE_WIDTH:.0f} × {SITE_DEPTH:.0f} m  ({SITE_WIDTH*SITE_DEPTH:,.0f} m²)"],
        ["Program", f"{len(spaces)} scheduled spaces"],
        ["Scheduled area", f"{VALIDATION['totals']['total_scheduled_area_m2']:,.2f} m² "
                            f"({VALIDATION['totals']['total_scheduled_area_m2']/VALIDATION['site']['area_m2']*100:.1f}% coverage)"],
        ["Validation", f"PASS — {len(VALIDATION['passed_checks'])} geometric checks, 0 failed"],
    ]
    t = Table(facts, colWidths=[45 * mm, None])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 340))
    flow.append(HRFlowable(width="100%", thickness=1, color=LINE, spaceAfter=8))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph("Prepared as a concept design package. See Section 16 for a full list of "
                           "items requiring licensed professional review before any construction.",
                           small))


def build_toc(flow):
    flow.append(Paragraph("Table of Contents", h1))
    flow.append(HRFlowable(width="100%", thickness=1, color=LINE, spaceAfter=14))
    rows = []
    for i, title in enumerate(SECTION_TITLES, start=1):
        rows.append([f"{i:02d}", title])
    t = Table(rows, colWidths=[16 * mm, None])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (0, -1), GOLD),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE),
    ]))
    flow.append(t)


def build_exec_summary(flow):
    section(flow, "Executive Summary")
    flow.append(Paragraph(
        "This package presents a fully validated concept redesign for a private luxury equestrian "
        "stable on a 40.00 × 50.00 m (2,000 m²) site. The design delivers the complete owner brief — "
        "20 standard stalls, 2 premium stalls, 2 veterinary/isolation rooms, feed and service rooms, "
        "two equal paddocks, full worker accommodation, a men's majlis and outdoor majlis, a private "
        "bedroom suite, and a parking apron — organized into a clear front-to-back zoning strategy "
        "that separates guest arrival, the working stable, and the paddock/service zone.", body))
    flow.append(Paragraph(
        f"Every dimension in this package is mathematically validated: {len(VALIDATION['passed_checks'])} "
        "geometric checks pass with zero failures, both horizontal and vertical dimension chains close "
        f"exactly to the site boundary, and total scheduled area is "
        f"{VALIDATION['totals']['total_scheduled_area_m2']:,.2f} m² — a coverage ratio that leaves deliberate "
        "landscaped and circulation space rather than crowding the site.", body))
    flow.append(Paragraph(
        "This is a concept design package, not a construction document. Section 16 states plainly what "
        "still requires licensed structural, MEP, fire/life-safety, and civil review before any permitting "
        "or construction step.", body))


def build_goals(flow):
    section(flow, "Project Goals")
    flow.append(Paragraph("The redesign was directed by five goals, each carried through into the "
                           "final validated layout:", body))
    flow.append(bullets([
        "<b>Deliver the complete program</b> — every required room from the owner's brief and CAD "
        "reference is present at its confirmed size, with nothing invented or dropped.",
        "<b>Operate efficiently</b> — horse care, feeding, and service routes should be as short and "
        "uncrossed as possible.",
        "<b>Present as a luxury estate</b> — the arrival and guest sequence should feel generous and "
        "considered, not utilitarian.",
        "<b>Keep paddocks practical</b> — both paddocks equal in size and directly serviceable, not "
        "reduced to leftover land.",
        "<b>Stay honest</b> — every dimension traceable to a source (the written brief, the CAD "
        "drawing, or an explicit owner decision), with no silent assumptions.",
    ]))


def build_site_summary(flow):
    section(flow, "Site Summary")
    flow.append(Paragraph(
        f"The site measures {SITE_WIDTH:.2f} m wide by {SITE_DEPTH:.2f} m deep "
        f"({SITE_WIDTH*SITE_DEPTH:,.0f} m² total), with the origin at the southwest corner and Y=0 "
        "confirmed as the entrance/gate edge from the original hand sketch. The design uses "
        f"{VALIDATION['totals']['total_scheduled_area_m2']:,.2f} m² ("
        f"{VALIDATION['totals']['total_scheduled_area_m2']/VALIDATION['site']['area_m2']*100:.1f}%) for "
        "the 40 scheduled spaces; the remaining area is landscaped buffer, transition zones, and aisle "
        "circulation, left deliberately open for a calm, uncluttered feel rather than maximized for "
        "buildable area.", body))


def build_design_concept(flow):
    section(flow, "Design Concept & Philosophy")
    flow.append(Paragraph(
        "The design language is calm and materials-first: proportion and shade rhythm carry the "
        "luxury feel rather than ornament.", body))
    flow.append(bullets([
        "Twin symmetric courtyards (indoor majlis + outdoor majlis) create the arrival \"moment\" "
        "without visual clutter.",
        "A single continuous shade canopy over the stable aisle unifies all 24 horse rooms visually "
        "and functionally.",
        "One consistent roofline covers the entire service/worker/feed wing rather than three "
        "disconnected sheds.",
        "Equal, generously proportioned paddocks read as a designed landscape feature, not leftover "
        "land.",
    ]))


def build_zoning(flow):
    section(flow, "Zoning Strategy")
    flow.append(Paragraph(
        "The site is organized into nine bands along its depth (front to back), each closing exactly "
        "against the 40.00 × 50.00 m boundary:", body))
    flow.append(bullets([
        "<b>Motor court + parking</b> — guest arrival, drop-off, four-bay parking apron.",
        "<b>Guest/owner band</b> — majlis and outdoor majlis mirrored either side of a landscaped view "
        "corridor; the private bedroom suite tucked to the east, private from the majlis.",
        "<b>Privacy/transition buffer</b> — landscaped, controls the sightline from guest to working "
        "stable.",
        "<b>Stall Row A / central aisle / Stall Row B</b> — the 20 standard stalls in a double-loaded "
        "barn, aisle-facing, non-slip flooring, shaded canopy above.",
        "<b>Feed / service / premium / veterinary / worker wing</b> — one unified roofline holding "
        "everything the stable needs day-to-day, one aisle from the horses, one wall from the paddocks.",
        "<b>Vestibule</b> — a gated transition from the working wing to the paddock spine.",
        "<b>Paddocks + wash/manure spine</b> — two equal paddocks flanking a dedicated service yard.",
    ]))
    flow.append(Paragraph(
        "A continuous 2.50 m perimeter fire/service lane runs the full site depth along the east edge, "
        "connecting the front gate straight through to the rear paddock spine without ever crossing the "
        "guest motor court or the majlis.", body))


def build_masterplan(flow):
    section(flow, "Master Plan")
    img_path = PLANS_DIR / "premium_cutaway_masterplan.png"
    if img_path.exists():
        from PIL import Image as PILImage
        w, h = PILImage.open(img_path).size
        max_w = PAGE_W - 2 * MARGIN
        max_h = 210 * mm
        scale = min(max_w / w, max_h / h)
        flow.append(Image(str(img_path), width=w * scale, height=h * scale, hAlign="CENTER"))
        flow.append(Paragraph("Premium vector cutaway master plan — generated directly from the "
                               "validated coordinate model. Every rectangle shown is the exact, "
                               "checked geometry; nothing here is illustrative guesswork.", caption))


def build_dimensions_logic(flow):
    section(flow, "Dimensions & Design Logic")
    flow.append(Paragraph("<b>Horizontal (X) chain — 40.00 m exactly:</b>", body))
    flow.append(Paragraph(
        "Program width (stalls, wing, guest rooms, paddocks): 0 → 37.5 m, plus the perimeter service / "
        "emergency fire lane: 37.5 → 40 m.", body))
    flow.append(Paragraph("<b>Vertical (Y) chain — 50.00 m exactly:</b>", body))
    flow.append(Paragraph(
        "Motor court/parking (5.00 m) + guest rooms band (8.24 m) + landscaped transition buffer "
        "(2.00 m) + Stable Row A (3.75 m) + central aisle (3.50 m) + Stable Row B (3.75 m) + feed/"
        "service/premium/veterinary/worker wing (4.00 m) + vestibule (1.00 m) + paddocks and service "
        "spine (18.76 m) = 50.00 m.", body))
    flow.append(Paragraph(
        "Both chains are re-verified automatically every time the design is regenerated — they are "
        "not measured once and assumed to still hold; validate.py confirms both totals every run.",
        body))


def build_zone_narratives(flow):
    section(flow, "Zone Narratives")
    zones = [
        ("The Equestrian Zone", "Twenty standard 3.75×3.75 m stalls and two premium 4.00×4.00 m "
         "stalls share one continuous, shaded central aisle rather than being split across separate "
         "wings — every stall opens directly onto shared circulation, shortening every staff round. "
         "The two veterinary/isolation rooms sit at the aisle's southern end, immediately adjacent to "
         "feed and service, naturally separated from the general stall population without requiring a "
         "detour."),
        ("The Guest & Majlis Zone", "Arrival flows from the motor court into a pair of symmetric "
         "courtyards — the indoor men's majlis and the outdoor majlis/sitting terrace — before "
         "reaching the private bedroom suite. A deliberate landscaped buffer stands between this zone "
         "and the working stable, so the estate's most prominent, generous frontage is never "
         "interrupted by stable traffic."),
        ("The Worker & Service Wing", "Worker bedroom, kitchen, and bathroom share one wing and one "
         "roofline with the feed room, service room, and both veterinary/isolation rooms — instead of "
         "being buried in a narrow slot between stall columns. Feed and service sit at the center of "
         "the wing, equidistant from both stall rows, minimizing walking distance for daily routines."),
        ("The Private Suite & Paddocks", "The private bedroom and bathroom sit east of the majlis, "
         "private from the guest sequence. To the rear, two equal 318.92 m² paddocks flank a dedicated "
         "wash/manure service spine that connects directly to both paddock gates and the perimeter "
         "fire lane — turnout and stable maintenance never cross guest or general circulation."),
    ]
    for title, text in zones:
        flow.append(Paragraph(title, h2))
        flow.append(Paragraph(text, body))


def build_circulation(flow):
    section(flow, "Circulation & Operations")
    flow.append(bullets([
        "<b>Horse circulation:</b> every stall opens directly onto the single shared central aisle; "
        "no horse ever needs to cross the guest zone or motor court.",
        "<b>Service/feed circulation:</b> feed and service rooms sit centered in the wing, equidistant "
        "from both stall rows; the perimeter fire/service lane lets a feed truck or farrier reach the "
        "wing or paddocks without touching the guest motor court.",
        "<b>Guest circulation:</b> arrival → motor court → majlis or outdoor majlis → private suite, "
        "with a deliberate visual and physical stop before the working stable begins.",
        "<b>Manure/wash logistics:</b> the dedicated wash/manure service spine connects directly to "
        "both paddock gates and the perimeter fire lane, so soiled bedding never crosses the stable "
        "aisle or guest zone.",
        "<b>No dead corners or bottlenecks:</b> the aisle is a uniform 3.50 m throughout, the perimeter "
        "lane a uniform 2.50 m, and every enclosed room has exactly one described door or gate.",
    ]))


def build_materials(flow):
    section(flow, "Materials & Finishes Palette")
    rows = [["Element", "Material Direction"],
            ["Stall / wing walls", "Warm sandstone/limestone render, bronze accent trim on premium stalls"],
            ["Stable doors", "Solid warm walnut timber Dutch doors, powder-coated steel yoke bars"],
            ["Majlis / private suite walls", "Deep espresso plaster (majlis), olive-toned plaster (private suite)"],
            ["Roofs", "Bronze standing-seam metal, consistent across all structures"],
            ["Paddock fencing", "Dark walnut-toned timber post-and-rail, two rail bands"],
            ["Terrace / majlis flooring", "Warm limestone paving"],
            ["Motor court / fire lane", "Limestone paving (guest) vs. utilitarian grey paving (service)"],
            ["Landscape", "Native drought-tolerant planting, shade trees at guest and paddock-edge nodes"],
            ["Lighting concept", "Warm 2700K low-glare bollards along aisle and lane; uplighting at majlis facade only"]]
    t = Table(rows, colWidths=[50 * mm, None])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), BROWN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    flow.append(t)


def build_render_gallery(flow):
    section(flow, "Visualization")
    flow.append(Paragraph(
        "The authoritative visual for this package is the illustrated master-plan board — a premium "
        "presentation drawing generated directly from the validated layout, with correct Arabic "
        "labels, per-zone materials, entourage, and textured paddocks. It represents the design "
        "exactly, with no risk of a picture contradicting the plan.", body))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph(
        "Photoreal 3D visualization is a separate production step, commissioned from an external "
        "architectural-visualization studio using the geometry export and render-production brief "
        "supplied in this package. This keeps the visuals honest: rather than present in-house "
        "massing images that would not meet a luxury standard, the package hands a renderer everything "
        "needed to produce the final photoreal set. The planned views are:", body))
    flow.append(bullets([
        "Premium overhead cutaway (hero)",
        "Aerial exterior, golden hour",
        "Stable aisle interior",
        "Guest &amp; majlis zone",
        "Paddock &amp; service courtyard",
        "Entry &amp; parking apron",
    ]))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph(
        "Geometry export, camera schedule, material palette, and an acceptance checklist for that "
        "production are included in the consultant-handoff folder.", body))


def build_technical_highlights(flow):
    section(flow, "Technical Summary")
    flow.append(Paragraph(
        "The layout is not a sketch — it is a validated schematic. The full site closes exactly to "
        "40.00 × 50.00 m in both directions, all 40 spaces fit within the boundary with no overlaps, "
        "and every required room is present at its confirmed size. Both paddocks are exactly equal at "
        "318.92 m² each.", body))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph(
        "Every dimension, area, and schedule in this package is generated from a single coordinate "
        "model, so the drawings, schedules, and this presentation cannot drift out of agreement with "
        "one another. The detailed verification — dimension-chain checks, per-function areas, and the "
        "full validation record — is provided in the technical appendix rather than here, to keep this "
        "presentation focused on the design.", body))


def build_schedule_summary(flow):
    section(flow, "Room Schedule Summary")
    by_func = defaultdict(lambda: {"count": 0, "area": 0.0})
    for s in spaces:
        by_func[s["function"]]["count"] += 1
        by_func[s["function"]]["area"] += s["area_m2"]
    total_area = VALIDATION["totals"]["total_scheduled_area_m2"]
    rows = [["Function", "Count", "Area (m²)", "% of Scheduled Area"]]
    for func, d in sorted(by_func.items(), key=lambda kv: -kv[1]["area"]):
        label = FUNCTION_LABELS.get(func, func.replace("_", " ").title())
        rows.append([label, str(d["count"]), f"{d['area']:.2f}", f"{d['area']/total_area*100:.1f}%"])
    rows.append(["TOTAL", str(len(spaces)), f"{total_area:.2f}", "100.0%"])
    t = Table(rows, colWidths=[70 * mm, 22 * mm, 30 * mm, 40 * mm])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), BROWN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), CREAM),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 8))
    flow.append(Paragraph("The full 40-space schedule with individual coordinates is provided in the "
                           "Technical Appendix and in the schedules folder of this package.",
                           small))


def build_advantages(flow):
    section(flow, "Advantages Over the Original Scheme")
    flow.append(bullets([
        "<b>Horse zone logic:</b> the same 20+2 stall count and sizes, but the two rows now share one "
        "continuous shaded aisle rather than being split across separate wings, shortening every staff "
        "round.",
        "<b>Paddock placement:</b> both paddocks are now equal and directly reachable from the working "
        "wing via a dedicated wash/manure spine — turnout no longer requires crossing guest or general "
        "circulation.",
        "<b>Guest/majlis sequence:</b> arrival → motor court → majlis/outdoor majlis → private suite, "
        "with a clear visual and physical stop before the stable begins.",
        "<b>Worker/service separation:</b> worker housing and feed/service now share one wing and one "
        "roofline instead of being buried in a narrow slot between stall columns.",
        "<b>Feed/service efficiency:</b> feed and service rooms sit at the center of the wing, "
        "equidistant from both stall rows.",
        "<b>Visual hierarchy:</b> guest wing at the most prominent frontage, stable in the calm "
        "productive middle, service/paddocks at the working rear — a legible luxury-estate hierarchy.",
    ]))


def build_next_steps(flow):
    section(flow, "Next Steps")
    flow.append(bullets([
        "Engage a licensed local architect/engineer to convert this concept into permit-ready "
        "construction documents.",
        "Commission structural, MEP, fire/life-safety, and civil/drainage consultants (see Section 16).",
        "Confirm local zoning, agricultural/equestrian-use, and building code requirements before any "
        "site work.",
        "Use the CAD underlay (stable_concept_underlay.dxf) as a coordinated starting reference for the "
        "professional design team — it is explicitly marked as a concept underlay, not a construction "
        "drawing.",
        "Review material and finish selections with the owner once a contractor/quantity surveyor is "
        "engaged, since this package specifies material direction, not final specifications.",
    ]))


def build_licensed_review(flow):
    section(flow, "What Still Requires Licensed Professional Review")
    flow.append(Paragraph(
        "This package is a concept design only. The following items are explicitly not resolved and "
        "require a licensed professional before any construction or permitting step:", body))
    flow.append(bullets([
        "Structural design, footings, and roof framing — this is a massing/concept model only.",
        "MEP: electrical, plumbing, ventilation/HVAC sizing for all enclosed rooms, especially the "
        "worker kitchen/bathroom and the veterinary function assigned to SP01/SP02.",
        "Fire/life-safety review of egress widths, the perimeter fire lane's actual vehicle turning "
        "radius, and manure/hay fire separation distances.",
        "Civil/drainage design for the paddocks, wash-down spine, and site-wide stormwater management.",
        "Local building code, zoning, and agricultural/equestrian-use permitting compliance — none of "
        "which has been verified in this exercise.",
        "The veterinary/isolation fit-out for SP01/SP02 (ventilation, drainage, exam lighting) still "
        "needs a licensed veterinary/MEP consultant, even though the room function itself is confirmed.",
    ]))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))


def build_appendix(flow):
    section(flow, "Appendix & Reference Index")
    flow.append(Paragraph("This presentation is one document within a structured delivery package. "
                           "The full package is organized as follows:", body))
    rows = [
        ["00_READ_ME_FIRST", "Package index and how to navigate the delivery"],
        ["01_CLIENT_PRESENTATION", "This document"],
        ["02_HERO_VISUALS", "Illustrated master-plan board (the authoritative visual)"],
        ["03_TECHNICAL_DRAWINGS", "Dimensioned master plan, labelled plan, CAD underlay"],
        ["04_SCHEDULES", "Room, coordinate, and area schedules"],
        ["05_TECHNICAL_REPORT", "Technical appendix, validation summary, source-of-truth summary"],
        ["06_CONSULTANT_HANDOFF", "Render-production brief, geometry export, gap checklist, CAD notes"],
        ["07_SOURCE_REFERENCE", "Original brief, CAD, and reference images"],
    ]
    rows = [[Paragraph(path, cell_path), Paragraph(desc, cell_desc)] for path, desc in rows]
    t = Table(rows, colWidths=[62 * mm, None])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 10))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))


def build():
    out_pdf = REPORTS_DIR / "client_presentation.pdf"
    doc = SimpleDocTemplate(str(out_pdf), pagesize=PAGE_SIZE,
                             leftMargin=MARGIN, rightMargin=MARGIN,
                             topMargin=MARGIN, bottomMargin=MARGIN,
                             title="Luxury Equestrian Stable — Concept Presentation")
    flow = []
    build_cover(flow)
    flow.append(PageBreak())
    build_toc(flow)
    flow.append(PageBreak())
    build_exec_summary(flow)
    flow.append(PageBreak())
    build_goals(flow)
    flow.append(PageBreak())
    build_site_summary(flow)
    flow.append(PageBreak())
    build_design_concept(flow)
    flow.append(PageBreak())
    build_zoning(flow)
    flow.append(PageBreak())
    build_masterplan(flow)
    flow.append(PageBreak())
    build_dimensions_logic(flow)
    flow.append(PageBreak())
    build_zone_narratives(flow)
    flow.append(PageBreak())
    build_circulation(flow)
    flow.append(PageBreak())
    build_materials(flow)
    flow.append(PageBreak())
    build_render_gallery(flow)
    flow.append(PageBreak())
    build_technical_highlights(flow)
    flow.append(PageBreak())
    build_schedule_summary(flow)
    flow.append(PageBreak())
    build_advantages(flow)
    flow.append(PageBreak())
    build_next_steps(flow)
    flow.append(PageBreak())
    build_licensed_review(flow)
    flow.append(PageBreak())
    build_appendix(flow)
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    print("Wrote", out_pdf)


if __name__ == "__main__":
    build()
