---
name: vai-perf-analysis
license: Apache-2.0 WITH LLVM-exception
compatibility: Requires VitisAI 6.3+
metadata:
  version: 6.3.0
  stage: beta
description: Analyze performance of VAIML compiled models. Uses the AI Analyzer SDK
  to extract detailed timing, operator metrics, and performance summaries, then answers
  any question about model performance -- layer timing, custom op cost, bottlenecks,
  partition breakdown, comparisons between runs, and more. Requires a Ryzen AI / Vitis
  AI Python environment with `dlanalyzer` available -- either by sourcing a venv activate
  script (`--t`) or by running inside a pre-provisioned environment such as the official
  Vitis AI Docker container. Use when the user wants to analyze model performance,
  find slow layers, compare compilation runs, understand custom op overhead, or generate
  a performance report.
---
<!--- Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.--->

# Performance Analysis Skill

## Access command

This skill must always be accessed through the worker, never in a different way.
Allowed workers: `vai-custom-op-worker`, or the `vai-flag-configuration` skill,
which is its own entry point.

## Description

Analyze performance of VAIML compiled models using the AI Analyzer SDK
(`dlanalyzer`) shipped with the Ryzen AI environment. Can answer any natural
language question about model performance -- layer timing, custom op cost,
bottlenecks, partition breakdown, host vs NPU split, and more.

## Optimization Target (READ FIRST)

**The number to optimize is `average_npu_time_usec` ("NPU Compute").**
This is the actual time the NPU spends executing the model per inference.
Always report it FIRST and frame the rest of the analysis around it.

