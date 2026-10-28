---
name: tilekernels-gpu-kernels
description: Expert skill for using TileKernels, a library of optimized GPU kernels for LLM operations (MoE routing, quantization, transpose, engram gating, Manifold HyperConnection) built with TileLang.
triggers:
  - use tilekernels for moe routing
  - optimize gpu kernels with tilelang
  - fp8 quantization kernel deepseek
  - mixture of experts kernel library
  - engram gating kernel
  - manifold hyperconnection kernel
  - tilekernels quantization
  - write optimized llm kernels with tilelang
---

# TileKernels GPU Kernel Library

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

TileKernels is a high-performance GPU kernel library for LLM operations (MoE routing, FP8/FP4 quantization, transpose, engram gating, Manifold HyperConnection) written in TileLang — a Python DSL for expressing GPU kernels with automatic optimization. Kernels target NVIDIA SM90/SM100 (Hopper/Blackwell) architectures and approach hardware performance limits.

## Requirements

- Python 3.10+
- PyTorch 2.10+
- TileLang 0.1.9+
- NVIDIA SM90 or SM100 GPU (H100/H200/B100/B200)
- CUDA Toolkit 13.1+

## Installation

```bash
# Development install (recommended for extending/modifying kernels)
pip install -e ".[dev]"

# Release install
pip install tile-kernels
```

## Project Structure

```
tile_kernels/
├── moe/        # MoE routing: top-k selection, token-to-expert mapping, weight normalization
├── quant/      # FP8/FP4/E5M6 quantization with fused SwiGLU ops
├── transpose/  # Batched matrix transpose
├── engram/     # Engram gating: fused RMSNorm, forward/backward, weight gradient reduction
├── mhc/        # Manifold HyperConnection: Sinkhorn normalization, mix split/apply
├── modeling/   # High-level torch.autograd.Function wrappers
├── torch/      # PyTorch reference implementations for validation
└── testing/    # Test and benchmark utilities
```

## Key Modules and Usage

### MoE Routing Kernels

```python
import torch
from tile_kernels.moe import (
    topk_gating,           # Top-k expert selection and scoring
    token_to_expert_map,   # Token-to-expert mapping
    fused_expand_reduce,   # Fused expansion/reduction
    weight_normalize,      # Weight normalization
)

# Top-k gating: select top-k experts per token
# logits: [num_tokens, num_experts]
logits = torch.randn(1024, 256, device="cuda", dtype=torch.float32)
topk_weights, topk_indices = topk_gating(logits, top_k=8)
# topk_weights: [num_tokens, top_k], topk_indices: [num_tokens, top_k]
```

### Quantization Kernels

```python
import torch
from tile_kernels.quant import (
    per_token_cast_fp8,      # Per-token FP8 quantization
    per_block_cast_fp8,      # Per-block FP8 quantization
    per_channel_cast_fp8,    # Per-channel FP8 quantization
    fused_swiglu_quant_fp8,  # Fused SwiGLU + FP8 quantization
)

# Per-token FP8 quantization
x = torch.randn(1024, 4096, device="cuda", dtype=torch.bfloat16)
x_fp8, scale = per_token_cast_fp8(x)
# x_fp8: [1024, 4096] in torch.float8_e4m3fn
# scale: [1024, 1] per-token scales

# Per-block FP8 quantization (common for weight quantization)
w = torch.randn(8192, 4096, device="cuda", dtype=torch.bfloat16)
w_fp8, scale = per_block_cast_fp8(w, block_size=128)

# Fused SwiGLU + FP8 cast (saves memory bandwidth)
gate = torch.randn(1024, 8192, device="cuda", dtype=torch.bfloat16)
up = torch.randn(1024, 8192, device="cuda", dtype=torch.bfloat16)
out_fp8, scale = fused_swiglu_quant_fp8(gate, up)
```

### Transpose Kernels

```python
import torch
from tile_kernels.transpose import batched_transpose

# Batched transpose for MoE weight manipulation
# x: [batch, M, N]
x = torch.randn(32, 1024, 4096, device="cuda", dtype=torch.bfloat16)
x_T = batched_transpose(x)
# x_T: [batch, N, M] = [32, 4096, 1024]
```

### Engram Gating Kernels

```python
import torch
from tile_kernels.engram import (
    engram_gate_forward,    # Forward pass with fused RMSNorm
    engram_gate_backward,   # Backward pass
    engram_weight_grad,     # Weight gradient reduction
)

# Forward pass
hidden = torch.randn(1024, 2048, device="cuda", dtype=torch.bfloat16)
weight = torch.randn(256, 2048, device="cuda", dtype=torch.bfloat16)
output, norm_hidden = engram_gate_forward(hidden, weight)
```

### Manifold HyperConnection (mHC) Kernels

```python
import torch
from tile_kernels.mhc import (
    sinkhorn_normalize,     # Sinkhorn normalization
    mhc_mix_split,          # Mix splitting
    mhc_mix_apply,          # Mix application
)

# Sinkhorn normalization for connection weights
conn_weights = torch.randn(8, 64, device="cuda", dtype=torch.float32)
normalized = sinkhorn_normalize(conn_weights, num_iters=20)
```

### High-Level Modeling Layers

