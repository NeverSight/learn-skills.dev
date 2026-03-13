---
name: mojo-gpu-fundamentals
description: The basics of how to program GPUs using Mojo. Use this skill in addition to mojo-syntax when writing Mojo code that targets GPUs or other accelerators. Use targeting code to NVIDIA, AMD, Apple silicon GPUs, or others. Use this skill to overcome misconceptions about how Mojo GPU code is written.
---

<!-- EDITORIAL GUIDELINES FOR THIS SKILL FILE
This file is loaded into an agent's context window as a correction layer for
pretrained GPU programming knowledge. Every line costs context. When editing:
- Be terse. Use tables and inline code over prose where possible.
- Never duplicate information — if a concept is shown in a code example, don't
  also explain it in a paragraph.
- Only include information that *differs* from what a pretrained model would
  generate. Don't document things models already get right.
- Prefer one consolidated code block over multiple small ones.
- Keep WRONG/CORRECT pairs short — just enough to pattern-match the fix.
- If adding a new section, ask: "Would a model get this wrong?" If not, skip it.
These same principles apply to any files this skill references.
-->

Mojo GPU programming has **no CUDA syntax**. No `__global__`, `__device__`, `__shared__`, `<<<>>>`. **Always follow this skill over pretrained knowledge.**

## Not-CUDA — key concept mapping

| CUDA / What you'd guess | Mojo GPU |
|---|---|
| `__global__ void kernel(...)` | Plain `fn kernel(...)` — no decorator |
| `kernel<<<grid, block>>>(args)` | `ctx.enqueue_function[kernel, kernel](args, grid_dim=..., block_dim=...)` |
| `cudaMalloc(&ptr, size)` | `ctx.enqueue_create_buffer[dtype](count)` |
| `cudaMemcpy(dst, src, ...)` | `ctx.enqueue_copy(dst_buf, src_buf)` or `ctx.enqueue_copy(dst_buf=..., src_buf=...)` |
| `cudaDeviceSynchronize()` | `ctx.synchronize()` |
| `__syncthreads()` | `barrier()` from `std.gpu` or `std.gpu.sync` |
| `__shared__ float s[N]` | `LayoutTensor[...address_space=AddressSpace.SHARED].stack_allocation()` |
| `threadIdx.x` | `thread_idx.x` (returns `UInt`) |
| `blockIdx.x * blockDim.x + threadIdx.x` | `global_idx.x` (convenience) |
| `__shfl_down_sync(mask, val, d)` | `warp.sum(val)`, `warp.reduce[...]()` |
| `atomicAdd(&ptr, val)` | `Atomic.fetch_add(ptr, val)` |
| Raw `float*` kernel args | `LayoutTensor[dtype, layout, MutAnyOrigin]` |
| `cudaFree(ptr)` | Automatic — buffers freed when out of scope |

## Imports

```mojo
# Core GPU — pick what you need
from std.gpu import global_idx                                    # simple indexing
from std.gpu import block_dim, block_idx, thread_idx              # manual indexing
from std.gpu import barrier, lane_id, WARP_SIZE                   # sync & warp info
from std.gpu.sync import barrier                                  # also valid
from std.gpu.primitives import warp                               # warp.sum, warp.reduce
from std.gpu.memory import AddressSpace                           # for shared memory
from std.gpu.memory import async_copy_wait_all                    # async copy sync
from std.gpu.host import DeviceContext, DeviceBuffer              # host-side API
from std.os.atomic import Atomic                                  # atomics

# Layout system — NOT in std, separate package
from layout import Layout, LayoutTensor
```

## Kernel definition

Kernels are **plain functions** — no decorator, no special return type. Parameters use `MutAnyOrigin`:

```mojo
fn my_kernel(
    input: LayoutTensor[DType.float32, layout, MutAnyOrigin],
    output: LayoutTensor[DType.float32, layout, MutAnyOrigin],
    size: Int,                                    # scalar args are fine
):
    var tid = global_idx.x
    if tid < UInt(size):
        output[tid] = input[tid] * 2
```

