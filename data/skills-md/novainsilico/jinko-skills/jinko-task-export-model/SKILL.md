---
name: jinko-task-export-model
description: >-
  Export a Jinkō computational model to another modeling tool and check the
  export numerically against Jinkō simple_solve. Targets: SBML, SimBiology code
  (a MATLAB script that uses SimBiology), SimBiology XLSX, Julia
  (DifferentialEquations.jl), and nlmixr2/rxode2 in R. Use this skill whenever
  the user wants to download, export, transfer, or convert a Jinkō model to
  SBML, MATLAB, SimBiology, Julia, R, nlmixr2, or rxode2, to run a Jinkō model
  outside Jinkō, to check that an exported model reproduces Jinkō, or to
  investigate why another solver diverges from Jinkō. Use it even when the user
  gives only a model link or short ID and names the tool.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Needs pint for the comparison
  (`pip install pint`). Each check needs the runtime of its target: libroadrunner for
  SBML, MATLAB with SimBiology (an MCP server or a local install) for
  SimBiology, Julia with DifferentialEquations.jl, or R with rxode2 and
  nlmixr2. Downloads alone need no runtime. The optional report needs
  matplotlib.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.17,<2.0"
license: MIT
---

# Export a Jinkō model

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and
> an SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup`
> skill (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes.
> If that skill is not found, install it from `novainsilico/jinko-skills`.

The user gets two things: the exported files, and an honest statement of how
far the export reproduces Jinkō. An export that was not run is not a checked
export. Say which one the user has.

## Targets

| User asks for | Target | Check runtime | Read |
| --- | --- | --- | --- |
| SBML | `sbml` | libroadrunner (Python) | `references/sbml.md` |
| MATLAB, SimBiology, `.m` script | `simbiology-code` | MATLAB with SimBiology | `references/simbiology.md` |
| SimBiology Excel, workbook, Model Builder | `simbiology-xlsx` | MATLAB with SimBiology | `references/simbiology.md` |
| Julia | `julia` | Julia | `references/julia.md` |
| R, nlmixr2, rxode2 | `nlmixr2` | R | `references/nlmixr2.md` |

Read the reference of the chosen target before you run it. For "MATLAB" or
"SimBiology" without more detail, use `simbiology-code`: it needs no manual
step. Jinkō does not export plain MATLAB code without SimBiology. When the user
asks for that, or for any other tool, say so and list the targets above.

## Workflow

`scripts/export_check.py` does the file handling and the maths. Use it, do not
present it to the user as a tool to learn. One run directory holds one export.
Use a dedicated folder in the workspace, such as `exports/<cm-sid>/<target>/`,
unless the user named one.

1. **Export.** `export <cm> --target <target> --output-dir <dir>`. Link the
   exported files. Report every conversion warning from the manifest: each one
   is a place where the export may differ from Jinkō. For a download-only
   request, stop here and say that no check ran.
2. **Choose the series.** `list-series <cm>` lists the time-dependent series.
   Use the ones the user named. Otherwise propose the model outputs (or a few
   species and observables) and let the user change them.
3. **Jinkō reference.** `reference --dir <dir> --ids <series...>`.
4. **Run the export.** Use the runner of the target (see its reference). For
   SimBiology, look for a MATLAB MCP server before any other MATLAB. If
   the runtime is missing, say what to install (the target reference has the
   commands) and ask. Do not install anything without the user's consent.
5. **Compare.** `compare --dir <dir>`. Show `comparison.md`. The comparison
   needs `pint` in the Python environment of the SDK (`pip install pint`).
6. **Report, only when the user asks for one.** `report --dir <dir>` writes
   `report.md` with a plot per series in `plots/` (needs matplotlib). To share
   it, publish it next to the model with `jinko-document`
   (`python -m jinko.cli.create_document_from_markdown`). Do not offer a report
   for a check nobody asked for.

## Rules for the check

- **Gate.** A series passes when its largest point-wise relative error against
  Jinkō is at most 1e-3, with a floor of 1e-5 times the Jinkō peak. Cmax and
  AUC errors are diagnostics: a structural error can keep the AUC and change
  the shape. Do not report PASS on Cmax or AUC alone.
- **Units.** Exports hold species as amounts in the extent unit. The script
  converts them to the Jinkō unit with the compartment volume and the molar
  mass. A conversion it cannot do is a failed input, not agreement.
- **Events.** At an event time, solvers report the state before or after the
  event. The script compares the closer one and counts these event points. The
  first time point is not compared.
- **A failure has a cause to find.** Check the Jinkō side first: Jinkō solves
  with the model's own tolerances, and its absolute tolerance applies to
  amounts in the extent unit. Tiny amounts (for example 1e-9 mol) then carry a
  large relative error in Jinkō itself. The export runner solves tightly
  (relative 1e-10). To confirm, and only with the user's consent, copy the
  model (`model.copy()`), tighten the copy's solving options
  (`edit_solving_options`), and check the copy. Never edit the user's model.
- **An export that does not run is the finding.** When the runner fails
  inside the exported program (a syntax error, a solver error), report the
  error as an export defect. Do not repair the exported file to make it pass.
- **Report what is true.** PASS, FAIL with the worst series and error, or no
  check with the reason. Name the series that were not checked. Link
  `comparison.json`. A divergence that remains with tight tolerances is a
  finding: say which construct is likely involved (events, conditional logic,
  unit conversion) and offer to report it.