Do NOT use the host-side "Kernel Launch Window" (formerly labeled "Kernel
Execution") as the optimization target. That value comes from
`get_performance_metrics()` host_profiling and measures the host's view of
the launch->completion window, so it includes NPU compute + DMA setup/
teardown + driver/runtime sync overhead. It is useful for end-to-end
latency accounting, but it is NOT what custom-op or kernel work moves.

When you produce a report:
1. Lead with **NPU Compute** (`average_npu_time_usec`) -- this is the
   target and the first value in the summary.
2. Then show **Total inference time** per inference (divide
   `total_execution_time_us` by `inference_count` if needed) for context.
3. Then the host-profiling breakdown, with the host kernel-window row
   labeled as a host-side measurement, not as the optimization target.
4. Express custom-op and per-op costs as a percentage of NPU Compute, not
   of the host kernel window.

## Parse Arguments

This skill expects arguments in this form:

```
<run_dir> [question] [--compare <run_dir2>]
```

Extract from `$ARGUMENTS`:
- **run_dir**: **(MANDATORY)** Path to the directory containing profiling
  outputs (`summary.csv`, `record_timer_*.json`, `partition.json`, etc.).
- **question**: Optional natural language question about performance.
  If omitted, generate a comprehensive performance summary.
- `--compare <run_dir2>`: Optional second run directory for side-by-side
  comparison.

Skill directory: the directory containing this SKILL.md file (referred to as
`<skill_dir>` below).

**Validation**: `run_dir` must exist and contain at least one of:
`summary.csv`, `record_timer_ts.json`, or a `record_timer_inference_*.json`
file. If missing, ask the user to provide the correct path.

## Script Reference

All analysis is done via `<skill_dir>/scripts/ai_extract.py`. It requires the Ryzen AI / Vitis AI Python environment to be available (so that `dlanalyzer` and friends are importable).

This skill supports two deployment models:

1. **Sourced venv**: the user passes `--t <activate_path>` and every shell that runs `python3` must `source <activate_path>` first.
2. **Pre-provisioned environment** (e.g. official Vitis AI Docker container): the Python packages are already on `PATH` / `PYTHONPATH`. No `--t` is provided and no sourcing is needed.

Wherever this document shows `<ENV_SETUP>` inside a bash snippet, expand it as follows:
- If `--t <path>` was provided: replace the `<ENV_SETUP>` line with `source <path> 2>/dev/null &&`.
- Otherwise: omit the `<ENV_SETUP>` token entirely (so the command starts directly with `python3`).

Do NOT search the filesystem for an activate script if `--t` is absent -- treat its absence as a deliberate signal that the environment is already in place.

All commands follow this pattern:

```bash
bash -c '<ENV_SETUP> python3 <skill_dir>/scripts/ai_extract.py <run_dir> [FLAGS] 2>/dev/null' | grep -v "^2026\|^Loaded ONNX\|^Error getting schema"
```

### Modes

| Flags | Output | Use for |
|-------|--------|---------|
| `--compact --human` | Human-readable summary | General overview, host vs NPU split |
| `--top N --human` | Top N slowest nodes | Finding biggest offenders |
| `--query "PATTERN" --human` | Matching nodes by name/type | Custom ops, specific layers |
| `--compact` | Compact JSON | Tool consumption |
| `--top N` | Top-N JSON | Tool consumption |
| `--query "PATTERN"` | Query JSON | Tool consumption |
| Any of above + `-o FILE` | JSON to file | Save for later or dual output |
| `--human -o FILE` | Human to stdout + JSON to file | Both at once |

### Examples

```bash
# Full summary
python3 ai_extract.py /path/to/run --compact --human

# Top 20 slowest individual NPU nodes
python3 ai_extract.py /path/to/run --top 20 --human

# All custom ops
python3 ai_extract.py /path/to/run --query "mydomain" --human

# A specific custom op by name (substring or regex)
python3 ai_extract.py /path/to/run --query "<op_name>" --human

# Just convolutions
python3 ai_extract.py /path/to/run --query "Conv" --human

# Human to terminal + JSON to file
python3 ai_extract.py /path/to/run --compact --human -o /tmp/perf.json
```

## Workflow

### Step 1: Get the overview

Run compact mode to get aggregated metrics:

```bash
bash -c '<ENV_SETUP> python3 <skill_dir>/scripts/ai_extract.py <run_dir> --compact --human 2>/dev/null' | grep -v "^2026\|^Loaded ONNX\|^Error getting schema"
```

This gives you: total inference time, NPU time, host profiling breakdown,
per-operator-type NPU breakdown (with custom ops highlighted), GMACS stats.

### Step 2: Find the biggest offenders (if needed)

```bash
bash -c '<ENV_SETUP> python3 <skill_dir>/scripts/ai_extract.py <run_dir> --top 20 --human 2>/dev/null' | grep -v "^2026\|^Loaded ONNX\|^Error getting schema"
```

Shows the top N slowest individual nodes sorted by cycle count, with
estimated time, plus what percentage of total NPU time they cover.

### Step 3: Drill into specifics (if needed)

Use `--query` to filter by operator name or type:

```bash
bash -c '<ENV_SETUP> python3 <skill_dir>/scripts/ai_extract.py <run_dir> --query "PATTERN" --human 2>/dev/null' | grep -v "^2026\|^Loaded ONNX\|^Error getting schema"
```

Pattern is regex or substring, case-insensitive. Matches against both
the `Name` and `Type` fields. Common patterns:
- `"mydomain"` -- all custom ops
- `"Conv"` -- convolution layers
- `"<op_name>"` -- a specific custom op by its registered name
- `"Sigmoid\|Tanh"` -- activation functions

### Step 4: Answer the question

Using the extracted data, answer the user's question directly with exact
numbers and percentages.

### Comparing two runs

Extract compact data from both directories separately and compare the
corresponding `operator_metrics` and summary values manually.

## Data Format Reference

### operator_metrics (from --compact)

Each entry has:
- `category`: `"npu"` or `"host_profiling"`
- `name`: Operator type (e.g. `"Conv2DBf16"`, `"mydomain.<op_name>"`)
- `count`: Number of instances
- `value_usec`: Total aggregated time in microseconds
- `percent`: Percentage of timeline
- `cycles_per_count`: Average cycles per invocation

### timing_data entries (from --query / --top)

Each entry has:
- `Name`: Instance name (e.g. `"node_Conv_179_Duplicated#1"`)
- `Type`: Operator type
- `Execution Time.Cycles`: Duration in cycles
- `Approx Time.us` (in --top) or computed as `cycles / clock_mhz`

### Common operator types

| Type | Description |
|------|-------------|
| `Conv2DBf16` | 2D Convolution (bf16) |
| `ClipBf16` / `ClipBf163D` | ReLU / Clip activation |
| `GemmBfp16` | Fully-connected / GEMM |
| `SigmoidTemplatedBf163D` | Sigmoid activation |
| `TanhTemplatedBf163D` | Tanh activation |
| `MulBf163D` | Element-wise multiply |
| `AddBf163D` | Element-wise add |
| `Transpose4dAdf` | 4D Transpose |
| `ReduceMeanTemplated` | Mean reduction |
| `mydomain.*` | Custom operator types |
