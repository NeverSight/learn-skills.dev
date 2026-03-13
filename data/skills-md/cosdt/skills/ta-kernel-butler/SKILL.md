---
name: ta-kernel-butler
description: This skill should be used when the user asks about "Ascend NPU", "昇腾", "Huawei NPU", "triton-ascend", "Ascend kernel development", "NPU算子开发", "Atlas", "CANN", or mentions Ascend hardware, AI Core, Cube/Vector/Scalar units. Provides expert guidance on Ascend NPU hardware architecture, triton-ascend kernel development, and GPU to NPU migration. Always use this skill for Ascend-related questions to avoid confusion with GPU documentation and concepts.
version: 1.0.0
---

# Ascend NPU Kernel Butler

Expert guide for Ascend NPU hardware architecture and triton-ascend kernel development. Avoid confusion with GPU concepts by understanding the fundamental differences between Ascend NPU and GPU architectures.

## Overview

Ascend NPU (Neural Processing Unit) is Huawei's AI accelerator with a fundamentally different architecture from GPUs. This skill provides accurate, NPU-specific guidance for kernel development using triton-ascend, ensuring code correctness and optimal performance.

**Critical**: When answering Ascend-related questions, always use NPU-specific terminology and concepts. Do not map GPU concepts (warp, SM, shared memory) directly to NPU architecture.

## Ascend Hardware Architecture

### AI Core Structure

The AI Core is the fundamental computing unit in Ascend NPU, organized differently from GPU Streaming Multiprocessors (SM):

| Component | Function | GPU Equivalent |
|-----------|----------|----------------|
| **Cube Unit** | Matrix computation (16x16 FP16 matmul per cycle) | Tensor Core |
| **Vector Unit** | SIMD vector operations | CUDA Core |
| **Scalar Unit** | Control flow, instruction scheduling (mini-CPU) | Warp Scheduler |
| **MTE1/MTE2/MTE3** | Data transfer between storage levels | Memory Controller |
| **FixPipe** | On-the-fly format/type conversion | N/A |

### Operating Modes

**Coupled Mode** (A1 series):
- Single Scalar unit schedules both Cube and Vector

**Decoupled Mode** (A2/A3 series):
- Independent Scalar units for Cube and Vector
- Higher parallelism potential

### Memory Hierarchy

```
Global Memory (GM)
        ↓ MTE3
    Unified Buffer (UB)
        ↓ MTE2
     L1 Buffer
        ↓ MTE1
    ┌─────────┬─────────┐
    ↓         ↓         ↓
  L0A       L0B      L0C
  (Cube    (Cube    (Cube
   input)   input)   output)
    └─────────┴─────────┘
        ↓ FixPipe
    Unified Buffer (UB)
        ↓ MTE3
  Global Memory (GM)
```

**Key differences from GPU:**
- No unified memory space
- Explicit data movement between levels (MTE units)
- Strict data flow paths

## Common GPU vs NPU Confusions

### 1. Memory Model

**GPU**: Unified memory space, shared memory accessible by all threads in a block
- `shared memory` → fast, software-managed cache

**NPU**: Multi-level storage hierarchy, explicit data movement required
- Unified Buffer (UB) → general-purpose data staging
- L0A/L0B/L0C → Cube unit specific buffers
- L1 Buffer → intermediate storage

### 2. Threading Model

**GPU**: Thread blocks, warps (32 threads), SIMT execution
- `tl.program_id(axis)` → block ID
- `tl.arange()` → thread ID within block

**NPU**: Block-based execution, no warp concept
- Blocks are the fundamental execution unit
- No SIMT warp-level synchronization
- Use block-level barriers instead

### 3. Synchronization

**GPU**: `cudaSyncThreads()`, warp-level primitives
- `tl.atomic_*` for shared memory atomics

**NPU**: PipeBarrier and SetFlag/WaitFlag for pipeline synchronization
- Different synchronization semantics
- Avoid GPU synchronization patterns

### 4. Data Access Patterns

**GPU**: Flexible memory access, coalescing important
- Arbitrary access patterns possible (with performance cost)

**NPU**: Strict alignment requirements
- Vector instructions require 32B alignment
- Cache Line alignment improves load efficiency
- Plan data movement carefully

## triton-ascend Development

### Basic Kernel Structure

