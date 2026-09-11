---
name: think-evidence-vs-inference-sort
description: Produces an evidence/inference ledger by sorting the claims in a prompt, document, or proposed conclusion into evidence, inference, and assumption, attaching a confidence level to each inference and flagging anything uncited. Use when a recommendation must be trusted, or when you need to audit the reasoning behind a conclusion in a high-stakes context.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.evidence-vs-inference-sort
  family: reasoning-clarity
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Evidence vs Inference Sort

Reasoning degrades when evidence (what is actually observed or verifiable) is blended with inference (what is deduced) and assumption (an unstated premise). Models are especially prone to this: they present fluent inference in the same confident register as fact. This skill separates them: it labels each claim in a body of text as evidence, inference, or assumption, records the basis for each, attaches a confidence level to inferences, and flags anything uncited. The output is an **evidence/inference ledger**. Note the boundary: this classifies claim *type*; it does not verify that the evidence is *true* (that is a separate, fact-checking job).

## When to Use

- A recommendation, plan, or conclusion must be trusted before it is acted on.
- High-stakes contexts: legal, medical, financial, safety, architecture and planning.
- Auditing the reasoning behind a conclusion, including the agent's own.
- As a step in a reasoning-audit workflow.

## When NOT to Use

- As a fact-checker. It labels what *kind* of claim something is, not whether it is true.
- On creative or exploratory work where rigor is not the point.
- On trivial claims, where sorting produces only noise.
- When the claims are already well-sourced and the leaps are already explicit.

## Instructions

When asked to sort evidence from inference, follow these steps:

1. **Collect the claims.** Break the prompt, document, or proposed conclusion into discrete claims. Keep each to one assertion.
2. **Label each claim.** Mark it **Evidence** (observed or verifiable, with a source), **Inference** (deduced from other claims), or **Assumption** (an unstated premise it depends on).
3. **Record the basis.** For evidence, name the source or observation. For inference, name what it is inferred from. For assumption, state the premise plainly.
4. **Rate inference confidence.** For each inference, assign high / medium / low and say why. Do not treat plausibility as verification.
5. **Flag the gaps.** Mark anything presented as fact but uncited, and any load-bearing assumption that is unexamined.
6. **Surface the load-bearing unknowns.** List the few unsupported claims that most need verification before the conclusion is trusted.
7. **Emit the ledger** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the ledger plus the load-bearing-unknowns list, not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] Every claim is labeled evidence, inference, or assumption.
- [ ] No confident inference is mislabeled as evidence.
- [ ] Inferences carry a confidence level with a reason.
- [ ] Uncited "facts" and unexamined assumptions are flagged.
- [ ] The output does not claim to have verified truth, only sorted claim type.
- [ ] The output is the ledger artifact, not prose.

## Evidence

Tier **P**. The evidence/inference distinction is a foundational critical-thinking competence (Facione, Delphi Report 1990), and explicit critical-thinking instruction shows moderate gains broadly (strongest for argument mapping, an adjacent technique). This specific "sort into a ledger" method is practitioner-grade, evidence is transferred from human contexts, and the skill verifies claim type, not truth. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed ledger.
