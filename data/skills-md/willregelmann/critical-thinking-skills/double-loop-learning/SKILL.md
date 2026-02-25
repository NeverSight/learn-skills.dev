---
name: double-loop-learning
description: Surfaces and assesses hidden assumptions behind decisions, designs, or recurring patterns — use when reviewing a design before committing, reflecting on recurring problems, or questioning why the same kinds of issues keep appearing
tags:
  - critical-thinking
  - decision-making
  - design-review
  - assumptions
---

# Double-Loop Learning Review

Surface the hidden assumptions behind decisions, then assess whether they still hold. Single-loop learning fixes errors; double-loop questions the goals, values, and mental models that produced them.

## Quick Reference

| Step | Job | Output |
|------|-----|--------|
| 1 | Identify input and mode | Pre-decision (artifact) or periodic review (patterns) |
| 2 | Interrogative pass | Draft list of falsifiable assumptions |
| 3 | Contrastive deepening | Sketches of alternatives -> additional assumptions missed |
| 4 | Assess and build map | Assumption map + prose summary |

## Process

### 1. Identify the Input

Determine the mode:

- **Pre-decision** — User provides an artifact (design, spec, architecture, code). Surface what it assumes.
- **Periodic review** — User points to a collection of past decisions, review results, a codebase, or asks to reflect on patterns. Surface recurring assumptions.

Read everything provided. If the input is insufficient to run the interrogative pass (e.g., no artifact, codebase, or decision history), ask the user to provide or point to the specific material to review.

### 2. Interrogative Pass

Work through probing questions adapted to the mode.

**Pre-decision (artifact-focused):**
- What is this optimizing for? What's being traded away?
- What constraints are treated as fixed? Which are actually choices?
- What does this assume won't change?
- What failure modes does this implicitly accept as unlikely?
- Who/what does this assume will behave a certain way?

**Periodic review (pattern-focused):**
- What kinds of problems keep recurring? What do they have in common?
- What approaches have been consistently chosen? What's been consistently avoided?
- What would someone new to this project find surprising or arbitrary?
- Which past decisions are still shaping current choices? Are they still valid?

State each assumption as a falsifiable belief (e.g., "Users will always authenticate via OAuth" not "authentication stuff"). If you can't imagine it being false, it's not specific enough. Note where in the input each assumption appears — this becomes the Source column in the map.

### 3. Contrastive Deepening

For each major assumption, briefly sketch what the design or decision would look like if that assumption were *false*. If inverting an assumption reveals a radically different design, there's a deeper assumption the interrogative pass didn't surface. Add it to the list.

**Pre-decision:** Invert the assumption and sketch the alternative design.
**Periodic review:** Invert the assumption and consider what the pattern of decisions would have been if it had been questioned earlier.

This step can be abbreviated for simple inputs but should not be skipped — it routinely finds 2-3 assumptions the questions miss.

### 4. Assess and Build the Map

For each surfaced assumption, assess:

- **Still Valid** — Evidence supports it, no action needed
- **Questionable** — Uncertain or eroding. Pair with an experiment to test it.
- **Invalidated** — Evidence contradicts it. Recommend a specific change.

Present the assumption map:

```
| # | Assumption | Source | Assessment | Action |
|---|-----------|--------|------------|--------|
| 1 | [falsifiable belief] | [where it shows up] | Still Valid | — |
| 2 | [falsifiable belief] | [where it shows up] | Questionable | [experiment to test] |
| 3 | [falsifiable belief] | [where it shows up] | Invalidated | [recommended change] |
```

Follow with a prose summary: count by assessment, highest-risk assumptions, and what would change if the Questionable/Invalidated ones were addressed.

## Common Mistakes

- **Listing facts instead of assumptions.** "The system uses PostgreSQL" is a fact. "PostgreSQL will handle our scale requirements" is an assumption.
- **Assumptions too vague to assess.** "We assume the architecture is good" is unfalsifiable. "Current service boundaries won't need to change for 2x traffic" is assessable.
- **Skipping the contrastive step.** The interrogative pass feels complete. It isn't. Inverting assumptions surfaces the ones you can't articulate — the water the fish doesn't see.
- **Marking everything Still Valid.** Every non-trivial system has assumptions under pressure. If nothing is Questionable, the review wasn't rigorous enough.

## Key Principles

- **Assumptions are falsifiable beliefs.** "We assume X" not "X is a consideration."
- **Questionable is the most valuable assessment.** Still Valid and Invalidated are easy. Questionable assumptions need experiments, not opinions — that's where the real leverage is.
- **The contrastive step catches what questions miss.** Questions surface assumptions you can articulate. Inverting surfaces ones you can't.
- **The map is the deliverable.** Not the questions asked, not the contrastive sketches. Those are working artifacts.
