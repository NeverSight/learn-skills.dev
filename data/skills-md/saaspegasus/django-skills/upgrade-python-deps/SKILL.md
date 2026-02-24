---
name: upgrade-python-deps
description: Upgrade Python dependencies using uv, then run post-upgrade checks to ensure nothing is broken.
allowed-tools: [
    Bash(uv lock *),
    Bash(uv sync *),
    Bash(make test *),
    Bash(uv run mypy *),
]
---

## Your task

Upgrade all Python dependencies and verify nothing is broken.

### Step 1: Upgrade the lock file

Run `uv lock --upgrade` to upgrade all dependencies to their latest compatible versions.

Review the output for any resolution errors. If there are conflicts, report them to the user
and ask how to proceed before continuing.

### Step 2: Sync the environment

Run `uv sync` to install the upgraded dependencies into the virtual environment.

### Step 3: Run post-upgrade checks

Run these checks sequentially, stopping if any step fails:
- **Type checking**: Run `uv run mypy .` and report any new type errors. These may be caused
  by updated type stubs or changes in library APIs.
- **Tests**: Run `make test` to verify the test suite still passes.

### Step 4: Summarize and commit

Summarize what was done:
- Which packages were upgraded (notable version changes)
- Whether any type errors were introduced
- Whether all tests passed
- Any issues that need manual attention

If there were failures, present the issues and ask how the user wants to proceed.

If everything passed, ask the user if they'd like to commit the changes. If yes, commit
using the `/commit` skill.
