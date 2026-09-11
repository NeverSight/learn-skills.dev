---
name: think-interval-calibration-check
description: Audits whether a stated confidence interval means what it claims by running an equivalent-bet indifference test on its width and scoring nominal confidence against the actual hit rate, emitting corrected intervals and a calibration scorecard. Use when a human-stated interval or confidence number drives a consequential plan, forecast, or commitment and has never been audited, and the worry is overprecision rather than a wrong central estimate. Calibrates human-stated uncertainty only, never the agent's own confidence, and resizes width without relocating the number. Not for lookupable facts and not a promise of full debiasing.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.interval-calibration-check
  family: meta-thinking-and-reflection
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Interval Calibration Check

People state uncertainty as intervals - "two to four weeks, 90 percent sure" - and those intervals are reliably too narrow. Overprecision is the most robust form of overconfidence: stated 90 percent intervals contain the true value far less than 90 percent of the time, and subjective intervals are sometimes only a fraction as wide as the judge's own information would warrant. A stated "90" that historically hits 50 is not a confidence level, it is a habit of speech, and everything downstream that takes the number literally - an expected-value calculation, a risk model, a commitment - inherits the error. This method interrogates the WIDTH of a stated uncertainty: does your 90 mean 90? It runs two coupled moves that both operate on the width and never on the location of the estimate - an **equivalent-bet indifference test** at elicitation time, and **hit-rate scoring** against resolved outcomes - and emits a **calibration scorecard**. The durable move is not asking "how sure are you?" again. It is converting that question into a concrete bet, widening until the bet is genuinely a toss-up, and scoring the stated confidence against the truths that actually arrive.

## When to Use

- A consequential plan, forecast, or commitment rests on a stated interval or confidence number that has never been audited - the "90 percent sure we ship in Q3" plan, the cost range in a proposal, the confidence column in a decision journal or assumption ledger.
- The same person or team makes repeated resolvable estimates, so a track record exists or can accumulate and the scored-feedback half has material to work with.
- A method that consumes probability numbers at face value sits immediately downstream (an expected-value decision tree, a risk model) - calibrate the inputs before the arithmetic launders them.
- The worry is that the stated confidence is too tight to trust (overprecision), not that the central number is in the wrong place.

## When NOT to Use

- **Do not run it on the agent's own confidence.** An LLM posing an equivalent bet to itself has no felt indifference to reveal; the test becomes the same self-report in different words, and verbalized model confidence is itself systematically overconfident (Xiong et al., 2024). This calibrates a human's stated intervals through elicitation. It is not a self-calibration device for the model. This is the central wall.
- **Do not use it when the problem is the location of the estimate, not the width.** A wrong number, well calibrated, is still wrong. Route a wrong central estimate to `think-reference-class-forecasting` (anchor on the base rate of comparable cases) or `think-fermi-estimation` (build the number from factors). Wrong number, use those; untrustworthy "sure," use this.
- **Do not calibrate an interval around a lookupable fact.** Where the answer can simply be checked, or no genuine uncertainty exists, calibrating its interval is theater.
- **Do not present a one-shot bet-test as a full calibration.** Without resolvable items only the bet-test half applies, and the bet device is the least-evidenced part of the protocol; say plainly that the scorecard is one-legged.
- **Do not promise full debiasing.** The controlled record shows partial correction with a stubborn residue. Promise tighter honesty about uncertainty, not calibrated certainty.
- **Do not confuse it with content moves.** It never asks what information is missing (that is the `consider-the-unknowns` move) and never generates a second estimate to average (that is `think-dialectical-bootstrapping`). It is content-blind: it only asks whether the stated number means what it claims.

## Instructions

When asked to pressure-test a stated confidence interval or audit whether a "90 percent sure" is worth its face value, follow these steps:

