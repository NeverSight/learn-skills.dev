---
name: review-work
description: Refactor-only review pass over a recent commit. Defaults to HEAD~1...HEAD; accepts an optional commit hash to widen the range. Applies generic refactoring heuristics plus the project's coding standards, refactors in place to improve clarity without changing behaviour, runs the project's typecheck and test commands with a self-fix cap of 5. Never commits. Use when user types /review-work after committing implementation.
---

# Review and refactor

`$ARGUMENTS` is optional: a commit hash. If passed, review `<hash>...HEAD`. Otherwise, review `HEAD~1...HEAD`.

The project's validation commands (typecheck, test) and coding standards location should have been provided to you — run `/setup-imick-skills` if not.

## Workflow

1. **Read the diff**:
   - `git diff <base>...HEAD` where `<base>` is the argument or `HEAD~1`
   - `git log <base>..HEAD --oneline` for context
2. **Review for** these generic refactoring heuristics:
   - Unnecessary complexity and nesting
   - Redundant code, abstractions, or wrapper functions that don't earn their keep
   - Comments that describe obvious code
   - Unclear variable or function names
   - Nested ternary operators — prefer if/else or switch
   - Unsafe casts, `any` types, unchecked assumptions
   - New behaviour that lacks tests
   - Injection vulnerabilities, credential leaks, or other security issues
3. **Apply project standards**: read the coding standards doc identified in setup (if any) and apply its rules on top of the heuristics above.
4. **Refactor in place**: edit the relevant files directly. Preserve behaviour exactly — only change *how* the code works, never *what* it does.
5. **Validate** using the project's typecheck and test commands from setup.
6. **Self-fix loop** on failures, cap = 5 attempts total. If exceeded, go to Failure mode.
7. **Report** the refinements and stop.

## When to do nothing

If the diff is already clean and well-structured, do nothing and say so. A refactor commit with no real refinements is noise — better to skip the cleanup than to produce an empty one.

## Failure mode

If typecheck or test is still red after 5 self-fix attempts:

- Stop. Do not commit, do not revert.
- Report the latest failure output verbatim.
- Tell the user: "Working tree is dirty. Inspect with `git diff`, or abandon with `git restore .`."

## Invariants

- **Never change behaviour.** Functionality, outputs, and observable behaviour must stay identical to the committed implementation.
- **Never delete or weaken tests.**
- **Never commit.** The user commits manually after reviewing the diff.
- Never modify the issue's triage state on the issue tracker (status, labels, inline `Status:` line, comments) — the user manages it.
- Never switch branches.
- Never `git add` or stage files — leave the working tree dirty for human review.