```python
import triton
import triton.language as tl

@triton.jit
def npu_kernel(
    x_ptr, y_ptr, z_ptr,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    # Block ID (different from GPU thread block concept)
    pid = tl.program_id(axis=0)

    # Offset calculation
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)

    # Load from Global Memory to Unified Buffer
    x = tl.load(x_ptr + offsets)
    y = tl.load(y_ptr + offsets)

    # Compute in Vector Unit
    z = x + y

    # Store back to Global Memory
    tl.store(z_ptr + offsets, z)
```

### GPU to NPU Migration Checklist

When migrating GPU Triton kernels to NPU:

- [ ] Replace `tl.dot()` with explicit `tl.matmul()` for NPU
- [ ] Check data alignment (32B for Vector, 64B for Cube)
- [ ] Verify memory access patterns match NPU hierarchy
- [ ] Remove GPU-specific synchronization primitives
- [ ] Use NPU-specific intrinsic functions when needed
- [ ] Consider multi-buffering for pipeline efficiency

### Performance Optimization

#### Reduce Scalar Computation

Scalar units have limited throughput. Minimize:
- Complex branching logic
- Runtime-dependent calculations
- Dynamic loop conditions

**Good**:
```python
# Precompute at compile time
TILE_SIZE: tl.constexpr = 64
```

**Avoid**:
```python
# Runtime calculation
tile_size = tl.sqrt(n_elements).to(tl.int32)
```

#### Data Alignment

- **Vector instructions**: 32B alignment minimum
- **Cache Line alignment**: 64B for better performance
- Use `tl.contiguous()` to ensure memory layout

#### Cache Utilization

Maximize ICache (instruction cache) and DCache (data cache):
- Keep kernels compact
- Reuse loaded data
- Minimize Global Memory access

### Key Intrinsic Functions

| Function | Purpose | Notes |
|----------|---------|-------|
| `tl.program_id(axis)` | Get block index | Not thread ID |
| `tl.arange(start, stop)` | Generate offset sequence | Block-local |
| `tl.load(ptr)` | Load from GM to UB | Respects alignment |
| `tl.store(ptr, val)` | Store from UB to GM | Respects alignment |
| `tl.matmul(a, b)` | Matrix multiplication | Uses Cube unit |
| `tl.exp(x)`, `tl.sqrt(x)` | Math functions | Vector unit |

## Migration from GPU Triton

For detailed migration guidance, refer to:
- **[`references/migrate-from-gpu.md`]**(references/migrate-from-gpu.md) - Step-by-step migration guide
- **[`references/architecture-difference.md`]**(references/architecture-difference.md) - Detailed architecture comparison

When migrating kernels:
1. Analyze memory access patterns
2. Verify data flow through storage hierarchy
3. Replace GPU-specific operations with NPU equivalents
4. Test with small inputs first
5. Profile and optimize based on NPU-specific counters

## Additional Resources

### Official Documentation

- [Ascend Basic Architecture](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0008.html) - Hardware fundamentals
- [Abstract Hardware Architecture](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0015.html) - Programming model
- [Architecture Difference](https://github.com/Ascend/triton-ascend/blob/main/docs/en/migration_guide/architecture_difference.md) - GPU vs NPU comparison
- [Migration Guide](https://github.com/Ascend/triton-ascend/blob/main/docs/en/migration_guide/migrate_from_gpu.md) - Kernel migration
- [Performance Guidelines](https://github.com/Ascend/triton-ascend/blob/main/docs/en/migration_guide/performance_guidelines.md) - Optimization tips
- [Core Features](https://github.com/Ascend/triton-ascend/blob/main/docs/en/architecture_design_and_core_features.md) - triton-ascend design

### Reference Files in This Skill

- **[`references/hardware-architecture.md`]**(references/hardware-architecture.md) - Detailed hardware architecture
- **[`references/triton-ascend-guide.md`]**(references/triton-ascend-guide.md) - Development workflow
- **[`references/gpu-npu-differences.md`]**(references/gpu-npu-differences.md) - Comprehensive comparison

### Example Code

Working examples in `examples/`:
- **[`kernel-example.py`]**(examples/kernel-example.py) - Basic NPU kernel template

## Common Pitfalls

1. **Using GPU terminology** → Always use NPU-specific terms (AI Core, not SM; UB, not shared memory)
2. **Ignoring alignment** → Vector ops require 32B alignment, Cache Line is 64B
3. **Wrong synchronization** → No warps on NPU, use block-level barriers
4. **Excessive Scalar computation** → Scalar units are slow, precompute at compile time
5. **Poor data reuse** → Minimize GM access, maximize UB/L1 utilization
