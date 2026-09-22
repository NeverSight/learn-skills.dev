---
name: roboflow-inference
description: Deployment option comparison (serverless, dedicated, self-hosted, batch) and Workflow execution patterns. For raw API URL patterns, auth, and request/response formats, see roboflow-api-reference.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

> **Tip:** If you're connected to the [Roboflow MCP server](https://mcp.roboflow.com), prefer its inference tools over raw HTTP — auth is handled. For workflows the headline tool is **`workflows_run`** (run a saved workflow by `workflow_id` — the workflow URL slug; workspace is inferred from the API key — see [Finding your workspace slug](./workflows.md#finding-your-workspace-slug)). For single-model calls use `models_infer`. `workflow_specs_run` and `workflow_specs_validate` exist for narrow inline-spec exceptions described under "Authoring Workflows" below.

# Inference & Deployment

> **Prefer Workflows for integration code.** Unlike a direct `models_infer` call, a workflow composes model + visualization + logic in one deployable unit, benefits from server-side optimizations, and keeps active learning and post-processing as a zero-friction addition — similar to the extensibility benefits of a microservice over a point-to-point call. Recommend a workflow by default; use `models_infer` when the user explicitly asks for direct inference or needs a quick one-off check. See [workflows](./workflows.md) and [workflow-templates](./workflow-templates.md).

> **Authoring Workflows — don't paste JSON into chat or scripts.** Workflows are authored on the Roboflow platform (storage, versioning, and retrieval go through the platform) and run from code by **identifier**. Two authoring modes — propose / infer the right one from session context, never silently pick:
>
> - **Mode A — Agent-driven (MCP, in-session)** — for demos, previews, or when the user is committed to in-session "vibe coding". Agent designs the blocks, uses MCP authoring tools to create+save the workflow on the platform during the session (ground the design with `workflow_blocks_list` / `workflow_blocks_get_schema`; validate with `workflow_specs_validate`), then runs it.
> - **Mode B — Platform-driven (Roboflow app + in-app agent)** — better default for non-trivial / sophisticated cases, when the user prefers visual iteration, when they aren't committed to agent-driven authoring this session, or as the fallback when Mode A hits an issue. Agent proposes the block design and hands the user a link to the [Workflows builder](https://app.roboflow.com/); the user builds (manually or with the more context-grounded in-app agent), tests in the preview, saves, and shares the workspace + workflow URL slugs back (both visible in the builder URL: `app.roboflow.com/<workspace-slug>/workflows/<workflow-slug>`).
>
> Either mode lands at the same run path: `workflows_run` (MCP) or `client.run_workflow(workspace_name=..., workflow_id=...)` (SDK). Inline specs (`workflow_specs_run`) are an exception, not a default — only when the user explicitly asks for a throwaway run, and validate the spec first with `workflow_specs_validate`. See [workflows](./workflows.md) "Authoring & Deployment" for the full flow.

