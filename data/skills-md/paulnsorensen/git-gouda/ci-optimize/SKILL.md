---
license: MIT
name: ci-optimize
description: Optimize GitHub Actions workflow wait time with measured evidence. Use for "speed up CI", "why is GitHub Actions slow", workflow comparisons, or /ci-optimize. Route local command timing to /build-optimize.
---

# CI optimization

Measure GitHub Actions wait time before changing. Preserve required checks, artifacts, and failure behavior.

## Discipline

**Iron Law:** Capture the baseline before proposing a concrete edit.

Explicit authorization is required before destructive cleanup, paid infrastructure, dependency installation, source edits, or remote dispatch.

**Red Flags** — stop when you notice these:

- A check, artifact, workload, or failure path is removed to create a speed result.
- A rerun, partial job page, or changed validation contract enters the primary cohort.
- A local result or zero exit status replaces a CI comparison.

| Rationalization | Why it fails | Required action |
| --- | --- | --- |
| "The cache change is obvious, so I can apply it now." | Measurement does not approve mutation. | Present the plan and wait. |
| "Parallel jobs add their durations." | The metric ends at the latest selected completion. | Measure from run creation. |
| "The rerun uses the same workflow, so it is comparable." | Schema version 1 excludes reruns from primary wait. | Keep reruns as diagnostics. |

## Workflow

1. Read repository instructions. Identify authoritative verification commands.
2. Select one workflow, event class, workload, validation contract, and selected job set.
3. Read [references/github.md](references/github.md) before capturing runs. Read [references/schemas.md](references/schemas.md) before constructing inputs.
4. Capture baseline initial attempts and every selected attempt-specific jobs page.
5. Capture the planned sample count plus headroom for exclusions. Normalize the baseline.
6. Inspect eligible and excluded observations.
7. For a mixed request, read [references/local.md](references/local.md) before defining local timing. Define a local run plan. Name the exact command, warmup and sample counts, cache operations, isolation, output paths, and cost.
8. For a mixed request, obtain explicit approval for the local run plan.
9. Present one concrete edit plan.
10. Name affected files, expected benefit, risks, verification, and any established rollback.
11. Obtain explicit edit-plan approval before any tracked-source edit, dispatch, or remote mutation.
12. Apply the approved change through existing implementation and verification workflows.
13. Repeat the complete CI capture with the same boundary. Include queue and startup delay.
14. Normalize the after dataset. Compare datasets with an explicit minimum sample count.
15. Read comparison JSON. Require `comparability: true`.
16. Verify required checks, coverage, artifacts, and failure behavior.
17. Report observations without promising a numeric gain. Stop after the report or when required input is missing.

Skip only local timing for a CI-only request. Local timing cannot establish CI wait improvement. Keep cache cohorts separate.

Acknowledgements record approved environment, cache-state, or local-command differences.
They cannot waive workload, validation, identity, or equivalent-coverage mismatches.
They do not prove causation or authorize edits.

## Commands

Resolve `CI_OPTIMIZE_HELPER` from the actual loaded `SKILL.md` directory.
Resolve symlinks before using `scripts/ci_optimize.py`.
Never derive the helper path from the consumer repository's current directory.
The helper does not execute commands, edit workflows, install dependencies, dispatch runs, or commit changes.

Run commands from the consumer repository's working directory:

```text
python3 "$CI_OPTIMIZE_HELPER" ci --input BEFORE-CAPTURES.json --output BEFORE.json
python3 "$CI_OPTIMIZE_HELPER" ci --input AFTER-CAPTURES.json --output AFTER.json
python3 "$CI_OPTIMIZE_HELPER" compare --before BEFORE.json --after AFTER.json --minimum-samples N --output COMPARISON.json
```

Run this sequence separately for approved cache cohorts with distinct output paths.
Use `--force` only to replace an existing explicit output file.
Run `python3 "$CI_OPTIMIZE_HELPER" --self-test` to check that excluded runs do not change the job set.

## Evidence and report

The CI metric spans run creation to the latest selected job completion.
Use initial attempts only for the primary cohort. Do not sum parallel job durations.
Report status, workflow and selected-job boundary, eligible and excluded counts, medians and range, and delta.
Report checks, artifacts, limitations, next approval, and evidence paths.
Preserve excluded observations and their reasons.
Return no more than 200 words.
Do not rename unrelated gates, add auto-fix checks, or change local build behavior.
