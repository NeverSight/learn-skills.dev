---
name: modal-compute
description: Run explicitly chosen research benchmark or replication jobs on Modal's serverless infrastructure. Use when a Feynman research workflow needs burst remote GPU compute and the Modal CLI is available.
---

# Modal Compute

Use the `modal` CLI for bounded research experiments that need burst GPU compute. No pod lifecycle to manage; write a decorated Python script, run it, and save raw outputs back into the research artifact folder. Do not use this skill to deploy services or unrelated batch jobs.

## Setup

```bash
pip install modal
modal setup
```

## Commands

| Command | Description |
|---------|-------------|
| `modal run script.py` | Run one research experiment script on Modal |
| `modal run --detach script.py` | Run a long research experiment and record the returned app/run identifier |
| `modal shell --gpu a100` | Open an interactive GPU shell for research environment debugging |

## GPU types

`T4`, `L4`, `A10G`, `L40S`, `A100`, `A100-80GB`, `H100`, `H200`, `B200`

Multi-GPU: `"H100:4"` for 4x H100s.

## Script pattern

```python
import modal

app = modal.App("experiment")
image = modal.Image.debian_slim(python_version="3.11").pip_install("torch==2.8.0")

@app.function(gpu="A100", image=image, timeout=600)
def train():
    import torch
    # training code here

@app.local_entrypoint()
def main():
    train.remote()
```

## When to use

- Bounded replication or benchmark jobs that need burst GPU
- No persistent state needed between runs
- Check availability: `command -v modal`
