---
name: semantic-versioning
description: >-
  Select, validate, or update a project's version according to Semantic
  Versioning 2.0.0. Use whenever a user asks to bump, release, tag, publish, or
  change a package/application version, and whenever a release plan needs a
  compatibility-based version recommendation.
---

# Semantic Versioning

Treat a version as a compatibility promise, not a counter. Follow the project's
release documentation and tooling first; validate that its version changes are
consistent with SemVer 2.0.0.

## Determine the correct version

1. Inspect the current version, latest published/tagged version, public APIs,
   release notes, and project-specific release rules. Identify which artifacts
   are actually versioned.
2. Compare the change with the existing public contract:
   - **MAJOR** (`X.0.0`): incompatible public API or behavior change.
   - **MINOR** (`0.X.0`): backwards-compatible public functionality.
   - **PATCH** (`0.0.X`): backwards-compatible bug fix.
3. For `0.y.z`, remember that SemVer treats the public API as unstable. Still
   use the project's documented compatibility policy and communicate breaking
   changes explicitly rather than silently treating every change as a patch.
4. Use prerelease identifiers for prerelease builds (for example,
   `2.1.0-rc.1`) and build metadata only for build identification; build
   metadata does not affect precedence.
5. If the impact is ambiguous, explain the uncertainty and ask before changing
   version files or creating a tag. If the user supplies a version, validate it
   and flag any mismatch instead of silently substituting another.

## Conventional Commits integration

When the project uses Conventional Commits for automated release selection,
verify the configured mapping. Common defaults are `feat` → MINOR, `fix` →
PATCH, and `!` / `BREAKING CHANGE:` → MAJOR. These are signals, not a substitute
for checking the actual compatibility impact and the project's release rules.

## Apply a version change safely

- Update every authoritative version declaration required by the project,
  including manifests, package metadata, generated constants, and release
  configuration as applicable.
- Update lockfiles only when the project's package manager or release process
  requires it; do not hand-edit generated lock data.
- Keep tags, changelog entries, artifacts, and published metadata aligned with
  the chosen version.
- Do not create/push a release tag or publish artifacts unless the user
  authorized that operation.
- Report the old and new versions, the SemVer rationale, changed version
  sources, and any release steps still pending.
