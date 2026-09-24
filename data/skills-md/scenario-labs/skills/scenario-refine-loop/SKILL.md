---
name: scenario-refine-loop
description: "Use when a Scenario output must be checked and improved rather than accepted first roll: iterating a generation until it matches the brief, fixing a batch that came back off-brief, retrying failed shots methodically, wiring an automated generate, review, revise loop, or deciding whether to re-prompt, swap references, inpaint, post-process, or change model. Keywords: refine, iterate, critique, review loop, QA, self-correction, verify, acceptance criteria, retry, drift."
license: MIT
---

# Scenario Refine Loop

## Overview

Agents fail generation QA in two symmetric ways: accepting the first roll, or rewording the whole prompt and re-rolling until the budget dies. Both skip the same two artifacts, a written rubric and a diagnosis. The loop that converges: rubric before generating, a small batch, a recorded verdict per asset, the cheapest targeted fix per failure, a hard round cap. Connection and the core loop: see the `scenario` skill. Critic tool contracts: `scenario-asset-analysis`. Baseline discipline: `scenario-consistency`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step        | Do                                                                                                                                                                           |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Rubric   | Before generating, turn the brief into pass/fail lines a viewer can check ("subject centered on a plain field"), never taste words                                           |
| 2. Generate | The smallest batch that tests the recipe, at the cheapest size or quality tier the schema offers on which every rubric line can still be judged; `dry_run` when cost matters |
| 3. Critique | `asset_analyze`: up to 10 images per call, one instruction embedding the rubric and a fixed per-image output shape                                                           |
| 4. Fix      | Route every fail line to the cheapest fix that addresses it (table below)                                                                                                    |
| 5. Stop     | A clean round ships; three rounds without one, or one line failing twice under different fixes, means report, not respin                                                     |

A tier change is a new generation, not the keeper enlarged: re-run only the keeper's recipe at delivery tier and re-critique it, or keep what passed and upscale it with a fidelity upscaler found by `search` `target="models"`, `filters={"tags": ["image-upscale"]}`, `public=true` (fidelity versus creative picks and sizing in `scenario-image-editing`, video upscaling in `scenario-video`).

When the bar is the configured brand brief rather than a task rubric, and the team's Quality Gate add-on is enabled, critique images with `asset_quality_gate_run` instead: its `reasons` and `suggestions` feed the fix table directly (`scenario-quality-gate`; where the gate is missing it degrades to this `asset_analyze` path).

Fix routing, cheapest first:

| The verdict says                                | Fix                                                                                                                                                                          |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One local defect on a keeper                    | Masked inpaint of that region; on a schema with no `mask` field, an instruction edit of the keeper naming that one change (`scenario-image`)                                 |
| A uniform finish off (grade, tint, crop)        | A deterministic tool pass (`scenario-image-editing`), not a re-roll                                                                                                          |
| Wrong content, composition, or rendered palette | Edit the delta clause, re-run from the approved baseline                                                                                                                     |
| Identity or style drift                         | Tighten the enumeration, add or re-role references (`scenario-consistency`)                                                                                                  |
| Every line failing                              | Change the model: re-discover with `recommend` (capability-shaped; `search` is for a name, a private model, or a tag-filtered lane such as `image-upscale`), keep the prompt |

Change one variable per round. A round that swaps prompt, references, and model at once cannot attribute the improvement, so the next failure restarts from zero.

## The two rules that keep the loop honest

- **Verdicts cite the rubric, not taste.** Instruct the critic to answer per image, in order: `<index>: pass|fail, <the failed line>`. "Could be better" is not a verdict; a loop chasing better instead of the brief sands off exactly what made the direction distinctive and converges on generic output.
- **Regenerate from the baseline, never from the last attempt.** Fixes re-run from the approved reference and prompt; chaining output to output compounds drift (`scenario-consistency` explains why).

## Worked example: four icons against a brief

1. Rubric from the brief, five lines: single object, centered, plain field, palette #2A9D8F and #E9C46A only, no text.
2. Generate four, one `model_run` each per `scenario-image`, then `jobs_wait`.
3. One `asset_analyze` call with all four ids in `images` and the rubric-plus-shape instruction; answers land as text assets, `asset_download` them to read the verdicts.
4. Two fail. Icon 2 is off palette, which is rendered content rather than a finish: edit the delta clause by pinning the hex codes in the prompt and re-run from the baseline. Icon 4 has one smeared edge: masked inpaint of that corner. Icons 1 and 3 ship untouched.
5. `jobs_wait` the fix runs, then re-critique only the two new assets with the byte-identical instruction. Clean round: stop, file the keepers in a collection (`scenario-asset-analysis`).

## Common mistakes

- Judging by glancing at `asset_display` in chat: unrecorded impressions do not accumulate; verdicts do.
- Asking `asset_analyze` to improve or fix the image: it returns text only; every fix is a new run.
- Re-rolling the whole batch because one item failed: route per item.
- Writing the rubric after seeing the batch: it inherits the batch's flaws as the standard.
- Running the loop uncapped: failed jobs are reimbursed, unsatisfying ones are not. Gate rounds on the costs the runs themselves report (`dry_run` prices the next round ahead); `usage` totals lag and answer the report after the run, not the mid-run gate.
- Retrying a criterion a third time on the same model: two misses under two different fixes is evidence about the model, not bad luck.
