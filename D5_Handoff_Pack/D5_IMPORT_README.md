# D5 Render — Import & Setup Guide

Luxury Equestrian Stable · validated schematic layout · handoff for final visualization.

**Do not change the layout, dimensions, room positions, paddocks, stall counts, or the
40.00 × 50.00 m site.** This geometry is validated and owner-confirmed. Your job is materials,
lighting, cameras, and entourage — not design.

---

## 1. What to import

- Import **`stable_scene.obj`** into D5 Render (File → Import Model, or drag-and-drop).
- Keep **`stable_scene.mtl`** in the same folder — D5 reads it automatically and pre-splits the
  model into materials (see §3).
- **Units: metres. Scale factor: 1.0 — do NOT rescale.** 1 OBJ unit = 1 metre. On import, set units
  to metres if prompted; the model must read as 40 m wide × 50 m deep.
- **Up axis: Z-up.** If D5 defaults to Y-up on OBJ import, choose **Z-up** so the buildings stand
  vertically and the site lies flat. (After import, confirm walls are vertical and roofs are on top.)
- **Origin:** the site's south-west corner sits at world origin (0, 0, 0). The site occupies
  X = 0…40 m (east), Y = 0…50 m (north), Z = 0…~4.3 m (up).

## 2. Geometry organization

The model is 41 named objects, grouped into logical zones (OBJ `g` groups) so you can select and
organize by zone in D5:

| Zone group | Contains |
|---|---|
| `Zone_Site` | Site ground pad |
| `Zone_Stable_Barn` | 20 standard stalls, 2 premium stalls, 2 veterinary/isolation rooms, feed room, service room |
| `Zone_Worker_Wing` | Worker bedroom, kitchen, bathroom |
| `Zone_Guest_Majlis` | Men's majlis, men's WC, outdoor majlis/terrace, private bedroom, private bathroom |
| `Zone_Paddocks_Service` | Two paddocks, wash/manure service yard, perimeter service lane |
| `Zone_Arrival_Parking` | Arrival/motor court, parking apron |

Each object is named `<ID>_<function>` (e.g. `S01_horse_stall`, `MJ01_majlis`, `PD01_paddock`),
matching `room_schedule.csv` / `coordinate_schedule.csv` exactly.

> The buildings are supplied as clean massing volumes (block walls + flat roof caps) with a small
> reveal gap between neighbours. This is the correct base for a visualization: add roof pitch/parapet
> detail, doors, and fine detail in D5 — but **do not move or resize anything.**

## 3. Materials to assign

The `.mtl` splits the model into these material slots. Replace each with a real D5 library material
(see `material_palette.csv` for the intended look and colour hints):

| MTL material slot | Assign in D5 | Notes |
|---|---|---|
| `wall_plaster_warm` | Warm sandstone / limestone plaster | Stable & wing walls |
| `wall_plaster_feature` | Deep espresso / olive feature plaster | Majlis + private suite |
| `stall_timber_front` | Warm walnut timber | Stall fronts / Dutch doors; add bronze trim to premium stalls |
| `roof_metal` | Bronze standing-seam metal | All roofs |
| `terrace_stone` | Warm limestone paving | Majlis terrace slab |
| `sand_paddock` | Raked / textured sand | Paddocks — use a displacement/bump sand |
| `paving_stone` | Limestone paving | Arrival court & parking apron |
| `paving_service` | Utilitarian grey paving | Service lane / wash yard |
| `ground_pad` | Neutral site ground | Base pad under everything |

Add entourage from the D5 library: realistic **shade trees** (never stepped-cube/toy trees), low
native planting, majlis rugs/floor seating/low tables, stall bedding/hay (and horses if desired),
and 3–4 luxury vehicles on the parking apron.

## 4. Camera views to create

Create one camera per row in **`camera_schedule.csv`** (positions/targets are in site metres, same
coordinate system as the model). Required deliverable views:

1. Premium overhead cutaway (hero)
2. Aerial exterior, golden hour
3. Stable aisle interior
4. Guest / majlis zone
5. Paddock / service courtyard
6. Entry / parking apron
7. Twilight hero (optional)

Lighting: warm late-afternoon / golden-hour sun, low from the south-west, long soft shadows; one or
two views may be dusk with warm interior/bollard glow. Lens 35–50 mm equivalent (no fish-eye).
Output ≥4K per view (hero cutaway ≥5000 px long edge), sRGB. See `render_production_brief.md` and
`render_view_checklist.md` for the full spec and acceptance criteria.

## 5. What must NEVER be changed

- The 40.00 × 50.00 m site boundary.
- Any room's size, position, or count (20 standard + 2 premium stalls; 2 veterinary/isolation rooms;
  feed room; service room 6.00 × 3.00 m).
- The two paddocks (equal, 318.92 m² each) — do not resize or move them.
- Owner-confirmed items: veterinary/isolation rooms (مصاب), service room 6.00 × 3.00 m, parking apron
  kept, outdoor majlis / private bathroom widths, worker bedroom footprint.

If a material or camera choice would require moving geometry, **stop and query** — do not adjust the
layout to suit a render.

## 6. Reference images

- `reference_images/hero_masterplan_board.png` — the validated master-plan board. **This defines the
  correct layout, zoning, and labels.** Match this arrangement exactly.
- `reference_images/original_style_reference.jpeg` — the client's original mood/style reference
  (warm materials, textured sand, furniture). Match the *warmth and materiality*, **not** its
  older geometry — use the validated layout above.

## 7. Textures

No texture files are bundled (`textures/` contains only a note). Assign materials from D5's own PBR
library per `material_palette.csv`. If you author custom textures, drop them in `textures/` and note
them here for provenance.
