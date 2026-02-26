---
name: jj-hunk
description: Programmatic hunk selection for jj (Jujutsu). Use when splitting commits, making partial commits, or selectively squashing changes without interactive UI.
---

# jj-hunk: Programmatic Hunk Selection

Use `jj-hunk` for non-interactive hunk selection in jj. Essential for AI agents that need to create clean, logical commits from mixed changes.

## When to Use This Skill

- Splitting a commit into multiple logical commits
- Committing only specific hunks (partial commit)
- Squashing only certain changes into parent
- Any hunk selection that would normally require `jj split -i` or `jj squash -i`

## Setup

```bash
cargo install jj-hunk
```

Add to `~/.jjconfig.toml`:
```toml
[merge-tools.jj-hunk]
program = "jj-hunk"
edit-args = ["select", "$left", "$right"]
```

## Core Workflow

### 1. List Hunks

```bash
jj-hunk list

# List hunks for a specific revision (diff vs parent)
# Note: revset must resolve to a single revision
jj-hunk list --rev @

# Emit YAML instead of JSON
jj-hunk list --format yaml
```

Options:
- `--rev <revset>` — diff the revision against its parent (revset must resolve to a single revision)
- `--format json|yaml|text` — output format (default: json)
- `--include <glob>` / `--exclude <glob>` — filter paths (repeatable)
- `--group none|directory|extension|status` — group output
- `--binary skip|mark|include` — binary handling (default: mark)
- `--max-bytes <n>` / `--max-lines <n>` — truncate before diffing
- `--spec <json|yaml>` / `--spec-file <path>` — preview using a spec filter
- `--files` — list files with hunk counts only
- `--spec-template` — emit a spec template (JSON/YAML only)

Output (JSON):
```json
{
  "files": [
    {
      "path": "src/foo.rs",
      "status": "modified",
      "hunks": [
        {
          "id": "hunk-7c3d...",
          "index": 0,
          "type": "replace",
          "removed": "old\n",
          "added": "new\n",
          "before": {"start": 1, "lines": 1},
          "after": {"start": 1, "lines": 1}
        },
        {
          "id": "hunk-2f91...",
          "index": 1,
          "type": "insert",
          "removed": "",
          "added": "// added\n",
          "before": {"start": 2, "lines": 0},
          "after": {"start": 2, "lines": 1}
        }
      ]
    },
    {
      "path": "src/bar.rs",
      "status": "modified",
      "hunks": [
        {
          "id": "hunk-aa12...",
          "index": 0,
          "type": "delete",
          "removed": "removed\n",
          "added": "",
          "before": {"start": 3, "lines": 1},
          "after": {"start": 3, "lines": 0}
        }
      ]
    }
  ]
}
```

Each hunk includes a stable `id` (sha256) alongside the 0-based `index`.

### 2. Build a Spec

Select hunks by index or `id` (emitted as `hunk-<sha256>`), or use file-level actions. Specs can be JSON or YAML:

```json
{
  "files": {
    "src/foo.rs": {"hunks": [0, "hunk-7c3d..."]},
    "src/bar.rs": {"ids": ["hunk-aa12..."]},
    "src/baz.rs": {"action": "keep"},
    "src/qux.rs": {"action": "reset"}
  },
  "default": "reset"
}
```

| Spec | Effect |
|------|--------|
| `{"hunks": [0, 2]}` | Include only hunks 0 and 2 |
| `{"hunks": ["hunk-..."]}` | Include hunks by id string |
| `{"ids": ["hunk-..."]}` | Include hunks by stable id |
| `{"action": "keep"}` | Include all changes |
| `{"action": "reset"}` | Discard all changes |
| `"default": "reset"` | Unlisted files are discarded |
| `"default": "keep"` | Unlisted files are kept |

`ids` and `hunks` are merged if both are provided.

### 3. Execute

Specs can be provided inline, read from stdin with `-`, or loaded via `--spec-file` (omit `<spec>` when using `--spec-file`).

```bash
# Split: selected hunks → first commit, rest → second commit
jj-hunk split '<spec>' "commit message"

# Read spec from a file (JSON or YAML)
jj-hunk split --spec-file spec.yaml "commit message"

# Commit: selected hunks committed, rest stays in working copy
jj-hunk commit '<spec>' "commit message"

# Read spec from stdin
cat spec.json | jj-hunk commit - "commit message"

# Squash: selected hunks squashed into parent
jj-hunk squash '<spec>'
```

## Examples

### Split Mixed Changes into Logical Commits

You have refactoring and a new feature mixed together:

```bash
# 1. See what hunks exist
jj-hunk list

# 2. Split out the refactoring first
jj-hunk split '{"files": {"src/lib.rs": {"hunks": [0, 1]}}, "default": "reset"}' \
  "refactor: extract helper function"

# 3. Remaining changes become second commit
jj describe -m "feat: add new feature"
```

### Commit Only Part of Your Changes

Keep experimental code in working copy while committing the fix:

```bash
jj-hunk commit '{"files": {"src/bug.rs": {"action": "keep"}}, "default": "reset"}' \
  "fix: handle null case"
```

### Squash Specific Files into Parent

```bash
jj-hunk squash '{"files": {"src/tests.rs": {"action": "keep"}}, "default": "reset"}'
```

### Keep Everything Except One File

```bash
jj-hunk split '{"files": {"src/wip.rs": {"action": "reset"}}, "default": "keep"}' \
  "feat: complete implementation"
```

## Direct jj --tool Usage

The commands above are wrappers. For direct control:

