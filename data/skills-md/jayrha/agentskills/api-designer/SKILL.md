---
name: api-designer
description: Designs clean, consistent REST and GraphQL APIs covering resource modeling, URL structure, versioning, pagination, filtering, error formats (RFC 9457 Problem Details), idempotency, authentication, rate limiting, and machine-readable contracts (OpenAPI 3.1 / GraphQL SDL). Use this skill when designing a new API or endpoint, reviewing an API design, choosing REST vs GraphQL, deciding on versioning or pagination strategy, defining error responses, adding idempotency keys, writing or critiquing an OpenAPI/GraphQL schema, or establishing API style guidelines and naming conventions.
license: MIT
---

# API Designer

## Overview
This skill helps you design HTTP/REST and GraphQL APIs that are predictable, evolvable, and pleasant to consume. It covers resource modeling, URI design, HTTP semantics, versioning, pagination, filtering/sorting, error contracts, idempotency, concurrency control, auth, rate limiting, and writing machine-readable contracts.

Keywords: REST, GraphQL, OpenAPI, Swagger, API design, endpoint, resource, versioning, pagination, cursor, idempotency, ETag, RFC 9457, Problem Details, rate limit, contract, HATEOAS, webhook.

Apply this skill whenever the user is creating, extending, or reviewing an API surface — not when they are merely calling an existing third-party API.

## Decision: REST vs GraphQL vs RPC
Pick the style before designing details.

- **REST** — default for resource-oriented CRUD, public APIs, heavy caching needs, file uploads/downloads, and broad client tooling. Plays well with HTTP caching, CDNs, and standard status codes.
- **GraphQL** — choose when clients need flexible, nested data selection, when you have many client types with divergent data needs, or to avoid over/under-fetching. Costs: caching, rate limiting, and observability are harder; needs query-depth/complexity limits.
- **gRPC / JSON-RPC** — choose for internal service-to-service, low-latency, streaming, or strongly-typed contracts where browser reach is not required.

When unsure, default to REST and expose a small GraphQL layer later if client flexibility becomes a real pain point. See `references/rest-checklist.md` and `references/graphql-checklist.md`.

## Workflow
Follow these steps in order. Do not jump to URLs or schemas before modeling resources.

1. **Identify the domain nouns (resources).** List the core entities and their relationships. Resources are nouns, not verbs. Group them into collections and members.
2. **Define the resource representation.** For each resource, decide its fields, types, which are read-only/required/nullable, and identifiers (prefer opaque string IDs over leaking DB primary keys).
3. **Map operations to HTTP methods (REST) or queries/mutations (GraphQL).** Use the safe/idempotent matrix in `references/http-semantics.md`. Avoid verbs in REST paths; model actions as sub-resources or status transitions.
4. **Design the URL structure / schema.** Lowercase, kebab-or-snake consistent, plural collections, nested only one level deep. See naming rules below.
5. **Choose pagination, filtering, and sorting.** Default to cursor pagination for large/changing datasets. Standardize query parameters.
6. **Define the error contract.** Adopt RFC 9457 Problem Details. One consistent shape across all endpoints. See `references/error-design.md`.
7. **Add reliability semantics.** Idempotency keys for unsafe-but-retryable POSTs, ETag/If-Match for optimistic concurrency, conditional requests for caching.
8. **Specify cross-cutting concerns.** AuthN/AuthZ, rate limiting + headers, versioning strategy, deprecation policy, CORS.
9. **Write the contract.** Produce OpenAPI 3.1 (REST) or SDL (GraphQL) as the source of truth. Use `templates/openapi-3.1-template.yaml` or `templates/graphql-schema-template.graphql`.
10. **Validate.** Run `scripts/lint_openapi.py` on the OpenAPI file to catch common design smells before review.

## Naming & URL Rules (REST)
- Collections are plural nouns: `/invoices`, `/users/{userId}/orders`.
- A member is the collection plus an ID: `/invoices/{invoiceId}`.
- No verbs in paths. Bad: `/getInvoice`, `/createUser`. Good: `GET /invoices/{id}`, `POST /users`.
- Actions that don't fit CRUD become sub-resources or controllers: `POST /orders/{id}/cancel`, `POST /messages/{id}/send`. Prefer modeling state: `PATCH /orders/{id}` with `{ "status": "cancelled" }` when it's a true state field.
- Nest at most one level. Beyond that, link by ID and offer query filters: prefer `/comments?postId=42` over `/users/1/posts/2/comments/3`.
- Use hyphens in multi-word path segments (`/billing-accounts`), and be consistent with field casing (`camelCase` or `snake_case`) — pick one and never mix.
- Query params for filtering/sorting/pagination; path params for identity.

