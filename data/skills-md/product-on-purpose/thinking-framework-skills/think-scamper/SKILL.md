---
name: think-scamper
description: Generates a structured set of variations on an existing idea, product, or process by running it through seven transformation prompts (substitute, combine, adapt, modify, put to other use, eliminate, reverse), then shortlists the most promising, producing an expansion sheet. Use when you have a seed idea and need to break past the obvious options; not for blank-page ideation.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.scamper
  family: divergent-ideation
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# SCAMPER

People and models fixate on the first few obvious variations of an idea. SCAMPER counters that by running an existing idea, product, or process through seven transformation prompts, each forcing a different kind of change: Substitute, Combine, Adapt, Modify (magnify or minify), Put to other use, Eliminate, Reverse. It is a later-stage method: it transforms a seed that already exists, it is not a blank-page generator. The output is an **expansion sheet** that ends in a shortlist of the most promising variations, not an undifferentiated pile of ideas.

## When to Use

- A seed idea, product, feature, or process already exists and needs to be pushed past the obvious.
- Late-stage ideation, or loosening a stuck or merely incremental option set.
- After the problem is framed and before converging on a choice.

## When NOT to Use

- Blank page. With no seed to transform, there is nothing to operate on; reframe first or use a different generator.
- When the problem needs reframing, not more options (use problem restatement).
- When you need to converge and decide (use a decision skill); this diverges.
- If the result would be volume without selection. The shortlist step is mandatory.

## Instructions

When asked to run SCAMPER, follow these steps:

1. **State the seed.** Name the existing idea, product, or process being transformed, in one sentence.
2. **Run the seven lenses.** For each, apply the prompt and generate one to three concrete variations:
   - **Substitute** a component, material, rule, or person.
   - **Combine** it with another idea, feature, or step.
   - **Adapt** a solution from a different domain.
   - **Modify** an attribute (magnify or minify it).
   - **Put to other use** (a different user, job, or context).
   - **Eliminate** a part, step, or assumption.
   - **Reverse** the order, roles, or direction.
3. **Skip what does not apply.** If a lens yields nothing real, say so rather than padding.
4. **Shortlist.** Select the three to five most promising variations to carry forward, and say why.
5. **Emit the expansion sheet** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the per-lens expansion plus the shortlist, not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] There was a real seed idea to transform (this is not blank-page ideation).
- [ ] Each applied lens produced a concrete variation, not a vague gesture.
- [ ] Lenses that do not apply are skipped with a note, not padded.
- [ ] A shortlist of three to five variations is selected, with reasons.
- [ ] The output is the expansion sheet artifact, not prose.

## Evidence

Tier **P**. SCAMPER is a practitioner ideation mnemonic (Eberle 1971, built on Osborn's idea-spurring checklists). Structured prompts can help break functional fixedness and broaden an option set, but there is no strong evidence SCAMPER specifically produces better or more original ideas than other generators, and increasing idea quantity is not the same as quality. Evidence is transferred from human contexts, not AI-validated. Methods with stronger generation evidence (Brainwriting / NGT) are separate skills. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed expansion sheet.
