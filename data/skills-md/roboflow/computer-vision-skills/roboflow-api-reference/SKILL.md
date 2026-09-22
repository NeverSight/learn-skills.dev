---
name: roboflow-api-reference
description: Protocol-level facts for Roboflow REST and Inference APIs — URL patterns, auth, parameters, error codes, and SDK quick-start. For deployment strategy and Workflow execution patterns, see roboflow-inference.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

> **Tip:** If you're connected to the [Roboflow MCP server](https://mcp.roboflow.com), prefer its tools (`projects_*`, `versions_*`, `models_*`, `workflows_*`, `images_*`, …) over raw REST calls — they handle auth, pagination, and typed responses for you. The REST patterns below stay relevant if you're not using MCP.

# Roboflow API Reference — Overview

## API Hosts

| Host | Base URL | Purpose |
|------|----------|---------|
| Platform API | `https://api.roboflow.com` | CRUD for projects, images, versions, training, upload |
| Serverless Inference | `https://serverless.roboflow.com` | Model inference + Workflow execution |
| Dedicated Deployment | `https://<name>.roboflow.cloud` | Private GPU inference (same API as serverless) |
| Self-hosted Inference | `http://localhost:9001` | Local inference server via `inference` package |

Use the `inference-sdk` Python package as the preferred client for all inference hosts. It handles auth, retries, and response parsing.

## Authentication

| Method | Where | Format |
|--------|-------|--------|
| Query parameter | All hosts | `?api_key=YOUR_KEY` |
| Request body | Platform API + Workflow inference | `"api_key": "YOUR_KEY"` in JSON body |
| Header | MCP server (`mcp.roboflow.com`) | `x-api-key: YOUR_KEY` (handled automatically by MCP) |

API keys are workspace-scoped. Get yours from **Workspace Settings > API Keys** in the Roboflow dashboard (`app.roboflow.com/{workspace}/settings/api`). Personal API keys are at `/settings/account` → API Keys tab.

## SDKs

| SDK | Install | Primary Use |
|-----|---------|-------------|
| Python (`inference-sdk`) | `pip install inference-sdk` | Inference via `InferenceHTTPClient` |
| Python (`roboflow`) | `pip install roboflow` | Upload, training, project management |
| JavaScript (`roboflow.js`) | Browser script tag | Real-time on-device web inference |
| iOS (Swift) | CocoaPods/SPM | On-device mobile inference |

### Python inference-sdk Quick Start

```python
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",  # or dedicated URL, or localhost
    api_key="YOUR_KEY"
)
result = CLIENT.infer("image.jpg", model_id="your-project/1")
```

### Python roboflow SDK Quick Start

```python
import roboflow

rf = roboflow.Roboflow(api_key="YOUR_KEY")
project = rf.workspace("my-workspace").project("my-project")

# Upload
project.upload(image_path="image.jpg", split="train")

# Inference
model = project.version(1).model
result = model.predict("image.jpg", confidence=40).json()
```

## Host Selection Guide

| Task | Host to Use |
|------|-------------|
| Run model inference | `serverless.roboflow.com` |
| Run Workflows | `serverless.roboflow.com` |
| Upload images | `api.roboflow.com` |
| Manage projects/versions | `api.roboflow.com` |
| Start training | `api.roboflow.com` |
| High-throughput / SLA inference | Dedicated deployment URL |
| Air-gapped / on-prem inference | Self-hosted `localhost:9001` |
| Real-time video / webcam / RTSP | WebRTC via `inference_sdk.webrtc` against serverless or local — see `roboflow://skills/roboflow-inference/workflows` ("Video Stream" section). Not a plain HTTP call. |

## Rate Limits

- Serverless API: rate limits vary by plan
- File upload max: 20 MB

## Related Pages

- `roboflow://skills/roboflow-api-reference/inference` — inference URL patterns, request/response formats
- `roboflow://skills/roboflow-api-reference/rest-api` — platform REST API endpoints (CRUD, upload, training)
- `roboflow://skills/roboflow-api-reference/api-key-management` — creating and managing API keys via REST, MCP tools, and Python CLI. **When creating a key, scope it to least privilege** if the workspace has Advanced API Keys; if not, tell the user scoped keys are an Enterprise feature.
