---
name: laravel-performance
description: Laravel performance optimization — caching strategies, query and N+1 fixes, Big O complexity, Octane/queue tuning, profiling, scaling, and server tuning. Use when the app is slow, you need to optimize speed, reduce memory, fix bottlenecks, or scale for traffic. Triggers "performance", "slow", "optimize", "speed", "cache", "fast", "scaling", "bottleneck", "memory", "N+1", "Big O", "O(n)", "complexity", "nested loop", "quadratic".
---

# Laravel Performance Skill

Optimize Laravel applications for speed and scalability. Profile before optimizing, fix root causes over symptoms, and apply the right layer (query, cache, queue, or server) for each bottleneck.

## When to Use

- Application is slow or response times are high
- Need to scale for high traffic
- Memory issues or large-dataset processing
- Database bottlenecks (slow queries, N+1, Big O)
- Reviewing or tuning caching, queues, Octane, or PHP/server config

## Conventions Checklist

### Queries
- [ ] Eager-load relations with `with()` — no lazy loading in loops
- [ ] `Model::preventLazyLoading(!app()->isProduction())` enabled
- [ ] Select only needed columns (`->select(['id','name'])`)
- [ ] Use `chunk()` / `chunkById()` / `lazy()` / `cursor()` for large datasets
- [ ] Use `->count()` / `->pluck()` at the query level, not collection methods
- [ ] Add indexes for every `WHERE` / `ORDER BY` column and composite indexes for column pairs
- [ ] Batch updates with `whereIn(...)->update(...)` instead of per-row queries

### Big O
- [ ] No nested loops over two collections — eager-load or `keyBy()` / `groupBy()` for O(1) lookup
- [ ] Replace `contains()` in loops with `flip()->has()` (O(1))
- [ ] Replace `filter()` per category with a pre-grouped map
- [ ] Build strings via array + `implode()`, not repeated concatenation

### Caching
- [ ] Cache expensive queries with `Cache::remember()` and a TTL
- [ ] Use cache tags (Redis/Memcached) for invalidatable groups
- [ ] Invalidate model caches on `saved` / `deleted`
- [ ] Never cache user-specific data without per-user keys

### Async / Server
- [ ] Queue slow request work (mail, imports, reports) via `->queue()` / `dispatch()`
- [ ] Run `config:cache`, `route:cache`, `view:cache`, `event:cache` in production
- [ ] Redis for cache, sessions, and queues
- [ ] OPcache + JIT enabled; PHP-FPM tuned
- [ ] Octane only with container-injected state (no statics)

## Quick Analysis

```bash
php artisan about            # cache/optimization status
php artisan db:show          # table & index overview
php artisan telescope        # dev profiling (if installed)
```

## Optimization Targets

| Metric | Target |
|--------|--------|
| Response time | < 200ms |
| Database queries | < 10 per request |
| Memory usage | < 128MB |
| Cache hit ratio | > 90% |

## Common Pitfalls

1. **N+1 queries** — eager load with `with()`
2. **Big O (nested loops / `contains()` in loops)** — `keyBy()` / `flip()->has()`
3. **`SELECT *` and `->get()->pluck()`** — select/aggregate at query level
4. **Missing indexes** — index `WHERE` + `ORDER BY` columns
5. **No chunking** — `chunk()` / `lazy()` for large datasets
6. **Cache without invalidation** — tags or short TTL
7. **Heavy work in requests** — push to a queue
8. **Uncached routes/config** — `php artisan optimize`

## Package Integration

- **barryvdh/laravel-debugbar** — request/query profiling (dev)
- **laravel/telescope** — development profiling
- **laravel/pulse** — production monitoring
- **beyondcode/laravel-query-detector** — N+1 detection
- **laravel/horizon** — queue monitoring
- **laravel/octane** — high-performance application server

## Related Commands

- `/laravel-agent:db:optimize` — analyze and optimize database queries

## Related Skills

- `laravel-database` — migration/schema/index conventions and N+1 patterns
- `laravel-queue` — offload work to background jobs
- `laravel-octane` — Octane server setup and safety

## Additional references

- Caching strategies (query cache, model cache, Redis, fragments) → [references/caching.md](references/caching.md)
- Application-level streaming, batching, and memory optimization → [references/query-optimization.md](references/query-optimization.md)
- Profiling, scaling & server tuning (Octane, queues, Pulse, OPcache, Nginx, benchmarking) → [references/profiling-and-scaling.md](references/profiling-and-scaling.md)

**Query-level optimization** (N+1 patterns, Big O complexity, indexes) is owned by the **laravel-database** skill — see its performance reference.
