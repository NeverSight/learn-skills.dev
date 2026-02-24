---
name: rust
description: Use cargo for Rust development with check-first workflow. Prefer cargo check over cargo build, use debug builds for testing, AVOID release builds unless explicitly needed.
---
# Rust/Cargo Development Skill

You are a Rust development specialist using cargo and related tools. This skill provides comprehensive workflows, best practices, and common patterns for Rust development.

## IMPORTANT: Build Strategy

**AVOID expensive builds:**
- **DON'T** use `cargo build --release` or `cargo install --path .` (very slow)
- **DON'T** build unless necessary - use `cargo check` first
- **DO** use `cargo check` to verify compilation (fast, no codegen)
- **DO** use `cargo run` for iterative development and testing functionality (builds debug + runs in one command)
- **DO** use debug builds for testing binaries (`cargo build` without `--release`)

**Decision tree:**
1. **Just checking if code compiles?** → `cargo check` (fastest)
2. **Developing/testing functionality?** → `cargo run` (builds debug + runs - use this for iteration)
3. **Need the binary artifact without running?** → `cargo build` (debug)
4. **Need optimized performance?** → Only then use `cargo build --release` (slow)

## Standard Development Workflow

### Command Execution Order

Always follow this sequence when developing or validating Rust code:

```bash
cargo test --quiet
cargo check --quiet       # Fast compilation check (PREFER - no binary output)
cargo clippy
```

**IMPORTANT**: Use `cargo check`, NOT `cargo build`, for validation. Only use `cargo build` when you actually need the binary artifact.

**For iterative development and testing functionality:**
```bash
cargo run                 # Builds debug and runs (PREFERRED for development iteration)
cargo run -- arg1 arg2    # Pass arguments to test different scenarios
# OR
cargo build --quiet       # Only if you need the binary artifact without running it
```

**Rationale:**
1. **Tests first**: Catch logic errors early
2. **Check second**: Fast compilation verification without codegen
3. **Clippy third**: Address code quality and style issues
4. **Run/Build last**: Use `cargo run` to iterate on functionality, or `cargo build` if you need the artifact

### Timeout Settings

Rust commands can be long-running, especially for large projects:

```bash
# Standard timeout (2 minutes) - sufficient for most operations
cargo test --quiet
cargo check --quiet
cargo build --quiet      # Debug build
# timeout: 120000

# Extended timeout ONLY for release builds (10 minutes) - AVOID if possible
cargo build --release    # WARNING: Very slow, only use when explicitly needed
# timeout: 600000
```

**Best practice**: Use the standard 2-minute timeout for check/test/debug builds. Only use extended timeout if you absolutely must do a release build.

## Clippy - Linting and Code Quality

### Auto-fix Workflow

Always attempt automatic fixes first:

```bash
cargo clippy --fix --allow-dirty
```

**Flags:**
- `--fix`: Automatically apply suggested fixes
- `--allow-dirty`: Allow fixes even with uncommitted changes
- Implies `--no-deps` and `--all-targets`

### Clippy Strategies

#### 1. Distinguish Warning Types

Separate actionable issues from domain-appropriate patterns:

**Actionable bugs:**
- Logic errors
- Potential panics
- Memory safety issues
- API misuse

**Domain-appropriate suppressions:**
- Domain-specific patterns (e.g., `cast_possible_truncation` in Excel formula evaluators)
- False positives (e.g., `unused_assignments` for loop invariants)
- Documentation lints for internal tools (e.g., `missing_errors_doc`)
- Style preferences that don't affect correctness (e.g., `needless_pass_by_value`)

#### 2. Suppression Hierarchy

**Function-level suppression:**
```rust
#[allow(clippy::cast_possible_truncation)]
fn process_excel_value(val: u64) -> u32 {
    val as u32  // Domain: Excel row numbers are always < u32::MAX
}
```

**Module-level suppression** (top of file):
```rust
#![allow(clippy::missing_errors_doc)]
#![allow(clippy::cast_possible_truncation)]

// Rest of module code...
```

**Project-level suppression** (Cargo.toml):
```toml
[lints.clippy]
missing_errors_doc = "allow"
cast_possible_truncation = "allow"
needless_pass_by_value = "allow"
```

#### 3. Systematic Approach

1. Run `cargo clippy` to see all warnings
2. Run `cargo clippy --fix --allow-dirty` to auto-fix
3. Review remaining warnings and categorize:
   - **Fix**: Legitimate issues
   - **Suppress**: Domain-specific or false positives
4. Add strategic suppressions at appropriate level
5. Result: Only actionable warnings remain

### Common Clippy Lints to Consider

**Often suppressed in domain-specific code:**
- `cast_possible_truncation` - When domain guarantees safety
- `cast_sign_loss` - When values are known positive
- `missing_errors_doc` - Internal tools/libraries
- `missing_panics_doc` - When panics are domain-impossible
- `needless_pass_by_value` - API design choices
- `module_name_repetitions` - Sometimes necessary for clarity
- `too_many_lines` - Large but cohesive functions
- `unused_assignments` - Loop invariants and initialization patterns

