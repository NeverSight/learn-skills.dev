---
name: agents-md-gen
description: This skill should be used when the user asks to "generate an AGENTS.md", "create a CLAUDE.md", "write agent instructions", "set up AGENTS.md", "make an AGENTS.md for this repo", "configure agent behavior", or mentions generating, writing, or improving an AGENTS.md or CLAUDE.md file for a project.
context: fork
---

# Generating AGENTS.md

This skill explores a codebase, detects patterns and conventions, and generates a minimal AGENTS.md that gives AI coding agents just enough context to work effectively — plus progressive disclosure files for domain-specific details.

**Voice:** Write like someone who respects the reader's token budget AND knows what actually matters in a codebase. Benefit-first — tell the agent what it needs to succeed, not everything you know. Concrete — exact commands, exact tool names, no "use the appropriate tool." Ruthlessly concise — every line loads on every single request. If it doesn't change agent behavior, delete it.

**Core principle:** The ideal AGENTS.md is as small as possible. ~150-200 instructions is the effective attention budget. Every token you add displaces tokens the agent needs for the actual task.

## Phase 1: Explore the codebase

Before writing anything, understand the project deeply. The AGENTS.md will be wrong if you skip this.

### 1.1 Detect project metadata

Look for these files (check all, not just the first match):

- `package.json`, `deno.json`, `bun.lock` — JS/TS ecosystem
- `Cargo.toml` — Rust
- `go.mod` — Go
- `pyproject.toml`, `setup.py`, `setup.cfg` — Python
- `Gemfile`, `*.gemspec` — Ruby
- `pom.xml`, `build.gradle`, `build.gradle.kts` — JVM
- `*.csproj`, `*.sln` — .NET
- `Makefile`, `Taskfile.yml`, `justfile` — build entry points
- `docker-compose*.yml`, `Dockerfile` — containerized
- IaC config files — infrastructure

Extract: project name, language(s), package manager, build system, test framework, linter, formatter.

### 1.2 Detect repo type

| Signal                                                                                              | Type                   |
| --------------------------------------------------------------------------------------------------- | ---------------------- |
| `bin` field, CLI framework imports (commander, clap, cobra, click, oclif), `main` with flag parsing | **CLI tool**           |
| Web framework imports (express, fastify, flask, django, gin, axum, rails), route definitions        | **Web app / API**      |
| `exports`/`main` with no `bin`, `lib.rs`, library-style public API, published to registry           | **Library**            |
| `workspaces`, `packages/` or `apps/` dirs, Nx/Turborepo/Lerna config, multiple `go.mod`             | **Monorepo**           |
| Helm charts, Terraform modules, Dockerfiles without app code                                        | **Infrastructure**     |
| `ios/`, `android/`, React Native/Flutter/Expo config                                                | **Mobile / native**    |
| `action.yml`, browser extension `manifest.json`, VS Code extension with `contributes`               | **Plugin / extension** |

### 1.3 Discover local patterns and conventions

This is where AGENTS.md differs from a README. You're looking for things an AI agent needs to know to produce code that fits the project — not things a human user needs to get started.

**Build & run commands:**

- How to build: `npm run build`, `cargo build`, `make`, etc.
- How to run tests: exact command, including flags the project uses
- How to lint/format: exact commands, including any `--fix` flags
- How to typecheck: if separate from build
- Any non-obvious dev setup steps

**Code patterns:**

