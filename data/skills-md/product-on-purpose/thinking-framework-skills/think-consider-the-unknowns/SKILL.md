---
name: think-consider-the-unknowns
description: Produces a known-unknowns ledger by enumerating the relevant evidence not in hand, the variables that bear on a judgment but are unknown or unobservable, rating each unknown by its bearing and its obtainability, then re-rating confidence against the mapped gap. Use when a consequential one-off judgment rests on thin or partial evidence, no usable base rate exists, and the confidence on the table may be inflated by what was never looked at. Not for cases with a real reference class, for widening a numeric interval, or for unknowns cheap enough to just go resolve.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.consider-the-unknowns
  family: assumption-and-belief-challenge
  evidence-tier: "M"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Consider the Unknowns

Confidence tracks the strength and coherence of the evidence you actually considered, and people systematically neglect what is missing - the consumer-psychology literature calls this bias omission neglect. A judgment built on three observations feels as solid as one built on thirty if the three cohere. Every other belief-challenge move works on material that is PRESENT: claims made, assumptions held, counterarguments available, failures imaginable. Consider-the-unknowns works on material that is ABSENT. The durable move is to make the absence itself an object of attention - list the relevant variables you do NOT have, classify each as resolvable or genuinely unobservable, rate how much each would change the call, and then re-state your confidence against that mapped gap. The output is a **known-unknowns ledger**: the judgment, the relevant unknown variables with their bearing and obtainability, a flag on the ones worth resolving before committing, and a re-rated confidence with the delta and the reason its size is what it is.

## When to Use

- A one-off, consequential judgment is being made from thin or partial evidence, and no usable base-rate class exists: a competitive read, a market-entry call, a diagnosis from incomplete data, a hiring or vendor judgment where the file is mostly silence.
- A confident call rests on a small, coherent slice of evidence, and it is worth knowing how much of that confidence comes from the evidence held versus from never having looked at what is missing.
- The judge is plausibly overconfident. The controlled evidence shows the move is selective - it cut confidence where people were overconfident and left well-calibrated judgments alone, closer to targeted medicine than to a blanket confidence tax.

## When NOT to Use

- **Do not use it when a genuine reference class exists.** Base rates beat introspective gap-mapping; route to `think-reference-class-forecasting`. Mapping unknowns when you could just look up the outside view is the slower, weaker path.
- **Do not use it to widen a numeric interval.** The nearest controlled test found post-estimate reasoning prompts largely ineffective for interval overprecision; mechanical widening, re-elicitation, and calibration training did better (Ferretti, Montibeller and von Winterfeldt, 2023). This is medicine for item- and domain-level confidence, not interval width. Selling it as interval-width repair is overclaiming.
- **Do not use it when the unknowns are cheap to resolve.** Go get the information. Cataloging resolvable unknowns instead of resolving them is procrastination with a worksheet.
- **Do not use it on an already-calibrated or underconfident judge.** The evidence shows little effect there, and on an anxious, underconfident call the ledger only feeds doubt.
- **Do not run it on a low-stakes, reversible decision.** An unknowns audit on a two-way door is process for its own sake. Triage one-way-vs-two-way first, and time-box the ledger when you do run it - the space of things you do not know is unbounded, so the ledger covers RELEVANT unknowns, not all unknowns.
- **Do not use it when a sibling skill owns the task.** Testing one specific named assumption is `think-what-would-have-to-be-true`; imagining how a plan fails is `think-premortem`; generating the strongest KNOWN case against a favored view is `think-red-team-light`. This move enumerates the absent, not the present.

## Instructions

When asked to pressure-test the confidence behind a judgment made from incomplete information, follow these steps:

