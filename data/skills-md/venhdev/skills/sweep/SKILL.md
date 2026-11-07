---
name: sweep
description: "Audit workspace hygiene, stage reclaimable transient artifacts, and atomically purge completed tasks, stale scratch files, and merged worktrees."
disable-model-invocation: true
---

# sweep — Workspace Hygiene & Clean-Purge Engine

## Operating Invariants

- **Pre-Mutation Gate**: Stage all candidate deletions in the Canonical Output Contract and halt for affirmative authorization before deleting files.
- **Active Work Preservation**: Purge exclusively verified completed artifacts; preserve plan dossiers in `.agents/scratch/plans/` containing active phases (`PLANNED`, `CLAIMED`, `IN_PROGRESS`, `DRIFTED`), task collections containing `ready` or `in-progress` tasks, dirty worktrees, and unmerged branches.
- **Targeted Scope**: Confine deletions strictly to `.agents/scratch/`, fully completed `.agents/tasks/<feature-slug>/` directories, and merged `.agents/worktree/` paths.
- **Atomic Execution**: Execute approved deletions atomically, prune orphaned git administrative metadata via `git worktree prune`, and report reclaimed status.

## Domain Rubric

### 1. Reclamation Dimensions
1. *Scratch & Dossiers*: Temporary scripts (`hitl-loop.sh`), subagent traces (`*-dossier.md`), absorbed spike directories, and completed plan dossiers (`COMPLETED` or `REJECTED`) in `.agents/scratch/`.
2. *Completed Task Collections*: Feature directories under `.agents/tasks/<feature-slug>/` where all contained tasks have `Status: done`.
3. *Merged Worktrees & Branches*: Clean worktrees under `.agents/worktree/` and squash-merged local branches verified via `scripts/prune-squashed.sh`.

### 2. State
- `CLEAN`: Workspace contains zero uncollected transient artifacts.
- `STAGED`: Reclaimable items identified and staged for user approval.
- `DONE`: Approved deletions executed and filesystem state verified.
- `UNRESOLVED`: Dirty working trees or unverified task states prevent safe deletion.

## Canonical Output Contract

```markdown
# Sweep Manifest: Workspace Hygiene · <CLEAN | STAGED | DONE | UNRESOLVED>

| Dimension | Target Coordinate | Reclamation Action |
| :--- | :--- | :--- |
| Scratch | .agents/scratch/<file_or_dir> | Delete ephemeral trace / PoC |
| Tasks | .agents/tasks/<feature-slug>/ | Delete completed feature collection |
| Worktree | .agents/worktree/<branch>/ | Remove worktree and prune metadata |
| Branch | <branch_name> | Delete squash-merged local branch |

Summary: <N> items staged for purge.
*(omit if clean)* Gap: <Blocker preventing deletion, e.g. dirty worktree.>
```

### Routing

- Workspace is CLEAN, continue development → (via /forge).
- Unfinished tasks detected during audit → (via /track-tasks).
- Ambiguous branch or task ownership → (via /clarify).

## Execution Protocol

1. **Audit**: Scan `.agents/scratch/`, `.agents/tasks/`, `.agents/worktree/`, and local branches. If clean, output `CLEAN` and halt.
2. **Stage**: Group candidate deletions by dimension, verify all safety constraints (zero uncompleted tasks, zero dirty trees), present `STAGED` manifest, and halt for authorization.
3. **Purge**: On approval, delete staged files/directories, run `git worktree prune`, execute `bash scripts/prune-squashed.sh`, and report `DONE`.
