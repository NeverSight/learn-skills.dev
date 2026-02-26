---
name: git-conventions
description: Git conventions for teams including conventional commits, branching strategies, PR workflows, merge strategies, and commit message formatting. Use when writing commit messages, creating branches, setting up Git workflows, or when the user asks about Git conventions, commit formats, branching strategies, or PR best practices.
---

# Git Conventions

## Conventional Commits

Format: `<type>(<scope>): <description>`

```
feat(auth): add OAuth2 login with Google
fix(api): handle null response from user endpoint
docs(readme): add deployment instructions
refactor(hooks): extract shared fetch logic into useApi
test(auth): add integration tests for login flow
chore(deps): update react to v19.1
```

### Types

| Type       | When to Use                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New feature or capability                               |
| `fix`      | Bug fix                                                 |
| `docs`     | Documentation only                                      |
| `style`    | Formatting, whitespace (no logic change)                |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                                 |
| `test`     | Adding or updating tests                                |
| `build`    | Build system or external dependencies                   |
| `ci`       | CI/CD configuration                                     |
| `chore`    | Maintenance tasks, tooling                              |
| `revert`   | Reverts a previous commit                               |

### Rules

- **Type** is required and lowercase.
- **Scope** is optional, lowercase, describes the area of change (`auth`, `api`, `ui`, `deps`).
- **Description** is required, imperative mood ("add", not "added" or "adds"), lowercase, no period at the end.
- **Body** (optional) explains _why_, not _what_. Wrap at 72 characters.
- **Breaking changes**: add `!` after the type/scope or include `BREAKING CHANGE:` in the footer.

```
feat(api)!: change authentication to use JWT tokens

BREAKING CHANGE: The session-based auth endpoints have been removed.
Clients must now use Bearer tokens in the Authorization header.
```

### Multi-Line Commits

```
fix(payments): prevent duplicate charge on retry

The retry logic was not checking if the original charge succeeded
before attempting a new one. Added idempotency key validation
to the charge endpoint.

Closes #1234
```

## Branching Strategy

### Branch Naming

```
feature/add-user-dashboard
fix/null-pointer-in-checkout
chore/upgrade-dependencies
docs/api-authentication-guide
refactor/extract-payment-service
```

Pattern: `<type>/<short-description>` using kebab-case.

### Trunk-Based Development (Recommended)

```
main ─────●────●────●────●────●─────
           \       /      \       /
            ●────●          ●────●
          feature/x       fix/y
```

- `main` is always deployable.
- Short-lived feature branches (1-3 days).
- Merge via squash or rebase to keep history linear.
- Use feature flags for long-running work instead of long-lived branches.

### Git Flow (When Required)

```
main    ─────●──────────────●───────
              \            /
develop ───●───●───●───●───●────●───
            \     /     \     /
             ●───●       ●───●
           feature/x   feature/y
```

- `main` — production releases.
- `develop` — integration branch.
- `feature/*` — branch from develop, merge back to develop.
- `release/*` — stabilization before production.
- `hotfix/*` — urgent fixes from main.

Use trunk-based development unless the project specifically requires Git Flow.

## Commit Best Practices

- **Atomic commits**: Each commit is one logical change that compiles and passes tests.
- **Commit often**: Small, frequent commits are easier to review, bisect, and revert.
- **Don't commit generated files**: Add build outputs, lock files changes (when unintended), and artifacts to `.gitignore`.
- **Don't commit secrets**: Never commit `.env`, API keys, credentials, or tokens.
- **Sign commits**: Use `git commit -S` for verified authorship.

## Pull Request Conventions

### PR Title

Follow the same conventional commit format:

```
feat(dashboard): add real-time notifications widget
fix(auth): resolve token refresh race condition
```

### PR Description Template

```markdown
## Summary

Brief description of what this PR does and why.

## Changes

- Added notification WebSocket connection
- Created NotificationBell component
- Updated header layout to include notifications

## Testing

- [ ] Unit tests pass
- [ ] Manual testing in staging
- [ ] Tested on mobile viewport

## Screenshots

(if applicable)
```

### PR Best Practices

- Keep PRs small (< 400 lines of diff when possible).
- One concern per PR — don't mix refactoring with feature work.
- Self-review before requesting reviews.
- Respond to all review comments, even if just "Done" or "Won't fix because...".
- Squash merge to keep main history clean.

## Merge Strategies

| Strategy     | When to Use                                          | Result                              |
| ------------ | ---------------------------------------------------- | ----------------------------------- |
| Squash merge | Feature branches to main                             | One clean commit per feature        |
| Rebase merge | When you want linear history with individual commits | Flat history, each commit preserved |
| Merge commit | When branch history matters (release branches)       | Explicit merge point                |

**Default recommendation**: Squash merge for feature branches into main. This gives a clean, bisectable history where each commit represents one complete feature or fix.

## .gitignore Essentials

```gitignore
# Dependencies
node_modules/

# Build output
dist/
build/
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db

# Debug
*.log
npm-debug.log*

# Test coverage
coverage/
```

## Useful Aliases

```shell
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm "commit -m"
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate -20"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.unstage "reset HEAD --"
```
