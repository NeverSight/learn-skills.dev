---
name: hls-optimize
description: Iteratively optimize the HLS kernel against a given criteria (e.g. minimize latency, reduce DSP usage, maximize throughput) by applying and measuring pragma and algorithmic changes.
license: MIT
argument-hint: <optimization-criteria>
metadata:
  author: "Alex Li, Sai Akhil Ayyagari"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# Skill: hls-optimize

Iteratively modify the kernel to improve performance against an optimization criteria, using the other skills to measure progress and committing each attempt.

**Optimization criteria**: $ARGUMENTS

Examples:
- `/hls-optimize minimize latency`
- `/hls-optimize minimize DSP usage while meeting timing`
- `/hls-optimize maximize throughput (minimize II)`
- `/hls-optimize reduce LUT count below 5000`

## Init component and git repository

**MANDATORY**: Before any optimization work, you MUST read and execute the `./reference/init-component.md` file.

**DO NOT** write your own git init commands. **DO NOT** use simplified git commands. You MUST execute the `./reference/init-component.md` file, which includes the `vitis-comp.json` check, specific git configuration, and .gitignore setup.

This ensures the HLS component is properly set up, with consistent git configuration, proper .gitignore setup, and correct baseline commit format across all optimization sessions.

## Philosophy

**One idea at a time.** Each attempt changes exactly one thing — one pragma, one algorithmic transformation, one loop restructuring. Never combine independent changes in a single attempt. You cannot attribute cause if multiple things changed simultaneously.

**Investigate before moving on.** After each synthesis, read the reports thoroughly. Do not just check whether latency went up or down — understand *why*. Read the loop detail table. Check II and achieved vs. target. Look for warnings in the log. If something unexpected happened, dig into it before proceeding.

**Use all available tools.** The synth skill gives access to BC file inspection, QoR JSON, inferred directives, and schedule details. Use `hls-component-basic-info` skill and the `hls-synth-report` skill for a quick overview. In synthesis log to inspect how the pragma used in the code. Use `./hls-scripts/qor_log.py` to track the history of changes. Verify that the change had the expected effect — not just in the report, but in the IR and schedule.

**Experimental changes are valid.** Sometimes the right move is to make a change that you don't expect to improve the metric, but that tests a hypothesis about the tool's behavior. Document what you expected and what actually happened. Understanding the compiler's behavior is itself valuable.

**Do not rush to run cosim or impl.** Use csim+csynth as the inner loop. Only escalate to cosim when csynth shows meaningful improvement (≥ 10% in cycles or a structural change like II reduction). Only run impl when cosim confirms improvement. The expensive steps are a gate, not a rubber stamp.

**Verify Vitis environment.** 

```bash
which vitis-run
```

If not found, check if the environment variable XILINX_VITIS is set. If not, ask the user for the value of XILINX_VITIS. Then source the settings file:

```bash
which vitis-run  # must be on PATH — set XILINX_VITIS to your Vitis install if not
```

Do not proceed until `vitis-run` is on PATH.

## Step 0: Establish baseline and get HLS design data

### 0a. Establish a baseline

Before making any change, ensure you have a measured baseline to compare against. The baseline consists of:

1. **cosim latency** (cycles) from cosimulation report
2. **post-route clock period** (ns) from the `hls-impl-report` skill's `postRoute` value (implementation report)
3. **true latency** = cycles × period
4. **resource utilization** (LUT, FF, DSP, BRAM, URAM) from the `hls-impl-report` skill's `placeRouteResourceSummary` value (implementation report)

When you establish the baseline, you must make sure the csimulation, synthesis, cosimulation and implementation flows have all been run successfully. If any of the reports is missing or stale, use skill of `hls-run-flow` to run the corresponding flow before recording the baseline.

### 0b. Get HLS design reports and data

**MANDATORY**: You MUST call the following functions to get ALL report-related data. **DO NOT** read `.rpt` files directly using file read tools — always use these functions.

- `hls-synth-report` skill: get the synthesis report and log content.
  - Returns `synthesisReportContent`, `synthesisPragmaReportContent`, and `synthesisLogContent`
- `hls-cosim-report` skill: get the cosimulation report content and dataflow process/channel content.
  - Returns `coSimulationReportContent` and `dataflowProcessAndChannelContent`
