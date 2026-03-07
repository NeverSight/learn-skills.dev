---
name: ignore
description: "Manage global ignore patterns for lint-relative-paths. TRIGGERS - statusline ignore, add ignore pattern, lint ignore, path lint exclude."
allowed-tools: Read, Bash, TodoWrite, TodoRead, AskUserQuestion
argument-hint: "[add|list|remove] [pattern]"
model: haiku
---

# Global Ignore Patterns

Manage global ignore patterns for the `lint-relative-paths` linter.

## Purpose

Some repositories intentionally use relative paths in markdown (e.g., `../docs/file.md`)
instead of repo-root paths (e.g., `/docs/file.md`). This command manages a global ignore
file that skips path validation for matching workspaces.

## Actions

| Action   | Description                             | Example                                   |
| -------- | --------------------------------------- | ----------------------------------------- |
| `add`    | Add a pattern to the global ignore file | `/statusline-tools:ignore add my-repo`    |
| `list`   | Show current patterns                   | `/statusline-tools:ignore list`           |
| `remove` | Remove a pattern from the ignore file   | `/statusline-tools:ignore remove my-repo` |

## Pattern Matching

Patterns use **substring matching**. A pattern matches if the workspace path contains the pattern.

**Example**: Pattern `alpha-forge` matches:

- `/Users/user/projects/alpha-forge`
- `/Users/user/eon/alpha-forge.worktree-feature-x`
- `/home/user/code/alpha-forge-v2`

## Ignore File Location

`~/.claude/lint-relative-paths-ignore`

Lines starting with `#` are comments.

## Execution

### Skip Logic

- If action + pattern provided -> execute directly
- If only `list` provided -> show patterns immediately
- If no arguments -> use AskUserQuestion flow

### Workflow

1. **Check Current State**: Run `list` to show existing patterns
2. **Action Selection**: Use AskUserQuestion to select action:
   - "Add a new pattern" -> prompt for pattern
   - "Remove an existing pattern" -> show current patterns to select
   - "Just view current patterns" -> display and exit
3. **Pattern Input**: For add/remove, AskUserQuestion with examples
4. **Execute**: Run the management script
5. **Verify**: Confirm changes applied

### AskUserQuestion Flow (No Arguments)

When invoked without arguments, guide the user interactively:

```
Question: "What would you like to do with lint-relative-paths ignore patterns?"
Options:
  - "Add pattern" -> "Add a new repository pattern to skip path linting"
  - "List patterns" -> "Show all current ignore patterns"
  - "Remove pattern" -> "Remove an existing pattern from the ignore list"
```

For "Add pattern":

```
Question: "Enter the repository pattern to ignore"
Note: Patterns use substring matching. Example: 'alpha-forge' matches any path containing 'alpha-forge'.
```

### Direct Execution (With Arguments)

Parse `$ARGUMENTS` and run the management script:

```bash
/usr/bin/env bash << 'IGNORE_SCRIPT_EOF'
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/statusline-tools}"
bash "$PLUGIN_DIR/scripts/manage-ignore.sh" $ARGUMENTS
IGNORE_SCRIPT_EOF
```

## Manual Editing

The ignore file can also be edited manually:

```bash
# View current patterns
cat ~/.claude/lint-relative-paths-ignore

# Add a pattern manually
echo "my-repo-pattern" >> ~/.claude/lint-relative-paths-ignore
```

## Troubleshooting

| Issue                 | Cause                     | Solution                                             |
| --------------------- | ------------------------- | ---------------------------------------------------- |
| Pattern not matching  | Substring match is strict | Use broader pattern (e.g., `forge` vs `alpha-forge`) |
| Ignore file not found | ~/.claude doesn't exist   | Create with `mkdir -p ~/.claude`                     |
| Permission denied     | File not writable         | Check file permissions with `ls -la`                 |
| Script not found      | Plugin not installed      | Reinstall plugin from marketplace                    |
