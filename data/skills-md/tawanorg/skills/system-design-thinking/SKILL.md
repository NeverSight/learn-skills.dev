---
name: system-design-thinking
description: >
  Frameworks for architectural decision-making and system design. Use when
  designing new systems, evaluating architecture options, breaking down complex
  problems, making build-vs-buy decisions, or when asked about "system design",
  "architecture", "how should I structure this", or "what's the best approach".
license: MIT
metadata:
  author: tawanorg
  version: '1.0.0'
---

# System Design Thinking

Frameworks for thinking about architecture before writing code. Design decisions are expensive to change—think first, code second.

## Core Philosophy

> "The goal of software architecture is to minimize the human resources required to build and maintain the required system." — Robert C. Martin

Architecture is about:
1. **Managing complexity** - Breaking big problems into smaller ones
2. **Enabling change** - Making the system adaptable
3. **Deferring decisions** - Keeping options open as long as possible
4. **Communicating intent** - Making the system understandable

## The Design Thinking Process

### 1. Understand Before Designing

> See `rules/start-with-requirements.md`

**Never design without understanding:**

| Understand | Questions to Ask |
|------------|------------------|
| **Users** | Who uses this? What do they need? How many? |
| **Data** | What data? How much? How fast does it grow? |
| **Operations** | Who runs it? How is it deployed? Monitored? |
| **Constraints** | Budget? Timeline? Team skills? Existing systems? |
| **Quality attributes** | Latency? Availability? Consistency? Security? |

### 2. Identify the Core Problem

Before jumping to solutions, articulate:

```
We need to [capability]
For [users/systems]
So that [business value]
Constrained by [limitations]
```

**Example:**
```
We need to process payment transactions
For 10,000 concurrent users
So that customers can complete purchases
Constrained by:
- 99.99% availability requirement
- PCI compliance
- <200ms response time
- Existing PostgreSQL infrastructure
```

### 3. Explore the Solution Space

Don't commit to the first idea. Generate options:

| Option | Pros | Cons | Risk |
|--------|------|------|------|
| Option A | ... | ... | ... |
| Option B | ... | ... | ... |
| Option C | ... | ... | ... |

### 4. Make and Document Decisions

> See `references/adr-template.md`

Every significant decision needs:
- **Context** - Why are we making this decision?
- **Options** - What did we consider?
- **Decision** - What did we choose?
- **Consequences** - What are the trade-offs?

---

## Trade-off Analysis

> See `references/trade-off-analysis.md` for detailed frameworks.

### The Iron Triangle

You can optimize for two, not all three:

```
        Speed
         /\
        /  \
       /    \
      /______\
   Scope    Quality
```

### CAP Theorem

Distributed systems can guarantee only two of three:

| Property | Meaning |
|----------|---------|
| **Consistency** | All nodes see the same data |
| **Availability** | Every request gets a response |
| **Partition tolerance** | System works despite network splits |

**In practice:** Network partitions happen, so choose CP or AP:
- **CP** (Consistency + Partition tolerance): Banking, inventory
- **AP** (Availability + Partition tolerance): Social feeds, caching

### Common Trade-offs

| Trade-off | When to favor A | When to favor B |
|-----------|-----------------|-----------------|
| **Consistency vs Availability** | Financial data, inventory | Social features, analytics |
| **Latency vs Throughput** | User-facing APIs | Batch processing |
| **Simplicity vs Flexibility** | MVP, small team | Platform, multiple use cases |
| **Build vs Buy** | Core differentiator | Commodity functionality |
| **Monolith vs Microservices** | Small team, new product | Large team, proven domain |

---

## Architecture Patterns Quick Reference

> See `references/architecture-styles.md` for detailed comparisons.

### When to Use What

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| **Monolith** | New products, small teams, unclear domains | Team > 10, independent scaling needed |
| **Modular Monolith** | Growing product, preparing for split | Already distributed |
| **Microservices** | Large teams, independent deployments | Small team, unclear boundaries |
| **Serverless** | Sporadic traffic, event-driven | Consistent high load, complex state |
| **Event-Driven** | Loose coupling, async workflows | Simple CRUD, strong consistency |

### Start Simple

> See `rules/prefer-simple-architecture.md`

```
Start here ──► Monolith ──► Modular Monolith ──► Microservices
                  │
                  └── Most projects never need to leave
```

**The Monolith First rule:** Unless you have proven scale requirements, start with a well-structured monolith.

---

## System Decomposition

### Finding Boundaries

> See `rules/define-boundaries-first.md`

Good boundaries have:
- **High cohesion** - Related things together
- **Low coupling** - Minimal dependencies across boundaries
- **Clear contracts** - Well-defined interfaces
- **Independent deployability** - Can change without coordinating

### Decomposition Strategies

| Strategy | How It Works | Best For |
|----------|--------------|----------|
| **By domain** | Business capabilities (Orders, Users, Payments) | Business-aligned teams |
| **By layer** | Presentation, Business, Data | Small teams, simple domains |
| **By feature** | End-to-end slices (Checkout, Search) | Feature teams |
| **By volatility** | Separate stable from changing parts | Mixed stability requirements |

### Domain-Driven Design (Quick Reference)

