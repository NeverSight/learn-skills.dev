---
name: scientific-eda
description: Defensive exploratory data analysis for scientific data (CSV, FASTA, etc.). Context-first, human-guided; one plot at a time, ask why before executing, append-only journal per session, scripts with PEP723 and uv run, WebP plots. Use when opening data files for EDA or when the user wants guided scientific data exploration.
license: MIT
---

# Scientific exploratory data analysis

This skill guides **defensive**, **human-led** exploratory data analysis on scientific data. The agent does not open files and dump code; it captures problem context first, helps narrow to a single first step, takes instruction from the user, and asks "why?" before executing when the user requests a specific plot or table.

## Usage

Use this skill when the user provides one or more data files (CSV, FASTA, or other scientific formats) and wants to explore or analyze them. **Start by capturing context**—do not load or plot data until the problem (biological, chemical, or data-science question) is clearly stated and the agent is aligned as a guided assistant.

## Requirements

- **uv** for running Python scripts: every script uses PEP723 inline script metadata and is run with **`uv run script.py`**. Do not run ad-hoc Python or raw interpreters; each script declares and manages its own dependencies.
- Ability to read the relevant data formats (pandas, BioPython, etc.) via dependencies declared in the script block.

## What It Does

1. **Context first** – Capture and record the problem context (what question, what domain) before touching the data.
2. **Single first step** – Help the user narrow to **one** first plot or one first summary (not a barrage of code or plots).
3. **Human-guided execution** – Take instruction on what to do next; when the user says "make this plot" or "give me that table," **ask why** before doing it, then execute.
4. **Session layout** – Each analysis is a **session**: one folder under `analysis/` with a descriptive name and start date/time, containing `journal.md`, `plots/`, and `scripts/`.
5. **Journal** – Append-only `journal.md` per session: record data shape (columns, rows, structure), what was done, and findings.
6. **Scripts and plots** – Throwaway scripts in `scripts/` (PEP723, `uv run`); plots saved as **WebP** (not PNG) for small file size; all under the session folder.
7. **Suggest next step** – After each action, suggest the most logical next step and let the user decide.

## How It Works

### Phase 1: Capture context (before touching data)

- **Do not** open the data file and start coding or plotting.
- Ask for or confirm: the **problem context**—biological, chemical, or data-science question; what the user hopes to learn or decide; and any constraints (e.g. specific variables, subsets).
- Record this in the session’s `journal.md` (see Phase 3). Only after context is recorded and agreed, proceed to inspect data shape and plan the first step.

### Phase 2: Start a data analysis session

- Create **one session folder** under `analysis/` (or a project-agreed base). Name it **descriptive + ISO datetime** at session start, e.g. `analysis/2025-02-05T14-30-00-protein-binding/`.
- **Canonical layout** for each session folder:
  - `journal.md` – append-only running journal for this session
  - `plots/` – all figures (WebP only for matplotlib)
  - `scripts/` – disposable scripts that load data, summarize, or make plots
- Session folder name must include date/time and a short descriptive slug so sessions are sortable and identifiable. See [references/session-structure.md](references/session-structure.md) for the canonical tree.

### Phase 3: Journal (append-only, per session)

- **Before each substantive action**, read the session’s `journal.md`.
- **Record in the journal:**
  - **Data shape**: after loading or inspecting the data, jot columns (and types if relevant), row count, and any structure (e.g. multi-index, FASTA count, key fields). Do this as soon as shape is known and after any major data step.
  - What was done (which script, which plot, which summary)
  - Findings, surprises, and follow-up ideas
- Use a **timestamp** per entry (e.g. ISO or compact `YYYY-MM-DD HH:MM`).
- Tags like `[SHAPE]`, `[PLOT]`, `[FINDING]`, `[NEXT]` keep the journal scannable. The journal is the session’s memory; use it to suggest the next step.

### Phase 4: Understand shape, then one first step

- **Shape of the data**: Before proposing or making plots, ensure the agent (and user) knows: what columns/fields exist, how many rows/records, and any critical structure. Record this in `journal.md` under a `[SHAPE]` entry.
- **Single first plot (or table)**: Help the user choose **one** first visualization or summary (e.g. one distribution, one overview table). Do not generate many plots at once; get alignment on that single step, then execute.

### Phase 5: Human-guided execution and "ask why"

- **Take instruction**: The user may ask for a specific plot, table, or filter. Execute only after clarity.
- **Ask why before doing**: When the user says "make this plot" or "give me that table," briefly ask **why** (e.g. what decision or question it supports). Then run the script and record the outcome in the journal.
- **After each action**: Suggest the **most logical next step** (one step), and let the user confirm or redirect. Do not auto-execute a long pipeline.

### Phase 6: Scripts (disposable, PEP723, uv run)

- All Python used for this EDA lives in **scripts** under the session’s `scripts/` folder.
- **Every script** has **PEP723 inline script metadata** at the top (`# /// script`, `requires-python`, `dependencies`, `# ///`). Run with **`uv run script.py`** (or `uv run scripts/script_name.py` with CWD = session folder). Do **not** run raw `python` or paste code in a REPL; the script is the unit of execution and owns its environment.
- Scripts are **throwaway**: they are for this session’s plots and summaries, not production. Paths in scripts are relative to the session folder (e.g. `../data/file.csv` or as agreed).

### Phase 7: Plots (WebP only for matplotlib)

- Save **all matplotlib (and similar) figures as WebP**, not PNG, to keep image sizes small. Use e.g. `fig.savefig("plots/overview.webp", format="webp")`.
- Write plot files into the session’s **`plots/`** directory. Name files descriptively (e.g. `distribution_response.webp`, `first_ten_records.webp`).
- Reference these plots in the journal when you record what was done.

### When EDA is in a Marimo notebook

When the user conducts this EDA workflow in a **Marimo notebook** (instead of scripts in `scripts/`), follow the same phases above (context first, one step, journal, ask why). In addition:

- **Markdown before and after code**: For each code cell in the notebook, add **markdown cells before and after** that explain what the code does and what the results mean. The markdown before sets up intent; the markdown after summarizes or interprets the output.

See [references/marimo-notebook-eda.md](references/marimo-notebook-eda.md) for the canonical convention.

## Guardrails

1. **Context before data** – Do not open or analyze the data until the problem context is stated and recorded in the session journal.
2. **One first step** – Propose and agree on a single first plot or summary; do not generate a large block of code or many plots in one go.
3. **Ask why** – When the user requests a specific plot or table, ask why (what question or decision it serves) before executing.
4. **Journal as memory** – Read and append to the session’s `journal.md`; record data shape and findings so the next step is informed.
5. **Scripts only via uv run** – No ad-hoc Python; every script has PEP723 metadata and is run with `uv run script.py`.
6. **WebP for plots** – Use WebP for matplotlib (and similar) output; do not save as PNG by default.
7. **Suggest, don’t assume** – After each action, suggest one logical next step and wait for the user to confirm or change direction.
8. **Marimo notebooks** – When EDA is in a Marimo notebook, add markdown cells before and after each code cell to explain intent and results (see [references/marimo-notebook-eda.md](references/marimo-notebook-eda.md)).
