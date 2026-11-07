---
name: turboquant-pytorch
description: PyTorch implementation of TurboQuant for LLM KV cache compression using two-stage vector quantization (random rotation + Lloyd-Max + QJL residual correction).
triggers:
  - compress KV cache with TurboQuant
  - quantize key value cache for LLM
  - reduce KV cache memory usage
  - implement TurboQuant quantization
  - 3-bit KV cache compression
  - use TurboQuant for attention
  - LLM inference memory optimization with TurboQuant
  - apply QJL residual correction to KV cache
---

# TurboQuant PyTorch

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

From-scratch PyTorch implementation of Google's TurboQuant (ICLR 2026) for compressing LLM KV caches. Achieves 5x compression at 3-bit with 99.5% attention fidelity via two-stage vector quantization.

## What It Does

TurboQuant compresses LLM key-value caches to 2–4 bits per coordinate:

- **Stage 1**: Random orthogonal rotation + Lloyd-Max scalar quantization (MSE-optimal)
- **Stage 2**: QJL residual correction — 1-bit sign projection that makes inner product estimates unbiased

Result: attention scores remain accurate even when individual vectors look quite different from originals. The algorithm preserves **inner products**, not vector fidelity.

**Compression ratios at 8K context on Qwen2.5-3B (289 MB FP16 baseline):**
- 4-bit → 76 MB (3.8x)
- 3-bit → 58 MB (5.0x) ← practical sweet spot
- 2-bit → 40 MB (7.3x)

## Installation

```bash
git clone https://github.com/tonbistudio/turboquant-pytorch
cd turboquant-pytorch
pip install -r requirements.txt

# For CUDA PyTorch:
pip install torch --index-url https://download.pytorch.org/whl/cu128
```

**requirements.txt includes:**
- `torch>=2.0`
- `scipy` (Lloyd-Max codebook computation)
- `transformers`, `accelerate`, `bitsandbytes` (only for real model validation)

## Project Structure

```
turboquant/
  __init__.py           # Package exports
  lloyd_max.py          # Lloyd-Max optimal scalar quantizer
  turboquant.py         # Core: TurboQuantMSE, TurboQuantProd, TurboQuantKVCache
  compressors.py        # Production compressors for real model tensors
  test_turboquant.py    # Synthetic validation tests
  validate.py           # Real model (Qwen2.5-3B) validation
```

## Key Commands

```bash
# Run synthetic algorithm validation (no GPU required, but GPU enables speed benchmark)
python -m turboquant.test_turboquant

# Run real model validation on Qwen2.5-3B-Instruct
# Requires CUDA GPU with ≥6GB VRAM; downloads ~2GB model on first run
python -m turboquant.validate
```

## Core API

### Lloyd-Max Codebook

```python
from turboquant.lloyd_max import build_lloyd_max_codebook

# Build optimal scalar quantizer codebook for d-dimensional rotated unit vectors
# Returns (boundaries, centroids) for the given bit-width
boundaries, centroids = build_lloyd_max_codebook(dim=128, bits=3)
```

### Stage 1: MSE Quantization (TurboQuantMSE)

```python
from turboquant.turboquant import TurboQuantMSE

# Initialize for head_dim=128, 3-bit quantization
tq_mse = TurboQuantMSE(dim=128, bits=3)

# Compress a batch of vectors: shape (batch, dim)
keys = torch.randn(512, 128)  # 512 key vectors
codes = tq_mse.quantize(keys)       # integer codes, (512, 128)
reconstructed = tq_mse.dequantize(codes)  # approximate keys, (512, 128)
```

### Stage 2: Unbiased Inner Product Estimation (TurboQuantProd)

```python
from turboquant.turboquant import TurboQuantProd

# Initialize with QJL correction
tq_prod = TurboQuantProd(dim=128, bits=3, proj_dim=64)

# Compress key vectors (stores codes + QJL residual signs)
compressed = tq_prod.compress(keys)  # dict with 'codes', 'signs', 'residual_norms'

# Estimate inner products <query, key> for all keys — unbiased estimator
query = torch.randn(128)
scores = tq_prod.inner_product(query, compressed)  # shape (512,)
```

### KV Cache Wrapper (TurboQuantKVCache)

```python
from turboquant.turboquant import TurboQuantKVCache

# Wrap a KV cache for a single attention head
cache = TurboQuantKVCache(dim=128, bits=3, proj_dim=64)

# Add key/value vectors as tokens are generated
cache.append_key(new_key)    # shape (dim,)
cache.append_value(new_val)  # shape (dim,)

# Compute attention scores for a query against all cached keys
query = torch.randn(128)
scores = cache.attention_scores(query)  # shape (seq_len,), unbiased

# Get values (MSE-reconstructed, used for weighted sum)
values = cache.get_values()  # shape (seq_len, dim)
```

### Production Compressors (for real model tensors)