- `hls-impl-report` skill： get the implementation report content.
  - Returns `postRoute`, `placeRouteResourceSummary` and `placeRouteFailFast`

### 0c. Run HLS flows if reports are missing or stale

If these reports do not exist or are stale, you must use the `hls-run-flow` skill to run the active component HLS flow.
Before running csim flow, you must check 'csim.profile_tripcount=1' in .cfg file. If it is not set, update the trip count. When you find it changes the trip count, you must run all flows (csim, csynth, cosim, impl) to get the updated reports before recording the baseline.

### 0d. Log the baseline QoR data for future comparison
On the unmodified kernel first.

Call `getSkillResourcePath` function with skillName and relativePath `./hls-scripts/qor_log.py` to get the full path to the script.

Then run `python3 "$qorLogScriptFullPath" --report "$synthesisReportContent"` to get a concise summary of the baseline. The `report` argument is required; the `label` and `csv` arguments are optional.
Record the baseline before starting optimization iterations.

## Step 1: Analyze the kernel

You must call `hls-component-basic-info` skill to get the basic component info, including `component_name`, `source_files`, `testbench_files`, `include_paths`, `top_function`. Read this information along with the `synthesisReportContent` and `synthesisLogContent` to analyze the kernel and identify bottlenecks.

- **High II on inner loops** → memory port bottleneck or long recurrence chain. Check loop table for `II achieved` vs `II target`. Read the warning messages in `synthesisLogContent` for the root cause.
- **Large iteration latency on unpipelined loops** → missing pipeline pragma, or loop not eligible for pipelining (e.g. variable trip count, non-trivial control flow, contains sub-loop).
- **Low resource utilization** → opportunity to trade area for performance (unrolling, partitioning). DSP at 2% means 98% of compute is still sequential.
- **High resource utilization** → risk of fit; verify after every change.
- **Sequential outer loop containing pipelined inner loop** → inner pipeline restarts on every iteration, dominant latency term.

Also read the Violation Report in the `synthesisLogContent` carefully — it identifies exactly which dependency causes each II violation, including the variable name and memory port.

## Step 2: Form a hypothesis

Before touching any code, write down:

1. **What you will change** (exact pragma or code transformation)
2. **What you expect to happen** in the `synthesisReportContent` (loop II, latency, resources)
3. **What would confirm the hypothesis** (e.g. "II drops from 5 to 2 because we have 2 memory ports now")
4. **What would falsify it** (e.g. "II stays at 5 despite partition → the bottleneck is the FMA recurrence, not memory")

This forces you to understand the compiler before running it, and makes failed experiments informative.

## Step 3: Choose one optimization technique

Pick one technique per attempt. See the full technique catalogue below.

### Pragma-only changes (lowest risk, try first)

| Technique | Pragma | Effect | When to use |
|---|---|---|---|
| Acknowledge II | `#pragma HLS PIPELINE II=<N>` | Prioritize II over satisfying timing pressure | II violation in csynth report (to acknowledge the real achievable II) |
| Loop unroll (partial) | `#pragma HLS UNROLL factor=<N>` | Replicates loop body N times, reduces trip count by N | Inner loop with known trip count divisible by N |
| Loop unroll (full) | `#pragma HLS UNROLL` | Fully unrolls loop; all iterations in parallel | Short loops (≤ 16 iterations), sufficient resources, constant loop trip count |
| Array partition (cyclic) | `#pragma HLS ARRAY_PARTITION variable=<x> cyclic factor=<N> dim=<D>` | Creates N memory banks; N parallel accesses per cycle | Memory port II bottleneck |
| Array partition (complete) | `#pragma HLS ARRAY_PARTITION variable=<x> complete dim=<D>` | Fully registers the array (no BRAM) | Small arrays only |
| Array partition (block) | `#pragma HLS ARRAY_PARTITION variable=<x> block factor=<N> dim=<D>` | Splits into N contiguous blocks | When access pattern is block-sequential |
| Loop flatten | `#pragma HLS LOOP_FLATTEN` | Merges nested loops into a single loop counter | Nested loops with loop-invariant bounds |
| Dataflow | `#pragma HLS DATAFLOW` | Task-level pipelining between functions or loops | Sequential stages that can overlap, non-innerloop pipelining |
| Expression balance | `#pragma HLS EXPRESSION_BALANCE` | Allow expression tree balancing on float | Floating point reductions in critical path |