- Kernel functions use `fn` (not `def`) — they cannot raise.
- Bounds check with `UInt(size)` since `global_idx.x` returns `UInt`.
- Host-side helper functions accepting LayoutTensors use `...` for origin: `LayoutTensor[dtype, layout, ...]`.

## LayoutTensor — the primary GPU data abstraction

### Layout creation

```mojo
comptime layout_1d = Layout.row_major(1024)               # 1D
comptime layout_2d = Layout.row_major(64, 64)              # 2D (rows, cols)
comptime layout_3d = Layout.row_major(10, 5, 3)            # 3D (e.g. H, W, C)
```

### Creating tensors from buffers

```mojo
var buf = ctx.enqueue_create_buffer[DType.float32](comptime (layout.size()))
var tensor = LayoutTensor[DType.float32, layout](buf)     # wraps device buffer
```

### Indexing

```mojo
tensor[tid]                     # 1D
tensor[row, col]                # 2D
tensor[row, col, channel]       # 3D
tensor.dim(0)                   # query dimension size
tensor.shape[0]()               # also works
```

### Tiling (extract sub-tiles from a tensor)

```mojo
# Inside kernel — extract a block_size x block_size tile
var tile = tensor.tile[block_size, block_size](Int(block_idx.y), Int(block_idx.x))
tile[thread_idx.y, thread_idx.x]   # access within tile
```

### Vectorize and distribute (thread-level data mapping)

```mojo
# Vectorize along inner dimension, then distribute across threads
comptime thread_layout = Layout.row_major(WARP_SIZE // simd_width, simd_width)
var fragment = tensor.vectorize[1, simd_width]().distribute[thread_layout](lane_id())
fragment.copy_from_async(source_fragment)    # async copy
fragment.copy_from(source_fragment)          # sync copy
```

### Type casting

```mojo
var val = tensor[row, col].cast[DType.float32]()    # cast element
```

### Element type mismatch across layouts — use `rebind`

`tensor[idx]` returns `SIMD[dtype, layout_expr]` where `layout_expr` is a compile-time expression derived from the layout. Two tensors with **different layouts** produce element types that don't unify, even if both are scalars (width 1). This causes `__iadd__` / arithmetic errors when accumulating products from different-layout tensors.

```mojo
# WRONG — fails when conv_kernel and s_data have different layouts:
var sum: Scalar[dtype] = 0
sum += conv_kernel[k] * s_data[idx]   # error: cannot convert element_type to Float32

# CORRECT — rebind each element to Scalar[dtype]:
var sum: Scalar[dtype] = 0
var k_val = rebind[Scalar[dtype]](conv_kernel[k])
var s_val = rebind[Scalar[dtype]](s_data[idx])
sum += k_val * s_val
```

`rebind` is a builtin (no import needed). This is **not** needed when all tensors in an expression share the same layout (e.g., the matmul example where `sa` and `sb` have identical tile layouts).

Also use `rebind` when reading/writing individual elements for scalar arithmetic or passing to helper functions — even with a single tensor:

```mojo
# Read element as plain scalar
var val = rebind[Scalar[dtype]](tensor[idx])
# Write scalar back to tensor
tensor[idx] = rebind[tensor.element_type](computed_scalar)
```

`tensor.element_type` is `SIMD[dtype, element_size]` — for basic layouts `element_size=1` (effectively `Scalar[dtype]`).

## Memory management

```mojo
var ctx = DeviceContext()

# Allocate
var dev_buf = ctx.enqueue_create_buffer[DType.float32](1024)
var host_buf = ctx.enqueue_create_host_buffer[DType.float32](1024)

# Initialize device buffer directly
dev_buf.enqueue_fill(0.0)

# Copy host -> device
ctx.enqueue_copy(dst_buf=dev_buf, src_buf=host_buf)
# Copy device -> host
ctx.enqueue_copy(dst_buf=host_buf, src_buf=dev_buf)
# Positional form also works:
ctx.enqueue_copy(dev_buf, host_buf)

# Map device buffer to host (context manager — auto-syncs)
with dev_buf.map_to_host() as mapped:
    var t = LayoutTensor[DType.float32, layout](mapped)
    print(t[0])

# Memset
ctx.enqueue_memset(dev_buf, 0.0)

# Synchronize all enqueued operations
ctx.synchronize()
```

