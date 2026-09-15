---
name: flash-moe-inference
description: Run 397B parameter Mixture-of-Experts LLMs on a MacBook using pure C/Metal with SSD streaming
triggers:
  - run a large language model on my laptop
  - stream expert weights from SSD
  - flash moe inference engine
  - run Qwen3.5 397B on Mac
  - mixture of experts on Apple Silicon
  - metal inference engine for large models
  - quantized MoE inference macOS
  - run 209GB model on MacBook
---

# Flash-MoE Inference Engine

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Flash-MoE is a pure C/Objective-C/Metal inference engine that runs **Qwen3.5-397B-A17B** (397B parameter Mixture-of-Experts) on a MacBook Pro with 48GB RAM at 4.4+ tokens/second. It streams 209GB of expert weights from NVMe SSD on demand — no Python, no ML frameworks, just C, Objective-C, and hand-tuned Metal shaders.

## Requirements

- **Hardware**: Apple Silicon Mac (M3 Max or similar), 48GB+ unified memory, 1TB+ SSD with ~210GB free
- **OS**: macOS 26+ (Darwin 25+)
- **Tools**: Xcode Command Line Tools, Python 3.x (for weight extraction only)
- **Model**: Qwen3.5-397B-A17B safetensors weights (download separately from HuggingFace)

## Installation & Build

```bash
# Clone the repo
git clone https://github.com/danveloper/flash-moe
cd flash-moe/metal_infer

# Build everything
make

# Verify build artifacts
ls infer chat main
```

The Makefile compiles `infer.m`, `chat.m`, `main.m` with Metal shader compilation for `shaders.metal`.

## Weight Preparation

### Step 1: Extract non-expert weights

```bash
# From the metal_infer/ directory
# Point to your downloaded Qwen3.5-397B safetensors directory
python3 extract_weights.py /path/to/Qwen3.5-397B-A17B-Instruct/

# Produces:
#   model_weights.bin   (~5.5GB, mmap'd at runtime)
#   model_weights.json  (tensor manifest)
#   vocab.bin           (vocabulary)
#   tokenizer.bin       (BPE tokenizer data)
```

### Step 2: Pack expert weights (4-bit, production)

```bash
# From repo root
python3 repack_experts.py /path/to/Qwen3.5-397B-A17B-Instruct/ metal_infer/packed_experts/

# Produces packed_experts/ directory (~209GB)
# Each expert is a separate file: layer_XX_expert_YYYY.bin
```

### Step 3: Optional 2-bit requantization (faster but breaks JSON/tool calling)

```bash
# Convert 4-bit experts to 2-bit (saves ~89GB, 120GB total)
python3 metal_infer/repack_experts_2bit.py \
    metal_infer/packed_experts/ \
    metal_infer/packed_experts_2bit/
```

## Key Commands

### Basic inference

```bash
cd metal_infer

# 4-bit inference (production quality, tool calling works)
./infer --prompt "Explain quantum computing" --tokens 100

# 2-bit inference (faster, breaks JSON/tool calling)
./infer --prompt "Explain quantum computing" --tokens 100 --2bit

# Per-layer timing breakdown
./infer --prompt "Hello" --tokens 20 --timing
```

### Interactive chat with tool calling

```bash
./chat
# Opens TUI with full tool calling support
# Uses 4-bit experts by default
```

### MoE-only benchmark (measures expert throughput)

```bash
./main
# Runs pure expert forward-pass benchmark
# Reports tokens/sec without attention overhead
```

## Project Structure

```
flash-moe/
├── paper/
│   └── flash_moe.pdf          # Full technical paper
├── metal_infer/
│   ├── infer.m                # Complete inference engine (~7000 lines)
│   ├── shaders.metal          # Metal compute kernels (~1200 lines)
│   ├── chat.m                 # Interactive chat TUI
│   ├── tokenizer.h            # Single-header C BPE tokenizer (449 lines)
│   ├── main.m                 # MoE-only benchmark
│   ├── Makefile
│   ├── extract_weights.py     # Safetensors → model_weights.bin
│   ├── repack_experts_2bit.py # 4-bit → 2-bit requantization
│   ├── train_predictor.py     # Expert routing prediction analysis
│   ├── model_weights.bin      # Non-expert weights (mmap'd)
│   ├── model_weights.json     # Tensor manifest
│   ├── vocab.bin
│   ├── tokenizer.bin
│   ├── packed_experts/        # 4-bit expert files (209GB)
│   └── packed_experts_2bit/   # 2-bit expert files (120GB, optional)
├── repack_experts.py          # 4-bit expert packing from safetensors
├── progress.py                # Results visualization
└── results.tsv                # Experiment log
```

