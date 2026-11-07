---
name: hls-ii-diagnose
description: 'Diagnose the root cause of an II (initiation interval) violation in a synthesized Vitis HLS component, classify the bottleneck, and cite the supporting evidence — without modifying source or running flows.'
license: MIT
argument-hint: <component_location> [loop-or-function-label]
metadata:
  author: "Zayn He"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->
# hls-ii-diagnose

Diagnose **why** a pipelined loop or function did not reach its target II, classify the bottleneck into a known category, and cite the evidence. This skill produces a *diagnosis only* — the calling agent (e.g. `hls-optimize`) decides whether and how to fix it.

## Why this skill exists

An II violation can stem from several distinct root causes that need completely different fixes, and the csynth summary table does not distinguish them — its violation labels are coarse (e.g. "Memory Dependency" is reported for recurrences that have nothing to do with memory ports), so agents reading only the summary often misdiagnose. Sweeping `#pragma HLS PIPELINE II=<N>` is also not a substitute for diagnosis: it works only when the fix happens to be an II target, can hurt timing, and never finds a structural fix (inline a callee, disable a shared mux). This skill forces a real diagnosis first.

## When to use

Use after C synthesis (`csynth`) has completed, when a pipelined loop or function has an achieved II greater than 1 — either `II achieved` > `II target` when a target is set, or `II achieved` > 1 with no target set.

