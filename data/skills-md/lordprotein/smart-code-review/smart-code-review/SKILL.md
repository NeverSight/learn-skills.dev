---
name: smart-code-review
description: "Expert code review with a senior engineer lens. Reviews git changes or targeted code (files, folders, features). Detects SOLID violations, security risks, and proposes actionable improvements."
---

# Code Review Expert

## Overview

Perform a structured code review with focus on SOLID, architecture, removal candidates, and security risks. Default to review-only output unless the user asks to implement changes.

**Two modes of operation:**

- **Default mode** (no argument): Reviews current git changes via `git diff`.
- **Targeted review mode** (with argument): Reviews specific code — a file path, folder, feature name, function, or keyword. The argument is interpreted flexibly: it can be a path (`src/auth/`), an entity name (`PaymentService`), or a description (`логика корзины`).

## Severity Levels

| Badge | Level | Description | Action |
|-------|-------|-------------|--------|
| 🔴 | **Critical** | Security vulnerability, data loss risk, correctness bug | Must block merge |
| 🟠 | **High** | Logic error, significant SOLID violation, performance regression | Should fix before merge |
| 🟡 | **Medium** | Code smell, maintainability concern, minor SOLID violation | Fix in this PR or create follow-up |
| 🟢 | **Low** | Style, naming, minor suggestion | Optional improvement |

## Workflow

### 0) Mode detection

If the user provides an argument (text after the skill command), switch to **targeted review mode**:

1. **Determine target type**:
   - If argument looks like a file/directory path → read those files directly
   - If argument is a name/keyword (e.g. "auth", "PaymentService", "роутинг") → use `rg`, `grep`, `find` to locate all related files, functions, classes, and modules
   - If argument is a description (e.g. "логика оплаты") → search for related code by keywords

2. **Scope the review**:
   - List all discovered files and ask the user to confirm the scope
   - If too many files found (>10), suggest narrowing down or review in batches

3. **Proceed to step 2** (skip git diff in step 1, review the discovered code instead)

If no argument is provided → proceed to step 1 (default git diff review).

### 1) Preflight context

> **Note**: In targeted review mode (step 0), this step is skipped — the review scope is already established.

- Use `git status -sb`, `git diff --stat`, and `git diff` to scope changes.
- If needed, use `rg` or `grep` to find related modules, usages, and contracts.
- Identify entry points, ownership boundaries, and critical paths (auth, payments, data writes, network).

**Edge cases:**
- **No changes**: If `git diff` is empty, inform user and ask if they want to review staged changes or a specific commit range.
- **Large diff (>500 lines)**: Summarize by file first, then review in batches by module/feature area.
- **Mixed concerns**: Group findings by logical feature, not just file order.

### 2) SOLID + architecture smells

- Load `references/solid-checklist.md` for general SOLID prompts.
- **If the project uses React**: also load `references/solid-react-checklist.md` for React-specific patterns (god-hooks, wide hook interfaces, component anti-patterns).

**MANDATORY procedure** — do NOT skip this, do NOT merge SOLID findings into general findings:

1. **Inventory**: List all major code units in scope (hooks, components, utility modules). Write them down.
2. **SRP scan**: For each hook and component from the inventory, answer: *"What is the single reason this would change?"* If the answer contains "and" — flag it.
3. **ISP scan**: For each hook that returns an object with 3+ fields, list its consumers and check which fields each consumer uses. If no consumer uses >60% of fields — flag it.
4. **OCP scan**: Search for hardcoded type/category/status checks in generic components (`if (type ===`, `switch(status)`, magic numbers with conditional display).
5. **DIP scan**: Check if components import store slice internals directly vs. using abstraction hooks.
6. **LSP scan**: Check for `as Type` casts bypassing type safety, ignored props, conditional children rendering.
7. **Record findings** directly into the `## Findings` section with appropriate severity (Critical/High/Medium/Low). SOLID violations are NOT separated into their own section — they are regular findings alongside security, quality, and other issues. The list of checked code units goes into the `**Units checked**` line at the top of Findings.

- When you propose a refactor, explain *why* it improves cohesion/coupling and outline a minimal, safe split.
- If refactor is non-trivial, propose an incremental plan instead of a large rewrite.

### 3) Removal candidates + iteration plan