**Generally should fix:**
- `redundant_closure` - Simplify code
- `unnecessary_unwrap` - Handle errors properly
- `manual_map` - Use iterator methods
- `match_same_arms` - Reduce duplication
- `needless_return` - Clean up style

### Explaining Lints

Get detailed information about any lint:

```bash
cargo clippy --explain <LINT_NAME>
```

### Command-line Lint Control

```bash
# Warn on specific lint
cargo clippy -- -W clippy::unwrap_used

# Deny specific lint (error)
cargo clippy -- -D clippy::unwrap_used

# Allow specific lint
cargo clippy -- -A clippy::needless_pass_by_value

# Forbid specific lint (cannot be overridden)
cargo clippy -- -F clippy::unwrap_used
```

## Common Cargo Commands

### Checking (Prefer This)

```bash
cargo check                    # Fast compilation check (PREFER THIS)
cargo check --quiet            # Suppress output
cargo check --all-targets      # Check all targets
```

**Use `cargo check` instead of `cargo build` when you just need to verify code compiles.**

### Building

```bash
cargo build                    # Debug build (use for testing binary)
cargo build --quiet            # Suppress output
cargo build --all-targets      # Build all targets (bins, libs, tests, benches)
cargo build --target <TARGET>  # Cross-compile for target

# AVOID unless explicitly needed (very slow):
cargo build --release          # Optimized release build (WARNING: SLOW)
```

### Testing

```bash
cargo test                     # Run all tests
cargo test --quiet             # Suppress output except failures
cargo test <NAME>              # Run specific test
cargo test --lib               # Test library only
cargo test --doc               # Test documentation examples
cargo test -- --nocapture      # Show println! output
cargo test -- --test-threads=1 # Run tests serially
```

### Running

```bash
cargo run                      # Run default binary (debug build)
cargo run --bin <NAME>         # Run specific binary
cargo run --example <NAME>     # Run example
cargo run -- <ARGS>            # Pass arguments to binary

# AVOID unless you need optimized performance (very slow to build):
cargo run --release            # Run optimized build (WARNING: SLOW)
```

### Documentation

```bash
cargo doc                      # Build documentation
cargo doc --open               # Build and open in browser
cargo doc --no-deps            # Only document this crate
```

### Dependency Management

```bash
cargo add <CRATE>              # Add dependency
cargo add <CRATE>@<VERSION>    # Add specific version
cargo add --dev <CRATE>        # Add dev dependency
cargo remove <CRATE>           # Remove dependency
cargo update                   # Update dependencies in Cargo.lock
cargo update <CRATE>           # Update specific dependency
```

### Project Management

```bash
cargo new <NAME>               # Create new binary project
cargo new --lib <NAME>         # Create new library project
cargo init                     # Initialize in current directory
cargo clean                    # Remove target directory
```

### Publishing and Package Info

```bash
cargo search <QUERY>           # Search crates.io
cargo publish                  # Publish to crates.io
cargo package                  # Create distributable package
cargo tree                     # Show dependency tree
```

## Process Management

### Cleaning Up Background Processes

Cargo can leave processes running that cause "resource busy" or lock errors:

```bash
pkill -f cargo
```

Use this before running cargo commands if you encounter:
- "resource busy" errors
- Cargo.lock contention
- Build hanging
- File lock errors

### Common Lock Issues

**Problem**: Multiple cargo processes fighting for Cargo.lock

**Solution**:
```bash
pkill -f cargo
cargo clean
cargo build
```

## Configuration Best Practices

### Cargo.toml Comments

Place comments on separate lines, not inline:

**Correct:**
```toml
# This dependency is used for CLI parsing
clap = "4.0"

# Linting configuration
[lints.clippy]
# Suppress in domain where values are guaranteed valid
cast_possible_truncation = "allow"
```

**Incorrect:**
```toml
clap = "4.0"  # This may cause parsing errors
cast_possible_truncation = "allow"  # Don't do this
```

### Lint Configuration Structure

```toml
[lints.clippy]
# Code quality - generally enforce
unwrap_used = "warn"
expect_used = "warn"

# Domain-specific allowances
cast_possible_truncation = "allow"
missing_errors_doc = "allow"

# Style preferences
needless_pass_by_value = "allow"
module_name_repetitions = "allow"
```

## Complete Development Workflows

### Workflow 1: New Feature Development

```bash
# 1. Create feature branch (outside cargo)
git checkout -b feature/new-thing

# 2. Develop code
# ... edit files ...

# 3. Run full validation sequence
cargo test --quiet
cargo check --quiet       # Use check, not build, for validation
cargo clippy

# 4. Auto-fix clippy warnings
cargo clippy --fix --allow-dirty

# 5. Re-run validation
cargo test --quiet
cargo check --quiet
cargo clippy

# 6. Commit changes
git add .
git commit -m "Add new feature"
```

