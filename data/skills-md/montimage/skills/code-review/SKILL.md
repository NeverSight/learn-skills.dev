---
name: code-review
version: 1.0.0
description: Perform code reviews following best practices from Code Smells and The Pragmatic Programmer. Use when asked to "review this code", "check for code smells", "review my PR", "audit the codebase", or need quality feedback on code changes. Supports both full codebase audits and focused PR/diff reviews. Outputs structured markdown reports grouped by severity.
---

# Code Review

Review code for quality issues, code smells, and pragmatic programming violations.

## Review Modes

### Mode 1: PR/Diff Review

```bash
# Get changed files
git diff --name-only <base>..HEAD
git diff <base>..HEAD
```

Focus only on changed lines and their immediate context.

### Mode 2: Full Codebase Audit

Scan all source files, prioritizing:
1. Entry points (main, index, app)
2. Core business logic
3. Frequently modified files (`git log --format='%H' | head -100 | xargs -I{} git diff-tree --no-commit-id --name-only -r {} | sort | uniq -c | sort -rn`)

## Review Checklist

### 1. Code Smells (Critical)

See [references/code-smells.md](references/code-smells.md) for full catalog.

**Bloaters** - Code that grows too large
- Long Method (>20 lines)
- Large Class (>200 lines)
- Long Parameter List (>3 params)
- Primitive Obsession

**Object-Orientation Abusers**
- Switch Statements (replace with polymorphism)
- Refused Bequest
- Alternative Classes with Different Interfaces

**Change Preventers**
- Divergent Change (one class, many reasons to change)
- Shotgun Surgery (one change, many classes affected)
- Parallel Inheritance Hierarchies

**Dispensables**
- Dead Code
- Duplicate Code
- Lazy Class
- Speculative Generality

**Couplers**
- Feature Envy
- Inappropriate Intimacy
- Message Chains
- Middle Man

### 2. Pragmatic Programmer Principles

**DRY (Don't Repeat Yourself)**
- Duplicated logic or knowledge
- Copy-paste code
- Repeated magic values

**Orthogonality**
- Components that should be independent but aren't
- Changes rippling across unrelated modules

**Reversibility**
- Hard-coded decisions that should be configurable
- Vendor lock-in without abstraction

**Tracer Bullets**
- Is the code testable end-to-end?
- Are there integration points?

**Good Enough Software**
- Over-engineering for unlikely scenarios
- Premature optimization

**Broken Windows**
- Commented-out code
- TODO/FIXME without tickets
- Inconsistent formatting

### 3. Security & Safety

- Input validation
- SQL injection risks
- XSS vulnerabilities
- Hardcoded secrets
- Unsafe deserialization

### 4. Maintainability

- Unclear naming
- Missing or outdated comments
- Complex conditionals
- Deep nesting (>3 levels)
- Missing error handling

## Output Format

Generate `CODE_REVIEW.md`:

```markdown
# Code Review Report

**Date**: YYYY-MM-DD
**Scope**: [PR #123 | Full Audit]
**Files Reviewed**: N

## Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| Major    | X |
| Minor    | X |
| Info     | X |

## Critical Issues

### [Category]: Issue Title
**File**: `path/to/file.ts:42`
**Smell**: [Code smell name]

Description of the issue.

**Before**:
```language
// problematic code
```

**Suggested Fix**:
```language
// improved code
```

## Major Issues
...

## Minor Issues
...

## Recommendations

1. Priority fixes
2. Refactoring suggestions
3. Architecture improvements
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Security risks, bugs, data loss potential | Must fix before merge |
| **Major** | Code smells, maintainability blockers | Should fix soon |
| **Minor** | Style, minor improvements | Nice to have |
| **Info** | Suggestions, alternatives | Optional |

## Resources

- [references/code-smells.md](references/code-smells.md) - Complete catalog of code smells with examples
