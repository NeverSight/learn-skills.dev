---
name: roadmap
description: Build evidence-backed software/product roadmaps from repo state, tickets, ideas, audit findings, or user goals — prioritize and sequence work across Now/Next/Later, milestones, dependencies, risks, and handoffs. Use when asked for a roadmap, feature roadmap, technical roadmap, release plan, milestone plan, backlog prioritization, sequencing, what to build next, or to turn improve/ideate/brainstorm/design-discussion outputs into an execution sequence. Not for implementing code or writing PR-level plans.
---

# Roadmap

Turn goals, candidate ideas, tickets, findings, and design docs into a high-level view of what's coming up.

A roadmap is **direction + prioritization + dependencies**. It says what capabilities, outcomes, or strategic tracks are likely next, why they matter, and what must happen before they are real. It is not a wish list, transcript, date promise, backlog dump, sprint plan, or implementation plan.

Default roadmap items are **outcomes/capabilities/features**. Use Agile-shaped nouns — epics, milestones, phases — only when they clarify sequencing or match the project's vocabulary. Features and epics describe what changes; milestones and phases describe ordering, gates, or release boundaries.

Stay one altitude above `writing-plans`: decide ordering, slices, gates, and handoffs; do not design unresolved internals or prescribe code. If one item needs product shaping, hand it to `brainstorm`. If technical choices are unresolved, hand it to `design-discussion`. If implementation is decided, hand it to `writing-plans`.

Never modify source code. Write only roadmap artifacts unless the user explicitly asks for downstream artifacts.

## Workflow

### Phase 1 — Set the altitude

Identify the roadmap's audience and horizon:

- **Audience:** maintainer, product owner, implementation agents, contributors, leadership, or future-you.
- **Horizon:** now/next/later by default; use releases, milestones, quarters, or dates only when the user gives a real cadence.
- **Scope:** whole repo, product area, feature family, technical debt, launch, migration, or agent execution stack.
- **Item vocabulary:** capability/feature by default; epic, milestone, phase, or initiative only when useful.
- **Output:** inline answer or durable artifact.

Ask only for missing decisions that would change the roadmap. Ask one question at a time and include your recommended default.

### Phase 2 — Recon

Gather source material before prioritizing:

- Read user-provided docs, issues, tickets, ideas, designs, plans, `README`, `AGENTS.md`/`CLAUDE.md`, `CONTEXT.md`, ADRs, and existing roadmaps.
- If the roadmap comes from `improve`, read the selected findings, rejected findings, and dependency notes.
- If the roadmap comes from ideation flow, read the relevant `docs/ideas/`, `docs/tickets/`, and `docs/agents/<slug>/` artifacts.
- If the roadmap is codebase-grounded and no candidates exist, do light read-only direction scouting: TODO/FIXME themes, half-built surfaces, documented-but-undelivered promises, surface asymmetries, high-churn areas, and adjacent capabilities the current architecture makes cheap.

Do not run mutating commands. If evidence is weak, mark the candidate as low confidence instead of padding it.

Default recon stops when you can name 5–10 plausible candidates with sources, or when the obvious source set is exhausted. If you find fewer than three candidates, say so and explain the evidence gap instead of wandering.

### Phase 3 — Normalize candidates

Convert every candidate into the same shape:

| Field | Meaning |
|-------|---------|
| Type | capability, feature, epic, milestone, phase, technical track, research/spike, migration, or decision |
| Outcome | What becomes true for users, maintainers, or the system |
| Evidence | Source doc, code `file:line`, ticket, finding, or user goal |
| First slice | The smallest coherent increment worth doing first |
| Dependency | What must happen before this can land or be useful |
| Risk | Delivery, product, technical, migration, or adoption risk |
| Confidence | HIGH / MED / LOW, based on evidence strength |
| Next handoff | `brainstorm`, `questions`, `research`, `design-discussion`, `writing-plans`, user decision, or `stop` |

Collapse duplicates. Split sprawling items. Reject generic suggestions that could apply to any repo.

### Phase 4 — Prioritize and sequence

Order by leverage, not volume:

1. Work that unlocks or de-risks later work.
2. High-value, low-effort items with strong evidence.
3. Learning spikes that retire major uncertainty before commitment.
4. Risky or expensive items only after prerequisites and validation gates exist.

Use **Now / Next / Later / Not now** unless the user gave a concrete release cadence. Dates without capacity evidence are false precision. Keep the output high-level enough that a maintainer can understand what's coming without reading implementation plans.

Every **Now** item needs a clear next move:

- Fuzzy product scope → `brainstorm`
- Missing facts or codebase unknowns → `questions` or `research`
- Unresolved technical choices → `design-discussion`
- Decided implementation → `writing-plans`
- Already tactical and small → ask whether to execute directly or capture it as a small `writing-plans` item
- No useful action → `stop`

### Phase 5 — Write and reconcile

For durable artifacts, choose the shape first:

- **Canonical project roadmap** — `./ROADMAP.md` at the project root. This is the default for a high-level view of what's coming up.
- **Scoped, historical, or alternate roadmap** — `./docs/roadmaps/<slug>.md` if `./docs/` exists, otherwise `./roadmaps/<slug>.md`.

Resolve the destination in this order:

1. User-specified path.
2. Existing project roadmap convention.
3. `./ROADMAP.md` for the canonical project roadmap.
4. Scoped roadmap path from the shape rules above.
5. Not obviously in a project? Ask.

Use `assets/roadmap-template.md`. Omit optional sections when they add no decision value. If the destination already exists, read it and update in place unless the user asks for a fresh roadmap. Preserve useful historical decisions; mark stale items as superseded instead of silently deleting context.

After writing, respond with the artifact path, the top Now items, and the next handoff to start.

## Invocation variants

- Bare `roadmap` → build a standard now/next/later roadmap from available inputs and light recon.
- `quick` → no broad scouting; use provided artifacts and obvious repo docs only.
- `deep` → fuller source review and candidate discovery before sequencing.
- `product`, `technical`, `migration`, `release`, `agent-execution` → focus the roadmap lens.
- `from improve` / `from tickets` / `from ideas` / `from plans` → prioritize those sources first.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Treating roadmap as a backlog dump | Cut aggressively; keep only high-level upcoming work and keep Not now explicit. |
| Inventing dates | Use Now/Next/Later unless cadence and capacity are real. |
| Letting generic ideas in | Require repo, artifact, user-goal, or code evidence. |
| Designing every item | Record the unresolved seam and route to the right next skill. |
| Writing PR-sized implementation plans | Stop at sequencing and hand off selected decided work to `writing-plans`. |
| Hiding uncertainty | Mark confidence and name the evidence gap. |

## Quality bar

Before finishing, check:

- The roadmap has a named audience, horizon, scope, and item vocabulary.
- Every Now/Next item is high-level enough to be roadmap material and has evidence plus a next handoff.
- Dependencies explain why the sequence matters.
- Not now records rejected or deferred work with one-line reasons.
- Dates, if present, are backed by an actual cadence or capacity assumption.
- The final answer says what was not reviewed or remains uncertain.
