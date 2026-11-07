---
name: fable-architecture
description: "Evaluate project specifications at inception (Step One), deterministically assess Scale & Load, Domain Decoupling, and Resource Intensity vectors, and automatically enforce a distributed Microservices Architecture when warranted, preventing monolith scaffolding."
user-invocable: true
allowed-tools: "Read Write Edit Bash Glob Grep"
metadata:
  version: "1.0.0"
  pack: "system"
  phase: "planned"
---

# Fable Architecture: Microservices Enforcement Engine

Evaluate project specifications at inception (**Step One**) to deterministically decide whether scale, throughput, concurrency, domain complexity, or workload heterogeneity warrant a distributed Microservices Architecture. When triggered, hard-constrain all primary coding agents and downstream subagents to strictly operate within a decoupled, microservices-driven execution paradigm, assign curated language-framework pairs by core competency, and enforce standard inter-service communication protocols.

---

## Mission

Intercept project specifications before any directory scaffolding or implementation begins to deterministically evaluate whether Scale & Load, Domain Decoupling, or Resource Intensity warrant a distributed architecture. When thresholds are tripped, hard-lock the agent workforce from scaffolding a monolith (`allowMonolith: false`), enforce decoupled microservices with curated polyglot language-framework stacks, and mandate dual-transport networking: North-South REST HTTP/JSON (OpenAPI 3.1) vs. East-West gRPC (Protocol Buffers) or Message Broker (RabbitMQ / Kafka).

---

## Activate When

- Project specification describes high concurrency ($\ge 5,000$ concurrent users/connections, $>10,000$ RPS/TPS).
- Specification defines $\ge 2$ decoupled operational domains (Identity/Auth, Billing/Stripe, Transcoding, AI Inference, Analytics, Messaging).
- Workload contains mixed CPU-bound kernels (heavy math, transcoding, cryptography) and I/O-bound pipelines (API Gateway, CRUD).
- User explicitly requests microservice evaluation, distributed architecture design, or polyglot stack assignment.
- Step One prompt evaluation hook detects architectural trigger thresholds.

---

## Do Not Activate When

- Project is a simple command-line script, utility, or single-file tool (`fable-execute`).
- Project is an isolated single-domain CRUD prototype or static blog where scale remains within monolithic boundaries.
- Task is only a localized bug fix or single-module refactoring (`fable-tdd` or `fable-simplify`).
- Broad work is already decomposed and only requires standard step-by-step planning (`fable-plan`).

---

## Situation Classification

| Category | Core Competency | Language | Framework Options | Primary Workload | Subagent Role |
|---|---|---|---|---|---|
| **Category A** | High-Concurrency APIs & Distributed Networking | **Go (Golang)** | `Fiber`, `Gin`, `Go-Kit` | Stateless routing, millions of messages/sec, edge proxying | `distributed-network-engineer` |
| **Category B** | I/O Intensive, Rapid API Gateway & Orchestration | **TypeScript** | `NestJS`, `Fastify` (Node.js) or `Elysia` (Bun) | Public API Gateway, BFF, CRUD, rapid business logic | `gateway-orchestrator` / `crud-engineer` |
| **Category C** | High-Performance Computational Kernels & Systems | **Rust** | `Axum`, `Actix-web` | Heavy math, cryptography, video transcoding, raw binary | `systems-kernel-engineer` |
| **Category D** | Artificial Intelligence, Data Engineering & ML | **Python** | `FastAPI` (with PyTorch/TensorFlow) | LLM routing, predictive modeling, embeddings, ML pipelines | `ai-inference-engineer` |
| **Category E** | Ultra-High Concurrency, Fault-Tolerant Real-Time Systems | **Elixir** | `Phoenix` (with LiveView) | Hundreds of thousands of persistent WebSockets, real-time messaging orchestration, zero-downtime | `realtime-systems-engineer` |

---

## Protocol

### Stage 1: Inception 3-Vector Evaluation
Evaluate incoming specification across 3 discrete vectors:
1. **Vector 1: Scale & Load** (0–10 score): Detect high concurrency ($\ge 5k$), throughput targets, latency SLAs.
2. **Vector 2: Domain Decoupling** (0–10 score): Detect operational domain boundaries (auth, billing, gateway, compute, ai, messaging, realtime).
3. **Vector 3: Resource Intensity** (0–10 score): Detect mixed CPU-bound vs. I/O-bound bottlenecks.
4. Calculate composite score: $(0.35 \times \text{Scale}) + (0.40 \times \text{Domain}) + (0.25 \times \text{Resource})$.