### Workflow 2: Fixing Clippy Warnings

```bash
# 1. See all warnings
cargo clippy

# 2. Auto-fix what's possible
cargo clippy --fix --allow-dirty

# 3. Review remaining warnings
cargo clippy

# 4. For domain-specific warnings, add suppressions
# Edit Cargo.toml [lints.clippy] section or add #[allow(...)]

# 5. Verify clean clippy
cargo clippy

# 6. Ensure tests still pass
cargo test --quiet
```

### Workflow 3: Debugging Build Issues

```bash
# 1. Clean build artifacts
cargo clean

# 2. Kill any stuck processes
pkill -f cargo

# 3. Check compilation only (faster)
cargo check

# 4. Full build with verbose output
cargo build --verbose

# 5. If still failing, check with different targets
cargo check --lib
cargo check --tests
```

### Workflow 4: Dependency Updates

```bash
# 1. Check current dependency tree
cargo tree

# 2. Update all dependencies
cargo update

# 3. Or update specific dependency
cargo update serde

# 4. Validate after update
cargo test --quiet
cargo check --quiet       # Use check, not build, for validation
cargo clippy

# 5. Review Cargo.lock changes
git diff Cargo.lock
```

### Workflow 5: Pre-commit Validation

```bash
# Complete validation before committing (PREFER THIS)
cargo test --quiet && cargo check --quiet && cargo clippy

# If any step fails, the sequence stops
# Fix issues and repeat

# NOTE: Only use cargo build instead of cargo check if you actually need
# the binary artifact. For validation, cargo check is sufficient and much faster.
```

## Performance Optimization

### Build Performance

```bash
# Use cargo check for fast iteration (PREFER THIS)
cargo check

# Parallel builds (default, but can tune)
cargo build -j 8

# Use cache-friendly flags (ONLY for actual releases)
cargo build --release --locked  # WARNING: SLOW - only for production releases
```

**Development tip**: `cargo check` is 2-10x faster than `cargo build` and sufficient for most development.

### Test Performance

```bash
# Run only unit tests (fast)
cargo test --lib

# Skip slow integration tests
cargo test --lib --bins

# Run specific test module
cargo test module_name::
```

## Common Patterns and Tips

### Pattern 1: Iterative Development

```bash
# Fast check loop
cargo check
# ... fix errors ...
cargo check
# ... fix more ...
cargo test --quiet  # when ready to validate
```

### Pattern 2: Release Preparation (ONLY for actual releases)

**WARNING**: Only use this workflow when preparing an actual release. For regular development, use the check-first workflow.

```bash
# Full validation for release (SLOW - only for actual releases)
cargo test
cargo test --release        # WARNING: SLOW
cargo build --release       # WARNING: VERY SLOW
cargo clippy -- -D warnings  # Deny all warnings
cargo doc --no-deps
```

**For regular development**, use instead:
```bash
cargo test --quiet
cargo check --quiet
cargo clippy
```

### Pattern 3: Multi-target Projects

```bash
# Check everything
cargo check --all-targets
cargo test --all-targets
cargo clippy --all-targets
```

### Pattern 4: Documentation Testing

```bash
# Test code examples in docs
cargo test --doc

# Build and review docs
cargo doc --open
```

## Error Handling

### Common Issues and Solutions

**Issue**: "could not compile due to previous error"
```bash
# Solution: Check specific error, may need cargo clean
cargo clean
cargo build
```

**Issue**: "waiting for file lock on package cache"
```bash
# Solution: Kill stuck processes
pkill -f cargo
```

**Issue**: Clippy warnings overwhelming
```bash
# Solution: Auto-fix first, then strategic suppression
cargo clippy --fix --allow-dirty
# Review remaining, add suppressions as needed
```

**Issue**: Tests passing but clippy failing
```bash
# Solution: This is normal - fix clippy issues or suppress appropriately
cargo clippy --fix --allow-dirty
# Then review and add strategic suppressions
```

## Quick Reference

```bash
# Development cycle (PREFER - use check for validation)
cargo test --quiet && cargo check --quiet && cargo clippy

# Auto-fix clippy
cargo clippy --fix --allow-dirty

# Clean and re-check
pkill -f cargo && cargo clean && cargo check

# Update dependencies
cargo update && cargo test --quiet && cargo check --quiet

# Documentation
cargo doc --open

# Add dependency
cargo add <crate>

# Fast iteration (just checking compilation)
cargo check

# Only build when you need the binary artifact
cargo build
```

## Integration with Git

After validation, use the git commit message writer agent:
- Captures comprehensive commit context
- Follows project conventions
- Professional, human-written style (no AI attribution per CLAUDE.md)

```bash
# After cargo validation passes:
git add .
# Then request commit (use commit message writer agent)
```
