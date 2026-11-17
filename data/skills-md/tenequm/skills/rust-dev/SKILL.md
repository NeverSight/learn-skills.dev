---
name: rust-dev
description: Day-1 guide to building well in Rust - ownership, errors as values, String vs &str, Box/Rc/Arc, anyhow vs thiserror, and a crate shortlist (tokio, serde, axum, sqlx). Use when starting a Rust project, fighting the borrow checker, or picking crates.
metadata:
  version: "0.9.0"
  categories: "development"
  topics: "rust, ownership, cargo, crates, tokio"
  upstream: "rust@1.99.1, tokio@1.54.1, axum@0.8.9, reqwest@0.13.5, sqlx@0.9.0, jiff@0.2.39, kache@2.0.0, dist@0.34.0, release-plz-action@0.5.148, cargo-zigbuild@0.24.1, insta@1.49.0"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/rust-dev
    emoji: "🦀"
---

# Rust Development - Day 1

A practical foundation for writing Rust apps well from the first commit. Not a textbook. Focuses on the differences from other languages, the day-1 decisions that shape everything else, and the small set of crates that cover most real apps.

## When to Use

- Starting a new Rust project (CLI, service, library)
- Coming to Rust from Python, JavaScript, Go, Java/C#, or C++
- Choosing between owned/borrowed types, smart pointers, trait objects vs generics
- Picking error handling strategy (`anyhow` vs `thiserror`)
- Deciding which crates to reach for
- Configuring a minimal but opinionated `Cargo.toml`, clippy, and rustfmt

## Day-1 Setup

```bash
# 1. Install the toolchain (rustup is the toolchain manager)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Confirm components (rustfmt and clippy ship with stable, rust-src enables IDE features)
rustup component add rustfmt clippy rust-src

# 3. Create a project
cargo new my-app          # binary (src/main.rs)
cargo new --lib my-lib    # library (src/lib.rs)

# 4. The dev loop (memorize these four)
cargo check     # fast type-check, no codegen
cargo run       # build and run (binary)
cargo run -- --verbose in.txt   # args after `--` go to your program, not to cargo
cargo test      # build and run tests (incl. doctests)
cargo clippy --all-targets   # lint, incl. tests/ and benches/ (run before pushing)
cargo fmt       # format

# 5. Manage dependencies without editing Cargo.toml by hand
cargo add tokio --features full
cargo remove tokio
cargo update                 # recompute Cargo.lock within existing semver ranges

# 6. Update the toolchain when a new stable ships (every six weeks)
rustup update
```

`cargo update` only moves within the version ranges already in `Cargo.toml`. Crossing a breaking version (`1.x` to `2.0`) needs a `Cargo.toml` edit or `cargo add <crate>@2`. For a `0.x` crate - most of the shortlist below - the minor number is the breaking one: Cargo treats versions as compatible when "their left-most non-zero major/minor/patch component is the same", so `axum` `0.8` to `0.9` is as breaking as `1.x` to `2.0`.

When a program panics, run it again with `RUST_BACKTRACE=1 cargo run` to see the call stack that led there - the panic message suggests it, and it is the first thing to reach for.

**rust-analyzer is mandatory.** It is the language server every editor uses (VS Code, Zed, Neovim, Helix, RustRover uses its own engine but is comparable). In VS Code, install the `rust-analyzer` extension and set `rust-analyzer.check.command` to `"clippy"` so you get lint feedback on save.

**Want a file watcher later?** `cargo install --locked bacon`, then run `bacon` in your project. Not needed on day 1.

## The Rust Mental Model in 5 Ideas

Rust trades two things you take for granted in most languages (a garbage collector and exceptions) for compile-time guarantees about memory, data races, and error handling. The shape of the language follows from that trade.

### 1. Ownership: every value has exactly one owner

Think of values like physical objects. A book, a file, a network connection. At any moment, **one variable owns it**. You can:

- **Move it**: `let b = a;` hands ownership to `b`. `a` is gone.
- **Borrow it immutably**: `&a` lets others look at it. Many readers allowed.
- **Borrow it mutably**: `&mut a` lets one person modify it. Exclusive access.
- **Clone it**: `a.clone()` makes a deep copy. Both keep their own.

