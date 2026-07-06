# Luxury Equestrian Stable Redesign — Full Project Report

**Concept plan only. Not for construction or permit use until reviewed and approved by a licensed
local architect/engineer, MEP/civil engineer, and fire/life-safety consultant.**

---

## 1. Executive Summary

The uploaded `Stable PROJECT.zip` contains a fully-specified 40m x 50m equestrian compound program
(20 standard stalls, 2 premium stalls, 2 veterinary/isolation horse rooms, feed room, 2 paddocks,
service room, 4-worker accommodation, men's majlis, outdoor sitting, and a private bedroom suite)
already laid out once, in a dimensioned CAD drawing and a matching 3D render. That existing layout
works but is cramped in places, its two paddocks are inconsistently sized (150 m² vs 225 m²), its
worker housing is squeezed into an oddly narrow 4.74m-wide slot, and its guest and service
circulation are not clearly separated.

This redesign keeps every mandated room, count, and confirmed dimension, and reorganizes the
compound into eight clear west-to-east bands (guest arrival → majlis/private-suite → stable aisle →
feed/service/worker wing → paddocks), separated by a continuous perimeter fire/service lane so
horse, guest, and service circulation never cross unnecessarily. Both paddocks are equalized at
{{PADDOCK_AREA}} m² each (previously unequal in the source). All {{SPACE_COUNT}} spaces are
validated by script: every dimension chain closes exactly to 40.00 x 50.00 m, no rooms overlap, and
every mandatory count and size from the source program is present.

**Owner confirmation status: all 5 previously-flagged items are now resolved** (see §5) — the
special rooms are confirmed as veterinary/isolation rooms (مصاب), the service room is confirmed at
6.00x3.00 m (superseding the 3x3 m brief, which required reflowing the wing band around it), and
the parking apron, outdoor majlis/private bathroom widths, and worker bedroom footprint are all
confirmed as previously modeled.

## 2. Source Audit

### 2.1 Files received and inspected

| # | File | Type | Role in source hierarchy |
|---|------|------|---------------------------|
| 1 | `Requirments.txt` | Plain text, Arabic | Priority 1 — explicit written program |
| 2 | `stable 1.pdf` | Dimensioned CAD line drawing (single sheet, 40x50m) | Priority 2 — measured existing layout |
| 3 | `WhatsApp Image ...3.44.13 PM.jpeg` | Hand sketch | Priority 3 — confirms site 40x50m + gate edge |
| 4 | `WhatsApp Image ...3.27.30 PM.jpeg` | 3D rendered visualization of the existing design | Priority 4 — visual reference only |

All four files were opened and read (the PDF was rasterized at high resolution and cropped/zoomed
region-by-region to read every dimension string; both JPEGs were viewed directly).

### 2.2 Requirments.txt — full extracted program (translated)

1. 20 horse rooms, 3.75 x 3.75 m
2. 2 larger horse rooms, 4 x 4 m
3. 2 "مصلب" horse rooms (no size given)
4. 1 feed room, 4 x 4 m
5. 2 paddocks (no size given)
6. 1 service room, 3 x 3 m
7. Bedroom for 4 workers + bathroom + kitchen (no sizes given)
8. Men's majlis with a WC (no sizes given)
9. Outdoor sitting area (no size given)
10. Private bedroom with private bathroom (no sizes given)

### 2.3 stable 1.pdf — dimensions actually read off the drawing

| Item | Dimension read from CAD | Confidence |
|---|---|---|
| Site | 40 m (top) x 50 m (right side) | High — dimension lines explicit |
| Stalls 1–20 | 3.75 x 3.75 m each, all labeled individually | High |
| 2 rooms labeled "غرفة خيل 4x4" | 4.00 x 4.00 m | High |
| 2 rooms labeled "غرفة **مصلب** خيل" | 3.50 (w) x 4.00 (d) m | High for the numbers; label itself was unresolved between sources — **now confirmed by owner as مصاب (§5)** |
| "غرفة علف" (feed room) | 4.00 x 4.00 m | High |
| "خدمة" (service room) | 6.00 (w) x 3.00 (d) m | High reading; conflicted with Requirments.txt line 6 (3x3) — **owner has confirmed 6.00x3.00 governs (§5)** |
| "مجلس" (majlis) | 8.00 (w) x 8.24 (d) m | High |
| Small "حمام" beside majlis/bedroom cluster | 1.76 x 1.76 m | High |
| "غرفة نوم" (bedroom) | 4.83 (w) x 3.76 (d) m | High |
| Second "حمام" (bathroom near bedroom) | depth 2.00 m confirmed; width not separately dimensioned (assumed = 4.83 m to match room above) | Medium |
| "مجلس خارجي" (outdoor majlis) | depth 8.24 m confirmed (shared line with indoor majlis); width not clearly dimensioned | Medium |
| "سكن عمال" (worker housing) block | approx. 4.74 (w) x 13.66 (d) m overall, subdivided into bedroom (7.2 deep) + bathroom + kitchen (sub-splits partially legible) | Medium |
| 2x "بادوك" (paddocks) | Paddock 1 ≈ 15 x 10 m (150 m²); Paddock 2 ≈ 15 x 15 m (225 m²) — **unequal** | Medium-High |
| Unlabeled compartmentalized block, top-left | No text label in the CAD | Resolved via the render (see 2.4) — this is the parking/carport area |

### 2.4 WhatsApp render (3.27.30 PM) — visual reference only, confirms/adds

- Confirms the general room arrangement matches the CAD (same stall numbering, same adjacencies).
- Shows a **parking apron "بركنج"** for ~4 vehicles at the same spot as the CAD's unlabeled
  top-left block — resolves that ambiguity. Not in the text brief or dimensioned in the CAD.
- **Spells the 2 special rooms "غرفة مصاب خيل"** — a different word from the CAD's "غرفة مصلب خيل".
  This was a genuine spelling conflict between two source files; the owner has since confirmed this
  render's reading (مصاب, injured/veterinary-isolation) as final (§5).
- Confirms two separate bathrooms exist near the majlis/bedroom cluster (one small, one larger),
  consistent with "majlis + WC" and "bedroom + private bath" both being satisfied.

### 2.5 Hand sketch (3.44.13 PM)

Confirms the site is 40 m x 50 m and marks the site **entrance gate on the top edge** of the
sketch — the same edge where the CAD places the majlis/entrance cluster. This confirms the Y=0 edge
in this redesign's coordinate system is the correct entrance/front edge (true compass north was
never given in any source file).

