---
name: ai-gateway
description: Configures TrueFoundry AI Gateway for unified OpenAI-compatible LLM access. Covers auth (PAT/VAT), model routing, rate limiting, and budget controls.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *) Bash(curl*) Bash(python*)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# AI Gateway

Use TrueFoundry's AI Gateway to access 1000+ LLMs through a unified OpenAI-compatible API with rate limiting, budget controls, load balancing, routing, and observability.

## When to Use

Access LLMs through TrueFoundry's unified OpenAI-compatible gateway, configure auth tokens (PAT/VAT), set up rate limiting, budget controls, or load balancing across providers.

## When NOT to Use

- User wants to deploy a self-hosted model → prefer `llm-deploy` skill; ask if the user wants another valid path (then connect to gateway)
- User wants to deploy tool servers → prefer `deploy` skill; ask if the user wants another valid path (service with tool-proxy)
- User wants to manage TrueFoundry platform credentials → prefer `status` skill; ask if the user wants another valid path

</objective>

<context>

## Overview

The AI Gateway sits between your application and LLM providers:

```
Your App → AI Gateway → OpenAI / Anthropic / Azure / Self-hosted vLLM / etc.
                ↑
         Unified API + Auth + Rate Limiting + Routing + Logging
```

**Key benefits:**
- **Single endpoint** for all models (cloud + self-hosted)
- **One API key** (PAT or VAT) instead of managing per-provider keys
- **OpenAI-compatible** — works with any OpenAI SDK client
- **Rate limiting** per user, team, or application
- **Budget controls** to enforce cost limits
- **Load balancing** across model instances with fallback
- **Observability** — request logging, cost tracking, analytics

## Gateway Endpoint

The gateway base URL is your TrueFoundry platform URL + `/api/llm`:

```
{TFY_BASE_URL}/api/llm
```

Example: `https://your-org.truefoundry.cloud/api/llm`

## Authentication

### Personal Access Token (PAT)

For development and individual use:

1. Go to TrueFoundry dashboard → **Access** → **Personal Access Tokens**
2. Click **New Personal Access Token**
3. Copy the token

### Virtual Access Token (VAT)

For production applications (recommended):

1. Go to TrueFoundry dashboard → **Access** → **Virtual Account Tokens**
2. Click **New Virtual Account** (requires admin privileges)
3. Name it and **select which models** it can access
4. Copy the token

**VATs are recommended for production** because:
- Not tied to a specific user (survives team changes)
- Support granular model access control
- Better for tracking per-application usage

</context>

<instructions>

## Calling Models

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-PAT-or-VAT>",
    base_url="https://<your-truefoundry-url>/api/llm",
)

# Chat completion
response = client.chat.completions.create(
    model="openai/gpt-4o",  # or any configured model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    max_tokens=200,
)
print(response.choices[0].message.content)
```

### Python (Streaming)

```python
stream = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Write a haiku about AI"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### cURL

```bash
curl "${TFY_BASE_URL}/api/llm/chat/completions" \
  -H "Authorization: Bearer ${TFY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 200
  }'
```

### JavaScript / Node.js

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "<your-PAT-or-VAT>",
  baseURL: "https://<your-truefoundry-url>/api/llm",
});

const response = await client.chat.completions.create({
  model: "openai/gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
});
```

### Environment Variables

Set these to use with any OpenAI-compatible library:

```bash
export OPENAI_BASE_URL="${TFY_BASE_URL}/api/llm"
export OPENAI_API_KEY="<your-PAT-or-VAT>"
```

Then any code using `openai.OpenAI()` without explicit parameters will use the gateway automatically.

## Supported APIs

| API | Endpoint | Description |
|-----|----------|-------------|
| **Chat Completions** | `/chat/completions` | Chat with any model (streaming + non-streaming) |
| **Completions** | `/completions` | Legacy text completions |
| **Embeddings** | `/embeddings` | Text embeddings (text + list inputs) |
| **Image Generation** | `/images/generations` | Generate images |
| **Image Editing** | `/images/edits` | Edit images |
| **Audio Transcription** | `/audio/transcriptions` | Speech-to-text |
| **Audio Translation** | `/audio/translations` | Translate audio |
| **Text-to-Speech** | `/audio/speech` | Generate speech |
| **Reranking** | `/rerank` | Rerank documents |
| **Batch Processing** | `/batches` | Batch predictions |
| **Moderations** | `/moderations` | Content safety |

## Supported Providers

The gateway supports 25+ providers including:

| Provider | Example Model Names |
|----------|-------------------|
| OpenAI | `openai/gpt-4o`, `openai/gpt-4o-mini` |
| Anthropic | `anthropic/claude-sonnet-4-5-20250929` |
| Google Vertex | `google/gemini-2.0-flash` |
| AWS Bedrock | `bedrock/anthropic.claude-3-5-sonnet` |
| Azure OpenAI | `azure/gpt-4o` |
| Mistral | `mistral/mistral-large-latest` |
| Groq | `groq/llama-3.1-70b-versatile` |
| Cohere | `cohere/command-r-plus` |
| Together AI | `together/meta-llama/Meta-Llama-3.1-70B` |
| Self-hosted (vLLM/TGI) | `my-custom-model-name` |

**Model names depend on how they're configured in your gateway.** Check the TrueFoundry dashboard → AI Gateway → Models for exact names.

## Adding Models & Providers

Currently done through the TrueFoundry dashboard UI:

1. Go to **AI Gateway → Models**
2. Click **Add Provider Account**
3. Select provider (OpenAI, Anthropic, etc.)
4. Enter API credentials
5. Select models to enable

### Adding Self-Hosted Models (Cluster-Internal)

After deploying a model with the `llm-deploy` skill:

1. Go to **AI Gateway → Models → Add Provider Account**
2. Select **"Self Hosted"** as the provider type
3. Enter the internal endpoint: `http://{model-name}.{namespace}.svc.cluster.local:8000`
4. The model becomes accessible through the gateway alongside cloud models

