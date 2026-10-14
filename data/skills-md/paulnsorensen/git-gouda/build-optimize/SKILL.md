---
license: MIT
name: build-optimize
description: Optimize local build, test, and check commands with measured wall-time evidence. Use for "speed up my build", "why is just check slow", or /build-optimize. Route GitHub Actions work to /ci-optimize.
---

# Local build optimization

Measure local wall time before changing. Preserve checks, artifacts, and failure behavior.

This skill covers local cargo, pytest, npm, pnpm, go, and just commands.
Use /ci-optimize for GitHub Actions workflow timing or changes.

## Discipline

**Iron Law:** Measure the approved run plan before proposing a concrete edit.

**Red Flags** — stop when you notice these:

1. An edit removes a check or artifact, changes the workload, or hides a failure.
2. Cache operations, sample counts, warmups, or isolation differ from the approved plan.
3. Cold and warm cohorts merge, or a blocked helper comparison becomes a speed claim.

| Rationalization | Why it fails | Required action |
| --- | --- | --- |
| "The warm run is faster, so every build is faster." | A warm run skips cold-cache work. | Report each cohort separately. |
| "Parallel tests are faster." | Parallel workers require test isolation. | Prove isolation before the plan. |
| "The helper is absent, so raw timings are enough." | Raw timings cannot pass the comparison gate. | Keep raw evidence and report comparison blocked. |

## References

Read methodology before defining the run plan.
Read the matching ecosystem reference before defining the run plan.
Read sibling local.md before capturing local timing.
Read sibling schemas.md before constructing normalized inputs.

- Ecosystem: [rust.md](references/rust.md), [python.md](references/python.md), [js-ts.md](references/js-ts.md), [go.md](references/go.md).
- Timing: [methodology.md](references/methodology.md).
- Sibling adapters: `local.md` and `schemas.md` in the ci-optimize skill's references directory.

## Workflow

1. Read repository instructions. Identify the authoritative local command.
2. Define a run plan with the exact command, warmup and sample counts, cache operations, isolation, output paths, and cost.
3. Obtain explicit approval for the run plan.
4. Measure baseline with the approved cache cohort(s).
5. Report baseline evidence.
6. Propose affected files, a benefit hypothesis, risks, verification, and any established rollback.
7. Wait for explicit edit-plan approval before changing tracked source.
8. Apply the approved change through the repository's existing edit path.
9. Re-measure the same protocol. Verify all checks, artifacts, and failure behavior.
10. Stop after the report or when required input is missing.

## Commands

Resolve `CI_OPTIMIZE_HELPER` from the actual loaded `SKILL.md` directory.
Resolve symlinks before appending `../ci-optimize/scripts/ci_optimize.py`.
Never derive the helper path from the consumer repository's current directory.
The helper does not execute commands, edit source, install dependencies, or commit changes.

Run commands from the consumer repository's working directory:

```text
python3 "$CI_OPTIMIZE_HELPER" from-hyperfine --input BEFORE-RAW.json --command 'COMMAND' --revision REVISION --environment ENV --cache-state STATE --workload-label LABEL --output BEFORE.json
python3 "$CI_OPTIMIZE_HELPER" from-hyperfine --input AFTER-RAW.json --command 'COMMAND' --revision REVISION --environment ENV --cache-state STATE --workload-label LABEL --output AFTER.json
python3 "$CI_OPTIMIZE_HELPER" compare --before BEFORE.json --after AFTER.json --minimum-samples N --output COMPARISON.json
```

Run this sequence separately for approved cache cohorts with distinct output paths.
Use `--force` only to replace an existing explicit output file.
Keep raw evidence when the sibling helper is absent.
Report comparison blocked when the helper is absent.
Do not install a helper or waive the comparison gate.

## Evidence and report

Read `COMPARISON.json`. Require `comparability: true`.
Report status, command boundary, eligible and excluded counts, medians and range, delta, checks, artifacts, limitations, next approval, and evidence paths.
Preserve every excluded sample and its reason.
Record approved context differences in acknowledgements.
Acknowledgements cannot waive workload or validation mismatches or prove equivalent coverage.
Describe observations without promising numeric gains. Return no more than 200 words.
Do not rename unrelated gates, add auto-fix checks, or change CI workflows.
