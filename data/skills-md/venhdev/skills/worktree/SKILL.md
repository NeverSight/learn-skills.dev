---
name: worktree
description: "Isolate concurrent agent sessions in dedicated Git worktrees under .agents/worktree/ to prevent workspace collisions."
disable-model-invocation: true
---

# worktree — Isolated Session & Branching Engine

## Operating Invariants

- **Path Isolation**: Confine all branch edits, shell commands, and test executions strictly within `.agents/worktree/<branch>`; forbid modifying root repository files from a worktree session.
- **Dirty Tree Breaker**: Verify working tree cleanliness via `git status --porcelain` before deleting a worktree; forbid deleting worktrees containing uncommitted modifications.
- **Pre-Mutation Gate**: Stage worktree creation or removal in Canonical Changeset format and halt turn immediately; forbid executing worktree mutations on disk without affirmative human authorization.

## Domain Rubric

### 1. Naming & Storage Conventions

- `<branch>`: Strictly format as `<type>/<slug>` (`feat/`, `fix/`, `refactor/`, `chore/`, `test/`).
- `<path>`: Dedicated path strictly under `.agents/worktree/<branch>`.
- Privacy Anchor: Root `.gitignore` must contain `.agents/worktree/`.

### 2. Supported Worktree Operations

- `[CREATE]`: Add a new worktree branch checked out at target path.
- `[DELETE]`: Remove worktree directory and prune git administrative metadata.
- `[LIST]`: Inspect active worktrees and associated branches.
- `[PRUNE]`: Clean up squash-merged branches safely via `scripts/prune-squashed.sh`.

## Canonical Output Contract

```text
# Changeset: Git Worktree <Action>

`-- .agents/worktree/<branch>/
    `-- [<ACTION>] <Worktree operation summary>.

Summary: 1 worktree affected (<branch>).
```

## Execution Protocol

### Phase 1: Pre-flight & Collision Audit

1. For create: Inspect `git worktree list` and verify no branch or directory collision exists.
2. For delete: Inspect `git status --porcelain` inside target `<path>`. If dirty, halt immediately and report uncommitted files.
3. For list: Run `git worktree list` and present active worktrees, halting turn immediately.

### Phase 2: Staging & Authorization Gate

1. Stage the planned worktree modification in Canonical Changeset format.
2. Present the staging summary and halt turn immediately for human authorization.

### Phase 3: Atomic Execution & Handoff

1. On approval, execute the required operation:
   - Create: `git worktree add <path> -b <branch> <base_ref>`
   - Delete: `git worktree remove <path> && git worktree prune`
   - Prune: `bash scripts/prune-squashed.sh <target_branch>`
2. Report operation completed with the absolute workspace path for IDE navigation.
