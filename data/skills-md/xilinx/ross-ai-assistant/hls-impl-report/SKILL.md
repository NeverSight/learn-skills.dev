---
name: hls-impl-report
description: 'Get Vitis HLS implementation report information (post-route clock, resource utilization,Fail Fast table gives utilization percentages) for a given HLS component.'
license: MIT
argument-hint: "[<component_location — path to the HLS component directory containing vitis-comp.json>]"
metadata:
  author: "Alex Li"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# hls-impl-report

Collect **Vitis HLS C implementation** artifacts from an HLS component directory and emit a single JSON object.

## When to use

After run impl (`impl`) has completed, use this skill to inspect post-route timing, resource utilization, and implementation logs

---

**Prerequisite:** the component must contain `hls/impl/report/verilog|vhdl/export_impl.rpt`

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
  "postRoute": "...",        // export_impl.rpt, Place & Route Timing Summary->Post-Route value
  "placeRouteResourceSummary": "...",  // Place & Route Resource Summary-> LUT,FF,DSP,BRAM,URAM,SRL
  "placeRouteFailFast": "..."            // Place & Route Fail Fast LUT FD DSP percentage
}
```

## How to invoke

Two equivalent methods — same JSON shape.

### 1. Inside the Vitis Unified IDE (preferred)

Call the `getHLSImplementationInfo` tool if available. It uses the currently selected project.

### 2. Outside Vitis Unified IDE (fallback)

Must `cd` into `./hls-scripts/` first.

```bash
cd ./hls-scripts
./run.sh <component_location>
```

Script source: [run.sh](./hls-scripts/run.sh)
