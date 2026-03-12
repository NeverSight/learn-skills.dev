---
name: dead-code-check
description: Generates dead code detection configurations for loom plan verification. Provides language-specific commands, fail patterns, and ignore patterns for Rust, TypeScript, Python, Go, and JavaScript. Use when adding code quality checks to acceptance criteria or truths fields in loom plans. Dead code detection catches incomplete wiring by identifying code that exists but is never called.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
trigger-keywords: dead code, dead-code, unused code, unused imports, unused functions, orphaned code, dead code detection, dead code check, code cleanup, unused variables, unreachable code, wiring verification
---

# Dead Code Detection

## Overview

Dead code detection identifies code that exists in your codebase but is never called, imported, or used. This is a critical signal for incomplete feature integration: if you've written a function but nothing calls it, the feature isn't wired up.

In loom plan verification, dead code checks serve two purposes:

1. **Wiring verification**: Catch features that were implemented but never integrated
2. **Code quality**: Identify cleanup opportunities and reduce maintenance burden

Dead code detection is especially valuable in **integration-verify stages**, where it acts as a final check that all implemented code is actually connected to the application.

## When to Use

- **integration-verify stages**: Final quality gate to catch orphaned code from all implementation stages
- **Per-stage acceptance criteria**: Immediate feedback during implementation
- **Code cleanup**: After refactoring or feature removal
- **Wiring validation**: Combine with wiring checks to verify feature integration

If dead code exists after implementation, it typically means:

- Feature wasn't wired into the application (CLI command not registered, route not mounted, etc.)
- Test code that isn't being run
- Leftover code from refactoring
- Incomplete implementation

## Language-Specific Configurations

### Rust

Rust has built-in dead code detection via the compiler and clippy.

**Recommended Approach: Use clippy with all warnings as errors**

```bash
cargo clippy -- -D warnings
```

This catches dead code plus many other issues (unused imports, variables, etc.).

**Dead-Code-Specific Check:**

```bash
RUSTFLAGS="-D dead_code" cargo build 2>&1
```

Or target just dead code warnings:

```bash
cargo clippy -- -D dead_code
```

**Fail Patterns:**

- `warning: unused`
- `dead_code`
- `unused import`
- `unused variable`
- `never used`
- `never constructed`

**Ignore Patterns:**

- Code with `#[allow(dead_code)]` attribute (intentional)
- Test modules (`#[cfg(test)]`)
- Main entry points (`fn main()`)
- Public API items intended for external consumers
- Items behind feature gates that aren't enabled

**YAML Template for Loom Plans:**

```yaml
# In acceptance criteria (recommended - catches more than just dead code)
acceptance:
  - "cargo clippy -- -D warnings"

# In truths (more specific dead code check)
truths:
  - "RUSTFLAGS=\"-D dead_code\" cargo build 2>&1 | grep -v 'Compiling' | grep -v 'Finished' | grep -q '^$'"

# Alternative: Check that clippy reports zero dead code warnings
truths:
  - "! cargo clippy -- -D dead_code 2>&1 | grep -q 'warning:'"
```

**Working Directory Consideration:**

Rust checks must run where `Cargo.toml` exists. If your project structure is:

```text
.worktrees/my-stage/
└── loom/
    └── Cargo.toml
```

Set `working_dir: "loom"` in your stage configuration.

---

### TypeScript

TypeScript dead code detection uses **ts-prune**, which finds unused exports.

**Installation:**

```bash
npm install --save-dev ts-prune
# or
bun add --dev ts-prune
```

**Command:**

```bash
npx ts-prune --error
# or
bunx ts-prune --error
```

The `--error` flag makes ts-prune exit with non-zero status if unused exports are found.

**Fail Patterns:**

- `used in module but not exported`
- `unused export`
- Files with unused exports reported

**Ignore Patterns:**

- `index.ts` files that re-export (barrel files)
- Type-only exports used for type checking
- Declaration files (`.d.ts`)
- Public API exports intended for library consumers
- Default exports in entry points

**Configuration File (`.tsprunerc`):**

```json
{
  "ignore": "index.ts|types.d.ts"
}
```

**YAML Template for Loom Plans:**

```yaml
# In acceptance criteria
acceptance:
  - "bunx ts-prune --error"

# In truths (verify zero unused exports)
truths:
  - "bunx ts-prune | wc -l | grep -q '^0$'"

# Alternative: Explicitly check for no unused exports
truths:
  - "! bunx ts-prune | grep -q 'used in module'"
```

**Working Directory:**

Run where `package.json` and `tsconfig.json` exist.

