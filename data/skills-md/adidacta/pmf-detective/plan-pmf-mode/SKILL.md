---
name: plan-pmf-mode
description: >
  Guide users through building their complete PMF context layer.
  Triggered by /plan-pmf command or when user wants to build full context.
allowed-tools: Read, Write, Glob, WebSearch, AskUserQuestion, Task
---

# PMF Plan Mode - Full Context Builder

You guide product builders through creating their complete PMF context layer in sequence: ICP → Value Proposition → MVP PRD → Validation Plan → Execute.

**Important:** The first 3 sections are **assumptions**. The validation plan decides how to test them, then routes to the right execution skill.

## How This Skill Works

This skill orchestrates the full flow by following each builder's process in sequence. Each builder skill (icp-builder, value-prop-builder, etc.) defines its own phases and questions — follow their SKILL.md instructions directly. This skill provides the sequencing, transitions, and progress tracking between sections.

## Your Role

- Walk users through all sections in order
- For each section, follow the corresponding builder skill's full flow
- One question at a time
- Save each section when complete
- Move to next section automatically

## The Flow

```
┌───────────────────────────────────────────────────────────────┐
│  PMF CONTEXT BUILDER                                          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Let's build your PMF context layer.                          │
│                                                               │
│  We'll work through 4 steps + execution:                      │
│  1. ICP — Who your customer is (assumption)                   │
│  2. Value Proposition — Why they should care (assumption)     │
│  3. MVP PRD — What to build & why (assumption)                │
│  4. Validation Plan — How you'll test these assumptions       │
│     │                                                         │
│     ├─→ Landing Page (if validating with signups)             │
│     ├─→ Outreach + Mom Test (if validating with talks)        │
│     └─→ Build with BMAD (if validating by building)           │
│                                                               │
│  Each section becomes a reference file Claude uses            │
│  when building anything for your product.                     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Section 1: ICP (icp-builder)

**Follow the full icp-builder flow.** Do NOT ask inline ICP questions here — the icp-builder defines all 5 phases:

1. Context & Broad Target (2 questions)
2. Pain Discovery with 5 Whys (3-6 questions)
3. Hypothesis Formation (2-3 questions, produces 3 hypotheses)
4. Parallel Research (automated — launches 3 research agents)
5. Compare & Select (user picks the strongest hypothesis)

When the icp-builder flow completes and saves `pmf/icp.md`, show the transition:

```
┌───────────────────────────────────────────────────────────────┐
│  ICP DEFINED                                                  │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Selected: [Hypothesis name]                                  │
│  Who: [Filtered persona summary]                              │
│  Pain: "[Emotional bedrock]"                                  │
│  Evidence: Pain [X]/5 │ Access [X]/5 │ Evidence [X]/5         │
│                                                               │
│  Saved to: pmf/icp.md                                         │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Progress: █████░░░░░░░░░░░░░░░  1/4 sections                 │
│  Next: Value Proposition                                      │
└───────────────────────────────────────────────────────────────┘
```

## Section 2: Value Proposition (value-prop-builder)

**Follow the full value-prop-builder flow.** Do NOT ask inline value prop questions here — the value-prop-builder defines all 5 phases:

1. Phase A: ICP Review (automated — reads pmf/icp.md)
2. Phase B: The Callout (2-3 questions)
3. Phase C: Craft the Magnet (2-3 questions)
4. Phase D: Generate Value Prop Options (1 question)
5. Phase E: CTA & Validation Goal (1 question)

When the value-prop-builder flow completes and saves `pmf/value-prop.md`, show the transition:

```
┌───────────────────────────────────────────────────────────────┐
│  VALUE PROPOSITION DEFINED                                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Callout: [Descriptor]                                        │
│  Magnet: [Desired future]                                     │
│  Message: [Selected value prop]                               │
│  CTA: [Action]                                                │
│                                                               │
│  Saved to: pmf/value-prop.md                                  │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Progress: ██████████░░░░░░░░░░  2/4 sections                 │
│  Next: MVP PRD                                                │
└───────────────────────────────────────────────────────────────┘
```

## Section 3: MVP (mvp-builder)

**Follow the full mvp-builder flow.** Do NOT ask inline questions here — the mvp-builder defines all 7 phases:

1. Phase A: Anchor the Promise (automated)
2. Phase B: Diverge — explore 3-5 aha moments
3. Phase C: Converge — pick the one
4. Phase D: Reverse-engineer the path step by step
5. Phase E: Features & Requirements per step
6. Phase F: Out of Scope
7. Phase G: Success Criteria

When the mvp-builder flow completes and saves `pmf/mvp.md`, show the transition:

```
┌───────────────────────────────────────────────────────────────┐
│  MVP PRD COMPLETE                                             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Aha Moment: [The key experience]                             │
│  Steps: [N] │ Features: [N] │ Requirements: [N]               │
│                                                               │
│  Saved to: pmf/mvp.md                                         │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Progress: ███████████████░░░░░  3/4 sections                 │
│  Next: Validation Plan                                        │
└───────────────────────────────────────────────────────────────┘
```

## Section 4: Validation Plan (validation-plan-builder)

**Follow the full validation-plan-builder flow.** It defines:

1. Phase A: Summarize assumptions (automated)
2. Phase B: Choose validation method (landing page / conversations / build & test)
3. Phase C: Define success criteria (GO / ITERATE / PIVOT thresholds)

When the validation-plan-builder flow completes and saves `pmf/validation-plan.md`, show the transition:

```
┌───────────────────────────────────────────────────────────────┐
│  VALIDATION PLAN SET                                          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Method: [Landing page / Conversations / Build & test]        │
│  Goal: [N] [metric] in [timeframe]                            │
│  GO: [X]+  │  ITERATE: [Y-Z]  │  PIVOT: <[Y]                  │
│                                                               │
│  Saved to: pmf/validation-plan.md                             │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│  Progress: ████████████████████  4/4 sections                 │
│  Next: Execute your validation plan                           │
└───────────────────────────────────────────────────────────────┘
```

## Section 5: Execute (routing — based on validation method)

The validation plan determines what happens next. Read `pmf/validation-plan.md` and follow the appropriate builder's flow based on the method:

**If Landing page:** Follow the landing-generator flow.
**If Conversations:** Follow the outreach-builder flow.
**If Build & test:** Follow the build-test-guide flow.

The validation-plan-builder already offers to route at the end. If the user chose "I'll do this later," remind them here:

```
┌───────────────────────────────────────────────────────────────┐
│  PMF CONTEXT LAYER COMPLETE                                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Your context layer is ready:                                 │
│                                                               │
│  [✓] pmf/icp.md              (assumption)                     │
│  [✓] pmf/value-prop.md       (assumption)                     │
│  [✓] pmf/mvp.md      (assumption — MVP PRD)                   │
│  [✓] pmf/validation-plan.md  (how you'll test)                │
│                                                               │
│  Your validation method: [method]                             │
│  Ready to execute? [route to appropriate skill]               │
│                                                               │
└───────────────────────────────────────────────────────────────┘

---
Created by Adi Shmorak, The P/MF Detective
For feedback: adi@adidacta.com
```

## Core Rules

- Ask ONE question at a time
- Wait for response before continuing
- Never skip sections without user consent
- Save each section before moving on
- Include "Not sure (needs research)" option on every question — adds to Open Questions with context
- Show progress after each section (not after each question)

## AskUserQuestion Guidelines

**IMPORTANT:** The header creates a visual divider that can disconnect the question from options.

To avoid confusion:
- Make questions **self-contained** - include all context in the question text itself
- Keep headers to **1 word max** or omit entirely
- Don't rely on text above the question to provide context

## Output Files

All outputs go to the `pmf/` folder:
- `pmf/icp.md` - Using template from `templates/outputs/icp.md`
- `pmf/value-prop.md` - Using template from `templates/outputs/value-prop.md`
- `pmf/mvp.md` - MVP PRD (features & requirements)
- `pmf/validation-plan.md` - Using template from `templates/outputs/validation-plan.md`

Execution outputs depend on validation method:
- `landing/` - Landing page (if landing page validation)
- `pmf/outreach-plan.md` - Outreach plan + Mom Test questions (if conversations)
- BMAD setup guidance (if build & test)

## Attribution

Created by Adi Shmorak, The P/MF Detective. For feedback: adi@adidacta.com
