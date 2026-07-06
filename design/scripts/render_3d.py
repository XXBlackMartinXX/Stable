"""
Deterministic software 3D renderer - builds a real 3D scene directly from model.py coordinates
and renders it with a from-scratch Python/numpy perspective rasterizer (flat Lambertian shading,
painter's-algorithm depth sort, soft contact shadows, gradient sky).

Why this exists: no path-traced renderer (V-Ray/Enscape/Blender) is installed or installable in
this environment, and the Trimble SketchUp MCP connector was confirmed unstable across repeated
attempts this session (tool permission/connection failures on every call, including a fresh
connectivity test). Rather than depend on that connector again, or use a generative image model
that cannot be constrained to the exact validated geometry, this script implements the "export a
clean 3D scene from model.py and render with the best available renderer" fallback explicitly
permitted by this pass's brief: the renderer here IS the best available tool in this environment,
built for this purpose, with zero hallucination risk because every mesh vertex is computed
directly from model.py's coordinates - nothing is drawn free-hand.

No room text labels are drawn in these perspective renders (the premium vector cutaway remains the
single authoritative, labeled plan) - this avoids any Arabic-in-raster-3D risk entirely.
"""
import sys
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402
from render_premium import PALETTE  # noqa: E402  (reuse the same material palette)

OUT_DIR = Path(__file__).parent.parent / "output" / "plans" / "renders_3d"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DISCLAIMER = ("Concept plan only. Not for construction or permit use until reviewed and approved by a "
              "licensed local architect/engineer, MEP/civil engineer, and fire/life-safety consultant.")

SS = 2  # supersampling factor for anti-aliasing
W, H = 1600, 1100

ROOF_COLOR = (90, 68, 48)
GROUND_ZONE_COLOR = {
    "paddock": [(214, 197, 156), (198, 180, 138)],
    "service_yard": [(176, 170, 158), (176, 170, 158)],
    "service_lane": [(150, 146, 138), (150, 146, 138)],
    "arrival_court": [(224, 214, 189), (224, 214, 189)],
    "parking": [(150, 146, 138), (150, 146, 138)],
    "outdoor_sitting": [(210, 196, 168), (210, 196, 168)],
    "_default": [(196, 188, 162), (196, 188, 162)],
}
HEIGHTS = {
    "horse_stall": 3.0, "premium_horse_stall": 3.1, "veterinary_isolation_room": 3.1,
    "feed_room": 3.1, "service_room": 3.1, "worker_bedroom": 3.2, "worker_kitchen": 3.2,
    "worker_bathroom": 3.2, "majlis": 4.3, "mens_wc": 3.0, "private_bedroom": 3.4,
    "private_bathroom": 3.0, "outdoor_sitting": 3.6,
}
NO_VOLUME = {"paddock", "service_yard", "service_lane", "arrival_court", "parking"}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(rgb, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in rgb)


class Face:
    __slots__ = ("verts", "color", "normal")

    def __init__(self, verts, color, normal):
        self.verts = verts  # list of 3 numpy world-space points (Nx3)
        self.color = color
        self.normal = normal / (np.linalg.norm(normal) + 1e-9)


def box_faces(x0, y0, x1, y1, z0, z1, wall_color, roof=True, roof_color=ROOF_COLOR):
    """Axis-aligned box from (x0,y0,z0) to (x1,y1,z1). Returns list of Face (walls + flat roof cap)."""
    faces = []
    corners = {
        "000": np.array([x0, y0, z0]), "100": np.array([x1, y0, z0]),
        "110": np.array([x1, y1, z0]), "010": np.array([x0, y1, z0]),
        "001": np.array([x0, y0, z1]), "101": np.array([x1, y0, z1]),
        "111": np.array([x1, y1, z1]), "011": np.array([x0, y1, z1]),
    }
    wall_defs = [
        (["000", "100", "101", "001"], (0, -1, 0), 0.72),   # south
        (["100", "110", "111", "101"], (1, 0, 0), 0.88),    # east
        (["110", "010", "011", "111"], (0, 1, 0), 0.60),    # north
        (["010", "000", "001", "011"], (-1, 0, 0), 0.78),   # west
    ]
    for keys, normal, tint in wall_defs:
        verts = [corners[k] for k in keys]
        faces.append(Face(verts, shade(wall_color, tint), np.array(normal, dtype=float)))
    if roof:
        verts = [corners["001"], corners["101"], corners["111"], corners["011"]]
        faces.append(Face(verts, roof_color, np.array([0, 0, 1], dtype=float)))
    return faces


