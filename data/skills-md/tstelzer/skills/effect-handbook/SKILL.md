---
name: effect-handbook
description: Canonical handbook for effect ecosystem usage in TypeScript. Always use when you interacting with effect code.
---

# Effect Handbook

## Purpose
Use this as the single source of truth for Effect-related guidance in this repository. Sections are index buckets, not a reading order.

## Routing Rules
- Do not read this handbook linearly.
- Pick one target file below.
- Follow `See also` only if that file is insufficient.
- Read exactly one: pick one target file first; only follow `See also` if needed.
- Top-level routing: intent → exact file path; sections are index buckets, not reading order.

## Quick Picks (Task -> File)
- Build a CLI command -> `sections/20-cli.md`
- Configure CLI options/flags -> `topics/cli-options.md`
- Configure CLI positional args -> `topics/cli-args.md`
- Build interactive CLI prompts -> `topics/cli-prompt.md`
- Define HTTP endpoint + handler -> `sections/30-http-server.md`
- Derive typed HTTP client -> `topics/http-derive-client.md`
- Add Swagger/OpenAPI docs -> `topics/http-swagger.md`
- Handle multipart upload -> `topics/http-multipart.md`
- Implement streaming HTTP endpoint -> `topics/http-streaming.md`
- Use FileSystem/Path/Url/Ndjson/Worker -> `sections/40-platform.md`
- NDJSON encode/decode streams -> `topics/platform-ndjson.md`
- Worker/WorkerRunner setup -> `topics/platform-worker.md`
- Run Stream into platform sink -> `topics/platform-stream-sink.md`
- Write Effect tests -> `sections/50-testing.md`
- Use @effect/vitest modes -> `topics/testing-vitest.md`
- Retry/repeat policy -> `topics/schedule-retry.md`
- Stream processing -> `topics/stream.md`
- Context/Layer wiring -> `topics/layer-context.md`
- Queue producer-consumer -> `topics/queue.md`
- HTTP middleware/auth -> `topics/http-middleware.md`
- Config/env vars -> `topics/config.md`

## By Domain
- Core (Effect type, composition, execution) -> `sections/00-foundations.md`, `sections/10-core-patterns.md`
- CLI (Command, Options, Args, Prompt) -> `sections/20-cli.md`
- HTTP (HttpApi, HttpApiBuilder, endpoints) -> `sections/30-http-server.md`
- Platform (FileSystem, Path, Url, Ndjson, workers) -> `sections/40-platform.md`
- Testing (it.effect, it.live, it.scoped, TestClock) -> `sections/50-testing.md`

## By Primitive
- `Ref`/`SynchronizedRef`/`FiberRef` -> `topics/refs.md`
- `Cause`/`Exit` -> `topics/cause-exit.md`
- `STM` -> `topics/stm.md`
- `Scope`/resource safety -> `topics/scope-resource.md`
- `Deferred` -> `topics/deferred.md`
- `Semaphore` -> `topics/semaphore.md`
- `Cache` -> `topics/cache.md`
- `Match` -> `topics/match.md`
- `Logger`/`Metric`/tracing -> `topics/observability.md`
- Concurrency/fibers/racing -> `topics/concurrency.md`
- Latch -> `topics/latch.md`
- `Stream` (async iterables, pagination) -> `topics/stream.md`
- `Schedule` (retry, repeat, backoff) -> `topics/schedule-retry.md`
- `Layer`/`Context` (dependency injection) -> `topics/layer-context.md`
- `Queue` (producer-consumer, back-pressure) -> `topics/queue.md`
- `PubSub` (broadcast to subscribers) -> `topics/pubsub.md`
- `HttpApiMiddleware` (auth, logging) -> `topics/http-middleware.md`
- `HttpApiClient` derivation -> `topics/http-derive-client.md`
- OpenAPI/Swagger -> `topics/http-swagger.md`
- Multipart -> `topics/http-multipart.md`
- HTTP streaming -> `topics/http-streaming.md`
- NDJSON -> `topics/platform-ndjson.md`
- Worker/WorkerRunner -> `topics/platform-worker.md`
- Stream + Sink integration -> `topics/platform-stream-sink.md`
- Vitest integration -> `topics/testing-vitest.md`
- `Config` (env, typed config) -> `topics/config.md`

