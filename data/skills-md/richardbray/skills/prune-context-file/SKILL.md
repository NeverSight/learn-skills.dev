---
name: prune-context-file
description: Audit and prune bloated CLAUDE.md or AGENTS.md context files using evidence-based criteria from research on what actually helps coding agents. Use when a user asks to trim, audit, review, or improve their CLAUDE.md, AGENTS.md, or any repository context file for AI coding agents.
---

# Prune Context File

Audit and prune a CLAUDE.md or AGENTS.md file using findings from Gloaguen et al. (2025), the first rigorous study of whether context files improve coding agent performance.

## Evidence Base (key findings)

- **LLM-generated context files reduce performance** by 0.5–2% and increase cost 20%+. Never suggest auto-generating a context file.
- **Developer-written files marginally help** (+4% avg) — except for Claude Code, which showed no benefit from developer-written files either.
- **Codebase overviews don't work.** Agents find relevant files at the same speed with or without directory listings and project structure sections.
- **Context files are redundant with existing docs.** They only help when a repo has *no other documentation at all*.
- **Tooling instructions are reliably followed.** Naming a specific tool (e.g. `uv`, `pytest`, a repo CLI) increases its usage 1.6–2.5× vs. not naming it. This is the highest-value content.
- **Instructions cause more testing and exploration**, increasing steps and cost. Unnecessary requirements make tasks harder.

**Paper:** "Evaluating AGENTS.md" — Gloaguen et al., arxiv.org/abs/2602.11988

## The Decision Test

For every line or section, ask: *Would the agent write different code, run different commands, or make different assumptions without this?*

- **Yes, always relevant** → keep in root
- **Yes, but only when working in a specific subdirectory** → move to a nested `CLAUDE.md` in that directory
- **No / agent can discover it from the codebase** → cut it

## Classification

### Cut (low value)
- Directory listings and project structure sections
- Tech stack entries discoverable from `package.json` / `requirements.txt` / `go.mod` (e.g. React, Express, Tailwind, TypeScript)
- Links to docs files the agent can find itself
- General coding standards Claude already applies by default (e.g. "use descriptive variable names", "avoid magic numbers")
- Project overview prose beyond one sentence

### Keep in root (high value, always relevant)
- **Specific commands**: build, test, migrate, seed, lint — only if non-obvious or not already expressed as `package.json` / `Makefile` / config scripts the agent can read directly
- **Non-obvious tooling**: libraries or CLIs the agent wouldn't default to (e.g. Better Auth vs. Passport, `uv` vs. `pip`)
- **Architectural constraints** that would cause wrong assumptions if missing (e.g. non-standard i18n strategy, monorepo layout quirks)
- **Behavioral rules**: git workflow, PR requirements, test requirements — things that must be enforced, not inferred
- **Project-specific conventions** the agent can't infer from code alone

### Move to subdirectory `CLAUDE.md` (relevant only in specific contexts)
Root `CLAUDE.md` loads every session regardless of task — content irrelevant to most work has a standing token cost. Subdirectory `CLAUDE.md` files (e.g. `/web/CLAUDE.md`, `/api/CLAUDE.md`) load **on-demand only** when the agent reads files in that subtree.

Move content here when it only applies to a specific part of the codebase:
- Frontend-only conventions (component patterns, CSS framework rules, specific UI libraries)
- Backend-only conventions (ORM patterns, API design rules, service layer constraints)
- Any subsystem with its own tooling, patterns, or non-obvious constraints

## Process

1. **Read** the target context file
2. **Classify** each section and bullet against the Cut/Keep criteria above
3. **Present** a proposed diff: list what you'd remove and why (one line per item)
4. **Wait for approval** before rewriting
5. **Write** the pruned file, keeping the same structure but leaner

## Output Format

When presenting the proposed changes, group by action:

```
REMOVE
- [Section/item] — [one-line reason]

KEEP
- [Section/item] — [one-line reason]

REWRITE
- [Section/item] → [what it becomes] — [one-line reason]
```

Then ask for confirmation before applying.
