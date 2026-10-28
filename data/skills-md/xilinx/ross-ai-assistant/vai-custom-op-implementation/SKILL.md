---
name: vai-custom-op-implementation
license: Apache-2.0 WITH LLVM-exception
compatibility: Requires VitisAI 6.3+
metadata:
  version: 6.3.0
  stage: beta
description: 'End-to-end custom AIE operator development for VAIML: extract a subgraph
  from an ONNX model, develop a custom kernel and tiling, validate with x86sim against
  a CPU reference, and re-integrate the custom op back into the full model. Use when
  the user wants to create a custom op, write a kernel, define tiling, compile for
  AIE, simulate with x86sim, or integrate a custom op into a model.'
---
<!--- Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.--->

# Custom Op Development Skill

## Access command

This skill must always be accessed through the worker, never in a different way.
Allowed worker: `vai-custom-op-worker`.

## Description

End-to-end workflow for developing custom AIE operators: extract a target subgraph, develop the custom op in isolation, validate with x86sim, and stitch the custom op back into the full model.

For developing **multiple** custom ops in parallel with coordinated agent teams,
use the `vai-custom-op` skill instead.

**IMPORTANT:** When any step fails (compilation, simulation, numeric comparison, integration), do not resort to trial and error. Instead, debug systematically: read the full error output, trace the data/control flow backward to find the root cause, and only then apply a targeted fix. Check if there are other skills available that can help with debugging. See the **Troubleshooting** section at the end of this document for common errors and their solutions.

## Table of Contents

