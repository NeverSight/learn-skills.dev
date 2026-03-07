---
name: list-repo-tasks
description: "List mise tasks grouped by namespace with dependency info. TRIGGERS - mise tasks, task list, show tasks, available tasks."
allowed-tools: Bash
argument-hint: "[namespace]"
model: haiku
---

# /mise:list-repo-tasks

List all mise tasks in the current repo, grouped by namespace with dependency information.

## Step 1: Get Task List

```bash
mise tasks ls 2>/dev/null
```

If no tasks found, report:

```
No mise tasks found in this repo.
To create release tasks: /mise:run-full-release
To learn task authoring: See mise-tasks skill
```

## Step 2: Group by Namespace

Parse the task list and group by colon-prefix namespace:

- `release:*` — Release workflow tasks
- `test:*` — Testing tasks
- `cache:*` — Cache management tasks
- `dev:*` — Development quality tasks (fmt, lint, typecheck)
- `validate:*` — Validation tasks
- `smoke:*` — Smoke/integration tests
- `bench:*` — Benchmarking
- Tasks without a namespace prefix go under "General"

## Step 3: Filter by Argument

If a namespace argument is provided (e.g., `/mise:list-repo-tasks release`):

- Filter to only tasks matching that namespace prefix
- Show the dependency DAG for those tasks:

```bash
# Show task details including depends
mise tasks ls --json 2>/dev/null | jq '.[] | select(.name | startswith("release:"))'
```

## Step 4: Show Dependency Chains

For filtered namespaces, show the dependency chain:

```
release:full
  └─ depends: release:postflight, release:pypi
     └─ release:postflight depends: smoke, release:build-all
        └─ release:build-all depends: release:version
           └─ release:version depends: release:sync
              └─ release:sync depends: release:preflight
```

## Example Output

```
═══════════════════════════════════════════
  mise Tasks: rangebar-py (45 tasks)
═══════════════════════════════════════════

release (10 tasks):
  full          Full release: version → build → smoke → publish
  dry           Preview without changes
  status        Current version info
  preflight     Validate prerequisites
  version       Bump version via semantic-release
  build-all     Build all platform artifacts
  macos-arm64   Build macOS ARM64 wheel
  linux         Build Linux wheel (cross-compile)
  sdist         Build source distribution
  pypi          Publish to PyPI

dev (4 tasks):
  fmt           Format code (cargo fmt + ruff)
  lint          Lint code (clippy + ruff)
  test          Run test suite
  deny          Check dependencies (cargo-deny)

cache (3 tasks):
  status        Show cache population status
  populate      Populate ClickHouse cache
  clear         Clear local cache

General:
  smoke         Integration smoke tests
  bench         Benchmarking suite
═══════════════════════════════════════════
```
