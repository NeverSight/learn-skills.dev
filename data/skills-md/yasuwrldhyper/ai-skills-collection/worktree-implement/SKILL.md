---
name: worktree-implement
description: git worktreeを自動作成して独立した実装環境を準備する。cleanup引数でworktreeを削除する。
argument-hint: <task-description> | cleanup
allowed-tools: Bash, Read, Glob, Write, AskUserQuestion
---

# /worktree-implement Skill

Create an isolated git worktree for implementing a feature or fix described in `$ARGUMENTS`.
If `$ARGUMENTS` is `cleanup`, remove the worktree instead.

---

## Phase 1: Parse Arguments

Check whether `$ARGUMENTS` equals `cleanup` (case-insensitive).

- If yes → skip to **Phase 3 (Cleanup)**.
- If no → continue to **Phase 2 (Create)**.

### Branch Name Generation

From the task description in `$ARGUMENTS`, derive a short, kebab-case branch name:

1. Detect intent prefix from keywords:
   - Bug / fix / error / issue → `fix/`
   - Docs / readme / documentation → `docs/`
   - Refactor / cleanup / restructure → `refactor/`
   - Test / spec / coverage → `test/`
   - Everything else → `feat/`

2. Slugify the description:
   - Lowercase
   - Replace spaces and special characters with `-`
   - Remove leading/trailing `-`
   - Truncate to 40 characters

Example: `"add payment webhook handler"` → `feat/add-payment-webhook-handler`

---

## Phase 2: Create Worktree

Run the following steps in order:

### 2-1. Verify repository state

```bash
git -C . rev-parse --show-toplevel
```

If this fails, stop and inform the user: "Not inside a git repository."

### 2-2. Check for uncommitted changes

```bash
git status --short
```

If there are uncommitted changes, warn the user:
```
⚠️  You have uncommitted changes in the current working tree.
    These will NOT be carried over to the new worktree.
    Continue? (yes / no)
```

Use AskUserQuestion to ask for confirmation before proceeding.

### 2-3. Create the worktree

```bash
git worktree add .claude/worktrees/<slug> -b <branch-name>
```

Where:
- `<slug>` is the kebab-case name (without prefix, e.g. `add-payment-webhook-handler`)
- `<branch-name>` is the full branch name (e.g. `feat/add-payment-webhook-handler`)

If a worktree with that name already exists, append `-2`, `-3`, etc. until unique.

### 2-4. Display result

After successful creation, display:

```
✅ Worktree created:
   Path:    .claude/worktrees/<slug>
   Branch:  <branch-name>
   Base:    <current-branch> @ <short-sha>

Next steps:
   cd .claude/worktrees/<slug>   # work in isolation
   /worktree-implement cleanup   # remove when done
```

---

## Phase 3: Cleanup

### 3-1. List existing worktrees

```bash
git worktree list
```

Display the list and ask the user which worktree to remove if multiple exist under `.claude/worktrees/`:

```
Worktrees under .claude/worktrees/:
  1. feat/add-payment-webhook-handler  →  .claude/worktrees/add-payment-webhook-handler
  2. fix/null-pointer-crash            →  .claude/worktrees/null-pointer-crash

Which worktree to remove? (enter number or branch name, or "all" to remove all)
```

Use AskUserQuestion to ask for confirmation.

### 3-2. Check for uncommitted changes

Before removing, run:

```bash
git -C .claude/worktrees/<name> status --short
```

If there are uncommitted changes, warn the user:
```
⚠️  Worktree '.claude/worktrees/<name>' has uncommitted changes.
    Removing it will discard these changes permanently.
    Proceed? (yes / no)
```

Use AskUserQuestion to confirm.

### 3-3. Remove worktree

```bash
git worktree remove .claude/worktrees/<name> --force
git worktree prune
```

### 3-4. Display result

```
✅ Worktree removed:
   Path:    .claude/worktrees/<name>
   Branch:  <branch-name> (branch still exists; delete with: git branch -d <branch-name>)

   git worktree prune completed.
```

If the user also wants to delete the branch, run:

```bash
git branch -d <branch-name>
```

(Use `-D` only if the user explicitly confirms the branch has unmerged changes they want to discard.)
