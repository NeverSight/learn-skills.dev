---
name: modern-rust
description: "Modern Rust release awareness for any Rust source, test, Cargo workspace, manifest, build script, toolchain, FFI, upgrade, or API work from Rust 1.72 onward."
---

# Modern Rust

Anchor Rust work in the repository's compatibility contract, not the model's
training cutoff.

## Orient

1. Inspect workspace and package `rust-version`, `edition`, and resolver
   settings in `Cargo.toml`; `rust-toolchain` or `rust-toolchain.toml`; and CI,
   container, and release toolchain pins when relevant.
2. Keep these signals distinct:

   | Signal | Meaning |
   | --- | --- |
   | `edition` | Per-crate language semantics; not an MSRV declaration |
   | `rust-version` | Minimum supported Rust compiler and Cargo |
   | Toolchain pin | Compiler selected for builds; not permission to raise MSRV |

3. Use syntax, standard-library APIs, Cargo features, and lints available at
   the declared MSRV and edition. If the MSRV is unstated, infer it
   conservatively from project policy and CI rather than raising it silently.
4. Read every release crossed by a toolchain or MSRV upgrade and any release
   whose feature affects the task. For an edition migration, run
   `cargo fix --edition` before changing `edition`, audit its safety-related
   edits, and test the supported toolchain range.
5. Use the latest patch in a selected `1.N` family. Point releases can fix
   miscompilations, security issues, and regressions without adding features.

## Release Index

Read a file when its feature affects the task or an upgrade crosses it.

- **2023:** [1.72](references/rust1.72.md) const evaluation and doctest paths ·
  [1.73](references/rust1.73.md) reference-cast lints and panic output ·
  [1.74](references/rust1.74.md) Cargo lints and registry authentication ·
  [1.75](references/rust1.75.md) async and opaque returns in traits.
- **2024:** [1.76](references/rust1.76.md) pointer identity ·
  [1.77](references/rust1.77.md) C literals, recursive async, and `offset_of!` ·
  [1.78](references/rust1.78.md) diagnostics and unsafe checks ·
  [1.79](references/rust1.79.md) inline const and associated bounds ·
  [1.80](references/rust1.80.md) lazy cells and `cfg` checking ·
  [1.81](references/rust1.81.md) core errors and expected lints ·
  [1.82](references/rust1.82.md) precise captures and raw references ·
  [1.83](references/rust1.83.md) const evaluation and macro fragments.
- **2025:** [1.84](references/rust1.84.md) provenance and MSRV-aware resolution ·
  [1.85](references/rust1.85.md) Rust 2024 and async closures ·
  [1.86](references/rust1.86.md) trait upcasting and disjoint mutation ·
  [1.87](references/rust1.87.md) trait captures and pipes ·
  [1.88](references/rust1.88.md) let-chains and cache collection ·
  [1.89](references/rust1.89.md) const inference and the Wasm C ABI ·
  [1.90](references/rust1.90.md) `rust-lld` and workspace publishing ·
  [1.91](references/rust1.91.md) C variadics and strict arithmetic ·
  [1.92](references/rust1.92.md) never fallback and zeroed allocation.
- **2026:** [1.93](references/rust1.93.md) musl and conditional assembly ·
  [1.94](references/rust1.94.md) `array_windows` and Cargo config inclusion ·
  [1.95](references/rust1.95.md) `if let` guards and `cfg_select!` ·
  [1.96](references/rust1.96.md) core ranges and stricter Wasm linking ·
  [1.97](references/rust1.97.md) v0 mangling and Cargo warning controls.

Rust remains on SemVer major 1; this skill treats each stable `1.N` feature
release as a version. Coverage starts at Rust 1.72 and ends at 1.97. For a
newer or uncertain toolchain, check the current
[official release announcements](https://blog.rust-lang.org/releases/) before
making version-sensitive decisions. Use these files for orientation, then
verify exact APIs and behavior in the official documentation for the relevant
toolchain.
