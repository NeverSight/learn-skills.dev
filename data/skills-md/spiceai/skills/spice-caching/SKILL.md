---
name: spice-caching
description: Configure Spice.ai in-memory caching for SQL query results, search results, and embeddings. Use when setting up caching, tuning cache TTL/size/eviction, configuring stale-while-revalidate, custom cache keys, or cache-control headers.
---

# Spice Caching

Configure in-memory caching for SQL query results, search results, and embeddings in the Spice runtime.

## Overview

Spice caches results from SQL queries (`/v1/sql`), search (`/v1/search`), and embeddings requests. All three caches are **enabled by default** with a 1-second TTL and 128 MiB max size. Caching applies to HTTP and Arrow Flight APIs.

## Configuration

Caching is configured under `runtime.caching` in `spicepod.yaml`:

```yaml
version: v1
kind: Spicepod
name: app

runtime:
  caching:
    sql_results:
      enabled: true
      max_size: 1GiB # Default 128MiB
      item_ttl: 1m # Default 1s
      eviction_policy: lru # lru | tiny_lfu
      hashing_algorithm: xxh3
      cache_key_type: plan # plan | sql
      encoding: none # none | zstd
      stale_while_revalidate_ttl: 30s # Default 0s (disabled)
    search_results:
      enabled: true
      max_size: 1GiB
      item_ttl: 1m
      eviction_policy: lru
    embeddings:
      enabled: true
      max_size: 128MiB
      item_ttl: 1m
```

## Common Parameters (All Cache Types)

| Parameter           | Default  | Description                                                                           |
| ------------------- | -------- | ------------------------------------------------------------------------------------- |
| `enabled`           | `true`   | Enable/disable the cache                                                              |
| `max_size`          | `128MiB` | Maximum cache size                                                                    |
| `eviction_policy`   | `lru`    | `lru` (Least Recently Used) or `tiny_lfu` (higher hit rate for skewed access)         |
| `item_ttl`          | `1s`     | Cache entry TTL (Time to Live)                                                        |
| `hashing_algorithm` | `xxh3`   | Hash for cache keys: `xxh3`, `ahash`, `siphash`, `blake3`, `xxh32`, `xxh64`, `xxh128` |

## SQL Results Extra Parameters

| Parameter                    | Default | Description                                                                                                        |
| ---------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------ |
| `cache_key_type`             | `plan`  | `plan` = logical plan (matches semantically equivalent queries); `sql` = raw SQL string (faster, exact match only) |
| `encoding`                   | `none`  | `none` or `zstd` (compresses cached results, 50-90% reduction)                                                     |
| `stale_while_revalidate_ttl` | `0s`    | Serve stale entries while refreshing in background. `0s` = disabled                                                |

## Choosing Parameters

### `cache_key_type`

- **`plan`** (default): Matches semantically equivalent queries even with different SQL syntax. Requires query parsing overhead.
- **`sql`**: Faster lookups, exact string match. Avoid with dynamic functions like `NOW()`.

### `eviction_policy`

- **`lru`** (default): Good general-purpose policy.
- **`tiny_lfu`**: Better hit rate when some queries are accessed much more frequently than others.

### `encoding`

- **`none`** (default): Zero compression overhead, uses more memory.
- **`zstd`**: High compression (50-90% reduction) with fast decompression. Use for large result sets.

### `hashing_algorithm`

- **`xxh3`** (default): Fastest general-purpose.
- **`ahash`** / **`xxh64`** / **`xxh128`**: Lower collision probability for many cached queries.
- **`blake3`**: Cryptographic security required.
- **`siphash`**: Protection against hash-flooding DoS attacks.

## Stale-While-Revalidate

When `stale_while_revalidate_ttl` is set to a non-zero value:

1. Cache entries are served normally until `item_ttl` expires.
2. After `item_ttl` expires but before `item_ttl + stale_while_revalidate_ttl`, the stale entry is served immediately with `STALE` status.
3. A background task refreshes the cache entry.
4. After `item_ttl + stale_while_revalidate_ttl`, the entry is evicted.

```yaml
runtime:
  caching:
    sql_results:
      enabled: true
      item_ttl: 10s
      stale_while_revalidate_ttl: 10s
      # Fresh for 10s → Stale (served while refreshing) for 10s → Evicted
```

> **Conflict warning**: When using `refresh_mode: caching` on a dataset, do not configure both `runtime.caching.sql_results.stale_while_revalidate_ttl` and `acceleration.params.caching_stale_while_revalidate_ttl` for the same dataset. Choose one approach.

## Cache Control Headers

### HTTP API

Use the standard `Cache-Control` header with `/v1/sql` and `/v1/search`:

| Directive          | Description                                                       |
| ------------------ | ----------------------------------------------------------------- |
| `no-cache`         | Skip cache for this request; cache the result for future requests |
| `min-fresh=N`      | Require cached entry to remain fresh for at least N seconds       |
| `max-stale=N`      | Accept stale responses up to N seconds old                        |
| `only-if-cached`   | Return only cached responses; error on cache miss                 |
| `stale-if-error=N` | Serve stale cache (up to N seconds) if fetching fresh data fails  |