When the owner goes out of scope, the value is dropped (memory freed, file closed, lock released). No GC, no manual `free`. This is RAII, enforced by the compiler.

### 2. Aliasing XOR mutability

At any moment, a piece of data has **either**:
- one mutable reference (`&mut T`), **or**
- any number of immutable references (`&T`),

never both. This single rule is what eliminates data races and most use-after-free bugs. The borrow checker enforces it. When it complains, it is telling you your data ownership story is unclear, not that the language is being difficult.

### 3. Errors are values, not exceptions

There is no `try`/`catch`. Functions that can fail return `Result<T, E>`. Functions that can return nothing useful return `Option<T>`. The compiler forces you to handle both. The `?` operator propagates errors up the call stack with one character:

```rust
fn read_config() -> Result<Config, anyhow::Error> {
    let text = std::fs::read_to_string("config.toml")?;  // ? = early-return on Err
    let config = toml::from_str(&text)?;
    Ok(config)
}
```

There is no `null`. `Option<T>` is `None` or `Some(value)`. The compiler will not let you forget the `None` case.

### 4. Traits are not Java interfaces

A `trait` defines behavior. Types `impl` traits. So far so familiar. The differences:

- **Static dispatch is the default.** When you write `fn f<T: Display>(x: T)`, the compiler generates a separate copy of `f` for each concrete `T` you call it with (monomorphization, like C++ templates). Zero runtime overhead.
- **Dynamic dispatch is opt-in** via `dyn Trait` (typically `Box<dyn Trait>` or `&dyn Trait`). One vtable lookup per call.
- **No inheritance.** Traits compose. If you find yourself reaching for `Deref` to "extend" a type, stop and use composition or an enum.
- **Orphan rule**: you can `impl YourTrait for SomeoneElsesType` or `impl SomeoneElsesTrait for YourType`, but not both foreign. This keeps dependency resolution sane.

### 5. The borrow checker is a design oracle

The most common newcomer mistake is treating compiler errors as obstacles to silence. They are not. Almost every borrow-check error reveals a real issue with **who owns what**. When you get stuck, the question is rarely "how do I make this compile" and almost always "what is the actual ownership relationship I want here?" Read the error. The compiler is unusually informative.

## The 3 Questions for Every Function Signature

Before writing a function, ask: does it need to **own**, **read**, or **modify** the input?

```rust
fn consume(s: String)        // owns:    function takes responsibility, caller loses it
fn read(s: &str)             // reads:   function looks at it, caller keeps it
fn modify(s: &mut String)    // mutates: function changes it in place
```

Defaults that work 90% of the time:
- Function parameters: prefer `&str` over `String`, `&[T]` over `Vec<T>` (these are slices, accept both owned and borrowed callers).
- Function returns: return owned types (`String`, `Vec<T>`). Returning references means lifetimes; avoid until you need them.
- Struct fields: prefer **owned** types (`String`, `Vec<T>`). Storing `&str` in a struct is the single most common newcomer trap and it cascades lifetime annotations through every type that holds your struct.

## Day-1 Decision Table

One-line answers to the choices that come up first.

| Decision | Default | When to pick the other |
|---|---|---|
| `String` vs `&str` (struct field) | `String` | Almost never `&str` until you have a real reason and understand lifetimes |
| `String` vs `&str` (function param) | `&str` | Use `String` only if you must own/store it inside |
| `Vec<T>` vs `&[T]` (param) | `&[T]` | `Vec<T>` only if you must own |
| `Box<T>` vs `Rc<T>` vs `Arc<T>` | `Box<T>` (single owner, heap) | `Arc<T>` for shared ownership across threads. Avoid `Rc<T>` as default; use `Arc<T>` so you do not refactor when you go async |
| `RefCell<T>` vs `Mutex<T>` | `Mutex<T>` (or `RwLock<T>`) | Same reason: works in async/threads, while `RefCell` does not |
| `Option<T>` vs `Result<T, E>` | `Option<T>` for "no value", `Result<T, E>` for "failed for a reason" | If the absence carries meaning the caller should handle, `Result` |
| `dyn Trait` vs `impl Trait` / `<T: Trait>` | Generic (`<T: Trait>` or `impl Trait`) - static dispatch | `Box<dyn Trait>` when you need a heterogeneous collection (`Vec<Box<dyn Animal>>`) |
| Errors in app code | `anyhow::Result<T>` everywhere | - |
| Errors in library code | `thiserror`-derived enum | Never `Box<dyn Error>` in public library APIs - forces callers to downcast |
| `&self` vs `&mut self` vs `self` | `&self` for getters, `&mut self` for setters, `self` for builders/consuming ops | - |
| Module layout | Inline modules until a file gets long, then split | One module = one file is a Java/C# instinct, not a Rust one |

