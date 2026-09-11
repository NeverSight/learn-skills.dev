---
name: think-belief-update-routine
description: Produces a belief-update ledger that re-scores a standing inventory of open beliefs against newly arrived evidence on a cadence - each belief carrying a prior confidence, the evidence accrued since the last review, a revised confidence with an explicit delta and direction, a reason for the size of the move (a guard against under-updating), and a next-review trigger. Use when you hold consequential open beliefs, forecasts, or standing assumptions that should track new evidence over time and you want a disciplined, recurring re-score - not a one-time decision record, a finished-event retro, or a single claim's conditions.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.belief-update-routine
  family: meta-thinking-and-reflection
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Belief-Update Routine

A belief-update routine **re-scores a standing inventory of open beliefs against newly arrived evidence, on a cadence**. For each tracked belief it records a prior confidence, the evidence accrued since the last review, a revised confidence with an **explicit delta and direction**, a stated reason for the *size* of the move, and a next-review trigger. The load-bearing move is the disciplined, recurring **re-score of a portfolio over time**: it makes under-updating (the robust human tendency to revise too little for the evidence) visible and correctable, and it keeps beliefs that should track reality - open forecasts, strategic theses, standing assumptions - honest against new information rather than quietly stale. The output is a structured **belief-update ledger**, not prose, designed to be reopened and re-scored on the next cadence.

## When to Use

- When you hold a set of consequential, genuinely open beliefs, forecasts, or standing assumptions that should track reality over time, and you want a recurring, disciplined re-score rather than a one-off.
- When **genuinely new evidence has arrived** since you last examined them, so there is something real to update on.
- When you suspect you are under-updating - holding a belief sticky as evidence accumulates against it - and you want the size of each update made explicit and checkable.
- When you want to build calibration on standing beliefs over many cycles, not judge a single decision.

## When NOT to Use

- **To record a single decision at the moment it is made.** That is `think-decision-journal`, which fixes one prediction in place at commit time and *forbids editing it afterward*. This routine is the opposite shape: it deliberately re-scores a *portfolio* of open beliefs *repeatedly*. Do not use it to capture a one-off decision (you lose the journal's contemporaneous lock), and do not use the journal to track evolving beliefs (you violate its do-not-edit rule).
- **To review a finished episode against what was expected.** That is `think-after-action-review`, which needs a *resolved outcome* and emits sustain/change process actions. This routine operates on beliefs that are still *open* and emits revised confidences, not action items.
- **To surface the conditions under which one contested claim would be the best choice.** That is `think-what-would-have-to-be-true`, which decomposes a single claim into its load-bearing conditions at one sitting. This routine re-scores a *portfolio* of beliefs *on a cadence* against accrued evidence.
- **When no genuinely new evidence has arrived.** Re-scoring on a calendar with nothing new is reflection theater: it manufactures motion or just re-anchors the prior. If nothing material has changed, the honest entry is "no new evidence; no update," not an invented delta.
- **For beliefs that never resolve and carry no real stakes.** Re-scoring trivia delivers no calibration and no decision value; the overhead is unrecovered.

## Instructions

When asked to run a belief-update routine, follow these steps:

1. **Assemble or load the belief inventory.** List the open beliefs being tracked, each as a one-line claim with its **prior confidence** (a percentage or band) and the date it was last scored. If this is the first run, capture the current confidence as the prior. Keep beliefs that are genuinely open and consequential; drop trivia that will never resolve.
2. **Gather the evidence accrued since the last review, per belief.** For each belief, list what has actually happened or come to light since the prior score - dated, sorted into *for* and *against*. If nothing material has arrived for a belief, say so explicitly; that belief's honest update is "no change."
3. **Re-score each belief, with an explicit delta and direction.** State the revised confidence and the **change from the prior** (for example, "65% -> 50%, down 15"). The delta and its direction are load-bearing: a re-score with no stated change is not an update.
4. **Justify the size of each move, guarding against under-updating.** For each non-trivial change, say *why the move is that size* given the strength of the evidence - and explicitly ask whether it is **large enough** (the conservatism guard) or whether you are clinging to the prior. For "no change," confirm that is because no real evidence arrived, not because the belief is sticky.
5. **Set a next-review trigger per belief.** A date, or the specific signal that should force an earlier re-score (a result lands, a metric crosses a line). This is what makes the ledger a recurring routine rather than a one-time note.
6. **Flag beliefs that have effectively resolved.** If a belief has now resolved, mark it for retirement from the open inventory and, where a decision rode on it, point to `think-after-action-review` to close the loop.
7. **Emit the belief-update ledger** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled belief-update ledger - a dated docket of beliefs, each with a prior confidence, the evidence accrued, a revised confidence with an explicit delta and direction, a reason for the size of the move, and a next-review trigger - not a prose essay about how your thinking has evolved.

## Quality Checklist

Before finalizing, verify:

- [ ] Every tracked belief is a concrete one-line claim with a prior confidence (percentage or band) and a date.
- [ ] The evidence accrued since the last review is listed per belief, dated, and sorted for/against - or explicitly noted as "none material."
- [ ] Each revised confidence states an explicit **delta and direction** (not just a new number).
- [ ] The **size** of each non-trivial move is justified against the evidence, with the under-updating guard applied (is the move large enough?).
- [ ] "No update" entries are confirmed as "no new evidence," not unexamined stickiness.
- [ ] Each belief has a next-review trigger (a date or a forcing signal).
- [ ] The output is the belief-update-ledger artifact, not prose.
- [ ] No overclaiming: the ledger surfaces and guards against under-updating and enables calibration over time; it is not claimed to make beliefs more accurate by a stated amount, and it is honest that its direct evidence is limited (see `evidence/dossier.md`).

## Evidence

Tier **P** (practitioner). The mechanism rests on a real, robust bias - people under-update relative to the evidence (conservatism; Edwards 1968) - and on the finding that incremental, evidence-weighted updating tracks accuracy *in scored-forecasting regimes* (Atanasov et al. 2020). But the routine itself is **barely tested directly** - the direct experimental tests of reflection-prompted belief revision are sparse and weak - and its typical use (fuzzy, non-resolving beliefs with no score) sits **outside** the scored-forecasting regime where the supporting evidence was gathered. So the skill claims the under-updating guard and the calibration-enabling record, and **does not advertise an effect size** or a guaranteed accuracy gain. The evidence is transferred from human studies and has not been validated for AI-augmented use. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed belief-update ledger on a real set of open beliefs.
