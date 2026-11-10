---
name: pipeline-manifest
description: "Build a traceability manifest linking analysis scripts to inputs, outputs, and manuscript figures or tables. Use when documenting a computational pipeline or locating the source of a reported artefact. Not for verifying that paper claims match code outputs; use the code-paper auditor."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[project-path]"
---

# Pipeline Manifest

Build and maintain a `pipeline.md` that maps every script in a research project to its inputs, outputs, and the paper figures/tables it feeds. Optionally add structured headers to scripts that lack them.

## When to Use

- When starting a multi-step empirical project (establish the pipeline early)
- Before sharing code with coauthors (makes the data flow legible)
- Before submission (ensures the replication package is traceable)
- After inheriting or reviving old code (pair with `code-archaeology`)
- When you can't remember which script produces Figure 3

## When NOT to Use

- Pure theory projects with no empirical pipeline
- Single-script projects (no pipeline to map)
- **Code quality review** — use the `code-review` agent instead (this skill maps structure, not quality)

## Modes

Ask the user which mode to run:

| Mode | What it does | Writes to |
|------|-------------|-----------|
| **Scan** (default) | Read-only. Scans scripts, builds `pipeline.md` | `pipeline.md` only |
| **Add headers** | Scan + insert structured headers into scripts that lack them | `pipeline.md` + script files |

In **Add headers** mode, show the proposed header for each script and get confirmation before writing. Never overwrite an existing structured header — only add to scripts that lack one.

## Structured Script Header Format

Every research script should begin with a structured header block. The format adapts to the language:

### Python

```python
# ============================================================================
# PURPOSE: [One sentence describing what this script does]
# INPUTS:  [Comma-separated list of input files, relative to project root]
# OUTPUTS: [Comma-separated list of output files, relative to project root]
# DEPENDS: [Scripts that must run before this one, or "none"]
# PAPER:   [Figure/table references this feeds, e.g. "Figure 2, Table 1", or "none"]
# ============================================================================
```

### R

```r
# ============================================================================
# PURPOSE: [One sentence describing what this script does]
# INPUTS:  [Comma-separated list of input files, relative to project root]
# OUTPUTS: [Comma-separated list of output files, relative to project root]
# DEPENDS: [Scripts that must run before this one, or "none"]
# PAPER:   [Figure/table references this feeds, e.g. "Figure 2, Table 1", or "none"]
# ============================================================================
```

### Stata

```stata
* ============================================================================
* PURPOSE: [One sentence describing what this script does]
* INPUTS:  [Comma-separated list of input files, relative to project root]
* OUTPUTS: [Comma-separated list of output files, relative to project root]
* DEPENDS: [Scripts that must run before this one, or "none"]
* PAPER:   [Figure/table references this feeds, e.g. "Figure 2, Table 1", or "none"]
* ============================================================================
```

### Julia

```julia
# ============================================================================
# PURPOSE: [One sentence describing what this script does]
# INPUTS:  [Comma-separated list of input files, relative to project root]
# OUTPUTS: [Comma-separated list of output files, relative to project root]
# DEPENDS: [Scripts that must run before this one, or "none"]
# PAPER:   [Figure/table references this feeds, e.g. "Figure 2, Table 1", or "none"]
# ============================================================================
```

## Header Field Definitions

