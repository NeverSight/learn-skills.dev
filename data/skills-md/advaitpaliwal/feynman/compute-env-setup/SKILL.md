---
name: compute-env-setup
description: Set up a reproducible Feynman compute environment for research jobs. Use when a task needs Python/R packages, GPU libraries, containers, Modal, SSH, caches, or managed model runtime setup.
---

# Compute Environment Setup

Use this skill before running a research job that needs a nontrivial runtime.

Workflow:

1. Identify the job type, hardware need, data size, package stack, secrets, and expected artifacts.
2. Choose the smallest working route: local notebook runtime, project virtualenv/conda, Modal, SSH/Slurm, or managed endpoint.
3. Verify credentials and CLIs through Feynman Settings or environment status without printing secret values.
4. Write an environment note containing package versions, install commands, cache paths, hardware, and failure modes.
5. Run a tiny smoke job before the expensive job and save the smoke logs.

The done state is a recorded, reproducible environment plus a successful smoke or a precise missing dependency.
