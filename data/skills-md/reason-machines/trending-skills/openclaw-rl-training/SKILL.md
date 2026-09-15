---
name: openclaw-rl-training
description: OpenClaw-RL framework for training personalized AI agents via reinforcement learning from natural conversation feedback
triggers:
  - train an agent with OpenClaw-RL
  - set up reinforcement learning for my AI agent
  - use GRPO or OPD with OpenClaw
  - configure async RL training pipeline
  - train agent from conversation feedback
  - set up agentic RL for terminal or GUI
  - use on-policy distillation with OpenClaw
  - deploy OpenClaw-RL with Tinker or local GPU
---

# OpenClaw-RL Training

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenClaw-RL is a fully asynchronous reinforcement learning framework that converts live multi-turn conversations into training signals for personalized AI agents. It wraps a self-hosted model as an OpenAI-compatible API via [OpenClaw](https://openclaw.ai), intercepts conversations, and continuously optimizes the policy in the background without interrupting usage. It also supports scalable RL for terminal, GUI, SWE, and tool-call agents.

## Architecture Overview

Four independent async loops that never block each other:
1. **Agent Serving** — OpenClaw-compatible API serving rollouts
2. **Rollout Collection** — Captures multi-turn conversations as training trajectories
3. **PRM/Judge Evaluation** — Scores turns using next-state feedback (majority voting optional)
4. **Policy Training** — GRPO/OPD/Combine training via [slime](https://github.com/THUDM/slime) or [Tinker](https://thinkingmachines.ai/tinker/)

## Installation

```bash
git clone https://github.com/Gen-Verse/OpenClaw-RL
cd OpenClaw-RL

# Install core dependencies
pip install -r requirements.txt

# Install slime (training backend)
cd slime && pip install -e . && cd ..

# Optional: install SGLang for fast inference
pip install sglang
```

## Project Structure

```
OpenClaw-RL/
├── openclaw-rl/          # Binary RL (GRPO) method
├── openclaw-opd/         # On-Policy Distillation method
├── openclaw-combine/     # Combined Binary RL + OPD
├── openclaw-test/        # Evaluation utilities
├── terminal-rl/          # Track 2: Terminal agent RL
├── gui-rl/               # Track 2: GUI agent RL
├── swe-rl/               # Track 2: SWE agent RL
├── toolcall-rl/          # Track 2: Tool-call agent RL
├── slime/                # Core training framework
└── openclaw/             # Runtime / API server
```

## Three Learning Paradigms

### 1. Binary RL (GRPO)
A Process Reward Model scores each turn from next-state feedback. Uses GRPO advantage estimation with PPO-style clipped surrogate loss.

### 2. On-Policy Distillation (OPD)
When next state reveals useful hindsight, a judge extracts a textual hint to augment the prompt, creating an enhanced teacher. Token-level log-probability gap becomes a directional advantage signal.

### 3. Combination Method (Recommended)
Merges Binary RL scalar supervision with OPD token-level directional signal. Strongest and most robust optimization.

## Quick Start — Personal Agent (Track 1)

### Binary RL Launch Script

```bash
# openclaw-rl/run_qwen3_7b_openclaw_rl.sh
export MODEL_PATH=/path/to/qwen3-7b
export DATA_PATH=/path/to/conversation/data
export CKPT_SAVE_DIR=/path/to/checkpoints

bash openclaw-rl/run_qwen3_7b_openclaw_rl.sh
```

### OPD Launch Script

```bash
export MODEL_PATH=/path/to/qwen3-7b
export JUDGE_MODEL_PATH=/path/to/judge-model
export DATA_PATH=/path/to/conversation/data

bash openclaw-opd/run_qwen3_7b_openclaw_opd.sh
```

### Combination Method (One Line)

```bash
# Launch with combined Binary RL + OPD
bash openclaw-combine/run_qwen3_7b_openclaw_combine.sh
```

## Configuration — Key Environment Variables

```bash
# Model configuration
export MODEL_PATH=/path/to/base/model
export JUDGE_MODEL_PATH=/path/to/judge/model   # For OPD
export PRM_MODEL_PATH=/path/to/prm/model       # For Binary RL

# Training configuration
export CKPT_SAVE_DIR=./checkpoints
export CKPT_ARGS="--save-interval 100 --save-dir $CKPT_SAVE_DIR"

# Rollout configuration
export ROLLOUT_ARGS="--rollout-batch-size 64 --num-rollouts-per-prompt 4"

# Optimizer configuration
export OPTIMIZER_ARGS="--lr 1e-6 --weight-decay 0.01 --adam-beta1 0.9 --adam-beta2 0.999"

# GPU partitioning (e.g., 8 GPUs: 4 for training, 4 for rollout)
export TRAIN_GPUS="0,1,2,3"
export ROLLOUT_GPUS="4,5,6,7"

# LoRA (optional, reduces GPU memory)
export LORA_ARGS="--lora-rank 64 --lora-alpha 128 --lora-dropout 0.05"
```

## LoRA Training

```bash
# Add LoRA args to any launch script
export LORA_ARGS="--use-lora --lora-rank 64 --lora-alpha 128"

# Example: LoRA Binary RL
bash openclaw-rl/run_qwen3_7b_lora_openclaw_rl.sh
```

## Custom Loss / Rollout Functions (Plugin API)

The slime framework exposes extension points without modifying core code:

```bash
# Custom loss function
--custom-loss-function-path ./my_method/custom_loss.py

# Custom rollout function  
--rollout-function-path ./my_method/custom_rollout.py

# Custom generation function
--custom-generate-function-path ./my_method/custom_generate.py

# Custom reward model
--custom-rm-path ./my_method/custom_rm.py
```

### Example Custom Loss (TypeScript-style config, Python implementation)

```python
# my_method/custom_loss.py
import torch
from typing import Dict, Any

def compute_loss(
    policy_logits: torch.Tensor,
    reference_logits: torch.Tensor,
    rewards: torch.Tensor,
    advantages: torch.Tensor,
    config: Dict[str, Any]
) -> torch.Tensor:
    """
    Custom GRPO-style loss with clipped surrogate objective.
    """
    # Log-ratio between policy and reference
    log_ratio = policy_logits - reference_logits
    ratio = torch.exp(log_ratio)
    
    clip_range = config.get("clip_range", 0.2)
    
    # PPO-style clipped objective
    clipped = torch.clamp(ratio, 1 - clip_range, 1 + clip_range)
    loss = -torch.min(ratio * advantages, clipped * advantages).mean()
    
    # KL penalty
    kl_coeff = config.get("kl_coeff", 0.01)
    kl_penalty = kl_coeff * log_ratio.mean()
    
    return loss + kl_penalty
```

### Example Custom Reward Model

```python
# my_method/custom_rm.py
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class CustomPRM:
    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, torch_dtype=torch.bfloat16
        )
        self.model.eval()

    def score(self, prompt: str, response: str, next_state: str) -> float:
        """
        Score a turn given prompt, response, and next-state feedback.
        """
        combined = f"Prompt: {prompt}\nResponse: {response}\nOutcome: {next_state}"
        inputs = self.tokenizer(combined, return_tensors="pt", truncation=True, max_length=2048)
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
        
        # Binary reward: positive class probability
        return torch.softmax(logits, dim=-1)[0, 1].item()


def get_reward_model(config):
    return CustomPRM(config["prm_model_path"])
```

## Deploying on Tinker (Cloud)

```bash
# One-line cloud deployment — Hybrid RL, OPD, Binary RL all supported
export TINKER_API_KEY=$TINKER_API_KEY
export TINKER_ENDPOINT=$TINKER_ENDPOINT

# Submit job via Ray
ray job submit --address $TINKER_ENDPOINT \
  --working-dir . \
  -- bash openclaw-combine/run_qwen3_7b_openclaw_combine.sh
```

## Track 2 — General Agentic RL

### Terminal Agent RL

```bash
export ENV_TYPE=terminal
export MAX_STEPS=20
export PARALLEL_ENVS=32   # Number of parallel environment instances

bash terminal-rl/run_terminal_rl.sh
```

### GUI Agent RL

```bash
export ENV_TYPE=gui
export SCREENSHOT_BACKEND=playwright   # or selenium
export PARALLEL_ENVS=16

bash gui-rl/run_gui_rl.sh
```

### Tool-Call Agent RL

```bash
export ENV_TYPE=toolcall
export TOOLS_CONFIG=./toolcall-rl/tools_config.json
export PARALLEL_ENVS=64

bash toolcall-rl/run_toolcall_rl.sh
```

### SWE Agent RL

```bash
export ENV_TYPE=swe
export SWE_BENCH_PATH=/path/to/swe-bench
export PARALLEL_ENVS=8   # SWE environments are heavier

bash swe-rl/run_swe_rl.sh
```

## Data Format — Conversation Trajectories

OpenClaw-RL automatically classifies API messages. Manual format for custom data:

```json
{
  "session_id": "user_session_abc123",
  "turns": [
    {
      "type": "main",
      "prompt": "Help me refactor this function to use async/await",
      "response": "Here's the refactored version: ...",
      "next_state": "User accepted the change and said 'perfect, thanks!'",
      "trainable": true
    },
    {
      "type": "side", 
      "prompt": "What is 2+2?",
      "response": "4",
      "trainable": false
    }
  ]
}
```

- **`main` turns**: Multi-turn interactions that form training trajectories
- **`side` turns**: Non-trainable system/utility turns excluded from training

## OpenClaw API Server Setup

```bash
# Start OpenClaw-compatible API server wrapping your model
export BASE_MODEL_PATH=/path/to/your/model
export OPENCLAW_PORT=8000
export OPENCLAW_HOST=0.0.0.0

# Using SGLang backend (recommended for speed)
python -m openclaw.server \
  --model-path $BASE_MODEL_PATH \
  --port $OPENCLAW_PORT \
  --backend sglang \
  --enable-rl-intercept          # Enable conversation capture for RL
  --rl-buffer-dir ./rl_buffer    # Where to store captured trajectories
```

```typescript
// Using the server as OpenAI-compatible API in TypeScript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:8000/v1",
  apiKey: process.env.OPENCLAW_API_KEY ?? "local",
});

const response = await client.chat.completions.create({
  model: "your-model-name",
  messages: [
    { role: "user", content: "Help me write a sorting algorithm" }
  ],
  stream: true,
});

for await (const chunk of response) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
```

## Majority Voting for Robust PRM Scoring

```bash
# Enable majority voting for more robust reward estimation
export MAJORITY_VOTE_N=5   # Number of judge calls per turn
export MAJORITY_VOTE_THRESHOLD=0.6

# Add to your launch script args:
--majority-vote-n $MAJORITY_VOTE_N \
--majority-vote-threshold $MAJORITY_VOTE_THRESHOLD
```

## Adding a New Method (Contribution Pattern)

```bash
# 1. Create a new top-level folder
mkdir my-new-method
cd my-new-method

# 2. Required files
touch README.md                           # Document what, how, env vars
touch run_qwen3_7b_my_method.sh          # Launch script
touch custom_loss.py                      # If custom loss needed
touch custom_rollout.py                   # If custom rollout needed
```

```bash
# run_qwen3_7b_my_method.sh — follow existing conventions
#!/bin/bash
set -e

MODEL_SIZE="7b"
MODEL_PATH=${MODEL_PATH:-/path/to/qwen3-7b}
CKPT_SAVE_DIR=${CKPT_SAVE_DIR:-./checkpoints/my-method}

CKPT_ARGS="--save-interval 50 --save-dir $CKPT_SAVE_DIR"
ROLLOUT_ARGS="--rollout-batch-size 32 --num-rollouts-per-prompt 4"
OPTIMIZER_ARGS="--lr 1e-6 --weight-decay 0.01"

ray job submit --working-dir .. -- \
  python slime/train.py \
    --model-path $MODEL_PATH \
    --custom-loss-function-path my-new-method/custom_loss.py \
    $CKPT_ARGS $ROLLOUT_ARGS $OPTIMIZER_ARGS
```

## Common Patterns

### Monitor Training Progress

```bash
# View Ray dashboard
ray dashboard  # Opens at http://localhost:8265

# Watch checkpoint saves
watch -n 10 ls -la $CKPT_SAVE_DIR

# Stream training logs
tail -f ./logs/training.log
```

### Resume from Checkpoint

```bash
export RESUME_CKPT=$CKPT_SAVE_DIR/checkpoint-500
# Add to launch script:
--resume-from-checkpoint $RESUME_CKPT
```

### Evaluate Trained Checkpoints

```bash
bash openclaw-test/run_eval.sh \
  --model-path $CKPT_SAVE_DIR/checkpoint-latest \
  --eval-tasks "conversation,coding,tool-use"
```

## Troubleshooting

**Out of GPU memory during rollout + training:**
```bash
# Use LoRA to reduce memory footprint
export LORA_ARGS="--use-lora --lora-rank 32"
# Or reduce parallel environments
export PARALLEL_ENVS=8
# Or use offloading
--offload-optimizer-state
```

**Async loop falling behind (buffer overflow):**
```bash
# Reduce rollout batch size or increase judge throughput
export ROLLOUT_ARGS="--rollout-batch-size 16"
# Or add more judge workers
--num-judge-workers 4
```

**PRM scores all near 0.5 (reward collapse):**
- Verify `next_state` fields contain meaningful feedback signals
- Check judge model prompt template matches expected format
- Try increasing majority vote N: `--majority-vote-n 7`

**SGLang server not starting:**
```bash
# Check SGLang version compatibility
pip install sglang==0.4.x  # Check slime/requirements.txt for pinned version
# Fallback to vLLM backend
--backend vllm
```

**Ray job submission fails:**
```bash
# Start Ray cluster first
ray start --head --num-gpus=$(nvidia-smi -L | wc -l)
# Then submit job
ray job submit --address auto -- bash run.sh
```

## Key References

- [Technical Report (arXiv)](https://arxiv.org/abs/2603.10165)
- [OpenClaw Plugin](https://openclaw.ai)
- [Slime Training Framework](https://github.com/THUDM/slime)
- [Tinker Cloud Platform](https://thinkingmachines.ai/tinker/)
- [SDFT Paper](https://arxiv.org/abs/2601.19897) — integrated in openclaw-opd
- [SDPO Paper](https://arxiv.org/abs/2601.20802) — integrated in openclaw-opd
