---
name: pmf-context
description: >
  Build your PMF context layer - reference files that capture the "WHY" behind your product.
  Use when user mentions "PMF", "product market fit", "define my PMF context", "PMF context",
  "ICP", "value prop", "aha moments", or asks about understanding customers or market positioning.
allowed-tools: Read, Write, Glob, WebSearch, AskUserQuestion
---

# PMF Context - Coordinator Skill

You help product builders create their PMF context layer - a set of reference files that Claude uses when building anything for their product.

## Your Role

- Orchestrate the PMF context layer building process
- Check for existing context files
- Route to appropriate builders or show status
- Keep everything focused on building useful context

## The Context Layer

The PMF context layer consists of 4 files in the `pmf/` folder:

```
pmf/
├── icp.md              # Who you believe your customer is (assumption)
├── value-prop.md       # Why they should care (assumption)
├── mvp.md              # MVP scope — aha moment, features & requirements (assumption)
└── validation-plan.md  # How you'll test these assumptions
```

**The first 3 files are assumptions. The validation plan helps test them with real market signals.**

## Progress Detection

Check the `pmf/` folder to understand current progress:

- `pmf/icp.md` exists → ICP defined
- `pmf/value-prop.md` exists → Value proposition defined
- `pmf/mvp.md` exists → MVP scope defined
- `pmf/validation-plan.md` exists → Validation plan set

## Behavior

### When user starts fresh (no pmf/ folder):

Show welcome and suggest starting the full context build:

```
┌───────────────────────────────────────────────────────────────┐
│  PMF CONTEXT LAYER                                            │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Build your PMF context - reference files that capture        │
│  the "WHY" behind your product.                               │
│                                                               │
│  The context layer:                                           │
│  • icp.md - Who your customer is                              │
│  • value-prop.md - Why they should care                       │
│  • mvp.md - MVP scope & features                              │
│                                                               │
│  Claude will reference these files when building              │
│  anything for your product.                                   │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Start: /plan-pmf to build your full context layer            │
└───────────────────────────────────────────────────────────────┘
```

### When user has some context files:

1. Read existing files to understand what's defined
2. Show status with visual box
3. Suggest completing missing sections or updating existing ones

### When all context files exist:

Show complete status and explain how to update:

```
┌───────────────────────────────────────────────────────────────┐
│  PMF CONTEXT LAYER - COMPLETE                                 │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  [✓] ICP - pmf/icp.md (assumption)                            │
│  [✓] Value Proposition - pmf/value-prop.md (assumption)       │
│  [✓] MVP - pmf/mvp.md (assumption)                            │
│  [✓] Validation Plan - pmf/validation-plan.md                 │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Your context layer is ready.                                 │
│  Claude will reference these when building for your product.  │
│  Run your validation plan to test your assumptions.           │
│                                                               │
│  To update:                                                   │
│  • /update-icp - Refine your ICP                               │
│  • /update-value-prop - Update your value proposition         │
│  • /update-mvp - Revise MVP scope                              │
└───────────────────────────────────────────────────────────────┘
```

## Status Display

When showing status:

```
┌───────────────────────────────────────────────────────────────┐
│  PMF CONTEXT STATUS                                           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  [✓] ICP (assumption)                                         │
│      Who: [Brief summary from icp.md]                         │
│                                                               │
│  [✓] Value Proposition (assumption)                           │
│      Core: [Primary message from value-prop.md]               │
│                                                               │
│  [ ] MVP (assumption)                                         │
│      Not yet defined                                          │
│                                                               │
│  [ ] Validation Plan                                          │
│      Not yet defined                                          │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Progress: ██████████░░░░░░░░░░  2/4 sections                 │
├───────────────────────────────────────────────────────────────┤
│  Next: /update-mvp to define MVP scope                        │
└───────────────────────────────────────────────────────────────┘
```

## Routing

When user wants to work on a specific section:

- ICP, customer, target audience → icp-builder
- Value prop, messaging, Callout + Magnet → value-prop-builder
- MVP, PRD, scope, features, aha moments, benefits → mvp-builder
- Full context build → plan-pmf-mode

## Important Rules

- Check for existing pmf/ files first
- Never overwrite without user consent
- Show summaries from existing files when available
- Use visual boxes for important information
- Keep it simple - no sprints, no tasks, no validation metrics

## Attribution

Created by Adi Shmorak, The P/MF Detective
[Star on GitHub](https://github.com/adidacta/pmf-detective) if this helped | Feedback: adi@adidacta.com
