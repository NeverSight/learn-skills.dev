---
name: jinko-task-from-nonmem
description: >-
  Convert a NONMEM run into a Jinkō trial set-up via the jinko-sdk. Use this skill whenever the user wants to import, translate, port or migrate a NONMEM model, control stream, .mod/.ctl/.lst file, .ext estimates, .phi individual estimates or a NONMEM data set into Jinkō, or asks to reproduce a published population-PK model that exists as NONMEM code. Emits the computational model, virtual population, protocol design and output set, checks the result numerically against a declared reference, and can publish the evidence as a Jinkō document. Use jinko-model to author a model from scratch, jinko-protocol to edit an existing protocol, jinko-vpop to edit a population, and jinko-calibration-cmaes to fit parameters.
compatibility: >-
  Needs `pip install "jinko-sdk[nonmem2jinko]"`; the converter ships with the SDK but its numerical extra does not install by default. Check set-up with the `jinko-sdk-setup` skill. Creating project items requires write access to the Jinkō project. The independent-parse check needs R with `nonmem2rx` and `rxode2`; without them the conversion still runs, but that check is unavailable rather than passed.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.16,<2.0"
license: MIT
---

# Jinkō Task: From NONMEM

Convert a NONMEM run into a working Jinkō trial.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. A
> session code can be exchanged only once, so call `get_session_code` again
> before this skill's own SDK process. If that skill is not found, install it
> from `novainsilico/jinko-skills`.
>
> This skill additionally needs the converter's extra, which the SDK does not
> install by default:
>
> ```bash
> pip install "jinko-sdk[nonmem2jinko]"
> ```
>
> The converter is the `nonmem2jinko` package. It ships inside `jinko-sdk` and
> is imported separately. The extra adds scipy, which the numerical check
> integrates the reference solve with. Without it every script still runs, and
> `--check solve` raises a message naming the extra.

## Core Rules

- Run the scripts. Never hand-translate `$PK`; only the scripts' output is verified.
- Always check the numbers, and report the measured agreement. Never claim a
  conversion succeeded without one, and never publish a report whose verdict
  has no result in it.
- Say which reference the numbers came from. `--reference scipy` isolates the
  platform; `rxode2` covers the reading too; `nonmem` compares against a
  `$TABLE` the original run wrote and needs no licence, only that file. They
  are not interchangeable. The `rxode2` numerical reference currently refuses
  models needing covariate overrides rather than comparing unequal inputs.
- Blocking error means stop. Do not pass `--allow-issues` without telling the
  user what is lost.
- Read the report before applying. Units and names are inferred, and some
  inferences will be wrong for a given data set.
- Wrong time unit changes the kinetics silently. Jinkō accepts arbitrary time
  units but solves and returns results in seconds. Confirm amount, volume and
  time against the data set.
- Compare on the platform's own time grid. `Time` is a requestable series;
  request it. A recorded event inserts its own points, so a grid rebuilt from
  `tMin`/`tStep` pairs values with the wrong times.

## Scripts

| Script | Does |
| --- | --- |
| `convert_model.py` | Control stream to computational model |
| `convert_trial.py` | Model plus vpop, protocol, output set, trial |
| `compare_against_reference.py` | The numerical check. Not optional |
| `upload_data_tables.py` | Population to data tables, bound to the trial and overlaid on a viz |
| `render_equivalence_report.py` | Measured comparison artifacts to a Markdown report |
| `publish_equivalence_report.py` | Report to a Jinkō document |

Project writes are dry-run by default and gated by `--apply`. Local artifact
outputs are explicit path arguments and preserve existing files where their
scripts expose `--overwrite`.

## Orchestration

1. Ask for `.ext`, `.phi` and the data set. Each improves the conversion; the
   control stream alone is enough to start.
2. Convert dry-run. Resolve what the report raises: `--time-unit`,
   `--amount-unit`, `--volume-unit`, `--unit SYMBOL=unit`,
   `--rename NONMEM=jinkoId`.
3. Apply, then run.
4. Check numerically using the same `--time-unit` as conversion. A skipped solve
   is a failure, not evidence. Report the number and its reference.
5. Render and offer an equivalence report whenever anyone other than the person
   running the conversion will rely on the model.

Every write step takes `--folder NAME --create-folder`, which keeps one run's
items together, and `--json-out FILE`, which is how the next step gets the
SIDs. Do not scrape them out of the prose.

`--parent-folder NAME` nests that folder inside another one. Use it when a
project accumulates several conversions: a folder named for the day holding one
subfolder per model keeps each run's evidence together, and the runs sort
chronologically. Without it a project's root fills up with model names and
nothing says which run each belongs to.

## Decisions

**Population** (`convert_trial.py`). `--population design` (default) is editable
in Jinkō afterwards. `phi` replays the fitted subjects. `sampled` draws from the
full multivariate normal represented by `$OMEGA`; a finite sample's realised
covariance has sampling error and must be measured rather than called exact.

**Random effects** (both converters). `--vpop-mode etas` (default) represents
the target `$OMEGA` covariance through ETA marginals and correlations.
`parameters` puts marginals on the derived parameters instead: it reads better
in the UI but is equivalent only without covariate effects.

**Dosing** (`convert_trial.py`). `--dosing auto` (default) uses arms when the
data set has an arm structure and per-patient slots when it does not. A study
where every subject has an individualised history — neonatal phenobarbital,
weight-banded single doses — has no arm structure, and `per-patient` puts each
patient's own dose times and amounts in the vpop. Needs `--population phi` or
`sampled`, because the schedule rides on the patient table.

**Uncertainty** (`convert_trial.py`). `--eps-clones N` gives a per-patient
predictive cone. Needs `--population phi` or `sampled`. Not a VPC — see
`references/residual-error.md`.

**Refused, with the record named:** steady-state (`SS`) dosing, `$MIX`, nested
random effects, `$OMEGA`/`$SIGMA` as SD, correlation or Cholesky, `$PRED`-only
models, abbreviated code that cannot be read (`MPAST`, a variable `ETA()`
subscript, `CALL`, `include`), a parameter the kinetics need that reads a
record-level data item such as `DV` or `EVID`, and `IF(AMT.GT.0) TDOS = TIME`
— which is refused precisely because substituting simulation time for it looks
right and silently gives zero time-since-dose.

**Reported, not refused:** `$PRIOR` and `$NONPARAMETRIC` shaped the estimation,
not the forward model, so the estimates convert as given.

**Converted with a stated approximation:** `DOSE = AMT` points at the model's
dose parameter, so a subject whose doses differ in amount reads only the first;
time-varying covariates keep their baseline only; a covariate selecting *which* random effect applies cannot be
one vpop marginal; a combined error model written through a weight
(`Y = F + W*EPS(1)`, `W = F*θ + θ`) is diagnosed with its coefficients but the
observable is emitted without residual error.

## References

- `references/workflow.md` — commands, flags, worked sequence
- `references/validation.md` — the numerical checks and what each proves
- `references/reporting.md` — equivalence reports, data tables, overlays
- `references/conversion-map.md` — what each NONMEM construct becomes
- `references/residual-error.md` — `$ERROR`, `$SIGMA`, the clone approximation

Generic mechanics belong to the lower-level skills: `jinko-model` for
components, `jinko-vpop` for populations, `jinko-protocol` for arms,
`jinko-trial` for runs, `jinko-data-table` for tables, `jinko-trial-viz` for
visualisations, `jinko-document` for documents.
