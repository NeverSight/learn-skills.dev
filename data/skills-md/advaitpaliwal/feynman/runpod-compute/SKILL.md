---
name: runpod-compute
description: Provision and manage GPU pods on RunPod for explicitly chosen long-running research experiments. Use when a Feynman replication, benchmark, or dataset-heavy research run needs persistent GPU compute with SSH access.
---

# RunPod Compute

Use `runpodctl` CLI for persistent GPU pods with SSH access during a specific research run. Do not use this skill for provider administration outside that run; tie every pod to a replication, benchmark, or dataset-heavy research objective.

## Setup

```bash
brew install runpod/runpodctl/runpodctl   # macOS
runpodctl config --apiKey=YOUR_KEY
```

## Commands

| Command | Description |
|---------|-------------|
| `runpodctl create pod --gpuType "NVIDIA A100 80GB PCIe" --imageName "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04" --name experiment` | Create a pod |
| `runpodctl get pod` | List all pods |
| `runpodctl stop pod <id>` | Stop (preserves volume) |
| `runpodctl start pod <id>` | Resume a stopped pod |
| `runpodctl remove pod <id>` | Terminate and delete |
| `runpodctl gpu list` | List available GPU types and prices |
| `runpodctl send <file>` | Transfer files to/from pods |
| `runpodctl receive <code>` | Receive transferred files |

## SSH access

```bash
ssh root@<IP> -p <PORT> -i ~/.ssh/id_ed25519
```

Get connection details from `runpodctl get pod <id>`. Pods must expose port `22/tcp`.

## GPU types

`NVIDIA GeForce RTX 4090`, `NVIDIA RTX A6000`, `NVIDIA A40`, `NVIDIA A100 80GB PCIe`, `NVIDIA H100 80GB HBM3`

## When to use

- Long-running research experiments needing persistent state
- Large research datasets required by a replication or benchmark
- Multi-step research work with SSH access between iterations
- Always stop or remove pods after experiments
- Check availability: `command -v runpodctl`
