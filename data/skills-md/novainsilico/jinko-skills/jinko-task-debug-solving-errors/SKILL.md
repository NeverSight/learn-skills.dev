---
name: jinko-task-debug-solving-errors
description: >-
  Investigate slow Jinkō solves, solver timeouts, non-finite ODE errors, and
  trial failures limited to some patients or arms. Collect pinned diagnostic
  evidence, compare controlled numerical experiments, and check candidate
  repairs. Use when simple_solve fails or takes at least 15 seconds, or a
  trial reports solving errors. A slow request is a triage signal, not proof
  of a model defect.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.17,<2.0"
license: MIT
---

# Debug solving errors

Find the failure mechanism and validate a repair against the original scenarios.
Use `jinko-model` for model edits and `jinko-trial` for trial mechanics. Preserve
source revisions and perform experiments on copies within the authorized scope.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and
> an SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup`
> skill (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes.
> Use `JINKO_API_KEY` when it is set. Otherwise, obtain a fresh session code
> before this skill's SDK process, as instructed by the setup skill.
> Also check that `python -m jinko.cli.debug_solving --help` works. If the
> command is missing, upgrade `jinko-sdk`. Do not replace the command with
> private transport calls.

## Collect before changing

Run the deterministic diagnostic command into a new directory. It does not edit
items or start trials. A model solve requires `--run-simple-solve` explicitly.

```bash
python -m jinko.cli.debug_solving --model-sid cm-... --out debug/model
python -m jinko.cli.debug_solving --trial-sid tr-... --revision 2 \
  --telemetry --out debug/trial
```

For one authorized model probe, select representative outputs and preserve exact
formula overrides in a JSON object. The command uses at most ten output slots.
Available telemetry fills remaining slots; absent metrics are reported as such.

```bash
python -m jinko.cli.debug_solving --model-sid cm-... --revision 4 \
  --run-simple-solve --timeseries-id Time --timeseries-id Drug \
  --overrides-json case.json --telemetry --out debug/probe
```

Use `--patient-id` to retain an exact patient row from the bound population;
this reads the population. The bundle also records the bound protocol and trial
options. Reconstruct the scenario from all three. Do not assume the model head,
its default settings, or a bare patient row represents the failed trial arm.
`--arm-id` limits telemetry downloads, not the original failure inventory.

Read `report.json` and collection errors before interpreting the bundle. Exit
codes are 0 for successful collection without detected failure, 1 for a reported
model/solve/patient failure, and 2 for incomplete collection or invalid input.
Neither exit 0 nor finite outputs establish numerical or scientific validity.

## Choose the investigation

- **Slow or timed out:** separate client wall time, solver time, compilation,
  and incomplete evidence. Treat at least 15 seconds as a configurable signal.
  Inspect the solver, tolerances, state scales, maximum step, and auxiliary
  events before choosing a bounded experiment.
- **Patient/arm subset:** group raw errors by patient and arm, compare exact
  inputs with a successful control, and retain the full failure set. Shared
  derivative names can conceal different upstream causes.
- **Non-finite derivative:** trace upstream expressions, including division,
  logarithms, roots, fractional powers, and switched branches. The reported
  derivative is not necessarily the first invalid expression. The reported
  last solved time may be an earlier output point.
- **Setup or export error:** inspect trial-context sanity, formulaic descriptor
  overrides, unit mode, and event schedule. Keep unit/conversion defects separate
  from runtime defects. For failed exports, preserve the error and use native
  JSON plus options when supported.

Read [investigation guidance](references/investigation.md) for telemetry meaning,
controlled solver experiments, and independent replication after a full timeout.

## Verify and report

Change one cause at a time. Compare the original failing case, a successful
control, and then all original subjects and arms. Check finite trajectories,
physiological constraints, event behavior, and numerical sensitivity. Halve the
maximum step or tighten tolerances for a justified comparison; do not call an
unconverged candidate validated merely because every subject completes.

Report evidence, hypotheses, copy-level changes, remaining failures, and open
scientific questions separately. Record pins, settings, override warnings,
metrics, and comparison tolerances. Never silently drop failing patients, loosen
accuracy to obtain completion, or apply a model-specific clamp to other models.
