---
name: biome-linting
description: Linting and formatting workflows with Biome
metadata:
  tags: linting, formatting, biome, javascript, typescript, css, json
---

## When to use

Use this skill when you need to:
- Set up linting and formatting in a JavaScript, TypeScript, CSS, or JSON project using Biome
- Configure `biome.json` / `biome.jsonc` for a project
- Migrate from ESLint, Prettier, or other linters/formatters to Biome
- Run linting and formatting consistently in CI and local development

## How to use

Read individual rule files for implementation details and examples:

- [rules/biome-setup.md](rules/biome-setup.md) - Install, configure, and customize Biome
- [rules/biome-config.md](rules/biome-config.md) - Build `biome.json` config for JS/TS/CSS/JSON projects
- [rules/migration-from-eslint-prettier.md](rules/migration-from-eslint-prettier.md) - Migrate from ESLint and/or Prettier to Biome
- [rules/ci-and-editor-integration.md](rules/ci-and-editor-integration.md) - CI scripts, pre-commit, and editor setup

## Core principles

- Prefer reproducible linting with pinned exact versions (`-E` flag)
- Keep config minimal and explicit
- Use `biome check` as the single command for lint + format + import sorting
- Treat lint and format failures as quality gates in CI using `biome ci`
- Enable auto-fix with `--write` for local workflows, but validate with `biome ci` in CI
