---
name: harness-engineering
description: |
  Set up OpenAI's harness engineering methodology in any repository. Creates the
  full agent-first infrastructure: AGENTS.md progressive disclosure map, architectural
  layer boundaries with mechanical enforcement, testing framework, CI pipeline,
  golden principles documentation, garbage collection scripts, and pre-commit hooks.
  Use when asked to "set up harness engineering," "make the repo agent-ready,"
  "add architectural boundaries," "set up testing and CI," or "adopt agent-first
  engineering." Works with any stack — React, Next.js, Python, Go, Rails, etc.
---

# Harness Engineering Setup

You are an expert in OpenAI's harness engineering methodology. Your goal is to
transform any repository into an agent-first engineering environment where AI
agents (Codex, Copilot, Claude, or any other) can independently navigate, build,
test, and validate code within mechanically enforced boundaries.

## Background

Harness engineering (coined by OpenAI) shifts human engineers from writing code
to designing environments. The "harness" — like horse tack — channels powerful
but unruly agents to run safely together. Key principles:

1. **Engineers become environment designers** — define constraints, not implementations
2. **Give agents a map, not an encyclopedia** — progressive disclosure via AGENTS.md
3. **If agents can't see it, it doesn't exist** — all knowledge in the repo
4. **Enforce architecture mechanically** — linters and tests, not markdown instructions
5. **Boring technology wins** — composable, stable, well-trained-on APIs
6. **Entropy management is garbage collection** — recurring cleanup agents
7. **Throughput changes merge philosophy** — minimal blocking gates
8. **Agent-to-agent code review** — humans escalated only for judgment calls

## Phase 0: Discovery

Before generating anything, you MUST understand the repository. Run these steps:

### 0a. Detect the Stack

Analyze the repo to determine:

```bash
# Check for stack indicators
ls package.json pyproject.toml Cargo.toml go.mod Gemfile build.gradle pom.xml composer.json mix.exs 2>/dev/null
cat package.json 2>/dev/null | head -50
cat pyproject.toml 2>/dev/null | head -30
```

Identify:
- **Language(s):** TypeScript, Python, Go, Rust, Ruby, Java, etc.
- **Framework(s):** React, Next.js, Django, FastAPI, Rails, Spring, etc.
- **Package manager:** npm, pnpm, yarn, pip, poetry, cargo, go mod, bundler
- **Build tool:** Vite, Webpack, tsc, setuptools, cargo, make
- **Test runner (if any):** Vitest, Jest, pytest, go test, RSpec, JUnit
- **Linter (if any):** ESLint, Ruff, pylint, golangci-lint, RuboCop

### 0b. Map the Architecture

```bash
# Get directory structure
find . -maxdepth 3 -type d | grep -v node_modules | grep -v .git | grep -v __pycache__ | sort

# Check for existing docs/config
ls AGENTS.md CLAUDE.md .cursorrules .github/copilot-instructions.md docs/ 2>/dev/null

# Check for existing CI
ls .github/workflows/*.yml 2>/dev/null

# Check for existing tests
find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -name "*_test.*" | grep -v node_modules | head -20

# Check for existing lint config
ls .eslintrc* eslint.config* .pylintrc pyproject.toml .rubocop.yml .golangci.yml 2>/dev/null
```

### 0c. Identify Layers

Every codebase has implicit architectural layers. Your job is to make them
explicit. Common patterns:

**Web Frontend (React/Vue/Svelte/Angular):**
```
types/        → No app imports (pure type definitions)
utils/        → No app imports (pure functions)
lib/          → types/ only (clients, configs, core utilities)
services/     → lib/, types/ (business logic, API wrappers)
hooks/states/ → lib/, services/, types/ (state management)
components/   → hooks/, lib/, types/ (UI layer)
pages/routes/ → components/, hooks/, lib/, types/ (route entry points)
```

**Backend API (Express/FastAPI/Rails/Spring):**
```
types/models/ → No app imports (data definitions)
config/       → types/ only (configuration)
db/repo/      → config/, types/ (data access layer)
services/     → db/, config/, types/ (business logic)
middleware/    → services/, config/, types/ (request processing)
routes/       → services/, middleware/, types/ (HTTP handlers)
```

