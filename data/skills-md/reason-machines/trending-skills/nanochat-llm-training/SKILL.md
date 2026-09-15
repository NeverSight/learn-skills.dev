---
name: nanochat-llm-training
description: Train your own GPT-2 level LLM for under $100 using nanochat, Karpathy's minimal hackable harness covering tokenization, pretraining, finetuning, evaluation, inference, and chat UI.
triggers:
  - train my own LLM with nanochat
  - run nanochat pretraining
  - reproduce GPT-2 with nanochat
  - nanochat finetuning and chat
  - set up nanochat on GPU node
  - nanochat speedrun leaderboard
  - configure nanochat depth and hyperparameters
  - talk to my nanochat model in chat UI
---

# nanochat LLM Training

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

nanochat is Karpathy's minimal, hackable harness for training LLMs end-to-end on a single GPU node. It covers tokenization, pretraining, SFT finetuning, RL, evaluation (DCLM CORE score), inference with KV cache, and a ChatGPT-like web UI. A single complexity dial (`--depth`) auto-configures all other hyperparameters (width, heads, LR, training horizon, weight decay) for compute-optimal training. You can reproduce GPT-2 capability (~$43,000 in 2019) for ~$48 on an 8×H100 node (~2 hours).

## Installation

nanochat uses `uv` for dependency management:

```bash
git clone https://github.com/karpathy/nanochat.git
cd nanochat
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
# Create venv and install deps
uv sync
source .venv/bin/activate
```

## Key Commands

### Full GPT-2 Speedrun (8×H100 node, ~2–3 hours, ~$48)

```bash
# Run the reference pipeline: data download, pretraining, SFT, eval, chat
bash runs/speedrun.sh
```

### Pretraining (distributed)

```bash
OMP_NUM_THREADS=1 torchrun --standalone --nproc_per_node=8 -m scripts.base_train -- \
    --depth=26 \
    --run="d26_run" \
    --model-tag="d26"
```

### Pretraining (single GPU)

```bash
python -m scripts.base_train -- \
    --depth=26 \
    --run="d26_single"
```

### Quick Research Iteration (~5 min, GPT-1 scale)

```bash
OMP_NUM_THREADS=1 torchrun --standalone --nproc_per_node=8 -m scripts.base_train -- \
    --depth=12 \
    --run="d12_exp" \
    --model-tag="d12" \
    --core-metric-every=999999 \
    --sample-every=-1 \
    --save-every=-1
```

### CPU / Apple Silicon (tiny model, ~minutes)

```bash
bash runs/runcpu.sh
```

### Serve Chat UI

```bash
# After training completes
source .venv/bin/activate
python -m scripts.chat_web
# Visit http://<your-server-ip>:8000/
```

### CLI Chat

```bash
python -m scripts.chat_cli -p "hello"
```

### Scaling Laws / Miniseries

```bash
bash runs/scaling_laws.sh   # sweep depths for scaling law data
bash runs/miniseries.sh     # train full compute-optimal miniseries
```

## The Depth Dial

The single most important parameter. Everything else is derived automatically:

| `--depth` | Approximate model scale | Notes |
|-----------|------------------------|-------|
| 6–8 | Tiny (toy) | CPU/MPS feasible |
| 12 | GPT-1 size | ~5 min on 8×H100, great for research iteration |
| 16 | Medium | ~15 min on 8×H100 |
| 24–26 | GPT-2 size | ~2 hrs on 8×H100, ~$48 |

```bash
# Smaller/faster experiments
python -m scripts.base_train -- --depth=12 --run="quick_test"

# Full GPT-2 grade
torchrun --standalone --nproc_per_node=8 -m scripts.base_train -- --depth=26 --run="gpt2_repro"
```

## Precision / dtype Configuration

nanochat uses explicit dtype management via `COMPUTE_DTYPE` in `nanochat/common.py`. No `torch.amp.autocast`.

