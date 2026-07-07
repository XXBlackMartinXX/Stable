# Textures

No texture files are bundled with this handoff. The geometry ships with solid-colour material
**slots** (see `../stable_scene.mtl` and `../material_palette.csv`); the intended look is achieved by
assigning real PBR materials from D5 Render's own library.

Recommended D5 library materials per slot:

| Material slot | D5 library material to use |
|---|---|
| `wall_plaster_warm` | Warm sandstone / limestone plaster |
| `wall_plaster_feature` | Deep espresso / olive feature plaster |
| `stall_timber_front` | Warm walnut timber (+ bronze trim on premium stalls) |
| `roof_metal` | Bronze standing-seam metal |
| `terrace_stone` / `paving_stone` | Warm limestone paving |
| `sand_paddock` | Raked / textured sand (with bump/displacement) |
| `paving_service` | Grey utility paving |
| `ground_pad` | Neutral site ground |

If you author or import custom texture maps, place them in this folder and list them here for
provenance so the handoff stays self-describing.
