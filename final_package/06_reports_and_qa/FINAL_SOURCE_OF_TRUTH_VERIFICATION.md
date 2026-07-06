# Final Source-of-Truth Verification — Luxury Equestrian Stable Redesign

**Every command below was actually executed this pass, in this order, against a clean checkout of
branch `claude/luxury-stable-redesign-weda7b`. Figures are copy-pasted from real command output, not
recalled from memory.**

## 1. Pipeline execution log

```
python3 design/scripts/validate.py            → OVERALL STATUS: PASS
python3 design/scripts/export_schedules.py    → Site: 40.0 x 50.0 m, 40 spaces scheduled
python3 design/scripts/export_dxf.py          → Wrote stable_concept_underlay.dxf
python3 design/scripts/render_svg.py          → Wrote + rendered plan_dimensioned / masterplan_luxury (svg+png)
python3 design/scripts/render_premium.py      → Wrote + rendered premium_cutaway_masterplan (svg+png)
python3 design/scripts/build_contact_sheet.py → Wrote render_contact_sheet.png (2400x3464)
python3 design/scripts/generate_report.py     → Regenerated source_audit.md: total_area=1648.01 m2 (82.4%), space_count=40, status=PASS
python3 design/scripts/generate_technical_sheets.py → Wrote technical_appendix.pdf
python3 design/scripts/generate_client_presentation.py → Wrote client_presentation.pdf
```

Every step completed with exit code 0, in the exact order specified. No manual out-of-band step is
required any more — `render_svg.py` and `render_premium.py` now call `cairosvg` themselves to
produce their PNGs (previously this was a separate, undocumented manual command; fixed this pass,
see §3).

## 2. Required facts re-verified

| Fact | Required | Actual | Result |
|---|---|---|---|
| Validation status | PASS, 0 failed | PASS, 0 failed (27 passed) | ✅ |
| Site | 40.00 × 50.00 m | 40.0 × 50.0 m | ✅ |
| Total scheduled area | 1,648.01 m² unless model proves otherwise | 1648.01 m² | ✅ |
| Total spaces | 40 | 40 | ✅ |
| Standard stalls | 20 | 20 (`horse_stall`) | ✅ |
| Premium stalls | 2 | 2 (`premium_horse_stall`) | ✅ |
| Veterinary/isolation rooms | 2, مصاب | 2 (`veterinary_isolation_room`) | ✅ |
| SV01 service room | 6.00 × 3.00 m | 6.0 × 3.0 m | ✅ |
| Paddocks | 2, equal | PD01 = PD02 = 318.92 m² | ✅ |
| X dimension chain | 40.00 m | 40.0 m | ✅ |
| Y dimension chain | 50.00 m | 50.0 m | ✅ |
| Resolved owner decisions | 5 | 5 | ✅ |
| Disclosed warnings | 1 (WK01/WBTH01 narrowing) | 1 | ✅ |

## 3. Real defect found and fixed during this re-run: non-deterministic render seed

While re-running the pipeline, `render_premium.py` was run twice in a row and its SVG output was
diffed — **it was not byte-identical between runs**. Root cause: the paddock sand-texture function
was seeded with `hash(s["id"]) % 1000`, and Python's built-in `hash()` for strings is randomized
per-process by default (`PYTHONHASHSEED` randomization, on since Python 3.3) unless explicitly
disabled. This means every regeneration of the premium cutaway silently produced a different sand
texture — a genuine reproducibility defect that contradicts this project's repeated claim of being
"fully deterministic, generated directly from model.py, zero hallucination risk."

**Fix applied:** `design/scripts/render_premium.py` now seeds with `zlib.crc32(s["id"].encode()) %
1000` — a fixed, deterministic hash — instead of Python's randomized `hash()`. Verified by running
the script twice in separate processes and diffing the output SVG byte-for-byte: **identical**. This
is now a genuinely reproducible generator, matching what every report has claimed of it.

## 4. Also fixed this pass: PNG rendering folded into the generator scripts

Previously, `render_svg.py` and `render_premium.py` only wrote `.svg` files; the corresponding `.png`
files were produced by a separate, manual `cairosvg` command that existed only in this assistant's
own shell history, not in any committed script. This meant the documented pipeline (`python3
render_svg.py`) did not actually reproduce every committed deliverable. **Fixed:** both scripts now
call `cairosvg.svg2png(...)` themselves at the end of their `main` flow, so running the script alone
regenerates both the `.svg` and its `.png` — the pipeline is now genuinely self-contained.

## 5. Cross-file consistency after regeneration

- `room_schedule.csv` (sum of all 40 `area_m2` values) = **1648.01** — matches `validation_report.json`.
- `source_audit.md` §9 total = **1648.01 m² (82.4%)** — matches.
- `technical_appendix.pdf` Sheet 02 and Sheet 04 totals = **1648.01** — matches (re-verified visually,
  see `PDF_VISUAL_QA_REPORT.md`).
- `client_presentation.pdf` Section 13 total = **1648.01** — matches.
- All five independently trace back to the same live read of `model.py`; none are hand-typed.

## 6. `final_package/` sync status after this pass's fixes

Comparing `design/output/` (freshly regenerated) against the existing `final_package/` copies, the
following files now legitimately differ (all for good reason — either this pass's determinism fix,
the §16 rewording, or routine PDF/DXF generation timestamps) and are re-copied in Phase 5 of this
pass:

- `premium_cutaway_masterplan.svg` / `.png` — content changed by the determinism fix (§3).
- `render_contact_sheet.png` — rebuilt from the corrected premium image.
- `client_presentation.pdf`, `technical_appendix.pdf` — regenerated (embed the corrected image;
  reportlab also stamps a fresh creation timestamp in PDF metadata, which is cosmetic and expected).
- `stable_concept_underlay.dxf` — `ezdxf` regenerates internal `$TDCREATE`/GUID metadata on every
  run (documented behavior, confirmed in `THREE_D_SYNC_REPORT.md` from a prior pass); geometry itself
  is unchanged.
- `source_audit.md` — content changed by the §16 dead-link fix (see `FINAL_REPO_PRODUCTION_REVIEW.md`
  §3.2).

Everything else (`room_schedule.csv`, `coordinate_schedule.csv`, `validation_report.json`,
`plan_dimensioned.svg`, `masterplan_luxury.svg`) is byte-identical between `design/output/` and
`final_package/`, confirming no drift where none was expected.

## 7. Conclusion

The source-of-truth pipeline is confirmed intact, and is now strictly more correct than before this
pass: it produces byte-reproducible output and no longer depends on an undocumented manual step. All
required facts match exactly. `final_package/` is refreshed in Phase 5 to absorb the legitimate
changes listed in §6.
