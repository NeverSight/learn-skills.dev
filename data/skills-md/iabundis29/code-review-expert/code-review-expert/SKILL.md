---
name: code-review-expert
description: "Expert code review of current git changes with a senior engineer lens. Detects SOLID violations, security risks, and proposes actionable improvements."
---

# Code Review Expert

## Overview

Perform a structured review with focus on SOLID, architecture, removal candidates, and security risks. Default to review-only output unless the user asks to implement changes.

## Initial Step: Choose Review Mode

Before starting, **ask the user which review mode they want**:

```
What would you like me to review?

1. **Specific PR** - Review a pull request (need PR URL or number)
2. **Compare Against Branch** - Review current changes against a target branch (e.g., main, develop, release)
3. **Review Current Changes** - Review staged or uncommitted changes in your working directory

Please choose one or provide details (e.g., PR link, target branch, or confirm working directory review).
```

**Why this matters**:
- **Specific PR**: Reviews the PR diff already pushed to remote (no local state needed)
- **Compare Against Branch**: Reviews your local changes against a branch baseline (good for in-progress work)
- **Current Changes**: Reviews staged/unstaged/uncommitted changes (good for pre-commit review)

## Severity Levels

| Level | Name | Description | Action |
|-------|------|-------------|--------|
| **P0** | Critical | Security vulnerability, data loss risk, correctness bug | Must block merge |
| **P1** | High | Logic error, significant SOLID violation, performance regression | Should fix before merge |
| **P2** | Medium | Code smell, maintainability concern, minor SOLID violation | Fix in this PR or create follow-up |
| **P3** | Low | Style, naming, minor suggestion | Optional improvement |

## Workflow

### 1) Preflight context

- **Confirm target branch first**: Ask which branch this PR is against (not always `main`/`master`)
  - Could be: `main`, `develop`, `release/x.y.z`, `staging`, feature branch, etc.
  - This determines the baseline for comparison
  - Different base branches = different diff = different review scope
  
- Use `git status -sb`, `git diff --stat`, and `git diff` to scope changes.
- If needed, use `rg` or `grep` to find related modules, usages, and contracts.
- Identify entry points, ownership boundaries, and critical paths (auth, payments, data writes, network).

**Prompt user for context:**
```
Before I review, please confirm:
1. What branch is this PR merging INTO? (e.g., main, release/1.2.0, develop)
2. Should I compare against that branch, or a different baseline?
3. Any specific areas you want me to focus on?
```

**Edge cases:**
- **No changes**: If `git diff` is empty, inform user and ask if they want to review staged changes or a specific commit range.
- **Large diff (>500 lines)**: Summarize by file first, then review in batches by module/feature area.
- **Mixed concerns**: Group findings by logical feature, not just file order.
- **Release branch**: Changes against release branches may have stricter stability requirements than develop

### 2) SOLID + architecture smells

- Load `references/solid-checklist.md` for specific prompts.
- Look for:
  - **SRP**: Overloaded modules with unrelated responsibilities.
  - **OCP**: Frequent edits to add behavior instead of extension points.
  - **LSP**: Subclasses that break expectations or require type checks.
  - **ISP**: Wide interfaces with unused methods.
  - **DIP**: High-level logic tied to low-level implementations.
- When you propose a refactor, explain *why* it improves cohesion/coupling and outline a minimal, safe split.
- If refactor is non-trivial, propose an incremental plan instead of a large rewrite.

### 3) Removal candidates + iteration plan

- Load `references/removal-plan.md` for template.
- Identify code that is unused, redundant, or feature-flagged off.
- Distinguish **safe delete now** vs **defer with plan**.
- Provide a follow-up plan with concrete steps and checkpoints (tests/metrics).

### 4) Security and reliability scan

- Load `references/security-checklist.md` for coverage.
- Check for:
  - XSS, injection (SQL/NoSQL/command), SSRF, path traversal
  - AuthZ/AuthN gaps, missing tenancy checks
  - Secret leakage or API keys in logs/env/files
  - Rate limits, unbounded loops, CPU/memory hotspots
  - Unsafe deserialization, weak crypto, insecure defaults
  - **Race conditions**: concurrent access, check-then-act, TOCTOU, missing locks
- Call out both **exploitability** and **impact**.

### 5) Code quality scan

