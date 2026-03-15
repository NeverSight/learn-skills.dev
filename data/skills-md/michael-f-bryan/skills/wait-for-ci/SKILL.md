---
name: wait-for-ci
description: Wait for a GitHub Actions run to finish with minimal terminal output and a reliable exit code. Use when an agent must wait for CI to pass (e.g. after push, after opening a PR, or when verifying a specific run). Prefer gh run watch with --exit-status and --compact to avoid flooding context with poll output.
---

# Wait for CI (GitHub Actions)

When waiting for a GitHub Actions run to complete, use `gh run watch` with flags that minimise stdout and provide a checkable exit code. Do **not** run plain `gh run watch <run-id>`; it polls every 3 seconds and prints full pipeline status each time, which wastes context.

## Command

```bash
gh run watch <run-id> --exit-status --compact
```

- **`--exit-status`**: Exits with non-zero status if the run fails. Use the command’s exit code to decide success/failure.
- **`--compact`**: Shows only relevant or failed steps instead of every step, reducing output size.

## Optional: reduce poll frequency

To cut down output further, increase the refresh interval (default 3 seconds):

```bash
gh run watch <run-id> --exit-status --compact --interval 10
```

## Checking the result

After the command exits:

- **Exit code 0** → run succeeded.
- **Non-zero exit code** → run failed or was cancelled.

In shell scripts or when deciding next steps, rely on `$?` or the command in a conditional, e.g.:

```bash
gh run watch 12345 --exit-status --compact || echo "CI failed"
```

## Getting a run ID

- From the URL of a run: `https://github.com/owner/repo/actions/runs/<run-id>`.
- From the CLI after a push: `gh run list --limit 1` and use the run ID from the first row.
- After `gh pr create` or `gh pr checks`: the run ID may be in the command output or from `gh run list`.

## Repo in another repository

Use `-R owner/repo` when the run is not in the current repo:

```bash
gh run watch <run-id> --exit-status --compact -R owner/repo
```