1. **State the judgment and the current confidence in one line.** Name the specific call under consideration and the confidence currently attached to it (a level or a rough percentage). The ledger exists to re-rate THIS confidence; with no judgment and no stated confidence, stop.
2. **Confirm this is the right move.** Check the walls: is there a real reference class (route to reference-class-forecasting)? Is the task widening a numeric interval (this is not that medicine)? Are the unknowns cheap to just resolve (go resolve them)? Is the judge already calibrated or underconfident (skip)? Is the decision low-stakes and reversible (triage first)? If any wall applies, say so and stop or redirect.
3. **Enumerate the relevant unknowns.** List the variables that bear on the judgment but are unknown, unobserved, or unobtainable - the evidence you do NOT have. Push past the obvious; the whole point is to surface what attention skipped. Keep it to RELEVANT unknowns and time-box: the space of the unknown is unbounded.
4. **Rate each unknown's bearing on the judgment.** For each, how much would knowing it move the call - high, medium, or low? A high-bearing unknown is one whose resolution could flip or substantially change the judgment.
5. **Classify each unknown's obtainability.** Mark each as resolvable (obtainable, and at roughly what cost or effort) or genuinely unobservable. This is what separates a gap you can close from a gap you must live with.
6. **Flag the unknowns worth resolving before committing.** The high-bearing AND resolvable unknowns are the action list: resolve these before the judgment hardens. High-bearing but unobservable unknowns are the irreducible uncertainty the confidence must honestly absorb.
7. **Re-rate confidence against the mapped gap.** State the new confidence, the delta from the original, and the reason the delta is the size it is. The move is selective - if the original confidence was already honest about the gap, the delta may be small or zero, and that is a valid result, not a failure.
8. **Emit the known-unknowns ledger artifact** per `references/TEMPLATE.md`: the judgment and original confidence, the table of unknowns with bearing and obtainability, the resolve-before-committing flags, and the re-rated confidence with its delta and rationale - including the pre-printed evidence caveat.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled known-unknowns ledger - the judgment, the table of relevant unknowns with bearing and obtainability, the resolve-first flags, and the re-rated confidence with its delta and reason - not a prose essay. Do not pad the ledger with every conceivable unknown; relevance and bearing are the filters.

## Quality Checklist

Before finalizing, verify:

- [ ] The judgment under consideration and its original confidence are both stated in one line.
- [ ] The walls were checked: no real reference class, not an interval-width task, unknowns not cheap to just resolve, judge not already calibrated or underconfident, decision not low-stakes-reversible. If a wall applied, the skill redirected or stopped instead of producing a ledger anyway.
- [ ] The unknowns listed are RELEVANT and absent - variables not in hand that bear on the call - not a restatement of claims already present or counterarguments already known.
- [ ] Each unknown has a bearing rating (how much it would move the call) AND an obtainability classification (resolvable, at what cost / unobservable).
- [ ] The high-bearing resolvable unknowns are flagged as the resolve-before-committing list.
- [ ] Confidence is re-rated with an explicit delta and the reason for its size; a small or zero delta is accepted as a valid selective result, not forced downward.
- [ ] The output is the known-unknowns ledger artifact, not prose.
- [ ] No overclaiming: the evidence is moderate (M) and transferred from human studies; claim a selective overconfidence-reduction and calibration aid, not a measured gain in AI decision outcomes, and never as interval-width repair (see `evidence/dossier.md`).

## Evidence

Tier **M** (governing; moderate). The move has direct controlled support: Walters, Fernbach, Fox and Sloman (2017, Management Science 63(12): 4298-4307) ran three studies in which prompting people to list unknowns before stating confidence substantially reduced overconfidence, beat the classic consider-the-alternative technique in a head-to-head comparison, and acted selectively - cutting confidence where judges were overconfident while leaving well-calibrated and underconfident domains alone. The underlying mechanism (neglect of missing information inflates confidence and judgment extremity) is independently confirmed by the omission-neglect program (Kardes et al., 2006; the Sanbonmatsu-Kardes line), with Koriat, Lichtenstein and Fischhoff (1980) as the adjacent antecedent. It is M and not S because the exact prompt is a single research line with no named independent replication, the comparison claim comes from that same paper, and the populations are students and online panels on trivia, not field decisions. It is NOT interval-width medicine: post-estimate reasoning prompts were largely ineffective for interval overprecision (Ferretti, Montibeller and von Winterfeldt, 2023). All evidence is transferred from human subjects; none studies an agent-produced ledger, which is why the skill ships as an M-tier calibration aid with hard walls, never as a measured decision-outcome improver. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed known-unknowns ledger on a real decision.
