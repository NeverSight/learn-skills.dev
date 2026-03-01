---
name: letta-configuration
description: Configure LLM models and providers for Letta agents and servers. Use when setting model handles, adjusting temperature/tokens, configuring provider-specific settings, setting up BYOK providers, or configuring self-hosted deployments with environment variables.
license: MIT
---

# Letta Configuration

Complete guide for configuring models on agents and providers on servers.

## When to Use This Skill

**Agent-level (model configuration):**
- Creating agents with specific model configurations
- Adjusting model settings (temperature, max tokens, context window)
- Configuring provider-specific features (OpenAI reasoning, Anthropic thinking)
- Changing models on existing agents

**Server-level (provider configuration):**
- Setting up BYOK (bring your own key) providers
- Configuring self-hosted deployments with environment variables
- Validating provider credentials
- Setting up custom OpenAI-compatible endpoints

**Not covered here:** Model selection advice (which model to choose) - see `agent-development` skill.

---

## Part 1: Model Configuration (Agent-Level)

### Model Handles

Models use a `provider/model-name` format:

| Provider | Handle Prefix | Example |
|----------|---------------|---------|
| OpenAI | `openai/` | `openai/gpt-4o`, `openai/gpt-4o-mini` |
| Anthropic | `anthropic/` | `anthropic/claude-sonnet-4-5-20250929` |
| Google AI | `google_ai/` | `google_ai/gemini-2.0-flash` |
| Azure OpenAI | `azure/` | `azure/gpt-4o` |
| AWS Bedrock | `bedrock/` | `bedrock/anthropic.claude-3-5-sonnet` |
| Groq | `groq/` | `groq/llama-3.3-70b-versatile` |
| Together | `together/` | `together/meta-llama/Llama-3-70b` |
| OpenRouter | `openrouter/` | `openrouter/anthropic/claude-3.5-sonnet` |
| Ollama (local) | `ollama/` | `ollama/llama3.2` |

### Basic Model Configuration

```python
from letta_client import Letta

client = Letta(api_key="your-api-key")

agent = client.agents.create(
    model="openai/gpt-4o",
    model_settings={
        "provider_type": "openai",  # Required - must match model provider
        "temperature": 0.7,
        "max_output_tokens": 4096,
    },
    context_window_limit=128000
)
```

### Common Settings

| Setting | Type | Description |
|---------|------|-------------|
| `provider_type` | string | **Required.** Must match model provider (`openai`, `anthropic`, `google_ai`, etc.) |
| `temperature` | float | Controls randomness (0.0-2.0). Lower = more deterministic. |
| `max_output_tokens` | int | Maximum tokens in the response. |

### Changing an Agent's Model

```python
client.agents.update(
    agent_id=agent.id,
    model="anthropic/claude-sonnet-4-5-20250929",
    model_settings={"provider_type": "anthropic", "temperature": 0.5},
    context_window_limit=64000
)
```

**Note:** Agents retain memory and tools when changing models.

### Provider-Specific Settings

For OpenAI reasoning models and Anthropic extended thinking, see `references/provider-settings.md`.

---

## Part 2: Provider Configuration (Server-Level)

### Quick Start

```bash
# Add provider via API
python scripts/setup_provider.py --type openai --api-key sk-...

# Generate .env for Docker
python scripts/generate_env.py --providers openai,anthropic,ollama

# Validate credentials
python scripts/validate_provider.py --provider-id provider-xxx
```

### Add BYOK Provider

```python
# Via REST API
curl -X POST http://localhost:8283/v1/providers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My OpenAI",
    "provider_type": "openai",
    "api_key": "sk-your-key-here"
  }'
```

### Supported Provider Types

`openai`, `anthropic`, `azure`, `google_ai`, `google_vertex`, `ollama`, `groq`, `deepseek`, `xai`, `together`, `mistral`, `cerebras`, `bedrock`, `vllm`, `sglang`, `hugging_face`, `lmstudio_openai`

For detailed configuration of each provider, see:
- `references/common_providers.md` - OpenAI, Anthropic, Azure, Google
- `references/self_hosted_providers.md` - Ollama, vLLM, LM Studio
- `references/all_providers.md` - Complete reference
- `references/environment_variables.md` - Docker/self-hosted setup

---

## Anti-Hallucination Checklist

Before configuring:

- [ ] Model handle uses correct `provider/model-name` format
- [ ] `model_settings` includes required `provider_type` field
- [ ] `context_window_limit` is set at agent level, not in `model_settings`
- [ ] Provider-specific settings use correct nested structure
- [ ] For self-hosted: embedding model is specified
- [ ] Temperature is within valid range (0.0-2.0)

## Scripts

**Model configuration:**
- `scripts/basic_config.py` - Basic model configuration
- `scripts/basic_config.ts` - TypeScript equivalent
- `scripts/change_model.py` - Changing models on existing agents
- `scripts/provider_specific.py` - OpenAI reasoning, Anthropic thinking

**Provider configuration:**
- `scripts/setup_provider.py` - Add providers via REST API
- `scripts/validate_provider.py` - Check provider credentials
- `scripts/generate_env.py` - Generate .env for Docker
