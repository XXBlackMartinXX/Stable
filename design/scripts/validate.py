"""
Mathematical Validation Agent (script form).
Runs coordinate/area/overlap/program checks against design/scripts/model.py
and writes validation_report.json + validation_report.txt.

Concept plan only. Not for construction or permit use.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH, Y_BANDS, X_BANDS  # noqa: E402

from shapely.geometry import box

OUT_DIR = Path(__file__).parent.parent / "output" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

passed = []
failed = []
warnings = []

def check(name, condition, detail=""):
    if condition:
        passed.append({"check": name, "detail": detail})
    else:
        failed.append({"check": name, "detail": detail})

# 1. Site boundary exact
check("Site width == 40.00 m", SITE_WIDTH == 40.00, f"SITE_WIDTH={SITE_WIDTH}")
check("Site depth == 50.00 m", SITE_DEPTH == 50.00, f"SITE_DEPTH={SITE_DEPTH}")

# enclosed rooms vs open/service zones
OPEN_FUNCS = {"paddock", "service_yard", "service_lane", "arrival_court", "outdoor_sitting"}
enclosed = [s for s in spaces if s["function"] not in OPEN_FUNCS or s["function"] == "paddock"]
# paddocks are fenced program spaces -> still check bounds + overlap, but not "enclosed building"
all_spaces = spaces

# 2. No room extends outside the site
out_of_bounds = []
for s in all_spaces:
    if s["x_min"] < 0 or s["y_min"] < 0 or s["x_max"] > SITE_WIDTH or s["y_max"] > SITE_DEPTH:
        out_of_bounds.append(s["id"])
check("All spaces fit inside site boundary", len(out_of_bounds) == 0, f"out_of_bounds={out_of_bounds}")

# 3. No overlaps between any two spaces (using shapely, exact geometry, tolerance 1mm^2)
# Exception: "parking" is a marked open-air sub-area within the arrival court, not a separate
# enclosed structure, so it is expected to overlap "arrival_court" - not a design defect.
NESTED_OPEN_PAIRS = {frozenset({"parking", "arrival_court"})}
by_id = {s["id"]: s for s in all_spaces}
polys = {s["id"]: box(s["x_min"], s["y_min"], s["x_max"], s["y_max"]) for s in all_spaces}
overlaps = []
ids = list(polys.keys())
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        fa, fb = by_id[ids[i]]["function"], by_id[ids[j]]["function"]
        if frozenset({fa, fb}) in NESTED_OPEN_PAIRS:
            continue
        a, b = polys[ids[i]], polys[ids[j]]
        if a.intersects(b):
            inter = a.intersection(b)
            if inter.area > 1e-6:
                overlaps.append((ids[i], ids[j], round(inter.area, 6)))
check("No overlapping spaces (parking-within-motor-court exempted)", len(overlaps) == 0, f"overlaps={overlaps}")

# 4. Stall counts exact
standard_stalls = [s for s in spaces if s["function"] == "horse_stall"]
premium_stalls = [s for s in spaces if s["function"] == "premium_horse_stall"]
special_rooms = [s for s in spaces if s["function"] == "special_horse_room_UNCONFIRMED"]
paddocks = [s for s in spaces if s["function"] == "paddock"]
feed_rooms = [s for s in spaces if s["function"] == "feed_room"]
service_rooms = [s for s in spaces if s["function"] == "service_room"]

check("Exactly 20 standard horse stalls", len(standard_stalls) == 20, f"count={len(standard_stalls)}")
check("Exactly 2 premium horse stalls", len(premium_stalls) == 2, f"count={len(premium_stalls)}")
check("Exactly 2 special horse rooms (label unresolved, flagged)", len(special_rooms) == 2, f"count={len(special_rooms)}")
check("Exactly 2 paddocks", len(paddocks) == 2, f"count={len(paddocks)}")
check("Exactly 1 feed room", len(feed_rooms) == 1, f"count={len(feed_rooms)}")
check("Exactly 1 service room", len(service_rooms) == 1, f"count={len(service_rooms)}")

# 5. Mandatory room sizes match
bad_standard = [s["id"] for s in standard_stalls if (s["width_m"], s["depth_m"]) != (3.75, 3.75)]
check("All standard stalls are 3.75 x 3.75 m", len(bad_standard) == 0, f"bad={bad_standard}")

bad_premium = [s["id"] for s in premium_stalls if (s["width_m"], s["depth_m"]) != (4.00, 4.00)]
check("All premium stalls are 4.00 x 4.00 m", len(bad_premium) == 0, f"bad={bad_premium}")

bad_feed = [s["id"] for s in feed_rooms if (s["width_m"], s["depth_m"]) != (4.00, 4.00)]
check("Feed room is 4.00 x 4.00 m", len(bad_feed) == 0, f"bad={bad_feed}")

bad_service = [s["id"] for s in service_rooms if (s["width_m"], s["depth_m"]) != (3.00, 3.00)]
check("Service room is 3.00 x 3.00 m", len(bad_service) == 0, f"bad={bad_service}")

# 6. Required program checklist presence
required_functions = {
    "worker_bedroom": "Worker bedroom (4 workers)",
    "worker_bathroom": "Worker bathroom",
    "worker_kitchen": "Worker kitchen",
    "majlis": "Men's majlis",
    "mens_wc": "Men's WC",
    "outdoor_sitting": "Outdoor sitting area",
    "private_bedroom": "Private bedroom",
    "private_bathroom": "Private bathroom",
}
for func, label in required_functions.items():
    present = any(s["function"] == func for s in spaces)
    check(f"Program item present: {label}", present, f"function={func}")

# 7. Dimension chain closes (X and Y bands sum exactly to site dims)
x_sum = round(sum(b[2] - b[1] for b in X_BANDS), 6)
y_sum = round(sum(b[2] - b[1] for b in Y_BANDS), 6)
check("Horizontal (X) dimension chain totals exactly 40.00 m", x_sum == 40.00, f"sum={x_sum}")
check("Vertical (Y) dimension chain totals exactly 50.00 m", y_sum == 50.00, f"sum={y_sum}")

# 8. Paddock size consistency (both paddocks equal area, matches notes/report)
paddock_areas = sorted(set(s["area_m2"] for s in paddocks))
check("Both paddocks have identical, consistent area", len(paddock_areas) == 1, f"areas={paddock_areas}")

# 9. Area sum sanity: total footprint <= site area
total_area = sum(s["area_m2"] for s in all_spaces)
site_area = SITE_WIDTH * SITE_DEPTH
check("Total scheduled area does not exceed site area", total_area <= site_area + 1e-6,
      f"total_area={round(total_area,2)}, site_area={site_area}")

# 10. Every room has a door/gate note (functional access)
missing_doors = [s["id"] for s in all_spaces if not s.get("door")]
check("Every space has a defined door/gate location", len(missing_doors) == 0, f"missing={missing_doors}")

# Warnings (non-blocking, honest disclosure)
assumption_items = [s["id"] for s in spaces if s["source"] in ("redesign_choice", "redesign_improvement")]
warnings.append({
    "warning": "Rooms sized/reflowed by redesign choice (no exact dimension in source, or deliberately "
               "changed from an inconsistent/inefficient existing layout) - see model.py notes per room",
    "items": assumption_items,
})
unresolved_label_items = [s["id"] for s in spaces if "UNRESOLVED" in s["source"] or "UNCONFIRMED" in s["function"]]
warnings.append({
    "warning": "Special horse room Arabic label (مصلب / مصاب) is unresolved; function not finalized",
    "items": unresolved_label_items,
})
warnings.append({
    "warning": "Service room sized 3.00x3.00m per Requirments.txt (explicit requirement); stable 1.pdf CAD "
               "dimensions the same room at 6.00x3.00m. Owner should confirm which governs.",
    "items": ["SV01"],
})
warnings.append({
    "warning": "Outdoor majlis/sitting width (OSA01) and private bathroom width (PBTH01) were not fully "
               "legible in stable 1.pdf; sized by redesign choice (see model.py notes). Confirm with owner.",
    "items": ["OSA01", "PBTH01"],
})
warnings.append({
    "warning": "Parking apron (PK01) found only in the rendered image, not in Requirments.txt or stable 1.pdf; "
               "included as an optional upgrade pending owner confirmation.",
    "items": ["PK01"],
})

result = {
    "site": {"width_m": SITE_WIDTH, "depth_m": SITE_DEPTH, "area_m2": site_area},
    "totals": {
        "space_count": len(all_spaces),
        "total_scheduled_area_m2": round(total_area, 2),
        "x_dimension_chain_sum_m": x_sum,
        "y_dimension_chain_sum_m": y_sum,
    },
    "passed_checks": passed,
    "failed_checks": failed,
    "warnings": warnings,
    "status": "PASS" if len(failed) == 0 else "FAIL",
}

(OUT_DIR / "validation_report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))

lines = []
lines.append("STABLE REDESIGN - MATHEMATICAL VALIDATION REPORT")
lines.append("Concept plan only. Not for construction or permit use until reviewed and approved by a licensed")
lines.append("local architect/engineer, MEP/civil engineer, and fire/life-safety consultant.")
lines.append("=" * 78)
lines.append(f"Site: {SITE_WIDTH} m x {SITE_DEPTH} m = {site_area} m^2")
lines.append(f"Total spaces scheduled: {len(all_spaces)}")
lines.append(f"Total scheduled area: {round(total_area,2)} m^2")
lines.append(f"X dimension chain sum: {x_sum} m (must equal 40.00)")
lines.append(f"Y dimension chain sum: {y_sum} m (must equal 50.00)")
lines.append(f"OVERALL STATUS: {result['status']}")
lines.append("=" * 78)
lines.append(f"\nPASSED CHECKS ({len(passed)}):")
for p in passed:
    lines.append(f"  [PASS] {p['check']} -- {p['detail']}")
lines.append(f"\nFAILED CHECKS ({len(failed)}):")
for f in failed:
    lines.append(f"  [FAIL] {f['check']} -- {f['detail']}")
lines.append(f"\nWARNINGS ({len(warnings)}):")
for w in warnings:
    lines.append(f"  [WARN] {w['warning']}")
    if w["items"]:
        lines.append(f"         items: {', '.join(w['items'])}")

(OUT_DIR / "validation_report.txt").write_text("\n".join(lines))

print("\n".join(lines))
print(f"\nWritten to {OUT_DIR}")
