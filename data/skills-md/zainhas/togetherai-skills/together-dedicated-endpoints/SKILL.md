---
name: together-dedicated-endpoints
description: Deploy models on dedicated single-tenant GPU endpoints via Together AI for predictable performance, no rate limits, autoscaling, and custom hardware. Use when users need dedicated inference endpoints, always-on model hosting, production deployments with SLAs, or scaling beyond serverless limits.
---

# Together Dedicated Endpoints

## Overview

Deploy models as dedicated endpoints with custom hardware and scaling. Benefits over serverless:
- Predictable performance unaffected by shared traffic
- No rate limits — scale with replica count
- 179+ models supported, including fine-tuned and custom models
- Autoscaling, speculative decoding, and prompt caching

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

1. Select a model and check hardware options
2. Create the endpoint with hardware and scaling config
3. Wait for READY state
4. Send inference requests using the endpoint name
5. Stop/delete when done to avoid charges

## Quick Start

### Check Available Hardware

```shell
together endpoints hardware --model mistralai/Mixtral-8x7B-Instruct-v0.1
```

### Create an Endpoint

```python
from together import Together
client = Together()

endpoint = client.endpoints.create(
    display_name="My Mixtral Endpoint",
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    hardware="2x_nvidia_h100_80gb_sxm",
    autoscaling={"min_replicas": 1, "max_replicas": 3},
)
print(endpoint.id)  # endpoint-xxxxxxxx for management
print(endpoint.name)  # account/model-name-hash for inference
```

```typescript
import Together from "together-ai";
const together = new Together();

const endpoint = await together.endpoints.create({
  model: "mistralai/Mixtral-8x7B-Instruct-v0.1",
  hardware: "2x_nvidia_h100_80gb_sxm",
  autoscaling: {
    min_replicas: 1,
    max_replicas: 3,
  },
});
console.log(endpoint.id);
```

```shell
curl -X POST "https://api.together.xyz/v1/endpoints" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "hardware": "2x_nvidia_h100_80gb_sxm",
    "display_name": "My Mixtral Endpoint",
    "autoscaling": {
      "min_replicas": 1,
      "max_replicas": 3
    }
  }'
```

```shell
together endpoints create \
  --model mistralai/Mixtral-8x7B-Instruct-v0.1 \
  --hardware 2x_nvidia_h100_80gb_sxm \
  --display-name "My Mixtral Endpoint" \
  --min-replicas 1 --max-replicas 3 \
  --no-speculative-decoding --wait
```

### Send Inference Requests

Use the **endpoint name** (not ID) as the `model` parameter:

```python
response = client.chat.completions.create(
    model="tester/mistralai/Mixtral-8x7B-Instruct-v0.1-bb04c904",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.chat.completions.create({
  model: "tester/mistralai/Mixtral-8x7B-Instruct-v0.1-bb04c904",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tester/mistralai/Mixtral-8x7B-Instruct-v0.1-bb04c904",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Manage Endpoints

```python
# Get endpoint status
endpoint = client.endpoints.retrieve("endpoint-abc123")
print(endpoint.state)

# Start / Stop
client.endpoints.update("endpoint-abc123", state="STARTED")
client.endpoints.update("endpoint-abc123", state="STOPPED")

# Update replicas
client.endpoints.update(
    "endpoint-abc123",
    autoscaling={"min_replicas": 2, "max_replicas": 4},
)

# Delete
client.endpoints.delete("endpoint-abc123")
```

```typescript
import Together from "together-ai";
const together = new Together();

// Get endpoint status
const endpoint = await together.endpoints.retrieve("endpoint-abc123");
console.log(endpoint.state);

// Start / Stop
await together.endpoints.update("endpoint-abc123", { state: "STARTED" });
await together.endpoints.update("endpoint-abc123", { state: "STOPPED" });

// Update replicas
await together.endpoints.update("endpoint-abc123", {
  autoscaling: { min_replicas: 2, max_replicas: 4 },
});

// Delete
await together.endpoints.delete("endpoint-abc123");
```

```shell
# Get endpoint status
curl "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"

# Stop endpoint
curl -X PATCH "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "STOPPED"}'

# Start endpoint
curl -X PATCH "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "STARTED"}'

# Delete endpoint
curl -X DELETE "https://api.together.xyz/v1/endpoints/endpoint-abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

```shell
# CLI management commands
together endpoints retrieve <ENDPOINT_ID>    # Check status
together endpoints list --mine               # List all endpoints
together endpoints start <ENDPOINT_ID>       # Start stopped endpoint
together endpoints stop <ENDPOINT_ID>        # Stop (pause billing)
together endpoints delete <ENDPOINT_ID>      # Permanently delete

# Update replicas (both min and max required together)
together endpoints update --min-replicas 2 --max-replicas 4 <ENDPOINT_ID>
```

## Key Concepts

### Hardware Format

Format: `{gpu-count}x_nvidia_{gpu-type}_{vram}_{link}`

Example: `2x_nvidia_h100_80gb_sxm`

### Endpoint Name vs ID

- **Endpoint ID** (e.g., `endpoint-e6c6b82f-...`): For management (start/stop/update/delete)
- **Endpoint Name** (e.g., `account/model-hash`): For inference requests as `model` parameter

### Autoscaling

Set `min_replicas` and `max_replicas`. When max > min, auto-scales based on load. More GPUs per replica = higher throughput, lower latency.

### Auto-Shutdown

Endpoints shut down after 1 hour of inactivity by default. Customize with `--inactive-timeout`.

### Speculative Decoding

Disabled by default. Improves average throughput but may increase tail latency. Enable by omitting `--no-speculative-decoding`.

### Prompt Caching

Always enabled. Caches previously processed prompts to reduce latency on repeated inputs.

### Availability Zones

```shell
together endpoints availability-zones  # List zones
together endpoints create --availability-zone us-east-1a ...
```

Only specify if you have geographic/latency requirements — restricting zones limits hardware availability.

## Billing

Charged per minute while the endpoint is running, even when idle. Stop the endpoint to pause charges. See [references/hardware-options.md](references/hardware-options.md) for hardware specs.

## Resources

- **Hardware configurations**: See [references/hardware-options.md](references/hardware-options.md)
- **Full API reference**: See [references/api-reference.md](references/api-reference.md)
- **Runnable script**: See [scripts/manage_endpoint.py](scripts/manage_endpoint.py) — create, monitor, use, stop/delete lifecycle (v2 SDK)
- **Official docs**: [Dedicated Endpoints](https://docs.together.ai/docs/dedicated-endpoints)
- **API reference**: [Endpoints API](https://docs.together.ai/reference/createendpoint)
