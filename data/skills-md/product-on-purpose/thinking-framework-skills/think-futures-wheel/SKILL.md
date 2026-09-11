---
name: think-futures-wheel
description: Produces a consequence map by tracing the first, second, and third order effects of a change or decision radiating outward from the center, surfacing ripples beyond the obvious and flagging the high-impact branches. Use when a decision has knock-on effects over time, or when first-order thinking is missing downstream risks and opportunities.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.futures-wheel
  family: systems-and-consequences
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Futures Wheel

Most analysis stops at first-order consequences: the immediate, obvious results. A futures wheel pushes past that. The change goes at the center; first-order consequences radiate around it; each of those spawns second-order consequences ("and then what?"); then third-order. The structure forces attention onto the downstream and cross-domain ripples that linear thinking skips, and flags the branches worth a response. The output is a **consequence map**. For a quick pass, a lightweight "second-order effects" mode runs only the first-to-second step.

## When to Use

- A decision or change has knock-on effects that play out over time.
- First-order analysis is missing downstream risks or opportunities.
- Scanning the systemic side effects of a new idea before committing.

## When NOT to Use

- Simple, linear situations with no meaningful higher-order effects.
- When you need to decide, not explore (hand the map to a decision skill).
- When the result would be branches to irrelevance rather than a focused map.

## Instructions

When asked to build a futures wheel, follow these steps:

1. **Center it.** State the change or decision at the middle, in one line.
2. **First order.** List the immediate, direct consequences. Span domains (technical, financial, customer, team, competitive), not just the obvious one.
3. **Second order.** For each meaningful first-order effect, ask "and then what happens?" and add its consequences.
4. **Third order.** For the branches that still matter, extend one more step. Stop a branch when it goes trivial.
5. **Flag the branches that matter.** Mark the high-impact or non-obvious consequences, and add a one-line "watch or do about it" for each.
6. **Emit the consequence map** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the nested consequence map with flagged branches, not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] The map reaches at least second order; it does not stop at first-order.
- [ ] First-order effects span multiple domains, not just the obvious one.
- [ ] Branches that go trivial are pruned, not padded.
- [ ] The high-impact or non-obvious branches are flagged with a response note.
- [ ] Branches are presented as possible ripples to watch, not predictions.
- [ ] The output is the consequence map artifact, not prose.

## Evidence

Tier **P**. The futures wheel is an established foresight method (Glenn, 1971; used in foresight practice and documented in primers such as UNICEF's 2025 guidance), valued for pushing analysis beyond first-order consequences. Its validation is qualitative; it does not predict the future, so branches are structured speculation, not probabilities. Evidence is transferred from human foresight practice, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed consequence map.
