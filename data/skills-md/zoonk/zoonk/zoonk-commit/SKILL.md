---
name: zoonk-commit
description: Guidelines for writing commit messages and PR descriptions. Use when creating commits, writing PR descriptions, or asking about commit format.
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Commit Messages

## Format

```
type(scope): short message
```

## Types

- `feat` - new feature
- `fix` - bug fix
- `refactor` - code refactoring
- `chore` - maintenance tasks (deps, config, tooling)

## Scopes

Use the owning app or package name as scope when working in this monorepo.

### Scope Selection Order

1. If the change is fully owned by one app in `apps/<name>`, use that app name.
2. If the change is fully owned by one package in `packages/<name>`, use that package name.
3. Only use an inferred scope like `deps`, `data`, `ci`, or `agents` when the change truly spans multiple workspaces or does not belong to a single app/package.
4. Do not pick a scope based on the kind of code changed (`data`, `ui`, styling, tests, etc.) when the files clearly belong to one app/package. The workspace owner wins.

**Inferred scopes** (when change doesn't fit an app/package):

- `agents` - CLAUDE.md, AGENTS.md, `.claude/` folder
- `ci` - GitHub workflows, CI/CD configuration
- `deps` - dependency updates across multiple packages
- `data` - data layer changes spanning multiple packages

### Good Scope Choices

- `fix(player): improve belt progress contrast` for changes in `packages/player/...`
- `fix(main): correct level page copy` for changes in `apps/main/...`
- `fix(api): handle null response in auth` for changes in `apps/api/...`
- `fix(data): normalize progress query` only when the data-layer change spans multiple apps/packages

### Avoid These Mistakes

- `fix(ui): improve belt progress contrast` when the change is in `packages/player`
- `fix(data): update main progress query` when the change is only in `apps/main`
- `fix(ui): restyle main level card` when the change is only in `apps/main`

## Examples

```
feat(main): add user profile page
fix(player): improve belt progress contrast
fix(api): handle null response in auth
refactor(db): use enum for status field
chore(deps): update react to v19
chore(agents): add commit skill
fix(ci): update node version in workflow
```

## Rules

- Use lowercase for entire message
- No period at the end
- Keep message under 72 characters
- Use imperative mood ("add" not "added")

# PR Descriptions

Use the same `type(scope): short message` format as the commit title.

Keep descriptions brief. Focus on what changed. No need to list verification commands run.
