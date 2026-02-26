---
name: bio-protein-clustering-pangenome
description: Cluster proteins into orthogroups and derive pangenome matrices.
---

# Bio Protein Clustering Pangenome

Cluster proteins into orthogroups and derive pangenome matrices.

## Instructions

1. Cluster proteins with MMseqs2 or ProteinOrtho.
2. Build presence/absence matrix.
3. Compute core/accessory/cloud/singleton partitions.
4. Identify single-copy orthologs for phylogenetic analysis.
5. Discriminate paralogs from orthologs in multi-copy gene families.
6. Calculate pangenome statistics (completeness, orthogroup occupancy).

## Quick Reference

| Task | Action |
|------|--------|
| Run workflow | Follow the steps in this skill and capture outputs. |
| Validate inputs | Confirm required inputs and reference data exist. |
| Review outputs | Inspect reports and QC gates before proceeding. |
| Tool docs | See `docs/README.md`. |
| References | See `references.md` and `../bio-skills-references.md`. |

## Input Requirements

Prerequisites:
- Tools available in the active environment (Pixi/conda/system). See `docs/README.md` for expected tools.
- Protein FASTA inputs are available.
Inputs:
- proteins.faa (FASTA protein sequences)

## Output

- results/bio-protein-clustering-pangenome/orthogroups.tsv
- results/bio-protein-clustering-pangenome/presence_absence.parquet
- results/bio-protein-clustering-pangenome/pangenome_report.md
- results/bio-protein-clustering-pangenome/logs/

## Quality Gates

- [ ] Cluster size distributions meet project thresholds.
- [ ] Matrix completeness meets project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify proteins.faa is non-empty and amino acid encoded.

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
