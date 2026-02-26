---
name: product-brainstorm
description: Guided requirements exploration through structured dialogue. Use when the user says "brainstorm", "explore this idea", "help me think through", or when requirements are fuzzy and need clarification before writing specs.
allowed-tools: ["Read", "Glob", "Grep", "AskUserQuestion", "Write"]
argument-hint: "[topic]"
---

# /product-brainstorm — Requirements Exploration

Guided dialogue to explore what to build before committing to specs. Helps clarify fuzzy ideas into concrete, actionable requirements.

## When to Use

- User says "brainstorm", "explore this idea", "help me think through"
- Requirements are fuzzy or incomplete
- Multiple approaches seem viable and need evaluation
- Before writing a PRD or tech spec

## Process

### Step 1: Understand the Problem

If `$ARGUMENTS` provides a topic, use it as the starting point. Otherwise, ask probing questions to understand the core need:
- **What problem are you solving?** (not what feature — the underlying problem)
- **Who is this for?** (specific user type, not "everyone")
- **What does success look like?** (measurable outcome)
- **What have you tried or considered already?**

Use AskUserQuestion to gather answers. Don't overwhelm — start with the most important question and build from there.

### Step 2: Surface Assumptions & Constraints

Identify hidden assumptions:
- What are you assuming about your users?
- What technical constraints exist? (platform, stack, timeline)
- What's explicitly out of scope?
- Are there dependencies on other features or teams?

### Step 3: Explore Approaches

Propose 2-3 distinct approaches with clear tradeoffs:

For each approach:
- **What it is** (1-2 sentences)
- **Pros** (what you gain)
- **Cons** (what you give up or risk)
- **Effort** (rough sense: small/medium/large)

Use AskUserQuestion to let the user choose or combine approaches.

### Step 4: Define Edges

For the chosen approach, explore edge cases:
- What happens when there's no data? (empty states)
- What happens when things fail? (error states)
- What are the boundary conditions? (limits, extremes)
- How does this interact with existing features?

### Step 5: Capture Output

Write a brainstorm summary to `docs/brainstorms/YYYY-MM-DD-<name>.md`:

```markdown
# Brainstorm: [Topic]
**Date:** YYYY-MM-DD

## Problem
[The core problem being solved]

## Target User
[Who this is for]

## Chosen Approach
[The selected approach and why]

## Key Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Edge Cases & Constraints
- [Edge case or constraint]

## Open Questions
- [Anything still unresolved]

## Next Steps
- [ ] Write PRD (`/product-prd`)
- [ ] Write tech spec (`/product-tech-spec`)
```

## Output

Save to: `docs/brainstorms/YYYY-MM-DD-<name>.md`

## Next Steps

- Ready to formalize? → `/product-prd`
- Know the architecture? → `/product-tech-spec`
- Ready to plan tasks? → `/engineer-plan`
