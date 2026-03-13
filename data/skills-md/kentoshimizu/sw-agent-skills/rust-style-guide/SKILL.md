---
name: rust-style-guide
description: "Style, review, and refactoring standards for Rust codebases. Trigger when `.rs`, `Cargo.toml`, or `Cargo.lock` files are created, changed, or reviewed and Rust-specific quality rules (ownership/borrowing clarity, error handling, trait/API design, crate boundaries) must be enforced. Do not use for C/C++ toolchain conventions, shell-only changes, or non-Rust runtime style concerns unless Rust artifacts are also changed. In multi-language pull requests, run together with other applicable `*-style-guide` skills."
---

# Rust Style Guide

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

Apply this checklist when writing or reviewing Rust code.

## Trigger Reference

- Use `references/trigger-matrix.md` as the canonical trigger and co-activation matrix.
- Resolve skill activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...` when automation is available.
- Validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Architecture and module boundaries
## Quality Gate Reference

- Use `references/quality-gate-command-matrix.md` for CI check-only vs local autofix command mapping.

1. Keep modules cohesive; expose only required public APIs.
2. Keep domain logic independent from transport/storage layers.
3. Isolate side effects and external dependencies behind traits where appropriate.
4. Avoid large monolithic modules; split by capability and ownership.

## Naming and structure

1. Follow Rust naming conventions (`snake_case`, `CamelCase`, `SCREAMING_SNAKE_CASE`).
2. Keep functions focused and minimize deep nesting.
3. Replace magic numbers with named constants and units (`MAX_RETRIES`, `TIMEOUT_MS`).
4. Prefer explicitness over clever macro-heavy abstractions for core logic.

## Type safety and data modeling

1. Model domain states with enums/newtypes to prevent invalid combinations.
2. Prefer typed structs over loosely typed maps for boundary payloads.
3. Encode invariants in constructors/builders.
4. Keep lifetimes and ownership semantics explicit where non-trivial.

## Error handling

1. Return `Result` for recoverable failures and use specific error enums/types.
2. Add context to errors (`thiserror`, `anyhow::Context`, or equivalent patterns).
3. Avoid `unwrap`/`expect` in production paths unless invariant is proven and documented.
4. Handle errors intentionally at boundaries (retry/map/log/rethrow).
5. Do not hide root-cause failures behind generic fallback behavior.

## Configuration and environment

1. Parse and validate configuration during startup.
2. Fail startup when required environment variables are missing.
3. Do not set fallback defaults for required environment variables.
4. Keep secrets out of source and logs.

## Security and compliance

1. Validate all untrusted input and enforce schema constraints.
2. Use safe query APIs/parameterization for persistence layers.
3. Avoid invoking shell commands with unchecked user input.
4. Redact sensitive values in logs and error messages.

## Performance and scalability

1. Profile before optimization and focus on measured bottlenecks.
2. Avoid unnecessary cloning/allocations in hot paths.
3. Stream large data and bound queues/channels.
4. Use explicit limits for retries, buffers, and parallelism.

## Testing and verification

1. Add unit tests for pure logic and integration tests for external boundaries.
2. Cover edge cases: invalid inputs, timeout, cancellation, concurrent access.
3. Add regression tests for each bug fix.
4. Document manual verification for behavior not covered by automation.

## Observability and operations

1. Emit structured logs with correlation IDs.
2. Emit metrics for latency, throughput, and failure classes.
3. Keep error types actionable for operational triage.
4. Ensure health checks surface dependency readiness.

## CI required quality gates (check-only)

1. Run `cargo fmt --all -- --check`.
2. Run `cargo clippy --all-targets --all-features -- -D warnings`.
3. Run `cargo test --all-targets --all-features`.
4. Reject changes that weaken compile-time guarantees.

## Optional autofix commands (local)

1. Run `cargo fmt --all`.
