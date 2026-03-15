---
name: git-conventional-commit
description: Create git commits following the Conventional Commits v1.0.0 specification (conventionalcommits.org). Use when the user asks to commit changes, says "/conventional-commit", or wants a well-structured commit message. Triggers on requests like "commit this", "commit my changes", "create a commit", or any git commit workflow. Analyzes staged/unstaged changes and produces compliant commit messages with proper type, scope, description, body, and footers.
compatibility: Requires git
metadata:
  author: jackchuka
  scope: generic
  confirms:
    - create git commit
---

# Conventional Commit

Create git commits that follow the Conventional Commits v1.0.0 specification.

## Workflow

### 1. Gather context

Run these in parallel:

```
git status
git diff --cached
git diff
git log --oneline -10
```

### 2. Analyze changes

- Identify **what** changed (files, functions, features, fixes)
- Identify **why** it changed (bug fix, new feature, refactor, etc.)
- Group related changes — if changes are unrelated, suggest splitting into multiple commits
- Check for sensitive files (.env, credentials, secrets) and warn before staging

### 3. Stage changes

- Stage only related changes with `git add <specific-files>`
- Never use `git add -A` or `git add .` without confirming with the user
- If unstaged changes exist that belong to a different logical change, leave them unstaged

### 4. Write the commit message

Format per Conventional Commits v1.0.0:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Type (required)

Pick the most specific type:

| Type       | When to use                                                        |
| ---------- | ------------------------------------------------------------------ |
| `feat`     | New feature or capability (correlates with SemVer MINOR)           |
| `fix`      | Bug fix (correlates with SemVer PATCH)                             |
| `docs`     | Documentation only                                                 |
| `style`    | Formatting, whitespace, semicolons — no logic change               |
| `refactor` | Code change that neither fixes a bug nor adds a feature            |
| `perf`     | Performance improvement                                            |
| `test`     | Adding or correcting tests                                         |
| `build`    | Build system or external dependencies (e.g., go.mod, package.json) |
| `ci`       | CI configuration and scripts                                       |
| `chore`    | Maintenance tasks that don't modify src or test files              |
| `revert`   | Reverts a previous commit                                          |

#### Scope (optional)

A noun in parentheses describing the section of the codebase:

```
feat(auth): add OAuth2 login flow
fix(parser): handle empty input gracefully
docs(readme): update installation steps
```

Derive scope from: package name, module, directory, or feature area.

#### Description (required)

- Imperative mood: "add" not "added" or "adds"
- Lowercase first letter
- No period at end
- Max ~50 characters for the entire first line (type + scope + description)

#### Body (optional)

- Separate from description with a blank line
- Explain **what** and **why**, not how
- Wrap at 72 characters
- Use when the description alone is insufficient

#### Footer (optional)

- Separate from body with a blank line
- Format: `token: value` or `token #value`
- Use `-` instead of spaces in tokens (except `BREAKING CHANGE`)

Common footers:

- `BREAKING CHANGE: <description>` — breaking API change (SemVer MAJOR)
- `Refs: #123` — reference issues
- `Reviewed-by: Name <email>`
- `Co-authored-by: Name <email>`

#### Breaking changes

Indicate with either:

1. An exclamation mark after type/scope, e.g. `feat(api)!: change response format`
2. A `BREAKING CHANGE:` footer with explanation
3. Both for maximum clarity

### 5. Create the commit

Use a HEREDOC for multi-line messages:

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add OAuth2 login flow

Implement OAuth2 authorization code flow with PKCE for
secure browser-based authentication. Replaces the legacy
session-based auth which had CSRF vulnerabilities.

BREAKING CHANGE: /api/login now returns a JWT instead of
setting a session cookie
Refs: #342
EOF
)"
```

For single-line commits:

```bash
git commit -m "fix(parser): handle empty input without panic"
```

### 6. Do NOT push

Never push to remote unless the user explicitly asks.

## Examples

Simple fix:

```
fix: resolve null pointer in user lookup
```

Scoped feature:

```
feat(api): add pagination to list endpoints
```

Multi-line with breaking change:

```
feat(config)!: switch to YAML configuration format

Migrate from JSON to YAML for all configuration files.
Existing JSON configs are no longer supported.

BREAKING CHANGE: configuration files must be in YAML format
Refs: #891
```

Documentation:

```
docs: correct typos in contributing guide
```

Multiple footers:

```
fix(db): prevent connection pool exhaustion

Add connection timeout and max idle settings to prevent
pool exhaustion under high load.

Refs: #456
Reviewed-by: Alice <alice@example.com>
```
