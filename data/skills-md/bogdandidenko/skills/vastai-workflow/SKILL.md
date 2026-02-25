---
name: vastai-workflow
description: Run a generic Vast.ai API lifecycle from offer search to teardown with safety checks and reproducible request steps. Use when users need to list/filter offers, create instances, attach SSH keys, poll readiness, stop/destroy instances, or inspect billing/usage, and when required runtime fields (image, instance type, API key source) should be collected in dialog with default suggestions.
---

# Vast.ai Workflow

## Overview

Use this skill for provider-level Vast.ai automation only.
Keep it project-agnostic and parameter-driven.

## Scope Boundaries

- Handle only Vast API workflow logic: offers, create, poll, SSH attach, lifecycle, billing.
- Do not embed project-specific repo paths, branch names, labels, or training commands.
- If the user asks for workload-specific execution (for example Reparo training), switch to the corresponding workload skill after infrastructure provisioning.

## Dialog-First Required Fields

Before any create/order call, confirm required runtime fields in dialog.
If the user does not provide them, propose defaults and ask for confirmation.

Required fields and default suggestions:

- `api_key_source`: default `VAST_API_KEY` environment variable.
  - If missing, suggest loading from a local file path the user confirms (for example `keys/.vast_env`).
- `instance_type` (offer filter): default `gpu_name="RTX 4090"`.
  - Ask whether to lock by exact GPU, VRAM minimum, region, max price, and reliability.
- `image`: default `pytorch/pytorch:latest`.
- `disk_gb`: default `64`.
- `count`: default `1`.
- `label`: do not ask by default.
  - Derive from Vast account identity when possible (nickname or email local-part).
  - Fallback label: `vast-user`.

Suggested minimal question set:
1. Which action now (`offers`, `create`, `status`, `ssh`, `destroy`, `billing`)?
2. Confirm runtime fields (`image`, `disk_gb`, instance filter).
3. Confirm API key source (`VAST_API_KEY` env vs file path).

If the user approves defaults, proceed without extra questions.

## Workflow

### 1) Preflight

- Check active instances first.
- If any instances are unintentionally active, ask whether to stop/destroy before creating a new one.
- Ensure API key is loaded and never echo it.

### 2) Find offers

- Query offers (`/bundles` is commonly reliable in practice).
- Apply user filters plus mandatory `rentable=true` and `rented=false`.
- Sort by user objective (price, performance, reliability).
- Use user policy for selection:
  - Default: choose cheapest valid offer.
  - Optional conservative mode: choose second cheapest.

### 3) Create instance

- Create from a single selected offer (`PUT /asks/{id}`).
- Use confirmed `image`, resolved `label`, and `disk_gb`.
- Parse and store the returned instance ID.
- If create fails (`no_such_ask` or already taken), re-query and retry once with next candidate.

Label resolution order:
1. Load profile/account endpoint data and use nickname when present.
2. If nickname missing, use the email local-part when available.
3. If neither field is available, use `vast-user`.

### 4) Readiness and access

- Poll instance status until running.
- Add SSH key to account and attach to instance.
- Retry SSH readiness for up to 2 minutes before declaring failure.

### 5) Lifecycle and billing

- Support start/stop/restart when available.
- Use destroy promptly when requested to prevent costs.
- Verify final state and check usage/invoices when needed.

## Request Templates

Use explicit, reproducible requests and validate JSON before chaining calls.

```bash
curl -sS -L -G "https://console.vast.ai/api/v0/<endpoint>/" \
  --data-urlencode "api_key=$VAST_API_KEY" \
  --data-urlencode "<param>=<value>"
```

```bash
curl -sS -L -X PUT "https://console.vast.ai/api/v0/asks/$OFFER_ID/?api_key=$VAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"image\":\"$IMAGE\",\"disk\":$DISK_GB,\"label\":\"$LABEL\"}"
```

## Error Handling

- `401/403`: API key missing, invalid, or not authorized for requested org/action.
- `429`: rate limit; retry with backoff.
- `4xx`: invalid endpoint or params; re-check request shape and required fields.
- `5xx`: provider-side issue; retry with backoff and re-validate state.
- Empty/parse failures: retry once, then save response to a temp file and parse from file.

## Resources

- `references/api.md`: concise endpoint map and safe calling checklist.
- Treat `references/api.md` as the working source for endpoint details and refresh it against official docs regularly.
