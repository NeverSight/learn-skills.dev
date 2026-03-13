---
name: trial-optimizer-graphical
description: "Optimize multiplicity control designs with a standalone, vendored trial_optimizer implementation (graphical procedures: alpha weights + transition matrix; optional group sequential/interim analyses with alpha spending). Use this skill whenever the user mentions trial_optimizer, graphical procedures, multiplicity/FWER, alpha allocation, transition matrices, or group sequential / interim analyses (O'Brien-Fleming, Pocock, Hwang-Shih-DeCani) and wants an optimized procedure or a reproducible optimization run."
---

# Trial Optimizer (Graphical + Sequential) Skill

Use this skill to turn a trial's *multiplicity problem statement* into a reproducible optimization run using the **standalone** `trial-optimizer-graphical` skill (it vendors the `trial_optimizer` Python package, so no separate repo checkout is required).

## What this skill produces
You will:
- Create a **JSON config** capturing the trial assumptions (effect sizes, correlation), objective (endpoint priorities / gating), and optimization parameters.
- Run a bundled runner script to produce:
  - `result.json` (optimal weights/transitions + Monte Carlo power metrics)
  - Optional plots (when dependencies are available):
    - `design_optimized.png` (graph visualization; needs `networkx`)
    - `training.png` (loss/objective history)

## Inputs you must confirm with the user
Collect (or infer from context) the following:
- `m`: number of hypotheses/endpoints
- `alpha`: one-sided familywise error rate (often 0.025)
- `effect_sizes`: expected Z-scale effects (length `m`)
- `correlation`: either a scalar equicorrelation (e.g. 0.3) or a full `m x m` correlation matrix
- Objective:
  - **weights**: relative importance per endpoint (length `m`)
  - optional **gating dependencies**: hierarchical rules like "H2 only counts if H1 succeeds"
- Whether this is **single-stage** (default) or **group sequential**:
  - `n_analyses`, `information_fractions`
  - spending function choice (OBF / Pocock / Linear / HSD(gamma)) and whether to optimize HSD gamma

If the user is unsure, default to:
- objective = weighted marginal rejection with equal weights
- single-stage (non-sequential)

## Workflow
### 1) Install Python dependencies
This skill vendors the `trial_optimizer` code, but you still need its Python dependencies installed in whatever environment you run the script.

Minimal install (PowerShell):
```powershell
python -m pip install --upgrade pip
python -m pip install torch numpy scipy matplotlib tqdm
```

Optional (only for the graph PNG):
```powershell
python -m pip install networkx
```

### 2) Create a config JSON
Start from one of the examples in `references/`:
- `references\config_example_graphical.json`
- `references\config_example_sequential.json`
- `references\config_example_gated.json`

Copy one next to where you want outputs, then edit it.

### 3) Run the optimization
From anywhere (using an explicit interpreter):
```powershell
$py = "<path-to-python-interpreter>"  # e.g. .\.venv\Scripts\python.exe on Windows
& $py <path-to-skill-dir>\scripts\run_trial_optimizer.py `
  --config .\trial_optimizer_config.json `
  --outdir .\trial_optimizer_out
```

### 4) Report results back to the user
Always include:
- Optimal weights (sum to 1)
- Transition matrix (rows should sum to <= 1)
- Benchmark power metrics (marginal, disjunctive, conjunctive, expected rejections)
- The output directory with artifacts

## Notes / gotchas
- The upstream project has migrated to the new objective API (`WeightedSuccess`, `MarginalRejection`, `GatedSuccess`). Avoid legacy objective class names.
- Optimization is stochastic; for "final" numbers, increase `benchmark.n_simulations` and consider increasing `optimizer.n_eval_samples`.
- For sequential designs, confirm information fractions are sensible and monotone increasing to 1.0.
