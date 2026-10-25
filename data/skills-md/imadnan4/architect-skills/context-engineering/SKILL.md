---
name: context-engineering
description: How to structure a repository so AI coding agents perform well. Use when setting up AGENTS.md/CLAUDE.md/.cursor rules, architecture docs, ADRs, context budgets, feature workflows, and reducing architecture drift.
when_to_use: |
  - setting up AGENTS.md / CLAUDE.md / .cursor rules
  - architecture docs, ADRs, context budgets for coding agents
  - reducing architecture drift in a repository
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Context Engineering & AI Coding Agent Architecture

LLMs are **context engines** — context quality determines architecture quality. Better context →
better reasoning → better code → fewer bugs. Never compensate for poor context with bigger prompts.
**Never let the AI discover or infer architecture — give it architecture.**

## Repository memory

A repository is memory. Every important decision must exist as documentation; knowledge that lives
only in conversation is already lost. Documentation is part of the source code.

## Standard layout

```
project/
├── AGENTS.md  README.md  CLAUDE.md  GEMINI.md
├── .architect/  docs/  apps/  packages/  infrastructure/  scripts/  tests/
```

Root should explain the project within five minutes.

## Agent instruction files

- **AGENTS.md** — universal; read first. Overview, architecture, workflow, standards, planning &
  review requirements. No implementation duplication.
- **CLAUDE.md** — planning, architecture, large refactors, repo navigation (reasoning-focused).
- **GEMINI.md** — large context, research, doc generation, architecture review.
- **Cursor rules** — formatting/naming/testing/imports/folders (no business rules).
- **Copilot instructions** — style, patterns, naming, comments, testing (no architectural decisions).

## Architecture folder & index

`docs/architecture/` holds Overview, System Diagram, ERD, API, Deployment, Scaling, Security,
Dependencies. `docs/architecture/index.md` links every doc and lists services, databases, queues,
caches, external APIs, events, workflows, ownership, dependencies. Architecture must be discoverable.

## ADRs

Every major decision becomes an ADR: Problem · Decision · Alternatives · Trade-offs · Consequences
· Owner · Date · Status. Reasoning should survive developers.

## Knowledge & context layers

Retrieve only the layer required:

| Layer | Scope |
|---|---|
| 1 | Current task |
| 2 | Current feature |
| 3 | Current service |
| 4 | Architecture |
| 5 | Entire repository |

Context budget: prioritize current task, relevant architecture, interfaces, tests, ADRs. Ignore
unrelated modules. **Quality > quantity.**

## Workflows

- **Feature:** Understand → Locate → Read Architecture → Read Domain → Read Interfaces → Plan →
  Implement → Test → Review. Never code immediately.
- **Discovery:** identify languages, frameworks, arch, package manager, DB, deploy, CI, testing,
  linting, security. Don't assume.
- **Local:** before editing a file, read imports/exports/interfaces/tests/usage/history.
- **Global:** before creating, search — does it exist / can it be reused / extended / simplified?
- **Planning:** goal, constraints, alternatives, chosen design, risks, plan, impact — then code.
- **Refactoring:** only when complexity/perf/maintenance/architecture measurably improve. Not "I
  prefer this."
- **Generated code** is a draft: review, validate, test, simplify. AI writes; engineers approve.

## Living docs & drift

- Context compression: each module summarizes purpose, responsibilities, public interfaces,
  dependencies, extension points (five-minute understanding).
- Architecture older than implementation is technical debt. On drift, update one side — never diverge.
- AI memory belongs in the repo, not conversation. Good naming reduces context needs.

## Review & health

- **PR review** verifies architecture, business rules, security, performance, testing, docs,
  breaking changes, observability, backward compatibility — every PR is an architecture review.
- **Health checklist:** README · Architecture · ADR · API · Tests · Docs · Examples · Changelog
  all updated. Knowledge stays synchronized.

## Architecture decision tree

```
Agent onboarding a repository
  ↓
AGENTS.md + architecture index exist? → NO → Create them
  ↓ YES
About to change code? → Read architecture → ADR → interfaces → tests
  ↓
Load only the context layer actually required
  ↓
Implement → Test → PR (architecture review)
```

## Anti-patterns

- ❌ Letting the AI discover / infer architecture
- ❌ Architecture docs older than implementation
- ❌ Knowledge living only in conversation
- ❌ Loading the entire repo as context
- ❌ Refactoring "because I prefer it"
- ❌ Treating generated code as truth · creating duplicate systems

## Architecture prompts

- Where is the architecture / ADR for this?
- What layer of context is actually needed?
- Does this already exist / can be reused?
- What module owns this?
- Does the doc match the implementation?
