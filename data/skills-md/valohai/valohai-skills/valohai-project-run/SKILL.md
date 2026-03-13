---
name: valohai-project-run
description: Create a Valohai project, link it to a local directory, and run executions or pipelines using the Valohai CLI. Use this skill when a user wants to set up a new Valohai project, link an existing project, run a step execution, run a pipeline, watch execution logs, or manage their Valohai project via the CLI. Triggers on mentions of vh project create, vh execution run, vh pipeline run, running on Valohai, or Valohai CLI commands.
license: Apache-2.0
metadata:
  author: valohai
  version: "1.0"
compatibility: Requires valohai-cli installed (pip install valohai-cli). Designed for Claude Code or similar AI coding agents.
---

# Valohai Project Setup and Execution

Set up a Valohai project and run ML steps using the Valohai CLI (`vh`). This covers project creation, linking, running executions, running pipelines, and monitoring jobs.

## Prerequisites

```shell
# Install the CLI
pip install valohai-cli

# Login (interactive)
vh login

# Login with token (for SSO or CI/CD)
vh login --token YOUR_TOKEN

# Login to self-hosted instance
vh login --host https://your-company.valohai.io --token YOUR_TOKEN
```

## Step-by-Step: Project Setup

### 1. Create a New Project

```shell
# Create and link to current directory
vh project create --name my-ml-project

# Create with description
vh project create --name my-ml-project --description "Image classification pipeline"

# Create under an organization (CASE SENSITIVE - must match exactly)
vh project create --name my-ml-project --owner my-org

# Create under an organization team (CASE SENSITIVE)
vh project create --name my-ml-project --owner my-org:ml-team

# Create without linking
vh project create --name my-ml-project --no-link
```

This creates the project on Valohai and links the current directory to it.

### 2. Link to an Existing Project

```shell
# Interactive selection from your projects
vh project link

# Or specify directly
vh project link --project my-org/my-ml-project
```

### 3. Check Project Status

```shell
# See current project link
vh project status

# List all your projects
vh project list

# Open project in browser
vh project open
```

## Step-by-Step: Running Executions

### 1. Run a Step (Ad-hoc)

During development, use `--adhoc` to run local code without Git commits:

```shell
# Basic run with local code
vh execution run train-model --adhoc

# Run and watch logs in real-time
vh execution run train-model --adhoc --watch

# Run with parameter overrides
vh execution run train-model --adhoc --epochs=100 --learning_rate=0.0001

# Run with input overrides
vh execution run train-model --adhoc --training-data=s3://bucket/new-data.csv

# Run with specific Docker image override
vh execution run train-model --adhoc --image pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Run with environment override
vh execution run train-model --adhoc --environment aws-eu-west-1-p3-2xlarge

# Run with tags
vh execution run train-model --adhoc --tag experiment-v2 --tag baseline

# Run with title
vh execution run train-model --adhoc --title "Baseline experiment with new data"

# Run with environment variables
vh execution run train-model --adhoc --var WANDB_MODE=disabled

# Combine multiple options
vh execution run train-model --adhoc --watch \
  --epochs=100 \
  --learning_rate=0.0001 \
  --training-data=s3://bucket/v2/train.csv \
  --tag baseline-v2
```

### 2. Run from a Git Commit

When code is committed and pushed:

```shell
# Run from latest fetched commit
vh execution run train-model

# Run from specific commit
vh execution run train-model --commit abc123

# Run from a branch/tag
vh execution run train-model --commit main
```

### 3. Monitor Executions

```shell
# List recent executions
vh execution list
vh execution list --count 10

# Stream logs from an execution
vh execution logs <counter-or-id> --stream

# Watch a running execution
vh execution watch <counter-or-id>

# Get execution details
vh execution info <counter-or-id>

# Open execution in browser
vh execution open <counter-or-id>

# List execution outputs
vh execution outputs <counter-or-id>

# Download outputs
vh execution outputs <counter-or-id> --download ./local-dir/

# Stop a running execution
vh execution stop <counter-or-id>
```

### 4. See Available Steps

```shell
# List steps in current commit
vh execution run
# (Without a step name, it shows available steps)
```

## Step-by-Step: Running Pipelines

### 1. Run a Pipeline

