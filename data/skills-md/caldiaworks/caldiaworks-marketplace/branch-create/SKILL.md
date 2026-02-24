---
name: branch-create
version: 0.2.0
description: "Create feature branches linked to issues with consistent naming conventions. Generates branch names from issue numbers and descriptions, creates the branch, and checks it out. Use when: create branch, new branch, feature branch, branch for issue, start working on issue, branch-create, /branch-create."
---

# Feature Branch Creation

Create a feature branch linked to an issue with a consistent naming convention. Works in any Git repository.

## Workflow

### Step 1: Collect Input

Gather the issue number for the branch name.

1. Ask the user for the issue number. If provided as an argument, use it directly.
2. If the issue number is provided, verify it exists with `gh issue view <number>`. If the issue does not exist, inform the user and stop.
3. Derive a short description from the issue title automatically. Only ask the user for a description if the issue has no title.

### Step 2: Generate Branch Name

Generate the branch name following the project's naming convention.

1. Default convention: `feature/<issue-number>-<description>`
2. Convert the description to lowercase kebab-case:
   - Replace spaces and underscores with hyphens
   - Remove special characters
   - Collapse consecutive hyphens

If the project has a different convention documented (e.g., in CLAUDE.md or CONTRIBUTING.md), follow that convention instead.

### Step 3: Create and Checkout

1. If a branch with the same name already exists, inform the user and ask whether to:
   - Checkout the existing branch, or
   - Choose a different name
2. Create the branch from the current HEAD: `git checkout -b <branch-name>`
3. Display the branch name and associated issue number.

## Constraints

- Do not push the branch to remote automatically. The user decides when to push.
- Do not modify the issue (no labels, no assignees) -- branch creation is the only action.
