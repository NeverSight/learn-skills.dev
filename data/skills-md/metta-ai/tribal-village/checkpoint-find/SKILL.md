---
name: checkpoint-find
description: "Locate the latest checkpoint for a run id and provide a follow-up play/eval command. Use when asked to find a checkpoint."
---

# Checkpoint Find

## Workflow
- Identify the run id or run directory.
- Locate the latest checkpoint file (for example under `train_dir/.../checkpoints`).
- Return the checkpoint path and a follow-up play/eval command tailored to the request.
