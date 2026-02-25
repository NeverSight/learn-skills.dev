---
name: vcs-commit
description: 'Standardized git commits following Conventional Commits. Supports mapping to GitHub and GitLab.'
---

# VCS Commit

## Conventional Commit Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Refactor
- `test`: Tests
- `perf`: Performance
- `chore`: Maintenance

### Breaking Changes
```
# Exclamation mark after type/scope
feat!: remove deprecated endpoint

# BREAKING CHANGE footer
feat: allow config to extend other configs

BREAKING CHANGE: `extends` key behavior changed
```

## Workflow
1. **Stage**: `git add <files>` (Group changes logically).
2. **Analyze**: Use `git diff --staged` to understand changes.
3. **Drafting**:
   - Write in **English only**.
   - Follow Conventional Commits.
   - Use imperative mood ("add" not "added").
4. **MITM Confirmation**: ALWAYS present the drafted commit message to the USER for approval before executing `git commit`.
5. **Commit**: `git commit -m "<type>(scope): <description>"`

## Best Practices
- One logical change per commit
- Present tense: "add" not "added"
- Imperative mood: "fix bug" not "fixes bug"
- Reference issues: `Closes #123`, `Refs #456`
- Keep description under 72 characters

## Git Safety Protocol
- **No Secrets**: Never commit API keys or credentials.
- NEVER run destructive commands (--force, hard reset) without explicit request
- NEVER skip hooks (--no-verify) unless user asks
- NEVER force push to main/master
- If commit fails due to hooks, fix and create NEW commit (don't amend)