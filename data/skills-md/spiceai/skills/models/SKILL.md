---
name: models
description: Configure AI/LLM model providers and connections in Spice — OpenAI, Anthropic, Azure, Google, xAI, Bedrock, Databricks, HuggingFace, and local GGUF models. Use this skill whenever the user wants to add a model, configure a specific LLM provider, set up an OpenAI-compatible endpoint (e.g. Groq, Ollama), serve a local model, configure system prompts, set parameter overrides (temperature, response format), or understand which providers are available. This skill is the model connector reference. For AI features like tools, memory, workers, and NSQL, see chat.
---

# Spice Model Providers

Model providers serve large language models (LLMs) through a unified OpenAI-compatible API.

## Version Compatibility

Written for **Spice v2.4.x** (checked against v2.4.0-rc.2). Check the user's runtime version before recommending configuration:

- **Find it**: `spice version` (CLI and runtime), `spiced --version`, or the image tag (`spiceai/spiceai:<tag>`, Helm `image.tag`). Not the runtime version: `version: v2` in `spicepod.yaml` (manifest schema) or SQL `version()` (DataFusion).
- **Markers**: unmarked content applies to v2.0.0 and later. Later additions are marked `(vX.Y.Z+)`; changes are marked **Removed**, **Deprecated**, **Changed**, or **Breaking in vX.Y.Z**.
- **Older runtime**: don't recommend a newer feature — offer `spice upgrade` or an alternative — and read that release line's docs, e.g. `https://spiceai.org/docs/v2.2/...` (`/docs/next/` tracks trunk, not a release). On v1.x, use the [v1.11 docs](https://spiceai.org/docs/v1.11) and the [v2.0 upgrade guide](https://spiceai.org/releases/v2.0-stable#upgrade-guide-from-v1x).
- **Newer runtime**: check the [release notes](https://spiceai.org/releases) for changes after v2.4.0-rc.2.

| Old | Change | Use instead |
| --- | --- | --- |
| `google_api_key` (Google AI Studio) | Breaking in v2.3.0 | `google_project` + `google_location` + one credential |
| `perplexity:` provider | Removed in v2.0.0 | Another provider |
| ONNX models, `/v1/predict` | Removed in v2.2.0 | An LLM provider |
| `spice.ai/<org>/<app>/models/<model>` (ONNX) | Removed in v2.2.0 | `spice.ai:<provider>/<model>` |
| `openai_<param>` on non-OpenAI providers | Deprecated in v1.5.0 | `<provider>_<param>` (e.g. `hf_temperature`) |
| `from: anthropic` defaulting to `claude-3-5-sonnet-latest` | Changed in v2.3.0 (retired model) | Default `claude-sonnet-4-6`, or pin `anthropic:<id>` |
| `evals:` section, `/v1/evals` | Removed in v2.0.0 | Nothing — delete the section |

## Model interfaces

Provider definitions live under `models` in `spicepod.yaml`. Inspect loaded models with
`spice models` or runtime `GET /v1/models`; use `chat` for `spice chat` and
`POST /v1/chat/completions`. Preserve the configured model name when moving between CLI, HTTP,
and OpenAI-compatible clients. Use `sdk` for client integration and `cloud` for hosted deployments.

## Basic Configuration

```yaml
models:
  - from: <provider>:<model_id>
    name: <model_name>
    params:
      <provider>_api_key: ${ secrets:API_KEY }
      tools: auto # optional: enable runtime tools
      system_prompt: | # optional: default system prompt
        You are a helpful assistant.
```

## Supported Providers

| Provider               | From Format                              | Status            |
| ---------------------- | ---------------------------------------- | ----------------- |
| OpenAI (or compatible) | `openai:gpt-4o`                          | Stable            |
| Anthropic              | `anthropic:claude-sonnet-4-5`            | Alpha             |
| Azure OpenAI           | `azure:gpt-4o-mini`                      | Alpha             |
| Google (Vertex AI)     | `google:gemini-2.5-pro`                  | Alpha             |
| xAI                    | `xai:grok-4.3`                           | Alpha             |
| Amazon Bedrock         | `bedrock:amazon.nova-lite-v1:0`          | Alpha             |
| Databricks             | `databricks:databricks-llama-4-maverick` | Alpha             |
| Spice.ai (v2.2.0+)     | `spice.ai:openai/gpt-4o`                 | Release Candidate |
| HuggingFace            | `hf:meta-llama/Llama-3-8B-Instruct`      | Release Candidate |
| Local file             | `file:./models/llama.gguf`               | Release Candidate |

Prefix aliases: `huggingface:` = `hf:`; `spiceai:` = `spice.ai:` (model ids are `<provider>/<model>`).
The `perplexity` provider is **Removed in v2.0.0**; ONNX/traditional ML models and `/v1/predict` are
**Removed in v2.2.0** — use an LLM provider instead. `from: xai` with no model defaults to `grok-4.3`.

**Breaking in v2.3.0 — Google models use Vertex AI.** `from: google` no longer accepts
`google_api_key` (Google AI Studio). Authenticate as a GCP service account with
`google_project`, `google_location`, and exactly one of `google_service_account_path`,
`google_service_account_key`, or `google_application_default_credentials: true`.

`from: anthropic` with no model id defaults to `claude-sonnet-4-6` (**Changed in v2.3.0**; the old
`claude-3-5-sonnet-latest` default is retired). HuggingFace chat models take `hf_token`
(**Changed in v2.3.0**; v2.2.0–v2.2.1 read only `huggingface_token`, still accepted as an alias).

## Features

| Feature                   | Description                            |
| ------------------------- | -------------------------------------- |
| **Tools**                 | SQL, search, memory, MCP               |
| **System Prompts**        | Declarative default system prompts     |
| **Parameterized Prompts** | Jinja templating in system prompts     |
| **Parameter Overrides**   | Temperature, response format, etc.     |
| **Memory**                | Persistent memory across conversations |
| **Local Serving**         | CUDA/Metal accelerated local models    |

## Examples

### OpenAI with Tools

```yaml
models:
  - from: openai:gpt-4o
    name: gpt4
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: auto
```

### OpenAI-Compatible Provider (e.g., Groq)

```yaml
models:
  - from: openai:llama3-groq-70b-8192-tool-use-preview
    name: groq-llama
    params:
      endpoint: https://api.groq.com/openai/v1
      openai_api_key: ${ secrets:GROQ_API_KEY }
```

### Google (Vertex AI) (v2.3.0+)

```yaml
models:
  - from: google:gemini-2.5-pro
    name: gemini
    params:
      google_project: my-project
      google_location: us-central1
      google_service_account_path: /etc/spice/gcp-sa.json
      # or google_service_account_key / google_application_default_credentials
```

### Model with Memory

```yaml
datasets:
  - from: memory:store
    name: llm_memory
    access: read_write

models:
  - from: openai:gpt-4o
    name: assistant
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: memory, sql
```

### With System Prompt and Parameter Overrides

```yaml
models:
  - from: openai:gpt-4o
    name: pirate_haikus
    params:
      system_prompt: |
        Write everything in Haiku like a pirate.
      openai_temperature: 0.1 # prefix = provider prefix, e.g. anthropic_temperature, hf_temperature
      openai_response_format: { 'type': 'json_object' } # a YAML map, not a quoted string
```

### Local Model (GGUF)

```yaml
models:
  - from: file:./models/llama-3.gguf
    name: local_llama
```

## Using Models

### Chat Completions API (OpenAI-compatible)

```bash
curl http://localhost:8090/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

Existing applications using OpenAI SDKs can swap endpoints without code changes.

### NSQL (Text-to-SQL)

The `/v1/nsql` endpoint converts natural language to SQL and executes it. Spice uses tools like `table_schema`, `random_sample`, and `sample_distinct_columns` to help models write accurate, contextual SQL:

```bash
curl -XPOST "http://localhost:8090/v1/nsql" \
  -H "Content-Type: application/json" \
  -d '{"query": "What was the highest tip any passenger gave?"}'
```

### CLI

```bash
spice chat
chat> Hello!
```

## Documentation

- [Model Providers](https://spiceai.org/docs/components/models)
- [Models Reference](https://spiceai.org/docs/reference/spicepod/models)
- [Model Grades Report](https://spiceai.org/docs/reference/models)
- [LLM Tools](https://spiceai.org/docs/features/large-language-models/tools)
- [Memory](https://spiceai.org/docs/features/large-language-models/memory)
- [Parameter Overrides](https://spiceai.org/docs/features/large-language-models/parameter_overrides)
- [Parameterized Prompts](https://spiceai.org/docs/features/large-language-models/parameterized_prompts)
- [Local Model Serving](https://spiceai.org/docs/features/large-language-models/serving)
- [Web Search](https://spiceai.org/docs/features/web-search) — via OpenAI hosted tools; the `websearch` tool was **Removed in v2.0.0**
