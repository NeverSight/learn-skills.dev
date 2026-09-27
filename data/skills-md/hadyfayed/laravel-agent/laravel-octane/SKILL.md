---
name: laravel-octane
description: Laravel Octane high-performance application servers — Swoole, RoadRunner, FrankenPHP; concurrent tasks, ticks, Octane cache, Swoole tables, and memory/state safety. Use when optimizing throughput, running Octane, or handling long-running workers.
---

# Laravel Octane Skill

Supercharge your Laravel application with Octane - a persistent application server for high-performance workloads.

## When to Use

- Need extreme performance (2-4x faster than PHP-FPM)
- High-traffic applications
- Concurrent task execution required
- Microservices with heavy request loads
- API servers with low latency requirements
- WebSocket or real-time features

## Quick Start

```bash
composer require laravel/octane
php artisan octane:install
php artisan octane:start
```

## Server Choice (summary)

| Server | Best for | Trade-off |
|--------|----------|-----------|
| **Swoole** | Max concurrency, coroutines, WebSockets | Requires PHP extension |
| **RoadRunner** | Easy deployment, no extension | Slightly slower |
| **FrankenPHP** | Modern PHP, Caddy + auto HTTPS | Newer, less mature |

## Conventions Checklist

### Memory & State Safety (critical)
- [ ] NEVER store request-specific data in static properties
- [ ] Use `$this->app->scoped(...)` for request-scoped bindings, not `singleton`
- [ ] Get the user from `request()->user()`, not a constructor property
- [ ] Store uploaded files immediately before dispatching jobs
- [ ] `DB::disconnect(...)` inside connection-iterating loops
- [ ] `View::composer(...)` for per-request shared data (not `View::share` with request data)

### Workers & Recycling
- [ ] Set `swoole.options.max_request` to recycle workers (e.g. 500-1000)
- [ ] `warm` frequently used services (view, db, queue, app services)
- [ ] Monitor memory via `Octane::tick(...)` and warn near limit
- [ ] Disable query log in production (`DB::connection()->disableQueryLog()`)

### Concurrency
- [ ] Use `Octane::concurrently([...])` for parallel DB/HTTP fetches
- [ ] Use `Octane::tick(...)` for periodic background work
- [ ] Use `Octane::cache()` / Swoole tables for hot in-memory data
- [ ] Use `Lazy` collections / `chunk()` for large datasets

### Deployment
- [ ] Run under Supervisor (or Docker) — never bare
- [ ] Reload with `php artisan octane:reload` (zero-downtime)
- [ ] Restart workers after deploy (`queue:restart` does NOT apply)

## Common Pitfalls

1. **Static properties with mutable state** — data leaks across requests
2. **Singleton bindings holding user state** — use `scoped`
3. **Auth set in constructor** — persists the wrong user
4. **Uploaded file deleted before processing** — store first
5. **DB connection leaks** — disconnect in loops
6. **Unwarmed services** — slow first requests
7. **`View::share` with request data** — stale user; use a composer
8. **No memory monitoring** — worker crashes from exhaustion

## Guardrails

- NEVER store request-specific data in static properties
- NEVER use singleton bindings for services with user state
- ALWAYS use scoped bindings for request-dependent services
- ALWAYS monitor memory usage in production
- ALWAYS set `max_request` to prevent memory leaks
- ALWAYS test concurrent scenarios
- NEVER share mutable state between requests

## Related Commands

```bash
php artisan octane:install --server=swoole        # or roadrunner / frankenphp
php artisan octane:start --watch                  # development
php artisan octane:start --workers=4 --task-workers=6 --max-requests=1000  # production
php artisan octane:reload                         # zero-downtime reload
php artisan octane:status
```

## Related Skills

- `laravel-performance` - General optimization strategies
- `laravel-queue` - Background job processing
- `laravel-websocket` - Real-time communication
- `laravel-database` - Database optimization for high concurrency

## Additional references

- Servers, install, configuration, deployment, commands → [references/setup-and-servers.md](references/setup-and-servers.md)
- Concurrent tasks, ticks, Octane cache, Swoole tables, events → [references/concurrency-and-tasks.md](references/concurrency-and-tasks.md)
- Memory/state safety, service container, testing, benchmarks, pitfalls, best practices, guardrails → [references/memory-safety-and-config.md](references/memory-safety-and-config.md)
