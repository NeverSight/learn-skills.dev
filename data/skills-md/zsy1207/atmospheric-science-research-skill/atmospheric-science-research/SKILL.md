---
name: atmospheric-science-research
description: >-
  Use this skill for file-based atmospheric or climate work with a real
  project structure rather than a one-off answer. Trigger it for NetCDF, GRIB,
  reanalysis, ERA5, CMIP, WRF, model output, EOF or PCA, climatology,
  anomaly, regression, composite, or other atmospheric diagnostics when the
  task involves planning, diagnostics or statistics, regridding, reusable
  computation, compute-vs-plot separation, publication-grade figures, or
  review of actual outputs. Also use it for existing atmospheric figure files
  or small figure-only patches inside an existing atmospheric or climate
  project when labels, levels, colorbars, legends, panel letters, layout, or
  exports need fixing without changing the scientific method. Do not use it
  for forecasts, literature summaries, pure writing, generic plotting outside
  atmospheric science, app or UI work, deployment, or simple one-step
  downloads.
---

# Atmospheric Science Research

Keep the control plane small: choose one mode, load only the needed references, and keep compute separate from plotting.

## Goal
Create a scientifically rigorous, visually appealing, and informative figure suitable for publication in a top-tier atmospheric science journal.

## Modes

- `Full`: `Plan -> Execute -> RR`
- `Execute-lite`: `Execute -> RR`
- `RR-only`: `RR`

Choose a mode first:
- use `Full` for a new project, new dataset, new processing method, or any task that may change the scientific conclusion
- use `Execute-lite` for a constrained patch to labels, ticks, units, legends, panel letters, colors, levels, spacing, filenames, or export settings; rerender the affected outputs, then continue into `RR`
- use `RR-only` when the task is to inspect or revise existing figure outputs; stay in `RR` until the result is `PASS` or `BLOCKED`
- if the science-change boundary is unclear after a light inspection, use `Full`

## Reference loader

Load only what the current step needs:
- [references/plan.md](references/plan.md): project planning and the optional single clarification stop
- [references/compute-acceleration.md](references/compute-acceleration.md): heavy compute, diagnostics, and reusable outputs
- [references/plot-standards.md](references/plot-standards.md): figure rendering, layout, export, and rejection checks
- [references/review.md](references/review.md): `RR` loop, outcomes, and minimum-patch revision scope
- [references/readme-template.md](references/readme-template.md): plan, delivery, and patch-update `README.md`

Do not load every reference file up front.

## 1. Project structure

- Use `data_processed/` and `figN/` only when the project has no established layout.
- Save reusable derived results in the project's processed-data location when one exists; otherwise use `data_processed/`.
- Keep figure work near the existing figure layout when one exists; otherwise use `figN/`.

## 2. Plan

For the `Plan` step:
- load [references/plan.md](references/plan.md)
- load [references/readme-template.md](references/readme-template.md)
- inspect the data only enough to design the work
- stop and ask the user if a scientific ambiguity remains
- write or update a short Chinese `README.md` aligned with the actual project structure


## 3. Execute

For all computation work:
- load [references/compute-acceleration.md](references/compute-acceleration.md)

For all figure work:
- load [references/plot-standards.md](references/plot-standards.md)

If subagents are available and the work can be split cleanly, divide it into compute and plot responsibilities:
- `compute agent`: ingest data, preprocess, run diagnostics, and save reusable outputs
- `plot agent`: read prepared outputs, render figures, and apply plotting standards
- integrate their outputs through reusable intermediates

If subagents are unavailable, keep the same split in separate modules or scripts.

Execution rules:
- choose the smallest workflow and the simplest defensible implementation that fully answers the scientific task
- keep heavy computation out of plotting scripts
- use the minimum code that solves the problem
- never recompute heavy diagnostics when only figure styling changed
- save reusable intermediate results once, then reuse them
- when modifying an existing project, touch only the files, comments, and formatting needed for the task; match the local style
- for `Execute-lite`, keep the patch and rerender scope to the minimum relevant code and affected outputs
- when no project structure exists, organize files using this default structure, using `fig1/` as the local example:
  - processed data in `data_processed/*.nc`
  - plotting scripts in `fig1/plot_*.py`
  - optional preprocessing or intermediate computation scripts in `fig1/compute_*.py`
  - figure outputs in `fig1/fig1_*.png` and `fig1/fig1_*.svg`

## 4. RR (`review & revision`)

For the `RR` step:
- load [references/review.md](references/review.md)
- load [references/plot-standards.md](references/plot-standards.md)
- open and review the actual output `PNG`, not only the code
- if a figure fails plotting standards or obvious physical-sense checks, patch the minimum relevant code
- repeat until the result is `PASS` or `BLOCKED`

## 5. README follow-through

Use one `README.md` across the project:
- in `Full`, write the plan version after data inspection and before execution. in `Execute-lite` or `RR-only`, keep the existing `README.md` and update it at final handoff only when paths, outputs, or the image summary changed
- update the delivery version at final handoff
- keep the README path section aligned with the actual project directories and outputs
- for later modifications, append only the new version notes and image summary

## 6. Web and uncertainty rule

Use search only after checking the local code, docs, and project notes when formulas, methods, or package usage remain unclear, or when debugging stalls without enough local evidence.

Just stop and ask the user when the uncertainty and ambiguity remains.

## 7. Keep the control plane minimal

Do not force the full flow for a tiny patch.
Do not load every reference file up front.
Do not create extra `QC`, `gate`, `audit`, or planning documents.
Do not rewrite working compute code for a figure-only issue.
