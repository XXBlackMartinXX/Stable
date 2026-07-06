# Quality Gap Analysis — Luxury Equestrian Stable Redesign

Gap between the current repo state (see `CURRENT_STATE_REVIEW.md`) and a polished, premium,
client-ready professional package. Each item states the specific weakness, why it matters, and the
planned fix for this pass.

## 1. Render quality (highest priority — user-flagged)

**Weakness:** `aerial_3d_render.png` is an unfinished-looking SketchUp massing screenshot: flat solid
colors, cube trees, no ground texture, no shadow modeling, and visible default axis lines (red/green/
blue) in frame. Compared to the original reference render — warm timber, hay-bale texture, real
furniture and rugs in the majlis, textured sand paddocks, modeled cars — the gap is large and the
"childish" characterization is fair.

**Why it matters:** this is the single asset a client looks at first. A flat massing box undersells
a genuinely well-planned, validated, owner-confirmed layout.

**Constraint (stated honestly up front):** this environment has no path-traced rendering engine
(no V-Ray/Enscape/D5/Twinmotion/Lumion/Blender available — checked directly, none installed and none
can be installed here) and the SketchUp MCP connector only supports flat solid-color materials, not
image textures (per its own SDK documentation). True photorealism at the reference image's fidelity
is not achievable with the tools actually available in this session. Two AI image-generation
connectors (Higgsfield, Adobe Firefly-based tools) are available, but text/image generative models
are unreliable for precise architectural floor plans and for Arabic text rendering — using one to
"reskin" the plan risks violating the project's own anti-hallucination rules (a generative model
could easily misplace rooms, invent stalls, or garble Arabic glyphs, none of which would be
verifiable against `model.py`). That path is rejected for the primary technical/plan render.

**Planned fix:**
- A new premium vector "cutaway" master illustration, built by code directly from `model.py`
  (zero hallucination risk — every rectangle is the validated coordinate), styled with layered
  fills, drop shadows, and tasteful vector entourage (stall bedding, majlis seating, bed icon,
  parked-car icons) to approach the reference image's composition and warmth within a vector
  medium, plus correctly-shaped Arabic labels per room (see item 3).
- A materially and compositionally upgraded SketchUp 3D pass: richer, warmer solid-color palette,
  textured-looking ground treatment (layered color blocks instead of one flat sand tone), shadows
  enabled, cleaned-up presentation style (no axis lines, proper background), and dedicated camera
  setups for the aerial, stable-aisle, paddock, majlis-exterior, and arrival/parking views.
- Full honesty about fidelity level in `RENDER_PRODUCTION_NOTES.md` — these are upgraded concept
  visualizations, not photoreal renders, and the report will say so explicitly.

## 2. No client-facing presentation

**Weakness:** nothing in the repo is a document a client could be handed. All outputs are CSV/JSON/
markdown/CAD or a bare PNG.

**Fix:** a polished multi-section client PDF (cover, executive summary, goals, site summary, design
concept, zoning, master plan, dimensions/logic, per-zone explanations, circulation, materials
palette, render gallery, technical highlights, schedule summary, advantages over the original
scheme, next steps, appendix) — built with real typographic hierarchy, not a text dump.

## 3. Arabic label rendering

**Weakness:** no current visual deliverable actually displays rendered Arabic text (the SVG plans
avoid it after the tofu-box bug fix; the 3D model has no text at all). Arabic is correct in the data
layer but invisible in the presentation layer.

**Fix:** render Arabic correctly in the new premium vector illustration by scoping `font-family` to
individual per-label `<text>` elements (Noto Sans Arabic only for Arabic runs, Helvetica/Arial for
Latin runs) instead of one global mixed-script font stack — this avoids the exact cairosvg fallback
bug found previously (reproduced and confirmed: a global stack silently drops Arabic glyphs to tofu
boxes; a script-scoped attribute per text run renders correctly). Verified before being called done.

## 4. No consolidated technical-sheet package

**Weakness:** the dimensioned plan is a single, dense sheet. There is no cover/title sheet, no
schedule-as-sheet, no key-metrics-at-a-glance sheet, and no sheet index — the kind of front matter a
consultant expects in a drawing set.

**Fix:** four additional sheets (project information, key metrics/area summary, master plan, room
schedule) assembled into a technical appendix PDF with a sheet index, alongside the existing PNG/SVG
exports (which are kept, not replaced).

## 5. No organized delivery structure

**Weakness:** everything lives under `design/output/`, mixed with working scripts. There is no
single folder a reviewer or client could be pointed to.

**Fix:** a `/final_package` folder (client presentation, technical appendix, renders, drawings,
schedules, reports, source-file reference) with a `FINAL_DELIVERABLE_INDEX.md`, built from copies of
the existing validated files — the working `design/` tree remains the actual source of truth and is
not restructured or duplicated destructively.

## 6. Report prose tone

**Weakness:** `source_audit.md` is accurate but reads as an engineering QA log — repetitive
"confirmed as modeled" phrasing, no narrative framing of *why* the redesign is better, no design
story.

**Fix:** the client PDF gets freshly written, polished, executive-tone narrative copy (design
rationale, zone explanations, advantages over the original scheme) that stays strictly within what
`source_audit.md` and `model.py` already establish as fact — no new claims, only better prose for
existing, source-grounded facts. `source_audit.md` itself is left intact as the technical record
(it is referenced, not rewritten, to avoid breaking its generator/template sync with `validate.py`).

## 7. What is explicitly NOT a gap (do not touch)

- Site boundary, room counts, room dimensions, owner-confirmed decisions — these are correct and
  frozen. No canary in this pass permits changing them without a proven geometry defect, and none
  was found.
- The disclaimer language ("Concept plan only...") and the DXF's "concept underlay only" marking —
  these are accurate and must appear unchanged (and in fact more prominently) in every new
  deliverable.
- `validate.py`'s check logic — no changes needed; it already passes cleanly.

## 8. Explicit truthfulness boundary for this pass

This pass will **not** claim: construction approval, permit-ready status, licensed engineering
sign-off, or code compliance verification. Every new document will carry the same disclaimer already
established in `source_audit.md`, and the client PDF will have an explicit, prominent section titled
"What Still Requires Licensed Professional Review" restating `source_audit.md` §18 without
softening it.