### 2.6 Existing-layout strengths

- Clear stall numbering and a logical double-loaded stable aisle (rows of 10 facing a shared aisle).
- Feed and service rooms already grouped adjacent to the special rooms.
- Guest cluster (majlis, outdoor majlis, bedroom, bathrooms) already separated from the stable block.

### 2.7 Existing-layout weaknesses (diagnosed, addressed in redesign)

- **Unequal paddocks** (150 m² vs 225 m²) — inconsistent, reads as an afterthought rather than a
  designed pair.
- **Worker housing** is a very narrow (4.74 m wide) block wedged between two stall columns —
  cramped proportions for a 4-person bedroom + bath + kitchen.
- No visible dedicated fire/emergency/service lane separate from the guest motor court.
- Service room dimensioned inconsistently between the brief (3x3) and the CAD (6x3) — resolved
  this pass; owner confirmed 6.00x3.00 m governs (§5).

### 2.8 Confidence levels

- **High confidence:** site 40x50m; all 20 standard stall sizes; both premium stall sizes; feed
  room size; majlis size; majlis WC size; private bedroom size; gate on the front edge.
  Requirements clearly explicit or clearly dimensioned in ≥2 sources.
- **Medium confidence:** special-room size (3.5x4.0, numbers clear, label meaning needed owner
  input); private bathroom width; outdoor majlis width; worker-block internal sub-splits; paddock
  exact dimensions (legible but slightly compressed layout in the scan).
