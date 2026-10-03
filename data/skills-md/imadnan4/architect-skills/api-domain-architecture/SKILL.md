---
name: api-domain-architecture
description: How to design APIs around BUSINESS DOMAINS, not database tables. Use when designing REST/GraphQL/gRPC/WebSocket endpoints, commands vs resources, auth, validation, idempotency, pagination, versioning, error contracts, caching, rate limits.
when_to_use: |
  - designing REST / GraphQL / gRPC / WebSocket APIs
  - commands vs resources, authentication, authorization, validation
  - idempotency, pagination, versioning, error contracts, caching, rate limits
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# API & Domain Architecture

The API is a **business contract**, not a database wrapper. The database is private; the API is
public. Expose business capabilities, never database structure.

## Design order

```
Business Process → Domain Model → Capabilities → API Contract → Implementation   (never DB → API)
```

## Domain first

Identify Actors, Resources, Actions, Rules, Relationships, Lifecycle **before** any endpoint.

- Bad: `POST /users`, `PUT /users`, `GET /users` (CRUD on tables)
- Good: `POST /organizations/{id}/invite`, `POST /checkout`, `POST /payments/{id}/refund`

## Resources vs commands

- **Resources** (data retrieval): `GET /projects`, `POST /projects`, `DELETE /projects/{id}`
- **Commands** (state change): `POST /projects/{id}/archive` — not `PATCH status=archived`

Intent matters more than HTTP verb.

## Layered responsibilities

| Layer | Owns |
|---|---|
| API | Receive → AuthN → AuthZ → Validate → Call domain → Respond (nothing more) |
| Domain | Business rules, calculations, policies, validation, state changes, orchestration |
| Infrastructure | DB, queues, Redis, email, storage, search, LLMs, payments, 3rd-party (replaceable) |

**Business logic never lives in** controllers/routes/pages/components. Use the repository pattern:
`Domain → Repository Interface → Implementation` (domain never couples to PostgreSQL/Mongo/Redis).

## Request lifecycle

```
Client → Gateway → AuthN → AuthZ → Validation → Rate Limiter → Domain → Repository → DB → Response
```

## AuthN vs AuthZ

- **Authentication:** *Who are you?* Prefer managed (WorkOS, Clerk, Auth0, Supabase, Cognito).
- **Authorization:** *What may you do?* Belongs in backend domain logic — never trust frontend checks.

## Protocol choice

| Need | Protocol |
|---|---|
| CRUD, business APIs, web, public APIs, admin | **REST** (default) |
| Many clients, flexible queries, mobile, complex dashboards | GraphQL |
| Internal services, streaming, low latency, typed contracts | gRPC |
| True realtime (presence, live collab, trading) | WebSockets |
| External event delivery | Webhooks (retries, signatures, replay, idempotency) |

## Critical rules

- **Validation:** everything (headers, query, body, cookies, path, files). Never trust clients.
- **Idempotency:** money ops (payments, refunds, bookings, subscriptions) must be repeatable-safe.
- **Pagination:** cursor (default) / offset (admin only). Never return all rows.
- **Versioning:** breaking change → new version; never silently change contracts.
- **Response shape:** `success, data, meta, pagination, errors` — predictable.
- **Errors:** machine-readable `code` + message + correlation ID + retryability (e.g.
  `INSUFFICIENT_FUNDS`, `RATE_LIMITED`), never *"Something went wrong."*
- **Async:** long task → `202 Accepted` + job ID + status endpoint.
- **Rate limits / caching:** protect every public endpoint; cache with explicit TTL + invalidation + ownership.
- **BFF:** different clients (web/mobile/desktop) get different APIs — don't force one shape.

## API checklist

- [ ] AuthN · AuthZ · Validation · Logging · Metrics · Tracing · Rate limiting
- [ ] Pagination · Idempotency · Documentation · Tests · OpenAPI updated · Monitoring · Alerts

## Architecture decision tree

```
Designing an endpoint
  ↓
Business action? → Command (POST /checkout)
Data retrieval?  → Resource (GET /projects)
Flexible client queries? → GraphQL
Internal high-throughput/streaming? → gRPC
Realtime truly required? → WebSockets
Notify external systems? → Webhooks
Long-running task? → 202 + job id + status endpoint
```

## Anti-patterns

- ❌ CRUD that mirrors database tables
- ❌ Business logic in controllers / components
- ❌ Domain coupled directly to PostgreSQL
- ❌ No idempotency on money operations
- ❌ Returning "Something went wrong"
- ❌ No pagination (returning all rows) · silent contract changes

## Architecture prompts

- Does this endpoint expose a capability or a table?
- What is the user's intent?
- Is it idempotent / paginated / versioned?
- Where does the business rule live?
- What does the client actually need to know?
