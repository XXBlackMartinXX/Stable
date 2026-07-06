# Render Production Notes — Luxury Equestrian Stable Redesign

**Concept visualization package only. Not for construction or permit use.**

This document records exactly what was produced for the render/visualization upgrade in this
pass, the tools actually used, what was attempted and did not complete, and an honest fidelity
comparison against the original reference render. Per `QUALITY_GAP_ANALYSIS.md` §1, this pass
committed up front to disclosing limitations rather than overclaiming, and this note follows
through on that commitment.

## 1. What is delivered

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | Premium vector cutaway master illustration | `design/output/plans/premium_cutaway_masterplan.svg` / `.png` (2280×2900) | **New this pass — primary upgraded visual** |
| 2 | 3D aerial massing render | `design/output/plans/aerial_3d_render.png` | Carried over unchanged from the prior 3D-sync pass (commit `a15ae7b`) |
| 3 | 3D massing thumbnail | `design/output/plans/sketchup_thumbnail.png` | Carried over unchanged from the prior 3D-sync pass |
| 4 | Dimensioned technical plan | `design/output/plans/plan_dimensioned.svg` / `.png` | Unchanged, preserved as-is (already strong per `CURRENT_STATE_REVIEW.md`) |
| 5 | Styled masterplan (SVG) | `design/output/plans/masterplan_luxury.svg` / `.png` | Unchanged, preserved as-is |
| — | Render contact sheet | `design/output/plans/render_contact_sheet.png` | **New this pass** — composite of all five above |

## 2. The primary new deliverable: the premium vector cutaway

`design/scripts/render_premium.py` generates `premium_cutaway_masterplan.svg/.png` directly from
`design/scripts/model.py` — every rectangle drawn is a validated coordinate read straight from the
source-of-truth model, not redrawn, estimated, or eyeballed from the reference image. This gives it
**zero geometric hallucination risk**, which is why it was chosen over any generative-image
approach (see §4 below for why that path was rejected).

Improvements over the previous plan renders:
- Layered gradient fills, soft drop shadows (`feGaussianBlur`), and a light bevel edge per room,
  replacing flat single-color fills.
- Vector entourage: hay-bale icons in stalls, a bed icon in the private bedroom, majlis floor
  seating icons, car icons at the parking apron, and layered-canopy trees at the guest zone and
  paddock edges.
- Textured sand paddocks: randomized (seeded, reproducible) ellipse "blobs" plus rake lines, clipped
  to each paddock's exact boundary.
- Correctly rendered Arabic room labels. Every label is drawn as its own `<text>` element scoped to
  a single font-family (`Noto Sans Arabic` for Arabic runs, `Helvetica/Arial` for Latin runs). This
  fixes a real, verified `cairosvg` bug: a `<text>` element with a *mixed* Latin+Arabic font-family
  stack does not fall back per-glyph, so Arabic runs silently render as tofu boxes when sharing an
  element with Latin text. The fix (one font per text element, never mixed) was proven in isolated
  test renders before being applied here, and is why this illustration is the first deliverable in
  the whole project to show real, legible Arabic room names.
- Label-fit-to-box sizing: every label's font size is shrunk until it provably fits its room's
  width, with narrow circulation strips (fire lane, service yard, arrival court) using ID-only
  labels rather than a full name that cannot fit. No label is clipped or overflows into a
  neighboring room — this was checked visually at 2–3x zoom during production, not assumed.

## 3. What did not change this pass, and why: the SketchUp 3D renders

Items 2 and 3 above (`aerial_3d_render.png`, `sketchup_thumbnail.png`) are **not new** — they are
carried over unchanged from the prior 3D-sync pass (`THREE_D_SYNC_REPORT.md`, commit `a15ae7b`).

This pass attempted to rebuild the SketchUp model with upgraded materials (warmer timber palette,
two-tone raked-look sand patches, paved motor court, post-and-rail paddock fencing, layered-canopy
trees) and then apply premium rendering options (shadows on, clean edge display, no visible axis
lines) and capture five additional camera views (aerial exterior, stable-aisle interior, paddock/
courtyard, guest/majlis, entry/arrival/parking). The geometry rebuild for the barn, worker wing,
guest/owner wing, paddock fencing, and landscaping was completed and re-verified against `model.py`
coordinate-by-coordinate. **The styling and multi-camera capture step did not complete**: the
Trimble SketchUp MCP connector disconnected repeatedly during this session (confirmed by repeated
"tool permission stream closed" and "server disconnected" errors across multiple retry attempts,
including after the connector reported itself reconnected), and no further model state could be
read back or saved once that happened. Rather than guess at unverifiable results or claim a camera
capture that didn't happen, this pass stops short and reports the gap honestly.

**Consequence:** `aerial_3d_render.png` and `sketchup_thumbnail.png` still show the flat massing
style flagged in `CURRENT_STATE_REVIEW.md` §3.4 (solid colors, visible red/green/blue axis lines,
no shadow modeling) — visible directly in the contact sheet above. They remain geometrically correct
(re-confirmed against `model.py` in the prior pass) but are not materially upgraded this pass.

## 4. Why no generative-AI image tool was used for the primary render

Two AI image-generation connectors are available in this environment (Higgsfield, Adobe Firefly-
based tools). They were deliberately not used to "reskin" the plan into something closer to the
reference image, for a specific, stated reason: text-to-image and image-to-image generative models
cannot be constrained to an exact floor plan or exact Arabic glyphs. Using one here would risk
silently inventing, moving, or mislabeling a room — a direct violation of this project's
anti-hallucination rules, and not verifiable against `model.py` the way the vector illustration is.
This constraint was decided and documented before any rendering work started, in
`QUALITY_GAP_ANALYSIS.md` §1, and held for the whole pass.

## 5. Honest fidelity comparison against the reference render

The reference image (`source_files/Stable PROJECT/WhatsApp Image ...3.27.30 PM.jpeg`) is a
photoreal-style render with image-based materials (real timber grain, real hay texture, shaded
figures/furniture). Nothing produced in this environment reaches that pixel-level fidelity:

- No path-tracing renderer (V-Ray/Enscape/D5/Twinmotion/Lumion/Blender) is installed or
  installable here — confirmed directly.
- The SketchUp MCP connector only ever supported flat solid-color materials, not image textures,
  even before this session's connectivity problems.
- The premium vector illustration approaches the reference's *composition and warmth* (layered
  color, shadow, entourage, texture) within a vector medium, but is a stylized cutaway diagram, not
  a photorender.

This gap is stated here explicitly so no deliverable in this package is mistaken for a photoreal
render it is not.

## 6. What this means for the final package

- The premium vector cutaway is the flagship visual for the client-facing presentation and appears
  first in the render gallery.
- The existing SketchUp renders are included as secondary massing views, labeled honestly as
  "concept massing, not materially finished" rather than presented as equivalent in quality to the
  vector illustration.
- Any future pass with a stable SketchUp/3D connection should pick up exactly where this one left
  off: geometry for all rooms is already correct and current (§3), so a future materials/camera
  pass does not need to re-derive any coordinates — only apply styling and capture views.
