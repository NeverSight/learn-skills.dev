---
name: redis-best-practices
description: Redis best practices and performance rules for production, for any Redis deployment including open source Redis, Valkey, Redis Cloud, AWS ElastiCache, Google Memorystore, Azure Cache, and Upstash. Based on real support cases and measured on real databases. Use when writing, reviewing, or debugging Redis code for performance or scale, when choosing between pipeline and MGET, KEYS and SCAN, or WATCH and Lua, or when the user mentions Redis best practices, Redis performance, slow Redis, Redis latency, high memory use, a high Redis bill, big keys, hot keys, large hashes, HGETALL, cache hit rate, TTL jitter, key expiration, cache stampede, maxmemory and eviction policies, unbounded lists or streams, XACK and consumer groups, pub/sub vs streams, Lua script blocking, key-based locking for Lua scripts, connection pooling, serverless connections, retries and timeouts, replication lag, ACL users, credential rotation, or Redis monitoring. Also explains errors such as OOM command not allowed, BUSY Redis is busy running a script, NOSCRIPT, CROSSSLOT, and Upstash limit errors.
license: MIT
metadata:
  author: Upstash
  homepage: https://upstash.com
---

# Redis Best Practices

Rules for code that talks to Redis, on any deployment. They come from real support cases and from tests on two engines:

- **Stock Redis:** Redis 8 with default settings and the client on the same machine, so no network cost.
- **Upstash Redis:** with the client in the same region, about 1 ms away.

