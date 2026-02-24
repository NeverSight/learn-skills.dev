---
name: ioredis
description: "ioredis v5 reference for Node.js Redis client — connection setup, RedisOptions, pipelines, transactions, Pub/Sub, Lua scripting, Cluster, and Sentinel. Use when: (1) creating or configuring Redis connections (standalone, cluster, sentinel), (2) writing Redis commands with ioredis (get/set, pipelines, multi/exec), (3) setting up Pub/Sub or Streams, (4) configuring retryStrategy, TLS, or auto-pipelining, (5) working with Redis Cluster options (scaleReads, NAT mapping), or (6) debugging ioredis connection issues. Important: use named import `import { Redis } from 'ioredis'` for correct TypeScript types with NodeNext."
---

# ioredis v5 — Node.js Redis Client

ioredis v5.x. Requires Node.js >= 12, Redis >= 2.6.12. 100% TypeScript.

## Critical: Import Style

```ts
// CORRECT — named import (required for NodeNext / moduleResolution: "nodenext")
import { Redis } from "ioredis";

// For Cluster:
import { Redis, Cluster } from "ioredis";
```

## When to Load References

| Need                                                                           | Reference file                                                       |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| Connection setup, RedisOptions, TLS, retryStrategy, lifecycle                  | [references/connection-options.md](references/connection-options.md) |
| Core API: pipelines, transactions, Pub/Sub, Lua scripting, scanning, events    | [references/core-api.md](references/core-api.md)                     |
| Streams, auto-pipelining, transformers, binary data, error handling, debugging | [references/advanced-patterns.md](references/advanced-patterns.md)   |
| Redis Cluster setup, ClusterOptions, Sentinel config, failover                 | [references/cluster-sentinel.md](references/cluster-sentinel.md)     |

## Quick Reference

| Operation      | Code                                                                       |
| -------------- | -------------------------------------------------------------------------- |
| Connect        | `new Redis()` or `new Redis(6379, "host")` or `new Redis("redis://...")`   |
| Get/Set        | `await redis.set("key", "val")` / `await redis.get("key")`                 |
| Pipeline       | `await redis.pipeline().set("a","1").get("a").exec()`                      |
| Transaction    | `await redis.multi().set("a","1").get("a").exec()`                         |
| Pub/Sub        | `sub.subscribe("ch")` / `sub.on("message", cb)` / `pub.publish("ch", msg)` |
| Lua script     | `redis.defineCommand("name", { numberOfKeys: 1, lua: "..." })`             |
| Scan           | `redis.scanStream({ match: "prefix:*", count: 100 })`                      |
| Graceful close | `await redis.quit()`                                                       |
| Force close    | `redis.disconnect()`                                                       |

## Common Gotchas

1. **Named import**: Always `import { Redis } from "ioredis"` with NodeNext resolution
2. **Pub/Sub isolation**: A subscribed client cannot run other commands — use separate instances
3. **`maxRetriesPerRequest`**: Default is 20. Set to `null` for infinite retries (required by BullMQ)
4. **Pipeline errors**: `pipeline.exec()` never rejects — errors are in each result's `[0]` position
5. **`showFriendlyErrorStack`**: Performance cost — never enable in production
6. **Cluster pipelines**: All keys in a pipeline must hash to slots served by the same node
7. **`enableAutoPipelining`**: 35-50% throughput improvement, safe to enable globally
