---
name: mise
description: |
  Mise (formerly rtx) polyglot tool version manager, environment variable manager, and task runner. Covers tool version management (install, use, pin across Node/Python/Rust/Go/Java and more), mise.toml task definitions (scripts, dependencies, watch mode, incremental builds), environment variable management (.env integration, per-directory env, redaction), project-level tool pinning, backend system (asdf, npm, pipx, cargo, GitHub releases), and comparison with alternatives (asdf, nvm, pyenv, Makefiles).

  Use when configuring development tool versions, defining project tasks in mise.toml, managing per-project environment variables, setting up polyglot dev environments, migrating from asdf or nvm, or automating build/test/lint/deploy workflows with mise run.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://mise.jdx.dev'
user-invocable: false
---

# Mise

## Overview

Mise is a **polyglot development tool manager** that handles tool versions, environment variables, and task running in a single CLI. It replaces asdf, nvm, pyenv, direnv, and Makefiles with a unified `mise.toml` configuration per project.

**When to use:** Managing multiple language runtimes per project, defining reproducible dev environments, running project tasks with dependencies, replacing scattered `.nvmrc`/`.python-version`/`.tool-versions` files, automating CI pipelines.

**When NOT to use:** Container-only workflows where all tools live in Docker images, single-language projects already well-served by their native version manager, production runtime management (mise is a dev tool).

## Version Resolution Order

Mise resolves tool versions by checking these sources in priority order:

1. `MISE_<TOOL>_VERSION` environment variable
2. `mise.toml` in current directory
3. `mise.toml` in parent directories (walks up the tree)
4. `.tool-versions` file (asdf compatibility)
5. Legacy files (`.nvmrc`, `.python-version`, `.ruby-version`)
6. `~/.config/mise/config.toml` (global default)

## Quick Reference

| Pattern               | Command / Config                         | Key Points                                  |
| --------------------- | ---------------------------------------- | ------------------------------------------- |
| Install tools         | `mise install`                           | Reads mise.toml, installs all listed tools  |
| Pin tool version      | `mise use node@22`                       | Writes to mise.toml in current directory    |
| Pin globally          | `mise use -g node@22`                    | Writes to ~/.config/mise/config.toml        |
| Run a task            | `mise run build`                         | Runs task defined in mise.toml              |
| Run with args         | `mise run test -- --watch`               | Passes args after `--` to the task          |
| Watch mode            | `mise watch build`                       | Re-runs task when sources change            |
| List tasks            | `mise tasks`                             | Shows all available tasks                   |
| Set env vars          | `[env]` section in mise.toml             | Per-directory, auto-activated on cd         |
| Load .env file        | `_.file = ".env"`                        | Loads dotenv into environment               |
| Extend PATH           | `_.path = ["./bin"]`                     | Prepends directories to PATH                |
| List installed        | `mise ls`                                | Shows all installed tool versions           |
| Outdated tools        | `mise outdated`                          | Shows tools with newer versions             |
| Upgrade tools         | `mise upgrade`                           | Upgrades tools to latest within constraints |
| Trust config          | `mise trust`                             | Trusts mise.toml in current directory       |
| Tool backends         | `"npm:prettier"` / `"cargo:cargo-watch"` | Install from npm, cargo, pipx, GitHub, etc. |
| Task dependencies     | `depends = ["lint", "test"]`             | Prerequisite tasks run first                |
| Incremental build     | `sources` + `outputs` on task            | Skips task if outputs newer than sources    |
| Exec without activate | `mise exec -- node app.js`               | Runs command with mise-managed tools        |
| Diagnostics           | `mise doctor`                            | Check installation and config health        |
| Prune unused          | `mise prune`                             | Remove tool versions not in any config      |
| Generate hook         | `mise generate git-pre-commit`           | Generate git pre-commit hook for tasks      |
| Env-specific config   | `.mise.staging.toml`                     | Activated via `MISE_ENV=staging`            |
| Shims for IDEs        | `mise settings set shims_on_path true`   | PATH-based shims for IDE compatibility      |

## Common Mistakes

| Mistake                                          | Correct Pattern                                                      |
| ------------------------------------------------ | -------------------------------------------------------------------- |
| Using `mise install node@22` without `mise use`  | `mise use node@22` both installs and pins to mise.toml               |
| Editing `.tool-versions` manually with mise      | Use `mise use` to update; mise.toml is preferred over .tool-versions |
| Forgetting `mise trust` on new project clone     | Run `mise trust` to activate untrusted config files                  |
| Using `depends` key for task dependencies        | Current key is `depends` (array), not `deps`                         |
| Running `mise run` without activating mise       | Run `mise activate` in shell profile or use `mise exec`              |
| Putting secrets directly in mise.toml            | Use `_.file = ".env.local"` and gitignore the .env file              |
| Expecting env vars without `cd`-ing into project | Mise activates env on directory change; use `mise env` to debug      |
| Using `latest` version in shared projects        | Pin specific major versions (`node = "22"`) for reproducibility      |
| Defining tasks in Makefile alongside mise        | Consolidate all tasks in mise.toml for one tool                      |
| Missing shebang in multi-line task scripts       | Add `#!/usr/bin/env bash` for explicit interpreter                   |
| Not using `sources`/`outputs` for slow tasks     | Define source globs for incremental skipping and watch mode          |
| Using `mise activate` in non-interactive scripts | Use `mise exec` or `eval "$(mise env)"` in scripts and CI            |

## Delegation

- **Task pattern discovery**: Use `Explore` agent
- **Configuration review**: Use `Task` agent
- **CI pipeline integration**: Use `Task` agent

> If the `rust` skill is available, delegate Rust toolchain management patterns to it.
> If the `python-uv` skill is available, delegate Python version and virtual environment patterns to it.
> If the `github-actions` skill is available, delegate CI workflow patterns to it.
> If the `docker` skill is available, delegate containerized workflow patterns to it.
> If the `pino-logging` skill is available, delegate logging configuration patterns to it.
> If the `sentry` skill is available, delegate error monitoring setup patterns to it.

## References

- [Tool version management and backends](references/tool-management.md)
- [Task definitions, dependencies, and scripts](references/task-runner.md)
- [Environment variables and dotenv integration](references/environment-variables.md)
- [Configuration files and settings](references/configuration.md)
- [Common task patterns for projects](references/task-patterns.md)
- [Migration from asdf, nvm, and alternatives](references/migration.md)
