---
name: idea-to-plan
description: Turn a vague idea or feature request into a written, reviewable spec and implementation plan before any code is written. Use when the user says "I want to build X", "help me think through", "I have an idea", or hands over an underspecified request.
---

# Idea to Plan

Convert an underspecified request into (1) a one-paragraph problem statement, (2) a scoped spec, and (3) a phased implementation plan — each shown to the user for sign-off before moving on. Never jump to code from a vague prompt.

## When to use

- The request is a goal, not a specification ("build a dashboard", "add auth").
- Requirements, constraints, or success criteria are missing or implied.
- The user is exploring whether something is worth building.

Do **not** use this for well-specified tasks, bug fixes with a clear repro, or mechanical changes — those go straight to implementation.

## Procedure

### 1. Restate the problem (before asking anything)

Write one paragraph: *who* has *what* problem, *why now*, and what "solved" looks like. Show it. If you can't write it, you don't understand the request — that gap is your first question.

### 2. Ask only decision-changing questions

Batch 3–6 questions that would change the design if answered differently. Skip anything with a safe default — state the default instead and move on. Good targets:

- Scope boundaries (what is explicitly **out**)
- Hard constraints (stack, deadline, data, compliance)
- Success criteria (how we'll know it works)
- The one assumption that, if wrong, wastes the most work

### 3. Write the spec

```
## Problem
## Goals / Non-goals
## Constraints
## Approach (1–3 sentences)
## Open questions
```

Keep it under one screen. Show it, get explicit "yes" on Goals/Non-goals before planning.

### 4. Write the phased plan

Break into phases that each deliver something verifiable:

```
Phase 1: <smallest end-to-end slice that proves the approach> — verify by <X>
Phase 2: ...
```

Each phase: concrete deliverable, the files/areas touched, and how it's verified. Flag dependencies and the riskiest phase. Front-load risk.

### 5. Hand off

Output the spec + plan as the final artifact. Recommend the first phase and stop — implementation is a separate step the user triggers.

## Quality bar

- Problem statement fits in one paragraph and names a real user.
- Non-goals are explicit (a spec with no non-goals is not scoped).
- Every phase is independently verifiable.
- No question asked that has an obvious default.
- Zero code until the spec is signed off.

## Anti-patterns

- Asking 15 questions when 4 decide the design.
- "Phase 1: set up the project" with no verifiable outcome.
- Restating the user's prompt back as if it were a spec.
- Designing the gold-plated version before the wedge is agreed.
