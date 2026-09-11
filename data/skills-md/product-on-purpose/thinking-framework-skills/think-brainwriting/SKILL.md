---
name: think-brainwriting
description: Generates ideas the way silent parallel brainwriting does, producing several independent idea streams that build on each other without anchoring on the first voice, then consolidates them into a shortlisted idea pool. Use when you need breadth of options and want to avoid the anchoring and conformity that make ordinary brainstorming underperform.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.brainwriting
  family: divergent-ideation
  evidence-tier: "S"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Brainwriting

Verbal group brainstorming reliably underperforms: only one person talks at a time (production blocking), and the room anchors on the first speaker. Brainwriting removes those losses by generating ideas silently and in parallel, then building on each other's written ideas. This skill adapts that for solo-plus-AI: produce several genuinely independent idea streams (distinct angles, generated without contaminating each other), then run a build-on round and consolidate into a shortlist. The output is an **idea pool**. The key is keeping the streams independent first; collapsing into one stream throws away the mechanism that does the work.

## When to Use

- You need breadth of options and want to avoid premature convergence.
- Anchoring or conformity would otherwise narrow the ideas (a single brainstorm).
- Early divergent generation, before any selection.

## When NOT to Use

- When you need to converge, rank, or decide (use a decision skill).
- When deep single-expert reasoning beats breadth.
- If the result would be volume with no build-on and no selection.

## Instructions

When asked to brainwrite, follow these steps:

1. **State the prompt** for ideation in one line.
2. **Generate independent streams.** Produce 3 to 4 separate idea streams, each from a distinct angle, persona, or constraint, generated as if blind to the others. Keep them visibly separate. Aim for a quota per stream.
3. **Build on, across streams.** Now combine and extend: take ideas from one stream and push them with another's logic. This is where brainwriting beats parallel lists.
4. **Consolidate and de-duplicate.** Merge near-duplicates; keep the distinct ideas.
5. **Shortlist.** Select the strongest ideas to carry forward, noting why.
6. **Emit the idea pool** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the separate streams, the build-on round, and a consolidated shortlist, not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] The streams were genuinely independent, not one list relabeled.
- [ ] A build-on round combined and extended across streams.
- [ ] Near-duplicates are merged; distinct ideas kept.
- [ ] A shortlist is selected with reasons.
- [ ] The output is the idea pool artifact, not prose.

## Evidence

Tier **S**. Across decades of replicated studies, silent parallel generation (nominal groups, brainwriting) outproduces traditional verbal brainstorming in quantity and quality of ideas, because it removes production blocking and anchoring (Diehl & Stroebe 1987; Mullen, Johnson & Salas 1991 meta-analysis; methods from Rohrbach 1968 and Delbecq & Van de Ven 1971). The strong evidence is for human groups; the solo-plus-AI adaptation transfers the mechanism (independent parallel streams plus build-on) but does not inherit a measured AI effect size. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed idea pool.
