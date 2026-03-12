---
name: litestar-caching
description: Configure Litestar response caching with route-level `cache` controls, app-level `ResponseCacheConfig`, store selection, TTL strategy, cache key design, and `cache_response_filter` rules. Use when optimizing read-heavy or polling-heavy Litestar endpoints without breaking correctness for tenant-, locale-, or auth-scoped responses. Do not use for write-heavy or immediately consistent workflows unless cache invalidation or versioning is designed explicitly.
---

# Caching

## Execution Workflow

1. Identify handlers whose responses are deterministic, expensive, and safe to replay.
2. Choose the route-level cache mode: `cache=True`, an explicit TTL in seconds, or `CACHE_FOREVER`.
3. Set app-level `ResponseCacheConfig` for `default_expiration`, store selection, and global key/filter behavior.
4. Design cache keys around every dimension that changes the payload: path, query params, method, tenant, locale, auth scope, feature flags, or headers.
5. Decide how stale data is controlled for mutable resources: short TTL, explicit delete, or versioned keys.
6. Verify hits, misses, and stale-data behavior with tests before treating the cache as production-safe.

## Core Rules

- Cache only responses that are safe to reuse for another equivalent request.
- Prefer short, explicit TTLs for mutable data.
- Treat `cache=True` as "use `ResponseCacheConfig.default_expiration`", not as "cache forever."
- Use `CACHE_FOREVER` only for truly immutable or explicitly versioned resources.
- Never cache personalized or permission-scoped responses unless the cache key fully partitions that context.
- Keep key builders deterministic and stable across processes.
- Use `cache_response_filter` to control which responses are written to cache after the status code is known.
- Do not assume Litestar provides automatic write-side invalidation for your domain objects; design it deliberately.

## Decision Guide

- Use `cache=True` when the app-wide default TTL is correct for the route.
- Use `cache=<seconds>` when a route needs a specific freshness window.
- Use `CACHE_FOREVER` when the payload is immutable, content-addressed, or versioned externally.
- Use app-level `ResponseCacheConfig` for baseline TTL, default key builder, named store selection, and response-write filtering.
- Use route-level `cache_key_builder=` when one handler needs extra key dimensions without changing the whole app.
- Keep the default key builder when the response varies only by method, path, and query params.
- Override the key builder when the response varies by headers, tenant, locale, auth identity, or feature flags.
- Use a distributed store such as Redis when multiple app instances must share cache state.

## Reference Files

Read only the sections you need:

- For route-level `cache` modes, `ResponseCacheConfig`, default expiration, and store wiring, read [references/route-and-config-patterns.md](references/route-and-config-patterns.md).
- For custom cache key builders, tenant/user safety, and invalidation/versioning strategy, read [references/key-builder-and-invalidation.md](references/key-builder-and-invalidation.md).
- For `cache_response_filter` examples and test patterns that prove cache correctness, read [references/filter-and-testing-patterns.md](references/filter-and-testing-patterns.md).

## Recommended Defaults

- Start with `cache=True` plus an explicit app-level `default_expiration`.
- Keep the default `MemoryStore` only for single-process or low-stakes cases.
- Move to a named shared store for horizontally scaled deployments.
- Include every response-shaping input in the cache key before enabling caching on auth-, locale-, or tenant-sensitive routes.
- Cache successful `GET` responses by default; be conservative with anything else.
- Prefer short TTLs over complex invalidation when freshness requirements allow it.

## Anti-Patterns

- Caching mutation endpoints or non-idempotent workflows.
- Using `cache=True` without noticing that `default_expiration=None` makes the entry indefinite.
- Reusing the default key builder on endpoints whose response varies by headers, cookies, auth, or tenant.
- Caching permission-gated responses without identity or scope in the key.
- Assuming a shared cache while still using per-process memory storage in a multi-instance deployment.
- Using `CACHE_FOREVER` for mutable business data without explicit invalidation or versioning.
- Treating `cache_response_filter` as a substitute for good key design.

## Validation Checklist

- Confirm the route is deterministic for the chosen cache key.
- Confirm TTL or forever-caching semantics match product freshness requirements.
- Confirm the configured store is shared or local by intent.
- Confirm the key builder covers all inputs that can change the payload.
- Confirm `cache_response_filter` allows and rejects the expected status codes and methods.
- Confirm cache hits occur on equivalent requests and miss on materially different ones.
- Confirm stale-data behavior is acceptable after writes, deployments, and worker restarts.
- Confirm tests cover both correctness and isolation for tenant-, locale-, or auth-scoped data.

## Cross-Skill Handoffs

- Use `litestar-stores` for backend store lifecycle, namespacing, and TTL policy beyond response caching.
- Use `litestar-testing` to lock down cache hits, misses, and stale-data boundaries.
- Use `litestar-security` or `litestar-authentication` when response visibility depends on user identity or permissions.
- Use `litestar-responses` when response metadata or specialized response containers affect what is safe to cache.

## Litestar References

- https://docs.litestar.dev/2/usage/caching.html
- https://docs.litestar.dev/2/reference/config.html#litestar.config.response_cache.ResponseCacheConfig
- https://docs.litestar.dev/2/reference/config.html#litestar.config.response_cache.default_cache_key_builder