- Read 5-10 representative source files. Look for:
  - Import style (named vs default, absolute vs relative paths, path aliases)
  - Error handling patterns (Result types, try/catch style, error classes)
  - Async patterns (async/await, promises, channels, goroutines)
  - State management approach
  - Naming conventions (camelCase, snake_case, PascalCase — for files, variables, types)
  - Test file location and naming (`*.test.ts` next to source? `tests/` directory? `_test.go`?)
  - Test style (describe/it, test(), #[test], table-driven)

**Architecture decisions:**

- Don't document file paths — they go stale. Instead note the conceptual organization:
  - "Feature-sliced architecture" or "MVC layout" or "domain-driven packages"
  - Key domain concepts and their vocabulary (e.g., "we call them 'organizations' not 'teams'")
  - Dependency direction (which layers depend on which)

**Config and tooling:**

- `.eslintrc`, `biome.json`, `rustfmt.toml`, `.editorconfig` — note their existence, don't duplicate their content
- CI pipeline files — what checks must pass
- Pre-commit hooks — what runs automatically

### 1.4 Check for existing AGENTS.md / CLAUDE.md

If one exists, read it carefully. Identify:

- What's still accurate
- What's stale or wrong
- What's bloated (duplicates linter config, documents file paths, states the obvious)
- What's genuinely useful and must be preserved

## Phase 2: Write the files

### 2.1 Root AGENTS.md — keep it minimal

The root file should contain ONLY what's relevant to every single task in the repo.

**Required (always include):**

- One-sentence project description
- Package manager (if not the ecosystem default)
- Build / typecheck / test / lint commands (if non-standard or multi-step)

**Include only if it changes agent behavior:**

- Key architectural constraints ("never import from `internal/` outside the package")
- Domain vocabulary that differs from obvious meaning
- Non-obvious conventions the linter doesn't catch
- Links to progressive disclosure files

**Never include:**

- File paths (they go stale — describe capabilities instead)
- Things the linter/formatter already enforces (the agent will see the errors)
- Obvious coding practices ("write clean code", "use meaningful names")
- Full language style guides (move to separate files)
- Comprehensive architecture overviews (move to separate file)

Template for a single repo:

```markdown
# AGENTS.md

[One sentence: what this project is.]

## Commands

[Only non-obvious ones. Skip if standard.]

- Build: `[command]`
- Test: `[command]`
- Test single: `[command for running one test]`
- Lint: `[command]`
- Typecheck: `[command]`
- Format: `[command]`

## Conventions

[3-7 bullets max. Only things the agent would get wrong without being told.]

- [Convention that isn't enforced by tooling]
- [Domain term clarification]
- [Architectural constraint]

For [language] conventions, see `docs/[LANGUAGE].md`.
For testing patterns, see `docs/TESTING.md`.
```

Template for a monorepo:

```markdown
# AGENTS.md

[One sentence: what this monorepo contains.]

Uses [package manager] workspaces.

## Commands

- Install: `[command]`
- Build all: `[command]`
- Test all: `[command]`

## Structure

[Brief conceptual description — not file paths.]

See each package's AGENTS.md for package-specific conventions.
```

### 2.2 Progressive disclosure files

Create separate files for domain-specific guidance. Only create files for areas where the project has meaningful conventions that aren't enforced by tooling.

**When to create a separate file:**

- 5+ related conventions that only matter for one domain
- Language-specific patterns the project follows consistently
- Testing patterns that differ from framework defaults
- API design patterns specific to the project

**When NOT to create a separate file:**

- The conventions are already in linter/formatter config
- There are fewer than 3 conventions to document
- The information is available in framework docs the agent already knows

**Format for progressive disclosure files:**

```markdown
# [Domain] Conventions

[2-3 sentences of context: what this covers and why.]

## [Category]

- [Convention with brief rationale]
- [Convention with brief rationale]

## [Category]

- [Convention with brief rationale]
```

Keep each file under 100 lines. If it's longer, split it further.

### 2.3 Monorepo: package-level AGENTS.md

For monorepos, each package/app with its own conventions gets its own AGENTS.md:

```markdown
# AGENTS.md

[One sentence: what this package does.]

[Stack: e.g., "TypeScript + Express + Prisma"]

## Commands

- Test: `[package-specific command]`
- Dev: `[package-specific command]`

## Conventions

- [Package-specific convention]
```

Don't repeat root-level conventions. The agent sees both files merged.

### 2.4 Infuse stack best practices

Based on the detected stack, include conventions that experienced engineers follow but agents commonly get wrong. Only include what's relevant to the actual project.

**These should go in progressive disclosure files, not the root AGENTS.md.**

Examples of high-value, stack-specific guidance:

- "Use `Result<T, E>` for recoverable errors, `panic!` only for invariant violations" (Rust)
- "Prefer server components by default. Add `'use client'` only when hooks or browser APIs are needed" (Next.js App Router)
- "Use `errgroup` for concurrent operations that should fail together" (Go)
- "Test behavior, not implementation. Mock at the boundary, not the unit" (any)
- "Prefer `Depends()` injection over importing services directly" (FastAPI)

Don't dump a style guide. Pick the 5-10 things the agent is most likely to get wrong based on what you saw in the actual code.

## Phase 3: Verify

Before presenting the output:

1. **Token budget check.** Is the root AGENTS.md under 50 lines? If not, move content to progressive disclosure files.
2. **Every command must be real.** Verify build/test/lint commands exist in package.json, Makefile, or equivalent.
3. **No file paths in root AGENTS.md.** Describe capabilities, not locations. Paths to progressive disclosure docs are the only exception.
4. **No duplication with tooling.** If the linter enforces it, don't document it.
5. **No obvious advice.** Read every line and ask: "Would the agent do the wrong thing without this?" If not, delete it.
6. **No stale content.** If preserving parts of an existing AGENTS.md, verify those parts are still accurate.
7. **Progressive disclosure files are referenced.** Every file you create must be linked from the root or from a parent file.
8. **Read it as the agent.** On every request, this loads before the user's task. Is every line worth that cost?

## Decision Policy

- **ALWAYS** explore the codebase before writing. Never generate from the project name alone.
- **ALWAYS** read actual source files to discover patterns. Don't infer conventions from metadata alone.
- **ALWAYS** verify every command you include by checking package.json / Makefile / build configs.
- **ALWAYS** prefer smaller. When in doubt, leave it out. The agent can discover things at runtime.
- **Ask before replacing**: if an AGENTS.md already exists, show the user what you'd change and confirm. Existing files may contain hard-won knowledge.
- **Describe capabilities, not file paths**: "Authentication is handled via JWT middleware" not "Auth lives in src/middleware/auth.ts."
- **Don't duplicate linter config**: if `.eslintrc` says no `var`, you don't need to say it again.
- **Don't state the obvious**: "Use TypeScript" in a TypeScript project wastes tokens.
- **Monorepos get layered files**: root + per-package. Don't repeat root conventions in packages.
- **Stack best practices go in separate files**: keep the root clean.

## Safety Rules

- **No secrets in output**: if you find API keys, tokens, or credentials while exploring, do not include them. Use placeholder names.
- **No invented conventions**: only document patterns you actually observed in the code. If you're unsure, read more files to confirm.
- **Read-only exploration**: do not modify any project files during the explore phase. Only write AGENTS.md and progressive disclosure files.
- **Preserve institutional knowledge**: if an existing AGENTS.md has non-obvious rules (e.g., "never use ORM for the analytics database — it's a different engine"), keep them even if you don't fully understand why.

## Error Handling

- **Empty repo / no code**: tell the user there's nothing to document yet. A project description placeholder is all you can offer.
- **No package manifest**: determine stack from code structure, imports, and file extensions instead.
- **Existing AGENTS.md with custom content**: don't silently overwrite. Show what you'd change and get confirmation.
- **Can't determine conventions**: when the codebase is inconsistent (mixed styles, no clear patterns), note the inconsistency to the user and ask what they want to standardize.
- **Massive monorepo**: focus on root AGENTS.md + the 3-5 most active packages. Don't try to cover everything in one pass.
- **Conflicting patterns**: if different parts of the codebase follow different conventions, flag the contradiction. Ask the user which to standardize on.
