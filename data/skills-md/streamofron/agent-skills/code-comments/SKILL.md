---
name: code-comments
description: Use when adding, modifying, or reviewing comments in source code
---

# Code Comments

Guidelines for writing effective comments that explain intent without cluttering code.

## When to Use

- Adding comments to explain non-obvious code
- Reviewing existing comments for clarity and accuracy
- Deciding whether code needs a comment or should be refactored instead

**NOT for:** language-specific documentation syntax (JSDoc, docstrings, Go doc comments), documentation generation, or commit messages.

## Procedure

1. **Determine if a comment is needed** — code should be self-documenting when possible. A comment is warranted when:
   - The *why* is not obvious from the code
   - A non-obvious decision or constraint exists
   - An edge case or workaround needs explanation
   - Future work or known limitations should be flagged (TODO/FIXME)

2. **Write concise, accurate comments** — every word must earn its place:
   - Prefer one-line comments; respect existing conventions and linting rules
   - Maximum three lines per comment block
   - State the intent or constraint, not what the code does
   - Use complete thoughts, not fragments that require re-reading

3. **Place comments effectively** — position matters:
   - Place comments above the code they describe, not inline (unless explaining a specific line)
   - Keep comments close to the code they document
   - Avoid trailing comments that push code far right

4. **Keep comments current** — outdated comments are worse than no comments:
   - Update comments when code changes
   - Remove comments that no longer apply
   - Never leave commented-out code without explanation

## What to Comment

- **Why, not what:** Explain the reasoning, not the mechanics
- **Non-obvious decisions:** Workarounds, performance choices, compatibility constraints
- **Edge cases:** Boundary conditions, error handling rationale
- **TODOs/FIXMEs:** Known limitations or future work with context

## What Not to Comment

- **Obvious code:** `// increment counter` above `counter++`
- **Commented-out code:** Delete it; git history preserves it
- **Redundant explanations:** Don't restate what the code clearly does
- **Noise:** Separator lines, decorative comments, author tags (use git blame)

## Pitfalls

- **Over-commenting:** Comments that restate the code add noise without value. If you need to explain what the code does, consider refactoring instead.
- **Outdated comments:** Comments that don't match the code mislead future readers. Always update or remove comments when changing code.
- **Commented-out code:** Dead code in comments clutters the file. Trust version control to preserve history.
- **Vague comments:** "TODO: fix this" without context is useless. Explain what needs fixing and why.
- **Long comments:** If a comment needs more than three lines, the code probably needs refactoring or the explanation belongs in documentation.

## Verification

After adding or reviewing comments, confirm:

- Each comment explains *why*, not *what*
- Comments are concise (one line preferred, three lines maximum)
- No commented-out code remains without justification
- Comments match the current code behavior
- Obvious code has no redundant comments

Quick checklist:
```
Does this comment explain why, not what?
Is it as short as possible without losing accuracy?
Does it fit in one line (or three at most)?
Is the comment still accurate?
Could the code be clearer instead of needing this comment?
```
