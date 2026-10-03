---
name: github-actions-pnpm-ci
description: Secure pnpm GitHub Actions CI
metadata:
  short-description: Secure pnpm GitHub Actions CI
---

# GitHub Actions pnpm CI

## Use This Shape

Install the bundled assets as the default CI shape:

- `.github/actions/prepare/action.yml` from `assets/prepare-action.yml`
- `.github/workflows/lint.yml` from `assets/workflows/lint.yml`
- `.github/workflows/test.yml` from `assets/workflows/test.yml`
- `.github/workflows/typecheck.yml` from `assets/workflows/typecheck.yml`
- `.github/workflows/build.yml` from `assets/workflows/build.yml`
- `.github/dependabot.yml` from `assets/dependabot.yml`

## Rules

- Keep remote actions pinned to full commit SHAs with the upstream semver tag in the same-line comment, for example `# v6.0.2`.
- Use `pnpm/action-setup` without a `version` input so it reads `packageManager` from `package.json`.
- Require `packageManager` to include pnpm integrity, for example `pnpm@10.33.4+sha512...`.
- Enable pnpm store caching by default with `actions/setup-node` `cache: pnpm`.
- Cache only the pnpm store; do not cache `node_modules`.
- Use `cache-dependency-path: pnpm-lock.yaml` for single-package repos.
- For workspaces, use both `pnpm-lock.yaml` and `pnpm-workspace.yaml` in `cache-dependency-path`.
- Install with `pnpm install --frozen-lockfile`.
- Keep CI token permissions at `contents: read` unless a job truly writes to GitHub.
- Add `concurrency` to every workflow.
- Add Dependabot for `github-actions` only.

## Adaptation

- If a script is missing, do not invent a command silently; first inspect `package.json` and use the closest existing script.
- If tests need Playwright, add `pnpm exec playwright install --with-deps chromium` before the test command.
- If a build needs dummy env vars, copy the repo-local pattern and keep secrets out of caches.
- If the repo already has user changes, preserve them and patch only the CI files needed.

## Validation

Run these after installing or updating the files:

```bash
pnpm exec actionlint
git diff --check
```

If `actionlint` is not available in the repo, use `pnpm dlx actionlint` or the repo's existing actionlint command.
