---
name: litestar-stores
description: Configure Litestar stores and the store registry for caching, server-side sessions, rate limiting, and other key-value state with explicit backend selection, bytes-safe data handling, TTL and renewal policy, namespacing, registry wiring, and lifecycle cleanup. Use when a Litestar app depends on `MemoryStore`, `FileStore`, `RedisStore`, `ValkeyStore`, or `StoreRegistry`. Do not use for relational persistence, domain repositories, or response-caching policy details that belong in database or caching-focused skills.
---

# Stores

Use this skill when the problem is Litestar's interchangeable key-value store layer, not relational data modeling.

## Execution Workflow

1. Decide whether the feature really belongs in a Litestar store: cache, session, rate limit, or other ephemeral/shared key-value state.
2. Choose the backend based on process model, durability, latency, and cleanup needs.
3. Decide whether stores should be wired explicitly by name, created lazily through `StoreRegistry`, or derived from a namespaced default factory.
4. Define key naming, namespacing boundaries, TTL policy, and any renewal-on-read behavior.
5. Wire integrations such as response caching, sessions, or rate limiting to named stores intentionally.
6. Plan cleanup and shutdown behavior, especially for `FileStore` expiry cleanup and Redis client ownership.
7. Verify expiry, isolation, and multi-worker behavior before relying on the store in production.

## Core Rules

- Treat stores as interchangeable key-value infrastructure, not as ad hoc object persistence.
- Design for the store contract: values are bytes-oriented, even when a backend has extra convenience behavior.
- Keep namespacing and store names intentional before using bulk operations like `delete_all()`.
- Match TTL policy to the feature: absolute expiry, renewal on access, or no expiry.
- Do not assume all backends clean up expired data the same way.
- Prefer named stores or namespaced stores over one flat keyspace shared by unrelated features.
- Use a distributed backend for any state that must survive across workers or instances.
- Make store ownership explicit when external clients or filesystem paths need lifecycle management.

## Decision Guide

- Use `MemoryStore` for simple single-process caching or low-stakes ephemeral state with minimal overhead.
- Use `FileStore` when persistence on disk matters more than speed, especially for larger or longer-lived data.
- Use `RedisStore` for general production-grade shared state, multi-worker communication, and namespaced bulk operations.
- Use `ValkeyStore` when you want Redis-style behavior on Valkey; Litestar documents it as equivalent in practice to Redis for these store concerns.
- Use explicit `stores={...}` mappings when integrations must resolve known store names.
- Use `StoreRegistry(default_factory=...)` when undefined store names should be created lazily from one policy.
- Use `with_namespace()` when one underlying backend should safely host multiple isolated logical stores.
- Use `litestar-caching` alongside this skill when response-cache TTL, cache keys, or cache filtering are the main design problem.

## Reference Files

Read only the sections you need:

- For store operations, bytes-vs-string behavior, TTL renewal, and cleanup mechanics, read [references/store-operations-and-data.md](references/store-operations-and-data.md).
- For backend selection tradeoffs and backend-specific operational notes, read [references/backend-selection-and-lifecycle.md](references/backend-selection-and-lifecycle.md).
- For `StoreRegistry`, namespacing, integration wiring, and default-factory patterns, read [references/registry-and-namespacing.md](references/registry-and-namespacing.md).

## Store Fundamentals

Litestar store operations center around a small async API:

- `set(key, value, expires_in=...)`
- `get(key, renew_for=...)`
- `delete(key)`
- `delete_all()`
- `exists(key)`
- `expires_in(key)`

Key behavioral rules from the docs:

- Stores generally accept bytes and return bytes.
- `set()` also accepts strings for convenience, but `get()` still returns bytes.
- `expires_in` can be set when writing data.
- `renew_for` can be passed to `get()` to extend TTL on access when the backend supports expiry for that key.
- If `delete()` is called for a missing key, it is a no-op.

## Backend Selection

### `MemoryStore`

- Default Litestar store.
- Lowest overhead.
- No persistence.
- Not thread-safe or multiprocess-safe.
- Avoid for multi-worker or multi-instance shared state.

### `FileStore`

- Persists data on disk.
- Slower than memory-backed approaches.
- Good fit when data volume, longevity, or backupability matters.
- Supports namespacing via sub-paths.
- Expired entries are not proactively removed; plan `delete_expired()` calls.

### `RedisStore`

- Suitable for almost all applications that need shared or durable-ish key-value infrastructure.
- Supports namespacing and safe namespace-scoped `delete_all()`.
- Native expiry behavior comes from Redis itself.
- Good fit for multi-worker deployments, sessions, rate limiting, and shared cache state.

### `ValkeyStore`

- Same practical guidance as `RedisStore` according to the Litestar docs.
- Supports namespacing.
- Use when the deployment standard is Valkey rather than Redis.

## TTL and Expiry Semantics

- Use `expires_in` on `set()` for absolute expiration.
- Use `renew_for` on `get()` for sliding expiration or access-based renewal, such as sessions or LRU-like behavior.
- Redis/Valkey use native expiry mechanisms.
- `FileStore` deletes expired values only when they are accessed or when `delete_expired()` is run explicitly.
- `MemoryStore` and `FileStore` may retain expired data until access or cleanup; do not treat TTL as equivalent to immediate background deletion on those backends.

## Namespacing

- Namespacing exists to make shared backends safe for multiple logical purposes.
- `with_namespace()` creates a child store whose operations affect only that namespace and its children.
- This is especially important before using `delete_all()`.
- `RedisStore` uses `LITESTAR` as the default namespace.
- Passing `namespace=None` disables Redis namespacing and makes `delete_all()` unavailable.
- File-backed namespacing uses sub-paths under the parent store path.

