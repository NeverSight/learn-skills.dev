---
name: git-commit
description: >
  Create git commits per project conventions — analyze, split, stage, message.
  Use when the user asks to commit, commit changes, or says "commit and MR" for
  the commit step. Load before staging or committing anything.
---

# git-commit

Create small, readable commits named according to project conventions.

## Execution

### Step 1 — Read project commit guidelines (HARD GATE)

You MUST find and read the project's commit documentation before proceeding. If none exists, use conventional commits with scope.

**Completion**: Commit format, scope rules, and any special conventions pinned — or the conventional-commits fallback chosen when no project commit doc exists.

### Step 2 — Analyze changes

Understand all staged and unstaged changes. Group related changes by logical scope.

**Completion**: Change set understood and grouped.

### Step 3 — Split into commits

Split into separate commits when changes are logically distinct. Each commit should be one coherent unit.

**Completion**: Commit plan ready.

### Step 4 — Create commits

For each commit: stage, write the message following project guidelines, remove any "co-authored" notes, include useful body descriptions for complex changes.

**Completion**: All commits created.

### Step 5 — Report

Print each commit hash and message.

**Completion**: All commits reported.
