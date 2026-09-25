---
name: scenario-quality-gate
description: "Use when a generated Scenario image needs a quality check or a brand-brief compliance verdict before it ships: pass/warn/fail scoring, on-brand review against a configured brief, QA gating a batch, pricing or refreshing a stored verdict, or iterating a generation until it clears the gate. Keywords: quality gate, quality check, QA, verdict, brief compliance, on-brand, brand brief, pass fail, score, review, asset_quality_gate_run."
license: MIT
---

# Scenario Quality Gate

## Overview

One tool, `asset_quality_gate_run`, scores a finished image asset and returns a `pass`/`warn`/`fail` verdict with 0 to 100 scores and per-dimension lists of `reasons` and `suggestions`: an AI-quality check always, plus brand-brief compliance when the team or project has a brief configured. Image assets only. Quality Gate is an Enterprise add-on: when it is not enabled for the team the call fails cleanly, so detect that, fall back to an `asset_analyze` review (see `scenario-asset-analysis`), and say so. Retrying never clears it.

The tool is catalog-only and write-class: get the schema with `scenario_tools_search`, then run it through `scenario_tool_execute_write` with `{name: "asset_quality_gate_run", parameters: {...}}`, scope ids inside `parameters` (the read executor rejects it by lane and names the right one). Or reconnect with `?toolsets=full`. Connection and scope: see the `scenario` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference: what a call costs

| Call                              | What happens                                                             | Cost                                                                       |
| --------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Plain call, usable verdict stored | Returns the stored verdict, `source: "stored"`                           | Free (the response carries no `creativeUnitsCost`)                         |
| Plain call, no usable verdict     | Runs a new analysis and stores the verdict, `source: "new_analysis"`     | Billed; the response carries `creativeUnitsCost` (1 CU as of this writing) |
| `rerun: true`                     | New analysis that replaces the stored verdict                            | Billed                                                                     |
| `dry_run: true`                   | Nothing runs; returns the price of a new analysis as `creativeUnitsCost` | Free                                                                       |

A plain call is a read only when a usable verdict already exists; otherwise the same call silently escalates to the billed analysis. "No usable verdict" covers both never-scored and a stored `error` result. When spend needs approval first, probe free: `dry_run: true`, or `asset_get`, whose `qualityGate` field carries the verdict and scores when one is stored (summary only; the stored `reasons` and `suggestions` come back through the tool, still free). `sensitivity` (`low`, `medium`, `high`; default is the team or project setting) shapes new analyses only and is ignored on stored reads. `rerun: true` is for after the brief or the sensitivity changed, nothing else: it re-bills and overwrites.

## Reading the verdict

The response is `source` plus `quality_gate`: `verdict`, `overallScore`, `aiQualityScore`, `briefComplianceScore`, `sensitivity`, `appliedBriefIds`, and `details`. With no brief configured the compliance dimension is absent entirely (`appliedBriefIds: []`, `overallScore` equals `aiQualityScore`); with one, `details.briefCompliance` sits beside `details.aiQuality`, each carrying a `score` and lists of `reasons` and `suggestions`, usually several of each.

## Turning the verdict into a better image

A verdict alone only sorts assets. The gate earns its cost when the feedback drives the next attempt:

- `reasons` name concrete flaws ("elongated finger anatomy on the left hand", "background gradient off the brief's palette"). Use them to pick the fix path per flaw: a local defect on an otherwise approved image is a masked inpainting pass (`scenario-image`); a global one is a regeneration.
- `suggestions` are written as edit instructions, often worded for manual retouching. Apply all that fit, not just the first: translate them into the next `model_run` prompt or parameters, or into the edit instruction.
- A regenerated image is a new asset, so a plain call scores it. `rerun` is never part of the loop. It may even come back pre-scored for free: teams with auto-detect enabled (`qualityGateAutoDetect: true` on their `teams_list` row) score new generations automatically.
- When a round repeats the same flaw classes at an unmoved score, rewording will not fix them: switch models (`recommend` again) or repair the flaw with a masked edit before spending another round.
- Fix the exit bar and a round cap up front: `verdict: "pass"` by default, or a score target the user names (`overallScore` at or above 90, say; the named bar then outranks a bare `pass`), and three rounds unless told otherwise, since every round bills a generation plus an analysis. At the cap, or when a round stops moving the scores, stop: report the best asset with its remaining flaws and ask before spending more rounds; unattended, deliver that best asset and flag the miss.

