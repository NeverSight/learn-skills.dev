---
name: finishing-grove-workspace
description: Use when implementation is complete, all tests pass, and the agent is operating inside a Grove workspace that needs to be resolved or cleaned up
---

I'm using the finishing-grove-workspace skill to wrap up this Grove workspace.

## Workflow

### Step 1: Detect workspace

```bash
test -f "$(git rev-parse --show-toplevel)/.grove/workspace.json"
```

If `.grove/workspace.json` is not found: this is not a Grove workspace. Use `superpowers:finishing-a-development-branch` instead.

### Step 2: Verify tests pass

Auto-detect the test command from marker files:

| Marker file | Test command |
|---|---|
| `go.mod` | `go test ./...` |
| `package.json` | `npm test` |
| `Cargo.toml` | `cargo test` |
| `build.gradle` / `build.gradle.kts` | `./gradlew test` |
| `pyproject.toml` / `requirements.txt` | `pytest` |
| `Makefile` | `make test` |

If tests fail, stop. Do not present completion options.

### Step 3: Read workspace metadata

```bash
cat .grove/workspace.json
```

Extract `id`, `golden_copy`, and `branch` from the JSON output.

### Step 4: Present options

Present exactly these four options:

1. Push branch and create a Pull Request
2. Push branch and destroy workspace
3. Keep workspace as-is
4. Discard work and destroy workspace

### Step 5: Execute choice

**Option 1: Push + PR**

Derive the PR title from the branch name and the body from a summary of commits since the golden copy.

```bash
git push -u origin <branch>
gh pr create --title "<title>" --body "<body>"
grove destroy <workspace-id>
cd <golden-copy-path>
```

**Option 2: Push + destroy**

```bash
git push -u origin <branch>
grove destroy <workspace-id>
cd <golden-copy-path>
```

**Option 3: Keep as-is**

Report: "Keeping workspace at <path>."

**Option 4: Discard**

Require the user to type "discard" before proceeding.

```bash
grove destroy <workspace-id>
cd <golden-copy-path>
```

## Quick Reference

| Option | Push branch | Create PR | Keep workspace | Cleanup |
|---|---|---|---|---|
| 1. Push + PR | yes | yes | no | yes |
| 2. Push + destroy | yes | no | no | yes |
| 3. Keep as-is | no | no | yes | no |
| 4. Discard | no | no | no | yes |

## Common Mistakes

- **Skipping test verification** — never present completion options before confirming tests pass.
- **Open-ended questions** — always present the structured four-option list; do not ask "what would you like to do?" in free form.
- **Automatic workspace cleanup** — if the user selects option 3, do not run `grove destroy`. Respect the choice to keep the workspace.
- **No confirmation for discard** — option 4 destroys uncommitted work; always require the user to type "discard" before executing.

## Red Flags

- `.grove/workspace.json` missing but `.grove/config.json` present — the agent is on the golden copy, not in a workspace. Route to `superpowers:finishing-a-development-branch`.
- `grove destroy` fails — the workspace ID may be stale. Run `grove list` to confirm the workspace exists before retrying.

## Integration

- **Replaces:** `superpowers:finishing-a-development-branch` when in a Grove workspace
- **Called by:** `superpowers:subagent-driven-development` (Step 7), `superpowers:executing-plans` (Step 5)
- **Pairs with:** `grove:using-grove`
