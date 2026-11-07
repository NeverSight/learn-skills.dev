---
name: freellmapi-proxy
description: OpenAI-compatible proxy aggregating 14 free-tier LLM providers with automatic failover and per-key rate tracking.
triggers:
  - set up freellmapi proxy
  - aggregate free LLM providers
  - openai compatible free tier proxy
  - route requests across multiple AI providers
  - free llm api failover setup
  - add provider keys to freellmapi
  - configure fallback chain for LLM providers
  - use free groq gemini cerebras together
---

# FreeLLMAPI Proxy

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

FreeLLMAPI is a self-hosted OpenAI-compatible proxy that aggregates free-tier API keys from ~14 AI providers (Google, Groq, Cerebras, SambaNova, NVIDIA, Mistral, OpenRouter, GitHub Models, Hugging Face, Cohere, Cloudflare, Zhipu, Moonshot, MiniMax) behind a single `/v1/chat/completions` endpoint. It handles automatic failover on 429/5xx, per-key rate tracking, sticky sessions for multi-turn conversations, and AES-256-GCM encrypted key storage.

---

## Installation

**Prerequisites:** Node.js 20+, npm.

```bash
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi
npm install

# Generate encryption key and set up environment
cp .env.example .env
echo "ENCRYPTION_KEY=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")" >> .env

# Development (server + Vite dashboard on :5173)
npm run dev

# Production build
npm run build
node server/dist/index.js   # serves API + dashboard on :3001
```

---

## Environment Variables

```bash
# .env
ENCRYPTION_KEY=<64-char hex string>   # Required — AES-256 key for provider key storage
PORT=3001                              # Optional — defaults to 3001
NODE_ENV=production                    # Optional
```

Never commit `.env`. The `ENCRYPTION_KEY` protects all stored provider API keys.

---

## Key Commands

```bash
npm run dev        # Start Express server + Vite dashboard in watch mode
npm run build      # Compile TypeScript server + build React dashboard
npm run lint       # ESLint across server/ and client/
npm run test       # Run test suite
```

---

## Provider Setup

1. Open the dashboard at `http://localhost:5173` (dev) or `http://localhost:3001` (prod).
2. Navigate to **Keys** page.
3. Add raw API keys for each provider you have. Keys are encrypted before SQLite storage.
4. Navigate to **Fallback Chain** to reorder provider priority.
5. Copy your unified `freellmapi-…` bearer token from the **Keys** page header.

**Supported providers and what to put in:**

| Provider | Where to get a free key |
|---|---|
| Google Gemini | https://ai.google.dev |
| Groq | https://groq.com |
| Cerebras | https://cerebras.ai |
| SambaNova | https://cloud.sambanova.ai |
| NVIDIA NIM | https://build.nvidia.com |
| Mistral | https://mistral.ai |
| OpenRouter | https://openrouter.ai |
| GitHub Models | https://github.com/marketplace/models |
| Hugging Face | https://huggingface.co |
| Cohere | https://cohere.com |
| Cloudflare Workers AI | https://developers.cloudflare.com/workers-ai |
| Zhipu | https://bigmodel.cn |
| Moonshot | https://platform.moonshot.cn |
| MiniMax | https://platform.minimax.io |

---

## Using the API

### Python (openai SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:3001/v1",
    api_key="freellmapi-your-unified-key",  # from dashboard Keys page
)

# Let the router pick the best available provider
response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Explain async/await in Python in two sentences."}],
)

print(response.choices[0].message.content)
# Which provider actually served this request:
print("Routed via:", response.headers.get("x-routed-via"))
```

### Request a specific model

```python
# Request a specific model — router finds a provider that has it
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Write a haiku about SQLite."}],
)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "List 5 TypeScript best practices."}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
print()
```

### curl

```bash
# Non-streaming
curl http://localhost:3001/v1/chat/completions \
  -H "Authorization: Bearer $FREELLMAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# Streaming
curl http://localhost:3001/v1/chat/completions \
  -H "Authorization: Bearer $FREELLMAPI_KEY" \
  -H "Content-Type: application/json" \
  --no-buffer \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Count to 5 slowly"}],
    "stream": true
  }'

# List available models
curl http://localhost:3001/v1/models \
  -H "Authorization: Bearer $FREELLMAPI_KEY"