```python
import torch
from tile_kernels.modeling import EngramGateLayer, MHCPipeline

# EngramGate as a trainable nn.Module-compatible layer
# Uses torch.autograd.Function internally
gate_layer = EngramGateLayer(
    hidden_size=2048,
    num_experts=256,
).cuda()

hidden_states = torch.randn(1024, 2048, device="cuda", dtype=torch.bfloat16)
gate_output = gate_layer(hidden_states)

# Manifold HyperConnection pipeline
mhc = MHCPipeline(
    num_connections=8,
    hidden_size=2048,
).cuda()
```

## Testing

```bash
# Test a single module (correctness only, 4 parallel workers)
pytest tests/transpose/test_transpose.py -n 4

# Test with benchmarking
pytest tests/transpose/test_transpose.py --run-benchmark

# Test MoE kernels
pytest tests/moe/ -n 4

# Test quantization kernels
pytest tests/quant/ -n 4

# Test engram kernels
pytest tests/engram/ -n 4

# Full pressure test (all tests, 2 repetitions, 4 workers)
TK_FULL_TEST=1 pytest -n 4 --count 2

# Test specific quantization variant
pytest tests/quant/test_fp8_cast.py -n 4 --run-benchmark
```

## Common Patterns

### Pattern: Fused MoE Forward Pass

```python
import torch
from tile_kernels.moe import topk_gating, token_to_expert_map
from tile_kernels.quant import per_token_cast_fp8

def moe_dispatch(hidden_states, gate_weight, top_k=8):
    """Full MoE dispatch using TileKernels."""
    # 1. Compute gating logits
    logits = torch.mm(hidden_states, gate_weight.T)  # [T, E]
    
    # 2. Top-k expert selection
    topk_weights, topk_indices = topk_gating(logits, top_k=top_k)
    
    # 3. Build token-to-expert routing map
    routing_map = token_to_expert_map(topk_indices, num_experts=gate_weight.shape[0])
    
    # 4. Quantize activations before expert computation
    hidden_fp8, scale = per_token_cast_fp8(hidden_states)
    
    return hidden_fp8, scale, topk_weights, routing_map
```

### Pattern: Using PyTorch Reference Implementations for Validation

```python
import torch
from tile_kernels.quant import per_token_cast_fp8
from tile_kernels.torch import per_token_cast_fp8 as per_token_cast_fp8_ref

# Compare kernel output vs PyTorch reference
x = torch.randn(512, 4096, device="cuda", dtype=torch.bfloat16)

out_kernel, scale_kernel = per_token_cast_fp8(x)
out_ref, scale_ref = per_token_cast_fp8_ref(x)

# Validate
torch.testing.assert_close(
    out_kernel.float(), out_ref.float(), atol=1e-2, rtol=1e-2
)
print("Kernel matches reference ✓")
```

### Pattern: Benchmarking a Kernel

```python
import torch
from tile_kernels.testing import benchmark_kernel
from tile_kernels.transpose import batched_transpose

x = torch.randn(64, 4096, 4096, device="cuda", dtype=torch.bfloat16)

# Using the testing utility
result = benchmark_kernel(
    fn=batched_transpose,
    args=(x,),
    warmup=25,
    rep=100,
)
print(f"Latency: {result.mean:.3f} ms, Bandwidth: {result.gbps:.1f} GB/s")
```

### Pattern: Custom TileLang Kernel (extending the library)

```python
# tile_kernels follow TileLang DSL patterns
import tilelang
import tilelang.language as T

def make_elementwise_scale_kernel(M, N, dtype="float16"):
    @T.prim_func
    def scale_kernel(
        A: T.Buffer((M, N), dtype),
        scale: T.Buffer((M,), "float32"),
        B: T.Buffer((M, N), dtype),
    ):
        # TileLang kernel body
        for i, j in T.grid(M, N):
            B[i, j] = T.cast(
                T.cast(A[i, j], "float32") * scale[i],
                dtype
            )
    return scale_kernel

# Compile and use
kernel = tilelang.compile(make_elementwise_scale_kernel(1024, 4096))
```

## Architecture-Specific Notes

- **SM90 (Hopper: H100/H200)**: Full support, primary target
- **SM100 (Blackwell: B100/B200)**: Full support
- Kernels use hardware-specific features (tensor memory accelerator, async copy, warp-specialized pipelines) — do NOT run on older GPUs (Ampere/Ada)

## Troubleshooting

### CUDA Architecture Mismatch
```
RuntimeError: CUDA error: no kernel image is available for execution on the device
```
→ You need SM90 or SM100. Check with: `python -c "import torch; print(torch.cuda.get_device_capability())"`

### TileLang Version Mismatch
```
ImportError: cannot import name 'xyz' from 'tilelang'
```
→ Ensure TileLang >= 0.1.9: `pip install tilelang>=0.1.9`

### CUDA Toolkit Version
```
error: identifier "__nv_fp8_e4m3" is undefined
```
→ Requires CUDA 13.1+. Check: `nvcc --version`

### Out of Shared Memory
→ Kernels are tuned for specific tile sizes. If you hit shared memory limits, reduce batch size or sequence length, or file an issue.

### Running Tests Without Benchmark Flag
```bash
# Benchmarks are opt-in to avoid slow CI
pytest tests/ -n 4                    # Fast correctness only
pytest tests/ -n 4 --run-benchmark    # Include performance numbers
```

## Citation

```bibtex
@misc{tilekernels,
      title={TileKernels},
      author={Xiangwen Wang, Chenhao Xu, Huanqi Cao, Rui Tian, Weilin Zhao, Kuai Yu and Chenggang Zhao},
      year={2026},
      publisher = {GitHub},
      howpublished = {\url{https://github.com/deepseek-ai/TileKernels}},
}
```
