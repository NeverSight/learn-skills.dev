---
name: working-with-mbx
description: Use when installing, activating, or troubleshooting mbx (Mr. Boxington), the shared compiler cache for Cargo - verifies that plain cargo actually goes through mbx, reads hit/miss/bypass summaries, diagnoses low cache reuse, and manages target/cache disk usage
---

# Working with mbx

## Overview

mbx (Mr. Boxington) is a shared compiler cache for Cargo, plus automatic management of
`target/` directories. Cargo still resolves dependencies and decides what needs building;
mbx restores matching compilations and runs the compiler for everything else.

Use this skill when:
- Installing mbx or enabling it for plain `cargo` commands
- A build reports few cache hits and you need to know why
- Deciding whether an mbx result (hit / miss / bypass) is expected
- Reclaiming disk from the cache store or managed target directories
- Adding mbx caching to CI, or migrating off sccache / rust-cache

## The Iron Rules

1. **Never combine mbx with sccache** - both wrap rustc through `RUSTC_WRAPPER`. If
   `RUSTC_WRAPPER` is already set, mbx defers to it and the build is **not cached**.
2. **Verify activation by Cargo's path, not by `mbx doctor` alone** - doctor does not
   recognize the native mise Rust tool option, so its setup warning alone does not mean
   wrapping is inactive.
3. **Diagnose before deleting** - run `mbx explain` on the build. Clearing the cache
   destroys evidence and the next build just runs cold.
4. **Measure reuse with two fresh target directories** - rerunning the same command in
   the same target measures Cargo's freshness check, not mbx.

## Install

### With mise (preferred)

```bash
mise use --global --tool-option mr_boxington=true rust mr-boxington
```

Requires mise 2026.9.2 or newer. This installs Rust and mbx and enables Cargo wrapping
through mise - no `mbx setup` needed. `--tool-option` applies to the **following** tool,
so it must stay before `rust`. Drop `--global` to enable it only in the current project.

To share it with a project, commit both tools in `mise.toml`:

```toml
[tools]
rust = { version = "stable", mr_boxington = true }
mr-boxington = "latest"
```

Both entries are required. Keep the project's existing Rust version when adding
`mr_boxington = true`. Run `mise install`, then build.

### Without mise

```bash
cargo install mbx --locked
mbx --version
```

Release archives for Linux (x86-64/ARM64, glibc and musl), macOS Apple Silicon, and
Windows (x86-64/ARM64) are on GitHub Releases with `SHA256SUMS`. See
[references/installation.md](references/installation.md).

To make plain `cargo` use mbx from a standalone install:

```bash
mbx setup
mbx setup --status
```

`mbx setup` also configures rust-analyzer's background check - the native mise option
does not. Scope it with `--global` or `--local`; `--yes` accepts the recommendation.

## Verify mbx Is Actually Being Used

This is the single most common failure: builds succeed, but nothing is cached.

```bash
command -v cargo     # Unix
mbx doctor
```

On Windows use `(Get-Command cargo).Path` or `where.exe cargo`.

`cargo` should resolve to one of:
- mise's command wrapper (e.g. `~/.local/share/mise/command-wrappers/bin/cargo`)
- a mise shim
- the stable mbx shim from `mbx setup`

**Calling `~/.cargo/bin/cargo` directly bypasses mise's integration entirely.**

### Non-interactive contexts (coding agents, SSH, desktop apps)

These often inherit a different `PATH` than an interactive terminal. Use either:

```bash
mise exec -- cargo build      # explicit, always works
```

or put mise's shims directory on that process's `PATH`. Check with `command -v cargo`
run *by the application itself*, and restart the app after changing its environment.
Prefixing with `mbx` also always works: `mbx build`.

## Running Builds

`mbx` passes Cargo arguments through unchanged:

```bash
mbx build
mbx test --workspace --all-features
mbx clippy --workspace --all-targets -- -D warnings
mbx +stable check --workspace          # rustup-style toolchain selection
```

Use the same toolchain, features, and profile across builds to reuse the same cached work.

## Reading the Result

A build prints a summary like:

```
mbx[cache]: 139 hits, 8 misses, 4 not looked up, 147 prefetched, 7 bypassed; 312.4 MiB downloaded, 0 B uploaded, 280.1 MiB stored locally
```

| Result | What happened |
| --- | --- |
| Hit | mbx restored a matching compilation |
| Miss | No result matched the key; successful compilation fills the cache |
| Not looked up | mbx lacked a usable input prediction and had to compile first |
| Bypassed | The invocation ran without shared caching |