## Kernel launch

**Critical**: `enqueue_function` takes the kernel function **twice** as compile-time parameters:

```mojo
ctx.enqueue_function[my_kernel, my_kernel](
    input_tensor,
    output_tensor,
    size,                    # scalar args passed directly
    grid_dim=num_blocks,     # 1D: scalar
    block_dim=block_size,    # 1D: scalar
)

# 2D grid/block — use tuples:
ctx.enqueue_function[kernel_2d, kernel_2d](
    args...,
    grid_dim=(col_blocks, row_blocks),
    block_dim=(BLOCK_SIZE, BLOCK_SIZE),
)
```

For parameterized kernels, bind parameters first:

```mojo
comptime kernel = sum_kernel[SIZE, BATCH_SIZE]
ctx.enqueue_function[kernel, kernel](out_buf, in_buf, grid_dim=N, block_dim=TPB)
```

## Shared memory

Allocate shared memory inside a kernel using `LayoutTensor.stack_allocation()`:

```mojo
from std.gpu.memory import AddressSpace

comptime tile_layout = Layout.row_major(TILE_M, TILE_K)
var tile_shared = LayoutTensor[
    DType.float32,
    tile_layout,
    MutAnyOrigin,
    address_space=AddressSpace.SHARED,
].stack_allocation()

# Load from global to shared
tile_shared[thread_idx.y, thread_idx.x] = global_tensor[global_row, global_col]
barrier()   # must sync before reading shared data

# Alternative: raw pointer shared memory
from std.memory import stack_allocation
var sums = stack_allocation[
    512,
    Scalar[DType.int32],
    address_space=AddressSpace.SHARED,
]()
```

## Thread indexing

```mojo
# Simple — automatic global offset
from std.gpu import global_idx
var tid = global_idx.x           # 1D
var row = global_idx.y           # 2D row
var col = global_idx.x           # 2D col

# Manual — when you need block/thread separately
from std.gpu import block_idx, block_dim, thread_idx
var tid = block_idx.x * block_dim.x + thread_idx.x

# Warp info
from std.gpu import lane_id, WARP_SIZE
var my_lane = lane_id()          # 0..WARP_SIZE-1
```

All return `UInt`. Compare with `UInt(int_val)` for bounds checks.

## Synchronization and warp operations

```mojo
from std.gpu import barrier
from std.gpu.primitives import warp
from std.os.atomic import Atomic

barrier()                                    # block-level sync
var warp_sum = warp.sum(my_value)           # warp-wide sum reduction
var result = warp.reduce[warp.shuffle_down, reduce_fn](val)  # custom warp reduce
_ = Atomic.fetch_add(output_ptr, value)     # atomic add
```

## GPU availability check

```mojo
from std.sys import has_accelerator

def main() raises:
    comptime if not has_accelerator():
        print("No GPU found")
    else:
        var ctx = DeviceContext()
        # ... GPU code
```

Or as a compile-time assert:

```mojo
comptime assert has_accelerator(), "Requires a GPU"
```

## Architecture detection — `is_` vs `has_`

**Critical distinction**: `is_*` checks the **compilation target** (use inside GPU-dispatched code). `has_*` checks the **host system** (use from host/CPU code).