### Algorithmic changes (higher risk, higher reward)

| Technique | Effect | When to use |
|---|---|---|
| Loop reordering | Changes memory access pattern; may improve spatial locality or expose better reuse | Poor memory reuse in inner loop; can turn random access into sequential |
| Tiling / blocking | Reuses on-chip data, reduces off-chip bandwidth, make buffer size constant | Memory bandwidth bound, variable size data to chunk into fixed size buffer |
| Local buffer | Stage data into local arrays to decouple memory access from compute | Repeated accesses to same memory region |
| Scalarization | Store data into individual scalars to allow arbitrary accesses and additional simplifications | Repeated accesses to the same memory element; can allow infinite access per cycle |
| Loop fusion | Merge two loop body into the same loop to reduce storage and allow for pipelining | Two consecutive loops with identical loop trip count working on the same buffers |
| Loop fission | Split the loop body into two separate loop to create independent processes in dataflow context | Loop body working on independent arrays/streams causing stall or complex control |
| Replace `float` with `ap_fixed<W,I>` | Shorter pipeline, fewer DSPs, faster clock | Fixed-point arithmetic acceptable for the application |
| Replace division with reciprocal multiply | Eliminates expensive divider | Division inside a loop by constant divisor |

### HLS library usage

```cpp
#include <ap_int.h>              // ap_int<N>, ap_uint<N> — arbitrary-width integers
#include <ap_fixed.h>            // ap_fixed<W,I> — fixed-point arithmetic
#include <ap_float.h>            // ap_float<W,E> — floating-point arithmetic with custom precision
#include <hls_math.h>            // hls::sqrt, hls::exp, etc. — HLS-optimized math
#include <hls_vector.h>          // hls::vector<T,N> — SIMD-style vectorized types
#include <hls_array_partition.h> // hls::scatter<T,K>, hls::gather<T,K> — SIMD-style scatter/gather on local arrays
#include <hls_stream.h>          // hls::stream<T> — FIFO communication between tasks
#include <hls_burst_maxi.h>      // hls::burst_maxi — high-performance M-AXI burst
```

## Step 4: Implement the change

Use the template to launch a sub-agent for each attempt. Fill in all bracketed fields before launching.

Key rules for the sub-agent:
- Make **only** the described change. Do not opportunistically fix other things.
- After each tool run, **read the output carefully** before deciding to proceed.
- If csynth warnings or loop table do not match the hypothesis, investigate before escalating.

## Step 5: Investigate the result thoroughly

For `run csynth`, do not just check the summary. Investigate systematically:

### 5a. Check for ignored-pragma warnings in the HLS log

Do this first — before reading any report. HLS frequently silently ignores pragmas that cannot be applied and emits a warning explaining why. If a pragma was ignored, the change you intended was **not applied** and the csynth result reflects the unmodified schedule. Reading the reports without knowing this leads to wrong conclusions.

check `pragma\|ignored\|cannot\|not applied\|warning` in `$synthesisLogContent` for any ignored pragma warnings.

Common ignored-pragma patterns to look for:

| Warning text (approximate) | Meaning |
|---|---|
| `pragma HLS PIPELINE ignored` | Loop is not eligible for pipelining (e.g. contains a sub-loop, variable trip count, or non-trivial control flow). |
| `pragma HLS UNROLL factor=N ignored` | Loop body cannot be fully unrolled (e.g. trip count not statically known, or factor does not divide trip count). |
| `pragma HLS ARRAY_PARTITION … ignored` | Variable is not a local array, or partition dim exceeds array rank. |
| `pragma HLS LOOP_FLATTEN ignored` | Loop bounds are not loop-invariant — flattening would change semantics. |
| `pipeline II target … cannot be achieved` | The target II was set but the scheduler could only achieve a higher value. Check the Violation Report for root cause. |

If a pragma was ignored, fix the pragma or restructure the code and re-run before drawing any conclusions from the reports.

### 5b. Read the synthesis report

Use the `synthesisReportContent` to check the loop table for the loops of interest. Look at II achieved vs. target, iteration latency, and resource usage.

Check:
- Did II change on the expected loop?
- Did II change on any other loop (unexpected side effect)?
- Did total latency change by the expected factor?
- Did resource usage change? By how much?

