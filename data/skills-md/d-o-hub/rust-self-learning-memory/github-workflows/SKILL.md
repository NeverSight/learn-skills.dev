---
name: github-workflows
description: Diagnose, fix, and optimize GitHub Actions workflows for Rust projects. Use when setting up CI/CD, troubleshooting workflow failures, optimizing build times, or ensuring best practices.
---

# GitHub Workflows

Diagnose, fix, and optimize GitHub Actions workflows for Rust projects.

## Quick Reference

- **[Caching Strategies](caching-strategies.md)** - Manual cache, rust-cache, sccache
- **[Troubleshooting](troubleshooting.md)** - Common issues, debugging, fixes
- **[Advanced Features](advanced-features.md)** - Coverage, security, benchmarking
- **[Release Management](release-management.md)** - Automated releases, versioning

## When to Use

- Setting up CI/CD for Rust projects
- Troubleshooting workflow failures
- Optimizing build times with caching
- Ensuring best practices for testing, linting, releases

## Before Making Changes

**ALWAYS verify current state first:**

```bash
# Get repo info
gh repo view --json nameWithOwner,owner,name

# List existing workflows
gh workflow list

# Check recent runs
gh run list --limit 10

# View workflow files
ls -la .github/workflows/
```

## Complete Rust CI Workflow

See the full workflow template with:
- Check job (format, clippy, check)
- Test job (unit, integration, doc tests)
- Coverage job (tarpaulin, codecov)
- Audit job (security, licenses)

See linked files for caching strategies, troubleshooting, and release management.

## Core Workflow Components

| Job | Purpose | Tools |
|-----|---------|-------|
| check | Code quality | rustfmt, clippy, cargo check |
| test | Verification | cargo test |
| coverage | Test metrics | cargo tarpaulin |
| audit | Security | cargo audit, deny |

## Common Patterns

- **Caching**: Dependencies, target directory, sccache
- **Matrix builds**: Multiple Rust versions, targets
- **Conditional jobs**: Skip on docs-only changes
- **Quality gates**: Block merge on failures
