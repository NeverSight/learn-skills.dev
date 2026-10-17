---
name: copper-coding-style
description: >-
  Coding style and conventions for the copper-rs (`cu29`) Rust workspace. Use when
  writing, editing, or reviewing Rust code, user documentation, or console/UI output
  in this repo so it matches house style:
  naming, import grouping, `CuResult`/`CuError` error handling, std/no_std discipline,
  the interning `debug!/info!/warning!/error!` logging macros, doc comments/doctests,
  clippy gotchas, payload trait bounds, and test layout. For runtime architecture see
  `copper-arch`; for core implementation constraints see `copper-core-dev`; for
  build/test/debug commands see `copper-workflow`.
---

# copper-rs — coding style & conventions

There is **no `rustfmt.toml` and no `[workspace.lints]`** — formatting is stock `cargo fmt`
(edition 2024) and lint policy is enforced on the command line (`clippy --deny warnings`).
Match the surrounding file; the patterns below are what "surrounding" looks like. Run
`just fmt` after every edit pass (see the `copper-workflow` skill).

## Naming

Public types are pervasively `Cu`-prefixed (`CuTask`, `CuMsg`, `CuError`, `CuResult`,
`CuContext`, `CuConfig`, `CuRuntime`, `CuHandle`...). Follow it for new public runtime
types. Crate *directories* use underscores (`cu29_runtime`, `cu_pid`); *published crate
names* use hyphens (`cu29-runtime`); the *import path* is the underscore form. The
`cu29::prelude::*` glob is the canonical app import surface — import from it in app/task
code, not from deep module paths. The V1 public-API contract is pinned in
`doc/v1-api-surface.md` and gated by `just api-check`; changing a public signature requires
a deliberate `just api-update`. Before writing `pub` at all, take the visibility ladder in
`copper-core-dev`.

Functions name the concrete operation and the thing it acts on — `assemble_steps`,
not `finish_plans`. Real examples: `build_culist_tuple`, `restore_keyframe`,
`stop_all_tasks`, `update_copperlist_rate`. Filler verbs are absent from the
workspace (zero `do_`, `perform_`, `execute_`, `manage_`, `helper_`); keep it that
way. Accessors read bare (`payload()`, `tov()`, `enabled()`) — the `get_` family in
`core/cu29_runtime/src/config.rs` and the graph API is legacy, extend it only inside
those types. Mutators keep `set_`/`clear_`, the mutable twin takes a `_mut` suffix,
predicates use `is_`. Constructors are `new` then `new_with_<thing>`; `with_<thing>`
is builder chaining only; `build_*` means proc-macro codegen emitting `TokenStream`
in `cu29_derive`. Reuse the established verb pairs instead of coining synonyms:
`freeze`/`thaw`, `encode`/`decode`, `start`/`stop`,
`preprocess`/`process`/`postprocess`, `send`/`receive`.

## Imports

Granular, one item per path, grouped as `crate::` → external crates → `core::`/`alloc::`,
with `#[cfg(feature = ...)]` attributes placed directly on the individual `use` line they
gate. Don't introduce glob imports in library code (the prelude is the deliberate exception
for downstream users).

## Error handling

Everything fallible returns `CuResult<T>` (`= Result<T, CuError>`); propagate with `?`.
Construct errors by:
- `CuError::from("message")` / `"msg".into()` for a plain message;
- `CuError::new_with_cause("message", source_err)` to wrap an underlying error (separate
  `std` and `no_std` impls exist — both available);
- builder style `CuError::from("msg").with_cause(e)` / `.add_cause("context string")`.

Read node config with `config.get::<T>("key")?` → `Option<T>`; for a required field use
`.get::<T>("key")?.ok_or(CuError::from("..."))?`. **Avoid `unwrap()`/`expect()` in library,
task, and runtime code** — return `CuResult`. `expect()` is acceptable only in example
`main()` bootstraps and tests. Never `panic!` on the real-time path.

## std vs no_std discipline (the most common way to break CI)

