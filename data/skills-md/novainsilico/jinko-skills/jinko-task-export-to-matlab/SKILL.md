---
name: jinko-task-export-to-matlab
description: >-
  Export a Jinkō computational model to SimBiology, apply its exported simulation
  settings in MATLAB, and compare selected time series with Jinkō simple_solve
  results. Use this skill whenever the user wants to transfer a Jinkō model to
  MATLAB/SimBiology, validate an Excel-based SimBiology export against Jinkō,
  reproduce a Jinkō simple solve in SimBiology, or investigate divergence between
  the two solvers. Use it even when the user gives only a model short ID or link
  and asks for a SimBiology comparison.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Downloading model in MATLAB/SimBiology
  format requires Jinkō project access. Needs PyYAML. Prefer an available
  MATLAB/SimBiology MCP server; otherwise the user needs MATLAB with SimBiology.
  Excel component import is a Model Builder action.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō to MATLAB / SimBiology

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

Guide the workflow, but use `scripts/jinko_matlab_parity.py` for deterministic
file handling and comparison maths. The helper is an implementation detail: do
not present it as a CLI users must learn or ask them to reproduce its commands.
This avoids repeated ad-hoc code and preserves context for the scientific result.

## MATLAB MCP capability gate

Before launching MATLAB, running MATLAB code, or saying that a MATLAB/SimBiology
MCP server is unavailable, explicitly inspect the complete callable tool registry
for MATLAB or SimBiology capabilities. Include lazily discoverable tools; do not
infer MCP absence from the initial tool summary alone. In environments that expose
`ALL_TOOLS`, query it for `matlab` or `simbiology`; otherwise use the platform's
tool-discovery mechanism.

- A callable MATLAB evaluation or script-execution MCP tool means the server is
  available. State that finding and use the MCP for MATLAB inspection, execution,
  and result retrieval.
- Use a local MATLAB CLI only after the full capability check finds no suitable
  MATLAB MCP operation. Record the fallback succinctly so the user can distinguish
  it from an MCP-backed run.
- Do not continue after an ambiguous discovery result: resolve it before choosing
  the execution path. This gate prevents an invisible or lazy-loaded MCP server
  from being bypassed.

## Start with the model, not the outputs

1. Complete the MATLAB MCP capability gate. Use the server when available; do not
   install or reconfigure one without the user's direction.
2. Ask only for the CM short ID (a Jinkō CM link is sufficient; extract its ID).
   Export before asking which outputs to compare.
3. Create a dedicated run directory such as `/tmp/jinko-to-matlab/<cm-sid>/` and
   invoke the helper's `export` command there. It safely extracts the bundle,
   requires exactly one workbook and its matching
   `SimulationSettings_<model_name>.yaml`, validates the settings, and writes
   `parity-manifest.json` with content hashes.

Do not ask for repeated confirmation after successful access, export, or manifest
validation. State the resulting workbook and settings paths succinctly.
The helper preserves existing manifests and result files by default. Review the
existing artifacts before using `--overwrite` for an intentional rerun.

## Reuse the imported project

Read `reuse.workbook_unchanged` in the manifest before requesting any Model
Builder action.

- If a discoverable saved `.sbproj` exists and the workbook is unchanged, reuse it.
  Apply the current exported settings for every comparison; a settings-only update
  does not require a reimport.
- If no saved project exists, the workbook changed, or several candidate projects
  are found, ask one concise question. For a changed/missing project, direct the
  user to create a blank Model Builder model, delete its default `unnamed`
  compartment, then use **Home → Model → Import Model Components from Excel**.
  Have them save the project in the run directory. Removing that placeholder
  prevents an extra compartment from being carried into the imported model. This
  is intentionally the only mandatory manual step: SimBiology has documented
  SBML/project imports, not an Excel-component import API.
- Never overwrite the supplied `.sbproj`. Load it into MATLAB and make all
  configuration/dose changes in memory for the current comparison only.

## Offer a single comparison choice

