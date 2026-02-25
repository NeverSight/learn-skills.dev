---
name: sam3
description: Create and work with Meta SAM 3 (facebookresearch/sam3) for open-vocabulary image and video segmentation with text, point, box, and mask prompts. Use when setting up SAM3 environments, requesting Hugging Face checkpoint access, generating inference scripts, integrating SAM3 into Python apps, fine-tuning with sam3/train configs, running SA-Co or custom evaluations, or debugging CUDA/checkpoint/prompt pipeline issues.
---

# SAM 3 (facebookresearch/sam3)

## Overview

Build, integrate, fine-tune, and evaluate Meta SAM 3 with reproducible commands and minimal setup friction.

## Quick Routing

| User intent | Action |
|---|---|
| Install SAM 3 and run first inference | Follow setup in `references/setup-and-inference.md` |
| Add SAM 3 to an existing Python app | Generate starter code with `scripts/create_inference_starter.py` and adapt API calls |
| Verify environment before setup/inference | Run `scripts/sam3_preflight_check.py` |
| Fine-tune on custom data | Use `references/training-and-eval.md` training flow and config guidance |
| Run SA-Co benchmarks or eval custom predictions | Use eval commands in `references/training-and-eval.md` and upstream `scripts/eval/*` docs |
| Debug runtime failures | Run the troubleshooting checklist in `references/setup-and-inference.md` |

## Core Workflow

1. Confirm objective and modality.
2. Set up environment and checkpoint access.
3. Run a smoke test.
4. Execute the task path: inference, training, or evaluation.
5. Return reproducible commands and file paths.

### 1) Confirm objective and modality

- Identify whether the user needs image inference, video inference, fine-tuning, or benchmark evaluation.
- Confirm whether CUDA is available and which GPU memory budget applies.
- Confirm whether Hugging Face access to `facebook/sam3` is already approved.

### 2) Set up environment and checkpoint access

Use a clean environment:

```bash
conda create -n sam3 python=3.12 -y
conda activate sam3
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
git clone https://github.com/facebookresearch/sam3.git
cd sam3
pip install -e .
```

Authenticate with Hugging Face before first model load:

```bash
hf auth login
```

Optionally run a preflight check before model download:

```bash
python scripts/sam3_preflight_check.py --strict
```

For full setup and verification commands, read `references/setup-and-inference.md`.

### 3) Run a smoke test

From this skill folder, generate a starter script:

```bash
python scripts/create_inference_starter.py --mode image --output ./sam3_smoke.py
```

Edit placeholders and run from a SAM3 checkout.

### 4) Execute the task path

- Image and video inference:
Use `references/setup-and-inference.md` to apply `Sam3Processor` and `build_sam3_video_predictor` patterns.
- Fine-tuning:
Use `references/training-and-eval.md` and start from a provided config in `sam3/train/configs`.
- Benchmark evaluation:
Use `references/training-and-eval.md` plus upstream dataset notes under `scripts/eval/gold`, `scripts/eval/silver`, and `scripts/eval/veval`.

### 5) Return reproducible output

- Report exact commands run and any config overrides.
- Include checkpoint source and authentication assumptions.
- Include prompt text, frame index, and confidence threshold when reporting inference outputs.

## Guardrails

- Do not assume checkpoint access is granted; verify login and permission first.
- Prefer official `sam3.model_builder` and predictor APIs over custom re-implementations.
- Keep generated scripts editable and avoid machine-specific absolute paths.
- If running on CPU, explicitly note expected performance limits before large jobs.

## Resources

- Setup and inference guide: `references/setup-and-inference.md`
- Training and evaluation guide: `references/training-and-eval.md`
- Starter generator: `scripts/create_inference_starter.py`
- Preflight checker: `scripts/sam3_preflight_check.py`
