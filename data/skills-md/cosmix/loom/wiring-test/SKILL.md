---
name: wiring-test
description: Generates wiring verification YAML for loom plans. Helps agents prove that features are properly integrated — commands registered, endpoints mounted, modules exported, components rendered. Use when writing truths/artifacts/wiring fields for loom plan stages.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
trigger-keywords: wiring, wiring-test, wiring test, integration test, integration verification, verify wiring, prove integration, command registered, endpoint mounted, module exported
---

# Wiring Test Skill

## Overview

**The Problem:** Tests can pass, code can compile, but the feature may never be wired up — command not registered, endpoint not mounted, module not imported, component never rendered. This is a common failure mode in integration.

**The Solution:** Wiring verification proves integration through three types of evidence:

1. **Truths** — Observable behaviors (shell commands returning exit 0)
2. **Artifacts** — Files that must exist with real implementation (not just empty files)
3. **Wiring** — Code patterns proving connection points (imports, registrations, mounts)

This skill helps you write strong `truths`, `artifacts`, and `wiring` fields for loom plan stage YAML metadata.

## When to Use

- When writing loom plan stages (especially `integration-verify` stages)
- When verifying that a feature is actually integrated into the application
- When reviewing acceptance criteria to ensure they prove functional integration
- When debugging why a "passing" feature doesn't work in practice

## Wiring YAML Format Reference

Loom plans use three verification fields to prove integration:

```yaml
truths:
  - "command-that-proves-behavior"
  - "another-observable-check"

artifacts:
  - "path/to/implementation.rs"
  - "path/to/another/file.ts"

wiring:
  - source: "path/to/integration/point.rs"
    pattern: "mod feature_name"
    description: "Feature module is imported in main"
  - source: "path/to/router.rs"
    pattern: "mount_feature_routes"
    description: "Feature routes are mounted in router"
```

**CRITICAL PATH RULE:** All paths (`artifacts`, `wiring.source`) are relative to the stage's `working_dir` field. If `working_dir: "loom"`, then paths resolve from inside the `loom/` directory.

**YAML SYNTAX WARNING:** NEVER put triple backticks inside YAML `description` fields. Use plain indented text for code examples instead.

## Templates by Feature Type

### CLI Command

For a new CLI command (e.g., `loom verify <stage-id>`):

```yaml
truths:
  - "loom verify --help"  # Command responds
  - "loom verify stage-1 --suggest"  # Primary use case works

artifacts:
  - "src/commands/verify.rs"  # Implementation exists
  - "src/verify/mod.rs"  # Supporting module exists

wiring:
  - source: "src/main.rs"
    pattern: "mod commands"
    description: "Commands module imported"
  - source: "src/commands/mod.rs"
    pattern: "pub mod verify"
    description: "Verify command exported"
  - source: "src/main.rs"
    pattern: "Commands::Verify"
    description: "Verify variant in CLI enum"
```

**Path Context:** If `working_dir: "loom"`, these paths resolve to `loom/src/commands/verify.rs`, etc.

### API Endpoint

For a REST endpoint (e.g., `POST /api/features`):

```yaml
truths:
  - "curl -f -X POST http://localhost:8080/api/features -d '{\"name\":\"test\"}'"
  - "curl -f http://localhost:8080/api/features | grep -q '\"features\"'"

artifacts:
  - "src/handlers/features.rs"
  - "src/routes/api.rs"

wiring:
  - source: "src/routes/api.rs"
    pattern: "post(\"/features\", create_feature)"
    description: "POST /features route registered"
  - source: "src/main.rs"
    pattern: "mount(\"/api\", api_routes())"
    description: "API routes mounted in application"
  - source: "src/handlers/mod.rs"
    pattern: "pub mod features"
    description: "Features handler exported"
```

**Note:** Functional check (curl) proves endpoint is reachable, not just that tests pass.

### Module/Library

For a new internal module (e.g., authentication module):

