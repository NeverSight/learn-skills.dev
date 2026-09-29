---
name: effect-ts
description: "Use when Effect services, typed errors, layers, runtimes, wrappers, streams, caching, or UI integration constrain the design."
---

# Effect TS

## Overview

Apply this modifier when Effect changes the design or review constraints. Name the active Effect boundary first, then load only the reference that governs it.

## When to Use

- Services, layers, and dependency wiring
- Typed error surfaces and runtime boundaries
- Streams, queues, concurrency, retries, and caching
- Effect wrappers around external SDKs
- Effect integration with React or Next-style UI code

## When Not to Use

- Use `engineering` as the primary skill for generic module shape or implementation
- Use `test-design` when framework-agnostic test selection is the primary task
- Route ordinary TypeScript utility work elsewhere unless Effect is central to it

## Minimal Workflow

1. Name the active Effect boundary: service, runtime, wrapper, stream, or UI integration.
2. Inspect the repository's service, layer, error, runtime, and testing conventions at that boundary.
3. Load only the references needed to settle the current design pressure.
4. Treat local examples as patterns. Verify version-sensitive APIs against the installed version and current official Effect documentation.
5. For guidance or review, state the chosen boundary, how it fits local conventions, any version assumptions, and the verification needed.
6. During implementation, apply these constraints within the primary `engineering` loop and stop only when that loop's fresh-verification condition is met.

## Reference Routing

- Read [references/CRITICAL_RULES.md](references/CRITICAL_RULES.md) for core anti-patterns and boundary rules.
- Read [references/NEXT_JS.md](references/NEXT_JS.md) for Next.js App Router integration when `@prb/effect-next` is already present or explicitly selected. This reference does not authorize adding the package.
- Read [references/STREAMS.md](references/STREAMS.md) for queues, hubs, channels, and streams.
- Read [references/TESTING.md](references/TESTING.md) for deterministic Effect testing.
- Read [references/OPTION_NULL.md](references/OPTION_NULL.md) for `Option` and `null` interop.
- Read [references/EFFECT_ATOM.md](references/EFFECT_ATOM.md) for effect-atom patterns.
- Read [references/BEST_PRACTICES/service-patterns.md](references/BEST_PRACTICES/service-patterns.md) for business services and method boundaries.
- Read [references/BEST_PRACTICES/error-patterns.md](references/BEST_PRACTICES/error-patterns.md) for typed errors and recovery semantics.
- Read [references/BEST_PRACTICES/layer-patterns.md](references/BEST_PRACTICES/layer-patterns.md) for dependency wiring, layer composition, and runtimes.
- Read [references/BEST_PRACTICES/schema-patterns.md](references/BEST_PRACTICES/schema-patterns.md) for schemas, decoding, and domain types.
- Read [references/BEST_PRACTICES/observability-patterns.md](references/BEST_PRACTICES/observability-patterns.md) for logging, tracing, metrics, and configuration.
- Read [references/BEST_PRACTICES/rpc-cluster-patterns.md](references/BEST_PRACTICES/rpc-cluster-patterns.md) for RPC, workflows, activities, and scheduled jobs.
- Read [references/BEST_PRACTICES/language-server.md](references/BEST_PRACTICES/language-server.md) for Effect language-server setup and diagnostics.
- Read [references/BEST_PRACTICES/effect-atom-patterns.md](references/BEST_PRACTICES/effect-atom-patterns.md) for advanced effect-atom caching, mutation, and resource patterns.
- Read [references/BEST_PRACTICES/anti-patterns.md](references/BEST_PRACTICES/anti-patterns.md) when reviewing Effect-specific misuse beyond the core rules.
- Read [CLIENT_WRAPPERS.md](CLIENT_WRAPPERS.md) when wrapping third-party SDKs.

## Failure modes

- Mixing incompatible service or error conventions in one codebase
- Letting wrapper code leak the raw client and bypass Effect boundaries
- Using Effect to justify unnecessary complexity in otherwise simple modules