```bash
# Skip cache for this query
curl -H "cache-control: no-cache" -XPOST http://localhost:8090/v1/sql -d 'SELECT 1'

# Only accept fresh results (at least 30s remaining)
curl -H "cache-control: min-fresh=30" -XPOST http://localhost:8090/v1/sql -d 'SELECT 1'

# Accept stale up to 60s
curl -H "cache-control: max-stale=60" -XPOST http://localhost:8090/v1/sql -d 'SELECT 1'

# Only return if cached
curl -H "cache-control: only-if-cached" -XPOST http://localhost:8090/v1/sql -d 'SELECT 1'
```

### Spice CLI

```bash
spice sql --cache-control no-cache
spice sql --cache-control min-fresh=30
spice sql --cache-control max-stale=60
spice sql --cache-control only-if-cached
spice search --cache-control no-cache
```

### Arrow FlightSQL

Set `cache-control` in request metadata:

```rust
let mut request = FlightDescriptor::new_cmd(sql_command_bytes).into_request();
request.metadata_mut().insert("cache-control", "no-cache");
```

JDBC:

```java
Properties props = new Properties();
props.setProperty("cache-control", "no-cache");
Connection conn = DriverManager.getConnection("jdbc:arrow-flight-sql://localhost:50051", props);
```

## Custom Cache Keys

Set the `Spice-Cache-Key` header to share cache entries across semantically equivalent but syntactically different queries. Valid keys: up to 128 alphanumeric characters plus `-` and `_`. Custom keys take precedence over `cache_key_type`.

```bash
# First query — cache MISS
curl -XPOST http://localhost:8090/v1/sql \
  -H "spice-cache-key: users_spiceai" \
  -d "select * from users where org_id = 1;"

# Different query, same cache key — cache HIT
curl -XPOST http://localhost:8090/v1/sql \
  -H "spice-cache-key: users_spiceai" \
  -d "select * from users where split_part(email, '@', 2) = 'spice.ai';"
```

> **Warning**: Ensure queries sharing a cache key are truly semantically equivalent. The runtime will return the cached result regardless of the actual query.

## Response Headers

Responses include a header indicating cache status:

| Cache Type       | Response Header               |
| ---------------- | ----------------------------- |
| `sql_results`    | `Results-Cache-Status`        |
| `search_results` | `Search-Results-Cache-Status` |

| Status     | Meaning                                              |
| ---------- | ---------------------------------------------------- |
| `HIT`      | Served from cache                                    |
| `MISS`     | Cache checked, result not found                      |
| `BYPASS`   | Cache bypassed (e.g., `cache-control: no-cache`)     |
| `STALE`    | Stale entry served while revalidating                |
| _(absent)_ | Cache did not apply (disabled or system table query) |

## Monitoring / Metrics

Cache metrics are available at the Prometheus-compatible metrics endpoint. Prefix by cache type: `results_*`, `search_results_*`, `embeddings_*`.

| Metric                   | Type    | Description               |
| ------------------------ | ------- | ------------------------- |
| `*_cache_max_size_bytes` | Gauge   | Configured max cache size |
| `*_cache_requests`       | Counter | Total cache lookups       |
| `*_cache_hits`           | Counter | Total cache hits          |
| `*_cache_items_count`    | Gauge   | Current items in cache    |
| `*_cache_size_bytes`     | Gauge   | Current cache size        |
| `*_cache_evictions`      | Counter | Total evictions           |
| `*_cache_hit_ratio`      | Gauge   | Hit ratio (hits / total)  |

## Common Recipes

### High-throughput Dashboard (Maximize Hit Rate)

```yaml
runtime:
  caching:
    sql_results:
      item_ttl: 30s
      max_size: 2GiB
      eviction_policy: tiny_lfu
      encoding: zstd
      stale_while_revalidate_ttl: 30s
```

### Low-Latency API (Exact Queries, Fast Lookups)

```yaml
runtime:
  caching:
    sql_results:
      item_ttl: 5s
      cache_key_type: sql
      hashing_algorithm: xxh3
```

### Disable Caching Entirely

```yaml
runtime:
  caching:
    sql_results:
      enabled: false
    search_results:
      enabled: false
    embeddings:
      enabled: false
```

## Troubleshooting

| Issue                                                | Solution                                                                                                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Always getting `MISS`                                | Check `item_ttl` is long enough; verify `cache_key_type` (`plan` matches equivalent queries, `sql` requires exact strings)                                |
| Cache filling up quickly                             | Increase `max_size`, enable `zstd` encoding, or reduce `item_ttl`                                                                                         |
| Stale data being served                              | Reduce `item_ttl` or `stale_while_revalidate_ttl`; use `cache-control: no-cache` for specific queries                                                     |
| Dynamic functions (`NOW()`) returning cached results | Switch to `cache_key_type: plan` or use `cache-control: no-cache`                                                                                         |
| SWR conflict error                                   | Don't set both `runtime.caching.sql_results.stale_while_revalidate_ttl` and `acceleration.params.caching_stale_while_revalidate_ttl` for the same dataset |