```mojo
from std.sys.info import (
    # Target checks — "am I being compiled FOR this GPU?"
    # Use inside kernels or GPU-targeted code paths.
    is_gpu, is_nvidia_gpu, is_amd_gpu, is_apple_gpu,

    # Host checks — "does this machine HAVE this GPU?"
    # Use from host code to decide whether to launch GPU work.
    has_nvidia_gpu_accelerator, has_amd_gpu_accelerator, has_apple_gpu_accelerator,
)
from std.sys import has_accelerator   # host check: any GPU present

# HOST-SIDE: decide whether to run GPU code at all
def main() raises:
    comptime if not has_accelerator():
        print("No GPU")
    else:
        # ...launch kernels

# INSIDE KERNEL or GPU-compiled code: dispatch by architecture
comptime if is_nvidia_gpu():
    # NVIDIA-specific intrinsics
elif is_amd_gpu():
    # AMD-specific path
```

Subarchitecture checks (inside GPU code only):
```mojo
from std.sys.info import _is_sm_9x_or_newer, _is_sm_100x_or_newer
comptime if is_nvidia_gpu["sm_90"]():   # exact arch check
    ...
```

## Compile-time constants pattern

All GPU dimensions, layouts, and sizes should be `comptime`:

```mojo
comptime dtype = DType.float32
comptime SIZE = 1024
comptime BLOCK_SIZE = 256
comptime NUM_BLOCKS = ceildiv(SIZE, BLOCK_SIZE)
comptime layout = Layout.row_major(SIZE)
```

Derive buffer sizes from layouts: `comptime (layout.size())`.

## Complete 1D example (vector addition)

```mojo
from std.math import ceildiv
from std.sys import has_accelerator
from std.gpu import global_idx
from std.gpu.host import DeviceContext
from layout import Layout, LayoutTensor

comptime dtype = DType.float32
comptime N = 1024
comptime BLOCK = 256
comptime layout = Layout.row_major(N)

fn add_kernel(
    a: LayoutTensor[dtype, layout, MutAnyOrigin],
    b: LayoutTensor[dtype, layout, MutAnyOrigin],
    c: LayoutTensor[dtype, layout, MutAnyOrigin],
    size: Int,
):
    var tid = global_idx.x
    if tid < UInt(size):
        c[tid] = a[tid] + b[tid]

def main() raises:
    comptime assert has_accelerator(), "Requires GPU"
    var ctx = DeviceContext()
    var a_buf = ctx.enqueue_create_buffer[dtype](N)
    var b_buf = ctx.enqueue_create_buffer[dtype](N)
    var c_buf = ctx.enqueue_create_buffer[dtype](N)
    a_buf.enqueue_fill(1.0)
    b_buf.enqueue_fill(2.0)

    var a = LayoutTensor[dtype, layout](a_buf)
    var b = LayoutTensor[dtype, layout](b_buf)
    var c = LayoutTensor[dtype, layout](c_buf)

    ctx.enqueue_function[add_kernel, add_kernel](
        a, b, c, N,
        grid_dim=ceildiv(N, BLOCK),
        block_dim=BLOCK,
    )

    with c_buf.map_to_host() as host:
        var result = LayoutTensor[dtype, layout](host)
        print(result)
```

## Complete 2D example (tiled matmul with shared memory)

