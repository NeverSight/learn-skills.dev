---
name: bio-gene-calling
description: Call genes and annotate basic features for prokaryotes, viruses, and eukaryotes.
---

# Bio Gene Calling

Call genes and annotate basic features for prokaryotes, viruses, and eukaryotes.

## Instructions

1. Select gene caller by organism class.
2. Run gene calling and produce GFF/FAA/FNA.
3. Detect tRNAs/rRNAs if requested.

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
- Input contigs or bins are available.
Inputs:
- contigs.fasta or bins/*.fasta

## Output

- results/bio-gene-calling/genes.gff3
- results/bio-gene-calling/proteins.faa
- results/bio-gene-calling/cds.fna
- results/bio-gene-calling/gene_metrics.tsv
- results/bio-gene-calling/logs/

## Quality Gates

- [ ] Gene count sanity checks pass.
- [ ] Start/stop codon checks pass.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify contigs are non-empty and DNA alphabet.
- [ ] Verify outputs contain expected feature types.

## Examples

### Example 1: Expected input layout

```text
contigs.fasta or bins/*.fasta
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.