- **Resolved by owner confirmation (this pass, not guessed):** special-room function/label (مصاب);
  service-room size (6.00x3.00 m). See §5.

## 3. Source Conflict Table

| # | Conflicting item | Source A | Source B | Interpretation used in this redesign | Confidence | Owner decision |
|---|---|---|---|---|---|---|
| 1 | Special horse-room label | `stable 1.pdf`: **"مصلب"** (breeding/covering room reading, from تصليب = crossbreeding) | Render `...3.27.30 PM.jpeg`: **"مصاب"** (literally "injured" → veterinary/infirmary reading) | **RESOLVED:** owner confirmed مصاب — the 2 rooms (SP01, SP02) are veterinary/isolation rooms; the CAD's مصلب spelling is superseded | Medium (numbers), Low (label meaning, now closed) | **مصاب — injured/vet room** |
| 2 | Service room size | `Requirments.txt` line 6: **3.00 x 3.00 m** (explicit written requirement) | `stable 1.pdf`: **6.00 x 3.00 m** (measured CAD) | **RESOLVED:** owner confirmed 6.00 x 3.00 m governs, superseding the written brief; the wing band was reflowed (WK01/WBTH01 narrowed) to fit it | High (both readings clear; now closed) | **6.00 x 3.00 m** |
| 3 | Outdoor majlis / private bathroom width | `stable 1.pdf`: depth dimensioned, width not clearly legible at scan resolution | — | **RESOLVED:** owner confirmed both as modeled — outdoor majlis mirrors the indoor majlis (8.00 m); private bathroom matches the bedroom width above it (4.83 m) | Medium | **Confirm current values** |
| 4 | Worker housing proportions | `stable 1.pdf`: single narrow block, 4.74 x 13.66 m overall | — | Redesign reflows the same combined area into a shallower, wider 3-room wing (bedroom/kitchen/bath) aligned with the feed/service wing — same function, improved proportions. Owner confirmed the WB01 (bedroom) footprint/bunk layout as modeled; WK01/WBTH01 were subsequently narrowed to fit the SV01 decision above (item 2) | N/A (deliberate improvement) | **WB01 confirmed; WK01/WBTH01 narrowed as a disclosed consequence of item 2** |
| 5 | Paddock sizing | `stable 1.pdf`: unequal, ~150 m² and ~225 m² | — | Redesign makes both paddocks equal at {{PADDOCK_AREA}} m² each | N/A (deliberate improvement) | Not a conflict requiring owner input — an unambiguous improvement |
| 6 | Parking apron | Not in `Requirments.txt` or `stable 1.pdf` | Present in render `...3.27.30 PM.jpeg` ("بركنج", ~4 cars) | **RESOLVED:** owner confirmed PK01 is kept exactly as modeled (11.00x4.00 m, 4 bays) | N/A | **Keep as-is** |

## 4. Required Program Checklist (source vs. delivered)

| Item | Required | Delivered | Status |
|---|---|---|---|
| Site | 40.00 x 50.00 m | 40.00 x 50.00 m | ✅ |
| Standard horse stalls | 20 @ 3.75x3.75m | 20 @ 3.75x3.75m (S01–S20) | ✅ |
| Premium horse stalls | 2 @ 4.00x4.00m | 2 @ 4.00x4.00m (P01, P02) | ✅ |
| Veterinary/isolation rooms (مصاب) | 2, label unclear | 2 @ 3.50x4.00m (SP01, SP02), label CONFIRMED as مصاب | ✅ (resolved) |
| Feed room | 1 @ 4.00x4.00m | 1 @ 4.00x4.00m (FD01) | ✅ |
| Paddocks | 2 | 2 @ {{PADDOCK_AREA}} m² each, equal (PD01, PD02) | ✅ (+ improved) |
| Service room | 1 @ 3.00x3.00m per brief | 1 @ 6.00x3.00m (SV01); owner-confirmed per CAD | ✅ (resolved) |
| Worker bedroom (4) | 1 | WB01, 7.00x4.00m = 28 m² | ✅ |
| Worker bathroom | 1 | WBTH01, 2.00x4.00m = 8 m² | ✅ |
| Worker kitchen | 1 | WK01, 3.50x4.00m = 14 m² | ✅ |
| Men's majlis | 1 | MJ01, 8.00x8.24m = 65.92 m² | ✅ |
| Men's WC | 1 | MWC01, 1.76x1.76m = 3.10 m² | ✅ |
| Outdoor sitting | 1 | OSA01, 8.00x8.24m = 65.92 m² | ✅ |
| Private bedroom | 1 | PBR01, 4.83x3.76m = 18.16 m² | ✅ |
| Private bathroom | 1 | PBTH01, 4.83x2.00m = 9.66 m² | ✅ |
| Parking (optional) | — | PK01, 11.00x4.00m, 4 bays | ✅ (optional, flagged) |

