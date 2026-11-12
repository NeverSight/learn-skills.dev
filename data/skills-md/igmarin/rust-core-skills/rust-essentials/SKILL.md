---
name: rust-essentials
type: atomic
tags: [atomic]
license: MIT
description: >-
  Trigger: Rust implementation, crate API, Cargo.lock, dependency version,
  compiler check. Establish project conventions and exact-version evidence
  before changing Rust code.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Rust Essentials

## RULES

1. Read the crate instructions, `Cargo.toml`, `Cargo.lock`, toolchain file, and the nearest relevant source or test. Follow existing architecture and dependencies.
2. Verify every crate API, feature, or import path against the locked version using local crate source/docs or a minimal compile. Do not infer APIs from newer examples.
3. Parse untrusted input at boundaries. Add types only for meaningful invariants; borrow when ownership need not transfer.
4. Use `Result` and `?` for expected failures. Add a dependency only when needed and after verifying its pinned API.
5. Keep `unsafe` rare and document the invariant that makes each block sound.

## Example

- ✅ Confirm the locked crate version and compile the API use before relying on it.
- ❌ Copy an API from the latest online example without checking the project's version.

## Validation

In the target crate, run `cargo fmt --check`, `cargo check`, and focused tests. For behavior changes, add and run a regression test; run `cargo clippy --all-targets -- -D warnings` and `cargo test` when supported.

## Integration

This is the baseline for `ownership-borrowing`, `type-driven-design`, and `error-handling`.
