---
name: deslop
description: Remove AI-generated code slop from the current branch. Use when the user says "deslop" or asks to clean up AI slop, remove AI code patterns, or clean the branch before committing.
---

# Deslop

Remove AI-generated code patterns from all changes in the current branch.

## Process

1. Run `git diff main` to get all changes
2. For each changed file, read the full file to understand existing style
3. Identify and remove slop patterns (see below), matching the file's existing style
4. Report a 1-3 sentence summary of changes

## Slop Patterns

Remove these when inconsistent with the surrounding code:

- **Unnecessary comments** - Comments a human wouldn't add or that don't match the file's commenting style
- **Defensive overkill** - Extra try/catch blocks, null checks, or validation that's abnormal for that area (especially on trusted/validated codepaths)
- **Type escape hatches** - Casts to `any` to bypass type issues
- **Single-use variables** - Variables used once immediately after declaration; inline the RHS instead
- **React prop interfaces** - Separate `interface Props` definitions; inline the props type directly
- **Style drift** - Any formatting, naming, or patterns inconsistent with the file

## Style Matching

Before editing, study the unchanged code in each file:

- Comment density and style
- Error handling patterns
- Variable naming conventions
- Type annotation style
- Component patterns (for React)

Only flag something as slop if it deviates from the file's established patterns.

## Output

End with only a 1-3 sentence summary of what was changed. No detailed lists.
