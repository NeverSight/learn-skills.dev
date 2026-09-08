---
name: rust-expert
description: >-
  Rust expert coding guidelines and best practices for writing idiomatic,
  production-quality Rust code. Use this skill whenever writing, reviewing, or
  refactoring Rust code — including designing APIs, handling errors, working
  with traits, managing resources, parsing CLI args, or choosing crates. Triggers
  on any Rust task: struct design, error handling, trait objects, async code,
  CLI tools, encryption, event systems, and dependency selection.
---

# Rust Expert Guidelines

These rules define the project's Rust coding standards. Apply them consistently across all Rust code.

## 1. Observer / Event Propagation — Use a `Listener` Trait

When an object needs to propagate internal events outward, define a `Listener` trait and accept it as a generic or trait object. This keeps the object's internals private while letting callers observe behavior.

```rust
pub trait Listener: Send + Sync {
    fn on_event(&self, event: Event);
}

pub struct Worker<L: Listener> {
    listener: L,
}
```

Never expose internal channels, callbacks, or state directly — route all outbound signals through the `Listener` interface.

## 2. Null Object — Use `DummyListener`, Not `Option<Box<dyn Listener>>`

When no listener is needed, use a no-op `DummyListener` struct that implements `Listener`. This eliminates `if let Some(...)` guards everywhere and keeps call sites clean.

```rust
pub struct DummyListener;
impl Listener for DummyListener {
    fn on_event(&self, _event: Event) {}
}

// Usage — no Option unwrapping needed:
let worker = Worker::new(DummyListener);
```

Never use `Option<Box<dyn Listener>>` as a substitute for an optional listener.

## 3. Trait Object Ownership — `Arc<dyn T>` for Shared, `Box<dyn T>` for Exclusive

| Situation | Use |
|---|---|
| Shared ownership across threads | `Arc<dyn T>` |
| Single owner, heap-allocated | `Box<dyn T>` |
| No polymorphism needed | Generic `T: Trait` (see rule 4) |

## 4. Prefer Generics Over `dyn T` When Polymorphism Is Unnecessary

If a type or function only ever works with one concrete type at each call site, use a generic parameter instead of a trait object. Monomorphization is zero-cost, avoids vtable overhead, and enables inlining.

```rust
// Prefer this:
fn process<L: Listener>(listener: &L) { ... }

// Over this (only when runtime dispatch is actually needed):
fn process(listener: &dyn Listener) { ... }
```

Use `dyn T` only when the concrete type is unknown at compile time or when you need to store heterogeneous types in a collection.

## 5. Encapsulation — Keep Interfaces Simple, Complexity Inside

The public API of a type should be minimal and stable. Implementation complexity (state machines, retries, locking strategies, internal protocols) belongs inside the function or struct, not in its signature or public fields.

Signs of leaking complexity:
- Callers must pass internal state or flags
- Public fields hold mutex guards or intermediate results
- A function's signature reveals its implementation strategy

Design from the outside in: write the ideal call site first, then implement to match it.

## 6. Error Handling — Use `anyhow::Result`

For application code and library internals where the caller does not need to match on error variants, use `anyhow::Result<T>`. Never use `Result<T, ()>` or `Result<T, String>`.

```rust
use anyhow::{Context, Result};

fn load_config(path: &Path) -> Result<Config> {
    let raw = fs::read_to_string(path)
        .with_context(|| format!("failed to read {}", path.display()))?;
    Ok(toml::from_str(&raw)?)
}
```

For library public APIs where callers need to distinguish error kinds, define a typed error with `thiserror` (see rule 7) and keep `anyhow` to internals.

## 7. Custom Error Types — Use `thiserror`

When a typed error is necessary (public library API, error matching), derive it with `thiserror`. Never implement `std::error::Error` by hand.

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("config file not found at {path}")]
    NotFound { path: PathBuf },
    #[error("invalid value for field `{field}`: {source}")]
    InvalidField { field: String, #[source] source: anyhow::Error },
}
```

## 8. Derive Formatting — Use `derive_more` Before Hand-Rolling

When the standard `#[derive(Debug)]` or `#[derive(Display)]` macros are insufficient (e.g., you need a custom `Display` on a complex struct), reach for `derive_more` before writing an impl manually.

```rust
use derive_more::{Display, Debug};

#[derive(Display, Debug)]
#[display("Peer({addr})")]
pub struct PeerInfo {
    addr: SocketAddr,
    // ...
}
```

Only write a manual `impl fmt::Display` or `impl fmt::Debug` if `derive_more` cannot express the required format.

## 9. CLI Argument Parsing — Use `clap`

Parse all command-line arguments with `clap` using its derive API. Do not use `std::env::args()`, `getopts`, or ad-hoc string splitting.

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "mytool", version, about)]
struct Args {
    #[arg(short, long, default_value = "config.toml")]
    config: PathBuf,

    #[arg(short, long)]
    verbose: bool,
}

fn main() {
    let args = Args::parse();
}
```

## 10. Resource Lifecycle — OOP + RAII via `rust-async-lifecycle`

Manage resources with RAII: the object is both the resource and its handler. Use the structured-concurrency patterns from the `rust-async-lifecycle` skill:

- Object owns the resource, the lifecycle (`TaskScope`), and the operations — do not split them
- `Drop` signals cancellation; `async fn close()` cancels and drains
- `tokio::spawn` lives at the call site; the spawned function stays pure; the cancellation `select!` sits at the top of the spawned task

Read the [`rust-async-lifecycle`](../rust-async-lifecycle/SKILL.md) skill for the full pattern, decision table, and audit workflow.

## 11. Cryptography — Use `aws-lc-rs`

For all cryptographic operations, depend on `aws-lc-rs`. Do not use `ring` or the RustCrypto family (`aes`, `sha2`, `rsa`, etc.) as direct dependencies.

```toml
[dependencies]
aws-lc-rs = "1"
```

`aws-lc-rs` is API-compatible with `ring` for most use cases and is backed by AWS's maintained fork of BoringSSL, with FIPS support available.

## 12. Scoped Cleanup — Use `scopeguard::defer!` for Local Resource Teardown

When a local variable or side effect needs guaranteed cleanup at scope exit — but doesn't warrant a full RAII wrapper type — use `scopeguard::defer!`. This is the Rust equivalent of `defer` in Go or a finally block, and is appropriate for one-off cleanup that is too small to deserve its own `Drop` impl.

```rust
use scopeguard::defer;

fn with_temp_file() -> Result<()> {
    let path = create_temp_file()?;
    defer! {
        let _ = fs::remove_file(&path);
    }

    // use the file; cleanup runs automatically on any exit path
    process(&path)?;
    Ok(())
}
```

Use `defer!` for: temporary files, unlocking external resources, resetting global state in tests, and any other ad-hoc cleanup that runs once. Prefer a proper `Drop` impl (RAII struct) when the same cleanup pattern recurs across multiple call sites.