Use the helper's `list-series` command to obtain statically time-dependent IDs.
Display them as the eligible outputs and ask the user to choose one to ten. Do not
include `Time` in that list or count it against the limit. Do not silently select,
rename, or substitute components.

Once the user selects outputs, call the helper's `solve` command. It sends the
exact Jinkō payload `['Time', *selected_ids]`; **`Time` is case-sensitive and is
not returned unless requested.** Pass the export's `parity-manifest.json` to the
command and require every requested series and `Time` in the response. The helper
converts Jinkō's returned seconds into the exported `TimeUnits` and writes
`matlab_output_times`; use those values as MATLAB `OutputTimes` and never derive a
uniform grid or pass raw Jinkō seconds to a differently configured MATLAB model.

## Run MATLAB with the exported configuration

Load the saved project, resolve the requested model (ask only if the project has
multiple models), and use its active configuration set. Apply the manifest's:

When the capability gate found a MATLAB MCP server, execute these operations with
that MCP in the existing MATLAB session. Do not replace it with a local CLI run.

```matlab
configset.CompileOptions.DefaultSpeciesDimension = settings.CompileOptions.DefaultSpeciesDimension;
configset.CompileOptions.DimensionalAnalysis = settings.CompileOptions.DimensionalAnalysis;
configset.CompileOptions.UnitConversion = settings.CompileOptions.UnitConversion;
configset.SolverOptions.AbsoluteTolerance = settings.SolverOptions.AbsoluteTolerance;
configset.SolverOptions.RelativeTolerance = settings.SolverOptions.RelativeTolerance;
configset.SolverType = settings.SolverType;
configset.TimeUnits = settings.TimeUnits;
configset.StopTime = settings.StopTime;
configset.SolverOptions.OutputTimes = matlabOutputTimes;
```

Before simulation, inspect model doses. If any are inactive, tell the user their
names and ask whether to activate them for this in-memory parity run, keep their
saved state, or stop. Do not persist that choice. Run `sbiosimulate`, collect only
the selected series and their units, and write a compact MATLAB-results JSON:

```json
{
  "dose_decision": "activate inactive doses for this run",
  "time": { "unit": "second", "values": [0, 3600] },
  "series": [{ "id": "Tumor", "unit": "mole", "values": [1, 2] }]
}
```

`time.unit` must reflect the MATLAB output time unit; each series ID must match
the selected Jinkō ID exactly. A missing component or unsupported unit conversion
is a mapping failure, not a reason to guess.

## Compare and report

Invoke the helper's `compare` command with the Jinkō and MATLAB JSON files. It:

- converts compatible `mole`/`substance_count` values using Avogadro's constant;
- converts common time units before alignment;
- retains the final value at each duplicate Jinkō timestamp (the post-event state)
  for pointwise matching, then integrates on unique increasing times;
- reports pointwise maximum absolute/relative error and mismatch count using
  `abs <= 1e-8 + 1e-6 * abs(jinko)` as diagnostics;
- computes trapezoidal Jinkō and MATLAB AUCs, and marks relative AUC error above
  1% as `WARN`. If the reference AUC is zero, report absolute AUC error and AUC
  status `N/A`; if any selected series has zero reference AUC, the overall status
  is also `N/A`, never an unqualified `PASS`.

Present `comparison.md` as the compact result table. Make the AUC status the
headline result; explain that pointwise mismatches can reflect solver/event-time
differences. Keep `comparison.json` and `comparison.csv` as run artifacts,
including units, conversions, selected outputs, and duplicate-time policy.

## Failure handling

- Stop with the specific precondition when settings, output IDs, or time alignment
  are missing. Do not continue with inferred values.
- Require explicit, compatible units and finite numeric time-series values. A
  missing unit, NaN, or infinity is a failed comparison input, not agreement.
- Keep selection at one to ten requested outputs. `Time` is mandatory internally.
- Do not edit the Jinkō model, its solving options, or the source project.
- Without MATLAB MCP, give the minimum commands for the current project and ask
  only for the MATLAB-results JSON needed by the helper; do not create a new
  persistent user workflow.