```yaml
truths:
  - "cargo test auth::"  # Module tests pass
  - "cargo check"  # Module compiles in context

artifacts:
  - "src/auth/mod.rs"
  - "src/auth/jwt.rs"
  - "src/auth/session.rs"

wiring:
  - source: "src/lib.rs"
    pattern: "pub mod auth"
    description: "Auth module exported from library root"
  - source: "src/main.rs"
    pattern: "use crate::auth"
    description: "Auth module imported in main"
```

### UI Component

For a React/Vue component (e.g., `FeatureCard`):

```yaml
truths:
  - "npm test -- FeatureCard"  # Component tests pass
  - "npm run build"  # Component compiles

artifacts:
  - "src/components/FeatureCard.tsx"
  - "src/components/FeatureCard.test.tsx"

wiring:
  - source: "src/components/index.ts"
    pattern: "export { FeatureCard }"
    description: "FeatureCard exported from components barrel"
  - source: "src/pages/Dashboard.tsx"
    pattern: "<FeatureCard"
    description: "FeatureCard rendered in Dashboard"
  - source: "src/pages/Dashboard.tsx"
    pattern: "import.*FeatureCard"
    description: "FeatureCard imported in parent component"
```

## Good vs Bad Examples

### Bad: Too Broad

```yaml
truths:
  - "cargo test"  # Only proves tests pass, not that feature works
  - "cargo build"  # Only proves it compiles

artifacts:
  - "src/"  # Too broad, proves nothing

wiring: []  # Missing — no integration proof
```

**Problem:** These checks don't prove the feature is wired up or functional. Tests can pass even if the feature is never registered/mounted/imported.

### Good: Specific and Functional

```yaml
truths:
  - "loom verify stage-1 --suggest"  # Proves verify command works end-to-end
  - "loom verify --help | grep -q 'suggest'"  # Proves --suggest flag exists

artifacts:
  - "src/commands/verify.rs"  # Implementation file
  - "src/verify/checker.rs"  # Core logic file

wiring:
  - source: "src/main.rs"
    pattern: "Commands::Verify"
    description: "Verify command variant in CLI enum"
  - source: "src/commands/mod.rs"
    pattern: "pub mod verify"
    description: "Verify module exported from commands"
  - source: "src/commands/verify.rs"
    pattern: "run_verification"
    description: "Core verification function exists"
```

**Why Better:**

- Truths prove the actual command works (not just tests)
- Artifacts prove specific implementation files exist
- Wiring proves the command is registered in the CLI and exposed correctly

## Refinement Questions

Before finalizing your wiring verification, ask yourself:

### Truths

1. **What exact command/endpoint/import will the user invoke?**
   - Not "tests pass" but "the actual feature responds"
2. **What output proves it's working (not just "no error")?**
   - Look for specific output, exit codes, or behaviors
3. **Can I test the primary use case end-to-end?**
   - Don't just check `--help`, actually run the feature

### Artifacts

1. **What files MUST exist for the feature to function?**
   - Not just directories or test files, but actual implementation
2. **Are these paths relative to `working_dir`?**
   - Double-check the stage's `working_dir` field
3. **Do these files contain real code (not stubs/TODOs)?**
   - Loom can check file size or grep for implementation patterns

### Wiring

1. **Where does the feature connect to the existing codebase?**
   - Commands → CLI parser, Endpoints → router, Modules → parent import
2. **What code pattern proves the connection exists?**
   - Look for imports, registrations, mount calls, enum variants
3. **Is the pattern specific enough to avoid false positives?**
   - `mod verify` is better than just `verify` (could match comments)

## Working Directory and Path Resolution

**CRITICAL:** All verification paths are relative to the stage's `working_dir` field.

```yaml
# Stage configuration
- id: my-stage
  working_dir: "loom"  # Commands execute from .worktrees/my-stage/loom/

  # Verification paths resolve relative to working_dir
  artifacts:
    - "src/feature.rs"  # Resolves to .worktrees/my-stage/loom/src/feature.rs

  wiring:
    - source: "src/main.rs"  # Resolves to .worktrees/my-stage/loom/src/main.rs
      pattern: "mod feature"
      description: "Feature module imported"
```

**Formula:** `RESOLVED_PATH = WORKTREE_ROOT + working_dir + path`

**Example:** If:

