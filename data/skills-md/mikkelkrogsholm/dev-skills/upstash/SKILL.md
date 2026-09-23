---
name: upstash
description: "Upstash — serverless Redis, QStash, and Vector database with per-request pricing optimized for edge and serverless environments. Use when building with Upstash or asking about its Redis client, QStash message queuing, rate limiting, workflows, or vector search. Fetch live documentation for up-to-date details."
---

# Upstash

> **CRITICAL: Your training data for Upstash is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://upstash.com/docs/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume an API exists — verify against current docs.

Upstash is a serverless data platform offering Redis, QStash (message queue), and Vector database with per-request pricing optimized for edge and serverless environments.
## Key Capabilities

- **QStash**: Built-in serverless message queue and scheduler — handles push delivery, retries, dead-letter queues, cron schedules, and URL groups without any additional infrastructure. Not a Redis feature; a separate product.
- **Auto-pipelining**: `@upstash/redis` automatically batches concurrent commands into a single HTTP request — no manual pipeline setup needed.
- **Hash field expiration**: Redis supports per-field TTL via `HEXPIRE` / `HPEXPIRE` — granular expiration below key level without external workarounds.
- **Vector hybrid search**: Vector database supports combining dense and sparse embeddings in a single index for improved relevance — no separate sparse index needed.
- **QStash flow control**: Built-in rate-limiting primitives per consumer endpoint — throttle delivery without a separate rate-limit layer.

## Best Practices

- **Use REST/HTTP SDK, not TCP connections, in serverless and edge runtimes.** Traditional Redis TCP clients exhaust connection limits fast in stateless environments. `@upstash/redis` uses HTTP and is the correct default; raw `ioredis` or `node-redis` will cause connection quota errors under load.
- **Use deduplication keys in QStash to prevent duplicate enqueuing.** QStash retries on failure by default (at-least-once delivery). A deduplication key (`Upstash-Deduplication-Id`) prevents the same message from being enqueued more than once within a ~2-hour window — it does not prevent redelivery. Your handler must still be idempotent to handle retries safely.
- **Acknowledge Redis Streams messages with XACK or the PEL will grow unbounded.** Consumer groups accumulate pending entries for unacknowledged messages. In serverless functions that may crash silently, missed `XACK` calls cause `ERR XReadGroup is cancelled` errors and stale pending entries.
- **Enable eviction in the Upstash console before hitting capacity.** The default behavior triggers `ERR DB capacity quota exceeded` rather than silently evicting old keys. Upstash uses its own proprietary eviction algorithm — it is not configurable via Redis `CONFIG SET maxmemory-policy`. Enable eviction as a binary toggle in the database settings before going to production.
- **Rotate signing keys and tokens on a schedule, not reactively.** Upstash token rotation is a manual operation with no automatic expiry. Plan key rotation in CI/CD pipelines; do not wait for a breach to rotate.