## Idioms to Internalize Early

These appear in nearly every Rust program. Learn them in week 1.

**`?` for error propagation.** Replaces nine lines of `match` with one character.
```rust
let body = reqwest::get(url).await?.text().await?;
```

**Iterator chains over manual loops.** Compile to the same machine code as hand-written loops (LLVM inlines closures). Idiomatic Rust is functional in style.
```rust
let active_emails: Vec<String> = users
    .iter()
    .filter(|u| u.active)
    .map(|u| u.email.clone())
    .collect();
```

**`match` exhaustiveness.** Add a new variant to an enum and every `match` that does not handle it becomes a compile error. Use this. It is one of the most powerful refactoring tools in any language.

**Let the compiler drive refactors.** The same trick works on structs: add a mandatory field with no `Default` and every existing constructor becomes a compile error - a free, exhaustive worklist of every site to update.

**`if let` and `let else`** for the common single-arm match.
```rust
if let Some(name) = user.name { println!("hi {name}"); }

let Some(name) = user.name else { return Err(anyhow!("no name")); };
// `name` is in scope from here on, no nesting
```

**`From` / `Into` for type conversions.** Implement `From`, get `Into` for free. `?` uses `From` to convert error types automatically.

**Combinators on `Option` / `Result`.** Reach for `.map`, `.and_then`, `.unwrap_or`, `.unwrap_or_else`, `.ok_or` before reaching for `match`.

**Derive macros.** `#[derive(Debug, Clone, PartialEq)]` gets you 80% of the boilerplate for free. Add `#[derive(Serialize, Deserialize)]` for JSON.

**Recent sugar.** Stabilized features worth knowing, newest first: `bool::ok_or` and `ok_or_else` (1.98) turn a condition straight into a `Result` (`ready.ok_or(Error::NotReady)?`). `cfg_select!` is a compile-time `match` over `cfg` predicates, replacing most uses of the `cfg-if` crate, and `if let` guards work on `match` arms (`match x { Some(v) if let Ok(n) = v.parse::<i32>() => ... }`) - both 1.95. `assert_matches!` and `debug_assert_matches!` (1.96) assert on a pattern rather than equality, which is the natural assertion for an enum. Two older ones you will see constantly and should not mistake for exotic: **let-chains** (`if let Some(x) = a && x > 3 { ... }`), stable in edition 2024 since 1.88, and **async closures** (`async || { ... }`, with the `AsyncFn` family of bounds), stable since 1.85.

## Coming From X, Here Is What Bites You

**From Python or JavaScript:**
- `let b = a;` for a heap value (like `String`, `Vec`) **moves** it. `a` is no longer usable. Use `&a` to borrow or `a.clone()` to copy.
- No null. `Option<T>` is forced on you.
- No exceptions. `Result<T, E>` and `?`. The compiler will not let you ignore errors.
- No inheritance. Composition + traits + enums.
- Variables are immutable by default. Add `mut` to mutate. Same for references: `&` vs `&mut`.
- Re-declaring a name is allowed and idiomatic: `let input = input.trim();` *shadows* the old binding with a new one, possibly of a different type. It is not mutation, and it is how Rust code converts a value in place without inventing `input2`.
- Integer types are explicit and indexing requires `usize`. They also overflow differently depending on the build: debug "includes checks for integer overflow that cause your program to _panic_ at runtime", while `--release` drops them and performs "_two's complement wrapping_". A test suite that passes can still wrap in production, so use `checked_*`/`saturating_*`/`wrapping_*` where the arithmetic can actually reach the edge, rather than relying on the debug panic to find it. `strict_add` and friends (stable since 1.91) panic on overflow in every build, and `overflow-checks = true` under `[profile.release]` keeps the debug behavior in production. And `as` between integer types silently truncates (`300_u32 as u8` is `44`) - use `u8::try_from(x)?` wherever the value might not fit.
- A `String` is not indexable. `s[0]` does not compile - see `references/ownership-and-types.md` for what to reach for instead.