Engines differ. Stock Redis runs commands on one main thread, so one slow command stalls every client. Valkey, managed services and Upstash change some defaults and limits. Rules below apply everywhere unless they name an engine, and [On Upstash](#on-upstash) collects what differs there.

## Decide what the database is

- **Cache:** eviction on, and a TTL on every key.
- **Store:** eviction off, backups on, and a size limit raised before it is hit.

Half the trouble in support comes from databases that are neither, growing until writes fail or keys vanish. A cache with no expirations and a high miss rate only grows.

Know the eviction policy. Open source Redis defaults to `noeviction`, which fails writes at the limit, and some managed services default to `volatile-lru`. For a pure cache, use `allkeys-lru` or `allkeys-lfu`, but remember they delete keys you may not be able to reload. `volatile-*` policies only evict keys with a TTL, so a store without TTLs frees nothing. Eviction is sampled and approximate, so keep headroom. A database pinned at its limit evicts all day.

## Batch with the right command

| Need | Use |
| --- | --- |
| Read many plain keys | `MGET` in chunks of 1,000 |
| Write many plain keys | `MSET` in chunks of 1,000 |
| Read many fields of one hash | `HMGET` |
| Mixed commands | Pipeline in chunks of 1,000 |
| All or nothing | `MULTI`/`EXEC` |

A pipeline saves round trips, never commands. `MGET` is one command, so it beats a pipeline of `GET`s wherever it fits. Reading 1,000 keys:

| Distance to the database | Await each `GET` | Pipeline | `MGET` |
| --- | --- | --- | --- |
| Same machine (stock Redis) | 46 ms | 3.6 ms | 1.3 ms |
| 1 ms (Upstash) | 1,023 ms | 6.7 ms | 3.8 ms |
| 116 ms (Upstash) | 118,016 ms | 172 ms | 140 ms |

Always chunk. Redis queues replies in memory, and normal clients have no output buffer limit by default. While stock Redis read 200,000 keys of 1 KB, another client's slowest read was 48.8 ms during one pipeline and 73.9 ms during one `MGET`, against 0.84 ms and 0.51 ms in chunks of 1,000. Lower the chunk size when values are large, because reply bytes are the real cost.

A pipeline isn't atomic, so if it fails partway, the commands before the failure stay applied. On a cluster, `MGET` and `MSET` need all their keys in one slot, so use hash tags or a pipeline per node.

Details and numbers: [Why MGET Is Faster Than a Redis Pipeline for Reading Many Keys](https://upstash.com/kb/redis-pipeline-vs-mget)

## Keep keys small and bounded

- Keep values in the tens of kilobytes. Redis's own guide calls hundreds of kilobytes a big key. Put large files in object storage and keep the path in Redis, or compress on the client. One cache served 400 KiB values at 12 M reads a day, which came to over 100 TB of bandwidth a month.
- Keep collections under about 10,000 members. Split larger ones by a hash of the ID or by time bucket.
- Prefer named fields to whole collections. On stock Redis at 1 million fields, `HGETALL` took 1,126 ms and stalled another client for 96 ms, while `HMGET` of 10 fields took 0.4 ms.
- Delete big keys with `UNLINK`. On stock Redis at 1 million fields, `DEL` took 319 ms and stalled another client for 314 ms, while `UNLINK` took 0.3 ms. Lazy freeing is off by default in Redis, and on by default in Valkey 8.
- Bound every queue from the first write: `XADD ... MAXLEN ~ 1000` or `MINID`, `LTRIM` after every `LPUSH`, and a TTL on temporary results, including anything a `*STORE` command produces.
- Spread hot keys. A key lives on one shard, so adding nodes won't help it. A local cache of a few seconds is the simplest fix, then read replicas, then splitting writes across keys.
- Find problem keys with `redis-cli --bigkeys`, `--memkeys`, `--hotkeys` (needs an LFU policy) and `MEMORY USAGE`.

Details and numbers: [How Big Should a Redis Key Be?](https://upstash.com/kb/redis-big-keys)

## TTLs and cache hit rate

- Put a TTL on every cache key, with `SET key value EX ttl` in one command.
- Add 10% jitter when many keys are written together. In a bulk load of 5,000 keys, it cut peak misses per second from 1,687 to 760 on stock Redis and from 1,683 to 779 on Upstash, which protects the database behind the cache. Total misses stay about the same, so a higher hit rate needs a longer TTL.
- Set jitter in milliseconds on short TTLs, or rounding removes it.
- Protect a single hot key with a lock or stale-while-revalidate, since jitter spreads many keys and one key still expires at one moment. See [the thundering herd guide](https://upstash.com/kb/thundering-herd-problem-cache-stampede).
- Cache negative results with a sentinel and a short TTL, or keep a membership set or bloom filter.
- Watch the miss rate. A cache that misses more than it hits is a bug: reads ask for one prefix and writes use another, or the TTL is shorter than the reuse interval. One database did 800 M reads a day at a 99 percent miss rate.

Details and numbers: [How TTL Jitter Protects Your Database When Redis Keys Expire Together](https://upstash.com/kb/redis-ttl-jitter)

## Commands

| Instead of | Use | Why |
| --- | --- | --- |
| `KEYS` in code | `SCAN`, or an index set | `KEYS` walks the whole keyspace in one call. With 1 million keys on stock Redis, ten calls at once stalled another client for 823 ms, against a normal read of 0.08 ms |
| `SCAN` with a low `COUNT` | `COUNT 1000` | `MATCH` filters after the walk, so finding 100 keys among 1 million took 9,953 pages at `COUNT 100` and 1,000 at `COUNT 1000` |
| Sweeping for the same keys repeatedly | A set that holds their names | One database swept its keyspace 525 times a day, and another once a second from edge functions |
| `HGETALL`, `SMEMBERS`, `LRANGE 0 -1` | `HMGET`, `SSCAN`, `LRANGE` windows | Whole-collection reads grow with the data |
| `XRANGE key - +` | `XRANGE` with `COUNT`, paging from the last ID | Same reason, and some engines limit the reply |
| `SET` then `EXPIRE` | `SET key value EX ttl` | One command, and no key left without a TTL |
| `EXISTS` then `SET` | `SET key value NX` | One command, no race |
| `EXISTS` then `GET` | `GET` | One command |
| `SORT` | A sorted set, or sort on the client | O(N log N) on the server |
| `INFO`, `DBSIZE`, `CONFIG GET` as health checks | `PING` | Some clients run these on every connection |
| `*STORE` on every call | Update the result on write, or `ZRANGESTORE ... LIMIT` | Each call recomputes the whole result. One database ran 740 K `ZINTERSTORE` a day |
| `FLUSHDB` in code | `SCAN` plus `UNLINK` by prefix, and separate databases per environment | One copied console command wipes the data |
| Polling `XLEN`, `XPENDING` or `TTL` in a loop | `XREADGROUP ... COUNT n BLOCK 5000` | One consumer group ran 1.3 M reads a day against 850 K acknowledgements |

- Never run `MONITOR` in production. It streams every command to one client, and can cut throughput by more than half.
- Give blocking reads a finite timeout and a small, limited pool, because each one parks a connection.
- Use pub/sub only when losing messages is fine. Delivery is at most once, and by default a subscriber is disconnected at 32 MB of buffered output. Use streams for anything durable.
- Have stream consumers call `XACK`, use `XAUTOCLAIM` for dead consumers, and add a dead-letter path. Trimming a stream doesn't clear its pending entries by default.
- Leave keyspace notifications off unless something consumes them. They cost every write.
- Name keys `service:entity:id`, and keep names short. Prefer prefixes to numbered databases, which clusters and many managed services don't offer. Use hash tags like `{tenant}` when multi-key commands or scripts must see keys together.
- Know what your library does per call. One database spent 2.3 M of its 9 M daily commands on `SCRIPT` alone.

Details and numbers: [How to List Keys in Redis Safely With SCAN](https://upstash.com/kb/redis-keys-vs-scan)

## Scripts and transactions

Use the built-in command first (`INCR`, `SET NX`), then a short Lua script, and `WATCH` only when few clients share a key. These are 1,000 updates to one key with 25 clients:

| Method | Stock Redis | Upstash |
| --- | --- | --- |
| Plain read then write | 959 updates lost, no error | 940 updates lost, no error |
| `WATCH` with retries | 1.6 s, 101 commands per update, 132 gave up | 8.1 s, 91 commands per update, 10 gave up |
| Lua script | 27 ms | 97 ms |

`WATCH` gets worse with distance, because an attempt takes three round trips. From 116 ms away, 200 updates with 25 clients took 55 s, against 1 s for Lua.

- A script blocks other commands for its whole run. On stock Redis, a 1 second script stalled another client for 1,033 ms.
- On Upstash, start scripts with `#!lua flags=allow-key-locking` so they [lock only their own keys](#on-upstash). Open source Redis and Valkey have no such flag and reject the script, so leave it off there.
- `busy-reply-threshold` (5 s by default) doesn't stop a script. Past it, other clients get `BUSY` errors, 1,124 of them during one 8 second script. After a script writes, the only way to stop it is `SHUTDOWN NOSAVE`.
- Scripts don't roll back. If one fails partway, its earlier writes stay. Check inputs first, write last, and make scripts safe to run twice.
- Never loop over an unbounded collection, and never call `KEYS` or `SCAN` or read a whole collection in a script. Don't build big tables or strings in Lua. Page with arguments from the client, and serialize on the client.
- Pass every key through `KEYS` and every value through `ARGV`. Clusters need declared keys to route the call. A body with a value baked in is a new script every call, and since Redis 7.4, `EVAL` scripts past 500 get evicted.
- Load scripts at startup with `SCRIPT LOAD`, and call `EVALSHA` with an `EVAL` fallback for `NOSCRIPT`.
- Don't wrap a script in `MULTI`. A script is already atomic.
- Lock with `SET key token NX PX ttl`, and release with a script that checks the token. Always set a TTL on the lock. On Redis 8.4 and later, `DELEX key IFEQ token` releases without a script.

Details and numbers: [Why Lua Scripts Beat WATCH When Many Clients Update One Redis Key](https://upstash.com/kb/redis-watch-vs-lua)

## Connections and clients

- Reuse connections. We measured 0.7 ms per `GET` on a reused TLS connection and 7.8 ms with a new one each time. AWS measured [0.21 ms against 2.82 ms](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/BestPractices.Clients.Redis.Connections.html). We saw databases at 112 K connections a day with 9 commands each.
- In serverless, create one client at module level and reuse it across warm invocations, or use an HTTP client. Don't subscribe from a function.
- Keep idle connections alive with keep-alive pings, and retry once on `ECONNRESET`. Proxies and load balancers close idle sockets.
- Size pools against `maxclients` (10,000 by default): pool size times processes times regions, before the next scale-out.
- Reconnect with backoff and jitter. A whole fleet reconnecting at once can take the server to 100% CPU.
- Limit client-side concurrency. A fan-out of ten thousand promises becomes ten thousand connections or queued requests.
- Set explicit timeouts and a retry budget. Retry only idempotent writes, since `INCR`, `LPUSH` and most scripts aren't safe to replay.
- Put the database where the clients are. Every request pays the distance, as the first table shows. Use a read replica near read-heavy fleets.
- Don't read back from a replica what you just wrote, unless you handle staleness.
- Pace bulk writes with smaller batches and client-side rate limits. A burst of big values can overflow the replication backlog (1 MB by default) and force full resyncs.
- Keep client libraries and runtimes current, and set `CLIENT SETINFO` per service, so the server can say which fleet did it.

## Security and operations

- Use one ACL user per service, with key-prefix patterns and the smallest command set, plus `-@dangerous`. Don't run production on the default user. Use ACLs in place of the deprecated `rename-command`.
- Rotate credentials by adding a user, switching, then deleting the old one. We found a database receiving 5,700 failed `AUTH` a day from a deployment nobody remembered.
- Keep secrets in a secret manager, and use `rediss://` with TLS on.
- Keep the server patched. CVE-2025-49844 is a CVSS 10.0 flaw in Lua that any authenticated user can reach.
- Delete what you don't use. Idle databases and read regions serving zero commands still bill.

Watch five numbers. Every incident behind these rules was visible in one of them a week ahead:

| Number | Where to read it on stock Redis |
| --- | --- |
| Miss rate | `keyspace_hits`, `keyspace_misses` in `INFO` |
| Slow commands and command mix | `SLOWLOG` (over 10 ms by default, excludes network time), `INFO commandstats`, `LATENCY DOCTOR` (monitor is off by default) |
| Memory against the limit | `used_memory`, `maxmemory`, `evicted_keys` |
| Connections against the limit | `connected_clients`, `rejected_connections` |
| Replication and write latency | `sync_full`, replica offsets, the client's write latency tail |

## Common errors

| Error | Meaning | Fix |
| --- | --- | --- |
| `OOM command not allowed when used memory > 'maxmemory'` | The database is at its memory limit, with `noeviction` or nothing it can evict | Add TTLs, choose an eviction policy, or raise the limit |
| `BUSY Redis is busy running a script` | A script ran past `busy-reply-threshold` | `SCRIPT KILL` if it hasn't written, then shorten the script |
| `NOSCRIPT No matching script` | The script isn't in the server's cache | Fall back to `EVAL` |
| `CROSSSLOT Keys in request don't hash to the same slot` | A multi-key command spans cluster slots | Use hash tags, or split the call |
| `ERR Unexpected flag in script shebang: allow-key-locking` | The flag only exists on Upstash, and this is open source Redis or Valkey | Remove the flag on this server |
| `EXECABORT` | A queued command was invalid, so the transaction was discarded | Fix the command and retry |

## On Upstash

Upstash runs its own engine: disk-backed, with per-key locks. A slow command usually stalls only its own key, and limits turn many stalls into errors. If Upstash MCP tools are available, read the database's stats and command mix through them first.

- **Billing:** on Pay as You Go, a pipeline of N bills N, a transaction N + 2, `MGET` 1, and a script 1 plus 1 per `redis.call`. An aborted `EXEC` still bills.
- **Rate:** most plans allow 10,000 commands per second, so reading 100,000 keys took 9.4 s with a pipeline and 528 ms with `MGET` in chunks.
- **Size:** one request or reply is limited to 10 MB on Free and Pay as You Go. `HGETALL` failed past about 200,000 small fields, and `LRANGE 0 -1` at 14 MB.
- **Eviction:** off by default, with one policy, `optimistic-volatile`, which samples at random and prefers keys with a TTL.
- **`KEYS`:** fails above about 5,000 results, and for any pattern once the database holds about 100,000 keys, so code that passed in testing can break in production.
- **`SCAN`:** a fixed prefix found 100 keys among 1 million in 1 page and 2 ms, while a leading wildcard took 93 pages and 607 ms. `COUNT` above 1,000 had no effect.
- **`XRANGE key - +`:** returns at most 1,000 entries with no error.
- **Streams:** a consumer that never acknowledged stopped at 900 pending entries, with a limit of 1,000.
- **Big keys:** a plain `HLEN` on a 1 million field hash took 566 ms once on Pay as You Go, and 9.4 s repeatedly on a free database with 64 MB of memory. Clients of that key wait, while unrelated keys stay at about 1 ms. One `HSCAN` page cost 276 ms at that size, so split instead of paging. `DEL` and `UNLINK` both returned in 0.9 ms.
- **Scripts:** a script takes a global lock by default, so scripts can't scale: back-to-back scripts of 50 ms cut an unrelated client's throughput by 87%. Write every script for key-based locking whenever you can, by starting it with `#!lua flags=allow-key-locking` and passing every key through `KEYS`. It then locks only those keys, and the same client lost 13%. `@upstash/ratelimit` runs its scripts this way since 2.1. It made no difference on a free database. Inside `MULTI`, a script always takes the global lock.
- **Script limit:** scripts were killed at about 250 ms, with or without the flag, and writes made before the kill stay. `createScript` in `@upstash/redis` handles the `EVALSHA` fallback.
- **`WATCH`:** needs TCP, since the REST API doesn't support it.
- **SDK:** `@upstash/redis` uses HTTP, so it needs no pool. Use 1.38.4 or later for `readYourWrites`.
- **Monitoring:** there is no `SLOWLOG`, so use the console and Prometheus metrics. `INFO` counters are per replica.

| Error | Meaning | Fix |
| --- | --- | --- |
| `ERR max request size exceeded` | One command or reply is over the plan's limit | Chunk it, or read in pages |
| `ERR max requests limit exceeded` | The monthly command quota ran out, and the server closes the connection partway through a pipeline | Send fewer commands, or upgrade |
| `ERR too many keys to fetch, please use SCAN` | `KEYS` matched more than about 5,000 keys | `SCAN` |
| `ERR KEYS command is disabled because total number of keys is too large` | The database holds about 100,000 keys or more | `SCAN` or an index set |
| `ERR Error running script: execution timed out` | The script ran past the time limit, and its earlier writes stay | Shorten it, and run many short calls |
| `ERR Dynamic keys are not allowed in Lua scripts` | A script with `allow-key-locking` touched a key it didn't declare | Pass the key through `KEYS` |
| `ERR XReadGroup is cancelled` | The consumer's pending list is near the limit of 1,000 | `XACK`, and read fewer at a time |
