---
name: rust
description: |
  Rust language patterns and ecosystem covering ownership, borrowing, lifetimes, error handling (Result/Option, thiserror, anyhow), async with Tokio, traits, generics, serde serialization, Cargo workspaces, and testing. Includes axum web framework, ratatui terminal UI, clap CLI parsing, criterion benchmarking, cargo-deny supply chain security, cargo-dist binary distribution, and release-plz changelog automation.

  Use when writing Rust code, designing ownership models, building async services with Tokio/axum, creating terminal UIs with ratatui, setting up CLI applications with clap, configuring CI/CD pipelines for Rust, benchmarking with criterion, auditing dependencies with cargo-deny, or distributing binaries with cargo-dist.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://doc.rust-lang.org/book/'
user-invocable: false
---

# Rust

## Overview

Rust is a systems programming language focused on safety, concurrency, and performance. The ownership system guarantees memory safety without garbage collection, and the type system enforces thread safety at compile time.

**When to use:** Systems programming, web services (axum), CLI tools (clap), terminal UIs (ratatui), WebAssembly, performance-critical applications, anything requiring memory safety without runtime overhead.

**When NOT to use:** Rapid prototyping where compile times matter more than safety, simple scripting tasks, projects where the team has no Rust experience and deadlines are tight.

## Quick Reference

| Pattern             | API / Tool                          | Key Points                           |
| ------------------- | ----------------------------------- | ------------------------------------ |
| Ownership transfer  | `let b = a;`                        | `a` is moved, no longer usable       |
| Borrowing           | `&T` / `&mut T`                     | One mutable OR many immutable refs   |
| Lifetime annotation | `fn f<'a>(x: &'a str) -> &'a str`   | Ties output lifetime to input        |
| Error propagation   | `?` operator                        | Converts and propagates errors       |
| Custom errors       | `thiserror::Error` derive           | Structured error types with Display  |
| Ad-hoc errors       | `anyhow::Result<T>`                 | Context chaining for applications    |
| Async runtime       | `#[tokio::main]`                    | Entry point for async programs       |
| Spawn task          | `tokio::spawn(async { })`           | Concurrent async task execution      |
| HTTP router         | `axum::Router::new().route(...)`    | Composable routing with extractors   |
| Extractors          | `Json<T>`, `Path<T>`, `State<T>`    | Type-safe request parsing            |
| Serialization       | `#[derive(Serialize, Deserialize)]` | serde with format-agnostic derives   |
| CLI parsing         | `#[derive(Parser)]`                 | clap derive API for arg parsing      |
| TUI rendering       | `terminal.draw(\|f\| { })`          | Immediate-mode ratatui rendering     |
| Benchmarking        | `criterion::Criterion`              | Statistical benchmarking framework   |
| Dep auditing        | `cargo deny check`                  | License, vulnerability, source audit |
| Binary release      | `cargo dist init`                   | Cross-platform binary distribution   |
| Changelog           | `release-plz update`                | Auto semver bump and changelog       |

## Common Mistakes

| Mistake                                 | Correct Pattern                               |
| --------------------------------------- | --------------------------------------------- |
| Returning reference to local variable   | Return owned type or use lifetime parameter   |
| Using `unwrap()` in library code        | Return `Result` and let caller decide         |
| `clone()` to satisfy borrow checker     | Restructure code to avoid the borrow conflict |
| Blocking in async context               | Use `tokio::task::spawn_blocking`             |
| Shared mutable state without sync       | Use `Arc<Mutex<T>>` or channels               |
| `String` where `&str` suffices          | Accept `&str` in function parameters          |
| Ignoring `must_use` warnings            | Handle or explicitly discard with `let _ =`   |
| Large enum variants                     | Box the large variant to reduce overall size  |
| `async fn` in traits without bounds     | Add `Send` bound or use `async-trait` crate   |
| Missing `#[tokio::test]` on async tests | Use `#[tokio::test]` instead of `#[test]`     |

## Delegation

- **Code exploration**: Use `Explore` agent
- **Architecture review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `docker` skill is available, delegate multi-stage container build patterns to it.
> If the `github-actions` skill is available, delegate CI pipeline configuration to it.
> If the `openapi` skill is available, delegate API specification and code generation to it.

## References

- [Ownership, borrowing, lifetimes, and type system patterns](references/ownership-and-types.md)
- [Error handling with Result, Option, thiserror, and anyhow](references/error-handling.md)
- [Async programming with Tokio runtime and concurrency](references/async-tokio.md)
- [Web APIs and backends with axum, tower, and sqlx](references/axum-web.md)
- [Terminal user interfaces with ratatui and crossterm](references/ratatui-tui.md)
- [CLI applications with clap, config, and signal handling](references/cli-applications.md)
- [Testing patterns and criterion benchmarking](references/testing-and-benchmarks.md)
- [Release pipeline with cargo-deny, cargo-dist, and release-plz](references/release-pipeline.md)