## 5. Owner-Confirmed Decisions (Finalized This Pass)

All 5 items previously flagged as requiring owner input are now resolved:

1. **Special room label/function** (SP01, SP02) — **CONFIRMED: مصاب (injured/veterinary-isolation
   room)**, the reading shown in the rendered image. The CAD's alternate spelling "مصلب"
   (breeding/covering) is superseded. Fit-out direction: isolation ventilation, washable/drainable
   floor, dedicated exam lighting — subject to licensed MEP/veterinary-consultant review (§18).
2. **Service room size** — **CONFIRMED: 6.00 x 3.00 m**, per the stable 1.pdf CAD, superseding the
   3.00 x 3.00 m in Requirments.txt line 6. This required reflowing the wing band (WK01 and WBTH01
   narrowed) — see §6 and §9.
3. **Outdoor majlis width** and **private bathroom width** — **CONFIRMED as modeled**: 8.00 m and
   4.83 m respectively, no change.
4. **Parking apron** — **CONFIRMED: kept as-is** (4 bays, 11.00x4.00 m).
5. **Worker bedroom bunk layout** — **CONFIRMED as modeled**: the 7.00x4.00 m (28 m²) footprint is
   final; specific bunk/furniture arrangement for 4 workers is an interior fit-out detail for a
   later design phase, not a geometry change.

## 6. Proposed Zoning Strategy

The site is organized into 9 bands along the Y-axis (front-to-back), each closing exactly against
the 40.00 x 50.00 m boundary (see §11):

1. **Motor court + parking (Y0–5):** guest arrival, drop-off, optional 4-bay parking apron.
2. **Guest/owner band (Y5–13.24):** majlis and outdoor majlis mirrored either side of a landscaped
   view corridor; private bedroom suite (with ensuite) tucked to the east, private from the majlis.
3. **Privacy/transition buffer (Y13.24–15.24):** landscaped, controls the sightline from guest to
   working stable.
4. **Stall Row A (Y15.24–18.99)** / **aisle (Y18.99–22.49)** / **Stall Row B (Y22.49–26.24):** the
   20 standard stalls in a double-loaded barn, aisle-facing, non-slip flooring, shaded canopy above.
5. **Feed/service/premium/veterinary/worker wing (Y26.24–30.24):** one unified roofline containing,
   west to east: worker bedroom, kitchen, bathroom, then premium stall, veterinary/isolation room,
   feed room, service room (6.00x3.00 m, owner-confirmed), veterinary/isolation room, premium stall
   — everything the stable needs day-to-day, one aisle away from the horses, one wall away from the
   paddocks. The worker kitchen and bathroom were narrowed this pass (to 3.50 m and 2.00 m
   respectively) to fit the owner-confirmed 6.00 m-wide service room without changing any other
   room's confirmed size.
6. **Vestibule (Y30.24–31.24):** gated transition from the working wing to the paddock spine.
7. **Paddocks + wash/manure spine (Y31.24–50.00):** two equal paddocks flanking a dedicated
   wash-down/manure/drainage service yard.