Counts describe compiler actions mbx observed. They do **not** include work Cargo skipped
because its outputs were already fresh - which is why a rerun can show zero hits.

```bash
mbx explain --last              # inspect the last recorded build, without running Cargo
mbx explain build --workspace   # run a build with diagnostics (preserves Cargo's exit status)
MBX_SUMMARY=full mbx build      # detailed breakdown
mbx tui                         # watch a build live, one row per compilation
```

### Measure real cache reuse

```bash
mbx build --target-dir target/cache-demo-first
mbx build --target-dir target/cache-demo-second
```

The second build can restore work recorded by the first. Use directory names that do not
already contain build outputs, and remove them afterwards - explicit targets are not
managed. Always compare wall-clock time too; "compiler time avoided" is summed across
actions, not elapsed time saved.

## Troubleshooting a Low Hit Rate

Run `mbx explain build --workspace` first - it groups identical causes and prints guidance
per category. Usual causes, roughly in the order they appear:

- **The store is cold.** A first build has no dep-info to derive keys from, so
  "could not look up" can dominate.
- **Incremental builds are enabled.** With `MBX_INCREMENTAL=1`, workspace members compile
  incrementally, those compilations bypass the cache, and crates above them miss too.
- **A link could not be described.** Native executables, tests, and proc macros are cached
  on Linux, macOS, and Windows, but links with custom or unmodeled inputs still run.
- **The inputs differ.** A different toolchain, feature set, profile, or `RUSTFLAGS`
  between checkouts is a different key, reported as an ordinary miss.
- **Build-script output differs.** A build script that embeds the checkout path in its
  output prevents reuse across checkouts.
- **The build chose its own C compiler.** Setting `CC`, `HOST_CC`, `CXX`, or `HOST_CXX`
  leaves host compilations outside mbx.
- **A Rust update.** The compiler is part of every key, so a toolchain roll invalidates
  every rustc action at once. This is expected, not a bug.

For a per-compilation record: `MBX_BYPASS_LOG=bypass.log mbx build`.

### Bypasses that are expected

`compiler-query` and `standard-input` are routine compiler probes with no output to cache.
The short summary leaves them out of its bypass count. Don't chase them.

## Other Common Symptoms

| Symptom | First check |
| --- | --- |
| Plain Cargo does not use mbx | `command -v cargo`; for standalone setup also `mbx setup --status` |
| Cargo waits for a target lock | Give simultaneous builds separate target directories |
| Cargo metadata fails before a build | `cargo metadata --no-deps --format-version 1` |
| Build storage is on NFS | Move `cache_dir` / `target.root` to local storage (mbx refuses NFS) |
| Remote requests fail | `mbx doctor`, then check authentication |
| Storage larger than expected | `mbx cache stats`, then `mbx gc --dry-run` |

### Bypass mbx for one command

```bash
MBX_DISABLE=1 cargo build
```

### Reporting a problem

```bash
mbx doctor --json
MBX_LOG=debug mbx build
MBX_BYPASS_LOG=bypass.log mbx build
```

These name absolute cache paths, any configured remote, and the crates you build.
Credentials are never printed.

## Managed Target Directories

Managed targets are **on by default**. For a checkout without an existing `target/`, mbx
places the target under its cache root and leaves a symlink:

```
target -> <cache root>/targets/v1/<checkout digest>
```

In a Git checkout, mbx adds the link path to `.git/info/exclude` when necessary, so
`git status` stays clean without touching the project's `.gitignore`.

mbx leaves the target alone when `--target-dir`, `CARGO_TARGET_DIR`, or Cargo's
`build.target-dir` names it.

Bring existing directories under management without deleting their contents:

```bash
mbx adopt                            # the current checkout
mbx adopt --recursive --dry-run ~/src  # preview
```

Disable placement with `MBX_TARGET_VIEWS=0` or `[target] views = false`.

## Disk Management

```bash
mbx cache stats     # action store, managed targets, learned incremental state
mbx cache dir       # where the store lives
mbx gc --dry-run    # preview collection under the configured budgets
mbx gc              # collect
mbx clean           # this workspace's managed target, link, and incremental state
mbx cache remove /path/to/workspace   # the above, plus forget its cache claims
mbx stats           # lifetime savings
```

Collection runs automatically after builds, at most once an hour. Budgets scale with the
disk holding the data:

