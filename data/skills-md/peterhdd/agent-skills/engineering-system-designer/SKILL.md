---
name: engineering-system-designer
description: "Design distributed systems, define architecture for scalability and reliability, or create system design documents. Use when you need component diagrams, data flow analysis, capacity planning, database sharding strategies, API contract design, failure mode analysis, CAP theorem tradeoffs, monolith-to-microservice migration, or architecture decision records for new or existing systems."
metadata:
  version: "1.0.0"
---

# System Design Guide

## Overview
This guide covers the process of turning product requirements into deployable, observable, and resilient distributed system architectures. Use it for greenfield architecture, scaling existing systems, design reviews, architecture decision records, or monolith-to-services migrations.

## Design Process

### 1. Requirements
Clarify functional needs, non-functional targets (latency, throughput, durability), read/write ratio, peak traffic patterns, and geographic distribution. If the stakeholder cannot provide traffic numbers, estimate from user count: assume 10% DAU/MAU ratio, 5 requests per session, 80% of traffic in 8 hours (peak = 3x average).

### 2. Capacity estimation
Calculate QPS, storage growth, and bandwidth. Project at 1x, 5x, and 10x load. Identify the bottleneck resource. Use `scripts/capacity_calculator.py` for calculations. Always show your math — never state capacity without derivation.

### 3. High-level architecture
Map components, data stores, queues, caches, and external dependencies. Define sync vs async boundaries. Start with the fewest components possible — if 3 boxes solve it, do not draw 7.

### 4. Component deep-dive
Specify technology choices with justification. Define partitioning, replication, consistency model, and cache invalidation per store. Every technology choice must answer: "Why this over the simpler alternative?"

### 5. Data model and API design
Design schemas for primary access patterns. Define API contracts with error codes and rate limits. Plan migration strategy. Every table must have its top 3 query patterns listed with expected latency.

### 6. Failure modes
List every component failure and its blast radius. Define circuit breakers, retries, timeouts, and fallbacks. For each failure mode, state: what breaks, who is affected, how it is detected, and what the automatic recovery is.

### 7. Monitoring
Specify metrics, alerts, and dashboards required before launch. Every SLO must have a corresponding alert. Every alert must have a runbook link.

## Decision Frameworks

### SQL vs NoSQL
- Use SQL (PostgreSQL default) when you need transactions across multiple entities, complex joins for reporting, or strong schema enforcement.
- Use NoSQL when your access patterns are key-value lookups, your schema changes frequently, or you need horizontal write scaling beyond a single node.
- **Specific cutoffs:** <10TB and relational access patterns = PostgreSQL. Key-value with <10ms latency at >100k QPS = Redis or DynamoDB. Document store with flexible schema and <50TB = MongoDB. Wide-column with >1PB or time-series at >1M writes/sec = Cassandra or ScyllaDB. Full-text search = Elasticsearch/OpenSearch alongside primary store (never as source of truth).

### Database Scaling Thresholds
- **Single PostgreSQL:** Handles up to ~10k QPS reads, ~5k QPS writes on modern hardware. If read-heavy (>80% reads), add read replicas first.
- **Read replicas:** Add when read QPS exceeds single-node capacity or read latency p95 >50ms. Expect 1-5s replication lag — design for eventual consistency on read replicas.
- **Connection pooling (PgBouncer):** Required when connections exceed 200. Never let applications open unbounded connections.
- **Sharding:** Required when single-node write QPS is insufficient or storage exceeds ~5TB on one node. Choose shard key by highest-cardinality, most-queried column. Hash-based sharding for uniform distribution; range-based for time-series or geographic data.
- **Caching with Redis:** Add when the same query runs >100 times/minute with identical results. Use cache-aside pattern. Set TTL explicitly — no caches without expiry. If cache hit rate <80%, the cache is not helping — remove it or fix the key design.

### Sync vs Async
- Use synchronous communication when the caller needs the result to proceed and latency under 200ms is achievable.
- Use asynchronous messaging when the operation can be completed later, you need to absorb traffic spikes, or downstream services have variable latency.
- **Queue selection:** SQS for simple job queues (<256KB messages, at-least-once delivery). RabbitMQ for routing/priority queues with <10k msg/sec. Kafka for event streaming with >10k msg/sec, replay capability, or multiple consumers on the same stream.

### Monolith vs Microservices
- Start with a monolith. Extract a service only when you have a clear scaling bottleneck, an independent deployment cadence requirement, or a team ownership boundary that causes merge conflicts.
- Never extract more than one service at a time. Validate operational readiness before the next extraction.
- **Team size rule:** <10 engineers = monolith. 10-50 engineers = modular monolith with clear domain boundaries. >50 engineers = microservices along team boundaries. Never let architecture outpace operational capability.

### Load Balancing and CDN
- <1k QPS: single instance with health checks is sufficient.
- 1k-50k QPS: Application Load Balancer with auto-scaling group (min 2 instances, scale on CPU >60% or request count).
- >50k QPS: Add CDN (CloudFront/Cloudflare) for static assets and cacheable API responses. If >80% of traffic is cacheable, CDN alone may handle the scale.
- Global users across >2 continents: multi-region deployment with Route 53 latency-based routing or Cloudflare global load balancing.

### Rate Limiting
- Apply at API gateway for all public endpoints. Default: 100 req/min per user, 1000 req/min per IP.
- For write-heavy endpoints (POST/PUT/DELETE): 10-30 req/min per user.
- For expensive operations (search, reports, exports): 5 req/min per user.
- Return `429 Too Many Requests` with `Retry-After` header. Log rate-limited requests for abuse detection.

