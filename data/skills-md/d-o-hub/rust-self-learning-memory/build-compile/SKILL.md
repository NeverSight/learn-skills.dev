---
name: build-compile
description: Build Rust code with proper error handling and optimization for development, testing, and production
---

# Build Compile Agent

Orchestrate Rust build operations with proper error handling, optimization, and workspace management. Use this agent when compiling the self-learning memory project or troubleshooting build errors in CI/CD pipelines.

## Core Capabilities

**Build Operations**
- Compile Rust workspaces with appropriate optimization levels
- Handle build errors with systematic debugging
- Manage cross-compilation and platform-specific targets
- Parallel build optimization for CI/CD

**Error Diagnosis**
- Parse compiler error messages
- Identify dependency conflicts
- Resolve feature flag issues
- Detect memory/timeout constraints

**Quality Assurance**
- Run clippy for lint checks
- Execute test suite compilation
- Verify release build integrity
- Validate stripped binary sizes

## Build Modes

| Mode | Use Case | Performance | Size | Flags |
|------|----------|-------------|------|--------|
| `dev` | Development iteration | Fast | Large | `--workspace` |
| `release` | Production deployment | Optimized | Medium | `--release --workspace` |
| `profile` | Performance analysis | Medium | Medium | `--release --timings` |
| `check` | Fast validation | Fastest | N/A | `--workspace` (type-check only) |
| `clean` | Artifact cleanup | N/A | N/A | `--clean` |

## CLI Integration

**For human operators**, see the build-rust CLI documentation:
```bash
# Quick development iteration
./scripts/build-rust.sh dev

# Production build
./scripts/build-rust.sh release

# Performance profiling
./scripts/build-rust.sh profile

# Fast type-check
./scripts/build-rust.sh check

# Clean artifacts
./scripts/build-rust.sh clean
```

## Error Handling Patterns

**Timeout Errors**
- Symptom: Build exceeds time limits
- Diagnosis: Check `CARGO_BUILD_JOBS` parallelism
- Solution: Reduce concurrency: `CARGO_BUILD_JOBS=4 cargo build`
- Alternative: Use `check` mode for faster feedback

**Memory Errors**
- Symptom: OOM during link phase
- Diagnosis: Monitor with `/usr/bin/time -v cargo build`
- Solution: `cargo build -j 1` (sequential)
- Fallback: Use `check` mode (no codegen)

**Dependency Conflicts**
- Symptom: Feature flag conflicts
- Diagnosis: `cargo tree -e features`
- Solution: `cargo update` for compatible versions
- Manual: Edit `Cargo.toml` feature resolution

**Platform-Specific**
- Symptom: Missing target triple
- Diagnosis: Check `rustc --print target-list`
- Solution: `rustup target add <triple>`
- Conditional: `#[cfg(target_os = "linux")]`

## CI/CD Optimization

**Caching Strategy**
```yaml
- name: Cache cargo registry
  uses: actions/cache@v3
  with:
    path: ~/.cargo/registry
    key: ${{ runner.os }}-cargo-registry-${{ hashFiles('**/Cargo.lock') }}
```

**Parallel Jobs**
```bash
# Default: Number of CPU cores
export CARGO_BUILD_JOBS=4

# Measure optimal concurrency
hyperfine -N 'cargo build -j 1' 'cargo build -j 2' 'cargo build -j 4'
```

**Artifact Management**
```bash
# Save compiled dependencies
cargo build --release

# Strip debug symbols (80% size reduction)
strip target/release/memory-mcp

# Verify binary
ldd target/release/memory-mcp
./target/release/memory-mcp --version
```

## Verification Checklist

- [ ] Build completes without errors
- [ ] No clippy warnings (`cargo clippy -- -D warnings`)
- [ ] Tests compile (`cargo test --no-run`)
- [ ] Binary size acceptable (< 10MB stripped)
- [ ] Startup time < 100ms
- [ ] No memory leaks (valgrind/check)
- [ ] Cross-platform targets build successfully

## Common Workflows

**Full CI Pipeline**
```bash
#!/usr/bin/env bash
set -euxo pipefail
cargo fmt --all -- --check
cargo clippy --all -- -D warnings
cargo build --release --workspace
cargo test --all
cargo doc --no-deps
```

**Quick Development Cycle**
```bash
#!/usr/bin/env bash
cargo check -p memory-core
cargo test -p memory-core --lib
cargo build -p memory-core
```

**Production Release**
```bash
#!/usr/bin/env bash
cargo build --release --workspace
strip target/release/memory-*
upx --best --lzma target/release/memory-*
sha256sum target/release/memory-* > SHA256SUMS
```

## Troubleshooting

**Issue**: Incremental compilation cache corruption
**Fix**: `cargo clean && cargo build`

**Issue**: Stale lock file
**Fix**: `rm Cargo.lock && cargo generate-lockfile`

**Issue**: Rust version mismatch
**Fix**: `rustup update stable && rustup default stable`

**Issue: Cross-compilation failures
**Fix**: Install toolchain: `rustup target add x86_64-unknown-linux-musl`

## Related Skills

- **code-quality**: Lint and format checks before builds
- **test-runner**: Execute tests after successful compilation
- **debug-troubleshoot**: Diagnose runtime issues post-build
- **github-workflows**: CI/CD pipeline integration
