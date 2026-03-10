---
name: project-analyzer
description: "Analyze codebase and create CLAUDE.md documentation. Use when analyzing project, understanding codebase, or creating documentation."
allowed-tools: [Task]
---

# ABOUTME: Automated codebase analysis and CLAUDE.md generation
# ABOUTME: Project structure mapping, convention detection, documentation creation

# Project Analyzer

Analyzes a codebase via a specialized agent (Haiku) that generates comprehensive CLAUDE.md documentation.

## When to Use

- Starting work on a new project
- Need to understand project structure
- Creating/updating project documentation

## Agent Invocation

Use the Task tool with:

```
subagent_type: "project-analyzer"
prompt: "Analyze the project in [directory] and create comprehensive CLAUDE.md documentation"
```

The agent will:
1. Scan directory structure
2. Identify language and framework
3. Analyze code patterns with ast-grep
4. Detect conventions
5. Generate CLAUDE.md

---

## Language Detection

| Indicator File | Language/Framework | Key Config Files |
|---|---|---|
| `go.mod` | Go | `go.sum`, `Makefile` |
| `pyproject.toml` | Python | `uv.lock`, `setup.py`, `.python-version` |
| `Gemfile` | Ruby/Rails | `Gemfile.lock`, `config/routes.rb` |
| `Package.swift` | Swift | `*.xcodeproj`, `*.xcworkspace` |
| `build.gradle.kts` | Kotlin/Android | `settings.gradle.kts`, `AndroidManifest.xml` |
| `package.json` | Node/React | `next.config.*`, `tsconfig.json` |
| `*.tf` | Terraform | `*.tfvars`, `terragrunt.hcl` |
| `Cargo.toml` | Rust | `Cargo.lock` |
| `docker-compose.yml` | Docker | `Dockerfile`, `.dockerignore` |

Also check: `.gitignore`, `.env.example`, `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`

Quality tools: `.golangci.yml` (Go), `ruff.toml` (Python), `.rubocop.yml` (Rails), `.eslintrc` (JS)

---

## Framework Detection

| Pattern | Framework |
|---|---|
| `config/routes.rb` | Rails |
| `next.config.*` | Next.js |
| `angular.json` | Angular |
| `nuxt.config.*` | Nuxt |
| `fastapi` in deps | FastAPI |
| `django` in deps | Django |
| `gin` or `echo` in go.mod | Go web |
| `Vapor` in Package.swift | Vapor |

---

## CLAUDE.md Required Sections
- Project purpose (1-2 sentences)
- Tech stack + versions
- Build/test/lint commands
- Architecture overview (directory structure)
- Key conventions and patterns
- Environment setup
- Vault Context (if vault is configured; see `_VAULT_CONTEXT.md`)

---

## Resources

**Related Skills:**
- Language analysis: `_AST_GREP.md`
- Go projects: `golang/SKILL.md`
- Python projects: `python/SKILL.md`
- Rails projects: `rails/SKILL.md`
- Terraform: `terraform/SKILL.md`
