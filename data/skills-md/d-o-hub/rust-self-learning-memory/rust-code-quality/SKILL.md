---
name: rust-code-quality
description: Perform comprehensive Rust code quality reviews against best practices for async Rust, error handling, testing, and project structure
---

# Rust Code Quality Review

Systematically review Rust code quality against best practices.

## Quality Dimensions

| Dimension | Focus | Tools |
|-----------|-------|-------|
| Structure | Files <500 LOC, module hierarchy | `find . -name "*.rs"` |
| Error Handling | Custom Error, Result<T>, no unwrap | `rg "unwrap\|Result<"` |
| Async Patterns | async fn, spawn_blocking, no blocking | `rg "async fn\|spawn_blocking"` |
| Testing | >90% coverage, integration tests | `cargo tarpaulin` |
| Documentation | Public APIs 100% documented | `cargo doc --no-deps` |

## Analysis Commands

```bash
# Project structure
find . -name "*.rs" -not -path "*/target/*" -exec wc -l {} + | sort -rn

# Error handling
rg "unwrap\(\)" --glob "!*/tests/*" --glob "*.rs"

# Async patterns
rg "async fn|spawn_blocking|tokio::" --glob "*.rs"

# Testing
cargo test --all
cargo tarpaulin --out Html

# Linting
cargo fmt -- --check
cargo clippy --all -- -D warnings
cargo audit
```

## Output Format

```markdown
# Rust Code Quality Report

## Summary
- **Score**: X/100
- **Critical Issues**: N
- **Warnings**: M

## By Dimension
- Structure: X/10 - [Status]
- Error Handling: X/10 - [Status]
- Async Patterns: X/10 - [Status]
- Testing: X/10 - [Status]
- Documentation: X/10 - [Status]

## Critical Issues
1. [Issue] - File:line
   - Fix: [Recommendation]

## Action Items
### High Priority
- [ ] Fix critical issues

### Medium Priority
- [ ] Address warnings
```

## Best Practices Checklist

✓ Files <500 LOC
✓ Clear module hierarchy
✓ Custom Error enum
✓ Result<T> for fallible ops
✓ No unwrap() in production
✓ async fn for IO operations
✓ spawn_blocking for CPU work
✓ >90% test coverage
✓ Public APIs documented
