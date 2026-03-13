---
name: agent-first-repo
description: >-
  Structure a repository and its documentation so AI coding agents can work effectively.
  Covers knowledge hierarchy, progressive disclosure, mechanical enforcement of architecture,
  and entropy management. Use when setting up a new project for agent-first development,
  refactoring a repo to be more agent-friendly, designing documentation structure for AI
  consumption, or optimizing an existing codebase for agent throughput. Triggers on: "agent-first",
  "make repo agent-friendly", "agent legibility", "optimize for AI agents", "repo structure
  for agents", "agent-first development", "harness engineering", "codex workflow".
---

# Agent-First Repository Design

Patterns for structuring a repository so AI coding agents can do effective, autonomous work.
Based on OpenAI's harness engineering approach: https://openai.com/index/harness-engineering/

The core insight: **if the agent can't see it in the repo, it doesn't exist.** Knowledge in
Slack, Google Docs, or people's heads is invisible to agents. The repository must be the
single source of truth.

## The Knowledge Hierarchy

A well-structured agent-first repo follows a layered documentation architecture:

```
AGENTS.md                    ~100 lines — table of contents, dev commands
ARCHITECTURE.md              codemap with boundaries and invariants
docs/
├── design-docs/
│   ├── index.md             catalogue of all design docs with status
│   ├── core-beliefs.md      agent-first operating principles
│   └── [feature-name].md    individual design documents
├── exec-plans/
│   ├── active/              in-progress execution plans
│   ├── completed/           finished plans (kept for context)
│   └── tech-debt-tracker.md known debt, prioritized
├── product-specs/
│   ├── index.md             catalogue of product specs
│   └── [feature-name].md    individual specs with acceptance criteria
├── references/
│   ├── [library]-llms.txt   LLM-friendly reference docs for key deps
│   └── [topic].md           reference material agents may need
├── generated/
│   └── db-schema.md         auto-generated from source of truth
├── DESIGN.md                design system and patterns
├── FRONTEND.md              frontend conventions
├── PLANS.md                 current priorities and roadmap
├── QUALITY_SCORE.md         quality grades per domain/layer
├── RELIABILITY.md           uptime, error budgets, SLOs
└── SECURITY.md              security model and boundaries
```

Not every project needs all of this. Start with AGENTS.md + ARCHITECTURE.md and grow
the `docs/` tree as the project demands it.

## The Three Pillars

### 1. Agent Legibility

Optimize the codebase for the agent's ability to reason about it, not human aesthetics.

**Prefer boring, composable technology.** Technologies with stable APIs, good documentation,
and broad representation in training data are easier for agents to model. "Boring" is a
feature, not a limitation.

**Inline over opaque.** Sometimes reimplementing a small subset of functionality is better
than depending on an opaque library the agent can't reason about. If the agent can read,
test, and modify the code directly, it has more leverage than if it's calling into a black box.

**Structured over unstructured.** Typed boundaries, structured logging, schema-validated
configs. Everything the agent interacts with should be queryable and parseable.

Parse data at system boundaries into precise types — don't let raw/untyped data flow
deep into business logic. For the full treatment, see the `parse-dont-validate` skill.

**Everything in the repo.** Design decisions, architectural rationale, product context,
quality assessments — if it matters, it's a versioned markdown file checked into the repo.
The moment a Slack thread resolves an architectural question, the conclusion goes into a
design doc.

### 2. Progressive Disclosure

Agents should start with minimal context and drill deeper as needed. Don't dump everything
into one file or into the initial prompt.

See [references/progressive-disclosure.md](references/progressive-disclosure.md) for the
full pattern, including directory structure, indexing, and cross-linking strategies.

### 3. Mechanical Enforcement

Encode architectural rules as linters and tests, not prose. Prose gets ignored; CI failures
don't. When documentation falls short, promote the rule into code.

See [references/mechanical-enforcement.md](references/mechanical-enforcement.md) for patterns
including custom linters with remediation messages, structural dependency tests, and layer
architecture enforcement.

## Entropy Management

Agent-generated code drifts. Agents replicate existing patterns — including bad ones. Without
active maintenance, the codebase accumulates inconsistency and technical debt faster than
a human-only codebase would.

See [references/entropy-management.md](references/entropy-management.md) for the golden
principles pattern, recurring cleanup cadence, and quality scoring approach.

## Companion Skills

This skill focuses on repository structure and documentation architecture. For specific
topics, load these companion skills:

| Topic | Skill | What It Covers |
|---|---|---|
| Writing AGENTS.md | `agents-md` | Structure, sections, anti-patterns for the entry point file |
| Architecture docs | `architecture-md` | Codemap with boundaries, invariants, cross-cutting concerns |
| Type-driven boundaries | `parse-dont-validate` | Parsing at boundaries, making illegal states unrepresentable |

## Quick Reference

| Need | Where to Look |
|---|---|
| Agent entry point file | `agents-md` skill |
| Architecture codemap | `architecture-md` skill |
| Layer docs for agents to drill into | [progressive-disclosure.md](references/progressive-disclosure.md) |
| Enforcing rules via linters/CI | [mechanical-enforcement.md](references/mechanical-enforcement.md) |
| Preventing codebase drift | [entropy-management.md](references/entropy-management.md) |
| Typing boundaries | `parse-dont-validate` skill |

## Workflow: Setting Up an Agent-First Repo

### For a new project:

1. Create `AGENTS.md` — dev commands, repo structure, boundaries (~100 lines)
2. Create `ARCHITECTURE.md` — bird's eye view, codemap, cross-cutting concerns
3. Set up `docs/` with at minimum `design-docs/index.md` and `core-beliefs.md`
4. Add mechanical enforcement — linter for dependency directions, structural tests
5. Establish quality scoring — grade each domain/layer, track in `QUALITY_SCORE.md`
6. Set up entropy management — recurring cleanup cadence, golden principles doc

### For an existing project:

1. Write `AGENTS.md` starting from what's in CI config and CONTRIBUTING.md
2. Write `ARCHITECTURE.md` by exploring the codebase (use the `architecture-md` skill)
3. Identify the top 3 architectural rules agents violate — encode as lints or tests
4. Move critical design context from Slack/docs/wikis into versioned repo files
5. Start a `QUALITY_SCORE.md` to track known gaps per module

## Anti-Patterns

- **Knowledge lives outside the repo** — Slack threads, Google Docs, wikis, Notion pages. If the agent can't `cat` it, it doesn't exist.
- **One giant AGENTS.md** — Monolithic instruction files crowd out actual task context. Use progressive disclosure.
- **Rules as prose only** — "Don't import from the API layer in workers" is ignored. A lint that fails CI is not.
- **No quality tracking** — Without explicit grades, drift is invisible until it's painful.
- **Manual cleanup Fridays** — Doesn't scale. Encode golden principles and automate scanning.
- **Opaque dependencies** — Libraries the agent can't read, test, or modify reduce leverage. Prefer transparent, in-repo code for critical paths.