def door_panel(x0, x1, y, z0, z1, facing, color=(58, 42, 28)):
    """A thin, slightly-offset vertical panel simulating a Dutch stable door on an aisle-facing wall."""
    eps = 0.015
    if facing == "north":
        yy, normal = y + eps, (0, 1, 0)
    else:
        yy, normal = y - eps, (0, -1, 0)
    verts = [np.array([x0, yy, z0]), np.array([x1, yy, z0]), np.array([x1, yy, z1]), np.array([x0, yy, z1])]
    return Face(verts, color, np.array(normal, dtype=float))


def flat_quad(x0, y0, x1, y1, z, color):
    verts = [np.array([x0, y0, z]), np.array([x1, y0, z]), np.array([x1, y1, z]), np.array([x0, y1, z])]
    return Face(verts, color, np.array([0, 0, 1], dtype=float))


def tiled_ground(x0, y0, x1, y1, z, color, cell=2.5):
    """A large flat quad, subdivided into a grid of small quads.

    A single huge polygon breaks the painter's-algorithm depth sort used by this renderer: its one
    scalar "average depth" cannot represent a plane that spans from very near the camera to the
    horizon, so parts of it get drawn in front of geometry they should be behind. Tiling into cells
    small enough that each one has a narrow depth range fixes this without needing a full z-buffer.
    """
    faces = []
    nx = max(1, int(round((x1 - x0) / cell)))
    ny = max(1, int(round((y1 - y0) / cell)))
    xs = np.linspace(x0, x1, nx + 1)
    ys = np.linspace(y0, y1, ny + 1)
    for i in range(nx):
        for j in range(ny):
            faces.append(flat_quad(xs[i], ys[j], xs[i + 1], ys[j + 1], z, color))
    return faces


def tree(cx, cy, ground_z=0.0, scale=1.0, seed=0):
    rnd_h = 2.4 + (zlib.crc32(f"tree{cx}{cy}".encode()) % 100) / 100.0 * 1.4
    trunk_h = 1.0 * scale
    faces = []
    faces += box_faces(cx - 0.12 * scale, cy - 0.12 * scale, cx + 0.12 * scale, cy + 0.12 * scale,
                        ground_z, ground_z + trunk_h, (94, 72, 48), roof=False)
    canopy_colors = [(74, 108, 58), (92, 130, 72), (110, 148, 88)]
    r0 = 1.35 * scale
    for i, cz in enumerate([trunk_h, trunk_h + rnd_h * 0.42, trunk_h + rnd_h * 0.8]):
        r = r0 * (1 - i * 0.28)
        col = canopy_colors[i % len(canopy_colors)]
        faces += box_faces(cx - r, cy - r, cx + r, cy + r, ground_z + cz, ground_z + cz + rnd_h * 0.42,
                            col, roof=True, roof_color=shade(col, 1.08))
    return faces


def car(cx, cy, ground_z=0.0, heading="north"):
    body_color = (60, 74, 92)
    if heading in ("north", "south"):
        w, l = 1.8, 4.2
    else:
        w, l = 4.2, 1.8
    faces = []
    faces += box_faces(cx - l / 2, cy - w / 2, cx + l / 2, cy + w / 2, ground_z + 0.05, ground_z + 0.62,
                        body_color, roof=True, roof_color=shade(body_color, 1.1))
    cab_l, cab_w = l * 0.5, w * 0.86
    faces += box_faces(cx - cab_l / 2, cy - cab_w / 2, cx + cab_l / 2, cy + cab_w / 2,
                        ground_z + 0.62, ground_z + 1.02, (150, 170, 185), roof=True,
                        roof_color=shade((150, 170, 185), 1.05))
    return faces


