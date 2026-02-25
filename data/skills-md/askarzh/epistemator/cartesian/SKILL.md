---
name: cartesian
description: This skill should be used when the user asks to "decompose a problem", "apply Cartesian method", "break this down systematically", "reduce to first principles", "analyze from the ground up", "apply methodical doubt", or wants to process input through Cartesian Reductionism to decompose complex wholes into clear, distinct parts.
version: 0.2.0
---

# Cartesian Reductionist Analysis

## Overview

A modern adaptation of Descartes' method of analysis from the *Discourse on Method* and *Rules for the Direction of the Mind*. This method systematically questions assumptions, decomposes, orders, and enumerates to arrive at clear and distinct understanding of any subject.

Unlike naive reductionism ("just break it into parts"), this method recognizes that decomposition can destroy emergent properties — wholes that behave differently from the sum of their parts. The reconstruction step is therefore essential: after decomposition, the analysis must account for how parts interact to produce the whole, including properties that exist only at the level of the whole.

Cartesian Reductionism excels at analyzing complex systems, unclear problems, tangled arguments, and any input where the whole is too complex to grasp without decomposition.

## Core Methodology — The Four Rules

1. **Rule of Evidence (Question Assumptions)** — Accept nothing as true that is not clearly and distinctly known to be so. Identify every assumption, presupposition, and received opinion in the input. In applied analysis, this means testing assumptions against evidence and logic — not Descartes' radical hyperbolic doubt, but a practical inventory of what is well-grounded vs. what is merely taken for granted.

2. **Rule of Division (Decompose)** — Divide the subject into as many parts as possible and as necessary for adequate resolution. Each part should be simple enough to be understood in isolation. Continue subdividing until reaching elements that are self-evident or irreducible.

3. **Rule of Order (Reconstruct)** — Begin with the simplest, most easily known elements and ascend step by step to knowledge of the most complex. Each step must follow necessarily from the previous. Build understanding from foundations upward.

4. **Rule of Enumeration (Verify)** — Make enumerations so complete and reviews so comprehensive that nothing is omitted. Check every link in the chain. Ensure no part has been skipped or assumed.

## Key Concepts

- **Clear and Distinct Ideas:** An idea is clear when it is present and accessible to the attentive mind. It is distinct when it is sharply separated from all other ideas, containing nothing that belongs to something else. Both criteria must be met.
- **Methodical Doubt as Tool:** Doubt is not the conclusion but the instrument. In practice, this means systematically asking "what evidence supports this?" and "could this be otherwise?" — not radical philosophical skepticism, but disciplined assumption-testing. After doubt, reconstruction on firm foundations begins.
- **Irreducible Elements:** The atomic components reached through decomposition — the point at which further division adds no clarity. What counts as irreducible depends on the domain: in software, it might be a single function; in an argument, a single premise; in a process, an atomic action. The test is: can this be understood fully in isolation, or does dividing it further lose meaning?
- **Order of Reasons:** The chain from simple to complex must be unbroken. Each conclusion depends only on what precedes it. If any link is uncertain, everything after it is uncertain.
- **Empirical Integration:** Decomposition and reconstruction should be informed by empirical evidence about how the system actually works. Armchair analysis of structure is insufficient — test your decomposition against observable behavior. If the parts you identified don't account for the whole's observed behavior, the decomposition is wrong.
- **Emergence Awareness:** Some properties exist only at the level of the whole and disappear when decomposed (e.g., consciousness from neurons, market behavior from individual trades). During reconstruction, explicitly note emergent properties that cannot be predicted from parts alone.

## Analysis Protocol

### Structured Mode (default)

Produce the analysis in this exact section order:

```
## Subject Statement
[What is being analyzed, in one clear sentence]

## Doubt Inventory
### Assumptions Identified
- [Assumption 1]: [Why it is doubtable]
- [Assumption 2]: [Why it is doubtable]
- [...]
### What Survives Doubt
- [Element 1]: [Why it is indubitable or well-grounded]
- [...]

## Decomposition Tree
[Break the subject into its constituent parts, recursively]
- Component A
  - Sub-component A.1
  - Sub-component A.2
    - Element A.2.a
    - Element A.2.b
- Component B
  - [...]

## Clear Premises
[List only the elements that are clear and distinct — the foundation for reconstruction]
1. [Premise 1] — [Why it is clear and distinct]
2. [Premise 2] — [Why it is clear and distinct]
3. [...]

## Reconstruction
[Build back up from clear premises to understanding of the whole, step by step]
1. From Premise 1 and 2, it follows that [X]
2. Combined with Premise 3, this entails [Y]
3. Therefore, the complex whole can be understood as [Z]

## Certainty Assessment
[Rate each component of the reconstruction]
- [Conclusion 1]: **Certain** / **Probable** / **Doubtful**
- [Conclusion 2]: **Certain** / **Probable** / **Doubtful**
- Emergent properties: [Properties of the whole not predictable from parts alone, if any]
- Overall assessment: [Summary of what is firmly known vs. what remains uncertain]

**Confidence: [0.0–1.0]** — [Brief justification for the rating]
```

### Interactive Mode

When the user requests interactive/Socratic analysis:

1. Ask the user to state the subject or problem they want to decompose
2. Walk through the doubt inventory together: present each assumption and ask if the user sees others
3. Decompose collaboratively: propose divisions and ask if they are atomic enough or need further splitting
4. Identify clear premises together: ask the user which elements feel indubitable
5. Reconstruct step by step: present each inference and ask if it follows necessarily
6. Assess certainty together: discuss which conclusions are firm and which are tentative

## Example

A brief example illustrating decomposition and reconstruction of "why is this web app slow?":

> **Assumption tested:** "The database is the bottleneck." — Doubtful without profiling data.
>
> **Decomposition:** Request lifecycle → DNS → TLS → server routing → authentication middleware → database query → serialization → network transfer → client rendering.
>
> **Irreducible element identified:** Database query takes 1200ms (measured). All other steps < 50ms.
>
> **Reconstruction:** The query is slow because it scans a full table (no index on the filtered column). Adding an index reduces it to 15ms. The whole (app latency) is explained by this single part — no emergent complexity here, pure decomposition suffices.
>
> **Confidence: 0.9** — Measured data confirms the bottleneck; the fix is straightforward, but untested in production.

## When to Apply This Framework

**Strong fit:**
- Complex systems that need to be understood piece by piece
- Problems where hidden assumptions may be causing confusion
- Technical architectures, business processes, or logical arguments that need decomposition
- Any input where "What are the fundamental parts and how do they relate?" is the core question

**Weak fit:**
- Value judgments or quality assessments (use Pirsig instead)
- Evaluating the truth of a specific proposition (use Scholastic instead)
- Generating creative alternatives (use Six Thinking Hats instead)
