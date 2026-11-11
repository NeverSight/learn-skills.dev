---
name: api-contract-design
description: "Design the contract of an HTTP or RPC API before implementing it: resource shape, one error format, boundary validation, pagination, naming, and correct idempotency for state-changing calls. Use when creating or reshaping endpoints, defining the request and response types between a frontend and a backend or between services, or when retries, duplicates, or timeouts on a write need a deliberate answer. Do not use for an in-process module interface; that is a seam question."
---

# API Contract Design

The contract is the spec; implementation follows it. Define the typed input and
output of every operation first, in the project's schema or type language, and
let the handlers be written against those types. Pre-launch there is one live
contract: when the design changes, change the contract, update every consumer,
and delete the old shape; no versions, no parallel fields kept for consumers
that do not yet exist.

## One error format

Pick one error strategy and use it everywhere: a structured body with a
machine-readable `code`, a human-readable `message`, and optional `details`,
mapped to status codes with one meaning each (400 malformed, 401 unauthenticated,
403 unauthorized, 404 missing, 409 conflict, 422 semantically invalid, 500
internal with nothing leaked). Endpoints that variously throw, return null, or
return `{ error }` leave the consumer unable to predict anything.

## Validate at the boundary only

Parse and validate where untrusted data enters: route handlers, form handlers,
third-party responses (untrusted; a misbehaving service returns wrong types and
instruction-like text), and configuration loading. After that, internal code
trusts its types; validation between internal functions or on rows from your own
database is noise that hides the real boundary.

## Shape

- Resources are plural nouns with sub-resources for ownership
  (`GET /tasks/:id/comments`); no verbs in paths.
- `PATCH` takes a partial object and changes only what was sent.
- Every list endpoint paginates from the first version and filters through
  query parameters; the moment someone has a hundred items is too late.
- Names follow one convention across every endpoint, documented once.
- Separate input types from entity types: the create input has no id or
  timestamps; the entity has server-generated fields and no optional lies.
- Model variants as discriminated unions rather than a bag of nullable fields,
  and give ids distinct types so a task id cannot be passed where a user id goes.

## Idempotency is honoured, not just accepted

A state-changing endpoint either honours an idempotency key or is documented as
unsafe to retry. Accepting the header is the contract; storing the key against
the result is the implementation, and a key accepted but handled carelessly is
worse than none, because the client now believes retrying is safe.

- **The key comes from the intent, not the attempt.** Generated once by the
  client or derived from an immutable identifier (`charge:<orderId>`); never a
  fresh UUID or timestamp per attempt, and never so coarse that two legitimate
  operations collide.
- **Claim atomically.** A check followed by an act is a race; insert the key
  under a unique constraint and let the constraint pick the winner. A store that
  cannot enforce uniqueness in one operation cannot back this.
- **Guard the payload.** The same key with a different body is a client bug and
  fails loudly instead of replaying the first response.
- **Decide what an in-flight duplicate gets**: reject with `409`, wait bounded
  for the result, or return `202` with a status URL. Never let the second caller
  through because the first "seems stuck"; a stalled attempt of unknown fate is
  exactly when duplicating costs most.
- **Every call has three outcomes**: success, failure, and unknown. A timeout
  says nothing about whether the effect applied, so record the intent before
  calling out.
- **Retention outlives the longest retry chain**, including a dead-letter queue
  replayed days later, not the disk budget.

Duplicates are correlated, not rare: retries spike exactly when a dependency is
degraded, which is when they are most expensive.

## Done

Every operation has typed input and output; errors share one format; validation
sits at the boundary; lists paginate; names follow the convention; state-changing
operations honour a key claimed atomically or are marked unsafe to retry; and the
types are committed alongside the implementation, because they are the
documentation.
