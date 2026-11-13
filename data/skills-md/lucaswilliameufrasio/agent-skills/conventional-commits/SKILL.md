---
name: conventional-commits
description: >-
  Draft or review commit messages using the Conventional Commits format. Use
  whenever asked to prepare, amend, or create a commit, or to check whether a
  change communicates its type, scope, and breaking impact clearly. Inspect the
  actual staged diff and repository conventions first.
---

# Conventional Commits

Use the Conventional Commits structure:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footers]
```

## Workflow

1. Do not commit unless the user asked for a commit or previously authorized
   autonomous commits. Do not push, amend, or rewrite history without
   authorization.
2. Inspect the staged diff and recent commit history. Stage only intended files;
   never use a broad staging command when unrelated changes may be present.
3. Select the type and optional scope from the actual change and repository
   conventions. Prefer one logical change per commit.
4. Draft a concise, imperative description after the colon. Keep the subject
   lowercase unless a proper noun or repository convention requires otherwise;
   omit the trailing period.
5. Describe why the change was made in the body when the subject is not enough.
   Add issue references and breaking-change footers where relevant.
6. Show the proposed message and run the repository's required pre-commit
   checks before creating the commit. Do not assume a particular language's
   checklist or skip a project-specific gate.

## Common types

| Type | Use |
| --- | --- |
| `feat` | Add user-facing or public capability |
| `fix` | Correct a defect |
| `refactor` | Restructure without changing intended behavior |
| `perf` | Improve performance |
| `test` | Add or change tests only |
| `docs` | Documentation-only change |
| `build` | Build system or dependency changes |
| `ci` | CI configuration or automation |
| `chore` | Other maintenance |
| `revert` | Revert an earlier change |

Use other valid types when a repository explicitly standardizes them. A scope is
optional and should name the affected subsystem, not repeat the whole summary.

## Breaking changes and SemVer signal

Mark an incompatible change with `!` after the type/scope and include a
`BREAKING CHANGE:` footer describing the impact and migration path. Example:

```text
feat(api)!: remove the legacy response field

BREAKING CHANGE: clients must read `displayName` instead of `name`.
```

When the repository maps Conventional Commits to releases, `feat` normally
signals a minor release, `fix` a patch release, and a breaking change a major
release. Verify that mapping against the project's release configuration; do
not infer or change a project version merely because a commit was made.

## Examples

```text
feat(cache): add bounded response caching
fix(parser): reject malformed empty headers
docs: explain local test setup
```