> **Security:** Only register model endpoints that you control. External or untrusted model endpoints can return manipulated responses. Use internal cluster DNS (`svc.cluster.local`) for self-hosted models. Verify provider API credentials are stored securely in TrueFoundry secrets, not hardcoded.

### Adding External OpenAI-Compatible APIs (NVIDIA, custom providers)

For externally hosted APIs that are OpenAI-compatible (e.g. NVIDIA Cloud APIs, custom inference endpoints), use `type: provider-account/self-hosted-model` with `auth_data`:

```yaml
# gateway.yaml — External hosted API (e.g. NVIDIA Cloud)
- name: nvidia-external
  type: provider-account/self-hosted-model
  integrations:
    - name: nemotron-nano
      type: integration/model/self-hosted-model
      hosted_model_name: nvidia/nemotron-3-nano-30b-a3b
      url: "https://integrate.api.nvidia.com/v1"
      model_server: "openai-compatible"
      model_types: ["chat"]
      auth_data:
        type: bearer-auth
        bearer_token: "tfy-secret://<tenant>:<group>:<key>"
```

And in a virtual model routing target, reference it as `"<provider-account-name>/<integration-name>"`:

```yaml
targets:
  - model: "nvidia-external/nemotron-nano"  # "<provider-account-name>/<integration-name>"
```

Apply with:
```bash
tfy apply -f gateway.yaml
```

> **WARNING:** `provider-account/nvidia-nim` does **not** exist in the schema — do not use it. Use `provider-account/self-hosted-model` with `auth_data` for all external OpenAI-compatible APIs (as shown above).

> **Schema source of truth:** For authoritative field names and types, read `servicefoundry-server/src/autogen/models.ts` in the platform repo. Do not guess field names from documentation alone.

## Applying Gateway Config

Gateway YAML is applied directly with `tfy apply` — no service build or Docker image involved:

```bash
# Preview changes
tfy apply -f gateway.yaml --dry-run --show-diff

# Apply
tfy apply -f gateway.yaml
```

**Do NOT delegate gateway applies to the `deploy` skill** (which is for service/application deployments). Gateway configs (`type: gateway-*`, `type: provider-account/*`) are applied inline with `tfy apply`.

**Test after apply:**
```bash
# Quick smoke test via curl
curl "${TFY_BASE_URL}/api/llm/chat/completions" \
  -H "Authorization: Bearer ${TFY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia-external/nemotron-nano",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 50
  }'
```

Or via Python:
```python
from openai import OpenAI
client = OpenAI(api_key="<PAT-or-VAT>", base_url=f"{TFY_BASE_URL}/api/llm")
resp = client.chat.completions.create(
    model="nvidia-external/nemotron-nano",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(resp.choices[0].message.content)
```

> **Note:** The `deploy` skill reference in the Routing Config section below is only for CI/CD GitOps pipelines — not for one-off gateway config applies.

## Load Balancing & Routing

The gateway supports intelligent request routing across multiple model instances.

### Weight-Based Routing

Distribute requests proportionally:
- 90% to Azure GPT-4o (primary)
- 10% to OpenAI GPT-4o (overflow)

### Latency-Based Routing

Automatically route to the lowest-latency model:
- Measures time per output token over last 20 minutes
- Models within 1.2x of fastest are treated equally
- Models with < 3 recent requests get preferential routing for data collection

### Priority-Based Routing

Route to highest-priority healthy model with SLA cutoff:
- Monitors average Time Per Output Token over 3-minute windows
- Auto-marks models unhealthy when TPOT exceeds threshold
- Automatic recovery when metrics improve

### Fallback Configuration

- **Default retry codes**: 429, 500, 502, 503
- **Default fallback codes**: 401, 403, 404, 429, 500, 502, 503
- Per-target retry attempts and delay intervals
- Auto-failover to backup models when primary is down

### Routing Config via GitOps

Routing configurations can be managed as YAML and applied via `tfy apply`:

```bash
# Store routing config in git, apply via CLI
tfy apply -f gateway-routing-config.yaml
```

See `deploy` skill (declarative apply workflow) and `gitops` skill for CI/CD integration.

## Rate Limiting

Control model usage per user, team, or application:

