---
name: rust
description: >
  Guide for writing idiomatic Rust code, based on Apollo GraphQL's best practices handbook plus async patterns for Tokio. Use this skill when:
  (1) writing new Rust code or functions,
  (2) reviewing or refactoring existing Rust code,
  (3) deciding between borrowing vs cloning or ownership patterns,
  (4) implementing error handling with Result types,
  (5) optimizing Rust code for performance,
  (6) writing tests or documentation for Rust projects,
  (7) writing async Rust with Tokio - tasks, channels, streams, async traits, graceful shutdown,
  (8) debugging async code: deadlocks, blocked runtimes, cancellation, Send bounds.
license: MIT
compatibility: Rust 1.70+ (1.75+ for async fn in traits), Cargo
allowed-tools: Bash(cargo:*) Bash(rustc:*) Bash(rustfmt:*) Bash(clippy:*) Read Write Edit Glob Grep
---

# Rust Best Practices

Apply these guidelines when writing or reviewing Rust code. 

## Best Practices Reference

Before reviewing, familiarize yourself with the relevant chapters. Read ALL relevant chapters in the same turn in parallel. Reference these files when providing feedback:

- [Chapter 1 - Coding Styles and Idioms](references/chapter_01.md): Borrowing vs cloning, Copy trait, Option/Result handling, iterators, import ordering, when to extract a function (duplication vs. wrong abstraction)
- [Chapter 2 - Clippy and Linting](references/chapter_02.md): Clippy configuration, important lints, workspace lint setup
- [Chapter 3 - Performance Mindset](references/chapter_03.md): Profiling, avoiding redundant clones, stack vs heap, zero-cost abstractions
- [Chapter 4 - Error Handling](references/chapter_04.md): Result vs panic, thiserror vs anyhow, error hierarchies
- [Chapter 5 - Automated Testing](references/chapter_05.md): Test naming, one assertion per test, snapshot testing
- [Chapter 6 - Generics and Dispatch](references/chapter_06.md): Static vs dynamic dispatch, trait objects, dyn compatibility
- [Chapter 7 - Type State Pattern](references/chapter_07.md): Compile-time state safety, when to use it
- [Chapter 8 - Comments vs Documentation](references/chapter_08.md): When to comment, `SAFETY:`/`CONTEXT:` prefixes, TODOs as issues, doc comments, rustdoc
- [Chapter 9 - Understanding Pointers](references/chapter_09.md): Thread safety, Send/Sync, pointer types
- [Chapter 10 - Async Patterns with Tokio](references/chapter_10.md): Execution model, JoinSet, channels, streams, async traits, graceful shutdown, async debugging

## Quick Reference

### Borrowing & Ownership
- Prefer `&T` over `.clone()` unless ownership transfer is required
- Use `&str` over `String`, `&[T]` over `Vec<T>` in function parameters
- Small `Copy` types (≤24 bytes) can be passed by value
- Use `Cow<'_, T>` when ownership is ambiguous

### Error Handling
- Return `Result<T, E>` for fallible operations; avoid `panic!` in production
- Never use `unwrap()`/`expect()` outside tests
- Use `thiserror` for library errors, `anyhow` for binaries only
- Prefer `?` operator over match chains for error propagation

### Performance
- Always benchmark with `--release` flag
- Run `cargo clippy -- -D clippy::perf` for performance hints
- Avoid cloning in loops; use `.iter()` instead of `.into_iter()` for Copy types
- Prefer iterators over manual loops; avoid intermediate `.collect()` calls

### Linting
Run regularly: `cargo clippy --all-targets --all-features --locked -- -D warnings`

Key lints to watch:
- `redundant_clone` - unnecessary cloning
- `large_enum_variant` - oversized variants (consider boxing)
- `needless_collect` - premature collection

Use `#[expect(clippy::lint)]` over `#[allow(...)]` with justification comment.

### Testing
- Name tests descriptively: `process_should_return_error_when_input_empty()`
- One assertion per test when possible
- Use doc tests (`///`) for public API examples
- Consider `cargo insta` for snapshot testing generated output

### Generics & Dispatch
- Prefer generics (static dispatch) for performance-critical code
- Use `dyn Trait` only when heterogeneous collections are needed
- Box at API boundaries, not internally

### Type State Pattern
Encode valid states in the type system to catch invalid operations at compile time:
```rust
struct Connection<State> { /* ... */ _state: PhantomData<State> }
struct Disconnected;
struct Connected;

impl Connection<Connected> {
    fn send(&self, data: &[u8]) { /* only connected can send */ }
}
```

### Async (Tokio)
- Never block an async thread: no `std::thread::sleep`, blocking I/O or heavy CPU work in `async fn` - use `spawn_blocking`
- Never hold a lock across `.await`; `std::sync::Mutex` is cheaper unless the guard must cross one
- Bound concurrency with `buffer_unordered`/`Semaphore`; use `JoinSet` to own and abort task groups
- Prefer channels over shared state - `mpsc` (work queue), `broadcast` (fan-out), `oneshot` (reply), `watch` (latest value)
- Put a timeout on every outbound call; handle shutdown via `CancellationToken`
- `async fn` in traits (1.75+) for static dispatch; `#[async_trait]` only when you need `dyn Trait`
- Instrument with `tracing`: `#[instrument]` on async fns, `.instrument(span)` on spawned tasks

### Documentation
- `//` comments explain *why* (safety, workarounds, design rationale)
- `///` doc comments explain *what* and *how* for public APIs
- Every `TODO` needs a linked issue: `// TODO(#42): ...`
- Enable `#![deny(missing_docs)]` for libraries
