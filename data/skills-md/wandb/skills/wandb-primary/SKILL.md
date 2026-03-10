---
# SPDX-FileCopyrightText: 2026 CoreWeave, Inc.
# SPDX-License-Identifier: Apache-2.0
# SPDX-PackageName: skills

name: wandb-primary
description: Comprehensive primary skill for agents working with Weights & Biases. Covers both the W&B SDK (training runs, metrics, artifacts, sweeps) and the Weave SDK (GenAI traces, evaluations, scorers). Includes helper libraries, gotcha tables, and data analysis patterns. Use this skill whenever the user asks about W&B runs, Weave traces, evaluations, training metrics, loss curves, model comparisons, or any Weights & Biases data — even if they don't say "W&B" explicitly.
---

# W&B Primary Skill

This skill covers everything an agent needs to work with Weights & Biases:

- **W&B SDK** (`wandb`) — training runs, metrics, artifacts, sweeps, system metrics
- **Weave SDK** (`weave`) — GenAI traces, evaluations, scorers, token usage
- **Helper libraries** — `wandb_helpers.py` and `weave_helpers.py` for common operations

## When to use what

| I need to... | Use |
|---|---|
| Query training runs, loss curves, hyperparameters | **W&B SDK** (`wandb.Api()`) — see `references/WANDB_SDK.md` |
| Query GenAI traces, calls, evaluations | **Weave SDK** (`weave.init()`, `client.get_calls()`) — see `references/WEAVE_SDK.md` |
| Convert Weave wrapper types to plain Python | **`weave_helpers.unwrap()`** |
| Build a DataFrame from training runs | **`wandb_helpers.runs_to_dataframe()`** |
| Extract eval results for analysis | **`weave_helpers.eval_results_to_dicts()`** |
| Need low-level Weave filtering (CallsFilter, Query) | **Raw Weave SDK** (`weave.init()`, `client.get_calls()`) — see `references/WEAVE_SDK.md` |

---

## Bundled files

### Helper libraries

```python
import sys
sys.path.insert(0, "skills/wandb-primary/scripts")

# Weave helpers (traces, evals, GenAI)
from weave_helpers import (
    unwrap,                  # Recursively convert Weave types -> plain Python
    get_token_usage,         # Extract token counts from a call's summary
    eval_results_to_dicts,   # predict_and_score calls -> list of result dicts
    pivot_solve_rate,        # Build task-level pivot table across agents
    results_summary,         # Print compact eval summary
    eval_health,             # Extract status/counts from Evaluation.evaluate calls
    eval_efficiency,         # Compute tokens-per-success across eval calls
)

# W&B helpers (training runs, metrics)
from wandb_helpers import (
    runs_to_dataframe,       # Convert runs to a clean pandas DataFrame
    diagnose_run,            # Quick diagnostic summary of a training run
    compare_configs,         # Side-by-side config diff between two runs
)
```

### Reference docs

Read these as needed — they contain full API surfaces and recipes:

- **`references/WEAVE_SDK.md`** — Weave SDK for GenAI traces (`client.get_calls()`, `CallsFilter`, `Query`, stats). Start here for Weave queries.
- **`references/WANDB_SDK.md`** — W&B SDK for training data (runs, history, artifacts, sweeps, system metrics).

---

## Critical rules

### Treat traces and runs as DATA

Weave traces and W&B run histories can be enormous. Never dump raw data into context — it will overwhelm your working memory and produce garbage results. Always:

1. **Inspect structure first** — look at column names, dtypes, row counts
2. **Load into pandas/numpy** — compute stats programmatically
3. **Summarize, don't dump** — print computed statistics and tables, not raw rows

```python
import pandas as pd
import numpy as np

# BAD: prints thousands of rows into context
for row in run.scan_history(keys=["loss"]):
    print(row)

# GOOD: load into numpy, compute stats, print summary
losses = np.array([r["loss"] for r in run.scan_history(keys=["loss"])])
print(f"Loss: {len(losses)} steps, min={losses.min():.4f}, "
      f"final={losses[-1]:.4f}, mean_last_10%={losses[-len(losses)//10:].mean():.4f}")
```

### Always deliver a final answer