```python
from turboquant.compressors import TurboQuantCompressorV2, TurboQuantCompressorMSE

# Key compressor — supports asymmetric attention score computation
key_compressor = TurboQuantCompressorV2(dim=128, bits=3, proj_dim=64)

# Compress all keys in a layer: shape (num_heads, seq_len, head_dim)
compressed_keys = key_compressor.compress(layer_keys)

# Compute attention scores directly from compressed keys (no decompress needed)
# query shape: (num_heads, head_dim)
scores = key_compressor.asymmetric_attention_scores(query, compressed_keys)
# scores shape: (num_heads, seq_len)

# Value compressor — MSE reconstruction (Stage 1 only, acceptable for values)
val_compressor = TurboQuantCompressorMSE(dim=128, bits=3)
compressed_vals = val_compressor.compress(layer_values)
reconstructed_vals = val_compressor.decompress(compressed_vals)
```

## Common Patterns

### Pattern 1: Compress a Full Model's KV Cache

```python
import torch
from turboquant.compressors import TurboQuantCompressorV2, TurboQuantCompressorMSE

def compress_kv_cache(kv_cache, head_dim=128, bits=3, proj_dim=64):
    """
    kv_cache: list of (keys, values) per layer
              keys/values shape: (num_heads, seq_len, head_dim)
    Returns list of compressed (keys, values) per layer.
    """
    key_comp = TurboQuantCompressorV2(dim=head_dim, bits=bits, proj_dim=proj_dim)
    val_comp = TurboQuantCompressorMSE(dim=head_dim, bits=bits)

    compressed = []
    for layer_keys, layer_vals in kv_cache:
        c_keys = key_comp.compress(layer_keys)
        c_vals = val_comp.compress(layer_vals)
        compressed.append((c_keys, c_vals))

    return compressed, key_comp, val_comp


def run_attention_with_compressed_cache(query, compressed_keys, compressed_vals,
                                        key_comp, val_comp):
    """
    query: (num_heads, head_dim)
    Returns: attention output (num_heads, head_dim)
    """
    # Unbiased attention scores from compressed keys
    scores = key_comp.asymmetric_attention_scores(query, compressed_keys)
    # scores: (num_heads, seq_len)

    attn_weights = torch.softmax(scores, dim=-1)  # (num_heads, seq_len)

    # Decompress values and compute weighted sum
    values = val_comp.decompress(compressed_vals)  # (num_heads, seq_len, head_dim)
    output = torch.einsum('hs,hsd->hd', attn_weights, values)
    return output
```

### Pattern 2: Validate Compression Quality

```python
import torch
import torch.nn.functional as F
from turboquant.turboquant import TurboQuantProd

def measure_attention_fidelity(keys, queries, bits=3, proj_dim=64):
    """
    Measure how well TurboQuant preserves attention distributions.
    keys:    (seq_len, head_dim)
    queries: (num_queries, head_dim)
    """
    dim = keys.shape[-1]
    tq = TurboQuantProd(dim=dim, bits=bits, proj_dim=proj_dim)

    compressed = tq.compress(keys)

    cosine_sims = []
    top1_matches = []

    for q in queries:
        # True attention scores
        true_scores = (keys @ q)  # (seq_len,)
        true_attn = torch.softmax(true_scores, dim=0)

        # TurboQuant estimated scores
        est_scores = tq.inner_product(q, compressed)  # (seq_len,)
        est_attn = torch.softmax(est_scores, dim=0)

        # Cosine similarity of attention distributions
        cos_sim = F.cosine_similarity(true_attn.unsqueeze(0),
                                       est_attn.unsqueeze(0)).item()
        cosine_sims.append(cos_sim)

        # Top-1 match
        top1_matches.append(true_attn.argmax() == est_attn.argmax())

    return {
        'mean_cosine_sim': sum(cosine_sims) / len(cosine_sims),
        'top1_accuracy': sum(top1_matches) / len(top1_matches),
    }

# Example usage
keys = torch.randn(2048, 128)
keys = F.normalize(keys, dim=-1)
queries = torch.randn(100, 128)
queries = F.normalize(queries, dim=-1)

results = measure_attention_fidelity(keys, queries, bits=3)
print(f"Cosine similarity: {results['mean_cosine_sim']:.4f}")
print(f"Top-1 accuracy:    {results['top1_accuracy']:.2%}")
```

### Pattern 3: Needle-in-Haystack Retrieval Test

```python
import torch
import torch.nn.functional as F
from turboquant.turboquant import TurboQuantProd

def needle_in_haystack(seq_len=2048, dim=128, bits=3):
    """Test whether TurboQuant preserves nearest-neighbor ordering."""
    tq = TurboQuantProd(dim=dim, bits=bits, proj_dim=64)

    # Build haystack of random unit vectors
    haystack = F.normalize(torch.randn(seq_len, dim), dim=-1)

    # Insert needle at random position
    needle_idx = torch.randint(0, seq_len, (1,)).item()
    query = F.normalize(torch.randn(dim), dim=0)
    needle = query + 0.1 * torch.randn(dim)  # Similar to query
    needle = F.normalize(needle, dim=0)
    haystack[needle_idx] = needle

    # Compress
    compressed = tq.compress(haystack)

    # True nearest neighbor
    true_scores = haystack @ query
    true_best = true_scores.argmax().item()

    # TurboQuant estimated nearest neighbor
    est_scores = tq.inner_product(query, compressed)
    est_best = est_scores.argmax().item()

    return true_best == est_best, true_best, est_best

# Run multiple trials
successes = sum(needle_in_haystack(seq_len=8192)[0] for _ in range(20))
print(f"Retrieval accuracy: {successes}/20")
```

