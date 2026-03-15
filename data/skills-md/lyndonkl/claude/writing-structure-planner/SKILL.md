---
name: writing-structure-planner
description: Use when planning, organizing, or diagramming the structure of a piece of writing. Invoke when user mentions outlining, organizing ideas, structure planning, article architecture, narrative flow, or needs help deciding how to arrange their material before drafting.
---

# Writing Structure Planner

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Structure Types Overview](#structure-types-overview)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill guides users through McPhee's structural diagramming method to plan writing architecture before drafting. It helps select from 8 structure types, create visual diagrams, and place gold-coin moments for reader engagement. Structure planning prevents disorganized writing and ensures material flows naturally.

## When to Use

Use this skill when:

- **Starting a new piece**: User has ideas/material but hasn't organized them yet
- **Restructuring a draft**: Existing piece feels disorganized or lacks flow
- **Choosing an approach**: User is unsure whether to use chronological, list, circular, etc.
- **Complex material**: User has many threads, perspectives, or data points to weave together
- **Outline creation**: User wants a roadmap before writing

Trigger phrases: "outline", "organize my ideas", "structure this", "how should I arrange", "plan the structure", "what order", "narrative architecture", "flow", "diagram my piece"

**Do NOT use for:**
- Revising existing prose (use `writing-revision`)
- Making messages memorable (use `writing-stickiness`)
- Final quality checks (use `writing-pre-publish-checklist`)

## Core Principles

1. **Structure arises from material**: Don't impose a structure - let the content suggest its natural organization
2. **Blueprint before building**: Always plan structure before drafting
3. **Invisible architecture**: Good structure is invisible to readers - they just experience flow
4. **Three options minimum**: Always sketch at least 3 structural options before choosing
5. **Gold-coin distribution**: Place reader rewards throughout, especially in the middle

## Workflow

Copy this checklist and track your progress:

```
Structure Planning:
- [ ] Step 1: Analyze material thoroughly
- [ ] Step 2: Explore structure options
- [ ] Step 3: Select and refine structure
```

**Before starting:** Review [resources/structure-types.md](resources/structure-types.md) for the 8 structure types, diagramming method, and selection criteria.

**IMPORTANT:** For analysis steps, output findings to analysis files in the current directory to ensure thorough coverage of all material. These analysis files remain in the project for your review.

**Step 1: Analyze material thoroughly**

Step 1.1: Gather and understand all material completely. Read everything the user has provided.

Step 1.2: Create analysis file `writer-structure-material-analysis.md` and output: ALL key points, anecdotes, data, quotes, and examples found in the material. Identify themes and patterns. Determine what's most important vs. supporting detail. Identify the natural organizing principle (time, space, importance, comparison). Note reader considerations (busy? engaged? unfamiliar? expert?).

Step 1.3: Present the material analysis to the user and confirm understanding is complete. Ask: "Did I miss any important material or themes?"

See [resources/structure-types.md - Gather Your Material](resources/structure-types.md#step-1-gather-your-material) for detailed guidance.

**Step 2: Explore structure options**

Step 2.1: Read the analysis file. Review all [8 Structure Types](resources/structure-types.md#structure-types) with examples.

Step 2.2: Create analysis file `writer-structure-options.md` and sketch 3 different structure options. For each option include: structure type name, diagram sketch, how user's material maps to it, pros and cons.

Step 2.3: Test each option against [Structure Selection Criteria](resources/structure-types.md#structure-selection-criteria). Present all 3 options to the user with your recommendation.

See [resources/structure-types.md - Sketch 3 Options](resources/structure-types.md#step-3-sketch-3-options) for detailed process.

**Step 3: Select and refine structure**

Step 3.1: Read the options file. Based on user's choice (or your recommendation if they defer), select the structure that best serves the material.

Step 3.2: Create the final annotated structure diagram. Map key moments and transitions. Identify where to place [gold-coin moments](resources/structure-types.md#gold-coin-placement-strategy) throughout (especially middle sections). Annotate with pacing and transition notes.

Step 3.3: Verify structure supports the through-line (promise -> delivery -> resonance). Test: Does this feel inevitable or forced? Present final annotated structure diagram for user review before drafting.

See [resources/structure-types.md - Select and Refine](resources/structure-types.md#step-5-select-and-refine) for detailed guidance.

**How to know if structure is working:**

If working: Readers won't notice it, they'll just experience flow and feel the piece is "well-organized."

If not working: Readers will feel lost, wonder "where is this going?", or abandon before the end.

Validate using [resources/evaluators/rubric_structure.json](resources/evaluators/rubric_structure.json). **Minimum standard**: Average score >= 3.5.

## Structure Types Overview

The 8 structure types available (see [resources/structure-types.md](resources/structure-types.md) for full details):

| Type | Best For |
|------|----------|
| List | Multiple independent points, how-to guides |
| Chronological | Narratives, historical accounts, processes |
| Circular/Cyclical | Hooking readers with drama, then providing context |
| Dual Profile | Character profiles, examining topic from multiple angles |
| Triple Profile | Complex characters in multiple contexts |
| Pyramid (Inverted) | News, executive summaries, busy readers |
| Parallel Narratives | Comparing/contrasting, multi-threaded stories |
| Custom Diagrams | Unique material that doesn't fit standard types |

## Guardrails

**Critical requirements:**

1. **Material-first**: Always understand the material before suggesting structure. Never impose a structure without understanding content.
2. **Three options**: Always generate at least 3 structural options. The second or third is often best.
3. **User collaboration**: Present options and let the user choose. Don't dictate structure.
4. **Gold-coin placement**: Every structure must include strategic placement of reader rewards, especially in the middle.
5. **Test the structure**: Ask "does this feel inevitable or forced?" before finalizing.

**Common pitfalls:**
- Defaulting to chronological when another structure serves better
- Front-loading all strong material in the opening
- Ignoring the "saggy middle" problem
- Imposing structure without understanding material
- Skipping the 3-option comparison step

## Quick Reference

**Key resources:**
- **[resources/structure-types.md](resources/structure-types.md)**: All 8 structure types, diagramming method, gold-coin strategy, selection criteria
- **[resources/evaluators/rubric_structure.json](resources/evaluators/rubric_structure.json)**: Quality scoring criteria

**Inputs required:**
- User's material, ideas, or topic description
- Target audience (if known)
- Any constraints (length, format, publication)

**Outputs produced:**
- Material analysis document
- 3 structure options with pros/cons
- Final annotated structure diagram with gold-coin placement
- Recommended writing order