## Pagination Cheat Sheet
- **Cursor (keyset) pagination — preferred.** Stable under inserts/deletes, scales. Response includes `{ "data": [...], "page": { "nextCursor": "...", "hasMore": true } }`. Request: `?limit=50&cursor=abc`.
- **Offset/limit — only for small, mostly-static datasets or admin tables needing "jump to page N".** `?limit=50&offset=100`. Beware drift and deep-offset cost.
- Always: a sane default limit, an enforced max limit, and a consistent envelope. Document the default sort order — cursors are meaningless without a deterministic sort.

## Quick Reference: Status Codes
- `200` OK (GET, PATCH/PUT returning body) · `201` Created (POST; include `Location`) · `202` Accepted (async) · `204` No Content (DELETE, empty PUT).
- `400` malformed · `401` unauthenticated · `403` authenticated-but-forbidden · `404` not found · `409` conflict (e.g., version mismatch, duplicate) · `410` gone (sunset resource) · `412` precondition failed (If-Match) · `422` semantically invalid body · `429` rate limited (add `Retry-After`).
- `500` unexpected · `503` unavailable (add `Retry-After`). Never return `200` with an error body. Full matrix in `references/http-semantics.md`.

## Idempotency & Concurrency (essentials)
- `GET`, `PUT`, `DELETE` are idempotent by HTTP definition; `POST` is not. For retry-safe creation/payment POSTs, accept an `Idempotency-Key` header and return the original result on replay. See `references/idempotency.md`.
- Use `ETag` + `If-Match` for optimistic concurrency on updates → `412` on mismatch. Use `If-None-Match` for cache validation → `304`.

## Versioning (essentials)
- Prefer URL major versioning for public APIs: `/v1/...`. Simple, visible, cache-friendly.
- Additive changes (new optional fields, new endpoints) are non-breaking and need no version bump. Removing/renaming fields, changing types, or tightening validation are breaking.
- Publish a deprecation policy: `Deprecation` and `Sunset` response headers + changelog. Details in `references/versioning.md`.

## Best Practices
- Design the contract first; generate or hand-write OpenAPI/SDL as the single source of truth.
- One consistent error shape everywhere (RFC 9457). Include a stable machine-readable `type`/`code`.
- Make responses self-consistent: same field for the same concept across all endpoints (`createdAt`, not sometimes `created`).
- Return created/updated representations so clients avoid an extra round-trip.
- Use UTC ISO-8601 timestamps with offset (`2026-06-08T10:00:00Z`), and explicit currency + minor units for money.
- Paginate every list endpoint from day one — never return unbounded arrays.
- Validate input strictly and reject unknown fields in writes; be liberal only in clearly versioned ways.
- Document rate limits and return `X-RateLimit-*` / `RateLimit` headers.

## Common Pitfalls
- Verbs in URLs and RPC-over-REST (`/api/doAction`).
- Returning `200 OK` for errors, or inconsistent error bodies per endpoint.
- Leaking internal IDs, SQL errors, or stack traces in responses.
- Unbounded list endpoints; offset pagination on huge tables.
- Breaking changes shipped without a version bump or deprecation window.
- Overusing nesting (`/a/{}/b/{}/c/{}`) instead of filters and links.
- Non-idempotent retries causing duplicate charges/records.
- GraphQL without depth/complexity limits (DoS) or with N+1 resolvers (no dataloader batching).

## Supporting Files
- `references/rest-checklist.md` — full REST design review checklist.
- `references/graphql-checklist.md` — GraphQL schema and operational checklist.
- `references/http-semantics.md` — methods, status codes, headers, caching, conditional requests.
- `references/error-design.md` — RFC 9457 Problem Details patterns and examples.
- `references/idempotency.md` — idempotency keys, concurrency, exactly-once patterns.
- `references/versioning.md` — versioning strategies, breaking-change rules, deprecation.
- `templates/openapi-3.1-template.yaml` — starter OpenAPI 3.1 spec with errors + pagination.
- `templates/graphql-schema-template.graphql` — starter GraphQL SDL with Relay pagination.
- `examples/orders-api.md` — worked REST example for an Orders domain.
- `scripts/lint_openapi.py` — stdlib linter for common OpenAPI design smells.
