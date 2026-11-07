---
name: flashkda-delta-attention
description: High-performance Kimi Delta Attention CUDA kernels built on CUTLASS for efficient recurrent state inference
triggers:
  - use FlashKDA for delta attention
  - implement Kimi delta attention kernels
  - flash KDA inference kernel
  - chunk_kda with FlashKDA backend
  - high performance delta attention CUDA
  - FlashKDA recurrent state attention
  - delta attention with CUTLASS kernels
  - optimize KDA with FlashKDA
---

# FlashKDA Delta Attention Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

FlashKDA provides high-performance CUDA kernels for Kimi Delta Attention (KDA) built on CUTLASS. It targets SM90+ GPUs (H100/H20 class) and integrates as a drop-in backend for `flash-linear-attention`'s `chunk_kda` operation.

## Requirements

- GPU: SM90+ (H100, H20, or newer)
- CUDA 12.9+
- PyTorch 2.4+
- Python 3.8+

## Installation

```bash
git clone https://github.com/MoonshotAI/FlashKDA.git flash-kda
cd flash-kda
git submodule update --init --recursive
pip install -v .
```

Install the FLA integration (optional but recommended):

```bash
pip install -U flash-linear-attention  # >= 0.5.0
```

## Core Kernel API

### `flash_kda.fwd`

The primary low-level kernel call:

```python
import torch
import flash_kda

flash_kda.fwd(
    q, k, v, g, beta, scale, out,
    A_log, dt_bias, lower_bound,
    initial_state=None,
    final_state=None,
    cu_seqlens=None
)
```

**Tensor shapes and dtypes:**

| Parameter     | Dtype        | Shape              | Notes                                      |
|---------------|--------------|--------------------|--------------------------------------------|
| `q`           | bf16         | `[B, T, H, K]`    | Query; K must be 128                       |
| `k`           | bf16         | `[B, T, H, K]`    | Key; K must be 128                         |
| `v`           | bf16         | `[B, T, H, V]`    | Value; V must be 128                       |
| `g`           | bf16         | `[B, T, H, K]`    | Gate logits (sigmoid/activation applied internally) |
| `beta`        | bf16         | `[B, T, H]`       | Beta logits (sigmoid applied internally)   |
| `scale`       | float        | scalar             | Attention scale factor                     |
| `out`         | bf16         | `[B, T, H, V]`    | Pre-allocated output tensor                |
| `A_log`       | fp32         | `[H]`             | Per-head log-gate parameter                |
| `dt_bias`     | fp32         | `[H, K]`          | Per-head gate bias                         |
| `lower_bound` | float        | scalar             | Gate lower bound, range `[-5.0, 0]`        |
| `initial_state` | bf16/fp32/None | `[B, H, V, K]` or `[N, H, V, K]` | Optional initial recurrent state |
| `final_state` | bf16/fp32/None | `[B, H, V, K]` or `[N, H, V, K]` | Optional output final state       |
| `cu_seqlens`  | int64        | `[N+1]`            | Optional cumulative seq lengths for varlen |

**Constraints:**
- `K == V == 128` required
- When `cu_seqlens` is provided, `B` must be 1 and `T` is total tokens across all sequences
- `initial_state` and `final_state` dtypes must match when both provided

## Usage via flash-linear-attention Backend (Recommended)

FlashKDA auto-dispatches from FLA's `chunk_kda` when installed:

```python
import torch
import logging
from fla.ops.kda import chunk_kda

# Optional: see dispatch decisions
logging.basicConfig(level=logging.INFO)

B, T, H, K, V = 2, 2048, 16, 128, 128

q     = torch.randn(B, T, H, K,  dtype=torch.bfloat16, device='cuda')
k     = torch.randn(B, T, H, K,  dtype=torch.bfloat16, device='cuda')
v     = torch.randn(B, T, H, V,  dtype=torch.bfloat16, device='cuda')
g     = torch.randn(B, T, H, K,  dtype=torch.bfloat16, device='cuda')
beta  = torch.randn(B, T, H,     dtype=torch.bfloat16, device='cuda')
A_log = torch.randn(H,           dtype=torch.float32,  device='cuda')
dt_bias = torch.zeros(H, K,      dtype=torch.float32,  device='cuda')
h0    = torch.zeros(B, H, V, K,  dtype=torch.float32,  device='cuda')

scale = K ** -0.5
lower_bound = -5.0

with torch.inference_mode():
    out, final_state = chunk_kda(
        q=q, k=k, v=v, g=g, beta=beta,
        scale=scale,
        initial_state=h0,
        output_final_state=True,
        use_gate_in_kernel=True,
        use_qk_l2norm_in_kernel=True,
        use_beta_sigmoid_in_kernel=True,
        safe_gate=True,
        A_log=A_log,
        dt_bias=dt_bias,
        lower_bound=lower_bound,
        transpose_state_layout=True,
    )
# out: [B, T, H, V], final_state: [B, H, V, K]
```

## Direct Low-Level Kernel Usage

```python
import torch
import flash_kda

def run_flash_kda(
    q, k, v, g, beta,
    A_log, dt_bias,
    lower_bound=-5.0,
    initial_state=None,
):
    B, T, H, K = q.shape
    V = v.shape[-1]
    scale = K ** -0.5

    out = torch.empty(B, T, H, V, dtype=torch.bfloat16, device=q.device)
    final_state = torch.zeros(B, H, V, K, dtype=torch.float32, device=q.device)

    flash_kda.fwd(
        q, k, v, g, beta,
        scale, out,
        A_log, dt_bias, lower_bound,
        initial_state=initial_state,
        final_state=final_state,
        cu_seqlens=None,
    )
    return out, final_state


B, T, H, K = 1, 4096, 8, 128
device = 'cuda'
dtype  = torch.bfloat16

q       = torch.randn(B, T, H, K,   device=device, dtype=dtype)
k       = torch.randn(B, T, H, K,   device=device, dtype=dtype)
v       = torch.randn(B, T, H, K,   device=device, dtype=dtype)  # V==K==128
g       = torch.randn(B, T, H, K,   device=device, dtype=dtype)
beta    = torch.randn(B, T, H,      device=device, dtype=dtype)
A_log   = torch.full((H,), -0.1,    device=device, dtype=torch.float32)
dt_bias = torch.zeros(H, K,         device=device, dtype=torch.float32)

with torch.inference_mode():
    out, state = run_flash_kda(q, k, v, g, beta, A_log, dt_bias)

print(out.shape)    # [1, 4096, 8, 128]
print(state.shape)  # [1, 8, 128, 128]
```

## Variable-Length (Packed) Batching

Use `cu_seqlens` for variable-length sequences packed into a single batch dimension:

```python
import torch
import flash_kda

# Two sequences of lengths 512 and 768, packed together
seq_lens = [512, 768]
T_total  = sum(seq_lens)
N        = len(seq_lens)
H, K, V  = 16, 128, 128

cu_seqlens = torch.tensor([0, 512, 1280], dtype=torch.int64, device='cuda')

# B must be 1 for varlen mode
q    = torch.randn(1, T_total, H, K, dtype=torch.bfloat16, device='cuda')
k    = torch.randn(1, T_total, H, K, dtype=torch.bfloat16, device='cuda')
v    = torch.randn(1, T_total, H, V, dtype=torch.bfloat16, device='cuda')
g    = torch.randn(1, T_total, H, K, dtype=torch.bfloat16, device='cuda')
beta = torch.randn(1, T_total, H,    dtype=torch.bfloat16, device='cuda')

A_log   = torch.zeros(H,    dtype=torch.float32, device='cuda')
dt_bias = torch.zeros(H, K, dtype=torch.float32, device='cuda')

out = torch.empty(1, T_total, H, V, dtype=torch.bfloat16, device='cuda')
# State shape is [N, H, V, K] in varlen mode
final_state = torch.zeros(N, H, V, K, dtype=torch.float32, device='cuda')

scale = K ** -0.5

with torch.inference_mode():
    flash_kda.fwd(
        q, k, v, g, beta,
        scale, out,
        A_log, dt_bias, lower_bound=-5.0,
        initial_state=None,
        final_state=final_state,
        cu_seqlens=cu_seqlens,
    )

print(out.shape)         # [1, 1280, 16, 128]
print(final_state.shape) # [2, 16, 128, 128]
```