## Architecture Overview

The model has **60 transformer layers**:
- 45 GatedDeltaNet (linear attention) layers
- 15 standard full attention layers
- Each layer: 512 experts, K=4 activated per token + 1 shared expert
- Hidden dimension: 4096

### Per-layer pipeline (4.28ms average at 4-bit)

```
CMD3(prev) → CMD1: attention projections + delta-net  [1.22ms GPU]
           → CPU: flush results                       [0.01ms CPU]  
           → CMD2: o_proj + norm + routing + shared    [0.55ms GPU]
           → CPU: softmax + topK routing               [0.003ms]
           → I/O: parallel pread K=4 experts           [2.41ms SSD]
           → CMD3: expert forward + combine + norm     [0.04ms encode, DEFERRED]
```

## Metal Shader Kernels

The `shaders.metal` file contains hand-written kernels. Key kernels:

```metal
// 4-bit dequantized matrix-vector multiply (FMA-optimized)
// Key insight: fma(nibble, scale*x, bias*x) instead of (nibble*scale + bias)*x
// Pre-compute scale*x and bias*x to fuse dequant+multiply in one FMA instruction

kernel void matvec_4bit_fma(
    device const uint8_t* weights [[buffer(0)]],
    device const float* scales    [[buffer(1)]],
    device const float* biases    [[buffer(2)]],
    device const float* x         [[buffer(3)]],
    device float* out             [[buffer(4)]],
    uint tid [[thread_position_in_threadgroup]],
    uint gid [[threadgroup_position_in_grid]])
{
    // ... tiled SIMD-reduced FMA kernel
    // 12% faster than naive (nibble * scale + bias) * x
}

// Fused SwiGLU activation
kernel void swiglu(device float* gate [[buffer(0)]],
                   device const float* up [[buffer(1)]],
                   uint gid [[thread_position_in_grid]])
{
    float g = gate[gid];
    gate[gid] = (g / (1.0f + exp(-g))) * up[gid];
}

// RMS normalization (two-pass)
kernel void rms_norm_pass1(...) // sum of squares reduction
kernel void rms_norm_pass2(...) // apply normalization

// GPU RoPE (fused with Q deinterleave and K normalization)
kernel void rope_qk(...)

// MoE combine + residual + sigmoid gate (fused)
kernel void moe_combine_residual(...)
```

## SSD Expert Streaming Pattern

The core innovation — loading only K=4 active experts per layer from SSD:

```objc
// Parallel expert loading using GCD dispatch groups
// From infer.m (conceptual pattern)

dispatch_group_t group = dispatch_group_create();
dispatch_queue_t ioQueue = dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0);

for (int k = 0; k < K_EXPERTS; k++) {
    int expert_id = top_k_indices[k];
    dispatch_group_async(group, ioQueue, ^{
        // Each expert: ~6.75MB at 4-bit
        char path[256];
        snprintf(path, sizeof(path), 
                 "packed_experts/layer_%02d_expert_%04d.bin",
                 layer, expert_id);
        
        int fd = open(path, O_RDONLY);
        // pread() — non-blocking, OS page cache handles LRU
        pread(fd, expert_buffer[k], expert_size, 0);
        close(fd);
    });
}

dispatch_group_wait(group, DISPATCH_TIME_FOREVER);
// GPU compute follows — serial pipeline is hardware-optimal on Apple Silicon
```

**Why `pread()` not `mmap()`**: mmap incurs per-page fault overhead on cold data (~5x slower). Direct `pread()` with OS page cache achieves ~71% hit rate naturally.

## GatedDeltaNet Linear Attention (BLAS)

