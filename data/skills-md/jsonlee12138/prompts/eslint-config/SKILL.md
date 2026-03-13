---
name: eslint-config
description: Use when configuring ESLint with @antfu/eslint-config for a single project or a monorepo workspace, including flat config setup, shared config packages, commit quality hooks, or migrations from legacy ESLint configs.
---

# ESLint Config

## Overview
Set up ESLint using `@antfu/eslint-config` for either a single project or a workspace package, and optionally enforce commit quality with `commitlint` + `husky` + `lint-staged`.

## Decision
- **Single project**: Choose when you have one app/package.
- **Workspace package**: Choose when multiple apps need a shared ESLint config in a monorepo.

## Quick Workflow
1. Choose single vs workspace.
2. Install dependencies.
3. Create `eslint.config.js` (flat config).
4. Add `lint` scripts.
5. Run `pnpm lint` to verify.
6. Add commit quality hooks (`.commitlintrc.cjs`, `.husky/*`, `.lintstagedrc`) if the team wants linting and commit message checks before push.

## Common Mistakes
- Mixing Prettier with ESLint formatting rules (prefer ESLint-only).
- Using legacy `.eslintrc` instead of `eslint.config.js`.
- Forgetting to build/publish the shared workspace config.
- Creating `.lintstagedrc` with unsupported syntax for your chosen format.
- Missing `commit-msg` hook, so commit message rules never run.
- Forgetting `package.json` `config.commitizen.path`, so `cz-git` is not picked up.

## Resources
- `references/single-project.md`
- `references/workspace.md`
- `references/vscode-settings.md`
- `references/commit-quality.md`
