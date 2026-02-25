---
name: go-write
description: Patterns and conventions for writing Go code. Covers API design, error handling, concurrency, interfaces, safety, performance, naming, testing, functional options, logging, and deterministic simulation testing.
---

# Go — Writing

## Core Principles

- **APIs are forever.** Exported symbols, function signatures, and interface methods cannot change without breaking callers.
- **Consistency over cleverness.** Follow established patterns even when a "smarter" approach exists.
- **Safety by default.** Prefer defensive copies, zero-value safety, and compile-time checks.
- **Handle errors exactly once.** Either log or return — never both.

## Reference Index

| Reference | Topics |
|-----------|--------|
| [api-design](references/api-design.md) | Export permanence, signature immutability, parameter objects, result objects |
| [errors](references/errors.md) | Handle-once, sentinel/structured/opaque strategy, wrapping, naming |
| [interfaces](references/interfaces.md) | Small interfaces, compile-time checks, consumer-side, upcasting, driver pattern |
| [concurrency](references/concurrency.md) | Mutex placement, channel sizing, goroutine lifecycle, context cancellation |
| [worker-pools](references/worker-pools.md) | Channel-based pools, context cancellation, WaitGroup shutdown |
| [safety](references/safety.md) | Defer cleanup, type assertions, no panic, copy at boundaries |
| [performance](references/performance.md) | `strconv` over `fmt`, pre-allocation, `strings.Builder` |
| [naming](references/naming.md) | Package naming, unexported global prefix, import aliases, receiver names |
| [declarations](references/declarations.md) | Short declarations, nil slices, zero-value structs, field names |
| [organization](references/organization.md) | Import grouping, function ordering, early returns, line length |
| [testing](references/testing.md) | Table-driven tests, subtests, `testify`, `go.uber.org/goleak` |
| [functional-options](references/functional-options.md) | Option interface, `apply` method, `WithX` constructors |
| [logging](references/logging.md) | slog handlers, typed attributes, LogValuer, context integration, log levels |
| [deterministic-simulation-testing](references/deterministic-simulation-testing.md) | `TimeNow` function type, seeded `*rand.Rand`, `fs.FS`, seed reproducibility |

## When to Apply

Apply when:
- Writing new Go code
- Refactoring existing Go code
- Generating Go tests

Do NOT apply to non-Go files (Dockerfiles, YAML, Makefiles, etc.).

## Quick Reference

**Errors**: Wrap with `fmt.Errorf("op: %w", err)`. Lowercase, no "failed to". Handle once. Sentinel (`ErrX`) for identity checks, structured (`XError`) for data, opaque `%w` for propagation.

**Interfaces**: Keep to 1-3 methods. Verify with `var _ I = (*T)(nil)`. Define at consumer. Driver pattern for extensibility.

**Concurrency**: Mutex as unexported field above guarded fields. Channels: size 0 or 1. Every goroutine needs stop signal + wait mechanism.

**Safety**: Two-value type assertions. Defer after acquire. No panic in libraries. Copy slices/maps at boundaries.

**Performance**: `strconv` > `fmt.Sprint`. Pre-allocate: `make([]T, 0, n)`. `strings.Builder` for concatenation.

**Style**: `:=` for locals. Named struct fields. Imports: stdlib → external. Early returns. ~99 char lines.

**Testing**: Table-driven `[]struct` with `t.Run`. `require` for preconditions, `assert` for checks.

**Options**: `Option` interface with `apply(*options)`. `WithX` constructors. Defaults in constructor.

**Logging**: Use `log/slog` with typed attributes (`slog.String`, `slog.Int`). `JSONHandler` in production, `TextHandler` in dev. Accept `*slog.Logger` as dependency. Implement `LogValuer` for sensitive types. Static messages, variable data in attributes.

**DST**: Inject non-deterministic sources via function types (`TimeNow`) and struct fields (`*rand.Rand`). Use `fs.FS` for I/O. Log seeds. Sort map iterations. Assert invariants. Match abstraction to need.
