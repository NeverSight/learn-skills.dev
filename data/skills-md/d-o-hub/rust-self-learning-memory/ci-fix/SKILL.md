---
name: ci-fix
description: Diagnose and fix GitHub Actions CI failures for Rust projects. Use when CI fails, tests timeout, or linting issues occur. Captures common patterns from CLAUDE_INSIGHTS_REPORT.md.
---

# CI Fix Skill

Diagnose and fix GitHub Actions CI failures using patterns from past CI issues.

## Quick Diagnosis Pattern

1. Get CI status:
```bash
gh run list --limit 5 --json status,conclusion,name,headBranch
```

2. Get failed job logs:
```bash
gh run view <run_id> --log --job <job_name>
```

3. Categorize failure:
- **lint**: fmt/clippy warnings
- **test**: test failures or timeouts
- **build**: compilation errors
- **security**: cargo audit/deny failures
- **coverage**: coverage threshold missed
- **deprecated**: old action versions (common!)

## Common Fixes (From History)

### Deprecated GitHub Actions
```bash
# Detect
grep -r "actions/checkout@v1" .github/workflows/
grep -r "actions-rs" .github/workflows/

# Fix: Update to v2+
```

### Optional Dependency Issues (libclang, wasmtime)
```bash
# Pattern: --all-features triggered optional dep issues
# Fix: Use workspace exclude
cargo build --workspace --exclude memory-mcp
```

### Clippy Lint Allow-List
```bash
# See new warnings
cargo clippy --all -- -D warnings | grep "warning:"

# Fix: Add #[allow(...)] comments
```

### Coverage Threshold
```bash
# Generate coverage
cargo tarpaulin --workspace

# Check threshold in .github/workflows/
```

### Benchmark Timeout
```bash
# Increase timeout-minutes in workflow YAML
```

## Fix Commands

```bash
# Linting
cargo fmt --all
cargo clippy --workspace --fix --allow-dirty

# Testing
cargo test --workspace -- --nocapture

# Security
cargo audit
cargo deny check

# Build
cargo build --workspace
```

## Success Criteria
- All CI jobs pass
- No new warnings introduced
- Changes committed if needed