Also check for general synthesis warnings:

check `warning\|critical\|fail\|error` in `synthesisReportContent` and `synthesisLogContent` for any synthesis warnings.

### 5c. Read the Violation

Check violation in `synthesisLogContent` for any II or Timing violations.

### 5d. Read the inferred directives

First, find the inferred directives file within the component directory:

```bash
find $component -name "inferred_directives.ini" 2>/dev/null
```

Then read the file to check whether HLS auto-applied any directives you didn't expect. Array partitions, loop flattening, pipeline pragmas can be inferred automatically and can interact with your pragma.

### 5e. Verify transformation in synthesis log (when hypothesis is about compiler behavior)

When you want to verify that HLS actually applied the transformation you intended (e.g., that a partition was respected, or that a loop was actually unrolled), search `synthesisLogContent` for key indicators.

**Search patterns by pragma type:**

| Pragma | Search pattern in `synthesisLogContent` | Confirmation |
|--------|----------------------------------------|--------------|
| `ARRAY_PARTITION` | `partitioned\|partition.*factor\|partition.*complete` | Look for "partitioned into N banks" or similar messages |
| `UNROLL factor=N` | `unroll\|unrolled\|trip count` | Look for "loop completely unrolled" or "loop unrolled by factor N" |
| `LOOP_FLATTEN` | `flatten\|flattened\|merged` | Look for "loop flattened" or "loops merged" messages |
| `PIPELINE` | `pipeline\|pipelined\|II=` | Look for "loop pipelined with II=N" |
| `DATAFLOW` | `dataflow\|FIFO\|channel` | Look for dataflow region and channel creation messages |

**Example grep commands:**

```bash
# Check if partition was applied
echo "$synthesisLogContent" | grep -i "partition"

# Check if unroll was applied
echo "$synthesisLogContent" | grep -i "unroll"

# Check if pipeline achieved target II
echo "$synthesisLogContent" | grep -i "pipeline.*II"

# General transformation summary
echo "$synthesisLogContent" | grep -iE "applied|transformed|optimized|inferred"
```

**Key things to look for:**
- After `ARRAY_PARTITION`: messages confirming partition into N banks, or warnings if partition was not applied
- After `UNROLL factor=N`: messages showing "unrolled by factor N" or "completely unrolled"
- After `LOOP_FLATTEN`: messages showing nested loops were merged into a single loop
- After `PIPELINE`: messages showing achieved II value

**If the expected transformation message is not found**, the pragma may have been ignored — cross-reference with Step 5a for ignored-pragma warnings.

### 5f. Log the result

```bash
python3 "$qorLogScriptFullPath" --report "$synthesisReportContent" --label "<technique-applied>" --csv .memory/qor_history.csv
```

This appends a row to `.memory/qor_history.csv` for tracking across attempts.

## Step 6: Record the result — MANDATORY after every attempt

**Do this before deciding whether to escalate or start the next attempt. Never skip this step.**

### 6a. Update `.memory/optimize_outcomes.md`

Append a row to the outcomes table immediately after reading the csynth report. Use the present attempt's data — do not wait until the end of the session. Include:
- Technique name
- Observed effect (cycles before → after, II change)
- Whether the hypothesis was confirmed
- Any unexpected behavior, side effects, or lessons

This file is read at the start of every session. If it is not updated after each attempt, the next session will repeat experiments that have already been run.

### 6b. Commit the state — MANDATORY, including for failed attempts

**Every attempt gets its own commit before anything else happens — including attempts that did not improve the metric.** The commit must happen *before* any `git checkout`, `git restore`, file edit, or next-attempt work. Skipping the commit on failure loses the experiment from history and is the most common mistake in this workflow.

Order of operations after every attempt (no exceptions):
1. Update `.memory/optimize_outcomes.md` (Step 6a).
2. `git add` + `git commit` (this step) — even if the build broke or the result was worse.
3. *Only then* may you revert, adapt, or move on.

**If the attempt improved the target metric or confirmed a useful hypothesis (keep the code):**

