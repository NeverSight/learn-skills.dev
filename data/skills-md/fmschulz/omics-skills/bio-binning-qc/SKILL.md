---
name: bio-binning-qc
description: Perform metagenomic binning, refinement, and QC with completeness/contamination checks.
---

# Bio Binning QC

Perform metagenomic binning, refinement, and QC with completeness/contamination checks.

## Instructions

1. Compute depth/coverage per sample.
2. Run multiple binners (MetaBAT2, SemiBin2, QuickBin).
3. Classify bins by domain (bacteria/archaea vs eukaryotes).
4. Run domain-specific QC:
5. CheckM2 for bacterial and archaeal bins
6. EukCC for eukaryotic bins
7. GUNC for contamination detection (all domains).

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
- Reference DB root: set `BIO_DB_ROOT` (default `/media/shared-expansion/db/` on WSU).
- Coverage/depth tables or reads available to compute coverage.
Inputs:
- contigs.fasta
- coverage.tsv (per-sample depth table)

## Output

- results/bio-binning-qc/bins/
- results/bio-binning-qc/bin_metrics.tsv
- results/bio-binning-qc/bin_qc_report.html
- results/bio-binning-qc/logs/

## Quality Gates

- [ ] Completeness and contamination meet project thresholds.
- [ ] Chimera and contamination flags are below thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify contigs.fasta and coverage.tsv are non-empty.
- [ ] Verify reference DBs for QC tools exist under the reference root.

## Examples

### Example 1: Expected input layout

```text
contigs.fasta
coverage.tsv (per-sample depth table)
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.