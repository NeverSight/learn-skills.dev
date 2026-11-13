---
name: interservice-protocol-selection-rest-grpc-graphql
description: Select and govern REST, gRPC, and GraphQL communication patterns by latency, coupling, and consumer needs. Use when defining or refactoring service communication strategy.
disable-model-invocation: true
---

# Interservice Protocol Selection REST gRPC GraphQL

## Use When

- Service APIs need protocol standardization
- Existing protocol mix causes complexity or performance problems

## Workflow

1. Classify interactions by sync/async, payload size, and fan-out.
2. Choose protocol per use case with explicit rationale.
3. Define schema contracts, error models, and compatibility rules.
4. Implement observability and resiliency controls per protocol.
5. Validate developer ergonomics and operational overhead.

## Required Checks

- Protocol choice aligns with latency and operability targets
- Schema governance includes backward compatibility policy
- Gateway translation overhead is understood and bounded

## Decision Framework

- Prefer REST for public, cache-friendly CRUD; gRPC for low-latency internal sync; GraphQL when consumers need shaped reads with strict query cost limits.
- Document error models, schema evolution rules, and breaking-change policy per protocol.
- Measure gateway translation overhead when mixing protocols at the edge.
- Avoid protocol proliferation without governance—standardize defaults per interaction class.

## Common Rationalizations And Rebuttals

- "GraphQL everywhere simplifies clients." -> Unbounded queries and N+1 resolver paths hurt reliability; use where fan-out shaping pays off.
- "gRPC is always faster." -> Operational complexity (schema, proxies, browser incompatibility) has cost; use internally unless justified externally.
- "REST versioning in URLs is enough." -> Explicit compatibility tests and deprecation timelines still required.

## Evidence Pack

- Protocol decision record per interaction type with latency and operability rationale
- Schema governance doc with backward-compatibility rules
- Load or latency comparison when gateway translates between protocols
- Observability config per protocol (trace propagation, error taxonomy)

## Exit Criteria

- Protocol usage is intentional, documented, and maintainable
- Service communication failures are easier to debug and control
