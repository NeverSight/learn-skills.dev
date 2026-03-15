---
name: ml-experimentation
description: Conduct machine learning experiments from planning through evaluation and report writing. Use when running ML experiments, testing hypotheses, training models, or writing up results. Covers single-hypothesis scoping, fast iteration loops, targeted logging, JOURNAL.md protocol, data-backed diagnostic plots, and scientific report writing.
license: MIT
---

# ML Experimentation

This skill guides a hypothesis-driven ML experiment life cycle: planning, fast iteration, script execution, targeted logging, journaling, diagnostic visualization, and scientific report writing.

## Usage

Use this skill when the user wants to run an ML experiment, test a model or idea, or write up experiment results. **First decide:** new experiment (different question → new experiment directory) or new run (same question, tweaks → new run under `runs/`). See [references/experiment-setup.md](references/experiment-setup.md) for that disambiguation, hypothesis scoping, and the fast-iteration checklist.

## Requirements

- Python 3.11+ with **uv** or **pixi** for running scripts: `uv run script.py` or, when pixi is the environment manager, `pixi run python script.py` (pixi reads `pyproject.toml` or `pixi.toml`).
- Dependencies declared via PEP723 inline script metadata in each script (or, with pixi, in pyproject.toml / pixi.toml).
- **Respect the user's training framework** (PyTorch, JAX, TensorFlow, etc.). **Run scripts in a GPU-enabled environment wherever possible**: with uv use GPU-enabled deps (e.g. JAX GPU extras, PyTorch via `[[tool.uv.index]]` CUDA index in the script block); with pixi use a GPU-enabled environment defined in pyproject.toml or pixi.toml. Fall back to CPU only when GPU is unavailable. See [references/script-patterns.md](references/script-patterns.md).

## What It Does

1. **Planning** – Decide new experiment (different question) vs new run (same question, tweaks). Extract one testable hypothesis, define success criteria, identify metrics to log; create experiment directory and JOURNAL.md (new experiment) or add a run under `runs/` (new run).
2. **De-risking** – Keep runs under ~60 seconds; scale down data, epochs, or model size before longer runs
3. **Scripts** – Disposable scripts with PEP723 metadata, run with `uv run` or `pixi run` (GPU-enabled environment preferred)
4. **Logging** – Log only what the hypothesis needs; avoid verbose or redundant logs
5. **Journal** – Read JOURNAL.md before each action; record observations, anomalies, hunches
6. **Plots and report** – Generate plots from logged data only; write a scientific report (abstract, intro, methods, results, discussion, conclusion) with no hallucination or editorialization

## How It Works

### Phase 1: Experiment Planning

- **New experiment vs new run:** If the user is answering a **different question** → start a new experiment (new directory, JOURNAL.md, canonical tree). If they are **tweaking to answer the same question** → add a new run under the existing experiment; name it **full ISO datetime + descriptive string** `YYYY-MM-DDTHH-MM-SS-<descriptive-string>` (e.g. `runs/2025-02-03T09-00-00-retry`). See [references/experiment-setup.md](references/experiment-setup.md).
- Extract a **single, testable hypothesis** from the user’s goal. Reject vague or multi-part goals; narrow to one claim that can be verified.
- Define **success and failure criteria** before running anything.
- List **metrics to log** that map directly to the hypothesis and criteria.
- For a **new experiment:** Create an experiment directory and add **JOURNAL.md** (see Phase 5). Use the **canonical tree**: experiment → `runs/YYYY-MM-DDTHH-MM-SS-<descriptive-string>/` → `logs/`, `plots/`, `checkpoints/`, `data/`. For a **new run:** Create only the new run directory under `runs/` (e.g. `runs/2025-02-03T09-00-00-retry/`) with `logs/`, `plots/`, `checkpoints/`, `data/`.

### Phase 2: De-risking Loop (Fast Iteration)

- **Target: single run completes in under 60 seconds.** If a run would take longer, scale down first.
- Scale down by: smaller data subset (representative, not just “first N”), fewer epochs, simpler or smaller model, or fewer evaluation steps.
- Sanity-check data loading, training loop, and evaluation on the scaled-down setup before committing to longer runs.
- If something would take > 2 minutes, find a proxy that finishes in under 1 minute.
- Before each run, verify the fast-iteration checklist in [references/experiment-setup.md](references/experiment-setup.md).
- **Each run is a directory under `runs/`** named **full ISO datetime + descriptive string** **`YYYY-MM-DDTHH-MM-SS-<descriptive-string>`** (e.g. `runs/2025-02-02T14-30-00-de-risk`, `runs/2025-02-02T15-00-00-full`, `runs/2025-02-03T09-00-00-retry`). Keep a running log; never overwrite an existing run. See [references/experiment-setup.md](references/experiment-setup.md) for the canonical tree.
- To **ignore failed or irrelevant runs** without deleting: list them in `IGNORED_RUNS.md` (or JOURNAL.md “Ignored runs”). See [references/experiment-setup.md](references/experiment-setup.md).

