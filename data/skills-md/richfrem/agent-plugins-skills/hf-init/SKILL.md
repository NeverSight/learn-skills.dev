---
name: hf-init
description: "Initialize HuggingFace integration - validates .env variables, tests API connectivity, and ensures the dataset repository structure exists. Use when onboarding a new project to HuggingFace or when credentials change."
allowed-tools: Bash, Read
dependencies: ["pip:hf_upload"]
---
# HuggingFace Init (Onboarding)

**Status:** Active
**Author:** Richard Fremmerlid
**Domain:** HuggingFace Integration

## Purpose

Sets up everything needed for HuggingFace persistence. Run this once when
onboarding a new project, or whenever credentials change.

## What It Does

1. **Validates** required `.env` variables are set
2. **Tests** API connectivity with the configured token
3. **Ensures** the dataset repository exists on HF Hub
4. **Creates** the standard folder structure (`lineage/`, `data/`, `metadata/`)
5. **Uploads** the dataset card (README.md) with configurable discovery tags

## Required Environment Variables

| Variable | Required | Description |
|:---------|:---------|:------------|
| `HUGGING_FACE_USERNAME` | ✅ Yes | Your HF username |
| `HUGGING_FACE_TOKEN` | ✅ Yes | API token (set in `~/.zshrc`, NOT `.env`) |
| `HUGGING_FACE_REPO` | ✅ Yes | Model repo name |
| `HUGGING_FACE_DATASET_PATH` | ✅ Yes | Dataset repo name |
| `HUGGING_FACE_TAGS` | ❌ No | Comma-separated discovery tags for dataset card |
| `HUGGING_FACE_PROJECT_NAME` | ❌ No | Pretty name for dataset card heading |
| `SOUL_VALENCE_THRESHOLD` | ❌ No | Moral/emotional charge filter (default: `-0.7`) |

## Usage

### Validate Config
```bash
python ./scripts/hf_config.py
```

### Full Init (Validate + Create Structure + Dataset Card)
```bash
python ./scripts/hf_init.py
```

### Validate Only (No Changes)
```bash
python ./scripts/hf_init.py --validate-only
```

## Quick Setup

```bash
# Token goes in shell profile (never committed):
export HUGGING_FACE_TOKEN=hf_xxxxxxxxxxxxx

# Project vars go in .env:
HUGGING_FACE_USERNAME=<your-username>
HUGGING_FACE_REPO=<your-model-repo>
HUGGING_FACE_DATASET_PATH=<your-dataset-repo>

# Optional customization:
HUGGING_FACE_TAGS=reasoning-traces,cognitive-continuity,your-project-tag
HUGGING_FACE_PROJECT_NAME=My Project Soul

# Run init
python ./scripts/hf_init.py
```
