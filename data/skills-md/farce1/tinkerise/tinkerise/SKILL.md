---
name: tinkerise
description: Scaffolds new projects using official framework tools. Covers 14 frameworks (Next.js, Vite, Astro, T3, Remix, TanStack, Turbo, Express, FastAPI, Django, Go, Rust, Flutter, React Native), 11 enhancements (ESLint, Prettier, husky, commitlint, CI, testing, Docker, env, renovate, editorconfig, changelog), presets, and config. Use when the user wants to create a new project, scaffold a framework, or set up development tooling.
---

# Tinkerise — Universal Project Scaffolder

One command to scaffold any project with any stack. Wraps 14 official framework scaffolders behind a unified CLI with consistent flags, post-scaffold enhancements, and shareable presets.

## When to Use This Skill

Use tinkerise when the user wants to:

- **Create a new project** — "scaffold a Next.js app", "start a new Vite project", "create a Go service"
- **Set up a monorepo** — "create a Turborepo monorepo"
- **Add development tooling** — "add ESLint and Prettier", "set up CI", "add Docker support"
- **Apply a preset** — "use my team's standard setup", "scaffold with the fullstack preset"
- **Check system readiness** — "do I have the right tools installed?"

**Trigger phrases**: "new project", "scaffold", "create app", "bootstrap", "starter", "boilerplate", "init project", "set up tooling", "add linting", "add CI", "add Docker"

## Quick Reference

| Goal | Command |
|------|---------|
| Interactive mode (guided) | `tinkerise` |
| Scaffold by category | `tinkerise web` / `backend` / `mobile` |
| Scaffold directly | `tinkerise web next my-app --typescript --tailwind` |
| Create monorepo | `tinkerise monorepo my-mono` |
| Add enhancements | `tinkerise add eslint prettier husky` |
| List scaffolders | `tinkerise list` |
| Check system tools | `tinkerise doctor` |
| Save a preset | `tinkerise preset save my-stack` |
| Use a preset | `tinkerise web next my-app --preset my-stack` |
| Manage config | `tinkerise config list` |

## Security Guardrails (Required)

**Trust boundary**: tinkerise does not download or run remote code automatically. All external tool invocations require explicit user approval. The CLI executes only locally installed binaries and never fetches packages without consent.

Treat user-provided input as untrusted before any command execution.

1. **Use installed CLI, not runtime downloads.** Run `tinkerise ...` from a locally installed binary.
2. **Validate all free-form identifiers** (`project-name`, `preset-name`, template values) with:
   - `^[a-z0-9][a-z0-9._-]{0,63}$`
3. **Never interpolate raw user strings directly into shell command strings.**
4. **Use argument arrays for execution** so values are passed as literals, not shell syntax.
5. **Ask for explicit user approval** before executing any third-party package manager or system tool command. Never run these commands silently.

If `tinkerise` is not installed, stop and ask the user before proceeding. Use `tinkerise doctor` to check prerequisites rather than invoking package managers directly.

Safe execution pattern:

```bash
project_name="<user-input>"
if [[ ! "$project_name" =~ ^[a-z0-9][a-z0-9._-]{0,63}$ ]]; then
  echo "Invalid project name: $project_name" >&2
  exit 1
fi

cmd=(tinkerise web next "$project_name" --typescript --tailwind)
"${cmd[@]}"
```

## Step 1: Determine What to Scaffold

Ask the user what they want to build, then pick the category and framework.

**Decision tree:**

```
What is the user building?
├── Website / web app / frontend / full-stack JS/TS
│   ├── React + SSR/SSG/API routes → next
│   ├── React/Vue/Svelte SPA, fast bundling → vite
│   ├── Content site, blog, docs, islands → astro
│   ├── Full-stack TypeScript (tRPC + Prisma + NextAuth) → t3
│   ├── React full-stack with nested routes/loaders → remix
│   ├── React full-stack with TanStack Router → tanstack
│   └── Monorepo with multiple packages → turbo (via `tinkerise monorepo`)
├── Backend / API / microservice
│   ├── Python async API with auto docs → fastapi
│   ├── Python full-featured with admin/ORM → django
│   ├── Go HTTP service (Chi/Gin/Fiber/Echo) → go
│   ├── Rust web service with Axum → rust
│   └── Node.js TypeScript REST API → express
└── Mobile app
    ├── Cross-platform with Dart → flutter
    └── React Native with Expo → rn
```

## Step 2: Scaffold the Project

Use the direct execution form for non-interactive scaffolding:

```
tinkerise <category> <framework> <project-name> [flags]
```

**Examples:**