**Full-Stack (Next.js/Nuxt/SvelteKit):**
```
types/        → No app imports
lib/          → types/ only (shared utilities)
db/           → lib/, types/ (database layer)
services/     → db/, lib/, types/ (business logic)
components/   → lib/, types/ (UI primitives)
features/     → components/, services/, lib/, types/ (feature modules)
app/pages/    → features/, components/, lib/, types/ (routes)
```

**Monorepo (Turborepo/Nx/Lerna):**
```
packages/types/   → No internal imports
packages/config/  → types/
packages/db/      → config/, types/
packages/api/     → db/, config/, types/
packages/ui/      → types/ only
packages/web/     → ui/, api/, types/
```

Adapt the layers to match the ACTUAL directory structure. Don't force a structure
that doesn't fit. Read the import patterns in the codebase to discover the real
dependency graph.

### 0d. Ask Clarifying Questions

Before proceeding, confirm with the user:
- Which directories should be treated as which layers?
- Are there any special import relationships to preserve?
- What testing framework preference do they have?
- Do they want the full setup or specific phases?

## Phase 1: AGENTS.md — The Map

Create `AGENTS.md` at the repo root. This is the MOST important file. It must be:
- **~100 lines** (not an encyclopedia)
- **A table of contents** pointing to docs/ subdirectories
- **The entry point** for any agent working in the repo

### Template

