---
name: copper-workflow
description: >-
  Build, test, and debugging workflow for the copper-rs (`cu29`) repo. Use when running
  CI-aligned `just` targets (pr-check/lint/test/std-ci/nostd-ci/api-check), adding or
  reviewing justfile recipes, publishing stable releases, setting up the
  environment to make those pass, rendering the DAG, expanding the runtime macro, or
  debugging a running/recorded app via the unified `.copper` log: extracting copperlists,
  resim (deterministic replay), the remote-debug API, or the Python export. For
  architecture see `copper-arch`; for code style see `copper-coding-style`.
---

# copper-rs — build, test & debugging workflow

Prefer `just` targets over ad-hoc cargo invocations — they mirror
`.github/workflows/general.yml`. Run `just fmt` after every edit pass. Before pushing, run
the narrowest fitting target; default to `just pr-check`. For lint/build changes run at
least `just lint`; include `just nostd-ci` when practical for shared/runtime surfaces.
Default branch is `master`.

Before starting a work pass, remove generated `Cargo.lock` files unless explicitly
asked otherwise; resolving without lockfiles matches CI. Do not remove them as final
cleanup.

## Adding justfile recipes

Add recipes only for reusable end-user operations or general development workflows
(build, format, lint, test suites, replay, export). Before adding one, identify who will
reuse it and when; extend or parameterize an existing recipe when it already serves that
workflow. Keep workspace-wide workflows in the root `justfile` and app-specific ones in
the app's `justfile`.

Do not add one-shot recipes for the current patch, debugging session, or a specific unit
test. Run a focused command such as `cargo test -p <crate> <test_filter>` directly instead
of committing a recipe for it. A test recipe should represent a maintained suite or
recurring validation workflow, rather than merely aliasing an individual test.

## Build & verification

| Command | Purpose |
|---|---|
| `just` / `just pr-check` | full local PR gate: `fmt` → `lint` → `api-check` → `test` |
| `just fmt` | format Rust (`cargo fmt`), TOML (`taplo`), **RON (`fmtron`)**, + prek hygiene hooks |
| `just lint` | `fmt-check` + `typos` + `clippy-std` + `clippy-nostd` (clippy is `--deny warnings`) |
| `just test` | `nextest` std (excludes embedded) + `nextest --no-default-features` |
| `just std-ci [mode=debug\|release\|cuda-release]` | mirror the std CI path (incl. caterpillar determinism test + template generation) |
| `just nostd-ci` | mirror embedded/no_std CI (clippy/build no-default-features + rp2350 thumbv8m + embedded crates) |
| `just api-check` / `just api-update` | check / refresh the V1 public-API snapshot (`cargo-public-api`, nightly) |
| `just dag [mission=]` | render the working-dir `copperconfig.ron` graph |
| `just expand-runtime pkg=<crate> bin=<bin> [features=]` | `cargo expand` the generated runtime |
| `just rtsan-smoke pkg= bin= [args=]` | run an app under the realtime sanitizer |
| `just docs` | build wiki + rustdoc locally |

Tooling: builds need **Rust 1.95+** (edition 2024). `just` targets self-check for required
tools and print the `cargo install` line if missing (`taplo-cli`, `fmtron`, `prek`,
`cargo-nextest`, `cargo-llvm-cov`, `cargo-public-api@0.51.0`, `cargo-expand`). The public-API
check needs a **pinned nightly** toolchain (`PUBLIC_API_TOOLCHAIN` in the justfile). Per-directory `justfile`s under `examples/`,
`components/`, etc. `import "../../justfile"` and add app-specific targets (`cl`, `resim`,
`mcap`, ...). The workspace is large/hardware-heavy: **package-focused verification
(`-p <crate>`) is often more pragmatic than a full-workspace run.**

### Environment setup (required for `pr-check`/`std-ci` to pass)
Without these, the checks fail on *environmental* (not code) errors — clippy-std/test pull
GUI/GStreamer/pcap crates and python-task tests:
- apt (mirrors `support/docker/Dockerfile.ubuntu`): `libudev-dev libpcap-dev libglib2.0-dev
  libssl-dev clang libclang-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
  libgstreamer-plugins-bad1.0-dev libwayland-dev libxkbcommon-dev`
- python: `pip3 install --break-system-packages cbor2` (for `cu-python-task` process-mode tests).

If this list ever fails, `support/docker/Dockerfile.ubuntu` is the source of truth — the
snapshot above will drift; the pointer will not.

## Logging & debugging

Use `copper-debug-replay` before adding instrumentation: extract recorded CopperLists
or structured text logs, then use resim, remote debug, or Python queries as needed.
Use `copper-coding-style` for structured logging macro syntax.

## Other gotchas

- **RON files are formatted with `fmtron`** (run via `just fmt`); a `.bak` is produced and
  auto-deleted. Don't hand-format RON. TOML is formatted with `taplo`. There is also a RON
  format check (`support/ci/check_ron_format.sh`) in `fmt-check`.
- The `.copper` log is written as slabs: a base `app.copper` plus `app_0.copper`,
  `app_1.copper`... Tools take the *base* path and find the slabs.
- `build.rs` in apps exports `LOG_INDEX_DIR` (`OUT_DIR`) so the interned-string index can
  be reconstructed. Examples must write logs under their own `logs/` directory, never
  the Copper repository's root `logs/`. App builders own log setup through
  `.with_log_path(...)`; examples may inject a custom logger with `.with_logger(...)`.
  A unified-log slab can exist even when task-message logging is disabled.
- Feature flags on `cu29` worth knowing: `std`, `signal-handler`, `textlogs`, `units`
  (default set), plus `reflect`, `remote-debug`, `safety-ids`, `parallel-rt` (requires std),
  `rtsan`, `async-cl-io`, `high-precision-limiter`, `sysclock-perf`, `defmt` (no_std logging).
- `cargo deny` advisory ignores live in `.config/deny.toml`; typo allowlist in
  `.config/_typos.toml`. Update those rather than disabling the checks.
- Docs sync: when a change in `core/` alters documented behavior, the maintainer expects
  follow-up PRs to the sibling `../copper-rs.wiki` and `../copper-rs-book` checkouts.

## Stable releases

When publishing a stable minor or patch release, including a backport, complete the
GitHub release checklist in the Copper checkout's `RELEASING.md`. Publish an entry for
the exact release tag using the global Copper Release Notes; keep Latest on the newest
stable version.
