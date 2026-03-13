---
name: writing-stickiness
description: Use when making messages more memorable or persuasive using the SUCCESs framework. Invoke when user mentions stickiness, making ideas stick, memorable messaging, persuasion, the Heath brothers, or wants to apply Simple, Unexpected, Concrete, Credible, Emotional, Stories principles.
---

# Writing Stickiness Enhancement

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [SUCCESs Framework Overview](#success-framework-overview)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill applies the Heath brothers' SUCCESs model (Simple, Unexpected, Concrete, Credible, Emotional, Stories) to make messages memorable and persuasive. It provides systematic analysis against all 6 principles, targeted improvements, and scoring using the stickiness scorecard (0-18 points).

## When to Use

Use this skill when:

- **Making messages memorable**: User wants their message to stick in readers' minds
- **Improving persuasion**: Message needs to be more compelling or convincing
- **Presentation prep**: Making slides or talk content more impactful
- **Marketing or messaging**: Crafting taglines, pitches, or campaigns
- **Any writing needing impact**: User wants writing to resonate beyond just being clear

Trigger phrases: "make it stick", "more memorable", "more persuasive", "more impactful", "stickiness", "make people care", "make it compelling", "SUCCESs", "Heath brothers", "punch it up"

**Do NOT use for:**
- Planning structure (use `writing-structure-planner`)
- General prose revision (use `writing-revision`)
- Final quality checks (use `writing-pre-publish-checklist`)

## Core Principles

1. **Six dimensions of stickiness**: Simple, Unexpected, Concrete, Credible, Emotional, Stories
2. **Diagnose before treating**: Score current stickiness first, then improve weakest areas
3. **Not all principles are equal**: Some matter more for certain contexts - prioritize accordingly
4. **Concrete beats abstract**: Brains think in images, not abstractions
5. **Individuals beat statistics**: One person's story moves people more than millions in data

## Workflow

Copy this checklist and track your progress:

```
Stickiness Enhancement:
- [ ] Step 1: Analyze against SUCCESs framework
- [ ] Step 2: Improve weak principles
- [ ] Step 3: Score and refine
```

**Before starting:** Review [resources/success-model.md](resources/success-model.md) for the complete SUCCESs framework with all 6 principles, stickiness scorecard, and before/after examples.

**IMPORTANT:** Analyze the ENTIRE document first and output findings to an analysis file in the current directory, then read that file to make improvements. This ensures complete coverage.

**Step 1: Analyze against SUCCESs framework**

Step 1.1: Read ENTIRE draft. Create analysis file `writer-stickiness-analysis.md` assessing the document against all 6 SUCCESs principles:

- **Simple** (0-3): Identify core message in 12 words or fewer. List competing messages. Rate clarity and focus.
- **Unexpected** (0-3): Identify surprise elements or curiosity gaps. Note where expectations could be violated. Rate attention-getting power.
- **Concrete** (0-3): List visualizable details. Identify abstract sections needing examples. Rate sensory specificity.
- **Credible** (0-3): Identify credibility sources (statistics, testability, authority, vivid details). Note unsupported claims. Rate believability.
- **Emotional** (0-3): Identify emotional connections and personal benefits. Note where motivation could be strengthened. Rate "care factor."
- **Stories** (0-3): Identify story or human elements. Note opportunities to add narrative. Rate mental simulation potential.

Step 1.2: Calculate total current stickiness score out of 18. Present findings to user.

See each principle's section in [resources/success-model.md](resources/success-model.md) for detailed scoring guidance.

**Step 2: Improve weak principles**

Step 2.1: Read analysis file. Identify the 2-3 weakest principles (scored 0-1).

Step 2.2: Work through ENTIRE draft making targeted improvements for each weak principle:
- **Simple**: Refine core message to 12 words or fewer. Strip competing ideas.
- **Unexpected**: Add surprise or curiosity gaps. Violate reader expectations.
- **Concrete**: Add visualizable details and specific examples. Replace abstractions.
- **Credible**: Add statistics (human-scale), testability ("try it yourself"), authority, or vivid details.
- **Emotional**: Strengthen personal benefits and emotional connections. Focus on individuals, not masses.
- **Stories**: Add narrative or human elements. Use challenge, connection, or creativity plots.

Step 2.3: Present improved version to user with changes highlighted.

See [resources/success-model.md](resources/success-model.md) for specific techniques and examples for each principle.

**Step 3: Score and refine**

Step 3.1: Score the revised message using the [Stickiness Scorecard](resources/success-model.md#stickiness-scorecard).

Step 3.2: Aim for 12+/18 for good stickiness, 15+/18 for excellent. If score is below 12, identify the weakest 2 principles and do another improvement pass focusing on those.

Step 3.3: Present final scored version with before/after comparison.

See [resources/success-model.md - Complete Example](resources/success-model.md#complete-example) for transformation patterns.

Validate using [resources/evaluators/rubric_stickiness.json](resources/evaluators/rubric_stickiness.json). **Minimum standard**: Average score >= 3.5.

## SUCCESs Framework Overview

| Principle | Key Question | Technique |
|-----------|-------------|-----------|
| **S**imple | What's the ONE core idea? | Commander's intent in 12 words |
| **U**nexpected | What will surprise readers? | Schema violation + curiosity gaps |
| **C**oncrete | Can readers visualize it? | Sensory details, specific examples |
| **C**redible | Why should readers believe it? | Human-scale stats, testability |
| **E**motional | Why should readers care? | Individual focus, identity appeal |
| **S**tories | Can readers simulate the experience? | Challenge/connection/creativity plots |

**Scoring:** Each principle rated 0-3. Total out of 18. Target 12+ for good, 15+ for excellent.

## Guardrails

**Critical requirements:**

1. **Score before improving**: Always analyze and score the current state before making changes
2. **Target weakest first**: Focus improvements on the lowest-scoring principles
3. **Preserve accuracy**: Never sacrifice truthfulness for stickiness - credibility matters
4. **Context-appropriate**: Not every piece needs maximum stickiness - match to purpose
5. **Re-score after improving**: Always score the revised version to measure improvement

**Common pitfalls:**
- Improving already-strong principles while ignoring weak ones
- Adding surprise that's random rather than relevant to the core message
- Using statistics that are too large to grasp (billions, trillions)
- Focusing on masses instead of individuals for emotional appeal
- Telling instead of showing when adding stories

## Quick Reference

**Key resources:**
- **[resources/success-model.md](resources/success-model.md)**: Complete SUCCESs framework, all 6 principles, scorecard, examples
- **[resources/evaluators/rubric_stickiness.json](resources/evaluators/rubric_stickiness.json)**: Quality scoring criteria

**Inputs required:**
- Draft text or message to enhance
- Target audience (if known)
- Context (presentation, article, email, pitch, etc.)

**Outputs produced:**
- Stickiness analysis with per-principle scores
- Improved version targeting weak principles
- Before/after comparison with score improvement
