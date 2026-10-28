---
name: vai-partition-analysis
license: Apache-2.0 WITH LLVM-exception
compatibility: Requires VitisAI 6.3+
metadata:
  version: 6.3.0
  stage: beta
description: Inspect the result of a VAIML compilation of a mixed-precision ONNX model
  and reduce the number of NPU partitions toward a single partition. Parses the compiler
  operation statistics (matched kernels / templated graphs), the partition count,
  and the AIE/CPU offload split; when more than one partition is produced, reads the
  CpuBecause messages and compilation warnings, classifies them, and proposes remediation.
  Remediation prefers the correct frontend (fe_args) flags over model patching; when
  the partition break originates from quantization, it proposes Quark configuration
  changes instead. Every proposed change is followed by a re-compilation to evaluate
  the result.
---

# Partition-Analysis Skill

## Access command

This skill must always be accessed through the worker, never in a different way.
Allowed worker: `vai-mixed-precision-worker`.

## Description

Inspect a VAIML compilation of a mixed-precision model and drive it toward a
**single NPU partition**. This skill does not compile by itself: it reads the
artifacts of a compilation that already ran, reports the partitioning it
achieved, and — when the model did not collapse to one partition — proposes the
**smallest change that can remove a partition boundary** and asks to re-compile
to evaluate it.

> **Scope rule (non-negotiable).** This skill reduces partitions by **choosing
> the right compiler frontend (`fe_args`) flags** and, when the break is
> caused by quantization, by **adjusting the Quark quantization configuration**.
> It does **NOT** patch the ONNX graph, rewrite nodes, change layer
> shapes/counts, or prune the model to force a pass. Model patching and model
> modification are out of scope — if nothing in the flag surface or the Quark
> config can close the gap, say so and stop.

> **Config key aliases.** `fe_args` and `fe_experiment` are the same option, as
> are `group_args` and `experiments`. Compiler logs and older configs may use either
> spelling — read both, write `fe_args` and `group_args`.

## Parse Arguments

This skill expects arguments in this form:

```
--compile-dir <vaiml_compile_dir> [--log <compile.log>] [--model <onnx>] [--config <vitisai_config.json>] [--device stx|ve2] [--quark-config <quark.json>]
```

- `--compile-dir <path>`: **(MANDATORY)** Directory containing the VAIML
  compilation artifacts (the cache dir produced by `compile.py` /
  `compile_probe.py`, e.g. `<model_stem>/` with `cache/vaiml_par_*` inside).
  The compile must have run with `keep_outputs: true` so the
  `*.chained_kernel.tosa.mlir` and the pass summaries are on disk.
- `--log <path>`: **(OPTIONAL)** The captured compiler stdout/stderr log. If not
  given, look for `compile.log`, `AIECompiler.log`, or the ORT capture under
  `--compile-dir`. The `[VAIML-COMPILE ...]` operation-statistics and
  partition-count lines are read from here.
- `--model <path>`: **(OPTIONAL)** The compiled ONNX model. Needed only when the
  remediation requires re-examining the graph (e.g. reading a `QuantizeLinear`
  scale/zero_point to decide whether `match-power-of-two-quant-kernel` can fire).
- `--config <path>`: **(OPTIONAL)** The `vitisai_config.json` that was compiled.
  New flag proposals are written on top of this file, never from scratch —
  every flag already present is carried forward.
- `--device <stx|ve2>`: **(OPTIONAL, default: ve2)** Target device. Governs
  whether BF16 (`enable_f32_to_bf16_conversion`) or FP16
  (`enable_f32_to_f16_conversion`) conversion is the right lever.
