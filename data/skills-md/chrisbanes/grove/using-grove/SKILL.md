---
name: using-grove
description: Use when starting feature work that needs isolation from the current workspace, or before executing implementation plans in a Grove-enabled repository
---

I'm using the using-grove skill to create an isolated workspace with warm build state.

## Workflow

### Step 1: Verify Grove is initialized

```bash
test -f "$(git rev-parse --show-toplevel)/.grove/config.json"
```

If `.grove/config.json` is not found: Grove is not initialized in this repo. Use the `grove:grove-config` skill to set it up first.

### Step 2: Verify grove CLI is installed

```bash
command -v grove
```

If not found: Grove CLI is not installed. See https://github.com/chrisbanes/grove for installation instructions.

### Step 3: Create workspace

```bash
grove create --branch <branch-name> --json
```

Parse the JSON output for `path` and `id`:

```json
{
  "id": "abc1",
  "path": "/tmp/grove/myapp/abc1",
  "branch": "agent/fix-login",
  "created_at": "2026-02-17T10:20:00Z",
  "golden_copy": "/Users/chris/dev/myapp"
}
```

### Step 4: Enter the workspace

```bash
cd <path-from-json>
```

### Step 5: Verify baseline

Run the project test suite. Auto-detect the test command from marker files:

| Marker file | Test command |
|---|---|
| `go.mod` | `go test ./...` |
| `package.json` | `npm test` |
| `Cargo.toml` | `cargo test` |
| `build.gradle` / `build.gradle.kts` | `./gradlew test` |
| `pyproject.toml` / `requirements.txt` | `pytest` |
| `Makefile` | `make test` |

If tests fail, report the failures and ask whether to proceed.

### Step 6: Report ready

```
Grove workspace ready.
  Path:        <workspace-path>
  Branch:      <branch-name>
  Build state: warm (cloned from golden copy)
```

## Quick Reference

| Command | Purpose |
|---|---|
| `grove create --branch <name> --json` | Create workspace, get JSON output |
| `grove list` | List active workspaces |
| `grove destroy <id>` | Remove a workspace |

## Common Mistakes

- **Using plain `git worktree`** — worktrees start with a cold build cache. Grove's CoW clone preserves warm build state, making the first build incremental rather than from scratch.
- **Skipping `--json` flag** — the JSON output is required to reliably extract the workspace path and ID for later use.
- **Not verifying grove initialized** — `grove create` will fail confusingly if `.grove/` is absent. Always check first.

## Red Flags

- `grove create` errors about uncommitted changes on the golden copy — clean up or commit the golden copy first, or use `--force` if the changes are intentional.
- Tests fail at baseline — the golden copy's build state is stale. Run `grove update` on the golden copy before creating workspaces.
- `grove` command not found after install — check PATH; grove installs to `$GOPATH/bin` by default.

## Integration

- **Replaces:** `superpowers:using-git-worktrees` — prefer this skill in any Grove project. Disable `using-git-worktrees` to avoid conflicts.
- **Called by:** `superpowers:brainstorming` (Phase 4), `superpowers:subagent-driven-development`, `superpowers:executing-plans`
- **Pairs with:** `grove:finishing-grove-workspace` — use that skill when implementation is complete and the workspace is ready to clean up.