**From Go:**
- Errors as values - same instinct, but use `?` instead of `if err != nil`.
- No `nil`. `Option<T>`.
- No GC and no goroutines: ownership + borrowing, async/await with `tokio`. The async model is cooperative (`await` is an explicit yield point), not preemptive.
- `interface{}` becomes traits. Default to generics for static dispatch; `Box<dyn Trait>` only when you need it.
- Static linking is the default. Binaries are bigger but self-contained.
- `panic!` should be reserved for unrecoverable bugs in app code; do not use it as Go-style "log and continue".

**From Java or C#:**
- Traits are not interfaces with virtual dispatch by default. `<T: Trait>` is monomorphized. `dyn Trait` is the opt-in dynamic version.
- No null references. `Option<T>`.
- No exceptions. `Result<T, E>` and `?`.
- No class inheritance. Use enums for sum types, traits for shared behavior.
- No GC: ownership and borrowing decide lifetimes. `Arc<T>` is the closest thing to a Java reference.
- Generics are monomorphized, not type-erased.

**From C++:**
- Like RAII, but the borrow checker enforces it at compile time.
- No copy/move constructors. `Clone` is explicit and `Copy` is a marker trait for cheap bitwise copies.
- No undefined behavior in safe code (in theory).
- `&` is a compile-time-checked borrow, not a raw pointer. Raw pointers exist (`*const T`, `*mut T`) but require `unsafe` to dereference.
- Smart pointers are `Box<T>` (`unique_ptr`), `Rc<T>` (`shared_ptr`, single thread), `Arc<T>` (`shared_ptr`, thread-safe).
- Macros are hygienic. Procedural macros (derive, attribute, function-like) are how `serde`, `tokio::main`, etc. work.

## The Crate Shortlist

These cover most real apps. Add them as needed; they are not all required.

| Crate | What it gives you |
|---|---|
| `serde` + `serde_json` | Serialization. `#[derive(Serialize, Deserialize)]` and you are done |
| `tokio` | Async runtime. `#[tokio::main]`, `tokio::spawn`, async I/O |
| `anyhow` | App error type. `anyhow::Result<T>`, `bail!`, `context()` |
| `thiserror` | Library error enums. `#[derive(thiserror::Error)]` |
| `clap` | CLI argument parsing. `#[derive(Parser)]` and you have a CLI |
| `reqwest` | HTTP client. Async by default, blocking feature available |
| `tracing` + `tracing-subscriber` | Structured logging. The default for any async code (replaces `log`) |
| `axum` | Web framework. Built on `tokio` + `hyper` + `tower`. The 2026 default |
| `sqlx` | Database access. Async, compile-time checked queries. PostgreSQL, MySQL, SQLite |
| `chrono` | Dates and times. The maintainer announced soft-deprecation in Jan 2026 and recommends `jiff` for new code. `jiff` (BurntSushi) is the successor but still pre-1.0 as of November 2026 (0.2.x, with the 1.0 tracking issue open and no date); blessed.rs now "weakly recommend[s] jiff" and names `time` as the other well-integrated option. Pick `chrono` for `serde`/`sqlx` integration today, `jiff` if you can tolerate pre-1.0 churn |

See `references/crate-shortlist.md` for one minimal example each.

## Top Anti-Patterns to Avoid

These are the mistakes that show up in every newcomer's code review. Avoid them.

