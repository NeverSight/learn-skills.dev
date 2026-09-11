---
name: think-question-burst
description: Generates a rapid burst of questions about a problem (questions only, no answers), then ranks them for which would most change the approach and selects the single most catalytic one to pursue, producing a ranked question set. Use when you are stuck, too attached to one framing, or need a better question before answering.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.question-burst
  family: divergent-ideation
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Question Burst

Stuck thinking is usually stuck on the wrong question. A question burst generates many questions about a problem in a short, constrained burst (questions only, no answers), to break attachment to the current framing, then ranks them and picks the single most catalytic one. Because a model can generate questions endlessly, the value here is not the generation, it is the **ranking and selection**: this skill produces a ranked set ending in one chosen next question, never a bulk dump. The output is that ranked question set.

## When to Use

- Stuck, or over-attached to a single framing of the problem.
- At the start of exploring an ambiguous problem, before committing to an answer.
- When a better question would unlock more than another answer.

## When NOT to Use

- To produce a bulk list of questions with no ranking or selection (low signal; the main failure mode for an AI).
- When the issue needs answers and convergence, not more questions.
- When the catalytic question is already known.

## Instructions

When asked to run a question burst, follow these steps:

1. **State the problem** in one line.
2. **Burst.** Generate roughly 12 to 20 questions about it. Questions only, no answers, no preamble. Mix angles: why, how, what-if, who, what-would-change-if. Keep it brief.
3. **Rank.** Order the questions by how much answering them would change the approach, not by how easy they are.
4. **Select.** Choose the single most catalytic "next question" and give a one-line reason it would shift the problem.
5. **Emit the ranked question set** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the ranked questions plus the one chosen next question, not a flat list and not answers.

## Quality Checklist

Before finalizing, verify:

- [ ] The burst was questions only, no answers.
- [ ] The questions are ranked by catalytic potential, not ease.
- [ ] Exactly one "next question" is selected with a reason.
- [ ] The output curates, it does not just dump a long list.
- [ ] The output is the ranked question set artifact.

## Evidence

Tier **P**. The method is Hal Gregersen's question burst (MIT Sloan): generate many questions under a strict questions-only rule, then find the catalytic ones. MIT Sloan reports participant benefits (broader view, recognizing one's own role); there is no controlled decision-outcome evidence, and for AI the generation half has little value, so this skill is built around curation. Evidence is transferred from human workshops, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed ranked question set.
