"""
Clean 3D geometry export (Wavefront OBJ + MTL) generated directly from the validated coordinate
model (design/scripts/model.py).

Purpose: hand a real, correctly-dimensioned 3D scene to an external visualization studio so they
can produce photoreal renders in Blender / Twinmotion / Lumion / Enscape / V-Ray / D5. This
environment has NO path-traced renderer, so photoreal output is produced downstream, not here.

Every vertex is computed from a room's actual x_min/y_min/x_max/y_max plus a per-function height.
Nothing is hand-modelled or invented. Units are METRES. Coordinate system: X = east (site width),
Y = north (site depth), Z = up. Origin (0,0,0) = site south-west corner.

Objects are grouped and assigned named materials by function so a studio can drop in real materials
(warm plaster, timber stable fronts, textured sand, stone paving) per group without guessing which
box is which.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

OUT_DIR = Path(__file__).parent.parent / "output" / "geometry_export"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Per-function extrusion height (m) and a named material. Heights are indicative massing for a
# visualization base; a studio refines roof pitch/parapet detail during production.
FUNC = {
    "horse_stall":              (3.0, "stall_timber_front"),
    "premium_horse_stall":      (3.2, "stall_timber_front"),
    "veterinary_isolation_room":(3.1, "wall_plaster_warm"),
    "feed_room":                (3.1, "wall_plaster_warm"),
    "service_room":             (3.1, "wall_plaster_warm"),
    "worker_bedroom":           (3.2, "wall_plaster_warm"),
    "worker_kitchen":           (3.2, "wall_plaster_warm"),
    "worker_bathroom":          (3.2, "wall_plaster_warm"),
    "majlis":                   (4.3, "wall_plaster_feature"),
    "mens_wc":                  (3.0, "wall_plaster_warm"),
    "private_bedroom":          (3.4, "wall_plaster_feature"),
    "private_bathroom":         (3.0, "wall_plaster_warm"),
    "outdoor_sitting":          (0.15, "terrace_stone"),   # terrace slab, near-flat
    "paddock":                  (0.0, "sand_paddock"),      # ground only
    "service_yard":             (0.0, "paving_service"),
    "service_lane":             (0.0, "paving_service"),
    "arrival_court":            (0.0, "paving_stone"),
    "parking":                  (0.0, "paving_stone"),
}

# Material -> (diffuse RGB 0..1) starting values; a studio replaces these with textured PBR.
MTL = {
    "ground_pad":          (0.84, 0.80, 0.71),
    "stall_timber_front":  (0.55, 0.38, 0.24),
    "wall_plaster_warm":   (0.86, 0.80, 0.69),
    "wall_plaster_feature":(0.42, 0.28, 0.20),
    "terrace_stone":       (0.88, 0.84, 0.76),
    "sand_paddock":        (0.84, 0.78, 0.63),
    "paving_service":      (0.62, 0.60, 0.56),
    "paving_stone":        (0.80, 0.76, 0.68),
    "roof_metal":          (0.30, 0.24, 0.18),
}


class ObjWriter:
    def __init__(self):
        self.v = []
        self.lines = []

    def _vert(self, x, y, z):
        self.v.append((x, y, z))
        return len(self.v)  # 1-indexed

    def box(self, x0, y0, x1, y1, z0, z1, name, wall_mtl, roof_mtl="roof_metal", roof=True, zone=None):
        if zone:
            self.lines.append(f"g {zone}")
        self.lines.append(f"o {name}")
        idx = {}
        for key, (px, py, pz) in {
            "000": (x0, y0, z0), "100": (x1, y0, z0), "110": (x1, y1, z0), "010": (x0, y1, z0),
            "001": (x0, y0, z1), "101": (x1, y0, z1), "111": (x1, y1, z1), "011": (x0, y1, z1),
        }.items():
            idx[key] = self._vert(px, py, pz)
        self.lines.append(f"usemtl {wall_mtl}")
        for a, b, c, d in [("000", "100", "101", "001"), ("100", "110", "111", "101"),
                            ("110", "010", "011", "111"), ("010", "000", "001", "011")]:
            self.lines.append(f"f {idx[a]} {idx[b]} {idx[c]} {idx[d]}")
        if roof:
            self.lines.append(f"usemtl {roof_mtl}")
            self.lines.append(f"f {idx['001']} {idx['101']} {idx['111']} {idx['011']}")

    def slab(self, x0, y0, x1, y1, z, name, mtl, zone=None):
        if zone:
            self.lines.append(f"g {zone}")
        self.lines.append(f"o {name}")
        a = self._vert(x0, y0, z); b = self._vert(x1, y0, z)
        c = self._vert(x1, y1, z); d = self._vert(x0, y1, z)
        self.lines.append(f"usemtl {mtl}")
        self.lines.append(f"f {a} {b} {c} {d}")

    def dump(self, path, mtllib):
        out = [f"# Luxury Equestrian Stable — validated geometry export (metres)",
               f"# Generated from design/scripts/model.py. Do not hand-edit; regenerate.",
               f"mtllib {mtllib}", ""]
        out += [f"v {x:.4f} {y:.4f} {z:.4f}" for (x, y, z) in self.v]
        out.append("")
        out += self.lines
        Path(path).write_text("\n".join(out) + "\n")


def write_mtl(path):
    lines = ["# Material starting values — replace with textured PBR in your renderer.", ""]
    for name, (r, g, b) in MTL.items():
        lines += [f"newmtl {name}", f"Kd {r:.3f} {g:.3f} {b:.3f}", "Ks 0.05 0.05 0.05", "Ns 20.0", ""]
    Path(path).write_text("\n".join(lines) + "\n")


# Logical zone grouping (OBJ `g` groups) so a renderer can select/organize by zone.
ZONE = {
    "horse_stall": "Zone_Stable_Barn", "premium_horse_stall": "Zone_Stable_Barn",
    "veterinary_isolation_room": "Zone_Stable_Barn", "feed_room": "Zone_Stable_Barn",
    "service_room": "Zone_Stable_Barn",
    "worker_bedroom": "Zone_Worker_Wing", "worker_kitchen": "Zone_Worker_Wing",
    "worker_bathroom": "Zone_Worker_Wing",
    "majlis": "Zone_Guest_Majlis", "mens_wc": "Zone_Guest_Majlis",
    "outdoor_sitting": "Zone_Guest_Majlis", "private_bedroom": "Zone_Guest_Majlis",
    "private_bathroom": "Zone_Guest_Majlis",
    "paddock": "Zone_Paddocks_Service", "service_yard": "Zone_Paddocks_Service",
    "service_lane": "Zone_Paddocks_Service",
    "arrival_court": "Zone_Arrival_Parking", "parking": "Zone_Arrival_Parking",
}


def main():
    w = ObjWriter()
    # Site ground pad
    w.slab(0, 0, SITE_WIDTH, SITE_DEPTH, -0.02, "site_ground_pad", "ground_pad", zone="Zone_Site")

    for s in spaces:
        h, mtl = FUNC.get(s["function"], (3.0, "wall_plaster_warm"))
        x0, y0, x1, y1 = s["x_min"], s["y_min"], s["x_max"], s["y_max"]
        name = f'{s["id"]}_{s["function"]}'
        zone = ZONE.get(s["function"], "Zone_Other")
        if h <= 0.001:
            w.slab(x0, y0, x1, y1, 0.0, name, mtl, zone=zone)
        else:
            g = 0.06  # reveal gap between adjacent volumes
            w.box(x0 + g, y0 + g, x1 - g, y1 - g, 0.0, h, name, mtl, zone=zone)

    obj_path = OUT_DIR / "stable_scene.obj"
    mtl_path = OUT_DIR / "stable_scene.mtl"
    w.dump(obj_path, "stable_scene.mtl")
    write_mtl(mtl_path)
    print(f"Wrote {obj_path} ({len(w.v)} vertices) and {mtl_path}")


if __name__ == "__main__":
    main()