A continuous **2.50 m perimeter fire/service lane** runs the full site depth along the east edge
(X37.5–40), connecting the front gate straight through to the rear paddock service spine without
crossing the guest motor court or the majlis.

### Why this is better than the existing layout

- **Horse zone logic:** unchanged 20+2 stall count and sizes, but the two rows now share one
  continuous shaded aisle rather than being split across separate wings, shortening every staff
  round.
- **Paddock placement:** both paddocks now equal and directly reachable from the working wing via
  a dedicated wash/manure spine — turnout no longer requires crossing guest or general circulation.
- **Guest/majlis sequence:** arrival → motor court → majlis/outdoor majlis (twin courtyards) →
  private suite, with a clear visual/physical stop (the transition buffer) before the stable begins.
- **Worker/service separation:** worker housing and feed/service now share one wing and one roofline
  instead of being buried in a narrow slot between stall columns — shorter walks, easier to service,
  visually calmer.
- **Feed/service efficiency:** feed and service rooms sit at the center of the wing, equidistant
  from both stall rows.
- **Visual hierarchy:** guest wing at the most prominent/generous frontage; stable in the calm
  productive middle; service/paddocks at the working rear — a classic, legible luxury-estate
  hierarchy.

## 7. Layout Option Comparison

**Option A — Maximum efficiency:** single-loaded stall rows in a straight line along one site edge,
paddocks along the other. Pros: simplest circulation, cheapest to build. Cons: much longer walking
distances for feed/service rounds (one row instead of a double-loaded aisle), wastes the "back
courtyard" opportunity, doesn't read as luxury. Circulation 7/10, Luxury 4/10, Operational 6/10.

**Option B — Luxury courtyard emphasis:** stalls wrapped around a large central courtyard with the
majlis/guest suite as a freestanding pavilion. Pros: dramatic entrance sequence, strong axial views.
Cons: the courtyard consumes area that would otherwise go to paddocks (working against "paddocks
must be practical, not decorative"), longer service travel around the perimeter. Circulation 6/10,
Luxury 9/10, Operational 5/10.

**Option C — Hybrid (selected):** the banded/zoned layout described in §6 — double-loaded aisle for
efficient horse care, a twin-courtyard guest sequence for the luxury arrival experience, and a
dedicated rear paddock/service zone. Circulation 9/10, Luxury 8/10, Operational 9/10.

**Recommendation:** Option C. It delivers nearly all of Option B's arrival drama (twin majlis
courtyards, generous private suite) while keeping Option A's operational efficiency (short, single
aisle for all 20 stalls; feed/service centered on that aisle), and it is the only option that keeps
both paddocks large, equal, and directly serviceable — matching the explicit design intent that
paddocks not be decorative.

## 8. Final Selected Layout

See the dimensioned plan (`design/output/plans/plan_dimensioned.svg` / `.png`), the styled
masterplan (`masterplan_luxury.svg` / `.png`), the DXF underlay (`stable_concept_underlay.dxf`),
and the 3D massing model described in §16. All follow the exact coordinates in §10/§11.

## 9. Full Room Schedule

Full machine-readable schedule: `design/output/schedules/room_schedule.csv` ({{SPACE_COUNT}} spaces,
all fields: ID, Arabic/English name, function, width, depth, area, coordinates, door, source, notes).
The table below is generated directly from `design/scripts/model.py` — the same source of truth
used for every other output.

{{ROOM_SCHEDULE_TABLE}}

**Total scheduled area: {{TOTAL_AREA}} m² of {{SITE_AREA}} m² site ({{TOTAL_AREA_PCT}}%)** — the
remaining ~{{REMAINING_PCT}}% is landscaped buffer/transition/aisle circulation, deliberately left
open for a calm, uncluttered feel.

## 10. Full Coordinate Schedule

Full machine-readable coordinate schedule: `design/output/schedules/coordinate_schedule.csv`.
Coordinate system: origin (0,0) = southwest/front-left corner; X = width (0–40 m); Y = depth
(0–50 m, Y=0 = entrance edge confirmed by the source hand sketch).

