---
name: scenario-model-comparison
description: "Use when comparing Scenario models on the same brief through MCP: a bake-off with shared prompts and inputs, cost, generation time and quality measured side by side, choosing a default model, testing a new release against the incumbent, or finding which model handles a style, edit, or reference image best. Keywords: model comparison, benchmark, bake-off, A/B test, contact sheet, cost per asset, latency."
license: MIT
---

# Scenario Model Comparison

## Overview

A comparison is one brief run unchanged across several models, then judged on criteria written down before the first paid call. Every candidate has its own contract, so the comparison lives in the normalization: what is held fixed, what each schema forces to differ, and where each number came from. `recommend` shortlists, `dry_run` prices, the `jobs_wait` rows carry the billed cost, the grid tool puts the results side by side, and a table delivers. Connection and the core loop: see the `scenario` skill; a rubric for judging output against a brief: `scenario-refine-loop`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step         | Do                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Frame     | One brief, its inputs (prompt text, reference asset ids), three to five pass/fail criteria, all written before running                            |
| 2. Shortlist | `recommend` with the brief as `prompt` (`limit` up to 10); `search` for candidates the user named; keep three to five                             |
| 3. Normalize | `model_schema_get` each candidate: the shared fields, the caps that differ, the flags that rewrite prompts                                        |
| 4. Price     | `model_run` with `dry_run: true` (top-level, beside `model_id`, never inside `parameters`) per candidate and utility model; apply the Budget gate |
| 5. Run       | `model_run` with top-level `wait: false` per candidate, launched back to back, then one `jobs_wait` over all the job ids                          |
| 6. Measure   | `cuCost` from the `jobs_wait` rows; `createdAt` to `updatedAt` from `job_get` for the seconds                                                     |
| 7. Judge     | The sheet from `model_scenario-grid-maker`, then each asset at full size, scored against the criteria                                             |
| 8. Deliver   | One table row per candidate; the assets filed in one collection and tagged by model id                                                            |

## Normalization

- Hold the brief fixed: the same prompt text byte for byte, the same reference asset ids, the same output count (one, unless every candidate exposes the same batch field; a model whose default sample count is above one multiplies its cost and must be pinned).
- Let the schemas differ only where they must. Sizes are enums or pixel pairs per model: pick the closest each allows to the brief's target and record the delivered `width` and `height` from `asset_get` beside the result, since a larger output costs more and reads sharper. Prompt caps differ (`max_length`): an overrun is a 400, never an implicit trim. Preserve an exact user brief: replace a candidate whose cap is too small, or ask before changing the brief for every candidate.
- Turn off what rewrites the prompt: a prompt-expansion or optimize flag left on for one candidate compares its rewrite, not the brief. Where a flag cannot be turned off, say so in the table.
- Seeds do not compare across models: a seed reproduces one model's own sampling and transfers nothing. Leave `seed` unset, or set it only for repeat runs of the same candidate.
- A Turbo and a Quality member of one family are two candidates, not one. A LoRA runs through its base (`runs_as` and `run_with`, see `scenario`), and its cost and time are the base run's.
- Where one family's skill prescribes tuning (a reference tag syntax, a strength dial), fairness means two rows for that candidate, defaults and tuned, rather than a tuned one against untuned rivals.

## Budget

Price generations and required grid, extraction, or analysis steps. For a hard total cap, count each launched job once, including in-flight commitments. Before the first and every later paid call, require: committed spend + the next call's quote + verified reservations for remaining required work <= the cap. A substitute-input quote cannot verify a reservation unless documented pricing proves it bounds the real payload. If the sheet needs outputs that do not yet exist and has no verified bound, do not launch the generations: propose staged spending or a revised plan and wait for the user's agreement. Do not silently drop requested candidates or artifacts to fit. `usage` reports consumed CU, not remaining credits; it cannot certify a balance for this budget gate.

## Measurement

