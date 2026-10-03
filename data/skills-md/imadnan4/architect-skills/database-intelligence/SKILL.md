---
name: database-intelligence
description: How to select and model databases from DATA, not hype. Use when choosing PostgreSQL, MySQL, MongoDB, DynamoDB, Redis, ClickHouse, Elasticsearch, or vector DBs; data modeling, normalization, indexing, migrations, multi-tenancy, backups.
when_to_use: |
  - choosing a database (Postgres, MySQL, MongoDB, DynamoDB, Redis, ClickHouse, vector DB)
  - data modeling, normalization, indexing
  - migrations, multi-tenancy, backups
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Database Intelligence

The application **owns** the data; the database only **stores** it. Design the data model first —
the database is an implementation detail and must never dictate application architecture.

## Selection pipeline

```
Business Problem → Entities → Relationships → Access Patterns → Consistency
               → Write Patterns → Read Patterns → Growth → Availability → Choose DB
```

## Step 1 — entities

Think *"What data exists?"* (Users, Orgs, Projects, Invoices, Orders, Messages, Events,
Embeddings, Files, Permissions) — never *"I need PostgreSQL."*

## Step 2 — relationships

One-to-one · one-to-many · many-to-many · hierarchical · graph · time-series · document ·
event-stream. Relationship complexity determines suitability.

## Step 3 — consistency

Classify first. *Can this ever be wrong?*

| Data | Consistency |
|---|---|
| Payments, wallets, inventory, auth | **Strong** |
| Shopping cart, feeds | Eventually acceptable |
| Analytics, logs, chat typing | Eventually fine |

## Database categories

| Category | Examples | Use for | Avoid for |
|---|---|---|---|
| Relational | PostgreSQL, MySQL | business apps, finance, SaaS, joins, transactions | — |
| Document | MongoDB, Firestore, Convex | flexible schema, nested docs, rapid iteration | heavy joins, financial, reporting |
| Key-Value | Redis, DynamoDB | sessions, cache, rate limits, locks, queues | primary DB (unless justified) |
| Time-Series | TimescaleDB, InfluxDB | metrics, IoT, telemetry | transactional workloads |
| Search | Elasticsearch, Typesense | full-text, autocomplete, ranking | hand-rolled `LIKE '%x%'` |
| Columnar | ClickHouse, BigQuery | analytics over billions of rows | OLTP |
| Vector | Qdrant, pgvector, Pinecone | RAG, embeddings, semantic search | replacing relational truth |
| Graph | Neo4j, Memgraph | social, recommendations, fraud | ordinary CRUD |
| Object Storage | S3, R2, GCS | user files | storing files in a DB |

## Default stack

Unknown requirements? Use **PostgreSQL + Redis + S3**. Solves nearly every SaaS. Add others only
when justified. **PostgreSQL-first:** battle-tested, ACID, JSON, extensions (pgvector), full-text,
partitioning, replication, logical decoding. Most startups never outgrow it.

## Modeling rules

- **Single source of truth:** one owner per piece of data; many projections (User→PG, cache→Redis,
  search→Elastic, embedding→Qdrant, analytics→ClickHouse).
- **Polyglot persistence** only when each DB has one responsibility — not "five DBs because microservices."
- **Normalize** until performance is measurable; **denormalize** only after evidence.
- **Indexes** speed reads, slow writes, cost storage — create intentionally, prune unused ones.
- **Migrations** must be versioned, repeatable, reversible, tested. Never edit prod tables manually.
- **Soft delete** only when recovery/audit/legal requires it; **UUIDv7/ULID** over sequential IDs in
  public APIs; transactions for payments/inventory/booking/wallets/orders.

## Multi-tenancy & backups

- Tenant strategy: shared table + tenant column (small SaaS) · schema per tenant (enterprise) ·
  DB per tenant (compliance). Never random.
- Every prod DB needs automated, **restore-tested** backups, PITR, and a disaster-recovery plan.
  An untested backup is not a backup.

## Review checklist

- [ ] Schema · indexes · constraints · FKs reviewed
- [ ] Backups + restore tested · slow-query logging on
- [ ] Migrations tested · capacity & growth estimated · retention defined

## Architecture decision tree

```
Need to persist data?
  ↓
Joins / transactions / financial? → PostgreSQL
Flexible schema / nested docs?    → Document (MongoDB)
Cache / sessions / rate limit?    → Redis (temporary only)
Keyword search?                   → Elasticsearch / Typesense
Semantic / RAG?                    → pgvector / Qdrant
Analytics over billions of rows?  → ClickHouse
User uploads?                     → S3 (metadata in DB)
Unknown?                          → PostgreSQL + Redis + S3
```

## Anti-patterns

- ❌ Exposing DB structure as application architecture
- ❌ Using MongoDB just because "NoSQL scales"
- ❌ Redis as the primary database
- ❌ Storing files inside the database
- ❌ Duplicating the source of truth across stores
- ❌ Denormalizing without evidence · unreviewed indexes · untested backups

## Architecture prompts

- What are the entities and their relationships?
- What consistency does this data require?
- Can PostgreSQL solve it first?
- Is this the single source of truth?
- What breaks at 100 / 10k / 1M rows?
