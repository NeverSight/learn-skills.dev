---
name: docker
description: Execute research code inside isolated Docker containers for safe replication, experiments, and benchmarks. Use when the user selects Docker as the execution environment or asks to run code safely, in isolation, or in a sandbox.
allowed-tools: Bash(docker:*)
---

# Docker Sandbox

Run research code inside Docker containers while Feynman stays on the host. The container gets the project files, runs the commands, and results sync back.

## When to use

- User selects "Docker Sandbox" as the execution environment in `/replicate` or `/autoresearch`
- Running untrusted code from a paper's repository
- Experiments that install packages or modify system state
- Any time the user asks to run research code safely or isolated for a Feynman workflow

## How it works

1. Build or pull an appropriate base image for the research code
2. Mount the project directory into the container
3. Run experiment commands inside the container
4. Results write back to the mounted directory

## Running commands in a container

For Python research code (most common):

```bash
docker run --rm -v "$(pwd)":/workspace -w /workspace python:3.11 bash -c "
  pip install -r requirements.txt &&
  python train.py
"
```

For projects with a Dockerfile:

```bash
docker build -t feynman-experiment .
docker run --rm -v "$(pwd)/results":/workspace/results feynman-experiment
```

For GPU workloads:

```bash
docker run --rm --gpus all -v "$(pwd)":/workspace -w /workspace pytorch/pytorch:latest bash -c "
  pip install -r requirements.txt &&
  python train.py
"
```

## Choosing the base image

| Research type | Base image |
| --- | --- |
| Python ML/DL | `pytorch/pytorch:latest` or `tensorflow/tensorflow:latest-gpu` |
| Python general | `python:3.11` |
| Node.js | `node:20` |
| R / statistics | `rocker/r-ver:4` |
| Julia | `julia:1.10` |
| Multi-language | `ubuntu:24.04` with manual installs |

## Persistent containers

For iterative experiments (like `/autoresearch`), create a named container instead of `--rm`. Choose a descriptive name based on the experiment:

```bash
docker create --name <name> -v "$(pwd)":/workspace -w /workspace python:3.11 tail -f /dev/null
docker start <name>
docker exec <name> bash -c "pip install -r requirements.txt"
docker exec <name> bash -c "python train.py"
```

This preserves installed packages across iterations. Clean up with:

```bash
docker stop <name> && docker rm <name>
```

## Notes

- The mounted workspace syncs results back to the host automatically
- Containers are network-enabled by default — add `--network none` for full isolation
- For GPU access, Docker must be configured with the NVIDIA Container Toolkit
