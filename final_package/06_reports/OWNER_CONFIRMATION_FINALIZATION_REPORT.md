# Owner Confirmation Finalization Report — Luxury Equestrian Stable Redesign

**Concept plan only. Not for construction or permit use until reviewed and approved by a licensed
local architect/engineer, MEP/civil engineer, and fire/life-safety consultant.**

This pass applies the owner's decisions on the 5 items previously flagged in
`FINAL_QA_LOCK_REPORT.md` / `design/output/reports/source_audit.md` §5, regenerates the full
pipeline from `model.py`, and fixes two rendering defects found during visual QA. No geometry was
changed beyond what those 5 decisions required.

## 1. Owner decisions applied

| # | Item | Decision | Geometry impact |
|---|---|---|---|
| 1 | Special horse rooms (SP01, SP02) label/function | **مصاب — injured/veterinary isolation room.** The CAD's alternate spelling "مصلب" is superseded. | None (size unchanged at 3.50x4.00 m); function/label/`source` field updated in `model.py`, `validate.py`, DXF layer name, SVG legend. |
| 2 | Service room (SV01) size | **6.00 x 3.00 m**, per stable 1.pdf CAD — supersedes the 3.00x3.00 m in Requirments.txt line 6. | SV01 resized 3.00x3.00 → 6.00x3.00 m. Required reflowing the whole wing band (see §2). |
| 3 | Parking apron (PK01) | **Keep as-is** (11.00x4.00 m, 4 bays). | None. |
| 4 | Outdoor majlis (OSA01) / private bathroom (PBTH01) widths | **Confirm current values** (8.00 m / 4.83 m). | None. |
| 5 | Worker bedroom (WB01) footprint/bunk layout | **Confirm current footprint** (7.00x4.00 m); bunk arrangement is an interior fit-out detail for later. | None. |

## 2. Wing-band reflow (consequence of decision #2)

SV01 growing from 3.00 m to 6.00 m wide no longer fit the original wing sequence (which had zero
spare width — it filled X0.50–37.00 of the 37.5 m usable band exactly). Rather than touch any
`required_program` room's confirmed size, the two adjoining **redesign-choice** rooms (no
source-mandated size) were narrowed to absorb the difference:

| Room | Before | After | Change |
|---|---|---|---|
| WK01 (Worker Kitchen) | 4.50 x 4.00 m (18 m²) | 3.50 x 4.00 m (14 m²) | −1.00 m width |
| WBTH01 (Worker Bathroom) | 3.00 x 4.00 m (12 m²) | 2.00 x 4.00 m (8 m²) | −1.00 m width |

The wing now spans X0.00–37.50 exactly (previously X0.50–37.00 with 1.00 m of unused margin),
flush with the stall rows above it. Every `required_program` room (P01, P02, SP01, SP02, FD01, and
now SV01) keeps its confirmed size unchanged. This trade-off is disclosed as a warning in
`validate.py`'s output, not hidden.

## 3. Rendering defects found and fixed during visual QA

Two real defects were found by actually opening the regenerated PNGs, not just re-running the
pipeline:

1. **Arabic legend text rendered as tofu boxes.** The SVG legend originally embedded the Arabic
   word "مصاب" directly. `cairosvg` (used to rasterize the SVG to PNG) does not perform per-glyph
   font fallback across a mixed-script font stack — reproduced in isolation: a `font-family`
   listing Helvetica/Arial before an Arabic font renders Arabic as empty boxes; reversing the order
   breaks the Latin text instead. Fix: replaced the embedded Arabic glyphs in the **rendered
   plans only** with a Latin transliteration ("mesab"); the Arabic name is still correct and intact
   in `model.py`, the CSV schedules, and this report's markdown (all of which render Arabic
   correctly through normal text encoding, not SVG rasterization).
2. **Narrow room labels overflowed their boxes.** WBTH01 (2.00 m wide) and MWC01 (1.76 m wide)
   had their ID text and dimension sub-label spill outside the room outline into neighboring rooms.
   Fix: room labels now compute a font size that fits the box width (down to a 5.5px floor), and
   the dimension sub-label is only drawn when it also fits legibly — otherwise it's omitted (the
   exact dimension remains available in the legend, schedule, and this report). Verified by
   zoomed-in crops of both previously-broken labels after the fix.

