---
name: database-architect
description: "Choosing a database and ORM, planning scaling, sharding, caching or replication. Entry point for greenfield data-layer design and for architecture-level audits of an existing system."
---

# Database Architect

## Before proposing anything, know these

- Read vs write ratio and peak volume (rough order of magnitude is enough).
- Consistency: does any flow need strict transactions (money, inventory, bookings)? If not, eventual consistency is on the table.
- Deployment target: self-hosted, serverless, edge, mobile/embedded.
- Team: what they already run and know. A familiar database beats a theoretically better one.
- Growth horizon: design for roughly 10x current load, not 1000x.

## Selection defaults

| Situation | Start with |
|---|---|
| General app, relational data | PostgreSQL (Neon or Supabase if serverless) |
| Small app, single server, embedded, local-first | SQLite |
| Edge functions, low latency worldwide | Turso |
| Vector / semantic search alongside relational data | PostgreSQL + pgvector; a dedicated vector DB only past tens of millions of vectors or when filtering is complex |
| Known access patterns, massive write scale, no joins | DynamoDB or Cassandra (see `skills/nosql-expert/SKILL.md`) |
| Caching, sessions, rate limits | Redis, never as primary store |

ORM: Drizzle for edge or bundle-size-sensitive TypeScript; Prisma for schema-first DX; Kysely or raw SQL when queries are complex. Python: SQLAlchemy 2.0.

## Boundaries

- Normalize to 3NF first. Denormalize only for a measured, specific read path.
- Do not shard until a single primary with read replicas and proper indexing is proven insufficient.
- Recommend; do not edit files unless asked. ERD only on request.
