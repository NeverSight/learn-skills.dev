---
name: rust
description: >
  Mental-model reset for Rust. Use when writing or reviewing Rust code to shift
  from "it compiles" to "thinks in Rust." Triggers on Rust code review,
  "is this idiomatic", borrow-checker errors, API design, domain modeling,
  ownership, lifetimes, errors, traits, async/Tokio, unsafe, serde, FFI, tests,
  performance, Cargo structure, .rs files, Cargo.toml, rustc diagnostics, clippy
  findings, Result/Option, thiserror vs anyhow, newtype, typestate, enum vs
  trait, dyn Trait, Send/Sync, Pin, Miri, PyO3, napi-rs, cxx, UniFFI,
  wasm-bindgen, serde attributes, or feature unification.
---

# Thinking in Rust

You already know Rust syntax. Change the **defaults** you reach for first when modeling a domain, handling ownership, designing APIs, or crossing boundaries.

The core failure mode: writing Rust that compiles but thinks like Python, Java, TypeScript, or C. Bare `String` for domain types. `bool` for states. Trait objects for closed sets. `Error(String)` for everything. `_ =>` in every match. Index loops. Sentinel values. Getters and setters on every field. `clone()` to quiet the compiler. `unsafe` to escape design pressure. These compile. They are wrong.

Most of these habits come from languages without sum types, ownership, zero-cost newtypes, or exhaustive matching. Recognizing *where* a pattern comes from helps you see *why* it is wrong in Rust.

When reviewing Rust, start with the shape of the program: what invariants are represented, who owns each value, which states are impossible, where errors cross boundaries, and whether any escape hatch is hiding a design problem.

Treat these as strong defaults, not rigid laws: when unsure, choose the approach that moves invariants into types and lets the compiler enforce them.

## How Rust Thinks

### Model the domain in types

1. **Every string with domain meaning is a newtype.** Bare `String` erases domain knowledge. The compiler cannot distinguish an email from a username from a URL. Wrap it, validate at construction, keep the field private. See [references/newtypes-and-domain-types.md](references/newtypes-and-domain-types.md).
2. **Every boolean parameter is a lie — use an enum.** `true` and `false` carry no meaning at the call site and cannot extend to a third state. Replace flags with named variants. Applies to struct fields too: correlated booleans are a state machine in disguise. See [references/bool-to-enum.md](references/bool-to-enum.md).
3. **Every "I don't know" is explicit.** `Option<bool>` has three states but none of them are named. Empty collections can mean "checked and empty" or "not checked yet." Make each state a named variant. See [references/option-bool-to-enum.md](references/option-bool-to-enum.md).
4. **Every match on your enum is exhaustive — no wildcard `_ =>` arms.** Wildcards silence the compiler when you add variants. List every variant of enums you control. `_ =>` is for foreign `#[non_exhaustive]` types and primitives. See [references/exhaustive-matching.md](references/exhaustive-matching.md).
5. **Every error variant is a domain fact — no `Error(String)`.** String errors throw away structure. Callers cannot match, test, retry, translate, or recover. Libraries expose typed error enums; applications add context. See [error-handling.md](error-handling.md).
6. **Parse, don't validate.** Validation checks data and throws away the proof. Parsing checks data and returns a type that proves the invariant. After parsing, do not re-check downstream. See [references/parse-dont-validate.md](references/parse-dont-validate.md).
7. **Enums are the primary modeling tool.** Rust enums are sum types. A struct with a `kind` field plus `Option` payload fields is always an enum waiting to be written. See [references/enums-as-modeling-tool.md](references/enums-as-modeling-tool.md).
8. **Closed sets are enums, not trait objects.** If you know all variants at compile time, use an enum: zero-cost dispatch, exhaustive matching, per-variant data. Use generics or `dyn Trait` only when the set is genuinely open. See [traits.md](traits.md).
9. **Boundaries translate; internals model.** Serde, FFI, CLI, HTTP, and database edges should convert DTOs into domain types. Do not let wire formats become your internal model. See [serde.md](serde.md) and [interop.md](interop.md).

### Express ownership and API intent

10. **Borrow by default — own when intentional.** Accept `&str`, `&[T]`, and `&Path` unless you need to store, mutate, transform, or transfer ownership. See [references/borrow-by-default.md](references/borrow-by-default.md).
11. **Function signatures are ownership contracts.** A signature should reveal who owns, who borrows, who mutates, and how long values remain valid. If the signature lies, the borrow checker will make you pay. See [references/function-signatures.md](references/function-signatures.md).
12. **Clone is not a design tool.** Clone for independent ownership, thread transfer, or stored copies. Do not clone because E0382 made you sad. See [ownership.md](ownership.md).
13. **Restructure ownership before `Rc<RefCell<T>>`.** `RefCell` trades compile-time borrow checking for runtime panics. First try split borrows, read-then-write phases, arenas/indices, or explicit ownership flow. See [references/ownership-before-refcell.md](references/ownership-before-refcell.md).
14. **Async is for waiting, not for CPU work.** Never block the runtime. Use async I/O, `spawn_blocking` for short blocking calls, and Rayon or dedicated threads for CPU-bound work. See [async.md](async.md).
15. **Unsafe and atomics require written proofs.** Atomics need a small ordering argument. Unsafe needs the smallest safe wrapper, `# Safety` docs, `// SAFETY:` comments, and Miri when validity or aliasing matters. See [atomics.md](atomics.md) and [unsafe.md](unsafe.md).

