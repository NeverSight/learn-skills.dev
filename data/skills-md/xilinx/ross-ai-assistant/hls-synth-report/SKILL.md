---
name: hls-synth-report
description: 'Get Vitis HLS synthesis report information (synth report, pragma report, and filtered synthesis log) for a given HLS component.'
license: MIT
metadata:
  author: "Alex Li"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# hls-synth-report

Collect **Vitis HLS C synthesis** artifacts from an HLS component directory and emit a single JSON object.

## When to use

After C synthesis (`csynth`) has completed, use this skill to inspect performance/resource estimates, applied pragmas, and synthesis warnings/errors for a component.

**Prerequisite:** the component must contain `hls/syn/report/csynth.rpt` and `hls/../logs/hls_compile.log`.

## Inputs

- `component_location` (string, required) — absolute path to the Vitis HLS component directory (the folder containing `vitis-comp.json`).
  - If the user specifies a component_location: use the user-specified component_location.
  - If the user does not specify component_location:
    - If inside Vitis Unified IDE: Call the `getActiveComponentLocation` tool to get the component_location.
    - If outside Vitis Unified IDE: Request the user to provide component_location.

## Output

JSON object printed to `stdout` with three string fields:

```json
{
  "synthesisReportContent": "...",        // csynth.rpt, truncated at the modules/loops marker
  "synthesisPragmaReportContent": "...",  // content from "== Pragma Report" to end
  "synthesisLogContent": "..."            // hls_compile.log, with noisy INFO: lines filtered out
}
```

## How to invoke

Two equivalent methods — same JSON shape.

### 1. Inside the Vitis Unified IDE (preferred)

Call the `getHLSSynthesisInfo` tool if available. It uses the currently selected project.

### 2. Outside Vitis Unified IDE (fallback)

Must `cd` into `./hls-scripts/` first.

```bash
cd ./hls-scripts
./run.sh <component_location>
```

Script source: [run.sh](./hls-scripts/run.sh)
