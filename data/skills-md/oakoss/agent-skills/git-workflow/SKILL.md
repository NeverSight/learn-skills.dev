---
name: git-workflow
description: 'Designs git workflows covering branching strategies, trunk-based development, stacked changes, conventional commits, CI/CD pipelines, and repository hygiene. Use when setting up branching models, writing commit messages, configuring GitHub Actions, managing stacked PRs, cleaning stale branches, creating issue templates, or recovering lost commits.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Git Workflow

Covers branching strategies, conventional commits, CI/CD automation, repository hygiene, and git internals. GitHub CLI usage is handled by a separate `github-cli` skill; this skill focuses on git workflow patterns and CI/CD configuration.

## Quick Reference

| Area        | Key Practice                                              |
| ----------- | --------------------------------------------------------- |
| Branching   | Trunk-based development with short-lived feature branches |
| Commits     | Conventional commits with imperative mood                 |
| History     | Linear history via rebase; squash noisy commits           |
| PRs         | Small, stacked changes; no mega PRs                       |
| Main branch | Always deployable; broken main is an emergency            |
| CI/CD       | Modular GitHub Actions with reusable workflows            |
| Merging     | Green CI + review required before merge                   |
| Versioning  | Semantic Release or Changesets (never manual)             |
| Branches    | Max 48 hours lifespan; auto-prune stale/merged            |
| Secrets     | OIDC Connect in pipelines; never hardcode tokens          |
| Signing     | Sign commits with SSH or GPG keys for verified authorship |

## Branch Naming

| Type     | Use For            | Example                |
| -------- | ------------------ | ---------------------- |
| feat     | New features       | `feat/add-user-auth`   |
| fix      | Bug fixes          | `fix/login-redirect`   |
| chore    | Maintenance        | `chore/update-deps`    |
| docs     | Documentation      | `docs/api-reference`   |
| refactor | Code restructuring | `refactor/auth-module` |

## Conventional Commit Types

| Type       | Purpose                               | Version Bump |
| ---------- | ------------------------------------- | ------------ |
| `feat`     | New features                          | Minor        |
| `fix`      | Bug fixes                             | Patch        |
| `docs`     | Documentation only                    | None         |
| `style`    | Formatting, no logic changes          | None         |
| `refactor` | Neither fix nor feature               | None         |
| `perf`     | Performance improvements              | Patch        |
| `test`     | Adding or correcting tests            | None         |
| `build`    | Build system or external dependencies | None         |
| `ci`       | CI configuration changes              | None         |
| `chore`    | Tooling, maintenance, non-src changes | None         |
| `revert`   | Revert a previous commit              | Varies       |

Append `!` after type/scope for breaking changes (major version bump).

## Pre-Merge Checks

All PRs require before merge:

- Lint
- Type check
- Tests
- Security scan
- Review approval (human or automated)

Auto-merge is acceptable for low-risk PRs when pipeline succeeds.

## Troubleshooting

| Issue                                  | Resolution                                                                         |
| -------------------------------------- | ---------------------------------------------------------------------------------- |
| Merge conflicts on long-running branch | Rebase onto main frequently; break remaining work into new branch if over 48 hours |
| Broken main branch                     | Treat as emergency; revert offending commit, then fix forward on a branch          |
| Lost commits or data recovery          | Use git reflog and object inspection (`git cat-file`, `git fsck`)                  |
| CI pipeline failures                   | Check reusable workflow versions; verify OIDC permissions                          |
| Stacked PR conflicts after rebase      | Restack entire chain from base; Graphite handles automatically with `gt restack`   |
| Large file accidentally committed      | Use `git filter-repo` to remove from history (not `git filter-branch`)             |

## Common Mistakes

| Mistake                                               | Correct Pattern                                               |
| ----------------------------------------------------- | ------------------------------------------------------------- |
| Keeping feature branches alive longer than 48 hours   | Merge or rebase daily; break large work into stacked PRs      |
| Committing directly to main without branch protection | Enable branch protection rules requiring CI and review        |
| Using merge commits that clutter history              | Rebase and squash to maintain linear history                  |
| Hardcoding tokens in GitHub Actions workflows         | Use OIDC Connect for authentication in CI/CD pipelines        |
| Creating monolithic CI workflows in a single file     | Split into reusable workflows and composite actions           |
| `Fix bug` as commit message                           | `fix(scope): correct bug description` (conventional)          |
| `feat: Added feature` (past tense)                    | `feat: add feature` (imperative mood, lowercase)              |
| Using `git filter-branch` for history rewriting       | Use `git filter-repo` (faster, safer, officially recommended) |
| Pushing to main directly                              | Create feature branch first                                   |
| Unsigned commits in shared repositories               | Configure commit signing with SSH or GPG keys                 |

## Delegation

- **Audit repository branch hygiene and stale branches**: Use `Explore` agent to list and classify branch age and merge status
- **Set up CI/CD pipelines with reusable workflows**: Use `Task` agent to create modular GitHub Actions configurations
- **Design branching strategy for a new project**: Use `Plan` agent to evaluate trunk-based vs Git Flow based on team needs

## References

- [branching-strategies.md](references/branching-strategies.md) -- Git Flow, GitHub Flow, GitLab Flow, One-Flow comparison and selection criteria
- [trunk-based-development.md](references/trunk-based-development.md) -- Core principles, workflow steps, feature flags, and anti-patterns
- [stacked-changes.md](references/stacked-changes.md) -- Stacked PRs concept, manual stacking, Graphite automation, best practices
- [conventional-commits.md](references/conventional-commits.md) -- Commit format, types, scopes, breaking changes, and full workflow
- [github-actions.md](references/github-actions.md) -- Reusable workflows, matrix testing, deployment environments, security
- [git-internals.md](references/git-internals.md) -- Object model, SHA hashing, index, references, packfiles, garbage collection
- [automation-scripts.md](references/automation-scripts.md) -- Branch pruning, semantic release, security scanning, stacked PR helpers
- [issue-templates.md](references/issue-templates.md) -- Bug report, feature request, task, and minimal issue templates
- [advanced-operations.md](references/advanced-operations.md) -- Commit signing, interactive rebase, worktrees, bisect, reflog recovery, and --force-with-lease
