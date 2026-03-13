---
name: sync-mutex
description: "Use this skill when working with @valentinkolb/sync distributed locks: exclusive critical sections across pods with withLock/withLockOrThrow, manual acquire/release, lease extension for long work, retry tuning, owner-safe release via Lua, and LockError handling."
---

# Sync Mutex

Lease-based distributed lock via Redis `SET NX PX`. One mutex instance per lock namespace, one lock per resource string.

## Decision Guide

- **Must-have exclusivity**: `withLockOrThrow(resource, fn)` — throws `LockError` if acquire fails.
- **Best-effort exclusivity**: `withLock(resource, fn)` — returns `null` if acquire fails.
- **Manual control**: `acquire()` → work → `release()` in `finally` block.
- **Long work**: call `extend(lock, ttlMs)` before expiry. If `extend()` returns `false`, the lock was lost — stop exclusive work immediately.

## Gotchas

- `defaultTtl` is 10s. If critical section takes longer and you don't `extend()`, the lock expires and another process can acquire it.
- `retryCount` default is 10, `retryDelay` default 200ms (+0-100ms jitter). Total acquire budget is ~2-3s.
- Resources > 128 chars are auto-hashed: key becomes `{prefix}:{id}:hash:{sha256}`.
- Release and extend use Lua owner-check scripts — only the lock holder can release/extend.
- No automatic lease renewal — you must call `extend()` explicitly.
- No fairness: contenders are not queued in order.
- `lock.expiration` is `Date.now() + ttl` at acquire/extend time. Use it to check remaining time before starting new work.
- The scheduler module uses mutex internally for leader election.

## API Reference

Read full API/types/config/defaults in [references/api.md](references/api.md).
