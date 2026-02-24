---
name: shape-up
description: >
  Guided Shape Up workflow for taking projects from idea to working software.
  Orchestrates the /shaping and /breadboarding skills through a structured
  process: Frame, Shape, Breadboard, Slice, Build. Works for both greenfield
  (0-1) and existing projects. Use when: starting a new project or feature,
  planning a significant change to an existing codebase, user says "shape this",
  "let's shape", "shape up", or wants to go from idea to implementation with
  structured problem/solution separation. Proactively guides each phase and
  suggests next steps.
---

# Shape Up

Orchestrate the full Shape Up workflow by invoking `/shaping` and `/breadboarding`
at the right moments. Be proactive — after each step, explain what was accomplished
and suggest the next move.

## Prerequisites

Requires the `/shaping` and `/breadboarding` skills to be installed. If missing,
instruct the user to install them from https://github.com/rjs/shaping-skills

## Workflow Overview

```
Frame → Shape → Breadboard → Slice → Build
```

| Phase | Purpose | Sub-skill | Output |
|-------|---------|-----------|--------|
| **Frame** | Capture the "why" | `/shaping` | Problem + Outcome |
| **Shape** | Separate problem from solution, iterate | `/shaping` | R (requirements) + selected Shape |
| **Breadboard** | Map affordances and wiring | `/breadboarding` | Affordance tables + diagram |
| **Slice** | Cut into demoable increments | `/breadboarding` | V1..V9 vertical slices |
| **Build** | Implement slice by slice | — | Working software |

## Entry Point Detection

Determine the project type, then follow the appropriate path:

**New project (empty or new directory)?** → Start at Phase 1: Frame
**Existing project with code?** → Start at Phase 0: Map Current System

## Phase 0: Map Current System (Existing Projects Only)

Before shaping a change to an existing codebase, understand what exists.

1. Ask: "What workflow or area of the system does this change affect?"
2. Read the relevant code to understand the current implementation
3. Invoke `/breadboarding` to map the existing system as `CURRENT`:
   - Trace the affected workflow through the code
   - Produce affordance tables (UI + Code) for the current system
   - Generate a wiring diagram showing how it works today

This `CURRENT` breadboard becomes the baseline. Proposed shapes will modify it.

**After completing:** Present the CURRENT breadboard and say:
> "Here's how the current system works. Now let's frame what we want to change.
> What problem are you trying to solve, or what outcome do you want?"

## Phase 1: Frame

Capture source material and distill it into Problem and Outcome.

1. Ask the user to describe what they want (or paste stakeholder quotes, requests, etc.)
2. Invoke `/shaping` — capture the description as Source material
3. Distill into:
   - **Problem** — What's broken, what pain exists
   - **Outcome** — What success looks like
4. Write to `shaping.md` in `.claude/` (or project root for standalone projects)

**After completing:** Present the frame and say:
> "Here's the frame. Does this capture the problem and desired outcome?
> Once confirmed, we'll start extracting requirements and sketching a solution."

## Phase 2: Shape

Iterate on problem (R) and solution (shapes) until a shape is selected.

1. Invoke `/shaping`
2. Offer both entry points:
   - **Start from R** — extract requirements from the frame
   - **Start from S** — if user already has a solution in mind, capture it as Shape A
3. Run the shaping loop:

```
Extract R → Sketch shape(s) → Fit check → Spike unknowns → Iterate
```

### Proactive Guidance During Shaping

After extracting initial R and Shape A, immediately show the fit check:

> "Here's R x A — the fit between requirements and the proposed solution."

Then suggest based on what the fit check reveals:

| Fit check shows | Suggest |
|----------------|---------|
| Flagged unknowns (warning markers) | "A2 is flagged — want me to spike it?" |
| Requirements failing | "R3 fails because [reason]. Should we revise the shape or adjust R3?" |
| All green | "The shape looks solid. Ready to breadboard?" |
| Multiple viable shapes | "Both A and B pass. Want to compare with `show me A x R` vs `B x R`?" |

### Shorthand Commands

Teach the user these as you go:

| Command | What it does |
|---------|-------------|
| `show me R x A` | Fit check: requirements against shape A |
| `show me A x R` | Rotated fit check: shape A against requirements |
| `spike A2` | Investigate a specific part in depth |
| `add R that...` | Add a new requirement |
| `sketch shape B` | Propose an alternative approach |

**Phase complete when:** A shape is selected (passes fit check, unknowns resolved).

> "Shape [X] is selected and all requirements pass. Ready to breadboard?"

## Phase 3: Breadboard

Detail the selected shape into concrete affordances with wiring.

1. Invoke `/breadboarding`
2. For existing projects: breadboard the **mixture** — existing + new affordances wired together
3. For new projects: breadboard from the shape's parts
4. Produce:
   - Places table
   - UI Affordances table
   - Code Affordances table
   - Wiring diagram (Mermaid)

**After completing:**
> "The breadboard shows [N] UI affordances, [N] code affordances across [N] places.
> Ready to slice into vertical increments?"

## Phase 4: Slice

Cut the breadboard into demoable vertical slices.

1. Invoke `/breadboarding` slicing procedure
2. Identify V1 as the minimal demoable increment
3. Layer additional capabilities as V2..V9
4. For each slice, define:
   - Which affordances it includes
   - What mechanism it demonstrates
   - A concrete demo statement

**After completing:** Present the slice summary and say:
> "We have [N] slices. V1 demos '[demo statement]'. Want to start building V1?"

## Phase 5: Build

Implement each slice, verify it works, then move to the next.

For each slice:

1. Create an implementation plan (`V[N]-plan.md`)
2. Build the slice
3. Verify: run and test to confirm the demo works
4. Update the Big Picture document with completion status

**After each slice:**
> "V[N] is complete — [demo statement] is working. Ready for V[N+1]?"

## File Management

| File | Purpose | Location |
|------|---------|----------|
| `shaping.md` | Ground truth for R, shapes, fit checks | `.claude/` or project root |
| `spike-[topic].md` | Investigation findings | `.claude/` or project root |
| `big-picture.md` | High-level summary of entire feature | `.claude/` or project root |
| `V[N]-plan.md` | Per-slice implementation plans | `.claude/` or project root |

## Resuming a Session

When invoked with an existing `shaping.md`:

1. Read the shaping doc to understand current state
2. Invoke `/shaping` — it will detect the existing doc and show the fit check for the selected shape
3. Identify what needs attention (unsolved requirements, pending slices)
4. Suggest the next action:
   - If shaping: "R4 is still undecided — want to discuss?"
   - If breadboarded: "Ready to slice?"
   - If sliced: "V3 is next — want to build it?"
   - If building: "V2 is complete. V3 demos '[statement]' — ready?"
