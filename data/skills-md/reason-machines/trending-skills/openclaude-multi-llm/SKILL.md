---
name: openclaude-multi-llm
description: Use Claude Code's full tool system with any OpenAI-compatible LLM — GPT-4o, DeepSeek, Gemini, Ollama, and 200+ models via environment variable configuration.
triggers:
  - "use claude code with openai"
  - "run claude code with a different model"
  - "plug in gpt-4o to claude code"
  - "use ollama with claude code"
  - "openclaude setup"
  - "claude code openai compatible provider"
  - "use deepseek with claude code tools"
  - "connect gemini to claude code"
---

# OpenClaude Multi-LLM Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenClaude is a fork of Claude Code that routes all LLM calls through an OpenAI-compatible shim (`openaiShim.ts`), letting you use any model that speaks the OpenAI Chat Completions API — GPT-4o, DeepSeek, Gemini via OpenRouter, Ollama, Groq, Mistral, Azure, and more — while keeping every Claude Code tool intact (Bash, FileRead, FileWrite, FileEdit, Glob, Grep, WebFetch, Agent, MCP, Tasks, LSP, NotebookEdit).

---

## Installation

### npm (recommended)

```bash
npm install -g @gitlawb/openclaude
# CLI command installed: openclaude
```

### From source (requires Bun)

```bash
git clone https://node.gitlawb.com/z6MkqDnb7Siv3Cwj7pGJq4T5EsUisECqR8KpnDLwcaZq5TPr/openclaude.git
cd openclaude
bun install
bun run build
# optionally link globally
npm link
```

### Run without build

```bash
bun run dev       # run directly with Bun, no build step
```

---

## Activation — Required Environment Variables

You must set `CLAUDE_CODE_USE_OPENAI=1` to enable the shim. Without it, the tool falls back to the Anthropic SDK.

| Variable | Required | Purpose |
|---|---|---|
| `CLAUDE_CODE_USE_OPENAI` | Yes | Set to `1` to activate OpenAI provider |
| `OPENAI_API_KEY` | Yes* | API key (*omit for local Ollama/LM Studio) |
| `OPENAI_MODEL` | Yes | Model identifier |
| `OPENAI_BASE_URL` | No | Custom endpoint (default: `https://api.openai.com/v1`) |
| `CODEX_API_KEY` | Codex only | ChatGPT/Codex access token |
| `CODEX_AUTH_JSON_PATH` | Codex only | Path to Codex CLI `auth.json` |

`OPENAI_MODEL` takes priority over `ANTHROPIC_MODEL` if both are set.

---

## Provider Configuration Examples

### OpenAI

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$OPENAI_API_KEY
export OPENAI_MODEL=gpt-4o
openclaude
```

### DeepSeek

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$DEEPSEEK_API_KEY
export OPENAI_BASE_URL=https://api.deepseek.com/v1
export OPENAI_MODEL=deepseek-chat
openclaude
```

### Google Gemini (via OpenRouter)

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$OPENROUTER_API_KEY
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_MODEL=google/gemini-2.0-flash
openclaude
```

### Ollama (local, no API key needed)

```bash
ollama pull llama3.3:70b

export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_MODEL=llama3.3:70b
openclaude
```

### Groq

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$GROQ_API_KEY
export OPENAI_BASE_URL=https://api.groq.com/openai/v1
export OPENAI_MODEL=llama-3.3-70b-versatile
openclaude
```

### Mistral

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$MISTRAL_API_KEY
export OPENAI_BASE_URL=https://api.mistral.ai/v1
export OPENAI_MODEL=mistral-large-latest
openclaude
```

### Azure OpenAI

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$AZURE_OPENAI_KEY
export OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment/v1
export OPENAI_MODEL=gpt-4o
openclaude
```

### Codex (ChatGPT backend)

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_MODEL=codexplan   # or codexspark for faster loops
# reads ~/.codex/auth.json automatically if present
# or set: export CODEX_API_KEY=$CODEX_TOKEN
openclaude
```

### LM Studio (local)

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:1234/v1
export OPENAI_MODEL=your-model-name
openclaude
```

### Together AI

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=$TOGETHER_API_KEY
export OPENAI_BASE_URL=https://api.together.xyz/v1
export OPENAI_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo
openclaude
```

---

## Architecture — How the Shim Works

The shim file is `src/services/api/openaiShim.ts` (724 lines). It duck-types the Anthropic SDK interface so the rest of Claude Code is unaware it's talking to a different provider.

```
Claude Code Tool System
        │
        ▼
Anthropic SDK interface (duck-typed)
        │
        ▼
openaiShim.ts  ← format translation layer
        │
        ▼
OpenAI Chat Completions API
        │
        ▼
Any compatible model
```

### What the shim translates

- Anthropic message content blocks → OpenAI `messages` array
- Anthropic `tool_use` / `tool_result` blocks → OpenAI `function_calls` / `tool` messages
- OpenAI SSE streaming chunks → Anthropic stream events
- Anthropic system prompt arrays → OpenAI `system` role messages

### Files changed from upstream

```
src/services/api/openaiShim.ts   ← NEW: the shim (724 lines)
src/services/api/client.ts       ← routes to shim when CLAUDE_CODE_USE_OPENAI=1
src/utils/model/providers.ts     ← added 'openai' provider type
src/utils/model/configs.ts       ← added openai model mappings
src/utils/model/model.ts         ← respects OPENAI_MODEL for defaults
src/utils/auth.ts                ← recognizes OpenAI as valid 3rd-party provider
```

---

## Developer Workflow — Key Commands

```bash
# Run in dev mode (no build)
bun run dev

