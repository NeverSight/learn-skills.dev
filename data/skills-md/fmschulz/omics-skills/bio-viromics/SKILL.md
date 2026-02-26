---
name: bio-viromics
description: Detect, classify, and QC viral contigs.
---

# Bio Viromics

Detect, classify, and QC viral contigs.

## Instructions

1. Run virus detection (geNomad).
2. Run CheckV for completeness/contamination.
3. Assign taxonomy and cluster genomes (vConTACT3 for hierarchical classification and gene-sharing network analysis).

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
- Input contigs are available.
Inputs:
- contigs.fasta

## Output

- results/bio-viromics/viral_contigs.fasta
- results/bio-viromics/checkv_results/
- results/bio-viromics/vcontact3_results/
- results/bio-viromics/viral_taxonomy.tsv
- results/bio-viromics/genome_clusters.tsv
- results/bio-viromics/viromics_report.md
- results/bio-viromics/logs/

## Quality Gates

- [ ] CheckV quality thresholds meet project standards.
- [ ] Contamination flags are below thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify contigs.fasta is non-empty.
- [ ] Verify viral reference DBs exist under the reference root.

## Examples

### Example 1: Expected input layout

```text
contigs.fasta
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.