- Worktree root: `.worktrees/my-stage/`
- `working_dir: "loom"`
- Artifact path: `"src/feature.rs"`

Then resolved path: `.worktrees/my-stage/loom/src/feature.rs`

**NO PATH TRAVERSAL:** Never use `../` in paths. All paths must be relative to `working_dir` or deeper.

## Copy-Paste YAML Templates

### CLI Command Template

```yaml
truths:
  - "myapp command --help"
  - "myapp command arg1 arg2"  # Primary use case

artifacts:
  - "src/commands/command.rs"

wiring:
  - source: "src/main.rs"
    pattern: "Commands::CommandName"
    description: "Command variant in CLI enum"
  - source: "src/commands/mod.rs"
    pattern: "pub mod command"
    description: "Command module exported"
```

### API Endpoint Template

```yaml
truths:
  - "curl -f -X GET http://localhost:PORT/api/endpoint"
  - "curl -f http://localhost:PORT/api/endpoint | grep -q 'expected_field'"

artifacts:
  - "src/handlers/endpoint.rs"
  - "src/routes/api.rs"

wiring:
  - source: "src/routes/api.rs"
    pattern: "get(\"/endpoint\", handler)"
    description: "Endpoint route registered"
  - source: "src/main.rs"
    pattern: "mount(\"/api\", routes)"
    description: "API routes mounted"
```

### Module Template

```yaml
truths:
  - "cargo test module::"
  - "cargo check"

artifacts:
  - "src/module/mod.rs"
  - "src/module/core.rs"

wiring:
  - source: "src/lib.rs"
    pattern: "pub mod module"
    description: "Module exported from library"
  - source: "src/main.rs"
    pattern: "use crate::module"
    description: "Module imported in main"
```

### UI Component Template

```yaml
truths:
  - "npm test -- ComponentName"
  - "npm run build"

artifacts:
  - "src/components/ComponentName.tsx"
  - "src/components/ComponentName.test.tsx"

wiring:
  - source: "src/components/index.ts"
    pattern: "export.*ComponentName"
    description: "Component exported from barrel"
  - source: "src/pages/Parent.tsx"
    pattern: "<ComponentName"
    description: "Component rendered in parent"
```

## Integration with Loom Verify Command

The `loom verify <stage-id>` command executes these checks:

1. **Truths:** Runs each shell command, expects exit 0
2. **Artifacts:** Checks files exist and are non-empty (> 100 bytes by default)
3. **Wiring:** Greps for patterns in source files, expects at least one match

Use `loom verify <stage-id> --suggest` to get fix suggestions when checks fail.

## Final Checklist

Before finalizing your wiring verification:

- [ ] At least one `truth` proves the feature works end-to-end (not just tests)
- [ ] All `artifacts` are specific implementation files (not directories or test files)
- [ ] All `wiring` entries have specific patterns (not generic strings like "feature")
- [ ] All paths are relative to `working_dir` (no `../` traversal)
- [ ] No triple backticks inside YAML `description` fields
- [ ] Patterns are specific enough to avoid false matches in comments
- [ ] Truth commands use `-q` flag for grep (silent mode, only exit code matters)

## Common Pitfalls

1. **Tests Pass ≠ Feature Works**
   - Bad: `truths: ["cargo test"]`
   - Good: `truths: ["loom verify stage-1"]`

2. **Generic Patterns Match Too Much**
   - Bad: `pattern: "verify"` (matches comments, strings)
   - Good: `pattern: "Commands::Verify"` (specific enum variant)

3. **Paths Wrong for working_dir**
   - Bad: `working_dir: "."` with artifact `"loom/src/file.rs"` (creates double path)
   - Good: `working_dir: "loom"` with artifact `"src/file.rs"` (resolves correctly)

4. **No Functional Verification**
   - Bad: Only checking files exist and tests pass
   - Good: Actually running the command/endpoint/import and checking output

5. **YAML Syntax Errors**
   - Bad: Using triple backticks in description field
   - Good: Using plain indented text for code examples

---

**Remember:** Wiring verification is your last line of defense against "works in isolation, broken in integration" failures. Make it count.
