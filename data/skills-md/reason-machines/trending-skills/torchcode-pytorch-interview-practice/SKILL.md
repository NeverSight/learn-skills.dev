---
name: torchcode-pytorch-interview-practice
description: LeetCode-style PyTorch interview practice environment with auto-grading for implementing softmax, attention, GPT-2 and more from scratch.
triggers:
  - implement pytorch operator from scratch
  - practice pytorch interview questions
  - torchcode problem
  - implement softmax layernorm attention from scratch
  - pytorch coding interview prep
  - run torchcode judge
  - check my pytorch implementation
  - implement transformer components from scratch
---

# TorchCode — PyTorch Interview Practice

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

TorchCode is a Jupyter-based, self-hosted coding practice environment for ML engineers. It provides 40 curated problems covering PyTorch fundamentals and architectures (softmax, LayerNorm, MultiHeadAttention, GPT-2, etc.) with an automated judge that gives instant pass/fail feedback, gradient verification, and timing — like LeetCode but for tensors.

---

## Installation & Setup

### Option 1: Online (zero install)
- **Hugging Face Spaces**: https://huggingface.co/spaces/duoan/TorchCode
- **Google Colab**: Every notebook has an "Open in Colab" badge

### Option 2: pip (for use inside Colab or existing environment)
```bash
pip install torch-judge
```

### Option 3: Docker (pre-built image)
```bash
docker run -p 8888:8888 -e PORT=8888 ghcr.io/duoan/torchcode:latest
# Open http://localhost:8888
```

### Option 4: Build locally
```bash
git clone https://github.com/duoan/TorchCode.git
cd TorchCode
make run
# Open http://localhost:8888
```

`make run` auto-detects Docker or Podman and falls back to local build if the registry image is unavailable (common on Apple Silicon/arm64).

---

## Judge API

The `torch_judge` package provides the core API used in every notebook.

```python
from torch_judge import check, status, hint, reset_progress

# List all 40 problems and your progress
status()

# Run tests for a specific problem
check("relu")
check("softmax")
check("layernorm")
check("attention")
check("gpt2")

# Get a hint without spoilers
hint("softmax")

# Reset progress for a problem
reset_progress("relu")
```

### `check()` return values
- Colored pass/fail per test case
- Correctness check against PyTorch reference implementation
- Gradient verification (autograd compatibility)
- Timing measurement

---

## Problem Set Overview

### Difficulty levels: Easy → Medium → Hard

| # | Problem | Key Concepts |
|---|---------|--------------|
| 1 | ReLU | Activation functions, element-wise ops |
| 2 | Softmax | Numerical stability, exp/log tricks |
| 3 | Linear Layer | `y = xW^T + b`, Kaiming init, `nn.Parameter` |
| 4 | LayerNorm | Normalization, affine transform |
| 5 | Self-Attention | QKV projections, scaled dot-product |
| 6 | Multi-Head Attention | Head splitting, concatenation |
| 7 | BatchNorm | Batch vs layer statistics, train/eval |
| 8 | RMSNorm | LLaMA-style norm |
| 16 | Cross-Entropy Loss | Log-softmax, logsumexp trick |
| 17 | Dropout | Train/eval mode, inverted scaling |
| 18 | Embedding | Lookup table, `weight[indices]` |
| 19 | GELU | `torch.erf`, Gaussian error linear unit |
| 20 | Kaiming Init | `std = sqrt(2/fan_in)` |
| 21 | Gradient Clipping | Norm-based clipping |
| 31 | Gradient Accumulation | Micro-batching, loss scaling |
| 40 | Linear Regression | Normal equation, GD from scratch |

---

## Working Through a Problem

Each problem notebook has the same structure:

```
templates/
  01_relu.ipynb       # Blank template — your workspace
  02_softmax.ipynb
  ...
solutions/
  01_relu.ipynb       # Reference solution (study after attempt)
```

### Typical notebook workflow

