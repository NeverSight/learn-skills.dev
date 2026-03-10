---
name: clean-codebase
description: >
  Remove dead code, unused imports, fix lint warnings, and normalize formatting
  across a codebase without changing business logic or architecture. Use when
  lint warnings have piled up during rapid development, unused imports and
  variables clutter files, dead code paths were never removed, formatting is
  inconsistent, or static analysis tools report fixable hygiene issues.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: maintenance
  complexity: intermediate
  language: multi
  tags: maintenance, cleanup, lint, dead-code, formatting
---

# clean-codebase

## When to Use

Use this skill when a codebase has accumulated hygiene debt:

- Lint warnings have piled up during rapid development
- Unused imports and variables clutter files
- Dead code paths exist but were never removed
- Formatting is inconsistent across files
- Static analysis tools report fixable issues

**Do NOT use** for architectural refactoring, bug fixes, or business logic changes. This skill focuses purely on hygiene and automated cleanup.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `codebase_path` | string | Yes | Absolute path to codebase root |
| `language` | string | Yes | Primary language (js, python, r, rust, etc.) |
| `cleanup_mode` | enum | No | `safe` (default) or `aggressive` |
| `run_tests` | boolean | No | Run test suite after cleanup (default: true) |
| `backup` | boolean | No | Create backup before deletion (default: true) |

## Procedure

### Step 1: Pre-Cleanup Assessment

Measure the current state to quantify improvements later.

```bash
# Count lint warnings by severity
lint_tool --format json > lint_before.json

# Count lines of code
cloc . --json > cloc_before.json

# List unused symbols (language-dependent)
# JavaScript/TypeScript: ts-prune or depcheck
# Python: vulture
# R: lintr unused function checks
```

**Expected:** Baseline metrics saved to `lint_before.json` and `cloc_before.json`

**On failure:** If lint tool not found, skip automated fixes and focus on manual review

### Step 2: Fix Automated Lint Warnings

Apply safe automated fixes (spacing, quotes, semicolons, trailing whitespace).

**JavaScript/TypeScript**:
```bash
eslint --fix .
prettier --write .
```

**Python**:
```bash
black .
isort .
ruff check --fix .
```

**R**:
```bash
Rscript -e "styler::style_dir('.')"
```

**Rust**:
```bash
cargo fmt
cargo clippy --fix --allow-dirty
```

**Expected:** All safe lint warnings resolved; files formatted consistently

**On failure:** If automated fixes introduce test failures, revert changes and escalate

### Step 3: Identify Dead Code Paths

Use static analysis to find unreferenced functions, unused variables, and orphaned files.

**JavaScript/TypeScript**:
```bash
ts-prune | tee dead_code.txt
depcheck | tee unused_deps.txt
```

**Python**:
```bash
vulture . | tee dead_code.txt
```

**R**:
```bash
Rscript -e "lintr::lint_dir('.', linters = lintr::unused_function_linter())"
```

**General approach**:
1. Grep for function definitions
2. Grep for function calls
3. Report functions defined but never called

**Expected:** `dead_code.txt` lists unused functions, variables, and files

**On failure:** If static analysis tool unavailable, manually review recent commit history for orphaned code

### Step 4: Remove Unused Imports

Clean up import blocks by removing references to packages never used.

**JavaScript**:
```bash
eslint --fix --rule 'no-unused-vars: error'
```

**Python**:
```bash
autoflake --remove-all-unused-imports --in-place --recursive .
```

**R**:
```bash
# Manual review: grep for library() calls, check if package used
grep -r "library(" . | cut -d: -f2 | sort | uniq
```

**Expected:** All unused import statements removed

**On failure:** If removing imports breaks build, they were used indirectly — restore and document

### Step 5: Remove Dead Code (Mode-Dependent)

**Safe Mode** (default):
- Only remove code explicitly marked as deprecated
- Remove commented-out code blocks (if >10 lines and >6 months old)
- Remove TODO comments referencing completed issues

**Aggressive Mode** (opt-in):
- Remove all functions identified as unused in Step 3
- Remove private methods with zero references
- Remove feature flags for deprecated features

