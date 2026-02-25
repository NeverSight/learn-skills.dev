---
name: go-lib-design
description: Designing Go libraries and packages for long-term evolution. Covers API surface management, dependency direction, backwards compatibility, trade-offs between parameter objects and functional options, and testability via deterministic simulation.
---

# Go Library Design

## Core Principles

- **Work backwards from usage.** Write pseudo-code and documentation before implementation. Design the API you want callers to see, then build it.
- **Minimize surface area.** Smaller API = more internal freedom. When in doubt, leave it out. You can always export later; you can never unexport.
- **Accept, don't instantiate.** Take dependencies as arguments (preferably interfaces). Never instantiate what you don't own.
- **Plan for growth.** Signatures are frozen at v1.0. Use parameter objects, result objects, or functional options so APIs can evolve without breaking callers.

## Reference Index

| Reference | Topics |
|-----------|--------|
| [design-process](references/design-process.md) | Four design axes, work backwards, minimize surface area |
| [surface-area](references/surface-area.md) | Internal packages, no global state, unknown outputs, mutation guards |
| [dependencies](references/dependencies.md) | Accept don't instantiate, accept interfaces, return structs |
| [evolution](references/evolution.md) | Breaking changes, param objects vs functional options, result objects |
| [testability](references/testability.md) | `TimeNow` function type, `*rand.Rand` injection, `WithX` options, deterministic outputs, DST readiness |

## When to Apply

Apply when:
- Designing a new Go library or shared package
- Reviewing a library's public API before v1.0
- Deciding between functional options and parameter objects
- Auditing a package's export surface

Do NOT apply to application-level code that won't be imported by other modules.

## Quick Reference

**Design process**: Write usage pseudo-code first. Optimize for usability, readability, flexibility, testability — in that order.

**Surface area**: Export only what you'll support forever. Use `internal/` for non-public helpers. No global state — use struct methods.

**Dependencies**: Accept `io.Reader`, not `*os.File`. Accept interfaces, return structs. Provide convenience constructors (`NewFromFile`) as wrappers.

**Evolution**: Cannot add params (use param objects), cannot add returns (use result objects), cannot add interface methods (use upcasting). Functional options for optional-only params with few required args; param objects when there are required fields or many options.

**Naming**: No `FooManager` — find the real noun. No `util`/`common`/`helpers` packages. Qualify short generic names with parent (`httptest`, not `test`).

**Docs**: Write for users, not maintainers. Don't bury the lede. Provide runnable examples. Keep a changelog separate from commit log.

**Testability**: Accept `TimeNow` function type and `*rand.Rand` via `WithX` options with real defaults. Use `fs.FS` for I/O. No global state. Deterministic output ordering. Match abstraction to need — function types over interfaces. Simulation is opt-in.
