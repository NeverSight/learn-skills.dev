---
name: build-test-guide
description: >
  Guide users to build and test their MVP using the BMAD Method with PMF context files.
  Use when user says "build it", "start building", "how do I build this",
  "BMAD", "implement", "code it", "create the app",
  or when the validation plan method is "build & test".
allowed-tools: Read, Glob, AskUserQuestion
---

# Build & Test Guide

You guide product builders on how to use the BMAD Method to build their MVP, using the PMF context files as the foundation.

## What is BMAD?

The **BMAD Method** (Breakthrough Method of Agile AI Driven Development) is an open-source AI-driven development framework. It provides specialized agents and structured workflows that take a product from requirements through architecture, stories, and implementation.

GitHub: https://github.com/bmad-code-org/BMAD-METHOD

**PMF Detective defines the WHY** (who's the customer, what's the promise, what's the aha moment, what to build).
**BMAD handles the HOW** (architecture, sprint planning, story implementation, code review).

## Prerequisites

Check that the PMF context layer exists:
- `pmf/icp.md` (required)
- `pmf/value-prop.md` (required)
- `pmf/mvp.md` (required — this is the MVP PRD with features & requirements)

If `pmf/mvp.md` is missing, inform the user:
```
To start building, you need your MVP PRD first — it defines what to build.

Missing: pmf/mvp.md

Use /plan-pmf to build your context layer, or tell me to
"define my MVP PRD" to start from the aha moment.
```

## The Flow

### Step 1: Review the MVP PRD (automated — no questions)

Read `pmf/mvp.md` and display a summary of what will be built:

```
┌───────────────────────────────────────────────────────────────┐
│  READY TO BUILD                                               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Aha Moment: [Name]                                           │
│  Steps: [N] steps in the Path to Aha                          │
│  Features: [N] features                                       │
│  Requirements: [N] requirements                               │
│                                                               │
│  Your MVP PRD (pmf/mvp.md) has everything                     │
│  you need to start building. Here's how.                      │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Step 2: Install BMAD

Check if BMAD is already installed by looking for a `.bmad/` directory or `bmad.config.*` file in the project root.

**If not installed:**

```
BMAD is not installed in this project yet.

To install, run:

  npx bmad-method install

When prompted:
- Select the "BMM" (BMad Method) module
- Choose your AI tool (Claude Code, Cursor, etc.)
- Install in your project root

After installation, come back and I'll help you
bridge your PMF context into BMAD's workflow.
```

Wait for the user to confirm installation is complete.

**If already installed:** Skip to Step 3.

### Step 3: Bridge PMF Context to BMAD (1 question)

BMAD has its own product brief and PRD workflows. The PMF context files contain the same information in a different format. The user needs to decide how to bridge them.

Use AskUserQuestion: "Your PMF context files already contain your product definition. How do you want to use them with BMAD?"

Options:
- **"Feed into BMAD's product brief"** — "Run /product-brief and reference pmf/ files as input. BMAD will restructure into its format."
- **"Skip to architecture"** — "Your MVP PRD already has features and requirements. Jump straight to /create-architecture and reference pmf/mvp.md."
- **"Quick path"** — "Use /quick-spec to analyze your PMF context and generate a tech spec with stories directly."

### Step 4: Provide the Prompt

Based on the user's choice, provide the exact prompt they should use with BMAD:

**If "Feed into product brief":**
```
Start BMAD with this prompt:

  /product-brief

When it asks about the product, tell it:

  "My product definition is in the pmf/ folder.
  Read pmf/icp.md for the customer profile,
  pmf/value-prop.md for the value proposition,
  and pmf/mvp.md for the MVP PRD with
  features and requirements."
```

**If "Skip to architecture":**
```
Start BMAD with:

  /create-architecture

Reference your MVP PRD:

  "My product requirements are defined in
  pmf/mvp.md — it has the features and
  high-level requirements for each step of the MVP.
  Use this as the basis for the architecture."
```

**If "Quick path":**
```
Start BMAD with:

  /quick-spec

Tell it:

  "Analyze my project and the pmf/ folder.
  pmf/mvp.md contains the MVP PRD with
  features and requirements. Generate a tech spec
  and stories from those requirements."
```

### Step 5: Remind About Scope

Display a final note:

```
┌───────────────────────────────────────────────────────────────┐
│  STAY IN SCOPE                                                │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Your MVP PRD defines what's IN and OUT of scope.             │
│  If BMAD suggests features not in pmf/mvp.md,                 │
│  check the "Out of Scope" section before adding them.         │
│                                                               │
│  The goal: deliver the aha moment, validate it,               │
│  then expand based on what you learn.                         │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Attribution

Created by Adi Shmorak, The P/MF Detective. For feedback: adi@adidacta.com

BMAD Method by BMad Code — https://github.com/bmad-code-org/BMAD-METHOD
