---
name: writing-rust
description: "Use when Rust ownership, borrowing, traits, error types, async, public API docs, or unsafe boundaries constrain the design."
---

# Writing Rust

## Overview

Apply this modifier when Rust's ownership, type, error, async, or unsafe rules materially constrain the design. Keep generic implementation work in the primary skill and load only the Rust reference needed for the current pressure.

## When to Use

- Ownership and borrowing affect the API or implementation
- Trait, generic, or typestate design is the main question
- Error surfaces, docs, async, or unsafe boundaries need Rust-specific judgment

## When Not to Use

- Use `engineering` as the primary skill for generic implementation structure
- Use `test-design` when test selection is the primary task
- Use `designing-data-intensive-systems` for workload or storage architecture

## Minimal Workflow

1. Inspect the current API, call sites, owned and borrowed data, error surface, and repository conventions.
2. State the Rust-specific pressure: ownership, lifetime coupling, trait shape, state modeling, async behavior, or an unsafe boundary.
3. Compare safe shapes that keep the invariants explicit, then prefer the one with the simplest ownership story.
4. Make soundness, ergonomics, and API-stability tradeoffs explicit where they differ.
5. For guidance or review, finish with the recommended API or ownership shape, the material tradeoffs, and the compiler, test, doctest, or lint evidence needed.
6. During implementation, apply these Rust constraints as a modifier inside the primary `engineering` loop and use its fresh-verification stop condition.

## Reference Routing

- Read [STYLE.md](STYLE.md) for naming, visibility, and docs.
- Read [PATTERNS.md](PATTERNS.md) for traits, builders, typestate, and wrapper patterns.
- Read [DOCS.md](DOCS.md) for docs and doctests.
- Read [SSR.md](SSR.md) when a Rust refactor spans many sites and rust-analyzer structural search and replace is safer than manual edits.

## Failure modes

- Importing patterns from other languages without Rust-specific justification
- Hiding lifetime or ownership coupling behind “ergonomic” APIs
- Letting `unsafe` sprawl across module boundaries
