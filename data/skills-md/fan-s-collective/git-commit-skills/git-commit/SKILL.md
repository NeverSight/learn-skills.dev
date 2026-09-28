---
name: git-commit
description: Generate Conventional Commits-style git commit messages from repository changes. Use when Codex needs to write, rewrite, review, or validate a commit message from staged or unstaged diffs, while deriving the correct type, scope, subject, and optional body from the current repository rather than assuming fixed scopes.
---

# Git Commit

## Overview

Write commit messages from actual repository changes. Prefer concise, intention-focused messages over file-by-file diff summaries. Treat `references/commit-convention.md` as the baseline style guide, then adapt scope and wording to the current repository.

## Workflow

1. Inspect the change set first.
   - Prefer `git diff --staged` when changes are staged.
   - Use `git diff` when no staged diff exists or when the user asks about unstaged changes.
   - Use `git status --short` to understand file scope.
   - If the repository contains a commit convention file, read it before writing the message. Check likely names such as `COMMIT_CONVENTION.md`, `CONTRIBUTING.md`, `.github/COMMIT_CONVENTION.md`, or `.github/CONTRIBUTING.md`.
   - Inspect recent commit subjects with `git log --format=%s -n 20` to infer the repository's preferred output language. Follow the dominant language used in history. If recent commit subjects are mixed with no clear dominant language, or if there is no commit history or another error prevents inspection, default to English.

2. Choose one commit intent.
   - If changes contain unrelated intents, recommend splitting commits.
   - If the user still wants one message, choose the dominant intent and explain the tradeoff briefly.

3. Choose the header:

```text
<type>(<scope>): <subject>
```

4. Add a body only when it clarifies intent, impact, compatibility, migration, or mixed change types.

## Type Selection

- `feat`: new feature
- `fix`: bug or defect fix
- `perf`: performance improvement
- `refactor`: implementation restructuring without external behavior changes
- `style`: formatting or code style only
- `test`: test additions or adjustments
- `docs`: documentation or comments
- `chore`: dependencies, build, scaffolding, and miscellaneous maintenance
- `ci`: CI changes
- `types`: type definition changes
- `revert`: revert an existing commit
- `wip`: temporary work-in-progress commit

For mixed changes, either split commits or use the dominant type in the header and type-prefixed bullets in the body.

## Scope Selection

Derive `scope` from the current repository. Do not reuse scopes from the reference file unless they match actual changed paths or local conventions.

Use this priority:

1. Use scopes explicitly defined by the repository's own commit convention.
2. Use a stable workspace/package/app/module name from changed paths, such as `api`, `web`, `cli`, `core`, `ui`, `docs`, or the package name.
3. Use a more precise long-lived submodule name only when the change is clearly concentrated there and the name is reusable.
4. Use `repo` for repository-level changes, cross-cutting changes, or changes that cannot be reduced to one module.

If no meaningful scope is required by the repository's convention, omit it only when the local style allows scope-less headers.

## Subject And Body

Write the subject as the core intent of the change. Keep it short, concrete, and action-oriented. Avoid vague subjects such as `update`, `fix bug`, or `optimize code`.

Match the output language to the repository's recent commit history. Use the dominant language when it is clear. If the recent history is inconsistent or mixed, or if there is no commit history or another inspection failure, write the commit message in English by default.

Write the body when useful:

- Describe intent, impact, and necessary background.
- Avoid restating each changed file.
- If all bullets are the same change type, do not repeat the type in every bullet.
- If the commit mixes change types, prefix body bullets with `type:`.

Examples:

```text
feat(auth): add session refresh flow

- 增加会话刷新入口，减少登录态过期后的重复认证
- 补齐旧 token 兼容逻辑，避免升级后状态丢失
```

```text
refactor: align release workflow

- refactor: 收敛构建与发布脚本的职责边界
- fix: 修正缺少版本号时的默认值异常
- docs: 补充新的发布流程说明
```

## Reference

Read `references/commit-convention.md` for the baseline Conventional Commits rules and examples. Override its scope examples with the current repository's structure.