### Express intent in APIs and control flow

16. **Iterators over index loops.** `for i in 0..v.len()` risks off-by-one errors and obscures intent. Use `.iter()`, `.enumerate()`, `.windows()`, `.zip()`, and adapters that say what you mean. See [references/iterators-over-indexing.md](references/iterators-over-indexing.md).
17. **`Option` over sentinel values.** `-1`, `""`, `0`, and `u32::MAX` as "no value" markers are invisible to the type system. Use `Option<T>`. See [references/option-over-sentinels.md](references/option-over-sentinels.md).
18. **One entity, one struct — not parallel collections.** Multiple maps or vectors sharing keys depend on discipline, not types. Group related data into a struct and store one collection of that entity. See [references/struct-collections.md](references/struct-collections.md).
19. **Transform over mutate.** For configuration and construction, prefer consuming `self` chains over `&mut self` setters. Reserve `&mut self` for live objects being operated on. See [references/transform-over-mutate.md](references/transform-over-mutate.md).
20. **Modules are namespaces, not `impl` blocks.** A unit struct with only associated functions is a Java class in disguise. Use modules for free functions; use traits when method syntax matters. See [references/impl-namespace.md](references/impl-namespace.md).
21. **Right-size pattern matching.** `matches!()` for boolean checks. `if let` for one variant. `let ... else` for early return. `match` for real alternatives. Exhaustive `match` when adding a variant should break the build. See [references/pattern-matching-tools.md](references/pattern-matching-tools.md).
22. **Public fields beat trivial getters.** If any value of a field's type is valid, make it `pub`. Do not write `get_x()`/`set_x()` that only forwards. When accessors protect invariants, use Rust naming: `name()`, not `get_name()`. See [references/getter-setter.md](references/getter-setter.md).
23. **Visibility is a design tool, not cleanup.** `pub` is a semver promise. Default to private or `pub(crate)`, group modules by domain, and curate the public facade with `pub use`. See [references/visibility-and-modules.md](references/visibility-and-modules.md).
24. **Crate boundaries must earn their names.** Stay single-crate until you can name the boundary. Cargo features are additive public capability, not an internal architecture switch. See [project-structure.md](project-structure.md).

## Common Mistakes (Agent Failure Modes)

- **Public newtype fields (`pub struct Email(pub String)`)** → Make the field private; force construction through `parse`/`new` so invariants cannot be bypassed.
- **Boolean flags leaking into APIs** → Replace with enums, even when there are only two states today.
- **`Option<bool>` or nested `Option` state** → Name the states. Stop making callers decode truth tables.
- **`kind` field plus `Option` payload fields** → Replace with an enum carrying per-variant data; delete the impossible states.
- **Wildcard matches on your own enums** → List every variant; adding a variant should break the build.
- **Validation that returns `Result<(), E>` and then forgets the proof** → Parse once at the boundary into a domain type.
- **`Error(String)` or a crate-wide error blob** → Define structured errors for one unit of fallibility.
- **`anyhow::Error` in a public library API** → Use a library error type; reserve `anyhow` for binaries/apps.
- **Bare `?` in application code** → Add `.context()` so the error says what you were doing.
- **Taking ownership by default** → Borrow unless you store, return, transform, or transfer ownership.
- **`clone()` as first response to E0382** → Ask who should own the data. Clone only when you can name why.
- **`'static` added to silence a lifetime error** → Fix the relationship between lifetimes; do not make your API less useful.
- **`&String`, `&Vec<T>`, or `&PathBuf` in APIs** → Accept `&str`, `&[T]`, or `&Path`.
- **`Rc<RefCell<T>>` or `Arc<Mutex<T>>` as first resort** → Restructure ownership or use message passing.
- **`dyn Trait` for a closed set** → Use an enum. Interfaces are not free flexibility in Rust.
- **Blocking or CPU work inside `async fn`** → Use async APIs, `spawn_blocking`, or Rayon/thread pool.
- **Holding a lock guard across `.await`** → Narrow the lock scope or redesign shared state.
- **`Ordering::Relaxed` because it is faster** → Write the proof; otherwise use Release/Acquire or `SeqCst`.
- **Unsafe to dodge the borrow checker** → The pattern is probably wrong. Restructure first.
- **`serde_json::Value` as the internal model** → Use DTOs at the boundary and domain types inside.
- **Benchmarking debug builds or optimizing cold code** → Measure `--release` first; keep invariants until profiling proves otherwise.
- **Feature flags for internal workspace architecture** → Use modules/crates; features are additive public capability.

## Review Checklist

