---
name: error-handling
type: atomic
tags: [atomic]
license: MIT
description: >-
  Trigger: Rust error handling, Result, ?, typed errors, recoverable failures,
  error propagation. Use when changing a failure contract.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Error Handling

## RULES

1. Preserve the crate's existing error contract. Use `Result` for recoverable failures and reserve panic for violated internal invariants.
2. Propagate expected errors with `?`; add context at a boundary when it improves diagnosis.
3. Preserve public typed errors. Follow the application's existing convention; do not add a dependency just to wrap one failure.
4. Do not unwrap user input, I/O, network, or parse results. Keep error messages useful without exposing secrets or sensitive input.

## Example

- ✅ Propagate a file-read failure with `?` using the crate's existing error type.
- ❌ Panic on a missing file that is part of ordinary input.

## Validation

Test expected error variants and boundary context; run `cargo check` and focused tests in the target crate.

## Integration

Start with `rust-essentials`; pair with `type-driven-design` when an error type encodes a domain invariant.
