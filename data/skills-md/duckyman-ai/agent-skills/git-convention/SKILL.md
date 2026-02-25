---
name: git-convention
description: Generate conventional git commit messages following Angular convention format. Use this skill when creating commits, writing commit messages, or reviewing git history. Triggers include "git commit", "commit message", "changelog", or requests to version control changes.
---

# Git Convention Skill

Generate conventional git commit messages following Angular commit convention format.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Type

Must be one of:

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `build` | Changes that affect the build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverts a previous commit |

## Scope

The scope should be the name of the npm package affected (as indicated by package.json).

Example scopes:
- `core`
- `auth`
- `user`
- `api`
- `ui`

## Subject

The subject contains a succinct description of the change:

- Use imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No period (.) at the end

## Body

The body should include the motivation for the change and contrast this with previous behavior:

- Use imperative, present tense: "change" not "changed" nor "changes"
- Include the motivation for the change and contrast this with previous behavior

## Footer

The footer should contain any information about Breaking Changes and is also the place to reference GitHub issues that this commit Closes.

Breaking Changes should start with the word `BREAKING CHANGE:` with a space or two newlines.

## Examples

### Feature with scope
```
feat(auth): add login with Google

Implement OAuth2 authentication flow using Google Sign-In
- Add GoogleSignInButton component
- Update auth service to handle OAuth tokens
- Add error handling for failed authentication

Closes #123
```

### Bug fix
```
fix(api): handle null response from user endpoint

Previously, null responses would crash the app.
Now returns empty user object instead.
```

### Breaking change
```
feat(core): change user model structure

BREAKING CHANGE: User.id is now String instead of int.

All database queries and API calls need to be updated
to handle string IDs.
```

### Documentation
```
docs(readme): update installation instructions

Added step for installing required system dependencies.
```

### Refactoring
```
refactor(user): extract validation logic to separate class

Move all user validation logic from UserService to
new UserValidator class for better testability.
```

### Multiple paragraphs in body
```
feat(api): add pagination support

Implement cursor-based pagination for list endpoints.

- Add PaginationFilter class
- Update repository methods to accept pagination params
- Add tests for pagination edge cases

This improves performance for large datasets and
reduces memory usage.
```

### Revert
```
revert: feat(auth): add login with Facebook

This reverts commit 1a2b3c4d
```

## Best Practices

**DO**:
- Use the present tense ("add" not "added")
- Use the imperative mood ("move" not "moves")
- Limit the first line to 72 characters or less
- Reference issues in the footer
- Explain what and why, not how
- Keep subject line short and descriptive
- Use body to explain what and why vs. how

**DON'T**:
- Use past tense
- Use period at the end of subject
- Capitalize first letter of subject
- Mix multiple types in one commit
- Write vague subjects like "update stuff"
- Include how you fixed it in the message
- Exceed 72 characters on first line

## Changelog Generation

Conventional commits enable automatic changelog generation:

```bash
# Using conventional-changelog
npm install -g conventional-changelog
conventional-changelog -p angular -i CHANGELOG.md -s
```

## Commit Linting

Enforce commit message conventions with commitlint:

```json
// commitlint.config.js
{
  "extends": ["@commitlint/config-angular"],
  "rules": {
    "type-enum": [2, "always", ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]],
    "type-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-case": [0]
  }
}
```

## Quick Reference

```
feat: add new feature
fix: fix bug
docs: update documentation
style: format code (no logic change)
refactor: refactor code
perf: improve performance
test: add/update tests
build: change build system
ci: change CI config
chore: other changes
revert: revert previous commit
```