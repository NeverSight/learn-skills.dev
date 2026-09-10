---
name: jinko-calibration-subsampling
description: >-
  Create, validate, run, inspect, reuse, and edit Jinkō virtual-population subsampling designs with the jinko-sdk.
  Use whenever a completed Trial's simulated patients must be filtered or selected to match population-level targets, then emitted as a matched Vpop.
  This is SDK mechanics only: do not use it to choose scientific targets, filters, or algorithm settings; do not use it to create or run the source Trial, author a Vpop, or orchestrate a calibration workflow.
compatibility: >-
  Check set-up with jinko-sdk-setup.
  Creating designs or generated Vpops requires write and run permissions in the Jinkō project.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō Subsampling SDK Workflows

| UI wording | API project-item type | SDK entry points |
| --- | --- | --- |
| Subsampling design | `SubsamplingDesign` | `trial.create_subsampling_design(...)`, `client.get_subsampling_design(...)` |
| Subsampled Vpop | `Vpop` | `design.generate_vpop(...)` |

Subsampling creates a derived, smaller Vpop by selecting patients from the Vpop simulated in a completed Trial so that the selected population best matches specified population-level targets.
It neither calibrates the model nor creates new patients.
Use `jinko-trial` to create, sanity-check, and run the source Trial, and `jinko-vpop` to inspect the generated Vpop.
Scientific choices belong to a workflow or domain expert, not this skill.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Canonical Flow

1. Retrieve the Trial, require `trial.status()["status"] == "completed"`, then inspect `trial.descriptors.scalars` and `trial.descriptors.categoricals`; descriptor IDs and arms must be taken from this Trial, not guessed from display labels.
2. Build a `SubsamplingDesign` with filters and population targets through `trial.create_subsampling_design(...)`.
3. Read `design.diagnostics`; do not generate while it has errors.
   Use `design.diagnostics.errors().explain()` to relate an error to its target or filter and its source-Trial descriptor.
4. Call `design.generate_vpop(...)` with all simulated-annealing options.
   The returned Vpop is immutable.
5. Inspect generated artifacts through `design.generated_vpops.list_with_details()`.
   Reuse a compatible design with `design.set_trial(other_trial)` before it is used, or edit its typed components such as `design.marginals`.

## Scalar Discovery and Candidate Estimates

Read `references/scalar-discovery-and-estimates.md` before choosing a Trial scalar or using platform-fitted law estimates. It distinguishes descriptor discovery, per-patient values, and candidate target forms without making the scientific choice for the user.

For a complete Python flow and the meaning of generation options, read `references/generation-and-diagnostics.md`.

## Typed Targets and Edits

- Numeric filters: descriptor builders such as `scalar.gte(18)`, or `design.numeric_filters.create_gte(...)` after creation.
- Scalar targets: `scalar.normal(...)`, `.uniform(...)`, `.weibull(...)`, and `design.marginals.create_*` / persisted-handle setters.
- Other supported SDK target surfaces: `design.categorical_filters`, `.categoricals`, `.correlations`, `.survivals`, `.summary_statistics`, and `.observables`.
  Read `references/creating-and-editing.md` before using one.
- The older UI guide says categorical constraints are unsupported, whereas the current SDK exposes typed categorical builders and services.
  Treat support as backend/version-dependent: create the design and require clean diagnostics before generation.

Use `design.edit(...)` only for advanced full-slice replacement.
Prefer typed subservices so immutable IDs and existing content are preserved.
A design can be pointed at another Trial only when descriptor/arm pairs remain compatible; use `design.set_trial(...)` and validate diagnostics again.

## Project Folder Hygiene

Propose a `YYYY-MM-DD-<experiment>` folder and reuse an exact-name match via `client.get_folder_by_name(name, exact_match_only=True)`.
Create folders and remote project items only after confirmation or when a script receives `--apply`.

## SDK Scripts

These are on `PATH` as console scripts once the SDK is installed, and also
runnable via `python -m` as shown below.

- `jinko.cli.create_subsampling_design`: dry-run creation of numeric filters, normal scalar marginals, and observables; `--apply` creates the design.
- `jinko.cli.generate_subsampled_vpop`: dry-run generation plan; `--apply` checks diagnostics and creates the Vpop.
- `jinko.cli.inspect_subsampling_design`: prints design content, diagnostics, source Trial, and generated-Vpop options/fitness without mutating anything.

Read `references/scripts.md` for invocation examples.

## Reference Routing

- `references/creating-and-editing.md`: descriptors, builders, target types, typed edits, and compatible Trial reuse.
- `references/scalar-discovery-and-estimates.md`: output-scalar discovery, per-patient scalar values, and platform candidate law estimates.
- `references/generation-and-diagnostics.md`: validation, annealing options, and generated-Vpop semantics.
- `references/inspection.md`: artifact listing, stored options, and fitness payload caveats.
- `references/scripts.md`: bundled-script invocation examples.