`recommend` reports modelled cost and latency, right for the shortlist and wrong as a result: `dry_run` prices the exact payload, and the `jobs_wait` row's `cuCost` is what was billed. Time comes from `job_get`, which returns `createdAt` and `updatedAt`; their difference on a finished job is the wall-clock latency including queue time, comparable across candidates launched within the same minute. Launch every candidate before waiting on any, within the team's concurrency ceiling (the 429 rows in `scenario`). Use the returned `actionLimit` on a concurrency 429; never infer the ceiling from this comparison's batch size. Re-call `jobs_wait` with `pending_job_ids` until every row is terminal. Record per candidate: model id, the exact `parameters` sent, `cuCost`, seconds, delivered dimensions, asset ids, and any normalization it forced (a size, a cap, a flag).

Video candidates are compared on contact sheets, never on a first frame: sweep each clip with `model_scenario-video-to-image-seq` (a fixed first-party id, Scenario's single deterministic frame extractor, so discovery would only re-derive it), wait for the extraction job, then sheet the frames per candidate; the extractor's frame-order and stride contract and the sheet's 100-image cap are in `scenario-video-editing`. Audio and 3D candidates are compared on the assets themselves through `asset_display`.

## Judging

Pre-registered criteria are pass/fail statements about the output ("the label text is legible", "the scar is on the left cheek", "no extra fingers", "the background is plain"), so a result is scored, not admired, and a surprising winner cannot rewrite the test after the fact. Score the literal criterion: a related feature or partial match is not a pass; ambiguous evidence is unverified. Build the sheet with `model_scenario-grid-maker` (a fixed first-party id, Scenario's single deterministic grid tool, so discovery would only re-derive it): `images` in candidate order, wrapped as an array even for one, since the array order is the legend (the tool has no labels), `columns` equal to the candidate count so one row is one brief, `cellRatio` matching the outputs, `padding` for a gutter. Then `asset_display` each output at full size: a sheet hides fine text, edge halos and small anatomy. Score every criterion for every candidate, and put cost and seconds in the same table so the trade-off is read in one place. For a large set, `asset_analyze` (catalog, cost-bearing, and write-class: `scenario_tools_search` then `scenario_tool_execute_write`, see `scenario`) can score a batch: the criteria list verbatim as its `instruction`, the outputs as `images`, one verdict per criterion per image, and a criterion the image cannot settle at output resolution (small lettering, a fine edge) recorded as unverified, never as a pass; pre-register that instruction with the criteria.

## Worked example: three image models on one prop brief

1. Frame: "a rusty iron key with a skull-shaped bow, hand-painted style, plain background", a 1024 square, criteria: skull bow present, exactly one key, no lettering, plain background.
2. `recommend` with that brief as `prompt` and `limit: 5`, then `search` with `target="models"`, `public=true` for the two models the user named; keep three. Never hardcode the ids: catalogs differ per team.
3. `model_schema_get` on each: prompt cap, size fields, sample-count field, any prompt-expansion flag.
4. `model_run` with `dry_run: true` (top-level) on each, the same prompt, the count field at one, the closest 1024 square each allows, the expansion flag off; write the three prices down and apply the Budget gate, including the required sheet.
5. `model_run` three times with `wait: false`, then one `jobs_wait` with the three job ids, re-called with `pending_job_ids` on a timeout; read `cuCost` off each row and `createdAt` and `updatedAt` off `job_get` for each job.
6. `model_scenario-grid-maker` with `images` as the three asset ids in candidate order and `columns: 3`; `asset_display` the sheet, then each asset; score the four criteria.
7. Deliver the table (model, parameters that differed, cost, seconds, dimensions, criteria passed, notes) and file the three outputs and the sheet in a collection (`collection_create`, then `collection_add_assets`), tagging each output with its model id through `asset_add_tags`.

## Common mistakes

- Quoting `recommend`'s numbers as results: they are modelled. Bill from `jobs_wait`, time from `job_get`.
- Different sizes or sample counts across candidates, or one candidate's prompt expansion left on: the comparison then measures the payload difference.
- One sample per candidate on a brief whose output varies wildly: run two or three where the budget allows, and say how many in the table.
- Reading a winner as a constant: the ranking is per brief and per team catalog. Re-run when either changes, and never write the winning id into a skill or a pipeline as a fixed value.
- Comparing video by first frame or a single still: sweep the clips into contact sheets.
- Shipping the sheet as the deliverable: the table with costs and criteria is the result; the sheet is evidence.
- Pasting signed download URLs into the report: file the assets and share the asset ids.
