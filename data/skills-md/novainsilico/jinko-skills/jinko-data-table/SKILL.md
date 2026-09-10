---
name: jinko-data-table
description: >-
  Create or inspect Jinkō data tables via the jinko-sdk. Use this skill whenever the user wants to upload observed data for trial overlays or calibration objectives from CSV, SQLite, or pandas DataFrame; check data-table schema columns; inspect existing data tables; or verify metadata.public.validForFitnessFunction. Do not use this skill for output sets; use jinko-output-set for that.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Creating data tables requires write access to the Jinkō project. DataFrame creation requires pandas.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō Data Table SDK Workflows

Use this skill for data-table mechanics through the SDK. Data tables can support trial overlays and calibration objectives; the row schema is the same, and fitness-function compatibility is reported by metadata when available.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Scope

- Use `client.create_data_table_from_csv()` for CSV files or bytes.
- Use `client.create_data_table_from_sqlite()` for SQLite files or bytes.
- Use `client.create_data_table_from_dataframe()` for pandas DataFrames.
- Inspect existing data tables with `get_data_table()`, `content()`, `summary()`, `validate()`, and `export()`.
- Check `metadata.public.validForFitnessFunction` after creation or inspection when available if the data table needs to be attached through trial/calibration `dataTableDesigns`.
- For trial workflows that attach data tables through `jinko-trial`, use a data table with `validForFitnessFunction: True`; point-value overlay tables may upload successfully but fail trial launch sanity.

## Project Folder Hygiene

- Prefer creating data tables inside a dedicated Jinkō folder instead of the project root. At the start of a workflow, ask for or propose a folder name, for example `YYYY-MM-DD-<experiment-name>`.
- Reuse an existing exact-match folder when possible: `client.get_folder_by_name(name, exact_match_only=True)`.
- If the folder does not exist, create it only after user confirmation or when a script is run with `--apply`.
- Resolve one folder object or folder id, then pass `folder=folder` to SDK creation calls that support it.

## Row Schema

Read `assets/data-table.json` before changing CSV structure.

Supported row shapes:

- Point-value row: `obsId`, `time`, `value`, plus optional `unit`, `armScope`, ranges, weight, and reference.
- Range row: `obsId`, `time`, `narrowRangeLowBound`, `narrowRangeHighBound`, plus optional `unit`, `armScope`, wide ranges, weight, and reference.

Use ISO-8601 duration strings for `time`, for example `PT0S`, `PT6H`, or `P1D`.

## Bundled Assets

- `assets/toy_data_table_values.csv`: point-value observations for trial overlays.
- `assets/toy_data_table_ranges.csv`: range observations suitable for calibration objective workflows.
- `assets/data-table.json`: schema subset for supported data-table rows.

## SDK Scripts

These are on `PATH` as console scripts once the SDK is installed, and also
runnable via `python -m` as shown below.

- `jinko.cli.create_data_table`: dry-run-validates every CSV row and creates a
  data table with `--apply`; use `--allowed-obs-id`, `--require-unit`,
  `--require-experiment-ref`, and `--require-fitness` for calibration inputs.
- `jinko.cli.inspect_data_table`: inspects existing data tables and can enforce
  fitness compatibility with `--require-fitness`.

Examples:

```bash
python -m jinko.cli.create_data_table --source skills/jinko-data-table/assets/toy_data_table_ranges.csv --method csv
python -m jinko.cli.create_data_table --source extracted.csv --allowed-obs-id Drug --require-unit --require-experiment-ref --require-fitness --apply
python -m jinko.cli.create_data_table --source skills/jinko-data-table/assets/toy_data_table_ranges.csv --method csv --apply
python -m jinko.cli.create_data_table --source skills/jinko-data-table/assets/toy_data_table_ranges.csv --method csv --folder 2026-06-15-fit-data --create-folder --apply
python -m jinko.cli.create_data_table --source skills/jinko-data-table/assets/toy_data_table_values.csv --method dataframe --apply
python -m jinko.cli.inspect_data_table --data-table-sid dt-... --fitness --validate
```

## Reference Routing

- Read `references/data-table-schema.md` for row shape and fitness-function notes.
- Read `assets/data-table.json` when checking required columns.