# Build distribution
bun run build

# Launch with persisted profile (.openclaude-profile.json)
bun run dev:profile

# Launch with OpenAI profile (requires OPENAI_API_KEY in shell)
bun run dev:openai

# Launch with Ollama profile (localhost:11434, llama3.1:8b default)
bun run dev:ollama

# Launch with Codex profile
bun run dev:codex

# Quick startup sanity check
bun run smoke

# Validate provider env + reachability
bun run doctor:runtime

# Machine-readable runtime diagnostics
bun run doctor:runtime:json

# Persist diagnostics report to reports/doctor-runtime.json
bun run doctor:report

# Full local hardening check (typecheck + smoke + runtime doctor)
bun run hardening:check

# Strict hardening (includes project-wide typecheck)
bun run hardening:strict
```

---

## Profile Bootstrap — One-Time Setup

Profiles save provider config to `.openclaude-profile.json` so you don't repeat env exports.

```bash
# Auto-detect provider (ollama if running, otherwise openai)
bun run profile:init

# Bootstrap for OpenAI
bun run profile:init -- --provider openai --api-key $OPENAI_API_KEY

# Bootstrap for Ollama with custom model
bun run profile:init -- --provider ollama --model llama3.1:8b

# Bootstrap for Codex
bun run profile:init -- --provider codex --model codexspark
bun run profile:codex
```

After bootstrapping, run the app via the persisted profile:

```bash
bun run dev:profile
```

---

## TypeScript Integration — Using the Shim Directly

If you want to use the shim in your own TypeScript code:

```typescript
// src/services/api/client.ts pattern — routing to the shim
import { openaiShim } from './openaiShim.js';

const useOpenAI = process.env.CLAUDE_CODE_USE_OPENAI === '1';

const client = useOpenAI
  ? openaiShim({
      apiKey: process.env.OPENAI_API_KEY,
      baseURL: process.env.OPENAI_BASE_URL ?? 'https://api.openai.com/v1',
      model: process.env.OPENAI_MODEL ?? 'gpt-4o',
    })
  : new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
```

```typescript
// Streaming usage pattern (mirrors Anthropic SDK interface)
const stream = await client.messages.stream({
  model: process.env.OPENAI_MODEL!,
  max_tokens: 32000,
  system: 'You are a helpful coding assistant.',
  messages: [
    { role: 'user', content: 'Refactor this function for readability.' }
  ],
  tools: myTools, // Anthropic-format tool definitions — shim translates them
});

for await (const event of stream) {
  // events arrive in Anthropic format regardless of underlying provider
  if (event.type === 'content_block_delta') {
    process.stdout.write(event.delta.text ?? '');
  }
}
```

---

## Model Quality Reference

| Model | Tool Calling | Code Quality | Speed |
|---|---|---|---|
| GPT-4o | Excellent | Excellent | Fast |
| DeepSeek-V3 | Great | Great | Fast |
| Gemini 2.0 Flash | Great | Good | Very Fast |
| Llama 3.3 70B | Good | Good | Medium |
| Mistral Large | Good | Good | Fast |
| GPT-4o-mini | Good | Good | Very Fast |
| Qwen 2.5 72B | Good | Good | Medium |
| Models < 7B | Limited | Limited | Very Fast |

For agentic multi-step tool use, prefer models with strong native function/tool calling (GPT-4o, DeepSeek-V3, Gemini 2.0 Flash).

---

## What Works vs. What Doesn't

### Fully supported
- All tools: Bash, FileRead, FileWrite, FileEdit, Glob, Grep, WebFetch, WebSearch, Agent, MCP, LSP, NotebookEdit, Tasks
- Streaming (real-time token output)
- Multi-step tool chains
- Vision/images (base64 and URL) for models that support them
- Slash commands: `/commit`, `/review`, `/compact`, `/diff`, `/doctor`
- Sub-agents (AgentTool spawns sub-agents using the same provider)
- Persistent memory

### Not supported (Anthropic-specific features)
- Extended thinking / reasoning mode
- Prompt caching (Anthropic cache headers skipped)
- Anthropic beta feature headers
- Token output defaults to 32K max (gracefully capped if model is lower)

---

## Troubleshooting

### `doctor:runtime` fails with placeholder key error

```
Error: OPENAI_API_KEY looks like a placeholder (SUA_CHAVE)
```

Set a real key: `export OPENAI_API_KEY=$YOUR_ACTUAL_KEY`

### Ollama connection refused

Ensure Ollama is running before launching:

```bash
ollama serve &
ollama pull llama3.3:70b
bun run dev:ollama
```

### Tool calls not working / model ignores tools

Switch to a model with strong tool calling support (GPT-4o, DeepSeek-V3). Models under 7B parameters often fail at multi-step agentic tool use.

### Azure endpoint format

The `OPENAI_BASE_URL` for Azure must include the deployment path:

```
https://<resource>.openai.azure.com/openai/deployments/<deployment>/v1
```

### Codex auth not found

If `~/.codex/auth.json` doesn't exist, set the token directly:

```bash
export CODEX_API_KEY=$YOUR_CODEX_TOKEN
```

Or point to a custom auth file:

```bash
export CODEX_AUTH_JSON_PATH=/path/to/auth.json
```

### Run diagnostics for any issue

```bash
bun run doctor:runtime       # human-readable
bun run doctor:runtime:json  # machine-readable JSON
bun run doctor:report        # saves to reports/doctor-runtime.json
```
