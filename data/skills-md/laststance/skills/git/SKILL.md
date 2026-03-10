---
name: git
description: |
  Git operations with intelligent commit messages and workflow optimization.
  Analyzes changes to generate Conventional Commit messages automatically.
  Covers status, commit, push, pull, branch, and merge operations.

  Use when:
  - User asks to commit, push, or check git status
  - User wants to create or switch branches
  - User needs help with merge or conflict resolution
  - User says "commit this", "push", "what changed", "create a branch"
  - Any git workflow operation

  Keywords: git, commit, push, pull, status, branch, merge, rebase, stash, log, diff
argument-hint: "[operation] [args]"
---

# Git — Intelligent Git Operations

Smart git workflow with automatic Conventional Commit message generation.

<essential_principles>

## Safety Rules

- **Conventional Commits**: All commit messages MUST follow `type(scope): description` format
  - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `build`, `style`
  - Scope: optional, derived from changed files/directories
  - Description: imperative mood, lowercase, no period
- **Destructive operations require user confirmation**: `push --force`, `reset --hard`, `branch -D`, `rebase` on shared branches, `clean -f`
- **Never skip hooks**: Do not use `--no-verify` unless user explicitly requests it
- **Smart Commit always active**: Analyze staged changes to generate meaningful messages automatically

</essential_principles>

## Operations

### status

Analyze repository state and provide actionable summary.

1. Run `git status` (never use `-uall` flag)
2. Run `git diff --stat` for change overview
3. Present:
   - Staged / unstaged / untracked file counts
   - Branch info and upstream tracking status
   - Recommended next action (e.g., "Ready to commit", "Changes need staging")

### commit

Generate a Conventional Commit from change analysis.

1. Run `git status` and `git diff --cached` (staged) and `git diff` (unstaged)
2. Run `git log --oneline -5` to match existing commit style
3. Analyze changes:
   - Determine `type` from nature of changes (new feature → `feat`, bug fix → `fix`, etc.)
   - Determine `scope` from affected directories/files
   - Write concise description focusing on "why" not "what"
4. If nothing is staged, ask user what to stage
5. Stage files with specific file names (avoid `git add -A` or `git add .`)
6. Commit using HEREDOC format:
   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): description
   EOF
   )"
   ```

### push

Sync local commits with remote.

1. Check upstream tracking: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`
2. If no upstream, push with `-u`: `git push -u origin <branch>`
3. If upstream exists: `git push`
4. **Never force-push without user confirmation**

### pull

Fetch and integrate remote changes.

1. `git pull --rebase` (prefer rebase over merge for clean history)
2. If conflicts arise, guide user through resolution

### branch

Create, switch, or manage branches.

1. **Create**: `git checkout -b <name>` with naming convention `type/description` (e.g., `feat/add-login`, `fix/header-alignment`)
2. **Switch**: `git checkout <name>`
3. **List**: `git branch -a` with upstream status
4. **Delete**: `git branch -d <name>` (use `-D` only with user confirmation)

### merge

Guided merge with conflict resolution support.

1. Check target branch is up to date: `git fetch origin`
2. Execute merge: `git merge <source>`
3. If conflicts:
   - List conflicting files
   - Show conflict markers for each file
   - Guide user through resolution options
   - After resolution: `git add <resolved-files> && git commit`

### stash

Temporarily save uncommitted changes.

1. **Save**: `git stash push -m "description"`
2. **List**: `git stash list`
3. **Apply**: `git stash pop` (or `apply` to keep in stash)

### log

View commit history with useful formatting.

1. Default: `git log --oneline -20`
2. Detailed: `git log --oneline --graph --all -20`

## Examples

```
/git status
/git commit
/git push
/git branch feat/dark-mode
/git merge main
/git stash save work in progress
/git log
```

## Boundaries

**Will:**
- Execute git operations with intelligent automation
- Generate Conventional Commit messages from change analysis
- Provide workflow guidance and best practice recommendations
- Handle conflict resolution with step-by-step guidance

**Will Not:**
- Modify repository configuration without explicit authorization
- Execute destructive operations without user confirmation
- Include project-specific workflow rules (those belong in CLAUDE.md or AGENTS.md)
