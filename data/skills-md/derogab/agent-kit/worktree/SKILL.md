---
name: worktree
description: Resolve missing gitignored files in a git worktree by symlinking them from the main repository.
---

## Context

- Git common dir: !`git rev-parse --git-common-dir`
- Git dir: !`git rev-parse --git-dir`
- Worktree list: !`git worktree list`
- Project root: !`git rev-parse --show-toplevel`

## Your task

Resolve the missing file or path described in: $ARGUMENTS

### Pre-flight checks

1. If `$ARGUMENTS` is empty, stop immediately and tell the user to provide the error message or missing path. Do nothing else.
2. If `Git common dir` and `Git dir` resolve to the same path, this is **not** a worktree. Stop and tell the user the missing file issue is unrelated to worktrees. Do nothing else.

### Parse the missing item

Extract the missing file or directory path(s) from `$ARGUMENTS`. It may be:
- A direct path (e.g. `src/config/keys`)
- An error message containing a path (e.g. `Cannot find module './config/secrets.js'`)
- Multiple paths separated by spaces

Resolve each path relative to the project root. Canonicalize it and verify the absolute path is strictly within the project root. If it escapes the project root (e.g. via `../` traversal), refuse the operation and inform the user.

If multiple paths are provided, repeat the workflow below for each one.

### Try project setup commands first

Skip this step if the missing item is clearly not something an install command would generate (e.g. credentials, API keys, `.env` files, config secrets).

Otherwise:
1. Look for a dependency manifest (`package.json`, `requirements.txt`, `Gemfile`, `go.mod`, etc.) and check for `prepare`, `postinstall`, `build`, or similar scripts.
2. Run the standard install/build command if it could plausibly generate the missing item.
3. If the item now exists, report success and stop — no symlink needed.

### Locate the source in the main repository

The first entry in `Worktree list` is the main worktree. Construct the expected path by combining the main repo root with the relative path of the missing item. If the item does **not** exist in the main repo either, stop and inform the user.

### Create a relative symlink

1. Ensure the parent directory exists in the worktree.
2. Compute the relative path from the symlink location to the source:
   ```bash
   perl -e 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])' "<source-path>" "<symlink-parent-dir>"
   ```
3. Create the symlink:
   ```bash
   ln -sfn "<relative-path-to-source>" "<target-path-in-worktree>"
   ```

### Verify and report

1. Verify the symlink resolves correctly (`ls -la`, `test -e`).
2. Report what was missing, where the symlink points, and confirmation it resolves.

### Rules

- Never copy files — always symlink so the worktree stays in sync.
- Use relative symlinks — they are more portable than absolute paths.
- Do not modify the main repository — only create symlinks in the worktree.
- Never modify symlinked files — changes would propagate to the main repo.
- Handle directories too — the missing item may be an entire directory.
- Always quote paths in shell commands.
- Do not run tests or other downstream verification.
- Do not send any text besides the tool calls.
