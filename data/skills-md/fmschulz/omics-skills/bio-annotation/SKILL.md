---
name: bio-annotation
description: Functional annotation and taxonomy inference from sequence homology.
---

# Bio Annotation

Functional annotation and taxonomy inference from sequence homology.

## Instructions

1. Run InterProScan for domain/family annotation.
2. Run eggnog-mapper for orthology-based annotation.
3. Run DIAMOND and resolve taxonomy with TaxonKit.

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
- Input FASTA and reference DBs are readable.
Inputs:
- proteins.faa (FASTA protein sequences).
- reference_db/ (eggNOG, InterPro, DIAMOND databases + taxdump).

## Output

- results/bio-annotation/annotations.parquet
- results/bio-annotation/taxonomy.parquet
- results/bio-annotation/annotation_report.md
- results/bio-annotation/logs/

## Quality Gates

- [ ] Annotation hit rate and taxonomy rank coverage meet project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify proteins.faa is non-empty and amino acid encoded.
- [ ] Verify required reference DBs exist under the reference root.

## Examples

### Example 1: Expected input layout

```text
proteins.faa (FASTA protein sequences).
reference_db/ (eggNOG, InterPro, DIAMOND databases + taxdump).
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.