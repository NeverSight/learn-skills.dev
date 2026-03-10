---
name: bio-structure-annotation
description: Structure prediction and structure-based annotation.
---

# Bio Structure Annotation

Structure prediction and structure-based annotation.

## Instructions

1. Run fast embedding screen (tm-vec).
2. Predict structures (boltz or colabfold) as needed.
3. Search structures with Foldseek and annotate hits.

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
- Protein FASTA inputs are available.
Inputs:
- proteins.faa (FASTA protein sequences)

## Output

- results/bio-structure-annotation/structures/
- results/bio-structure-annotation/structure_hits.tsv
- results/bio-structure-annotation/structure_report.md
- results/bio-structure-annotation/logs/

## Quality Gates

- [ ] Prediction success rate meets project thresholds.
- [ ] Search hit thresholds meet project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify proteins.faa is non-empty and amino acid encoded.
- [ ] Verify Foldseek databases exist under the reference root.

## Examples

### Example 1: Expected input layout

```text
proteins.faa (FASTA protein sequences)
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.