1. **Storing `&str` (or any reference) in a struct.** Causes lifetime annotations to cascade through every caller. Use `String` until you have a profiler-backed reason not to.
2. **Reaching for `Rc<RefCell<T>>` (or `Arc<Mutex<T>>`) to simulate Python/JS object graphs.** First ask whether you need shared mutable state at all - usually plain ownership, or passing data through a channel, is cleaner. When you genuinely do, prefer `Arc<Mutex<T>>` over `Rc<RefCell<T>>` so adding threads later is not a refactor.
3. **`Box<dyn Error>` in library public APIs.** Forces callers to downcast. Define a typed error enum with `thiserror`. `Box<dyn Error>` is acceptable inside a binary, never in a published library.
4. **`.unwrap()` and `.expect()` outside prototypes and tests.** Use `?` and propagate - for an `Option`, `.ok_or_else(|| anyhow!(...))?` does the conversion. When a value genuinely cannot be absent, prefer `.expect("why it cannot fail")` over `.unwrap()`: the message is the comment that documents the invariant.
5. **Brute-force `.clone()` until it compiles.** Sometimes cloning is right, but if you are scattering `.clone()` to silence the borrow checker, the design is wrong. Step back and ask the 3 questions about who owns what.
6. **Trying to inherit via `Deref`**. `Deref` is for smart-pointer-like wrappers, not for OOP-style "extends". Use composition.
7. **Reaching for `unsafe`.** App developers should essentially never need it. `unsafe` does not turn off the borrow checker; it lets you do five specific things (deref raw pointers, call unsafe functions, access mutable statics, implement unsafe traits, access union fields) with the contract that you have manually verified the invariants.
8. **Reading untrusted input with `.lines()` or `read_line`.** These allocate without bound. `BufRead::read_line`'s own docs warn that "it is possible for an attacker to continuously send bytes without ever sending a newline or EOF" - and `.lines()` inherits that behavior, since each item is a `read_line` under the hood. Either way a hostile or malformed peer can drive your process out of memory. Bound the read with `Read::take(n)`, and use `BufRead::skip_until` (stable since 1.83) to discard an over-long line. `for line in reader.lines()` is the first thing every tutorial teaches and almost none mention this.
9. **Trusting `std::fs::write` with data you cannot lose.** It truncates and then writes in place, so a crash or power loss mid-write leaves a zero-length or half-written file - and a successful return does not mean the bytes reached the disk. For state files and manifests: write to a temp file *in the same directory*, call `File::sync_all()`, `rename` it over the target, and on Unix also `sync_all()` the parent directory so the rename itself survives a reboot. (`tempfile::NamedTempFile::persist` does the rename, not the syncs.)
10. **Assuming a file lock ends when the `File` drops.** `File::lock` (stable since 1.89) is released when the file "(along with any other file descriptors/handles duplicated or inherited from it) is closed, or if the [`unlock`] method is called". A process spawned on another thread at that moment briefly holds an inherited duplicate between fork and exec, so a lock released only by dropping the `File` is sometimes still held when the next caller tries to take it - which surfaces as a flaky test long before it surfaces in production. Call `file.unlock()` explicitly in your guard's `Drop`.

## What to Defer

You do not need these on day 1. Some you may never need.

- **Lifetimes in struct fields.** Avoid by using owned types. The day you genuinely need them, you will know.
- **`Pin`, `Future` internals, manual `poll` impls.** Just write `async fn` and `.await`.
- **`unsafe` and FFI.** Almost never for app code.
- **Procedural macros.** Library author territory.
- **Higher-ranked trait bounds (`for<'a>`)**, variance, `PhantomData`. Expert territory.
- **`Cell`, `OnceCell`, `LazyLock`, `MaybeUninit`.** Reach for these when you have a specific reason.

## Minimal Cargo.toml

Single-crate, edition 2024, opinionated lints. Drop into a fresh project.

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]

[dev-dependencies]

[profile.release]
lto = "thin"
codegen-units = 1

# =============================================================================
# Lints. Loose-but-helpful: deny obvious bugs, warn on common smells, leave
# room to learn. Upgrade to clippy::pedantic later if you want the full ride.
# =============================================================================
[lints.rust]
# "deny", not "forbid": forbid cannot be lifted by a local #[allow] with a
# SAFETY comment, and that bites on ordinary mmap, not just FFI.
unsafe_code     = "deny"
unreachable_pub = "warn"