For each candidate deletion:
1. Verify zero references in codebase
2. Check git history for recent activity (skip if modified in last 30 days)
3. Remove code and add entry to `CLEANUP_LOG.md`

**Expected:** Dead code removed; `CLEANUP_LOG.md` documents all deletions

**On failure:** If uncertain whether code is truly dead, move to `archive/` directory instead

### Step 6: Normalize Formatting

Ensure consistent formatting across all files (even if not caught by linters).

1. Normalize line endings (LF vs CRLF)
2. Ensure single newline at end of file
3. Remove trailing whitespace
4. Normalize indentation (spaces vs tabs, indent width)

```bash
# Example: Fix line endings and trailing whitespace
find . -type f -name "*.js" -exec sed -i 's/\r$//' {} +
find . -type f -name "*.js" -exec sed -i 's/[[:space:]]*$//' {} +
```

**Expected:** All files follow consistent formatting conventions

**On failure:** If sed breaks binary files, skip and document

### Step 7: Run Tests

Validate that cleanup didn't break functionality.

```bash
# Language-specific test command
npm test              # JavaScript
pytest                # Python
R CMD check           # R
cargo test            # Rust
```

**Expected:** All tests pass (or same failures as before cleanup)

**On failure:** Revert changes incrementally to identify breaking change, then escalate

### Step 8: Generate Cleanup Report

Document all changes for review.

```markdown
# Codebase Cleanup Report

**Date**: YYYY-MM-DD
**Mode**: safe | aggressive
**Language**: <language>

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lint warnings | X | Y | -Z |
| Lines of code | A | B | -C |
| Unused imports | D | 0 | -D |
| Dead functions | E | F | -G |

## Changes Applied

1. Fixed X lint warnings (automated)
2. Removed Y unused imports
3. Deleted Z lines of dead code (see CLEANUP_LOG.md)
4. Normalized formatting across W files

## Escalations

- [Issue description requiring human review]
- [Uncertain deletion moved to archive/]

## Validation

- [x] All tests pass
- [x] Backup created: backup_YYYYMMDD/
- [x] CLEANUP_LOG.md updated
```

**Expected:** Report saved to `CLEANUP_REPORT.md` in project root

**On failure:** (N/A — generate report regardless of outcome)

## Validation Checklist

After cleanup:

- [ ] All tests pass (or same failures as before)
- [ ] No new lint warnings introduced
- [ ] Backup created before any deletions
- [ ] `CLEANUP_LOG.md` documents all removed code
- [ ] Cleanup report generated with metrics
- [ ] Git diff reviewed for unexpected changes
- [ ] CI pipeline passes

## Common Pitfalls

1. **Removing Code Still Used via Reflection**: Static analysis misses dynamic calls (e.g., `eval()`, metaprogramming). Always check git history.

2. **Breaking Implicit Dependencies**: Removing imports that were used by dependencies. Run tests after every import removal.

3. **Deleting Feature Flags for Active Features**: Even if unused in current branch, feature flags may be active in other environments. Check deployment configs.

4. **Over-Aggressive Formatting**: Tools like `black` or `prettier` may reformat code in ways that trigger unnecessary diffs. Configure tools to match project style.

5. **Ignoring Test Coverage**: Cannot safely clean codebases without tests. If coverage is low, escalate for test additions first.

6. **Not Backing Up**: Always create `backup_YYYYMMDD/` directory before deleting anything, even if using git.

## Related Skills

- [tidy-project-structure](../tidy-project-structure/SKILL.md) — Organize directory layout, update READMEs
- [repair-broken-references](../repair-broken-references/SKILL.md) — Fix dead links and imports
- [escalate-issues](../escalate-issues/SKILL.md) — Route complex problems to specialists
- [r-packages/run-r-cmd-check](../../r-packages/run-r-cmd-check/SKILL.md) — Run full R package checks
- [devops/dependency-audit](../../devops/dependency-audit/SKILL.md) — Check for outdated dependencies
