"""Generate room_schedule.csv and coordinate_schedule.csv from model.py."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model import spaces, SITE_WIDTH, SITE_DEPTH  # noqa: E402

OUT_DIR = Path(__file__).parent.parent / "output" / "schedules"
OUT_DIR.mkdir(parents=True, exist_ok=True)

fields = ["id", "arabic_name", "english_name", "function", "width_m", "depth_m",
          "area_m2", "x_min", "y_min", "x_max", "y_max", "door", "source", "notes"]

with open(OUT_DIR / "room_schedule.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for s in spaces:
        w.writerow(s)

with open(OUT_DIR / "coordinate_schedule.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["id", "english_name", "x_min", "y_min", "x_max", "y_max", "width_m", "depth_m", "area_m2"])
    w.writeheader()
    for s in spaces:
        w.writerow({k: s[k] for k in w.fieldnames})

print(f"Wrote room_schedule.csv and coordinate_schedule.csv to {OUT_DIR}")
print(f"Site: {SITE_WIDTH} x {SITE_DEPTH} m, {len(spaces)} spaces scheduled")
