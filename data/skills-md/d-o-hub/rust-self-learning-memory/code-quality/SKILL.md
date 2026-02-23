---
name: code-quality
description: Maintain high code quality through formatting, linting, and static analysis. Use code-quality skill and scripts for rustfmt, clippy, or cargo audit.
---

# Code Quality

Use the code-quality scripts for all operations.

## Usage

```bash
# Format check (fast)
./scripts/code-quality.sh fmt

# Lint with clippy
./scripts/code-quality.sh clippy

# Security audit
./scripts/code-quality.sh audit

# Run all quality gates
./scripts/code-quality.sh check

# Auto-fix common issues
./scripts/code-quality.sh clippy --fix
```

## Quality Gates

| Check | Command |
|-------|---------|
| Format | `cargo fmt --all -- --check` |
| Lint | `cargo clippy --all -- -D warnings` |
| Audit | `cargo audit` |
| Full | `./scripts/quality-gates.sh` |
| Coverage | `cargo llvm-cov --html --output-dir coverage` |
| Docs | `cargo doc --no-deps` |

## Rust Quality Dimensions

| Dimension | Focus | Check |
|-----------|-------|-------|
| Structure | Files <500 LOC, module hierarchy | `find . -name "*.rs" -exec wc -l {} +` |
| Error Handling | Custom Error, Result<T>, no unwrap | `rg "unwrap()" --glob "*.rs" --glob "!*/tests/*"` |
| Async Patterns | async fn, spawn_blocking, no blocking | `rg "async fn\|spawn_blocking" --glob "*.rs"` |
| Testing | >90% coverage, integration tests | `cargo llvm-cov` |
| Documentation | Public APIs 100% documented | `cargo doc --no-deps` |

## Rust-Specific Anti-Patterns

- **Excessive Clone**: Use borrowing or Arc
- **Unnecessary Unwrap**: Use `?` operator
- **Deep Nesting**: Extract methods to flatten
- **Large Functions**: Split into smaller functions (< 50 LOC)
- **Deadlocks**: Release locks before `.await`

## Best Practices Checklist

- [ ] Files <500 LOC
- [ ] Clear module hierarchy
- [ ] Custom Error enum with Result<T>
- [ ] No unwrap() in production code
- [ ] async fn for IO operations
- [ ] spawn_blocking for CPU work
- [ ] >90% test coverage
- [ ] Public APIs documented
- [ ] SOLID principles applied
- [ ] No code duplication (DRY)

## Dependency Monitoring (ADR-036)

Track duplicate dependency count as a quality metric:

```bash
# Count duplicate dependency roots (target: < 100)
cargo tree -d | grep -cE "^[a-z]"

# Find unused dependencies
cargo install --locked cargo-machete cargo-shear
cargo machete
cargo shear

# Find unused features
cargo install --locked cargo-unused-features
cargo unused-features analyze
```

## References

- [ADR-036: Dependency Deduplication](../../../plans/adr/ADR-036-Dependency-Deduplication.md)
- [ADR-032: Disk Space Optimization](../../../plans/adr/ADR-032-Disk-Space-Optimization.md)

Consolidated from these former skills (preserved in `_consolidated/`):
- `rust-code-quality` — Rust-specific quality dimensions, analysis commands, report format
- `clean-code-developer` — SOLID principles, refactoring techniques, anti-patterns
