---
name: create-agents
description: Write, audit, and improve AGENTS.md files for AI coding agents. Use when creating or improving agent context for a codebase.
---

Include only what genuinely helps, ruthlessly cut everything else. These principles apply regardless of language or framework — C#, Python, TypeScript all follow the same rules.

## Core Principles

- **Minimum viable requirements.** Ask of each line: "Does this earn its cost on nearly every session?" If not, cut it. Every line loads on every session — brevity has direct cost benefits.
- **Two failure modes.** (1) *Length* — as instruction count grows, compliance degrades uniformly, not just for new instructions. (2) *Task-irrelevant requirements* — correct instructions not needed for the current task still get followed, increasing cost and reducing success.
- **Don't send an LLM to do a linter's job.** Style guidelines add instructions and irrelevant context. Use actual linters, wired to hooks if the harness supports it.
- **Never auto-generate.** Auto-generated files are stuffed with documentation the agent can read directly. Write by hand.
- **Architecture and overview sections have weak evidence** in root files. Exception: scoped sub-files can carry richer context — they only load when the agent is already working in that area.

## Single File vs. Hierarchical System

**Single root file** for simple projects: one app, one language, one team. Keep it under 100 lines.

**Hierarchical system** for monorepos, large codebases, or multiple apps/packages/services. The harness auto-loads AGENTS.md files as the agent navigates — `apps/web/AGENTS.md` only loads when the agent works there.

### Hierarchical Rules

**Place files at semantic boundaries** — where responsibilities shift or contracts matter. Not in every directory.

**Least Common Ancestor for shared knowledge** — shared facts belong in the shallowest file covering all relevant paths. Never duplicate across siblings.

**Downlink from parent to children** — reference child files so the agent can follow the hierarchy:

```
## Sub-areas
- `packages/ui/AGENTS.md` — component library conventions
- `apps/api/AGENTS.md` — API server, auth, database access
```

**Build leaf-first** — write deepest files first. Parents summarize children's AGENTS.md files, not raw code.

**Scoped files can be richer** — entry points, invariants, and pitfalls are appropriate in a file that only loads for one service.

## Writing a New AGENTS.md

```markdown
# Project or Area Name

One sentence: what it does and why it exists.

## Stack
Tech stack. Package manager or build tool (be explicit — agents assume defaults).
Path aliases if non-standard. Infrastructure if non-obvious (DB, cache, queue).
Directory tree only if ownership boundaries aren't obvious. 1-2 levels max.

## Development
Verification commands only: typecheck, lint, test. What to run before finishing.
Skip inferrable commands. Include non-obvious ones whose names don't reveal purpose
(e.g. `cf-typegen`, `db:migrate`, `dotnet ef database update`).

## Conventions
Only things the agent can't infer from reading the code.
No style rules — use a linter.
```

A Reference Docs section is fine — only add a pointer if the agent genuinely needs to read it before working in that area.

## Auditing an Existing AGENTS.md

Measure first: total lines, distinct instructions, style rules, overview sections. Classify each: essential and universal (keep), task-specific or architectural (cut or demote to pointer), style/lint rule (remove), redundant or stale (remove).

For hierarchical systems: check whether root content belongs in a scoped sub-file, and whether sub-files duplicate knowledge that belongs at their LCA.

Present before/after line counts, what was cut and why, and the complete rewritten file.

## Maintenance

On significant changes, update affected AGENTS.md files leaf-first. A CI agent that detects changed files and proposes updates is worth building.

## Anti-Patterns to Flag

**Command dump** — inferrable commands like `dev`, `build`, `start` listed in full.

**Deep tree** — directory structures more than 2 levels deep. Replace with a sentence.

**Architecture tour** — system overviews in a root file. One sentence of purpose, or push into a scoped sub-file.

**Style guide** — formatting rules. Use a linter.

**Code museum** — large inline snippets. Use `file:line` references.

**Hotfix graveyard** — accumulated one-off corrections. Delete them.

**Auto-generated blob** — output from auto-init commands. Rewrite from scratch.

**Stale reference** — outdated paths or commands. Update or remove.

**Duplicated siblings** — the same fact in two sub-files. Hoist to their LCA.