```

### TypeScript / Node.js

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:3001/v1",
  apiKey: process.env.FREELLMAPI_KEY,
});

async function chat(userMessage: string): Promise<string> {
  const response = await client.chat.completions.create({
    model: "auto",
    messages: [{ role: "user", content: userMessage }],
  });
  return response.choices[0].message.content ?? "";
}

// Streaming version
async function streamChat(userMessage: string): Promise<void> {
  const stream = await client.chat.completions.create({
    model: "auto",
    messages: [{ role: "user", content: userMessage }],
    stream: true,
  });

  for await (const chunk of stream) {
    const delta = chunk.choices[0]?.delta?.content;
    if (delta) process.stdout.write(delta);
  }
  console.log();
}
```

---

## Tool Calling

Tool calling works across all supported providers. OpenAI-compatible providers receive requests verbatim; Gemini requests are automatically translated to `functionDeclarations`/`functionResponse` format and back.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:3001/v1",
    api_key="freellmapi-your-unified-key",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        },
    }
]

# Step 1: Model requests a tool call
first = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "What's the weather in Karachi?"}],
    tools=tools,
    tool_choice="required",
)

call = first.choices[0].message.tool_calls[0]
print(f"Tool requested: {call.function.name}({call.function.arguments})")

# Step 2: Execute the tool locally, feed result back
final = client.chat.completions.create(
    model="auto",
    messages=[
        {"role": "user", "content": "What's the weather in Karachi?"},
        first.choices[0].message,  # assistant message with tool_calls
        {
            "role": "tool",
            "tool_call_id": call.id,
            "content": '{"temp_c": 32, "condition": "sunny"}',
        },
    ],
    tools=tools,
)

print(final.choices[0].message.content)
```

### Streaming tool calls

```python
stream = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "What's the weather in Karachi?"}],
    tools=tools,
    tool_choice="required",
    stream=True,
)

tool_call_chunks = []
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.tool_calls:
        tool_call_chunks.extend(delta.tool_calls)
    if chunk.choices[0].finish_reason == "tool_calls":
        print("Tool call complete — assemble chunks and execute")
```

---

## Multi-turn Conversations (Sticky Sessions)

The proxy keeps multi-turn conversations on the same model for 30 minutes to avoid hallucination spikes from mid-conversation model switches. Pass a consistent `session_id` in requests if the provider supports it, or rely on the proxy's automatic session tracking.

```python
messages = [{"role": "system", "content": "You are a helpful coding assistant."}]

# Turn 1
messages.append({"role": "user", "content": "Write a Python function to flatten a nested list."})
resp1 = client.chat.completions.create(model="auto", messages=messages)
assistant_msg = resp1.choices[0].message
messages.append({"role": "assistant", "content": assistant_msg.content})
print(assistant_msg.content)

# Turn 2 — sticky session keeps same provider
messages.append({"role": "user", "content": "Now add type hints to that function."})
resp2 = client.chat.completions.create(model="auto", messages=messages)
print(resp2.choices[0].message.content)
```

---

## LangChain Integration

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

llm = ChatOpenAI(
    model="auto",
    openai_api_base="http://localhost:3001/v1",
    openai_api_key=os.environ["FREELLMAPI_KEY"],
    streaming=True,
)

response = llm.invoke([HumanMessage(content="Summarise the CAP theorem in one paragraph.")])
print(response.content)
```

---

## Response Headers

Every response includes diagnostic headers:

| Header | Description |
|---|---|
| `X-Routed-Via` | `<platform>/<model>` — which provider served the request |
| `X-Fallback-Attempts` | Number of providers tried before success (only present if > 0) |

```python
response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "hi"}],
)
# Headers are on the raw httpx response:
raw = response._response  # openai SDK exposes underlying httpx response
print(raw.headers.get("x-routed-via"))        # e.g. "groq/llama-4-scout"
print(raw.headers.get("x-fallback-attempts")) # e.g. "2"
```

---

## How the Router Works

