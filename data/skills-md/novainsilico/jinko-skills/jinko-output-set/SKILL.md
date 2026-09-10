---
name: jinko-output-set
description: >-
  Create, inspect, validate, and incrementally edit Jinkō output sets via the
  jinko-sdk: simple output sets (measure designs) that list scalar measures
  derived from model outputs, and advanced output sets (scoring designs) that
  define constraints, scalars, and weighted objectives for scoring virtual
  populations. Validate scoring expressions and read diagnostics before
  attaching an output set elsewhere. Do not use this skill for attaching a
  simple or advanced output set to a trial and running it; use jinko-trial for
  that. Do not use this skill for data-table creation or fitness-function
  metadata; use jinko-data-table for that. Do not use this skill for calibration
  setup or CMA-ES options.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Creating output sets requires
  write access to the Jinkō project; simple output sets also require an
  existing model. Advanced output sets can be created standalone. Objective
  preview rendering benefits from IPython and matplotlib but degrades to
  plain text without them.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō Output Set SDK Workflows

Use this skill for output-set mechanics through the SDK: creating, validating, inspecting, and incrementally editing simple and advanced output sets.
Keep trial attachment in `jinko-trial`, calibration attachment in `jinko-calibration-cmaes`, and data tables in `jinko-data-table`.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Core Concepts

Jinkō uses different names for the same objects in the UI, the API, and the SDK.

| UI wording          | API project-item type | SDK entry points                                              |
| -------------------- | ---------------------- | -------------------------------------------------------------- |
| Simple output set    | `MeasureDesign`         | `client.create_simple_output_set(...)`, `SimpleOutputSet`     |
| Advanced output set  | `ScoringDesign`         | `client.create_advanced_output_set(...)`, `AdvancedOutputSet` |

An advanced output set groups three component kinds: constraints (boolean per-patient eligibility expressions), scalars (numeric formulas derived from simulation output), and objectives (range-based scoring rules with a weight).
Scalars serialize under the raw JSON key `components.measures` — do not confuse with simple-output-set "measures".

## Discovering Output Ids

Never invent output ids.
Call `model.time_dependent_ids()` to discover the model's valid output ids before creating a simple output set, same as `jinko-trial` does.
Advanced-output-set formulas reference output ids or other scalar ids by name.
Scoring-formula time values are always seconds, regardless of the model time
unit. Formulas do not support time-unit annotations: convert scientific times
explicitly. Consequently, `int(X)` and `auc(X)` have a seconds time component;
declare their scalar units with `*s`.
If unsure whether a piece of formula syntax is still supported, validate it with `client.validate_scoring_formula(...)` rather than assuming old examples still apply.
Read `references/formula-language.md` before writing any non-trivial constraint/scalar/objective formula or component filter. It gives the actual grammar (time reduction functions, time indexing, arm references) and documents validation messages.

## Simple Output Set Workflow

```python
model = client.get_model("cm-...")
output_set = client.create_simple_output_set(model, model.time_dependent_ids())
# Equivalently: model.create_simple_output_set([...])
```

Measures accept output-id strings (shorthand for `{"timeseriesId": id}`) or dicts for custom names, origins, and point-in-time/across-time functions.
Edit with `.content()`, `.measures`, `.replace_all_measures()`, `.add_measures()`, `.remove_measures()`, `.update_measure()`.
See `references/simple-output-set.md` for the full schema.

## Advanced Output Set Workflow

```python
scoring_design = client.create_advanced_output_set(
    constraints=[{"id": "adults", "constraint": "age >= 18"}],
    scalars=[{"id": "auc", "formula": "auc(Drug)", "unit": "mg/L*s"}],
    objectives=[
        {
            "id": "obj_auc",
            "formula": {
                "target": "auc(Drug)",
                "range": {
                    "narrowRangeLowBound": 8.0,
                    "narrowRangeHighBound": 12.0,
                    "wideRangeLowBound": 5.0,
                    "wideRangeHighBound": 15.0,
                },
            },
            "weight": 1.0,
        }
    ],
    name="PK scoring",
)
```

