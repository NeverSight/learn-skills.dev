---
name: setup-for-oss
description: Review and bootstrap open-source repo health (OSS) by auditing or scaffolding README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, SECURITY, GitHub templates, CI workflows, Renovate, publishing (pkg-pr-new + npm Trusted Publishing), linting/formatting, Changesets, and automation. Use when asked to review OSS setup, check OSS health, or set up/add OSS files and workflows.
---

# Setup for OSS

## Quick start

1. Decide mode:
   - **Audit mode**: user asks to review/check OSS health.
   - **Scaffold mode**: user asks to set up/add OSS files or workflows.
2. Collect context (minimal):
   - Repo name, package manager, monorepo vs single package, publishable npm packages.
   - Author/org details from `package.json` or git config.
   - Existing health files and workflows.
3. Load references as needed:
   - Health files: `references/health-files.md`
   - GitHub templates: `references/github-templates.md`
   - CI workflows: `references/ci-workflows.md`
   - Publishing: `references/publishing.md`
   - Linting/formatting: `references/linting-formatting.md`
   - Dependency/versioning: `references/dependency-versioning.md`

## Mode decision tree

- If the request includes **audit/review/check**: run **Audit mode** and return a prioritized missing/incomplete list.
- If the request includes **setup/add/bootstrap/scaffold**: run **Scaffold mode** and create/modify files.
- If unclear, default to **Audit mode** and ask a single clarifying question only if blocking.

## Context detection checklist

Use this before auditing or scaffolding:

- **Project name**: from `package.json:name` or repo folder name.
- **Author/org**: from `package.json:author`, `repository`, or git config.
- **Package manager**:
  - `pnpm-lock.yaml` → pnpm
  - `package-lock.json` → npm
  - `yarn.lock` → yarn
  - `bun.lockb` → bun
- **Monorepo vs single**:
  - `workspaces` in package.json, `pnpm-workspace.yaml`, or `turbo.json` → monorepo
- **Publishable packages**:
  - `package.json:private=false` or packages with `publishConfig`
- **Has tests**:
  - `test` script, `vitest`, `jest`, `playwright`, or `__tests__` directories
- **Conventional commit scopes**:
  - workspace package/app names for monorepo; otherwise top-level areas (src/docs/ci)

## Audit mode

1. Scan for required health files and templates:
   - README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, SECURITY
   - `.github` issue templates, PR template, release config, funding
2. Scan for CI/CD workflows:
   - `autofix.yml`, `ci.yml`, `semantic-pull-request.yml`, `label-pr.yml`
3. If publishable npm packages exist, verify:
   - `ci.yml` includes `publish` job using pkg-pr-new (PR-only)
   - `release.yml` uses npm Trusted Publishing (OIDC) and pinned SHAs
4. Scan for Renovate config, linting/formatting, versioning tooling:
   - `renovate.json`, `eslint.config.js`, `.editorconfig`, `.changeset/config.json`, `.npmrc`, `.config/automd.ts`
5. Produce a report:
   - Missing files
   - Incomplete/misaligned content (e.g., wrong license or missing security reporting)
   - Optional vs required (explicit)
   - Minimal next steps

## Scaffold mode

1. Create any missing required files using templates in references.
2. Adapt content:
   - Replace placeholders with project name, author/org, repo URLs, and package manager.
   - Include CI jobs only relevant to the repo (test job only if tests exist).
   - Include publishing and release workflows only if publishable packages exist.
3. Ensure all outputs are in English.
4. Summarize what was created/updated and any manual follow-ups (e.g., install GitHub Apps).

## Required vs optional outputs

**Required (always when scaffolding OSS setup):**
- README.md
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- LICENSE (Apache-2.0 default unless specified)
- SECURITY.md
- .github/funding.yml
- .github/ISSUE_TEMPLATE/bug-report.yml
- .github/ISSUE_TEMPLATE/enhancement-request.yml
- .github/ISSUE_TEMPLATE/feature-request.yml
- .github/ISSUE_TEMPLATE/question.yml
- .github/pull_request_template.md
- .github/release.yml
- .github/workflows/autofix.yml
- .github/workflows/ci.yml
- .github/workflows/semantic-pull-request.yml
- .github/workflows/label-pr.yml
- renovate.json
- eslint.config.js
- .editorconfig
- .changeset/config.json
- .npmrc
- .config/automd.ts

**Conditional (only when publishable npm packages exist):**
- .github/workflows/release.yml with npm Trusted Publishing (OIDC)
- `ci.yml` publish job with pkg-pr-new

## Manual follow-ups to report

- Install GitHub Apps: Renovate and pkg-pr-new (when needed).
- Configure npm Trusted Publisher in npmjs.com settings for publishable packages.
- Optionally enable npm 2FA and disallow tokens.

## Reference map

- Health files and README structure → `references/health-files.md`
- GitHub templates and release categories → `references/github-templates.md`
- CI workflows and jobs → `references/ci-workflows.md`
- Publishing (pkg-pr-new + npm Trusted Publishing) → `references/publishing.md`
- Linting/formatting → `references/linting-formatting.md`
- Renovate, Changesets, .npmrc, automd → `references/dependency-versioning.md`
