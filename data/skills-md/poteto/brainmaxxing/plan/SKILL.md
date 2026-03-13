---
name: plan
description: >-
  Break down medium-to-large tasks into phased plans in brain/plans/. Planning only — does not
  implement. Use for new features, multi-file refactors, or architectural changes — not small
  fixes. Triggers: "plan this", "break this down".
---

# Plan

Produce implementation plans grounded in project principles. Write plans to `brain/plans/`. **Do NOT implement anything — the plan is the deliverable.**

**Use Tasks to track progress.** Create a task for each step (TaskCreate), mark each in_progress when starting and completed when done (TaskUpdate). Check TaskList after completing each step.

## Step 0 — Triage Complexity

Before running the full planning workflow, assess whether this task actually needs a plan:

**Trivially small (1–2 files, obvious approach):**
Tell the user this task doesn't need a plan and suggest implementing directly without the plan skill. **Stop here — do not implement.**

**Needs planning (proceed to Step 1):**
- The change spans 3+ files or introduces new architecture
- There are multiple valid approaches and the user should weigh in
- The task has unclear scope or cross-cutting concerns
- The user explicitly asks for a plan

## Step 1 — Load Principles

Read `brain/principles.md`. Follow every `[[wikilink]]` and read each linked principle file. These principles govern all plan decisions — refer back to them throughout.

**Do NOT skip this. Do NOT use memorized principle content — always read fresh.**

## Step 2 — Define Scope and Constraints

Use `AskUserQuestion` to resolve ambiguity before exploring the codebase:

- What is in scope vs explicitly out of scope?
- Are there constraints (dependencies, platform requirements, existing patterns to preserve)?
- What does "done" look like?

Frame questions with concrete options. If the request is already clear, confirm scope boundaries briefly and move on.

## Step 3 — Explore Context with Subagents

**Always** delegate exploration to subagents via the `Task` tool. Never do large-scale codebase exploration in the main context.

Spawn exploration agents (subagent_type: `Explore`) to:
- Read existing code in affected areas
- Identify patterns, conventions, and dependencies
- Map architecture relevant to the change
- Find tests, types, and related infrastructure

Run multiple agents in parallel when investigating independent areas.

## Step 4 — Gather Domain Skills

Check installed skills (`.agents/skills/`, `.claude/skills/`) for any that match the plan's domain. **Invoke matched skills** — read their output and incorporate domain guidance into the plan.

If the plan touches a domain **not covered** by installed skills, use `find-skills` to search for a relevant skill. If one is found, install it (project-local) and incorporate its guidance. Note what was installed so the user can see it. After the plan is written, delete any one-off skills that won't be needed again.

## Step 5 — Write the Plan

Create the plan directory and files manually:

1. Create `brain/plans/NN-slug-name/overview.md` (or a single file for simple plans)
2. Create phase files as needed
3. Update `brain/plans/index.md` with a link to the new plan

### Phase sizing

- **1 function/type + tests** per phase, or **1 bug fix** — not "one file" or "one component" (too variable)
- **Max 2-3 files touched** per phase when possible
- **Prefer 8-10 small phases** over 3-4 large ones — small phases keep future options open
- If a phase lists >5 test cases or >3 functions, split it

For small plans, a single file at `brain/plans/NN-plan-name.md` is fine.

For plans with 3+ phases, create a directory:

```
brain/plans/42-mvp/
├── overview.md
├── phase-1-scaffold.md
├── phase-2-layout.md
├── phase-3-drawing.md
└── testing.md
```

Non-phase files (like `testing.md`) are fine alongside phases.

### Overview file

Must include:
- **Context** — what problem this solves and why
- **Scope** — what's included, what's explicitly excluded
- **Constraints** — technical, platform, dependency, or pattern constraints
- **Applicable skills** — domain skills from Step 4 (list by name so implementers invoke them)
- **Phases** — ordered links to phase files: `[[plans/42-mvp/phase-1-scaffold]]`
- **Verification** — project-level verification commands

### Phase files

Each phase file must include:
- Back-link: `Back to [[plans/42-mvp/overview]]`
- **Goal** — what this phase accomplishes
- **Changes** — which files are affected and what changes, described at a high level
- **Data structures** — name the key types/schemas before logic, but a one-line sketch is enough — don't write full definitions
- **Verification** — static and runtime checks for this phase (see Step 6)

**Keep plans high-level.** Describe *what* and *why*, not *how* at the code level. A phase should read like a brief to a senior engineer: goals, boundaries, key types, and verification — not code snippets or pseudocode.

Order phases per the sequencing principle: infrastructure and shared types first, features after. Each phase should be independently shippable.

**Skill changes:** If a phase involves creating or updating a skill (any file in `.claude/skills/` or `.agents/skills/`), the phase must instruct the implementer to use the `skill-creator` skill during that phase.

### Redesign check

For changes touching existing code, apply redesign-from-first-principles:
> "If we were building this from scratch with this requirement, what would we build?"

Don't bolt changes onto existing designs — redesign holistically.

### Alternatives check

For architectural decisions, briefly sketch 2-3 approaches in the overview's Constraints section. State which was chosen and why. This prevents premature commitment and documents the design space explored.

## Step 6 — Verification Strategy

Every phase **must** have a verification section with both:

### Static
- Type checking passes
- Linting passes
- Code follows project conventions
- Tests written and passing

### Runtime
- What to test manually (launch the app, exercise the feature path)
- What automated tests to write (unit, integration, e2e)
- Edge cases to cover
- For UI: visual verification via screenshot

Per prove-it-works: "it compiles" is not verification. Every phase must describe how to **prove** the change works.

## Step 7 — Update Plans Index

Update `brain/plans/index.md` with a wikilink to the new plan's overview.

Do NOT edit `brain/index.md` — the auto-index hook maintains it automatically.

## Step 8 — Present to User

Summarize the plan: list the phases, scope boundaries, applicable skills, and verification approach. Ask the user to review the plan files in `brain/plans/`.

**Stop here.** Do not begin implementation. The user decides when and how to execute the plan.
