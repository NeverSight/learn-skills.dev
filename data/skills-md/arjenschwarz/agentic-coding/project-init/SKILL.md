---
name: project-init
description: Initialize Claude Code project settings with standard hooks and language-specific permissions. Use when setting up a new project for Claude Code or adding standard configuration to an existing project.
---

# Project Init

Initialize a project with standard Claude Code configuration.

## What It Does

1. Adds a SessionStart hook to `.claude/settings.json` for remote environment setup
2. Detects project languages and adds appropriate tool permissions

## Language Detection

The script detects languages based on project files and adds permissions:

| Detection File | Language | Permissions Added |
|----------------|----------|-------------------|
| `go.mod` | Go | `go`, `golangci-lint`, `staticcheck`, `govulncheck` |
| `Package.swift`, `*.xcodeproj` | Swift | `swift`, `xcodebuild`, `swiftlint`, `xcrun` |
| `package.json` | Node.js | `npm`, `npx`, `node`, plus `yarn`/`pnpm`/`bun` if lockfiles present |
| `pyproject.toml`, `requirements.txt` | Python | `python`, `pip`, `uv`, `pytest`, `ruff`, `mypy` |
| `Cargo.toml` | Rust | `cargo`, `rustc` |
| `Gemfile` | Ruby | `ruby`, `bundle`, `rake`, `rspec` |
| `pom.xml` | Java (Maven) | `mvn`, `java` |
| `build.gradle` | Java (Gradle) | `gradle`, `./gradlew`, `java` |
| `Dockerfile` | Docker | `docker`, `docker-compose` |
| `*.tf` | Terraform | `terraform`, `tofu` |
| `Makefile` | Make | `make` |

`git` is always included.

## Usage

Run the setup script from your project directory:

```bash
~/.claude/skills/project-init/scripts/setup-project.sh
```

The script:
- Creates `.claude/settings.json` if it doesn't exist
- Merges hooks and permissions into existing settings without overwriting
- Is idempotent (safe to run multiple times)
- Requires `jq` for JSON manipulation

## Batch Setup

To initialize multiple projects:

```bash
for dir in ~/projects/*; do
  (cd "$dir" && ~/.claude/skills/project-init/scripts/setup-project.sh)
done
```
