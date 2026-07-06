# Source of Truth Lock — Luxury Equestrian Stable Redesign

This document freezes the facts this pass is not allowed to change without a proven geometry defect.
Every number below was re-derived by actually running the pipeline (`validate.py`) at the start of
this pass, not copied from a prior report.

## 1. Geometry lock

- **Site:** 40.00 m (X, width) × 50.00 m (Y, depth) = 2,000.00 m². Origin (0,0) = southwest corner;
  Y=0 is the confirmed entrance/gate edge (per the original hand sketch).
- **Space count:** 40 spaces total in `design/scripts/model.py`.
- **Total scheduled area:** 1,648.01 m² (82.4% of site).
- **Dimension chains:** X chain sums to exactly 40.00 m; Y chain sums to exactly 50.00 m.
- **Single source of truth file:** `design/scripts/model.py`. All schedules, plans, DXF, and the 3D
  model are derived from it — never edited independently.

## 2. Room program lock (counts and mandatory sizes)

| Program item | Count | Size | Status |
|---|---|---|---|
| Standard horse stalls | 20 | 3.75×3.75 m | required_program |
| Premium horse stalls | 2 | 4.00×4.00 m | required_program |
| Veterinary/isolation rooms (مصاب) | 2 | 3.50×4.00 m | owner-confirmed label/function |
| Feed room | 1 | 4.00×4.00 m | required_program |
| Service room | 1 | 6.00×3.00 m | owner-confirmed (supersedes 3.00×3.00 brief) |
| Paddocks | 2 | 318.92 m² each, equal | required_program + redesign improvement |
| Worker bedroom | 1 | 7.00×4.00 m | owner-confirmed |
| Worker kitchen | 1 | 3.50×4.00 m | owner-confirmed (narrowed to fit SV01) |
| Worker bathroom | 1 | 2.00×4.00 m | owner-confirmed (narrowed to fit SV01) |
| Men's majlis | 1 | 8.00×8.24 m | cad_sourced |
| Men's WC | 1 | 1.76×1.76 m | cad_sourced |
| Outdoor majlis/sitting | 1 | 8.00×8.24 m | owner-confirmed |
| Private bedroom | 1 | 4.83×3.76 m | cad_sourced |
| Private bathroom | 1 | 4.83×2.00 m | owner-confirmed |
| Parking apron (optional) | 1 | 11.00×4.00 m, 4 bays | owner-confirmed: kept |

## 3. Owner decisions lock (5 of 5 resolved, none reopened this pass)

1. **مصاب — injured/veterinary isolation room.** The CAD's alternate spelling "مصلب" is superseded.
2. **Service room 6.00×3.00 m** governs over the 3.00×3.00 m written brief.
3. **Parking apron kept** exactly as modeled.
4. **Outdoor majlis / private bathroom widths confirmed** as modeled.
5. **Worker bedroom footprint confirmed** as modeled.

These are not reopened, re-litigated, or altered in this pass. Any presentation copy referencing
them must match this table exactly.

## 4. Validation lock

Re-ran `python3 design/scripts/validate.py` at the start of this pass:

- **Status: PASS**
- Passed checks: 27
- Failed checks: **0**
- Disclosed warnings: 1 (WK01/WBTH01 narrowing — a documented trade-off from decision #2, not a
  defect)
- Resolved owner decisions tracked: 5

No discrepancy was found between this live run and what `validation_report.json`/`.txt` and
`source_audit.md` already state. **No geometry defect was found. Nothing in §1 or §2 is being
changed in this pass.**

## 5. 3D model source lock

The 3D model must be built from `design/scripts/model.py` in its current state (post owner-
confirmation, post 3D-sync — commit `a15ae7b` and later), **not** from either of the two earlier 3D
builds (the original pre-owner-confirmation model, or any intermediate draft). The most recent 3D
sync (`THREE_D_SYNC_REPORT.md`) already confirmed the SketchUp model reflects SV01 at 6.00×3.00 m,
WK01/WBTH01 at their narrowed widths, and SP01/SP02 as veterinary/isolation rooms. Any new 3D/render
work in this pass builds on top of that already-correct geometry — it upgrades materials, lighting,
camera work, and composition only. It does not rebuild or re-derive coordinates.

## 6. What this lock permits changing in this pass

- Visual style, materials, lighting, camera framing, and composition of 3D outputs.
- Typography, layout, and narrative prose of presentation documents.
- File organization/packaging (copies into a new `/final_package` structure).
- Arabic label *rendering* technique (font-scoping fix), not Arabic *content* (unchanged).

## 7. What this lock forbids changing in this pass

- Any coordinate, dimension, room count, or function in `model.py`.
- Any of the 5 owner-confirmed decisions.
- `validate.py`'s check logic or thresholds.
- The disclaimer / concept-only wording, in substance (it may be reformatted, not softened).

This lock is binding for the remainder of this pass.
