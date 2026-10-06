---
name: af-project
description: Apply af-project conventions when creating or evolving Alfin's personal software projects. Trigger when asked to follow this project guideline, scaffold a new repository, implement Rust/Actix APIs or SvelteKit frontends, review architecture, or enforce full-stack project standards.
license: Viewing-Only
metadata:
  author: Alfin Syahruddin
  version: "1.0.0"
---

# af-project

Reusable architecture, workflow, and code guidelines for Alfin's personal projects.

> [!NOTE]
> Rust/Actix and SvelteKit represent the standard reference stack **when building a new backend and web application**. For other platforms (e.g., iOS, Android, CLI tools, ML pipelines), follow the shared rules (Setup, Documentation, Workflow) and the target platform's idiomatic design patterns.

---

## Inviolable Golden Rules

When creating or modifying code under this guideline, agents and contributors must strictly enforce these invariants:

1. **Strict Layer Segregation**: Routes only extract HTTP inputs and invoke services. Repositories only execute parameterized SQL. Services orchestrate business rules and external I/O. All domain DTOs strictly reside in `entities/`.
2. **Unified API Envelope**: Every endpoint returns `AppResponse<T>` (`Result<Json<BaseResponse<T>>, AppError>`) via `.json()` or `.json_data()`. Never return ad-hoc, raw JSON structures.
3. **Zero Unwraps in Production**: Never use `.unwrap()` or `.expect()` in production Rust paths; propagate errors via `Result<T, AppError>` and `?`.
4. **Svelte 5 Runes Only**: All frontend components must use modern Svelte 5 Runes (`$props`, `$state`, `$derived`, `$effect`). Never generate legacy Svelte 3/4 syntax (`export let`, `$:`, `on:click`).
5. **Pure CSR Mode**: The web frontend is strictly a single-page application (`export const ssr = false;` in root `+layout.ts`). Never create server routes (`+page.server.ts` or `+server.ts`).
6. **Zero-Egress E2E Tests**: Playwright browser tests run with only the frontend dev server. Every API request must be intercepted with mock fixtures; tests must fail fast on unmocked requests.
7. **Natural Language Commits**: When a commit is authorized, write a descriptive message. Do NOT use Conventional Commit prefixes (`feat:`, `fix:`). Multiline commit messages with dashed bullet points are explicitly intended for multi-part changes. Message style does not authorize creating a commit.
8. **Append-Only Migrations**: Never modify or reorder migrations that have already been applied. Always create a new sequential file under `backend/migrations/` (e.g. `YYYYMMDDHHMM_description.sql`).
9. **No `@layer components` for Feature Styling**: Never use Tailwind `@layer components` or global `@apply` abstractions for feature- or page-specific styling. Colocate styles directly in Svelte components using utility classes or scoped `<style>` blocks.

---

## Agent Decision Matrix: What to Read

Find your current task and read only the relevant reference files:

| If your task is...                                            | Read this reference first                                                                                         |
| :------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------- |
| **Starting a new project from scratch**                       | [Setup](references/setup-project.md)                                                                             |
| **Deciding where to place new files or folders**              | [Project Structure](references/project-structure.md)                                                              |
| **Selecting libraries or adding dependencies**                | [Tech Stack](references/tech-stack.md)                                                                            |
| **Writing or updating README.md, AGENTS.md, or docs/**        | [Documentation](references/documentation.md)                                                                      |
| **Running tests, linting, Docker, or handoff**                | [Workflow & Verification](references/workflow.md)                                                                 |
| **Managing environment variables, secrets, or Compose**       | [Environment and Compose](references/environment-and-docker.md)                                                   |
| **Building a new backend endpoint, migration, or service**    | [Backend Code Patterns](references/backend/code-patterns.md) → [Vertical Slice](references/backend/feature.md)     |
| **Modifying core backend startup, config, or error handling** | [Backend Foundations](references/backend/foundations.md)                                                          |
| **Implementing auth, passwords, or Redis session tracking**   | [Backend Optional Components](references/backend/optional-components.md)                                          |
| **Building a new frontend page, component, or state module**  | [Frontend Code Patterns](references/frontend/code-patterns.md) → [Vertical Slice](references/frontend/feature.md)  |
| **Modifying frontend setup, CSS tokens, or API client**       | [Frontend Foundations](references/frontend/foundations.md)                                                         |
| **Implementing auth state, toasts, or theme toggling**        | [Frontend Optional Components](references/frontend/optional-components.md)                                         |

---

## Standard Agent Execution Procedure

1. **Inspect Context**: Check repository manifests (`Cargo.toml`, `package.json`), existing tests, and contributor documentation.
2. **Follow Boundaries**: Keep domain DTOs in `entities/`, queries in `repositories/`, logic in `services/`, and routes thin.
3. **Execute Verification**: Select and report checks appropriate to the changed area, following [Workflow & Verification](references/workflow.md). Distinguish failures caused by the change from unrelated or baseline failures.
4. **Handoff Clearly**: Summarize implemented changes, tests run, and operational limits.
