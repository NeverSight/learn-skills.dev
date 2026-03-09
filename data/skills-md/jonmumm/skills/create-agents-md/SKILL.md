---
name: create-agents-md
description: >
  Bootstrap AGENTS.md as a short table-of-contents plus a structured docs/
  directory (architecture, product specs, acceptance tests, ADRs, exec plans,
  quality grades). Use when AGENTS.md is missing, when asked to "create
  AGENTS.md", "bootstrap project for agents", or "set up agent context".
---

# Create AGENTS.md

Create `AGENTS.md` as the agent's **table of contents** — a ~100-line map
pointing to deeper sources of truth in `docs/`. Agents start here,
then load only what they need (progressive disclosure).

> **Philosophy:** AGENTS.md is a map, not an encyclopedia.
> A monolithic instruction file crowds out the task and rots instantly.
> Keep it short; point to deeper docs.

## When to Use

- The project has no `AGENTS.md` and you're about to run a swarm or any agent workflow.
- User asks to "create AGENTS.md", "set up this repo for agents", or "bootstrap agent context".
- The project has an existing AGENTS.md that is overly long or monolithic and needs restructuring.

## What to Do

### Phase 1: Pre-Flight Detection

Before generating anything, detect and report.

#### 1. Inspect the Project

| Check | How |
|-------|-----|
| Project name | `package.json` name, or directory name |
| Package manager | `bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm |
| Framework & stack | Read `package.json` deps, config files (tsconfig, vitest, playwright, detox, stryker, etc.) |
| Source layout | Scan top-level directories (`src/`, `app/`, `lib/`, `services/`, `db/`, `e2e/`, etc.) |
| Existing agent docs | Check for `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `spec/`, `docs/` |
| Existing gitignore | Check `.gitignore` for `.swarm/`, `.claude/` |

#### 2. Detect Feedback Commands

Auto-detect from `package.json` scripts, then confirm with user:

| Command | Look for in scripts |
|---------|-------------------|
| Typecheck | `typecheck`, `tsc`, `type-check` |
| Lint | `lint`, `biome`, `eslint` |
| Test | `test`, `test:unit`, `vitest`, `jest` |
| Coverage | `test:coverage` |
| Mutation | `test:mutate`, `test:mutate:incremental` |
| E2E | `test:e2e`, `e2e`, `detox test` |

#### 3. Report and Confirm

Show the user what you found and what will be generated:

```
Pre-Flight: create-agents-md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project:           my-app (pnpm, TypeScript, React, Vitest)
Feedback commands:  typecheck, lint, test, test:mutate:incremental
Existing docs:     CLAUDE.md found (will reference from Knowledge Base)
                   spec/SPEC.md found (will migrate to docs/product-specs/)

Will generate:
  AGENTS.md                           (~100 lines, the TOC)
  docs/ARCHITECTURE.md                (system map)
  docs/product-specs/index.md         (product requirements catalog)
  docs/acceptance/index.md            (acceptance test catalog)
  docs/adrs/index.md                  (ADR catalog)
  docs/design-docs/index.md           (design doc catalog)
  docs/design-docs/core-beliefs.md    (agent-first principles)
  docs/exec-plans/active/             (active plans directory)
  docs/exec-plans/completed/          (completed plans directory)
  docs/QUALITY.md                     (quality grades)

Proceed? [Y/n]
```

Only generate after user confirms.

### Phase 2: Generate

#### 1. Create `docs/` directory structure

Always create the full structure:

```
docs/
├── ARCHITECTURE.md                ← system map
├── QUALITY.md                     ← quality grades per domain/layer
├── lessons.md                     ← persistent project lessons (meta)
├── product-specs/
│   ├── index.md                   ← catalog of product spec files
│   └── (migrate existing spec files here, or create starters)
├── acceptance/
│   ├── index.md                   ← catalog of .feature files
│   └── (seed .feature files from existing specs if available)
├── adrs/
│   ├── index.md                   ← catalog of ADRs
│   └── (seed from existing "Key Decisions" sections)
├── design-docs/
│   ├── index.md                   ← design doc catalog
│   └── core-beliefs.md            ← agent-first principles
└── exec-plans/
    ├── active/                    ← plans being worked
    └── completed/                 ← finished plans (history)
```

