---
name: jinko-protocol
description: >-
  Design or edit multi-arm Jinkō protocol designs via the jinko-sdk. Use this skill whenever the user wants to compare doses, schedules, administration routes, treatment activation flags, or combinations of treatments by overriding model component values per arm. Protocol designs assign values to model-defined inputs; dosing functions, schedule parameterization, treatment activation logic, and administration-mode logic belong in the model. Use jinko-model when those functions or inputs do not exist yet. Use jinko-trial for running trials.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Creating or editing protocol designs requires write access to the Jinkō project.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō Protocol SDK Workflows

Use this skill for protocol-design mechanics through the SDK. Keep the separation of concerns explicit: the model defines treatment-regimen functions and inputs; the protocol instantiates those inputs per arm.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Separation Of Concerns

- Protocol designs only override component values, with different override values per arm.
- Dosing functionality is defined at the model level: schedule parameterization, dose parameterization, treatment activation/deactivation through categorical parameters, route or administration mode through categorical parameters, and any formulas that interpret those inputs.
- In the model, define the treatment-regimen function and its input components.
- In the protocol, assign values to those inputs, as if instantiating that function for each arm.
- If a needed override key does not exist as a model input, switch to `jinko-model` first and add the model component or dosing logic there.

## Core Rules

- Prefer `client.create_protocol_design(arms, model=model)` when a model is available.
- Use `client.create_protocol_design_from_csv(csv_file_path=...)` when arms come from a spreadsheet. The CSV is posted as-is; the platform parses and validates it against its own protocol design CSV schema. This path does not accept a `model` argument; link a model with `client.create_protocol_design(...)` instead if that's required. See `assets/toy_protocol_arms.csv` for an example file and `references/protocol-design.md` for the SDK call.
- Link protocol designs to a model when possible so the protocol design carries the model snapshot reference.
- The override `key` must target a protocol-runnable model input, such as `Dose` or `route` in the toy model.
- Use formulas as strings, for example `"1.0"`, `"iv"`, or `"PT24H"` depending on the target component.
- Include control relationships when comparing arms; use `armControl` to identify the comparator arm.
- Edit individual arms on an existing design with `protocol.arms` (`get`, `create`, `set_control`, `set_active`, `set_weight`, `set_override`, `delete`, `compare_overrides`), not by replacing the raw design payload.
- Require explicit confirmation or script `--apply` before creating or updating project items.

## Project Folder Hygiene

- Prefer creating protocol designs inside a dedicated Jinkō folder instead of the project root. At the start of a workflow, ask for or propose a folder name, for example `YYYY-MM-DD-<experiment-name>`.
- Reuse an existing exact-match folder when possible: `client.get_folder_by_name(name, exact_match_only=True)`.
- If the folder does not exist, create it only after user confirmation or when a script is run with `--apply`.
- Resolve one folder object or folder id, then pass `folder=folder` to SDK creation calls that support it.

## Bundled Assets

- `assets/toy_protocol_arms.json`: three arms with two routes and three doses. The `iv` route repeats across two arms.
- `assets/toy_protocol_arms.csv`: the same three arms in CSV form, one row per arm, for use with `create_protocol_design_from_csv`.
- `assets/protocol.json`: subset of the OpenAPI schema for protocol arm shape.

## SDK Scripts

These are on `PATH` as console scripts once the SDK is installed, and also
runnable via `python -m` as shown below.

- `jinko.cli.create_protocol_design`: creates a three-arm protocol design, optionally linked to a model.
- `jinko.cli.create_protocol_design_from_csv`: creates a protocol design from a CSV file of arms.
- `jinko.cli.edit_protocol_design_arms`: upserts arms and overrides on an existing protocol design via the `arms` mutator service. It retains arms and overrides omitted from the input; use explicit `protocol.arms.delete(...)` or `arm.remove_override(...)` calls for removals.
- `jinko.cli.inspect_protocol_design`: prints protocol content or a concise arm summary.

Examples:

```bash
python -m jinko.cli.create_protocol_design --model-sid cm-...
python -m jinko.cli.create_protocol_design --model-sid cm-... --apply
python -m jinko.cli.create_protocol_design --model-sid cm-... --folder 2026-06-15-regimens --create-folder --apply
python -m jinko.cli.create_protocol_design_from_csv --csv skills/jinko-protocol/assets/toy_protocol_arms.csv --apply
python -m jinko.cli.edit_protocol_design_arms --protocol-design-sid pd-... --arms skills/jinko-protocol/assets/toy_protocol_arms.json --apply
python -m jinko.cli.inspect_protocol_design --protocol-design-sid pd-... --summary
```

## Arm Shape

Each arm should include:

- `armName`: stable arm identifier.
- `armOverrides`: list of `{ "key": "<model-input-id>", "formula": "<arm-specific-value>" }` entries.
- `armIsActive`: usually `true` for active arms.
- `armWeight`: usually `1` unless weighted simulations are intentional (for calibration).
- `armControl`: `null` for the comparator arm, or another arm name for arms compared against a control.

Default toy arms:

- `iv_low_dose`: `Dose=1.0`, `route=iv`, no control arm.
- `po_mid_dose`: `Dose=2.0`, `route=po`, controlled by `iv_low_dose`.
- `iv_high_dose`: `Dose=3.0`, `route=iv`, controlled by `iv_low_dose`.

## Reference Routing

- Read `references/protocol-design.md` for separation of concerns and SDK patterns.
- Read `assets/protocol.json` when validating arm payload shape.
