---
name: valkey
description: 'Valkey (Redis-compatible) in-memory data store for caching, session storage, pub/sub, queues, and distributed locks. Use when configuring Valkey or Redis-compatible caching, choosing eviction policies, implementing rate limiting, setting up pub/sub or streams, writing Docker Compose services, migrating from Redis, or tuning performance. Use for valkey, redis, cache, session, pub/sub, streams, distributed-lock, rate-limit, sorted-set.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://valkey.io/commands/'
user-invocable: false
---

# Valkey

Open-source, Redis-compatible in-memory data store maintained by the Linux Foundation. Forked from Redis OSS 7.2.4 (BSD 3-Clause license). Drop-in replacement for Redis OSS 2.x through 7.2.x — same protocol, commands, and data formats.

**When to use**: Caching, session storage, rate limiting, pub/sub messaging, task queues, leaderboards, distributed locks, real-time counters, or any workload requiring sub-millisecond key-value operations.

**When NOT to use**: Primary relational data store, large object storage (>512 MB values), workloads requiring strong ACID transactions across multiple keys without Lua scripting.

## Quick Reference

| Task               | Approach                                                 | Key Point                               |
| ------------------ | -------------------------------------------------------- | --------------------------------------- |
| Cache-aside        | `GET` -> miss -> DB read -> `SET key val EX ttl`         | Always set a TTL, even a long one       |
| Session storage    | `HSET session:{id} field val` + `EXPIRE`                 | Sliding TTL on each request             |
| Rate limiting      | `INCR` + `EXPIRE` (fixed window) or sorted set (sliding) | Sorted set for precision                |
| Distributed lock   | `SET lock:{res} token NX PX 30000`                       | Always set expiry to prevent deadlocks  |
| Queue (simple)     | `LPUSH` + `BRPOP`                                        | Blocking pop with timeout               |
| Queue (reliable)   | Streams + `XGROUP` + `XACK`                              | Consumer groups for at-least-once       |
| Pub/Sub            | `SUBSCRIBE` / `PUBLISH`                                  | Fire-and-forget, no persistence         |
| Streams            | `XADD` + `XREADGROUP`                                    | Persistent, replayable, consumer groups |
| Leaderboard        | Sorted set: `ZADD` / `ZREVRANGE`                         | O(log N) rank operations                |
| Unique count       | `PFADD` + `PFCOUNT` (HyperLogLog)                        | ~12 KB memory, 0.81% error              |
| Eviction policy    | `maxmemory-policy allkeys-lru`                           | Best default for most workloads         |
| Docker setup       | `valkey/valkey:8.1-alpine`                               | Health check: `valkey-cli ping`         |
| Persistence        | AOF (`appendonly yes`) + RDB snapshots                   | AOF for durability, RDB for backups     |
| Client library     | `ioredis` or `iovalkey` (official fork)                  | All Redis clients work unchanged        |
| Migrate from Redis | Swap binary, keep data files                             | RDB/AOF compatible through Redis 7.2    |

## Common Mistakes

| Mistake                                | Correct Pattern                                  |
| -------------------------------------- | ------------------------------------------------ |
| Using `KEYS *` in production           | Use `SCAN` with cursor for iteration             |
| No TTL on cache keys                   | Always set TTL — unbounded growth causes OOM     |
| `DEL` on large keys blocking server    | Use `UNLINK` for async deletion                  |
| Pub/Sub for durable messaging          | Use Streams with consumer groups for persistence |
| Same TTL on all keys (thundering herd) | Add jitter: `EX (base + random(0, spread))`      |
| No `maxmemory` set in production       | Set `maxmemory` + eviction policy explicitly     |
| Using `MULTI/EXEC` for locking         | Use `SET ... NX PX` for distributed locks        |
| Storing large blobs (>1 MB values)     | Store references; keep values small              |
| No health check in Docker Compose      | Add `valkey-cli ping` health check               |
| Ignoring `requirepass` in production   | Always set authentication + ACLs                 |

## Delegation

- **Discover caching patterns and data model review**: Use `Explore` agent
- **Plan migration strategy from Redis to Valkey**: Use `Plan` agent
- **Implement full caching layer with tests**: Use `Task` agent

> If the `docker` skill is available, delegate Compose networking and multi-stage build patterns to it.
> If the `performance-optimizer` skill is available, delegate application-level caching strategy to it.
> If the `database-security` skill is available, delegate ACL and TLS configuration review to it.

## References

- [Data structures and commands](references/data-structures.md) -- Strings, hashes, lists, sets, sorted sets, streams, HyperLogLog, bitmaps, geospatial
- [Caching patterns](references/caching-patterns.md) -- Cache-aside, write-through, TTL strategies, eviction policies, client-side caching, invalidation
- [Common patterns](references/common-patterns.md) -- Rate limiting, distributed locks, queues, session storage, pub/sub, streams, leaderboards
- [Docker and deployment](references/docker-and-deployment.md) -- Compose setup, persistence, replication, Sentinel, Cluster, security, migration from Redis