---

### Python

Python dead code detection uses **vulture**, which finds unused code including functions, classes, variables, and imports.

**Installation:**

```bash
pip install vulture
# or
uv add --dev vulture
```

**Command:**

```bash
vulture src/ --min-confidence 80
```

The `--min-confidence` flag (0-100) controls false positive rate. Higher values mean fewer false positives but might miss some dead code.

**Fail Patterns:**

- `unused function`
- `unused class`
- `unused variable`
- `unused import`
- `unreachable code`

**Ignore Patterns:**

- `__init__.py` files
- `__all__` definitions (explicit public API)
- Magic methods (`__str__`, `__repr__`, `__eq__`, etc.)
- Test files and fixtures (often use dynamic discovery)
- Setup.py and configuration files

**Configuration File (`pyproject.toml`):**

```toml
[tool.vulture]
min_confidence = 80
paths = ["src", "tests"]
ignore_names = ["setUp", "tearDown", "test_*"]
```

**YAML Template for Loom Plans:**

```yaml
# In acceptance criteria
acceptance:
  - "vulture src/ --min-confidence 80"

# In truths (verify zero issues)
truths:
  - "vulture src/ --min-confidence 80 | wc -l | grep -q '^0$'"

# Alternative: Check for specific patterns
truths:
  - "! vulture src/ --min-confidence 80 | grep -q 'unused function'"
  - "! vulture src/ --min-confidence 80 | grep -q 'unused import'"
```

**Working Directory:**

Run where your Python source code is (usually project root or where `pyproject.toml` exists).

---

### Go

Go dead code detection uses **staticcheck**, a comprehensive static analysis tool.

**Installation:**

```bash
go install honnef.co/go/tools/cmd/staticcheck@latest
```

**Command:**

```bash
staticcheck ./...
```

**Relevant Checks:**

- `U1000` - unused code (function, type, const, var)
- `U1001` - unused field

**Fail Patterns:**

- `is unused`
- `field .* is unused`
- `func .* is unused`
- `U1000` check code
- `U1001` check code

**Ignore Patterns:**

- Exported symbols in library packages (public API)
- Interface method implementations (required by interface even if not directly called)
- Functions assigned to variables for use via reflection
- Code behind build tags not currently enabled

**Configuration File (`.staticcheck.conf`):**

```text
checks = ["all", "-ST1000"]
```

**YAML Template for Loom Plans:**

```yaml
# In acceptance criteria
acceptance:
  - "staticcheck ./..."

# In truths (verify no unused code)
truths:
  - "! staticcheck ./... | grep -q 'U1000'"
  - "! staticcheck ./... | grep -q 'is unused'"

# Alternative: Check exit code
truths:
  - "staticcheck ./... 2>&1 | wc -l | grep -q '^0$'"
```

**Working Directory:**

Run where `go.mod` exists (usually project root).

---

### JavaScript

JavaScript dead code detection uses **unimported**, which finds unused files and unresolved imports.

**Installation:**

```bash
npm install --save-dev unimported
# or
bun add --dev unimported
```

**Command:**

```bash
npx unimported
# or
bunx unimported
```

**Fail Patterns:**

- `unresolved import`
- `unused file`
- Files listed in output

**Ignore Patterns:**

- Config files (`.eslintrc.js`, `jest.config.js`, etc.)
- Entry points (`index.js`, `main.js`)
- Dynamic imports using variables
- Files imported via build tools (Webpack, Vite, etc.)

**Configuration File (`.unimportedrc.json`):**

```json
{
  "entry": ["src/index.js", "src/server.js"],
  "extensions": [".js", ".jsx"],
  "ignorePatterns": ["**/node_modules/**", "**/*.config.js"]
}
```

**YAML Template for Loom Plans:**

```yaml
# In acceptance criteria
acceptance:
  - "bunx unimported"

# In truths (verify no unused files)
truths:
  - "bunx unimported | wc -l | grep -q '^0$'"

# Alternative: Check for specific issues
truths:
  - "! bunx unimported | grep -q 'unused file'"
  - "! bunx unimported | grep -q 'unresolved import'"
```

**Working Directory:**

Run where `package.json` exists.

---

## Handling False Positives

Dead code detection tools report false positives in these common scenarios:

### 1. Entry Points

**Problem:** Main functions, CLI handlers, API route handlers — nothing in your code calls them directly, but they're invoked by the runtime/framework.

**Solutions:**

