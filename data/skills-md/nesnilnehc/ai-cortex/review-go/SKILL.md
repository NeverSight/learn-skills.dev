---
name: review-go
description: "Review Go code for language and runtime conventions: concurrency, context usage, error handling, resource management, API stability, type semantics, and testability. Language-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Go

## Purpose

Review code in **Go** for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on concurrency and goroutine lifecycle, context usage, error handling, resource management, API stability, type and zero-value semantics, and testability.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope -> language -> framework -> library -> cognitive for Go projects.
- **Go-only review**: When the user wants only language/runtime conventions checked (e.g. after adding a new Go file).
- **Pre-PR Go checklist**: Ensure concurrency, context, and error handling patterns are correct.

**When to use**: When the code under review is Go and the task includes language/runtime quality. Scope (diff vs paths) is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Go language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection (diff vs codebase), security review, or architecture review; do not review non-Go files for Go-specific rules unless explicitly in scope.

### Review checklist (Go dimension only)

1. **Concurrency and goroutine lifecycle**: Proper use of goroutines, channels, sync primitives, WaitGroup usage, channel closing, select patterns, and avoidance of goroutine leaks or data races.
2. **Context usage**: Context passed through request paths, cancellation and deadlines respected, avoid context.Background() in request handlers, and no storing context in long-lived structs.
3. **Error handling**: Errors checked and returned; wrapping with `%w`; use of `errors.Is/As`; avoid panic for expected errors; avoid error shadowing.
4. **Resource management**: `defer Close()` for io.Closer, `resp.Body.Close()` on HTTP responses, `Stop()` for Timer/Ticker, and `cancel()` for contexts.
5. **API stability and modules**: Stability of exported APIs, changes to exported types and interfaces, backward compatibility, and Go version/module expectations (go.mod, build tags).
6. **Type and zero-value semantics**: Nil interface vs typed nil pitfalls, pointer vs value receivers, map/slice initialization, copying and aliasing of slices, and zero-value correctness.
7. **Testability and interfaces**: Prefer small interfaces, injection over globals, and seams for deterministic tests.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or by the scope skill. This skill does not decide scope; it reviews the provided Go code for language conventions only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-go**.

---

## Restrictions

- **Do not** perform security, architecture, or scope selection. Stay within Go language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-Go code for Go-specific rules unless the user explicitly includes it (e.g. embedded code snippets).

---

## Self-Check

- [ ] Was only the Go language/runtime dimension reviewed (no scope/security/architecture)?
- [ ] Are concurrency, context usage, error handling, resource management, API stability, type semantics, and testability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-go, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line?

---

## Examples

### Example 1: Goroutine leak

- **Input**: Goroutine started in a request handler that waits on a channel that is never closed or canceled.
- **Expected**: Emit a finding for goroutine leak and missing cancellation; reference the handler and channel usage. Category = language-go.

### Example 2: Error handling

- **Input**: Function returns `fmt.Errorf("failed: %v", err)` and the caller compares errors with `==`.
- **Expected**: Emit a finding to wrap with `%w` and use `errors.Is/As`; reference the error construction and comparison. Category = language-go.

### Edge case: Mixed Go and SQL

- **Input**: Go file with embedded SQL strings for database queries.
- **Expected**: Review only Go conventions (context usage, error handling, resource cleanup). Do not emit SQL-injection findings; that is for review-security or review-sql.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `language-go`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1-3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `internal/worker/pool.go:87`
- **Category**: language-go
- **Severity**: major
- **Title**: Goroutine leak due to missing cancellation
- **Description**: The goroutine blocks on a channel that is never closed or canceled, so it will leak per request.
- **Suggestion**: Pass a context and exit on cancellation, or close the channel when the work is done.
```
