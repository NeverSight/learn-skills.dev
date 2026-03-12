---
name: git-workflow
description: Git workflow best practices including commit messages, branching strategies, pull requests, and collaboration patterns. Use when working with Git version control.
---

# Git Workflow Best Practices

## Purpose

This skill provides guidance on Git workflow best practices to ensure clean commit history, effective collaboration, and maintainable version control in your projects.

## When to Use This Skill

Auto-activates when:

- Mentions of "git", "commit", "branch", "merge", "pull request"
- Working with version control operations
- Creating or reviewing commits
- Managing branches and releases

## Commit Messages

### Conventional Commits Format

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring (no feature or bug fix)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system or dependency changes
- `ci`: CI/CD configuration changes
- `chore`: Other changes (tooling, maintenance)

**Examples:**

```
feat(auth): add OAuth2 authentication support

Implement OAuth2 authentication flow using the authorization
code grant type. Supports Google and GitHub providers.

Closes #123
```

```
fix(api): handle null response from database query

Previously, null responses would cause the API to crash.
Now returns 404 with appropriate error message.

Fixes #456
```

### Commit Message Best Practices

1. **Use imperative mood** in subject line: "Add feature" not "Added feature"
2. **Keep subject line under 50 characters**
3. **Capitalize subject line**
4. **No period at end of subject line**
5. **Separate subject from body with blank line**
6. **Wrap body at 72 characters**
7. **Explain what and why, not how**
8. **Reference issues/tickets in footer**

## Branching Strategy

### Branch Naming Convention

Use descriptive, hierarchical branch names:

```
<type>/<issue-number>-<short-description>
```

**Examples:**
- `feature/123-oauth-authentication`
- `fix/456-null-pointer-crash`
- `docs/789-api-documentation`
- `refactor/321-simplify-parser`
- `hotfix/999-security-vulnerability`

### Git Flow Strategy

Common branching model:

```
main (production)
  ├── develop (integration)
  │   ├── feature/123-new-feature
  │   ├── feature/456-another-feature
  │   └── fix/789-bug-fix
  ├── release/1.2.0
  └── hotfix/critical-security-fix
```

**Branch purposes:**
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `fix/*`: Bug fixes
- `release/*`: Release preparation
- `hotfix/*`: Critical production fixes

### Branch Management

**Creating a feature branch:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/123-new-feature
```

**Keeping branch up to date:**
```bash
git checkout develop
git pull origin develop
git checkout feature/123-new-feature
git rebase develop
```

**Cleaning up merged branches:**
```bash
git branch -d feature/123-new-feature  # Local
git push origin --delete feature/123-new-feature  # Remote
```

## Pull Requests

### Pull Request Description Template

```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- Add new authentication module
- Update user model with OAuth fields
- Add tests for OAuth flow

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Closes #123
Relates to #456

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

### PR Best Practices

1. **Keep PRs small and focused**: One feature/fix per PR
2. **Write clear descriptions**: Explain what, why, and how
3. **Self-review before requesting review**: Catch obvious issues
4. **Add tests**: Every PR should include relevant tests
5. **Update documentation**: Keep docs in sync with code
6. **Respond to feedback promptly**: Address review comments quickly

## Common Operations

### Amending Last Commit

```bash
# Add changes to previous commit
git add .
git commit --amend --no-edit

# Update commit message
git commit --amend -m "Updated commit message"
```

**Warning:** Only amend commits that haven't been pushed!

### Interactive Rebase

Clean up commit history:
```bash
git rebase -i HEAD~3  # Last 3 commits
```

**Commands:**
- `pick`: Keep commit as-is
- `reword`: Change commit message
- `squash`: Combine with previous commit
- `fixup`: Like squash, but discard message
- `drop`: Remove commit

### Stashing Changes

```bash
# Save changes
git stash push -m "WIP: working on feature"

# List stashes
git stash list

# Apply and remove latest stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

### Cherry-Picking Commits

```bash
git cherry-pick <commit-hash>

# Multiple commits
git cherry-pick <commit-hash1> <commit-hash2>

# Range of commits
git cherry-pick <start-hash>^..<end-hash>
```

### Undoing Changes

**Discard uncommitted changes:**
```bash
git restore <file>          # Unstaged changes
git restore --staged <file> # Staged changes
git reset --hard HEAD       # All changes (DESTRUCTIVE!)
```

**Undo commits:**
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Keep changes in working directory, unstage
git reset HEAD~1

# Discard changes completely (DESTRUCTIVE!)
git reset --hard HEAD~1
```

**Revert commit (safe for shared branches):**
```bash
git revert <commit-hash>  # Creates new commit that undoes changes
```

## Collaboration Patterns

### Keeping Fork Updated

```bash
# Add upstream remote (one time)
git remote add upstream <original-repo-url>

# Fetch and merge upstream changes
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Resolving Merge Conflicts

```bash
# Start merge/rebase
git merge develop  # or git rebase develop

# Edit files to resolve conflicts marked by Git

# Mark as resolved
git add <resolved-file>

# Complete merge
git commit  # for merge
# or
git rebase --continue  # for rebase
```

## Git Configuration

### Essential Git Config

```bash
# User information
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default branch name
git config --global init.defaultBranch main

# Rebase by default on pull
git config --global pull.rebase true

# Better log format
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

### Useful Aliases

```bash
# Common shortcuts
git config --global alias.st status
git config --global alias.ci commit
git config --global alias.co checkout
git config --global alias.br branch

# Undo last commit (keep changes)
git config --global alias.undo "reset --soft HEAD~1"

# Delete merged branches
git config --global alias.cleanup "!git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d"
```

## Security Best Practices

### Avoiding Sensitive Data

1. **Never commit secrets**: API keys, passwords, tokens
2. **Use .gitignore**: Exclude sensitive files
3. **Use environment variables**: Store secrets outside repo
4. **Use git-secrets**: Tool to prevent committing secrets

```bash
# Install git-secrets
brew install git-secrets  # macOS

# Initialize in repo
git secrets --install
git secrets --register-aws

# Scan for secrets
git secrets --scan-history
```

### Signing Commits

```bash
# Generate GPG key
gpg --gen-key

# Configure Git to use GPG
git config --global user.signingkey <key-id>
git config --global commit.gpgsign true

# Sign commit
git commit -S -m "Signed commit message"
```

## .gitignore Best Practices

### Common Patterns

```gitignore
# Operating System
.DS_Store
Thumbs.db

# IDE/Editor
.vscode/
.idea/
*.swp

# Language-specific
__pycache__/
*.pyc
node_modules/
*.class
target/

# Build artifacts
dist/
build/
*.egg-info/

# Environment
.env
.env.local
venv/
env/

# Logs
*.log
logs/

# Temporary files
*.tmp
.cache/
```

### gitignore Tips

- Use `**` for recursive directory matching
- Use `!` to negate patterns (whitelist files)
- Use `#` for comments
- Test patterns: `git check-ignore -v <file>`

## Key Takeaways

1. Write clear, conventional commit messages
2. Use descriptive branch names with type prefixes
3. Keep pull requests small and focused
4. Rebase feature branches to keep history clean
5. Never commit sensitive data
6. Use `.gitignore` effectively
7. Review code thoughtfully and constructively
8. Keep branches up to date with main/develop
9. Sign commits for security
10. Configure Git aliases for efficiency