## Store Registry

- `Litestar.stores` exposes the application's `StoreRegistry`.
- A registry can start from a mapping of store names to store instances.
- `app.stores.get(name)` returns a registered store or creates one via the registry's `default_factory`.
- The default registry factory returns a new `MemoryStore` for unknown names.
- You can pass a custom `StoreRegistry` to change that behavior globally.
- `StoreRegistry.register(name, store, allow_override=False)` is the explicit registration path when dynamic creation is not enough.

## Integration Wiring

Litestar integrations resolve stores by name through the registry. Important consequences:

- Response caching defaults to the `response_cache` store name unless configured otherwise.
- Session middleware defaults to the `sessions` store name unless configured otherwise.
- Rate limiting resolves its store by name as well.
- These names are conventions, not magic constants; you can point integrations at other names with their own config.
- One registry can host multiple backends for different integrations, or one namespaced backend can serve many integrations through the default factory.

## Data Contract and Serialization Boundary

- The portable store contract is bytes-based.
- Do not rely on backend-specific object behavior if the store may be swapped later.
- `MemoryStore` can technically hold arbitrary Python objects because it stores directly in memory, but Litestar's documented interface does not guarantee that portability.
- Serialize structured values explicitly before storing when backend interchangeability matters.

## Cleanup and Lifetime

- Call `delete_expired()` periodically for `MemoryStore` and especially `FileStore` when stale entries would otherwise accumulate.
- `FileStore.delete_expired()` is a good startup or maintenance task when the directory is long-lived.
- If you create a `RedisStore` directly around your own Redis client and do not use the helper lifecycle, you are responsible for shutting that client down.
- Prefer `RedisStore.with_client(...)` or explicit ownership flags when you want Litestar/the store to manage the client lifecycle.

## Recommended Defaults

- Keep `MemoryStore` only for local development, single-process apps, or low-stakes ephemeral state.
- Prefer Redis or Valkey for shared cache, sessions, and rate limits in production.
- Use explicit store names for integrations when different backends serve different concerns.
- Use one root namespaced Redis/Valkey store when you want shared infrastructure with isolated logical children.
- Serialize structured data to bytes or strings intentionally rather than leaning on `MemoryStore` object storage.
- Run expiry cleanup on file-backed stores as a deliberate maintenance task.

## Example Pattern

```python
from litestar import Litestar, get
from litestar.config.response_cache import ResponseCacheConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.stores.redis import RedisStore
from litestar.stores.registry import StoreRegistry


root_store = RedisStore.with_client()


@get("/cached", cache=True, sync_to_thread=False)
def cached_handler() -> str:
    return "hello"


app = Litestar(
    [cached_handler],
    stores=StoreRegistry(default_factory=root_store.with_namespace),
    response_cache_config=ResponseCacheConfig(store="response_cache"),
    middleware=[
        ServerSideSessionConfig(store="sessions").middleware,
        RateLimitConfig(rate_limit=("second", 10), store="rate_limit").middleware,
    ],
)
```

## Anti-Patterns

- Using `MemoryStore` for state that must be shared across workers or processes.
- Treating stores as a substitute for relational or queryable persistence.
- Storing arbitrary Python objects because `MemoryStore` happens to allow it.
- Using one flat keyspace and then calling `delete_all()` without namespaces or isolated store names.
- Assuming expired entries disappear immediately on `FileStore` or `MemoryStore`.
- Forgetting to clean up filesystem-backed expired entries.
- Passing `namespace=None` to Redis and then expecting safe namespace-scoped bulk deletion.
- Assuming integration store names are fixed and unchangeable instead of config-driven.
- Adding Memcached as if it were a supported drop-in backend.

## Validation Checklist

- Confirm the selected backend matches process topology and durability requirements.
- Confirm values are serialized in a backend-portable way when portability matters.
- Confirm TTL behavior matches actual backend semantics, including renewal-on-read where used.
- Confirm file- or memory-backed stores have an explicit expired-entry cleanup strategy when needed.
- Confirm namespacing or store naming prevents cross-feature collisions and unsafe bulk deletion.
- Confirm `app.stores.get(name)` resolves the intended store for each integration.
- Confirm cache, sessions, and rate limiting are pointed at the intended store names.
- Confirm Redis/Valkey client shutdown ownership is explicit.
- Confirm multi-worker deployments do not depend on `MemoryStore`.

## Cross-Skill Handoffs

- Use `litestar-caching` for response-cache TTL, key-builder, and cache-filter strategy.
- Use `litestar-authentication` or `litestar-security` when session/auth data is the main concern.
- Use `litestar-middleware` when rate limit or session middleware behavior is the primary task.
- Use `litestar-app-setup` for startup/shutdown cleanup hooks around store maintenance.
- Use `litestar-testing` to verify expiry, integration wiring, and multi-backend behavior.

## Litestar References

- https://docs.litestar.dev/latest/usage/stores.html
- https://docs.litestar.dev/latest/usage/caching.html
- https://docs.litestar.dev/latest/reference/stores/base.html
- https://docs.litestar.dev/latest/reference/stores/memory.html
- https://docs.litestar.dev/latest/reference/stores/registry.html
- https://docs.litestar.dev/latest/reference/stores/file.html
- https://docs.litestar.dev/latest/reference/stores/redis.html
- https://docs.litestar.dev/latest/reference/stores/valkey.html
