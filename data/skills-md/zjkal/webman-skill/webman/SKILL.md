---
name: webman
description: >-
  Expert skill for the webman framework (a long-lived, in-memory PHP framework
  based on workerman). Covers routing, controllers, middleware, database/Redis,
  custom processes, timers, coroutines (v2), plugin development, and guarding
  against memory leaks and cross-request state pollution under the resident
  process model. Use when the project has start.php, config/process.php, or
  support/bootstrap.php, or when the user mentions webman, workerman,
  常驻内存 PHP, 协程 PHP, or long-lived/in-memory PHP.
---

# webman Framework Development

webman is a high-performance, long-lived in-memory PHP framework built on
[workerman](https://www.workerman.net/). Unlike PHP-FPM (bootstrap per request,
tear down after response), correct webman code starts from understanding the
resident-process model.

## Core Mental Model: Resident Memory

After startup, a worker stays in memory and handles thousands of requests.
Hard rules that follow:

1. **Never `exit` / `die`**: they kill the whole worker and drop every
   connection on that process.
2. **Static properties / globals survive across requests**: data written by the
   previous request can "leak" into the next. Keep request-scoped data in local
   variables, `$request` attributes, or `support\Context` under coroutines.
3. **Singletons are shared across requests**: do not store request state on
   singletons; array properties that only grow are memory leaks.
4. **Code changes need reload/restart** (`php start.php reload`). In debug
   mode, `status` / `connections` help diagnose issues.
5. **Controllers are new per request by default** (`controller_reuse => false`
   in `config/app.php`). If reuse is enabled, controller properties also
   survive across requests.

## Project Layout

```
├── app/                  # Application code
│   ├── controller/       # Controllers (optional; MVC or DDD as you prefer)
│   ├── model/            # Models
│   ├── middleware/       # Middleware
│   └── functions.php     # Custom helpers
├── config/               # All configuration
│   ├── route.php         # Routes
│   ├── process.php       # Process definitions (HTTP, custom, timers)
│   ├── middleware.php    # Middleware registration
│   ├── database.php      # Database (illuminate/database)
│   ├── redis.php         # Redis
│   └── plugin/           # Plugin config
├── plugin/               # Application plugins
├── public/               # Static assets (only web-accessible directory)
├── process/              # Custom process classes
├── support/              # Framework bridge code
└── start.php             # Entry point
```

## Common Commands

```bash
composer create-project workerman/webman   # create project

# Linux / macOS
php start.php start        # foreground (debug)
php start.php start -d     # daemon (production)
php start.php reload       # graceful reload (code updates, keep connections)
php start.php restart -d   # full restart (required after process.php, Timer, or resident data changes)
php start.php stop
php start.php status       # process memory, request counts
php start.php connections  # connection info

# Windows (no daemon / reload)
php windows.php
```

**reload vs restart**: reload only reloads app code (`app/` and most of
`config/`). Changes to `config/process.php` or timers/connections already
created in `onWorkerStart` are not reloaded — use restart.

## Coding Conventions

- PHP >= 8.0 (webman v2 requires 8.1+); always `declare(strict_types=1)`.
- Controller signatures: `public function action(Request $request): Response`,
  with `support\Request`.
- Return `Webman\Http\Response` via helpers (`response()`, `json()`, `view()`,
  `redirect()`, …). Do not `echo`.
- Prefer `illuminate/database` (`Db::table()` / Eloquent models extending
  `support\Model`).
- Read config with `config('app.debug')`; never `include` config files.
- Log with `support\Log` (`Log::info()` / `Log::channel('xx')->info()`), not
  `error_log` or `echo`.

## Do / Don't Cheatsheet

| Don't | Do |
|---|---|
| `exit()` / `die()` to end a request | `return response(...)` or throw |
| `$_GET` / `$_POST` / `$_SESSION` | `$request->get()` / `$request->post()` / `$request->session()` |
| `header()` / `setcookie()` | `$response->header()` / `$response->cookie()` |
| Unbounded static arrays | Bounded cache (LRU) or Redis |
| Request data on singletons | Locals / `support\Context` (coroutines) |
| Timers created per request in app code | Custom process in `config/process.php` |
| Static vars for request state under coroutines | `support\Context::set()` / `get()` |

## References (read on demand)

- Routing, controllers, request/response APIs: [references/routing-controller.md](references/routing-controller.md)
- Middleware (onion model, CORS, auth): [references/middleware.md](references/middleware.md)
- Database, Redis, cache, pagination, transactions: [references/database-redis.md](references/database-redis.md)
- Custom processes, WebSocket/TCP, timers: [references/custom-process.md](references/custom-process.md)
- Coroutines (webman v2), Context, concurrency, pools: [references/coroutine.md](references/coroutine.md)
- Lifecycle, memory leaks, prevention: [references/memory-lifecycle.md](references/memory-lifecycle.md)
- Plugin development (library vs app plugins): [references/plugin.md](references/plugin.md)
