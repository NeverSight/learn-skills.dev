---
name: bitrix24-agent
description: Design, implement, debug, and harden integrations between AI agents and Bitrix24 REST API (webhooks, OAuth 2.0, scopes, events, batch, limits, and REST 3.0). Use when asked to connect AI assistants/agents to Bitrix24, automate CRM/tasks/chats, process Bitrix24 events, choose an auth model, or resolve Bitrix24 API errors and performance issues.
---

# Bitrix24 Agent (Lean + Reliable)

Use this skill to deliver correct Bitrix24 integrations with low token usage and production-safe defaults.

## Quick Start

Use this flow unless the user asks for a different one:

1. Pick intent + one minimal pack (`core` by default).
2. Run a read probe first.
3. For writes, use plan then execute with confirmation.

Read probe:

```bash
python3 skills/bitrix24-agent/scripts/bitrix24_client.py user.current --params '{}'
```

Safer write flow:

```bash
python3 skills/bitrix24-agent/scripts/bitrix24_client.py crm.lead.add \
  --params '{"fields":{"TITLE":"Plan demo"}}' \
  --packs core \
  --plan-only

python3 skills/bitrix24-agent/scripts/bitrix24_client.py \
  --execute-plan <plan_id> \
  --confirm-write
```

## Runtime Prerequisites

Required environment:

- `B24_DOMAIN`
- `B24_AUTH_MODE` = `webhook` or `oauth`

Webhook mode:

- `B24_WEBHOOK_USER_ID`
- `B24_WEBHOOK_CODE`

OAuth mode:

- `B24_ACCESS_TOKEN`
- `B24_REFRESH_TOKEN`
- `B24_CLIENT_ID` and `B24_CLIENT_SECRET` (for `--auto-refresh`)

Useful safety/reliability flags:

- `B24_REQUIRE_PLAN=1` for mandatory plan->execute on write/destructive calls
- `B24_PACKS=core,...` for default pack set
- `B24_RATE_LIMITER=file` with `B24_RATE_LIMITER_RATE` and `B24_RATE_LIMITER_BURST`

## Default Mode: Lean

Apply these limits unless the user asks for deep detail:

- Load at most 2 reference files before first actionable step.
- Start from `references/packs.md`.
- Then open only one target file: `references/catalog-<pack>.md`.
- Open `references/chains-<pack>.md` only if the user needs workflow steps.
- Open `references/bitrix24.md` only for auth architecture, limits, event reliability, or unknown errors.

Response limits:

- Use concise output (goal + next action + one command).
- Do not retell documentation.
- Do not dump large JSON unless requested.
- Return only delta if guidance was already given.

## Routing Workflow

1. Determine intent:
- method call
- troubleshooting
- architecture decision
- event/reliability setup

2. Normalize product vocabulary:

- "collabs", "workgroups", "projects", "social network groups" -> `collab` (and `boards` for scrum).
- "Copilot", "CoPilot", "BitrixGPT", "AI prompts" -> `platform` (`ai.*`).
- "open lines", "contact center connectors", "line connectors" -> `comms` (`imopenlines.*`, `imconnector.*`).
- "feed", "live feed", "news feed" -> `collab` (`log.*`).
- "sites", "landing pages", "landing" -> `sites` (`landing.*`).
- "booking", "calendar", "work time", "time tracking" -> `services` (`booking.*`, `calendar.*`, `timeman.*`).
- "orders", "payments", "catalog", "products" -> `commerce` (`sale.*`, `catalog.*`).
- "consents", "consent", "e-signature", "sign" -> `compliance` (`userconsent.*`, `sign.*`).

3. Choose auth quickly:

- one portal/internal integration: webhook
- app or multi-portal lifecycle: OAuth

4. Select minimal packs:

- default `core`
- add only required packs: `comms`, `automation`, `collab`, `content`, `boards`, `commerce`, `services`, `platform`, `sites`, `compliance`, `diagnostics`

## Execution Flow (Safe by Default)

Command template:

```bash
python3 skills/bitrix24-agent/scripts/bitrix24_client.py <method> \
  --params '<json>' \
  --packs core
```

Guardrails to enforce:

- allowlist via packs and `--method-allowlist`
- write gate with `--confirm-write`
- destructive gate with `--confirm-destructive`
- optional two-phase write with `--plan-only` and `--execute-plan`
- idempotency for writes (auto or `--idempotency-key`)
- audit trail unless `--no-audit` is explicitly needed

## Reliability and Performance

Pagination and sync safety:

- Never stop after first `*.list` page.
- Keep deterministic ordering and persist checkpoints after successful page persistence.

Batch rules:

- Maximum 50 commands per `batch`.
- No nested `batch`.
- Split oversized batches and parse per-command errors.

Limits and retries:

- Treat `QUERY_LIMIT_EXCEEDED` and `5xx` as transient.
- Use exponential backoff with jitter (client default).
- Use shared rate limiter keyed by portal in multi-worker setups.

Events:

- Online events are not guaranteed delivery.
- For no-loss pipelines, use offline flow:
  - `event.offline.get(clear=0)`
  - process idempotently with retry budget
  - `event.offline.error` for failed items
  - `event.offline.clear` only for successful/DLQ'ed items
- Use `scripts/offline_sync_worker.py` as baseline.

## Error Handling

Fast mapping:

| Error code | Typical cause | Immediate action |
|---|---|---|
| `WRONG_AUTH_TYPE` | method called with wrong auth model | switch webhook/OAuth model for this method |
| `insufficient_scope` | missing scope | add scope and reinstall/reissue auth |
| `expired_token` | OAuth token expired | refresh token (`--auto-refresh` or external refresh flow) |
| `QUERY_LIMIT_EXCEEDED` | burst above portal budget | backoff, queue, tune limiter, reduce concurrency |
| `ERROR_BATCH_LENGTH_EXCEEDED` | batch payload too large | split batch |
| `ERROR_BATCH_METHOD_NOT_ALLOWED` | unsupported method in batch | call directly |

Escalate to deep reference (`references/bitrix24.md`) on:

- unknown auth/permission behavior
- recurring limit failures
- offline event loss concerns
- OAuth refresh race or tenant isolation issues

## Quality Guardrails

- Never expose webhook/OAuth secrets.
- Enforce least-privilege scopes and tenant isolation.
- Keep writes idempotent where possible.
- Validate `application_token` in event handlers.
- Prefer REST v3 where compatible; fallback to v2 where needed.

## Reference Loading Map

1. `references/packs.md` for pack and loading strategy.
2. `references/catalog-<pack>.md` for method shortlist.
3. `references/chains-<pack>.md` for implementation chains.
4. `references/bitrix24.md` for protocol-level troubleshooting and architecture decisions.

Useful search shortcuts:

```bash
rg -n "^# Catalog|^# Chains" references/catalog-*.md references/chains-*.md
rg -n "WRONG_AUTH_TYPE|insufficient_scope|QUERY_LIMIT_EXCEEDED|expired_token" references/bitrix24.md
rg -n "offline|event\\.bind|event\\.offline|application_token" references/bitrix24.md
```

## Scripts

- `scripts/bitrix24_client.py`: method calls, packs, allowlist, confirmations, plans, idempotency, audit, rate limiting, retries.
- `scripts/offline_sync_worker.py`: offline queue polling, bounded retries, DLQ handling, safe clear flow, graceful shutdown.
