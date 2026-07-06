"""
Luxury Equestrian Stable - Redesign Geometry Model
Concept design only. Not for construction or permit use.

Coordinate system:
  Origin (0,0) = southwest (front-left) corner of the site, at the entrance/street side.
  X axis = site width, 0.00 <= x <= 40.00 (west -> east)
  Y axis = site depth, 0.00 <= y <= 50.00 (Y=0 front/entrance, Y=50 rear boundary)
  Units: meters.

PROVENANCE (Source Extraction Agent output - see design/output/reports/source_audit.md for the
full audit). Uploaded package: "Stable PROJECT.zip" containing:
  - Requirments.txt        (explicit written program - source hierarchy priority #1)
  - stable 1.pdf           (dimensioned existing CAD plan - priority #2)
  - WhatsApp ...3.27.30 PM.jpeg  (3D render of the existing design - visual reference only, priority #4)
  - WhatsApp ...3.44.13 PM.jpeg  (hand sketch confirming site 40x50m + gate on north/front edge - priority #3)

Every room below carries a `source` field:
  "required_program"      - explicit in Requirments.txt, size mandated
  "cad_sourced"            - dimension read directly off stable 1.pdf
  "cad_sourced_approx"     - dimension estimated from stable 1.pdf where the drawing was only
                             partially legible/dimensioned (see source_audit.md)
  "redesign_choice"        - no dimension given anywhere in source; sized by this redesign
                             (flagged for owner confirmation)
  "redesign_improvement"   - deliberately changed from the (inconsistent/inefficient) existing
                             layout as a named improvement, not a blind copy

RESOLVED (owner confirmation, this pass): the 2 rooms spelled "مصلب" in stable 1.pdf but "مصاب" in
the rendered image (WhatsApp 3.27.30 PM) are CONFIRMED by the owner as مصاب - injured/veterinary
isolation rooms. Function, label, and fit-out direction (isolation ventilation, vet drainage, exam
lighting) are now final; see OWNER_CONFIRMATION_FINALIZATION_REPORT.md for the decision record.

RESOLVED (owner confirmation, this pass): the service room (SV01) is CONFIRMED at 6.00 x 3.00 m,
matching the stable 1.pdf CAD reading rather than the 3.00 x 3.00 m in Requirments.txt line 6. This
required reflowing the wing band (see the wing section below) since the wider service room no
longer fits the original layout without adjustment; the worker kitchen (WK01) and worker bathroom
(WBTH01) were narrowed to absorb the difference - both were redesign-choice rooms with no source-
mandated size, so this trade-off does not touch any explicitly required dimension. See
OWNER_CONFIRMATION_FINALIZATION_REPORT.md.

RESOLVED (owner confirmation, this pass): outdoor majlis (OSA01) and private bathroom (PBTH01)
widths, the parking apron (PK01), and the worker bedroom (WB01) footprint are all CONFIRMED as
previously modeled - no geometry change needed for these four items.
"""

SITE_WIDTH = 40.00
SITE_DEPTH = 50.00

# ---------------------------------------------------------------------------
# Zones (non-room bands used for narrative/report + dimension-chain proof)
# ---------------------------------------------------------------------------
Y_BANDS = [
    ("Motor court / arrival + parking apron", 0.00, 5.00),
    ("Guest rooms band (majlis / outdoor majlis-sitting / private suite)", 5.00, 13.24),
    ("Landscaped transition / privacy buffer", 13.24, 15.24),
    ("Stable Row A (standard stalls S01-S10)", 15.24, 18.99),
    ("Central stable aisle", 18.99, 22.49),
    ("Stable Row B (standard stalls S11-S20)", 22.49, 26.24),
    ("Feed / service / premium / special / worker wing", 26.24, 30.24),
    ("Vestibule / gate transition to paddock spine", 30.24, 31.24),
    ("Paddocks + central wash/manure service spine", 31.24, 50.00),
]

X_BANDS = [
    ("Program width (stalls, wing, guest rooms, paddocks)", 0.00, 37.50),
    ("Perimeter service / emergency fire lane", 37.50, 40.00),
]

# ---------------------------------------------------------------------------
# Spaces: every enclosed room + functional open zone
# ---------------------------------------------------------------------------
spaces = []

