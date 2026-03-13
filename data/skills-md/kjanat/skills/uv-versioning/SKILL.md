---
name: uv-versioning
description: Version bumping workflow for uv projects. Use when reading/updating package versions, planning release bump chains, or validating main vs workspace package bumps.
license: MIT
metadata:
  author: kjanat
  version: "1.0"
---

# uv-versioning

Safe, repeatable `uv version` usage for single-package and workspace projects.

## Use When

- You need current package version quickly.
- You need semantic/pre-release/post/dev bump updates.
- You need workspace package bumping via `--package`.
- You want preview-only changes via `--dry-run`.

## Core Rules

- Prefer `--dry-run` first for any non-trivial bump.
- Multiple `--bump` flags are allowed; order matters.
- Use `--package <name>` for workspace member bumps.
- Use `--output-format json` when scripts consume output.

## Read Version

```bash
uv version
uv version --short
uv version --output-format json
```

Workspace member:

```bash
uv version --package pykeepass-stubs
uv version --package pykeepass-stubs --output-format json
```

## Bump Components

Supported components:

- `major`, `minor`, `patch`
- `alpha`, `beta`, `rc`
- `post`, `dev`
- `stable`

Semantics:

- `major`: `1.2.3 -> 2.0.0`
- `minor`: `1.2.3 -> 1.3.0`
- `patch`: `1.2.3 -> 1.2.4`
- `alpha`: `1.2.3a4 -> 1.2.3a5`
- `beta`: `1.2.3b4 -> 1.2.3b5`
- `rc`: `1.2.3rc4 -> 1.2.3rc5`
- `post`: `1.2.3.post5 -> 1.2.3.post6`
- `dev`: `1.2.3a4.dev6 -> 1.2.3.dev7`
- `stable`: clear pre/dev/post to stable core, e.g. `1.2.3b4.post5.dev6 -> 1.2.3`

## Common Patterns

Main package:

```bash
uv version --bump major --bump alpha --dry-run
uv version --bump major --bump alpha

uv version --bump stable --dry-run
uv version --bump stable
```

Workspace package:

```bash
uv version --package pykeepass-stubs --bump major --bump alpha --dry-run
uv version --package pykeepass-stubs --bump major --bump alpha

uv version --package pykeepass-stubs --bump stable --dry-run
uv version --package pykeepass-stubs --bump stable
```

General form:

```bash
uv version [--package <workspace-member>] \
  --bump <major|minor|patch|post|dev|alpha|beta|rc|stable> \
  [--bump <...> ...] [--dry-run]
```

## Release Hygiene

- Keep bump commands aligned with repo release trigger policy.
- In split-release repos, do not mix main-package and stubs-package bumps.
- After real bump, confirm workflows/tags expect same normalized version.
