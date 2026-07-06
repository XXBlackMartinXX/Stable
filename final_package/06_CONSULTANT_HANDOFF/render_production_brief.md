# Render Production Brief — Luxury Equestrian Stable

**For:** an external architectural-visualization studio or 3D artist.
**Goal:** produce a set of premium, photoreal renders of this stable design, faithful to the
validated layout supplied here.

> **Why this brief exists:** photoreal rendering requires professional software (Blender/Cycles,
> Twinmotion, Lumion, Enscape, V-Ray, or D5). That software is not available in the environment
> where this package was produced, so the photoreal renders are commissioned externally using the
> geometry and specification below. Do **not** re-invent the layout — it is fixed and validated.

## 1. Project overview

A private luxury equestrian stable. Warm, calm, materials-first luxury — proportion, shade, and
natural materials rather than ornament. The mood target is a serene desert-estate stable at golden
hour: warm stone/plaster, timber stable fronts, raked sand paddocks, mature shade trees.

## 2. Site

- 40.00 m (east–west) × 50.00 m (north–south) = 2,000 m².
- 40 scheduled spaces; scheduled built/allocated area 1,648.01 m² (82.4%).
- Origin (0,0) = south-west corner. Y = 0 is the entrance/gate edge (gate to the north/far side).

## 3. Validated layout source files (authoritative — build from these)

| File | Use |
|---|---|
| `design/output/geometry_export/stable_scene.obj` + `.mtl` | Import-ready 3D massing, correctly dimensioned, grouped by function with named materials. **Primary geometry source.** |
| `03_TECHNICAL_DRAWINGS/dimensioned_master_plan.png` | Exact dimensions and room positions. |
| `02_HERO_VISUALS/01_premium_masterplan_cutaway.png` | Colour/zoning/entourage intent and Arabic labels. |
| `04_SCHEDULES/room_schedule.csv` | Every room's exact size and function. |

The OBJ is indicative massing (flat roofs, block volumes). Refine roofs, doors, and detail during
production — but **do not move, resize, add, or remove rooms.** Dimensions are fixed.

## 4. Required render views

See `camera_schedule.csv` for exact camera positions/targets (in site metres). Deliver these six:

1. **Premium overhead cutaway** — top-down 3/4 hero, whole site, roofs cut away to read the plan.
2. **Aerial exterior hero** — elevated 3/4 from the south-west, golden hour.
3. **Stable aisle interior** — down the central aisle, both stall rows, shade canopy overhead.
4. **Guest / majlis zone** — the indoor + outdoor majlis and arrival sequence.
5. **Paddock / courtyard** — the two paddocks and the wash/service spine between them.
6. **Entry / parking** — arrival court, gate, and the 4-bay parking apron.

## 5. Camera descriptions

Eye height ~1.6 m for eye-level views; 25–40 m for aerials. 35–50 mm equivalent lens (avoid extreme
wide-angle distortion). Three-quarter angles preferred over flat elevations. Full positions in
`camera_schedule.csv`.

## 6. Material palette

See `material_palette.csv`. Summary:

- **Stable / wing walls:** warm sandstone/limestone render; bronze accent trim on premium stalls.
- **Stable doors:** solid warm walnut timber Dutch doors; powder-coated steel yoke bars.
- **Majlis / private suite:** deep espresso plaster (majlis), olive-toned plaster (private suite).
- **Roofs:** bronze standing-seam metal, consistent across all structures.
- **Paddock fencing:** dark walnut-toned timber post-and-rail, two rail bands.
- **Paddock ground:** raked/textured sand.
- **Terrace / majlis flooring:** warm limestone paving.
- **Motor court:** limestone paving (guest); service lane: utilitarian grey paving.

## 7. Lighting style

Warm late-afternoon / golden-hour sun, low angle from the south-west, long soft shadows. Sky:
clear-to-hazy warm gradient. One or two hero views may be dusk with warm interior/bollard glow.
Physically based; soft ambient occlusion in corners; no blown highlights.

## 8. Reference-image style notes

The client's reference is a warm, softly-lit overhead cutaway with visible timber, hay texture,
rugs/furniture in the majlis, textured sand paddocks, and parked cars. Match that *warmth and
materiality*, but use **this** validated layout, not the reference's older geometry.

## 9. Arabic label handling

Do **not** burn Arabic room labels into 3D perspective renders (font-shaping errors are a common
failure). Keep perspective renders label-free. If a labelled plan is needed, overlay labels
afterward in 2D from the supplied master plan — or simply reuse the supplied vector master-plan
board, which already carries correct Arabic.

## 10. Furniture / entourage

- Majlis: floor seating, rugs, low tables.
- Private/worker rooms: beds, simple furniture (kept subtle).
- Stalls: bedding, hay, the odd horse if desired.
- Parking apron: 3–4 luxury vehicles.
- Landscape: mature shade trees at the guest zone and paddock edges (realistic canopies — **never
  stepped-cube "toy" trees**), low native planting.

## 11. Forbidden mistakes (automatic rejection)

- Flat/untextured massing boxes; cube or stepped-block trees.
- Visible modelling axes, gizmos, or default grey clay with no materials.
- Any change to room count, size, or position vs. the validated layout.
- Broken/garbled Arabic burned into a render.
- Distorted furniture, extreme fish-eye lens, or a layout that contradicts the master plan.

## 12. Output requirements

- Resolution: minimum 3840 × 2160 (4K) per view; hero cutaway 5000 px on the long edge.
- Format: 16-bit PNG or TIFF masters; plus web-sized JPGs.
- Colour: sRGB.
- Naming: see `render_view_checklist.md` (e.g. `01_premium_masterplan_cutaway_4k.png`).

## 13. Quality checklist

Every delivered render must pass `render_view_checklist.md` before acceptance. If a view fails,
it is not delivered as final.