Shared crates are `#![cfg_attr(not(feature = "std"), no_std)]`. In that code use `core::`
and `alloc::` (e.g. `use alloc::{string::String, vec::Vec, boxed::Box, format};`) —
**never `std::`** outside a `#[cfg(feature = "std")]` block. Gate host-only APIs with
`#[cfg(feature = "std")]` and provide a `#[cfg(not(feature = "std"))]` counterpart where
the type must still exist. Guard illegal feature combos with `compile_error!` (e.g.
`parallel-rt` requires `std`). Verify with `just nostd-ci` (or at least
`cargo build --no-default-features`) whenever you touch shared crates, traits, or macros.

## Logging macros are NOT `std`/`log` macros

`debug!`/`info!`/`warning!`/`error!`/`critical!` are proc macros (`cu29_log_derive`) that
**intern** the format string into the unified log. Constraints that bite:
- the first arg is a **string literal**, optionally preceded by a `CuContext`
  expression (`debug!(ctx, "msg {}", val)`) that attaches callsite origin metadata;
- accepted placeholder forms (`cu29_log_derive`): plain `{}` with trailing args
  (`debug!("id={} ok={}", id, ok)`), named params (`debug!("a = {}", my_value = a)`),
  and std-style inline capture with optional format spec (`debug!("hash: {hash:?}")`).
  **Not** supported: positional `{0}` and bare `{:?}` without an identifier.
- they compile out below the active `log-level-*` feature (`critical!` always stays).
  **Default (no `log-level-*` feature set) is profile-driven** via
  `core/cu29_log_derive/build.rs`: **`debug` in dev builds, `info` in release** — so a
  `debug!(...)` line vanishes in `cargo build --release` unless you pass
  `--features cu29/log-level-debug`.

Use these for any temporary instrumentation; do not reach for `println!`/`eprintln!`. (See
`copper-workflow` for why the recorded log, not ad-hoc prints, is the debugging surface.)

## Doc comments & doctests

Every module opens with a `//!` summary. Public items get `///` docs; non-trivial APIs
include a ` ```rust ` `# Example` block. **Doctests run in CI** (`cargo test --doc` in
`std-ci` debug) — keep examples compiling.

## Clippy gotchas that recur here

All under `--deny warnings`: no redundant same-type casts (`x as u64` when `x: u64`);
prefer `.is_multiple_of(n)` over `% n == 0`; collapse nested `if`/`if let` into
`if let` chains when `collapsible_if` applies. `#[allow(dead_code)]` is tolerated; other
blanket `allow`s are rare — justify them.

## Payloads

Message payloads must satisfy `CuMsgPayload`: `Default + Debug + Clone + Encode + Decode<()>
+ Serialize + DeserializeOwned + Reflect (+ TypePath under the reflect feature)`. In practice
`#[derive(Default, Debug, Clone, Encode, Decode, Serialize, Deserialize, Reflect)]` (bincode
`Encode`/`Decode` come from `cu29::bincode`). It's a blanket impl — anything meeting the
bounds is a payload automatically.

## Tests

Unit tests live in a `#[cfg(test)] mod tests` at the bottom of the file, `#[test] fn
test_*`. Runner is `cargo nextest` (`just test`); use `tempfile` for scratch dirs. Hardware
crates that can't run in parallel are pinned to the `serial-integration` test group in
`.config/nextest.toml` — add new exclusive hardware crates there. `cu_caterpillar` carries
the **determinism regression test** (`determinism_record_and_resim`, feature
`determinism_ci`) that CI runs single-threaded with `COPPER_DETERMINISM_ITERS` — if you
change runtime execution/replay behavior, expect to keep it green.

## Documentation scope

Component and crate READMEs are user documentation, including on crates.io. Keep
repository CI commands, maintainer regression recipes, and generic Cargo test
instructions in `CONTRIBUTING.md`. Include commands in user docs when they help
configure, run, or use the component.

Describe behavior, requirements, and errors directly. Avoid lists of absent or
unrelated features and implementation history. Keep generic component docs generic;
put device-specific configuration, lifecycle, and wiring in the device's docs or
integration example. Apply this to READMEs, rustdoc, code comments, and PR descriptions.
For behavior changes, follow the docs-sync rule in `copper-workflow`.

## Console and UI

Assume Unicode-capable terminals. Generate unit symbols once and reuse them across
consumers; use Unicode mathematical notation. Use Catppuccin Mocha for interactive
terminals, UIs, prototypes, and diagrams; avoid cyan, amber, and Copper color. Omit
ANSI styling from recorded logs, machine exports, and redirected output by default.