## Section Index
- `sections/00-foundations.md` — Effect type, creation, composition, run boundaries
- `sections/10-core-patterns.md` — Layers, retries, refs, concurrency, streams
- `sections/20-cli.md` — Command, Options, Args, Prompt, subcommands
- `sections/30-http-server.md` — HttpApi, HttpApiEndpoint, HttpApiBuilder
- `sections/40-platform.md` — FileSystem, Path, Url, Ndjson, workers
- `sections/50-testing.md` — it.effect, it.live, it.scoped, TestClock

## Topic Index
- `topics/refs.md` — Ref, SynchronizedRef, FiberRef
- `topics/cause-exit.md` — Cause, Exit, failure inspection
- `topics/stm.md` — STM transactions, TRef
- `topics/scope-resource.md` — Scope, acquireUseRelease, resource safety
- `topics/deferred.md` — Deferred, one-shot signaling
- `topics/semaphore.md` — Semaphore, bounded concurrency
- `topics/cache.md` — Cache, TTL, lookup
- `topics/match.md` — Match, exhaustive pattern matching
- `topics/observability.md` — Logger, Metric, tracing
- `topics/concurrency.md` — Concurrency settings, fibers, racing, interruption
- `topics/latch.md` — Latch gating and one-way release patterns
- `topics/stream.md` — Stream creation, consumption, transformations, combining
- `topics/schedule-retry.md` — Retry/repeat with exponential, jittered, custom schedules
- `topics/layer-context.md` — Context.Tag, Layer, dependency composition
- `topics/queue.md` — Bounded/unbounded queues, offer/take, back-pressure
- `topics/pubsub.md` — Broadcast to multiple subscribers, subscribe/publish
- `topics/http-middleware.md` — HttpApiMiddleware.Tag, security, provides
- `topics/http-derive-client.md` — Typed client derivation from HttpApi
- `topics/http-swagger.md` — Swagger/OpenAPI docs and annotations
- `topics/http-multipart.md` — Multipart upload schemas
- `topics/http-streaming.md` — Streaming requests and responses
- `topics/platform-ndjson.md` — NDJSON pack/unpack and schema channels
- `topics/platform-worker.md` — Worker pools and WorkerRunner
- `topics/platform-stream-sink.md` — Stream to sink/file integration
- `topics/cli-options.md` — Full options constructors and combinators
- `topics/cli-args.md` — Full args constructors and combinators
- `topics/cli-prompt.md` — Interactive prompts and composition
- `topics/testing-vitest.md` — `it.effect`, `it.live`, `it.scoped`, `TestClock`
- `topics/config.md` — Config.string/integer, env fallback, nested config

## Conventions
- Section files: What it is | When to use | When not to use | Minimal examples | Common pitfalls | See also
- Topic files: same structure, compact (~60–120 lines)
- Paths are relative to this SKILL.md; sections and topics use relative `../` for cross-links

## When to Use This Handbook
- Implementing Effect-based services, CLIs, HTTP APIs, or tests
- Looking up primitives (Stream, Schedule, Queue, Layer, Config)
- Resolving common pitfalls (run boundaries, retry layers, auth middleware)
- Choosing between similar primitives (Queue vs PubSub, Ref vs STM)
- Debugging Effect execution (run boundaries, fiber interruption, scoped resources)

## Package References
- `effect` — core runtime
- `@effect/cli` — Command, Options, Args, Prompt
- `@effect/platform` — HttpApi, FileSystem, Path, Url
- `@effect/platform-node` — NodeContext, NodeHttpServer, NodeRuntime
- `@effect/vitest` — it.effect, it.live, it.scoped
