---
name: valohai-yaml-step
description: Create valohai.yaml step definitions for ML projects. Use this skill when a user wants to define a new step in valohai.yaml, configure Docker images, set up commands, define parameters/inputs for a step, or create a complete valohai.yaml from scratch for their ML project. Triggers on mentions of valohai.yaml, step definition, YAML configuration, Docker image selection, or creating Valohai steps.
license: Apache-2.0
metadata:
  author: valohai
  version: "1.0"
compatibility: Requires Python. Designed for Claude Code or similar AI coding agents.
---

# Create Valohai YAML Steps

Create and configure `valohai.yaml` step definitions that describe how ML code should run on Valohai. A step defines the Docker image, commands, parameters, and inputs for an execution.

## Philosophy

The `valohai.yaml` file is the single source of truth for your ML workflows. It lives in the repository root and is version-controlled alongside your code. Your code stays framework-agnostic and portable - all platform configuration is in this file.

## Step-by-Step Instructions

### Design Principle: Steps Should Run Independently

**IMPORTANT**: Every step should be runnable on its own, without relying on a pipeline to provide its inputs. Whenever possible, set a `default` value for inputs so users can test and debug individual steps via `vh execution run step-name --adhoc` without needing to run the full pipeline first. Pipeline edges override these defaults at runtime.

Look for default values in the existing code, README, documentation, config files, or data paths already referenced in the project. Only add a default if you can find a real, meaningful value. Do not invent placeholder URLs or dummy paths.

### 1. Analyze the Project

Before creating the YAML, understand the project:

- **What scripts exist?** (train.py, preprocess.py, evaluate.py, infer.py)
- **What framework?** (PyTorch, TensorFlow, scikit-learn, XGBoost, HuggingFace, etc.)
- **What Python version?** (Check pyproject.toml, setup.py, .python-version)
- **What dependencies?** (requirements.txt, pyproject.toml, conda environment)
- **Does it need GPU?** (CUDA imports, torch.cuda, tf.config)
- **What are the inputs?** (datasets, pretrained models, config files)
- **What are the outputs?** (trained models, metrics, plots, predictions)
- **What are the configurable values?** (hyperparameters, paths, flags)

### 2. Choose the Docker Image

Select an appropriate base image:

| Framework | CPU Image | GPU Image |
|-----------|-----------|-----------|
| Python only | `python:3.11` | N/A |
| TensorFlow | `tensorflow/tensorflow:2.15.0` | `tensorflow/tensorflow:2.15.0-gpu` |
| PyTorch | `pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime` | Same (includes CUDA) |
| HuggingFace | `huggingface/transformers-pytorch-gpu:latest` | Same |
| scikit-learn | `python:3.11` | N/A |
| R | `r-base:4.3.0` | N/A |
| Custom | Your own Docker image from a registry | Your own Docker image |

**Guidelines:**
- The Docker image is the execution environment, not your code container
- Don't include your code or data in the image
- Pin version tags for reproducibility (avoid `latest`)
- If using GPU, choose an image with the right CUDA version

### 3. Install Dependencies in Commands

**IMPORTANT**: The Docker image is a clean base environment. Your project's dependencies (from `requirements.txt`, `pyproject.toml`, `environment.yml`, etc.) are NOT pre-installed. You must install them as part of the step commands BEFORE running your script, otherwise you'll get `ModuleNotFoundError`.

Look for dependency files in the project:

