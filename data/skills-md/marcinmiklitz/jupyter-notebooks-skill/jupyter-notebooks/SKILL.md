---
name: jupyter-notebooks
description: |
  Build, manipulate, execute, validate, and version-control Jupyter notebooks
  programmatically. Use when working with .ipynb files, creating notebooks from
  code, running parameterised analyses, diffing/merging notebooks in git,
  stripping outputs, or converting notebooks to other formats. Triggers on:
  jupyter, notebook, ipynb, nbformat, nbconvert, nbclient, papermill, nbdime,
  cell, kernel, execute notebook, parameterise, notebook diff, notebook merge.
license: MIT
metadata:
  author: marcinmiklitz
  version: "0.1.0"
---

# Jupyter Notebooks Skill

Programmatic notebook operations from CLI only (no Jupyter UI):
- create notebooks and templates,
- perform cell-level CRUD and metadata edits,
- execute whole notebooks or selective ranges,
- validate structure and operational notebook hygiene,
- convert formats,
- inspect/strip outputs,
- run content-aware diff and merge.

Python requirement: **3.9+**.

## Dependencies and Invocation

Scripts require these Python packages:

- **Core:** `nbformat`, `nbclient`, `nbconvert`, `nbdime`
- **Optional:** `papermill`, `nbstripout`

Each script declares its own dependencies via PEP 723 inline metadata (the `# /// script` block at the top of each file). Read this block to determine exactly which packages a script needs.

### Before first use

Run the preflight check to verify environment readiness:

```bash
python scripts/nb_preflight.py --mode auto
```

This script has no dependencies (stdlib only). It supports `--mode auto|python|uv`:
- `auto` (default): succeed if either Python-mode or uv-mode is ready,
- `python`: check interpreter package availability directly,
- `uv`: verify `uv run` readiness by smoke-testing all script `--help` entrypoints.

It emits a JSON report to stdout with `ok`, `ok_python`, `ok_uv`, `ok_execute`, and mode-specific details.

If packages are missing:

1. Determine the project's package manager by inspecting the environment (look for `pyproject.toml`, `requirements.txt`, `Pipfile`, `uv.lock`, `poetry.lock`, or similar).
2. Install the missing packages using that tooling. If you lack permission or are unsure, ask the user.
3. Re-run `nb_preflight.py` to confirm.

Do not skip or abandon a script because its dependencies are not currently installed. Resolve them first.

### How to invoke

Run scripts with whatever Python interpreter the project environment provides:

```bash
python scripts/<tool>.py [args]
```

If the project uses a tool that handles PEP 723 inline metadata automatically (e.g. `uv run`), that works too — the metadata block in each script is compatible.

### Additional requirements

- Execution (`nb_execute.py`) requires a Jupyter kernel (typically `ipykernel`).
- PDF export depends on external tools (pandoc/TeX or webpdf stack) beyond Python packages.

## Script Map

- `scripts/nb_create.py`: Create notebook from blank/template/script; inject script as one cell into existing notebook.
- `scripts/nb_cells.py`: Cell CRUD, reorder, metadata/tags, bulk ops, regex search.
- `scripts/nb_execute.py`: Execute with `nbclient` (default), selective range execution, or papermill mode.
- `scripts/nb_validate.py`: Schema validation + operational lint checks for CI/pre-commit.
- `scripts/nb_convert.py`: Convert notebook to html/pdf/latex/script/markdown/rst/slides.
- `scripts/nb_metadata.py`: Notebook/cell metadata and tag management.
- `scripts/nb_outputs.py`: Output listing, size checks, stripping, image extraction, clear execution counts.
- `scripts/nb_diff.py`: nbdime-backed diff (text/json) and three-way merge.

## Task Routing

- Create new notebook/template/script-to-notebook:
- Use `scripts/nb_create.py`.
- Inspect or mutate cell layout/content:
- Use `scripts/nb_cells.py`; details in `references/cell-operations.md`.
- Execute notebook:
- Use `scripts/nb_execute.py`; decision guidance in `references/execution-guide.md`.
- Parameterized runs:
- Use `scripts/nb_execute.py --papermill`; patterns in `references/papermill-patterns.md`.
- Validate for CI:
- Use `scripts/nb_validate.py`; rules in `references/validation-and-linting.md`.
- Export to document/script formats:
- Use `scripts/nb_convert.py`.
- Manage metadata/tags:
- Use `scripts/nb_metadata.py`; schema map in `references/metadata-reference.md`.
- Handle outputs/size/images:
- Use `scripts/nb_outputs.py`; guidance in `references/output-handling.md`.
- Diff/merge in git workflows:
- Use `scripts/nb_diff.py`; setup in `references/versioning-guide.md`.
- Failure/timeout/kernel issues:
- See `references/error-handling.md`.

## Quick-Reference Table

- Create notebook: `nb_create.py`
- Edit cells: `nb_cells.py`
- Execute notebook: `nb_execute.py`
- Validate notebook: `nb_validate.py`
- Convert/export: `nb_convert.py`
- Metadata/tag ops: `nb_metadata.py`
- Output management: `nb_outputs.py`
- Diff/merge: `nb_diff.py`

## Quick-Start One-Liners

Create from template:

```bash
python scripts/nb_create.py --template data-analysis --output notebooks/0.1-mmk-initial-eda.ipynb
```

Add a code cell:

```bash
python scripts/nb_cells.py --input notebooks/0.1-mmk-initial-eda.ipynb add --cell-type code --source "print('hello')"
```

Execute selective range (cornerstone pattern):

```bash
python scripts/nb_execute.py --input notebooks/0.1-mmk-initial-eda.ipynb --start-index 3 --end-index 7
```

Validate for CI:

```bash
python scripts/nb_validate.py --input notebooks/0.1-mmk-initial-eda.ipynb --forbid-outputs
```

Convert to markdown:

```bash
python scripts/nb_convert.py --input notebooks/0.1-mmk-initial-eda.ipynb --to markdown --output reports/eda.md
```

## Output Convention

Scripts follow a consistent contract:
- Human-readable progress logs on **stderr**.
- Machine-readable JSON payload on **stdout**.
- Exit codes:
- general scripts: `0` success, `1` error.
- `nb_validate.py`: `0` no issues, `1` issues found, `2` runtime/tool failure.

## Versioning Defaults

- Use CCDS-style notebook naming for order and ownership:
- `<step>-<owner>-<description>.ipynb`
- Prefer `nbstripout` + `nbdime` together for repository hygiene and readable diffs.
- Example `.gitattributes` is provided in `assets/.gitattributes.example`.