```python
# Cell 1: Import judge
from torch_judge import check, hint
import torch
import torch.nn as nn

# Cell 2: Your implementation
def my_relu(x: torch.Tensor) -> torch.Tensor:
    # TODO: implement ReLU without using torch.relu or F.relu
    raise NotImplementedError

# Cell 3: Run the judge
check("relu")
```

---

## Real Implementation Examples

### ReLU (Problem 1 — Easy)
```python
def my_relu(x: torch.Tensor) -> torch.Tensor:
    return torch.clamp(x, min=0)
    # Alternative: return x * (x > 0)
    # Alternative: return torch.where(x > 0, x, torch.zeros_like(x))
```

### Softmax (Problem 2 — Easy, numerically stable)
```python
def my_softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    # Subtract max for numerical stability (prevents overflow)
    x_max = x.max(dim=dim, keepdim=True).values
    x_shifted = x - x_max
    exp_x = torch.exp(x_shifted)
    return exp_x / exp_x.sum(dim=dim, keepdim=True)
```

### LayerNorm (Problem 4 — Medium)
```python
def my_layer_norm(
    x: torch.Tensor,
    weight: torch.Tensor,   # gamma (scale)
    bias: torch.Tensor,     # beta (shift)
    eps: float = 1e-5
) -> torch.Tensor:
    mean = x.mean(dim=-1, keepdim=True)
    var = x.var(dim=-1, keepdim=True, unbiased=False)
    x_norm = (x - mean) / torch.sqrt(var + eps)
    return weight * x_norm + bias
```

### RMSNorm (Problem 8 — Medium, LLaMA-style)
```python
def rms_norm(x: torch.Tensor, weight: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    rms = torch.sqrt((x ** 2).mean(dim=-1, keepdim=True) + eps)
    return (x / rms) * weight
```

### Scaled Dot-Product Self-Attention (Problem 5 — Medium)
```python
import torch.nn.functional as F
import math

def scaled_dot_product_attention(
    Q: torch.Tensor,  # (B, heads, T, head_dim)
    K: torch.Tensor,
    V: torch.Tensor,
    mask: torch.Tensor = None
) -> torch.Tensor:
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    attn_weights = F.softmax(scores, dim=-1)
    return torch.matmul(attn_weights, V)
```

### Multi-Head Attention (Problem 6 — Medium)
```python
class MyMultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        self.d_model = d_model

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        B, T, C = x.shape

        def split_heads(t):
            return t.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)

        Q = split_heads(self.W_q(x))
        K = split_heads(self.W_k(x))
        V = split_heads(self.W_v(x))

        attn_out = scaled_dot_product_attention(Q, K, V, mask)
        # (B, heads, T, head_dim) -> (B, T, d_model)
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, T, C)
        return self.W_o(attn_out)
```

### Cross-Entropy Loss (Problem 16 — Easy)
```python
def cross_entropy_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    # logits: (B, C), targets: (B,) with class indices
    # Use logsumexp trick for numerical stability
    log_sum_exp = torch.logsumexp(logits, dim=-1)  # (B,)
    log_probs = logits[torch.arange(len(targets)), targets]  # (B,)
    return (log_sum_exp - log_probs).mean()
```

### Dropout (Problem 17 — Easy)
```python
class MyDropout(nn.Module):
    def __init__(self, p: float = 0.5):
        super().__init__()
        self.p = p

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.training or self.p == 0:
            return x
        mask = torch.bernoulli(torch.ones_like(x) * (1 - self.p))
        return x * mask / (1 - self.p)  # inverted scaling
```

### Kaiming Init (Problem 20 — Easy)
```python
def kaiming_init(weight: torch.Tensor) -> torch.Tensor:
    fan_in = weight.size(1)
    std = math.sqrt(2.0 / fan_in)
    with torch.no_grad():
        weight.normal_(0, std)
    return weight
```