```bash
git add <source_file> .memory/optimize_outcomes.md
git commit -F - <<'EOF'
<technique>: <what changed> → <observed effect>

Hypothesis: <what you expected>
Observed: <what actually happened in csynth/cosim/impl>
Baseline: cosim=<X> cycles, post-route=<Y> ns, true latency=<Z> ms
After:    cosim=<X'> cycles, post-route=<Y'> ns, true latency=<Z'> ms
Resources: LUT <A>→<A'>, DSP <B>→<B'>
EOF
```

**If the attempt did not help, latency got worse or not improved — commit first, then revert:**

```bash
# 1. Commit the failed state as-is (code + memory update) so the exact change is preserved
git add <source_file> .memory/optimize_outcomes.md
git commit --allow-empty -F - <<'EOF'
experiment(<technique>): <what changed> — did not help

Hypothesis: <what you expected>
Observed: <what actually happened — why it failed or made QoR worse / etc.>
EOF

# 2. Verify the commit actually landed before reverting. If `git status` is not clean
#    after the commit, STOP and investigate — do not run the checkout below.
git log -1 --oneline
git status --short

# 3. Only after the commit is confirmed, revert the kernel to the previous working state.
git checkout HEAD~1 -- <source_file>
```

`--allow-empty` ensures the commit still lands even if the only thing that changed was a file that has since been auto-regenerated to its prior content (e.g., a report). The verification step (`git log -1` + `git status --short`) is what catches the case where the commit silently did not happen — if you see your commit in `git log` and `git status` is clean, the failed attempt is safely preserved and you may revert.

Committing before reverting preserves the exact failing code in history, making it possible to inspect, diff, or re-apply it later. A failed experiment that teaches you something is not wasted work.

## Step 7: Decide whether to escalate

| csynth result | Action |
|---|---|
| Latency improved ≥ 10% OR II reduced on a dominant loop | Escalate: run cosimulation flow |
| Latency unchanged, but hypothesis was confirmed (e.g. II matched expected value) | Valid data. Move on to the next hypothesis. |
| Latency got worse | Investigate why, then **commit (Step 6b) before reverting**. The result may reveal a real constraint. |
| csim FAIL | Fix logic error or revert immediately. |

For `run cosim`: call `hls-cosim-report` skill to get `coSimulationReportContent` and `dataflowProcessAndChannelContent`. Compare cosim cycles to csynth estimate. For designs with memory backpressure, cosim can be significantly worse than csynth estimates; for compute-bound kernels, they should be close.

For `run impl`: only run when cosim confirms latency improvement. Call `hls-impl-report` skill and use `postRoute` for the actual post-route clock period and compute true latency = cosim_cycles × period_ns.

**DO NOT** read `.rpt` files directly using file read tools to extract information. Always use the provided functions to ensure consistency and correctness.

## Step 8: Update skills with lessons learned

After each attempt — successful or not — update the relevant `SKILL.md` with findings that are general enough to apply to future kernels:

- If a technique had an unexpected interaction with HLS (e.g., auto-inferred flatten conflicted with your pipeline pragma), note it.
- If the Violation Report pointed to a root cause that wasn't obvious from the loop table, note the pattern.
- If the IR inspection revealed something unexpected (e.g., the partition was not reflected in the IR), note it.

## Cost model for the inner loop

| Step | Typical runtime | When to run |
|---|---|---|
| `run csim` | 5–30 s | Always — correctness gate |
| `run csynth` | 10–60 s | Always — the main investigation tool |
| `run cosim` | 30 s – 5 min | When csynth shows ≥ 10% improvement in latency cycles, or a structural improvement (II reduction on dominant loop) |
| `run impl` | 1 – 30 min | When cosim confirms improvement |

## Stopping criteria

Stop iterating when any of the following is true:
- The optimization criteria is met.
- Three consecutive attempts produced no improvement, and no new hypothesis remains to test.
- Resource utilization is approaching device limits (> 60% of any constrained resource) and further improvement requires more resources.
- The improvement per attempt has diminished to < 5% of baseline.

When stopping criteria are met, summarize the lessons learned.

**In interactive mode**: ask the user if they want to update the relevant `SKILL.md` with the new insights. The update role is described in step 8 above.

**In non-interactive mode** (invoked via `claude --print`): skip the prompt — do NOT update any `SKILL.md`. Print the summary and exit.

## Known outcomes

Outcomes are recorded in `.memory/optimize_outcomes.md`.
Read this file at the start of each session to avoid repeating experiments.
