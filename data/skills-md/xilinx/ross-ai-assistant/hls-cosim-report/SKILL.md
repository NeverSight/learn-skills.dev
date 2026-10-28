---
name: hls-cosim-report
description: 'Get Vitis HLS cosimulation report information for a given HLS component.'
license: MIT
metadata:
  author: "Alex Li"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# hls-cosim-report

Collect **Vitis HLS cosimulation** artifacts from an HLS component directory and emit a single JSON object.

## When to use

After cosimulation has completed, use this skill to inspect performance/resource estimates, dataflow process and channel infos for a component.

**Prerequisite:** the component must contain `hls/.autopilot/db/process_info.csv`.

## Inputs

- `component_location` (string, required) — absolute path to the Vitis HLS component directory (the folder containing `vitis-comp.json`).
  - If the user specifies a component_location: use the user-specified component_location.
  - If the user does not specify component_location:
    - If inside Vitis Unified IDE: Call the `getActiveComponentLocation` tool to get the component_location.
    - If outside Vitis Unified IDE: Request the user to provide component_location.

## Output

- `stdout`: JSON (pretty-printed)
  - Top-level: a JSON object.
  - The JSON object includes:
    - `coSimulationReportContent`
    - `dataflowProcessAndChannelContent`

## How to invoke

Two equivalent methods — same JSON shape.

### 1. Inside the Vitis Unified IDE (preferred)

Call the `getHLSCoSimulationInfo` tool if available. It uses the currently selected project.

### 2. Outside Vitis Unified IDE (fallback)

Must `cd` into `./hls-scripts/` first.

```bash
cd ./hls-scripts
./run.sh <component_location>
```

Script source: [run.sh](./hls-scripts/run.sh)