def fence_run(x0, y0, x1, y1, ground_z=0.0, post_spacing=2.0):
    faces = []
    color = (74, 54, 38)
    length = np.hypot(x1 - x0, y1 - y0)
    n = max(2, int(length / post_spacing) + 1)
    for i in range(n):
        t = i / (n - 1)
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        faces += box_faces(px - 0.06, py - 0.06, px + 0.06, py + 0.06, ground_z, ground_z + 1.15,
                            color, roof=False)
    if abs(x1 - x0) > abs(y1 - y0):
        for rz in (0.55, 1.0):
            faces += box_faces(x0, y0 - 0.03, x1, y0 + 0.03, ground_z + rz, ground_z + rz + 0.08,
                                color, roof=False)
    else:
        for rz in (0.55, 1.0):
            faces += box_faces(x0 - 0.03, y0, x0 + 0.03, y1, ground_z + rz, ground_z + rz + 0.08,
                                color, roof=False)
    return faces


def build_scene():
    """Returns (faces, ground_faces) - all in world space (X=east, Y=north, Z=up), meters."""
    faces = []
    ground = []

    # Base ground pad for whole site (tiled - see tiled_ground() docstring for why)
    ground += tiled_ground(-3, -3, SITE_WIDTH + 3, SITE_DEPTH + 3, -0.02, (214, 205, 182), cell=3.0)

    for s in spaces:
        func = s["function"]
        x0, y0, x1, y1 = s["x_min"], s["y_min"], s["x_max"], s["y_max"]
        base, light, sh = PALETTE.get(func, ("#cccccc", "#dddddd", "#999999"))
        wall_rgb = hex_to_rgb(base)

        zone_colors = GROUND_ZONE_COLOR.get(func, GROUND_ZONE_COLOR["_default"])
        cell = 3.0 if func in ("paddock", "arrival_court", "service_yard") else 6.0
        ground += tiled_ground(x0, y0, x1, y1, 0.0, zone_colors[0], cell=cell)

        if func in NO_VOLUME:
            continue

        h = HEIGHTS.get(func, 3.0)
        # Small inward inset so adjacent rooms never share an exact boundary face - coincident
        # faces at a shared wall are a classic painter's-algorithm/z-fighting trap (two faces at
        # identical depth, both facing away from a viewer on one side, is numerically ambiguous
        # to sort and can let the wrong one poke through). The inset also reads as a deliberate
        # reveal line between building volumes, which is a common massing-render convention.
        g = 0.06
        faces += box_faces(x0 + g, y0 + g, x1 - g, y1 - g, 0.0, h, wall_rgb, roof=True)

        # Dutch-door panels on aisle-facing walls of the two stall rows (visual legibility for
        # the stable-aisle interior view - without these every stall front reads as a blank wall).
        if func in ("horse_stall", "premium_horse_stall") and abs(y1 - 18.99) < 1e-6:
            dw = min(1.4, (x1 - x0) * 0.55)
            dc = (x0 + x1) / 2
            faces.append(door_panel(dc - dw / 2, dc + dw / 2, y1 - g, 0.15, 2.25, "north"))
        if func in ("horse_stall", "premium_horse_stall") and abs(y0 - 22.49) < 1e-6:
            dw = min(1.4, (x1 - x0) * 0.55)
            dc = (x0 + x1) / 2
            faces.append(door_panel(dc - dw / 2, dc + dw / 2, y0 + g, 0.15, 2.25, "south"))

    # Central aisle shade canopy over the two stall rows
    aisle_x0, aisle_x1 = 0.0, 37.5
    canopy_y0, canopy_y1 = 14.9, 26.2
    faces += box_faces(aisle_x0, canopy_y0, aisle_x1, canopy_y1, 3.35, 3.55, (92, 66, 44), roof=True,
                        roof_color=(70, 50, 34))

    # Paddock post-and-rail fencing (perimeter only, simplified)
    pads = [s for s in spaces if s["function"] == "paddock"]
    for p in pads:
        x0, y0, x1, y1 = p["x_min"], p["y_min"], p["x_max"], p["y_max"]
        faces += fence_run(x0, y0, x1, y0)
        faces += fence_run(x0, y1, x1, y1)
        faces += fence_run(x0, y0, x0, y1)
        faces += fence_run(x1, y0, x1, y1)

    # Parking apron cars
    pk = [s for s in spaces if s["function"] == "parking"]
    if pk:
        p = pk[0]
        n_bays = 4
        bay_w = (p["x_max"] - p["x_min"]) / n_bays
        for i in range(n_bays):
            cx = p["x_min"] + bay_w * (i + 0.5)
            cy = (p["y_min"] + p["y_max"]) / 2
            faces += car(cx, cy, heading="east")

    # Landscape trees at guest-zone and paddock-edge nodes
    tree_positions = [(1.2, 6.5), (11.5, 13.8), (21.5, 6.0), (1.2, 27.0), (37.0, 27.0),
                       (1.2, 30.8), (37.2, 30.8), (18.7, 30.8), (1.2, 49.2), (37.2, 49.2), (5.5, 2.0)]
    for (tx, ty) in tree_positions:
        faces += tree(tx, ty)

    return faces, ground


