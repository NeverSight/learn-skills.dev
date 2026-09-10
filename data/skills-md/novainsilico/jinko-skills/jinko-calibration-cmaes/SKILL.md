---
name: jinko-calibration-cmaes
description: >-
  Create, run, poll, and inspect results for Jinkō CMA-ES calibrations via
  the jinko-sdk: attach data tables and/or an advanced output set as
  fitness-function sources, set CMA-ES options and parameter priors, launch
  and monitor the run, and read performance/results payloads. Use whenever
  the user needs the SDK mechanics of building or driving a Calibration
  object. Do not use this skill for calibration business rules (defaults,
  diagnostics, deliverable rules). Do not use this skill for advanced output
  set / scoring design authoring — use jinko-output-set. Do not use this skill
  for data-table creation or validForFitnessFunction checks — use
  jinko-data-table. Do not use this skill for model or protocol
  authoring — use jinko-model / jinko-protocol. Do not use this skill for
  calibration-plan orchestration or iteration workflow.
compatibility: >-
  Check set-up with jinko-sdk-setup. Creating/running calibrations requires
  write and run permissions.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō CMA-ES Calibration SDK Workflows

| UI wording  | API project-item type | SDK entry points |
| ----------- | ---------------------- | ----------------- |
| Calibration | `Calibration`           | `client.create_calibration(...)`, `model.create_calibration(...)`, `Calibration` domain object |

The calibration manager API is CMA-ES only — no type/method discriminator exists. "Subsampling" is an unrelated VPop-generator feature, not a calibration type.
This skill is pure SDK mechanics: no defaults, no diagnostics, no when-to-calibrate guidance.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Minimum Calibration

- `parameters`: priors to calibrate (required, ≥1).
- At least one fitness-function source (required): `dataTableDesigns` (data table must report `metadata.public.validForFitnessFunction: True`, see `jinko-data-table`) and/or an advanced output set with objectives (see `jinko-output-set`). This skill creates neither input.
- `CalibrationOptions`: `seed` + `thresholdWeightedScore` are schema-required and have contract defaults `0` and `1`; `populationSize` + `numberOfIterations` have no contract defaults and are functionally required. The bundled creation script requires population size and iteration count, and uses the contract defaults for omitted seed and threshold; pass all four explicitly when reproducibility policy requires it.

Two encoding rules are mandatory before creation:

- With `log_transform=True`, `mean` and `std` are in `log10(x)` coordinates, but `min_bound` and `max_bound` remain in the original physical coordinates of `x`. If planned bounds are written in log10 coordinates, exponentiate them first: `physical_bound = 10**log10_bound`. A calibration sanity warning such as `MAX_BOUND_LOWER_THAN_MEAN_LOG` indicates this mapping is inconsistent.
- For every attached fitness data table, set `options.log_transform_wide_bounds` to every distinct `obsId` in that table unless the user explicitly requests linear bound scaling for a named observable. This is the SDK field behind the UI's **Scale bounds** option.

## Create

```python
model = client.get_model("cm-...")
data_table = client.get_data_table("dt-...")
calibration = model.create_calibration(
    parameters=[
        {
            "id": "k_elim",
            "mean": -1.0,
            "std": 0.5,
            "log_transform": True,
            "min_bound": 0.001,
            "max_bound": 10.0,
        }
    ],
    data_tables=[
        {
            "data_table": data_table,
            "include": True,
            "options": {
                "weight": 1.0,
                "log_transform_wide_bounds": sorted({
                    row["obsId"] for row in data_table.export()
                }),
            },
        }
    ],
    calib_seed=42,
    calib_threshold_weighted_score=0.0,
    calib_number_of_iterations=100,
    calib_population_size=12,
)
```

Equivalent client-level call: `client.create_calibration(model=model, ...)`.
`calibrationOptionsOverride`, `solvingOptionsOverride`, `coreVersion` have no typed kwarg — use `client.create_calibration_from_json(json_content=payload)` / `client.calibrations.create_raw(payload)`.
See `references/creating-a-calibration.md` for full field tables.

Solving times can be set post-creation with `calibration.set_solving_times(t_max=timedelta(days=28), t_step="P1D")`; each duration may be a `timedelta` or ISO 8601 string.

## Run & Poll

```python
calibration.run()
final_status = calibration.wait_until_completed(timeout=3600)
```

See `references/running-and-polling.md` for `.get_sanity()`, `.status()`, and
`StoppingReason` values.

## Results

```python
calibration.performance()  # raw dict
calibration.results_summary()  # raw dict
calibration.objective_weights()  # raw dict, {objective_id: weight}
calibration.results.sorted_patients(
    sort_by="optimizationWeightedScore desc"
)  # raw, low-level
```

All results accessors return unparsed dicts today. See `references/results-and-inspection.md`.

## Project Folder Hygiene

Same as `jinko-trial`/`jinko-data-table`: propose a `YYYY-MM-DD-<experiment>` folder, reuse an exact-name match via `client.get_folder_by_name(name, exact_match_only=True)`, create only on confirmation or `--create-folder --apply`.

## SDK Scripts

These are on `PATH` as console scripts once the SDK is installed, and also
runnable via `python -m` as shown below.

- `jinko.cli.create_cmaes_calibration`: dry-run by default, creates a calibration with `--apply`.
- `jinko.cli.run_calibration`: runs and polls an existing calibration with `--apply`.
- `jinko.cli.inspect_calibration`: prints/writes raw performance/results_summary/objective_weights/sorted_patients JSON.

```bash
python -m jinko.cli.create_cmaes_calibration --model-sid cm-... --data-table-sid dt-... --parameter "k_elim:-1.0:0.5:0.001:10.0:log" --seed 42 --threshold-weighted-score 0.0 --iterations 100 --population-size 12
python -m jinko.cli.create_cmaes_calibration --model-sid cm-... --data-table-sid dt-... --parameter "k_elim:-1.0:0.5:0.001:10.0:log" --seed 42 --threshold-weighted-score 0.0 --iterations 100 --population-size 12 --folder 2026-07-07-calib --create-folder --apply
python -m jinko.cli.run_calibration --calibration-sid ca-... --apply --timeout 3600
python -m jinko.cli.inspect_calibration --calibration-sid ca-... --performance --results-summary --objective-weights --output-dir calib-results
```

## Reference Routing

- `references/creating-a-calibration.md`: full field tables, three creation patterns.
- `references/running-and-polling.md`: run/stop/status/sanity, `JobStatus`, `StoppingReason`.
- `references/results-and-inspection.md`: performance/results_summary/objective_weights/results.* field tables and caveats.
