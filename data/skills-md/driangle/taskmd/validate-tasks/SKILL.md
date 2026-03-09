---
name: validate-tasks
description: Validate task files for format and convention errors. Use when the user wants to check their task files.
allowed-tools: Bash
---

# Validate

Validate task files using the `taskmd` CLI.

## Instructions

The user's arguments are in `$ARGUMENTS` (e.g. a directory path, `--format json`).

1. Run `taskmd validate $ARGUMENTS`
   - If `$ARGUMENTS` is empty, run: `taskmd validate`
2. Present the validation results to the user
3. If there are errors, suggest fixes
