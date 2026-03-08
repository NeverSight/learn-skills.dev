---
name: cuda-kernel-refine
description: Iterative CUDA kernel optimization using NVIDIA profiling tools (nsys, ncu). Use when optimizing kernels, improving throughput, reducing bandwidth, analyzing roofline, comparing benchmarks, or investigating register pressure and occupancy.
---

# CUDA Kernel Refinement Loop

**One change per cycle:** baseline → profile → classify → optimize → verify → compare → loop. Multiple simultaneous changes make it impossible to attribute improvement. Revert on regression.

## 1. Establish Baseline

Discover the project's benchmark infrastructure before running anything:

1. Check `Makefile` for bench/profile targets (`make bench`, `make profile`, etc.)
2. Check for benchmark binaries (`cargo bench`, `pytest-benchmark`, a custom `e2e_bench` binary)
3. Look at CI scripts or README for the canonical benchmark invocation
4. If no benchmark exists, write a minimal one that exercises the hot path with measurable output

Run with enough iterations for stable results — coefficient of variation <5%.

```bash
# Save baseline (JSON or structured output preferred for diff later)
./benchmark --iterations 5 --json-output /tmp/bench-baseline.json
```

Record: primary metric (tok/s, GFLOPS, GB/s, or latency ms), stddev, and workload parameters (input size, batch size, context depth). You need all three for meaningful comparison later.

## 2. Profile with nsys

### Capture

```bash
nsys profile --stats=true -o /tmp/nsys-profile ./app [args]
```

### Quick look (JSON)

```bash
# Kernel timing summary — sort by Time(%) to find hotspot
nsys stats -r cuda_gpu_kern_sum --format json /tmp/nsys-profile.nsys-rep

# CUDA API calls (spot synchronization overhead, excessive cudaMalloc)
nsys stats -r cuda_api_sum --format json /tmp/nsys-profile.nsys-rep

# Memory operations by size (spot unnecessary small D2H/H2D transfers)
nsys stats -r cuda_gpu_mem_size_sum --format json /tmp/nsys-profile.nsys-rep
```

### Deep analysis (SQLite — the real power tool)

For custom queries, export to SQLite and use SQL directly. This is far more powerful than JSON for kernel-level analysis.

```bash
# Export nsys trace to SQLite
nsys export --type sqlite /tmp/nsys-profile.nsys-rep
# Creates /tmp/nsys-profile.sqlite

# Top kernels by time with full names
sqlite3 -header -column /tmp/nsys-profile.sqlite \
  "SELECT
     printf('%.1f%%', 100.0*sum(k.end-k.start)/(SELECT sum(end-start) FROM CUPTI_ACTIVITY_KIND_KERNEL)) as pct,
     count(*) as calls,
     printf('%.1f', sum(k.end-k.start)/1e6) as total_ms,
     printf('%.1f', avg(k.end-k.start)/1e3) as avg_us,
     s.value as kernel
   FROM CUPTI_ACTIVITY_KIND_KERNEL k
   JOIN StringIds s ON k.shortName = s.id
   GROUP BY s.value
   ORDER BY sum(k.end-k.start) DESC
   LIMIT 20"

# Per-token analysis (for inference: normalize by decode_tokens)
sqlite3 -header -column /tmp/nsys-profile.sqlite \
  "SELECT
     printf('%.0f', count(*) * 1.0 / <DECODE_TOKENS>) as 'launches/tok',
     printf('%.1f', sum(end-start)/1e6/<DECODE_TOKENS>) as 'ms/tok',
     printf('%.1f', avg(end-start)/1e3) as 'us/launch'
   FROM CUPTI_ACTIVITY_KIND_KERNEL"

# Kernel launch configs (grid, block, registers) — find dimension mismatches
sqlite3 -header -column /tmp/nsys-profile.sqlite \
  "SELECT s.value as kernel, k.gridX, k.gridY, k.gridZ,
     k.blockX, k.blockY, k.blockZ, k.registersPerThread as regs,
     count(*) as launches, printf('%.1f', avg(k.end-k.start)/1e3) as avg_us
   FROM CUPTI_ACTIVITY_KIND_KERNEL k
   JOIN StringIds s ON k.shortName = s.id
   GROUP BY s.value, k.gridX, k.gridY, k.gridZ, k.blockX, k.blockY, k.blockZ
   ORDER BY sum(k.end-k.start) DESC LIMIT 20"
```

