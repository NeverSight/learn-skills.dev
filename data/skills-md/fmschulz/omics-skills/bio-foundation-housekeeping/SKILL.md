---
name: bio-foundation-housekeeping
description: Initialize a bioinformatics project scaffold with reproducible environments, schemas, and data cataloging. Use for new projects or repo setup.
---

# Bio Foundation Housekeeping

Initialize a bioinformatics project scaffold with reproducible environments, schemas, and data cataloging. Use for new projects or repo setup.

## Instructions

1. Create standard directory layout (data/, results/, schemas/, workflows/, src/, notebooks/).
2. Initialize Pixi workspace and lockfile; define tasks.
3. Define LinkML schemas and generate Pydantic models.
4. Create DuckDB catalog and register parquet tables.

## Quick Reference

| Task | Action |
|------|--------|
| Run workflow | Follow the steps in this skill and capture outputs. |
| Validate inputs | Confirm required inputs and reference data exist. |
| Review outputs | Inspect reports and QC gates before proceeding. |
| Tool docs | See `docs/README.md`. |
| References | - See ../bio-skills-references.md |

## Input Requirements

Prerequisites:
- Tools available in the active environment (Pixi/conda/system). See `docs/README.md` for expected tools.
- Target project root is writable.
Inputs:
- project root (path)
- metadata schema requirements
- workflow engine preference (optional)

## Output

- pixi.toml
- pixi.lock
- schemas/
- data/catalog.duckdb
- results/bio-foundation-housekeeping/report.md
- results/bio-foundation-housekeeping/logs/

## Quality Gates

- [ ] Schema generation succeeds and models are importable.
- [ ] pixi.lock is created and consistent with pixi.toml.
- [ ] DuckDB catalog is readable.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify project root exists and is writable.
- [ ] Validate generated schemas against expected fields.

## Examples

### Example 1: Expected input layout

```text
project root (path)
metadata schema requirements
workflow engine preference (optional)
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.