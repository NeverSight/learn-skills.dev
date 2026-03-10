---
name: first-principles-thinking
description: Apply first principles thinking whenever the user is questioning whether a design, strategy, or solution is fundamentally right — not just well-executed. Triggers on phrases like "are we solving the right problem?", "why do we do it this way?", "is this the best approach?", "everyone does X but should we?", "we've always done it this way", "challenge our assumptions", "start from scratch", "is there a better way?", or when the user seems to be iterating on a flawed premise rather than questioning the premise itself. Also trigger when a proposed solution feels like an incremental improvement on something that may be fundamentally broken. Don't optimize a flawed foundation — question it first.
---

# First Principles Thinking

**Core principle**: Strip away assumptions, conventions, and analogies. Reduce everything to the fundamental truths you *know* to be true, then rebuild from there. Most thinking is by analogy — "we do it this way because that's how it's done." First principles asks: *why is it done that way at all?*

---

## The Core Process

### Step 1: Identify the Current Belief or Solution
State clearly what is currently assumed, accepted, or proposed:
- What is the existing approach?
- What problem is it trying to solve?
- What does everyone in this space assume to be true?

### Step 2: Challenge Every Assumption
For each element of the current approach, ask:
- *"Is this actually true, or do we believe it because we've always believed it?"*
- *"Is this a constraint of reality, or a constraint of convention?"*
- *"What would have to be true for this assumption to be wrong?"*

Distinguish between:
- **Physical constraints**: Laws of nature, math, physics — these are real
- **Resource constraints**: Time, money, people — real but changeable
- **Conventional constraints**: "You can't do X" meaning "nobody has done X yet"
- **Inherited assumptions**: Decisions made for past conditions that no longer apply

### Step 3: Identify the Fundamental Truths
What do you *actually* know, stripped of convention?
- What is the core need being served?
- What are the irreducible requirements?
- What would this look like if you designed it from zero, knowing only what's physically true?

### Step 4: Rebuild From the Ground Up
Starting only from fundamental truths, reconstruct the solution:
- What's the simplest approach that satisfies the real requirements?
- What would this look like if invented today, with today's capabilities?
- What existing constraints can be eliminated now that you're not inheriting them?

---

## Output Format

### 🏛️ Current Belief / Approach
State what's being questioned:
- The existing design, strategy, or assumption
- Why it exists (historical or conventional reason)
- What problem it was meant to solve

### 🔬 Assumption Deconstruction
For each major assumption:
| Assumption | Type | Actually true? | Evidence |
|-----------|------|---------------|----------|
| "We need X to do Y" | Conventional | Maybe not | Reason |
| "This requires Z" | Physical | Yes | Because... |
| "Users expect A" | Inherited | Unvalidated | Never tested |

### 🧱 Fundamental Truths Identified
What do we *actually* know, independent of convention?
- Core need: [The real underlying need being served]
- Hard constraints: [What is genuinely immovable]
- Validated facts: [What has been empirically confirmed]

### 🔨 Rebuilt Solution
Starting from fundamentals:
- What does the solution look like without inherited assumptions?
- What changes dramatically?
- What stays the same (and why — what fundamental truth supports it)?
- What's now possible that wasn't in the old frame?

### ⚠️ Assumption Risks
Which surviving assumptions are highest-risk?
- If any single assumption proves wrong, what breaks?
- Which assumptions should be validated before committing?

---

## Thinking Triggers

- *"What is this actually trying to accomplish at the most basic level?"*
- *"If we were building this today with no legacy, what would we do?"*
- *"Is this a law of nature or a law of habit?"*
- *"Who decided this was the right way, and what were their constraints?"*
- *"What would a brilliant outsider — who doesn't know our conventions — suggest?"*
- *"Are we solving the problem, or are we solving our version of the problem?"*

---

## Analogy vs. First Principles

Most thinking operates by analogy:
> *"We do it like company X does it"* / *"The industry standard is Y"* / *"That's how it's always been done"*

Analogy-based thinking is fast and usually adequate. But it **inherits the constraints and mistakes of the original**. When something is fundamentally broken or when you need a step-change improvement — not an incremental one — analogy thinking will never get you there.

First principles is slower but the only path to **genuinely novel solutions**.

---

## Example Applications
- **"Should our agent pipeline be sequential?"** → Why sequential? What's the fundamental constraint? Is it ordering of dependencies, or just convention borrowed from waterfall?
- **"We need a dedicated QA team"** → Is QA a separate function by necessity, or because testing was historically slow and manual?
- **"Our API needs versioning"** → What's the actual need — backward compatibility. What's the minimum mechanism that provides that, built from scratch?
- **"We need standups every day"** → What's the fundamental need? Coordination. What are all the ways to achieve that, unconstrained by "meeting" as a format?