Replace `<DECODE_TOKENS>` with the number of tokens generated in the trace.

### Interpret the profile

- **High `Instances` + moderate `Avg`** → per-layer kernel, fusion opportunity
- **Low `Instances` + high `Avg`** → single expensive kernel, optimize internals
- **Many small kernels** → launch overhead ("death by a thousand cuts"), count launches/token to quantify
- **High `cudaMalloc` count in API summary** → framework allocator overhead, consider memory pools

## 3. Check Register Usage

```bash
nvcc -cubin -arch=<target_sm> -Xptxas=-v kernel.cu -o /tmp/kernel.cubin
```

Output format:

```text
ptxas info    : Compiling entry function 'kernel_name' for 'sm_121a'
ptxas info    : Function properties for kernel_name
    0 bytes stack frame, 0 bytes spill stores, 0 bytes spill loads
ptxas info    : Used 29 registers, used 0 barriers
```

Key signals:

| Signal                 | Meaning                                   | Action                                       |
| ---------------------- | ----------------------------------------- | -------------------------------------------- |
| Spill stores/loads > 0 | Register pressure                         | `__launch_bounds__` or reduce live variables |
| Registers > 64         | Occupancy limited by registers            | Check ncu Occupancy section                  |
| Stack frame > 0        | Function calls or array-to-local demotion | Inline functions, use shared memory          |
| Barriers > 0           | Shared memory synchronization             | Expected with `__syncthreads()`              |

## 4. Drill Down with ncu

**Requires GPU performance counter permissions.**

```bash
# Default sections (SOL + occupancy), fast
ncu -k "kernel_regex" -c 5 ./app [args]

# Full metrics including roofline
ncu -k "kernel_regex" --set full -o /tmp/ncu-report ./app [args]

# CSV for specific metrics
ncu --csv -k "kernel_regex" --metrics \
  sm__throughput.avg.pct_of_peak_sustained_elapsed,\
  dram__throughput.avg.pct_of_peak_sustained_elapsed \
  ./app [args]
```

If you get `ERR_NVGPUCTRPERM`, performance counters are restricted. Fix with:

```bash
# Option A: run ncu with sudo
sudo ncu -k "kernel_regex" -c 5 ./app [args]

# Option B: kernel module parameter (persistent, requires reboot)
sudo sh -c 'echo "options nvidia NVreg_RestrictProfilingToAdminUsers=0" > /etc/modprobe.d/ncu-permissions.conf'
```

Section sets (choose based on what you need):

- **Default** (`SpeedOfLight`, `Occupancy`) — fast, answers "is this compute or memory bound?"
- **`--set detailed`** — adds instruction mix, memory workload breakdown, warp scheduling. Use when default sections show a bottleneck but don't explain why.
- **`--set full`** — adds roofline charts. 10-50x slower. Only use when you need the visual roofline or are writing up an analysis.

## 5. Classify Bottleneck

From ncu `SpeedOfLight` section (or infer from kernel type if ncu unavailable):

| SM SOL %    | Memory SOL % | Classification     | Optimization Direction                |
| ----------- | ------------ | ------------------ | ------------------------------------- |
| Low         | High (>60%)  | **Memory-bound**   | Reduce traffic, wider loads, fuse ops |
| High (>60%) | Low          | **Compute-bound**  | Fast math, ILP, tensor cores          |
| Low         | Low          | **Latency-bound**  | Occupancy, reduce sync, overlap       |
| High        | High         | **Well-optimized** | Algorithmic changes or accept         |

### Bandwidth utilization (memory-bound kernels)

For inference workloads, compute bandwidth utilization directly — this is more actionable than abstract roofline:

```text
data_per_step = weight_bytes + activation_bytes + KV_cache_bytes  (read + write)
theoretical_min_time = data_per_step / hw_bandwidth
utilization = theoretical_min_time / actual_time
```

