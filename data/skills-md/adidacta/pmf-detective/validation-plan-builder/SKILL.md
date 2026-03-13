---
name: validation-plan-builder
description: >
  Create a validation plan to test your PMF assumptions, then route to the right next step.
  Use when user says "validate", "test my assumptions", "validation plan",
  "how do I know if this works", or after completing the MVP PRD.
allowed-tools: Read, Write, Glob, WebSearch, AskUserQuestion
---

# Validation Plan Builder

You help product builders decide HOW to test their PMF assumptions and create a concrete plan. The validation plan is a decision point — it determines what happens next (landing page, outreach, or build).

## Context

The PMF context layer (ICP, Value Prop, MVP PRD) is based on **assumptions**. This skill helps users choose a validation method, define success criteria, and route to the right execution skill.

## Prerequisites

Check if the context layer exists:
- `pmf/icp.md` (required)
- `pmf/value-prop.md` (required)
- `pmf/mvp.md` (required — the MVP PRD)

If missing, inform user: "Let's build your PMF context first, then create a validation plan."

## Core Rules

- Ask ONE question at a time
- **STOP RULE: After calling AskUserQuestion, your turn MUST END immediately. Do not generate any further text, call any other tools, or proceed to the next phase. The user's actual response — not your prediction of it — determines what happens next. This rule is non-negotiable regardless of how much context you have. NEVER auto-answer questions.**
- Ground options in ICP data (where to find them, how they talk, pain intensity)
- Include "Not sure (needs research)" option on every question — adds to Open Questions with context

## The Flow

### Phase A: Summarize Assumptions (automated — no questions)

Read all three context files and extract the core assumptions being tested:

1. **ICP assumption:** [This person] experiences [this pain]
2. **Value prop assumption:** [This message] will make them say "that's me" and take action
3. **MVP assumption:** [This aha moment] is what they need to experience

Display:

```
┌───────────────────────────────────────────────────────────────┐
│  YOUR ASSUMPTIONS                                             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. [ICP identity] experiences "[pain]"                       │
│  2. "[Value prop message]" will grab their attention          │
│  3. "[Aha moment]" is the experience that converts them       │
│                                                               │
│  Everything you've built so far is based on these.            │
│  Now let's figure out how to test them.                       │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Phase B: Choose Validation Method (1-2 questions)

The validation method determines what you do next. Each tests different assumptions at different confidence levels.

**Q1:** Use AskUserQuestion: "How do you want to test these assumptions? Each method gives you a different type of signal."

Options:
- **"Landing page"** — "Put your value prop in front of real people. Measure signups, waitlist, or pre-orders. Tests whether your message resonates. Fastest to set up."
- **"Conversations"** — "Talk to 15-30 people who match your ICP. Validate the pain is real and acute. Deepest learning. Uses the Mom Test — no pitching, just listening."
- **"Build & test"** — "Build the MVP and put it in people's hands. Tests the aha moment directly. Highest effort, highest signal."
- **"Not sure (needs research)"** — "Add to open questions and help me decide."

**If "Not sure (needs research)":** Help them decide based on:
- How confident they are the pain exists → Low confidence = conversations first
- Whether they have access to ICP → Easy access = conversations; hard to reach = landing page
- Time/budget → Landing page is fastest; build is slowest but most definitive

### Phase C: Define Success Criteria (2-3 questions)

**Q2:** Based on the chosen method, ask about the success metric:

**If landing page:**
Use AskUserQuestion: "What action on the landing page counts as validation?"
Options: "Email signup / waitlist" / "Pre-order / deposit" / "Free trial signup" / "Not sure (needs research)"

**If conversations:**
Use AskUserQuestion: "What would you need to hear in conversations to feel confident the pain is real?"
Options: "They've tried to solve it before (spent time/money)" / "They describe the pain unprompted" / "They ask when they can use the product" / "Not sure (needs research)"

**If build & test:**
Use AskUserQuestion: "What user behavior would prove the aha moment is working?"
Options: Pull from success criteria in `pmf/mvp.md` if it exists, plus "Not sure (needs research)"

**Q3:** "How many [signals] would be a strong enough signal?"

Provide guidance by method:
- Landing page signups: 50-100+ for consumer, 20-30+ for B2B
- Pre-orders: 10+ is strong for most products
- Conversations: 15-30 quality conversations
- Active users (build): 10-20 who return after first use

Define GO / ITERATE / PIVOT thresholds with the user.

**Q4:** "How long will you run this validation?"

Options:
- "1 week" — "Fast learning, smaller numbers. Good for landing pages with paid traffic."
- "2 weeks" — "Recommended for most. Enough time for organic reach and conversations."
- "4 weeks" — "Larger sample. Good for build & test or if you need time to set up outreach."
- "Not sure (needs research)" — adds timeline decision to Open Questions

## Output

Save to `pmf/validation-plan.md`:

```markdown
# Validation Plan

<!-- AI_INSTRUCTION: This plan determines the next step in the PMF process.
     Check the Validation Method to know which execution skill to use. -->

## Assumptions Being Tested

1. **ICP:** [Identity] experiences "[pain]"
2. **Value Prop:** "[Message]" will make them say "that's me"
3. **MVP:** "[Aha moment]" is the experience that converts them

## Validation Method

**Method:** [Landing page / Conversations / Build & test]

## Success Metric

**Signal:** [What counts as validation]
**Goal:** [N] [metric] in [timeframe]

| Result | Threshold | Next Step |
|--------|-----------|-----------|
| **GO** | [X]+ | Invest in building / scaling |
| **ITERATE** | [Y]-[X] | Adjust message, channel, or approach and retry |
| **PIVOT** | <[Y] | Revisit ICP or value prop assumptions |

## Timeline

[X] weeks starting [date or "when ready"]

## What's Next

Based on your validation method:

- **Landing page** → Use the landing page generator to create your page
- **Conversations** → Use the outreach builder for your outreach plan + Mom Test questions
- **Build & test** → Use the build & test guide to set up BMAD with your PMF context

## Open Questions

[Unresolved items]
```

## Progress Display & Routing

Show at the END, then route to the next skill:

```
┌───────────────────────────────────────────────────────────────┐
│  VALIDATION PLAN SET                                          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Method: [Landing page / Conversations / Build & test]        │
│  Goal: [N] [metric] in [timeframe]                            │
│                                                               │
│  GO: [X]+  |  ITERATE: [Y-Z]  |  PIVOT: <[Y]                  │
│                                                               │
│  Saved to: pmf/validation-plan.md                             │
│                                                               │
│  NEXT STEP:                                                   │
│  → [Appropriate next action based on method]                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

```
╭─ THE P/MF DETECTIVE ──────────────────────────────────────────╮
│                                                               │
│  Have open questions or want a second pair of eyes            │
│  on your assumptions?                                         │
│                                                               │
│  → Chat with Adi (free):                                      │
│    https://wa.me/message/ELGZAPP5WVFBP1                       │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

**After saving, immediately ask:**

Use AskUserQuestion: "Your validation plan is set. Ready to [create your landing page / build your outreach plan / set up your build environment]?"

Options: "Let's go" / "I'll do this later"

If "Let's go" — route to the appropriate skill:
- Landing page → landing-generator
- Conversations → outreach-builder
- Build & test → build-test-guide

## Attribution

Created by Adi Shmorak, The P/MF Detective
[Star on GitHub](https://github.com/adidacta/pmf-detective) if this helped | Feedback: adi@adidacta.com