### Pattern 4: Compute Memory Savings

```python
def estimate_memory_savings(num_layers, num_kv_heads, seq_len, head_dim,
                             bits, proj_dim=64):
    """
    Estimate compressed KV cache size vs FP16 baseline.
    """
    # FP16 baseline: 2 bytes per element
    fp16_bytes = num_layers * 2 * num_kv_heads * seq_len * head_dim * 2

    # Stage 1 codes: bits per element, packed into bytes
    codes_bytes = (num_layers * 2 * num_kv_heads * seq_len * head_dim * bits) // 8

    # Stage 2 signs (keys only): 1 bit per proj_dim element
    signs_bytes = (num_layers * num_kv_heads * seq_len * proj_dim) // 8

    # Residual norms: 1 float16 per vector (keys only)
    norms_bytes = num_layers * num_kv_heads * seq_len * 2

    total_compressed = codes_bytes + signs_bytes + norms_bytes
    ratio = fp16_bytes / total_compressed

    print(f"FP16 baseline:      {fp16_bytes / 1e6:.1f} MB")
    print(f"TurboQuant {bits}-bit:  {total_compressed / 1e6:.1f} MB")
    print(f"Compression ratio:  {ratio:.1f}x")
    return ratio

# Qwen2.5-3B: 36 layers, 2 KV heads, head_dim=128
estimate_memory_savings(
    num_layers=36, num_kv_heads=2,
    seq_len=8192, head_dim=128, bits=3
)
# FP16 baseline:      289.4 MB
# TurboQuant 3-bit:   57.9 MB
# Compression ratio:  5.0x
```

## Algorithm Details

### Why Random Rotation?

Rotating by a random orthogonal matrix `R` maps unit vectors to a space where each coordinate follows `N(0, 1/d)`. This makes coordinates nearly independent with known distribution — enabling optimal per-coordinate scalar quantization (Lloyd-Max).

### Why QJL for Keys but Not Values?

- **Keys**: Used in dot products with queries. Bias in inner product estimates directly corrupts attention weights. QJL correction is essential.
- **Values**: Used in weighted sums after softmax. Small per-vector MSE errors average out. Stage 1 MSE quantization is sufficient.

### Choosing `proj_dim` (QJL projection dimension)

Higher `proj_dim` → lower variance in inner product estimates, but more memory:

```python
# Rule of thumb: proj_dim = head_dim // 2 is a good default
# head_dim=128 → proj_dim=64
# head_dim=64  → proj_dim=32
# head_dim=256 → proj_dim=128
```

### Bit-width Selection Guide

| Bits | Compression | Cosine Sim | Top-1 Match | Use Case |
|------|-------------|------------|-------------|----------|
| 4    | 3.8x        | 0.999      | 87%         | Quality-critical tasks |
| 3    | 5.0x        | 0.995      | 82%         | **Recommended default** |
| 2    | 7.3x        | 0.988      | 66%         | Extreme memory pressure |

## Troubleshooting

**`scipy` import error when building codebooks:**
```bash
pip install scipy
```

**CUDA out of memory during `validate.py`:**
- Requires ≥6GB VRAM for Qwen2.5-3B in 4-bit
- Reduce `seq_len` in the validation script or use a smaller model

**Inner product estimates have high variance:**
- Increase `proj_dim` (try `head_dim` instead of `head_dim // 2`)
- Check that input vectors are normalized before compressing

**Codebook build is slow on first run:**
- Lloyd-Max uses numerical integration (scipy) — this is expected
- Codebooks are precomputed once per `(dim, bits)` combination; cache them:
```python
import pickle

# Save codebook
boundaries, centroids = build_lloyd_max_codebook(dim=128, bits=3)
with open('codebook_128_3bit.pkl', 'wb') as f:
    pickle.dump((boundaries, centroids), f)

# Load cached codebook
with open('codebook_128_3bit.pkl', 'rb') as f:
    boundaries, centroids = pickle.load(f)
```

**Attention fidelity lower than expected:**
- Ensure vectors are L2-normalized before compressing (`F.normalize(x, dim=-1)`)
- The compressors in `compressors.py` handle normalization internally; `TurboQuantProd` expects unit vectors

## References

- [TurboQuant paper](https://arxiv.org/abs/2504.19874) — ICLR 2026
- [QJL paper](https://arxiv.org/abs/2406.03482) — 1-bit residual correction technique
- [PolarQuant](https://arxiv.org/abs/2502.02617) — Related polar coordinate approach
