---
name: setup-ux
description: Set up or refresh UX Skills for a new or existing project by capturing product intent, learning users and evidence, the design system, engineering environment, accessibility expectations, terminology, and consequential decisions. Use only when the user explicitly asks to set up, initialize, connect, learn, or refresh UX Skills/project context; do not activate during ordinary UX work.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
  ux-skills-invocation: "explicit"
---

# Setup UX

Learn enough for future UX work to start from intent and evidence instead of guesswork.

## Always

- **Context** — inspect what is already known before asking the user to repeat it. Use `.ux/INTENT.md` when product purpose or outcome can change the answer, and load only the additional project context the task needs.
- **User** — ground the work in the people affected, their goal, task, context, and available evidence. Do not invent user needs, behaviors, or personas.
- **Evidence** — keep known, inferred, assumed, unknown, and conflicted information distinct when the difference matters.
- **System** — prefer established product language, components, patterns, and rules before inventing new ones.
- **Clear** — lead with the useful point, use the minimum structure needed, and remove generic AI filler.
- **Trust** — never invent evidence, requirements, rationale, implementation status, or compliance.
- **Outcome** — for substantial multi-step work, keep intent active, use a small `.ux/STATE.md` only when continuity needs it, prioritize the highest-impact unresolved gap before polishing, and verify the actual experience against intent before declaring completion.

Do not recite these rules to the user unless one of them materially affects the answer.

Do not introduce research questions, personas, or discovery work when the user and task are already clear or the missing information would not materially change the work.

## Decide the setup path

Determine whether this is a new project or an existing one. Infer the path when the available project makes it obvious. Otherwise ask one short question: is this a new project/product, or are we working with an existing one?

Do not create a second setup skill. Both paths end in the same small `.ux/` context layer.

## New project: capture intent conversationally

There may be little useful project evidence yet, so begin with the user's idea in their own words. Ask only the next question whose answer could materially change what gets designed.

Useful areas to resolve, as needed, are:

- why this should exist and what should become better or newly possible;
- who is affected and what they need to accomplish;
- the essential experience or journey;
- current scope and explicit non-goals;
- constraints already known;
- what success means, if it has been defined;
- available evidence versus assumptions and unknowns.

Ask one or a small number of related questions at a time. Do not run a fixed questionnaire or require every heading to be complete before work can start.

Write `.ux/INTENT.md` first once the intent is concrete enough to guide decisions. Show the useful synthesis to the designer and let corrections override inference.

## Existing project: inspect before reconstructing intent

Explore the repository and connected sources before asking questions. Inspect what is available: README and product docs, existing user research, analytics and support evidence, package files, Storybook, components, tokens, design-system docs, Figma or other connected design sources, accessibility guidance, issue/PR templates, and existing decisions.

Reconstruct a draft of product intent from authoritative evidence, but keep **current behavior** separate from **intended outcome**. Code can prove that a flow exists; it usually cannot prove why the organization chose it.

Ask only about material gaps, conflicts, or intent that cannot be established reliably. Do not ask the user for information you can discover.

If an older `.ux/` directory contains only `CONTEXT.md`, `DESIGN-SYSTEM.md`, and `DECISIONS.md`, preserve those files and add `INTENT.md`; do not rewrite established context merely to match the new structure.

## Keep the context small

Create or refresh the smallest useful core:

```text
.ux/
├── INTENT.md
├── CONTEXT.md
├── DESIGN-SYSTEM.md
└── DECISIONS.md
```

Read `references/context-contract.md` for ownership, templates, evidence status, migration, intent updates, and when a project justifies splitting context into smaller files.

### INTENT.md

Owns why the product or capability exists, intended outcome, people affected, core task/experience, current scope and non-goals, material constraints, success when known, and material assumptions or unknowns.

Keep it short. It is a north star, not a PRD.

### CONTEXT.md

Owns the operating environment: observable product mechanics, major journeys, evidence locations, engineering stack and workflow, accessibility expectations, terminology, and stable project facts that help future UX work.

Do not duplicate intent just because both files mention the product.

### DESIGN-SYSTEM.md

Record the actual design-system sources and rules: Storybook, Figma, component packages, tokens, source-of-truth order, reuse expectations, and contribution path.

### DECISIONS.md

Keep a lightweight index of consequential UX or architecture decisions. If the project already has ADRs or another decision system, point to that instead of creating a competing one.

## Use progressive context

Do not create a research repository, persona library, journey catalog, or constraints folder during setup by default.

Split information into smaller files only when density, repeated use, or distinct ownership makes the split useful. Examples include `.ux/users/tasks.md`, `.ux/evidence/research.md`, or `.ux/constraints/accessibility.md` for projects that genuinely need them.

Future skills should load `INTENT.md` when product purpose, outcome, scope, or success can change the answer, then load only the additional context relevant to the task. Do not treat the whole `.ux/` directory as mandatory context for every request.

`.ux/STATE.md` is not part of setup and is not a fifth core context file. A future agent may create it only for substantial multi-step work when continuity would otherwise be lost. It is disposable working state, not durable product truth.

## Missing information is allowed

Do not block setup because something is unknown. Ask only when an answer would materially change future recommendations.

Never turn assumptions into facts. Label claims about people, evidence, requirements, decisions, intent, and material unknowns as known, inferred, assumed, unknown, or conflicted when the distinction matters; ordinary product mechanics do not need labels.

## Refresh intent carefully

Treat `INTENT.md` as stable, not frozen. Existing intent is the default and should survive routine design and implementation work.

Change it only when explicit human direction or authoritative evidence shows that the product's purpose, intended outcome, people, scope, non-goals, material constraints, or definition of success has actually changed. Make the smallest useful edit instead of regenerating the file.

A small clarification can be refined in place when it makes an already-established intent more precise without changing its meaning. A consequential change should preserve the decision or evidence that caused it in `DECISIONS.md` or the project's existing ADR/RFC system.

Never rewrite intent to rationalize the current implementation, remove an inconvenient constraint, or make completed work appear aligned after the fact. Agent inference alone does not override established intent.

## Finish usefully

Tell the designer what you learned, the few important gaps you found, and whether intent, user context, and the design system are sufficiently understood to start working.

Then stop. Do not turn setup into an audit or a discovery workshop.
