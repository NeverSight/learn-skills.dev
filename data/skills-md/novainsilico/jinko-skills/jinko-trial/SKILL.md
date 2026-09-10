---
name: jinko-trial
description: >-
  Create, sanity-check, run, poll, and download results for Jinkō in-silico trials via the jinko-sdk. Use this skill whenever the user wants to set up a trial from a computational model and simple output set, optionally attach a vpop, protocol, data table, or advanced scoring output set, launch a trial, wait for completion, inspect completed trials, or download TimeSeries and Scalar results as pandas DataFrames. Do not use this skill for model editing, vpop creation, protocol design authoring, data-table upload, output-set creation/editing, or trial visualization.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Creating/running trials requires write and run permissions in the Jinkō project. Result DataFrame conversion requires pandas; raw ZIP/CSV download works without pandas.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō Trial SDK Workflows

Use this skill for trial setup, sanity checks, run/poll, and result download. Keep creation of upstream assets in their dedicated skills: `jinko-model`, `jinko-vpop`, `jinko-protocol`, `jinko-data-table`, and `jinko-output-set` (simple and advanced output sets).

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Minimum Trial

A minimum trial is composed of:

- A computational model.
- Solving options, using the model defaults unless an override is explicitly provided.
- A simple output set, defined as the list of component time series that should be saved and visualized. Use `model.time_dependent_ids()` as the default output ids when the user has not specified ids.

Optional trial inputs:

- Vpop.
- Protocol design.
- Data table design(s).
- Advanced output set/scoring design.

## Sanity Constraints

Do not launch while trial sanity reports errors. **Always confirm this by calling `trial.sanity()` — not by re-running standalone checks from upstream skills (`validate_scoring_formula`, `client.validate_scoring_condition`, `scoring_design.diagnostics`, etc.).** Those checks only validate an asset in isolation; they cannot see how it behaves once bound to this concrete trial. `trial.sanity()` is the same trial-context check the Jinkō UI runs before launch and is the source of truth for launch-readiness — see `references/trial-setup.md` for the pre-launch workflow and `errors after standalone validation passed` troubleshooting.

Typical constraints surfaced by trial sanity:

- The computational model cannot have sanity errors.
- All descriptors in the protocol must correspond to model components.
- All descriptors in the vpop must correspond to model components.
- All descriptors in data-table `obsId` columns must correspond to model components.
- All data-table `armScope` values must correspond to protocol arms when a protocol is used.
- The advanced output set (scoring design) must resolve cleanly against this trial's model outputs and simple output set — this can fail here (`ADVANCED_OUTPUTS_ERRORS`) even when `jinko-output-set`'s standalone validation passed.

If sanity errors are reported, show them and ask whether the user wants help fixing the upstream asset.

## Core SDK Methods

- Create simple output set: `client.create_simple_output_set(model, model.time_dependent_ids())` unless explicit output ids were requested. See `jinko-output-set` for measure shapes and advanced output sets (constraints/scalars/objectives).
- Create trial: `client.create_trial(model, data_tables=..., vpop=..., protocol=..., simple_output_set=..., advanced_output_set=...)`.
- Edit solving options after creation: `trial.edit_solving_options({...})`; use `trial.get_solving_options(as_iso8601=True)` to inspect raw duration strings, or omit the flag for `timedelta` values. For focused edits, use `trial.set_solving_times(t_max=timedelta(days=28), t_step="P1D")` with either representation.
- Pre-launch sanity check (required before `run()`): `trial.sanity()` — returns a raw `dict` (the JSON response, not a typed object) with one component report per key (`model`, `protocol`, `vpop`, `outputSet` for the simple output set, `scorings` for the advanced output set, `dataTables`, `solvingTimes`), each with `["sanity"]["errors"]`/`["sanity"]["warnings"]` and `["sanity"]["componentsSanity"]` for per-component detail.
- Run trial: `trial.run()`.
- Poll: `trial.wait_until_completed(timeout=1800)`.
- Discover time series: `trial.output_ids()`.
- Discover scalars and arms: `trial.results.summary()`.
- Download time series as pandas when available: `trial.results.timeseries({...}).to_dataframe()`.
- Download scalars as pandas when available: `trial.results.scalars([...]).to_dataframe()`.
- Without pandas, use `TabularDownload.raw_bytes`; result payloads may be CSV or zipped CSV.

When data tables are attached, pass them through the supported `data_tables=` argument. Require each data table to report `metadata.public.validForFitnessFunction is True` before creating the trial; reject `False`, missing, and malformed values.

## Project Folder Hygiene

- Prefer creating output sets and trials inside a dedicated Jinkō folder instead of the project root. At the start of a workflow, ask for or propose a folder name, for example `YYYY-MM-DD-<experiment-name>`.
- Reuse an existing exact-match folder when possible: `client.get_folder_by_name(name, exact_match_only=True)`.
- If the folder does not exist, create it only after user confirmation or when a script is run with `--apply`.
- Resolve one folder object or folder id, then pass `folder=folder` to trial creation calls. For simple output sets, create them first and then move them with `output_set.move_to_folder(folder)`.

## Retry And Reuse Hygiene

- For one user request, keep one named local setup script and update it rather than creating `run_v2.py`, `run_v3.py`, and similar copies.
- When a trial or output set fails validation, inspect and repair the existing item first. Re-run `trial.sanity()` after the repair.
- Create a new trial or output set only when the user requests an independent scenario, the existing item is immutable/incompatible, or a repair would destroy a result the user asked to preserve. State the reason when creating a replacement.

## SDK Scripts

These are on `PATH` as console scripts once the SDK is installed, and also
runnable via `python -m` as shown below.

- `jinko.cli.find_completed_trial_results`: lists trials, finds the first completed one, prints its summary, and downloads TimeSeries and Scalar results to pandas DataFrames.
- `jinko.cli.setup_and_run_trial`: creates a simple output set, creates a trial from model plus optional assets, sanity-checks, optionally runs, polls, and optionally downloads results.

Examples:

```bash
python -m jinko.cli.find_completed_trial_results --limit 20 --output-dir trial-results
python -m jinko.cli.setup_and_run_trial --model-sid cm-...
python -m jinko.cli.setup_and_run_trial --model-sid cm-... --output-id Drug
python -m jinko.cli.setup_and_run_trial --model-sid cm-... --output-id Drug --folder 2026-06-15-trial-run --create-folder --apply --run
python -m jinko.cli.setup_and_run_trial --model-sid cm-... --output-id Drug --vpop-sid vp-... --protocol-design-sid pd-... --data-table-sid dt-... --apply --run --download-results
```

## Reference Routing

- Read `references/trial-setup.md` for trial creation, the safe pre-launch sanity-check workflow, and troubleshooting `ADVANCED_OUTPUTS_ERRORS`/"The following advanced outputs have errors".
- Read `references/trial-results.md` for completed-trial discovery and result downloads.