```shell
# Run pipeline with local code
vh pipeline run my-pipeline --adhoc

# Run from Git
vh pipeline run my-pipeline

# Run with title and tags
vh pipeline run my-pipeline --adhoc --title "Full training run" --tag weekly

# Override node parameters
vh pipeline run my-pipeline --adhoc --train-node.epochs=200

# Override node inputs
vh pipeline run my-pipeline --adhoc --train-node.dataset=s3://bucket/v2/

# Override pipeline-level parameters
vh pipeline run my-pipeline --adhoc --learning_rate=0.0001

# Override environment for all nodes
vh pipeline run my-pipeline --adhoc --environment aws-eu-west-1-p3-2xlarge
```

### 2. Monitor Pipelines

```shell
# List pipelines
vh pipeline list

# Stop a pipeline
vh pipeline stop <counter-or-id>
```

### 3. Debug Failed Pipeline Executions

**CRITICAL: Pipeline numbers and execution numbers are different things.** A pipeline contains multiple executions (one per node). When a pipeline fails, you must find and inspect the **specific failed execution**, not the pipeline itself.

```shell
# WRONG - this is the pipeline number, not an execution number
vh execution logs 42 --stream

# CORRECT workflow:
# 1. Open the pipeline in the browser to see which node failed
vh pipeline list

# 2. List executions to find the ones belonging to your pipeline
vh execution list

# 3. Stream logs from the specific EXECUTION that failed (not the pipeline number)
vh execution logs <execution-counter> --stream

# 4. Get details about the failed execution
vh execution info <execution-counter>
```

Each node in a pipeline creates its own execution with its own counter number. Always use the execution counter (visible in the execution list or the web UI) when fetching logs, not the pipeline counter.

## Step-by-Step: Complete Workflow

Here's the full workflow from zero to running:

```shell
# 1. Create project directory
mkdir my-ml-project && cd my-ml-project

# 2. Create Valohai project
vh project create --name my-ml-project

# 3. Create your training script (train.py)
# 4. Create valohai.yaml (see valohai-yaml-step skill)

# 5. Validate the YAML
vh lint

# 6. Run your first execution
vh execution run train-model --adhoc --watch

# 7. View results in browser
vh execution open

# 8. Run with different parameters
vh execution run train-model --adhoc --watch --epochs=100 --learning_rate=0.0001

# 9. Once satisfied, commit and push code
git add . && git commit -m "Add Valohai configuration"
git push origin main

# 10. Fetch latest commit on Valohai
vh project fetch

# 11. Run from Git (reproducible)
vh execution run train-model --watch
```

## YAML Management

**IMPORTANT**: Always run `vh lint` after any change to `valohai.yaml`. This is the first thing to try when executions fail due to configuration issues. It validates syntax, checks references, and catches common mistakes.

```shell
# Validate valohai.yaml - run this after every YAML change
vh lint

# Generate YAML step from a Python file (if using valohai-utils)
vh yaml step train.py

# Generate pipeline YAML from Python pipeline definition
vh yaml pipeline pipeline.py
```

## Other Useful Commands

```shell
# List available environments
vh environments

# List project commits
vh project commits

# List data/files in the project
vh data list

# List project aliases
vh alias list

# Manage environment variables
vh project env-var list
vh project env-var create MY_VAR=value
vh project env-var delete MY_VAR

# List tasks (hyperparameter sweeps)
vh task list
vh task stop <id>
```

## Common Workflows

### Quick Iteration Loop

```shell
# Edit code → run → check results → repeat
vh execution run train-model --adhoc --watch
# (Make changes to code)
vh execution run train-model --adhoc --watch --epochs=200
```

### Hyperparameter Comparison

```shell
# Run multiple experiments
vh execution run train-model --adhoc --tag lr-001 --learning_rate=0.001
vh execution run train-model --adhoc --tag lr-0001 --learning_rate=0.0001
vh execution run train-model --adhoc --tag lr-00001 --learning_rate=0.00001

# Compare in the web UI
vh project open
```

### Pipeline Development

```shell
# Test individual steps first
vh execution run preprocess-data --adhoc --watch
vh execution run train-model --adhoc --watch

# Then run the full pipeline
vh pipeline run training-pipeline --adhoc
```

## Edge Cases

- `--adhoc` packages and uploads your local working directory - ensure no large files or secrets are present (use `.valohaiignore` to exclude files)
- Parameters and inputs are passed as `--name=value` after the step name
- The CLI auto-detects parameters vs inputs: URLs (containing `://`) are treated as input overrides
- Without `--watch`, the command returns immediately after queuing the execution
- `vh lint` validates YAML syntax but doesn't check if Docker images or environments exist
- For remote-only projects (no local Git), omit `--adhoc` and use `--commit`
