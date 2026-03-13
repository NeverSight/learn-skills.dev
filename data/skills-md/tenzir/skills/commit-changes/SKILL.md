---
name: commit-changes
description: >-
  Commit changes in Tenzir projects. Use when committing, staging, splitting
  changes into logical units, writing commit messages, or when the user says
  "commit this", "save my changes", "let's check this in", or "make a commit."
  Also use when the user wants to run linters or formatters before committing.
metadata:
  requires:
    skills:
      - follow-python-conventions
---

# Commit Changes

Commit changes as clean, reviewable snapshots.

## Workflow

### 1. Gather change context

Gather `git` context to identify what changed.

### 2. Run project checks

Run the project's relevant linters, type checkers, and formatters. For Python
projects, delegate to the `follow-python-conventions` skill for the specific
quality gates.

### 3. Perform commits

Split orthogonal changes into separate logical units. For each unit:

1. Stage the relevant files.
2. [Create the commit message](references/write-commit-messages.md).
3. Perform the commit.
