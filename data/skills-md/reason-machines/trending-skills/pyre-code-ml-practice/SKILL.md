---
name: pyre-code-ml-practice
description: Self-hosted ML coding practice platform with 68 problems covering Transformers, diffusion, RLHF, and more — instant browser feedback, no GPU required.
triggers:
  - "set up pyre code practice platform"
  - "add a new ml coding problem to pyre"
  - "how do I run the grading service"
  - "configure AI help for pyre code"
  - "pyre code problem set and learning paths"
  - "implement a coding challenge in pyre"
  - "troubleshoot pyre code submission grading"
  - "deploy pyre code with docker"
---

# Pyre Code ML Practice Platform

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Pyre Code is a self-hosted ML coding practice platform with 68 problems ranging from ReLU to flow matching. Users implement internals of modern AI systems (Transformers, vLLM, TRL, diffusion models) in a browser editor with instant pass/fail feedback, no GPU required.

---

## Installation

### Option A — One-liner (recommended)

```bash
git clone https://github.com/whwangovo/pyre-code.git
cd pyre-code
./setup.sh
npm run dev
```

`setup.sh` creates a `.venv` (prefers `uv`, falls back to `python3 -m venv`), installs all Python deps, then prints the start command.

### Option B — Conda

```bash
git clone https://github.com/whwangovo/pyre-code.git
cd pyre-code
conda create -n pyre python=3.11 -y && conda activate pyre
pip install -e ".[dev]"
npm install
npm run dev
```

### Option C — Docker

```bash
git clone https://github.com/whwangovo/pyre-code.git
cd pyre-code
docker compose up --build
```

Progress persists in a Docker volume. Reset with `docker compose down -v`.

### After installation

- **Grading service**: `http://localhost:8000`
- **Web app**: `http://localhost:3000`

---

## Project Structure

```
pyre/
├── web/                        # Next.js frontend
│   ├── src/app/                # Pages and API routes
│   ├── src/components/         # UI components
│   └── src/lib/                # Utilities, problem data
├── grading_service/            # FastAPI backend (grading API)
├── torch_judge/                # Judge engine — problem definitions + test runner
│   ├── problems/               # Individual problem modules
│   └── runner.py               # Test execution logic
├── setup.sh                    # Environment bootstrap script
├── package.json                # Dev scripts (runs frontend + backend concurrently)
└── pyproject.toml              # Python package config
```

---

## Key Commands

```bash
# Start both frontend and backend concurrently
npm run dev

# Start only the grading service (FastAPI)
cd grading_service && uvicorn main:app --reload --port 8000

# Start only the frontend (Next.js)
cd web && npm run dev

# Run Python tests
pytest torch_judge/

# Install Python package in editable mode with dev deps
pip install -e ".[dev]"

# Docker: build and start
docker compose up --build

# Docker: stop and remove volumes (reset progress)
docker compose down -v
```

---

## Configuration

### Environment Variables

Create `web/.env.local` to override defaults:

```bash
# URL of the FastAPI grading service
GRADING_SERVICE_URL=http://localhost:8000

# SQLite database path for progress tracking
DB_PATH=./data/pyre.db
```

### AI Help (Optional)

Copy `web/.env.example` to `web/.env` and configure:

```bash
AI_HELP_BASE_URL=https://api.openai.com/v1
AI_HELP_API_KEY=$OPENAI_API_KEY
AI_HELP_MODEL=gpt-4o-mini
```

Any OpenAI-compatible endpoint works: OpenAI, Anthropic via proxy, Ollama, etc. Users can also set their own key in the UI if no server-side config is present.

---

## Problem Categories

| Category | Examples |
|---|---|
| **Fundamentals** | ReLU, Softmax, GELU, SwiGLU, Dropout, Embedding, Linear, Kaiming Init |
| **Normalization** | LayerNorm, BatchNorm, RMSNorm |
| **Attention** | Scaled Dot-Product, Multi-Head, Causal, GQA, Flash, Differential, MLA |
| **Position Encoding** | Sinusoidal PE, RoPE, ALiBi, NTK-aware RoPE |
| **Architecture** | GPT-2 Block, ViT Block, Conv2D, MoE, Depthwise Conv |
| **Training** | Adam, Cosine LR, Gradient Clipping, Mixed Precision, Activation Checkpointing |
| **Distributed** | Tensor Parallel, FSDP, Ring Attention |
| **Inference** | KV Cache, Top-k Sampling, Beam Search, Speculative Decoding, Paged Attention |
| **Alignment** | DPO, GRPO, PPO, Reward Model |
| **Diffusion** | Noise Schedule, DDIM Step, Flow Matching, adaLN-Zero |
| **Adaptation** | LoRA, QLoRA |
| **Reasoning** | MCTS, Multi-Token Prediction |
| **SSM** | Mamba SSM |

