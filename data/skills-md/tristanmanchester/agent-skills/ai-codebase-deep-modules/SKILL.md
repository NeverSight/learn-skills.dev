---
name: ai-codebase-deep-modules
description: >-
  Designs and refactors software codebases to be AI-friendly by aligning the filesystem with domain/feature boundaries, creating deep (greybox) modules with small public interfaces, enforcing import boundaries, and tightening tests/feedback loops. Use when the user asks to "make the codebase AI-ready", "reduce coupling", "introduce deep modules", "create module boundaries", "restructure folders by feature", "define service interfaces", or "plan a refactor + tests so AI agents can work safely".
compatibility: Works in skills-compatible coding assistants with repository file access. Optional scripts require Python 3.
metadata:
  author: generated-from-transcript
  version: "1.0.0"
---

# AI Codebase Deep Modules

Turn “a web of shallow, cross-importing files” into a codebase that is **easy for AI (and humans) to navigate, change, and test**.

This skill is built around four ideas:

1. **The codebase matters more than the prompt.** AI struggles when feedback is slow, structure is unclear, and dependencies are tangled.
2. **Match the filesystem to the mental model.** Group code the way you *think* about it (features/domains/services), not as a grab-bag of utilities.
3. **Prefer deep modules.** Lots of implementation behind a small, well-designed public interface.
4. **Treat deep modules as greyboxes.** Lock behaviour with tests at the boundary; internal code becomes replaceable.

## When to use this skill

Use this skill when the user wants any of the following:

- Refactor an existing repo to be **more navigable** and **safer for AI-assisted coding**
- Introduce/strengthen **module boundaries**, reduce coupling, or eliminate “spaghetti imports”
- Restructure the repo **by feature/domain** (a “map you hold in your head” reflected on disk)
- Define **service/module interfaces**, public APIs, and “only import from here” rules
- Build **fast feedback loops** (tests, typecheck, lint) so AI can verify changes quickly
- Plan a refactor with **incremental steps**, acceptance criteria, and tests

Do **not** use this skill for:
- One-off debugging of an isolated error (use normal debugging / code review)
- Purely stylistic refactors with no boundary or testing implications
- Writing greenfield code where the user already has a clear modular architecture (unless they want a module template)

## Inputs this skill expects (minimal)

If available, ask for or infer:

- Language/runtime (TS/JS, Python, Go, Java/Kotlin, etc.)
- How to run **the fastest meaningful check** (unit tests, typecheck, lint, build)
- The top 3–7 “chunks” of product behaviour (domains/features/services)
- Any hard constraints (monorepo tooling, existing packages, deployment boundaries)

If the user hasn’t provided this, **do not stall**. Make best-effort guesses by inspecting:
- `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Makefile`, `justfile`
- `src/`, `app/`, `packages/`, `services/`, `modules/`
- existing test folders and CI configs

---

# Workflow

## Step 0 — Establish the feedback loop (non-negotiable)

Goal: ensure there is a **fast “did it work?” loop** before and during refactors.

1. Identify the quickest command that provides signal:
   - Typecheck: `tsc -p tsconfig.json`
   - Unit tests: `npm test`, `pytest -q`, `go test ./...`
   - Lint: `eslint .`, `ruff check`, `golangci-lint run`
2. Prefer a **single “verify” entrypoint**:
   - `make verify`, `just verify`, `npm run verify`, `./scripts/verify.sh`
3. If tests are missing, propose the smallest viable starting point:
   - Smoke tests for core flows
   - Contract tests for the boundaries you’re about to introduce
4. If the loop is slow, propose speed-ups *before* large refactors:
   - Run only impacted packages
   - Split unit vs integration tests
   - Cache dependencies in CI

Deliverable: a short “Feedback loop” section with the exact commands and expected outputs.

## Step 1 — Reconstruct the mental map of the codebase

Goal: identify the natural groupings that already exist in the product.

1. List the product domains/features (aim for 3–10):
   - e.g. `auth`, `billing`, `thumbnail-editor`, `video-editor`, `cms-forms`
2. For each domain, identify:
   - entrypoints (routes/controllers/handlers)
   - data boundaries (models/schemas)
   - external dependencies (APIs, DB, queues)
3. Capture the current pain:
   - “Where do people get lost?”
   - “What breaks when we change X?”
   - “Where are imports crossing domains?”

Deliverable: a **Module Map** (table) with: domain, responsibilities, key files, current coupling risks.

## Step 2 — Design deep modules (few, chunky, stable interfaces)

Goal: reduce the number of things the agent must keep in working memory.

For each domain/module candidate:

1. Define the **public interface** (small surface area):
   - functions/classes/commands exposed
   - public types/data contracts
   - error/edge-case semantics
2. Define what is **explicitly internal**:
   - helper functions, adapters, DB queries, parsing, etc.