### Gradient Clipping (Problem 21 — Easy)
```python
def clip_grad_norm(parameters, max_norm: float) -> float:
    params = [p for p in parameters if p.grad is not None]
    total_norm = torch.sqrt(sum(p.grad.data.norm() ** 2 for p in params))
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1:
        for p in params:
            p.grad.data.mul_(clip_coef)
    return total_norm.item()
```

### Gradient Accumulation (Problem 31 — Easy)
```python
def train_with_accumulation(model, optimizer, dataloader, accumulation_steps=4):
    optimizer.zero_grad()
    for i, (inputs, targets) in enumerate(dataloader):
        outputs = model(inputs)
        loss = criterion(outputs, targets) / accumulation_steps  # scale loss
        loss.backward()

        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
```

---

## Common Patterns & Tips

### Numerical stability pattern
Always subtract the max before `exp()`:
```python
# WRONG — can overflow for large values
exp_x = torch.exp(x)

# CORRECT — numerically stable
exp_x = torch.exp(x - x.max(dim=-1, keepdim=True).values)
```

### Causal attention mask (for GPT-style models)
```python
def causal_mask(T: int, device) -> torch.Tensor:
    return torch.tril(torch.ones(T, T, device=device)).unsqueeze(0).unsqueeze(0)
```

### nn.Module skeleton (used in many problems)
```python
class MyLayer(nn.Module):
    def __init__(self, ...):
        super().__init__()
        self.weight = nn.Parameter(torch.empty(...))
        self.bias = nn.Parameter(torch.zeros(...))
        self._init_weights()

    def _init_weights(self):
        nn.init.kaiming_uniform_(self.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ...
```

### Train vs eval mode pattern
```python
def forward(self, x):
    if self.training:
        # use batch statistics
        mean = x.mean(dim=0)
        var = x.var(dim=0, unbiased=False)
        # update running stats
        self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * mean
        self.running_var = (1 - self.momentum) * self.running_var + self.momentum * var
    else:
        # use running statistics
        mean = self.running_mean
        var = self.running_var
    return (x - mean) / torch.sqrt(var + self.eps) * self.weight + self.bias
```

---

## Project Structure

```
TorchCode/
├── templates/          # Blank notebooks for each problem (your workspace)
│   ├── 01_relu.ipynb
│   ├── 02_softmax.ipynb
│   └── ...
├── solutions/          # Reference solutions (study after attempting)
│   └── ...
├── torch_judge/        # Auto-grading package
│   ├── __init__.py     # check(), status(), hint(), reset_progress()
│   └── tasks/          # Per-problem test cases
├── Dockerfile
├── Makefile
└── pyproject.toml      # torch-judge package definition
```

---

## Troubleshooting

### Docker image not available for Apple Silicon (arm64)
```bash
# make run auto-falls back to local build, or force it:
make build
make start
```

### `check()` not found in Colab
```bash
!pip install torch-judge
# then restart runtime
```

### Notebook reset to blank template
Use the toolbar "Reset" button in JupyterLab to reset any notebook to its original blank state — useful for re-practicing a problem.

### Gradient check fails but output is correct
Ensure your implementation uses PyTorch operations (not NumPy) so autograd works:
```python
# WRONG — breaks autograd
import numpy as np
result = np.exp(x.numpy())

# CORRECT — autograd compatible
result = torch.exp(x)
```

### Viewing reference solution
After attempting a problem, open the matching file in `solutions/`:
```
solutions/02_softmax.ipynb
```

---

## Key Concepts Tested

| Concept | Problems |
|---------|----------|
| Numerical stability | Softmax, Cross-Entropy, LogSumExp |
| Autograd / `nn.Parameter` | Linear, LayerNorm, all nn.Module problems |
| Train vs eval behavior | BatchNorm, Dropout |
| Broadcasting | LayerNorm, RMSNorm, attention masking |
| Shape manipulation | Multi-Head Attention (view, transpose, contiguous) |
| Weight initialization | Kaiming Init, Linear Layer |
| Memory-efficient training | Gradient Accumulation, Gradient Clipping |
