---
name: bitrix24-rest-api
description: 'Call Bitrix24 REST from outside or from an app, cloud and on-premise. Use for webhook vs OAuth auth, token refresh, batch, list pagination, limits, QUERY_LIMIT_EXCEEDED, event.bind, placements, BX24.js, REST 3.0, crm.item.list calls.'
---

# Bitrix24 REST API (client side)

Baseline: Bitrix24 cloud; on-premise main 23.0+ · Verified: rest 26.650.0 (main 26.800.0), b24restdocs 2026-09-30

Consuming REST. Registering your own methods in a module: `bitrix-rest`. Docs lookup for agents (MCP), Vibecode: `bitrix24-ai-tools`.

| Task | Read |
| --- | --- |
| Webhook vs local app vs Marketplace OAuth, token refresh, scopes | `rules/auth.md` |
| URL and body format, lists, fast pagination, batch | `rules/calls.md` |
| Limits, error codes, retry and backoff | `rules/limits-errors.md` |
| Events, outbound webhooks, offline events, placements | `rules/events-placements.md` |
| REST 3.0 (`/rest/api/`), Idempotency-Key, OpenAPI | `rules/rest-v3.md` |
| b24phpsdk, b24jssdk, BX24.js, CRest | `rules/sdk.md` |
| On-premise specifics | `rules/on-premise.md` |

## Invariants

- Never guess a method, field or filter: look it up (MCP from `bitrix24-ai-tools`, or `method.get` on the target portal).
- Webhook URLs, `client_secret`, tokens and `application_token` live in env or a secret store; never in VCS, browser code, logs or shared URLs.
- Least privilege: request only the scopes the scenario calls. A call also runs with the rights of its user.
- Detect errors by the `error` key (and `result.result_error` in batch), not by HTTP status.
- Treat every inbound call (event, placement, install) as untrusted until `auth.application_token` matches the value stored for its `member_id`.
- HTTPS only. Handlers acknowledge fast, queue the work and process it idempotently.