```markdown
# {Project Name} — Agent Orientation Map

> {One-line description of what this project does.}

## Stack

| Layer | Tech |
|-------|------|
| {Language} | {version} |
| {Framework} | {version} |
| {Database} | {type} |
| {Other} | {details} |

## Architecture Layers

Dependency flows **downward only**. Never import upward.

{Generate the layer diagram from Phase 0c discovery}

## Key Conventions

- {Convention 1 — brief, with pointer to docs/golden-principles/ for details}
- {Convention 2}
- {Convention 3}

## Commands

```sh
{build command}
{test command}
{lint command}
{dev command}
```

## Documentation Map

```
docs/
├── architecture/         Dependency graph, layer rules
├── guides/               Setup, testing, deployment how-tos
├── golden-principles/    Canonical patterns (DO/DON'T examples)
└── {other categories as needed}
```

## Where to Look First

| Task | Start here |
|------|-----------|
| {common task 1} | {directory/file} |
| {common task 2} | {directory/file} |
| {common task 3} | {directory/file} |
```

## Phase 2: Documentation Structure

### 2a. Restructure docs/

If docs exist, reorganize them. If not, create the structure.

```bash
mkdir -p docs/architecture docs/guides docs/golden-principles
```

Move existing docs into appropriate subdirectories using `git mv` to preserve
history. Categories to consider:
- `architecture/` — layer rules, dependency flow, system design
- `guides/` — local dev, testing, deployment, onboarding
- `golden-principles/` — canonical coding patterns
- `features/` — feature specifications (if applicable)
- `integrations/` — third-party service docs (if applicable)
- `security/` — auth, access control docs (if applicable)
- `historical/` — completed work, migration notes (if applicable)

Only create subdirectories that make sense for the repo's scale.

### 2b. Create docs/architecture/LAYERS.md

This is the definitive reference for the layer hierarchy. Include:

1. **Layer diagram** — ASCII diagram with allowed dependency directions
2. **Hard rules** — violations that cause CI failure
3. **What each layer contains** — responsibility and key files
4. **Remediation guide** — for each common violation, explain how to fix it

Every error message in CI should point to this file.

### 2c. Create Golden Principles

Create 3-5 golden principles docs in `docs/golden-principles/`. Each should be
30-60 lines with DO and DON'T examples. Common candidates:

- **IMPORTS.md** — path aliases, import ordering, no deep relative imports
- **NAMING.md** — file naming, export conventions, variable naming
- **ERROR_HANDLING.md** — how to handle and report errors
- **LOGGING.md** — logging conventions (if a custom logger exists)
- **DATA_FETCHING.md** — how to fetch and cache data (frontend)
- **TESTING.md** — how to write tests, what to test, patterns to follow

Read the actual codebase patterns before writing these. Don't guess — discover.

## Phase 3: Testing Infrastructure

### 3a. Choose the Right Test Runner

| Stack | Test Runner | Install |
|-------|------------|---------|
| Vite/React/Vue | Vitest | `npm i -D vitest @testing-library/react jsdom` |
| Next.js | Vitest or Jest | `npm i -D vitest @testing-library/react jsdom` |
| Node.js/Express | Vitest or Jest | `npm i -D vitest` |
| Python | pytest | `pip install pytest pytest-cov` |
| Go | go test (built-in) | No install needed |
| Rust | cargo test (built-in) | No install needed |
| Ruby/Rails | RSpec or Minitest | `gem install rspec` |

### 3b. Create Test Configuration

Set up the test runner with:
- Path alias resolution matching the main build config
- Coverage reporting
- Test file patterns
- Setup files for common test utilities

### 3c. Create Test Utilities

Create common test helpers:
- **Mock factories** — for database clients, API clients, auth contexts
- **Render helpers** — (frontend) wrap components with providers for testing
- **Fixture factories** — generate test data

### 3d. Create the Architecture Boundary Test

This is the MECHANICAL ENFORCEMENT — the most critical test. It:

1. Scans all source files in the project
2. Parses import/require statements
3. Determines which layer each file belongs to
4. Validates that imports respect the layer rules
5. Fails with descriptive, actionable error messages

**Key design decisions:**
- Use the language's file I/O to scan (node:fs, os.walk, filepath.Walk)
- Parse imports with regex (good enough — no need for AST)
- Report violations with: `"VIOLATION: {file} imports from {target} — {layer} cannot import from {target_layer}. {remediation}. See docs/architecture/LAYERS.md"`
- Maintain a `KNOWN_VIOLATIONS` list that acts as a ratchet — you can only remove entries, never add without review
- The test passes if all violations are in the known list and fails if new ones appear

### 3e. Write Example Tests

Write 3-5 example tests that demonstrate the testing patterns for the codebase:
- A pure utility function test
- A configuration/setup validation test
- A component/handler test (if applicable)
- The architecture boundary test

## Phase 4: Linting & Boundary Enforcement

### 4a. Add Import Restriction Rules

Use the linter's native capabilities to enforce boundaries. Every error message
MUST include remediation instructions — the error output IS agent context.

**ESLint (JavaScript/TypeScript):**
Use `no-restricted-imports` with `patterns` in separate config objects per layer:
```javascript
{
  files: ['src/lib/**/*.{ts,tsx}'],
  rules: {
    'no-restricted-imports': ['error', {
      patterns: [{
        group: ['@/services/*', '@/hooks/*', '@/components/*', '@/pages/*'],
        message: 'lib/ is Layer 3 — cannot import from higher layers. See docs/architecture/LAYERS.md'
      }]
    }]
  }
}
```

**Ruff/pylint (Python):**
Use `banned-api` or custom checks via `[tool.ruff.lint.per-file-ignores]`.

**Go:**
Use `depguard` via golangci-lint.

**Rust:**
Use `clippy` restrictions or workspace dependency rules in Cargo.toml.

### 4b. Add Import Ordering (if applicable)

Enforce consistent import ordering:
- **ESLint:** `eslint-plugin-import` with `import/order`
- **Python:** `isort` via Ruff
- **Go:** `goimports` (built-in)
- **Rust:** `rustfmt` (built-in)

## Phase 5: CI/CD Pipeline

### 5a. Create CI Workflow

Create `.github/workflows/ci.yml` with parallel jobs:

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup {language}
        # Use appropriate setup action
      - run: {install_command}
      - run: {lint_command}

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup {language}
      - run: {install_command}
      - run: {typecheck_command}

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup {language}
      - run: {install_command}
      - run: {test_command}

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup {language}
      - run: {install_command}
      - run: {build_command}
```

Adapt the jobs to the stack. Not every stack needs all 4 jobs. Python may not
need a separate `build` job. Go may combine `typecheck` into `build`.

## Phase 6: Garbage Collection

### 6a. Create GC Check Scripts

Write simple scripts (in the repo's primary language or shell) that scan for
common violations of golden principles. Each script should:

1. Scan the source directory
2. Look for a specific anti-pattern
3. Report violations with file:line format
4. Exit 0 if clean, exit 1 if violations found

Common GC checks (pick the ones relevant to the stack):
- **Raw console/print statements** — should use a logger
- **Default exports** — should use named exports (JS/TS)
- **Inline magic numbers** — should use named constants
- **Large files** — files exceeding size limits (300 warn, 500 error)
- **TODO/FIXME/HACK comments** — track tech debt
- **Unused imports** — dead code detection
- **Missing type annotations** — (Python/TS)

### 6b. Create GC Runner

A single script that runs all GC checks and produces a summary:

```bash
npm run gc        # or
python scripts/gc_run_all.py  # or
make gc
```

### 6c. Create Scheduled GitHub Action

```yaml
name: Garbage Collection

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9am UTC
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  gc-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        # Setup language
      - name: Run GC
        run: {gc_command} > gc-report.txt 2>&1 || true
      - name: Create or update issue
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('gc-report.txt', 'utf8');
            const title = '🧹 Weekly Garbage Collection Report';
            const issues = await github.rest.issues.listForRepo({
              owner: context.repo.owner, repo: context.repo.repo,
              state: 'open', labels: 'garbage-collection', per_page: 1
            });
            const body = `## GC Scan — ${new Date().toISOString()}\n\n\`\`\`\n${report}\n\`\`\``;
            if (issues.data.length > 0) {
              await github.rest.issues.createComment({
                owner: context.repo.owner, repo: context.repo.repo,
                issue_number: issues.data[0].number, body
              });
            } else {
              await github.rest.issues.create({
                owner: context.repo.owner, repo: context.repo.repo,
                title, body, labels: ['garbage-collection']
              });
            }
```

## Phase 7: Pre-commit Hooks (Optional but Recommended)

### JavaScript/TypeScript:
```bash
npm install -D husky lint-staged
npx husky init
# .husky/pre-commit: npx lint-staged
# package.json: "lint-staged": { "*.{ts,tsx}": ["eslint --fix"] }
```

### Python:
```bash
pip install pre-commit
# .pre-commit-config.yaml with ruff, mypy, pytest hooks
pre-commit install
```

### Go:
```bash
# Use golangci-lint as a pre-commit hook
# Or use the pre-commit framework with Go hooks
```

## Execution Order

When the user says "set up harness engineering," execute in this order:

1. **Phase 0** — Discovery (ALWAYS do this first, NEVER skip)
2. **Phase 1** — AGENTS.md
3. **Phase 2** — Docs structure + LAYERS.md + golden principles
4. **Phase 3** — Testing infrastructure + architecture boundary test
5. **Phase 4** — Linter boundary enforcement rules
6. **Phase 5** — CI pipeline
7. **Phase 6** — Garbage collection scripts + workflow
8. **Phase 7** — Pre-commit hooks

Ask the user before starting: "Should I set up all phases, or specific ones?"

Work on a feature branch (`feat/harness-engineering`) in a new git worktree if
the user requests it.

## Important Rules

1. **Never hardcode project-specific details.** This skill works for ANY repo.
   Discover the stack, don't assume it.
2. **Read before you write.** Always read existing files before generating new
   ones. Match the repo's existing code style.
3. **Use git mv for doc restructuring.** Preserve git history.
4. **Every error message is agent context.** Remediation instructions go in the
   error output, not just in docs.
5. **The architecture test is a ratchet.** Known violations list can only shrink,
   never grow without explicit review.
6. **Don't break existing behavior.** New lint rules should warn, not error, if
   there are pre-existing violations across the codebase.
7. **Test your work.** Run the test suite, linter, and GC scripts after setup to
   verify everything works.
