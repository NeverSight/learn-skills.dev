---
name: nebius-batch-synthetic
description: Generate synthetic training data using Nebius Token Factory batch inference (50% cheaper than real-time, async, no rate-limit impact). Use this skill whenever the user wants to run batch inference on Nebius, generate synthetic datasets at scale, create instruction-tuning data, run async LLM jobs on large prompt sets, or export batch results as fine-tuning JSONL. Trigger for phrases like "generate synthetic data with Nebius", "run batch inference", "create training data at scale", "async LLM generation", "batch job on Token Factory", "generate QA pairs", or any question about bulk/offline inference or synthetic data pipelines on Nebius.
---

# Nebius Batch Inference — Synthetic Data Generation

Run large-scale async LLM jobs at 50% cost, no rate-limit impact. Ideal for generating synthetic training datasets, annotation, evaluation sets, or any offline bulk inference.

## Prerequisites

```bash
pip install openai
export NEBIUS_API_KEY="your-key"
```

API base: `https://api.tokenfactory.nebius.com/v1/`

## Limits & pricing

| Constraint | Value |
|------------|-------|
| Max requests per file | 5,000,000 |
| Max file size | 10 GB |
| Completion window | 24 hours |
| Cost vs real-time | **50% cheaper** |
| Rate limits | Not consumed |

## Complete pipeline

### 1. Build JSONL batch file

Each line = one inference request. All requests must use the same model.

```python
import json, uuid

prompts = [
    "Explain vector databases for beginners.",
    "What is the difference between RAG and fine-tuning?",
    # ... up to 5M prompts
]

with open("batch_requests.jsonl", "w") as f:
    for prompt in prompts:
        f.write(json.dumps({
            "custom_id": str(uuid.uuid4()),   # unique ID to match results
            "url": "/v1/chat/completions",
            "body": {
                "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
                "messages": [
                    {"role": "system", "content": "You are a helpful expert."},
                    {"role": "user",   "content": prompt},
                ],
                "max_tokens": 1024,
                "temperature": 0.7,
            },
        }) + "\n")
```

### 2. Upload + create batch job

```python
from openai import OpenAI
client = OpenAI(base_url="https://api.tokenfactory.nebius.com/v1/", api_key=API_KEY)

with open("batch_requests.jsonl", "rb") as f:
    file_obj = client.files.create(file=f, purpose="batch")

batch = client.batches.create(
    input_file_id=file_obj.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "synthetic-data-gen"},
)
print(f"Batch: {batch.id}  status={batch.status}")
```

### 3. Poll until complete

```python
import time

while True:
    batch = client.batches.retrieve(batch.id)
    counts = batch.request_counts
    print(f"status={batch.status}  done={counts.completed}/{counts.total}")
    if batch.status in ("completed", "failed", "cancelled", "expired"):
        break
    time.sleep(30)
```

### 4. Download outputs

```python
content = client.files.content(batch.output_file_id)
results = [json.loads(line) for line in content.text.strip().splitlines()]
```

Each result record:
```json
{
  "custom_id": "...",
  "response": {
    "body": {
      "choices": [{"message": {"content": "The model's response..."}}]
    }
  }
}
```

### 5. Export as fine-tuning JSONL

```python
# Build custom_id → original prompt lookup
id_to_prompt = {}
with open("batch_requests.jsonl") as f:
    for line in f:
        req = json.loads(line)
        user_msg = next(m["content"] for m in req["body"]["messages"] if m["role"] == "user")
        id_to_prompt[req["custom_id"]] = user_msg

with open("training.jsonl", "w") as out:
    for rec in results:
        reply  = rec["response"]["body"]["choices"][0]["message"]["content"].strip()
        prompt = id_to_prompt.get(rec["custom_id"], "")
        if len(reply) < 50:      # quality filter
            continue
        out.write(json.dumps({
            "messages": [
                {"role": "user",      "content": prompt},
                {"role": "assistant", "content": reply},
            ]
        }) + "\n")
```

## Tips for synthetic data quality

- Use a **large teacher model** (70B+) to generate, then fine-tune a smaller model — teacher distillation
- Set `temperature: 0.6–0.8` for diverse yet coherent outputs
- Add a quality filter (min length, keyword checks) before using as training data
- Run deduplication on `custom_id` before uploading as training file

## Clean up batch files

You can have up to 500 batch files. Delete old ones:
```python
client.files.delete("file_123")
```

## Bundled reference

Read `references/batch-format.md` when the user asks about JSONL structure, file limits, or output format.

## Reference script

Full working script: `scripts/05_batch_inference_synthetic.py`

Docs: https://docs.tokenfactory.nebius.com/ai-models-inference/batch-inference