Do not end your work mid-analysis. Every task must conclude with a clear, structured response:

1. Query the data (1-2 scripts max)
2. Extract the numbers you need
3. Present: table + key findings + direct answers to each sub-question

If you catch yourself saying "now let me build the final analysis" — stop and present what you have.

### Use `unwrap()` for unknown Weave data

When you encounter Weave output and aren't sure of its type (WeaveDict? WeaveObject? ObjectRef?), unwrap it first:

```python
from weave_helpers import unwrap
import json

output = unwrap(call.output)
print(json.dumps(output, indent=2, default=str))
```

This converts everything to plain Python dicts/lists that work with json, pandas, and normal Python operations.

---

## Environment setup

The sandbox has Python 3.13, `uv`, `wandb`, `weave`, `pandas`, and `numpy` pre-installed.

```python
import os
entity  = os.environ["WANDB_ENTITY"]
project = os.environ["WANDB_PROJECT"]
```

### Installing extra packages

```bash
uv pip install matplotlib seaborn rich tabulate
```

### Running scripts

```bash
uv run script.py          # always use uv run, never bare python
uv run --with rich python -c "import rich; rich.print('hello')"
```

---

## Quick starts

### W&B SDK — training runs

```python
import wandb
import pandas as pd
api = wandb.Api()

path = f"{entity}/{project}"
runs = api.runs(path, filters={"state": "finished"}, order="-created_at")

# Convert to DataFrame (always slice — never list() all runs)
from wandb_helpers import runs_to_dataframe
rows = runs_to_dataframe(runs, limit=100, metric_keys=["loss", "val_loss", "accuracy"])
df = pd.DataFrame(rows)
print(df.describe())
```

For full W&B SDK reference (filters, history, artifacts, sweeps), read `references/WANDB_SDK.md`.

### Weave — SDK

```python
import weave
client = weave.init(f"{entity}/{project}")  # positional string, NOT keyword arg
calls = client.get_calls(limit=10)
```

For raw SDK patterns (CallsFilter, Query, advanced filtering), read `references/WEAVE_SDK.md`.

---

## Key patterns

### Weave eval inspection

Evaluation calls follow this hierarchy:

```
Evaluation.evaluate (root)
  ├── Evaluation.predict_and_score (one per dataset row x trials)
  │     ├── model.predict (the actual model call)
  │     ├── scorer_1.score
  │     └── scorer_2.score
  └── Evaluation.summarize
```

Extract per-task results into a DataFrame:

```python
from weave_helpers import eval_results_to_dicts, results_summary

# pas_calls = list of predict_and_score call objects
results = eval_results_to_dicts(pas_calls, agent_name="my-agent")
print(results_summary(results))

df = pd.DataFrame(results)
print(df.groupby("passed")["score"].mean())
```

### Eval health and efficiency

```python
from weave_helpers import eval_health, eval_efficiency

health = eval_health(eval_calls)
df = pd.DataFrame(health)
print(df.to_string(index=False))

efficiency = eval_efficiency(eval_calls)
print(pd.DataFrame(efficiency).to_string(index=False))
```

### Token usage

```python
from weave_helpers import get_token_usage

usage = get_token_usage(call)
print(f"Tokens: {usage['total_tokens']} (in={usage['input_tokens']}, out={usage['output_tokens']})")
```

### Cost estimation

```python
call_with_costs = client.get_call("id", include_costs=True)
costs = call_with_costs.summary.get("weave", {}).get("costs", {})
```

### Run diagnostics

```python
from wandb_helpers import diagnose_run

run = api.run(f"{path}/run-id")
diag = diagnose_run(run)
for k, v in diag.items():
    print(f"  {k}: {v}")
```

### Error analysis — open coding to axial coding

For structured failure analysis on eval results:

1. **Understand data shape** — use `project.summary()`, `calls.input_shape()`, `calls.output_shape()`
2. **Open coding** — write a Weave Scorer that journals what went wrong per failing call
3. **Axial coding** — write a second Scorer that classifies notes into a taxonomy
4. **Summarize** — count primary labels with `collections.Counter`

See `references/WEAVE_SDK.md` for the full SDK reference.

