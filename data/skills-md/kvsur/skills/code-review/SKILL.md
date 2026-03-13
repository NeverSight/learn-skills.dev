---
name: code-review
description: "Expert code review of specified change ranges with a senior engineer lens. Detects SOLID violations, security risks, and proposes actionable improvements."
---

# Code Review Expert

## Overview

Perform a structured review of the specified change ranges with focus on SOLID, architecture, removal candidates, and security risks. Default to review-only output unless the user asks to implement changes.

## Supported Review Scope
1. Code snippets (single functions, classes, modules, or similar units)
2. Git change sets (specific commit hashes, current uncommitted changes including staged and unstaged files, branch-to-branch diffs, or the latest commit)
3. Repository-wide review (full project codebase)
4. Design artifacts (architecture docs, technical design proposals, and related specifications)

If the user does not explicitly define the review scope, default to reviewing the current repository's staged and unstaged changes, and confirm this scope before starting. If the user provides a scope, restate and confirm it, then proceed with the review.

## Severity Levels

| Level | Name | Description | Action |
|-------|------|-------------|--------|
| **P0** | Critical | Security vulnerability, data loss risk, correctness bug | Must block merge |
| **P1** | High | Logic error, significant SOLID violation, performance regression | Should fix before merge |
| **P2** | Medium | Code smell, maintainability concern, minor SOLID violation | Fix in this PR or create follow-up |
| **P3** | Low | Style, naming, minor suggestion | Optional improvement |

## Workflow

### 1) Preflight context

- Confirm the review scope with the user before starting. 
- Identify entry points, ownership boundaries, and critical paths (auth, payments, data writes, network).

**Edge cases:**
- **No changes**: If `changes` is empty, inform user and ask if they want to review staged changes or a specific commit range.
- **Large diff (>500 lines)**: Summarize by file first, then review in batches by module/feature area.
- **Mixed concerns**: Group findings by logical feature, not just file order.

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
- Check for:
  - **Error handling**: swallowed exceptions, overly broad catch, missing error handling, async errors
  - **Performance**: N+1 queries, CPU-intensive ops in hot paths, missing cache, unbounded memory
  - **Boundary conditions**: null/undefined handling, empty collections, numeric boundaries, off-by-one
- Flag issues that may cause silent failures or production incidents.

### 6) React Project Best Practices
- If the project uses React and the `vercel-react-best-practices` skill is installed locally, review whether the code adheres to the best practices defined in that skill.
- If the `vercel-react-best-practices` skill is not installed, prompt the user to install it for React-specific best practice coverage.

## Output Format

Output the review results in the following format:

```markdown

## 📊 Overall Assessment
> [Verdict: Approved ✅ / Approved with Changes ⚠️ / Requires Redesign ❌]
> [One-sentence summary]

If there are no obvious defects in the MR that could cause program bugs, output “No issues found.”
Otherwise, report the issues in the following format. Pay attention to severity classification. If there are no issues in a given category, the table may be left empty.

## 🚨 Must Fix (Critical)
| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | xxx  | xx   | xxx   | xxx            |

## ⚠️ Should Fix (Warning)
| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | xxx  | xx   | xxx   | xxx            |

## 💡 Suggestions (Info)
| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | xxx  | xx   | xxx   | xxx            |

```

## Output File
Save the formatted review output to a `[file-name]-review.md` file under the `code-review` directory in the project root, replacing `[file-name]` with the name of the reviewed file (without extension). If the review scope is a branch or commit, use `branch-[branch-name]-review.md` or `commit-[commit-hash]-review.md` as the file name.

## Resources

### references/

| File | Purpose |
|------|---------|
| `solid-checklist.md` | SOLID smell prompts and refactor heuristics |
| `security-checklist.md` | Web/app security and runtime risk checklist |
| `code-quality-checklist.md` | Error handling, performance, boundary conditions |
| `removal-plan.md` | Template for deletion candidates and follow-up plan |