Example: FP4 weights read 5.1 GB/token on 273 GB/s → theoretical min 18.7ms, actual 24ms → 78% utilization. The 22% gap is your optimization headroom.

### Without ncu

If no counter permissions, infer from kernel behavior:

- Elementwise ops (activation functions, normalization) → almost always memory-bound
- Reductions with few output elements (layernorm, softmax) → likely compute-bound on the reduction
- Large matmuls → compute-bound
- Many tiny kernels with low total time → latency-bound (launch overhead)

### Identify host-side bottlenecks

Not all overhead lives in GPU kernels. Check for:

- **D2H synchronization points**: search for device-to-host copies in the codebase — `cudaMemcpy(..., DeviceToHost)`, `cudaStreamSynchronize`, and framework-specific equivalents (PyTorch: `.item()`, `.cpu()`, `.numpy()`; Candle: `.to_vec1()`; CUDA C++: `cudaMemcpyAsync` with sync). Each one stalls the GPU pipeline. Count them per inference step — eliminating unnecessary D2H syncs is often the single biggest win.
- **Excessive allocations**: check `cudaMalloc` count in `nsys stats -r cuda_api_sum`. ML frameworks (Candle, PyTorch eager) often allocate fresh GPU buffers for every intermediate tensor. Hundreds of allocations per step is a sign of framework overhead.
- **CPU-side compute**: sampling, tokenization, or postprocessing running on CPU while GPU idles. Shows up as gaps between kernel launches in the nsys timeline.

## 6. Optimization Strategies

### Memory-bound

Goal: reduce bytes moved per operation.

- **Kernel fusion** (see latency-bound for prioritization): every intermediate tensor written to global memory and read back is wasted bandwidth
- **Vectorized loads**: `uint4` (128-bit) = 8 BF16 or 4 FP32 per load. Requires pointer alignment. Verify with SASS (`LDG.E.128`).
- **Shared memory reuse**: cache data accessed by multiple threads (use stride D+1 to avoid bank conflicts)
- **Reduce precision**: FP8/FP4 weights cut memory traffic 2-4x with minimal accuracy loss. Keep accumulation in FP32.

### Compute-bound

Goal: do more useful math per cycle.

- **Fast math intrinsics**: `__expf()`, `__rsqrtf()`, `__fdividef()` — lower precision but 2-4x faster than full-precision equivalents
- **Warp shuffle**: `__shfl_down_sync(0xffffffff, val, offset)` for intra-warp reductions — avoids shared memory round-trip
- **ILP**: interleave independent operations so the scheduler can hide latency. `#pragma unroll` for known-trip-count loops.
- **Tensor cores**: WMMA/MMA for matrix ops — 8-16x throughput over FP32 CUDA cores but requires specific data layouts and alignment

### Latency-bound (launch overhead)

- **Kernel fusion** — the primary remedy. Prioritize candidates by:
  1. `launches_per_step × layers` — a 3-kernel sequence in a 32-layer model eliminates 96 launches when fused
  2. Memory traffic eliminated — fusing `residual_add + rmsnorm` saves one full tensor round-trip per layer
  3. Implementation complexity — simple elementwise fusions (sigmoid×mul, silu×mul) are easy wins; attention-level fusions require careful shared memory management
- **Eliminate D2H sync points** — move computation to GPU, batch device-to-host transfers to end of step (see section 5 "host-side bottlenecks" for how to find them)
- **Increase occupancy** — `__launch_bounds__(maxThreads, minBlocks)` when ncu shows low occupancy limiting throughput

## 7. SASS Inspection (optional)

Use when profiling shows an unexplained gap between expected and actual performance, or to verify the compiler is generating what you intended (vectorized loads, no spills, etc.).

```bash
cuobjdump -sass /tmp/kernel.cubin     # SASS disassembly
nvdisasm /tmp/kernel.cubin            # SASS with control flow
```

