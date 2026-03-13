---
name: pr-worktree-workflow
description: Complete workflow for creating git worktrees and Pull Requests, including worktree setup, branch management, and PR creation.
---

# PR + Worktree Workflow

## Common Mistakes (Read First)

**DO NOT use this skill when:**
- User only mentions worktree (use `using-git-worktrees` instead)

**When to prompt user:**
- If user says "create a PR" or "I want to make a PR" → Ask: "Would you like me to use the pr-worktree-workflow to create a worktree and PR together?"

## Overview

This skill integrates `using-git-worktrees` and `my-pull-requests` to provide a complete task-to-PR workflow:

1. **Create Worktree** - Use `using-git-worktrees` to establish isolated workspace
2. **Implement Feature** - Work in the new branch
3. **Create PR** - Create Pull Request from the completed work
4. **Verify PR** - Confirm PR status

**Core Principle:** Worktree isolation + PR process = reliable feature development

**Opening Announcement:** "I'm using the pr-worktree-workflow skill to complete the full workflow from worktree creation to PR."

## Interaction Pattern (Follow This)

Based on how the skill is invoked, respond differently:

### Case 1: Skill loaded manually + NO task provided
→ Ask: "What task would you like me to work on?"

### Case 2: Skill loaded manually + task IS provided
→ Execute workflow directly (skip confirmation)

### Case 3: User mentions "PR" or "Pull Request" in conversation (without loading skill)
→ Ask: "Would you like me to use the pr-worktree-workflow to create a worktree and PR together?"

## Workflow Steps

### Phase 1: Create Worktree

**Invoke `using-git-worktrees` skill:**

```
I'm using the using-git-worktrees skill to set up an isolated workspace.
```

Follow `using-git-worktrees` skill:
1. Check existing directory (.worktrees or worktrees)
2. Verify directory is ignored by .gitignore
3. Create worktree with new branch
4. Run project setup (npm install / poetry install etc.)
5. Verify test baseline

### Phase 2: Create PR-Opening Commit

**Make the first commit specifically for creating the PR:**

```bash
# In worktree directory
cd .worktrees/<branch-name>

# First commit - creates the PR foundation
git add -A
git commit -m "chore: create PR for <feature-name>

## TODO
- [ ] Implement feature
- [ ] Add tests
- [ ] Update documentation"
```

### Phase 3: Create WIP PR (Draft)

**Immediately after first commit, create a draft PR:**

```bash
# Create draft PR (WIP) - title format: scope: summary
gh pr create --title "feat: <feature-name>" \
  --body "## Motivation
- Why this change is needed

## Approach
- How the feature is implemented

## Considered Alternatives
- Alternative approaches considered

## Risk & Rollout
- Potential risks and rollout strategy

## Testing Evidence
- Test results or evidence

## Status: Work in Progress
- [ ] Task 1
- [ ] Task 2

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Breaking change" \
  --base main \
  --draft
```

**Why create WIP PR immediately:**
- PR link is available for tracking from the start
- Changes are already backed up remotely
- Can reference PR in commit messages

### Phase 4: Implement Feature (Iterative)

Continue development with multiple commits:

```bash
# In worktree directory
cd .worktrees/<branch-name>

# Regular development flow
# 1. Write code
# 2. Run tests
# 3. Commit changes
git add -A
git commit -m "feat: implement <feature-part-1>"

# Push to update PR
git push

# Continue with more commits as needed...
git add -A
git commit -m "feat: implement <feature-part-2>"

git push
```

### Phase 5: Mark Ready for Review

**When feature is complete, update PR:**

```bash
# Finalize title and mark ready - title format: scope: summary
gh pr edit <PR-NUMBER> --title "feat: <feature-name>"

# If using draft:
gh pr ready <PR-NUMBER>

# Or open in browser to mark ready
gh pr view <PR-NUMBER> --web
```

Update PR body to reflect completion:

