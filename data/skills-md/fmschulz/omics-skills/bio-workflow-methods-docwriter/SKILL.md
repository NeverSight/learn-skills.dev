---
name: bio-workflow-methods-docwriter
description: Generate reproducible Methods documentation from workflow run artifacts (Nextflow/Snakemake/CWL), including exact commands, versions, parameters, QC gates, and outputs.
---

# Bio Workflow Methods Docwriter

Create publication-ready Methods and run documentation from real workflow artifacts.

## Instructions

1. Collect the workflow evidence package (logs, configs, version files).
2. Build `run_manifest.yaml` strictly from evidence.
3. Validate the manifest against the schema.
4. Draft `METHODS.md` with a concise workflow summary at the top.
5. Verify QC gates and reproducibility details are captured.

## Quick Reference

| Task | Action |
|------|--------|
| Evidence checklist | See `reference/evidence-checklist.md` |
| Manifest schema | `schemas/run-manifest.schema.json` |
| Validate manifest | `python scripts/validate_run_manifest.py run_manifest.yaml` |
| Examples | See `examples/` |

## Input Requirements

- Workflow artifacts (Nextflow/Snakemake/CWL logs and configs)
- Tool version records or container digests
- QC reports and output manifests

## Output

- `METHODS.md` (workflow summary + detailed steps)
- `run_manifest.yaml` (machine-readable run manifest)

## Quality Gates

- [ ] No invented commands, versions, or parameters
- [ ] Every step has inputs, outputs, and versions captured
- [ ] Workflow summary appears at top of `METHODS.md`

## Examples

### Example 1: Validate a manifest

```bash
python scripts/validate_run_manifest.py run_manifest.yaml
```

## Troubleshooting

**Issue**: Missing tool versions in logs
**Solution**: Mark as `NOT CAPTURED` and add a note on how to capture next time.