- Load `references/code-quality-checklist.md` for coverage.
- Load `references/component-organization-checklist.md` if changes include React/React Native components.
- Load `references/typescript-checklist.md` if changes include TypeScript code.
- Load `references/react-native-checklist.md` if changes include React Native code.
- Load `references/redux-checklist.md` if changes include Redux code.
- Load `references/native-bridge-checklist.md` if changes include native code (Swift, Kotlin) or bridge methods.
- Check for:
  - **Error handling**: swallowed exceptions, overly broad catch, missing error handling, async errors
  - **Performance**: N+1 queries, CPU-intensive ops in hot paths, missing cache, unbounded memory
  - **Boundary conditions**: null/undefined handling, empty collections, numeric boundaries, off-by-one
  - **Component organization**: Component size, single responsibility, JSX structure, hook patterns
  - **TypeScript specific**: Type safety, use of `any`, null handling, function signatures, generics, enums
  - **React Native specific**: Memory leaks, lifecycle issues, FlatList optimization, platform differences, safe area handling
  - **Redux specific**: State normalization, reducer purity, selector memoization, async middleware patterns
  - **Native bridge specific**: Memory leaks across bridge, thread safety, type conversion, error propagation, platform differences
- Flag issues that may cause silent failures or production incidents.

### 6) Output format

Structure your review as follows:

```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]

---

## Findings

### P0 - Critical
(none or list)

### P1 - High
1. **[file:line]** Brief title
  - Description of issue
  - Suggested fix

### P2 - Medium
2. (continue numbering across sections)
  - ...

### P3 - Low
...

---

## Removal/Iteration Plan
(if applicable)

## Additional Suggestions
(optional improvements, not blocking)
```

**Inline comments**: Use this format for file-specific findings:
```
::code-comment{file="path/to/file.ts" line="42" severity="P1"}
Description of the issue and suggested fix.
::
```

**Clean review**: If no issues found, explicitly state:
- What was checked
- Any areas not covered (e.g., "Did not verify database migrations")
- Residual risks or recommended follow-up tests

### 7) Next steps confirmation

After presenting findings, ask user how to proceed:

```markdown
---

## Next Steps

I found X issues (P0: _, P1: _, P2: _, P3: _).

**How would you like to proceed?**

1. **Fix all** - I'll implement all suggested fixes
2. **Fix P0/P1 only** - Address critical and high priority issues
3. **Fix specific items** - Tell me which issues to fix
4. **No changes** - Review complete, no implementation needed

Please choose an option or provide specific instructions.
```

**Important**: Do NOT implement any changes until user explicitly confirms. This is a review-first workflow.

## Resources

### Complete Checklist Reference

| File | Purpose | When to Load |
|------|---------|--------------|
| `solid-checklist.md` | SOLID principles, architecture smells, refactor heuristics | Always (step 2) |
| `security-checklist.md` | Security vulnerabilities, crypto, race conditions, data integrity | Always (step 4) |
| `code-quality-checklist.md` | Error handling, performance, boundary conditions | Always (step 5) |
| `component-organization-checklist.md` | Component size, JSX structure, hook patterns | React/RN components |
| `typescript-checklist.md` | Type safety, generics, interfaces, narrowing | TypeScript files |
| `react-native-checklist.md` | Memory leaks, lifecycle, FlatList, platform differences | React Native code |
| `redux-checklist.md` | State shape, reducers, selectors, async | Redux code |
| `native-bridge-checklist.md` | Swift/Kotlin, bridge communication, thread safety | Native code or bridge |
| `removal-plan.md` | Template for safe removal and migration planning | Deletion/refactoring |

See `references/README.md` for comprehensive index and usage guide.

---

## Detailed Workflow Guidance

### Step 1: Preflight Context - Key Questions

**What to analyze:**
- **FIRST: Confirm target branch** - What branch is this PR merging into?
  - Examples: `main`, `develop`, `release/1.2.0`, `staging`, `hotfix/bug-fix`
  - This is the baseline for git diff
  - Different branches = different scope and stability requirements
- How many files changed? (2 vs 20 vs 100)
- Feature, bugfix, or refactor?
- Changes in critical paths (auth, payments, database)?
- Any cascading changes requiring 10+ files?

**Commands to run:**
```bash
git status -sb              # Quick overview
git branch -a               # List all branches
git diff --stat origin/TARGET_BRANCH  # Compare against target
git diff origin/TARGET_BRANCH # Full diff
git diff --name-only | wc -l # Count files
```

**🔴 Critical First Step - Ask User**:
```
Which branch is this PR against?
  [ ] main/master
  [ ] develop
  [ ] release/x.y.z (which version?)
  [ ] staging
  [ ] feature branch (which feature?)
  [ ] hotfix branch
  [ ] other (specify)

I'll use this as the baseline for comparison.
```

---

### Step 2: SOLID Check - Core Anti-patterns