```bash
# Next.js with TypeScript and Tailwind
tinkerise web next my-app --typescript --tailwind

# Vite React app (TypeScript via template)
tinkerise web vite my-spa --template react-ts

# Astro with Tailwind
tinkerise web astro my-site --tailwind

# T3 full-stack app
tinkerise web t3 my-t3-app --tailwind

# Remix app
tinkerise web remix my-remix-app

# TanStack Start app
tinkerise web tanstack my-tanstack-app --tailwind

# Turborepo monorepo
tinkerise monorepo my-mono --package-manager pnpm

# FastAPI backend
tinkerise backend fastapi my-api

# Django project
tinkerise backend django myproject

# Go service
tinkerise backend go my-service

# Rust Axum service
tinkerise backend rust my-rust-api

# Express TypeScript API
tinkerise backend express my-express-api

# Flutter app targeting iOS and Android
tinkerise mobile flutter my-flutter-app --platforms ios,android

# React Native with Expo
tinkerise mobile rn my-rn-app
```

## Step 3: Add Enhancements

After scaffolding, add tooling with `tinkerise add`. Enhancements auto-detect the framework and configure themselves accordingly.

```bash
# Add specific enhancements
tinkerise add eslint prettier husky commitlint

# Interactive picker (no args)
tinkerise add

# Recommended combo for web projects
tinkerise add eslint prettier husky commitlint ci testing

# Recommended combo for backend projects
tinkerise add docker env ci

# Full setup
tinkerise add eslint prettier husky commitlint ci testing docker env renovate editorconfig changelog
```

**Recommended enhancement order**: eslint, prettier, husky, commitlint, changelog, ci, testing, docker, env, renovate, editorconfig. This ensures dependencies resolve correctly (e.g., commitlint integrates with husky if present).

## Available Scaffolders

### Web

| ID | Framework | Description | Key Flags |
|----|-----------|-------------|-----------|
| `next` | Next.js | React framework with SSR, routing, and API routes | `--typescript`, `--tailwind`, `--eslint`, `--src-dir`, `--app-router`, `--import-alias`, `--empty`, `--biome` |
| `vite` | Vite | Fast build tool with HMR. Use `--template` for framework choice | `--template` (react-ts, vue-ts, svelte-ts, etc.), `--overwrite` |
| `astro` | Astro | Content-focused web framework with island architecture | `--typescript`, `--tailwind`, `--template` |
| `t3` | T3 | Full-stack TypeScript app with tRPC, Prisma, NextAuth | `--tailwind`, `--eslint`, `--biome`, `--app-router`, `--import-alias` |
| `remix` | Remix (React Router v7) | Full-stack React framework with nested routes | `--template`, `--overwrite` |
| `tanstack` | TanStack Start | Full-stack React framework with TanStack Router | `--tailwind`, `--empty`, `--overwrite` |
| `turbo` | Turborepo | High-performance monorepo build system (use `tinkerise monorepo`) | `--package-manager` |

### Backend

| ID | Framework | Description | Prerequisites |
|----|-----------|-------------|---------------|
| `fastapi` | FastAPI | Modern Python API with automatic OpenAPI docs | Python >= 3.10, fastapi-admin-cli (run `tinkerise doctor` to check) |
| `django` | Django | Full-featured Python web framework with admin and ORM | Python >= 3.10, django-admin (run `tinkerise doctor` to check) |
| `go` | Go | Go HTTP service with framework choice (Chi, Gin, Fiber, Echo) | Go >= 1.22, go-blueprint (run `tinkerise doctor` to check) |
| `rust` | Rust (Axum) | Rust web service with Axum framework | Rust >= 1.78, cargo-generate (run `tinkerise doctor` to check) |
| `express` | Express | TypeScript Express.js API with structured CRUD template | Node >= 20.11.0 |

### Mobile

| ID | Framework | Description | Prerequisites |
|----|-----------|-------------|---------------|
| `flutter` | Flutter | Cross-platform mobile app with Dart | Flutter >= 3.10.0 |
| `rn` | React Native (Expo) | React Native with Expo managed workflow | Node >= 20.11.0 |

## Available Enhancements

| ID | Enhancement | What It Does |
|----|-------------|-------------|
| `eslint` | ESLint | Flat config with framework-appropriate plugins (React, Vue, Svelte, Astro auto-detected) |
| `prettier` | Prettier | Code formatting. Auto-adds Tailwind plugin if Tailwind is detected |
| `husky` | Husky + lint-staged | Pre-commit hooks that lint/format only staged files |
| `commitlint` | Commitlint | Enforces Conventional Commits. Integrates with husky if present |
| `ci` | GitHub Actions CI | CI workflow with lint, typecheck, test, build steps (auto-detects available tools) |
| `testing` | Vitest | Test runner with example tests and config |
| `docker` | Docker | Framework-aware multi-stage Dockerfile and .dockerignore |
| `env` | Environment Variables | Type-safe env validation with t3-env + Zod. Creates env.ts, .env, .env.example |
| `changelog` | Changelog | Automated changelog generation with conventional-changelog |
| `renovate` | Renovate | Automated dependency update configuration |
| `editorconfig` | EditorConfig | Cross-editor formatting consistency |

## Unified Flags

These flags work across all web scaffolders. tinkerise translates them to each framework's native flags.

