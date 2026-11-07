---
name: hls-component-basic-info
description: 'Get Vitis HLS component basic informations for a given HLS component. The basic informations includes component name, source files, testbench files, include paths and top function'
license: MIT
metadata:
  author: "Alex Li"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# hls-component-basic-info

This skill collects **Vitis HLS component basic** information from an HLS component directory.

It is implemented by calling the script:

- [run.sh](./hls-scripts/run.sh)

That script:
- takes exactly **one argument**: `<component_location>`
- prints a JSON object describing the content of component basic info

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
    - `component_name` (str of component name)
    - `source_files` (list of source file path)
    - `testbench_files` (list of testbench file path)
    - `include_paths` (list of include path)
    - `top_function` (str of top function)

## How to invoke

Must `cd` into `./hls-scripts/` first.

```bash
cd ./hls-scripts
./run.sh <component_location>
```