- [Parse Arguments](#parse-arguments)
- [Environment Setup Convention](#environment-setup-convention)
- [Critical Workflow Rules](#critical-workflow-rules)
  - [1. Use Sub-Agents for Compilation and Simulation](#1-use-sub-agents-for-compilation-and-simulation)
  - [2. Use Local Git for State Management](#2-use-local-git-for-state-management)
  - [3. Using a board for validation and performance data retrival](#3-using-a-board-for-validation-and-performance-data-retrival)
  - [4. X86 Simulation using runner_type, and re-compiling](#4-x86-simulation-using-runner_type-and-re-compiling)
- [Development Methodology](#development-methodology)
- [Design Constraints: Inputs, Outputs, and Standard Library](#design-constraints-inputs-outputs-and-standard-library)
  - [Multi-input: pack extras into WTS via tiling and DMA](#multi-input-pack-extras-into-wts-via-tiling-and-dma)
  - [Multi-output: concatenate in the kernel, split via tiling and DMA](#multi-output-concatenate-in-the-kernel-split-via-tiling-and-dma)
  - [Innermost-dim DMA alignment: reshape over pad](#innermost-dim-dma-alignment-reshape-over-pad)
  - [Quantized subgraphs: absorb the boundary DQ/Q, make the op an int op](#quantized-subgraphs-absorb-the-boundary-dqq-make-the-op-an-int-op)
- [Compiler Flags: Do Not Touch the Model-Wide Knobs](#compiler-flags-do-not-touch-the-model-wide-knobs)
- [Stack and Heap Sizing](#stack-and-heap-sizing)
  - [The four checks you MUST apply](#the-four-checks-you-must-apply)
- [Phase 1: Subgraph Extraction](#phase-1-subgraph-extraction)
  - [1a. Extract the subgraph (Model A)](#1a-extract-the-subgraph-model-a)
  - [1b. Generate CPU reference data](#1b-generate-cpu-reference-data)
  - [1c. Create Model B (Custom Op model)](#1c-create-model-b-custom-op-model)
- [Phase 2: Create the Custom Op](#phase-2-create-the-custom-op)
  - [2a. Context analysis](#2a-context-analysis)
  - [2b. ONNX Custom Op YAML](#2b-onnx-custom-op-yaml)
  - [2c. Config YAML](#2c-config-yaml-custom_op_namenameyaml)
  - [2d. Kernel C++](#2d-kernel-c-custom_op_namenamecpp)
  - [2e. Tiling Python](#2e-tiling-python-custom_op_namename_tilingpy)
  - [2f. Vitis AI Config](#2f-vitis-ai-config-vitisai_configjson)
  - [2g. Tutorial Examples for Inspiration](#2g-tutorial-examples-for-inspiration)
- [Phase 3: Compile](#phase-3-compile)
- [Phase 4: Simulate and Validate](#phase-4-simulate-and-validate)
  - [4a. Run x86sim with the same inputs from Phase 1b](#4a-run-x86sim-with-the-same-inputs-from-phase-1b)
  - [4b. Compare x86sim output against CPU reference](#4b-compare-x86sim-output-against-cpu-reference)
  - [Debugging (only if 4b fails)](#debugging-only-if-4b-fails)
- [Phase 5: Kernel Optimization](#phase-5-kernel-optimization)
  - [Optimization is data-driven -- ALWAYS, board or no board](#optimization-is-data-driven----always-board-or-no-board)
- [Phase 6: Model Re-integration](#phase-6-model-re-integration)
  - [6a. Create the integration directory](#6a-create-the-integration-directory)
  - [6b. Stitch the custom op into the full model](#6b-stitch-the-custom-op-into-the-full-model)
  - [6c. Set up vitisai_config.json](#6c-set-up-vitisai_configjson)
- [Phase 7: End-to-End Verification](#phase-7-end-to-end-verification)
  - [7a. Compile the integrated model (REQUIRED)](#7a-compile-the-integrated-model-required)
  - [7b. Generate full-model CPU reference](#7b-generate-full-model-cpu-reference)
  - [7c. Compare outputs](#7c-compare-outputs)
- [Key Architecture Facts](#key-architecture-facts)
- [Script Reference](#script-reference)
- [Troubleshooting](#troubleshooting)
  - [Common Errors](#common-errors)
  - [Environment Setup Checklist](#environment-setup-checklist)

## Parse Arguments

This skill expects arguments in this form:

```
[operation_description] [--t <activate_path>] --model <onnx_model> --vitisai-config <config_json> --nodes <node1> [<node2> ...]
```

Extract from `$ARGUMENTS`:
- **Operation description**: what the custom op should do and which ops to target
- `--t <path>`: **(OPTIONAL)** Path to a Ryzen AI / Vitis AI / product virtual environment activate script. Provide this only when the Python environment is NOT already on the shell. Omit it when the environment is pre-provisioned (e.g. inside the official Vitis AI Docker container, where `flexml`, `onnx`, `onnxruntime`, etc. are already importable from system Python). See "Environment Setup Convention" below.
- `--model <path>`: **(MANDATORY)** Path to the ONNX model file
- `--vitisai-config <path>`: **(MANDATORY)** Path to the vitisai_config.json file
- `--nodes <node1> [<node2> ...]`: **(MANDATORY)** Node names or op types to extract as a custom op subgraph

Skill directory: the directory containing this SKILL.md file (referred to as `<skill_dir>` below).

**Validation**: Before proceeding, verify all mandatory arguments are present. If any are missing, ask the user to provide them. Do NOT treat `--t` as missing-and-required: its absence is a deliberate signal to skip venv sourcing (see next section).

## Environment Setup Convention

This skill supports two deployment models:

1. **Sourced venv**: the user passes `--t <path>` and every shell that runs `python3` / `aiecompiler` must `source <path>` first.
2. **Pre-provisioned environment** (e.g. official Vitis AI Docker container, sandbox image): the Python packages and binaries are already on `PATH` / `PYTHONPATH`. `--t` is NOT provided; no sourcing is needed.

Wherever this document shows `<ENV_SETUP>` inside a bash snippet, expand it as follows:
- If `--t <path>` was provided: replace the `<ENV_SETUP>` line with `source <path>`.
- Otherwise: delete the `<ENV_SETUP>` line entirely.

**Do NOT auto-detect or guess an activate script.** If `--t` is absent, trust that the calling shell already has `python3 -c "import flexml"` working. Searching the filesystem for a venv to source is a bug, not a fallback.

A quick sanity check you MAY run once at startup (especially when `--t` is absent) is `python3 -c "import flexml, onnx, onnxruntime"`. If that fails, stop and ask the user how the environment should be set up rather than hunting for one.

## Critical Workflow Rules

### 1. Use Sub-Agents for Compilation and Simulation

**NEVER run compilation or simulation commands directly in the main agent.** These produce verbose output that pollutes the main context window. Always use the vai-custom-op-worker sub-agent.

**For compilation:**
```
Use Agent tool with subagent_type="vai-custom-op-worker" and a prompt like:
"Run the following command and report whether it succeeded or failed,
including any error messages if it failed:
bash -c '
<ENV_SETUP>
export DEBUG_VAIML_PARTITION=1
export FLEXML_PRINT_VITISTOOLS_OUTPUT=1
cd <working_dir>
python <skill_dir>/scripts/compile.py <model>.onnx
'"
```

**For x86sim** (same cache as the compile above; the x86sim config selects the runner -- see Critical Workflow Rule 4):
```
Use Agent tool with subagent_type="vai-custom-op-worker" and a prompt like:
"Run the following command and report the full output, especially any
printf statements from the kernel and the final pass/fail status:
bash -c '
<ENV_SETUP>
cd <working_dir>
python <skill_dir>/scripts/run.py <model>.onnx \
    --input-dir <working_dir>/reference_data \
    --output-dir <working_dir>/x86sim_outputs \
    --vitisai-config vitisai_config_x86sim.json --num-runs 1
'"
```

The sub-agent will return a concise summary. Only escalate to the main context if there are errors that need debugging.

### 2. Use Local Git for State Management

**ALWAYS create a local git repo in the working directory** at the start of development. Commit after every successful milestone so you can easily revert to a known-good state when experimenting. **EXCEPTION** If the user doesn't have git available in their workspace, you can skip this section and the saving of milestones. You should still do defensive programming and create backups if you're not sure about the changes you're about to perform.

```bash
cd <working_dir>
git init
git add -A
git commit -m "Initial custom op files for <op_name>"
```

**Commit at these milestones:**
- After creating all initial files (Phase 2)
- After successful compilation (Phase 3)
- After successful x86sim (Phase 4)
- Before attempting any optimization (Phase 5)
- After each successful optimization step (Phase 5)

### 3. Using a board for validation and performance data retrival

Always establish that there is a board or a script to execute inference on a board
before starting:

- Use the `scripts/run_on_board.py` next to this skill, unless the user tells you otherwise, in which case
  you need to follow the user's instructions and commands.

- If the board run script fails to reach a board (unreachable board or no board), STOP and ask the user
  if and how they run inference on their board (their own script, harness, or command). Board execution
  might be mandatory or optional depending on user's goals and it is not possible to disambiguate,
  unless explicitely mentioned in the prompt. You MUST prompt the user with the following warnings about not having
  a board in the loop:
    - Not having a board might impact functional correctness. Without board testing, this skill can only rely on x86sim for
      numeric accuracy which doesn't map one to one to the hardware.
    - Not having a board impact the data-driven optimization loop because optimization will only be guided by static metrics
      such as static code analysis and initiation intervals. Without dynamic data optimization is a best guess and it can result
      in sub-optimal solutions
  The user MUST give explicit consent to the above points.
- If the user cannot provide board access, offer to switch to static data collection for performance guidance
  and function validation throuh x86 simulation.
- **Headless (no interactive user):** don't block on the question -- proceed with
  static analysis (Phase 5a) and report that latency was not measured.

### 4. X86 Simulation using runner_type, and re-compiling

**One compile serves both hardware and x86 runners, but you MUST ask for the x86
half.** The default build emits only the hardware artifacts (`ctrl_pkts.xclbin`,
`aie_control.elf`) and records `runner_type: "hw"` in the cache. The x86
simulator library (`libx86_sim.so`) is built only when `aiecompiler_args`
carries both of these flags:

```json
      "aiecompiler_args": "--compile-for-x86sim=true --x86sim-as-shared-library=true",
```

**Always include `--msg-severity="77-23879:error:100"`** to promote the hardware-only L2 shared-buffer overlap warning to a compile error (x86sim ignores it, but it corrupts results on the board).

**The runner is chosen at run time, by the config you hand `run.py`.** Keep a
copy of the vitisai config with one extra key and use different processes for compilation and simulation:

```json
    "runner_type": "x86sim",
```

Pass that copy to `run.py` and the VitisAI EP loads the simulator as a shared
library, so an ordinary ONNX Runtime session *is* the simulation -- against the
same Phase 3 cache, with no recompile. Pass the normal config and the same cache
runs on the board.

**Never put `runner_type: "x86sim"` in the config you compile with.** The value
is written into the cache, and omitting the key later means *unspecified*, not
`"hw"` -- so a subsequent board run falls back to the cached `x86sim`, tries to
load the x86-64 `libx86_sim.so` on the aarch64 board, and fails (see
Troubleshooting). The effective runner is the config's value when present,
otherwise the cached one.

**x86sim is functionally correct, not bit-accurate.** It compiles the kernel for
native x86 while the AIE path may use emulated fp32, so the two round
differently on values near a rounding boundary. Use it to catch functional bugs
(wrong tile, wrong core offset, wrong axis, garbage output); keep the board as
the authority for any exactness claim.

**Both runners are the same `run.py`, so an x86sim run destroys a board run's
profiling data in the same directory.** Profiling is always on and the artifacts
land in the working directory, not in `--output-dir`. Session creation deletes the
whole `record_timer_*.json` glob while `partition.json`/`summary.csv` survive
stale, so spot-checking those two misleads. x86sim also writes only host
wall-clock timers -- `record_timer_ts.json` (NPU cycles) is **board-only**. Copy
board artifacts aside, or simulate elsewhere, before running `/vai-perf-analysis`.

**You MUST re-run `compile.py` after changing any custom op file** -- kernel
.cpp, tiling Python, YAML config, ONNX model, or `vitisai_config.json` -- before
simulating or running on the board. Nothing in the run path recompiles.

## Development Methodology
Start with a single-stamp, 16-core implementation -- x86sim validates correctness on all 16 cores. Use the `mul/2_distributed` or `negate/2_distributed` tutorials as starting templates.

**Always use the AieConfig signature:** `getTiling(opInterface, tiling: tensor_expr.AieConfig)` -- an `AieConfig` has one entry per overlay stamp, so it works on a single-stamp overlay and requires no rewrite when the op moves to a multi-stamp one (see `tiling.md`).

**Honor `tp_size` (from the vitisai_config).** `tp_size: N` provisions the overlay with N stamps (N*16 cores) but does not by itself use them -- your tiling decides. If `tp_size: N` (N>1), distribute across all N stamps (`assert len(tiling) == N`) by giving each its own slice of the DDR tensor; configuring only one leaves N-1 stamps idle. Treat a user-provided `tp_size` as a hard requirement.

1. **4x4 distributed** (single-stamp) -- scalar kernel, validate correctness with x86sim
2. **Optimized kernel** -- vectorize with `aie::vector`, add `AIE_PIPELINE` hints

## Design Constraints: Inputs, Outputs, and Standard Library

Custom ops supports many inputs while being only limited by the amount of channels connecting
the DDR to the memory tiles. Each channel can be configured independently during tiling and
associated to different (or the same) DDR inputs. The connections from the memory tiles to the cores
are limited to 2, i.e, there are only 2 physical channels that we can use to push data from the memory tiles
into the core tiles. The best possible solution when dealing with more than 2 inputs is to use the DMA controllers
to pack or concatenate the variables when reading from DDR into the memory tiles. This comes at zero cost
but it is not a generic solution to all the custom ops since whatever variables are created in the memory tiles
still need to be themselves tiled and transferred to the cores.

Custom ops only support **1 output tensor**. The best known solution for dealing with multiple outputs - within one
custom op - is to concatenate the multiple results in the memory tile varible and use `onnx.Slice` or another custom op
to split the results into two or more, while updating the respective consumers.

When possible, always prefer a solution that works around the arity limits using the Tiling API and the DMA controllers - not by adding nodes to the ONNX graph - as to avoid round trips to the DDR memory which reduce data locality and are expensive.

### Multi-input: pack extras into WTS via tiling and DMA

Favor L2 packing: whenever possible, carefully choose a L2 location for each input
and read it into L2 from L3 with a dedicated channel; send the resulting packet to L1.
You usually need two L2 buffers; one to be sent across columns to L1, and one to be
sent across rows.

If absolutely necessary, you may resort to packing data in L3 using ONNX
`Concat` nodes. Keep the ONNX graph lean -- avoid auxiliary `Concat`/`Reshape` nodes
whose only purpose is to assemble WTS. The kernel can read each component
from a fixed offset inside the IFM/WTS buffers.

Example: an op with 3 dynamic inputs (`input_a`, `input_b`, `input_c`)
plus constant `weights`. Concat the dynamic inputs into IFM and pack
`input_c` alongside `weights` in WTS:
```
IFM = [input_a(64), input_b(64)]      = [128]    -- dynamic inputs concatenated
WTS = [weights(8448), input_c(960)]    = [9408]   -- weights + dynamic input packed
```
The kernel reads `input_b` from `ifm[64]` and `input_c` from `wts[8448]`.
Choose IFM vs. WTS based on the broadcast pattern: on the 4x4 overlay
IFM is broadcast column-wise and WTS row-wise.

### Multi-output: concatenate in the kernel, split via tiling and DMA

Write all logical outputs concatenated into one contiguous OFM buffer in
the kernel. Use tiling transforms on `ofm_mem` (`Reshape`, `Transpose`,
`TileTo`, `SpatialDistribute2D`) so the L2 -> DDR DMA reorders/splits
the concatenated OFM and each logical output lands contiguously in DDR.
This avoids per-invocation ONNX `Slice`/`Reshape` nodes downstream. For
chained ops, the concatenated output can feed directly as the next op's
IFM without any explicit split.

### Innermost-dim DMA alignment: reshape over pad

The infrastructure automatically pads the innermost dimension up to the
DMA-alignment granularity. That pad is expensive, and on the output side
it typically also forces a trailing slice to recover the live extent --
both of which should be avoided whenever possible.

The preferred fix is to **reshape the tensor in L3 memory** so the
innermost dimension is already a multiple of the DMA granularity (e.g.
fold a small inner dim into an adjacent outer one). This costs nothing
at runtime when it collapses to a layout change.

When you reshape at the boundary, **pass the original shape into the
custom op via ONNX attributes** and forward those attributes into
`lp_params` from the tiling Python. The boundary shape exists only to
satisfy DMA alignment; the original shape usually carries semantic
meaning (e.g. `[B, H, W, C]`), and both the tiling and `kernel.cpp` need
that meaning to compute strides, loop bounds, and any per-axis logic
correctly.

Caveat: the reshape must be consistent with your tiling. A dimension
that is squeezed (or fused away) by the reshape cannot be tiled along
afterwards, so any axis you still need as a tiling axis must survive
the reshape intact. Plan the boundary shape and the tiling together.

Recipe:

- **ONNX graph**: declare the custom op's IFM/OFM with a single flat
  inner dim that is already DMA-aligned (e.g. `shape = [H * W * C]`).
  Pass the original geometric shape (`H`, `W`, `C`, ...) as **op
  attributes** on the custom op so the semantic meaning is not lost
  at the boundary.
  Insert `onnx.Reshape` nodes if necessary.
- **Tiling Python**: reshape the L3 (DDR) tensor to the flat view
  before handing it to the DMA, e.g.
  `ifm.getTensorVar().Reshape([flat_size])` before
  `set_l3_to_l2_transfer`, and the symmetric form for OFM with
  `set_l2_to_l3_transfer`. Tile in 1D space at the DMA boundary, and
  forward the geometric attributes into `lp_params` so the kernel
  receives them.
- **Kernel (`kernel.cpp`)**: read `H`, `W`, `C` (and any per-tile
  fields such as `tile_x_start`, `tile_y_start`, `tile_rows`,
  `tile_cols` for a distributed tiling) from `lp_params`. The kernel
  keeps full geometric awareness -- strides, loop bounds, per-axis
  logic -- while the DMA path only ever sees a 1D, DMA-aligned buffer.

Apply this to **every** custom-op surface -- IFM, OFM, intermediates,
flow/grid -- not just the first one that complained. If you padded an
inner dim to make compilation pass, you should have used this pattern
instead.

### Quantized subgraphs: absorb the boundary DQ/Q, make the op an int op

A quantized ONNX model might not contain low-precision operations but it can
contain **float operations wrapped in a `DQ -> op -> Q` bracket** -- *fake
quantization*. The tensor is stored in the quantized type,
`DequantizeLinear` widens it to float, the op computes in float, and
`QuantizeLinear` narrows it back:

```
int8 --DQ--> float --[Conv]--> float --Q--> int8
```

Fake quantization is **int8 only** (VINT8) and is expressed with the
standard ONNX `QuantizeLinear` / `DequantizeLinear` ops.

The two halves of the bracket are **inverse functions**:
`DQ(x) = (x_q - zp) * scale` and `Q(y) = round(y / scale) + zp` compose to
the identity (up to rounding).

The bracketed `op` is usually a single operation, but a number of known
chains count as one quantized pattern and must be absorbed **together**.
The most common by far are a conv followed by its activation:

- `Conv -> Relu`
- `Conv -> LeakyRelu`
- `AveragePool -> Mul`

(For a comprehensive list check the `mixed-precision` skill suite)

**The DQ and the Q are a precision annotation, not compute.** They exist
so the graph stays type-correct in ONNX semantics. On the NPU nothing widens to float and
nothing narrows back -- the FE detects the pattern and emits genuine lower-precision kernels. The
round trip through float is never materialized, and the data is processed in the quantized type.

A custom op can be represented using the real lower-precision types.
So we can consider the QDQ nodes to be part of the custom op and then
absorb them into your kernel. Your custom op is then an op in the
**quantized type itself**.

`tutorial/conv2d/conv3x3_int8_2stamp` is a complete worked example (see its
README section "INT8 requantization"); the saturation and rounding modes it
sets at kernel entry are *strictly required* for bit-exactness, not a
nicety.

> **Not every quantization format is a bracket.** MX6/BFP quantization is
> a *single* op -- the AMD Quark `com.amd.quark.BFPQuantizeDequantize`
> node, which quantizes and dequantizes in one shot -- placed on each
> input of the operation it quantizes:
> ```
> com.amd.quark.BFPQuantizeDequantize -> op
> ```
> so detect it by that shape -- there is no trailing counterpart to pair
> with, and looking for a `DQ -> op -> Q` sandwich will miss it entirely.

> **MX6 CUSTOM OPS ARE EXPERIMENTAL AND HAVE NO KNOWN EXAMPLES.** You MUST NOT
> start one on your own initiative -- stop, say so, and get explicit user consent.

For more detail on any of this -- the quantization formats and how they
encode scales, which precisions each device supports, and how quantized
boundaries are handled at the whole-model level -- see the
**`mixed-precision`** skill (the quantization orchestrator). It is the
reference for model-level quantization decisions; this section covers
only what a custom op author needs at the subgraph boundary.

## Compiler Flags: Do Not Touch the Model-Wide Knobs

The `vitisai_config.json` flags are **model-wide**: one overlay and one set of
compiler settings serve every partition. A flag you change to make your op fit
therefore changes how every other layer is compiled, and the damage does not show
up where you made it -- your op keeps compiling and passing x86sim, while the
failure surfaces at integration (Phases 6-7), in layers you never touched. Treat
the following as fixed unless the user explicitly tells you otherwise:

- **Overlay selection.** The overlay fixes the core-tile grid and the DMA
  source/destination topology for the entire model. Design your tiling for the
  overlay you were given instead of asking for a different one.
- **`optimize_level`.** It has wide repercussions -- it can change which overlay
  is chosen and how many AIE-to-DDR connections are provisioned -- and it applies
  to the whole model. Leave it alone.
- **`stack_size` / `heap_size`.** These steal L1 from the tiler's buffers. Leave
  them at their defaults and shrink the kernel instead -- see
  [Stack and Heap Sizing](#stack-and-heap-sizing).

## Stack and Heap Sizing

**Do NOT add or modify `stack_size` or `heap_size` in a custom-op YAML.** A stack
or heap overflow is a signal that the **kernel** has too much live state.
Enlarging `stack_size`/`heap_size` silently steals L1 from the tiler's
double-buffered inputs and outputs (those you can transfer into with
`set_l2_to_l1_transfer`), so a "fix" here quietly shrinks the tiles you
can afford elsewhere and masks a kernel that is too heavy. The measured peak in
the `.calltree`/`.map` artifacts is a **diagnostic** to tell you what to shrink
in the kernel -- never a value to copy into the YAML. See "Determining the stack
and heap size" in `README.md` for how to read those two files, but ignore its
closing advice to put the measured peak in the YAML.

### The four checks you MUST apply

Measure as above, then genuinely apply **all four** of the following:

1. **Move scratch out of the stack/heap into a framework-managed buffer.** Any
   multi-KB working buffer belongs in an ADF/DM buffer; the usual idiom is to
   over-allocate the OFM L1 buffer so it holds `output + scratch` and to drain
   only the real output sub-view on the L1->L2 DMA. The kernel binds the full
   allocation, so it has room to scribble with no `static`, no heap, no stack. See
   the oversized-OFM-buffer section of `tutorial/conv2d/README.md` for the sizing
   rule and the sliced drain.
2. **Shrink live sets via loop splitting** (see `vai-aie-kernel-development`):
   break one fat loop into passes that hand intermediates through DM, so each loop
   has fewer simultaneously-live vectors.
3. **Keep temporaries small (per-row / 8-lane)** (see `vai-aie-kernel-development`):
   process one 8-lane row at a time instead of keeping full 64-lane tiles live;
   use named locals instead of addressable vector arrays; keep reductions in
   registers. Remove dynamic/temporary allocations and static scratch/LUTs (they
   consume heap).
4. **Constrain pipelining on the pressure-heavy loops.** Over-aggressive
   pipelining/unrolling widens live ranges and forces spills; disable or limit it
   on the specific loop the `.lst` shows spilling, and re-measure.

A correct kernel that fits the default budget beats a marginally faster one that needs a bigger budget.

## Phase 1: Subgraph Extraction

**Note:** If the model contains only a single node, there is no subgraph to extract -- skip Phase 1a and use the model directly as both Model A and the basis for Model B.

**Understand the subgraph's neighbors before extracting.** A custom op's producers and consumers constrain the DDR memory layout of its inputs and outputs. Matching those layouts inside the custom op is normally cheap -- a few cycles in the cores or a different DMA configuration, negligible next to the main compute. Ignoring them forces extra data movement at integration, which can be far more expensive and can make the whole op impossible to integrate. So investigate the neighbors' DDR layout requirements up front rather than discovering the mismatch in Phase 6/7.

Since `--nodes` is provided as a skill argument, extract the subgraph directly. The script auto-infers input/output tensor cut points from the node names.

### 1a. Extract the subgraph (Model A)

```bash
<ENV_SETUP>
mkdir -p <working_dir>
python <skill_dir>/scripts/onnx_cut.py \
    --model <full_model>.onnx \
    --nodes <node_1> [<node_2> ...] \
    --output <working_dir>/model_a.onnx
```

The extracted `model_a.onnx` is the **reference model** -- it uses standard ONNX ops and runs on CPU for golden reference verification.

If the node names are ambiguous or you need to inspect the model first, use `--report`:
```bash
python <skill_dir>/scripts/onnx_cut.py --model <full_model>.onnx --report
```

### 1b. Generate CPU reference data

Run the extracted model on CPU to produce golden reference outputs:

```bash
python <skill_dir>/scripts/compile.py \
    <working_dir>/model_a.onnx --cpu \
    --input-dir <working_dir>/reference_data \
    --output-dir <working_dir>/reference_data
```

**Pass both `--input-dir` and `--output-dir`, pointing at `reference_data`.**
`--output-dir` covers only the outputs; without `--input-dir` the inputs go to
`<model_stem>_inputs/` and every later step expecting `reference_data/inputs.npz`
(Phase 4 x86sim, Phase 5 board run) fails to find it. The directory is generated
on first use and its inputs reused on re-runs.

This saves:
- `reference_data/inputs.npz` (plus one `.npy` per input) -- inputs used
  (**must be reused for x86sim in Phase 4**)
- `reference_data/outputs.npz` -- golden reference outputs
- `reference_data/<output_name>.npy` -- individual output files for comparison with `compare_npy.py`

### 1c. Create Model B (Custom Op model)

Generate the custom op ONNX model for the nodes from Model A that correspond to the custom op using `onnx_stitch.py`:

```bash
python <skill_dir>/scripts/onnx_stitch.py \
    --model <working_dir>/model_a.onnx \
    --nodes <node_name_or_op_type> \
    --custom-op-name <op_name>
```

## Phase 2: Create the Custom Op

### 2a. Context analysis

Phase 1 highlights the importance of looking at the surrounding context. A custom op does not exist on its own -- it is part of a bigger model. That context must be established before you write a line of kernel code, and it must stay in view for the rest of the flow. Subgraph extraction exists only to shorten the round trip from modification to verification;

A custom op may inherit DDR layout requirements from its producer and consumer. A convolution or matmul feeding the op, for instance, constrains the layout of the DDR tensor it ingests. Encode those constraints in the YAML through the `ddr_tensor_layout` / `onnx_tensor_layout` fields. If you don't, the compiler inserts transposes around the custom op, and those transposes routinely cost more than the custom op saves.

**The goal of the custom op is to absorb any data movement that is not part of the original ONNX model.** Even when the baseline (or `model_a.onnx`) contains a transpose merely to connect two operations -- one of which becomes the custom op -- that transpose must be absorbed into the custom op rather than left standing beside it.

DDR Layout is an essential component of the custom op; it determines the tiling. Discovering a layout requirement after the kernel works means the tiling you built and tuned was never the final one.

Consequence of not considering the custom op context:

- **Implementation is thrown away** Absorbing a layout usually forces a different retiling, e.g. transposed L3/L2 shapes or a different DMA configuration. That invalidates the kernel structure, the L1/L2 buffer shapes, and the tiling script together.
- **The optimization rounds are spent against the wrong target.** Every round of board-guided tuning is measured on a tiling that is about to be replaced.
- **The dead end arrives late and is expensive to leave.** By the time an op is complete and validated, a retiling is a large, risky change on working code. In practice the layout fix gets deferred, and the model ships with a compiler-inserted transpose.

Doing the analysis up front costs one compilation of the neighbourhood. Doing it late costs the kernel.

#### Output of this phase

Produce a report of the form:

```
input_<n>:
  async: <false|true>
  onnx_tensor_layout: <layout>
  ddr_tensor_layout: <layout>
output_<n>:
  async: <false|true>
  onnx_tensor_layout: <layout>
  ddr_tensor_layout: <layout>
```

If no layout change is required, leave the report empty and the next stage won't set any DDR requirements. If one argument doesn't need to change but another one does, just set `async: <false|true>` and don't set `onnx_tensor_layout`/`ddr_tensor_layout`. The `async` field is required when specifying the DDR tensor layout, but `onnx_tensor_layout`/`ddr_tensor_layout` are optional.

`input_<n>` and `output_<n>` can be set seperately. This means that if we only have requirements on the output we don't need to specify a layout for the input and vice-versa.

As the onnx/ddr layout information can only be applied to the original onnx inputs and outputs. Scratch buffers don't have any layout because they are only writen and read by the same custom op.

### 2b. ONNX Custom Op YAML

Model B (the custom op ONNX model) was already created in Phase 1c. Now create the remaining files in `<working_dir>/`:

Model B was generated in Phase 1. If you need to customize it further (e.g., add extra attributes), you can edit the .onnxtxt version. See [README.md](../../README.md) for the `.onnxtxt` format and how to convert between `.onnx` and `.onnxtxt`.

The model must have `shape` and `data_type` attributes on the custom op node (required by VAIML shape inference):

**Manual creation (if needed) using .onnxtxt format:**
```
<
    ir_version: 7,
    opset_import: ["" : 13, "mydomain" : 1]
>
test(float[<shape>] <inputs>) => (float[<shape>] <output>) {
    <output> = mydomain.<op_name><data_type = "float32", shape = [<shape>]>(<inputs>)
}
```

**Using Python (onnx helper):**
```python
node = onnx.helper.make_node(
    "<op_name>",
    inputs=[...],
    outputs=[...],
    domain="mydomain",
    shape=[...],        # REQUIRED: output shape
    data_type="float32" # REQUIRED: output data type
)
```

### 2c. Config YAML (`custom_op_<name>/<name>.yaml`)

```yaml
---
tiling: "<name>_tiling.py"
```

Need a different DDR layout than the ONNX one (e.g. NCHW -> HCWN_C8 for a conv)?
Add `onnx_tensor_layout` / `ddr_tensor_layout` per input/output and VAIML folds
the conversion into the DMA (prefer this over pre-arranging data offline):
```yaml
  inputs: # add one entry per input
    - onnx_tensor_layout: "N C H W"
      ddr_tensor_layout: "H C/8 W N 8"   # HCWN_C8 (C vectorized by 8)
```
See `tutorial/conv2d/README.md` -> "Input layout: HCWN_C8, and who converts to
it" and the main [README.md](../../README.md) "Data layout specification".

You can figure out which data layout is used by the producer and consumer of your custom op by looking at the compilation log. It is emitted as a INFO. For instance:

```
Custom op Unary1 (mydomain.unary) operand 0 uses a different memory layout than its producer, possibly causing suboptimal data movement. This op: ONNX tensor layout = "A B C D", DDR Layout = "A B C/8 D 8"; producer op: ONNX layout = "A B C D", DDR layout = "A B C D".
```

### 2d. Kernel C++ (`custom_op_<name>/<name>.cpp`)

**MANDATORY: Target a 4x4 distributed implementation out of the box.** This is the default and expected starting point -- write the kernel so it can run on all 16 cores with broadcast IFM and per-core OFM collection. You can use the following templates (see below) to get started.

- **Unary op** (one IFM): read `tutorial/negate/2_distributed/`
  (`negate_tiling.py`, `kernel/negate_kernel.cpp`, `custom_op_negate.yaml`)
  in full.
- **Binary op** (two IFMs): read `tutorial/mul/2_distributed/`
  (`custom_mul_tiling.py`, `kernel/custom_mul_kernel.cpp`,
  `custom_op_mul.yaml`) in full. **The second IFM must be
  Transpose-distributed across columns due to the overlay
  architecture** -- the `mul/2_distributed` template is the canonical
  example of how to do this.
- **Six-column stamping**: read `tutorial/mul/4_distributed_6stamp/`
  (and the negate equivalent if you need a unary 6-stamp reference)
  so you understand how the 4x4 grid is replicated across the 6
  columns of the overlay.

The focus on this section is to get a kernel that is functionally correct. Performance is a secondary concern but some optimizations that don't increase complexity can already be tackled here. For example, you should prefer native hardware type like `bfloat16` over software emulated types like `float32/64`.

#### Analyze Parallelism Before Choosing a Tiling Strategy

**CRITICAL: Do a proper analysis of the algorithm's parallelism.** The presence of a sequential dependency in one dimension does NOT mean the entire operation is inherently sequential. Different dimensions of the computation may have independent parallelism opportunities.

**Methodology -- work backward from the output to the inputs:**

1. **Identify the output dimensions.** What is the shape of the output tensor? Each dimension is a candidate for tiling/distribution across cores.

2. **For each output dimension, trace the data dependencies.** Ask: "Can two different output elements along this dimension be computed independently?" If yes, this dimension can be tiled across cores.

3. **Separate sequential dependencies from parallel dimensions.** An operation may have a loop-carried dependency in one dimension (e.g., a recurrence across a sequence) while being fully parallel in another dimension (e.g., independent output features). These are **separate concerns** -- a dependency in one dimension does not eliminate parallelism in another.

4. **Choose the tiling strategy based on the parallel dimensions.** Distribute the parallel dimensions across the 4x4 grid. Keep the sequential dimensions within each core (processed in a loop).

5. **Only after exhausting all dimensions** should you consider implementing the op sequentially on a single core. A proper analysis may reveal that an operation assumed to be "inherently sequential" actually has significant parallelism in its output dimensions.

**Example pattern:** An operation computes `output[seq, features]` where `seq` has a recurrence (each step depends on the previous) but `features` is fully independent. The wrong conclusion is "recurrence means single core." The correct approach is to tile the `features` dimension across 16 cores while processing `seq` sequentially within each core. This gives 16x parallel throughput on the feature computation even though the sequence is sequential.

**Common mistake:** Seeing a sequential dependency and immediately deciding the op has no parallelism at all. This wastes 15 of 16 available cores. Always ask: "Which dimensions CAN be parallelized?" before asking "Which dimensions CANNOT?"

**NOTE:** If you need to include `printf` and `<cstdio>` for debug purposes, you must safeguard it with `#ifdef __X86SIM__`. This ensure that the debug messages are only active during x86 simulation and won't break AIE compilation.

**Unary kernel template:**
```cpp
#include <adf.h>
#include <aie_api/aie.hpp>

namespace custom_ops {
static constexpr int <name>_lp_size = 1;

template <typename dtype_ifm, typename dtype_ofm>
__attribute__((noinline)) void <kernel_name>(
    adf::input_buffer_conf<dtype_ifm, adf::bpc_sync_0d> &__restrict ifm,
    adf::output_buffer_conf<dtype_ofm, adf::bpc_sync_0d> &__restrict ofm,
    const uint32_t (&lp_params)[<name>_lp_size]) {
  auto *in = (dtype_ifm *__restrict)(ifm.data());
  auto *out = (dtype_ofm *__restrict)(ofm.data());
  uint32_t size = lp_params[0];
  for (unsigned i = 0; i < size; ++i) {
    out[i] = /* compute */;
  }
}
} // namespace custom_ops
```

**Binary kernel template** -- add second input buffer (and a template parameter `dtype_wts`) between `ifm` and `ofm`.

#### Kernel Guidelines Checklist

Go through every item below before you call the kernel done. These are silent
failure modes -- the kernel compiles either way.

- [ ] **CRITICAL: Always prefer AIE API library calls over ad-hoc implementations of algorithms -- never use `std::`.** The AIE API (`aie::` namespace, from `<aie_api/aie.hpp>`) provides highly optimized, vectorized operations that are portable across AIE architectures. Ad-hoc implementations (LUTs, polynomial approximations) are slower, less accurate, and not portable.
  **Before writing or optimizing any kernel math you MUST read the bundled AIE API
  reference** --
  `aie_api_references.md`, which
  ships with the **vai-aie-kernel-development** skill. It is the detailed catalog of
  AIE API primitives -- core (load/store, arithmetic, reductions), fused /
  advanced (`mac_square`, `msc_square`, `reduce_add_v`,
  `invsqrt`, `to_float`/`to_fixed`), and transcendentals/composition examples
  (`tanh`, `exp2`, sigmoid-via-tanh) -- giving each primitive's dtype support,
  vectorization, accumulator type, and a math-pattern -> API lookup. Going through
  it is not optional: it is how you pick the idiomatic vectorized/fused op instead
  of guessing a signature, hand-rolling a LUT/polynomial, or falling back to
  `std::`.
  For anything the reference does not cover, look the headers up in the active
  product environment; its
  "If it's not here: discover from the headers"
  section covers how to resolve that directory and which header answers which
  question -- including the rule to scope every search to it, because a
  `find`/`grep -r` from the env root stalls.

- [ ] **Always set the core's saturation + rounding modes once at kernel entry** -- in every kernel, unconditionally. This is core-wide state (not per-op) that governs any **narrowing cast out of the accumulator**: `int32 >> shift -> int8/uint8` (requant) *and* `fp32 accum -> bf16`:

  ```cpp
  aie::tile::current().set_saturation(aie::saturation_mode::saturate);  // clamp, don't wrap
  aie::tile::current().set_rounding(aie::rounding_mode::conv_even);     // round-half-to-even; match your reference
  ```

  These are persistent core state, so guard with a `static` flag and set before any `to_vector<...>(shift)` cast. **Strictly required for int8/quantized bit-exactness** (wrong modes = the classic "correct except +/-1 on some elements", or wrapped-overflow garbage); **best practice for bf16** too (they affect the `fp32->bf16` rounding), though tolerance-based bf16 checks often pass without it. Don't rely on defaults -- set them to match your reference. See `tutorial/conv2d/conv3x3_int8_2stamp` and its README "Set saturation + rounding mode for any narrowing cast".

- [ ] **For 4x4 distributed kernels** -- always use `aie::tile::current().id().row % 4` and `aie::tile::current().id().col % 4` to compute offsets into broadcast buffers. Keep the `% 4` even in single-stamp kernels where it looks redundant: `id()` returns absolute physical coordinates, so dropping it silently breaks multi-stamp overlays (every stamp but stamp 0 indexes out of bounds and emits zeros).

### 2e. Tiling Python (`custom_op_<name>/<name>_tiling.py`)

**General instructions:**

Follow the example of kernel tiling and tiling script creation from the `tiling.md` file.

**Very important:** Report to the user the data flow relation that came out of your analysis. It needs to be symbolic and contain information about how tiles of outputs relate to tiles of inputs. For instance, it should look like this:
```
 * Input tiles (buffer `ifm`) of size T + K
 * Kernel weights (buffer `wts`) of size K, need to stay unchanged across all kernel calls.
 * Output tiles (buffer `ofm`) of size T
 * Tiles are indexed from i = 0 to i = L_out / T - 1
 * For the tile indexed by i:
   * The tile of output produced is out[T * i] to out[T * (i+1) - 1],
   * One tile of input is needed, from in[T * i] to in[T * (i+1) + K - 1].
```

Use this symbolic relation to create the tiling script, and report to the user the data movement that you determined:
* which core executes which tile (give a table with row/column layout),
* what does each L2 buffer contain,
* which data from the L2 buffer goes to each column, which goes to each row (if the WTS channel is used),
* what is the position of each result tile collected back in L2.
Then implement a tiling script using that information.

**4x4 distributed template (default starting point):**

This is the canonical 16-core unary tiling, mirroring `negate/2_distributed`. IFM is broadcast across columns, OFM is collected per-core via `SpatialDistribute2D`. Double-buffered (ping/pong) at both L2 and L1.

Sample tiling script:
```python
from pathlib import Path

import tensor_expr


def getTiling(
    opInterface: tensor_expr.OperatorInfo, tiling: tensor_expr.AieConfig
) -> None:
    OVERLAY_ROWS = 4
    OVERLAY_COLS = 4

    # One entry per overlay stamp/phase. This template configures stamp 0; see
    # the note below for spreading the work over every stamp/phase.
    spu = tiling[0][0]

    ifm, ofm = opInterface  # unary; for binary add `wts`
    assert ifm.getPaddedShape() == ofm.getPaddedShape(), (
        "ifm/ofm padded shape inconsistent"
    )

    # Per-core tile size (in elements). 0x800 = 2K bf16 elements = 4KB.
    # Sized so IFM ping+pong (broadcast across all 4 rows) and OFM
    # ping+pong fit in the 64KB L1, avoiding the 0xB000-0xD000 stack/heap.
    tileSize = 0x0800

    assert ifm.getPaddedShape()[0] % (tileSize * OVERLAY_COLS * OVERLAY_ROWS) == 0, (
        f"IFM shape {ifm.getPaddedShape()[0]} is not divisible by the tile size {tileSize} and overlay dimensions {OVERLAY_COLS}x{OVERLAY_ROWS}"
    )
    nb_temporal_iterations = ifm.getPaddedShape()[0] // (tileSize * OVERLAY_COLS * OVERLAY_ROWS)

    # L1 addresses: IFM needs OVERLAY_ROWS x tileSize per buffer
    # because each core in a column holds a full row of the broadcast.
    ifm_ping_addr = 0x0000  # to 0x3FFF (4 * tileSize = 16KB)
    ifm_pong_addr = 0x4000  # to 0x7FFF
    ofm_ping_addr = 0xD000  # to 0xDFFF (tileSize = 4KB)
    ofm_pong_addr = 0xE000  # to 0xEFFF

    # Total elements in the tensor
    size = 1
    for dim in ifm.getPaddedShape():
        size *= dim

    # L1 (core) buffers -- IFM holds the full column-broadcast slice
    ifm_mk = tensor_expr.TensorVar.make(
        [tensor_expr.Location(ifm_ping_addr), tensor_expr.Location(ifm_pong_addr)],
        [OVERLAY_ROWS, tileSize],
        type=ifm.getDType(),
    )
    ofm_mk = tensor_expr.TensorVar.make(
        [tensor_expr.Location(ofm_ping_addr), tensor_expr.Location(ofm_pong_addr)],
        [tileSize],
        type=ofm.getDType(),
    )

    # L2 (mem) buffers -- one full 4x4 tile across all cores, ping/pong
    L2_full_tile_size = tileSize * OVERLAY_ROWS * OVERLAY_COLS
    ifm_mem = tensor_expr.TensorVar.make(
        locations=[tensor_expr.Location(0, 0, 0), tensor_expr.Location(0, 0, 0x10000)],
        shape=[OVERLAY_COLS, OVERLAY_ROWS, tileSize],
        type=ifm.getDType(),
    )
    # Set the number of ping-pong buffer rotations of ifm_mem that will take place
    ifm_mem.setTemporalIterations(nb_temporal_iterations)
    ofm_mem = tensor_expr.TensorVar.make(
        locations=[tensor_expr.Location(1, 0, 0), tensor_expr.Location(1, 0, 0x10000)],
        shape=[OVERLAY_COLS, OVERLAY_ROWS, tileSize],
        type=ofm.getDType(),
    )
    # Set the number of ping-pong buffer rotations of ofm_mem that will take place
    ofm_mem.setTemporalIterations(nb_temporal_iterations)

    # DDR -> L2: stream the flattened tensor in L2-sized tiles
    ifm_l3_l2 = [ch for ch in spu.get_l3_to_l2_channels() if ch.mem_tile_port.tile_col == 0][0]
    spu.set_l3_to_l2_transfer(
        ifm_l3_l2,
        ifm.getTensorVar().Reshape([size]).TileBy(index=0, tileLen=L2_full_tile_size),
        ifm_mem.Reshape([L2_full_tile_size]),
    )

    # L2 -> L1 IFM: column-broadcast. Each column gets 1/4 of L2;
    # every core in that column receives the full quarter.
    ifm_l2_l1 = spu.get_l2_to_l1_channels(broadcast=tensor_expr.broadcast_on.COLUMNS)
    tiled_ifm_l2 = ifm_mem.TileTo(index=0, numTiles=OVERLAY_COLS)
    for col, ch in enumerate(ifm_l2_l1):
        spu.set_l2_to_l1_transfer(ch, tiled_ifm_l2[col], ifm_mk)

    # L1 -> L2 OFM: each core writes 1/16 of the tile, gathered via
    # SpatialDistribute2D into the [COLS, ROWS, tileSize] L2 buffer.
    ofm_l1_l2 = spu.get_l1_to_l2_channels()
    distributed_ofm_l2 = ofm_mem.Reshape(
        [OVERLAY_COLS, OVERLAY_ROWS, tileSize]
    ).SpatialDistribute2D(
        dimA=0, dimB=1, tileACount=OVERLAY_COLS, tileBCount=OVERLAY_ROWS
    )
    for col, ch in enumerate(ofm_l1_l2):
        spu.set_l1_to_l2_transfer(
            ch,
            ofm_mk,
            distributed_ofm_l2[col],
        )

    # L2 -> DDR
    ofm_l2_l3 = spu.get_l2_to_l3_channels()[0]
    spu.set_l2_to_l3_transfer(
        ofm_l2_l3,
        ofm_mem.Reshape([L2_full_tile_size]),
        ofm.getTensorVar().Reshape([size]).TileBy(index=0, tileLen=L2_full_tile_size),
    )

    # Each kernel invocation processes tileSize elements
    spu.set_kernel_params([tileSize])
    # Set the arguments to be the L1 buffers we passed (plus the lp_params)
    spu.set_kernel_arguments([ifm_mk, ofm_mk])
    # Mandatory: give the kernel's name and containing file
    spu.set_kernel_function_name("sample_op")
    spu.set_kernel_impl(Path("sample_op.cpp"))
    # Mandatory: give the number of kernel calls (even for 1 call)
    spu.set_kernel_nb_calls(nb_temporal_iterations)
```

**Using every stamp:** the template above fills stamp 0 only. To use a multi-stamp overlay, loop `for stamp_idx, stamp in enumerate(tiling)` and give each stamp its **own slice of the DDR tensor** (the L1/L2 addresses stay identical per stamp) -- see `negate/4_distributed_vectorized_2stamp` and `mul/3_distributed_2stamp` for the canonical split.

For binary ops: add a second operand, typically named `wts`, to the `opInterface` unpack; create a corresponding `wts_mem` L2 variable at `Location(3, 0, 0)` (typically row-broadcast via `wts_mem.TileTo(index=0, numTiles=OVERLAY_ROWS)`), and add `set_l3_to_l2_transfer` / `set_l2_to_l1_transfer` calls. Use `spu.get_l2_to_l1_channels(broadcast=tensor_expr.broadcast_on.ROWS)` as channels to pass that input from L2 to L1. See `mul/2_distributed` for the canonical binary 4x4 pattern.

For details on 4x4-core distribution and additional patterns, see [README.md](../../README.md) for L2 shape `[COLS, ROWS, tileSize]` patterns.

### 2f. Vitis AI Config (`vitisai_config.json`)

```json
{
  "passes": [{
    "name": "vaiml_partition",
    "plugin": "vaip-pass_vaiml_partition",
    "vaiml_config": {
      "keep_outputs": true,
      "optimize_level": 2,
      "enable_f32_to_bf16_conversion": true,
      "logging_level": "info",
      "fe_args": "small-tensor-threshold-unwrapping=0",
      "experiment_features": ["KeepOrphanNodes"],
      "aiecompiler_args": "--compile-for-x86sim=true --x86sim-as-shared-library=true --msg-severity=\"77-23879:error:100\"",
      "custom_ops": {
        "mydomain.<op_name>": {
          "op_config": "custom_op_<name>/<name>.yaml"
        }
      }
    }
  }],
  "target": "VAIML",
  "targets": [{"name": "VAIML", "pass": ["vaiml_partition"]}]
}
```

`--compile-for-x86sim=true --x86sim-as-shared-library=true` build the x86
simulator library (`libx86_sim.so`). **CRITICAL: keep them in every config you
compile with, in every phase** -- Phase 3, each Phase 5 re-compile, and the
Phase 7 integrated compile.
`--msg-severity="77-23879:error:100"` promotes the L2 shared-buffer overlap
warning to an error, so hardware-only buffer-placement bugs fail the compile
instead of silently corrupting results on the board.

Compile with this config as-is. For Phase 4, copy it to
`vitisai_config_x86sim.json` and add one key:

```json
      "runner_type": "x86sim",
```

That copy is only ever passed to `run.py`, never to `compile.py` -- one cache
serves both runners. See Critical Workflow Rule 4.

### 2g. Tutorial Examples for Inspiration

Complete working examples are bundled at `<skill_dir>/tutorial/`:

| Tutorial | Description | Key pattern |
|----------|------------|-------------|
| `negate/0_untiled/` | Simplest unary op | 1x1, no tiling, whole tensor in L1 |
| `negate/1_tiled/` | Tiled unary op | TileBy(), double buffering |
| `negate/2_distributed/` | 4x4 distributed unary | 16-core tiling, broadcast, core ID offsets |
| `negate/3_distributed_and_vectorized/` | Optimized unary | aie::vector, pipelining |
| `mul/0_untiled/` | Simplest binary op | Two inputs (IFM + WTS) |
| `mul/1_tiled/` | Tiled binary op | Separate L2 columns for IFM/WTS |
| `mul/2_distributed/` | 4x4 distributed binary | IFM column broadcast, WTS row broadcast |
| `mul/5_performant_overlay` | Performant overlay | Channel distribution for the performant overlay |
| `topk/0_untiled/` | Custom attributes | Reads ONNX attributes (k) |
| `topk/1_tiled/` | Async outputs | Asynchronous buffer management |
| `reducemax/` | Reduction over different axes | Outer-axis vs inner-most-axis (de-interleave) strategies |
| `gridsample2d/` | Complex 2D op | Multi-input, 4x4 distribution |
| `affinegrid2d/` | Affine grid generation | Vectorized and distributed variants |
| `gemm/` | GEMM + bias (== pointwise 1x1 conv) | `aie::mmul`, operand pre-blocking, per-row weight distribution, bias folded into weights, multi-memtile L2 staging, weight streaming |
| `conv2d/conv3x3_int8_2stamp/` | Spatial 3x3 stride-1 INT8 conv | `aie::mmul` int8, halo rows, in-register sliding window (`shuffle_down_fill`), multi-call depth reduction (OFM async ratio), **persistent psum/scratch via an oversized OFM buffer (not stack/heap)**, int8 requant, native-faithful reproduction |

Read these files to understand patterns for your specific use case. Each tutorial contains:
- `.onnxtxt` / `.onnx` -- model definition
- `custom_op_*/` -- kernel .cpp, tiling .py, config .yaml
- `vitisai_config.json` -- compilation config
- `run.py` -- test script

## Phase 3: Compile

**IMPORTANT: Use `compile.py` to compile the model.**
**IMPORTANT: Run this in a sub-agent -- see "Critical Workflow Rules" above.**

Commit your files to the local git repo before compiling:
```bash
cd <working_dir> && git add -A && git commit -m "Ready to compile <op_name>"
```

```bash
bash -c '
<ENV_SETUP>
export DEBUG_VAIML_PARTITION=1
export FLEXML_PRINT_VITISTOOLS_OUTPUT=1
cd <working_dir>
python <skill_dir>/scripts/compile.py <model_b>.onnx
'
```

Successful compilation prints `Compilation successful`.

**CRITICAL**: The compiler may report success even when tiling fails (VAIML falls back to CPU silently). Always verify:
- Check for `"Compilation successful"` in the output
- Verify `<model_stem>/cache/vaiml_par_0/0/backend/gen_tg_adf/` is non-empty -- if empty, tiling failed

**IMPORTANT:** When compilation fails, do not guess at fixes. Read the full error output, identify the root cause (tiling plugin, AIE compiler, or linker), and apply a targeted fix. See the **Troubleshooting** section for common compilation errors.

## Phase 4: Simulate and Validate

**IMPORTANT: Run x86sim in a sub-agent -- see "Critical Workflow Rules" above.**

The validation flow uses the **same inputs** for both CPU reference and x86sim, then compares outputs with `compare_npy.py`.

### 4a. Run x86sim with the same inputs from Phase 1b

The simulation is just an ONNX Runtime session driven by the x86sim config
(Critical Workflow Rule 4), so you use the ordinary `run.py` against the Phase 3
cache -- no recompile -- and point `--input-dir` at the `reference_data/`
directory that `compile.py --cpu` wrote in Phase 1b, so both runs see identical
data.

```bash
bash -c '
<ENV_SETUP>
cd <working_dir>
python <skill_dir>/scripts/run.py <model_b>.onnx \
    --vitisai-config vitisai_config_x86sim.json \
    --input-dir <working_dir>/reference_data \
    --output-dir <working_dir>/x86sim_outputs \
    --num-runs 1
'
```

Outputs land in `x86sim_outputs/` as `.npy` files named after the output tensor,
in the same format as the CPU reference -- feed them straight to
`compare_npy.py`.

**`--num-runs 1` is a correctness requirement, not a performance tip.** The
default of 10 gives you an all-zero `outputs.npz` while still reporting success
under x86sim (Troubleshooting 22). Nothing to time here anyway; large tensors take
minutes.

### 4b. Compare x86sim output against CPU reference

Use `compare_npy.py` to check for numeric mismatches between the CPU golden reference (Phase 1b) and the x86sim output:

```bash
python <skill_dir>/scripts/compare_npy.py \
    <working_dir>/reference_data/<output_name>.npy \
    <working_dir>/x86sim_outputs/<output_name>.npy \
    --rtol 0.01 --atol 0.015 --verbose
```

This prints:
- Max absolute difference
- Mean absolute difference
- Number of elements exceeding tolerance
- `SUCCESS` or `ERROR` verdict

If the comparison passes, the custom op is functionally correct -- proceed to Phase 5 (kernel optimization).

If the comparison **fails**, do not randomly change tiling or kernel code. Instead, work through the **Debugging** subsection below: inspect the generated tiling header (step 1) and add printf to the kernel (step 2) to trace the root cause of the mismatch before applying any fix.

### Debugging (only if 4b fails)

The following debug strategies are listed in terms of complexity. Inpecting the ADF header file is the cheapest thing to do while printf debugging requires a recompilation and might take a bit longer.

#### 1. Inspect the generated tiling header

The compiler generates a tiling header that shows the actual ADF parameters derived from your Python tiler. This is the first thing to check when outputs are wrong:

```
<working_dir>/<model_stem>/cache/vaiml_par_0/custom_ops/<opname>_<instancename>_[0-9]*_multi_layer_overlay.h
```
There is one such header per instance of the custom op. You need to find the problematic header either as given by the AIE Compiler.

Read this file and verify:
- Tile sizes match what you expect
- Buffer addresses and shapes are correct
- Number of kernel invocations matches your tiling strategy
- L2 and L1 buffer dimensions are consistent

See [README.md](../../README.md) "Debugging Tiling" section for details.

#### 2. Printf debugging

**Only add printf AFTER Phase 3 compilation succeeds.** Guard all printf calls with `#ifdef __X86SIM__` so they compile for x86sim but not for AIE. After adding printf, re-run `compile.py` and then `run.py` to see the debug output.

**Wrap all printf calls in `#ifdef __X86SIM__` guards** so they are only active during x86 simulation and won't break AIE compilation if left in accidentally:

**Debug iteration loop:**
1. Edit the kernel .cpp to add printf (see examples below)
2. Re-run `compile.py` (normal config) to rebuild with the printf statements
3. Re-run `run.py` with the x86sim config and `--input-dir reference_data`
4. Inspect the printf output to identify the problem
5. Fix the kernel or tiling, re-compile, re-run x86sim, compare again
6. When done, remove debug printf before finalizing

**What to print to diagnose mismatches** (see [README.md](../../README.md) for full details):

```cpp
#ifdef __X86SIM__
#include <cstdio>
#endif

// 1. Verify kernel is called the expected number of times
#ifdef __X86SIM__
static uint32_t call_count = 0;
printf("Kernel call #%u, tile_size=%u\n", call_count, lp_params[0]);
call_count++;
#endif

// 2. Check input data arrived correctly (first/last elements)
#ifdef __X86SIM__
printf("  in[0]=%.4f in[%u]=%.4f\n", (float)in[0], size-1, (float)in[size-1]);
#endif

// 3. Check computed output values
#ifdef __X86SIM__
if (i < 4) {
    printf("  [%u] in=%.4f out=%.4f\n", i, (float)in[i], (float)out[i]);
}
#endif

// 4. For 4x4: verify core position and data offsets
#ifdef __X86SIM__
int row = aie::tile::current().id().row % 4;
int col = aie::tile::current().id().col % 4;
printf("Core (%d,%d): offset=%u\n", row, col, offset);
#endif
```

**Common causes of numeric mismatches:**
- **Wrong tile size in lp_params**: kernel processes more/fewer elements than the tile contains
- **Wrong buffer offset in 4x4**: core reads from wrong position in broadcast buffer
- **Wrong data movement**: L2->L1 transfer shape doesn't match kernel expectation
- **Padding mismatch**: compiler pads tensors (use `getPaddedShape()` in tiling)
- **bf16 precision**: expected when comparing bf16 kernel output against float32 CPU reference (rtol=0.01, atol=0.015 should accommodate this)

**Tip:** Using `#ifdef __X86SIM__` guards means printf will only be active during x86 simulation and won't break AIE compilation. However, clean up debug printf before finalizing the kernel.

#### 3. Manually inject ADF code

**WARNING:** Only use this if all possibilities to adapt the python tiling code are exhausted for the `AieConfig` tiling API. Manually injecting ADF is decouraged because it creates (verbose) code that is hard to maintain or adapt to other AIE topologies. Howerver, if you hit a limit on what the tiling `AieConfig` tiling API can represent, and before resorting to other legacy APIs, this is the path you must take.

The ADF header is a header file where the data movement and scheduling of AIE kernels is done. This is the file used to integrate your operator with the overall AIE graph. When you provide a python tiling script, this file is generated for you - togehter with a kernel.yaml file - and contains the data movement instructions the tiling script requested.

You can provide your own manually-written ADF header. To do so, its name needs to be supplied in the custom op config's optional `ml_adf_header` field, alongside the kernel YAML directory:

```yaml
ml_adf_header: "<mydomain>_<mycustomop>_<output_name>_<instance_nb>_multi_layer_overlay.h"
kernel_yaml_dir: "<dir_to>/<mydomain>.<mycustomop>_<instance_nb>.yaml>"
```

> Note: We provide the directory containing the kernel YAML and not the filename itself. The reason is that the filename is automatically constructed after the name of the operation and instance number.

Providing ADF header yourself is possible if you need to modify the automatically-generated ADF header. Doing so stops the auto-generation of ADF headers and kernel YAML for the given custom op. In this case, you can start from the automatically generated header. Assuming that `mydomain.mycustomop` is the name of the custom op in ONNX, you can find the generated ADF header under `custom_ops` inside your results/artifact folder, with the name `mydomain_mycustomop_0_multi_layer_overlay.h`. The generated kernel YAML is located next to it in the same directory.

Before modifying the custom op registration YAML with the new two files, you must perform the following adaptations:
  - Rename `mydomain.mycustomop_0.yaml` -> `mydomain.mycustomop.yaml` as to drop the instance number.
  - Edit the "stamp" entry to have a `defined_value` of 1. We always want a stamp value of 1 even if we implement more than one stamp. This value doesn't really set the number of stamps being used, it is just an indicator to the backend that stamp is implemented by the custom op itself.
    ```yaml
      - name: stamp
        data_type: uint32
    +   defined_value: 1
    ```
  - Edit the number of channels used by the DDR tensors. Those are named `num_ifm_shim_ch`, `num_wts_shim_ch`, `num_ifm<N>_shim_ch`, `num_scratch_0_in_shim_ch`, `num_scratch_0_out_shim_ch` and `num_ofm_shim_ch`. Ideally you have MLIR files that result from the previous compilation from where you can deduce the numbers.
    ```yaml
      - name: num_ifm_shim_ch
        data_type: uint32
    +   defined_value: 2
    ```

## Phase 5: Kernel Optimization

**Phase 5 is MANDATORY.** Passing Phase 4 with a scalar fallback kernel
is NOT a valid stopping point -- the kernel must be optimized before
proceeding to Phase 6. A correct-but-unoptimized kernel is an
incomplete custom op.

**Mandatory exit criteria** (all must hold before reporting Phase 5
complete or proceeding to Phase 6):

- BOTH `/vai-aie-kernel-development` AND `/vai-aie-compiler-oriented-optimizations`
  were invoked. The two are complementary:
  - `vai-aie-kernel-development` covers architecture-level patterns
    (vectorization, loop splitting for register pressure, in-place
    updates, VLIW slot awareness, NOINLINE core pattern).
  - `vai-aie-compiler-oriented-optimizations` covers Peano-compiler-specific
    pragmas and hints (restrict pointers, DM bank annotations, loop
    pragmas / hints, software pipelining pre-RA vs post-RA, loop
    versioning, vector alignment, sub-32-bit handling, optimization
    remarks).
  Skipping either skill is not allowed -- many wins (e.g. unblocking
  software pipelining, fixing alignment-driven scalarization) live only
  in the compiler-oriented skill.
- **Vectorization was attempted.** A scalar `for` loop is acceptable as
  the *final* kernel ONLY if vectorization was tried, broke
  correctness or was structurally infeasible for this op, and the
  reason is documented in the report (or `optimization_verdict` /
  `peer_insights` when running under `vai-custom-op`).
- All other applicable techniques from both skills were considered and
  applied where they fit.
- Phase 4 (compile + x86sim + `compare_npy.py`) was re-run after each
  optimization change and still passes.
- **Static metrics were inspected after every compile** -- the `.lst` schedule,
  see step 5a -- and each optimization was chosen from what they showed. This
  applies with or without a board; there is no exemption.
- **Board-based measurement was performed before integration whenever
  a board is available.** See step 5b below. Board measurement is part
  of Phase 5, not deferred to Phase 7 -- the kernel's per-op cost,
  bottleneck class (compute vs DMA vs sync), and the impact of each
  optimization step must be known on real hardware before declaring
  Phase 5 complete. Skipping board measurement is allowed ONLY when
  no board is reachable, and the absence must be documented. NPU compute
  time is measured via `/vai-perf-analysis`.
- Each successful optimization step is committed to the local git repo.

### Optimization is data-driven -- ALWAYS, board or no board

The performance is very important. **MANDATORY:** After **each compilation**, inspect the
Peano-generated `.lst` (disassembly listing) files to see how the kernel can be
improved further.

**Never** change a kernel speculatively: measure, optimize the bottleneck the data
points to, re-measure to confirm the change actually helped, then repeat. Step 5
requires **both** kinds of metric - static and dynamic - whenever both are obtainable:

If no board is reachable, the static half of step 5 is still mandatory on every
compile and the exit criteria above still apply; you simply cannot rank
optimizations by measured impact and must lean on the best-practice lists from
the two skills above.

1. Load the **vai-aie-kernel-development** skill (invoke `/vai-aie-kernel-development`)
   AND the **vai-aie-compiler-oriented-optimizations** skill
   (invoke `/vai-aie-compiler-oriented-optimizations`).
2. Apply the optimization techniques from both skills to the kernel:
   restrict pointers, DM bank annotations, NOINLINE core pattern,
   vectorization, loop pipelining pragmas, software pipelining hints,
   loop versioning, vector alignment, etc.
3. After each optimization change, loop back to **Phase 4** (simulate
   and validate) to confirm the kernel is still functionally correct.
4. Commit each successful optimization step to the local git repo.
5. **Measure -- static metrics always, dynamic metrics whenever a board is
   available. MANDATORY.**

   **5a. Static metrics (every compile, no board required).**
   **Finding the `.lst`:** don't guess the core coordinate -- glob the AIE build
   tree and use whatever kernel listing actually exists. Make a strong effort to
   locate it; if you can't find one, fail loudly and re-check rather than silently
   skipping the analysis.
   **What to extract from the `.lst`:** the emitted VLIW schedule
   (software-pipelining status and II, vector vs. scalar slot usage, spills, and
   stalls). Feed those findings back into the optimization loop to target the
   specific bottleneck the disassembly reveals. See
   `/vai-aie-compiler-oriented-optimizations` for how to read and act on these
   listings and the related optimization remarks.

   **5b. Dynamic metrics (board).** Use the `run_on_board.py` script from
    `<skill_dir>/scripts/`, or another user-provided mechanism to validate on
     the board. To do so:
   - Reuse the Phase 3 cache directly, with no recompile. Just pass the normal
     `vitisai_config.json`, not the x86sim copy (Critical Workflow Rule 4).
   - Run on the board, **reusing the same `inputs.npz` from Phase 1b** so the
     board outputs can be compared against the CPU golden reference.
     You usually only need to pass the working directory as `-p` argument and
     the target board host name / IP address; you may also be provided with
     an username + password / SSH key to use, which you need to use in that case.
     The arguments after `--` are forwarded to `run.py` (check the `run.py` syntax):
     ```bash
     bash -c '
     <ENV_SETUP>
     cd <working_dir>
     python <skill_dir>/scripts/run_on_board.py \
         -p <working_dir> \
         --boardhost <BOARDHOST> \
         [--board-user <BOARD_USER>] \
         [--board-password <PASSWORD>] \
         [--board-key <SSH_KEY>] \
         -- <model_b>.onnx \
            --input-dir <working_dir>/reference_data \
            --output-dir <working_dir>/board_outputs
     '
     ```
     Add `--dry-run` first to preview the command before executing.
   - **Verify numeric accuracy on the board.** Hardware execution can diverge
     from x86sim (different rounding, real DMA behavior, race conditions), so
     re-run the comparison from Phase 4b against the board outputs:
     ```bash
     python <skill_dir>/scripts/compare_npy.py \
         <working_dir>/reference_data/<output_name>.npy \
         <working_dir>/board_outputs/<output_name>.npy \
         --rtol 0.01 --atol 0.015 --verbose
     ```
     If x86sim passed but the board fails, the bug is hardware-specific (DMA
     alignment, bank conflicts, sync issues) -- do not proceed with performance
     optimization until correctness on the board is restored.
   - **MANDATORY** Then invoke the **vai-perf-analysis** skill (`/vai-perf-analysis`) on the run
     artifacts to get a per-op timing breakdown. The canonical entry point
     is `vai-perf-analysis/scripts/ai_extract.py` -- it reports the actual NPU
     compute time per op. Do NOT measure custom-op performance with Python
     `time.time()` wrappers around the inference call: wall-clock
     measurements include host-side overhead (data movement, ORT dispatch,
     sync waits) that can be **10-20x larger** than the NPU compute time
     itself. When the user asks "how fast is this op", reach for
     `ai_extract.py` first; only fall back to wall-clock if nothing else is
     available, and label the result as wall-clock so it is not confused
     with NPU compute time.
     When the question is specifically "how long did *this* custom op
     take", pass `--query <op_name>` (the op's registered name) to
     `ai_extract.py`. The compact overview and `--top N` views can both
     miss or under-report a single op, so the per-op number must come from
     `--query`.
     Use the report to answer: how much NPU compute time is the custom op
     actually taking? Where in the kernel (compute vs. DMA vs. sync) is
     that time being spent? Which optimization from
     `vai-aie-kernel-development` targets that bottleneck?
   **The loop is MANDATORY, not a single pass.** Use what the metrics tell you to
   choose the next optimization from step 2, then repeat steps 3-5 -- re-measuring
   the static metrics on every compile and the dynamic ones whenever a board is
   available -- until the data shows the kernel is no longer a bottleneck or
   further optimization shows diminishing returns. One optimization pass, or a
   pass whose effect you never re-measured, does not complete Phase 5.

   If no board is available, keep running the loop on static metrics alone and
   apply the best-practice optimizations from `vai-aie-kernel-development`, but flag
   clearly to the user that the gains are unverified and may regress
   real-hardware performance.

Only proceed to Phase 6 once the kernel is both correct and optimized.

Self-audit: Before declaring a kernel's tiling final and optimize, verify
that all the following distribution and optimzation axes are exercised.

```
Kernel code:
- [ ] Did you make aggressive use of vectorization?
- [ ] Did you rely on the AIE API instead of doing ad-hoc implementations?
- [ ] Did you use the best practices from sibling skills on kernel programming?
- [ ] Are `stack_size`/`heap_size` left at defaults? (They must be -- if the kernel overflows, apply the four checks in "Stack and Heap Sizing" instead of raising the budget.)

Tiling:
- [ ] Did you design tiling from first principles starting from the output and considering the algorithm?
- [ ] After each L3<->L2 Transpose, is the innermost (DMA burst) axis still large? Don't push a small/sub-word axis innermost -- reorder in-kernel instead.
- [ ] Did you make use of Transpose/Repeat to minimize L3<->L2 Data transfers?
- [ ] Does the tiling instantiate kernels on all columns of the overlay?
- [ ] Does the tiling instantiate kernels on all stamps of the overlay (honoring `tp_size`; see Development Methodology)?
- [ ] If you decided for a 1x1 tiling implementation, is it due to overlay or algorithm constraints?
```



## Phase 6: Model Re-integration

After validating the custom op, create an integration directory and stitch the custom op back into the full model.

### 6a. Create the integration directory

Create a new directory next to the custom op working directory to hold the integrated model and its config. `<integration_dir>` defaults to `integration/`:

```bash
mkdir -p <integration_dir>
```

The `<integration_dir>` should only contain one `record_timer_ts.json` - `record_timer_ts.json` in sub-directories are also forbidden which means that one folder contains only one board run - from executing the final model on the board. `<integration_dir>` is called `integration` by default and stays right under `<working_dir>`. The cache directory with the compilation artifacts must also stay in `integration`: this is inteded to be an hermetic directory from which we can analyze performance data with AI Analyzer.

### 6b. Stitch the custom op into the full model

```bash
<ENV_SETUP>
python <skill_dir>/scripts/onnx_stitch.py \
    --model <full_model>.onnx \
    --nodes <node_name_or_op_type_1> [<node_name_or_op_type_2> ...] \
    --custom-op-name <op_name> \
    --domain mydomain \
    --output <integration_dir>/integrated_model.onnx
```

This replaces the original subgraph with a `mydomain.<op_name>` custom op node, preserving:
- All other nodes in the graph
- Initializers used by the custom op (as additional inputs)
- Graph inputs and outputs
- Opset declarations (adds the custom domain)

### 6c. Set up vitisai_config.json

Copy the original vitisai_config.json to the integration directory and add a `custom_ops` entry pointing to the custom op implementation from `<working_dir>`:

```bash
cp <original_vitisai_config> <integration_dir>/vitisai_config.json
```

Then edit `<integration_dir>/vitisai_config.json` to add the `custom_ops` section inside `vaiml_config`, with the `op_config` path pointing to the YAML in the custom op working directory:

```json
"custom_ops": {
    "mydomain.<op_name>": {
        "op_config": "<working_dir>/custom_op_<name>/<name>.yaml"
    }
}
```

The path to `op_config` must be either absolute or relative to `<integration_dir>`. Since the kernel .cpp, tiling .py, and YAML config live in `<working_dir>/custom_op_<name>/`, use the absolute path to avoid ambiguity.

**Add the x86sim flags to this copied config** :

```json
      "aiecompiler_args": "--compile-for-x86sim=true --x86sim-as-shared-library=true",
```

## Phase 7: End-to-End Verification

**This phase is MANDATORY.** At minimum, the integrated model must compile successfully.

### 7a. Compile the integrated model (REQUIRED)

**Run in a sub-agent.** This verifies the custom op is correctly wired into the full model and that the compiler accepts it.

```bash
bash -c '
<ENV_SETUP>
export DEBUG_VAIML_PARTITION=1
export FLEXML_PRINT_VITISTOOLS_OUTPUT=1
cd <integration_dir>
python <skill_dir>/scripts/compile.py \
    integrated_model.onnx \
    --vitisai-config vitisai_config.json
'
```

Verify: check for `"Compilation successful"` and verify that the custom op appears in a list of ops starting by:
```
-----------------------
INFO: [VAIML-COMPILE 1000] Operation statistics for AIE partitions:
 Operations encountered:
-----------------------
[...]
  templatedGraph:mydomain.myop ...
```
The op MUST NOT appear in a list of ops starting by:
```
-----------------------
INFO: [VAIML-COMPILE 1000] Operation statistics for CPU partitions:
 Operations encountered:
-----------------------
```


**IMPORTANT:** When integration compilation fails, trace the root cause systematically -- this is a different failure mode from Phase 3. The full model context introduces new constraints (e.g., different tensor shapes, shim channel conflicts), so the bug may be either in the config or in the custom op itself. The bug is not from compile.py, do not attempt to fix this script.

### 7b. Generate full-model CPU reference

```bash
python <skill_dir>/scripts/compile.py \
    <full_model>.onnx --cpu \
    --input-dir <integration_dir>/full_reference_data \
    --output-dir <integration_dir>/full_reference_data
```

Same rule as Phase 1b: pass `--input-dir` too, or the full-model inputs land in
`<model_stem>_inputs/` and the 6c comparison has no inputs to feed the integrated
model with.

### 7c. Compare outputs

Run x86sim on the integrated model and compare against the original model's CPU output to verify end-to-end correctness.

## Key Architecture Facts

See [README.md](../../README.md) for the complete architecture reference.

**Quick reminders:**
- VAIML converts float32 -> bfloat16 automatically; kernels receive bfloat16
- L1: 64KB total, 0xA000-0xDFFF reserved for stack/heap
- L2: 512KB per mem tile column; input tensor placement: for column-wise broadcast to L1 on tiles 0-2, for row-wise broadcast to L1 on tiles 2-3
- Output in L2 on tiles 0-2
- Tile sizes must be aligned to kernel vectorization (e.g., multiples of 16 for bfloat16 vectors)
- DMA requires 32-bit aligned transfers
- **No stdc++ runtime**: `std::exp`, `std::tanh`, `std::sqrt`, `<cmath>`, `<algorithm>` are NOT available. Use the AIE API (`aie::` namespace) and NLF hardware intrinsics (`::tanh()`, `::exp2()`) instead
- Custom ops support at most 2 inputs in the core tiles; pack extras into IFM/WTS via tiling or the DMA controllers, see "Multi-input" in Design Constraints.
- Custom ops produce 1 output; concatenate outputs in the kernel and split using slicing, see "Multi-output" in Design Constraints.

## Script Reference

| Script | Usage |
|--------|-------|
| `compile.py` | `python <skill_dir>/scripts/compile.py <model>.onnx` (VitisAI compile) or `compile.py <m> --cpu --output-dir <dir>` (CPU inference) |
| `run.py` | `python <skill_dir>/scripts/run.py <model>.onnx` -- runs on VitisAI hardware, **or in x86sim** when the `--vitisai-config` you pass sets `runner_type: "x86sim"` |
| `onnx_cut.py` | `python <skill_dir>/scripts/onnx_cut.py --model <m> --report` or `--nodes <n1> [<n2>] --output <out>` |
| `create_custom_op_model.py` | `python <skill_dir>/scripts/create_custom_op_model.py --model model_a.onnx --custom-op-name <n> --output model_b.onnx` or `--inspect` |
| `onnx_stitch.py` | `python <skill_dir>/scripts/onnx_stitch.py --model <m> --nodes <n1> [<n2>] --custom-op-name <n> --output <out>` |
| `compare_npy.py` | `python <skill_dir>/scripts/compare_npy.py <ref>.npy <test>.npy --rtol 0.01 --atol 0.015` |
| `run_on_board.py` | `python <skill_dir>/scripts/run_on_board.py` (run on remote board via SSH) |
| `custom_ops_utils.py` | Imported by other scripts (not called directly) |

## Troubleshooting

### Common Errors

1. **`custom op shape infer get shape and data_type failed`** -- The custom op node in the ONNX model is missing the required `shape` and `data_type` attributes.
2. **`unsupported data type 1`** -- XRT not installed; compilation succeeded but inference cannot run.
3. **Buffer overlap in L1** -- Check that ping/pong addresses don't overlap and avoid 0xA000-0xDFFF.
4. **DMA alignment errors** -- Innermost dimension must allow 32-bit aligned transfers.
5. **Shape mismatch in transfers** -- L2 buffer inner dims must match L1 buffer shape exactly.
6. **`kernel_ratios` mismatch** -- Async buffer acquire/release count in C++ must match Python `kernel_ratios`.
7. **Compilation reports success but tiling failed silently** -- Check for `"Compilation successful"`, `"ERROR:"` messages during compilation, and that the op is under `"Operation Statistics for CPU"` instead of `"Operation statistics for AIE Partitions"`.
8. **x86sim NaN / garbage** -- When `enable_f32_to_bf16_conversion: true`, data files must contain bfloat16 data, not float32.
10. **`RepeatToMatch` shape error** -- Use `.Reshape([flat_size])` on DDR tensor before `set_l3_to_l2_transfer`.
11. **`Reshape sizes invalid`** -- Use `getPaddedShape()` instead of `getShape()` when computing buffer sizes.
12. **`set_l2_to_l1_transfer()` TypeError with 2D list** -- `SpatialDistribute2D` returns a nested 2D Python list of `TensorExpr`s, which `set_l2_to_l1_transfer()` does not accept. Use `tensorvar.TileTo(index=0, numTiles=n_rows)` instead, which returns a single `TensorExpr` encoding the row distribution (also works with columns).
13. **`We have not finished Reshape for TensorExprs`** -- This VAIML error is **non-fatal**. The framework logs it as a plugin warning (tags `VAIML-MKT 13999` / `VAIML-COMPILE 1000`) but does not abort compilation. If this error shows up, despite the process exiting with 0 and printing `"Success!"`, the compilation of the custom op failed. You need to fix the tiling in that case.
14. **Compilation exit code 0 masks tiling errors** -- VAIML may log `Reshape sizes invalid` or `RepeatToMatch shape mismatch` errors but still exit 0 with `"Custom ops model compiled successfully"`. These plugin errors are not propagated to the process exit code. Always check the actual log output for errors, not just the exit code. A model that compiles with logged errors may still fail at runtime.
15. **Kernel signature mismatch from tiling script** -- The kernel must have the number of arguments set in `set_kernel_params` plus the last argument being `lp_params`.
16. **AIE runtime failure despite successful compilation** -- The custom op compiles and VAIML reports 100% AIE offload, but `sess.run()` throws `RUNTIME_EXCEPTION: Custom op '<name>' couldn't be executed on the AIE`. CPU fallback is not supported for custom ops. Common causes: (a) kernel C++ signature does not match the generated ADF call from tiling, (b) tiling produces data movement specs that pass compile validation but fail hardware execution, (c) `gen_tg_adf/` files contain errors masked by exit code 0. Check `l2_to_l3_tiling_analysis.csv` and the `pm_reload_analysis0.cc` generated source for clues.
17. **`mydomain:<op_name>(-1) is not a registered function/op`** -- OnnxRuntime cannot find the custom op during session creation. This happens when the custom op shared library is not built or not correctly loaded. Note: `custom_ops_utils.register_custom_ops_from_vitisai_config()` registers ops at the Python level, but `VitisAIExecutionProvider` performs its own C++ op lookup independently. For VAIML compilation, use `compile.py` which handles registration correctly. For standalone inference, ensure the shared library path is correct in `vitisai_config.json`.
18. **`Reshape()` after `Tile()` is not supported** -- Calling `.Reshape()` on a `TensorExpr` that has already been tiled (via `Tile()` or `TileBy()`) causes `RuntimeError: "not finished Reshape"`. Reshape must be applied before tiling operations. Reorder the chain to `.Reshape([...]).TileBy(...)` instead of `.TileBy(...).Reshape([...])`.
19. **Wrong dimension tiling on multi-dimensional data** -- When tiling multi-dimensional data (e.g., `[Cin, Din, Hin, Win]`), tile on the correct dimension to preserve data layout. Flattening to 1D then tiling loses the multi-dimensional structure. Wrong: `Reshape([Cin*Din*HW]).Tile(0, ...)` (mixes Cin and D dimensions). Right: `Reshape([Cin, Din*HW]).Tile(1, ...)` (tiles D within each Cin channel).
20. **Daemon endpoint bind failure on board** -- If a board-side runtime daemon log reports `"Failed to create acceptor endpoint ..., exception: bind: Cannot assign requested address"`, the daemon cannot bind to its loopback endpoint -- typically because the relevant IPv4/IPv6 stack is disabled on the board host. This is an infrastructure issue, not a kernel/tiling bug. Check the loopback configuration on the board host.
21. **`Failed to load x86sim library ...` on the board**, then `RUNTIME_EXCEPTION ... HW context creation unsuccessful` -- `runner_type` resolved to `x86sim` (see the preceding `[VAIML-CUSTOMOP] runner_type:` line), so the board tried to load the x86-64 `libx86_sim.so` on aarch64. Either you passed the x86sim config, or you *compiled* with the key: the cache stores it, and omitting it later means unspecified, not `"hw"`. Check with `grep -o 'runner_type[^,}]*' <cache>/vaiml_par_0/compile_flags.json` and recompile without it.
22. **x86sim outputs all zeros, yet `Execution successful` and exit code 0** -- `--num-runs` left at its default of 10. Only the first iteration computes (`ERROR: Layered execution is supported only for designs that have a single run iteration`); the rest yield zeros and `run.py` saves the last. Use `--num-runs 1`. Not a cache/config problem -- recompiling with `runner_type: "x86sim"` changes nothing.

### Environment Setup Checklist

```bash
<ENV_SETUP>                                    # source <activate>, or omit if pre-provisioned
export DEBUG_VAIML_PARTITION=1                 # Show partition info
export FLEXML_PRINT_VITISTOOLS_OUTPUT=1        # Show aiecompiler output
rm -rf /tmp/$USER/vaip/.cache                  # Clear cache if needed
```
