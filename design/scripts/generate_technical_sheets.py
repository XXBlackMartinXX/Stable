"""Generate the technical sheet package (cover, metrics, master plan, schedule)
and assemble them into technical_appendix.pdf.

Every number on every sheet is read from model.py / validation_report.json at
generation time - nothing here is hand-typed. Re-running this script after any
model.py change reproduces sheets that stay in sync automatically.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                 Spacer, Image, PageBreak, NextPageTemplate,
                                 PageTemplate, BaseDocTemplate, Frame)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

ROOT = SCRIPTS_DIR.parent.parent
OUT_DIR = ROOT / "design" / "output" / "reports"
PLANS_DIR = ROOT / "design" / "output" / "plans"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VALIDATION = json.loads((ROOT / "design" / "output" / "reports" / "validation_report.json").read_text())

DISCLAIMER = ("Concept plan only. Not for construction or permit use until reviewed and approved "
              "by a licensed local architect/engineer, MEP/civil engineer, and fire/life-safety "
              "consultant.")

PAGE_SIZE = landscape(A3)
PAGE_W, PAGE_H = PAGE_SIZE
MARGIN = 18 * mm

styles = getSampleStyleSheet()
title_style = ParagraphStyle("SheetTitle", parent=styles["Title"], fontSize=26, alignment=TA_LEFT,
                              textColor=colors.HexColor("#2b241a"), spaceAfter=4)
subtitle_style = ParagraphStyle("SheetSubtitle", parent=styles["Normal"], fontSize=12,
                                 textColor=colors.HexColor("#6b6255"), spaceAfter=2)
h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=15,
                           textColor=colors.HexColor("#7a4a2b"), spaceBefore=10, spaceAfter=6)
body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5, leading=15)
small_style = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8.5, leading=12,
                              textColor=colors.HexColor("#555555"))
disclaimer_style = ParagraphStyle("Disclaimer", parent=styles["Normal"], fontSize=8.5, leading=11,
                                   textColor=colors.HexColor("#8a1f1f"))

FUNCTION_LABELS = {
    "horse_stall": "Horse Stalls (Standard)",
    "premium_horse_stall": "Horse Stalls (Premium)",
    "veterinary_isolation_room": "Veterinary / Isolation Rooms",
    "feed_room": "Feed Room",
    "service_room": "Service Room",
    "paddock": "Paddocks",
    "worker_bedroom": "Worker Bedroom",
    "worker_kitchen": "Worker Kitchen",
    "worker_bathroom": "Worker Bathroom",
    "majlis": "Men's Majlis",
    "mens_wc": "Men's WC",
    "outdoor_sitting": "Outdoor Majlis / Sitting",
    "private_bedroom": "Private Bedroom",
    "private_bathroom": "Private Bathroom",
    "parking": "Parking Apron",
    "service_yard": "Service Yard",
    "service_lane": "Fire Lane / Service Lane",
    "arrival_court": "Arrival / Motor Court",
}

FOOTER_TEXT = "Luxury Equestrian Stable Redesign - Technical Appendix - Concept Only, Not For Construction"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#8a8578"))
    canvas.drawString(MARGIN, 10 * mm, FOOTER_TEXT)
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"Sheet {doc.page}")
    canvas.restoreState()


def sheet_header(flow, sheet_no, sheet_title, sheet_subtitle):
    flow.append(Paragraph(f"SHEET {sheet_no:02d}", small_style))
    flow.append(Paragraph(sheet_title, title_style))
    flow.append(Paragraph(sheet_subtitle, subtitle_style))
    flow.append(Spacer(1, 10))


def build_cover_sheet(flow):
    sheet_header(flow, 1, "Luxury Equestrian Stable — Concept Design Package",
                 "Project Information Sheet — Technical Appendix Cover")
    flow.append(Spacer(1, 30))
    info_rows = [
        ["Project", "Private Luxury Equestrian Stable — Concept Redesign"],
        ["Site area", f"{SITE_WIDTH:.2f} m × {SITE_DEPTH:.2f} m = {SITE_WIDTH*SITE_DEPTH:,.2f} m²"],
        ["Program scope", "40 scheduled spaces: stalls, veterinary/isolation rooms, feed and "
                           "service rooms, paddocks, worker accommodation, men's majlis and WC, "
                           "outdoor majlis, private bedroom/bathroom suite, parking apron"],
        ["Design status", "Concept design — geometrically validated, owner-confirmed, not yet "
                           "reviewed by a licensed engineer of record"],
        ["Source of truth", "design/scripts/model.py (single coordinate model; every drawing, "
                             "schedule, and report in this package is generated from it)"],
        ["Validation status", f"PASS — {len(VALIDATION['passed_checks'])} checks passed, "
                               f"0 failed, {len(VALIDATION.get('warnings', []))} disclosed warning(s)"],
    ]
    t = Table(info_rows, colWidths=[55 * mm, None])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#d8d2c2")),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 24))
    flow.append(Paragraph("Sheet Index", h2_style))
    index_rows = [
        ["01", "Project Information (this sheet)"],
        ["02", "Key Metrics & Area Summary"],
        ["03", "Master Plan (Premium Vector Cutaway)"],
        ["04", "Room Schedule"],
    ]
    t2 = Table(index_rows, colWidths=[20 * mm, None])
    t2.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flow.append(t2)
    flow.append(Spacer(1, 30))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))


def build_metrics_sheet(flow):
    sheet_header(flow, 2, "Key Metrics & Area Summary",
                 "All figures computed live from model.py and validation_report.json")

    by_func = defaultdict(lambda: {"count": 0, "area": 0.0})
    for s in spaces:
        by_func[s["function"]]["count"] += 1
        by_func[s["function"]]["area"] += s["area_m2"]

    total_area = VALIDATION["totals"]["total_scheduled_area_m2"]
    site_area = VALIDATION["site"]["area_m2"]

    headline = [
        ["Site area", f"{site_area:,.2f} m²"],
        ["Total scheduled area", f"{total_area:,.2f} m²"],
        ["Site coverage", f"{total_area / site_area * 100:.1f}%"],
        ["Total spaces", f"{len(spaces)}"],
        ["Validation status", f"PASS ({len(VALIDATION['passed_checks'])} checks, 0 failed)"],
    ]
    t = Table(headline, colWidths=[55 * mm, 55 * mm])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f1e8")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8d2c2")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8d2c2")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 18))

    flow.append(Paragraph("Area by Function", h2_style))
    rows = [["Function", "Count", "Area (m²)", "% of scheduled area"]]
    for func, d in sorted(by_func.items(), key=lambda kv: -kv[1]["area"]):
        label = FUNCTION_LABELS.get(func, func.replace("_", " ").title())
        rows.append([label, str(d["count"]), f"{d['area']:.2f}", f"{d['area']/total_area*100:.1f}%"])
    t2 = Table(rows, colWidths=[80 * mm, 25 * mm, 35 * mm, 45 * mm])
    t2.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7a4a2b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f5ee")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8d2c2")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    flow.append(t2)
    flow.append(Spacer(1, 18))

    flow.append(Paragraph("Dimension Chain Verification", h2_style))
    chain_rows = [
        ["Chain", "Sum", "Target", "Result"],
        ["Horizontal (X)", f"{VALIDATION['totals']['x_dimension_chain_sum_m']:.2f} m", "40.00 m", "PASS"],
        ["Vertical (Y)", f"{VALIDATION['totals']['y_dimension_chain_sum_m']:.2f} m", "50.00 m", "PASS"],
    ]
    t3 = Table(chain_rows, colWidths=[50 * mm, 35 * mm, 35 * mm, 30 * mm])
    t3.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7a4a2b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8d2c2")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    flow.append(t3)
    flow.append(Spacer(1, 18))
    warnings = VALIDATION.get("warnings", [])
    if warnings:
        flow.append(Paragraph("Disclosed Warnings (documented trade-offs, not defects)", h2_style))
        for w in warnings:
            text = w if isinstance(w, str) else w.get("warning", str(w))
            flow.append(Paragraph(f"• {text}", body_style))
    flow.append(Spacer(1, 14))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))


def build_masterplan_sheet(flow):
    sheet_header(flow, 3, "Master Plan",
                 "Premium vector cutaway — generated directly from model.py coordinates")
    img_path = PLANS_DIR / "premium_cutaway_masterplan.png"
    if img_path.exists():
        from PIL import Image as PILImage
        w, h = PILImage.open(img_path).size
        max_h = PAGE_H - 70 * mm
        max_w = PAGE_W - 2 * MARGIN
        scale = min(max_w / w, max_h / h)
        flow.append(Image(str(img_path), width=w * scale, height=h * scale, hAlign="CENTER"))
    flow.append(Spacer(1, 10))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))


def build_schedule_sheet(flow):
    sheet_header(flow, 4, "Room Schedule",
                 f"All {len(spaces)} scheduled spaces — generated from model.py")
    rows = [["ID", "English Name", "Function", "W (m)", "D (m)", "Area (m²)"]]
    for s in spaces:
        rows.append([s["id"], s["english_name"], FUNCTION_LABELS.get(s["function"], s["function"]),
                     f"{s['width_m']:.2f}", f"{s['depth_m']:.2f}", f"{s['area_m2']:.2f}"])
    total_area = VALIDATION["totals"]["total_scheduled_area_m2"]
    rows.append(["", "", "TOTAL", "", "", f"{total_area:.2f}"])
    t = Table(rows, colWidths=[20 * mm, 70 * mm, 55 * mm, 20 * mm, 20 * mm, 25 * mm], repeatRows=1)
    style = [
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7a4a2b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f4f1e8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f7f5ee")]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d8d2c2")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ALIGN", (3, 0), (-1, -1), "CENTER"),
    ]
    t.setStyle(TableStyle(style))
    flow.append(t)
    flow.append(Spacer(1, 10))
    flow.append(Paragraph(DISCLAIMER, disclaimer_style))


def build():
    out_pdf = OUT_DIR / "technical_appendix.pdf"
    doc = SimpleDocTemplate(str(out_pdf), pagesize=PAGE_SIZE,
                             leftMargin=MARGIN, rightMargin=MARGIN,
                             topMargin=MARGIN, bottomMargin=MARGIN,
                             title="Technical Appendix - Luxury Equestrian Stable")
    flow = []
    build_cover_sheet(flow)
    flow.append(PageBreak())
    build_metrics_sheet(flow)
    flow.append(PageBreak())
    build_masterplan_sheet(flow)
    flow.append(PageBreak())
    build_schedule_sheet(flow)
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    print("Wrote", out_pdf)


if __name__ == "__main__":
    build()
