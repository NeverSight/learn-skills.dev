---
name: bio-phylogenomics
description: Build marker gene alignments and phylogenetic trees.
---

# Bio Phylogenomics

Build marker gene alignments and phylogenetic trees.

## Instructions

1. Extract marker genes or SSU rRNA sequences.
2. Align and trim sequences using project-standard workflows.
3. Build ML trees with bootstraps:
4. Standard accuracy: Use IQ-TREE (comprehensive model selection, publication-quality)
5. Fast mode: Use IQ-TREE -fast (exploratory analysis, large datasets >10K sequences)
6. Very large datasets: Use VeryFastTree (>100K sequences, ultra-fast)
7. Post-process trees with ETE Toolkit:
8. Calculate tree statistics (branch lengths, distances, topology metrics)
9. Root, prune, or collapse nodes as needed
10. Filter by bootstrap support values
11. Add taxonomic or trait annotations
12. Generate publication-quality visualizations

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
- Marker gene set or alignments available.
Inputs:
- markers.faa (marker genes) or alignments.fasta

## Output

- results/bio-phylogenomics/alignments/
- results/bio-phylogenomics/trees/
- results/bio-phylogenomics/phylo_report.md
- results/bio-phylogenomics/logs/

## Quality Gates

- [ ] Alignment length and missingness meet project thresholds.
- [ ] Bootstrap support summary meets project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify markers.faa is non-empty and aligned sequences are consistent.

## Examples

### Example 1: Expected input layout

```text
markers.faa (marker genes) or alignments.fasta
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.