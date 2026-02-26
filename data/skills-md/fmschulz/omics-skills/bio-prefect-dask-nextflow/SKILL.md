---
name: bio-prefect-dask-nextflow
description: Design and scaffold bioinformatics pipelines using Prefect+Dask for local/distributed execution or Nextflow for HPC schedulers.
---

# Bio Prefect + Dask + Nextflow

Choose and scaffold the right workflow engine for local, distributed, or HPC bioinformatics pipelines.

## Instructions

1. Collect requirements (scheduler, container policy, data location, scale).
2. Choose engine: Prefect+Dask, Nextflow, or Hybrid.
3. Generate a runnable scaffold with clear data layout and resources.
4. Validate with a small test and resume/retry checks.

## Quick Reference

| Task | Action |
|------|--------|
| Engine choice | See `decision-matrix.md` |
| Prefect+Dask scaffold | See `prefect-dask.md` |
| Prefect on Slurm | See `prefect-hpc-slurm.md` |
| Nextflow on HPC | See `nextflow-hpc.md` |
| Examples | See `examples.md` |

## Input Requirements

- Workflow requirements and steps
- Target environment (local, cluster, cloud)
- Scheduler and container constraints
- Data locations and expected volumes

## Output

- Engine recommendation with rationale
- Runnable scaffold (files + commands)
- Resource plan per step
- Validation plan and checkpoints

## Quality Gates

- [ ] Tiny test run completes end-to-end
- [ ] Resume/retry behavior verified
- [ ] Resource plan matches cluster limits

## Examples

### Example 1: Engine recommendation

```text
Choice: Nextflow
Why: CLI-heavy pipeline, HPC scheduler required, reproducible cache/resume needed.
```

## Troubleshooting

**Issue**: Workflow fails on HPC due to environment mismatch
**Solution**: Pin container/conda versions and validate with a minimal test dataset.
