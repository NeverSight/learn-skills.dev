---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace using Antigravity 2.0's native workspace isolation.

**Core principle:** Detect existing isolation first. Then use `Workspace: "branch"` on `invoke_subagent`. Never use manual `git worktree add`.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

**Before creating anything, check if you are already in an isolated workspace.**

**Verify Git Repository Existence:**

If not inside a git repository, you cannot use worktrees. Check if you need to run `git init` first.

```bash
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "ERROR: Not inside a Git repository."
    exit 1
fi
```

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Verify:

```bash
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** Already isolated. Skip to Step 2.

**If `GIT_DIR == GIT_COMMON` (or in a submodule):** Normal repo. Proceed to Step 1.

## Step 1: Create Isolated Workspace

**For subagent tasks:** Use `Workspace: "branch"` parameter on `invoke_subagent`. This creates an isolated workspace on a new git branch automatically. The platform handles directory placement, branch creation, and cleanup.

**For parent orchestrator feature branches:** Use `git checkout -b <branch>` directly. No worktree needed — the orchestrator works in place on a feature branch.

## Step 2: Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Step 3: Verify Clean Baseline

Run tests to ensure workspace starts clean:

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.
**If tests pass:** Report ready.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Subagent task | `Workspace: "branch"` on `invoke_subagent` |
| Parent orchestrator | `git checkout -b <branch>` |
| Tests fail during baseline | Report failures + ask |

## Workspace Mode Decision Table

Antigravity 2.0 supports three workspace modes for subagents. Choose based on the agent's role:

| Mode | Syntax | Use for | Example |
|------|--------|---------|----------|
| `branch` | `Workspace: "branch"` | Agents that need isolated write access | Implementers, fixers |
| `inherit` | `Workspace: "inherit"` | Read-only agents | Reviewers, analyzers |
| `share` | `Workspace: "share"` | Agents editing different files in same repo | Parallel fixers on separate test files |

**Rules of thumb:**
- If the agent writes code → `branch`
- If the agent only reads and reports → `inherit`
- If multiple agents edit non-overlapping files → `share`

## Red Flags

**Never:**
- Use `git worktree add` — use `Workspace: "branch"` instead
- Create a worktree when Step 0 detects existing isolation
- Skip baseline test verification
- Proceed with failing tests without asking

**Always:**
- Run Step 0 detection first
- Use native workspace isolation
- Auto-detect and run project setup
- Verify clean test baseline
