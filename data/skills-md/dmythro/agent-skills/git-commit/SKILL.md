---
name: git-commit
description: Conventional Commits format for all git commits and PR/MR titles. Defines
  type prefixes, scope rules, breaking change syntax, and commit message structure
---

# Conventional Commits

**Default commit format: [Conventional Commits](https://www.conventionalcommits.org/).** Use this format for all commits and PR/MR titles unless the project defines its own commit conventions (in CLAUDE.md, AGENTS.md, contributing guides, or similar). Project-specific rules always take priority.

## When to Use

- **Making any git commit** -- this skill defines the required format
- **Creating PR/MR titles** -- squash merges use the title as the commit message
- **Writing squash merge messages** -- must follow the same format
- **Reviewing commit message format** -- validate against these rules

## Critical Rules

1. **Project rules override this skill** -- if the project defines commit message conventions (issue number prefixes, custom formats, etc.), follow those instead. This skill is the default when no project-specific rules exist.
2. **Type is required** -- never commit without a type prefix
3. **Description is lowercase**, imperative mood, no period: `fix: handle null response` not `Fix: Handled null response.`
4. **No `Co-Authored-By` trailer** -- never add it to commit messages

---

## Provider Detection

Detect the git provider to use the correct CLI:

```bash
git remote get-url origin
```

| Remote URL contains                | Provider | CLI    | PR term |
|------------------------------------|----------|--------|---------|
| `github.com`                       | GitHub   | `gh`   | PR      |
| `gitlab.com` or self-hosted GitLab | GitLab   | `glab` | MR      |

If ambiguous or both present, ask the user.

---

## Format

```text
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

## Types

| Type       | When                                                    |
|------------|---------------------------------------------------------|
| `feat`     | New feature or capability                               |
| `fix`      | Bug fix                                                 |
| `docs`     | Documentation only                                      |
| `style`    | Formatting, whitespace, semicolons (no logic change)    |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                                 |
| `test`     | Adding or updating tests                                |
| `build`    | Build system or external dependencies                   |
| `ci`       | CI/CD configuration                                     |
| `chore`    | Maintenance tasks, tooling, config                      |

## Rules

1. **Type is required** -- never commit without a type prefix
2. **Scope is optional** but encouraged for multi-module repos: `feat(auth): add OAuth2 flow`
3. **Description is lowercase**, imperative mood, no period: `fix: handle null response` not `Fix: Handled null response.`
4. **Breaking changes** use `!` after type/scope: `feat(api)!: remove v1 endpoints`
5. **PR/MR titles follow the same format** -- squash merges use the PR/MR title as the commit message
6. **No `Co-Authored-By` trailer** -- never add it to commit messages

## Commit Examples

```bash
git commit -m "feat: add user profile page"
git commit -m "fix(auth): prevent token refresh race condition"
git commit -m "docs: update API reference for v2 endpoints"
git commit -m "refactor(db): extract connection pooling logic"
git commit -m "feat(api)!: change response format for /users"
```

## PR/MR Title Examples

| Provider | Create PR/MR with title                                              |
|----------|----------------------------------------------------------------------|
| GitHub   | `gh pr create --title "feat: add dark mode" --body "..."`            |
| GitLab   | `glab mr create --title "feat: add dark mode" --description "..."` |
