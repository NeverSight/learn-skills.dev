---
name: together-fine-tuning
description: Fine-tune open-source LLMs on Together AI with LoRA, Full fine-tuning, DPO preference tuning, VLM (vision-language) fine-tuning, and Bring Your Own Model (BYOM). Supports 30+ models including Llama, Qwen, DeepSeek, Gemma, Mistral. Use when users want to train, fine-tune, customize, adapt, or specialize language models on custom data.
---

# Together Fine-Tuning

## Overview

Fine-tune models on Together AI with a complete workflow: prepare data, upload, train, monitor, deploy.

**Methods:**
- **LoRA** (recommended): Trains small subset of weights — faster, cheaper, enables serverless LoRA inference
- **Full fine-tuning**: Updates all weights — maximum customization, higher cost
- **DPO (Preference)**: Trains on preferred vs non-preferred output pairs
- **VLM fine-tuning**: Fine-tune vision-language models on image+text data

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## Quick Start

### 1. Prepare Data

Conversational format (most common):

```jsonl training_data.jsonl
{"messages": [{"role": "system", "content": "You are helpful."}, {"role": "user", "content": "What is AI?"}, {"role": "assistant", "content": "AI is artificial intelligence."}]}
{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi! How can I help?"}]}
```

### 2. Upload and Check

```python
from together import Together
client = Together()

# Check format
from together.utils import check_file
report = check_file("training_data.jsonl")
assert report["is_check_passed"]

# Upload
file_resp = client.files.upload(file="training_data.jsonl", purpose="fine-tune", check=True)
print(file_resp.id)
```

```typescript
import { upload } from "together-ai/lib/upload";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const filepath = path.join(__dirname, "training_data.jsonl");
const file = await upload(filepath);
console.log(file.id);
```

```shell
# Upload file
curl "https://api.together.xyz/v1/files/upload" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -F "file=@training_data.jsonl" \
  -F "file_name=training_data.jsonl" \
  -F "purpose=fine-tune"
```

```shell
# CLI: check and upload
together files check "training_data.jsonl"
together files upload "training_data.jsonl"
```

### 3. Start LoRA Fine-Tuning (Recommended)

```python
job = client.fine_tuning.create(
    training_file=file_resp.id,
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Reference",
    lora=True,
    n_epochs=3,
    learning_rate=1e-5,
    suffix="my-model-v1",
)
print(job.id)
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.fineTuning.create({
  model: "meta-llama/Meta-Llama-3.1-8B-Instruct-Reference",
  training_file: "file-abc123",
});
console.log(response.id);
```

```shell
curl -X POST "https://api.together.xyz/v1/fine-tunes" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Reference",
    "training_file": "file-abc123",
    "n_epochs": 3,
    "learning_rate": 1e-5,
    "suffix": "my-model-v1"
  }'
```

```shell
# CLI
together fine-tuning create \
  --training-file "file-abc123" \
  --model "meta-llama/Meta-Llama-3.1-8B-Instruct-Reference" \
  --lora \
  --n-epochs 3 \
  --learning-rate 1e-5 \
  --suffix "my-model-v1"
```

### 4. Monitor

```python
status = client.fine_tuning.retrieve(job.id)
print(status.status)  # Pending → Queued → Running → Uploading → Completed

for event in client.fine_tuning.list_events(id=job.id).data:
    print(event.message)
```

```typescript
import Together from "together-ai";
const together = new Together();

const fineTune = await together.fineTuning.retrieve("ft-abc123");
console.log(fineTune.status);

const events = await together.fineTuning.listEvents("ft-abc123");
console.log(events);
```

```shell
curl "https://api.together.xyz/v1/fine-tunes/ft-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"

# List events
curl "https://api.together.xyz/v1/fine-tunes/ft-abc123/events" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json"
```

```shell
# CLI: status and events
together fine-tuning status ft-abc123
together fine-tuning list-events ft-abc123
together fine-tuning retrieve ft-abc123
```

### 5. Use Fine-Tuned Model

**Serverless LoRA** (immediate, no deployment):
```python
response = client.chat.completions.create(
    model=job.output_name,
    messages=[{"role": "user", "content": "Hello!"}],
)
```

**Dedicated Endpoint**:
```python
endpoint = client.endpoints.create(
    display_name="My Fine-tuned Model",
    model=job.output_name,
    hardware="4x_nvidia_h100_80gb_sxm",
    autoscaling={"min_replicas": 1, "max_replicas": 1},
)
```

## Full Fine-Tuning