- **Requests per minute (RPM)** limits
- **Tokens per minute (TPM)** limits
- Per-model or global limits
- Configure via TrueFoundry dashboard → AI Gateway → Rate Limiting

## Budget Controls

Enforce cost limits:

- Per-user spending caps
- Per-team budgets
- Per-model cost limits
- Automatic blocking when budget exceeded
- Configure via TrueFoundry dashboard → AI Gateway → Budget Limiting

## Observability

### Request Logging

All gateway requests are logged with:
- Input/output tokens
- Latency (TTFT, total)
- Cost
- Model and provider
- User identity
- Custom metadata

### Custom Metadata

Tag requests with custom metadata for tracking:

```python
response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    extra_headers={
        "X-TFY-LOGGING-CONFIG": '{"project": "my-app", "environment": "production"}'
    },
)
```

### Analytics

View usage analytics in TrueFoundry dashboard:
- Requests/minute per model
- Tokens/minute per model
- Failures/minute per model
- Cost breakdown by model, user, team

### OpenTelemetry Integration

Export traces to your observability stack:
- Prometheus + Grafana
- Datadog
- Custom OTEL collectors

## Guardrails

For content filtering, PII detection, prompt injection prevention, and custom safety rules, use the `guardrails` skill. It configures guardrail providers and rules that apply to this gateway's traffic.

## MCP Gateway Attachment Flow

If a user has already deployed a tool server and wants to attach it to MCP gateway:

1. Verify deployment status and endpoint URL (`deploy` + `applications` skills)
2. Register the endpoint as an MCP server (`mcp-servers` skill)
3. Confirm registration ID/name and share how to reference it in policies

## Framework Integration

The gateway works with popular AI frameworks:

### LangChain

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="openai/gpt-4o",
    api_key="<your-PAT-or-VAT>",
    base_url="https://<your-truefoundry-url>/api/llm",
)
```

### LlamaIndex

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    model="openai/gpt-4o",
    api_key="<your-PAT-or-VAT>",
    api_base="https://<your-truefoundry-url>/api/llm",
)
```

### Cursor / Claude Code / Cline

Configure the gateway as a custom API endpoint in your coding assistant settings:
- Base URL: `{TFY_BASE_URL}/api/llm`
- API Key: Your PAT or VAT

## Presenting Gateway Info

When the user asks about gateway configuration:

```
AI Gateway:
  Endpoint: https://your-org.truefoundry.cloud/api/llm
  Auth:     Personal Access Token (PAT) or Virtual Access Token (VAT)

Available Models (check dashboard for current list):
| Model Name        | Provider     | Type        |
|-------------------|-------------|-------------|
| openai/gpt-4o     | OpenAI      | Cloud       |
| my-gemma-2b       | Self-hosted | vLLM (T4)   |
| anthropic/claude   | Anthropic   | Cloud       |

Usage:
  export OPENAI_BASE_URL="https://your-org.truefoundry.cloud/api/llm"
  export OPENAI_API_KEY="your-token"
  # Then use any OpenAI-compatible SDK
```

</instructions>

<success_criteria>

## Success Criteria

- The user can call LLMs through the gateway endpoint using an OpenAI-compatible SDK or cURL
- The user has a valid authentication token (PAT or VAT) configured for gateway access
- The agent has confirmed the target model name is available in the user's gateway configuration
- The user can verify successful responses from the gateway with correct model output
- The agent has provided working code snippets tailored to the user's language and framework
- Rate limiting, budget controls, or routing are configured if the user requested them

</success_criteria>

<references>

## Composability

- **Deploy model first**: Use `llm-deploy` skill to deploy a self-hosted model, then add to gateway
- **Need API key**: Create PAT/VAT in TrueFoundry dashboard → Access
- **Rate limiting**: Configure in dashboard → AI Gateway → Rate Limiting
- **Routing config**: Use `deploy` skill (declarative apply workflow) to apply routing YAML via GitOps
- **tool servers**: Use `deploy` skill to deploy tool servers (service with tool-proxy), register in gateway
- **Check deployed models**: Use `applications` skill to see running model services
- **Benchmark through gateway**: Use your preferred load-testing tool against gateway endpoints

</references>

<troubleshooting>

## Error Handling

### 401 Unauthorized
```
Gateway authentication failed. Check:
- API key (PAT or VAT) is valid and not expired
- Using correct header: Authorization: Bearer <token>
```

### 403 Forbidden
```
Model access denied. Your token may not have access to this model.
- PATs inherit user permissions
- VATs only have access to explicitly selected models
- Check with your admin to grant model access
```

### 429 Rate Limited
```
Rate limit exceeded. Options:
- Wait and retry (check Retry-After header)
- Request higher limits from admin
- Use load balancing to distribute across providers
```

### 502/503 Provider Error
```
Upstream provider error. The gateway will automatically:
- Retry on configured status codes
- Fallback to alternate models if routing is configured
If persistent, check provider status page or self-hosted model health.
```

### Model Not Found
```
Model name not found in gateway. Check:
- Exact model name in TrueFoundry dashboard → AI Gateway → Models
- Provider account is active and model is enabled
- Your token has access to this model
```

</troubleshooting>