## Design Principles
- **CAP theorem awareness**: Know which two of consistency, availability, and partition tolerance your system prioritizes, and document the tradeoff explicitly. If you cannot state the CAP tradeoff for each data store in your design, the design is incomplete.
- **Start simple**: Begin with the fewest components that satisfy requirements. Add complexity only when measurements demand it. A new component must justify itself with a specific bottleneck it resolves — "might need it later" is not justification.
- **Design for failure**: Every component will fail. Define what happens when it does before writing any code. If a component has no failure mode analysis, it is not ready for production.
- **Prefer boring technology**: Choose well-understood tools with strong operational track records over novel alternatives unless a clear, quantified advantage exists (>2x throughput, >50% cost reduction, or enabling a feature impossible with the boring option).
- **Make decisions reversible**: Favor designs where components can be swapped, scaled, or removed independently without system-wide rewrites. If replacing a component requires changing >3 services, add an abstraction layer.

## Estimation Quick Reference
- **Storage:** 1M users, 10 fields avg 100 bytes each = ~1GB raw data. Multiply by 3x for indexes + overhead.
- **Bandwidth:** 1 API call avg 5KB response at 10k QPS = 50MB/s = 400Mbps. Plan for 2x headroom.
- **QPS from DAU:** DAU * avg_requests_per_session / seconds_in_peak_hours. Peak = 3x average.
- **Replication:** 3 replicas minimum for durability. Cross-region replication adds 50-200ms latency.
- **Connection math:** Each PostgreSQL connection uses ~10MB RAM. 100 connections = 1GB just for connections. Use PgBouncer if >200 connections needed.

## Reference: System Design Document Template
Every system design document should contain:
- Problem statement and functional requirements.
- Non-functional requirements with specific numeric targets.
- Capacity estimation with calculations shown.
- High-level architecture diagram description (components, data flow, protocols).
- Data model with access patterns and indexing strategy.
- API contracts for all service boundaries.
- Failure mode analysis for every component.
- Monitoring plan with specific metrics and alert thresholds.
- Cost estimate for infrastructure at launch and at 10x scale.

## Self-Verification Protocol
After completing a system design, verify it against these checks before presenting:
- Every component has a failure mode analysis. If you cannot state what happens when a component dies, the design is incomplete.
- Every data store has its CAP tradeoff documented explicitly. "We chose AP over CP because..." is required.
- Capacity math is shown for 1x, 5x, and 10x. If any number was assumed without derivation, flag it as an assumption.
- Every technology choice answers: "Why this over the simpler alternative?" If the answer is "it's what I know," that is valid for a monolith but not for a distributed system.
- API contracts exist for every service boundary with request/response schemas, error codes, and rate limits.
- The monitoring plan has specific metric names, alert thresholds, and runbook references — not just "we will monitor it."
- Cross-reference: re-read the functional requirements and confirm every single one maps to at least one component. If a requirement is not served by any component, the design has a gap.
- Cost estimate is present. If the infrastructure cost exceeds $10k/month, justify each major line item.

## Failure Recovery
- **Design does not meet latency target**: Identify the longest path in the call chain. Add caching at the bottleneck first. If still insufficient, move to async processing or denormalize the data model. Never add more components to fix a latency problem — reduce the number of hops.
- **Write throughput exceeds single-node capacity**: Verify the bottleneck is real (run EXPLAIN ANALYZE on the hot query). If confirmed, shard by the highest-cardinality write key. If the write pattern is append-only (logs, events), use Kafka or a time-series DB instead of sharding a relational store.
- **Design review reveals missed requirement**: Do not bolt on a fix. Go back to step 1 (requirements), update capacity estimates, and re-evaluate the high-level architecture. A design that grows by accretion breaks under load.
- **Stakeholder asks for a feature that contradicts a design principle**: Document the tradeoff explicitly. "Adding real-time sync requires moving from CP to AP for this store. This means users may see stale data for up to 5 seconds." Let the stakeholder decide with real tradeoff data, not vague concerns.
- **Estimated cost is too high**: Cut from the edge inward. Remove CDN → reduce replica count → downsize instances → simplify to monolith. Never cut monitoring or backups to save cost.

## Existing System Assessment
When asked to redesign or scale an existing system:
1. **Measure before proposing** — Get current QPS, p50/p95/p99 latencies, error rates, and storage growth rate. Designs based on guesses fail.
2. **Identify the actual bottleneck** — Profile, do not guess. The bottleneck is rarely where people think it is. Check: slow queries (pg_stat_statements), connection saturation, CPU vs I/O bound, cache hit rates.
3. **Find the 80/20** — What single change would resolve 80% of the scaling problem? Start there. Common answers: add an index, add a cache, add a read replica, move a heavy job to async.
4. **Preserve what works** — If the current system handles 80% of traffic fine, do not rewrite it. Scale the 20% that is breaking.
5. **Migrate incrementally** — Strangler fig pattern: route new traffic to the new system, gradually migrate old traffic. Never do a big-bang cutover on a system serving >1k QPS.

## Scripts

- `scripts/capacity_calculator.py` -- Calculate QPS, storage, and bandwidth from traffic assumptions. Run with `--help` for options.

See [Code Examples](references/code-examples.md) for full implementation patterns including capacity estimation, API contracts, database schema with sharding, and circuit breaker.

See [Worked Examples](references/worked-examples.md) for complete system design walkthroughs of a URL shortener and a WhatsApp-like chat system, covering requirements through production architecture.

See [Failure Analysis](references/failure-analysis.md) for failure mode analysis templates, cache strategy comparisons, load shedding, bulkhead pattern, and chaos engineering checklists.

See [Scaling Patterns](references/scaling-patterns.md) for consistent hashing, database sharding, CQRS, rate limiting, back-pressure handling, and AWS cost estimation templates.