| Hardware | Default | Override |
|----------|---------|---------|
| CUDA SM 80+ (A100, H100) | `bfloat16` | `NANOCHAT_DTYPE=float32` |
| CUDA SM < 80 (V100, T4) | `float32` | `NANOCHAT_DTYPE=float16` |
| CPU / MPS | `float32` | — |

```bash
# Force fp32 for inference
NANOCHAT_DTYPE=float32 python -m scripts.chat_cli -p "hello"

# Force bf16 for training
NANOCHAT_DTYPE=bfloat16 torchrun --nproc_per_node=8 -m scripts.base_train

# float16 training (enables GradScaler automatically)
NANOCHAT_DTYPE=float16 torchrun --nproc_per_node=8 -m scripts.base_train
```

**How it works:** Weights stored in fp32 (optimizer precision), custom `Linear` casts to `COMPUTE_DTYPE` in forward pass, embeddings stored directly in `COMPUTE_DTYPE` to save memory.

## Key Python Modules

```
nanochat/
├── gpt.py              # GPT nn.Module Transformer
├── engine.py           # Inference with KV Cache
├── dataloader.py       # Tokenizing Distributed Data Loader
├── dataset.py          # Download/read utils for pretraining data
├── optim.py            # AdamW + Muon optimizer (1GPU and distributed)
├── core_eval.py        # DCLM CORE score evaluation
├── loss_eval.py        # Bits-per-byte evaluation
├── checkpoint_manager.py  # Save/Load checkpoints
├── common.py           # Utilities, COMPUTE_DTYPE
├── execution.py        # Python code execution tool for LLM
└── engine.py           # Efficient KV-cache inference

scripts/
├── base_train.py       # Pretraining entry point
├── chat_web.py         # Web chat UI server
└── chat_cli.py         # CLI chat interface

runs/
├── speedrun.sh         # Reference full pipeline (GPT-2 speedrun)
├── scaling_laws.sh     # Scaling law sweeps
├── miniseries.sh       # Full compute-optimal miniseries
└── runcpu.sh           # CPU/MPS example
```

## Real Code Examples

### Load and Run Inference on a Trained Model

```python
import torch
from nanochat.gpt import GPT
from nanochat.engine import InferenceEngine
from nanochat.checkpoint_manager import CheckpointManager

# Load checkpoint
ckpt_manager = CheckpointManager("checkpoints/d26")
model, config = ckpt_manager.load()
model.eval()

# Run inference with KV cache
engine = InferenceEngine(model)
output = engine.generate(
    prompt="Once upon a time",
    max_new_tokens=200,
    temperature=0.8,
    top_p=0.95,
)
print(output)
```

### Custom Training Script with Depth Dial

```python
import subprocess

def train_model(depth: int, run_name: str, nproc: int = 8):
    """Launch a compute-optimal training run for given depth."""
    cmd = [
        "torchrun",
        "--standalone",
        f"--nproc_per_node={nproc}",
        "-m", "scripts.base_train",
        "--",
        f"--depth={depth}",
        f"--run={run_name}",
        f"--model-tag={run_name}",
    ]
    subprocess.run(cmd, env={"OMP_NUM_THREADS": "1", **__import__("os").environ})

# Quick research iteration
train_model(depth=12, run_name="my_experiment_d12")

# Full GPT-2 grade
train_model(depth=26, run_name="my_gpt2_repro")
```

### Adjust Device Batch Size for Lower VRAM

```bash
# Default device_batch_size=32 needs ~80GB VRAM per GPU
# Reduce for smaller GPUs (gradient accumulation handles the rest)
torchrun --standalone --nproc_per_node=4 -m scripts.base_train -- \
    --depth=12 \
    --device_batch_size=16 \
    --run="low_vram_run"

# Even smaller
python -m scripts.base_train -- \
    --depth=8 \
    --device_batch_size=4 \
    --run="single_gpu_small"
```

### Monitoring Key Metrics in wandb