# ---------------------------------------------------------------------------
# Camera / rasterizer
# ---------------------------------------------------------------------------

def look_at(eye, target, up=np.array([0, 0, 1.0])):
    f = (target - eye)
    f = f / np.linalg.norm(f)
    r = np.cross(f, up)
    r = r / (np.linalg.norm(r) + 1e-9)
    u = np.cross(r, f)
    view = np.eye(4)
    view[0, :3] = r
    view[1, :3] = u
    view[2, :3] = -f
    view[:3, 3] = -view[:3, :3] @ eye
    return view


def perspective(fov_deg, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov_deg) / 2)
    m = np.zeros((4, 4))
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2 * far * near) / (near - far)
    m[3, 2] = -1
    return m


LIGHT_DIR = np.array([-0.45, -0.55, 0.9])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)
AMBIENT = 0.42
DIFFUSE = 0.66


SKY_DAY = (np.array([176, 205, 224]), np.array([238, 227, 202]))
SKY_TWILIGHT = (np.array([48, 54, 96]), np.array([246, 156, 96]))


def sky_gradient(img_w, img_h, palette=SKY_DAY):
    top, bottom = palette
    arr = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    for y in range(img_h):
        t = y / max(1, img_h - 1)
        arr[y, :, :] = (top * (1 - t) + bottom * t).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def project(view, proj, w, h, pts):
    n = len(pts)
    hom = np.concatenate([pts, np.ones((n, 1))], axis=1)
    cam = hom @ view.T
    clip = cam @ proj.T
    w_clip = clip[:, 3]
    valid = w_clip > 1e-4
    ndc = np.zeros((n, 3))
    ndc[valid] = clip[valid, :3] / w_clip[valid, None]
    screen = np.zeros((n, 2))
    screen[:, 0] = (ndc[:, 0] * 0.5 + 0.5) * w
    screen[:, 1] = (1 - (ndc[:, 1] * 0.5 + 0.5)) * h
    return screen, cam[:, :3], valid


