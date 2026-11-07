---
name: vai-aie-kernel-development
license: Apache-2.0 WITH LLVM-exception
compatibility: Requires VitisAI 6.3+
metadata:
  version: 6.3.0
  stage: beta
description: Comprehensive AIE kernel development guide covering architecture-level
  optimization techniques, result analysis, and compiler-independent patterns. Covers
  loop splitting for register pressure, in-place updates, signedness optimization,
  VLIW slot awareness, result analysis (disassembly, DM maps, calltree, profiling),
  and general kernel coding practices. Ships aie_api_references.md, the detailed AIE
  API primitive catalog (per-dtype support, vectorization, accumulator types, math-pattern
  to API lookup). For Peano compiler-specific pragmas, loop hints, software pipelining
  details, and optimization remarks, see the vai-aie-compiler-oriented-optimizations
  skill.
---
<!--- Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.--->

# AIE Kernel Development Guide

## Access command

This skill must always be accessed through the worker, never in a different way.
Allowed worker: `vai-custom-op-worker`.

## Description

This guide covers compiler-independent techniques and analysis methods for
writing high-performance AIE kernels. It applies regardless of whether
you are using Peano or any other AIE compiler backend.

For Peano-specific compiler pragmas, loop hints, software pipelining
(pre-RA vs post-RA), loop versioning, and reading optimization remarks,
see the **vai-aie-compiler-oriented-optimizations** skill.


## 1. Architecture Fundamentals

AIE cores are VLIW (Very Long Instruction Word) processors. Key properties:

- **VLIW slots**: Each cycle can issue multiple operations in parallel
  (load, store, scalar, vector, etc.) if they fit into different slots.
  Filling more slots per cycle = higher throughput.
- **In-order execution**: No out-of-order engine. The compiler must
  statically schedule instructions to hide latencies.
- **Zero-overhead loops (ZOL)**: Hardware loop support that eliminates
  branch overhead. The compiler converts eligible loops automatically.
- **Multiple memory banks**: Data memory (DM) is banked (A, B, C, D).
  Two loads or a load and a store can execute simultaneously if they
  access different banks.
- **Software pipelining**: The most important optimization for inner
  loops. It overlaps consecutive iterations so that instructions from
  multiple iterations are in-flight simultaneously.

The compiler needs developer hints (restrict, bank annotations, trip
counts, pipelining directives) to produce optimal schedules.


## 2. Vectorization and the AIE API

Two techniques compound to give most of the speedup on AIE cores:

- **Vectorization** uses the vector datapath that scalar code leaves idle.
  Speedup scales roughly with the vector width for the chosen element type
  (e.g. 32-way for int8 mul on AIE-ML), provided the loop is also software
  pipelined and not memory bound.
- **Library calls** delegate to implementations written by the AIE API
  authors. They are vector-aware, tuned per architecture (AIE1/AIE2/AIE-ML),
  and well tested across element types and accumulator widths.

Prefer the AIE API over hand-rolled intrinsics: it gives you vectorization
and portability across AIE variants in one call, and the compiler schedules
it better than ad-hoc intrinsic sequences. Only fall back to raw intrinsics
when profiling shows the API call is the bottleneck and a custom schedule
can demonstrably do better.

**Start from the bundled reference.** Before writing or optimizing any kernel
math, read [aie_api_references.md](aie_api_references.md) next to this file: it
catalogs the AIE API primitives (core, fused/advanced, data movement/shuffle,
`aie::mmul`) with their dtype support, lane width, and accumulator type, plus a
math-pattern -> API table. Use it to pick the idiomatic fused primitive instead
of hand-rolling a LUT or polynomial.

