---
name: ci-verify-setup
description: Set up a project-level `verify` command and GitHub Actions `CI.yml` that runs the same checks on pull requests and pushes.
---

# CI + Verify Setup Skill

Use this skill when the user asks to:

- add CI
- create/update `.github/workflows/CI.yml`
- add a `verify` script/command
- ensure local checks match CI checks

## Goal

Create a reliable, repeatable verification pipeline where:

1. Developers run one command locally: `verify`
2. CI runs the exact same command on PRs and pushes
3. The setup is minimal, deterministic, and easy to maintain

## Required Outcomes

- A project-level `verify` command/script exists
- `.github/workflows/CI.yml` exists and runs `verify`
- CI uses the project's package manager/runtime correctly
- Existing scripts/config are reused (avoid duplication)
- Changes are validated by running `verify` locally (if possible)

## Workflow

### 1) Inspect project tooling

Detect:

- language/runtime (Node, Python, etc.)
- package manager from lockfile (`bun.lock`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`)
- existing scripts/commands (`lint`, `test`, `typecheck`, `build`)
- current CI files/workflows (if any)

### 2) Define `verify` command

Rules:

- Prefer composing existing scripts over new custom logic
- Keep `verify` focused on quality gates (typecheck/lint/test)
- Include build only if project convention expects it
- Do not remove or break existing scripts

Recommended Node default:

- `typecheck && lint && test`
- If no typecheck exists, use lint + test
- If no tests exist, use typecheck + lint

### 3) Add/update package scripts

For JS/TS projects:

- Create `scripts.verify` in `package.json`
- Keep command package-manager-friendly (e.g., `bun run`, `pnpm`, `npm run` usage consistent with repo conventions)

### 4) Create/update `.github/workflows/CI.yml`

Requirements:

- Trigger on `pull_request` and `push` (default branch + feature branches)
- Minimal permissions (`contents: read`)
- Concurrency cancellation for duplicate branch runs
- Correct runtime setup and dependency install
- Single `verify` execution step

### 5) Validate end-to-end

- Run local `verify`
- Fix obvious breakages introduced by the setup
- Report any pre-existing failures separately

## CI Template Guidance (Node/Bun example)

Use this shape (adapt versions/commands to repo):

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v2

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Verify
        run: bun run verify
```

## Guardrails

- Never hardcode secrets in workflow files
- Never weaken checks to make CI green
- Avoid adding extra jobs unless requested
- Keep diffs focused (scripts + CI only unless needed)
- Preserve existing CI behavior unless user asked to replace it

## Completion Checklist

- [ ] `verify` command added or improved
- [ ] `CI.yml` added/updated to run `verify`
- [ ] Runtime + package manager setup is correct
- [ ] Local `verify` run attempted and results reported
- [ ] Any residual issues clearly documented