- `--quark-config <path>`: **(OPTIONAL)** The Quark JSON config that produced the
  quantized model. Required only when the remediation is a quantization change
  (see [Quark-config remediation](#remediation-b-quark-configuration-when-the-break-is-quantization)).

Skill directory: the directory containing this `SKILL.md` (referred to below as
`<skill_dir>`). The reused CpuBecause/offload parser is `offload_gap.py` in the
scripts folder of the `vai-flag-configuration` skill.

Scripts of that skill are addressed through a shell variable: before running any
snippet below, set `VAI_FLAG_CONFIGURATION_SCRIPTS` to the script directory of
the `vai-flag-configuration` skill, and set
`VAI_CUSTOM_OP_IMPLEMENTATION_SCRIPTS` to the script directory of the
`vai-custom-op-implementation` skill.

## Phase 1 — Read the partitioning the compiler achieved

The compiler reports the partitioning in its log. Extract three facts, in order.

### 1a. Operation statistics (what matched, and as what)

The compiler prints an operation census after frontend matching:

```
INFO: [VAIML-COMPILE 1000] Operation statistics for the model:
 Operations encountered:
-----------------------
  kernel:AddBf163D (bf16, bf16) -> (bf16)                             , 25
  kernel:DequantizeLinear3D (i8) -> (bf16)                            , 1
  kernel:GeluLUTQi83D (i8, ui8) -> (i8)                               , 12
  kernel:Gemm (i8, i8, i16) -> (bf16)                                 , 12
  kernel:LayerNormRowMajor1Pass (i8, i8, i8) -> (i8)                  , 25
  kernel:QuantizeLinear3D (bf16) -> (i8)                              , 25
  templatedGraph:MX9MHAs256d512m2048Adf (i8, f32, f32, ...) -> (bf16) , 12
```

Parse each line into `(match_kind, name, in_dtypes, out_dtypes, count)` where
`match_kind` is `kernel` or `templatedGraph`. Report this as a table. The dtypes
matter: a `kernel:...Bf16...` line means the op was placed on the NPU in bf16; a
line that still carries `f32`/`float32` in its signature is a red flag (a naked
float op the frontend did not convert — see the `[MLLIB]` `config.dtype` failures
below). The exact kernels and templated graphs differ per model; do not assume a
fixed set.

### 1b. Partition count (the number to drive to 1)

```
INFO: [VAIML-COMPILE 1000] Partition completed with 1 partition
INFO: [VAIML-COMPILE 1046] 100.00% of operations will run on AIE, 0.00% of operations will run on CPU.
```

Extract:
- **partition count** from `Partition completed with N partition`;
- **AIE / CPU split** from `[VAIML-COMPILE 1046] X% ... on AIE, Y% ... on CPU`.

**Success criterion:** exactly **1 partition** and **100.00% on AIE**. When both
hold, report success (with the operation-statistics table for the record) and
stop — there is nothing to remediate.

### 1c. Where each partition breaks (only when count > 1)

For a multi-partition result the compiler names the boundary op of each break:

```
Partition 0 breaks at: CpuBecause("/model.6/.../Transpose_2_output_0_DequantizeLinear") / CpuBecause(".../Split_output_1_DequantizeLinear")
Partition 1 breaks at: CpuBecause("/model.6/.../Transpose_3_output_0_DequantizeLinear")
```

Collect every `Partition N breaks at: CpuBecause(...)` line. The op named inside
each `CpuBecause(...)` is the boundary that split the graph — these are the ops
to remove from the CPU. `graph_partition_trace.csv` under `cache/` carries the
same information in tabular form when present.

## Phase 2 — Read the CpuBecause messages and warnings (when count > 1)

Every operator the compiler pushed to the CPU becomes an `xten_nn.subgraph` with
`Reason = "CpuBecause"`, an `Op` attribute (the responsible operation) and a
`Message` (the compiler's own explanation) in the
`*.chained_kernel.tosa.mlir`. **Do not hand-parse the MLIR** — reuse the parser
that already ships in the `vai-flag-configuration` skill:

```bash
python3 - <<'PY'
import sys
import os
sys.path.insert(0, os.environ["VAI_FLAG_CONFIGURATION_SCRIPTS"])
from offload_gap import find_chained_kernel_mlir, offload_gap, classify_message
mlir = find_chained_kernel_mlir("<compile-dir>")
for entry in offload_gap(mlir):                 # ranked by node count
    route = {m: classify_message(m).route for m in entry.messages}
    print(entry.op, entry.count, entry.messages, route)
print("MLIR:", mlir)
PY
```

`offload_gap()` returns, biggest-first, every op type still on the CPU with the
compiler's verbatim `Message` and a routing tag from `classify_message()`. Also
read the compiler's **warnings** (`WARNING: [VAIML-...]` in the log and
`preliminary-`/`final-vaiml-pass-summary.txt` under `cache/`) — a warning often
names the same boundary from the FE side.

### CpuBecause routing table (from `offload_gap.classify_message`)

Only these markers are attributable to a stage; anything else is
`unclassified` and must be reported **verbatim**, never guessed at.

| Marker in `Message` | Route | What it means | First thing to try |
|---|---|---|---|
| `User requested this layer to be partitioned out` | `user-config` | This run's own config pushed the layer to CPU. | Review the active flags in `--config` before proposing new ones — you may be causing the break. |
| `Unwrapping layer with ...` | `tiling-unwrap` | The tiling engine could not place the named kernel. | Kernel-specific chaining flag or spilling analysis (hand to `vai-flag-configuration` / `vai-perf-analysis`), not a quantization change. |
| `... [FE]` | `fe` (frontend) | The frontend did not match the operator. | A frontend flag that **decomposes or rewrites** the op, else it is a quantization-boundary or custom-op issue. |
| `... [BE]` | `be` (backend) | No backend kernel for this shape/dtype. | A rewrite flag (e.g. conv↔gemm) that reaches a supported kernel. |
| `... [MLLIB]` | `mllib` | A kernel-library constraint rejected the layer. | Read the constraint; commonly a `config.dtype` mismatch → a naked float op that must be converted (see below). |

### Common CpuBecause messages and their cause (cite the message verbatim)

These are frequently seen on mixed-precision models. Match on the message text,
then follow the remediation in Phase 3.

| Message (substring) | Cause | Primary remediation class |
|---|---|---|
| `Standalone tosa.cast is not supported [FE]` | A naked float cast left at an island/function edge. | Frontend flag — dtype conversion (Remediation A). |
| `Standalone dequantizeLinear is not supported [FE]` / `Standalone quantizeLinear is not supported [FE]` | A lone Q or DQ sits on a partition/function edge (the classic partition-break op in `Partition N breaks at`). | Frontend flag — edge/power-of-two quant kernel (A). If the Q/DQ cannot be matched, it is a **quantization** issue (B). |
| `YAML constraints failed [MLLIB]: ... 'config.dtype' ... float32 ... incompatible` | A kernel (e.g. `MulBf16`, `GemmBfp16`, `AddBf163D`) was asked to run in `float32` because a naked float op was not converted. | Frontend flag — enable bf16/f16 conversion (A). |
| `Dataformat Edge to Op can not be fixed` | Layout mismatch at a function edge. | Frontend flag — data-storage / layout (A). Not model patching. |
| `Reshape with start garbage cannot be merged into non-AIE consumer` / `PseudoOp:Reshape only supports bf16, fp16, int8, and uint8` | A reshape feeds a CPU consumer or carries an unsupported dtype. | Frontend flag; if dtype is float32, converge it via dtype conversion (A). |
| `Small tensor (threshold 100) in function edge` | A tiny tensor at an edge is cheaper on CPU by the threshold heuristic. | Frontend flag — small-tensor threshold (A), **but this conflicts with a max-offload goal**: only unwrap when a single partition is the explicit goal. |
| `onnx.Transpose in function edge` | A transpose landed on a partition edge. | Frontend flag (A). Never insert/rewrite transposes in the ONNX. |
| `Datatype Unsupported [FE]: tosa.select : i1` / `Unsupported gather with constant data input and non-scalar indices [FE]` | A genuinely unsupported op/dtype at the frontend. | Often not fixable by a public flag — report verbatim; may need quantization change (B) or is a hard limit. |

## Phase 3 — Propose remediation (frontend flags first)

Decide the remediation **class** per gap entry from its route and message, then
propose the concrete change. Always prefer Remediation A. Only use Remediation B
when the break is caused by quantization. Never patch the model.

### Remediation A — frontend (`fe_args`) flags (default)

This is the primary path for reducing partitions. Reuse the analysis already
implemented by the sibling skills:

1. **Delegate dtype/island reasoning to `/vai-fe-dtype`**
   (`vai-fe-args`): it classifies the model's island
   topology and returns the required conversion + kernel-matching flags. The two
   levers it produces are the ones that collapse most mixed-precision breaks:
   - **Naked float ops** (`config.dtype ... float32 ... incompatible`, standalone
     `tosa.cast`): set `enable_f32_to_bf16_conversion: true` (STX/BF16) or
     `enable_f32_to_f16_conversion: true` with `device: ve2` (Telluride/FP16).
   - **Standalone Q/DQ at edges** (`Standalone [de]quantizeLinear ... [FE]`,
     `Partition N breaks at: CpuBecause(...DequantizeLinear)`): add
     `match-power-of-two-quant-kernel=1` so the boundary Q/DQ is matched as an
     NPU kernel, and/or offload the boundary conversion to the runtime with
     `edge-quantization-in-rt=1` (or the one-sided `input-quantization-in-rt=1` /
     `output-dequantization-in-rt=1`). These are equivalent to the mixed-precision
     `group_args`/`match-power-of-two-quant-kernel` settings the orchestrator
     already documents.
2. **Turn the CpuBecause gap into candidate flags** with the
   `vai-flag-configuration` catalog. From the same gap entries produced in
   Phase 2:
   ```bash
   python3 - <<'PY'
   import os, sys; sys.path.insert(0, os.environ["VAI_FLAG_CONFIGURATION_SCRIPTS"])
   from offload_gap import find_chained_kernel_mlir, offload_gap, match_gap_to_flags
   from flag_catalog import load_catalog, proposable
   gap = offload_gap(find_chained_kernel_mlir("<compile-dir>"))
   cat = proposable(load_catalog(), objectives=["offload"], autonomous=False)
   for spec, reason in match_gap_to_flags(gap, cat):
       print(spec.name, "::", reason, "::", spec.path)
   PY
   ```
   `match_gap_to_flags` returns only flags that target an op **still on the CPU**,
   ranked so a flag naming the missing op comes before a generic element-wise
   match. Treat it as a **shortlist**: read each flag's catalog description and
   discard any whose mechanism does not apply to the cited op. Only propose
   `public: true` flags — never a flag outside the public catalog.
3. **Backend `[BE]` gaps**: propose a rewrite flag that reaches a supported
   kernel (e.g. `enable-conv-to-im2col-and-gemm=1` / `prefer-conv-to-gemm-conversion=true`
   for a Conv with no backend kernel). Cite the flag's catalog path.
4. **`tiling-unwrap` gaps**: this is a placement/spilling problem, not a
   frontend or quantization one. Hand the compile dir to `/vai-flag-configuration`
   (or `/vai-perf-analysis`) for a kernel-chaining/spilling flag rather than
   changing dtype or quantization.
5. **Respect existing flags and the budget.** Write proposals on top of
   `--config`, carrying every flag already set. Propose at most a **few** flag
   changes per iteration so the effect stays interpretable, and record for each
   flag its catalog source path, the default it deviates from, and a one-line
   rationale drawn from the compiler message. A proposal without a cited source
   and reason is incomplete — do not present it.

**`needs-consent` flags:** never enable an accuracy-trading or
contract-changing flag (e.g. `small-tensor-threshold-unwrapping`,
`use-accurate-mode`, `indices-are-positive`) on the user's behalf. Offer it with
the trade-off stated and wait for consent.

### Remediation B — Quark configuration (when the break is quantization)

Use this only when the partition break originates from **how the model was
quantized**, i.e. the gap is a standalone Q/DQ or a quant-boundary that a
frontend flag cannot match. Typical signals:

- `match-power-of-two-quant-kernel=1` cannot fire because the boundary
  `QuantizeLinear` has a **non-power-of-two scale** or a **non-zero zero_point**
  (read the initializers off `--model`; Quark symmetric-int8 usually satisfies
  both). Fix it at the source: quantize **symmetric int8 with power-of-two
  scales and zero_point 0** (`"ActivationSymmetric": true`, symmetric weight/act
  specs) so the boundary Q/DQ becomes matchable.
- The mixed-precision assignment creates **many small float islands**, each
  bounded by a DQ→float→Q pair that becomes a partition break. Reduce the number
  of boundaries by moving the float/int8 cut so contiguous regions share one
  precision (fewer transitions), or promote/demote the offending layers — via the
  Quark config's `specific_layer_config` / `target_node_names`, **not** by
  editing the graph. Fewer precision transitions ⇒ fewer partitions.
- Naked float ops leaked because casts were not emitted as QDQ: ensure
  `"BF16QDQToCast": true` and that `enable_f32_to_bf16_conversion` is consistent
  with the config, and keep `EnableDualQuantNodePairs` where dual QDQ pairs are
  needed at boundaries.

Apply the change by re-running quantization through the orchestrator's
`mixed_precision_quantize.py` with the adjusted Quark JSON (hand back to
`/vai-quantize` or `/vai-quantization-guide --mode requantize`). **Do not** hand-edit Q/DQ
nodes in the ONNX — change the Quark config and re-quantize.

> If a break is neither a frontend-flag case nor a quantization case (e.g.
> `Datatype Unsupported [FE]: tosa.select : i1`, a genuine unsupported op),
> report it verbatim and state that it is outside this skill's flag/quant
> surface. Do not invent a fix and do not patch the model.

## Phase 4 — Re-compile to evaluate (every time)

**A proposal is not a result.** Every change this skill proposes MUST be followed
by a VAIML re-compilation so its effect on the partition count is measured, not
assumed. After writing the new `vitisai_config.json` (Remediation A) or producing
a re-quantized model (Remediation B):

1. Ask the user to re-compile (a choice), or state that you are re-compiling in
   autonomous mode, and run the compile with `keep_outputs: true`. Use the same
   compiler entry point the orchestrator uses:
   ```bash
   # Fast frontend/partition probe (no AIE binary) — enough to read the new
   # partition count and CpuBecause set:
   python3 "$VAI_FLAG_CONFIGURATION_SCRIPTS/compile_probe.py" <model>.onnx \
       --vitisai-config <updated_vitisai_config.json> \
       --mode capability --cache-dir <model_stem> -o compile_probe.json

   # Full board-ready compile (when validating the final result):
   python3 "$VAI_CUSTOM_OP_IMPLEMENTATION_SCRIPTS/compile.py" <model>.onnx \
       --vitisai-config <updated_vitisai_config.json>
   ```
   The fast `capability` probe reaches the same frontend/partition stage that
   emits the operation statistics and `CpuBecause` set, so it is the cheap way to
   check whether a partition boundary was removed; switch to the full
   `compile.py` before claiming a board-ready single-partition result.
2. Re-run Phase 1 on the fresh artifacts. Report the **partition-count delta**
   (e.g. `3 → 1`) and the new AIE/CPU split, and whether each previously-broken
   `CpuBecause` boundary is gone.
3. **Loop.** If more than one partition remains, take the next-largest gap entry
   and repeat Phases 2–4. Stop when the model reaches **1 partition / 100% AIE**,
   when no untried proposable flag or Quark change remains, or when the residual
   break is outside the flag/quant surface — and say which of these ended the loop.

## Output

Produce a **Partition Analysis report**:
- the operation-statistics table (matched kernels / templated graphs with dtypes
  and counts);
- the **partition count** and **AIE/CPU %** split, with the success verdict
  (1 partition / 100% AIE, or not);
- when > 1 partition: the ranked CpuBecause gap (op, node count, verbatim
  message, route) and, per entry, the proposed remediation (frontend flag with
  its catalog path + rationale, or Quark-config change), each cited to the
  compiler message it addresses;
- the **re-compilation** you ran (or propose to run) to evaluate the change, and
  the resulting partition-count delta once available.

Cite every proposal to a source the user can open (the compiler `Message`, the
flag's catalog path via `FlagSpec.path`, the doc anchor for a `vaiml_config`
field). A proposal without a citation and a reason is incomplete.