For anything it does not cover, read the headers themselves -- its
["discover from the headers"](aie_api_references.md#if-its-not-here-discover-from-the-headers)
section is the single source of truth for resolving the header directory out of
the active environment and for which header answers which question. One rule
worth repeating here: scope every search to that directory, because a `find` or
`grep -r` from the env root or prefix walks a tree large enough to stall.

## 3. VLIW Slot Awareness

Understanding which instructions occupy which VLIW slots is essential
for identifying parallelism opportunities and slot conflicts.

### VLIW Slot Overview

A typical AIE core exposes parallel issue slots that can be roughly grouped
as follows. Consult the architecture reference for your specific target
device for the exact slot table and instruction set.

| Slot     | Role     | Typical Instructions                                  |
|----------|----------|-------------------------------------------------------|
| Load A   | Load     | Vector and scalar loads, pointer-add updates          |
| Load B   | Load     | Second load port, unpack/move                         |
| Store    | Store    | Vector store, pack, shift-round-saturate, convert     |
| Scalar   | Scalar   | Integer ALU, compare, branch, lock acquire/release    |
| Move     | Move     | Vector shuffle/select/shift, accumulator move         |
| Move imm | Move imm | Immediate moves, immediate branches                   |
| Vec MAC  | Vec MAC  | Vector multiply-accumulate, add, subtract, negate     |
| Mat MAC  | Mat MAC  | Matrix multiply-accumulate (integer / float variants) |

### Conflict Detection

If two instructions in the same loop body need the same slot, they
cannot execute in the same cycle. This increases the minimum initiation
interval (MII).

Example: Two VLD instructions both need slot A or B. If the loop body
has 4 VLD operations, and only slots A and B can issue loads, the
resource MII is at least 2.

### Common AI/ML Operation Mappings

| Operation     | Instruction Sequence                     |
|--------------|------------------------------------------|
| Softmax      | VEXP2 + VADDR + VINV                     |
| ReLU         | VMAX_LT                                  |
| MatMul       | MMAC (supports sparse)                    |
| Convolution  | VMOV.conv + MMAC                          |
| Quantization | VSRS + VCLAMP                             |


## 4. Register Pressure: Loop Splitting and Small Temporaries

When a loop is under register pressure, the compiler wastes instructions
on spill-to-stack and reload within the inner loop. This inflates II
and reduces throughput.

### Detection
- Look for stack spills in the generated assembly (`.lst` file)
- Stack spill instructions appear as stores to DM addresses in the
  system region
- If the inner loop has more vector variables alive than physical
  registers, spills are inevitable

### Solution: Split the Loop

Split the loop into two passes, using DM for intermediate results:

```cpp
// BEFORE: single loop with high register pressure
for (int i = 0; i < N; i++) {
    // load input, load weights, compute MAC, apply activation,
    // quantize, store -- too many live registers
}

// AFTER: two loops, each with lower pressure
// Pass 1: compute and store intermediate
for (int i = 0; i < N; i++) {
    auto result = compute(input[i], weights[i]);
    intermediate[i] = result;  // DM write
}
// Pass 2: post-process from intermediate
for (int i = 0; i < N; i++) {
    auto val = intermediate[i];  // DM read
    output[i] = activate_and_quantize(val);
}
```

Each resulting loop has fewer live registers and can be pipelined more
effectively. The DM read/write cost is typically cheaper than the
spill/reload overhead in a bloated single loop.

### Solution: Keep Temporaries Small (per-row / 8-lane)

The other lever on the same problem: instead of restructuring the loop, shrink
how much state is live inside it. A kernel that holds a whole tile in registers
spills; one that walks the tile a row at a time does not.

```cpp
// HEAVY: a full 64-lane tile stays live across the computation
aie::vector<bfloat16, 64> tile = aie::load_v<64>(in);
tile = do_stuff(tile);
aie::store_v(out, tile);

// LIGHT: one 8-lane row live at a time (small live set)
for (int r = 0; r < 8; ++r) {
    aie::vector<bfloat16, 8> row = aie::load_v<8>(in + r * 8);
    row = do_stuff(row);
    aie::store_v(out + r * 8, row);
}
```

The same idea applies to everything else the kernel keeps around: prefer named
locals over addressable vector arrays (indexing forces the compiler to give the
array a DM home), keep reductions in registers, and drop dynamic/temporary
allocations and static scratch/LUTs, which consume heap.

**Reach for this only when you actually need to cut stack/register usage.**
Narrower vectors mean more iterations and less work per instruction, so it trades
throughput for pressure relief. Confirm from the `.lst` (spills) or a stack
overflow that pressure is the real problem before shrinking anything.


## 5. In-Place Updates

When a kernel must read and write the same buffer (in-place operation),
use two separate pointers with different bank hints and `__restrict`
to allow dense inner loops:

```cpp
// BAD: single pointer for read-modify-write -- compiler assumes alias
for (int i = 0; i < N; i++) {
    buf[i] = process(buf[i]);
}

// GOOD: two pointers with bank hints and restrict
void inplace_core(
    dtype __aie_dm_resource_a *__restrict read_ptr,
    dtype __aie_dm_resource_b *__restrict write_ptr,
    int count) {

    for (int i = 0; i < count; i++) {
        auto val = aie::load_v<VEC_LEN>(read_ptr);
        read_ptr = byte_incr(read_ptr, VEC_BYTES);
        auto result = process(val);
        store_v(write_ptr, result);
        write_ptr = byte_incr(write_ptr, VEC_BYTES);
    }
}

// Call with same base address, different bank hints
inplace_core(
    (dtype __aie_dm_resource_a *__restrict)buf,
    (dtype __aie_dm_resource_b *__restrict)buf,
    N);
```

The "fake" bank hints tell the compiler to schedule the load and
store in parallel (different bank ports), even though they point to
the same physical memory. Combined with `__restrict`, this enables
full pipelining.


## 6. Signedness Optimization

When both signed and unsigned integer types need the same processing,
avoid duplicating the kernel. Use a single signed type signature with
runtime signedness control:

```cpp
// GOOD: single function handles both int8 and uint8
void both_signedness(
    int8_t *__restrict ifm,
    int8_t *__restrict ofm,
    bool signed_fm) {

    // Use aie::to_fixed_sign() to handle signedness at runtime
    auto vec = aie::load_v<VEC_LEN>(ifm);
    auto result = aie::to_fixed_sign(vec, /* sign_vector */, shift);
    // ... process ...
}
```

This halves program memory (PM) usage compared to maintaining separate
signed/unsigned kernel variants.


## 7. Restrict Pointers

The `__restrict` qualifier tells the compiler that a pointer does not
alias any other pointer in scope. This is the single most impactful
optimization annotation for AIE kernels.

### Key Rules

- **The function containing the hot loop must receive `__restrict`
  pointers as parameters**, not buffer references. The `.data()`
  extraction and restrict cast belong in the wrapper that calls it.
- Never cast away `__restrict` when applying bank annotations --
  combine them in the same declaration.
- Apply `__restrict` to all function pointer parameters that don't
  alias each other, including parameter struct references.

### Pattern: Inline Wrapper + Noinline Core

```cpp
// Public API: INLINE, does type dispatch and pointer casting
template <typename dtype>
INLINE void my_kernel(
    adf::input_buffer_conf<dtype, ...> &__restrict ifm,
    adf::output_buffer_conf<dtype, ...> &__restrict ofm,
    params_t &params) {
    my_kernel_core<dtype>(
        (dtype __aie_dm_resource_a *__restrict)ifm.data(),
        (dtype __aie_dm_resource_b *__restrict)ofm.data(),
        params);
}

// Core function: NOINLINE, receives properly qualified pointers
template <typename dtype>
__attribute__((noinline)) void my_kernel_core(
    dtype __aie_dm_resource_a *__restrict ifm_ptr,
    dtype __aie_dm_resource_b *__restrict ofm_ptr,
    params_t &__restrict params) {
    // Hot loop here -- compiler sees full restrict + bank info
}
```


## 8. DM Bank Annotations

AIE data memory is banked. Annotating pointers with their bank
assignment enables simultaneous memory operations in the same VLIW
bundle.

### Syntax
```cpp
dtype __aie_dm_resource_a *ptr;    // Bank A
dtype __aie_dm_resource_b *ptr;    // Bank B
dtype __aie_dm_resource_c *ptr;    // Bank C
dtype __aie_dm_resource_d *ptr;    // Bank D
```

### Typical Assignments

| Data         | Bank | Rationale                                    |
|-------------|------|----------------------------------------------|
| Input (IFM) | A    | Loads via load port A                        |
| Weights     | B    | Separate bank enables parallel loads         |
| Output (OFM)| B    | Stores via store port B, parallel with A     |
| Bias / TDM  | C/D  | Secondary data, flexible placement           |

### Same-Bank Conflict

If two pointers loaded in the same iteration are on the same bank,
loads serialize. Always put concurrently accessed data on different
banks.


## 9. Vector Load/Store Alignment

Vector loads and stores require address alignment to the vector width.
Misaligned accesses cause undefined behavior or hardware exceptions.

| Vector Width | Alignment Required |
|--------------|-------------------|
| 256-bit      | 32-byte aligned   |
| 512-bit      | 64-byte aligned   |
| 1024-bit     | 128-byte aligned  |

For unaligned streaming access, use FIFO intrinsics
(`fifo_ld_pop` / `fifo_st_push`) which handle alignment internally.


## 10. Sub-32-Bit Load/Store Limitations

Loads and stores narrower than 32 bits (`int8`, `int16`, `bfloat16`
scalars) trigger hardware read-modify-write, making them significantly
more expensive than vector-width operations.

**Rule**: Always use vector-width loads and stores (`aie::load_v`,
`store_v`) in performance-critical loops. Avoid scalar sub-word
memory operations inside hot loops.


## 11. Result Analysis

### Compile Artifacts

In `Work/aie/{X}_{Y}/Release/` (single core tests typically use core
(0,0)):

| File               | Contents                                          |
|-------------------|---------------------------------------------------|
| `{X}_{Y}.lst`     | Disassembled assembly -- inspect for slot usage,   |
|                   | spills, and instruction count per loop             |
| `{X}_{Y}.map`     | Compile-time DM allocation for stack/heap          |
| `{X}_{Y}.calltree`| Function call tree with per-function summary       |
|                   | (instruction count, stack depth, PM size)          |

### Profiling Results

The file `profile_instr_{x}_{y}.xml` contains the aiesim profiling
result from the Instruction Set Simulator (ISS).

**Important**: The `{x}_{y}` coordinates in profile files count
differently than `Work/aie/` folders -- they include the mem tile
row, so the most typical value is `(0, 1)` not `(0, 0)`.

### Using the Calltree for QoR Analysis

The `.calltree` file provides per-function metrics that are critical
for QoR (Quality of Results) analysis:

- **Column 2 (`stack_desc`)**: Stack usage per function -- take the
  maximum across multi-core runs
- **Column 6 (`func_desc`)**: Program memory (PM) size per function
  -- take the maximum across multi-core runs

These values should be compared against metadata expectations. Automate the
extraction with a small script that parses the `.calltree` columns when
running this analysis at scale.

### Using the .map File for Heap Analysis

The `.map` file contains the DMb memory map section. Parse it to
determine heap usage by summing referenced symbols, rounded to
4-byte alignment. Take the maximum across multi-core runs.

### Quick Diagnosis from Artifacts

| Symptom                     | Check                                | Likely Cause                    |
|----------------------------|--------------------------------------|---------------------------------|
| High instruction count     | `.lst` inner loop body               | Spills, slot conflicts, or      |
|                            |                                      | unoptimized conversion chains   |
| Large stack size           | `.calltree` column 2                 | Too many live variables,        |
|                            |                                      | split the loop                  |
| PM bloat                   | `.calltree` column 6                 | Inlined code, loop versioning   |
|                            |                                      | duplication                     |
| Cycle count >> expected    | `profile_instr` vs theoretical II    | Memory stalls, lock contention, |
|                            |                                      | DMA latency                     |


## 12. Innermost Loop Bound Factors

Three factors can bound innermost loop optimization:

1. **Slot conflicts**: Prevents VLIW bundling. Check the VLIW slot
   table (Section 3) to identify which instructions compete for the
   same slot.

2. **Register pressure**: Check the number of registers used, taking
   instruction latency into account. Stack spills in the `.lst` file
   indicate register overuse. Consider loop splitting (Section 4).

3. **Insufficient loop range**: The loop range annotation guarantees
   the compiler can safely pipeline. Without it, the compiler must
   be conservative about prologue/epilogue peeling.


## 13. AIE Core Coding Rules

These rules apply to all AIE kernel code regardless of compiler:

- AIE intrinsics and AIE API (`aie::` calls) often hold both unsigned
  and signed vectors in the same container type (e.g., `v32int16` for
  both `int16` and `uint16`), with signedness controlled by an extra
  argument. Do not expand such abstractions.
- `printf` from `stdio.h` can be used for debugging, but it can cause
  compilation failure in innermost loops. Use it outside hot loops or
  guard with `#ifdef __X86SIM__`.
- Use the AIE API (`aie::` namespace) instead of raw intrinsics when
  possible -- it is more portable and readable.
- Avoid `me_primitive` calls.


## 14. Related Skills

- **vai-aie-compiler-oriented-optimizations** -- Peano-specific pragmas
  (`AIE_PREPARE_FOR_POSTPIPELINING`, `AIE_LOOP_RANGE`, `AIE_LOOP_HINT`,
  etc.), software pipelining details (pre-RA vs post-RA), loop
  versioning (`VERSIONED_LOOP`), and reading optimization remarks.
  This guide is authored and maintained by the AIE compiler developers
  and serves as the **source of truth** for all compiler-oriented
  optimization techniques. It should not be overlooked when optimizing
  kernel performance -- always consult it alongside this skill.
