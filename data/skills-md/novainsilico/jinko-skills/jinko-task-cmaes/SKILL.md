---
name: jinko-task-cmaes
description: >-
  Execute a CMA-ES calibration from confirmed Jinkō inputs: assemble the model,
  protocol, output sets, fitness data tables, parameter priors, and optimizer
  options; create and run the Calibration; and return the supported results.
  Use when the user wants to perform a CMA-ES calibration, not when they need
  to choose a calibration strategy, infer priors, design objectives, or decide
  whether results are acceptable.
compatibility: >-
  Check set-up with jinko-sdk-setup. Creating and running calibrations requires
  write and run permissions.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# CMA-ES Calibration Task

Execute a confirmed calibration specification. Do not invent objectives,
constraints, parameter priors, optimizer options, or acceptance criteria.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Inputs

Require:

- a model SID;
- parameter priors with physical bounds;
- `seed`, `thresholdWeightedScore`, `numberOfIterations`, and `populationSize`;
- at least one fitness source: calibration-ready data tables and/or an advanced
  output set containing objectives;
- any protocol, simple output set, advanced output set, folder, and name needed
  by the specification.

If quantitative evidence has not yet been converted into a calibration-ready
table, use `jinko-task-extract-data-table`. Use `jinko-data-table`,
`jinko-output-set`, `jinko-model`, and `jinko-protocol` only for their respective
Jinkō object mechanics.

## Workflow

1. Resolve every input to its intended SID and snapshot. Present missing or
   ambiguous inputs instead of guessing.
2. Use `jinko-calibration-cmaes` and its bundled creation script. Review its
   dry-run output before applying it. The script owns parameter encoding,
   fitness-table eligibility, bound scaling, creation, and post-creation sanity;
   stop on an error and surface warnings.
3. Return the created calibration SID, revision, snapshot, URL, and effective
   options for confirmation.
4. Use the lower-level run script to perform pre-launch sanity, launch, and wait
   for a terminal state. Do not relaunch a terminal snapshot; create or update a
   configuration so the intended change has a new snapshot.
5. Use the lower-level inspection interfaces to collect the final status,
   stopping reason, performance, results summary, objective weights, and the
   patient sorted first by `optimizationWeightedScore` when available. Fetch
   per-patient scalars, timeseries, errors, or augmented data tables only when
   their required selectors are present in the result metadata.

## Return

Return:

- calibration SID, revision, snapshot, and URL;
- effective input references, priors, and optimizer options;
- sanity warnings, terminal status, stopping reason, and performance;
- supported result payloads and best-patient identity, with the iteration and
  scenario arm needed for subsequent result calls;
- a concise account of unavailable requested outputs.

Do not claim a separate run ID, convergence analysis, score-evolution curve,
best-patient parameter values, parameter posterior, or simulation-vs-data plot
unless the returned API payloads actually provide the required data.