| File Found | Install Command |
|------------|----------------|
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` (with pip) | `pip install .` or `pip install -e .` |
| `pyproject.toml` (with uv) | `pip install uv && uv pip install --system .` |
| `setup.py` | `pip install .` |
| `environment.yml` (conda) | `conda env update -n base -f environment.yml` |
| `Pipfile` | `pip install pipenv && pipenv install` |
| Inline dependencies | `pip install torch numpy pandas ...` |

Always place install commands before any Python script execution in the `command` list.

### 4. Keep Commands Simple — Use Helper Scripts

**IMPORTANT**: Step commands in `valohai.yaml` must be simple and human-readable. Never put bash loops, inline Python one-liners, complex piped commands, or multi-line logic directly in the `command` list.

If a step needs non-trivial setup or orchestration logic (e.g., downloading extra resources, converting formats, running multiple sub-steps), **create a helper Python script** in a `valohai/` folder and call it from the command:

```yaml
# WRONG - complex logic crammed into commands
command:
  - pip install -r requirements.txt
  - for f in /valohai/inputs/data/*.tar; do tar xf "$f" -C /tmp/data; done
  - python -c "import os; [os.rename(f, f.lower()) for f in os.listdir('/tmp/data')]"
  - python train.py {parameters}

# CORRECT - clean commands, logic lives in a helper script
command:
  - pip install -r requirements.txt
  - python valohai/prepare_data.py
  - python train.py {parameters}
```

The helper script `valohai/prepare_data.py` contains the extraction and renaming logic. This keeps the YAML readable, the logic testable, and avoids shell quoting nightmares.

**Rule of thumb**: If a command line is longer than ~80 characters or uses shell control flow (loops, conditionals, subshells), move it to a helper script.

### 5. Create the Step Definition

#### Minimal Step

```yaml
- step:
    name: train-model
    image: python:3.11
    command:
      - pip install -r requirements.txt
      - python train.py
```

#### Complete Step with All Options

```yaml
- step:
    name: train-model
    description: Train a classification model on the prepared dataset
    category: Training
    image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
    environment: aws-eu-west-1-p3-2xlarge
    command:
      - pip install -r requirements.txt
      - python train.py {parameters}
    parameters:
      - name: epochs
        type: integer
        default: 50
        description: Number of training epochs
      - name: learning_rate
        type: float
        default: 0.001
        min: 0.00001
        max: 0.1
        description: Initial learning rate
      - name: batch_size
        type: integer
        default: 32
        choices: [8, 16, 32, 64, 128, 256]
      - name: model_type
        type: string
        default: resnet50
        choices: [resnet18, resnet50, resnet101, efficientnet_b0]
      - name: use_augmentation
        type: flag
        default: true
        pass-true-as: --use_augmentation=True
        pass-false-as: --use_augmentation=False
    inputs:
      - name: training-data
        default: s3://my-bucket/datasets/train/
      - name: validation-data
        default: s3://my-bucket/datasets/val/
      - name: pretrained-model
        optional: true
    time-limit: 2h
    no-output-timeout: 30m
```

### 5. Step Properties Reference

#### Required Properties

| Property | Description |
|----------|-------------|
| `name` | Unique step identifier. Used in CLI: `vh exec run <name>` |
| `image` | Docker image for the execution environment |
| `command` | Command(s) to run. String or list of strings |

#### Optional Properties

| Property | Description |
|----------|-------------|
| `description` | Help text shown in UI |
| `category` | Group steps in UI (e.g., "Training", "Preprocessing") |
| `environment` | Default compute environment (ID or name substring) |
| `parameters` | Configurable values (see parameter migration skill) |
| `inputs` | Data files to download before execution |
| `time-limit` | Max execution time (`"2h"`, `"1h 30m"`, or seconds) |
| `no-output-timeout` | Kill if no stdout for this duration |
| `environment-variables` | Environment variables with defaults |
| `environment-variable-groups` | Groups of env vars to include |
| `stop-condition` | Auto-stop condition based on metrics (e.g., `accuracy >= 0.99`) |
| `upload-store` | Override default output data store |
| `resources` | Kubernetes resource requests/limits |

### 6. Multi-Step YAML

Most ML projects have multiple steps:

```yaml
# Preprocessing step
- step:
    name: preprocess-data
    image: python:3.11
    command:
      - pip install pandas numpy scikit-learn
      - python preprocess.py {parameters}
    parameters:
      - name: test_split
        type: float
        default: 0.2
      - name: random_seed
        type: integer
        default: 42
    inputs:
      - name: raw-data
        default: s3://bucket/raw-data.csv

# Training step
- step:
    name: train-model
    image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
    command:
      - pip install -r requirements.txt
      - python train.py {parameters}
    parameters:
      - name: epochs
        type: integer
        default: 50
      - name: learning_rate
        type: float
        default: 0.001
      - name: batch_size
        type: integer
        default: 32
    inputs:
      - name: dataset
        default: s3://bucket/processed/
      - name: pretrained-model
        optional: true

# Evaluation step
- step:
    name: evaluate-model
    image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
    command:
      - pip install -r requirements.txt
      - python evaluate.py
    inputs:
      - name: model
        default: datum://latest-trained-model
      - name: test-data
        default: s3://bucket/test/

# Batch inference step
- step:
    name: batch-inference
    image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
    command:
      - pip install -r requirements.txt
      - python inference.py
    inputs:
      - name: model
        default: datum://production-model
      - name: data
        default: s3://bucket/inference-data/
```

### 7. Command Patterns

```yaml
# Single command
command: python train.py

# Multiple commands (run sequentially)
command:
  - pip install -r requirements.txt
  - python preprocess.py
  - python train.py {parameters}

# PARAMETER SYNTAX - uses COLONS, not brackets or parentheses
#
# {parameters}              → all params as --name=value
# {parameter:name}          → one param as --name=value
# {parameter-value:name}    → one param as raw value only
#
# WRONG: {parameter-value[name]} {parameter[name]} {parameter(name)}
# RIGHT: {parameter-value:name}  {parameter:name}  (always use colons!)

# {parameters} - expands ALL parameters with --name=value format (preferred)
command:
  - python train.py {parameters}
# Expands to: python train.py --epochs=50 --learning_rate=0.001

# {parameter:name} - ONE parameter as --name=value (standalone, never after --)
command:
  - python train.py --model /valohai/inputs/model/*.onnx {parameter:conf} {parameter:iou}
# Expands to: python train.py --model /valohai/inputs/model/*.onnx --conf=0.5 --iou=0.7

# {parameter-value:name} - ONE parameter as RAW VALUE ONLY (no --name= prefix)
command:
  - python train.py --threshold {parameter-value:threshold}
# Expands to: python train.py --threshold 0.5

# WRONG - never combine --flag={parameter:name}, it double-wraps the argument
# --conf={parameter:conf} expands to --conf=--conf=0.5 which BREAKS argparse

# Install from different sources
command:
  - DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y libgl1-mesa-glx
  - pip install -r requirements.txt
  - python train.py

# Conditional commands
command:
  - pip install -r requirements.txt
  - python preprocess.py && python train.py {parameters}
```

**IMPORTANT: Non-interactive commands and shell isolation.**

Each YAML list item runs in a **separate shell**. This means `export` on one line does NOT carry over to the next. Chain commands that share environment on the same line:

```yaml
# WRONG - export doesn't carry to the next line (separate shells)
command:
  - export DEBIAN_FRONTEND=noninteractive
  - apt-get update && apt-get install -y tzdata   # WILL STILL PROMPT

# CORRECT - chain export on the same line so it applies to both commands
command:
  - DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
  - pip install -r requirements.txt
  - python train.py {parameters}
```

Always use `-y` (or `--yes`) and `DEBIAN_FRONTEND=noninteractive` with `apt-get install`. Executions run unattended - any interactive prompt will hang the execution indefinitely.

### 8. Environment Variables

```yaml
- step:
    name: train-model
    image: python:3.11
    command:
      - python train.py
    environment-variables:
      - name: WANDB_MODE
        default: disabled
        description: Disable W&B logging on Valohai
      - name: HF_HOME
        default: /valohai/inputs/hf-cache/
    environment-variable-groups:
      - secret-api-keys-group-uuid
```

### 9. Resource Configuration (Kubernetes)

```yaml
- step:
    name: train-large-model
    image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
    command:
      - python train.py
    resources:
      cpu:
        min: 4
        max: 8
      memory:
        min: 16384  # MB
        max: 32768
      devices:
        nvidia.com/gpu: 1
```

## Common Patterns by Project Type

### Computer Vision

```yaml
- step:
    name: train-detector
    image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
    command:
      - pip install ultralytics
      - python train.py {parameters}
    parameters:
      - name: epochs
        type: integer
        default: 100
      - name: img_size
        type: integer
        default: 640
      - name: batch_size
        type: integer
        default: 16
    inputs:
      - name: dataset
        keep-directories: suffix
```

### NLP/LLM Fine-tuning

```yaml
- step:
    name: finetune-llm
    image: huggingface/transformers-pytorch-gpu:latest
    command:
      - pip install peft bitsandbytes
      - python finetune.py {parameters}
    parameters:
      - name: model_name
        type: string
        default: meta-llama/Llama-2-7b-hf
      - name: lora_r
        type: integer
        default: 16
      - name: learning_rate
        type: float
        default: 0.0002
      - name: num_train_epochs
        type: integer
        default: 3
    inputs:
      - name: training-data
    environment-variables:
      - name: HF_TOKEN
        optional: false
```

### Data Pipeline

```yaml
- step:
    name: etl-pipeline
    image: python:3.11
    command:
      - pip install pandas pyarrow
      - python etl.py {parameters}
    parameters:
      - name: date_from
        type: string
        default: "2024-01-01"
      - name: date_to
        type: string
        default: "2024-12-31"
    inputs:
      - name: raw-data
        default: s3://data-lake/raw/
        keep-directories: suffix
```

## Validation

**IMPORTANT**: Always run `vh lint` after creating or modifying `valohai.yaml`. This validates the YAML syntax, checks parameter types, verifies input/output definitions, and catches common mistakes before you attempt to run anything.

```shell
vh lint
```

If `vh lint` reports errors, fix them before proceeding. Common issues:
- Indentation errors (YAML is whitespace-sensitive)
- Missing required fields (`name`, `image`, `command`)
- Invalid parameter types (must be `integer`, `float`, `string`, or `flag`)
- Duplicate step or parameter names
- Invalid `pass-as` format strings

Once lint passes, test with a run:

```shell
vh execution run step-name --adhoc --watch
```

## Edge Cases

- The `valohai.yaml` file must be in the repository root
- Step names must be unique within the YAML file
- Step names can contain letters, numbers, spaces, hyphens, and parentheses
- If `{parameters}` is not in the command, parameters are appended to the last command
- Multiple YAML files can be used via imports (see Valohai docs on multi-file YAML)
- Commands run sequentially; if one fails, subsequent commands don't execute
- The working directory inside the container is `/valohai/repository/`
- Each YAML command list item runs in a separate shell - `export` on one line won't carry to the next
- Always use non-interactive flags (`-y`, `DEBIAN_FRONTEND=noninteractive`) for package installs - executions have no TTY
