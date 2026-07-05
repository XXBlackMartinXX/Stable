"""
Generate a DXF CAD underlay from the validated model.
CONCEPT CAD UNDERLAY ONLY - NOT FOR CONSTRUCTION.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

import ezdxf

OUT_DIR = Path(__file__).parent.parent / "output" / "plans"
OUT_DIR.mkdir(parents=True, exist_ok=True)

doc = ezdxf.new("R2010", setup=True)
msp = doc.modelspace()

LAYERS = {
    "SITE_BOUNDARY": {"color": 7},
    "HORSE_STALLS": {"color": 30},
    "SPECIAL_UNCONFIRMED": {"color": 1},
    "SERVICE_FEED": {"color": 3},
    "WORKER": {"color": 5},
    "GUEST_OWNER": {"color": 6},
    "PADDOCK": {"color": 84},
    "CIRCULATION": {"color": 9},
    "TEXT": {"color": 7},
    "GRID": {"color": 253},
    "TITLEBLOCK": {"color": 1},
}
for name, props in LAYERS.items():
    doc.layers.add(name=name, color=props["color"])

FUNC_LAYER = {
    "horse_stall": "HORSE_STALLS",
    "premium_horse_stall": "HORSE_STALLS",
    "special_horse_room_UNCONFIRMED": "SPECIAL_UNCONFIRMED",
    "feed_room": "SERVICE_FEED",
    "service_room": "SERVICE_FEED",
    "worker_bedroom": "WORKER",
    "worker_kitchen": "WORKER",
    "worker_bathroom": "WORKER",
    "majlis": "GUEST_OWNER",
    "mens_wc": "GUEST_OWNER",
    "outdoor_sitting": "GUEST_OWNER",
    "private_bedroom": "GUEST_OWNER",
    "private_bathroom": "GUEST_OWNER",
    "paddock": "PADDOCK",
    "service_yard": "CIRCULATION",
    "service_lane": "CIRCULATION",
    "arrival_court": "CIRCULATION",
}

# Site boundary
msp.add_lwpolyline(
    [(0, 0), (SITE_WIDTH, 0), (SITE_WIDTH, SITE_DEPTH), (0, SITE_DEPTH), (0, 0)],
    dxfattribs={"layer": "SITE_BOUNDARY"},
)

# 5m coordinate grid (construction lines, thin)
for gx in range(0, int(SITE_WIDTH) + 1, 5):
    msp.add_line((gx, 0), (gx, SITE_DEPTH), dxfattribs={"layer": "GRID"})
for gy in range(0, int(SITE_DEPTH) + 1, 5):
    msp.add_line((0, gy), (SITE_WIDTH, gy), dxfattribs={"layer": "GRID"})

# Rooms
for s in spaces:
    layer = FUNC_LAYER.get(s["function"], "CIRCULATION")
    x0, y0, x1, y1 = s["x_min"], s["y_min"], s["x_max"], s["y_max"]
    msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
        dxfattribs={"layer": layer},
    )
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    msp.add_text(
        s["id"], dxfattribs={"layer": "TEXT", "height": 0.5, "insert": (cx, cy + 0.3)}
    ).set_placement((cx, cy + 0.3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    dim_label = f'{s["width_m"]:.2f}x{s["depth_m"]:.2f}m'
    msp.add_text(
        dim_label, dxfattribs={"layer": "TEXT", "height": 0.28}
    ).set_placement((cx, cy - 0.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

# Linear dimensions along the two axes (overall + a few key chain segments)
dimstyle = "EZDXF"
msp.add_linear_dim(
    base=(0, -3), p1=(0, 0), p2=(SITE_WIDTH, 0), dimstyle=dimstyle,
    dxfattribs={"layer": "TITLEBLOCK"}
).render()
msp.add_linear_dim(
    base=(-3, 0), p1=(0, 0), p2=(0, SITE_DEPTH), angle=90, dimstyle=dimstyle,
    dxfattribs={"layer": "TITLEBLOCK"}
).render()

# Title block text + disclaimer
msp.add_text(
    "LUXURY EQUESTRIAN STABLE - CONCEPT CAD UNDERLAY ONLY - NOT FOR CONSTRUCTION",
    dxfattribs={"layer": "TITLEBLOCK", "height": 1.0}
).set_placement((0, SITE_DEPTH + 3))

msp.add_text(
    "Concept plan only. Not for construction or permit use until reviewed and approved by a licensed local "
    "architect/engineer, MEP/civil engineer, and fire/life-safety consultant.",
    dxfattribs={"layer": "TITLEBLOCK", "height": 0.5}
).set_placement((0, SITE_DEPTH + 1.5))

out_path = OUT_DIR / "stable_concept_underlay.dxf"
doc.saveas(out_path)
print(f"Wrote DXF concept underlay to {out_path}")
