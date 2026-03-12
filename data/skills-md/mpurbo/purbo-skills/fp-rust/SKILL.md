---
name: fp-rust
description: >
  Functional Programming in Rust — opinionated guidelines for writing idiomatic,
  FP-first Rust code. Use this skill whenever writing, reviewing, refactoring,
  or scaffolding Rust code. Covers: functional core / imperative shell architecture,
  immutability-first patterns, pure functions, algebraic data types, pipeline-oriented
  programming with iterators and Result chains, error handling as data, dependency
  rejection over dependency injection, type-driven design (parse don't validate,
  typestate), and concurrency via message passing. Also use when the user asks about
  Rust project structure, Rust error handling patterns, Rust iterator pipelines,
  Cargo.toml setup for a new Rust project, or Rust code review. Apply these guidelines
  even when the user doesn't explicitly mention "functional programming" — this is the
  default coding style for all Rust work.
---

# Functional Rust Skill

Write Rust that is idiomatic, readable, and practical while maximizing FP principles.
Rust is not Haskell — ownership IS the type-level effect system. Let FP emerge
naturally from Rust's idioms: ownership, borrowing, iterators, enums, and traits.

For detailed patterns, code examples, library guidance, and rationale, read the
companion reference:
`cat ${SKILL_PATH}/references/FP_RUST_GUIDELINES.md`

Load the reference when you need: specific code examples for a pattern, library
selection guidance (Appendix A/C), Clippy configuration (Appendix D), or the
FP ↔ Rust concept map (Appendix B).

---

## Core Architecture: Functional Core, Imperative Shell

Every program is a pure core surrounded by a thin imperative shell.

**Core** (in `src/core/`):
- Never performs IO, reads clock, or logs
- Receives data, returns data (or `Result`/`Option` as decisions)
- Tested with pure unit tests — no mocks needed

**Shell** (in `src/shell/` and `src/main.rs`):
- Reads, writes, logs, calls core's pure functions
- Interprets core's decisions into effects
- Tested with integration tests

**Litmus test:** If `core/` imports `std::io` or `tokio`, it belongs in `shell/`.

```
src/
├── main.rs              # Shell: wiring, IO, entry point
├── shell/               # Adapters: HTTP, DB, FS, CLI
├── core/                # Pure domain logic — NO std::fs, NO tokio
│   ├── types.rs         # ADTs, newtypes, domain models
│   ├── transform.rs     # Pure transformations
│   └── validate.rs      # Validation combinators
└── lib.rs               # Re-exports core
```

---

## The Seven Principles

Apply these in order of priority when writing or reviewing Rust code:

### 1. Borrow > Clone > Mutate

- Borrow (`&T`) for reads — zero cost, pure
- Clone/Copy for transformations — create new values
- Mutate (`&mut T`) only as last resort, encapsulated

Pass Copy types (`i32`, `bool`, `f64`, `Duration`) by value, not reference.
Accept `&str` over `String`, `&[T]` over `Vec<T>` in parameters.
Defer `.to_string()`, `.collect()` until the last possible moment.

### 2. Pure Functions

A function is pure if: same inputs → same output, no side effects.
When a function needs something impure (time, random), inject it as a parameter:

```rust
// ❌ fn is_expired(token: &Token) -> bool { token.expires_at < SystemTime::now() }
// ✅ fn is_expired(token: &Token, now: SystemTime) -> bool { token.expires_at < now }
```

The signature tells the full story: no `&mut self`, no `&dyn SomeService`, no global state.

### 3. Algebraic Data Types

- Use `enum` (sum types) to model possibilities — not flag fields or stringly-typed status
- Use `struct` (product types) with private fields and constructors
- Wrap primitives in newtypes: `struct UserId(Uuid)`, `struct Amount(Decimal)`
- Match exhaustively — avoid `_ =>` that silently swallows future variants
- Make illegal states unrepresentable via typestate pattern

### 4. Pipeline-Oriented Programming

Default to iterator chains (`.iter().map().filter().collect()`), not `for` loops.
Use `?` operator and `.and_then()` for Result chains (railway-oriented programming).
Return `impl Iterator<Item = T>` over `Vec<T>` when possible — defer `.collect()`.