Quick checks (you don't need to read every instruction):

- **Grep for `STL`/`LDL`** — local memory access means register spills. If present, reduce register pressure.
- **Grep for `LDG.E.128`/`STG.E.128`** — confirms vectorized 128-bit loads/stores are being generated. If you wrote `uint4` loads but see `LDG.E.32`, alignment or type issues prevented vectorization.
- **Count `BAR.SYNC`** — compare to your `__syncthreads()` count. More barriers than expected means the compiler inserted extra synchronization.

## 8. Verify Correctness

**Always verify before benchmarking.** A faster kernel that produces wrong results is not an optimization.

```bash
# Project tests
cargo test / pytest / make test

# Memory errors (out-of-bounds, leaks, misaligned access)
compute-sanitizer --tool memcheck ./app [args]

# Shared memory data races
compute-sanitizer --tool racecheck ./app [args]

# Uninitialized device memory reads
compute-sanitizer --tool initcheck ./app [args]

# Sync hazards (divergent __syncthreads)
compute-sanitizer --tool synccheck ./app [args]
```

`compute-sanitizer` has significant overhead (10-100x). Use small inputs for correctness checks, full inputs for benchmarks.

## 9. Compare Results

Run the **same benchmark** as baseline — same workload, same iteration count, same GPU state (no other processes competing for bandwidth).

```bash
./benchmark --iterations 5 --json-output /tmp/bench-after.json
```

Compare against the baseline numbers you recorded in step 1:

```text
Metric           Baseline    After       Delta
─────────────    ────────    ────────    ──────
Throughput       37.1 tok/s  39.8 tok/s  +7.3%
Stddev           ±0.4        ±0.5
Launches/token   622         478         -23%
GPU ms/token     26.2        24.1        -8.0%
```

Decision framework:

- **Delta < stddev of either run** → indistinguishable from noise. Run more iterations (10+) or use a longer workload before concluding.
- **Delta > stddev and > 3%** → real improvement, accept the change
- **Any regression in throughput** → revert, then analyze why (check if a different kernel got slower — fusion can shift pressure)

Also check for side effects:

- Peak GPU memory (fusion can increase shared memory or register usage)
- Correctness (re-run tests if not done in step 8)
- Performance at different workloads (a prefill optimization might hurt decode, or vice versa)

## Common Pitfalls

- **Grid dimension limits**: y and z max at 65535; only x supports 2^31-1. Use `blockIdx.x` for sequence/batch dimensions that can exceed 65535.
- **Shared memory bank conflicts**: 32 banks x 4 bytes. Power-of-2 column strides cause conflicts. Pad to stride D+1.
- **Divergent `__syncthreads()`**: undefined behavior. All threads in a block must reach the same barrier. Use `compute-sanitizer --tool synccheck` to detect.
- **Vectorized load alignment**: `uint4` loads require 16-byte aligned pointers. Verify alignment before using wide loads.
- **Profiling overhead**: nsys adds ~5-10% overhead, ncu adds 10-50x. Profile numbers are relative (compare before/after), not absolute production performance.
- **`__launch_bounds__` vs `--maxrregcount`**: `--maxrregcount` is per-file (all kernels); `__launch_bounds__` is per-kernel. Prefer per-kernel control.
- **Occupancy chasing**: >60% occupancy is usually sufficient. Maximizing occupancy by forcing lower register counts can cause spills that hurt more than the occupancy helps.
- **Unified memory systems** (Grace Hopper, DGX Spark): no PCIe transfer overhead, but bandwidth can be 3-7x lower than discrete GDDR7. This means batch=1 decode is almost always memory-bound — prioritize weight compression (FP8/FP4) and fusion over compute optimizations.
- **Hidden D2H syncs in hot loops**: check section 5 "host-side bottlenecks" — a single unnecessary GPU→CPU sync per layer × 32 layers = 32 pipeline stalls per step. Often the biggest win before touching any kernel code.
- **Framework allocator overhead**: eager-mode ML frameworks allocate/free GPU buffers for every intermediate tensor. At 600+ allocations per inference step, `cudaMalloc` overhead itself becomes measurable. Check `cuda_api_sum` for `cudaMalloc` call counts.
- **Fusing the wrong thing**: profile first. A kernel taking 0.1% of GPU time isn't worth fusing no matter how many launches it has. Focus on the top-3 time consumers and the top launch-count contributors.
