---
name: memrise
description: Operate the Memrise CLI for community courses, including authentication setup, course/level/word lookup, pool searches, and adding items. Use when requests mention `memcli` commands or the npm package `memrise-cli` (which installs the `memcli` binary), especially for command construction, troubleshooting flags, and script-friendly JSON output.
---

# Memrise

## Overview

Use this skill to run `memcli` safely and produce exact commands for common Memrise course operations.
Prefer commands that can be pasted directly, and switch to JSON output when results are consumed by scripts.

Read `references/commands.md` when you need full command/flag coverage.
Read `references/example-output.md` when you need concrete output examples.

## Runbook

1. Confirm installation state.
2. Confirm authentication source (env vars or flags).
3. Run a read-only command first (`courses`, `course-levels`, `words`, `search-pool`).
4. For level diagnostics, use `course-levels --include-empty` to surface empty/draft levels.
5. For automation, append `--output json` when supported.
6. Before write operations (`add-to-course`, `add-to-level`, `add-level`), validate the target IDs and fields with read commands.

## Installation And Auth

Use package install commands:

```bash
npm install -g memrise-cli
# or
bun add -g memrise-cli
```

Use environment variables by default:

```bash
export MEMRISE_USERNAME="your_username"
export MEMRISE_PASSWORD="your_password"
export MEMRISE_CLIENT_ID="your_client_id" # optional
```

For installed CLI usage with environment credentials:

```bash
memcli courses --output json
```

If running from source during development:

```bash
bun run ./dist/index.js courses --output json
```

Use `--username` and `--password` only when explicitly requested.

## Common Tasks

Use these as canonical examples:

```bash
# list teaching courses
memcli courses

# list levels (including empty drafts)
memcli course-levels <course-id> --include-empty

# list course words
memcli words <course-id>

# list words in a level with limit
memcli words <course-id> --level 1 --limit 10

# search pool by field
memcli search-pool <pool-id> --field "1=Hello"

# add item to course
memcli add-to-course <course-id> --field "1=Hello" --field "2=Bonjour"
```

When needed, use JSON columns format instead of repeated fields:

```bash
memcli add-to-course <course-id> --columns '{"1":"Hello","2":"Bonjour"}'
```

## Output Strategy

Use default human-readable output for interactive use.
Use `--output json` for automation, parsing, and downstream tools.

## Safety Checks

Before write operations:

1. Confirm the target object exists (`course-by-id`, `course-levels`, `get-pool`).
2. Confirm the fields map to the course column layout (`course-columns`).
3. Prefer a small test insert in a known sandbox course before bulk updates.

If credentials fail, re-check env var names and whether the user wants explicit `--username/--password` flags.

## Version Notes

Current npm package behavior (verified with `memcli --help`):
- `levels|course-levels` supports `--include-empty`.
- `rename-level|set-level-title` and `delete-level|remove-level` are available.
- Prefer live `memcli --help` output over stale examples when behavior differs.
