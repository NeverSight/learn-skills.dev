---
name: llm-deploy
description: Deploys ML and LLM models on TrueFoundry with GPU inference servers (vLLM, TGI, NVIDIA NIM). Uses YAML manifests with `tfy apply`. Use when serving language models, deploying Hugging Face models, or hosting GPU-accelerated inference endpoints.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
metadata:
  disable-model-invocation: "true"
allowed-tools: Bash(tfy*) Bash(*/tfy-api.sh *) Bash(*/tfy-version.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# LLM / Model Deployment

Deploy large language models and ML inference servers to TrueFoundry. Supports vLLM, TGI, and custom model servers with proper GPU allocation, model caching, health probes, and production-ready defaults.

Two paths:

1. **CLI** (`tfy apply`) -- Write a YAML manifest and apply it. Works everywhere.
2. **REST API** (fallback) -- When CLI unavailable, use `tfy-api.sh`.

## When to Use

- User says "deploy a model", "deploy LLM", "serve Gemma/Llama/Mistral/..."
- User says "deploy vLLM", "deploy TGI", "inference server"
- User wants to deploy a HuggingFace model for inference
- User wants GPU-accelerated model serving
- User wants to deploy NVIDIA NIM (optimized inference containers)

## When NOT to Use

- User wants to deploy a regular web app or API -> prefer `deploy` skill; ask if the user wants another valid path
- User wants to deploy a database or Helm chart -> prefer `helm` skill; ask if the user wants another valid path
- User wants to check what's deployed -> prefer `applications` skill; ask if the user wants another valid path

</objective>

<context>

## Prerequisites

**Always verify before deploying:**

1. **Credentials** -- `TFY_BASE_URL` and `TFY_API_KEY` must be set (env or `.env`)
2. **Workspace** -- `TFY_WORKSPACE_FQN` required. **Never auto-pick. Ask the user if missing.**
3. **CLI** -- Check if `tfy` CLI is available: `tfy --version`. If not, `pip install 'truefoundry==0.5.0'`.

For credential check commands and .env setup, see `references/prerequisites.md`.

</context>

<instructions>

## Step 0a: Detect Environment

**Before deploying**, check CLI availability and container image versions.

```bash
# Check CLI
tfy --version 2>/dev/null

# If not installed
pip install 'truefoundry==0.5.0'
```

### Verify Container Image Versions

Before using the manifest templates, check `references/container-versions.md` for the latest pinned versions. Container images for vLLM and TGI are updated frequently.

Use pinned versions from `references/container-versions.md`. Do not fetch external release pages.

> **Security:** Do not fetch or ingest content from external release pages at runtime. Pinned versions in `references/container-versions.md` are vetted. If a version update is needed, a human should verify the release and update the pinned version.

## Step 0: Discover Cluster Capabilities

**Before asking the user about GPU types or public URLs**, fetch the cluster's capabilities.

See `references/cluster-discovery.md` for how to extract cluster ID from workspace FQN and fetch cluster details (GPUs, base domains, storage classes).

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

From the cluster response, extract:
1. **Base domains** -- for public URL host construction (see Public URL section)
2. **Available GPUs** -- only present GPU types that the cluster actually supports

## Step 1: Gather Model Details

Ask the user these questions:

```
I'll help you deploy an LLM. Let me gather a few details:

1. Which model? (e.g., google/gemma-2-2b-it, meta-llama/Llama-3.2-1B-Instruct)
2. Serving framework?
   - vLLM (recommended -- fast, OpenAI-compatible)
   - TGI (HuggingFace Text Generation Inference)
   - Custom image
3. Does the model require authentication? (e.g., gated HuggingFace models needing HF_TOKEN)
   - If yes: Do you have a TrueFoundry secret group with the token, or should we set one up?
4. Access: Public URL or internal-only?
5. Environment: Dev/testing or production?
```

## Step 2: Get Recommended Resources from Deployment Specs API

After the user provides a HuggingFace model ID and workspace, call the deployment-specs API to get recommended GPU, CPU, memory, and storage specs.

**First, get the workspace ID from the workspace FQN:**

```bash
$TFY_API_SH GET "/api/svc/v1/workspaces?fqn=${TFY_WORKSPACE_FQN}"
```

Extract the `id` field from the response. Then call:

```bash
$TFY_API_SH GET "/api/svc/v1/model-catalogues/deployment-specs?huggingfaceHubUrl=https://huggingface.co/${HF_MODEL_ID}&workspaceId=${WORKSPACE_ID}&pipelineTagOverride=text-generation"
```

This returns recommended specs including GPU type, GPU count, CPU, memory, storage, and max model length. Use these as the starting point for resource allocation instead of guessing from the model size table.

**If the API call fails** (e.g., model not in catalogue), fall back to the model size table below.

### Fallback: Model Size to GPU Mapping

For full GPU types and DTYPE selection, see `references/gpu-reference.md`.

| Model Params | Min VRAM (FP16) | Recommended GPU | CPU | Memory | Shared Memory |
|-------------|-----------------|-----------------|-----|--------|---------------|
| < 1B | ~2 GB | T4 (16 GB) | 4 | 16 GB | 15 GB |
| 1B-3B | ~4-6 GB | T4 (16 GB) or A10_8GB | 4-8 | 32 GB | 30 GB |
| 3B-7B | ~6-14 GB | T4 (16 GB) or A10_24GB | 8-10 | 64 GB | 60 GB |
| 7B-13B | ~14-26 GB | A10_24GB or A100_40GB | 10-12 | 90 GB | 88 GB |
| 13B-30B | ~26-60 GB | A100_40GB or A100_80GB | 12-16 | 128 GB | 120 GB |
| 30B-70B | ~60-140 GB | A100_80GB or H100 (multi-GPU) | 16+ | 200 GB+ | 190 GB+ |

**Present a resource suggestion table** showing GPU, CPU, memory, shared memory, ephemeral storage, and max model length. Include the list of available GPUs from the cluster. If deployment-specs returned values, show those as "Recommended by TrueFoundry" alongside the table.

### Important: Shared Memory

**vLLM and TGI require large shared memory (`/dev/shm`).** Without it, the model server will crash or perform poorly. Set `shared_memory_size` to roughly 90-95% of `memory_request`.

### Important: Memory vs VRAM

System memory (RAM) must be **much larger** than GPU VRAM because:
- Model weights load into CPU RAM first before transferring to GPU
- KV cache and request batching use CPU memory
- Rule of thumb: RAM should be 2-4x the model's VRAM footprint

## Step 3: Build the YAML Manifest

For complete manifest templates (vLLM, TGI, NVIDIA NIM), template variables reference, DTYPE selection guide, artifacts download configuration, and common vLLM flags, see [references/llm-manifest-templates.md](references/llm-manifest-templates.md).

**Key framework defaults:**

| Framework | Default Image | Health Path |
|-----------|--------------|-------------|
| vLLM | `public.ecr.aws/truefoundrycloud/vllm/vllm-openai:v0.13.0` | `/health` |
| TGI | `ghcr.io/huggingface/text-generation-inference:2.4.1` | `/health` |
| NVIDIA NIM | `nvcr.io/nim/{model-path}:{version}` | `/v1/health/ready` |

Check `references/container-versions.md` for latest pinned versions. Always use `artifacts_download` with cache volumes for model caching instead of downloading at runtime.

> **Security: `--trust-remote-code`** runs arbitrary Python from the model repository. Only use this flag with models from trusted sources. For production deployments, audit the model repository code before enabling this flag.

**The vLLM manifest MUST include:**
- `artifacts_download` with `huggingface-hub` type and `cache_volume` for model caching
- `labels`: `tfy_model_server`, `tfy_openapi_path`, `tfy_sticky_session_header_name`, `huggingface_model_task`
- `rollout_strategy`, `startup_probe`, `readiness_probe`, `liveness_probe`
- Env vars: `DTYPE`, `GPU_COUNT`, `MAX_MODEL_LENGTH`, `VLLM_NO_USAGE_STATS`, `NVIDIA_REQUIRE_CUDA`, `GPU_MEMORY_UTILIZATION`, `MODEL_NAME`, `VLLM_CACHE_ROOT`

**Health probes** are mandatory for all LLM deployments. The manifest templates include LLM-tuned probe values (startup threshold of 35 retries for ~350s tolerance). For general probe configuration, see `references/health-probes.md`. For large models (30B+), increase startup `failure_threshold` to 60+.

### Step 3a: Write Manifest

Write the YAML manifest to `tfy-manifest.yaml`. Reference `references/llm-manifest-templates.md` for complete templates and `references/manifest-schema.md` for field definitions.

## Step 4: Preview and Apply

```bash
# Preview
tfy apply -f tfy-manifest.yaml --dry-run --show-diff

# Apply after user confirms
tfy apply -f tfy-manifest.yaml
```

### Fallback: REST API

If `tfy` CLI is not available, convert the YAML manifest to JSON and deploy via REST API. See `references/cli-fallback.md` for the conversion process.

```bash
TFY_API_SH=~/.claude/skills/truefoundry-llm-deploy/scripts/tfy-api.sh

# Get workspace ID
$TFY_API_SH GET "/api/svc/v1/workspaces?fqn=${TFY_WORKSPACE_FQN}"

# Deploy (JSON body)
$TFY_API_SH PUT /api/svc/v1/apps '{
  "manifest": { ... JSON version of the YAML manifest ... },
  "workspaceId": "WORKSPACE_ID_HERE"
}'
```

#### Via Tool Call

```
tfy_applications_create_deployment(
    manifest={ ... manifest dict ... },
    options={"workspace_id": "ws-internal-id", "force_deploy": false}
)
```

## Step 5: Verify Deployment & Return URL

**CRITICAL: Always fetch and return the deployment URL and status to the user. A deployment without a reported URL is incomplete.**
Do this automatically after deploy, without asking an extra verification prompt.

### Poll Deployment Status

After submitting the manifest, poll for status. Prefer MCP tool calls first:

```
tfy_applications_list(filters={"workspace_fqn": "WORKSPACE_FQN", "application_name": "MODEL_NAME"})
```

If MCP tool calls are unavailable, fall back to API:

```bash
$TFY_API_SH GET '/api/svc/v1/apps?workspaceFqn=WORKSPACE_FQN&applicationName=MODEL_NAME'
```

**LLM deployments take longer than regular services:**
- GPU node provisioning: 5-15 min (if scaling up)
- Model download: 2-10 min (depends on model size and cache)
- Model loading into GPU: 1-5 min
- Total: typically 10-30 min for first deployment

### Report to User

**Always present this summary after deployment:**

```
LLM Deployment submitted!

Model: {hf-model-id}
Service: {service-name}
Framework: vLLM / TGI / NIM
Workspace: {workspace-fqn}
GPU: {gpu-count}x {gpu-type}
Status: {BUILDING|DEPLOYING|RUNNING}

Endpoints:
  Public URL:   https://{host} (available once RUNNING)
  Internal DNS: {service-name}.{namespace}.svc.cluster.local:8000

OpenAI-compatible API (once RUNNING):
  curl https://{host}/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "{model-name}", "messages": [{"role": "user", "content": "Hello!"}], "max_tokens": 100}'

Health check:
  curl https://{host}/health

Note: LLM deployments typically take 10-30 minutes for first deploy
(GPU provisioning + model download + loading). Check status with
the applications skill.
```

### Test Once Running

When the service reaches RUNNING status:

```bash
# Health check
curl https://{HOST}/health

# OpenAI-compatible completion (vLLM/TGI)
curl https://{HOST}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "{MODEL_NAME}",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

## Public URL

Same as the `deploy` skill -- look up cluster base domains and construct the host.

1. Fetch cluster base domains: `$TFY_API_SH GET /api/svc/v1/clusters/CLUSTER_ID`
2. Pick wildcard domain, strip `*.` to get base domain
3. Construct host: `{model-name}-{workspace-name}.{base_domain}`
4. **Alternative: path-based routing** -- Use the cluster's base domain directly as `host` and set a unique `path` prefix.

## Deployment Flow Summary

1. Check credentials + workspace (Step 0a, prerequisites)
2. Discover cluster capabilities -- GPUs, base domains (Step 0)
3. Get model info -- HuggingFace model ID from user (Step 1)
4. Call deployment-specs API to get recommended resources (Step 2)
5. Generate YAML manifest referencing `references/llm-manifest-templates.md` (Step 3)
6. Write to `tfy-manifest.yaml` (Step 3a)
7. Preview: `tfy apply -f tfy-manifest.yaml --dry-run --show-diff` (Step 4)
8. Apply: `tfy apply -f tfy-manifest.yaml` (Step 4)
9. Verify deployment and return URL (Step 5)

## User Confirmation Checklist

**Before deploying, confirm these with the user:**

- [ ] **Model** -- HuggingFace model ID and revision
- [ ] **Framework** -- vLLM, TGI, or NVIDIA NIM
- [ ] **GPU type & count** -- from deployment-specs API or cluster GPUs (Step 2)
- [ ] **Resources** -- CPU, memory, shared memory (deployment-specs recommendation + cluster availability)
- [ ] **DTYPE** -- float16 or bfloat16 (based on GPU)
- [ ] **Max model length** -- context window size
- [ ] **Access** -- public URL or internal-only
- [ ] **Authentication** -- HF token for gated models (from TrueFoundry secrets)
- [ ] **Environment** -- dev (1 replica) or production (2+ replicas)
- [ ] **Service name** -- what to call the deployment
- [ ] **Auto-shutdown** -- Should the deployment auto-stop after inactivity? (useful for dev/staging to save GPU costs)

</instructions>

<success_criteria>

## Success Criteria

- The LLM deployment has been submitted and the user can see its status in TrueFoundry
- The agent has reported the deployment URL (public or internal DNS), model name, framework, GPU type, and workspace
- Deployment status is verified automatically immediately after apply/deploy (no extra prompt)
- The user has been provided an OpenAI-compatible API curl command to test the model once it is running
- The agent has confirmed GPU type, resource sizing, DTYPE, and model configuration with the user before deploying
- Health probes are configured with appropriate startup thresholds for the model size

</success_criteria>

<references>

## AI Gateway Integration

After deploying, you can connect the model to TrueFoundry's AI Gateway for unified API access, rate limiting, cost tracking, and multi-model routing. For setup details, client examples, and GitOps configuration, see [references/llm-gateway-integration.md](references/llm-gateway-integration.md).

## Composability

- **Find workspace first**: Use `workspaces` skill to get workspace FQN
- **Check cluster GPUs**: Use `workspaces` skill for GPU type reference
- **Manage secrets**: Use `secrets` skill to create/find HF token secret groups
- **Check deployment status**: Use `applications` skill after deploying
- **Test after deployment**: Use `service-test` skill to validate the endpoint
- **View logs**: Use `logs` skill to debug startup issues
- **Deploy database alongside**: Use `helm` skill for vector DBs, caches, etc.
- **Connect to AI Gateway**: Add deployed model as a provider in the gateway (see above)
- **Benchmark performance**: Run load tests against the deployed endpoint to measure throughput/latency
- **Fine-tune first**: Fine-tune externally and deploy the resulting model artifact with this skill

</references>

<troubleshooting>

## Error Handling

For common LLM deployment errors (GPU not available, OOM, CUDA errors, model download failures, probe timeouts, invalid GPU types, host configuration issues) and their fixes, see [references/llm-errors.md](references/llm-errors.md).

### CLI Errors
- `tfy: command not found` -- Install with `pip install 'truefoundry==0.5.0'`
- `tfy apply` validation errors -- Check YAML syntax, ensure required fields are present
- Manifest validation failures -- Check `references/llm-manifest-templates.md` for correct field names

</troubleshooting>