```python
# nanochat logs to wandb automatically. Key metrics to watch:
# - val_bpb: validation loss in bits-per-byte (vocab-size-invariant)
#   as a function of step, total_training_time, total_training_flops
# - core_metric: DCLM CORE score (target > 0.2565 to beat GPT-2)
# - train/mfu: Model FLOPS utilization
# - train/tok_per_sec: Training throughput

# Set wandb project via env var before training
import os
os.environ["WANDB_PROJECT"] = "my-nanochat-runs"
```

### Synthetic Data for SFT Personality

```python
# dev/gen_synthetic_data.py — generate identity/personality data
# Then mix into SFT stage per the guide:
# https://github.com/karpathy/nanochat/discussions/139

# Example: generate data and point SFT to it
python dev/gen_synthetic_data.py --output data/identity_sft.jsonl
# Then reference in your SFT script configuration
```

## Common Patterns

### Research Iteration Loop

```bash
# 1. Make a code change in nanochat/
# 2. Run quick d12 to validate
OMP_NUM_THREADS=1 torchrun --standalone --nproc_per_node=8 -m scripts.base_train -- \
    --depth=12 --run="test_my_change" \
    --core-metric-every=999999 --sample-every=-1 --save-every=-1
# 3. Check wandb: val_bpb vs step/time/flops
# 4. If promising, test at d16 or d26
```

### FP8 Training (H100 only, for speedrun)

```bash
# FP8 is used in the speedrun for additional speedup
# See runs/speedrun.sh for the exact invocation
bash runs/speedrun.sh
```

### Evaluate CORE Score Only

```bash
python -m nanochat.core_eval --checkpoint checkpoints/d26/latest
```

### Serve on Lambda / Remote Machine

```bash
# On remote machine after training:
source .venv/bin/activate
python -m scripts.chat_web
# Access via: http://<PUBLIC_IP>:8000/
# Use `screen` or `tmux` to keep alive
screen -S nanochat
python -m scripts.chat_web
# Ctrl+A, D to detach
```

## Troubleshooting

### OOM / Out of VRAM

```bash
# Reduce --device_batch_size (default 32)
# Code uses gradient accumulation to maintain effective batch size
--device_batch_size=16   # Try 16, 8, 4, 2, 1
```

### Single GPU is 8× Slower

This is expected. Omit `torchrun` and use `python -m scripts.base_train` directly. Gradient accumulation kicks in automatically to maintain equivalent total batch size.

### Running on Non-CUDA Hardware

```bash
# MPS (Apple Silicon) or CPU — use runcpu.sh as template
bash runs/runcpu.sh
# Results will be weak; this is for development/debugging only
```

### float16 Gradient Underflow

```bash
# nanochat auto-enables GradScaler when NANOCHAT_DTYPE=float16
NANOCHAT_DTYPE=float16 torchrun --nproc_per_node=8 -m scripts.base_train -- --depth=12
# Note: RL scripts do NOT support float16 (SFT and base_train do)
```

### V100 / T4 (SM < 80) — No bf16

```bash
# Default falls back to float32; optionally use float16
NANOCHAT_DTYPE=float16 torchrun --nproc_per_node=8 -m scripts.base_train -- --depth=12
```

### Chat UI Not Accessible

```bash
# Ensure the port (default 8000) is open in your cloud provider's firewall/security group
# Use the public IP, not localhost:
# http://<PUBLIC_IP>:8000/
```

## Resources

- **DeepWiki Q&A**: https://deepwiki.com/karpathy/nanochat
- **Discussions**: https://github.com/karpathy/nanochat/discussions
- **Discord**: `#nanochat` channel on Karpathy's Discord
- **Leaderboard docs**: `dev/LEADERBOARD.md`
- **Beating GPT-2 guide**: https://github.com/karpathy/nanochat/discussions/481
- **Miniseries v1**: https://github.com/karpathy/nanochat/discussions/420
- **Adding abilities guide**: https://github.com/karpathy/nanochat/discussions/164