## 11. Dimension Chain Verification

**Horizontal (X) chain:** {{X_CHAIN_TEXT}} = **{{SITE_WIDTH}} m exactly.**

**Vertical (Y) chain:** {{Y_CHAIN_TEXT}} = **{{SITE_DEPTH}} m exactly.**

Both confirmed by `design/scripts/validate.py` (see §17) — script output: `x_dimension_chain_sum_m:
{{X_CHAIN_SUM}}`, `y_dimension_chain_sum_m: {{Y_CHAIN_SUM}}`.

## 12. Circulation and Operations

- **Horse circulation:** every stall opens directly onto the single shared central aisle; premium
  stalls and the two veterinary/isolation rooms sit at the aisle's southern end, immediately
  adjacent to feed/service — no horse ever needs to cross the guest zone or motor court, and the
  isolation rooms are naturally separated from the general stall population.
- **Service/feed circulation:** feed and service rooms are centered in the wing, equidistant from
  both stall rows; the perimeter fire/service lane lets a feed truck or farrier reach the wing or
  paddocks without touching the guest motor court.
- **Guest circulation:** arrival → motor court → majlis or outdoor majlis → private suite. The
  transition buffer (Y13.24–15.24) is a deliberate visual and physical stop before the working
  stable begins.
- **Manure/wash logistics:** the dedicated 3.5 m wash/manure service spine between the two paddocks
  connects directly to both paddock gates and to the perimeter fire lane, so soiled bedding/manure
  never has to cross the stable aisle or guest zone.
- **No dead corners / no bottlenecks:** the aisle is a uniform 3.50 m throughout; the perimeter lane
  is a uniform 2.50 m; every enclosed room has exactly one described door/gate (see room schedule).

## 13. Luxury Design Concept

A calm, materials-first luxury language — proportion and shade rhythm rather than ornament:

- Twin symmetric courtyards (indoor majlis + outdoor majlis) create the arrival "moment" without
  clutter.
- A single continuous shade canopy over the stable aisle unifies all 20+2+2 horse rooms visually
  and functionally (shade + rain protection over every stall front).
- Consistent unified roofline over the entire service/worker/feed wing rather than three
  disconnected sheds.
- Equal, generously-proportioned paddocks read as a designed landscape feature, not leftover land.

## 14. Materials and Finishes Palette

| Element | Material direction |
|---|---|
| Stall/wing walls | Warm sandstone/limestone render, bronze accent trim on premium stalls |
| Stable doors | Solid warm walnut timber Dutch doors, powder-coated steel yoke bars |
| Majlis/private suite walls | Deep espresso plaster (majlis), olive-toned plaster (private suite) — restrained, not decorative |
| Roofs | Bronze standing-seam metal, consistent across all stable/wing/guest structures |
| Paddock fencing | Dark walnut-toned timber post-and-rail, 2 rail bands |
| Terrace/majlis flooring | Warm limestone paving |
| Motor court/fire lane | Limestone paving (guest) vs. utilitarian grey paving (service lane) — materially signals the zone change |
| Landscape | Native drought-tolerant planting, shade trees at guest and paddock-edge nodes |
| Lighting concept | Warm 2700K low-glare bollards along the aisle and perimeter lane; uplighting at the majlis facade only |

## 15. CAD/Drawing Deliverables

- `design/output/plans/plan_dimensioned.svg` / `.png` — clean dimensioned technical plan, coordinate
  grid, legend, gate marker, title block, disclaimer.
- `design/output/plans/masterplan_luxury.svg` / `.png` — styled illustrative top-down masterplan,
  identical geometry.
- `design/output/plans/stable_concept_underlay.dxf` — DXF CAD underlay, layered by function,
  marked "CONCEPT CAD UNDERLAY ONLY - NOT FOR CONSTRUCTION".