## 4. Validation status (after this pass)

| Metric | Value |
|---|---|
| Status | **PASS** |
| Passed checks | 27 |
| Failed checks | **0** |
| Warnings (disclosed) | 1 — the WK01/WBTH01 narrowing described in §2 |
| Resolved owner decisions tracked | 5 (all of §1) |
| Total scheduled area | 1,648.01 m² (82.4% of the 2,000.00 m² site) — up from 1,647.01 m² by the net +1.00 m² of the SV01/WK01/WBTH01 reflow |
| X dimension chain | 40.00 m exactly |
| Y dimension chain | 50.00 m exactly |
| Paddocks | 2 × 318.92 m² (equal, unchanged) |

## 5. Disclaimers and markings verified present

- Both plans (`plan_dimensioned.svg/.png`, `masterplan_luxury.svg/.png`) still carry: *"Concept
  plan only. Not for construction or permit use until reviewed and approved by a licensed local
  architect/engineer, MEP/civil engineer, and fire/life-safety consultant."* — confirmed visually,
  unclipped.
- `stable_concept_underlay.dxf` still carries *"LUXURY EQUESTRIAN STABLE - CONCEPT CAD UNDERLAY
  ONLY - NOT FOR CONSTRUCTION"* plus the same disclaimer sentence — confirmed by reading the DXF's
  TEXT entities directly.

## 6. Known gap (disclosed, not hidden)

The 3D SketchUp massing model (`Luxury_Equestrian_Stable_Concept.skp`, referenced in
`source_audit.md` §16) was built **before** this finalization pass. It still shows SV01 at its old
3.00x3.00 m size and does not reflect the WK01/WBTH01 narrowing. The 2D plans, DXF, CSVs, and this
report are all current as of this pass; only the `.skp` lags. It should be regenerated from the
current `model.py` before being used as a visual reference. This is tracked as an unchecked item in
`source_audit.md` §19.

## 7. Files changed this pass

Regenerated (by the pipeline, from `model.py`):
- `design/output/reports/validation_report.json` / `.txt`
- `design/output/reports/source_audit.md`
- `design/output/schedules/room_schedule.csv` / `coordinate_schedule.csv`
- `design/output/plans/plan_dimensioned.svg` / `.png`
- `design/output/plans/masterplan_luxury.svg` / `.png`
- `design/output/plans/stable_concept_underlay.dxf`

Edited directly (source of truth / tooling):
- `design/scripts/model.py` — owner decisions applied; wing band reflowed; provenance docstring
  updated to RESOLVED status for all 5 items
- `design/scripts/validate.py` — service-room check now requires 6.00x3.00 m; special-room function
  key renamed to `veterinary_isolation_room`; added a `resolved_decisions` list alongside `warnings`
- `design/scripts/export_dxf.py` — DXF layer renamed `SPECIAL_UNCONFIRMED` → `VETERINARY_ISOLATION`
- `design/scripts/render_svg.py` — function key/colors renamed; dropped the now-inapplicable
  dashed/unconfirmed styling; fixed the two rendering defects in §3; legend text updated
- `design/scripts/report_template.md` — rewrote §1, §2.3–2.8, §3–§6, §12, §16–§20 to reflect
  resolved status instead of open questions
- `design/scripts/generate_report.py` — added the `RESOLVED_DECISIONS_LIST` token; fixed
  singular/plural grammar in the generated validation summary

Added:
- `OWNER_CONFIRMATION_FINALIZATION_REPORT.md` — this file

## 8. Commit hash

This pass's commit: `02997f2caa27364431cf1a05e84c87ded6241b49` (`02997f2`)
Branch: `claude/luxury-stable-redesign-weda7b`

## 9. Conclusion

All 5 previously-open owner-confirmation items are now resolved and reflected consistently across
every generated output (model, validation report, CSVs, SVG/PNG plans, DXF, and the narrative
report). Two genuine rendering defects were caught by actually inspecting the regenerated images
(not just re-running scripts) and fixed at the generator level. The only remaining disclosed item is
the 3D model lag noted in §6, and the standard set of licensed-professional reviews already listed
in `source_audit.md` §18 (structural, MEP, fire/life-safety, civil/drainage, code/permitting — none
of which were in scope for this pass).