```bash
# Write spec to file
echo '{"files": {"src/foo.rs": {"hunks": [0]}}, "default": "reset"}' > /tmp/spec.json

# Run jj with the tool
JJ_HUNK_SELECTION=/tmp/spec.json jj split -i --tool=jj-hunk -m "message"
```

## Hunk Types

| Type | Meaning |
|------|---------|
| `insert` | New lines added |
| `delete` | Lines removed |
| `replace` | Lines changed (removed + added) |

## Agent Workflow Examples

### Understanding the Output

Always start by inspecting what hunks exist:

```bash
jj-hunk list
```

Example output:
```json
{
  "files": [
    {
      "path": "src/db/schema.ts",
      "status": "modified",
      "hunks": [
        {"id": "hunk-98af...", "index": 0, "type": "insert", "removed": "", "added": "import { pgTable }...\n", "before": {"start": 1, "lines": 0}, "after": {"start": 1, "lines": 1}},
        {"id": "hunk-21b3...", "index": 1, "type": "insert", "removed": "", "added": "export const users = pgTable...\n", "before": {"start": 2, "lines": 0}, "after": {"start": 2, "lines": 1}}
      ]
    },
    {
      "path": "src/api/routes.ts",
      "status": "modified",
      "hunks": [
        {"id": "hunk-cc19...", "index": 0, "type": "replace", "removed": "// TODO\n", "added": "app.get('/users', ...);\n", "before": {"start": 10, "lines": 1}, "after": {"start": 10, "lines": 1}},
        {"id": "hunk-4b20...", "index": 1, "type": "insert", "removed": "", "added": "app.get('/posts', ...);\n", "before": {"start": 11, "lines": 0}, "after": {"start": 11, "lines": 1}}
      ]
    },
    {
      "path": "src/lib/utils.ts",
      "status": "modified",
      "hunks": [
        {"id": "hunk-11bf...", "index": 0, "type": "replace", "removed": "function old()...\n", "added": "function new()...\n", "before": {"start": 5, "lines": 1}, "after": {"start": 5, "lines": 1}},
        {"id": "hunk-ee43...", "index": 1, "type": "insert", "removed": "", "added": "export function helper()...\n", "before": {"start": 6, "lines": 0}, "after": {"start": 6, "lines": 1}},
        {"id": "hunk-09ad...", "index": 2, "type": "delete", "removed": "// dead code\n", "added": "", "before": {"start": 20, "lines": 1}, "after": {"start": 20, "lines": 0}}
      ]
    }
  ]
}
```

### File-Level Selection

When all hunks in a file belong to the same logical change:

```bash
# Keep entire file, reset everything else
jj-hunk split '{"files": {"src/db/schema.ts": {"action": "keep"}}, "default": "reset"}' "feat: add database schema"
```

### Hunk-Level Selection

When a single file has mixed concerns (most powerful feature):

```bash
# src/lib/utils.ts has:
#   - hunks 0, 2: refactoring (rename + delete dead code)
#   - hunk 1: new feature (helper function)

# Extract just the refactoring
jj-hunk split '{"files": {"src/lib/utils.ts": {"hunks": [0, 2]}}, "default": "reset"}' "refactor: clean up utils"

# Hunk 1 remains in working copy for the next commit
jj describe -m "feat: add helper function"
```

### Mixed Selection

Combine file-level and hunk-level in one spec:

```bash
# Keep all of schema.ts + only hunk 0 from routes.ts
jj-hunk split '{"files": {"src/db/schema.ts": {"action": "keep"}, "src/api/routes.ts": {"hunks": [0]}}, "default": "reset"}' "feat: add users table and endpoint"

# Next: remaining routes.ts hunk
jj-hunk split '{"files": {"src/api/routes.ts": {"action": "keep"}}, "default": "reset"}' "feat: add posts endpoint"

# Final: utils changes
jj describe -m "refactor: utils cleanup"
```

### Complete Workflow Example

Starting with a messy commit containing schema, API, and refactoring changes:

```bash
# 1. Edit the commit
jj edit <revision>

# 2. Inspect all hunks
jj-hunk list

# 3. Split in narrative order

# Infrastructure first
jj-hunk split '{"files": {"src/db/schema.ts": {"action": "keep"}}, "default": "reset"}' "feat: add database schema"

# Refactoring second (specific hunks from utils.ts)
jj-hunk split '{"files": {"src/lib/utils.ts": {"hunks": [0, 2]}}, "default": "reset"}' "refactor: clean up utils"

# Feature using the refactored code
jj-hunk split '{"files": {"src/lib/utils.ts": {"action": "keep"}, "src/api/routes.ts": {"hunks": [0]}}, "default": "reset"}' "feat: add users endpoint"

# Remaining changes
jj describe -m "feat: add posts endpoint"

# 4. Verify
jj log -r 'trunk()..@'
```

### Verifying Splits

After splitting, verify each commit has the right content:

```bash
# Check stats for each commit
jj diff -r <rev1> --stat
jj diff -r <rev2> --stat

# Or view the log
jj log
```

## Tips

- **Always list first**: Run `jj-hunk list` to see hunk indices/ids before building specs
- **Prefer ids for stability**: Use `ids` when hunks might shift between list and apply
- **Use default wisely**: `"default": "reset"` is safer (explicit inclusion), `"default": "keep"` is convenient for excluding specific files
- **Combine with jj**: After splitting, use `jj describe` to refine commit messages
- **Exact paths required**: File paths must match exactly (e.g., `"src/lib.rs"` not `"src/"`)
