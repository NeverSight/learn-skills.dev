---
name: designing-apis
description: Designs and safely evolves APIs around real client needs and explicit compatibility. Use when choosing an API shape, adding or changing endpoints, errors, pagination, idempotency, async work, streaming, webhooks or versioning, or reviewing an API change. Not for HTTP basics or generic SDKs.
license: Apache-2.0
---

# Designing APIs

Design the smallest contract that satisfies the stated clients, data shape, latency,
and failure requirements. Prefer a boring, consistent API that fits the existing
project over a theoretically complete one; every extra abstraction becomes
compatibility surface.

## Workflow

- [ ] **Inspect before deciding.** Read repository guidance, neighboring
      handlers/routes, schemas, serializers, authentication, OpenAPI or equivalent
      contract files, client usage, and relevant tests. Record conventions that must
      remain stable.
- [ ] **Clarify the use case.** Identify callers, read/write operations, cardinality,
      latency and freshness, partial failure behavior, expected growth, authorization
      boundaries, and whether clients need one resource, an operation, or flexible
      projections. Ask only questions that change the design.
- [ ] **Write the decision brief.** Compare the smallest plausible resource-oriented
      shape with an operation/RPC shape; consider GraphQL only when client query
      variability or aggregation genuinely dominates. Choose one shape and state
      rejected alternatives and constraints.
- [ ] **Specify the contract.** Define identifiers, representations, required versus
      optional fields, nullability, state transitions, validation,
      authentication/authorization semantics, error envelope, pagination/filter/sort
      rules, idempotency, and observability-safe examples. Match local naming and
      media conventions.
- [ ] **Plan change safety.** Classify the change as additive, behavior-changing, or
      breaking. Define compatibility guarantees, rollout, migration, deprecation
      notice and removal criteria, and how old clients behave. Read
      `references/evolution.md` for nontrivial changes.
- [ ] **Choose async or realtime only when needed.** If work exceeds request
      expectations, survives disconnects, or needs fan-out, select polling, a status
      resource, SSE, or webhooks based on client and delivery needs. Read
      `references/realtime-and-async.md`.
- [ ] **Implement or hand off safely.** Update the contract, implementation,
      generated artifacts if the repository uses them, and focused tests together. Do
      not invent gateway, federation, HATEOAS, or microservice boundaries without a
      demonstrated requirement.
- [ ] **Validate.** Run the project's contract, unit/integration, lint, and
      compatibility checks. Test malformed input, authorization, retries, duplicate
      delivery, stale cursors, partial failures, and old-client behavior where
      relevant. Fix discrepancies and repeat.

## Shape decisions

| Need | Default | Choose an alternative when |
|---|---|---|
| CRUD around stable domain entities | Resource-oriented endpoints with consistent representations | The action is not naturally a resource transition |
| A domain command with a clear verb and invariant | An explicit operation/command endpoint | Modeling it as CRUD would hide intent or produce unsafe semantics |
| Many clients need different fields/joins | A query contract with bounded, documented selection | A few fixed views cover clients; then keep fixed representations |
| Long work or eventual completion | Create/submit an operation and expose status/result | Work is reliably short and atomic |
| Server-to-client incremental updates | SSE for one-way ordered updates | Clients send frequent messages back on the same connection (WebSockets), or the receiver is not connected (webhooks, or polling a status resource) |

Do not choose REST, RPC, or GraphQL by ideology. Evaluate the client's query shape,
mutation semantics, caching, authorization, generated-client needs, operational
complexity, and evolution cost. Read `references/resource-shapes.md` when the
boundary between resource and operation is unclear.

## Contract rules

- Use one error envelope across the API. Include a stable machine-readable code,
  human-safe message, request/correlation identifier, and field or retry metadata only
  when actionable. Never require clients to parse prose; do not leak stack traces or
  secrets.
- Make successful and error status semantics consistent with neighboring endpoints.
  Document validation versus authentication, authorization, conflict, rate,
  dependency, and transient failures separately when clients can react differently.
- For collections, define a stable ordering, page size limits, filtering grammar, and
  whether totals are exact, estimated, or omitted. Prefer opaque cursors for
  changing/high-volume data; use page numbers only when stable random access matters.
  Read `references/resource-shapes.md` for cursor and representation details.
- Make retries safe deliberately. Use idempotency keys for retryable non-idempotent
  commands, scope them to the authenticated actor and operation, retain the result
  long enough for the retry window, and define mismatch/expiry behavior. Do not
  promise idempotency merely because a method looks familiar.
- Treat webhook and stream delivery as at-least-once unless a stronger guarantee is
  actually implemented. Include event identifiers, ordering scope, timestamps,
  schema version, signature/authentication rules, retry/backoff, deduplication
  guidance, and replay or resync behavior.
- Avoid breaking changes to field meaning, type, requiredness, enum behavior,
  authorization, ordering, error codes, or pagination tokens. Add before removing;
  tolerate unknown response fields when clients can.

## Decision brief and implementation output

Use this compact format in the issue, plan, or response:

```markdown
# API decision: <capability>

## Context and clients
- Callers / operations:
- Constraints and existing conventions:

## Decision
- Shape and example request/response:
- Errors, auth, pagination/filtering:
- Retry, async, realtime, or delivery semantics:

## Alternatives
- <alternative>: rejected because <client/maintenance/evolution cost>

## Compatibility and rollout
- Existing clients:
- Deprecation/removal or migration:
- Tests and validation:
```

If implementing, report changed contract and code paths, compatibility impact, tests run, and any unresolved assumption. Keep the brief even when no code change is requested.

## Gotchas

- "Optional" is not harmless: adding a required request field or changing absent versus null can break old clients.
- A cursor is a contract, not an encoded offset. Keep it opaque, validate its scope and expiry, and define behavior when the underlying sort key disappears.
- A 202 response without a discoverable status/result contract is not an asynchronous API. Define ownership, states, cancellation, expiry, and failure retrieval.
- Webhooks and streams do not remove polling needs: provide resumption, replay, or a reconciliation path when missed events matter.
- Deprecation is not a header alone. Name affected clients, publish the replacement, measure use, set a sunset condition, and remove only after the stated compatibility window.

## References

- `references/evolution.md` — read for compatibility, versioning, deprecation, or migration decisions.
- `references/resource-shapes.md` — read for resource/operation/query choices and collection contracts.
- `references/realtime-and-async.md` — read for long-running work, SSE, webhooks, retries, and resumption.
- `assets/agents-snippet.md` — copy when a project wants durable API-design guidance in its agent instructions.
