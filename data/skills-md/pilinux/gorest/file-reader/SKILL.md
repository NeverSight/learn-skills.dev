---
name: file-reader
description: Precisely read source files or snippets and return concise, citation-backed facts needed for decisions or edits.
license: MIT
metadata:
  mode: read-only
  purpose: reading
---

# File Reader

## When to Use

- User requests exact lines, signatures, constants, or a short factual summary of a specific file or function.

## Responsibilities

- Read only the minimum necessary lines and provide `path:line` citations.
- Extract inputs, outputs, side effects, and error handling where relevant.

## Rules

- Do not modify files or run shell commands.
- Prefer targeted reads over whole-file dumps.

## Output

- 2-6 sentence summary.
- Minimal code snippets (only necessary lines) with `path:line`.
- Suggested follow-ups (1-2 paths).

## Examples

- "Show the password hashing implementation in `lib/` with exact lines."
- "What does `model.Auth` look like including struct tags?"

## Related Skills

- `explain-code` (synthesis), `code-navigation` (locate files)