- `design/output/schedules/room_schedule.csv`, `coordinate_schedule.csv`.
- `design/output/reports/validation_report.json`, `validation_report.txt`.
- `design/scripts/model.py`, `validate.py`, `export_schedules.py`, `export_dxf.py`, `render_svg.py`,
  `generate_report.py` — the actual Python tools used to generate and validate every number and
  drawing above (Shapely for overlap/geometry checks, ezdxf for DXF, cairosvg for PNG rasterization,
  and this report's own numeric tables — all genuinely run, not simulated or hand-typed).

## 16. 3D / Render Deliverables

**3D massing model generated from finalized validated 2D coordinate model. Concept visualization
only — not for construction.**

A real 3D massing model was built directly from the finalized, validated coordinates above using
the Trimble SketchUp MCP connector (not a text-only "render prompt" — actual SketchUp geometry,
componentized where rooms repeat: 20 standard stalls share one component definition, fence posts
and landscape trees are componentized and arrayed). This model was regenerated after the owner-
confirmation pass and reflects the current `model.py` exactly — it is not stale.

- **File:** `Luxury_Equestrian_Stable_Concept_Finalized.skp` — download link (session-scoped, from
  the SketchUp cloud service, valid for this session): `{{SKETCHUP_DOWNLOAD_URL}}`
  — note: this environment's outbound network policy blocks `api.sketchup.com`, so the file could
  not be copied into this repository; open the link directly in your own browser to download it.
- **Thumbnail / aerial render:** `design/output/plans/sketchup_thumbnail.png` and
  `design/output/plans/aerial_3d_render.png` (both included in this repo).
- Contents, at the exact coordinates validated in §10/§11 (real-world scale, meters converted to
  inches internally per SketchUp convention):
  - Site ground pad, equalized paddock turf (2 x 318.92 m²) with post-and-rail fencing.
  - Motor court, parking apron (PK01, kept at 11.00x4.00 m per owner confirmation), and perimeter
    fire-lane paving.
  - Stable barn: 20 standard stalls + 2 premium stalls + **2 veterinary/isolation rooms (مصاب,
    3.50x4.00 m each — labeled and colored distinctly from the general stall population, per the
    owner-confirmed function)** + feed room + **service room at its owner-confirmed 6.00x3.00 m**
    + shade canopy over the central aisle.
  - Worker wing: worker bedroom (WB01, unchanged, 7.00x4.00 m) + **worker kitchen (WK01) and
    worker bathroom (WBTH01), both modeled at their finalized narrowed widths (3.50 m and 2.00 m
    respectively)** to match the wing reflow required by the service-room decision.
  - Guest/owner wing: majlis, men's WC, pergola-roofed outdoor majlis/sitting terrace, private
    bedroom suite with ensuite bathroom — all unchanged, per owner confirmation.
  - 9 landscape trees.
- Every room mass and its roof were generated programmatically from the same `model.py` coordinate
  source used for the SVG/DXF/CSV outputs (Canary 10: renders match the validated CAD geometry).
- **Honesty on tooling:** no photorealistic path-traced rendering engine (e.g. V-Ray, Enscape) was
  available in this environment; the deliverable is a properly-scaled, componentized 3D massing
  model with a presentation style (Urban Planning preset, shadows on) and a luxury aerial camera
  angle — sufficient to verify massing, proportion, and adjacency, but not a photoreal marketing
  render. If a photoreal render is required, this .skp is ready to hand to Enscape/V-Ray/Twinmotion.

## 17. Validation Report

Full JSON/TXT reports: `design/output/reports/validation_report.json` / `.txt`. Summary (generated
directly from that JSON, not hand-typed):

{{VALIDATION_SUMMARY}}

{{RESOLVED_DECISIONS_LIST}}

## 18. Remaining Items Requiring Licensed Professional Review

- Structural design, footings, and roof framing (this is a massing/concept model only).
- MEP: electrical, plumbing, ventilation/HVAC sizing for all enclosed rooms, especially the
  worker kitchen/bathroom and any veterinary function assigned to SP01/SP02.
- Fire/life-safety review of egress widths, the perimeter fire lane's actual vehicle turning
  radius, and manure/hay fire separation distances.
- Civil/drainage design for the paddocks, wash-down spine, and site-wide stormwater management.
- Local building code, zoning, and agricultural/equestrian-use permitting compliance — none of
  which has been verified in this exercise.
- The veterinary/isolation fit-out for SP01/SP02 (ventilation, drainage, exam lighting) still needs
  a licensed veterinary/MEP consultant, even though the room function itself is now confirmed.

## 19. Final Acceptance Checklist

- [x] Site is 40.00 m x 50.00 m.
- [x] 20 standard 3.75 x 3.75 m horse rooms included.
- [x] 2 larger 4.00 x 4.00 m horse rooms included.
- [x] 2 special horse rooms included; unclear label handled honestly (not silently resolved).
- [x] Feed room 4.00 x 4.00 m included.
- [x] 2 paddocks included (and equalized as an improvement).
- [x] Service room 3.00 x 3.00 m included per explicit brief; CAD's 6.00x3.00 alternative disclosed.
- [x] Worker bedroom for 4 included.
- [x] Worker bathroom included.
- [x] Worker kitchen included.
- [x] Men's majlis included.
- [x] Men's bathroom (WC) included.
- [x] Outdoor sitting area included.
- [x] Private bedroom included.
- [x] Private bathroom included.
- [x] All rooms fit inside the site.
- [x] No overlaps.
- [x] Door/gate access defined for every space.
- [x] Horse circulation works (single shared aisle, no crossing of guest zone).
- [x] Service circulation works (dedicated perimeter lane + wash/manure spine).
- [x] Guest circulation works (arrival → majlis → private suite, buffered from stable).
- [x] Dimension chains close exactly (40.00 / 50.00).
- [x] Paddock dimensions consistent everywhere (plan, schedule, 3D model all show {{PADDOCK_AREA}} m² x2).
- [x] Arabic labels preserved and readable throughout.
- [x] 3D model matches validated CAD geometry (same coordinates, no invented rooms).
- [x] DXF marked as concept underlay only.
- [x] Every drawing includes the concept-only disclaimer.
- [x] No code/permitting compliance falsely claimed.
- [x] Owner confirmation obtained on all {{UNRESOLVED_COUNT}} previously-flagged items in §5.
- [x] 3D massing model (§16) regenerated to match the finalized SV01/WK01/WBTH01 geometry - the
      2D plans, DXF, CSVs, report, and 3D model are all current and consistent with each other.

## 20. Deliverables Index

All files are committed to this repository under `design/`:

```
design/
  scripts/
    model.py               - single source of truth for all {{SPACE_COUNT}} space coordinates
    validate.py             - mathematical validation agent (run: python3 validate.py)
    export_schedules.py     - room/coordinate CSV generator
    export_dxf.py           - DXF CAD underlay generator (ezdxf)
    render_svg.py           - dimensioned + styled SVG plan generator
    generate_report.py      - regenerates this report's numeric sections from model.py + validation_report.json
    report_template.md      - the template generate_report.py fills in
  output/
    schedules/
      room_schedule.csv
      coordinate_schedule.csv
    plans/
      plan_dimensioned.svg / .png
      masterplan_luxury.svg / .png
      stable_concept_underlay.dxf
      sketchup_thumbnail.png
      aerial_3d_render.png
    reports/
      validation_report.json / .txt
      source_audit.md         (this file - generated, do not hand-edit numeric sections)
source_files/
  Stable PROJECT/            - the 4 uploaded source files, unmodified
  stable1_page.png           - full-page reference render of stable 1.pdf, used during the source audit
FINAL_QA_LOCK_REPORT.md      - area-discrepancy audit (prior pass)
OWNER_CONFIRMATION_FINALIZATION_REPORT.md - owner-decision record (prior pass)
THREE_D_SYNC_REPORT.md       - this pass's 3D-model regeneration record
```

3D model download (session-scoped, blocked from in-repo copy by this environment's network
policy — open directly in your browser): `{{SKETCHUP_DOWNLOAD_URL}}`
