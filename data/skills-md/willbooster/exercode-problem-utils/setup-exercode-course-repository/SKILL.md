---
name: setup-exercode-course-repository
description: Use before generating or improving Exercode course content to ensure the repository has tracked mise-managed runtimes and Bun tooling for authoring and evaluating content.
---

# Set up an Exercode course repository

Prepare the repository tooling required to author and evaluate Exercode course content. Do not create or modify learning content.

## Tracked tooling setup

The repository tracks its tooling instead of ignoring it.

- `package.json` contains `private: true`, `type: "module"`, and the repository name.
- `@exercode/problem-utils` is an exact production dependency at its latest published version.
- `bun.lock` is tracked.
- Bun and Node.js are managed by mise with exact versions. Preserve an existing `mise.toml`, `.mise.toml`, or `.tool-versions`; when none exists, create `.tool-versions`.
- `.gitignore` includes `node_modules/`, `.DS_Store`, and `.tmp/`. It does not ignore `package.json` or `bun.lock`.
- Preserve compatible existing runtime versions, tools, dependencies, and scripts. Do not replace an existing mise or package setup wholesale.

## Workflow

1. Read the repository instructions and inspect only the tracked root tooling files, including `mise.toml`, `.mise.toml`, and `.tool-versions` when present.
2. Keep the repository's existing mise format. Ensure it pins exact Bun and Node.js versions, preserving compatible exact versions and every unrelated tool. If multiple mise files exist, do not duplicate a tool already declared in any of them; add missing tools to an existing TOML config. If none exists, create `.tool-versions` with the exact current stable Bun version and current LTS Node.js version.
3. If a mise TOML config is present, run `mise trust --yes`. Run `mise install`, then use the installed `bun` command normally for the remaining setup.
4. Create or update `package.json`, then run `bun add --exact @exercode/problem-utils@latest` so `package.json` and `bun.lock` agree.
5. Ensure `.gitignore` contains the required tooling entries without removing compatible existing entries.
6. Do not create, modify, move, validate, or evaluate any course, lecture, material, problem, contest, asset, or other learning-content file.