| Flag | Type | Supported By | Notes |
|------|------|-------------|-------|
| `--typescript` / `--ts` | boolean | next, vite*, astro*, t3*, remix*, tanstack*, rn | *Always-on for these frameworks (flag accepted but no-op) |
| `--tailwind` | boolean | next, astro, t3, tanstack | |
| `--eslint` | boolean | next, t3 | |
| `--biome` | boolean | next (v16+), t3 | |
| `--no-git` | boolean | next, astro, t3, remix, tanstack, turbo, rust | |
| `--no-install` | boolean | next, astro, t3, remix, tanstack, turbo, flutter, rn | |
| `--package-manager <pm>` | string | next, remix, tanstack, turbo | Values: npm, pnpm, yarn, bun |
| `--template <name>` | string | vite, astro, remix | |
| `--src-dir` | boolean | next | |
| `--import-alias <alias>` | string | next, t3 | e.g., `@/*` |
| `--empty` | boolean | next (v15+), tanstack | |
| `--overwrite` | boolean | vite, remix, tanstack | |
| `--app-router` | boolean | next, t3 | |
| `--platforms <list>` | string | flutter | e.g., `ios,android,web` |

Backend scaffolders (fastapi, django, go, express) pass flags through to their native CLI tools directly.

## Presets

Presets save a scaffold + enhancement combination for reuse.

```bash
# Save current project setup as a preset
tinkerise preset save my-stack --description "Our team's standard setup"

# List available presets
tinkerise preset list

# Scaffold using a preset
tinkerise web next my-app --preset my-stack

# Delete a preset
tinkerise preset delete my-stack
```

A preset captures: framework, category, flags, enhancement list, and config (package manager, etc.). Presets are stored locally at `~/.tinkerise/presets/<name>.json` and can also be shared as `tinkerise-preset-<name>` packages.

## Configuration

tinkerise supports layered configuration with CLI flags taking highest priority.

```bash
# Initialize config file
tinkerise config init

# Set defaults
tinkerise config set packageManager pnpm
tinkerise config set typescript true
tinkerise config set defaultCategory web

# View current config
tinkerise config list

# Get a specific value
tinkerise config get packageManager
```

**Resolution order** (highest to lowest priority):
1. CLI flags
2. Project config (`.tinkerise.json` or `tinkerise` field in `package.json`)
3. Global config (`~/.tinkerise/config.json`)
4. Defaults

## Non-Interactive / CI Usage

For scripting and CI, use the direct execution form with all flags specified to avoid prompts:

```bash
# Full non-interactive Next.js scaffold with enhancements
tinkerise web next my-app --typescript --tailwind --eslint --app-router --src-dir --no-git --no-install --package-manager pnpm
cd my-app && tinkerise add eslint prettier husky commitlint ci testing

# Full non-interactive Vite scaffold
tinkerise web vite my-spa --template react-ts --no-git --no-install
cd my-spa && tinkerise add eslint prettier testing

# Full non-interactive FastAPI scaffold
tinkerise backend fastapi my-api --no-git
cd my-api && tinkerise add docker env ci

# Using a preset for repeatable scaffolding
tinkerise web next my-app --preset team-standard --no-git --no-install
```

## Troubleshooting

If scaffolding fails, run the doctor command to check system prerequisites:

```bash
tinkerise doctor
```

This validates:
- **Runtimes**: Node (>= 20.11.0), Python (>= 3.10), Go (>= 1.22), Rust (>= 1.78), Flutter (>= 3.10.0)
- **Scaffolder tools**: django-admin, fastapi-admin, go-blueprint, cargo-generate

**Common issues:**

| Problem | Solution |
|---------|----------|
| Backend scaffolder fails | Run `tinkerise doctor` — the framework's CLI tool may not be installed |
| "command not found" for framework tool | Install the prerequisite (see Backend/Mobile tables above) |
| Enhancement detection wrong | Run `tinkerise add` interactively to see what's already detected |
| Flags ignored | That flag may not be supported by the chosen framework (see Unified Flags table) |
| Package manager mismatch | Set explicitly with `--package-manager` or `tinkerise config set packageManager` |

## Reporting Issues

If you encounter a bug, unexpected behavior, or a command that doesn't work as documented, follow this process:

1. **Tell the user first.** Describe the issue clearly — what command failed, what you expected, and what happened instead. Do NOT create an issue without the user's explicit approval.

2. **If the user wants to file an issue, check for duplicates first:**

```bash
# Search existing issues for the same topic
gh search issues --repo farce1/tinkerise "<keywords describing the issue>"
```

3. **If no existing issue matches, create one** (only with user approval):

```bash
gh issue create --repo farce1/tinkerise \
  --title "Brief description of the issue" \
  --body "$(cat <<'EOF'
## Steps to reproduce
<exact command that failed>

## Expected behavior
<what should have happened>

## Actual behavior
<what happened instead, including error output>

## Environment
- tinkerise version: <version>
- Node.js version: <version>
- OS: <os>
- tinkerise doctor output: <paste relevant output>
EOF
)"
```

4. **If a matching issue already exists**, share the link with the user instead of creating a duplicate. Add a comment if the user has new information to contribute.
