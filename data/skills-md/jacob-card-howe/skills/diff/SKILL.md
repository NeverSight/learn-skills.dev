---
name: diff
description: Smart review of current uncommitted changes with structured analysis and issue detection.
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[--staged] [--file path] [path...]"
---

Review current uncommitted changes and provide structured analysis.

## Process

Parse `$ARGUMENTS`:
- `--staged`: only review staged changes
- `--file <path>`: review changes in a specific file only
- Positional args: paths to restrict the diff to

1. **Gather the diff**:
   ```bash
   # Both staged and unstaged by default
   git diff HEAD
   # If --staged:
   git diff --cached
   # Show summary stats
   git diff HEAD --stat
   ```

   If there are no changes, check for untracked files:
   ```bash
   git status --short
   ```

2. **Analyze the changes** — for each file changed:

   ### Check for problems
   - **Security**: secrets, credentials, API keys, tokens added to tracked files
   - **Correctness**: syntax errors detectable from the diff (unclosed brackets, broken YAML indentation, invalid JSON)
   - **Debugging artifacts**: `console.log`, `print()`, `TODO`, `FIXME`, `XXX`, `HACK` that look unintentional
   - **Conflict markers**: leftover `<<<<<<<`, `=======`, `>>>>>>>`
   - **Large additions**: files > 500 lines added, binary files

   ### Summarize the changes
   - Group by purpose: feature, fix, refactor, config change, etc.
   - Note any files that were renamed, deleted, or newly created

3. **Output format**:

```
## Changes Summary
**Files changed:** <count> (+<additions>/-<deletions>)

### By category
- **Config:** <files and what changed>
- **Code:** <files and what changed>
- **Other:** <files and what changed>

## Issues
- <any problems found, or "None detected">

## Review
<1-2 sentence overall assessment — is this ready to commit?>
```

4. If no issues found, keep it brief — just the summary and a green light.

## Notes

- Never stage, commit, or modify files. This skill is read-only.
- If the diff is very large (>2000 lines), summarize by file and flag the most critical changes.