| Field | What it contains | How to populate |
|-------|-----------------|-----------------|
| **PURPOSE** | One sentence. What does this script do? | Read the script and summarise |
| **INPUTS** | Files this script reads. Paths relative to project root. | Grep for `read`, `load`, `import`, `open`, `use` patterns |
| **OUTPUTS** | Files this script writes. Paths relative to project root. | Grep for `write`, `save`, `export`, `ggsave`, `savefig`, `sink` patterns |
| **DEPENDS** | Other scripts that must run first (their outputs are this script's inputs). | Trace input files back to the scripts that produce them |
| **PAPER** | Which figures, tables, or sections in the paper use this script's output. | Match output filenames against `\includegraphics`, `\input`, `\include` in `.tex` files |

## Workflow

### Phase 1: Discover Scripts

Scan the project for research scripts:

```
code/**/*.{py,R,r,do,jl,m}
src/**/*.{py,R,r,do,jl,m}
scripts/**/*.{py,R,r,do,jl,m}
```

Exclude:
- `__pycache__/`, `.venv/`, `renv/`, `node_modules/`
- Test files (`test_*.py`, `*_test.R`)
- Setup/config scripts (`setup.py`, `conftest.py`)

Sort by filename (numerical prefixes like `01_`, `02_` determine natural order).

### Phase 2: Extract Pipeline Information

For each script:

1. **Check for existing header.** Look for the `PURPOSE:` / `INPUTS:` / `OUTPUTS:` / `DEPENDS:` / `PAPER:` pattern in the first 20 lines.

2. **If header exists:** Parse it directly. Trust the header as ground truth.

3. **If no header:** Read the full script and infer:
   - **Inputs:** File read operations (`pd.read_csv`, `read.csv`, `readRDS`, `load`, `use`, `open`, `import delimited`, `fread`, `arrow::read_parquet`, `readr::read_*`)
   - **Outputs:** File write operations (`to_csv`, `write.csv`, `saveRDS`, `save`, `ggsave`, `plt.savefig`, `export`, `sink`, `write_parquet`, `fwrite`, `outsheet`, `estout`)
   - **Dependencies:** Cross-reference — if script B reads a file that script A writes, then B depends on A
   - **Paper links:** Match output filenames against `\includegraphics{...}` and `\input{...}` in `.tex` files

### Phase 3: Build Dependency Graph

From the extracted information, construct:

1. **Execution order** — topological sort of the dependency graph. Flag cycles as errors.
2. **Orphan detection** — scripts whose outputs are never used by another script or the paper. These may be exploratory/deprecated.
3. **Missing link detection** — inputs that no script produces and that don't exist in `data/raw/`.

### Phase 4: Build Paper Linkage

Scan all `.tex` files in `paper/` for:
- `\includegraphics{path}` — figures
- `\input{path}` — tables or sub-documents
- `\include{path}` — chapters

Match these paths to script outputs. Build a reverse map: for each figure/table in the paper, which script(s) produce it?

### Phase 5: Write pipeline.md

Write `pipeline.md` to the project root using the format below.

### Phase 6 (Add Headers Mode Only): Insert Headers

For scripts missing structured headers:
1. Generate the header from Phase 2 analysis
2. Show the proposed header to the user
3. On confirmation, insert at the top of the file (after any shebang line or encoding declaration)

## pipeline.md Format

```markdown
# Pipeline Manifest

> Auto-generated by `pipeline-manifest` on YYYY-MM-DD.
> Manually edit the PAPER column and any inferred values that are wrong.
> Re-run `pipeline-manifest` to refresh after adding or modifying scripts.

## Pipeline Table

| # | Script | Purpose | Inputs | Outputs | Depends | Paper |
|---|--------|---------|--------|---------|---------|-------|
| 1 | `code/01_clean.R` | Clean raw survey data | `data/raw/survey.csv` | `data/processed/survey_clean.rds` | none | -- |
| 2 | `code/02_merge.R` | Merge survey with admin data | `data/processed/survey_clean.rds`, `data/raw/admin.csv` | `data/processed/merged.rds` | `01_clean.R` | -- |
| 3 | `code/03_analysis.R` | Run main regressions | `data/processed/merged.rds` | `results/main_results.rds`, `paper/figures/fig_coef.pdf` | `02_merge.R` | Figure 2 |
| 4 | `code/04_robustness.py` | Robustness checks | `data/processed/merged.rds` | `results/robustness.csv`, `paper/figures/fig_robust.pdf` | `02_merge.R` | Figure 3, Table A1 |

## Figure & Table Manifest

| Paper Reference | Producing Script | Output File |
|----------------|-----------------|-------------|
| Figure 2 | `code/03_analysis.R` | `paper/figures/fig_coef.pdf` |
| Figure 3 | `code/04_robustness.py` | `paper/figures/fig_robust.pdf` |
| Table A1 | `code/04_robustness.py` | `results/robustness.csv` |

## Dependency Graph

```
data/raw/survey.csv ─┐
                     ├─> 01_clean.R ─> data/processed/survey_clean.rds ─┐
data/raw/admin.csv ──┘                                                  ├─> 02_merge.R ─> data/processed/merged.rds ─┬─> 03_analysis.R
                                                                        │                                            └─> 04_robustness.py
```

## Diagnostics

### Orphan Scripts
Scripts whose outputs are not consumed by any other script or the paper.

### Missing Inputs
Files referenced as inputs but not produced by any script and not found in `data/raw/`.

### Execution Order
Recommended order based on dependency resolution:
1. `code/01_clean.R`
2. `code/02_merge.R`
3. `code/03_analysis.R`
4. `code/04_robustness.py` (can run in parallel with step 3)
```

## Updating an Existing pipeline.md

If `pipeline.md` already exists:

1. Read it and parse the existing table
2. Re-scan scripts (some may have been added, removed, or modified)
3. **Preserve manual edits** — if the user has edited the PAPER column or added notes, keep those values. Only update fields that can be re-derived from code (PURPOSE, INPUTS, OUTPUTS, DEPENDS).
4. Flag changes: "2 scripts added, 1 script removed, 3 entries updated"
5. Write the updated file

## Cross-References

- **the `code-review` agent** — Quality review for individual scripts (checks header presence in Category 2: Script Structure)
- **`code-archaeology`** — For understanding unfamiliar code before building the manifest
- **`pre-submission-report`** — Pipeline manifest helps verify the replication package is complete
- **`init-project-research`** — New projects can run `pipeline-manifest` once scripts exist