[lints.clippy]
all = { level = "deny", priority = -1 }
# Idiomatic helpers
# Note: uninlined_format_args moved to clippy::pedantic (allow-by-default)
# during the 1.89/1.90 cycle, so an explicit warn keeps the nudge active.
uninlined_format_args         = "warn"
semicolon_if_nothing_returned = "warn"
implicit_clone                = "warn"
# Smells in non-prototype code
dbg_macro   = "warn"
todo        = "warn"
print_stdout = "warn"   # use `tracing::info!` instead in real apps
```

When you do need to silence a lint, prefer `#[expect(clippy::lint_name, reason = "why")]` (stable since 1.81) over `#[allow]`: `expect` warns once the lint stops firing, so stale suppressions surface instead of piling up. Clippy's `allow_attributes` and `allow_attributes_without_reason` (both in the opt-in `restriction` group) enforce it. One catch: a lint that fires on only one OS needs `#[cfg_attr(unix, expect(...))]`, or the `expect` is unfulfilled - and warns - everywhere else.

## rustfmt.toml

```toml
style_edition = "2024"
edition       = "2024"
```

That is enough. rustfmt's defaults are good. Some teams add `use_small_heuristics = "Max"` to keep more code on single lines. Fancy options like `imports_granularity` and `group_imports` are still nightly-only as of November 2026 (rustfmt tracking issues #4991 and #5083), and rustfmt does not format the arms of a `cfg_select!` on stable yet.

Run `cargo fmt` before you start editing (or commit any pre-existing drift on its own) so formatting noise stays out of your diff, and make `cargo fmt --check` its own CI step.

## rust-toolchain.toml (optional but recommended)

Pins the toolchain per project so everyone on the team uses the same Rust - but only with an exact version. `channel = "stable"` means "whatever stable this machine last installed", so two machines disagree silently, and a compiler cache keyed on the exact `rustc` never shares artifacts between them. Bump the pin deliberately (see `references/dev-environment.md`).

```toml
[toolchain]
channel    = "1.99.1"
components = ["rustfmt", "clippy", "rust-src"]
profile    = "minimal"
```

The file is a rustup feature. A `rustc` from Nix, a distro package, or Homebrew ignores it, so on those machines you get whatever compiler is installed. Even under rustup it is not the top of the precedence list: a `rustup override set` for the directory (and `RUSTUP_TOOLCHAIN`, and `cargo +toolchain`) wins over it, so a forgotten override silently makes the file dead weight. Overrides and the file also rank by proximity: a `rust-toolchain.toml` closer to the current directory beats a directory override set further up. `rustup show` tells you which toolchain is active and why; `rustup override unset` clears it.

## .gitignore

```
/target
```

Commit `Cargo.lock`. `cargo new` tracks it, and the Cargo guide's advice is "When in doubt, check `Cargo.lock` into the version control system". The FAQ deliberately stops short of making that universal - "whether you do is dependent on the needs of your package" - but for an application it is unambiguously right, and committing it is now the ordinary default for libraries too.

## Project Structure

```
my-app/
  src/
    main.rs        # binary entry point: fn main()
    lib.rs         # OR a library crate root
    config.rs      # module: declared as `mod config;` in main.rs/lib.rs
    api/           # nested module
      mod.rs       # OR `api.rs` next to api/ folder (2018+ style preferred)
      users.rs
    bin/           # extra binaries: src/bin/admin.rs -> `cargo run --bin admin`
  examples/        # runnable examples: `cargo run --example demo`
  tests/           # integration tests (each file is its own crate)
    smoke.rs
  Cargo.toml
  Cargo.lock
  rust-toolchain.toml
  rustfmt.toml
  .gitignore
```

Inline modules with `mod { ... }` until a file gets long, then split. Do not pre-split.

