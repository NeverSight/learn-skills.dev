---
name: figures4papers-python-plot-skill
description: Use when generating or refactoring Python figure scripts in the ChenLiu-1996/figures4papers style, including assets/ outputs and figure_* source folders. Trigger for requests like "draw paper figure", "reproduce figure from script", "add a new figure module", or "batch-run plotting scripts with consistent publication-quality output settings."
---

# figures4papers-python-plot-skill

## Overview

Implement publication-ready Python plotting workflows using the `figures4papers` layout (`assets/` plus domain-specific `figure_*` directories).

## Workflow

1. Detect repository layout.
2. Create or update a dedicated `figure_*` folder for each figure task.
3. Keep plotting code deterministic and save outputs to `assets/`.
4. Run scripts and verify generated files exist and are non-empty.

## Layout Rules

- Keep rendered files in `assets/`.
- Keep source code in `figure_*` directories.
- Use stable output names under `assets/` (for example: `assets/figure_3.png`, `assets/figure_3.pdf`).
- Prefer one entry script per figure directory (for example: `figure_Dispersion/plot.py`).

## Repository Coverage

Cover these known folders from `ChenLiu-1996/figures4papers`:

- `figure_CellSpliceNet`
- `figure_Cflows`
- `figure_Dispersion`
- `figure_FPGM`
- `figure_ImmunoStruct`
- `figure_RNAGenScape`
- `figure_brainteaser`
- `figure_ophthal_review`

Cover these known README figure categories:

- Bar plots for quantitative comparison
- Composition and breakdown charts
- Trend/line plots
- Heat maps
- 3D sphere visualizations
- Miscellaneous examples

## Implementation Checklist

- Confirm Python environment and plotting dependencies are available.
- Add clear constants for seed, DPI, size, and output paths.
- Save at least one vector or high-resolution output (`.pdf` or high-DPI `.png`).
- Use `tight_layout()`/equivalent to avoid clipping labels.
- Exit with non-zero code on failed render.

## Quick Commands

```bash
python scripts/check_repo_coverage.py --root .
python scripts/run_figure.py --figure-dir figure_Dispersion --entry plot.py --out assets/figure_dispersion.png
```

## References

- Read `references/repo-style.md` before generating or refactoring figure folders.
