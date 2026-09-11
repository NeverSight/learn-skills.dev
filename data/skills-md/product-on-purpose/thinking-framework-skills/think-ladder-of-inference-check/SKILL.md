---
name: think-ladder-of-inference-check
description: Produces an annotated reasoning trace that reconstructs how a conclusion was reached, from the observable data, to the data actually selected, to the meaning and assumptions added, then flags the riskiest leap and tests an alternative interpretation. Use when a conclusion feels certain but rests on interpretation, or to audit a contested inference.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.ladder-of-inference-check
  family: assumption-and-belief-challenge
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Ladder of Inference Check

People move from observation to action up an invisible, near-instant ladder: all available data, the data they select, the meaning they add, the assumptions they make, the conclusion they draw, the action they take. The leaps feel like facts. This skill slows the climb back down for a given conclusion: it reconstructs the rungs, exposes where selection and interpretation crept in, flags the riskiest leap, and tests at least one alternative interpretation of the same data. The output is an **annotated reasoning trace**, not prose.

## When to Use

- A conclusion feels certain but actually rests on interpretation.
- A disagreement traces to two people reading the same situation differently.
- Auditing a contested inference, including the agent's own conclusion.
- As a step in a reasoning-audit workflow, often after an evidence/inference sort.

## When NOT to Use

- The conclusion follows from direct, verifiable data with no real inferential leap.
- To generate ideas or options (wrong tool).
- On trivial matters where the climb does not matter.
- As a way to dress up and defend the conclusion you already hold.

## Instructions

When asked to check the ladder of inference, follow these steps:

1. **State the conclusion** being examined, in one sentence.
2. **List the observable data available** - everything that could have been noticed, not just what was used.
3. **Identify the data actually selected** - which subset the conclusion was built on, and what was left out.
4. **Surface the meaning and assumptions added** - the interpretation laid on the selected data, and the assumptions that interpretation requires.
5. **Flag the riskiest rung** - the single leap most likely to be wrong or selective.
6. **Test an alternative interpretation** - give at least one credible different reading of the same data, and what it would imply.
7. **Emit the reasoning trace** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the reconstructed ladder with a flagged rung and an alternative interpretation, not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] Observable data includes what was left out, not only what was used.
- [ ] The meaning and assumptions added are stated explicitly, separate from the data.
- [ ] The single riskiest rung is named.
- [ ] At least one credible alternative interpretation is given.
- [ ] The trace tests the climb rather than rationalizing the conclusion.
- [ ] The output is the reasoning trace artifact, not prose.

## Evidence

Tier **P**. The ladder is an influential practitioner model (Argyris; Senge, *The Fifth Discipline*, 1990). The underlying phenomenon (people select data and add interpretation, then treat conclusions as fact) is well grounded in cognitive psychology, but the ladder itself is a map, not a validated intervention, and evidence is transferred from human contexts, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed reasoning trace.
