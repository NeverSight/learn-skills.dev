---
name: scholastic
description: This skill should be used when the user asks to "analyze an argument", "apply scholastic method", "use quaestio disputata", "examine a thesis", "find objections and replies", "apply Thomistic analysis", or wants to process input through the Modern Scholastic framework of structured disputation.
version: 0.3.0
---

# Modern Scholastic Analysis

## Overview

A modern adaptation of the quaestio disputata — the structured disputation framework originating with Thomas Aquinas. This method systematically examines a proposition by articulating the strongest possible objections, then responding to each with precise distinctions.

Unlike the medieval form, this modern adaptation does not presuppose a shared metaphysical or theological framework. It incorporates empirical evidence, surfaces hidden epistemological assumptions, and is designed to be legible across philosophical traditions.

The Scholastic method excels at analyzing arguments, claims, propositions, and any input where the goal is to determine the truth or validity of a position through rigorous dialectical examination.

## Core Methodology

1. **Formulate the Question (Quaestio)** — Convert the input into a precise question or clearly stated thesis. The question may be yes/no ("Whether X is the case?"), comparative ("Whether X is better than Y?"), or explanatory ("What accounts for X?"). It must be specific enough to admit determinate answers.

2. **Raise Objections (Objectiones)** — Construct 3-5 steel-manned objections against the position under examination. Each objection must be the strongest possible case, not a straw man. Apply the principle of charity: formulate each objection as a thoughtful interlocutor would.

3. **Determine the Response (Respondeo)** — The master's own voice. Open with the strongest counter-argument (the traditional sed contra pivot), then provide the main analysis and resolution. Address each objection individually, showing exactly where it succeeds, fails, or requires qualification. Use precise distinctions (distinguo) to resolve apparent contradictions. Use the formal distinction pattern: "The objection holds insofar as X, but fails insofar as Y."

4. **Final Determination (Determinatio)** — Synthesize the analysis into a clear, qualified conclusion. State what has been established, what remains uncertain, and what further questions arise. Include a **confidence rating** (0.0–1.0) indicating how strongly the analysis supports the determination, with a brief justification for the rating.

## Key Concepts

- **Distinguo (Distinction):** The primary analytical tool. When a claim appears both true and false, distinguish the senses in which it is each. Types of distinction include: formal/material, absolute/relative, per se/per accidens, and where appropriate, formalize using symbolic logic (e.g., ∀x(Fx → Gx) vs. ∃x(Fx ∧ ¬Gx)) to make the logical structure of a distinction explicit.
- **Principle of Charity:** Every objection must be constructed at maximum strength. Weak objections produce weak analysis.
- **Qualification over Refutation:** The goal is rarely to completely destroy a position but to determine the precise conditions under which it holds or fails.
- **Epistemological Self-Awareness:** Unlike medieval Scholasticism, the modern method cannot take metaphysical realism or any epistemic framework as a shared starting point. When an argument presupposes a contested epistemological position (e.g., that essences are real, that final causes exist, that moral facts are knowable), surface the presupposition explicitly and address it. The analysis should be legible to interlocutors who do not share its premises.
- **Empirical Integration:** Incorporate relevant scientific and empirical evidence as data within the analysis. Treat empirical findings the way medieval Scholastics treated Aristotelian natural philosophy — as the best available account of how things are, subject to philosophical interpretation but not to be dismissed or ignored.

## Analysis Protocol

### Structured Mode (default)

Produce the analysis in this exact section order:

```
## Quaestio
[The precise question under examination]

## Objectiones
### Objection 1
[Steel-manned objection]
### Objection 2
[Steel-manned objection]
### Objection 3
[Steel-manned objection]

## Respondeo
[Open with the strongest counter-argument (sed contra pivot), then main analysis.]

### Reply to Objection 1
[Precise reply using distinctions: "The objection holds insofar as X, but fails insofar as Y."]
### Reply to Objection 2
[Precise reply using distinctions]
### Reply to Objection 3
[Precise reply using distinctions]

## Determinatio
[Final qualified conclusion]

**Confidence: [0.0–1.0]** — [Brief justification for the rating]
```

### Interactive Mode

When the user requests interactive/Socratic analysis:

1. Begin by asking the user to state their position or question clearly
2. Help refine the quaestio through clarifying questions
3. Present one objection at a time and ask the user to respond before offering the next
4. After all objections are raised, offer the respondeo as a collaborative refinement of the user's thinking, addressing each objection with distinctions
5. Conclude with the determinatio, noting where the user's understanding evolved

## Example

A brief example illustrating the objection–reply pattern with a distinction:

> **Objection:** Free will is impossible because every event has a prior cause, and human decisions are events. Therefore all decisions are determined.
>
> **Reply:** The objection holds insofar as human decisions are events with causal antecedents (*per accidens* — as physical processes, they participate in causal chains). But it fails insofar as it equates causal influence with causal determination (*per se* — the claim that prior causes *necessitate* a unique outcome is a further metaphysical commitment, not entailed by causation alone). Distinguo: "every event has a prior cause" is true in the sense that every event has *contributing* causes, but not in the sense that every event has *sufficient and necessitating* causes.

## When to Apply This Framework

**Strong fit:**
- Evaluating truth claims or propositions
- Analyzing philosophical or ethical arguments
- Examining policy positions with competing considerations
- Any input where "Is X true/valid/justified?" is the core question

**Weak fit:**
- Creative ideation (use Six Thinking Hats instead)
- Systems decomposition (use Cartesian Reductionism instead)
- Value/quality judgments without propositional structure (use Pirsig instead)
