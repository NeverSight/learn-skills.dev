---
name: jinko-task-define-param-to-calibrate
description: >-
  Classify directly valued Jinkō model inputs by evidence source and assign
  inputs needing calibration to explicit calibration steps. Use when the user
  wants to decide which parameters, categorical parameters, or species initial
  conditions should be calibrated and record the decision with `s::*` and
  `CalibIter::*` tags. Do not use for choosing datasets, estimating priors,
  drafting calibration plans, or running calibrations.
compatibility: >-
  Check set-up with jinko-sdk-setup. Applying labels requires model write access.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Define Parameters To Calibrate

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

Classify model inputs from supplied evidence; do not infer unsupported provenance
or invent calibration steps.

## Inputs

Require:

- a model SID;
- documentation or other evidence for the current input values;
- an explicit ordered list of calibration step identifiers and each step's biological
  scope;
- any user overrides and whether existing labels may be replaced.

## Labels

Assign at most one source tag per eligible input:

- `s::knowledge`: supported by literature, expert knowledge, or a reference
  model;
- `s::arbitrary`: deliberately fixed without an evidence-derived value;
- `s::to-calibrate`: insufficiently informed and intended for calibration;
- `s::calibrated`: preserve when present; never assign in this task.

Assign `CalibIter::<step>` only with `s::to-calibrate`, using an explicitly
provided step whose scope covers the input. Absence means the input is not
assigned to calibration. Leave uncertain inputs unchanged and report them.

## Workflow

1. Use `jinko-model` to inspect parameters, categorical parameters, and species
   initial conditions. Exclude derived formulas, technical infrastructure, and
   non-input components.
2. Preserve existing `s::*` and `CalibIter::*` tags unless relabeling was
   requested. For each remaining input, classify its source from the evidence.
3. Map every `s::to-calibrate` input to the first supplied step whose scope fully
   covers its biological role. If no unique step qualifies, leave it unchanged
   and add it to `todo`.
4. Write the proposed mutations as JSON and run
   `scripts/apply_calibration_labels.py` in dry-run mode, then with `--apply`
   after review. The script validates source/step consistency, duplicate
   assignments, component kinds, existing-label conflicts, and allowed model
   mutations before applying one component batch.
5. Re-fetch the model and return the new revision and snapshot with a compact
   report: assigned and preserved labels, counts by source and step, and `todo`
   entries with reasons.

The mutation plan has this shape:

```json
{
  "in_scope_steps": ["2", "3"],
  "assignments": [
    {"component_id": "k_elim", "source": "to-calibrate", "calibration_step": "2"},
    {"component_id": "body_weight", "source": "knowledge"}
  ]
}
```

Do not change values, units, descriptions, equations, structure, or unrelated
tags. `todo` items are reported, not encoded as placeholder tags.
