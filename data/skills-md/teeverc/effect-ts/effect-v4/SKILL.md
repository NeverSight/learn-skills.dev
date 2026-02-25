---
name: effect-v4
description: "Effect v4 (beta) development and v3 → v4 migration guidance. Use when building new Effect v4 code or upgrading from v3, including API renames, behavior changes, before/after examples, and v4-specific patterns for services, layers, generators, yieldable, error handling, and schema codecs."
---

# Effect v4 (Beta) - Development & Migration

## Overview

Comprehensive guidance for Effect v4 development and migration from v3. This skill provides:

1. **v4 Core Patterns** - Guide to building new v4 code with ServiceMap, layers, generators, schema codecs
2. **v3 → v4 Migration** - Step-by-step migration guidance with API renames, behavior changes, and before/after examples

**Status:** Effect v4 is beta software under active development in [effect-smol](https://github.com/Effect-TS/effect-smol). The core programming model is stable, but `effect/unstable/*` modules may receive breaking changes in minor releases. For production use, review official v4 beta guidance and stability notes.

All bundled migration guides are sourced from the official effect-smol migration documentation.

## Quick Triage

### Building v4 Code

- Core Effect types and combinators (Result, Option, Chunk, Duration): `references/core-usage.md`
- Broader data types (DateTime, BigDecimal, HashSet, Redacted): `references/data-types-advanced.md`
- Equality, Order, Hash, Equivalence semantics: `references/behavior-traits.md`
- Expected errors vs defects, `catch*` combinators: `references/error-management.md`
- Sandboxing, Cause inspection, `catchCause`: `references/error-tooling.md`
- Exit and Cause structure, result inspection: `references/exit-cause.md`
- Services and dependency injection (ServiceMap, layers): `references/dependency-management.md`
- Layer construction, memoization, `{ local: true }`: `references/layer-patterns.md`
- Resource lifecycles, Scope, `acquireRelease`: `references/resource-management.md`
- Running effects, `Runtime` removal, run boundaries: `references/runtime-execution.md`
- Fibers, `forkChild`, `forkDetach`, fork options: `references/concurrency.md`
- References (replaces FiberRef), `ServiceMap.Reference`: `references/concurrency-advanced.md`
- Schedules, repetition, spaced/fixed/exponential: `references/scheduling.md`
- Retries, backoff, schedule composition: `references/scheduling-retry.md`
- Streams, queues, PubSub, STM: `references/streams-queues-stm.md`
- HTTP clients and external APIs: `references/http-client.md`
- HTTP servers and API definitions: `references/http-server.md`
- Request batching and data loaders: `references/request-resolver.md`
- Caching and memoization: `references/caching.md`
- Configuration and config providers: `references/configuration.md`
- Advanced config, redaction: `references/configuration-advanced.md`
- Logs, metrics, tracing: `references/observability.md`
- Logger/metrics/tracing setups and exporters: `references/observability-examples.md`
- Wiring log/metric/trace layers: `references/observability-wiring.md`
- Sequential workflows and yieldable patterns: `references/generators.md`
- Schema validation, parsing, encoding (codecs): `references/schema.md`
- Stream consumption with reducers (Sink): `references/sink.md`
- Deterministic time in tests (TestClock): `references/testing.md`
- Broader testing services and test layers: `references/testing-stack.md`
- Command, FileSystem, Path, Terminal, KeyValueStore: `references/platform-primitives.md`
- LLM workflows, planning, tool use via Effect AI: `references/ai.md`
- Bundle-size constrained runtimes (Micro): `references/micro.md`
- Migrating from Promise/async: `references/migration-async.md`
- Common pitfalls and runtime errors: `references/troubleshooting.md`
- Docs-to-guide map from `llms.txt`: `references/docs-index.md`

### Migrating from v3

- Full migration overview, quick-reference table, ordered checklist: `references/migration.md`
- Runtime and run functions: `references/migration/runtime.md`
- Error handling and error channel changes: `references/migration/error-handling.md`
- Cause flattening and new structure: `references/migration/cause.md`
- Services and environment changes (Context.Tag → ServiceMap.Service): `references/migration/services.md`
- Fiber references and context locals: `references/migration/fiberref.md`
- Forking and fiber APIs (fork → forkChild, etc.): `references/migration/forking.md`
- Fiber keep-alive behavior changes: `references/migration/fiber-keep-alive.md`
- Scope and resource lifecycle patterns: `references/migration/scope.md`
- Layer memoization and Layer.fresh: `references/migration/layer-memoization.md`
- Generator and Effect.gen changes: `references/migration/generators.md`
- Yieldable protocol (non-Effect yieldables): `references/migration/yieldable.md`
- Equality and structural comparison: `references/migration/equality.md`

## Workflow

1. Ask which v3 APIs or files are in scope and which failures or regressions to avoid.
2. Open only the relevant migration notes from `references/migration/`.
3. Produce a mapping of v3 to v4 APIs, including before/after code snippets.
4. Call out behavior changes, edge cases, and test updates needed.
5. Provide a short, ordered migration checklist tailored to the code in question.

## Example Requests

- "Migrate this v3 `Runtime` usage to v4 and explain the new run functions."
- "Update our v3 error handling to v4 and show before/after examples."
- "We use FiberRefs and forking; what needs to change in v4?"
- "Explain the generator/yieldable changes and update this Effect.gen usage."
- "Do we need to change any Scope or Layer memoization behavior in v4?"

## References - v4 Core

Comprehensive v4-specific guides (all updated for v4 APIs, no deprecated patterns):

- `references/core-usage.md` - Core Effect types and combinators (Result, Option, Chunk)
- `references/data-types-advanced.md` - DateTime, BigDecimal, HashSet, Redacted
- `references/behavior-traits.md` - Structural equality by default, Equal, Order, Hash
- `references/error-management.md` - `catch*` renames, `catchReason`, `catchEager`
- `references/error-tooling.md` - `catchCause`, sandboxing, Cause inspection
- `references/exit-cause.md` - Flattened Cause structure, Reason iteration
- `references/dependency-management.md` - ServiceMap, services, layers
- `references/layer-patterns.md` - Cross-provide memoization, `{ local: true }`
- `references/resource-management.md` - `Scope.provide` (was `Scope.extend`)
- `references/runtime-execution.md` - `Runtime<R>` removed, run* at the edge
- `references/concurrency.md` - `forkChild`/`forkDetach`, fork options, keep-alive
- `references/concurrency-advanced.md` - `ServiceMap.Reference` (was `FiberRef`)
- `references/scheduling.md` - Schedules and repetition
- `references/scheduling-retry.md` - Retries and backoff
- `references/streams-queues-stm.md` - Streams, queues, PubSub, STM
- `references/http-client.md` - HTTP clients
- `references/http-server.md` - HTTP servers
- `references/request-resolver.md` - Request batching
- `references/caching.md` - Caching and memoization
- `references/configuration.md` - Configuration
- `references/configuration-advanced.md` - Advanced config, redaction
- `references/observability.md` - Logs, metrics, tracing
- `references/observability-examples.md` - Concrete logger/metrics/tracing setups
- `references/observability-wiring.md` - Wiring observability layers
- `references/generators.md` - Effect.gen and yieldable patterns
- `references/schema.md` - Schema codecs (decode/encode)
- `references/sink.md` - Stream consumption with Sink
- `references/testing.md` - TestClock and deterministic time
- `references/testing-stack.md` - Test layer composition
- `references/platform-primitives.md` - Command, FileSystem, Path, Terminal
- `references/ai.md` - LLM workflows via Effect AI
- `references/micro.md` - Bundle-size constrained runtimes
- `references/migration-async.md` - Migrating from Promise/async
- `references/troubleshooting.md` - Common pitfalls
- `references/versioning.md` - Version guidance
- `references/docs-index.md` - Docs-to-guide routing map

## References - v3 → v4 Migration

- `references/migration.md` - **Start here**: full overview, quick-reference table, ordered checklist
- `references/migration/cause.md` - Cause flattening and structure
- `references/migration/equality.md` - Equality and comparison changes
- `references/migration/error-handling.md` - Error channel and catch* renames
- `references/migration/fiber-keep-alive.md` - Fiber lifecycle changes
- `references/migration/fiberref.md` - FiberRef and References changes
- `references/migration/forking.md` - Fork, forkChild, forkDetach changes
- `references/migration/generators.md` - Effect.gen pattern updates
- `references/migration/layer-memoization.md` - Layer.fresh and memoization
- `references/migration/runtime.md` - Runtime and run* functions
- `references/migration/scope.md` - Scope and resource lifecycle
- `references/migration/services.md` - Context.Tag → ServiceMap.Service
- `references/migration/yieldable.md` - Yieldable protocol changes
