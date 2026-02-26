---
name: notebook-ai-agents-skill
description: Create/refactor reproducible analysis notebooks with Marimo (preferred) or Jupyter (minimal support). Use for interactive, narrative-first analyses.
---

# Notebook AI Agents Skill (Marimo First)

Build narrative-first, reproducible notebooks with strict run-all validation and clean data loading patterns. Prefer Marimo for new notebooks; support Jupyter only when needed for existing .ipynb files.

## Instructions

1. Prefer Marimo for new work. Create a `.py` notebook and keep cells small and deterministic.
2. Outline the notebook (purpose, data sources, analysis steps, outputs) before coding.
3. Use project-relative paths and DuckDB for data loading (TSV/Parquet preferred).
4. Build plots with the shared style rules.
5. Validate by running the notebook end-to-end (Marimo: `marimo run`; Jupyter: restart kernel + run all).

## Quick Reference

| Task | Action |
|------|--------|
| Marimo docs | https://docs.marimo.io/ |
| Jupyter (legacy) | See `docs/notebook_structure.md` |
| Pixi + Jupyter (legacy) | See `docs/pixi_jupyter.md` |
| Data loading | See `docs/data_loading_duckdb.md` |
| Plot styling | See `docs/plot_style.md` |
| Validation | See `docs/verification.md` |
| Templates (legacy) | `templates/kiss_notebook_template.py` |

## Input Requirements

- Notebook scope and goals
- Data file paths (TSV/Parquet preferred)
- Python environment (Pixi recommended)
- Marimo installed (preferred) or Jupyter available (legacy)

## Output

- Reproducible notebook with narrative markdown
- Validated run-all execution
- Plots and tables suitable for reporting

## Quality Gates

- [ ] Narrative text precedes code for each major step
- [ ] All cells run top-to-bottom without hidden state
- [ ] Data paths are project-relative and verified
- [ ] Plots are labeled, readable, and consistent

## Examples

### Example 1: Run a Marimo notebook

```bash
marimo run notebooks/analysis.py
```

### Example 2: Execute a Jupyter notebook (legacy)

```bash
python scripts/execute_notebook.py path/to/notebook.ipynb
```

## Troubleshooting

**Issue**: Marimo fails to run due to missing dependencies
**Solution**: Install required packages in the Pixi environment and re-run.

**Issue**: Jupyter notebook fails on restart
**Solution**: Remove hidden state, re-run from a clean kernel, and fix warnings.