- Identify code that is unused, redundant, or feature-flagged off.
- Classify each candidate into two categories:
  - **Safe to remove now**: no active consumers, evidence of non-usage (0 references, dead flag). List location, rationale, deletion steps, verification.
  - **Defer removal (plan required)**: has consumers or needs migration. Note preconditions, breaking changes, migration steps, timeline, rollback plan.
- **Checklist before any removal**:
  - [ ] Searched codebase for all references (`rg`, `grep`)
  - [ ] Checked for dynamic/reflection-based usage
  - [ ] Verified no external consumers (APIs, SDKs, docs)
  - [ ] Feature flag telemetry reviewed (if applicable)
  - [ ] Tests updated/removed
  - [ ] Documentation updated
  - [ ] Team notified (if shared code)

### 4) Security and reliability scan

- Load `references/security-checklist.md` for coverage.
- Check for:
  - XSS, injection (SQL/NoSQL/command), SSRF, path traversal
  - AuthZ/AuthN gaps, missing tenancy checks
  - Secret leakage or API keys in logs/env/files
  - Rate limits, unbounded loops, CPU/memory hotspots
  - Unsafe deserialization, weak crypto, insecure defaults
  - **Race conditions**: concurrent access, check-then-act, TOCTOU, missing locks
  - **New dependencies**: If new packages were added, check justification (could stdlib solve it?), maintenance status, and bundle size impact. Flag unjustified or unmaintained additions as 🟡 Medium.
- Call out both **exploitability** and **impact**.

### 5) Code quality scan

- Load `references/code-quality-checklist.md` for coverage.
- Check for:
  - **Error handling**: swallowed exceptions, overly broad catch, missing error handling, async errors
  - **Boundary conditions**: null/undefined handling, empty collections, numeric boundaries, off-by-one
  - **Test coverage gap**: If changed code lacks corresponding test updates, flag as 🟡 Medium. Note which behaviors are untested. Do NOT write tests — only flag the gap.
  - **Breaking changes**: Check for renamed/removed public APIs, changed function signatures, altered response shapes, removed exports. If the change is in a shared library or API layer, flag breaking changes as 🟠 High with migration guidance.
- Flag issues that may cause silent failures or production incidents.

### 6) Performance scan

- Load `references/performance-checklist.md` for coverage.
- Check for:
  - **Algorithmic complexity**: nested loops O(n²), linear search instead of hash, sort inside loop, recursion without memoization
  - **Memory leaks**: unsubscribed listeners, uncleaned timers, closures capturing large objects, unbounded collections, missing resource cleanup
  - **CPU hot paths**: expensive ops in loops, blocking sync I/O, redundant computation
  - **Database & I/O**: N+1 queries, over-fetching, missing pagination, missing indexes
  - **Caching**: missing cache, no TTL, no invalidation, key collisions
- For each finding, estimate impact: note input size sensitivity and expected degradation pattern.
- All performance findings go into the `### ⚡ Performance` category within the `## Findings` section.

### 7) Output format

Load `references/finding-format.md` for the per-finding template and formatting rules.

Structure your review as follows:

````markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]

---

## Findings

**Units checked**: `useMyHook`, `MyComponent`, `utilFunction`, ...

### 🛡 Security & Reliability
(findings formatted per finding-format.md template)

### 🏗 Architecture & SOLID
(findings formatted per finding-format.md template)

### ⚡ Performance
(findings formatted per finding-format.md template)

### 🧹 Code Quality
(findings formatted per finding-format.md template)

### 🗑 Removal Candidates
(if applicable)

---

## Additional Suggestions
(optional improvements, not blocking)
````

**Clean review**: If no issues found, explicitly state:
- What was checked
- Any areas not covered (e.g., "Did not verify database migrations")
- Residual risks or recommended follow-up tests

### 8) Next steps confirmation

After presenting findings, ask user how to proceed:

```markdown
---

## Next Steps

I found X issues (🔴 Critical: _, 🟠 High: _, 🟡 Medium: _, 🟢 Low: _).

**How would you like to proceed?**

1. **Fix all** - I'll implement all suggested fixes
2. **Fix Critical/High only** - Address 🔴 and 🟠 issues
3. **Fix specific items** - Tell me which issues to fix
4. **No changes** - Review complete, no implementation needed
```

**Important**: Do NOT implement any changes until user explicitly confirms. This is a review-first workflow.