## Stateful Inference (Multi-turn / Streaming)

Pass `initial_state` from a previous call to maintain recurrent state across chunks:

```python
import torch
import flash_kda

H, K, V = 16, 128, 128
B = 2
scale = K ** -0.5

def inference_step(q, k, v, g, beta, A_log, dt_bias, state=None):
    T = q.shape[1]
    out = torch.empty(B, T, H, V, dtype=torch.bfloat16, device='cuda')
    new_state = torch.zeros(B, H, V, K, dtype=torch.float32, device='cuda')
    flash_kda.fwd(
        q, k, v, g, beta, scale, out,
        A_log, dt_bias, lower_bound=-5.0,
        initial_state=state,
        final_state=new_state,
        cu_seqlens=None,
    )
    return out, new_state

A_log   = torch.zeros(H,    dtype=torch.float32, device='cuda')
dt_bias = torch.zeros(H, K, dtype=torch.float32, device='cuda')

state = None
for chunk_idx in range(4):
    q    = torch.randn(B, 256, H, K, dtype=torch.bfloat16, device='cuda')
    k    = torch.randn(B, 256, H, K, dtype=torch.bfloat16, device='cuda')
    v    = torch.randn(B, 256, H, V, dtype=torch.bfloat16, device='cuda')
    g    = torch.randn(B, 256, H, K, dtype=torch.bfloat16, device='cuda')
    beta = torch.randn(B, 256, H,    dtype=torch.bfloat16, device='cuda')

    with torch.inference_mode():
        out, state = inference_step(q, k, v, g, beta, A_log, dt_bias, state)
    print(f"Chunk {chunk_idx}: out={out.shape}, state={state.shape}")
```

## Configuration & Environment Variables

| Variable          | Values    | Effect                                           |
|-------------------|-----------|--------------------------------------------------|
| `FLA_FLASH_KDA`   | `0` / `1` | Set to `0` to force Triton fallback in FLA       |

```bash
# Disable FlashKDA, use Triton path
FLA_FLASH_KDA=0 python your_script.py
```

## Running Tests

```bash
bash tests/test.sh
```

- `tests/test_fwd.py` — correctness tests against PyTorch reference and flash-linear-attention

## Common Patterns & Troubleshooting

### Check dispatch logging

```python
import logging
logging.basicConfig(level=logging.INFO)
# Successful: [FLA Backend] kda.chunk_kda -> flashkda
# Rejected:   [FLA Backend] kda.chunk_kda rejected: <reason>
```

### Verify GPU compatibility

```python
import torch
cap = torch.cuda.get_device_capability()
assert cap >= (9, 0), f"FlashKDA requires SM90+, got SM{cap[0]}{cap[1]}"
```

### K and V must be 128

```python
# WRONG — will error
q = torch.randn(1, 512, 8, 64, ...)   # K=64 not supported

# CORRECT
q = torch.randn(1, 512, 8, 128, ...)  # K=128 required
```

### Use `torch.inference_mode()` not `torch.no_grad()`

```python
# FlashKDA requires inference_mode for FLA dispatch
with torch.inference_mode():
    out, state = chunk_kda(...)
```

### State dtype consistency

```python
# initial_state and final_state must have matching dtypes
initial = torch.zeros(B, H, V, K, dtype=torch.float32, device='cuda')
final   = torch.zeros(B, H, V, K, dtype=torch.float32, device='cuda')  # must match
# bf16 initial + fp32 final → error
```

### `lower_bound` valid range

```python
lower_bound = -5.0   # valid: range is [-5.0, 0]
lower_bound = -2.5   # valid
lower_bound = 0.0    # valid boundary
lower_bound = -10.0  # out of spec — use -5.0 as safe minimum
```

### IntelliSense / clangd setup for development

```bash
bash setup_clangd.sh
# Generates .clangd with correct include paths for CUDA/CUTLASS sources
```