#### 2. Create `AGENTS.md`

Use the template below. Fill every placeholder with real values.
Aim for 80–100 lines.

#### 3. Update `.gitignore`

Append if not already present:
```
# Agent working files
.swarm/
.claude/
```

### Phase 3: Seed Content (Optional)

If the project has existing docs that map to the new structure, offer to
migrate content:

| Existing | Offer to migrate to |
|----------|-------------------|
| `spec/SPEC.md` or similar behavioral spec | `docs/product-specs/` (prose) + `docs/acceptance/` (Gherkin distillation) |
| Inline architecture diagram in old AGENTS.md | `docs/ARCHITECTURE.md` |
| "Key Decisions" bullet list | Individual ADR files in `docs/adrs/` |
| Platform gotchas, framework rules | `docs/design-docs/platform-gotchas.md` |
| Visual design / theme docs | `docs/design-docs/visual-design.md` |

## Product Specs vs. Acceptance Tests

These are related but distinct:

```
Product Specs (docs/product-specs/)       Acceptance Tests (docs/acceptance/)
─────────────────────────────────────     ──────────────────────────────────────
Prose. Human intent. The "what & why."    Gherkin. Testable contract. The "how to verify."
Organized by domain area.                 Organized by feature, date-named like migrations.
Evolves as the product vision changes.    Updated when specific behaviors change.
Read by humans and agents for context.    Read by agents to verify behavior, can generate
                                          runnable tests (Playwright, Detox, Vitest).

Example:                                  Example:
"Users hear audio chunks and self-grade   Feature: Listening Session
 their comprehension using an Anki-style    Scenario: Grade gating — phrases tapped
 rating system. Grade gating restricts      Given the answer is revealed
 higher grades when hints are used."        And I have tapped 1 or more phrases
                                            Then the "All" grade button should be disabled
```

**The flow:**
1. Product specs capture the vision and requirements (prose)
2. Acceptance tests distill the specs into precise, testable scenarios (Gherkin)
3. E2E tests implement the scenarios as runnable code (Playwright/Detox)

**When requirements change:**
1. Update the product spec first (the intent)
2. Update or create acceptance test .feature files (the contract)
3. The failing acceptance tests drive the implementation change

### Product Spec File Naming

Use domain-based names in `docs/product-specs/`:
- `overview.md` — high-level product description, target user, core principles
- `data-model.md` — schemas, entities, relationships
- `screens.md` or individual screen files (e.g., `home-screen.md`, `session-screen.md`)
- `api-integration.md` — external API contracts
- `visual-design.md` — theme, typography, haptics (can also live in design-docs/)

For large specs (like a 400-line monolith), break them into domain files
during migration. Each file should be independently useful — an agent working
on the audio system should only need to load `audio-system.md`, not the
entire product spec.

### Acceptance Test File Naming

Use date-prefixed names in `docs/acceptance/`:
- `YYYY-MM-DD-feature-name.feature`
- e.g., `2026-03-07-listening-session.feature`

New features get new files with today's date. When requirements change,
either update the existing file or create a new dated file (if the
change is significant enough to track chronologically).

## AGENTS.md Template

Fill all `[PLACEHOLDER]` values. Aim for 80–100 lines.

