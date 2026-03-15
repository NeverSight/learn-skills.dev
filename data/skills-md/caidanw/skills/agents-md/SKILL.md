---
name: agents-md
description: >-
  Write effective AGENTS.md files that give coding agents the context they need to work
  in a repository. Use when creating a new AGENTS.md, improving an existing one, setting up
  a repo for AI coding agents, or onboarding agents to a codebase. Triggers on: "write AGENTS.md",
  "create AGENTS.md", "agent instructions", "set up repo for agents", "configure coding agent",
  "onboard agent to codebase", "agent context file".
---

# Writing Effective AGENTS.md Files

AGENTS.md is a README for coding agents. It lives at the repo root and tells agents how to
build, test, lint, navigate, and contribute to the project. Based on the agents.md open format
(https://agents.md) and lessons from OpenAI's harness engineering approach.

## Core Principle: Map, Not Manual

Keep AGENTS.md short (~100-150 lines). It's a **table of contents**, not an encyclopedia.

The "one big instruction file" approach fails because:
- **Context is scarce.** A giant file crowds out the actual task and code.
- **Everything-is-important becomes nothing-is-important.** Agents pattern-match locally instead of navigating intentionally.
- **It rots instantly.** A monolithic manual becomes a graveyard of stale rules.
- **It's hard to verify.** A single blob doesn't lend itself to freshness checks.

Point to deeper docs elsewhere. The agent starts with AGENTS.md and drills into
references as needed.

## What to Include

### 1. Dev Environment & Commands

The most immediately useful section. Concrete commands, not prose.

```markdown
## Commands
- Install: `npm install`
- Dev server: `npm run dev`
- Test single file: `npx vitest run path/to/test.ts`
- Test all: `npm test`
- Lint: `npm run lint`
- Format: `npm run format`
- Type check: `npm run typecheck`
```

Include any prerequisites or non-obvious setup. If the project uses Docker, Nix, or
a custom build system, say so here.

### 2. Repository Structure

Key paths and what lives where. Keep it high-level — 1 line per directory.

```markdown
## Repository Structure
- `src/api/` — HTTP API layer, routes and validation
- `src/store/` — Database access, all SQL lives here
- `src/worker/` — Background job processing
- `src/types/` — Shared domain types
- `tests/` — Test files mirror source structure
- `docs/` — Architecture and design documentation
```

For the full treatment of how to write an architecture codemap with boundaries
and invariants, see the `architecture-md` skill.

### 3. Architecture Boundaries

What can depend on what. What's deliberately absent. These are the rules agents
violate most often without explicit guidance.

```markdown
## Architecture Boundaries
- API layer never accesses the database directly — always goes through `src/store/`
- `src/types/` has zero dependencies on other source modules
- Workers communicate via the store interface, never import API code
- No circular dependencies between top-level modules
```

### 4. Coding Standards (Non-Obvious Only)

Don't list things the agent already knows (like "use const over let"). List only
project-specific conventions the agent couldn't infer from reading the code.

```markdown
## Coding Standards
- Strict TypeScript — no `any`, no `as` casts except in test files
- Errors: use `Result<T, E>` pattern from `src/types/result.ts`, not thrown exceptions
- Logging: always use structured logger from `src/logger.ts`, never `console.log`
- Naming: database columns are snake_case, TypeScript properties are camelCase
```

### 5. Testing Instructions

How to run tests, where they live, patterns to follow, what to cover.

```markdown
## Testing
- Tests live next to source: `src/foo.ts` -> `src/foo.test.ts`
- Use `describe`/`it` blocks, not `test()`
- Mock external services, never hit real APIs in tests
- New features require tests — cover success, failure, and edge cases
- Run relevant tests before submitting: `npx vitest run src/path/`
```

### 6. PR & Commit Conventions

```markdown
## Commits & PRs
- Conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- PR title format: `type(scope): description`
- Run `npm run lint && npm test` before committing
- Keep PRs focused — one logical change per PR
```

### 7. Boundaries (Do / Don't / Ask First)

Explicit guardrails prevent costly mistakes.

```markdown
## Boundaries
- **Never:** commit secrets, credentials, or tokens
- **Never:** use destructive git operations (force push, hard reset) without asking
- **Never:** edit generated files by hand when a generation workflow exists
- **Ask first:** large cross-module refactors, new dependencies, migration changes
```

### 8. References

Pointers to deeper documentation. This is where the "table of contents" pattern
pays off — keep AGENTS.md lean, point elsewhere for depth.

```markdown
## References
- Architecture: see `ARCHITECTURE.md`
- API docs: see `docs/api-reference.md`
- Design decisions: see `docs/design-docs/`
- Deployment: see `docs/deployment.md`
```

## What to Omit

- **README content** — Don't duplicate project description, installation for end users, badges
- **Language basics** — Don't explain TypeScript/Python/Rust fundamentals
- **Every lint rule** — Only list non-obvious, project-specific ones
- **Prose paragraphs** — Use bullet points and code blocks. Agents parse structure, not essays
- **Things that change every PR** — Only include stable conventions
- **Implementation details** — "How the scheduler works" belongs in ARCHITECTURE.md, not here

## Monorepo Pattern

Root AGENTS.md for global rules. Nested AGENTS.md per package for package-specific
instructions. The closest file to the edited code wins.

```
AGENTS.md                    # global: commit conventions, CI, shared tooling
packages/api/AGENTS.md       # API-specific: routes, middleware, auth patterns
packages/worker/AGENTS.md    # worker-specific: job patterns, retry behavior
packages/shared/AGENTS.md    # shared lib: no side effects, pure functions only
```

Keep nested files focused on what's **different** about that package. Don't repeat
global rules — the agent reads both the nearest file and the root.

## Anti-Patterns

- **The novel** — 500+ lines of prose. Nobody reads it, agent or human.
- **Stale rules** — "Always use library X" when the team switched to Y months ago. Stale rules are worse than no rules — agents follow them faithfully.
- **Redundant guidance** — Restating what the linter already enforces. If `eslint` catches it, don't list it.
- **Vague instructions** — "Write clean code" is useless. "Use structured logger, never console.log" is actionable.
- **Missing commands** — The agent should be able to build, test, and lint from AGENTS.md alone without reading CI config.

## Quality Checklist

Before finishing, verify:

- [ ] Can an agent build, test, lint, and format using only the commands listed?
- [ ] Is the repository structure documented at the directory level?
- [ ] Are architecture boundaries explicit (what can't depend on what)?
- [ ] Are only non-obvious coding standards listed?
- [ ] Are there clear "never do" guardrails?
- [ ] Does it point to deeper docs rather than trying to contain everything?
- [ ] Is it under ~150 lines?
- [ ] Would a stale rule here cause real damage? If so, can it be enforced mechanically instead?
