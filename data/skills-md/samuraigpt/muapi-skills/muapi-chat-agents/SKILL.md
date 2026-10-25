---
name: muapi-chat-agents
description: Run Claude Code or Codex CLI on Muapi (api.muapi.ai) using Muapi credits instead of a separate vendor account. Use when the user wants a local coding agent to use Muapi as its model provider, asks which Muapi models work with Claude Code or Codex, or needs the base URL, API key variable, provider block or model name for either agent. Covers Claude Code (Anthropic Messages) and Codex CLI (OpenAI Responses), model discovery, verification and troubleshooting.
---

# Muapi chat agents

Muapi serves coding agents natively, so no translation proxy is needed:

| Agent | Protocol | Base URL | Models endpoint |
|---|---|---|---|
| Claude Code | Anthropic Messages | `https://api.muapi.ai/anthropic` | `GET /anthropic/v1/models` |
| Codex CLI | OpenAI Responses | `https://api.muapi.ai/openai/v1` | `GET /openai/v1/models` |

Usage bills against the user's Muapi credits at the same per-model prices as the Muapi API. Auth is
always the user's Muapi API key, read from `MUAPI_API_KEY` (never paste or commit it).

## Rules

- Do not put the full request URL in the base URL. Agents append `/v1/messages` or `/responses` themselves.
- Always read model ids from the models endpoint. Never rely on a remembered list.
- Put provider settings in user-level config, never in project files.
- Authenticate with `Authorization: Bearer <key>` (Claude Code's `ANTHROPIC_AUTH_TOKEN` does this) or `x-api-key`.
- A request is checked against the wallet before it runs, so the balance must cover a worst-case request
  (a large prompt plus the full output limit on a big model can hold a dollar or more; the unused part is returned).

## Setup

1. `export MUAPI_API_KEY=your_key` (PowerShell: `$env:MUAPI_API_KEY = "your_key"` and `setx MUAPI_API_KEY "your_key"`).
2. List models:
   ```bash
   curl -s -H "Authorization: Bearer $MUAPI_API_KEY" https://api.muapi.ai/anthropic/v1/models
   curl -s -H "Authorization: Bearer $MUAPI_API_KEY" https://api.muapi.ai/openai/v1/models
   ```
   (Windows PowerShell: use `curl.exe`.)

### Claude Code

Add to `~/.claude/settings.json` (or `.claude/settings.local.json`, never the committed project file):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.muapi.ai/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<your Muapi API key>",
    "ANTHROPIC_MODEL": "claude-sonnet-5-5"
  }
}
```

Or export `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN="$MUAPI_API_KEY"` in the shell before starting `claude`.
`settings.json` env values are literal, so prefer the shell exports to keep the key out of files.
Run `/status` inside Claude Code to confirm the base URL, and `claude --debug` to see requests.

### Uncensored (abliterated) models in Claude Code

`GET /anthropic/v1/models` also lists the tool-capable abliterated models. Use the same base URL and key, pick one with `claude --model <id>`, and set `ANTHROPIC_DEFAULT_HAIKU_MODEL` and `ANTHROPIC_SMALL_FAST_MODEL` to that same id (otherwise Claude Code's background requests 404). Warn the user: quality varies by model (smaller models can skip steps on multi-file tasks), there is no prompt caching so every turn re-bills the whole conversation, and output is capped at 16,384 tokens per response. Codex CLI can use them too through `/openai/v1` (set `model` to the id); this path is tested with real Codex CLI sessions (file write, shell and `apply_patch` tool calls on qwen, mimo and glm), but quality varies by model.

### Codex CLI

`~/.codex/config.toml`:

```toml
model = "gpt-5-6-sol"
model_provider = "muapi"

[model_providers.muapi]
name = "Muapi"
base_url = "https://api.muapi.ai/openai/v1"
env_key = "MUAPI_API_KEY"
wire_api = "responses"
```

`env_key` names the variable that holds the key; it is not the key. Set `model` explicitly to an id from
the models endpoint. Provider ids `openai`, `ollama` and `lmstudio` are reserved, so use `muapi`.
Run `codex doctor` to verify. Optional: `model_reasoning_effort = "high"`.

## Troubleshooting

| Problem | Fix |
|---|---|
| 401 | Header must be `Authorization: Bearer <key>` or `x-api-key`. Check the key at https://muapi.ai/dashboard |
| 402 / insufficient credit | Balance cannot cover the worst case for that request; top up, or lower the output limit |
| 404 model not found | Use an id from the models endpoint |
| `/v1/v1/messages` in errors | Remove the path suffix from the base URL |
| Claude Code asks to log in to Anthropic | Quit the terminal, export the variables, reopen it, start `claude` from that shell |
| Codex ignores the provider | Move settings to `~/.codex/config.toml` (user level) |
| 5xx / provider error | Retry; the proxy already retries a backup route once |
