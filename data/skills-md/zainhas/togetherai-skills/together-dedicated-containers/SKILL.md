---
name: together-dedicated-containers
description: Deploy custom Dockerized inference workloads on Together AI's managed GPU infrastructure using Dedicated Container Inference (DCI). Tools include Jig CLI for building/deploying, Sprocket SDK for request handling, and a private container registry. Use when users need custom model serving, containerized inference, Docker-based GPU workloads, or workloads beyond standard model endpoints.
---

# Together Dedicated Containers

## Overview

Run custom Dockerized inference workloads on Together's managed GPU infrastructure. You bring the container — Together handles compute, autoscaling, networking, and observability.

**Components:**
- **Jig CLI**: Build, push, and deploy containers
- **Sprocket SDK**: Python SDK for handling inference requests inside containers
- **Container Registry**: `registry.together.xyz` for storing images
- **Queue API**: Async job submission with priority and progress tracking

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

1. Write inference code using Sprocket SDK (`setup()` + `predict()`)
2. Build container with Jig CLI (`jig build`)
3. Push to registry (`jig push`)
4. Deploy (`jig deploy`)
5. Send requests to your deployment

## Quick Start

### 1. Install Jig CLI

```shell
pip install together
# Set your API key as an environment variable:
# export TOGETHER_API_KEY=<your-api-key>
```

### 2. Create Inference Worker

```python
# worker.py
import sprocket

class MyWorker(sprocket.Sprocket):
    def setup(self):
        """Load model and resources (runs once at startup)."""
        import torch
        self.model = torch.load("model.pt")

    def predict(self, args: dict) -> dict:
        """Handle a single inference request."""
        input_data = args
        result = self.model(input_data["prompt"])
        return {"output": result}
```

### 3. Configure Project

```toml
# pyproject.toml
[project]
name = "my-inference-service"
version = "0.1.0"
dependencies = ["sprocket"]

[[tool.uv.index]]
name = "together-pypi"
url = "https://pypi.together.ai/"

[tool.uv.sources]
sprocket = { index = "together-pypi" }

[tool.jig.image]
cmd = "python worker.py --queue"
copy = ["worker.py"]

[tool.jig.deploy]
gpu_type = "h100-80gb"
gpu_count = 1
```

### 4. Build, Push, Deploy

```shell
jig build                    # Build Docker image
jig push                     # Push to registry.together.xyz
jig deploy                   # Deploy to Together infrastructure
jig status                   # Check deployment status
jig logs                     # View logs
```

### 5. Send Requests

Check the health endpoint:

```shell
curl https://api.together.ai/v1/deployments/my-inference-service/health \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

Submit a job via the Queue API:

```shell
curl -X POST "https://api.together.ai/v1/queue/submit" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "my-inference-service",
    "payload": {"prompt": "Hello world"},
    "priority": 1
  }'
```

Response:

```json
{
  "request_id": "req_abc123",
  "status": "pending"
}
```

Poll for the result:

```shell
curl "https://api.together.ai/v1/queue/status?model=my-inference-service&request_id=req_abc123" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

Response (when complete):

```json
{
  "request_id": "req_abc123",
  "model": "my-inference-service",
  "status": "done",
  "outputs": {"output": "..."}
}
```

Or use the Python `requests` library:

```python
import os
import requests

response = requests.post(
    "https://api.together.ai/v1/queue/submit",
    headers={"Authorization": f"Bearer {os.environ['TOGETHER_API_KEY']}"},
    json={
        "model": "my-inference-service",
        "payload": {"prompt": "Hello world"},
        "priority": 1,
    },
)
print(response.json())
```

Or submit directly via the Jig CLI:

```shell
together beta jig submit --payload '{"prompt": "Hello world"}' --watch
```

## Sprocket SDK

The SDK provides the `sprocket.Sprocket` base class:

- `setup()`: Called once at startup — load models, warm up caches
- `predict(args: dict) -> dict`: Called per request — process input and return output
- File handling: Upload/download files within predictions
- GPU access: Full CUDA access inside the container

## Queue API

For async workloads, use the Queue API for job submission with:
- Priority-based fair queuing
- Progress tracking
- Job status polling

## Key Jig CLI Commands

All commands are subcommands of `together beta jig`. Use `--config <path>` to specify a custom config file (default: `pyproject.toml`).

### Build and Deploy

| Command | Description |
|---------|-------------|
| `jig init` | Create a starter `pyproject.toml` with defaults |
| `jig dockerfile` | Generate a Dockerfile from config (for debugging) |
| `jig build` | Build container image locally |
| `jig build --tag <tag>` | Build with a specific image tag |
| `jig build --warmup` | Build and pre-generate compile caches (requires GPU) |
| `jig push` | Push image to `registry.together.xyz` |
| `jig deploy` | Build, push, and create/update deployment |
| `jig deploy --build-only` | Build and push only, skip deployment creation |
| `jig deploy --image <ref>` | Deploy an existing image, skip build and push |

### Deployment Management

| Command | Description |
|---------|-------------|
| `jig status` | Show deployment status and configuration |
| `jig list` | List all deployments in your organization |
| `jig logs` | View deployment logs |
| `jig logs --follow` | Stream logs in real-time |
| `jig endpoint` | Print the deployment's endpoint URL |
| `jig destroy` | Delete the deployment |

### Queue

| Command | Description |
|---------|-------------|
| `jig submit --payload '<json>'` | Submit a job to the queue |
| `jig submit --prompt '<text>'` | Submit with shorthand prompt payload |
| `jig submit --watch` | Submit and wait for the result |
| `jig job_status --request-id <id>` | Get the status of a submitted job |
| `jig queue_status` | Show queue backlog and worker status |

### Secrets

| Command | Description |
|---------|-------------|
| `jig secrets set --name <n> --value <v>` | Create or update a secret |
| `jig secrets list` | List all secrets for the deployment |
| `jig secrets unset <name>` | Remove a secret |

### Volumes

| Command | Description |
|---------|-------------|
| `jig volumes create --name <n> --source <path>` | Create a volume and upload files |
| `jig volumes update --name <n> --source <path>` | Update a volume with new files |
| `jig volumes describe --name <n>` | Show volume details and contents |
| `jig volumes list` | List all volumes |
| `jig volumes delete --name <n>` | Delete a volume |

## Resources

- **Full Jig CLI reference**: See [references/jig-cli.md](references/jig-cli.md)
- **Sprocket SDK reference**: See [references/sprocket-sdk.md](references/sprocket-sdk.md)
- **App template**: See [scripts/sprocket_hello_world.py](scripts/sprocket_hello_world.py) — minimal Sprocket worker with pyproject.toml example
- **Official docs**: [Dedicated Container Inference](https://docs.together.ai/docs/dedicated-container-inference)
- **Official docs**: [Containers Quickstart](https://docs.together.ai/docs/containers-quickstart)
- **API reference**: [Deployments API](https://docs.together.ai/reference/deployments-create)
