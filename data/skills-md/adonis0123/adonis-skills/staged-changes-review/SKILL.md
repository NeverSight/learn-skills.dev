---
name: staged-changes-review
description: Comprehensive review of staged Git changes for risk assessment, error detection, and impact analysis. Use when the user wants to review staged changes, check for errors before commit, analyze risks in git staged files, validate code changes before committing, or needs suggestions on staged modifications.
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "1.0.0"
---

# Staged Changes Review

This skill provides comprehensive analysis of Git staged changes to identify risks, errors, and potential issues before committing code.

## 输出要求 / Output Requirements

**重要：本技能必须使用中文输出所有分析结果和建议。**

- **语言 (Language)**: 始终使用中文回复
- **编码 (Encoding)**: 使用 UTF-8 编码
- **风格 (Style)**: 专业、详细、实用，提供具体的代码示例和修改建议

## Core Workflow

When invoked, follow this systematic review process:

### Step 1: Retrieve Staged Changes

```bash
# Get the diff of staged changes
git diff --cached

# Get list of staged files
git status --short | grep "^[MARC]"
```

### Step 2: Multi-Perspective Analysis

Analyze the staged changes from four critical perspectives:

#### 2.1 Syntax and Compilation Errors

- Missing imports or undefined references
- Type errors and incorrect type annotations
- Syntax errors (missing semicolons, brackets, quotes)
- Invalid API usage or method signatures
- Malformed JSON/YAML/configuration files

#### 2.2 Logic and Runtime Errors

- Null pointer / undefined access risks
- Off-by-one errors in loops and array access
- Incorrect error handling (missing try-catch, unhandled promises)
- Memory leaks (unclosed resources, event listeners)
- Race conditions in async code

#### 2.3 Breaking Changes and Side Effects

- API signature changes affecting consumers
- Database schema modifications
- Environment variable changes
- Dependency version updates with breaking changes
- Removed or renamed public functions/classes

When potential breaking changes are detected:
```bash
# Search for usages of modified functions/classes
git grep -n "functionName" -- "*.js" "*.ts"

# Check if migrations are included for schema changes
find . -name "*migration*" -mtime -1

# Review related test files
git diff --cached --name-only | grep test
```

#### 2.4 Security Vulnerabilities

- Hardcoded credentials, API keys, or secrets
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Insecure data handling (unencrypted PII)
- Authentication/authorization bypasses

### Step 3: Contextual Code Inspection

When issues are found, examine related code:

```bash
# View full file context
git show HEAD:<filename>

# Search related code patterns
git grep -n "relatedPattern" -- "*.ext"
```

### Step 4: Confidence Scoring

| Level | Score | Examples |
|-------|-------|----------|
| HIGH | 90-100 | Syntax errors, type mismatches, clear security issues |
| MEDIUM | 60-89 | Potential logic errors, suspicious patterns |
| LOW | 20-59 | Code smells, style concerns |

### Step 5: Generate Review Report

Present findings in this format:

```markdown
## Staged Changes Review

### Summary
- **Files Changed**: <count>
- **High Risk Issues**: <count>
- **Medium Risk Issues**: <count>
- **Security Concerns**: <count>

### Critical Issues (Confidence >= 80)

#### 1. [Category] Issue Title
**File**: `path/to/file.ext:line`
**Severity**: CRITICAL | HIGH | MEDIUM
**Confidence**: <score>/100

**Problem**: [Description]
**Impact**: [What happens if committed]
**Recommendation**: [Specific fix]

### Files Review Summary

| File | Status | Issues | Risk Level |
|------|--------|--------|-----------|
| path/to/file1 | Clean | 0 | Low |
| path/to/file2 | Warning | 2 | Medium |
| path/to/file3 | Critical | 1 | High |
```

## Quick Reference

| Perspective | Key Checks |
|-------------|------------|
| Syntax | Imports, types, brackets, API usage |
| Logic | Null access, loops, error handling, async |
| Breaking | API changes, schema, dependencies |
| Security | Secrets, injection, XSS, auth |

## Additional Resources

For language-specific patterns and edge cases, see:
- `references/language-patterns.md` - Language-specific validation rules
- `references/edge-cases.md` - Special scenarios and optimizations
