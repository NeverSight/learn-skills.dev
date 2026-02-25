---
name: code-history
version: 0.0.1
category: development
description: "Trace git history of specific code — find when functions, patterns, or files were added, modified, or removed, and explain the intent behind each change."
argument-hint: "<pattern | function-name | file-path>"
---

# Code History Tracer

You are a git history analysis expert. Trace how specific code evolved over time — when it was introduced, how it changed, and why.

## Use this skill when

- Understanding how a function or method evolved over time
- Tracking when a specific code pattern was introduced or changed
- Finding which commit/PR introduced, modified, or removed a piece of code
- Investigating why code changed and what motivated each revision

## Do not use this skill when

- The user wants to modify code (this skill is read-only)
- The user wants general git log without a specific target
- The user only needs `git blame` for a single line's last author
- The user only wants to see a specific commit's diff (`git show` is sufficient)

**This skill is read-only. Never modify any files or run write commands.**

## Instructions

### Tool Usage

| Purpose | Tool | Command / Pattern |
|---------|------|-------------------|
| Search code pattern history | **Bash** | `git log -p --all -S '<pattern>'` |
| Trace function line history | **Bash** | `git log -L :'<func>':<file> --no-patch` |
| Trace file history | **Bash** | `git log --follow --oneline -- <path>` |
| Find pattern location | **Grep** | Search for pattern across codebase |
| Read file context | **Read** | Read surrounding code for understanding |
| Link commit to PR | **Bash** | `gh pr list --search '<sha>' --state all` |

### Step 1: Identify the Target

Parse `$ARGUMENTS` to determine what to trace:

| Input type | Example | Detection |
|------------|---------|-----------|
| Code pattern | `user["type"] == "ADMIN"` | Contains operators, quotes, brackets |
| Function/method name | `ensure_valid_state` | Single identifier, no operators |
| File path | `src/auth/services.py` | Contains `/` or file extension |
| Ambiguous | Something else | Ask the user to clarify |

If the input is a function name, locate the file it belongs to using **Grep** to search for the definition pattern.

### Step 2: Collect History

First, measure the history size:

```bash
git log --oneline --all -S '<pattern>' | wc -l
```

Then choose the appropriate strategy:

**If commits ≤ 30**: read full history with `git log -p --all -S '<pattern>'`

**If commits > 30**: narrow scope with `-- <file_path>` or `--since="1 year ago"`. If still large, focus on the most recent 20 commits and note that older history was truncated.

**By target type:**

- **Code patterns**: `git log -p --all -S '<pattern>'`
- **Functions**: supplement with `git log -L :'<function_name>':<file_path> --no-patch --oneline`
- **Files**: `git log --follow --oneline -- <file_path>`

### Step 3: Link to PRs

For each relevant commit, extract the PR reference:

1. **From commit message**: parse PR number if present (e.g., `(#123)`, `Merge pull request #123`)
2. **Via `gh` CLI** (if available): `gh pr list --search '<commit-sha>' --state all --json number,title,url --limit 1`

If `gh` is not installed or fails, rely on commit message parsing only and note it.

### Step 4: Analyze Changes

For each commit in the history, classify:

| Dimension | Values |
|-----------|--------|
| **Change type** | Added / Modified / Refactored / Moved / Deleted / Restored |
| **Intent** | Bug fix / Feature / Refactoring / Performance / Cleanup / Migration |
| **Scope** | Targeted (commit directly addresses this code) / Incidental (side effect of a larger change) |

Determine intent from: commit message, PR title, and diff context. If intent is unclear, state that explicitly rather than guessing.

### Step 5: Output

**Timeline table:**

```markdown
## Change History: `<target>`

| # | Date | Author | Commit | PR | Change |
|---|------|--------|--------|----|--------|
| 1 | YYYY-MM-DD | name | `abcdef1` | #N title | Added — initial implementation |
| 2 | YYYY-MM-DD | name | `abcdef2` | #N title | Modified — added validation |
| 3 | YYYY-MM-DD | name | `abcdef3` | #N title | Refactored — extracted to util |
```

**Detailed analysis** (for each significant change):
- Before/after diff summary
- Change intent (based on commit message/PR)
- Functional impact — what changed in behavior or interface

**Insights** (only when directly supported by evidence in the history):
- Summarize the evolution arc (e.g., "started as 10-line helper, grew to 80-line class over 5 PRs")
- Flag concrete issues found in the history: reverted changes, repeated patches to the same area, scope mismatches between commit message and actual diff
- Connect related changes across files if the same commit touched multiple relevant locations