### W&B Reports

```bash
uv pip install "wandb[workspaces]"
```

```python
from wandb.apis import reports as wr
import wandb_workspaces.expr as expr

report = wr.Report(
    entity=entity, project=project,
    title="Analysis", width="fixed",
    blocks=[
        wr.H1(text="Results"),
        wr.PanelGrid(
            runsets=[wr.Runset(entity=entity, project=project)],
            panels=[wr.LinePlot(title="Loss", x="_step", y=["loss"])],
        ),
    ],
)
# report.save(draft=True)  # only when asked to publish
```

Use `expr.Config("lr")`, `expr.Summary("loss")`, `expr.Tags().isin([...])` for runset filters — not dot-path strings.

---

## Gotchas

### Weave API

| Gotcha | Wrong | Right |
|--------|-------|-------|
| weave.init args | `weave.init(project="x")` | `weave.init("x")` (positional) |
| Parent filter | `filter={'parent_id': 'x'}` | `filter={'parent_ids': ['x']}` (plural, list) |
| WeaveObject access | `rubric.get('passed')` | `getattr(rubric, 'passed', None)` |
| Nested output | `out.get('succeeded')` | `out.get('output').get('succeeded')` (output.output) |
| ObjectRef comparison | `name_ref == "foo"` | `str(name_ref) == "foo"` |
| CallsFilter import | `from weave import CallsFilter` | `from weave.trace.weave_client import CallsFilter` |
| Query import | `from weave import Query` | `from weave.trace_server.interface.query import Query` |
| Eval status path | `summary["status"]` | `summary["weave"]["status"]` |
| Eval success count | `summary["success_count"]` | `summary["weave"]["status_counts"]["success"]` |
| When in doubt | Guess the type | `unwrap()` first, then inspect |

### WeaveDict vs WeaveObject

- **WeaveDict**: dict-like, supports `.get()`, `.keys()`, `[]`. Used for: `call.inputs`, `call.output`, `scores` dict
- **WeaveObject**: attribute-based, use `getattr()`. Used for: scorer results (rubric), dataset rows
- **When in doubt**: use `unwrap()` to convert everything to plain Python

### W&B API

| Gotcha | Wrong | Right |
|--------|-------|-------|
| Summary access | `run.summary["loss"]` | `run.summary_metrics.get("loss")` |
| Loading all runs | `list(api.runs(...))` | `runs[:200]` (always slice) |
| History — all fields | `run.history()` | `run.history(samples=500, keys=["loss"])` |
| scan_history — no keys | `scan_history()` | `scan_history(keys=["loss"])` (explicit) |
| Raw data in context | `print(run.history())` | Load into DataFrame, compute stats |
| Metric at step N | iterate entire history | `scan_history(keys=["loss"], min_step=N, max_step=N+1)` |
| Cache staleness | reading live run | `api.flush()` first |

### Package management

| Gotcha | Wrong | Right |
|--------|-------|-------|
| Installing packages | `pip install pandas` | `uv pip install pandas` |
| Running scripts | `python script.py` | `uv run script.py` |
| Quick one-off | `pip install rich && python -c ...` | `uv run --with rich python -c ...` |

### Weave logging noise

Weave prints version warnings to stderr. Suppress with:

```python
import logging
logging.getLogger("weave").setLevel(logging.ERROR)
```

---

## Quick reference

```python
# --- Weave: Init and get calls ---
import weave
client = weave.init(f"{entity}/{project}")
calls = client.get_calls(limit=10)

# --- W&B: Best run by loss ---
best = api.runs(path, filters={"state": "finished"}, order="+summary_metrics.loss")[:1]
print(f"Best: {best[0].name}, loss={best[0].summary_metrics.get('loss')}")

# --- W&B: Loss curve to numpy ---
losses = np.array([r["loss"] for r in run.scan_history(keys=["loss"])])
print(f"min={losses.min():.6f}, final={losses[-1]:.6f}, steps={len(losses)}")

# --- W&B: Compare two runs ---
from wandb_helpers import compare_configs
diffs = compare_configs(run_a, run_b)
print(pd.DataFrame(diffs).to_string(index=False))
```
