---
name: sync-ratelimit
description: "Use this skill when working with @valentinkolb/sync rate limiting in Bun/TypeScript: creating per-identifier sliding-window limiters, choosing check() vs checkOrThrow(), handling RateLimitError with resetIn/Retry-After headers, tuning window size, and reasoning about Redis key layout."
---

# Sync RateLimit

Atomic sliding-window rate limiter backed by Redis Lua. One limiter instance per logical limit — reuse across requests.

## Decision Guide

- **Soft limit** (custom response): use `check(identifier)` and inspect `result.limited`.
- **Hard limit** (fail fast): use `checkOrThrow(identifier)` and catch `RateLimitError`.
- **Retry-After header**: `Math.ceil(error.resetIn / 1000)`.

## Gotchas

- `windowSecs` defaults to `1` — very short. For API rate limiting set explicitly (e.g. `60`).
- Identifiers > 128 chars are auto-hashed with sha256 before becoming Redis keys.
- The window is sliding (weighted carry-over from previous window), not fixed-bucket.
- One Lua script per `check()` call — no batching across identifiers.
- No automatic request queuing or delay — rate-limited callers must handle backoff themselves.
- Redis key pattern: `{prefix}:{id}:{identifier}:{windowNumber}`, keys expire after `windowSecs * 2`.

## API Reference

Read full API/types/config/defaults in [references/api.md](references/api.md).