**Out of scope:** choosing/applying the fix (that is the caller's decision), running any flow, and designs whose II already meets target.

## Inputs

- `component_location` (string, required) — absolute path to the Vitis HLS component directory (the folder containing `vitis-comp.json`).
  - If the user does not specify it and you are inside the Vitis Unified IDE, call `getActiveComponentLocation`. Otherwise ask the user.
- `target_label` (string, optional) — a specific loop or function to focus on. If omitted, diagnose the loop/function with the worst `II achieved / II target` ratio.

## Prerequisite

The component must already be synthesized. This skill does **not** run flows. If the synthesis reports/log are missing or stale, ask the caller to run `hls-run-flow` first.

## Workflow

### Step 1 — Get the synthesis report and log

Invoke the `hls-synth-report` skill on `component_location` to obtain `synthesisReportContent`, `synthesisPragmaReportContent`, and `synthesisLogContent`. Use the report to find the loop/function with the worst II ratio if no `target_label` was given.

### Step 2 — Extract the pipelining block(s)

**Do not rely on the summary tables.** The real evidence is in the per-loop/function block delimited by `Pipelining loop ...` / `Pipelining function ...` and `Pipelining result ...` in the synthesis log. These blocks contain the carried-dependence warning (`HLS 200-880`), scheduler notes, and resource-limit messages.

**Use the raw `logs/hls_compile.log`, not the filtered log.** The `Pipelining loop ...` / `Pipelining result ...` markers are `INFO:` lines, and the `hls-synth-report` skill filters `INFO:` lines out of `synthesisLogContent` — so they are missing from the filtered content. Read the component's raw log at `<component_location>/logs/hls_compile.log`.

Pull the block for each loop/function with `awk` over the markers:

```bash
LOG=<component_location>/logs/hls_compile.log
# all pipelining blocks (each ends with its "Pipelining result" line showing Target/Final II):
awk '/Pipelining (loop|function)/{f=1} f; /Pipelining result/{f=0}' "$LOG"
# jump straight to the result lines to spot violations (Final II > Target II, or > 1 with no target):
grep -E "Pipelining result" "$LOG"
# then read the full block for the violating target by name:
awk "/Pipelining (loop|function) '<target_label>'/{f=1} f; /Pipelining result/{f=0}" "$LOG"
```

Read the full block — not just the result line. Note the carried variable name and type (scalar vs array element), the distance/offset, the producer/consumer line numbers (`HLS 200-880`), and any timing (`HLS 200-887`) or resource-limit messages.

### Step 2b — Confirm the long-latency element in the schedule report

When the violation is a carried dependence (a recurrence across iterations), the log's `HLS 200-880` line names the carried *variable* and the producer/consumer ops, but it does **not** always reveal *which* operation on the path carries the latency (e.g. it may name only a `store`/`load` of the carried scalar, while the real cost is a non-inlined call between them). Do not infer this from source alone — confirm it in the **authoritative schedule report**:

```
<component_location>/hls/.autopilot/db/<module>.verbose.sched.rpt
```

where `<module>` is the violating loop/function's module name from the `HLS 200-880` message (e.g. `test_Pipeline_encryption_cfb8_loop`). Each line shows an operation, the schedule stages it spans (`[20/20]…[1/20]` = a 20-stage operation), and its delay, e.g.:

```
ST_3 : Operation 72 [20/20] (1.18ns) ---> "%output_block = call i8 @process, ..." [cfb.hpp:442] ---> 'call' ...
```

Trace the recurrence on the carried variable through the stages: the operation that spans the most stages (or whose delay dominates) between the carried store and its next-iteration load **is** the long-latency element — and tells you directly whether it is a `call` (→ inline), a memory `load`/`store` (→ lower memory latency), or a long arithmetic chain (→ restructure). Cite the specific `ST_n … Operation … (delay)` lines as evidence.

### Step 3 — Classify the bottleneck

First decide whether the limiter is a **carried dependence** (a recurrence across iterations) or a **resource shortage** (a single-iteration access that exceeds available resources). Then pick the specific category:

**Pre-check**

- **(a) No II target** — no `II=<N>` was specified. Without a target, timing constraints take priority over most II-related constraints, so HLS may relax II to whatever satisfies timing. You are encouraged to verify this is actually the cause — e.g. some operations on the recurrence path were given longer latency to satisfy timing — before classifying as (a). The natural check is whether re-synthesizing with an explicit II target would close the gap (but that is the caller's action, not this skill's).

**Carried-dependence bottlenecks**

- **(b) Long latency on the recurrence path** — the recurrence carries a dependence whose round-trip latency the scheduler cannot fit into the target II, so II grows to cover it. The general task is to find *which element on the path is long and why the scheduler cannot shorten it*. Common sources (not exhaustive):
  - a non-inlined function call, treated as a black-box latency the scheduler cannot retime across;
  - a memory load/store whose access latency sits on the path;
  - a registered shared-resource mux inserted by resource sharing;
  - a long combinational chain that the scheduler lengthened to satisfy timing (overlaps with (a) when no II target was set).

  Identify the specific source using the schedule report (Step 2b) — the carried variable, the operations on the path (`load`/`store`/`call`/`add`/…), and their per-operation latencies — because the fix direction depends on it (inline the callee, lower the memory latency, disable sharing, or restructure to shorten the chain).

**Resource-shortage bottlenecks**

- **(c) Memory port shortage** — within a single iteration, the unrolled accesses to a memory exceed its available ports. This is *not* a cross-iteration dependence; it surfaces as a different class of violation in the log.

**Categories are not mutually exclusive — report every cause the evidence supports.** Two situations call for reporting more than one:

- **Co-occurring causes.** A single violation can have more than one real cause at once. The most common pair is (a) + (b): no II target was set *and* the recurrence carries a long-latency element. Here both are true and both matter — without a target the scheduler never tries to shorten the path, and even with a target the path latency still caps the achievable II. Report both, and make the relationship explicit (e.g. "(b) is the physical limiter; (a) is why the scheduler accepted the relaxed II"). The `next_step` should then cover both levers (set an II target *and* shorten the path).
- **Genuine ambiguity.** If the evidence cannot distinguish between two plausible categories, report both with their supporting evidence rather than guessing.

### Step 4 — Locate the source

Identify the source location of the bottleneck: the carried variable, the callee, or the memory access, depending on the category. Use the line numbers from the `HLS 200-880` message and the source files reported by `hls-component-basic-info` if needed.

### Step 5 — Cite the evidence

For every claim in the diagnosis, point at the supporting artifact: synthesis-log line(s) (the `HLS 200-880`/`HLS 200-887` text and the `Pipelining result` line), the `verbose.sched.rpt` `ST_n … Operation … (delay)` line(s) that identify the long-latency element (Step 2b), and source line(s). The caller must be able to verify the diagnosis independently. For a category (b) classification, the schedule-report citation is what distinguishes a grounded diagnosis from a guess — prefer it over inferring the long-latency element from source.

## Output

Emit a structured diagnosis:

- `target_label` — the loop or function being diagnosed
- `achieved_ii` / `target_ii`
- `category` — one or more of (a)–(c) above (report all that the evidence supports; see Step 3); for (b), name the specific long-latency source on the path
- `evidence` — log line numbers, source line numbers, schedule excerpts
- `next_step` — high-level recommendation (e.g. "specify II target", "inline callee", "lower memory latency", "increase memory ports", "restructure to break recurrence"). Pragma or directive names (e.g. `inline`, `bind_storage`) may appear **only when paired with the mechanism they address**. The caller makes the final decision on whether and how to apply them.

## Constraints

This skill MUST NOT:

- Modify source files.
- Run csim / csynth / cosim / impl flows. (Use `hls-run-flow` for that.)
- Recommend a fix without naming the underlying mechanism.
