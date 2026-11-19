---
name: jinko-task-import-model
description: >-
  Import a model built in another modeling tool into Jinkō, check that Jinkō
  accepts and solves it, and, when the user asks, check it numerically against
  the source tool. Sources: SBML, SimBiology XLSX, a Monolix structural model,
  a Monolix project (.mlxtran), and a NONMEM run (.mod, .ctl, .lst, .ext,
  .phi, data set), which becomes a model, vpop, protocol design, output set,
  and trial checked against a declared reference. Routes a published paper to jinko-task-paper2model. Use
  this skill whenever the user wants to import, upload, port, translate, or
  migrate a model file or a NONMEM run into Jinkō, to bring a BioModels,
  COPASI, SimBiology, Monolix, or NONMEM model to Jinkō, to reproduce a
  population-PK model that exists as NONMEM code, or to check that an imported
  model reproduces its source tool, even when the user only gives a file path.
  Use jinko-model to author a model from scratch and jinko-task-export-model
  to go from Jinkō to another tool.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. The optional comparison needs
  pint (`pip install pint`) and the runtime of the source: libroadrunner for
  SBML, MATLAB with SimBiology for SimBiology, or a CSV of the source tool's
  results for Monolix and any other tool. NONMEM needs
  `pip install "jinko-sdk[nonmem2jinko]"`, and R with `nonmem2rx` and `rxode2`
  for its independent-parse check. The optional report needs matplotlib.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.17,<2.0"
license: MIT
---

# Import a model into Jinkō

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and
> an SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup`
> skill (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes.
> If that skill is not found, install it from `novainsilico/jinko-skills`.

The user gets a Jinkō model and an honest statement of what was established.
There are two different claims:

- **Jinkō accepts and solves the model**: the sanity check. A model can solve
  and still be wrong.
- **The Jinkō model reproduces the source tool**: the comparison, and nothing
  else.

Say which one the user has. Never call an import verified on the sanity check
alone.

## Routes

| Source | Route |
| --- | --- |
| SBML (`.xml`, `.sbml`) | `client.create_model_from_file()` |
| SimBiology XLSX | `client.create_model_from_file()` |
| Monolix structural model (Mlxtran with `[LONGITUDINAL]`, often `.txt`) | `client.create_model_from_file(..., file_format="monolix")` |
| Monolix project (`.mlxtran`) | `client.import_monolix_project()`: it also creates a simple output set and a trial |
| NONMEM (`.mod`, `.ctl`, `.lst`, `.ext`, `.phi`) | `python -m nonmem2jinko`. Read `references/nonmem.md` and follow it instead of the workflow below: it has its own checks |
| A paper, equations, or code with no import format | `jinko-task-paper2model` |

For any other format, say that Jinkō cannot import it and list the formats
above. Ask whether the source tool can export SBML. Do not translate a model
into Jinkō by hand under this skill: an unchecked translation looks like an
import.

## Workflow

1. **Import.** Confirm the model name and a dedicated destination folder with
   the user. Leave `trust_units` and `rename_ids` unset unless the user asks.
   Report every conversion warning: each one is a place where the import may
   differ from the source. A Monolix project creates items named `Untitled`:
   rename them.
2. **Sanity check.** `model.diagnostics.errors()` must be empty, and
   `model.simple_solve()` must return each series it is asked for. A Monolix
   structural model has no input values (they belong to the project), so its
   solve is NOT RUN, not failed. On a failure, stop. Present the diagnostic,
   the candidate fixes (see `jinko-model`), and a recommendation, then wait.
3. **Report.** Link the model with its `.url`. Say PASS, FAIL, or NOT RUN for
   the sanity check. Say that the imported model carries no Jinkō tags, and
   offer `jinko-model` to add the `output`, `i::*`, and `s::*` tags. Offer the
   comparison with the source tool. Do not run it unasked.

### Unit errors after an import

SBML often holds numbers without units, for example a dose `A + 3` or a
trigger `time >= 5`. With the default settings, Jinkō checks units and
reports these as `UNIT_CHECKING_ERROR`. Present the two options and let the
user choose:

- Keep unit checking and give the literals their units with `jinko-model`.
- Import again with `trust_units=False`. Jinkō then turns unit checking off
  (`NoUnitCheck`) and reports species as amounts.

## Comparison with the source tool

Run it only when the user asks. `scripts/import_check.py` does the file
handling and the maths. Use it, do not present it to the user as a tool to
learn. One run directory holds one comparison, for example
`imports/<cm-sid>/check/`.

1. **Choose the series.** `list-series <cm>` lists the time-dependent series.
   Use the ones the user named. Otherwise propose the model outputs, or a few
   species, and let the user change them.
2. **Jinkō side.** `reference <cm> --dir <dir> --ids <series...>`.
3. **Source side.** Read the reference of the source and run its step:

   | Source | Step | Read |
   | --- | --- | --- |
   | SBML | `run-sbml --dir <dir> --source <file>` | `references/sbml.md` |
   | SimBiology | `prepare-matlab --dir <dir> --project <.sbproj>` | `references/simbiology.md` |
   | Monolix, any other tool | `from-csv --dir <dir> --csv <file> --time-unit <unit>` | `references/csv.md` |

   If the runtime is missing, say what to install and ask. Do not install
   anything without the user's consent.
4. **Compare.** `compare --dir <dir>`. Show `comparison.md`.
5. **Report, only when the user asks for one.** `report --dir <dir>` writes
   `report.md` with a plot per series in `plots/` (needs matplotlib). To share
   it, publish it next to the model with `jinko-document`
   (`python -m jinko.cli.create_document_from_markdown`). Do not offer a report
   for a check nobody asked for.

## Rules for the comparison

- **Gate.** A series passes when its largest point-wise relative error against
  Jinkō is at most 1e-3, with a floor of 1e-5 times the Jinkō peak. Cmax and
  AUC errors are diagnostics. Do not report PASS on Cmax or AUC alone.
- **A failure has a cause to find.** Check the Jinkō side first. Jinkō solves
  with the model's own tolerances, and the default grid is coarse, so small
  values carry a large relative error in Jinkō itself. To confirm, and only
  with the user's consent, copy the model (`model.copy()`), tighten the copy's
  solving options, and check the copy. Never edit the user's model.
- **Do not edit the source to make it pass.** A divergence that remains is a
  finding: say which construct is likely involved (events, units, conditional
  logic) and offer to report it.
- **Report what is true.** PASS, FAIL with the worst series and error, or NOT
  RUN with the reason. Name the series that were not checked. Link
  `comparison.json`.