**SRP violations** (most common):
- Module handles auth + payments + notifications
- Service validates, fetches, caches, and logs

**OCP violations**:
- Adding new payment type requires editing 5 switch statements
- New user role requires modifying UserService class

**Refactor suggestions**:
- Show before/after
- Explain *why* (improves cohesion, enables testing)
- Suggest incremental steps if complex

---

### Step 3: Removal Candidates - Classification

**Safe to remove now** (do it):
- Dead code with zero references
- No external API
- No dependencies on this code

**Defer removal** (create plan):
- Active consumers
- Breaking change required
- Needs migration period

---

### Step 4: Security - High-Impact Checks

**Must check** (security-sensitive):
- New auth endpoints protected? ✅ or ❌
- Authorization checks present? ✅ or ❌
- No secrets in code? ✅ or ❌
- SQL/NoSQL injection possible? ✅ or ❌
- Race conditions in concurrent code? ✅ or ❌

**Report format**:
- "Is this exploitable?" (Yes/No)
- "What's the impact?" (read data? modify? crash?)

---

### Step 5: Code Quality - Language-Specific

**TypeScript**:
- Any usage of `any`?
- Null checks present?
- Function return types explicit?

**React/RN components**:
- Component > 200 lines?
- useEffect cleanup present?
- Keys on lists?

**Redux**:
- State normalized?
- Selectors memoized?

**Native (Swift/Kotlin)**:
- Memory leaks in closures?
- Thread-safe access?

---

## Common Review Patterns

### Pattern: Component Too Large
**Signs**: 300+ lines, multiple useState, multiple useEffect, deeply nested JSX
**Fix**: Split into smaller focused components
**Reference**: `component-organization-checklist.md`

### Pattern: Memory Leak
**Signs**: useEffect no cleanup, event listener not removed, timer not cleared
**Fix**: Add cleanup function
**Reference**: `react-native-checklist.md`

### Pattern: Type Confusion
**Signs**: `any` usage, force casting with `as`
**Fix**: Use proper types, type guards
**Reference**: `typescript-checklist.md`

### Pattern: Race Condition
**Signs**: Concurrent writes, check-then-act, no locks
**Fix**: Use atomic operations or distributed locks
**Reference**: `security-checklist.md`

---

## Quick Decision Guide

### Should I block this PR?

```
P0 issues present? → BLOCK ❌
P1 issues unresolved? → BLOCK ❌
P2 issues but deferrable? → REQUEST CHANGES (allow follow-up)
All clear? → APPROVE ✅
```

### Is component size a problem?

```
> 300 lines? → YES, too large
7+ useState hooks? → YES, too much state
4+ levels JSX nesting? → YES, unreadable
Multiple useEffect for unrelated logic? → YES, split
```

### Is this a memory leak?

```
useEffect without cleanup? ⚠️
Event listener unsubscribed? ✅ or ❌
Timer/callback cleared? ✅ or ❌
"this" binding released? ✅ or ❌
```

---

## Example Review Output

```markdown
## Code Review Summary

**Files**: src/auth/useAuth.ts (45 lines), src/Login.tsx (120 lines)
**Assessment**: REQUEST_CHANGES

---

## P0 - Critical

1. **src/auth/useAuth.ts:23** - Hardcoded API key
   - **Issue**: `const API_KEY = 'sk_live_123'` exposed in code
   - **Risk**: If repo leaked, key compromised
   - **Fix**: Use `process.env.API_KEY`

## P1 - High

2. **src/Login.tsx:45** - Missing error handling
   - **Issue**: `login()` call not wrapped in try/catch
   - **Risk**: Unhandled promise rejection crashes app
   - **Fix**: Add `.catch()` or wrap in try/catch

## P2 - Medium

3. **src/Login.tsx:15** - useEffect cleanup missing
   - **Issue**: Subscription created but never removed
   - **Risk**: Memory leak on unmount
   - **Fix**: Return cleanup function with `unsubscribe()`

## Next Steps

1. Fix P0 issues (hardcoded key)
2. Fix P1 issues (error handling)
3. P2 deferrable to follow-up PR

Ready when you are!
```

---

## Important Reminders

🔴 **Do NOT implement changes without explicit user confirmation** through the workflow.

✅ **DO be specific** - Line numbers, code samples, exact issues

✅ **DO explain rationale** - Why this matters, not just "fix it"

✅ **DO offer examples** - "Here's bad, here's better"

✅ **DO prioritize correctly** - P0 blocks, P2 doesn't

✅ **DO praise good patterns** - See something good? Call it out
