---
name: inversion-premortem
description: Apply inversion and pre-mortem thinking whenever the user asks to evaluate a plan, strategy, architecture, feature, or decision before execution — or when they want to stress-test something that already exists. Triggers on phrases like "is this a good idea?", "what could go wrong?", "review this plan", "should we do this?", "are we missing anything?", "stress-test this", "what are the risks?", or any request to validate a decision or design. Use this skill proactively — if the user is about to commit to something, this skill should be consulted even if they don't ask for it explicitly.
---

# Inversion & Pre-mortem Skill

**Core principle**: Instead of asking "how do we make this succeed?", ask "how does this definitely fail?" — then work backwards. Surfaces hidden assumptions, fragile dependencies, and blind spots that forward-thinking analysis misses.

---

## Two Complementary Techniques

### Technique 1: Inversion
Flip the problem. If you want to understand how a system succeeds, first rigorously define how it fails.

**Process:**
1. State the goal clearly: *"We want X to succeed."*
2. Invert it: *"What would guarantee X fails completely?"*
3. List all failure conditions exhaustively — be adversarial, not optimistic
4. For each failure condition: **is it currently present, partially present, or guarded against?**
5. The unguarded ones become your risk register

**Key question to ask**: *"What assumptions must be true for this to work — and what happens if they're false?"*

### Technique 2: Pre-mortem
Imagine you're 12 months in the future. The project/system/decision has **failed badly**. Now explain why.

**Process:**
1. Vividly imagine the failure: *"It's [date]. This has completely fallen apart."*
2. Write the failure story in past tense — what happened?
3. Identify the 3–5 root causes that led to failure
4. For each cause: **what early warning signal would have been visible?**
5. Map signals back to today: **which of those signals exist right now?**

---

## Output Format

### 💀 Failure Modes (Inversion)
For each identified failure mode:
- **Condition**: What must go wrong for this to fail?
- **Likelihood**: Low / Medium / High
- **Currently guarded?**: Yes / Partially / No
- **What guards it** (or what's missing)

### 🪦 The Failure Story (Pre-mortem)
A short narrative: *"It's [future date]. Here's what happened..."*
- Name the specific sequence of events
- Call out the moment where it became unrecoverable
- Identify what **looked fine** at the start but was actually fragile

### ⚠️ Hidden Assumptions
List the beliefs the plan depends on that haven't been validated:
- Technical assumptions
- Human/team behavior assumptions
- Market or user assumptions
- Dependencies on external systems or actors

### 🛡️ Mitigations
For each high-likelihood, unguarded failure mode:
- Concrete action to reduce risk
- Early warning metric to monitor
- Reversibility assessment: *Can we undo this if it fails?*

---

## Thinking Triggers

Use these prompts to deepen the analysis:
- *"What is the single most likely way this fails?"*
- *"Who is most likely to be frustrated by this in 6 months, and why?"*
- *"What do we believe that might be wrong?"*
- *"If we had to bet against this succeeding, where would we put our money?"*
- *"What's the optimistic assumption hiding in plain sight?"*

---

## Example Applications
- **Evaluating a new feature**: What user behaviors are we assuming? What if adoption is 10x lower than expected?
- **Architecture decision**: What if the third-party API we depend on changes its contract? What if latency doubles?
- **Hiring or team change**: What does this look like if the new hire isn't a fit after 3 months?
- **Growth strategy**: Imagine we executed perfectly and it still failed — why?