---

## Adding a New Problem

Problems live in `torch_judge/problems/`. Each problem is a Python module with a standard structure:

```python
# torch_judge/problems/my_new_problem.py

import torch
import torch.nn as nn
from typing import Any

PROBLEM_ID = "my_new_problem"
TITLE = "My New Problem: Implement Foo"
DIFFICULTY = "medium"  # "easy" | "medium" | "hard"
CATEGORY = "Fundamentals"

DESCRIPTION = """
## My New Problem

Implement the `foo` function that does XYZ.

### Input
- `x` (Tensor): shape `(batch, dim)`

### Output
- Tensor of shape `(batch, dim)`

### Formula
$$\\text{foo}(x) = x^2 + 1$$
"""

STARTER_CODE = """
import torch

def foo(x: torch.Tensor) -> torch.Tensor:
    # Your implementation here
    pass
"""

REFERENCE_SOLUTION = """
import torch

def foo(x: torch.Tensor) -> torch.Tensor:
    return x ** 2 + 1
"""

def make_test_cases() -> list[dict[str, Any]]:
    \"\"\"Return a list of test cases, each with inputs and expected outputs.\"\"\"
    cases = []
    
    # Basic case
    x = torch.tensor([[1.0, 2.0, 3.0]])
    cases.append({
        "input": {"x": x},
        "expected": x ** 2 + 1,
        "description": "Basic 1x3 tensor",
    })
    
    # Batch case
    x = torch.randn(4, 16)
    cases.append({
        "input": {"x": x},
        "expected": x ** 2 + 1,
        "description": "Batch of 4, dim 16",
    })
    
    # Edge case: zeros
    x = torch.zeros(2, 8)
    cases.append({
        "input": {"x": x},
        "expected": torch.ones(2, 8),
        "description": "Zero tensor",
    })
    
    return cases


def grade(submission_code: str) -> dict[str, Any]:
    \"\"\"Execute submission and return grading results.\"\"\"
    namespace = {}
    exec(submission_code, namespace)
    
    if "foo" not in namespace:
        return {"passed": 0, "total": 0, "error": "Function 'foo' not found"}
    
    fn = namespace["foo"]
    test_cases = make_test_cases()
    results = []
    
    for i, case in enumerate(test_cases):
        try:
            output = fn(**case["input"])
            passed = torch.allclose(output, case["expected"], atol=1e-5)
            results.append({
                "case": i + 1,
                "description": case["description"],
                "passed": passed,
                "error": None if passed else f"Output mismatch: got {output}, expected {case['expected']}",
            })
        except Exception as e:
            results.append({
                "case": i + 1,
                "description": case["description"],
                "passed": False,
                "error": str(e),
            })
    
    passed = sum(r["passed"] for r in results)
    return {
        "passed": passed,
        "total": len(results),
        "results": results,
    }
```

### Register the problem

After creating the module, register it in the problem registry (typically `torch_judge/registry.py` or equivalent):

```python
from torch_judge.problems import my_new_problem

PROBLEMS = [
    # ... existing problems ...
    my_new_problem,
]
```

---

## Grading Service API

The FastAPI grading service at `http://localhost:8000` exposes:

```bash
# Health check
GET /health

# List all problems
GET /problems

# Get a specific problem
GET /problems/{problem_id}

# Submit a solution
POST /submit
Content-Type: application/json

{
  "problem_id": "relu",
  "code": "import torch\n\ndef relu(x):\n    return torch.clamp(x, min=0)"
}

# Response
{
  "problem_id": "relu",
  "passed": 3,
  "total": 3,
  "results": [
    {"case": 1, "description": "Basic positive values", "passed": true, "error": null},
    {"case": 2, "description": "Negative values", "passed": true, "error": null},
    {"case": 3, "description": "Mixed values", "passed": true, "error": null}
  ]
}
```

### Calling the grading API from Python

```python
import requests

response = requests.post(
    "http://localhost:8000/submit",
    json={
        "problem_id": "softmax",
        "code": """
import torch

def softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    x_max = x.max(dim=dim, keepdim=True).values
    x_exp = torch.exp(x - x_max)
    return x_exp / x_exp.sum(dim=dim, keepdim=True)
"""
    }
)

result = response.json()
print(f"Passed {result['passed']}/{result['total']} test cases")
for r in result["results"]:
    status = "✓" if r["passed"] else "✗"
    print(f"  {status} Case {r['case']}: {r['description']}")
    if r["error"]:
        print(f"      Error: {r['error']}")
```