```
Request arrives
      │
      ▼
Router scans fallback chain (priority order)
      │
      ├─ For each model: is there a healthy key under all rate caps?
      │     RPM / RPD / TPM / TPD tracked per (platform, model, key)
      │
      ├─ Picks first viable (platform, model, key) tuple
      │
      ├─ Decrypts key in-memory, calls provider SDK
      │
      └─ On 429 / 5xx / timeout:
            Put key on cooldown → retry next model (up to 20 attempts)
```

**Rate limit tracking:** The router tracks `RPM`, `RPD`, `TPM`, and `TPD` counters per `(platform, model, key)` triple. When a key hits a cap it's cooled down automatically and the next viable key/model is tried.

**Health checks:** Background probes classify each key as `healthy`, `rate_limited`, `invalid`, or `error`. The router skips non-healthy keys without making a live request.

---

## Dashboard Pages

| Page | Purpose |
|---|---|
| **Keys** | Add/remove provider credentials, view health status, copy unified API key |
| **Fallback Chain** | Drag to reorder provider priority |
| **Playground** | Interactive chat showing which provider served each message + latency |
| **Analytics** | Request volume, success rate, token counts, latency, per-provider breakdown (24h/7d/30d) |

---

## Production Deployment (Raspberry Pi / Linux)

```bash
# Build
npm run build

# Install PM2
npm install -g pm2

# Start
pm2 start server/dist/index.js --name freellmapi
pm2 save
pm2 startup

# nginx reverse proxy (optional)
# /etc/nginx/sites-available/freellmapi
server {
    listen 80;
    server_name your.domain.com;
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_buffering off;          # Required for SSE streaming
        proxy_cache_control no-cache; # Required for SSE streaming
    }
}
```

Memory footprint: ~40 MB RSS at idle on a Pi 4.

---

## Adding a New Provider

Create a new adapter in `server/src/providers/`:

```typescript
// server/src/providers/myprovider.ts
import type { ProviderAdapter, ChatRequest, ChatResponse } from "../types";

export const myProviderAdapter: ProviderAdapter = {
  name: "myprovider",
  models: ["my-model-v1", "my-model-v2"],

  async chat(request: ChatRequest, apiKey: string): Promise<ChatResponse> {
    // Call provider API, return OpenAI-shaped response
    const res = await fetch("https://api.myprovider.com/v1/chat", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: request.model,
        messages: request.messages,
      }),
    });
    const data = await res.json();
    return {
      id: data.id,
      object: "chat.completion",
      choices: [{ message: data.choices[0].message, finish_reason: "stop", index: 0 }],
      usage: data.usage,
    };
  },

  async *stream(request: ChatRequest, apiKey: string): AsyncGenerator<string> {
    // Yield SSE chunks
  },
};
```

Register in `server/src/providers/index.ts` and add rate limit caps to the router config.

---

## Troubleshooting

**"No healthy keys available"**
- Check the Keys dashboard — all keys may be rate-limited or invalid.
- Wait for cooldown (usually a few minutes for RPM limits) or add more keys.
- Verify the key is valid by testing it directly against the provider's API.

**Requests always fall back to the same provider**
- Check the Fallback Chain order in the dashboard.
- Ensure keys for higher-priority providers are marked `healthy`.

**Streaming stops mid-response**
- If behind nginx, ensure `proxy_buffering off` is set.
- Check provider-side token/minute caps — the stream may be cut by a mid-stream rate limit.

**`ENCRYPTION_KEY` error on startup**
- Ensure `ENCRYPTION_KEY` in `.env` is exactly 64 hex characters (32 bytes).
- Regenerate: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`

**Tool calls not working with a specific provider**
- Not all free-tier models support function calling. Check the provider's docs.
- Try `model="auto"` — the router will pick a tool-capable model.
- Gemini tool calls are auto-translated; others pass through as-is.

**High latency on first request**
- Health checks run periodically in the background. The first request after startup may probe a few keys. Subsequent requests are faster.

---

## Limitations

- Text-only — no vision/multimodal inputs
- No embeddings (`/v1/embeddings`)
- No image generation (`/v1/images/*`)
- No audio/speech (`/v1/audio/*`)
- No legacy completions (`/v1/completions`)
- No moderation (`/v1/moderations`)
- `n > 1` not supported (single completion per request)
- Single-user by design — no per-user billing or multi-tenant auth
- Personal/experimental use only — review each provider's ToS before production use