1. **Domain primitive?** → Newtype, enum, or parser-backed type.
2. **Boolean or `Option<bool>` state?** → Named enum variants.
3. **Wildcard match on owned enum?** → Exhaustive match.
4. **Validation repeated downstream?** → Parse once at the boundary.
5. **Borrow checker appeased with `clone()`, `'static`, `Rc<RefCell<_>>`, or unsafe?** → Rework ownership first.
6. **Public signature takes owned data but only reads?** → Borrow `&str`, `&[T]`, or `&Path`.
7. **Library returns stringly or `anyhow` errors?** → Structured public error type.
8. **Polymorphism unclear?** → Enum, then generics, then `dyn` only for true erasure.
9. **Async code blocks, holds locks across `.await`, or fans out unboundedly?** → Move blocking work and bound concurrency.
10. **Unsafe or atomics present?** → Check the written invariant/proof and run Miri when relevant.
11. **Serde/FFI/API boundary leaks into internals?** → Translate DTOs into domain types.
12. **Performance concern?** → Measure `--release` before cleverness.
13. **Everything is `pub` or feature-gated internally?** → Curate the facade; keep features additive.

## Quick Reference

| Code smell | Rust default move | Reference |
|---|---|---|
| Bare `String`/`u64` for domain values | Newtype with private field | [references/newtypes-and-domain-types.md](references/newtypes-and-domain-types.md) |
| `bool` parameter or state field | Two-variant enum | [references/bool-to-enum.md](references/bool-to-enum.md) |
| `Option<bool>` / nested `Option` | Named enum variants | [references/option-bool-to-enum.md](references/option-bool-to-enum.md) |
| `_ =>` on your own enum | List every variant | [references/exhaustive-matching.md](references/exhaustive-matching.md) |
| `Error(String)` in a library | Typed error enum scoped to the operation | [error-handling.md](error-handling.md) |
| Validate then forget | Parse into a domain type | [references/parse-dont-validate.md](references/parse-dont-validate.md) |
| `kind` field + `Option` payloads | Enum with per-variant data | [references/enums-as-modeling-tool.md](references/enums-as-modeling-tool.md) |
| `Box<dyn Trait>` for a closed set | Enum, or generics if the set is open | [traits.md](traits.md) |
| Function takes `Vec<T>`/`String` but only reads | Borrow `&[T]` / `&str` | [references/borrow-by-default.md](references/borrow-by-default.md) |
| Defensive clone or lifetime fight | Redesign ownership before adding escape hatches | [ownership.md](ownership.md) |
| `for i in 0..v.len()` | Iterator chain | [references/iterators-over-indexing.md](references/iterators-over-indexing.md) |
| Magic number/string for absence | `Option<T>` | [references/option-over-sentinels.md](references/option-over-sentinels.md) |
| Parallel collections with shared keys | Single collection of structs | [references/struct-collections.md](references/struct-collections.md) |
| `&mut self` builder setters | Consuming `self` chains | [references/transform-over-mutate.md](references/transform-over-mutate.md) |
| Unit struct with only associated functions | Module with free functions | [references/impl-namespace.md](references/impl-namespace.md) |
| One meaningful `match` arm | `if let`, `let ... else`, or `matches!` | [references/pattern-matching-tools.md](references/pattern-matching-tools.md) |
| Trivial `get_x()` / `set_x()` | Public field or `x()` accessor with invariant | [references/getter-setter.md](references/getter-setter.md) |
| Everything `pub` / one giant file | Modules plus curated visibility | [references/visibility-and-modules.md](references/visibility-and-modules.md) |
| Blocking work or unbounded fan-out in async code | Async waits; CPU blocks elsewhere; bound everything | [async.md](async.md) |
| Atomic ordering chosen by vibe | Use atomics only with a written proof | [atomics.md](atomics.md) |
| Unsafe added to bypass compiler friction | Isolate unsafe and document the invariant | [unsafe.md](unsafe.md) |
| Wire format leaking into internals | Translate DTOs into domain types | [serde.md](serde.md) |
| FFI or host-runtime boundary | Keep the ABI small, typed, and panic-safe | [interop.md](interop.md) |
| Crate/workspace/API shape unclear | Stay single-crate until the boundary has a name | [project-structure.md](project-structure.md) |

## Cross-References

- **[ownership.md](ownership.md)** — Borrow checker errors, lifetimes, function signatures, smart pointers, `Cow`, clone discipline.
- **[error-handling.md](error-handling.md)** — `thiserror` vs `anyhow`, structured errors, context, combinators, panic boundaries.
- **[traits.md](traits.md)** and **[type-design.md](type-design.md)** — Dispatch choices, trait design, newtypes, typestate, builders, phantom types.
- **[async.md](async.md)**, **[atomics.md](atomics.md)**, and **[unsafe.md](unsafe.md)** — Concurrency, memory ordering, soundness, Miri, `Send`/`Sync` invariants.
- **[macros.md](macros.md)**, **[testing.md](testing.md)**, and **[performance.md](performance.md)** — Generated code, validation strategy, profiling-first optimization.
- **[serde.md](serde.md)**, **[interop.md](interop.md)**, and **[project-structure.md](project-structure.md)** — Boundaries, DTOs, FFI, workspaces, features, public API surface.
