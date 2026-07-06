# Internal QA Notes (not part of the client deliverable)

This `99_INTERNAL_QA/` folder holds internal quality-assurance material. It is **not** intended for
the client and is excluded from the client-facing folders (`00`–`07`).

## Contents

- **`repo_review.md`** — the honest owner-rejection review that triggered this rescue pass (what
  failed, what was removed, what was rebuilt).
- **`final_qa_report.md`** — the final owner-acceptance QA gate for this package.

## Where the rest of the internal history lives

The full internal engineering/process history (earlier pass reports: current-state review, quality
gap analysis, source-of-truth lock, 3D-sync report, owner-confirmation record, prior QA reports,
render notes) remains in the **repository root**, not in this client package, to keep the delivery
clean. See the repository `git log` for the complete provenance trail.

## On the removed 3D renders

The earlier flat software-massing renders (`design/output/plans/renders_3d/`,
`aerial_3d_render.png`, `sketchup_thumbnail.png`) are **not** included anywhere in this package.
They remain in the working `design/output/` tree only as an internal geometry-massing check. They
were correctly rejected as not meeting a luxury client standard; photoreal renders are to be
produced externally per `06_CONSULTANT_HANDOFF/render_production_brief.md`.