```markdown
# AGENTS.md

## Project

- **Name:** [PROJECT NAME]
- **Description:** [One-line description]
- **Tech stack:** [e.g. TypeScript, React, Vite, Vitest, Playwright, Stryker]
- **Package manager:** [pnpm/npm/yarn/bun]
- **Source layout:**
  - `[dir]/` — [purpose]
  - `[dir]/` — [purpose]

## Feedback Commands

Run in this order. All must pass before committing.

1. `[Typecheck command]`
2. `[Lint command]`
3. `[Unit test command]`
4. `[Mutation command — only if detected]`
5. `[E2E command — only if detected]`

## Knowledge Base

Start here. Load deeper docs **only when working on the relevant domain.**

| Topic                      | Location                                                   |
|----------------------------|------------------------------------------------------------|
| Architecture overview      | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)               |
| Product specs              | [docs/product-specs/index.md](docs/product-specs/index.md) |
| Acceptance tests (Gherkin) | [docs/acceptance/index.md](docs/acceptance/index.md)       |
| Architectural decisions    | [docs/adrs/index.md](docs/adrs/index.md)                   |
| Design docs & principles   | [docs/design-docs/index.md](docs/design-docs/index.md)     |
| Active execution plans     | [docs/exec-plans/active/](docs/exec-plans/active/)         |
| Quality grades             | [docs/QUALITY.md](docs/QUALITY.md)                         |
| Lessons learned            | [docs/lessons.md](docs/lessons.md)                         |

> **Progressive disclosure:** Do NOT load all docs upfront. Read this file,
> then load the specific doc relevant to your current task.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Verify Before Done**: Run tests. Ask: "Would a staff engineer approve this?"
- **Spec Traceability**: Every behavior should trace to an acceptance test in docs/acceptance/.
- **Architecture First**: Consult docs/adrs/ before making structural decisions.

## Keeping Docs Current

**Stale docs are worse than no docs. Updating docs is part of completing any task.**

When your work affects any of these, update them as part of the same change:

| If you...                            | Then update...                                           |
|--------------------------------------|----------------------------------------------------------|
| Change a feature's behavior          | Product spec + acceptance test .feature file             |
| Add a new feature                    | Product spec + new .feature file + docs/acceptance/index.md |
| Make a structural decision           | Create a new ADR in docs/adrs/ + update index            |
| Change module boundaries / data flow | docs/ARCHITECTURE.md                                     |
| Fix a platform gotcha or learn a rule| docs/design-docs/ (e.g. platform-gotchas.md)             |
| Improve or degrade quality metrics   | docs/QUALITY.md                                          |
| Change the tech stack                | This file (AGENTS.md Project section)                    |
| Learn from a mistake or failed approach | docs/lessons.md                                       |

Do NOT defer doc updates to a separate task. The agent (or human) who makes
the change is the one who knows the context — capture it now.

## Maintaining Acceptance Tests

- When requirements change, update the relevant `.feature` file in `docs/acceptance/`
- New features MUST have acceptance scenarios before implementation begins
- Update `docs/acceptance/index.md` when adding/removing feature files
- Use `YYYY-MM-DD-feature-name.feature` naming (sorted chronologically)
- Acceptance tests are the contract — if the code doesn't match the .feature file,
  the code is wrong (unless the spec changed, in which case update the spec first)

## Maintaining Product Specs

- Product specs capture the vision and requirements in prose
- When the product evolves, update the relevant spec file in `docs/product-specs/`
- Break large specs into domain files — each independently loadable
- Specs should be readable without loading the entire knowledge base

## Maintaining Architectural Decisions

- When making structural decisions (new deps, pattern changes, tech choices),
  create `docs/adrs/YYYY-MM-DD-decision-name.md`
- ADRs are append-only — never edit old decisions, create new ones that supersede
- Update `docs/adrs/index.md` with the new entry

## Lessons

Two levels of lessons, serving different purposes:

- **`docs/lessons.md`** — persistent project knowledge. Things any agent needs to
  know: platform gotchas discovered the hard way, architectural mistakes to avoid,
  patterns that work well. This file is versioned and survives across all runs.
- **`.swarm/lessons.md`** — tactical swarm-specific lessons. Merge strategies,
  agent coordination tips, worktree issues. Managed by the swarm skill.

After any mistake or failed approach:
1. Ask: "Would this lesson help ANY future agent working on this project?"
   - Yes → add to `docs/lessons.md`
   - Only relevant to swarm operations → add to `.swarm/lessons.md`
2. Review `docs/lessons.md` at the start of each task

## Off-Limits

- [Project-specific: e.g. Don't modify CI without approval; don't change DB schema]
```