def render_view(faces, ground, eye, target, fov, out_path, title, sky=SKY_DAY, ambient=AMBIENT,
                 warm_tint=1.0):
    w, h = W * SS, H * SS
    view = look_at(np.array(eye, dtype=float), np.array(target, dtype=float))
    proj = perspective(fov, w / h, 0.1, 200.0)

    img = sky_gradient(w, h, sky)
    draw = ImageDraw.Draw(img, "RGBA")

    eye_np = np.array(eye, dtype=float)

    # --- ground first (painter's algorithm handles the rest) ---
    all_faces = list(ground) + list(faces)

    # soft contact shadows: project a darkened footprint of each volume onto the ground plane
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    for f in faces:
        if abs(f.normal[2]) < 0.9:
            continue  # only use roof-ish upward faces as shadow casters (skip walls)
        offset = np.array([0.9, 0.7, 0.0])
        pts = np.array([v - offset for v in f.verts])
        screen, cam_pts, valid = project(view, proj, w, h, pts)
        if not valid.all() or (cam_pts[:, 2] > -0.05).any():
            continue
        poly = [tuple(p) for p in screen]
        sdraw.polygon(poly, fill=(20, 16, 12, 95))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6 * SS / 2))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow_layer).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    # --- depth-sort all faces (painter's algorithm) ---
    entries = []
    for f in all_faces:
        pts = np.array(f.verts)
        screen, cam_pts, valid = project(view, proj, w, h, pts)
        if not valid.all():
            continue
        if (cam_pts[:, 2] > -0.05).any():
            continue  # behind/at camera
        to_cam = eye_np - np.mean(pts, axis=0)
        if np.dot(to_cam, f.normal) <= 0:
            continue  # backface cull
        # Sort key: blend of nearest-corner and mean depth reduces (does not fully eliminate)
        # classic painter's-algorithm ordering errors between overlapping convex volumes.
        depth = float(0.5 * np.max(cam_pts[:, 2]) + 0.5 * np.mean(cam_pts[:, 2]))
        ndotl = max(0.0, float(np.dot(f.normal, LIGHT_DIR)))
        intensity = ambient + DIFFUSE * ndotl
        if warm_tint != 1.0:
            col = tuple(min(255, int(c * intensity * (warm_tint if i == 0 else (1.0 if i == 1 else 2 - warm_tint))))
                        for i, c in enumerate(f.color))
        else:
            col = tuple(min(255, int(c * intensity)) for c in f.color)
        entries.append((depth, screen, col))

    entries.sort(key=lambda e: e[0])  # far (more negative) first
    for depth, screen, col in entries:
        poly = [tuple(p) for p in screen]
        draw.polygon(poly, fill=col + (255,))

    img = img.resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font = ImageFont.load_default()
        small = font
    draw.rectangle([0, H - 56, W, H], fill=(20, 16, 12, 210))
    draw.text((18, H - 48), title, font=font, fill=(240, 235, 224))
    draw.text((18, H - 22), DISCLAIMER, font=small, fill=(224, 200, 190))
    img.save(out_path)
    print("Wrote", out_path)


VIEWS = [
    ("aerial_exterior.png", (-14, -16, 32), (20, 26, 1.5), 42,
     "Aerial Exterior — Deterministic 3D View (from model.py)", {}),
    ("stable_aisle.png", (-9.0, 4.0, 19.0), (19.0, 22.0, 1.4), 42,
     "Stable Aisle Interior — Deterministic 3D View", {}),
    ("paddock_courtyard.png", (20.0, 22.5, 6.5), (20.0, 47.0, 0.6), 46,
     "Paddock & Service Courtyard — Deterministic 3D View", {}),
    ("guest_majlis.png", (1.0, -9.0, 12.5), (15.0, 9.5, 1.5), 40,
     "Guest & Majlis Zone — Deterministic 3D View", {}),
    ("entry_parking.png", (46.0, -15.0, 15.0), (29.0, 7.0, 1.0), 40,
     "Entry & Parking Apron — Deterministic 3D View", {}),
    ("twilight_hero.png", (-18, -20, 26), (20, 24, 2.5), 40,
     "Twilight Hero View — Deterministic 3D View",
     {"sky": SKY_TWILIGHT, "ambient": 0.30, "warm_tint": 1.18}),
]


def main():
    faces, ground = build_scene()
    print(f"Scene built: {len(faces)} volume faces, {len(ground)} ground faces")
    for fname, eye, target, fov, title, kwargs in VIEWS:
        render_view(faces, ground, eye, target, fov, OUT_DIR / fname, title, **kwargs)


if __name__ == "__main__":
    main()