3. Decide the dependency direction:
   - Prefer: `domain → shared primitives`
   - Avoid: `domain ↔ domain` cross-imports
4. Keep the interface boring and predictable:
   - stable names
   - minimal parameters
   - explicit return types / result objects

Deliverable: an **Interface Spec** for each deep module:
- Public API (signatures)
- Invariants (pre/post conditions)
- Examples (happy path + one edge case)

See: [references/module-templates.md](references/module-templates.md)

## Step 3 — Align the filesystem to the map (progressive disclosure)

Goal: make it obvious where to look.

Default rule: **outside code imports only from a module’s public entrypoint**.

Recommended structure (adapt per language):

- `src/<module>/`
  - `index.*` (public exports)
  - `types.*` (public types)
  - `internal/` (implementation details; not imported from outside)
  - `__tests__/` or `tests/` (contract tests for the public API)

If the repo uses packages, prefer `packages/<module>/` with explicit exports.

Deliverable: a “Move plan” listing:
- directories to create
- files to move
- import paths to update
- temporary compatibility shims (if needed)

## Step 4 — Make modules greyboxes with boundary tests

Goal: you shouldn’t need to understand internals to trust behaviour.

1. Write/identify **contract tests** for each module’s public API:
   - behavioural checks
   - key error cases
   - side effects (DB writes, events emitted) via fakes/spies
2. Keep tests close to the interface:
   - treat internals as replaceable
3. Only add internal unit tests where:
   - performance-critical logic needs tight coverage
   - tricky algorithms deserve direct tests

Deliverable: test plan + initial contract test skeletons.

See: [references/testing-and-feedback.md](references/testing-and-feedback.md)

## Step 5 — Enforce boundaries (so the architecture stays true)

Goal: prevent the codebase from drifting back into a web.

Pick the lightest viable enforcement:

- **Conventions + code review** (baseline)
- **Lint rules** (TS/JS: `no-restricted-imports`, ESLint boundary plugins)
- **Architecture tests** (assert “module A cannot import module B”)
- **Language-level boundaries** (Go `internal/`, Rust `pub(crate)`, Java modules)

Deliverable: an “Enforcement” section with the exact rules and where to configure them.

See: [references/boundary-enforcement.md](references/boundary-enforcement.md)

## Step 6 — Refactor incrementally (strangler pattern)

Goal: avoid giant-bang rewrites.

Suggested sequence:

1. Create the new module folder and **public interface** (empty implementation).
2. Add contract tests (they will fail).
3. Add a thin adapter that wraps existing code (tests pass).
4. Move internals gradually behind the interface:
   - keep exports stable
   - delete old entrypoints only once usage is migrated
5. Repeat module-by-module.

Deliverable: a stepwise refactor plan with checkpoints and rollback options.

---

# Output format (what to produce)

When this skill is activated, produce a structured plan using this outline:

1. **Current state summary** (1–2 paragraphs)
2. **Fast feedback loop** (exact commands)
3. **Module Map** (table)
4. **Proposed deep modules** (list + responsibilities)
5. **Interface specs** (per module)
6. **Filesystem changes** (move plan)
7. **Boundary enforcement** (rules + tooling)
8. **Testing strategy** (contract tests first)
9. **Incremental migration steps** (with checkpoints)

Optional: copy the template from `assets/architecture-plan-template.md`.

---

# Examples

## Example 1 — Broad request
User says: “Make our TypeScript monorepo more AI-friendly. It’s hard to find things and tests are slow.”

Actions:
1. Identify `verify` loop (typecheck + unit tests) and how to run it per package.
2. Produce a module map (3–7 modules).
3. Propose deep modules with a clear public interface (`index.ts`, `types.ts`).
4. Recommend boundary enforcement via ESLint `no-restricted-imports`.
5. Add contract tests for each module.

Result: a concrete refactor plan and initial skeletons that can be executed incrementally.

## Example 2 — Specific boundary problem
User says: “Auth imports billing and billing imports auth. We keep breaking things.”

Actions:
1. Identify dependency cycle and why it exists (shared types? shared DB code?).
2. Extract a deep module interface boundary:
   - `auth` exports `getCurrentUser()`, `requireAuth()`
   - `billing` depends on those interfaces only (no deep imports)
3. Move shared primitives into `shared/` or `platform/` module.
4. Add an architecture rule to prevent the cycle returning.

Result: cycle removed, boundaries enforced, behaviour locked by tests.

---

# Troubleshooting

## Skill feels too “high level”
Use the template and references to get concrete:
- [references/module-templates.md](references/module-templates.md)
- [references/prompts.md](references/prompts.md)

## Refactor is risky / unknown behaviour
Prioritise greybox contract tests first:
- freeze behaviour at the public interface
- only then move internals

## Boundaries are hard to enforce in TS/JS
Start with lint rules and path conventions; add architecture tests if needed.
See: [references/boundary-enforcement.md](references/boundary-enforcement.md)
