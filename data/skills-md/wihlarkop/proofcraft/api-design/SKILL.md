---
name: api-design
description: >-
  Design or evolve consumer-facing contracts for REST/HTTP, RPC, GraphQL, events, webhooks, or
  streams. Use for resource/operation semantics, schemas, errors, idempotency, pagination,
  concurrency preconditions, compatibility, versioning, and deprecation. Own the contract consumers
  rely on, not backend implementation or how this project integrates with somebody else's API.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# API Design

Make consumer-visible semantics explicit enough that providers and consumers do not have to guess.

## Workflow

1. Identify the consumer job, domain terms, authority, sensitivity, and failure modes.
2. Choose the interface shape that fits the interaction: request/response, query, command, event, webhook, or stream.
3. Define representation semantics: identifiers, absent vs null, defaults, enums, timestamps/units, ordering, filtering, and pagination.
4. For mutations, define validation, preconditions, idempotency scope, concurrency behavior, partial outcomes, long-running operations, and retry-safe errors.
5. For async contracts, define delivery/duplicate/order semantics and how consumers detect gaps or replay.
6. Evaluate compatibility from each consumer perspective and plan additive evolution/deprecation where possible.
7. Keep implementation framework and storage details out of the public contract unless they are intentionally part of it.

## Stop

Stop when a consumer can implement correctly without guessing success, failure, retry, compatibility, or data semantics.
## Reference Guide

Load only the references needed for the current task:

- [contract semantics](references/contract-semantics.md)
- [errors idempotency](references/errors-idempotency.md)
- [evolution events](references/evolution-events.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