def add(id_, ar, en, func, x0, y0, x1, y1, door, source, notes=""):
    spaces.append(dict(
        id=id_, arabic_name=ar, english_name=en, function=func,
        x_min=round(x0, 3), y_min=round(y0, 3), x_max=round(x1, 3), y_max=round(y1, 3),
        width_m=round(x1 - x0, 3), depth_m=round(y1 - y0, 3),
        area_m2=round((x1 - x0) * (y1 - y0), 4),
        door=door, source=source, notes=notes,
    ))

# --- HORSE ZONE: 20 standard stalls, two rows of 10, flanking central aisle ---
STALL = 3.75
for i in range(10):
    x0 = i * STALL
    add(f"S{i+1:02d}", "غرفة خيل", f"Standard Horse Stall {i+1}", "horse_stall",
        x0, 15.24, x0 + STALL, 18.99,
        door="south wall, aisle-facing", source="required_program",
        notes="Row A. 3.75x3.75m per Requirments.txt line 1 and stable 1.pdf. Dutch door, yoke bars, "
              "non-slip rubber pavers.")

for i in range(10):
    x0 = i * STALL
    add(f"S{i+11:02d}", "غرفة خيل", f"Standard Horse Stall {i+11}", "horse_stall",
        x0, 22.49, x0 + STALL, 26.24,
        door="north wall, aisle-facing", source="required_program",
        notes="Row B. 3.75x3.75m per Requirments.txt line 1 and stable 1.pdf.")

# --- Wing band (Y26.24-30.24): worker rooms (west) | premium/vet/feed/service (center-east) ---
# Reflowed this pass to fit SV01 at its owner-confirmed 6.00 x 3.00 m (was 3.00 x 3.00 m), which no
# longer fits the original sequence without adjustment. WK01 and WBTH01 (both redesign-choice rooms
# with no source-mandated size) were narrowed to absorb the extra 3.00 m; every required_program
# room (P01, P02, SP01/SP02 dimensions, FD01, SV01) keeps its confirmed size unchanged. The wing now
# spans X0.00-37.50 exactly (previously 0.50-37.00 with 1.00 m of unused margin), flush with the
# stall rows above it.
WING_Y0, WING_Y1 = 26.24, 30.24

add("WB01", "غرفة نوم عمال", "Worker Bedroom (4 workers)", "worker_bedroom",
    0.00, WING_Y0, 7.00, WING_Y1, door="north wall, service-corridor-facing",
    source="redesign_improvement",
    notes="7.00 x 4.00 m = 28 m2. stable 1.pdf shows an existing worker block (سكن عمال + حمام + "
          "مطبخ combined) approx. 4.74 x 13.66 m deep and narrow, wedged between stall columns. "
          "Redesign reflows the same program into a shallower, wider footprint aligned with the "
          "feed/service wing for a cleaner unified roofline and easier staff access - same function, "
          "improved proportions. Footprint and bunk layout for 4 workers CONFIRMED by owner as-is.")

add("WK01", "مطبخ العمال", "Worker Kitchen", "worker_kitchen",
    7.00, WING_Y0, 10.50, WING_Y1, door="north wall, service-corridor-facing",
    source="redesign_improvement", notes="3.50 x 4.00 m = 14 m2. Narrowed from an earlier 4.50 m width "
          "this pass to absorb the owner-confirmed 6.00 m service room (SV01) below; no source-"
          "mandated size for this room, so this is a redesign trade-off, not a lost requirement.")

add("WBTH01", "حمام العمال", "Worker Bathroom", "worker_bathroom",
    10.50, WING_Y0, 12.50, WING_Y1, door="north wall, service-corridor-facing",
    source="redesign_improvement", notes="2.00 x 4.00 m = 8 m2. Narrowed from an earlier 3.00 m width "
          "this pass to absorb the owner-confirmed 6.00 m service room (SV01) below; no source-"
          "mandated size for this room, so this is a redesign trade-off, not a lost requirement.")

add("P01", "غرفة خيل 4x4", "Premium Horse Stall 1", "premium_horse_stall",
    12.50, WING_Y0, 16.50, WING_Y1, door="north wall, corridor-facing",
    source="required_program", notes="4.00 x 4.00 m exactly as labeled 'غرفة خيل 4x4' in stable 1.pdf.")

