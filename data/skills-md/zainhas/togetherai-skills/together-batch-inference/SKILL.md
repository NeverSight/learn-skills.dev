---
name: together-batch-inference
description: Process large volumes of inference requests asynchronously at up to 50% lower cost via Together AI's Batch API. Supports up to 50K requests per batch, 100MB max file size. Use when users need batch processing, offline inference, bulk data classification, synthetic data generation, or cost-optimized large-scale LLM workloads.
---

# Together Batch Inference

## Overview

Process thousands of requests asynchronously at up to 50% cost discount. Ideal for workloads that don't need real-time responses:
- Evaluations and data analysis
- Large-scale classification
- Synthetic data generation
- Content generation and summarization
- Dataset transformations

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

## Workflow

1. Prepare a `.jsonl` batch file with requests
2. Upload the file with `purpose="batch-api"`
3. Create a batch job
4. Poll for completion
5. Download results

## Quick Start

### 1. Prepare Batch File

Each line: `custom_id` (unique) + `body` (request payload).

```jsonl batch_input.jsonl
{"custom_id": "req-1", "body": {"model": "deepseek-ai/DeepSeek-V3", "messages": [{"role": "user", "content": "Hello!"}], "max_tokens": 200}}
{"custom_id": "req-2", "body": {"model": "deepseek-ai/DeepSeek-V3", "messages": [{"role": "user", "content": "Explain quantum computing"}], "max_tokens": 200}}
```

### 2. Upload and Create Batch

```python
from together import Together
client = Together()

# Upload
file_resp = client.files.upload(file="batch_input.jsonl", purpose="batch-api", check=False)

# Create batch
batch = client.batches.create(input_file_id=file_resp.id, endpoint="/v1/chat/completions")
print(batch.job.id)
```

```typescript
import Together from "together-ai";
const client = new Together();

// Upload (use the file ID returned by the Files API)
const fileId = "file-abc123";

const batch = await client.batches.create({
  endpoint: "/v1/chat/completions",
  input_file_id: fileId,
});

console.log(batch);
```

```shell
# Upload the batch file
curl -X POST "https://api.together.xyz/v1/files" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -F "purpose=batch-api" \
  -F "file=@batch_input.jsonl"

# Create the batch (use the file id from upload response)
curl -X POST "https://api.together.xyz/v1/batches" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input_file_id": "file-abc123", "endpoint": "/v1/chat/completions"}'
```

### 3. Check Status

```python
status = client.batches.retrieve(batch.job.id)
print(status.status)  # VALIDATING → IN_PROGRESS → COMPLETED
```

```typescript
import Together from "together-ai";
const client = new Together();

const batchId = batch.job?.id;

let batchInfo = await client.batches.retrieve(batchId);
console.log(batchInfo.status);
```

```shell
curl -X GET "https://api.together.xyz/v1/batches/batch-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

### 4. Download Results

```python
if status.status == "COMPLETED":
    with client.files.with_streaming_response.content(id=status.output_file_id) as response:
        with open("batch_output.jsonl", "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
```

```typescript
import Together from "together-ai";
const client = new Together();

const batchInfo = await client.batches.retrieve(batchId);

if (batchInfo.status === "COMPLETED" && batchInfo.output_file_id) {
  const resp = await client.files.content(batchInfo.output_file_id);
  const result = await resp.text();
  console.log(result);
}
```

### 5. Cancel / List

```python
client.batches.cancel(batch_id)      # Cancel a batch
batches = client.batches.list()       # List all batches
```

```typescript
import Together from "together-ai";
const client = new Together();

// List all batches
const allBatches = await client.batches.list();
for (const batch of allBatches) {
  console.log(batch);
}
```

```shell
# Cancel a batch
curl -X POST "https://api.together.xyz/v1/batches/batch-abc123/cancel" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"

# List all batches
curl -X GET "https://api.together.xyz/v1/batches" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

## Status Flow

| Status | Description |
|--------|-------------|
| `VALIDATING` | Input file being validated |
| `IN_PROGRESS` | Batch processing |
| `COMPLETED` | Done — download results |
| `FAILED` | Processing failed |
| `CANCELLED` | Batch was cancelled |
| `EXPIRED` | Job expired before completion |

Output order may differ from input — use `custom_id` to match results.

## Models with 50% Discount

| Model ID | Discount |
|----------|----------|
| deepseek-ai/DeepSeek-R1-0528-tput | 50% |
| meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8 | 50% |
| meta-llama/Llama-4-Scout-17B-16E-Instruct | 50% |
| meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo | 50% |
| meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo | 50% |
| meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo | 50% |
| meta-llama/Meta-Llama-3-70B-Instruct-Turbo | 50% |
| meta-llama/Llama-3-70b-chat-hf | 50% |
| meta-llama/Llama-3.3-70B-Instruct-Turbo | 50% |
| Qwen/Qwen2.5-72B-Instruct-Turbo | 50% |
| Qwen/Qwen2.5-7B-Instruct-Turbo | 50% |
| Qwen/Qwen3-235B-A22B-fp8-tput | 50% |
| Qwen/Qwen3-235B-A22B-Thinking-2507 | 50% |
| Qwen/Qwen2.5-VL-72B-Instruct | 50% |
| mistralai/Mixtral-8x7B-Instruct-v0.1 | 50% |
| mistralai/Mistral-7B-Instruct-v0.1 | 50% |
| zai-org/GLM-4.5-Air-FP8 | 50% |
| openai/whisper-large-v3 | 50% |

All serverless models are available for batch — models not listed have no discount.

## Rate Limits

- **Max enqueued tokens**: 30B per model
- **Per-batch limit**: 50,000 requests
- **File size**: 100MB max
- **Separate pool**: Doesn't consume standard rate limits

## Error Handling

Check `error_file_id` for per-request failures:

```jsonl
{"custom_id": "req-1", "error": {"message": "Invalid model specified", "code": "invalid_model"}}
```

## Best Practices

- Aim for 1,000-10,000 requests per batch
- Validate JSONL before submission
- Use unique `custom_id` values
- Poll status every 30-60 seconds
- Most batches complete within 24 hours (allow 72 hours for large/complex models)
- Batch files can be reused for multiple jobs

## Resources

- **Full API reference**: See [references/api-reference.md](references/api-reference.md)
- **Runnable script**: See [scripts/batch_workflow.py](scripts/batch_workflow.py) — complete upload → create → poll → download pipeline (v2 SDK)
- **Runnable script (TypeScript)**: See [scripts/batch_workflow.ts](scripts/batch_workflow.ts) — minimal OpenAPI `x-codeSamples` extraction for list/create/retrieve/cancel (TypeScript SDK)
- **Official docs**: [Batch Inference](https://docs.together.ai/docs/batch-inference)
- **API reference**: [Batch API](https://docs.together.ai/reference/batch-create)
