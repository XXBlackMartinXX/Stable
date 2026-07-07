# D5 Handoff QA

Quality gate for the D5 Render handoff pack. Every check below was executed against the actual
files, not assumed. **This was a packaging/export task only — no geometry was designed, moved, or
resized.**

## 1. Site is 40.00 × 50.00 m — CONFIRMED

- `model.py`: `SITE_WIDTH = 40.0`, `SITE_DEPTH = 50.0` → 40.00 × 50.00 m = 2,000 m².
- Exported OBJ bounding box: **X 0.00 → 40.00 m, Y 0.00 → 50.00 m**, Z 0.00 → 4.30 m (up).
- Origin at the site's south-west corner (0, 0, 0). Units: metres, scale 1.0.

## 2. No geometry changed — CONFIRMED

- `design/scripts/model.py` and `design/scripts/validate.py` are **unmodified** in this pass
  (`git diff` shows no changes to either).
- `python3 design/scripts/validate.py` → **OVERALL STATUS: PASS** (unchanged).
- The OBJ export is generated directly from `model.py`; the only export-side change this pass was
  adding OBJ zone `g` groups (organization metadata) — it did **not** alter any vertex coordinate.
  Bounding box and object count are identical before and after (41 objects, extents 40 × 50 m).
- Room program re-verified by direct query: 40 spaces; 20 standard stalls; 2 premium stalls; 2
  veterinary/isolation rooms; 2 paddocks; feed room; service room.

## 3. Owner decisions preserved — CONFIRMED

- Veterinary / isolation rooms (**مصاب**) — 2 present, function intact.
- Service room **SV01 = 6.00 × 3.00 m** — confirmed.
- Parking apron kept (PK01, 11.00 × 4.00 m).
- Both paddocks equal at **318.92 m² each** — confirmed.
- Outdoor majlis, private bathroom, and worker-bedroom footprints unchanged.

## 4. Files exported successfully — CONFIRMED

- OBJ: 41 named objects, 177 faces, 300 vertices; valid Wavefront OBJ referencing
  `stable_scene.mtl`.
- Zone groups present: `Zone_Site`, `Zone_Stable_Barn`, `Zone_Worker_Wing`, `Zone_Guest_Majlis`,
  `Zone_Paddocks_Service`, `Zone_Arrival_Parking`.
- MTL: 9 material slots (`wall_plaster_warm`, `wall_plaster_feature`, `stall_timber_front`,
  `roof_metal`, `terrace_stone`, `sand_paddock`, `paving_stone`, `paving_service`, `ground_pad`).
- All CSV schedules present and consistent with the model (total scheduled area 1,648.01 m²).

## 5. Exact file list (`D5_Handoff_Pack/`)

```
D5_Handoff_Pack/
├── stable_scene.obj                 (geometry, metres, Z-up, origin SW corner)
├── stable_scene.mtl                 (9 material slots)
├── room_schedule.csv                (40 spaces, full attributes)
├── coordinate_schedule.csv          (per-room coordinates)
├── area_summary.csv                 (area by function + totals)
├── camera_schedule.csv              (7 camera views, site-metre coordinates)
├── material_palette.csv             (material direction + colour hints)
├── render_view_checklist.md         (per-view acceptance criteria)
├── render_production_brief.md       (full render brief)
├── D5_IMPORT_README.md              (import + material + camera setup steps)
├── reference_images/
│   ├── hero_masterplan_board.png    (validated master-plan board — the correct layout)
│   └── original_style_reference.jpeg(client mood/style reference)
└── textures/
    └── README.md                    (no bundled textures; assign D5 library materials)
```

Delivered as **`D5_Handoff_Pack.zip`** at the repository root.

## 6. Verdict

**PASS.** The handoff pack is complete, the geometry is byte-faithful to the validated,
owner-confirmed layout, the OBJ imports at correct scale/origin/orientation, and the D5 setup steps
are documented. Nothing in the validated design was changed.