**Everything is private by default**, including to a parent module. `mod config;` makes the module exist; it does not make anything inside it reachable. That is the source of the most common early "why can't I call this" error, and the fix is a visibility keyword on the item (and on the module, if it is nested): `pub` exposes it to the outside world, `pub(crate)` exposes it only within your own crate. `pub(crate)` is the right default for anything that is not part of a library's published API - it is what lets the `unreachable_pub` lint in the table below tell you something useful.

**Naming an item in another module** is the next error after visibility (`unresolved import`). A path starting with `crate::` is absolute from your crate root, `super::` is the parent module, and `self::` the current one: `use crate::config::Config;` works from anywhere in the crate, `use super::helper;` from a child module. `pub use` re-exports an item at a shorter path - `pub use crate::api::users::User;` in `lib.rs` lets callers write `my_lib::User` without seeing your internal layout.

**Keep `main.rs` thin**, even in a binary: argument parsing plus a call into `lib.rs`. Integration tests in `tests/` can only reach a library crate, so logic left in `main.rs` cannot be tested from there (see `references/testing.md`).

The layout above is one crate. The moment you want a second - a shared library plus a CLI, a server plus its client - you need a Cargo **workspace**, along with the `Cargo.toml` machinery that goes with growing past a single crate: feature flags, build scripts, and what `rust-version` actually controls. That is `references/project-shape.md`.

## Learning Path

1. **The Rust Book** (https://doc.rust-lang.org/book/) - canonical, free, current. The interactive Brown University version (https://rust-book.cs.brown.edu/) adds quizzes and visualizations.
2. **Rustlings** (https://github.com/rust-lang/rustlings) - exercises in parallel with The Book.
3. **100 Exercises to Learn Rust** (https://rust-exercises.com/) - alternative or supplement to Rustlings, slightly newer.
4. **Rust for Rustaceans** (Jon Gjengset) - the post-beginner book. Read after you are comfortable.
5. **Zero to Production in Rust** (Luca Palmieri) - if you are building a backend service. Note: the book uses `actix-web` while `axum` is the 2026 default; the patterns translate cleanly.

For looking up syntax: **Rust by Example** (https://doc.rust-lang.org/rust-by-example/).

For curated crate recommendations: **blessed.rs** (https://blessed.rs/crates).

## Reference Docs

Detailed material lives in `references/`. Read each when you hit the topic.

- **ownership-and-types.md** - ownership, borrowing, lifetimes, `String`/`&str`/`Cow`, why a string is not indexable, slices, `HashMap` and the `entry` API, smart pointers, the self-referential struct trap
- **error-handling.md** - `Result`, `?`, `anyhow` vs `thiserror` patterns, wrapping at the boundary rather than before it, custom error enums, when `panic!` is appropriate
- **traits-and-generics.md** - traits as bounds, `dyn` vs `impl Trait` vs generics, common derives, `From`/`Into`/`Display`/`Debug`, closures and the `Fn`/`FnMut`/`FnOnce` family, blanket impls, the orphan rule
- **async-basics.md** - threads and `mpsc` before async, `tokio`, `#[tokio::main]`, `.await`, `Send`/`Sync`, bounded concurrency, cancellation and graceful shutdown on SIGTERM, common pitfalls (blocking in async, `MutexGuard` across `.await`)
- **crate-shortlist.md** - a minimal usage example for each crate above, plus the production defaults that bite
- **project-shape.md** - past one crate: workspaces and inherited dependencies, `[workspace.lints]`, feature flags, `build.rs`, what `rust-version` controls, `#[non_exhaustive]`
- **testing.md** - what to test and what to skip, pragmatic test organization, keeping the suite fast, the minimal high-value tool kit
- **dev-environment.md** - the fast build loop, build caching (kache setup and its quirks, sccache, rust-cache), keeping `target/` in check, platform-aware linker guidance, CI, file watchers
- **releasing.md** - shipping a binary: `dist` vs a hand-rolled `release-plz` + `cargo-zigbuild` pipeline, `[profile.dist]`, cross-compiling every target from one runner, fanning out to binstall/Homebrew/Nix, and guarding what the published crate contains
- **performance.md** - profiling before optimizing, benchmarking with criterion/divan, the real runtime wins
