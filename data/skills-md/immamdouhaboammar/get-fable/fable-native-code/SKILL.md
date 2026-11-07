---
name: fable-native-code
description: Use when writing or editing code in an existing codebase — before adding comments, docstrings, try/catch blocks, validation, logging, or TODOs the surrounding file doesn't have, and before explaining your style choices in the reply.
version: 1.0.0
pack: build
inputs:
  - source_diff
  - target_file
requires:
  - codebase_access
produces:
  - idiomatic_code
gates:
  - no_defensive_bloat
  - style_matched
fallback: fable-execute
mutatesWorkspace: true
parallelSafe: true
neural_links:
  precursors:
    - fable-execute
    - fable-tdd
  continuations:
    - fable-verify
    - fable-simplify
  lateral_peers:
    - fable-scope-discipline
  recovery: fable-recover
---

# Fable Native Code

Your diff should read like the file's longtime owner wrote it. The file has a style — naming, error handling, comment density, formatting. Write in it. Your personal preferences are not improvements; they're an accent.

## Purpose

Enforce codebase idioms and suppress foreign AI patterns. Eliminate defensive bloat, excessive comments, unnecessary try/catch blocks, unrequested logging, and conversational justification of coding style.

## When to Use

- When writing or editing code in an existing repository.
- Before adding docstrings, comments, type annotations, or validations to a file that lacks them.
- When choosing naming conventions, error-handling patterns, or import structures.
- When reviewing a completed diff before finalizing the turn.

## When NOT to Use

- When bootstrapping a brand new project from scratch with no established idioms (use `fable-architecture` or `fable-execute`).
- Refactoring architectural boundaries or decoupling modules (use `fable-simplify`).
- Performance benchmarking and algorithmic optimization (use `fable-review`).

## Inputs

- `source_diff`: The proposed code modification.
- `target_file`: The existing source file, its surrounding conventions, and neighboring modules.

## Expected Outputs

- `idiomatic_code`: Clean, minimal, idiom-matched code edits that blend seamlessly with surrounding style.
- `clean_diff`: A diff free of cosmetic churn, gratuitous comments, and defensive wrapping.

## Procedure

1. **Match the File**: Follow naming, error-handling idiom, comment density, formatting, and import organization. If the file has one comment per 200 lines, your addition almost certainly has zero.
2. **Comment Invariants Only**: Comments state only constraints the code cannot show — invariants, gotchas, why-not-the-obvious-way. Never what the next line does, never narration of your change ("now correctly handles X"), never justification aimed at a reviewer.
3. **Suppress Defensive Bloat**: No try/catch around code that works, no validating invariants the types or callers already guarantee, no logging, config, or flags nobody asked for.
4. **Don't Narrate Restraint**: The urge to explain what you didn't add ("note: I deliberately left out the doc comment because…") is the same urge that adds it — displaced into the reply. Deliver the code; mention style only if the user asks.
5. **Clean Exit**: No debug prints, no commented-out code, no TODO crumbs you created.
6. **Codebase Vocabulary**: Names come from the codebase's existing vocabulary. Don't coin a second name for an existing concept.

## Decision Rules

### Contrast Example: Terse Go File

Task: add `clampWindow` to a terse Go file whose only comment in 200 lines marks a sorting invariant; callers guarantee `max >= 0`.

**Foreign (AI habits, not the file's):**
```go
// clampWindow clamps start and end into the valid range [0, max] and
// normalizes inverted windows. Returns (start, start) when end < start.
func clampWindow(start, end, max int) (int, int) {
    if max < 0 {
        return 0, 0 // defensive: should never happen
    }
    ...
}
```

**Native (what the file's owner would write):**
```go
func clampWindow(start, end, max int) (int, int) {
    if start < 0 {
        start = 0
    }
    if end > max {
        end = max
    }
    if end < start {
        end = start
    }
    return start, end
}
```

- If surrounding code uses early returns, use early returns.
- If surrounding code lets errors bubble up, bubble them up; do not swallow or wrap them in unrequested custom errors.
- Never add a docstring unless the enclosing interface or file strictly enforces docstrings on all exported symbols.

## Tool Policy

- Read neighboring functions before editing to absorb file conventions.
- Use precise line replacement tools (`replace_file_content`) to prevent whitespace and indentation drift.
- Do not reformat untouched lines in the same file.

## Evidence Requirements

- Provide the exact diff showing changes integrate natively with the file.
- Passing test suite and linter confirming zero stylistic or typing violations.

## Failure Handling

- If linter flags a style mismatch, conform strictly to the project's linter rules.
- If an unneeded comment or debug print slipped into the diff, remove it immediately before completing the turn.

## Completion Criteria

- Diff reads as if authored by the repository's primary maintainer.
- Zero defensive bloat, zero unrequested logging, zero artificial comments.
- Code compiles, passes existing style checks, and passes all unit tests.
