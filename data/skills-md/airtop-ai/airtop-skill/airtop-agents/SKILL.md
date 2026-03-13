---
name: airtop-agents
description: List, run, and monitor Airtop agents. Use when asked to run an Airtop agent, check agent status, list agents, or invoke a webhook agent.
license: MIT
compatibility: Requires curl, jq, and a shell environment. Requires an Airtop API key from https://portal.airtop.ai/api-keys.
allowed-tools: Bash Read Write
metadata:
  author: airtop-ai
  version: "1.0"
---

# Airtop Agents Skill

You can list, run, monitor, and cancel Airtop agents using their REST API.

## Authentication

The Airtop API key is required for all operations. Resolve it in this order:

1. `$AIRTOP_API_KEY` environment variable
2. A `.env` file in this skill's directory containing `AIRTOP_API_KEY=...`
3. If neither is found, **offer the user two options** before proceeding:

> **Option A — Set it up yourself (recommended if you prefer not to share your key in chat):**
>
> Run these commands in your terminal:
> ```
> cp "$(dirname "$SKILL_PATH")/.env.example" "$(dirname "$SKILL_PATH")/.env"
> ```
> Then open the `.env` file and replace `your-api-key-here` with your key from https://portal.airtop.ai/api-keys.
>
> Once done, say "done" and I'll pick it up automatically.
>
> **Option B — Paste it here and I'll save it for you:**
>
> Paste your API key (from https://portal.airtop.ai/api-keys) and I'll write it to the `.env` file so it's available for future use.

Print both options exactly as above (with the actual resolved path instead of the `$(dirname ...)` expression) and wait for the user to choose. Do not assume a preference.

### Handling a pasted key (Option B)

**Important — always load the key from the `.env` file, never use a pasted value directly.**

When a user provides their API key interactively (e.g. pasting it into chat), text copied from web UIs or chat messages can contain invisible Unicode characters (zero-width spaces, byte-order marks, etc.) that silently break authentication. To avoid this:

1. **Write the key to `.env` first** — this round-trips it through file I/O which strips invisible characters:
   ```bash
   echo "AIRTOP_API_KEY=<pasted-value>" > "$(dirname "$SKILL_PATH")/.env"
   ```
2. **Then read it back** from the file to get a clean value:
   ```bash
   API_KEY=$(grep AIRTOP_API_KEY "$(dirname "$SKILL_PATH")/.env" | cut -d= -f2-)
   ```

Even when `$AIRTOP_API_KEY` is already set in the environment, prefer loading from `.env` if the file exists — the environment variable may have been set in the same shell session from a pasted value and could carry the same invisible characters.

Never assign a user-pasted key directly to a shell variable and use it in API calls (e.g. `API_KEY="<pasted-value>"` followed by `curl -H "Authorization: Bearer $API_KEY"`). Always go through the `.env` file write-then-read cycle to sanitize the value.

### Loading and validating the key

Once the `.env` file exists (whether set up by the user or written by you), load and validate:

```bash
API_KEY=$(grep AIRTOP_API_KEY "$(dirname "$SKILL_PATH")/.env" | cut -d= -f2-)
```

**Validate the key immediately** after loading it:
```bash
curl -sf -H "Authorization: Bearer ${API_KEY}" "https://api.airtop.ai/api/v2/agents?limit=1" > /dev/null
```
If this returns a non-zero exit code, tell the user their API key appears invalid and link them to https://portal.airtop.ai/api-keys.

## Base URL

All authenticated API endpoints use: `https://api.airtop.ai/api`

Webhook endpoints (run agent, poll result) use the public path: `https://api.airtop.ai/api/hooks/`

## Argument Parsing

Parse `$ARGUMENTS` as follows:

```
list [--name <filter>]              List agents
run <agent-name-or-id> [--vars {}]  Run an agent with optional config variables
status <agentId> <invocationId>     Check invocation status
cancel <agentId> <invocationId>     Cancel a running invocation
history <agentId>                   View recent invocations
```

If `$ARGUMENTS` is empty or unrecognized, show the usage summary above and ask the user what they'd like to do.

## Commands

### 1. List Agents

```bash
curl -s -H "Authorization: Bearer $API_KEY" \
  "https://api.airtop.ai/api/v2/agents?limit=25&sortBy=lastRun&sortOrder=desc&createdByMe=true"
```

Always include `createdByMe=true` to show only agents owned by the current user (not the entire organization).

Optional query parameters to append:
- `&name=<filter>` — case-insensitive partial match (use when `--name` is provided)
- `&enabled=true` — filter to enabled agents only
- `&published=true` — filter to published agents only

**Display**: Format the response as a markdown table with columns: Name, ID, Enabled, Last Run. Show the `pagination.total` count in a header line.

Example output:
```
Found 3 agents:
| Name              | ID                                   | Enabled | Last Run    |
|-------------------|--------------------------------------|---------|-------------|
| Price Tracker     | 550e8400-e29b-41d4-a716-446655440000 | Yes     | 2 hours ago |
| Lead Enricher     | 6ba7b810-9dad-11d1-80b4-00c04fd430c8 | Yes     | Yesterday   |
| Competitor Monitor| 6ba7b811-9dad-11d1-80b4-00c04fd430c8 | No      | Never       |
```

### 2. Run Agent

This is a multi-step process:

**Step 1 — Resolve agent by name or ID.**

If the argument looks like a UUID, use it directly as the agent ID. Otherwise, search by name:

```bash
curl -s -H "Authorization: Bearer $API_KEY" \
  "https://api.airtop.ai/api/v2/agents?name=$(printf '%s' '<agent-name>' | jq -sRr @uri)&createdByMe=true"
```

- If exactly one agent matches, use it (but still validate it in Step 2).
- If multiple agents match, prefer enabled and published agents over disabled or draft-only ones. If there is still ambiguity, display them in a table (with Enabled and Published status columns) and ask the user to pick one.
- If no agents match, tell the user no agent was found and suggest running `list`.

**Step 2 — Validate the agent is runnable.**

Fetch the full agent details (already available from step 1 if resolved by name, or fetch now):

```bash
curl -s -H "Authorization: Bearer $API_KEY" \
  "https://api.airtop.ai/api/v2/agents/<agentId>"
```

Check the following before proceeding:

- **Disabled agent** (`enabled` is `false`): Tell the user the agent is disabled and cannot be run. Suggest they enable it in the Airtop portal.
- **Draft-only agent** (`hasDraft` is `true` AND `publishedVersion` is absent): Tell the user the agent has only a draft version and has never been published. It must be published in the Airtop portal before it can be invoked via webhook.
- **Published agent with draft** (`hasDraft` is `true` AND `publishedVersion` is present): The agent is runnable. Note to the user that the agent has unpublished draft changes, and the published version will be used. Use the `publishedVersion` value for the version parameter.
- **Published agent** (`publishedVersion` is present, `hasDraft` is `false`): The agent is runnable. Use the `publishedVersion` value for the version parameter.

**Step 3 — Check required configVars.**

The agent details response includes a `versionData.configVarsSchema` field. Inspect it for `required` properties. If the user has not provided values for required configVars via `--vars`, prompt them for the missing values before invoking.

Display the required and optional parameters with their descriptions and defaults so the user knows what to provide.

**Step 4 — Get the agent's webhook.**

```bash
curl -s -H "Authorization: Bearer $API_KEY" \
  "https://api.airtop.ai/api/v2/agents/<agentId>/webhooks?limit=10"
```

Use the first webhook from the `webhooks` array. If no webhooks exist, tell the user the agent needs a webhook configured in the Airtop portal (https://portal.airtop.ai).

**Step 5 — Invoke the webhook.**

```bash
curl -s -X POST "https://api.airtop.ai/api/hooks/agents/<agentId>/webhooks/<webhookId>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "configVars": { <user-provided key-value pairs from --vars, or empty object {}> },
    "version": <publishedVersion from agent details>
  }'
```

Always use the `publishedVersion` value from the agent details as the `version` parameter — never hardcode it.

The response contains `{ "invocationId": "<uuid>" }`. Save this for polling.

**Step 6 — Poll for the result.**

```bash
curl -s "https://api.airtop.ai/api/hooks/agents/<agentId>/invocations/<invocationId>/result" \
  -H "Authorization: Bearer $API_KEY"
```

Polling rules:
- Poll every **5 seconds**
- Print a status update to the user after each poll (e.g., "Status: Running...")
- Terminal statuses: `Completed`, `Failed`, `Cancelled`
- **Timeout after 5 minutes** (60 polls). If not complete, tell the user the invocation is still running and provide the invocation ID so they can check later with the `status` command.

**Step 7 — Display the result.**

- On `Completed`: Show the `output` field. If it's JSON, format it nicely. If it's a string, display it directly.
- On `Failed`: Show the `error` field and the full status.
- On `Cancelled`: Inform the user the invocation was cancelled.

### 3. Check Status

Poll a specific invocation's result:

```bash
curl -s "https://api.airtop.ai/api/hooks/agents/<agentId>/invocations/<invocationId>/result" \
  -H "Authorization: Bearer $API_KEY"
```

Display the `status` field. If terminal, also display `output` or `error`.

Note: This requires both the agent ID and invocation ID. If the user only provides one, ask for the other.

### 4. Cancel Invocation

```bash
curl -s -X DELETE -H "Authorization: Bearer $API_KEY" \
  "https://api.airtop.ai/api/v2/agents/<agentId>/invocations/<invocationId>?reason=user_requested"
```

Confirm to the user that the cancellation was requested.

### 5. View History

```bash
curl -s -H "Authorization: Bearer $API_KEY" \
  "https://api.airtop.ai/api/v2/agents/<agentId>/invocations?limit=10"
```

Display results as a table with columns: Invocation ID, Status, Trigger, Started At.

## Error Handling

- **401 Unauthorized**: Tell the user their API key is invalid or expired. Direct them to https://portal.airtop.ai/api-keys.
- **404 Not Found**: The agent or invocation doesn't exist. Suggest checking the ID or running `list`.
- **429 Rate Limited**: Tell the user they've hit the rate limit and should wait before retrying.
- **No webhook configured**: Explain that the agent needs a webhook set up in the Airtop portal before it can be invoked from the CLI.
- **Multiple name matches**: List all matches and ask the user to pick one or use the agent ID directly.
- **Empty API key**: Guide the user to set `AIRTOP_API_KEY` or provide it interactively.

## Important Notes

- Always use `curl -s` (silent mode) to avoid progress bars in output.
- Parse all JSON responses with `jq` or inline JSON parsing in bash.
- The webhook invoke and poll endpoints are under `/api/hooks/` (public path), NOT `/api/v2/`.
- The list, webhooks, history, and cancel endpoints are under `/api/v2/` (authenticated path).
- When displaying times, convert ISO timestamps to human-readable relative times (e.g., "2 hours ago").
