---
name: slurm-info-summary
description: Gather and cache SLURM cluster information (partitions, GPUs, memory, QOS limits). Generates a readable summary doc on first run; returns the cached doc on subsequent runs.
---

# SLURM Info Summary

Collect SLURM cluster specs and save a polished, human-readable reference document.

## Steps

1. **Check for existing doc**: Look for `~/.claude/skills/slurm-info-summary/references/slurm-cluster-summary.md`.

2. **If the doc already exists**:
   - Tell the user: "SLURM cluster summary already exists at `~/.claude/skills/slurm-info-summary/references/slurm-cluster-summary.md`."
   - Read the file and display its content.
   - Do NOT re-run the script. Stop here.

3. **If the doc does NOT exist**:
   - Run `~/.claude/skills/slurm-info-summary/scripts/gather-slurm-info.sh` and capture stdout.
   - Parse the raw output (structured with `=== SECTION ===` markers) and produce a **polished markdown summary** following the template below.
   - Write the summary to `~/.claude/skills/slurm-info-summary/references/slurm-cluster-summary.md`.
   - Display the summary to the user.
   - Tell the user the file path where it was saved.

## Output Template

Use the raw data to produce a summary that matches this structure and style exactly. Convert raw memory values from MB to human-readable GB/TB. Derive node types by grouping nodes with the same prefix (e.g. `ravc`, `ravg`, `ravh`, `ravl`).

```markdown
# <ClusterName> Cluster Overview

> Auto-generated on <UTC timestamp> by `/slurm-info-summary`

All compute nodes use **<CPU model>** processors with **<sockets> sockets, <cores>/socket, <threads> threads/core = <total logical CPUs> CPUs** per node.

---

## Partitions

| Partition | Nodes | Node Type | Memory/Node | GPUs/Node | Max Walltime | Max Nodes/Job | Oversubscribe |
|-----------|-------|-----------|-------------|-----------|--------------|---------------|---------------|
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## Node Types

| Prefix | Count | Memory | GPUs | Notes |
|--------|-------|--------|------|-------|
| ... | ... | ... | ... | ... |

---

## Key Partition Differences

- **`<partition_a>` vs `<partition_b>`**: <explain the difference concisely>
- ...

---

## QOS Limits (notable only)

| QOS | Max Nodes/Job | Max Running Jobs | Max Submit Jobs | Max Walltime |
|-----|---------------|------------------|-----------------|---------------|
| ... | ... | ... | ... | ... |

Only include QOS entries that have at least one non-empty limit.

---

## Usage Examples

Provide 5-7 ready-to-use `sbatch`/`srun` examples covering:
- Interactive session
- Single-node CPU job (small partition)
- Multi-node CPU job (general partition)
- Single-GPU shared job (gpu1 partition)
- Multi-node GPU exclusive job (gpu partition)
- Quick GPU dev/test (gpudev partition)
- High-memory node request (if available)

## Key Tips

- Bullet list of practical tips: billing weights, constraint flags, useful commands (`squeue`, `scancel`), etc.
```

## Important

- Do NOT output the raw script data to the user. Only output the polished summary.
- Keep the summary concise but complete.
- The "Node Availability" section from the script is point-in-time data — do NOT include it in the saved summary (it would be stale).
- **Physical cores vs logical CPUs**: Nodes with hyperthreading have more logical CPUs than physical cores (e.g., 72 physical cores = 144 logical CPUs with 2 threads/core). SLURM's `--cpus-per-task` counts **physical cores**. When describing per-GPU resource limits for shared partitions, always state the value in **physical cores** and note the logical CPU count parenthetically. For example: "18 physical cores (36 logical CPUs) and 125 GB memory per GPU".