```markdown
## Status: Ready for Review ✅

- [x] Task 1
- [x] Task 2

## Testing Evidence
- Test results or evidence

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Breaking change
```

### Phase 6: Verify PR

After creating PR, invoke `my-pull-requests` skill to confirm status:

```
I'm using the my-pull-requests skill to verify the PR status.
```

## Quick Reference

| Phase | Action | Skill Reference |
|-------|--------|-----------------|
| 1. Worktree | Create isolated workspace | `using-git-worktrees` |
| 2. PR Commit | First commit for PR | `git commit` |
| 3. WIP PR | Create draft PR immediately | `gh pr create --draft` |
| 4. Development | Implement with multiple commits | (built-in) |
| 5. Ready | Mark PR ready for review | `gh pr ready` |
| 6. Verification | Confirm PR status | `my-pull-requests` |

## Common Scenarios

### Scenario 1: New Feature Development

```
User: I need to develop a new login feature

AI: I'm using the pr-worktree-workflow skill to complete the full workflow from worktree creation to PR.

[Phase 1: Invoke using-git-worktrees]
- Check .worktrees/ directory
- Verify ignored
- Create worktree: .worktrees/login-feature -b feature/login
- Run npm install
- Verify tests pass

[Phase 2: Development]
- Implement login feature
- git add -A && git commit -m "feat: add login feature"
- git push -u origin feature/login

[Phase 3: Create PR]
gh pr create --title "feat: add login feature" --body "..."

[Phase 4: Verification]
Invoke my-pull-requests to confirm PR status

PR created: https://github.com/owner/repo/pull/123
Worktree location: /project/.worktrees/login-feature
```

### Scenario 2: Bug Fix

```bash
# Similar flow, use fix/ prefix
git worktree add .worktrees/bug-fix -b fix/<issue-name>
# ... after fixing
gh pr create --title "fix: <description>" --base main
```

### Scenario 3: Large Refactoring

```bash
# Use refactor/ prefix
git worktree add .worktrees/refactor-api -b refactor/api-cleanup
# ... after refactoring
gh pr create --title "refactor: clean up API" --base main
```

## Branch Naming Conventions

| Type | Prefix | Example |
|------|--------|---------|
| New Feature | feature/ | feature/user-auth |
| Bug Fix | fix/ | fix/login-validation |
| Refactoring | refactor/ | refactor/api-cleanup |
| Experiment | experiment/ | experiment/new-algorithm |
| Documentation | docs/ | docs/readme-update |

## Notes

### Worktree Cleanup

After completing PR, optionally cleanup worktree:

```bash
# Delete remote branch
git push origin --delete <branch-name>

# Delete local worktree
git worktree remove .worktrees/<branch-name>

# Clean up orphaned branches
git branch -d <branch-name>
```

### Stay Synced

Before starting work, ensure main branch is up-to-date:

```bash
git fetch origin
git checkout main
git pull origin main
git checkout <feature-branch>
```

### PR Description Template

```markdown
## Description
<!-- Describe what you did and why -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
<!-- Describe how to test your changes -->

## Checklist
- [ ] Tests pass locally
- [ ] Code follows project style
- [ ] Documentation updated (if needed)
```

## Integration

**Called by:**
- `brainstorming` - when design is approved
- `executing-plans` - when there's an implementation plan
- `subagent-driven-development` - when subagent needs to execute tasks

**Works with:**
- `using-git-worktrees` - Worktree creation
- `my-pull-requests` - PR status verification
- `finishing-a-development-branch` - Branch completion cleanup

## Error Handling

### Worktree Creation Failed

```
Error: fatal: '<path>' already exists
```

Solution: Check if directory already exists or use different branch name

### Push Failed

```
Error: fatal: The current branch <branch> has no upstream branch.
```

Solution: Use `git push -u origin <branch>` to set upstream

### PR Creation Failed

```
Error: GraphQL: Repository not found
```

Solution: Ensure you're in correct repo directory or authenticated via `gh auth login`
