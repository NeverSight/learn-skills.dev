---
name: think-decision-journal
description: Produces a decision journal entry that records a consequential decision at the moment it is made - the decision, the rationale, the predicted outcome, an explicit confidence level, and the assumptions it rests on - so it can be honestly reviewed later against what actually happened. Use when committing to a consequential, uncertain decision (a launch, hire, investment, bet, or strategic choice) and you want to lock in the prediction now to defeat hindsight bias and build calibration, or when pairing a record-now step with a later review.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.decision-journal
  family: meta-thinking-and-reflection
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Decision Journal

A decision journal records a decision *at the moment it is made* - the decision, the rationale, the predicted outcome, an explicit confidence level, and the assumptions it rests on - so it can be reviewed later against what actually happened. The load-bearing move is **timing**: the prediction is fixed in place before the outcome is known, while the reasoning and the felt confidence are still uncontaminated by the result. That contemporaneous record is the one reliable defense against hindsight bias ("I knew it all along"), it separates decision quality from outcome quality, and it supplies the recorded-prediction half of a calibration loop. The output is a structured **decision journal entry**, not prose, designed to be reopened and scored later.

## When to Use

- At the point of committing to a consequential, genuinely uncertain decision: a launch, hire, investment, vendor choice, bet, or strategic direction.
- When you can still state an honest prediction, confidence level, and set of assumptions before the outcome is known.
- When you intend to review the decision later against reality - it pairs with an after-action review (record now, review later).
- When you want to build calibration over many decisions, not judge a single one.

## When NOT to Use

- **To review a decision after the outcome is already known.** That is an after-action review (`think-after-action-review`); writing a "journal entry" after the result back-fits the prediction, the exact distortion this method exists to prevent.
- **For trivial or fully reversible (two-way-door) decisions.** The capture overhead is not worth it for a cheaply undone choice with no real uncertainty.
- **When no expectation can be honestly stated.** If there is no genuine prediction, confidence, or assumption to record, the entry is theater.
- **To surface only the conditions that must hold for a choice to be right.** That is `think-what-would-have-to-be-true`; the journal captures the whole decision plus a predicted outcome and confidence for calibration.
- **As a substitute for actually reviewing entries later.** A journal nobody revisits delivers no calibration; if there is no intent to review, skip it.

## Instructions

When asked to record a decision journal entry, follow these steps:

1. **Confirm the decision is worth journaling, and not already resolved.** State the decision in one or two sentences. If it is trivial, fully reversible, or the outcome is already known, say so and stop (and for a known outcome, point to `think-after-action-review`).
2. **Record the situation and the rationale.** The context as it stands *now*, and why this choice is being made. Capture the real reasoning, including what makes it a hard call.
3. **Record the options considered and not taken.** The alternatives on the table and the short reason each was set aside. This is part of the rationale a later review will check.
4. **State the predicted outcome and an explicit confidence.** What is expected to happen by a stated date, and a confidence as a percentage or band (for example, "70%"). The confidence must be explicit; a prediction without a stated confidence cannot be calibrated.
5. **Name the assumptions the decision rests on.** The specific things being taken as true that, if wrong, would change the call. List them so they can be checked later, not left implicit.
6. **Set a review date and the signals to check then.** A concrete date for an after-action review, and the observable signals that will tell you whether the prediction held. This is what makes the entry reviewable rather than a diary note.
7. **Emit the decision journal entry** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled decision journal entry - dated, with a predicted outcome, an explicit confidence, named assumptions, and a review date - not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The entry is dated and written *before* the outcome is known (not a back-fitted record of a decision already resolved).
- [ ] The predicted outcome is concrete and tied to a stated date.
- [ ] Confidence is explicit (a percentage or band), so it can be scored later.
- [ ] The assumptions the decision rests on are named specifically, not left implicit.
- [ ] A review date and the signals to check then are set, so the entry is actually reviewable.
- [ ] The output is the decision journal entry artifact, not prose.
- [ ] No overclaiming: the entry enables honest review and calibration; it is not claimed to make the decision turn out better (see `evidence/dossier.md`).

## Evidence

Tier **P** (practitioner). The mechanism rests on well-supported findings - hindsight bias is real and hard to suppress by willpower (Fischhoff 1975), and recorded probabilistic predictions plus feedback improve calibration over time (Tetlock & Gardner 2015) - but the practice itself, popularized by practitioners (Duke 2018), has **limited controlled evidence** that journaling improves decision outcomes. The journal's value is in making later review honest and calibration possible, not in guaranteeing better results. The evidence is transferred from human studies and practice and has not been validated for AI-augmented use. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed decision journal entry on a real decision.