add("SP01", "غرفة مصاب خيل", "Veterinary / Isolation Room 1", "veterinary_isolation_room",
    16.50, WING_Y0, 20.00, WING_Y1, door="north wall, corridor-facing",
    source="cad_sourced + owner_confirmed",
    notes="3.50 x 4.00 m, dimensions read directly off stable 1.pdf. Label/function CONFIRMED by "
          "owner this pass as 'مصاب' (injured/veterinary-isolation room) - the reading shown in the "
          "rendered image (WhatsApp 3.27.30 PM); the CAD's alternate spelling 'مصلب' is superseded. "
          "Positioned away from the general stall population, adjacent to feed/service and nearest "
          "the rear wash/service yard - correct functional location for isolation/vet use. Fit-out "
          "should provide independent ventilation, a washable/drainable floor, and dedicated exam "
          "lighting (licensed MEP/vet consultant review required before construction).")

add("FD01", "غرفة علف", "Feed Room", "feed_room",
    20.00, WING_Y0, 24.00, WING_Y1, door="north wall, corridor-facing",
    source="required_program", notes="4.00 x 4.00 m exactly as labeled 'غرفة علف' in stable 1.pdf.")

add("SV01", "غرفة خدمة", "Service Room", "service_room",
    24.00, WING_Y0, 30.00, WING_Y0 + 3.00, door="north wall, corridor-facing",
    source="cad_sourced + owner_confirmed",
    notes="6.00 x 3.00 m, CONFIRMED by owner this pass as governing over the 3.00 x 3.00 m in "
          "Requirments.txt line 6 - stable 1.pdf's CAD dimension is now the final size. Oriented with "
          "the 6.00 m dimension along the aisle (matching the CAD reading) and flush to the aisle-"
          "facing wall of the wing, leaving a 1.00 m recessed service alcove at the rear (consistent "
          "with the special/service room massing rhythm elsewhere in the wing).")

add("SP02", "غرفة مصاب خيل", "Veterinary / Isolation Room 2", "veterinary_isolation_room",
    30.00, WING_Y0, 33.50, WING_Y1, door="north wall, corridor-facing",
    source="cad_sourced + owner_confirmed", notes="See SP01 note - identical owner-confirmed label/function applies.")

add("P02", "غرفة خيل 4x4", "Premium Horse Stall 2", "premium_horse_stall",
    33.50, WING_Y0, 37.50, WING_Y1, door="north wall, corridor-facing",
    source="required_program", notes="4.00 x 4.00 m exactly as labeled 'غرفة خيل 4x4' in stable 1.pdf.")

# --- Guest / owner zone (front band, Y5.00-13.24) ---
add("MJ01", "مجلس", "Men's Majlis", "majlis",
    2.00, 5.00, 10.00, 13.24, door="north wall, motor-court-facing",
    source="cad_sourced", notes="8.00 x 8.24 m = 65.92 m2, dimensions read directly off stable 1.pdf "
                                 "('مجلس', width 8, depth 8.24).")

add("MWC01", "حمام (مجلس)", "Men's WC (majlis)", "mens_wc",
    10.00, 5.00, 11.76, 6.76, door="west wall, majlis-adjacent",
    source="cad_sourced", notes="1.76 x 1.76 m = 3.10 m2, dimensions read directly off stable 1.pdf small "
                                 "'حمام' beside the bedroom/majlis cluster. stable 1.pdf shows two 'حمام' "
                                 "rooms in this cluster; this one is assigned to the majlis per "
                                 "Requirments.txt line 8 ('مجلس رجال مع دورة مياه').")

add("OSA01", "مجلس خارجي / جلسة خارجية", "Outdoor Majlis / Sitting Area", "outdoor_sitting",
    12.50, 5.00, 20.50, 13.24, door="open arcade, no enclosing door (shaded pergola)",
    source="cad_sourced_approx + owner_confirmed",
    notes="8.00 x 8.24 m, mirrored to match the indoor majlis footprint for a symmetric twin-courtyard "
          "composition. stable 1.pdf labels this 'مجلس خارجي' with a confirmed depth of 8.24 m (shared "
          "dimension line with the indoor majlis); its width was not fully legible in the drawing, so "
          "8.00 m was a redesign choice matching the majlis for symmetry - CONFIRMED by owner as final "
          "this pass. Satisfies Requirments.txt line 9 ('جلسة خارجية').")

