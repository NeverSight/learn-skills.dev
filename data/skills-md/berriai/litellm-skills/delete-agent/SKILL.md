---
name: delete-agent
description: >
  Delete an AI agent from a live LiteLLM proxy. Ask for the agent_id and
  confirm before calling DELETE /v1/agents/{agent_id}.
license: MIT
compatibility: Requires curl.
metadata:
  author: BerriAI
  version: "1.0"
allowed-tools: Bash(curl:*)
---

# Delete Agent

Remove an AI agent from a live LiteLLM proxy.

## Setup

```
LITELLM_BASE_URL  — e.g. https://my-proxy.example.com
LITELLM_API_KEY   — proxy admin key
```

## Ask the user

1. **agent_id** — if they don't have it, list first:
   ```bash
   curl -s "$BASE/v1/agents" -H "Authorization: Bearer $KEY"
   ```
2. **Confirm** — show the agent name and ask for confirmation.

## Run

```bash
curl -s -X DELETE "$BASE/v1/agents/<agent_id>" \
  -H "Authorization: Bearer $KEY"
```

## Output

Confirm deletion. Note that any keys or integrations pointing to this agent will stop working.
