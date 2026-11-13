---
name: environment-preflight
description: >-
  Inspect a project's structure, frameworks, and tech stack, then verify in the
  user's shell and development environment whether the agent has direct access
  to the required runtimes, package managers, and CLIs. Use this skill when
  starting work in a repository, before running builds/tests/toolchains, or when
  diagnosing missing command-line tools—and notify the user clearly whenever
  required tools are missing or inaccessible.
---

# Environment Preflight

Before assuming you can build, test, lint, migrate, or run a project's toolchain, **inspect the repository to determine what technologies it uses**, then **probe the active shell environment** to confirm direct access to every required tool. Never guess, fabricate tool output, or silently skip a check when a CLI is unavailable.

## 1. Identify Project Stack & Required Tools

Scan the repository root (and workspace/monorepo packages, if present) for manifests, lockfiles, and configuration files to map the tech stack:

- **Runtimes & Version Pins**: `.nvmrc`, `.node-version`, `.python-version`, `.ruby-version`, `.tool-versions`, `mise.toml`, `rust-toolchain.toml`, `go.mod`, `engines` in `package.json`, `requires-python` in `pyproject.toml`.
- **Package Managers & Lockfiles**: `package.json` + `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `bun.lockb`, `pyproject.toml` / `uv.lock` / `poetry.lock` / `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle*`, `Gemfile`, `composer.json`.
- **Frameworks, Build & Quality Tools**: Scripts and configs (e.g., `scripts` in `package.json`, `Makefile`, `justfile`, `Taskfile.yml`, `tsconfig.json`, `vite.config.*`, `next.config.*`, `pytest.ini`, `ruff.toml`, `.eslintrc*`, `biome.json`).
- **Infrastructure & External CLIs**: `Dockerfile`, `docker-compose.yml`, `terraform/`, `k8s/`, `.github/workflows/*`, database/migration configs (e.g., `prisma/`, `drizzle.config.*`, `alembic.ini`), or cloud/platform configs (`vercel.json`, `firebase.json`, `fly.toml`).

From these files, build a concise list of **required** tools for the current task (e.g., runtime, package manager, test runner, linter/typechecker, container or cloud CLI) and **optional** tools.

## 2. Probe the Shell & Development Environment

Check what the agent can directly execute in the current terminal/shell:

1. **Check binary availability**:
   - POSIX (`bash`/`zsh`/`sh`): `command -v <tool>` (or `which <tool>`).
   - Windows PowerShell: `Get-Command <tool> -ErrorAction SilentlyContinue`.
2. **Check project-local and version-manager paths** before concluding a tool is missing:
   - Node.js: `./node_modules/.bin/<tool>` (or `npx` / `pnpm exec` / `bunx`).
   - Python: `.venv/bin/<tool>`, `venv/bin/<tool>`, or `uv run <tool>`.
   - Version managers: `nvm`, `fnm`, `mise`, `asdf`, `pyenv`, `rbenv`, `rustup` (check if shims exist or if the shell hasn't initialized them).
3. **Verify versions & runtime readiness**:
   - Run lightweight version checks (`<tool> --version` or `<tool> version`) and compare against project version pins.
   - For daemon- or auth-dependent CLIs (e.g., `docker`, `kubectl`, `gh`, `aws`, `gcloud`, `psql`), verify operational access when the task requires them (e.g., `docker info`, `gh auth status`)—not just binary existence.
4. **Do not mutate the system silently**:
   - Never install global packages, modify shell profiles, or change system toolchains without explicit user approval.

## 3. Classify Findings & Notify the User

Categorize each required tool into one of three states:

- **Ready**: Accessible in the agent's shell (or project-local environment) with a compatible version.
- **Accessible with caveats**: Installed, but requires activating a local environment (e.g., `.venv`, `nvm use`), has a version mismatch against project pins, or its daemon/auth/network access is unavailable in the current shell.
- **Missing / Inaccessible**: Not installed or not reachable from the agent's terminal environment.

### When Tools Are Missing or Inaccessible

**Notify the user immediately** before proceeding with work that depends on those tools. Keep the notification concise and actionable:

1. **What is missing or blocked**: Name the exact tool/CLI and which part of the project or task requires it (e.g., `pnpm` required by `pnpm-lock.yaml`, `docker` daemon unreachable).
2. **What was checked**: Mention the probe performed (e.g., `command -v pnpm`, `.venv/bin/pytest`, `docker info`) and the observed error or version mismatch.
3. **How to resolve**: Provide clear installation, `PATH`/environment activation, or permission instructions—or ask the user to run the command locally and share the output if the agent environment cannot access it.
4. **Impact on current task**: State clearly whether you can still make progress (e.g., implementing code changes while deferring test/build verification to the user) or whether the task is blocked until the tool is available.

## 4. Session Discipline

- Run this preflight once when entering an unfamiliar project or starting a new toolchain-dependent task; do not repeat identical probes on every step.
- Re-probe only when switching to a different subproject/stack or after the user confirms they installed or fixed a tool.