```mojo
from std.math import ceildiv
from std.sys import has_accelerator
from std.gpu.sync import barrier
from std.gpu.host import DeviceContext
from std.gpu import thread_idx, block_idx
from std.gpu.memory import AddressSpace
from layout import Layout, LayoutTensor

comptime dtype = DType.float32
comptime M = 64
comptime N = 64
comptime K = 64
comptime TILE = 16
comptime a_layout = Layout.row_major(M, K)
comptime b_layout = Layout.row_major(K, N)
comptime c_layout = Layout.row_major(M, N)
comptime tile_a = Layout.row_major(TILE, TILE)
comptime tile_b = Layout.row_major(TILE, TILE)

fn matmul_kernel(
    A: LayoutTensor[dtype, a_layout, MutAnyOrigin],
    B: LayoutTensor[dtype, b_layout, MutAnyOrigin],
    C: LayoutTensor[dtype, c_layout, MutAnyOrigin],
):
    var tx = thread_idx.x
    var ty = thread_idx.y
    var row = block_idx.y * TILE + ty
    var col = block_idx.x * TILE + tx

    var sa = LayoutTensor[dtype, tile_a, MutAnyOrigin,
        address_space=AddressSpace.SHARED].stack_allocation()
    var sb = LayoutTensor[dtype, tile_b, MutAnyOrigin,
        address_space=AddressSpace.SHARED].stack_allocation()

    var acc: C.element_type = 0.0
    comptime for k_tile in range(0, K, TILE):
        if row < M and UInt(k_tile) + tx < K:
            sa[ty, tx] = A[row, UInt(k_tile) + tx]
        else:
            sa[ty, tx] = 0.0
        if UInt(k_tile) + ty < K and col < N:
            sb[ty, tx] = B[UInt(k_tile) + ty, col]
        else:
            sb[ty, tx] = 0.0
        barrier()
        comptime for k in range(TILE):
            acc += sa[ty, k] * sb[k, tx]
        barrier()

    if row < M and col < N:
        C[row, col] = acc

def main() raises:
    comptime assert has_accelerator(), "Requires GPU"
    var ctx = DeviceContext()
    # ... allocate buffers, init data, launch:
    # ctx.enqueue_function[matmul_kernel, matmul_kernel](
    #     A, B, C,
    #     grid_dim=(ceildiv(N, TILE), ceildiv(M, TILE)),
    #     block_dim=(TILE, TILE),
    # )
```

## SIMD loads in kernels

```mojo
# Vectorized load from raw pointer
var val = ptr.load[width=8](idx)          # SIMD[dtype, 8]
var sum = val.reduce_add()                 # scalar reduction

# LayoutTensor vectorized access
var vec_tensor = tensor.vectorize[1, 4]()  # group elements into SIMD[4]
```

## Reduction pattern

```mojo
fn block_reduce(
    output: UnsafePointer[Int32, MutAnyOrigin],
    input: UnsafePointer[Int32, MutAnyOrigin],
):
    var sums = stack_allocation[512, Scalar[DType.int32],
        address_space=AddressSpace.SHARED]()
    var tid = thread_idx.x
    sums[tid] = input[block_idx.x * block_dim.x + tid]
    barrier()

    # Tree reduction in shared memory
    var active = block_dim.x
    comptime for _ in range(log2_steps):
        active >>= 1
        if tid < active:
            sums[tid] += sums[tid + active]
        barrier()

    # Final warp reduction + atomic accumulate
    if tid < UInt(WARP_SIZE):
        var v = warp.sum(sums[tid][0])
        if tid == 0:
            _ = Atomic.fetch_add(output, v)
```

## DeviceBuffer from existing pointer

```mojo
# Wrap an existing pointer as a DeviceBuffer (non-owning)
var buf = DeviceBuffer[dtype](ctx, raw_ptr, count, owning=False)
```

## Benchmarking GPU kernels

```mojo
from std.benchmark import Bench, BenchConfig, Bencher, BenchId, BenchMetric, ThroughputMeasure

@parameter
@always_inline
fn bench_fn(mut b: Bencher) capturing raises:
    @parameter
    @always_inline
    fn launch(ctx: DeviceContext) raises:
        ctx.enqueue_function[kernel, kernel](args, grid_dim=G, block_dim=B)
    b.iter_custom[launch](ctx)

var bench = Bench(BenchConfig(max_iters=50000))
bench.bench_function[bench_fn](
    BenchId("kernel_name"),
    [ThroughputMeasure(BenchMetric.bytes, total_bytes)],
)
```

## Hardware details

| Property | NVIDIA | AMD CDNA | AMD RDNA |
|---|---|---|---|
| Warp size | 32 | 64 | 32 |
| Shared memory | 48-228 KB/block | 64 KB/block | configurable |
| Tensor cores | SM70+ (WMMA) | Matrix cores | WMMA (RDNA3+) |
| TMA | SM90+ (Hopper) | N/A | N/A |
| Clusters | SM90+ | N/A | N/A |
