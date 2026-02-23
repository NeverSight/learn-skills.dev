---
name: eurouter-integration
description: Guide developers integrating EUrouter into their applications. EUrouter is an OpenAI-compatible AI gateway for EU/GDPR compliance. Use when integrating EUrouter, switching from OpenRouter or OpenAI, configuring EU data residency, routing AI requests to EU providers, managing API keys, or asking about EUrouter's API for chat completions, embeddings, streaming, tool calling, vision, model routing, or GDPR compliance features.
license: MIT
metadata:
  author: eurouter
  version: "1.0"
allowed-tools: Read
---

# EUrouter Integration Guide

You are helping a developer integrate **EUrouter** into their application. EUrouter is a drop-in replacement for the OpenAI API, purpose-built for EU customers requiring GDPR compliance. It routes AI requests to 10 providers through a single OpenAI-compatible API at `https://api.eurouter.ai`.

**Supported providers:** OpenAI, Anthropic, Mistral, Scaleway (FR), GreenPT, Microsoft Foundry, Nebius, IONOS (DE), OVHcloud (FR), AWS Bedrock.

When helping developers, always load the relevant reference files from the `references/` directory in this skill folder based on what they need. Do not load all references at once.

---

## Authentication

EUrouter uses API keys in the format `eur_<publicId>.<secret>`.

Send the key via either header:
- `Authorization: Bearer eur_...`
- `x-api-key: eur_...`

For organization-scoped requests, add: `x-org-id: <uuid>`

Keys are created via `POST /api/v1/keys` and the full key is shown **only once** at creation. It cannot be retrieved later.

---

## Drop-in Migration from OpenAI

EUrouter is designed as a drop-in replacement. Only two things change:

