---
name: copper-core-dev
description: >-
  Core-runtime development guide for the copper-rs (`cu29`) workspace. Use when changing
  code under `core/` or runtime-wide behavior: execution planning, task/bridge traits,
  proc-macro generation, config parsing, resource wiring, unified logging and replay,
  public API surfaces, real-time performance, or `std`/`no_std` compatibility. For the
  execution-model overview see `copper-arch`; for code conventions see
  `copper-coding-style`; for CI-aligned verification see `copper-workflow`.
---

# copper-rs core development

Use this skill for changes to the runtime and SDK implementation, not for ordinary
application or component authoring. Read `copper-arch` first when the task depends on the
task-graph, message-flow, resource, mission, or replay mental model.

The repository root `AGENTS.md` holds always-on policy and skill routing. When sources
disagree, use **code > rustdoc/API > wiki/book narrative**. The default branch is
`master`.

## Core workspace map

- `core/cu29` — primary user-facing crate. Its prelude is the normal downstream import
  surface (`use cu29::prelude::*;`), and `lib.rs` is `#![no_std]`-aware.
- `core/cu29_runtime` — runtime implementation:
  - `config.rs` — RON schema and graph validation.
  - `curuntime.rs` — `CuRuntime` and `compute_runtime_plan`, the topological plan embedded
    by the macro.
  - `cutask.rs` — task traits, `CuMsg`, and `Freezable`.
  - `cubridge.rs` — bridges and typed channels.
  - `app.rs` — `CuApplication` lifecycle traits.
  - `resource.rs` — typed HAL/resource wiring.
  - `simulation.rs`, `app_sim.rs`, and `replay.rs` — simulation and replay.
  - `remote_debug.rs` — remote-debug support behind the `remote-debug` feature.
  - `monitoring.rs` and `reflect.rs` — monitoring and feature-gated reflection.
- `core/cu29_derive` — `#[copper_runtime]`, `bundle_resources`, `resources`,
  `safety_case`, and `gen_cumsgs!` proc macros.
- `core/cu29_export` — log-reader CLI, MCAP/JSON/CSV export, and the feature-gated Python
  API.
- `core/cu29_unifiedlog` — `.copper` slab format and storage.
- Supporting core crates include `cu29_clock`, `cu29_traits`, `cu29_value`, `cu29_log*`,
  `cu29_soa_derive`, `cu29_units`, and `cu29_intern_strs`.

Outside `core/`, use these as integration and regression surfaces:

- `components/` — reusable sources, sinks, tasks, bridges, payloads, monitors, codecs,
  resource bundles, libraries, and test helpers.
- `examples/` — executable documentation. Start with `examples/cu_caterpillar/`, which
  also carries the determinism regression test.
- `support/cargo_cunew/templates/` — project templates (`cu_project` and `cu_full`).
- `support/ci/embedded_crates.py` and embedded examples/components — the practical
  `no_std` build surface.
- `vendor/` — patched dependencies referenced from workspace Cargo configuration.

`default-members` covers only the core platform-neutral crates. Full-workspace builds
include hardware and GUI dependencies; use `copper-workflow` before choosing a check.

## Design constraints

### Prefer static, generated structure

A robot's component graph is known ahead of time. Prefer types, compile-time wiring, and
proc-macro/codegen enforcement over runtime string-keyed lookup, service discovery, or
dynamic topology. Treat generated code as an intended architecture surface.

Do not introduce environment-variable APIs unless explicitly requested. Prefer constants
for implementation choices.
For a genuine user-facing choice, ask whether it belongs in RON config, but require a
real use case before expanding the schema.

### Protect the real-time path

Do not allocate on the real-time stack or path. Treat a new allocation, copy,
serialization pass, blocking operation, or latency increase there as a design-level
change. Keep offline and debug-only costs feature-gated away from the hot path, and use
preallocation, fixed capacity, compile-time sizing, and borrowing where practical.
Require explicit user approval before accepting added hot-path copies, allocation,
serialization, or latency. Startup allocation volume also matters: embedded targets
may have extremely small memory budgets.

Use `just rtsan-smoke` for a runnable hot-path change. Apply `copper-api-flavor` whenever
the change introduces or reshapes a user-facing trait, adapter, or config policy.

### Decide visibility before writing `pub`

