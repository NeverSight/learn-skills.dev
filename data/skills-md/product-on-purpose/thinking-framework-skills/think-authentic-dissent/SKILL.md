---
name: think-authentic-dissent
description: Checks whether a decision has genuine minority dissent or only smooth surface consensus, identifies who actually holds a contrary view, and plans how to elicit and protect real dissent, flagging clearly where a view is constructed rather than authentically held. Use when consensus feels too easy, or to set up genuine challenge before a high-stakes call.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.authentic-dissent
  family: assumption-and-belief-challenge
  evidence-tier: "S"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Authentic Dissent

Genuine minority dissent makes a group reason better: a person who truly holds a contrary view makes the majority search more broadly and consider more options, even when the dissenter is wrong. The catch, established by the same research, is that **role-played devil's advocacy does not replicate this** - assigned dissent gets discounted as performance. So an AI cannot *be* the dissent; anything a model argues against a plan is constructed, the weaker kind. This skill therefore does not pretend to be the dissenter. It engineers the conditions for real dissent: it audits whether genuine dissent exists, surfaces who holds it, plans how to elicit and protect it, and flags constructed dissent as constructed. The output is a **dissent audit and plan**.

## When to Use

- A group decision shows suspiciously smooth consensus and nobody is really pushing back.
- You can influence how challenge is gathered (who speaks, anonymous input, outside reviewers).
- Before a high-stakes call where you want genuine, not performed, challenge.

## When NOT to Use

- As a source of dissent itself: the model's contrarian view is constructed, not authentic (use `red-team-light` for that, which is honest about being constructed).
- In a purely solo setting with no access to other people - you cannot manufacture authentic dissent.
- When genuine dissent already exists and is being heard.
- To "assign a devil's advocate" and consider the job done (the evidence says that does not deliver the benefit).

## Instructions

When asked to set up or audit dissent, follow these steps:

1. **Audit the consensus.** Is the agreement genuine, or is it smoothness from anchoring, hierarchy, or conformity? Note signs (no one names a downside, the senior view landed first, dissent would be costly).
2. **Locate real dissent.** Identify whether anyone actually holds a minority view, and whether it is being voiced, ignored, or suppressed.
3. **Label what is in play.** Mark any current "dissent" as authentic (a real holder) or constructed (assigned/role-played/AI). Do not let constructed dissent count as the real thing.
4. **Plan to elicit and protect genuine dissent.** Concrete moves: anonymous pre-reads, asking the quietest person first, bringing in an outside reviewer who genuinely disagrees, separating generation from evaluation, protecting the dissenter from cost.
5. **For high stakes, prescribe a real dissenter.** Recommend finding a person who actually holds the contrary view, rather than relying on a constructed critique.
6. **Emit the dissent audit and plan** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the audit plus an elicit-and-protect plan, not a constructed counter-argument (that is `red-team-light`'s job).

## Quality Checklist

Before finalizing, verify:

- [ ] The consensus is assessed for whether it is genuine or smoothed by hierarchy/conformity.
- [ ] Any dissent currently in play is labeled authentic vs constructed.
- [ ] The plan gives concrete ways to elicit and protect real dissent.
- [ ] For high stakes, it prescribes finding a real dissenter, not relying on constructed critique.
- [ ] The skill does not present the model's own contrarian view as authentic dissent.
- [ ] The output is the dissent audit/plan artifact, not prose.

## Evidence

Tier **S**. Authentic minority dissent reliably broadens a group's thinking (Nemeth et al. 2001; *In Defense of Troublemakers*), and the same research shows role-played devil's advocacy does not replicate it. That negative result is load-bearing here: an AI's contrarian output is constructed, so this skill works on the conditions for real dissent rather than claiming to supply it. The evidence is for human groups; it bounds, not just transfers to, AI use. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed dissent audit and plan.
