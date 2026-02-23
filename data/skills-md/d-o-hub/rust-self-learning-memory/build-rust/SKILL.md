---
name: build-rust
description: Optimized Rust build operations with timing, profiling, and workspace support
---

# Rust Build Operations

Efficiently build Rust workspaces with the build-rust CLI.

## Usage

```bash
# Development (fast, debug symbols)
./scripts/build-rust.sh dev

# Release (optimized, stripped)
./scripts/build-rust.sh release

# Profile with timing information
./scripts/build-rust.sh profile

# Fast type-check only
./scripts/build-rust.sh check

# Clean build artifacts
./scripts/build-rust.sh clean

# Build specific crate
./scripts/build-rust.sh release memory-core
```

## Modes

| Mode | Purpose | Flags |
|------|---------|--------|
| `dev` | Development build | `--workspace` |
| `release` | Production optimized | `--release --workspace` |
| `profile` | Performance timing | `--release --timings` |
| `check` | Fast type-check | `--workspace` |
| `clean` | Clean artifacts | `--clean` |

## Disk Space Optimization (ADR-032)

The dev profile is optimized to reduce target/ size (~5.2 GB → ~2 GB):

```toml
# .cargo/config.toml
[profile.dev]
debug = "line-tables-only"    # ~60% smaller debug artifacts

[profile.dev.package."*"]
debug = false                 # No debug info for dependencies

[profile.dev.build-override]
opt-level = 3                 # Faster proc-macro execution

[profile.debugging]
inherits = "dev"
debug = true                  # Full debug when needed: --profile debugging
```

**Linker**: Use `mold` on Linux for 2-5x faster link times:
```toml
[target.'cfg(target_os = "linux")']
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```

**Cleanup**: `cargo clean` or `./scripts/clean-artifacts.sh`

## Common Issues

**Timeouts**
- Use `dev` mode for faster iteration
- Reduce parallel jobs: `CARGO_BUILD_JOBS=4 ./scripts/build-rust.sh release`

**Memory errors**
- Build with fewer jobs: `cargo build -j 4`
- Use `check` instead of full build

**Dependency conflicts**
- Update: `cargo update`
- Check tree: `cargo tree -e features`
- Check duplicates: `cargo tree -d | grep -cE "^[a-z]"`

**Platform-specific**
- Install targets: `rustup target add <triple>`
- Conditional compilation: `#[cfg(target_os = "linux")]`

## References

- [ADR-032: Disk Space Optimization](../../../plans/adr/ADR-032-Disk-Space-Optimization.md)
- [ADR-036: Dependency Deduplication](../../../plans/adr/ADR-036-Dependency-Deduplication.md)
