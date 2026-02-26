---
name: bio-reads-qc-mapping
description: Ingest, QC, and map reads with reproducible outputs. Use for raw read processing and coverage stats.
---

# Bio Reads QC Mapping

Ingest, QC, and map reads with reproducible outputs. Use for raw read processing and coverage stats.

## Instructions

1. Parse sample sheet and validate inputs.
2. For short reads: Run QC/trimming (bbduk).
3. For long reads: Trim adapters (Porechop) and filter by quality/length (Filtlong).
4. Map reads (bbmap or minimap2) and generate coverage tables.

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
- Sample sheet and reads are available.
Inputs:
- sample_sheet.tsv
- reads/*.fastq.gz
- reference.fasta (optional)

## Output

- results/bio-reads-qc-mapping/trimmed_reads/
- results/bio-reads-qc-mapping/qc_reports/
- results/bio-reads-qc-mapping/mapping_stats.tsv
- results/bio-reads-qc-mapping/coverage.tsv
- results/bio-reads-qc-mapping/logs/

## Quality Gates

- [ ] Post-QC read count sanity checks pass.
- [ ] Mapping rate meets project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Validate sample sheet schema and FASTQ integrity.

## Examples

### Example 1: Expected input layout

```text
sample_sheet.tsv
reads/*.fastq.gz
reference.fasta (optional)
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.