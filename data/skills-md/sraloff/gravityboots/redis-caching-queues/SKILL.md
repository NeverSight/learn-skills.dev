---
name: redis-caching-queues
description: Redis patterns, caching strategies, and Laravel Horizon / Python task queues.
---

# Redis Caching & Queues

## When to use this skill
- Implementing caching (KV store).
- Setting up background job queues.
- Configuring Redis persistence.

## 1. Caching Strategies
- **TTL**: Always set a Time-To-Live (TTL) for cache keys to prevent memory leaks.
- **Keys**: Use namespaced keys `app:user:123` to avoid collisions.
- **Invalidation**: Prefer short TTLs over complex invalidation logic where possible.

## 2. Queues
- **Laravel**: Use `redis` driver for queue. Run `php artisan horizon` for monitoring.
- **Python**: Use Celery or RQ backed by Redis.
- **Atomicity**: Use `LPUSH`/`RPOP` or Streams for reliable messaging.

## 3. Configuration
- **Maxmemory**: Configure `maxmemory` and eviction policy (`allkeys-lru` for cache, `noeviction` for queues).
- **Persistence**: Enable RDB snapshots for queues; AOF for higher durability needs.