1. **Name the focal claim and confirm there is genuine uncertainty.** State the quantity and its stated interval with the nominal confidence ("ship date 8-11 weeks out, 90 percent"). If the answer is lookupable or there is no real uncertainty, stop and say so - calibrating it is theater.
2. **Confirm the problem is width, not location.** If the worry is that the central number is in the wrong place, route to `think-reference-class-forecasting` or `think-fermi-estimation` and stop. This method resizes the stated uncertainty; it never relocates the estimate.
3. **Confirm the judge is a human.** Calibrate a human's stated intervals only. Never present the agent's own self-administered bet as calibration (Xiong et al., 2024). If no human judge is in the loop, say the method does not apply.
4. **Run the equivalent-bet test on each interval.** Offer the judge a choice between (a) betting that the truth falls inside their stated interval and (b) a reference lottery that pays at exactly the nominal probability (the classic device is a wheel with a winning region the size of the nominal confidence). A preference for the wheel reveals felt confidence is below the stated number - they are overconfident, widen the interval. A preference for the interval reveals it is above - narrow it. Iterate the bet against the adjusted interval until the judge is genuinely indifferent.
5. **Record the bet verdict and the adjusted interval.** For each claim, log the original interval, the bet verdict (wheel-preferred / interval-preferred / indifferent), and the adjusted interval at indifference.
6. **Score the track record wherever outcomes resolve.** If the judge has a battery of resolvable items with known answers, or their own past predictions that have since resolved, score the hit rate against the nominal confidence. Diagnose over- or underprecision (90s that hit 50 are overprecise; 70s that hit 90 are underprecise) and feed the score back before the next round.
7. **Mark the scorecard one-legged when no items resolve.** With no resolvable track record, only the bet-test half ran. Say so plainly; do not present a bet-only result as a verified calibration.
8. **Emit the calibration scorecard** per `references/TEMPLATE.md`: each interval, its nominal confidence, the bet verdict, the adjusted interval, and the hit rate and over/underprecision diagnosis where a track record exists - with the pre-printed evidence caveat carried into the artifact.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled calibration scorecard - the focal claims, each stated interval with its nominal confidence, the equivalent-bet verdict, the adjusted interval at indifference, and the hit-rate-versus-nominal diagnosis wherever outcomes resolve - not a prose essay. The evidence caveat ships inside the artifact by construction. Never present the agent's own confidence as a calibrated reading, and never report the central estimate as corrected (this method resizes width, it does not relocate the number).

## Quality Checklist

Before finalizing, verify:

- [ ] The focal claim has genuine uncertainty and is not lookupable, and the problem is width (overprecision), not a wrong central estimate.
- [ ] The judge is a human; the agent's own confidence was never presented as a calibrated reading.
- [ ] Each interval ran the equivalent-bet test and was iterated to genuine indifference, with the original interval, the bet verdict, and the adjusted interval all recorded.
- [ ] Where resolvable items exist, the hit rate is scored against the nominal confidence with an explicit over- or underprecision diagnosis; where they do not, the scorecard is marked one-legged.
- [ ] Only the WIDTH of the uncertainty was adjusted; the location of the estimate was left alone.
- [ ] The output is the calibration scorecard artifact, not prose.
- [ ] No overclaiming: the evidence is practitioner-grade (P) and transferred from human studies; the caveat carries that debiasing is partial, not a guarantee of calibrated certainty (see `evidence/dossier.md`).

## Evidence

Tier **P** (governing; preliminary M overturned to P). The underlying phenomenon - interval overprecision - is established at strong-research level: 98 percent intervals cover roughly 60 percent of true values (Alpert and Raiffa, 1982), and 90 percent intervals contain the truth less than 45 percent of the time (Soll and Klayman, 2004). Scored feedback is among the few interventions with controlled evidence of improving calibration (Lichtenstein, Fischhoff and Phillips, 1982). But a robust bias is not evidence the specific fix works. The M-flavored training results sit on siblings, not this protocol: Lichtenstein and Fischhoff (1980) trained two-alternative half-range items with modest-to-nil transfer, and Klayman et al. (1999) show calibration is not unitary across formats, blocking that transfer; the controlled interval-time remedies tested are fractile decomposition and full-range assignment (Soll and Klayman 2004; Haran, Moore and Morewedge 2010), not the equivalent bet; the strongest training gain (Chang et al., 2016) came from a bundled curriculum; and the equivalent-bet device itself has zero controlled outcome evidence - only interview doctrine (Spetzler and Stael von Holstein, 1975) and excluded vendor data (Hubbard). Grading M would launder cousins' robustness onto the actual move, so the governing grade is P. All evidence is transferred from human subjects; nothing validates the protocol run by or on an AI agent, and the model cannot calibrate itself (verbalized LLM confidence is overconfident - Xiong et al., 2024). The skill ships as an uncertainty-honesty aid that promises partial correction, never calibrated certainty. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed calibration scorecard on a real decision.