```python
job = client.fine_tuning.create(
    training_file=file_resp.id,
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Reference",
    lora=False,  # Must explicitly set False
    n_epochs=3,
    learning_rate=1e-5,
    suffix="full-ft-v1",
)
```

```shell
# CLI: use --no-lora for full fine-tuning
together fine-tuning create \
  --training-file "file-abc123" \
  --model "meta-llama/Meta-Llama-3.1-8B-Instruct-Reference" \
  --no-lora \
  --n-epochs 3 \
  --learning-rate 1e-5 \
  --suffix "full-ft-v1"
```

## DPO Preference Fine-Tuning

Provide paired preferred/non-preferred outputs:

```jsonl preference_data.jsonl
{"input": {"messages": [{"role": "user", "content": "Explain AI"}]}, "preferred_output": [{"role": "assistant", "content": "AI is a broad field..."}], "non_preferred_output": [{"role": "assistant", "content": "It means computers."}]}
```

```python
job = client.fine_tuning.create(
    training_file=preference_file_id,
    model="meta-llama/Llama-3.2-3B-Instruct",
    training_method="dpo",
    dpo_beta=0.2,  # Controls deviation from reference (0.05-0.9)
    lora=True,
)
```

Best practice: Run SFT first, then DPO from checkpoint:
```python
dpo_job = client.fine_tuning.create(
    training_file=preference_file_id,
    from_checkpoint=sft_job_id,
    model="meta-llama/Llama-3.2-3B-Instruct",
    training_method="dpo",
    dpo_beta=0.2,
)
```

## BYOM (Bring Your Own Model)

Fine-tune any CausalLM model under 100B params from HuggingFace:

```python
job = client.fine_tuning.create(
    model="togethercomputer/llama-2-7b-chat",  # Base template
    from_hf_model="HuggingFaceTB/SmolLM2-1.7B-Instruct",  # Your model
    training_file=file_id,
    hf_api_token="hf_xxx",  # Optional, for private repos
)
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `model` | Base model to fine-tune | Required |
| `training_file` | Uploaded file ID | Required |
| `validation_file` | Optional validation file ID | None |
| `lora` | LoRA fine-tuning | True |
| `n_epochs` | Training epochs | 1 |
| `learning_rate` | Weight update rate | 1e-5 |
| `batch_size` | Examples per iteration | "max" |
| `train_on_inputs` | Train on user messages | "auto" |
| `suffix` | Custom model name suffix | None |
| `n_checkpoints` | Checkpoints to save | 1 |
| `warmup_ratio` | Warmup steps ratio | 0 |
| `n_evals` | Validation evaluations | 0 |
| `wandb_api_key` | W&B monitoring | None |
| `training_method` | "sft" or "dpo" | "sft" |
| `from_checkpoint` | Continue from previous job | None |

## Continue Training

```python
job = client.fine_tuning.create(
    training_file=new_file_id,
    from_checkpoint=previous_job_id,  # or output model name
)
```

## Manage Jobs

```python
client.fine_tuning.list()                  # List all jobs
client.fine_tuning.retrieve(job_id)        # Get status
client.fine_tuning.list_events(id=job_id)  # Get logs
client.fine_tuning.cancel(id=job_id)       # Cancel
client.fine_tuning.delete(job_id)          # Delete (irreversible)
```

```typescript
const jobs = await together.fineTuning.list();               // List all jobs
const job = await together.fineTuning.retrieve("ft-abc123"); // Get status
const events = await together.fineTuning.listEvents("ft-abc123"); // Get logs
await together.fineTuning.cancel("ft-abc123");               // Cancel
```

```shell
# CLI
together fine-tuning list
together fine-tuning retrieve ft-abc123
together fine-tuning status ft-abc123
together fine-tuning list-events ft-abc123
together fine-tuning cancel ft-abc123
together fine-tuning delete ft-abc123
```

## Resources

- **Data format details**: See [references/data-formats.md](references/data-formats.md)
- **Supported models**: See [references/supported-models.md](references/supported-models.md)
- **Deployment options**: See [references/deployment.md](references/deployment.md)
- **Runnable script**: See [scripts/finetune_workflow.py](scripts/finetune_workflow.py) — upload → train → monitor → deploy pipeline (v2 SDK)
- **Official docs**: [Fine-tuning Quickstart](https://docs.together.ai/docs/fine-tuning-quickstart)
- **Official docs**: [Fine-tuning Models](https://docs.together.ai/docs/fine-tuning-models)
- **Official docs**: [LoRA Training](https://docs.together.ai/docs/lora-training-and-inference)
- **API reference**: [Fine-tuning API](https://docs.together.ai/reference/post-fine-tunes)