add("PBR01", "غرفة نوم خاصة", "Private Bedroom", "private_bedroom",
    22.50, 5.00, 27.33, 8.76, door="north wall, private courtyard-facing",
    source="cad_sourced", notes="4.83 x 3.76 m = 18.16 m2, dimensions read directly off stable 1.pdf "
                                 "('غرفة نوم', 4.83 wide x 3.76 deep).")

add("PBTH01", "حمام (خاص)", "Private Bathroom", "private_bathroom",
    22.50, 8.76, 27.33, 10.76, door="north wall, ensuite from private bedroom",
    source="cad_sourced_approx + owner_confirmed",
    notes="4.83 x 2.00 m = 9.66 m2. Depth of 2.00 m read directly off stable 1.pdf; width assumed "
          "equal to the bedroom above it (no separate width dimension legible in the source drawing) "
          "- CONFIRMED by owner as final this pass.")

# --- Parking (found in the rendered image only - optional program addition, KEPT by owner decision) ---
add("PK01", "بركنج", "Parking Apron (4 bays)", "parking",
    26.00, 0.50, 37.00, 4.50, door="direct from motor court, open-air",
    source="found in render only + owner_confirmed",
    notes="11.00 x 4.00 m apron for 4 vehicles. Not present in Requirments.txt or dimensioned in "
          "stable 1.pdf; visible only in the rendered image (WhatsApp 3.27.30 PM, labeled 'بركنج'). "
          "CONFIRMED by owner this pass to be kept as modeled.")

# --- Paddocks (Y31.24-50.00) ---
add("PD01", "بادوك 1", "Paddock 1", "paddock",
    0.00, 31.24, 17.00, 50.00, door="east gate at x=17.00, onto service spine",
    source="required_program / redesign_improvement",
    notes="17.00 x 18.76 m = 318.92 m2. stable 1.pdf shows the 2 existing paddocks as UNEQUAL "
          "(approx. 15x10m = 150 m2 and 15x15m = 225 m2) - inconsistent and flagged as a weakness "
          "in the existing layout. Redesign makes both paddocks equal and larger, per the design "
          "intent that paddocks be practical, not decorative, and consistently dimensioned.")

add("PD02", "بادوك 2", "Paddock 2", "paddock",
    20.50, 31.24, 37.50, 50.00, door="west gate at x=20.50, onto service spine",
    source="required_program / redesign_improvement",
    notes="17.00 x 18.76 m = 318.92 m2. Equal to PD01 - see PD01 note.")

# --- Functional open zones included for completeness (not enclosed rooms) ---
add("WSY01", "ممر الخدمة والغسيل", "Wash / Manure Service Spine", "service_yard",
    17.00, 31.24, 20.50, 50.00, door="gates at both paddocks + connects to fire lane",
    source="redesign_choice", notes="3.50 x 18.76 m = 65.66 m2 open service yard: wash-down bay, manure "
                                     "skip, water point, drainage channel. Not an enclosed room.")

add("FL01", "ممر الخدمة والطوارئ المحيطي", "Perimeter Service / Fire Lane", "service_lane",
    37.50, 0.00, 40.00, 50.00, door="gated at motor court (north) and paddock spine (south)",
    source="redesign_choice", notes="2.50 x 50.00 m = 125 m2 continuous perimeter lane for emergency "
                                     "vehicle access and service/feed delivery, kept separate from the "
                                     "guest motor court. Confirms the hand-sketch note that the site gate "
                                     "sits on the front (Y=0) edge - this lane connects that gate straight "
                                     "through to the rear paddock service spine.")

add("MC01", "ساحة الاستقبال", "Motor Court / Arrival", "arrival_court",
    0.00, 0.00, 37.50, 5.00, door="main entrance gate, north edge (y=0), per hand-sketch orientation",
    source="cad_sourced_approx", notes="37.50 x 5.00 m landscaped guest arrival & drop-off, open (not "
                                        "enclosed). Gate position confirmed by the hand sketch "
                                        "(WhatsApp 3.44.13 PM), which marks the site entrance on this edge.")

if __name__ == "__main__":
    for s in spaces:
        print(s["id"], s["english_name"], s["area_m2"])