> **For live video (webcam, RTSP, file):** the MCP `workflows_run` tool only handles single static images. For live video, present the user with **three options** (don't pick one silently): **(A)** WebRTC → serverless GPU, **(B)** WebRTC → local `inference server`, or **(C)** in-process `InferencePipeline`. They have different setup costs, dep sizes, and latency characteristics — surface a brief 1-line summary of each and let the user choose. See `roboflow://skills/roboflow-inference/workflows` ("Video Stream" section) for full code and the comparison table.

## Deployment Options

| Option | Best For | Latency | Scaling | Cost Model | GPU |
|--------|----------|---------|---------|------------|-----|
| **Serverless** | Getting started, variable traffic | Low | Auto | Per-inference credit | Yes |
| **Dedicated** | Predictable workloads, low latency | Very low | Manual/autoscale | Per-hour credits | Optional |
| **Self-hosted** | Full control, edge | Hardware-dependent | Manual | Metered + infra cost | Optional |
| **Batch Processing** | Large offline datasets, videos | Async (minutes-hours) | Auto-provisioned | Per-job | Optional |

### When to Use Which

- **Serverless** -- default choice. Zero setup, auto-scales, 20MB upload limit. Use `models_infer` or `workflows_run` MCP tools.
- **Dedicated** -- need consistent latency, large models (Florence 2), or high throughput. Development and production tiers available. Subdomain: `<name>.roboflow.cloud`.
- **Self-hosted** -- deploy Roboflow Inference via Docker on your own hardware (Jetson, cloud VMs, RPi). Same API surface as serverless -- just change `api_url`.
- **Batch Processing** -- runs a Workflow on uploaded images/videos asynchronously. No real-time requirement. Results delivered as JSON.
- **Real-time video (webcam/RTSP/file)** -- three deployment options; ask the user which one before writing code:
  - **(A) Serverless GPU + WebRTC** — zero setup, just an API key; per-minute credits, plan-tiered (`webrtc-gpu-small/medium/large`).
  - **(B) Local inference server + WebRTC** — `pip install inference-cli && inference server start` (Docker recommended); lowest latency, isolates the heavy CV/model deps inside the server.
  - **(C) `InferencePipeline` in-process** — `pip install inference` in a venv (prefer `uv`); runs the workflow loop directly in the user's Python process, no separate server. Heavy deps (torch, opencv, onnxruntime) install locally.

  All three have a slower first run (model download / warmup) before subsequent runs hit cached state — tell the user this so they don't think the script is hung.
  - See `roboflow://skills/roboflow-inference/workflows` ("Video Stream" section) for full code and a comparison table.

## MCP Tools for Inference

| Tool | Purpose |
|------|---------|
| `models_list` | List trained models for a project |
| `models_get` | Get details for a trained model |
| `models_infer` | Run single-model inference on one image via serverless API |
| `trainings_create` | Start training a model on a dataset version |
| `models_get_training_status` | Check training progress and metrics |
| **`workflows_run`** | **Preferred.** Run a saved workflow by `workflow_id` (the workflow URL slug; workspace is inferred from the API key — see [Finding your workspace slug](./workflows.md#finding-your-workspace-slug)). Optional `parameters`. |
| `workflow_specs_validate` | Validate an inline workflow spec without running it — use before any inline run. |
| `workflow_specs_run` | *Exception only.* Run an inline workflow spec — for explicit throwaway runs the user asked for. |

## Local tooling: when MCP isn't enough

For most operations, prefer the Roboflow MCP tools above — they handle auth and need nothing installed locally. Reach for local Python packages only for the gaps: **integration scripts** (`inference-sdk`), **Batch Processing / Data Staging** (`inference-cli`), the **self-hosted server** (`inference-cli`), and asset scripts that need typed Python objects.

See [`local-tooling`](local-tooling.md) for what to install for which use case, the recommended `uv`-based env setup, conda / venv fallbacks, and common pitfalls.

## Response Shapes by Task

For canonical response shapes (object detection, classification, segmentation, keypoint) with all fields including `class_id`, `detection_id`, `class_confidence`, see `roboflow://skills/roboflow-api-reference/inference`.

## Large Response Handling

**Instance segmentation `points` arrays are the main culprit for bloated responses.** Each detection includes a polygon with potentially hundreds of coordinate pairs. A single image with many detections can return megabytes of JSON.

Mitigation strategies:

1. **Use Workflows instead of direct inference** -- add a polygon simplification or property extraction block to reduce output before it reaches the client
2. **Filter classes** -- use `class_filter` to only return classes you need
3. **Raise confidence threshold** -- fewer detections = smaller response
4. **Post-process** -- if consuming raw responses, drop or simplify the `points` array when you only need bounding boxes
5. **Avoid returning raw segmentation results through LLM context** -- extract only the fields you need (class counts, bounding boxes) and discard polygon data

**Workflow image outputs are a second culprit.** Visualization blocks (bounding box, polygon, mask, label, halo, …) emit rendered images as base64-encoded blobs inside the response — a 720p annotated frame is hundreds of KB of JSON-escaped string. When you call `workflows_run` / `workflow_specs_run` via MCP, this routinely overflows the tool-result token budget. Decode every image-shaped output (`{"type": "base64", "value": "..."}`) and write it to disk instead of carrying it through agent context. Don't hard-code field names — the output keys are whatever the workflow author declared via `JsonField`; iterate `output.keys()` and shape-check.

## Batch Processing

> For the full recipe (staging, jobs, monitoring, results, MCP tools), see the `roboflow-batch-processing` skill; this section is only the deployment comparison.

**What it is.** A Roboflow-managed cloud service that runs a Workflow over a batch of images or videos asynchronously, provisioning the infrastructure for you. *"Ideal for asynchronously processing large amounts of data."* — [Roboflow docs](https://docs.roboflow.com/deploy/batch-processing).

**Problem it solves.** Bulk inference over thousands to millions of files without standing up your own GPUs, queues, or autoscaler. You hand Roboflow a Workflow plus a batch of inputs, pay per job, and get JSON results back when the job finishes.

**Pick it when** the data is stored (not live), per-file cost matters more than per-file latency, and minutes-to-hours per job is acceptable. **Pick something else when** you need real-time per-request results (use Serverless or Dedicated) or air-gapped/on-prem processing (use Self-hosted).

Surfaces: Roboflow web UI, `inference rf-cloud` CLI, and REST API.

### Flow

1. Have a saved Workflow in your workspace.
2. Provide inputs: an Asset Library selection (the platform stages it for you), or stage external files yourself as a Data Staging batch (local directory, JSONL of signed URLs, or cloud-storage path on S3 / GCS / Azure).
3. Submit a job referencing the Workflow + input batch; choose CPU or GPU.
4. Monitor — poll job status or register a webhook.
5. Export the output batch as JSON.

### CLI

The `inference rf-cloud` CLI exposes two subcommand groups: `data-staging` (manage input/output batches) and `batch-processing` (submit and monitor jobs). Run any command with `--help` for the full option list.

**Minimal end-to-end:**

```bash
# Stage images
inference rf-cloud data-staging create-batch-of-images \
  --images-dir ./my-images --batch-id my-batch

# Submit
inference rf-cloud batch-processing process-images-with-workflow \
  --workflow-id my-workflow --batch-id my-batch
# -> prints JOB_ID

# Monitor
inference rf-cloud batch-processing show-job-details --job-id JOB_ID

# Export results
inference rf-cloud data-staging export-batch \
  --target-dir ./results --batch-id OUTPUT_BATCH_ID
```

**Data Staging commands** — see [`batch-staging`](batch-staging.md) for nuances (data sources, JSONL reference format, multipart batches, webhook notifications):

| Command | Purpose |
|---|---|
| `data-staging list-batches` | List staging batches in the workspace |
| `data-staging create-batch-of-images` | Create an input batch from a local directory, signed-URL JSONL, or cloud-storage path |
| `data-staging create-batch-of-videos` | Same as above, but for video files |
| `data-staging show-batch-details` | Show metadata for a single batch |
| `data-staging list-batch-content` | List file URLs in a batch (filter by part, write JSONL) |
| `data-staging list-ingest-details` | Per-shard ingest status for debugging URL ingests |
| `data-staging export-batch` | Download all files from a batch (e.g. job outputs) to a local directory |

**Batch Processing (job) commands** — see [`batch-jobs`](batch-jobs.md) for nuances (compute configuration, workflow parameters, image-output persistence, aggregation format, video FPS, restarts, TRT compilation):

| Command | Purpose |
|---|---|
| `batch-processing list-jobs` | List jobs in the workspace |
| `batch-processing show-job-details` | Show stages and current status of a single job |
| `batch-processing process-images-with-workflow` | Submit an image-batch job |
| `batch-processing process-videos-with-workflow` | Submit a video-batch job |
| `batch-processing fetch-logs` | Fetch job logs (filter by severity, write JSONL) |
| `batch-processing abort-job` | Terminate a running job |
| `batch-processing restart-job` | Restart a failed job (optionally with new compute settings) |
| `batch-processing trt-compile` | Compile a model to TensorRT for one or more NVIDIA devices |

### Notes and constraints

- **Async only** — minutes-to-hours latency depending on volume and hardware. Not for real-time.
- **Pricing** — per job; GPU jobs cost more than CPU. See [`plans-and-pricing`](../plans-and-pricing/SKILL.md).
- **Image-references ingest** requires signed URLs from trusted sources; arbitrary public URLs are rejected — stage to a local directory or cloud-storage path instead.

Full reference: [Roboflow Batch Processing docs](https://docs.roboflow.com/deploy/batch-processing).