Add components incrementally with `scoring_design.components.add_constraint(...)`, `.add_scalar(...)`, `.add_objective(...)` — each call creates a new versioned snapshot. For a batch, validate every component and check all ids for conflicts before the first call; if a later request fails, report the ids already applied.
See `references/advanced-output-set.md` for full schemas, the components service, and the raw JSON escape hatch.

## Validation & Diagnostics

Constraint and formula expressions are validated automatically inside `create()` and `components.add_*()`.
They always raise `ValidationError` on failure — `show_validation` only controls whether a report is printed, it does not suppress the raise.

```python
if scoring_design.diagnostics.errors():
    print(scoring_design.diagnostics.errors().explain())
```

`sd.diagnostics` is chainable: `.for_kind(...)`, `.with_severity(...)`, `.with_code(...)`, `.for_component(...)`, `.errors()`, `.warnings()`, `.has_errors()`, `.by_component()`, `.by_kind()`, `.by_severity()`, `.explain()`.
Use `sd.diagnostics_at(revision)` for a historical snapshot.

**What this validates, and what it does not.** `client.validate_scoring_formula(...)`/`validate_scoring_condition(...)` and `sd.diagnostics` only check the scoring design in isolation — formula syntax, referenced ids resolving to *something*, constraint/objective shape.
They do not know about any concrete trial. A formula can pass every check here and still fail once the advanced output set is bound to a trial (e.g. it references a measure that exists on this model but not on the trial's simple output set, or a unit/time-window mismatch with the trial's protocol).
Passing standalone validation is necessary, not sufficient, for trial compatibility — never report an advanced output set as "trial-ready" based on this skill's checks alone. Use `jinko-trial`'s trial-sanity step (`trial.sanity()`) once the output set is attached to a concrete trial.

## Attaching to Trials/Calibrations

This skill only creates, inspects, and edits output sets — it does not attach them or run anything, and it cannot confirm trial compatibility (see above).
For trials, use `jinko-trial`: `model.create_trial(simple_output_set=..., advanced_output_set=..., ...)`, then run `trial.sanity()` before launch — see `jinko-trial`'s pre-launch check.
For calibrations, use `jinko-calibration-cmaes` for the SDK call (`model.create_calibration(simple_output_set=..., advanced_output_set=..., ...)`).
A calibration needs at least one fitness-function source: a data table with `validForFitnessFunction: True` (see `jinko-data-table`) and/or an advanced output set with objectives.

## SDK Scripts

These are on `PATH` as console scripts once the SDK is installed, and also
runnable via `python -m` as shown below.

- `jinko.cli.create_simple_output_set`: dry-run by default, creates a simple output set with `--apply`.
- `jinko.cli.create_advanced_output_set`: dry-run by default, creates an advanced output set with `--apply`.
- `jinko.cli.inspect_output_set`: inspects an existing simple or advanced output set.
- `jinko.cli.edit_advanced_output_set`: adds constraints/scalars/objectives to an existing advanced output set.

```bash
python -m jinko.cli.create_simple_output_set --model-sid cm-... --output-id Drug
python -m jinko.cli.create_simple_output_set --model-sid cm-... --output-id Drug --folder 2026-07-07-output-sets --create-folder --apply
python -m jinko.cli.create_advanced_output_set --constraint "adults:age >= 18" --scalar "auc:auc(Drug)" --name "PK scoring"
python -m jinko.cli.create_advanced_output_set --from-json skills/jinko-output-set/assets/advanced_output_set_example.json --apply
python -m jinko.cli.inspect_output_set --kind advanced --sid sc-... --diagnostics
python -m jinko.cli.edit_advanced_output_set --sid sc-... --add-objective "obj_auc:auc(Drug):8:12:5:15:1.0" --show-diagnostics --apply
```

## Reference Routing

- Read `references/simple-output-set.md` for measure dict shapes and editing methods.
- Read `references/advanced-output-set.md` for constraint/scalar/objective shapes, validation, diagnostics, and tags.
- Read `references/formula-language.md` for the constraint/scalar/objective formula grammar (functions, time indexing, arm references) and its pitfalls.
