---
name: writing-rust
description: Use when writing or reviewing Rust that handles recoverable errors with Result and `?`, uses `.unwrap()` or `.expect()`, chooses between `&str` and `String`, adds `.clone()` or `.to_string()`, or uses async code, the Tokio runtime, or older futures 0.1 APIs.
---

# Writing Rust

## Overview

Write idiomatic Rust: propagate errors with `Result` and `?`, borrow strings instead of allocating them, and use current Tokio with `async`/`await`.

**Core principle:** Production code returns errors to its caller instead of panicking, and it only allocates when ownership is actually needed. "It compiles" and "it is shorter" are not reasons to unwrap or clone.

These rules apply to new code and requested changes. Do not migrate existing working code that is outside the request.

## Quick Reference

| Area | Do | Do not |
| --- | --- | --- |
| Recoverable errors | Return `Result` and propagate with `?` | Call `.unwrap()` or `.expect()` in production code |
| Intentional panics | Keep `.unwrap()`/`.expect()` to examples, tests, or code paths where a panic is explicitly intended and justified | Use them to skip error handling |
| Strings | Take `&str` for borrowed text; use `String` only for owned text | Add unnecessary `.to_string()` or `.clone()` calls |
| Async | Use current Tokio with `async`/`await` | Use older futures 0.1 APIs |

## Error Handling

Use `?` and `Result` types for recoverable errors. Avoid `.unwrap()` and `.expect()` in production code; keep them to examples, tests, or code paths where a panic is explicitly intended and justified.

Good:

```rust
fn read_config(path: &Path) -> Result<String, std::io::Error> {
    std::fs::read_to_string(path)
}
```

Bad:

```rust
fn read_config(path: &Path) -> String {
    std::fs::read_to_string(path).unwrap()
}
```

Propagating through several fallible steps with `?`:

```rust
fn load_port(path: &Path) -> Result<u16, Box<dyn std::error::Error>> {
    let raw = std::fs::read_to_string(path)?;
    Ok(raw.trim().parse()?)
}
```

When a panic really is intended, make the reason explicit:

```rust
let regex = Regex::new(r"^\d+$").expect("static pattern is valid");
```

## String Handling

Use `&str` for borrowed string slices and `String` for owned strings. Avoid unnecessary `.to_string()` and `.clone()` calls.

Good:

```rust
fn shout(name: &str) -> String {
    name.to_uppercase()
}

let owned = String::from("ada");
let loud = shout(&owned);
```

Bad:

```rust
fn shout(name: String) -> String {
    name.to_uppercase()
}

let owned = String::from("ada");
let loud = shout(owned.clone());
```

## Async Runtime

Use current Tokio with `async`/`await`. Avoid older futures 0.1 APIs.

Good:

```rust
#[tokio::main]
async fn main() -> Result<(), std::io::Error> {
    let contents = tokio::fs::read_to_string("config.toml").await?;
    println!("{contents}");
    Ok(())
}
```

Bad (futures 0.1 combinators and `Item`/`Error` associated types):

```rust
use futures::Future;

fn load() -> Box<dyn Future<Item = String, Error = std::io::Error>> {
    // ...
}
```

## Red Flags

Stop and use the idiomatic form if you think or see:

- "`.unwrap()` is fine here; it will not fail." In production code, return a `Result` instead.
- "Use `.expect()` in the handler to keep the signature simple."
- "Clone it so the borrow checker stops complaining" when borrowing `&str` would do.
- "Take `String` as the parameter type so callers do not need to think about it."
- "Use the futures 0.1 style because the example I found does."
- "The old style still works." Working code is not the same as current convention; a legacy reason is a concrete tool or platform constraint, not familiarity.

## Common Mistakes

- Leaving `.unwrap()` or `.expect()` in code that runs in production because the failure "should not happen".
- Returning a plain value from a function whose body can fail, and unwrapping inside it, instead of returning `Result`.
- Taking `String` parameters and cloning at call sites where `&str` would be enough.
- Calling `.to_string()` on a value that is already an owned `String` or only needs to be borrowed.
- Copying futures 0.1 patterns from older tutorials instead of current Tokio `async`/`await`.
- Rewriting unrelated working Rust code while making a small change; apply these rules to new or requested changes only.
