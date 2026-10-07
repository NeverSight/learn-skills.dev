---
name: release-ci
description: "Release automation, CI workflows, release-please configuration, contribution gate, and lockfile formatting in quota-axi."
user-invocable: false
---

# Release Automation, CI & Contribution Gate

This document describes the automated release pipeline, CI workflow constraints, contribution gate architecture, and repository maintenance rules in quota-axi.

---

## Release Process & Automation

- **Conventional Commits**: Releases are driven by conventional commit messages (`feat:`, `fix:`, `chore:`, etc.) merged into `main`.
- **Release Please**:
  - Automatically manages version bumps, changelog generation, and release PRs.
  - `.release-please-manifest.json` was primed at `0.1.0` (the version published manually before release-please integration); release-please updates it with each release.
  - `release-please-config.json` locks `bootstrap-sha` to `9f5dc949c50ab8ac0a441be777e1c3693ee0b612` (the commit producing the published 0.1.0 package). Never alter this SHA unless correcting the published baseline.
  - **Never Hand-Edit Generated Files**: Do not manually edit `CHANGELOG.md` or `.release-please-manifest.json`. A guard workflow (`.github/workflows/guard-generated-files.yml`) automatically rejects PRs that touch them.
- **npm Publishing**:
  - Merging the release PR triggers `.github/workflows/release-please.yml` to publish to npm.
  - Uses npm's OIDC trusted-publisher flow (`id-token: write` + `--provenance`) without stored token secrets.
  - Publishing steps are gated only on `steps.release.outputs.release_created`; the workflow has no repository guard. The binding to this package comes from npm's trusted-publisher OIDC configuration.
- **Skill Generation**:
  - `skills/quota-axi/SKILL.md` is generated from `src/skill.ts`.
  - Regenerate via `pnpm run build:skill` rather than editing directly. CI validates parity via `pnpm run build:skill -- --check`.

---

## CI Workflows & Exclusion Rules

- **Release Output Set Exclusions**:
  - Every `pull_request` workflow (`ci.yml`, `guard-generated-files.yml`) must include a `paths-ignore` filter covering the release-please output set (`.release-please-manifest.json`, `CHANGELOG.md`, `package.json`).
- **Gate Check Exception**:
  - The single deliberate exception to the `paths-ignore` rule is `.github/workflows/no-mistakes-required.yml`.
  - The gate check verdict is a function of the pull request body, not the changed files. Adding a path filter would drop the gate on PRs that still require attestation.
  - Both sides of this rule are guarded by `test/release-ci-exclusions.test.ts`.

---

## Contribution Gate Architecture

- **Contributor Workflow**: [CONTRIBUTING.md](../../CONTRIBUTING.md) defines contributor requirements, PR expectations, and exemptions.
- **Trusted Repository Configuration**:
  - `.no-mistakes.yaml` defines `commands.prepare` and `commands.test` (`pnpm test`), alongside `test.instructions` for post-baseline live validation.
  - `allow_repo_commands` remains disabled so untrusted pull request branches cannot inject arbitrary commands or agents.
  - Guarded by `test/no-mistakes-config.test.ts`.
- **Composite Action Pinning**:
  - `.github/workflows/no-mistakes-required.yml` delegates enforcement to `kunchenguid/no-mistakes/.github/actions/require-no-mistakes` pinned to an immutable commit SHA.
  - The pin is bumped only via deliberate, standalone pull requests.

---

## Lockfile Formatting

- The repository's `pnpm-lock.yaml` is formatted with Prettier.
- After updating dependencies, run:
  ```sh
  pnpm exec prettier --write pnpm-lock.yaml
  ```
- This ensures dependency diffs remain minimal and clean. CI's `pnpm install --frozen-lockfile` accepts Prettier-formatted YAML.
