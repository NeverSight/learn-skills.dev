---
name: boy-scout-rule
description: When touching existing code and wanting to leave it better. Use when the user says "clean this up while I'm here," "should I fix this," "tech debt," "while I'm in this file," or "incremental improvement." For full refactoring, see solid or separation-of-concerns.
metadata:
  version: 1.0.0
---

# Boy Scout Rule

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Leave every file you touch a little better than you found it. Not a lot better — a little better. Incremental improvement compounds into a clean codebase over time.

## Why This Matters in Production

Codebases don't rot overnight. They degrade one shortcut at a time — a hardcoded value here, a skipped rename there, a TODO that lives for three years. The Boy Scout Rule is the antidote: it makes improvement the default, not a scheduled event.

Teams that practice this never need "cleanup sprints." Their code stays healthy because maintenance happens continuously, embedded in regular feature work.

But this only works with discipline: improvements must be **small, safe, and scoped**. A "cleanup" that touches 40 files and breaks two features is worse than leaving the mess.

## Rules

1. **Fix what you see, within scope.** If you open a file to fix a bug and notice a misleading variable name, rename it. If you see a dead import, remove it. These are safe, low-risk improvements.
2. **Keep cleanups in separate commits.** A feature commit should contain the feature. A cleanup commit should contain the cleanup. Mixing them makes code review harder and reverts dangerous.
3. **Don't refactor what you don't understand.** If you open an unfamiliar file and something looks wrong, investigate before "fixing" it. What looks like dead code might be a critical fallback. What looks like a typo might be intentional.
4. **Scope your improvements.** Boy Scout Rule means fixing a confusing name or adding a missing type annotation. It does not mean redesigning a module you happened to walk past.
5. **Leave a trail.** If you notice a problem too large to fix in passing, create an issue or add a `TODO(ticket-number)` so it doesn't get forgotten.

## What Counts as "A Little Better"

- Renaming a variable from `x` to `user_count`
- Removing an unused import or dead code
- Adding a missing type annotation
- Fixing a misleading comment (or removing a comment that restates the code)
- Replacing a magic number with a named constant
- Simplifying a conditional that's more complex than necessary
- Fixing a compiler/linter warning

## What Does NOT Count

- Rewriting a function in a "better" style without functional change
- Migrating to a new pattern across the whole codebase
- Adding features or changing behavior
- Reformatting files to match a different style (use autoformatters for this)
- Refactoring code that is unfamiliar to you without full understanding

## Boundaries

- **Size limit:** If a cleanup would touch more than ~20 lines or span multiple modules, it's not a Boy Scout improvement — it's a refactoring task that deserves its own ticket and review.
- **Tension with "don't touch what you don't own":** In shared codebases, small improvements are generally welcome. Large refactors across module boundaries require coordination. Know the difference.
- **Tension with minimal diffs:** Some teams prefer PRs that only contain the intended change. In that case, put Boy Scout cleanups in a separate PR.

## Code Review Checklist

- [ ] Are the cleanups genuinely low-risk and obviously correct?
- [ ] Are cleanups in separate commits from feature work?
- [ ] Does the cleanup touch only code the author is actively working in?
- [ ] Would reverting the cleanup leave the feature intact?

## Related Skills

- **kiss**: For identifying what "simpler" looks like
- **convention-over-configuration**: For knowing what the project's conventions are before "fixing" things
- **dry**: For spotting duplication worth consolidating