| Budget | Default | Bounds |
| --- | --- | --- |
| `gc.max_size` (action store) | 5% of the disk | 5 GiB to 500 GiB |
| `target.max_size` (managed targets) | 10% of the disk | 10 GiB to 100 GiB |
| `gc.incremental_max_size` (learned incremental) | 5% of the disk | 10 GiB to 100 GiB |

Managed targets are also collected after `target.max_age` (30 days) unused, and whenever
their checkout is gone. The cache is disposable - it can always be rebuilt. Note that
`cargo clean` does **not** remove mbx's private incremental state; `mbx clean` does.

## Configuration

Three sources, first value found wins:

1. Environment variables (`MBX_*`)
2. `.mbx.toml` at the Cargo workspace root - **build-policy and scheduler settings only**
3. `mbx/config.toml` in the platform config directory:
   - Linux: `~/.config/mbx/config.toml`
   - macOS: `~/Library/Application Support/mbx/config.toml`
   - Windows: `%APPDATA%\mbx\config.toml`

Unknown TOML keys are rejected, so a misspelled setting is an error. Machine paths,
remote-cache configuration, credentials, target placement, and garbage collection are
**not** accepted from a repository's `.mbx.toml`.

Keep a laptop responsive by capping the machine-wide compiler pool (it defaults to every
logical CPU and 85% of physical memory):

```toml
[scheduler]
cpus = 4
memory = "8GiB"
```

Per-feature off switches:

| Switch | Turns off |
| --- | --- |
| `MBX_SCHEDULER=0` | machine-wide compile scheduling |
| `MBX_CC=0` | build-script and `mbx exec` C/C++ caching |
| `MBX_TARGET_VIEWS=0` | managed target directories |
| `MBX_CACHE_LINKS=0` | native link caching |
| `MBX_LEARNED_INCREMENTAL=0` | learned incremental reuse |
| `MBX_SAVINGS=off` | the savings line |

## CI

```yaml
steps:
  - uses: actions/checkout@v7
  - uses: jdx/mr-boxington-action@v1
  - run: mbx test --workspace
```

Install the toolchain **before** the action - generated keys cover the OS, architecture,
and the identity of the `rustc` on `PATH`. Pushes to the default branch fill the archive;
pull requests, including from forks, are restore-only. mbx automatically uses its
explanatory CI summary when `CI` or `GITHUB_ACTIONS` is set.

Migrating from sccache is **removal**: take it out of `RUSTC_WRAPPER`,
`build.rustc-wrapper` in `~/.cargo/config.toml`, and any install steps, then run
`mbx doctor`. Migrating from rust-cache is replacing the action - running both over the
same paths adds duplicate restore/save work.

## Available References

- [references/getting-started.md](references/getting-started.md) - install to first cached build
- [references/setup.md](references/setup.md) - Cargo wrapping, rust-analyzer, verifying Cargo's path
- [references/troubleshooting.md](references/troubleshooting.md) - symptom table and diagnostics
- [references/cache-results.md](references/cache-results.md) - hit/miss/bypass, measuring reuse
- [references/limits.md](references/limits.md) - exactly what mbx will and will not cache
- [references/managed-targets.md](references/managed-targets.md) - target placement, adoption, budgets
- [references/configuration.md](references/configuration.md) - full setting reference
- [references/incremental.md](references/incremental.md) - learned incremental reuse
- [references/scheduling.md](references/scheduling.md) - parallel builds, machine-wide pool
- [references/github-action.md](references/github-action.md) - CI setup
- [references/cookbook/migrate.md](references/cookbook/migrate.md) - from sccache or rust-cache
- [references/cookbook/local-development.md](references/cookbook/local-development.md) - editors, watch loops, debugging
- [references/remote-cache.md](references/remote-cache.md) - cache server and S3 backends
- [references/cli/](references/cli/) - per-command flags and arguments

Refresh all of the above with `./update-docs.sh`.

## Red Flags - You're About to Violate

- Leaving sccache configured "just in case" → mbx silently stops caching
- "`mbx doctor` warned about setup, so mbx isn't active" → check `command -v cargo` first
- Running the same build twice in one target to prove caching works → measures Cargo freshness
- Clearing the cache to fix a low hit rate → run `mbx explain --last` first
- Chasing `compiler-query` / `standard-input` bypasses → routine probes, nothing to cache
- Telling a coding agent or CI script to call `~/.cargo/bin/cargo` → bypasses mise integration
- Putting `[remote]` credentials in a checked-in `.mbx.toml` → rejected; use env vars
- Adding `cargo clean` to a watch loop → throws away Cargo's freshness information