Preference order:
```
.iter().map().filter().collect()  >  for + match (no mut)  >  for + mut accumulator
```

### 5. Errors Are Values

- Domain errors as typed enums with `thiserror`
- `anyhow::Result` in shell, typed errors in core
- Never `unwrap()`/`expect()` in core — propagate with `?`
- Never `panic!` for expected conditions
- Test both Ok and Err paths

### 6. Dependency Rejection Over Injection

Pass data in, get data out. Don't inject `&dyn Repository` — instead:
- Shell fetches data from IO
- Shell passes data to pure core function
- Core returns decisions as values (including `Vec<Command>` for effects)
- Shell interprets and executes effects

Trait abstraction only when genuinely multiple runtime backends (not "for testing").

### 7. Concurrency via Message Passing

- `Arc<T>` (immutable sharing) over `Arc<Mutex<T>>` (mutable sharing)
- Channels (`mpsc`, `oneshot`, `broadcast`) for coordination
- `rayon::par_iter()` for CPU-bound parallel computation
- Keep async in the shell; core stays sync and pure

---

## Decision Checklist

Run through when writing or reviewing any function:

1. **IO/clock/randomness?** → Shell. Inject data, not services.
2. **Can params be borrowed?** → `&T`, `&str`, `&[T]`. Copy types by value.
3. **Uses `mut`?** → Replace with transform/fold/map. If needed, encapsulate.
4. **Uses `unwrap()`?** → Only in shell/test/provably safe.
5. **Types tight enough?** → `String` → newtype? `Option` → separate type? `bool` → enum?
6. **Data pipeline?** → `.iter()` chains or `.and_then()`. Defer `.collect()`.
7. **Dependency needed?** → Reject it. Pass data, not services.
8. **Error handling complete?** → Typed enums, exhaustive match, both paths tested.
9. **Documented?** → `///` on public items, comments explain "why" not "what".

---

## `mut` Concession Litmus Test

Before using `mut` in core code:

1. Can I restructure to avoid it?
2. Is the mutation encapsulated (invisible to caller)?
3. Does the function remain deterministic from caller's perspective?

Acceptable concessions: performance-critical inner loops (with profiling evidence),
builder patterns (produced value is immutable), complex fold readability,
`OnceCell`/`LazyLock` for memoization, `tracing` for diagnostics only.

---

## Key Pattern: `fn(mut self) -> Self`

This is NOT impure mutation — it's a value-to-value transform where Rust reuses
memory. The caller passes ownership in and gets a new value out:

```rust
fn with_discount(mut order: Order, pct: f64) -> Order {
    order.total *= 1.0 - pct;
    order
}
```

Don't clone the world just to "look functional."

---

## Crate Stack (Always Include)

```toml
[dependencies]
itertools = "0.14"       # Extended pipeline combinators
tap = "1"                # .pipe() and .tap() for pipeline readability
derive_more = { version = "1", features = ["full"] }  # Newtype ergonomics
thiserror = "2"          # Domain error enums
serde = { version = "1", features = ["derive"] }
rust_decimal = "1"       # Financial math (no floats)
anyhow = "1"             # Shell error handling
tokio = { version = "1", features = ["full"] }  # Shell async runtime
tracing = "0.1"          # Structured logging
```

For library evaluation, conditional crates (frunk, imbl, rayon, proptest), Clippy
configuration, and the full FP ↔ Rust concept map, consult the reference document.

---

## When Reviewing Code

Flag these patterns and suggest FP alternatives:

| Smell | Suggest |
|-------|---------|
| `let mut` for accumulation | `.fold()` or `.map().collect()` |
| `for` loop pushing into Vec | Iterator pipeline |
| `&dyn Trait` in core for testability | Dependency rejection |
| `unwrap()` in core/library code | `?` or explicit error handling |
| String/bool for domain states | Enum (sum type) or newtype |
| `Arc<Mutex<T>>` | Channels or `Arc<T>` immutable snapshot |
| IO in core functions | Move to shell, pass data in |
| `_ =>` catch-all in match | Exhaustive match with explicit variants |
| Nested if-let for Option/Result | `.map()`, `.and_then()`, `?` pipeline |
| `.clone()` to satisfy borrow checker | Restructure lifetimes, or use `&T` |
