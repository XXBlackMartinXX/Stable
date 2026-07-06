# Render Finalization Report — Luxury Equestrian Stable Redesign

**Concept visualization package. Not for construction or permit use.**

This report records what was actually done to replace the weak 3D massing renders identified as
the single biggest remaining quality gap in `FINAL_REPO_PRODUCTION_REVIEW.md` and (before that)
`CURRENT_STATE_REVIEW.md` / `QUALITY_GAP_ANALYSIS.md`. It states the tools used, the exact source
geometry, what was inspected, and an honest fidelity verdict — no overclaiming.

## 1. What was tried, in the order the brief required

1. **Trimble SketchUp MCP connector, live styling/camera session.** Attempted at the start of this
   phase: a fresh `build_model` connectivity test failed immediately with a tool-permission/
   connection error, identical to the failure pattern documented in the prior pass's
   `RENDER_PRODUCTION_NOTES.md`. The MCP layer for this session is confirmed unstable (this is the
   second pass in a row where it failed on first contact) — no further retries were made, per the
   lesson already recorded from the prior pass that retrying an unstable connector does not fix a
   systemic problem.
2. **Blender or another local 3D application.** Checked directly: `blender` is not on `PATH`, `bpy`
   is not importable, and no path-traced renderer (V-Ray/Enscape/Twinmotion/Lumion/POV-Ray) is
   installed or installable in this environment. Confirmed absent, not assumed.
3. **Export a clean 3D scene from `model.py` and render it with the best available renderer.**
   This is the path taken. Since no 3D rendering application is available, "the best available
   renderer" in this environment is a purpose-built one: `design/scripts/render_3d.py`, a
   from-scratch Python/NumPy perspective rasterizer written this pass specifically for this
   purpose (see §2).
4. **Generative AI as post-production only.** Not used. With a working deterministic renderer
   produced in step 3, there was no need to fall back to a generative image model, which would have
   reintroduced the exact hallucination risk this project has rejected in every prior pass.

## 2. What `render_3d.py` actually does

- Reads `spaces`, `SITE_WIDTH`, `SITE_DEPTH` directly from `design/scripts/model.py` — the same
  single source of truth as every other deliverable. Every wall, roof, and ground plane vertex is
  computed from a room's actual `x_min/y_min/x_max/y_max` and a fixed per-function height; nothing
  is hand-placed or estimated.
- Builds a real 3D scene: extruded room volumes with flat roof caps, a componentized layered-canopy
  tree (reused/adapted from the same design language as the premium vector cutaway), simple two-box
  cars at the parking apron, post-and-rail paddock fencing, Dutch-door panels on the aisle-facing
  stall walls, and a continuous shade canopy over the central aisle.
- Renders with its own perspective camera (look-at + perspective projection matrices), flat
  Lambertian shading (ambient + diffuse term from a fixed directional light), back-face culling, a
  painter's-algorithm depth sort, soft blurred contact shadows, a gradient sky, and 2× supersampled
  anti-aliasing.
- **No room text labels are drawn in these perspective views.** The premium vector cutaway remains
  the single authoritative, labeled plan — this was a deliberate choice to keep zero Arabic-in-raster
  risk in the 3D renders, rather than attempt on-image label placement in a perspective view.

## 3. Real defects found and fixed while building this renderer

Building a renderer from scratch surfaced concrete bugs, each found by actually rendering and
looking at the output — not assumed correct from the code:

