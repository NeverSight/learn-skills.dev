---
name: rasptorch
description: Operate rasptorch (NumPy deep learning library) via its agent-native CLI, consuming JSON output. Supports tensors, model creation (mlp, cnn, cv, jev, gru, transformer, linear), training, save/load, and UI/chat modes.
metadata:
  clawdbot:
    os: [windows, linux]
    requires:
      anyBins: [rasptorch, python, py]
  interface:
    version: "1.0"
    transport: "cli"
    output_format: "json"
    stateful: true
    long_running: [ui, chat]
---

# rasptorch skill

Use this skill to operate **rasptorch** from any agent harness by calling its **agent-native CLI** and consuming structured JSON output.

## Interface contract

| Field | Value |
|-------|-------|
| Transport | CLI (stdout/stderr) |
| Output format | JSON (pass `--json` on every call) |
| Stateful | Yes — model registry persists within a session |
| Long-running | `rasptorch ui` (Streamlit), `rasptorch chat` (REPL) |

### How to invoke

Prefer the installed console script:

```bash
rasptorch --json <command> [args...]
```

If the console script is unavailable, use module invocation from this repo:

```bash
python -m rasptorch.CLI.cli --json <command> [args...]
```

### Backend selection

Always prefer `--backend auto` unless the user asks to pin a specific backend:

- `--backend auto` (default): choose best available backend
- `--backend vulkan`: prefer Vulkan GPU backend
- `--backend opencl`: use OpenCL backend
- `--backend cuda`: use CUDA backend (CuPy or PyTorch CUDA provider)
- `--backend numpy`: CPU backend (internal key: `cpu`)

## Read-only checks

### Environment + GPU status

```bash
rasptorch --json info
```

Key fields: `vulkan_available`, `vulkan_using_real_gpu`, `vulkan_status`.

## Tensor workflows

### Create tensors

```bash
rasptorch --json --backend numpy tensor random --shape 2,3,4 --device cpu --dtype float32
rasptorch --json tensor zeros --shape 3,4 --device auto
rasptorch --json --backend vulkan tensor ones --shape 5,10 --device gpu
```

Notes:
- Keep shapes small unless the user explicitly requests large workloads.
- Prefer `--backend auto` unless the user asks to pin a specific backend.

## Model workflows (stateful)

Model commands keep a session-like registry of created models.

### Create models

```bash
# Linear (single layer)
rasptorch --json model linear --input-size 10 --hidden-sizes 32,16 --output-size 2

# MLP (multi-layer perceptron)
rasptorch --json model mlp --layers 64,32,16,2

# CNN (convolutional network)
rasptorch --json model cnn --in-channels 3 --out-channels 16,32

# CV (computer vision: Conv2d blocks -> Flatten -> Linear)
rasptorch --json model cv --in-channels 3 --out-channels 32,64 --num-classes 10 --input-hw 32

# JEV (decision: MLP outputting a decision vector)
rasptorch --json model jev --input-size 10 --hidden-sizes 32,16 --num-decisions 2

# GRU (gated recurrent unit)
rasptorch --json model gru --input-size 8 --hidden-size 32 --num-layers 1

# Transformer
rasptorch --json model transformer --vocab-size 32000 --d-model 256 --num-heads 8 --num-layers 4
```

### List / remove models

```bash
rasptorch --json model list
rasptorch --json model remove --model-id <model-id>
```

### Save / load (writes files)

Only do this when the user requests it (or approves writing files):

```bash
rasptorch --json model save --model-id <model-id> --path ./model.pkl
rasptorch --json model load --path ./model.pkl
```

### Train (writes compute + may take time)

Only run training after user approval:

```bash
rasptorch --json model train --model-id <model-id> --epochs 5 --lr 0.001 --batch-size 32 --device auto --optimizer Adam
```

## UI / chat modes

- `rasptorch ui` starts a Streamlit server (long-running). Only launch with user approval.
- `rasptorch chat` starts an interactive REPL. Avoid in automated tool flows.

## Error handling

- Non-zero exit code indicates failure; inspect stderr for details.
- JSON output is emitted on stdout; errors may be returned as JSON with an `error` field.
- Always check the exit code before parsing stdout as JSON.

## Capability discovery

Run `rasptorch --json info` to discover available backends, GPU status, and supported commands at runtime.