- **Rust**: Entry points like `fn main()` are automatically excluded. For CLI subcommands, ensure they're registered in the command enum.
- **TypeScript/JavaScript**: Configure entry points in tool config (ts-prune, unimported)
- **Python**: Use `__all__` to mark public API, vulture respects it
- **Go**: Exported functions in `main` package are excluded

### 2. Test Code

**Problem:** Test functions are called by the test runner, not by application code.

**Solutions:**

- **Rust**: Code in `#[cfg(test)]` modules is automatically excluded
- **TypeScript/JavaScript**: Exclude test directories in config
- **Python**: Ignore patterns like `test_*`, `setUp`, `tearDown`
- **Go**: Test files (`*_test.go`) are automatically handled

### 3. Framework Magic

**Problem:** Decorators, derive macros, annotations that use code implicitly.

**Examples:**

- Rust: `#[derive(Serialize)]` uses private fields
- Python: `@dataclass`, `@property` decorators
- TypeScript: Decorators in frameworks like Angular, NestJS

**Solutions:**

- Use language-specific ignore annotations
- Configure tools to ignore decorated items
- For Rust, use `#[allow(dead_code)]` on specific items

### 4. Public API / Library Code

**Problem:** Code exported for external consumers appears unused within the project.

**Solutions:**

- **Rust**: Public items (`pub`) in library crates are excluded by default
- **TypeScript**: Use `.tsprunerc` to ignore library entry points
- **Python**: Define `__all__` to mark public API
- **Go**: Exported symbols (capitalized) in library packages are excluded

### 5. Feature Flags and Conditional Compilation

**Problem:** Code behind disabled feature flags or build tags.

**Solutions:**

- **Rust**: Enable relevant features when running checks (`--features=all`)
- **Go**: Use build tags to include all variants
- **Python/TypeScript/JavaScript**: Comment or temporarily enable features during checks

### 6. Dynamic Loading and Reflection

**Problem:** Code loaded dynamically or invoked via reflection.

**Solutions:**

- Document these cases clearly
- Use tool-specific ignore comments
- Consider integration tests that exercise dynamic code paths

---

## Integration with Loom Plans

### Placement in Plan Stages

**Best Practice: integration-verify stage**

Dead code checks are most valuable as a final quality gate:

```yaml
stages:
  - id: integration-verify
    name: "Integration Verification"
    stage_type: integration-verify
    working_dir: "loom"
    acceptance:
      - "cargo test"
      - "cargo clippy -- -D warnings" # Includes dead code check
    truths:
      - "! cargo clippy -- -D dead_code 2>&1 | grep -q 'warning:'"
```

**Per-Stage Checks:**

Can also add to individual implementation stages for immediate feedback:

```yaml
stages:
  - id: implement-auth
    name: "Implement Authentication"
    stage_type: standard
    working_dir: "loom"
    acceptance:
      - "cargo test auth"
      - "cargo clippy --package auth -- -D warnings"
```

### Combining with Wiring Checks

Dead code detection is a strong signal but not definitive proof. Combine with `wiring` checks:

```yaml
stages:
  - id: integration-verify
    name: "Integration Verification"
    stage_type: integration-verify
    working_dir: "loom"
    acceptance:
      - "cargo clippy -- -D warnings"
    wiring:
      - source: "src/main.rs"
        pattern: "Commands::NewCommand"
        description: "New command registered in CLI enum"
      - source: "src/commands/mod.rs"
        pattern: "pub mod new_command"
        description: "New command module exported"
    truths:
      - "loom new-command --help" # Functional verification
```

This triple-check approach (dead code + wiring + functional) catches integration issues reliably.

### Working Directory and Paths

**Critical Reminder:** The `working_dir` field determines where commands execute.

Example project structure:

```text
.worktrees/my-stage/
├── loom/
│   ├── Cargo.toml       <- Build tools expect this directory
│   └── src/
└── CLAUDE.md
```

**Correct Configuration:**

```yaml
- id: verify
  working_dir: "loom" # Where Cargo.toml exists
  acceptance:
    - "cargo clippy -- -D warnings"
  truths:
    - "test -f src/new_feature.rs" # Relative to working_dir (loom/)
```

**Wrong Configuration:**

```yaml
- id: verify
  working_dir: "." # Wrong - no Cargo.toml here
  acceptance:
    - "cargo clippy -- -D warnings" # FAILS: could not find Cargo.toml
```

**Path Resolution Rule:** ALL paths in acceptance, truths, artifacts, and wiring are relative to `working_dir`.

---

## YAML Best Practices

### Never Use Triple Backticks in YAML Descriptions

**Wrong:**