| Concept | Meaning | Example |
|---------|---------|---------|
| **Bounded Context** | Clear boundary with its own model | "Orders" vs "Inventory" |
| **Ubiquitous Language** | Shared vocabulary within context | "Order" means same thing to all |
| **Aggregate** | Cluster of entities, one root | Order with OrderItems |
| **Domain Event** | Something that happened | OrderPlaced, PaymentReceived |

---

## Data Architecture

> See `references/data-architecture.md`

### Data Flow First

Before designing components, understand:

1. **What data exists?** - Entities, relationships, volumes
2. **How does it flow?** - Sources, transformations, destinations
3. **Who owns it?** - Single source of truth for each entity
4. **How fresh must it be?** - Real-time, near-real-time, batch

### Storage Decisions

| Need | Consider |
|------|----------|
| Structured data, ACID | PostgreSQL, MySQL |
| Document/flexible schema | MongoDB, DynamoDB |
| Key-value, caching | Redis, Memcached |
| Time series | InfluxDB, TimescaleDB |
| Search | Elasticsearch, Algolia |
| Analytics/OLAP | BigQuery, Snowflake, ClickHouse |
| File/blob storage | S3, GCS, Azure Blob |

### Data Consistency Patterns

| Pattern | Consistency | Use When |
|---------|-------------|----------|
| **Single database** | Strong | Simple apps, single service |
| **Database per service** | Eventual | Microservices, independent scaling |
| **Saga pattern** | Eventual | Distributed transactions |
| **CQRS** | Eventual | Read/write scaling differs |
| **Event sourcing** | Eventual | Audit trail, temporal queries |

---

## Integration Patterns

> See `references/integration-patterns.md`

### Sync vs Async

| Synchronous | Asynchronous |
|-------------|--------------|
| Request/Response | Events/Messages |
| Simple, immediate | Resilient, decoupled |
| Tight coupling | Loose coupling |
| Cascading failures | Isolated failures |
| REST, gRPC | Queues, Pub/Sub |

### When to Use What

```
Need immediate response? ──► Sync (REST/gRPC)
                │
                No
                │
                ▼
Can caller continue without result? ──► Async (Queue/Event)
                │
                No
                │
                ▼
Use async with callback/webhook
```

---

## Scalability Thinking

> See `references/scalability-patterns.md`

### Scaling Strategies

| Strategy | How | When |
|----------|-----|------|
| **Vertical** | Bigger machine | Quick fix, stateful services |
| **Horizontal** | More machines | Stateless services, proven bottleneck |
| **Caching** | Store computed results | Read-heavy, expensive computations |
| **Partitioning** | Split data by key | Large datasets, geographic distribution |
| **Async processing** | Queue work for later | Spiky traffic, heavy operations |

### Performance Budget

Before optimizing, set targets:

```
Page load: < 2s
API response: < 200ms (p99)
Background job: < 30s
Availability: 99.9% (8.76 hours downtime/year)
```

---

## Design for Operations

> See `rules/consider-operations.md`

### Operability Checklist

Every system needs:

- [ ] **Health checks** - Is it running? Is it healthy?
- [ ] **Logging** - What happened? (Structured, searchable)
- [ ] **Metrics** - How is it performing? (Latency, errors, throughput)
- [ ] **Alerting** - When does it need attention?
- [ ] **Deployment** - How do we release changes safely?
- [ ] **Rollback** - How do we undo bad releases?
- [ ] **Disaster recovery** - What if everything fails?

### The "3 AM Test"

Ask: "If this breaks at 3 AM, can someone fix it?"

- Are errors clear and actionable?
- Are runbooks documented?
- Can issues be diagnosed from logs/metrics?
- Can it be rolled back quickly?

---

## Quick Reference Checklist

### Before Designing

- [ ] Requirements understood (functional + non-functional)
- [ ] Constraints identified (budget, timeline, skills, compliance)
- [ ] Success criteria defined (measurable)
- [ ] Stakeholders aligned

### During Design

- [ ] Multiple options explored
- [ ] Trade-offs explicitly stated
- [ ] Simplest solution that works chosen
- [ ] Boundaries clearly defined
- [ ] Data flow mapped
- [ ] Failure modes considered

### After Design

- [ ] Decision documented (ADR)
- [ ] Operability addressed
- [ ] Migration path identified (if replacing existing)
- [ ] Team understands and agrees

---

## Rules

Atomic decision heuristics. Each rule follows: Context → Heuristic → Why.

| Rule | File |
|------|------|
| Start with Requirements | `rules/start-with-requirements.md` |
| Prefer Simple Architecture | `rules/prefer-simple-architecture.md` |
| Define Boundaries First | `rules/define-boundaries-first.md` |
| Design for Failure | `rules/design-for-failure.md` |
| Document Decisions | `rules/document-decisions.md` |
| Consider Operations | `rules/consider-operations.md` |
| Data Flow First | `rules/data-flow-first.md` |
| Async Over Sync | `rules/async-over-sync.md` |

## Reference Files

Deep dives on specific topics.

| Topic | File |
|-------|------|
| Trade-off Analysis | `references/trade-off-analysis.md` |
| Architecture Styles | `references/architecture-styles.md` |
| Scalability Patterns | `references/scalability-patterns.md` |
| Integration Patterns | `references/integration-patterns.md` |
| Data Architecture | `references/data-architecture.md` |
| ADR Template | `references/adr-template.md` |