---

## Example Implementations

### Scaled Dot-Product Attention

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(
    q: torch.Tensor,  # (batch, heads, seq, d_k)
    k: torch.Tensor,
    v: torch.Tensor,
    mask: torch.Tensor | None = None,
) -> torch.Tensor:
    d_k = q.size(-1)
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, v)
```

### RMSNorm

```python
import torch

def rms_norm(x: torch.Tensor, weight: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    rms = x.pow(2).mean(dim=-1, keepdim=True).add(eps).sqrt()
    return x / rms * weight
```

### LoRA Linear Layer

```python
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, rank: int = 4, alpha: float = 1.0):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.02)
        self.lora_A = nn.Parameter(torch.randn(rank, in_features) * 0.02)
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.scale = alpha / rank

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        base = x @ self.weight.T
        lora = x @ self.lora_A.T @ self.lora_B.T
        return base + self.scale * lora
```

### Cosine Learning Rate Schedule

```python
import math

def cosine_lr(step: int, max_steps: int, lr_max: float, lr_min: float = 0.0) -> float:
    if step >= max_steps:
        return lr_min
    progress = step / max_steps
    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * progress))
```

### KV Cache (Inference)

```python
import torch
from dataclasses import dataclass, field

@dataclass
class KVCache:
    keys: list[torch.Tensor] = field(default_factory=list)
    values: list[torch.Tensor] = field(default_factory=list)

    def update(self, new_k: torch.Tensor, new_v: torch.Tensor):
        self.keys.append(new_k)
        self.values.append(new_v)

    def get(self) -> tuple[torch.Tensor, torch.Tensor]:
        return torch.cat(self.keys, dim=-2), torch.cat(self.values, dim=-2)

    def __len__(self) -> int:
        return len(self.keys)
```

---

## Learning Paths

Choose a path based on your goal:

| Path | Focus |
|---|---|
| **Transformer Internals** | Activations → Normalization → Attention → GPT-2 Block |
| **Attention & Position Encoding** | Every attention variant + RoPE, ALiBi, NTK-RoPE |
| **Train a GPT from Scratch** | Embeddings → architecture → loss → optimizer → tricks |
| **Inference & Distributed** | KV cache, quantization, sampling, tensor parallel, FSDP |
| **Alignment & Reasoning** | Reward model → DPO → GRPO → PPO → MCTS |
| **Vision Transformer** | Conv → patch embedding → ViT block |
| **Diffusion & DiT** | Noise schedule → DDIM → flow matching → adaLN-Zero |
| **LLM Frontier Architectures** | GQA, Differential Attention, MLA, MoE, MTP |

Recommended progression:
```
Fundamentals → Transformer Internals → Train a GPT from Scratch
                      │                         │
                      ▼                         ▼
             Attention & PE            Inference & Distributed
                      │                         │
                      ▼                         ▼
             LLM Frontier Archs        Alignment & Reasoning
```

---

## Troubleshooting

### Grading service not reachable

```bash
# Check if the service is running
curl http://localhost:8000/health

# If not, start it manually
cd grading_service
source ../.venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Python environment issues

```bash
# Verify correct Python is active
which python && python --version  # should be 3.11+

# Reinstall deps
pip install -e ".[dev]"

# With uv
uv pip install -e ".[dev]"
```

### Frontend can't connect to grading service

Check `web/.env.local`:
```bash
GRADING_SERVICE_URL=http://localhost:8000
```
Restart Next.js after changing `.env.local`.

### Docker: port conflicts

```bash
# Check what's on port 3000 or 8000
lsof -i :3000
lsof -i :8000

# Stop conflicting processes, then retry
docker compose up --build
```

### Submission always fails with import errors

Ensure the submission code only uses packages available in the environment. Core deps include `torch`, `numpy`, `math`. Check `pyproject.toml` for the full list.

### Progress not persisting

The SQLite DB lives at `./data/pyre.db` by default. For Docker, ensure the volume is mounted:
```yaml
# docker-compose.yml
volumes:
  - pyre_data:/app/data
```

---

## Contributing a Problem

1. Create `torch_judge/problems/{problem_id}.py` using the structure above
2. Include `PROBLEM_ID`, `TITLE`, `DIFFICULTY`, `CATEGORY`, `DESCRIPTION`, `STARTER_CODE`, `REFERENCE_SOLUTION`, `make_test_cases()`, and `grade()`
3. Register in the problem registry
4. Write at least 3 test cases: basic, edge case, and a larger/random tensor case
5. Verify with `pytest torch_judge/` before opening a PR
6. Open an issue first for new categories or structural changes