## After Creating

- Tell the user the structure is ready. Agents will read AGENTS.md as their entry point.
- You can output `<promise>AGENTS_CREATED</promise>` when done so scripts know
  to continue.

## Starter File Templates

### `docs/ARCHITECTURE.md`

```markdown
# [PROJECT NAME] — Architecture

## System Map

[Describe the high-level architecture. Include module boundaries,
data flow, and external dependencies. Keep this current.]

## Module Boundaries

| Module | Directory | Responsibility |
|--------|-----------|---------------|
| ... | ... | ... |
```

### `docs/product-specs/index.md`

```markdown
# Product Specs

Product requirements and vision, organized by domain.
These are the source of truth for WHAT the product does and WHY.

Update these when the product vision or requirements change.
Acceptance tests in `docs/acceptance/` are the testable distillation
of these specs.

| Spec File | Covers |
|-----------|--------|
| ... | ... |
```

### `docs/acceptance/index.md`

```markdown
# Acceptance Tests

Gherkin scenarios defining the behavioral contract of the application.
These are the testable distillation of product specs in `docs/product-specs/`.

Maintained as `.feature` files, date-named and sorted chronologically.

| Date | Feature File | Covers |
|------|-------------|--------|
| ... | ... | ... |

## Relationship to Product Specs

Product specs (prose) → Acceptance tests (Gherkin) → E2E tests (runnable)

When requirements change:
1. Update the product spec (the intent)
2. Update or create the .feature file (the contract)
3. Failing acceptance tests drive the implementation change
```

### `docs/adrs/index.md`

```markdown
# Architectural Decision Records

Decisions are append-only. Never edit old ADRs — supersede with new ones.
Named `YYYY-MM-DD-short-description.md` and sorted chronologically.

| Date | Decision | Status |
|------|----------|--------|
| ... | ... | Accepted |
```

### `docs/design-docs/core-beliefs.md`

```markdown
# Core Beliefs

Operating principles for agent-first development in this project.

1. **Repository is the system of record** — anything not in the repo
   doesn't exist for agents
2. **Progressive disclosure** — start with AGENTS.md, load deeper
   docs only when needed
3. **Enforce mechanically** — prefer linters and tests over documentation
   for enforcing rules
4. **Stale docs are actively harmful** — keep docs current or delete them
5. **Docs are part of the change** — updating docs is not a separate task,
   it's part of completing the work
```

### `docs/QUALITY.md`

```markdown
# Quality Grades

Grade each domain/layer on a scale. Update after major changes.

| Domain | Grade | Notes |
|--------|-------|-------|
| ... | ... | ... |

Grading scale:
- **A** — Well tested, clean architecture, documented
- **B** — Adequate tests, minor debt, mostly documented
- **C** — Gaps in coverage, some debt, docs may be stale
- **D** — Significant gaps, needs attention
- **F** — Untested, undocumented, high risk
```

### `docs/lessons.md`

```markdown
# Lessons Learned

Persistent project knowledge. Things any agent (or human) needs to know.
Updated whenever a mistake is made, a gotcha is discovered, or a pattern proves
effective. Review this file at the start of each task.

> **Rule of thumb:** If this lesson would save a future agent from making
> the same mistake, it belongs here. If it's only about swarm coordination
> or merge strategy, it goes in `.swarm/lessons.md` instead.

## Platform & Framework

- [e.g. "NativeWind v4: never use @tailwind base — it breaks Pressable styles"]
- [e.g. "Detox on Fabric: testID alone doesn't work, must add nativeID too"]

## Architecture

- [e.g. "Keep all Gemini calls in a single service file — spreading them causes inconsistent error handling"]

## Testing

- [e.g. "Always disable Detox synchronization for async operations"]

## Process

- [e.g. "When breaking up a monolith, move tests first — they tell you what's actually coupled"]
```
