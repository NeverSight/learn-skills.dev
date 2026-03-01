---
name: fix-ci
description: Automatically diagnose and fix CI failures in the current PR. Retrieves failed logs from GitHub Actions, categorizes the failure (lint, format, type-check, test), applies targeted fixes, verifies locally, and commits/pushes. Use when CI fails after push.
---

# Fix CI Failures

This skill automatically diagnoses and fixes CI failures for the current branch by fetching GitHub Actions logs, categorizing the failure, applying targeted fixes, and pushing the result.

## Usage

```
/fix-ci           # Auto-diagnose and fix
/fix-ci --dry-run # Show what would be fixed without applying
```

## Workflow

### Step 1: Fetch CI Failure Details

Determine the current branch:

```bash
git branch --show-current
```

Fetch the latest CI run for this branch:

```bash
gh run list --branch <current-branch> --limit 1 --json databaseId,conclusion
```

- If the latest run has `"conclusion": "failure"`, fetch the failed logs:
  ```bash
  gh run view <run-id> --log-failed
  ```
- If no failed run is found (conclusion is "success" or no runs exist), report "No CI failures found" and stop.

### Step 2: Categorize Failure

Parse the failed log output to determine the failure type(s):

- **lint**: ruff check errors (look for `ruff check` output, rule codes like E, F, I, UP, B, SIM)
- **format**: ruff format errors (look for `ruff format` output, "would reformat" messages)
- **type**: mypy errors (look for `mypy` output, type annotation errors like "Incompatible type", "Missing return")
- **test**: pytest failures (look for `pytest` output, "FAILED" markers, assertion errors)
- **multiple**: if more than one category is detected, fix them in order: format -> lint -> type -> test

### Step 3: Apply Fixes

Apply targeted fixes based on the failure category:

**For format errors:**
```bash
ruff format synapse/ tests/
```

**For lint errors:**
```bash
ruff check --fix synapse/ tests/
```

**For type errors:**
- Read the specific mypy error messages from the log
- Identify the file and line number for each error
- Read the source code around the error location
- Apply targeted fixes to the type annotations (add return types, fix incompatible types, add missing imports)

**For test failures:**
- Read the pytest output to identify failing test names and assertion errors
- Read the failing test code and the source code under test
- Determine whether the fix belongs in the source code or the test
- Apply the targeted fix

After each fix category, run the corresponding check locally to verify before proceeding to the next category.

If `--dry-run` flag is provided: report what would be fixed for each category but do NOT apply any changes, do NOT commit, and do NOT push.

### Step 4: Local Verification

Run all relevant checks to verify the fixes:

```bash
ruff check synapse/ tests/
```

```bash
ruff format synapse/ tests/ --check
```

```bash
uv run mypy synapse/
```

If test failures were involved:
```bash
pytest
```

If any check still fails after the initial fix, attempt one more targeted fix for that category (max 1 retry per category). If it still fails after the retry, proceed to the error handling step.

### Step 5: Commit and Push

After all checks pass locally:

1. Stage only modified files (do NOT stage untracked files):
   ```bash
   git add -u
   ```

2. Commit with a descriptive message indicating which categories were fixed:
   ```bash
   git commit -m "fix: resolve CI failures (<categories>)"
   ```
   Where `<categories>` is a comma-separated list of what was fixed (e.g., `lint, format` or `test` or `format, lint, type, test`).

3. Push to the current branch:
   ```bash
   git push
   ```

4. Report a summary of what was fixed, including:
   - Which failure categories were detected
   - Which files were modified
   - Whether all local checks pass

### Step 6: Error Handling

- **gh CLI not authenticated**: If `gh run list` fails with an authentication error, report "GitHub CLI is not authenticated. Run `gh auth login` first." and stop.
- **Fixes do not resolve the issue**: If local verification still fails after one retry per category, report exactly what remains broken (include the error output) and stop. Do NOT commit partial fixes that leave CI in a broken state.
- **Never force-push**: Always use `git push`, never `git push --force` or `git push --force-with-lease`.

## Examples

### Auto-diagnose and fix all CI failures
```
/fix-ci
```

### Preview what would be fixed without applying changes
```
/fix-ci --dry-run
```

## Tool Configuration

This project uses the following CI checks (from pyproject.toml):

### Ruff
- Target: Python 3.10
- Line length: 88
- Rules: E, F, I, UP, B, SIM
- Ignored: E501, B008
- Excluded: synapse/proto/a2a_pb2*.py

### Mypy
- Strict mode with disallow_untyped_defs
- Tests have relaxed rules (ignore_errors)
- Proto files excluded

### Pytest
- asyncio_mode: auto
- Run with: `pytest` or `pytest tests/ -v`
