---
name: bio-assembly-qc
description: Assemble genomes/metagenomes and produce assembly QC artifacts.
---

# Bio Assembly QC

Assemble genomes/metagenomes and produce assembly QC artifacts.

## Instructions

1. Select assembler based on read type and genome size.
2. Run assembly with resource-aware settings.
3. Run QUAST/MetaQUAST and summarize metrics.

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
- Sufficient disk and RAM for chosen assembler.
Inputs:
- reads/*.fastq.gz (raw reads).
- assembler choice (spades | flye).

## Output

- results/bio-assembly-qc/contigs.fasta
- results/bio-assembly-qc/assembly_metrics.tsv
- results/bio-assembly-qc/qc_report.html
- results/bio-assembly-qc/logs/

## Quality Gates

- [ ] Assembly size range and N50 distribution meet project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify reads are present and gzip-readable.
- [ ] Check available disk space before assembly.

## Examples

### Example 1: Expected input layout

```text
reads/*.fastq.gz (raw reads).
assembler choice (spades | flye).
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.