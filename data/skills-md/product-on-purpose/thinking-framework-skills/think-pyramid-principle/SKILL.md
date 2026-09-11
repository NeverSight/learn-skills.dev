---
name: think-pyramid-principle
description: Produces a pyramid that structures a recommendation answer-first - a single governing thought on top, a small set of MECE, deliberately ordered key arguments beneath it, and supporting evidence under each (Minto), with an optional SCQA intro framing. Use when a conclusion or recommendation already exists and must be communicated clearly to a busy or senior reader, when findings need to be ordered into a tight top-down case, or when a write-up buries its point under context.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.pyramid-principle
  family: synthesis
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Pyramid Principle

Most recommendations are delivered in the order they were discovered - context, then analysis, then, eventually, the point - forcing the reader to hold a pile of facts in mind and guess where they lead. The pyramid principle inverts that: the conclusion (the **governing thought**, the one thing the reader should do or believe) goes first; beneath it sit a small set of **MECE key arguments** that together justify it; beneath each sits its **supporting evidence**. The reader descends only as far as their trust requires and can stop at the top with the recommendation in hand. The output is a structured **pyramid** (governing thought + ordered key lines + support), not a flowing essay. It composes a clear case; it does not check whether the case is sound.

## When to Use

- A conclusion or recommendation already exists and must be communicated to a busy or senior reader who needs the headline first.
- Findings, analysis, or a memo need to be ordered into a tight top-down case instead of a chronological narrative.
- A draft buries its point under context and reasons, and needs restructuring so the answer leads.
- Preparing an executive summary, a decision memo, or the spine of a recommendation deck.

## When NOT to Use

- **Early exploratory thinking, before a conclusion exists.** Answer-first structure forces a premature headline; do the thinking first, then structure the answer.
- **To test whether an argument holds.** Auditing reasons, co-premises, and objections for soundness is argument analysis (use **think-argument-mapping**). The pyramid composes a case; it does not check it.
- **To decompose a question for analysis.** Breaking a problem into MECE sub-questions to investigate is an issue tree (use **think-issue-tree**), which structures the *question* for the analyst; the pyramid structures the *answer* for the reader.
- **To make a thin case look authoritative.** Confident structure can lend false weight to weak evidence; a tidy pyramid is not a validated argument.

## Instructions

When asked to apply the pyramid principle, follow these steps:

1. **State the governing thought.** Capture, in one sentence, the single conclusion or recommendation the reader should walk away with. If no conclusion exists yet (the thinking is still exploratory), say so and stop - this is the wrong tool.
2. **Draft the key arguments.** List the small set of reasons (aim for three to five) that, taken together, justify the governing thought. Each must directly answer the question the governing thought provokes ("why do you say that?").
3. **Make the set MECE.** Test the key arguments for overlap (mutually exclusive - merge or re-cut any that restate each other) and for gaps (collectively exhaustive - add anything material the set is missing). Keep it small; do not pad.
4. **Order the key arguments deliberately.** Arrange them by one intelligible logic - importance, time sequence, or structure - not in the order they occurred to you. State which ordering you used.
5. **Attach supporting evidence.** Under each key argument, list the facts, data, or sub-points that support it. This is where detail lives, so the top stays scannable.
6. **Check the logic both ways.** Verify vertically (each level answers the one above) and horizontally (the key lines actually sum to the governing thought - no more, no less). Fix the structure if they do not hold.
7. **Optionally frame the intro with SCQA.** If an opening hook helps, write a **S**ituation the reader accepts, the **C**omplication that disturbs it, the **Q**uestion it raises, and the **A**nswer (= the governing thought).
8. **Emit the pyramid.** Produce the artifact in `references/TEMPLATE.md`: the governing thought, the ordered key lines, and the supporting evidence under each, as an explicit tree.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled pyramid (governing thought, ordered key lines, supporting evidence, optional SCQA intro), not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The governing thought is a single, concrete conclusion stated first - not a topic, a question, or a teaser.
- [ ] There is a small set of key arguments (roughly three to five), each answering "why?" for the governing thought.
- [ ] The key arguments are MECE: no two overlap, and nothing material to the claim is missing.
- [ ] The key arguments are in a deliberate order (importance, time, or structure), and the ordering logic is stated.
- [ ] The key lines actually sum to the governing thought - they justify it, no more and no less.
- [ ] Supporting evidence sits under the right key line, keeping the top level scannable.
- [ ] The output is the pyramid artifact, not prose.
- [ ] No overclaiming: the skill makes the recommendation clearer to follow; it does not certify that the recommendation is correct (see `evidence/dossier.md`).

## Evidence

Tier **P** (practitioner). The pyramid principle is a widely and durably adopted convention for executive communication (Minto 1987); its core "state the answer first" move is consistent with general reading-comprehension findings on stating the main point up front. There is **no body of controlled studies on the named method**, and that comprehension research is adjacent (it tested thesis-first prose in general, not the pyramid, not business recommendations). The evidence is transferred from human practice, not validated for AI-augmented use. The honest value is mechanical: it makes the agent lead with the conclusion and surface an inspectable structure, rather than burying the point. It does not make the recommendation correct. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed pyramid on a real recommendation.
