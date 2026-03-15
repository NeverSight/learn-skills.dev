---
name: agentic-progressive-disclosure-architecture
description: Build codebases for agentic coding with progressive disclosure using module trees, API-first top layers, and implementation split by depth (best fit for Rust and Go).
---

# Agentic Progressive Disclosure Architecture

Use this skill when you want code structure that reveals intent first and implementation details only when deeper files are loaded.

## What it is

Progressive disclosure for code architecture mirrors how skills are read:

1. Top layer: short explanation + module map + API signatures.
2. Middle layer: domain-focused modules that re-export or wire submodules.
3. Leaf layer: detailed implementations.

This pattern is strongest in **Rust** and **Go** where module/package boundaries are explicit.

## When to use it

- Agent-heavy coding workflows where small context windows must stay focused.
- Large systems where API shape should be visible without loading full implementations.
- Teams comfortable with IDE/LSP navigation for jump-to-definition and symbol search.

## Architecture rules

- Keep top-level files mostly declarative (exports, signatures, short docs).
- Place heavy logic in deeper modules/files.
- Re-export from higher layers to preserve ergonomic public APIs.
- Use concrete implementations with forwarding at higher layers (avoid interface-only top-level patterns for this technique in Go).
- Keep this orthogonal to existing clean-code practices (naming, testing, error handling, etc.).

## Recursive disclosure behavior

Apply the same disclosure split at every depth:

1. A module exposes intent and API shape.
2. It forwards or re-exports into child modules.
3. Children repeat this pattern until leaf implementation files.
4. Add an `AGENTS.md` at each level to describe the relevant context and constraints for that subtree.

This creates a navigable tree where each node progressively reveals detail.

## Implementation examples (separate reference)

- Rust example: `references/rust-module-forwarding.md`
- Go example (concrete type + forwarding): `references/go-package-forwarding.md`

## Validation in skill design

Benchmarking and deep performance validation belong to skill design and rollout evaluation, not core skill usage instructions.

Recommended checks:

- Tests assert callers can rely only on top-level APIs/re-exports.
- Callers can use top-level APIs without importing leaf implementation modules.
- Navigation remains fast via IDE/LSP symbols and definitions.
