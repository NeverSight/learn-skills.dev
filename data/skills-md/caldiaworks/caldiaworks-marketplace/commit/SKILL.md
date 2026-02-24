---
name: commit
version: 0.3.0
description: "Create focused git commits with change review, selective staging, and auto-drafted messages. Use when: commit, git commit, save changes, commit my work, make a commit, stage and commit, review changes before committing. Also use when the user says /commit or asks to commit specific files."
---

# Git Commit

Guide the user through creating a focused, well-described git commit. This skill works in any Git repository.

Commits happen frequently during development -- they protect against lost work and repository damage. Speed and clarity matter.

## Workflow

### Step 1: Review Changes

Show the user what has changed so they can decide what to commit.

1. Run `git status` to display staged and unstaged changes.
2. Run `git diff` (unstaged) and `git diff --staged` (staged) to show the content of changes.
3. If there are no changes at all (clean working tree with nothing staged), inform the user there is nothing to commit and stop.

### Step 2: Stage Files

Determine which files to include in this commit.

- If the user has already specified files to commit, stage those files with `git add`.
- If files are already staged, skip to Step 3.
- If no files are staged, stage all changed files automatically. If the user specified particular files, stage only those.

Stage specific files by name -- avoid `git add -A` or `git add .` as they can accidentally include sensitive files or unintended changes.

### Step 3: Commit

Draft a commit message and create the commit.

1. Analyze the staged diff to draft a concise commit message:
   - First line: imperative summary under 72 characters
   - Blank line, then body with context if the change is non-trivial
   - Follow repository conventions if visible from recent `git log`
2. Create the commit with the drafted message.
3. Display the resulting commit hash and message.

Use a HEREDOC to pass the commit message to avoid shell escaping issues:
```bash
git commit -m "$(cat <<'EOF'
Commit message here
EOF
)"
```

### Error Recovery

**Pre-commit hook failure**: If a pre-commit hook fails, display the hook's error output. After the user fixes the issue, create a new commit -- never use `--amend`, because the failed commit did not happen and amending would modify the previous (unrelated) commit.

## Before Finishing

After creating the commit, check for leftover changes:

- **Remaining changes?** Run `git status` after the commit. If unstaged changes remain, inform the user -- they may be related changes that should be included, or incidental changes that need a plan for when they will be committed.

## Constraints

- Never use `--no-verify` or skip hooks unless the user explicitly requests it.
- Never use `git add -A` or `git add .` -- always stage specific files.
- Never amend a commit unless the user explicitly requests it.
- Do not add co-author trailers or attribution to commit messages.