`doc/v1-api-surface.md` is the contract: every public item is `stable` (V1 semver),
`experimental` (may change without a major bump), `internal` (public only because proc
macros, generated code, tests, or rustdoc need a path), or `deprecated`. Already-internal:
`CuRuntime` fields, `CuRuntimeParts`, `CuRuntimeBuilder`, the `*Instantiator` traits,
`ProcessStepOutcome`/`ProcessStepResult`, the CopperList managers, generated mission
modules, and tuple access through `copper_runtime_mut()`.

Pick the narrowest rung that works:

- `pub(crate)` — default. Nothing outside the crate needs it.
- `#[doc(hidden)] pub` — the `internal` rung. Generated code or another crate needs the
  path, users do not. This is how `planner` and `CuContext::from_runtime_metadata` stay
  reachable while staying out of the contract.
- plain `pub` — a real user-facing addition. Add it to `doc/v1-api-surface.md` under the
  right label in the same commit.

`just api-check` (inside `just pr-check`) diffs `cargo public-api` against the checked-in
snapshots in `api/v1/`. Two mechanics decide whether it catches you:

- **`#[doc(hidden)]` items are omitted from the snapshot.** A plain `pub` addition fails
  the check with a diff; the same item marked `#[doc(hidden)]` passes silently. Use that
  to express intent, not to quiet CI — `just api-update` is the deliberate gesture for an
  intended change, and re-running it to erase an unexplained diff hides a real leak.
- **Only `cu29`, `cu29-build`, `cu29-runtime`, `cu29-traits`, `cu29-derive`,
  `cu29-export`, and `cu29-unifiedlog` are gated.** `cu29_clock`, `cu29_value`,
  `cu29_log*`, `cu29_units`, `cu29_soa_derive`, `cu29_intern_strs`, and everything under
  `components/` are not. Because `cu29::prelude` glob-re-exports several of them and the
  `cu29` snapshot records only the re-export name, a new `pub` item in `cu29_clock`
  reaches every user's prelude and still passes `api-check`. In those crates the label
  decision is yours alone — no gate will make it for you.

### Treat `std`/`no_std` as an API axis

Do not assume host APIs in shared crates. Consider embedded impact immediately when
changing shared traits, macros, messages, or runtime code. Gate host-only behavior and run
`just nostd-ci` when practical. Platform priority is Linux, then macOS, then preserving
`no_std`; Windows CI intentionally covers a smaller core-only scope.

### Preserve deterministic replay

Execution order, logged message layout, component state, keyframes, time behavior, and
generated types all participate in replay. A runtime change that affects one of these can
alter recorded logs or make resim diverge. Use the determinism regression in
`cu_caterpillar` and the `copper-debug-replay` workflow instead of validating only the
live path.

Do not paper over a runtime or generation problem with glue that hides the underlying
model. Expand generated code when macro behavior is unclear.

## Where to make a change

- Runtime planning or execution: `core/cu29_runtime/src/curuntime.rs` and `app.rs`.
- Task API, messages, lifecycle, or freezing: `core/cu29_runtime/src/cutask.rs`.
- Bridge API and channel generation: `core/cu29_runtime/src/cubridge.rs`.
- RON schema or graph validation: `core/cu29_runtime/src/config.rs`; use
  `copper-ron-config`.
- Runtime proc-macro generation: `core/cu29_derive/src/lib.rs`; use
  `copper-macro-debug` and expand the affected app.
- Resources and HAL injection: `core/cu29_runtime/src/resource.rs` and
  `examples/cu_resources_test/`.
- Unified logging, export, and replay: `core/cu29_unifiedlog/`, `core/cu29_export/`, and
  `core/cu29_runtime/src/{simulation,app_sim,replay,remote_debug}.rs`; use
  `copper-debug-replay`.
- Templates and project-generation DX: `support/cargo_cunew/templates/{cu_project,cu_full}/`.
- Embedded compatibility: `support/ci/embedded_crates.py`, embedded resource components,
  and the `cu_rp2350_skeleton` example.

## Before finishing a core change

1. Apply `copper-coding-style` to the Rust diff.
2. Apply the most specific companion skill: `copper-api-flavor`, `copper-ron-config`,
   `copper-macro-debug`, or `copper-debug-replay`.
3. Check downstream examples, components, templates, generated code, and `no_std` targets
   touched by the public or generated surface.
4. Use `copper-workflow` to select and run the narrowest CI-aligned checks; default to
   `just pr-check` when the environment supports the full gate.
