---
name: effect-ts
description: Review and guide Effect TypeScript best practices based on effect.solutions standards. Use when implementing Effect patterns, services, layers, error handling, data modeling, config, testing, or CLI development.
compatibility: opencode
metadata:
  source: https://www.effect.solutions/
  cli: effect-solutions
---

# Effect Expert

Use this skill when working with Effect services, layers, schema errors, config, and runtime integration.

## Load Triggers

Load this skill when:

- User mentions `Effect`, `Layer`, `Context.Tag`, `Schema.TaggedError`, `Effect.gen`, or `Effect.fn`
- You are editing service files in `packages/services/` or `agent-tools/*`
- You need test strategy for Effect code (`@effect/vitest`, test layers)
- You need Effect runtime integration (TRPC/server boundaries)

## First Step (Always)

Before implementing or reviewing, fetch current recommendations:

```bash
effect-solutions list
effect-solutions show tsconfig
effect-solutions show basics
effect-solutions show services-and-layers
effect-solutions show data-modeling
effect-solutions show error-handling
effect-solutions show config
effect-solutions show testing
effect-solutions show cli
```

Effect guidance evolves. Do not rely on stale memory.

## Decision Tree

- **Service design or refactor** -> `references/services-and-layers.md`
- **Typed errors, Option/Either, recovery** -> `references/error-handling.md`
- **TRPC/server runtime boundary** -> `references/framework-integration.md`
- **CLI tooling in `agent-tools/*`** -> `references/agent-tools-patterns.md`
- **Testing and mocks** -> `references/testing-layers.md`

## Project Rules (Do Not Break)

- Prefer service co-location (`Context.Tag` + static `layer` in one file)
- Use `Schema.TaggedError` for domain errors
- Do not access `Option`/`Either` internals via `_tag`; use helpers (`match`, `isNone`, `isLeft`)
- For Effect dependencies, mock with Layers, not `vi.mock()`
- Keep one clear provide boundary at entry points

## Output Expectations

When advising or implementing, return:

1. Which `effect-solutions show ...` topics were checked
2. Which reference file(s) were used and why
3. Concrete change proposal following existing project patterns
4. Verification plan (typecheck/tests)

## Reference Index

- `references/services-and-layers.md`
- `references/error-handling.md`
- `references/framework-integration.md`
- `references/agent-tools-patterns.md`
- `references/testing-layers.md`
