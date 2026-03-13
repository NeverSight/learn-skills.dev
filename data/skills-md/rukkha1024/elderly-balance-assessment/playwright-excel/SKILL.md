---
name: playwright-excel
description: Integrate Excel (.xlsx) data into Playwright codegen scripts by replacing hardcoded values with config-driven lookups, loading data with polars, and validating every step with Playwright MCP (start MCP from the repo if not running). Use for Playwright automation updates that require Excel-backed data, config.yaml centralization, or MCP validation/reporting.
---

# Playwright Excel Integration

## Overview
Convert Playwright codegen scripts into Excel-driven automations with centralized config and required MCP validation.

## Environment
- Use the `playwright` conda environment.
- Before running any Python command, run: `conda run -n playwright python -c "import sys; print(sys.executable)"`
- Do not create or activate any venv or `.venv`.

## Inputs
- Playwright codegen script path
- Excel `.xlsx` path
- Mapping lines: `"hardcoded_value" -> Excel[Sheet][FilterCol==FilterVal][DataCol]`
- Optional override: `PLAYWRIGHT_TARGET_SUBJECT`

## Workflow
1. Analyze the Playwright script and the Excel structure (sheets, columns, sample rows).
2. Detect hardcoded `.fill()` values and confirm that each has a mapping; request clarification for mismatches.
3. Ensure dependencies in the `playwright` conda env (prefer `conda install -n playwright`, fall back to `conda run -n playwright pip install`).
4. Create or update `config.yaml` using centralized control (paths, patterns, column definitions, constants, tunables, shared texts).
5. Modify the Playwright script:
   - Add a config loader and an Excel loader (polars; see `references/excel-loading.md`).
   - Replace hardcoded values with `data[...]`.
6. Always run Playwright MCP validation; if MCP is not running, start it from this repo before continuing (see `references/mcp-validation.md`).
7. When refactoring existing pipelines/logic, generate outputs and compare MD5 checksums with reference files (see `references/md5-validation.md`).
8. Run the updated script with `conda run -n playwright python`.

## References
- `references/excel-loading.md`
- `references/mcp-validation.md`
- `references/md5-validation.md`
- `references/examples.md`