**Python (openai SDK):**
```python
from openai import OpenAI

# Before (OpenAI direct)
# client = OpenAI(api_key="sk-...")

# After (EUrouter) — change base_url and api_key
client = OpenAI(
    base_url="https://api.eurouter.ai/api/v1",
    api_key="eur_YOUR_KEY_HERE"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Node.js (openai SDK):**
```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.eurouter.ai/api/v1",
  apiKey: "eur_YOUR_KEY_HERE",
});

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
});
```

**Important:** All existing OpenAI model names work as-is (e.g., `gpt-4o`, `claude-3-5-sonnet`, `mistral-large-3`). No model name changes needed when migrating.

---

## Core Endpoints

All endpoints are prefixed with `/api`. Base URL: `https://api.eurouter.ai`

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/chat/completions` | POST | Yes | Chat completions (streaming, tools, vision, audio, reasoning) |
| `/api/v1/completions` | POST | Yes | Legacy text completions |
| `/api/v1/embeddings` | POST | Yes | Text embeddings |
| `/api/v1/responses` | POST | Yes | OpenAI Responses API compatible |
| `/api/v1/models` | GET | No | List/filter model catalog |
| `/api/v1/providers` | GET | No | List available providers |
| `/api/v1/credits` | GET | Yes | Check credit balance (EUR) |
| `/api/v1/keys` | CRUD | Yes | Manage API keys |
| `/api/v1/routing-rules` | CRUD | Yes | Manage named routing configs |
| `/health` | GET | No | Health check |

For full endpoint schemas, load `references/endpoints.md`.

---

## EU/GDPR Compliance

This is EUrouter's key differentiator. Add a `provider` object to any generation request to enforce compliance:

```json
{
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": "Hello"}],
  "provider": {
    "data_residency": "eu",
    "eu_owned": true,
    "data_collection": "deny",
    "max_retention_days": 0
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data_residency` | `string` | Region code — `"eu"`, `"de"`, `"fr"`, etc. Only endpoints in that region |
| `eu_owned` | `boolean` | Only EU-headquartered providers (Scaleway, IONOS, OVHcloud, GreenPT, Mistral) |
| `data_collection` | `"allow" \| "deny"` | `"deny"` excludes providers that use data for training |
| `max_retention_days` | `number` | Max data retention. `0` = zero-data-retention only |

**Ready-to-use compliance profiles:**

```json
// Strict GDPR: EU owned, no training data, zero retention, EU hosted
{ "eu_owned": true, "data_collection": "deny", "max_retention_days": 0, "data_residency": "eu" }

// EU hosted, cheapest price
{ "data_residency": "eu", "sort": "price" }

// Specific EU providers only
{ "only": ["scaleway", "ionos", "ovhcloud"] }
```

For all provider preference fields, load `references/provider-preferences.md`.

---

## Model Fallback

Pass a `models` array to try multiple models in order. If all providers for the first model fail, EUrouter tries the next:

```json
{
  "models": ["claude-3-5-sonnet", "gpt-4o", "mistral-large-3"],
  "messages": [{"role": "user", "content": "Hello"}],
  "provider": { "data_residency": "eu" }
}
```

**Note:** Model fallback is NOT supported for embeddings (vector dimensions differ between models). Only provider fallback (same model, different provider endpoint) works for embeddings.

---

## Routing Rules

Create reusable routing configurations to avoid repeating provider preferences on every request:

```json
// Create a rule once:
// POST /api/v1/routing-rules
{
  "name": "gdpr-strict",
  "provider": {
    "eu_owned": true,
    "data_collection": "deny",
    "max_retention_days": 0,
    "data_residency": "eu"
  }
}

// Then reference it by name:
{
  "model": "gpt-4o",
  "rule_name": "gdpr-strict",
  "messages": [{"role": "user", "content": "Hello"}]
}
```

You can also reference by UUID with `rule_id`. Per-request `provider` preferences merge with the rule — request-level values take precedence.

**Dry-run testing:** Use `POST /api/v1/routing-rules/dry-run` to preview which providers satisfy a routing config without making a real request.

For full routing rules API, load `references/routing-rules.md`.

---

## Model Discovery

```
GET /api/v1/models
GET /api/v1/models?provider=scaleway
GET /api/v1/models?supported_parameters=tools,vision
GET /api/v1/models?category=embedding
```

Prices are returned as strings in the model's `pricing` object with a `currency` field. Credits are in EUR.

---

## Response Headers

Every generation endpoint returns routing transparency headers:

| Header | Description |
|--------|-------------|
| `x-provider-id` | Internal provider UUID |
| `x-provider-slug` | Provider name (e.g., `openai`, `scaleway`) |
| `x-routing-strategy` | Strategy used for routing |
| `x-model-used` | Actual model slug used |
| `x-model-variant` | Variant suffix if applicable (`:free`, `:nitro`) |
| `x-fallback-count` | Number of provider fallbacks (only present if > 0) |
| `x-model-fallback-count` | Number of model fallbacks (only present if > 0) |

---

## Streaming

Set `"stream": true` for SSE streaming. Format is OpenAI-compatible:

```
data: {"id":"chatcmpl-...","object":"chat.completion.chunk","choices":[{"delta":{"content":"Hello"},"index":0,"finish_reason":null}]}

data: [DONE]
```

For usage stats in the final chunk, add `"stream_options": { "include_usage": true }`.

---

## Error Format

All errors follow:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Model not found"
  },
  "requestId": "uuid"
}
```

Key error codes: `UNAUTHORIZED` (401), `FORBIDDEN` (403), `NOT_FOUND` (404), `BAD_REQUEST` (400), `INSUFFICIENT_QUOTA` (402), `SERVICE_UNAVAILABLE` (503).

---

## Reference Files

Load these based on the developer's specific need:

| Need | File |
|------|------|
| Full endpoint request/response schemas | `references/endpoints.md` |
| All provider routing preference fields | `references/provider-preferences.md` |
| Routing rules CRUD + dry-run API | `references/routing-rules.md` |
| Python code examples (openai SDK) | `references/code-examples-python.md` |
| Node.js/TypeScript code examples | `references/code-examples-node.md` |
| curl examples | `references/code-examples-curl.md` |
