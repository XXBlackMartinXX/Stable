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

# --- area_summary.csv: area by function, computed live ---
from collections import defaultdict  # noqa: E402

FUNC_LABEL = {
    "horse_stall": "Standard Horse Stalls", "premium_horse_stall": "Premium Horse Stalls",
    "veterinary_isolation_room": "Veterinary / Isolation Rooms", "feed_room": "Feed Room",
    "service_room": "Service Room", "paddock": "Paddocks", "worker_bedroom": "Worker Bedroom",
    "worker_kitchen": "Worker Kitchen", "worker_bathroom": "Worker Bathroom", "majlis": "Men's Majlis",
    "mens_wc": "Men's WC", "outdoor_sitting": "Outdoor Majlis / Sitting",
    "private_bedroom": "Private Bedroom", "private_bathroom": "Private Bathroom",
    "parking": "Parking Apron", "service_yard": "Service Yard",
    "service_lane": "Fire Lane / Service Lane", "arrival_court": "Arrival / Motor Court",
}
agg = defaultdict(lambda: {"count": 0, "area": 0.0})
for s in spaces:
    agg[s["function"]]["count"] += 1
    agg[s["function"]]["area"] += s["area_m2"]
site_area = SITE_WIDTH * SITE_DEPTH
total = sum(v["area"] for v in agg.values())
with open(OUT_DIR / "area_summary.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(["function", "count", "area_m2", "pct_of_scheduled"])
    for func, v in sorted(agg.items(), key=lambda kv: -kv[1]["area"]):
        wr.writerow([FUNC_LABEL.get(func, func), v["count"], f"{v['area']:.2f}",
                     f"{v['area'] / total * 100:.1f}%"])
    wr.writerow([])
    wr.writerow(["TOTAL SCHEDULED", len(spaces), f"{total:.2f}", f"{total / site_area * 100:.1f}%"])
    wr.writerow(["SITE AREA", "", f"{site_area:.2f}", "100.0%"])
print("Wrote area_summary.csv")