````yaml
truths:
  - description: |
      Check for dead code like this:
      ```
      cargo clippy -- -D warnings
      ```
    command: "cargo clippy -- -D warnings"
````

This breaks YAML parsing.

**Correct:**

```yaml
truths:
  - "cargo clippy -- -D warnings" # Check for dead code
```

Or with explicit description:

```yaml
truths:
  - description: "Check for dead code using clippy with all warnings as errors"
    command: "cargo clippy -- -D warnings"
```

### Silent Grep with -q

When using `grep` in truths, use `-q` (quiet) flag to suppress output:

```yaml
truths:
  - "! cargo clippy -- -D dead_code 2>&1 | grep -q 'warning:'"
```

The `!` negates the result (exit 0 if grep finds nothing).

### Exit Code Checks

Tools that exit non-zero on finding issues can be used directly:

```yaml
acceptance:
  - "cargo clippy -- -D warnings" # Exits non-zero on warnings
  - "staticcheck ./..." # Exits non-zero on issues
  - "bunx ts-prune --error" # Exits non-zero on unused exports
```

---

## Tool Installation Checklist

Before adding dead code checks to your plan, ensure tools are available:

**Rust:**

- Built-in: `rustc`, `cargo`
- `cargo install clippy` (usually included with rustup)

**TypeScript:**

- `bun add --dev ts-prune` or `npm install --save-dev ts-prune`

**Python:**

- `uv add --dev vulture` or `pip install vulture`

**Go:**

- `go install honnef.co/go/tools/cmd/staticcheck@latest`

**JavaScript:**

- `bun add --dev unimported` or `npm install --save-dev unimported`

Add installation steps to your `knowledge-bootstrap` stage or document in project README.

---

## Examples

### Example 1: Rust Project with Comprehensive Checks

```yaml
stages:
  - id: integration-verify
    name: "Integration Verification"
    stage_type: integration-verify
    working_dir: "loom"
    acceptance:
      - "cargo test"
      - "cargo clippy -- -D warnings"
      - "cargo build --release"
    truths:
      - "test -f src/commands/new_feature.rs"
      - "! cargo clippy -- -D dead_code 2>&1 | grep -q 'warning:'"
    wiring:
      - source: "src/main.rs"
        pattern: "Commands::NewFeature"
        description: "New feature command registered"
```

### Example 2: TypeScript API with Dead Export Check

```yaml
stages:
  - id: verify-api
    name: "Verify API Implementation"
    stage_type: integration-verify
    working_dir: "api"
    acceptance:
      - "bun test"
      - "bunx ts-prune --error"
      - "bun run typecheck"
    truths:
      - "bunx ts-prune | wc -l | grep -q '^0$'"
      - "curl -f http://localhost:3000/api/health"
```

### Example 3: Python Data Pipeline

```yaml
stages:
  - id: verify-pipeline
    name: "Verify Data Pipeline"
    stage_type: integration-verify
    working_dir: "pipeline"
    acceptance:
      - "pytest"
      - "vulture src/ --min-confidence 80"
      - "mypy src/"
    truths:
      - "! vulture src/ --min-confidence 80 | grep -q 'unused function'"
      - "test -f src/pipeline/transform.py"
    wiring:
      - source: "src/main.py"
        pattern: "from pipeline.transform import TransformStage"
        description: "Transform stage imported in main pipeline"
```

### Example 4: Go Microservice

```yaml
stages:
  - id: verify-service
    name: "Verify Microservice"
    stage_type: integration-verify
    working_dir: "service"
    acceptance:
      - "go test ./..."
      - "staticcheck ./..."
      - "go build"
    truths:
      - "! staticcheck ./... | grep -q 'U1000'"
      - "! staticcheck ./... | grep -q 'is unused'"
      - "test -f cmd/server/main.go"
```

---

## Summary

Dead code detection is a powerful verification tool for loom plans:

1. **Catches incomplete wiring**: Code exists but isn't called = feature not integrated
2. **Language-specific tools**: Rust (clippy), TypeScript (ts-prune), Python (vulture), Go (staticcheck), JavaScript (unimported)
3. **Best in integration-verify**: Final quality gate after all implementation stages
4. **Combine with wiring checks**: Dead code detection + wiring patterns + functional tests = comprehensive verification
5. **Handle false positives**: Entry points, tests, framework magic — configure tools appropriately
6. **Working directory matters**: Set `working_dir` to where build tools expect (where Cargo.toml, package.json, go.mod exist)

Use this skill when designing verification strategies for loom plans. Copy-paste the YAML templates and adapt tool configurations to your project's structure.
