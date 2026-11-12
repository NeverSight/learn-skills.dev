---
name: clean-architecture-microservices
description: Clean Architecture and microservices design-pattern guidance for structuring maintainable services, defining bounded contexts, designing APIs and events, choosing service boundaries, and building resilient distributed systems. Use for architecture reviews, new service design, microservice decomposition, migration planning, or workflow diagrams.
---

# Clean Architecture & Microservices Design Patterns

Use this skill to design software boundaries deliberately at two levels: **inside a service**, keep business policy independent from infrastructure; **between services**, keep business capabilities cohesive, data ownership explicit, and communication contracts stable. Do not treat either Clean Architecture or microservices as mandatory. Select the smallest structure that satisfies changeability, team ownership, scale, reliability, and delivery constraints.

## Load the right reference

- Read `references/pattern_catalog.md` for pattern definitions, selection guidance, benefits, and failure modes.
- Read `references/design_workflows.md` for the end-to-end architecture workflow and pattern combinations.
- Read the `.mmd` and `.png` files in `references/` when a workflow image or editable diagram source is needed.
- Read `references/visual_validation.md` only when checking the generated diagram assets or updating them.

## Apply the design workflow

1. **Clarify the problem.** Separate functional behavior from quality attributes such as latency, availability, deployability, security, operability, cost, and team autonomy. Record scope and exclusions.
2. **Analyze the domain.** Identify business capabilities, actors, events, policies, subdomains, vocabulary, and the boundaries where a model or rule changes meaning.
3. **Choose service boundaries.** Prefer high cohesion and loose coupling. Align services with business capabilities and ownership; do not split by technical layers such as “database service” or “messaging service.”
4. **Define data ownership.** Give each service an authoritative data store or clearly named ownership boundary. Share contracts and events rather than tables. State transaction, consistency, retention, and migration rules.
5. **Structure each service.** Keep domain entities and rules independent of frameworks; put use cases and application policies in the application layer; define ports for external capabilities; implement adapters for HTTP, persistence, messaging, and providers.
6. **Design contracts.** Define REST/RPC APIs or events, schemas, versioning, compatibility, authentication, authorization, idempotency, pagination, timeouts, and error semantics. Prefer consumer needs over internal object shapes.
7. **Choose interaction patterns.** Use synchronous calls for immediate decisions within the latency budget. Use events or queues for decoupling, burst absorption, replay, and eventual projections. Use orchestration or choreography deliberately for long-running workflows.
8. **Design failure behavior.** Add bounded timeouts, retry budgets with jitter, circuit breakers, bulkheads, idempotency, dead-letter handling, health signals, and graceful degradation. Specify what happens when a dependency, broker, region, or data store fails.
9. **Make operations observable.** Define logs, metrics, traces, correlation/context propagation, SLOs, alerts, audit events, deployment health checks, and ownership escalation paths.
10. **Validate before expanding.** Test architecture boundaries, contract compatibility, duplicate and out-of-order delivery, failure injection, rollback, migration recovery, load, tail latency, and restore procedures.

## Use these non-negotiable rules

- Keep dependencies pointing toward higher-level policy and domain rules; infrastructure and frameworks depend inward through ports or adapters.
- Keep a service cohesive around a business capability and its bounded context; avoid distributed monoliths that require synchronized releases or shared databases.
- Prefer one service owning a piece of data. If a cross-service transaction is unavoidable, state the consistency model and use a Saga, transactional outbox, or compensating action rather than pretending a local transaction spans the network.
- Treat events as public contracts. Define schema evolution, ordering, deduplication, replay, retention, and poison-message behavior.
- Use a strangler migration or anti-corruption layer when replacing a legacy system; do not leak legacy models into the new domain.
- Make resilience and observability part of the initial design, not a post-incident add-on.
- Do not introduce microservices when a modular monolith can meet the requirements with less operational complexity.

## Produce architecture answers in this structure

1. **Context and assumptions.** State the business goal, actors, constraints, workload, and unknowns.
2. **Domain model and boundaries.** Show capabilities, bounded contexts, service ownership, and important aggregates or policies.
3. **Service structure.** Explain the Clean Architecture layers, ports, adapters, dependency direction, and test seams.
4. **Contracts and data.** Define APIs/events, versioning, ownership, transactions, consistency, idempotency, and migration rules.
5. **Interaction and workflow.** Draw synchronous and asynchronous paths, including retries, timeouts, circuit breakers, and compensations.
6. **Operations and delivery.** Cover deployment independence, configuration, secrets, observability, SLOs, rollback, and ownership.
7. **Trade-offs and alternatives.** Explain why the chosen pattern is appropriate, what it costs, and when to simplify or split further.
8. **Validation plan.** List contract, integration, load, failure-injection, migration, and disaster-recovery tests.

## Diagram requirements

Use the bundled Mermaid sources for exact architecture relationships and render their PNG counterparts when an image is requested. Keep diagrams readable: show business boundaries, dependency direction, data ownership, communication mode, and resilience controls. Do not use decorative AI-generated diagrams for formal node-edge relationships. The included images are:

- `clean_architecture_dependency_flow.png`: inward dependency flow from adapters and infrastructure toward application and domain policy.
- `service_decomposition_workflow.png`: domain analysis through bounded contexts, aggregates, service boundaries, contracts, and iterative evolution.
- `resilient_microservice_flow.png`: gateway, Clean Architecture services, owned databases, synchronous dependency protection, events, consumers, and observability.
