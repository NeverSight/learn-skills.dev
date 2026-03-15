---
name: good-code
description: >
  Generate a project-specific CLAUDE.md (or AGENTS.md) with coding standards, style guides, and
  best practices. Triggers on any request to set up a project, initialize coding standards,
  create or update CLAUDE.md or AGENTS.md, configure agent instructions, add code quality rules,
  or start a new codebase. Use this skill at the start of every new project.
---

# Code Design Principles — Agent Skill

You are setting up agent instructions for this project based on the **6 Principles of Good Code Design**: Consistent, Correct, Clear, Concise, Simple, Salient.

## Step 1: Check for Existing Files

Before writing anything, check if any of these files already exist in the project root:
- `CLAUDE.md`
- `AGENTS.md`
- `.cursorrules`
- `.github/copilot-instructions.md`

If any exist, show the user what was found and ask whether to:
- **Merge** the principles into the existing file
- **Replace** the existing file
- **Cancel**

Do not overwrite without explicit confirmation.

## Step 2: Detect Project Stack

Scan the project root for configuration files to determine the stack:

| File | Stack |
|------|-------|
| `package.json` | Node.js / TypeScript / JavaScript |
| `tsconfig.json` | TypeScript |
| `pyproject.toml` | Python (modern) |
| `setup.py` / `setup.cfg` | Python (legacy) |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `Gemfile` | Ruby |
| `pom.xml` / `build.gradle` | Java / Kotlin |
| `mix.exs` | Elixir |
| `Package.swift` | Swift |

Also detect:
- **Package manager**: Look for `uv.lock`, `poetry.lock`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `Pipfile.lock`
- **Test framework**: Look for `pytest.ini`, `jest.config.*`, `vitest.config.*`, `.mocharc.*`, test directories
- **Linter/formatter**: Look for `.eslintrc.*`, `biome.json`, `ruff.toml`, `.prettierrc.*`, `rustfmt.toml`

## Step 3: Read the Template

Read the `CLAUDE.md` file located in this skill's directory (next to this SKILL.md file). This is the base template you will customize. For the full rationale behind each principle, see `PRINCIPLES.md` in the same directory.

## Step 4: Generate the Instructions File

Using the template from Step 3, create a `CLAUDE.md` (or `AGENTS.md` if the user's agent platform prefers it) in the project root. The template includes Python and TypeScript as examples — adapt the language-specific sections to match the detected stack:

1. **Style Guide** — Replace the Python/TypeScript subsections with idiomatic style entries for the detected language(s).
2. **Project Setup** — Replace with actual setup instructions: package manager commands, build/test/lint scripts found in the project's config files (`package.json` scripts, `Makefile`, `pyproject.toml`, etc.). The Python section in the template shows the level of detail expected.

## Step 5: Confirm

After writing the file, tell the user:
- What file was created and where
- What stack was detected
- What sections were customized
- Suggest they review and adjust the Project Setup section for any project-specific tooling