The recurrence update uses Accelerate BLAS — 64% faster than scalar:

```objc
// GatedDeltaNet state update per head (conceptual pattern)
// state: 128×128 float matrix, 64 heads
// From infer.m

#import <Accelerate/Accelerate.h>

for (int h = 0; h < 64; h++) {
    float* S = state + h * 128 * 128;  // 128×128 state matrix
    float* q = Q + h * 128;
    float* k = K + h * 128;
    float* v = V + h * 128;
    
    // β·(k⊗v) outer product update
    // cblas_sger: S += beta * (k ⊗ v)
    cblas_sger(CblasRowMajor, 128, 128,
               beta[h], k, 1, v, 1, S, 128);
    
    // Decay: S = alpha * S
    cblas_sscal(128 * 128, alpha[h], S, 1);
    
    // Output: o = S @ q
    cblas_sgemv(CblasRowMajor, CblasNoTrans,
                128, 128, 1.0f, S, 128, q, 1, 0.0f,
                output + h * 128, 1);
}
```

## Performance Configuration

### 4-bit (production default)
- **Quality**: Excellent — full tool calling, correct JSON
- **Speed**: 4.36 tok/s
- **Disk**: 209GB

### 2-bit (speed testing only)
- **Quality**: Good — but breaks JSON/tool calling (`\name\` instead of `"name"`)
- **Speed**: 5.74 tok/s (7.05 peak single token with warm cache)
- **Disk**: 120GB
- Uses `F_NOCACHE` flag to avoid page cache thrashing

## What NOT to Try (Learned from 58 Experiments)

| Approach | Why it fails |
|----------|-------------|
| `mmap()` expert files | Per-page fault overhead: 5x slower than `pread()` |
| `dispatch_io` | `dispatch_data` management overhead: -70% |
| `F_RDADVISE` prefetch | SSD DMA + GPU share memory controller — concurrent access: -73% GPU speed |
| Custom Metal LRU cache | GPU memory pressure: -38% vs OS page cache |
| LZ4 expert compression | Decompress overhead > warm cache savings: -13% |
| Temporal expert prediction | 25% hit rate, wastes SSD bandwidth: -18% |
| Speculative early routing | Cache pollution: -38% |
| MTP speculative decoding | MoE I/O scales per-token (unlike dense models): break-even |
| Spin-poll GPU wait | CPU thermal throttle competes with GPU: -23% |
| Parallel SSD + GPU overlap | Unified memory controller arbitration: net negative |

**Key principle**: On Apple Silicon, GPU DMA and SSD DMA share the same memory controller. The serial pipeline (GPU → SSD → GPU) is hardware-optimal.

## Troubleshooting

### Build fails
```bash
# Ensure Xcode CLI tools are installed
xcode-select --install

# Check Metal compiler is available
xcrun -sdk macosx metal --version
```

### Out of memory
The engine is designed to use ~6GB active:
- 5.5GB: `model_weights.bin` (mmap'd, read-only)
- ~200MB: Metal scratch buffers
- Remaining ~42GB: OS page cache for expert data

If you see OOM, check for other processes consuming unified memory:
```bash
sudo memory_pressure
vm_stat
```

### Slow performance
```bash
# Check SSD speed — needs ~17GB/s for target performance
# Run with timing to identify bottleneck
./infer --prompt "Hello" --tokens 5 --timing

# Verify packed_experts/ is on internal SSD, not external drive
diskutil info /
```

### Wrong expert directory
```bash
# Default paths expected by infer.m:
# metal_infer/packed_experts/     (4-bit)
# metal_infer/packed_experts_2bit/ (2-bit)

# Ensure you're running from metal_infer/ directory
cd metal_infer
./infer --prompt "test"
```

### Tool calling broken
Use 4-bit, not 2-bit. The 2-bit quantization corrupts quote characters in JSON output, making tool calling unreliable. Always use the default 4-bit configuration for agentic workloads.

## Memory Safety

The engine explicitly manages all allocations:
- No unbounded caches
- Expert data never accumulates in GPU memory
- `model_weights.bin` is mmap'd read-only — kernel manages pages
- Expert files are opened/read/closed per inference step
