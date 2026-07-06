# Consultant Handoff — Luxury Equestrian Stable Redesign

**Concept design package. Not for construction or permit use.** This folder is the entry point for
a licensed architect or engineering consultant picking up this project. Read this file first.

## 1. What this package is

A geometrically validated, owner-confirmed **concept design** for a private luxury equestrian
stable on a 40.00 × 50.00 m site. It is client-ready and consultant-ready — a real, coordinated
starting point — but it is explicitly **not** a construction document set, and nothing in it should
be built from without the licensed review listed in `PRODUCTION_READINESS_GAP_CHECKLIST.md`.

## 2. Where to start

1. **`../06_reports_and_qa/source_audit.md`** — the full technical record: source conflicts, owner
   decisions, zoning rationale, circulation logic, and materials direction. Read this first; it is
   the single most complete narrative of *why* the design is the way it is.
2. **`../04_drawings_cad/stable_concept_underlay.dxf`** — the coordinated CAD reference. Marked
   concept-only; use it as a starting layer, not a base to build permit drawings directly on top of.
3. **`../05_schedules/room_schedule.csv` and `coordinate_schedule.csv`** — the exact, validated
   coordinates and dimensions for all 40 spaces.
4. **`../../PRODUCTION_READINESS_GAP_CHECKLIST.md`** (repo root, also copied into this folder) —
   the authoritative list of what is and is not done. Read this before scoping any engagement.

## 3. Single source of truth

Every deliverable in this package — schedules, drawings, renders, both PDFs — is generated from one
file: `design/scripts/model.py`. If any question arises about an exact dimension or room count,
that file (and `design/output/reports/validation_report.json`, its live validation output) is the
authoritative answer, not any narrative description in a report.

## 4. What has already been checked (so you don't have to re-derive it)

- Site boundary closes exactly at 40.00 × 50.00 m (both dimension chains verified programmatically).
- No overlapping spaces; every space fits inside the site boundary.
- All 40 required program spaces present at their confirmed sizes (20 standard + 2 premium stalls,
  2 veterinary/isolation rooms, feed room, service room at owner-confirmed 6.00×3.00 m, 2 equal
  318.92 m² paddocks, full worker accommodation, majlis + outdoor majlis, private suite, parking).
- 5 owner decisions resolved and documented (see `SOURCE_OF_TRUTH_LOCK.md` in `06_reports_and_qa/`).

None of this substitutes for your own professional verification — it simply means you are not
starting from an unvalidated sketch.

## 5. What has explicitly NOT been checked (do not assume otherwise)

See `PRODUCTION_READINESS_GAP_CHECKLIST.md` §D in full. In short: no structural, MEP, civil/
drainage, fire/life-safety, zoning/code, or site-survey work has been done. No door/window
schedules, wall sections, foundation details, or cost estimate exist. These are exactly the scopes a
licensed team should quote and deliver next.

## 6. Contact points for questions about this package

This package was produced as a software-engineering/design-automation exercise (see
`RENDER_FINALIZATION_REPORT.md` in `03_final_renders/` for full tooling disclosure). There is no
design office contact attached to this repository; route professional questions to whichever
licensed architect/engineer your organization engages per §F of the gap checklist.
