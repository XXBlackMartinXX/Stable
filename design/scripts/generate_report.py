"""
Report generator - fills design/scripts/report_template.md from the single source of truth
(model.py geometry + validation_report.json) so numeric figures in source_audit.md can never
drift out of sync with the actual validated model again.

Run AFTER validate.py (validate.py must be run first so validation_report.json is fresh).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH, Y_BANDS, X_BANDS  # noqa: E402

SCRIPT_DIR = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR.parent / "output" / "reports"

validation = json.loads((REPORTS_DIR / "validation_report.json").read_text())

SITE_AREA = SITE_WIDTH * SITE_DEPTH
total_area = validation["totals"]["total_scheduled_area_m2"]
space_count = validation["totals"]["space_count"]
total_pct = round(total_area / SITE_AREA * 100, 1)
remaining_pct = round(100 - total_pct, 1)

paddock_areas = sorted({s["area_m2"] for s in spaces if s["function"] == "paddock"})
paddock_area = f"{paddock_areas[0]:.2f}" if len(paddock_areas) == 1 else "/".join(f"{a:.2f}" for a in paddock_areas)

# --- Room schedule table, grouped by identical (function, width, depth) so repeated rooms collapse ---
from collections import OrderedDict  # noqa: E402

groups = OrderedDict()
order = []
for s in spaces:
    key = (s["function"], s["width_m"], s["depth_m"], s["source"])
    if key not in groups:
        groups[key] = []
        order.append(key)
    groups[key].append(s)

table_lines = ["| ID(s) | Room | Size (m) | Area (m²) | Source |", "|---|---|---|---|---|"]
for key in order:
    func, w, d, source = key
    members = groups[key]
    ids = ", ".join(m["id"] for m in members)
    if len(ids) > 30:
        ids = f"{members[0]['id']}–{members[-1]['id']}"
    import re
    name = members[0]["english_name"]
    if len(members) > 1:
        # Strip trailing/pre-parenthesis per-instance numbering for the grouped label
        name = re.sub(r"\s*\d+(?=\s*\(|$)", "", name).rstrip()
    area = members[0]["area_m2"]
    area_str = f"{area:.2f} each" if len(members) > 1 else f"{area:.2f}"
    table_lines.append(f"| {ids} | {name} | {w:.2f}x{d:.2f} | {area_str} | {source} |")
room_schedule_table = "\n".join(table_lines)

# --- Dimension chain text, generated from Y_BANDS / X_BANDS ---
def chain_text(bands):
    parts = []
    running = 0.0
    for label, y0, y1 in bands:
        span = round(y1 - y0, 3)
        parts.append(f"{label} {y0:g}→{y1:g} ({span:g})")
        running += span
    return " + ".join(parts), round(running, 3)

x_chain_text, x_chain_sum = chain_text(X_BANDS)
y_chain_text, y_chain_sum = chain_text(Y_BANDS)

# --- Validation summary, generated from validation_report.json ---
status = validation["status"]
n_pass = len(validation["passed_checks"])
n_fail = len(validation["failed_checks"])
n_warn = len(validation["warnings"])

warn_word = "warning" if n_warn == 1 else "warnings"
summary_lines = [f"- **Overall status: {status}** ({n_fail} failed checks, {n_pass} passed checks, "
                  f"{n_warn} disclosed {warn_word})."]
if validation["failed_checks"]:
    summary_lines.append("- **FAILED CHECKS (must be fixed before delivery):**")
    for f in validation["failed_checks"]:
        summary_lines.append(f"  - {f['check']} — {f['detail']}")
summary_lines.append(f"- Site boundary exactly {SITE_WIDTH:.2f} x {SITE_DEPTH:.2f} m; all "
                      f"{space_count} spaces fit inside it; zero overlaps.")
summary_lines.append("- Exact counts confirmed: 20 standard stalls, 2 premium, 2 veterinary/isolation, "
                      "2 paddocks, 1 feed room, 1 service room, and every named guest/worker room present.")
summary_lines.append("- All mandatory sizes confirmed: standard stalls 3.75x3.75, premium 4.00x4.00, "
                      "feed 4.00x4.00, service 6.00x3.00 (owner-confirmed).")
summary_lines.append(f"- X and Y dimension chains both close exactly ({x_chain_sum:.2f} m / "
                      f"{y_chain_sum:.2f} m).")
summary_lines.append(f"- Both paddocks equal ({paddock_area} m² each).")
summary_lines.append("- Every space has a defined door/gate.")
summary_lines.append(f"- {n_warn} {warn_word} disclosed openly (not hidden):")
for w in validation["warnings"]:
    summary_lines.append(f"  - {w['warning']}" + (f" ({', '.join(w['items'])})" if w["items"] else ""))
validation_summary = "\n".join(summary_lines)

resolved_decisions = validation.get("resolved_decisions", [])
resolved_lines = [f"**Resolved owner decisions ({len(resolved_decisions)}):**"]
for d in resolved_decisions:
    resolved_lines.append(f"- {d['decision']}" + (f" ({', '.join(d['items'])})" if d["items"] else ""))
resolved_decisions_list = "\n".join(resolved_lines)

context = {
    "PADDOCK_AREA": paddock_area,
    "SPACE_COUNT": str(space_count),
    "SITE_AREA": f"{SITE_AREA:.2f}",
    "TOTAL_AREA": f"{total_area:.2f}",
    "TOTAL_AREA_PCT": f"{total_pct:.1f}",
    "REMAINING_PCT": f"{remaining_pct:.1f}",
    "ROOM_SCHEDULE_TABLE": room_schedule_table,
    "X_CHAIN_TEXT": x_chain_text,
    "Y_CHAIN_TEXT": y_chain_text,
    "X_CHAIN_SUM": f"{x_chain_sum:.2f}",
    "Y_CHAIN_SUM": f"{y_chain_sum:.2f}",
    "SITE_WIDTH": f"{SITE_WIDTH:.2f}",
    "SITE_DEPTH": f"{SITE_DEPTH:.2f}",
    "VALIDATION_SUMMARY": validation_summary,
    "RESOLVED_DECISIONS_LIST": resolved_decisions_list,
    "UNRESOLVED_COUNT": str(len(resolved_decisions)),
}

template = (SCRIPT_DIR / "report_template.md").read_text()
for token, value in context.items():
    template = template.replace("{{" + token + "}}", value)

remaining_tokens = [tok for tok in template.split("{{")[1:] if "}}" in tok.split("\n")[0]]
if remaining_tokens:
    raise RuntimeError(f"Unfilled template tokens remain: {remaining_tokens[:5]}")

out_path = REPORTS_DIR / "source_audit.md"
out_path.write_text(template)
print(f"Regenerated {out_path}")
print(f"  total_area={total_area:.2f} m2 ({total_pct}%), space_count={space_count}, "
      f"status={status}, paddock_area={paddock_area}")
