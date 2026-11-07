---
name: commit-and-push
description: Audit local changes, pull latest remote updates, compose a descriptive commit message with rationale and scope, and push to remote. Use when the user asks to commit, push code, sync changes with remote, or ship work.
---

# Commit and Push

Safely package local changes into descriptive, atomic commits and synchronize with the remote repository.

## Steps

### 1. Remote Synchronization

Pull incoming changes from the remote tracking branch before committing local work to prevent split histories or push conflicts.

- Fetch remote updates: `git fetch`
- Pull changes from remote: `git pull --rebase` (or `git pull` if standard merge is preferred)
- **Completion criterion**: Local branch is up to date with remote tracking branch, with any pull conflicts resolved.

### 2. Working Tree Audit

Examine all modified, added, deleted, and untracked files to build full context on what changed and why.

- Run `git status` to view current branch and file states across working directory and staging index.
- Run `git diff` for unstaged changes and `git diff --staged` for staged changes.
- **Completion criterion**: Every changed file and diff chunk is categorized into staged work, ignored scratch files, or uncommitted files.

### 3. Selective Staging & Safety Filter

Stage deliberate changes while guarding against committing temporary files or sensitive material.

- Verify no secrets, credentials, environment files (`.env`), or temporary scratch files are staged.
- Stage intended files explicitly (`git add <file1> <file2>` or `git add .` after verification).
- **Completion criterion**: Staging index contains strictly intended changes; no secret or scratch files present.

### 4. Descriptive Commit Message Formulation

Construct a clear commit message consisting of an imperative summary header and a detailed body explaining motivation and scope.

- **Header**: Imperative mood summary (max 72 chars), optionally using conventional prefixes (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- **Body**: Detailed breakdown including:
  - **Why**: The problem, requirement, or intent behind the change.
  - **What**: Summary of key changes made across files or modules.
  - **Context/Issues**: References to issue numbers or breaking changes if applicable.
- Execute commit: `git commit -m "<header>" -m "<body>"`
- **Completion criterion**: Commit is created locally, and `git log -n 1` shows the descriptive header and body.

### 5. Remote Push & Verification

Publish local commits to the remote tracking branch and confirm clean synchronization.

- Push to upstream branch: `git push` (or `git push -u origin <branch>` if upstream tracking is not set).
- Verify clean status: `git status -sb`
- **Completion criterion**: `git status` reports working tree clean and local branch up to date with remote tracking branch.