### Stage 2: Verdict & Monolith Lockout
- If any single vector $\ge 7.0$ OR composite score $\ge 6.0$:
  - Set `verdict: 'microservices'` and `allowMonolith: false`.
  - Scaffolding a monolithic application is strictly locked out.
- Otherwise:
  - Set `verdict: 'monolith'` and `allowMonolith: true`.

### Stage 3: Polyglot Stack Assignment & Decomposition
- Ensure API Gateway is instantiated as Service #1 using Category B (TypeScript/NestJS).
- For each identified operational domain, assign dedicated service stack from Categories A–E.
- Guarantee at least 2 distinct domain worker services alongside the Gateway.

### Stage 4: Communication Standards Contract
- **North-South**: REST HTTP/JSON with OpenAPI 3.1 schemas and TLS 1.3.
- **East-West**: gRPC with Protocol Buffers (`proto/`) or Message Broker (Kafka/RabbitMQ). Prohibit internal HTTP/JSON.

### Stage 5: Output Architecture Manifest
- Generate structured TOON manifest `microservices_manifest.toon` and companion `docker-compose.yml`.

---

## Decision Rules

- When `allowMonolith: false`, any attempt to generate a single-directory application or shared database is an immediate invariant violation.
- Every internal East-West RPC service interface must be defined via a strict `.proto` IDL before implementing client or server code.
- Heavy CPU computation must never run on the Node.js event loop; always route to Category C (Rust) or Category D (Python).
- High throughput stateless message streams must be routed to Category A (Go) distributed networking services.
- If a sub-service requires managing hundreds of thousands of persistent WebSocket connections, real-time messaging orchestration, or zero-downtime fault tolerance, auto-select Category E: Elixir (Phoenix/LiveView).
- External clients must never directly call internal East-West gRPC services; all client traffic enters via API Gateway.

---

## Invariants

- Monolith scaffolding is locked out whenever any vector $\ge 7.0$ or composite $\ge 6.0$.
- Internal service-to-service communication strictly prohibits un-typed HTTP/JSON when microservices are enforced.
- Every microservice owns its private data persistence layer; shared relational tables across service boundaries are forbidden.
- Architecture manifests are serialized in valid TOON format before product scaffolding begins.

---

## Failure Taxonomy

### Inappropriate Monolith Scaffolding
Agent attempts to build a single repo with monolithic controllers despite tripped scale/domain thresholds. Resolution: Hard intercept, reject directory structure, trigger `fable-architecture` re-decomposition.

### East-West Transport Downgrade
Internal services communicating over plain HTTP/JSON REST instead of gRPC. Resolution: Generate `.proto` IDL contract in `proto/` and wire gRPC transport bindings.

### CPU Event Loop Starvation
Placing video transcoding or heavy cryptography in Node.js/TypeScript. Resolution: Extract CPU-intensive logic into a dedicated Rust Category C microservice.

### Domain Boundary Bleed
Multiple business domains accessing the same database schema directly. Resolution: Enforce service boundary with private datastore and gRPC interface.

---

## Anti-Patterns

- Generating a monolith to "keep it simple" when concurrency is $\ge 50,000$ RPS.
- Sharing a single PostgreSQL database across all services with cross-domain foreign keys.
- Using untyped HTTP/JSON for internal backend-to-backend communication.
- Embedding deep learning model inference in a Go or TypeScript CRUD service.
- Skipping API Gateway and exposing internal gRPC ports directly to public clients.

---

## Completion Criteria

- 3-vector evaluation is completed and recorded with discrete scores and composite score.
- Architecture manifest (`microservices_manifest.toon`) is emitted with explicit services table.
- Monolith lockout state (`allowMonolith: false`) is established if thresholds are tripped.
- Communication contract strictly enforces North-South REST vs. East-West gRPC/Brokers.
- Specialized subagent roles and polyglot stacks are assigned for each decomposed service.

---

## Progressive Resources

- Vector scoring guide: `references/vector-scoring.md`
- Tech stack matrix: `references/tech-stack-matrix.md`
- Communication standards: `references/communication-standards.md`
- Subagent role distribution: `references/subagent-role-distribution.md`
- Example walkthroughs: `examples/fintech-scale-walkthrough.md`, `examples/ai-media-pipeline-walkthrough.md`
- Templates: `templates/microservices-manifest.toon`, `templates/docker-compose.microservices.yml`, `templates/service-contract.proto`
- Validation script: `scripts/evaluate-architecture.py`