### Phase 3: Script Execution

- All Python scripts use **PEP723 inline script metadata** and are run with **`uv run script.py`** or, when pixi is the environment manager, **`pixi run python script.py`** (pixi uses `pyproject.toml` or `pixi.toml`). **Always run train/eval in a GPU-enabled environment when possible** (uv: CUDA index or jax[cuda*] in script block; pixi: GPU-enabled env in pyproject.toml or pixi.toml).
- **Run scripts with CWD = experiment directory** so paths like `runs/2025-02-02T14-30-00-de-risk`, `runs/2025-02-02T15-00-00-full` are relative to the experiment. Scripts **accept only the descriptive name** (e.g. `uv run train.py de-risk` or `pixi run python train.py de-risk`); **datetime is auto-calculated**. The **training script** (`train.py`) **creates the run directory** (logs/, plots/, checkpoints/, data/) so the experiment is **self-contained**—no external scaffold; see [references/script-patterns.md](references/script-patterns.md) for the Typer-based train scaffold.
- **Longer runs:** When executing a run that will take more than a minute or two, **pass a custom timeout** to the shell/bash tool used to run the script (e.g. the tool’s `timeout` parameter), otherwise the tool may hit its default execution timeout and the run may be killed before completion.
- Scripts are **disposable**: they are experiment artifacts, not production code. Include any **synthetic data generation** scripts in `<experiment>/` (e.g. `generate_data.py`); run them with CWD = experiment directory.
- **Train and eval scripts:** Use the user's chosen framework and **prefer GPU-enabled dependencies** (JAX GPU extras, PyTorch via `[[tool.uv.index]]` CUDA index when using uv; GPU deps in pyproject.toml/pixi.toml when using pixi) so runs are performant; fall back to CPU only when GPU is unavailable.
- Use the patterns in [references/script-patterns.md](references/script-patterns.md) for data loading, training, and evaluation.

### Phase 4: Logging (Targeted)

- Log **only what the hypothesis and success criteria need**.
- Required: metrics that determine success/failure (e.g. loss, accuracy, F1).
- Optional: diagnostics that could explain unexpected results (e.g. per-batch stats, timing).
- Avoid: verbose debug logs, full model state, gradients (unless the hypothesis is about them).
- Use **loguru** for logging; write to the run’s **`logs/`** directory (e.g. `runs/2025-02-02T14-30-00-de-risk/logs/train.log`, `runs/2025-02-02T15-00-00-full/logs/eval.log`). See [references/logging-guide.md](references/logging-guide.md).

### Phase 5: JOURNAL.md Protocol

- **Before each action** (next run, next script, next analysis): read JOURNAL.md.
- Record: observations, anomalies, unexpected behavior, hunches, follow-ups.
- Add a **timestamp** to each entry.
- Use tags: `[WEIRD]`, `[HUNCH]`, `[TODO]`, `[RESOLVED]` so entries are scannable.
- The journal is the primary memory for the experiment; use it to decide the next step and to inform the Discussion section of the final report.

### Phase 6: Diagnostic Plots and Reporting

**Plots**

- **Before plotting:** Read `IGNORED_RUNS.md` (and JOURNAL.md’s “Ignored runs” section if present); exclude any listed runs from plots.
- Generate **only** plots that correspond to **logged data**. Do not invent or assume data.
- Examples: training curves (loss/accuracy vs step/epoch), metric distributions, comparison bars.
- Save plots in the run’s **`plots/`** directory (e.g. `runs/2025-02-02T15-00-00-full/plots/loss_curve.webp`), generated from that run’s `logs/`.
- If you log epoch and loss to e.g. `runs/2025-02-02T15-00-00-full/logs/train.log`, generate `runs/2025-02-02T15-00-00-full/plots/loss_curve.webp` from that log; do not plot quantities that were not logged.

**Scientific Report**

- **Before writing:** Exclude runs listed in `IGNORED_RUNS.md` or JOURNAL.md “Ignored runs” from the report narrative and figures; do not delete those runs from disk.
- Structure: **Abstract**, **Introduction**, **Methods**, **Results**, **Discussion**, **Conclusion**.
- **No hallucination**: only refer to data that was actually collected (cite log files, tables, figures).
- **No editorialization**: state what happened and what the data show; do not state what you wish had happened.
- Include highlights from JOURNAL.md (e.g. anomalies, resolved issues) in Discussion.
- Use the template in [references/report-template.md](references/report-template.md).

## Guardrails

1. **No long runs without justification** – If a script would take > 2 minutes, either get explicit confirmation or propose a scaled-down run that finishes in under 1 minute. When running a longer run, **pass a custom timeout** to the shell/bash tool so it does not hit the default execution timeout.
2. **Journal-first** – Always read JOURNAL.md before suggesting or taking the next action.
3. **Data-backed plots only** – Never generate a plot without corresponding logged data; every curve or point must come from a specified log or file.
4. **Report factuality** – Every claim in the report must be tied to a specific log file, table, or figure; no unsupported claims.
