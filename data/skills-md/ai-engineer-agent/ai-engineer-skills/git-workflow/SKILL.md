---
name: git-workflow
description: Git workflow expert. Use when managing branches, commits, merges, rebases, and release processes.
disable-model-invocation: true
argument-hint: [action]
---

# Git Workflow

Execute git workflow action: $ARGUMENTS

## Commit Messages
Follow Conventional Commits format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

## Common Workflows

### Feature Branch
1. `git checkout -b feat/<description>` from `main`
2. Make changes with focused commits
3. Rebase on main before PR: `git fetch origin && git rebase origin/main`
4. Push and create PR

### Hotfix
1. `git checkout -b fix/<description>` from `main`
2. Make the fix with test
3. Push and create PR with priority label

### Release
1. Update version in package files
2. Update CHANGELOG.md
3. Create release commit: `git commit -m "chore: release v1.2.3"`
4. Tag: `git tag -a v1.2.3 -m "Release v1.2.3"`
5. Push: `git push origin main --tags`

## Best Practices
- Keep commits atomic — one logical change per commit
- Write commit messages in imperative mood: "Add feature" not "Added feature"
- Never force push to shared branches (main, develop)
- Use `git rebase -i` to clean up local history before PR
- Use `git stash` for temporary context switches
- Review your own diff before committing: `git diff --staged`
- Use `.gitignore` for build artifacts, dependencies, secrets, IDE files