`scenario-refine-loop` carries the loop discipline beyond the gate: one variable per round, regeneration from the approved baseline, and fix routing when the criteria go past the brief.

## What the verdict does not cover

The gate is an artifact detector. Measured on real assets, three limits to design around:

- **Artifacts, not plausibility.** A panel whose car carried two different wheels, a whitewall on one only, and no wheel arch above the rear tire scored 92 and `pass` at `sensitivity: "high"`, with `reasons` praising the chrome rims that were the defect. What is impossible rather than ugly needs a structural check of your own: counts and attachment (hands, fingers per hand, limbs, wheels, each attached to one body), part to whole (a wheel sits inside an arch, a guard sits on its own blade, a reflection sits under what casts it), and what carries the weight.
- **It has never seen your reference.** `briefCompliance` needs a configured brief, and a brief is text, so no call can tell you this is not the same car or costume as the plate it was generated from. Compare the asset against its reference yourself, item by item.
- **A composite averages its parts.** A 12-panel storyboard scored 88 and `pass` while one of its panels was physically impossible. Score the unit you are willing to reject: split a composite with `model_scenario-image-slicer`, score each part, repair only the failures, and recompose with `model_scenario-compose-image`.

The score is also a weak signal that a structural repair landed: a broken panel and its corrected replacement both scored 92, and only the `reasons` changed. Re-read the flaw list, do not watch the number.

## Worked example: iterate a hero prop to pass

1. Generate per `scenario-image`: `model_run`, `jobs_wait`, collect the asset id.
2. `scenario_tools_search` with `query="quality gate"` once for the schema, then `dry_run: true` on the first asset to surface the per-analysis price.
3. Score: `scenario_tool_execute_write` with `{name: "asset_quality_gate_run", parameters: {asset_id, team_id, project_id}}`. It returns `source: "new_analysis"` and a `quality_gate` carrying `verdict: "warn"`, `briefComplianceScore: 58`, and `details.briefCompliance.suggestions` asking for the logo at the top left and a flatter background.
4. Fold both suggestions into the prompt, regenerate, and score the new asset with a plain call (no `rerun`).
5. `verdict: "pass"`: deliver, and file it (collections and tags per `scenario-asset-analysis`). Later reads of any scored asset are free stored reads.
6. The brief changes next sprint: only then `rerun: true` on the assets that must be re-judged.

## Common mistakes

- Treating a plain call as a free read: without a usable stored verdict it silently runs and bills the analysis. Probe with `dry_run` or `asset_get` first when the spend matters.
- Passing `rerun: true` out of habit: it re-bills verdicts that were free to read. Its one job is refreshing after the brief or sensitivity changed.
- Expecting `briefComplianceScore` with no brief configured: `quality_gate` carries it and `details.briefCompliance` only when `appliedBriefIds` is non-empty.
- Applying one suggestion and rescoring each time: the lists usually carry several fixes, and one regeneration can absorb them all.
- Running it through `scenario_tool_execute_read`: write-class, rejected by lane.
- Scoring a video, 3D, or audio asset: image assets only.
- Assuming a fresh upload has no verdict: uploads deduplicate by content, so identical bytes return the same long-lived asset id whatever the filename, and a re-upload of a file the team scored before carries its stored verdict.
- Setting `sensitivity` on a call that returns a stored verdict: it applies to new analyses only; stricter scoring of an already-scored asset requires `rerun: true`.
- Retrying the entitlement failure: Quality Gate is an Enterprise add-on. Degrade to the `asset_analyze` review in `scenario-asset-analysis` and tell the user why.