- **Ground-plane painter's-algorithm failure:** an early version used one giant quad for the site's
  base ground pad. A single polygon that spans from very near the camera to the horizon cannot be
  represented by one scalar "depth" for sorting purposes, so large chunks of it were drawn in front
  of buildings that should have occluded it — this produced a scene that was almost entirely a flat
  tan color with buildings barely visible. **Fixed** by tiling every ground surface (site pad, and
  each room's colored ground footprint) into a grid of small quads (`tiled_ground()`), each with a
  narrow enough depth range for the sort to behave correctly.
- **Camera framing failures in three of the six required views:** the first attempts at the
  "stable aisle interior," "paddock/courtyard," and "guest/majlis" cameras placed the eye too close
  to walls or tree canopies, producing unreadable, dominant close-up masses instead of a legible
  scene. **Fixed** by repositioning every camera to an elevated three-quarter angle (the same style
  that worked cleanly for the aerial view), verified by rendering and visually inspecting each one
  before accepting it.
- **Blank stall fronts:** the two stall rows initially had no visual break on their aisle-facing
  walls, so the "stable aisle" view read as two flat colored walls with no sense of individual
  stalls. **Fixed** by adding a `door_panel()` — a thin inset Dutch-door-colored panel on each
  aisle-facing stall wall, positioned from the real room geometry (centered on each stall's
  `x_min`/`x_max`).
- **A twilight view that wasn't actually twilight:** the optional "hero" shot initially used the
  same daylight sky gradient as every other view while being labeled "Twilight Hero View" — a minor
  but real truth-in-labeling issue. **Fixed** by giving that one view its own warm sunset sky
  gradient, lower ambient light, and a warm color tint, and confirmed visually.

## 4. Required renders — delivered

All six saved to `design/output/plans/renders_3d/`:

| # | File | View |
|---|---|---|
| 1 | `aerial_exterior.png` | Aerial exterior — whole-site 3/4 view |
| 2 | `stable_aisle.png` | Stable aisle interior (elevated, both stall rows + canopy visible) |
| 3 | `paddock_courtyard.png` | Paddock / service-yard courtyard |
| 4 | `guest_majlis.png` | Guest / majlis zone |
| 5 | `entry_parking.png` | Entry / arrival / parking apron |
| 6 | `twilight_hero.png` | Optional twilight/hero beauty shot |

The premium top-down cutaway (`premium_cutaway_masterplan.png`, item 1 of the render brief) was
already delivered in the prior pass and is unchanged; it remains the primary labeled plan.

`design/scripts/build_contact_sheet.py` was updated to feature this new set as the gallery
centerpiece (see the regenerated `render_contact_sheet.png`), with the old duplicate SketchUp
image now shown exactly once, explicitly labeled "superseded."

## 5. Old renders: superseded, not silently deleted

`aerial_3d_render.png` and `sketchup_thumbnail.png` (byte-identical duplicates, per
`FINAL_REPO_PRODUCTION_REVIEW.md` §3.1) are kept in the repository for provenance — they are the
record of the prior pass's geometry-sync check — but are no longer presented in the render gallery
as current views. The contact sheet and both client-facing PDFs now feature the new deterministic
3D set as the "3D render" deliverable, with the legacy image shown once, clearly labeled superseded.

## 6. Honest fidelity verdict

**Photorealistic quality was not achieved, and is not claimed.** This is a flat-shaded,
supersampled-but-still-simple rasterizer with painter's-algorithm hidden-surface removal, not a
path tracer — there is no global illumination, no real material texture, no reflections, and shadow
softness is a blurred approximation, not physically simulated. It is, however, a genuine, correctly
projected 3D scene built from real geometry and real perspective cameras, with shading, soft
shadows, a gradient sky, and legible massing — a categorical improvement over the previous
deliverable's flat solid-color boxes with visible SketchUp axis lines and cube-shaped trees (see the
side-by-side in the contact sheet, items 2-7 vs. item 10).

**If true photoreal rendering is required**, the exact external tool needed is a path-traced
renderer with material/texture support — V-Ray, Enscape, Twinmotion, Lumion, or Blender/Cycles —
fed by a proper 3D export (OBJ/FBX/glTF) of the same `model.py` geometry. That export step is not
part of this pass's scope but would be straightforward to add: `render_3d.py`'s `build_scene()`
function already produces a complete, correctly-dimensioned face list that could be serialized to
any standard 3D interchange format.

## 7. Conclusion

The 3D render gap flagged in three consecutive prior reports is resolved within the honest limits of
this environment: six new, correctly-projected, shaded 3D views plus a re-styled twilight hero shot
now exist, built deterministically from the validated model with zero hallucination risk, replacing
reliance on an MCP connector that has failed on first contact in two consecutive passes. The
previous flat massing images are preserved for provenance but no longer presented as the current 3D
deliverable.
