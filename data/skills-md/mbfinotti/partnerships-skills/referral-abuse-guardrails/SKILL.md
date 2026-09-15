---
name: referral-abuse-guardrails
description: Define the operational guardrails that stop end customers from gaming a refer-a-friend program - reward caps, velocity limits and cooldowns, reward-hold windows tied to the refund window, eligibility rules, identity-verification gates, a published enforcement ladder, and abuse-monitoring signals. Produces a guardrail spec for B2C and B2B SaaS referral program managers. Use whenever the user mentions referral abuse, self-referral, fake accounts claiming referral rewards, referral rings, or a referral code leaking to coupon forums, even if they never say abuse. Do NOT use for professional-affiliate traffic fraud - use mbfinotti/partnerships-skills@affiliate-fraud-detection instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.9"
---

# Referral Abuse Guardrails

Define the guardrails that stop end customers from gaming a customer refer-a-friend program, and deliver them as a guardrail spec: rules with thresholds, verification gates, a reward-hold policy, an enforcement ladder, and monitoring signals. This skill protects whatever reward structure already exists - it never redesigns it.

No ratified standard covers consumer referral abuse. Borrow exactly four things, nothing more, and only as a mental model, never as a compliance claim:

- GIVT/SIVT shape (ad-measurement standards): a cheap deterministic tier plus an expensive corroborative tier.
- OWASP OAT-019 Account Creation: the automated slice only.
- Trust-and-safety enforcement-ladder principles: proportionality, consistency, transparency, for the enforcement section.
- Sybil-attack result, as the strategic frame: fake identities can never be fully detected without a central identity authority, so every guardrail is really a cost imposed on the abuser.

The goal is making abuse unprofitable, not catching everything.

## Ground Rules

- Strictly defensive. Describe each abuse pattern only to the depth a defender needs to recognize and block it: state the observable tell in program data, never evasion technique, tooling, or step-by-step exploitation.
- Label every numeric threshold with its provenance: published program terms, academic result, vendor rule of thumb, or a baseline the user derives from their own data. Never present a vendor heuristic as an industry constant.
- Warn off two circulating numbers: "referral fraud = 21% of all ecommerce fraud" is circular vendor citation (vendors quoting each other) and the "$443B in false declines vs $48B fraud" figure is unverifiable precision. Cite the mechanism - false positives cost more than fraud because they carry lost LTV - never those numbers.
- Separate the genuine abuser from the aggressive bargain-hunter. The first gets the enforcement ladder; the second gets a rule tweak and is often worth retaining.
- A rule not published in the program terms before a referral was made is not enforceable against that referral. Design every rule together with its publication.

## Interview

Ask before designing anything. One question per message; multiple-choice where possible; skip anything already answered.

- What are the program mechanics and reward structure in force: sidedness, reward type and value per side, payout trigger?
- B2B, B2C, or both?
- What is the user-account and identity model: email-only signup? Phone? Payment instrument on file before the qualifying event?
- Which verification capabilities exist today (email confirmation, SMS, disposable-domain blocking, device signals, billing webhooks)?
- What data can actually be queried: referral events, signup metadata, payment records, refund/chargeback records, retention by cohort?
- What abuse has been seen so far, and how was it noticed?
- What reward value is at risk: per reward, and per month across the program?
- How long is the refund or chargeback window on the underlying purchase?
- What is the tolerance for friction versus leakage - would you rather overpay a few gamers or lose a few real referrals?
- Are program terms published today, and what do they already say about caps, eligibility, and reward denial?
- By what date must the guardrails be live - a relaunch, a board review, or an incident already bleeding?
- Do you want a one-off fix for the abuse already seen, or a compounding control set that keeps holding as the program scales?
- What is the effort ceiling: engineering time this cycle, review headcount, and is the qualifying event changeable at all?

The last three set the control ordering in Workflow step 4, so ask them before designing anything - by step 4 the reader has already committed to a path.

## Workflow

1. Run the Interview; collect every answer the spec depends on.
2. Confirm the scope boundary: the reward structure (sidedness, type, size, trigger) is a given. If it is the problem, say so and route to `mbfinotti/partnerships-skills@referral-incentive-design` (see Reference).
3. Map the program's abuse surface from [references/abuse-patterns.md](references/abuse-patterns.md): which patterns the reward value, identity model, and qualifying event actually expose it to.
4. Work the control ladder, using [references/guardrail-mechanics.md](references/guardrail-mechanics.md). Six controls compete for the same hours:

   - **Event**: qualifying-event design.
   - **Caps**: budget ceiling, velocity limits, cooldowns.
   - **Hold**: reward hold window.
   - **Eligibility**: rules with memory.
   - **Verification**: gates.
   - **Review**: manual review.

   Vendor blogs present this order backwards - detection tooling first, program design last. Rank them:

   - efficiency: `event > caps == hold > eligibility > verification > review`
   - value: `event > eligibility > hold > verification > caps > review`
   - effort: `review > event > verification > eligibility > caps == hold`
   - compliance cost: `verification > eligibility > event == caps == hold > review`

   Caps and hold tie because each is a payout-side number published in terms, shipped in one config change, gating no legitimate user, and each bounds a loss the other cannot - caps bound volume, hold bounds reversal. Event, caps and hold tie on compliance cost because none touches identity data or needs sign-off. Review sits lowest on that axis because a human in the loop _reduces_ exposure: several regimes bar a fully automated denial.

   Effort is composite here - friction charged to legitimate users, build time, reversibility. Event design ranks high on it because rewiring the trigger is a quarter of product and billing work, yet still leads on efficiency: that cost is one-time engineering, while verification charges every legitimate signup forever.

   Default: caps, hold, and published eligibility in the first pass, always. Climb to event redesign whenever the current qualifying event is bare signup or an unpaid action - nothing below it holds while the event is free to fake.

   This order starves verification gates and manual review. Both are high value against the two abuses caps and holds cannot touch - automated account farming, B2B shell entities - and both lose every efficiency round. Promote them when per-item review cost sits below the reward value (the B2B default), or when an incident is confirmed automated rather than opportunistic.

   Re-rank on the Interview answers and name in the spec which answer moved which control:

   - A hard live-by date promotes caps, hold, and eligibility (config, one sprint) and schedules event redesign for the next cycle - never drops it.
   - A compounding mandate promotes event design and eligibility memory, which keep working at no ongoing cost.
   - A low effort ceiling deletes manual review and the upper verification rungs from the spec outright rather than parking them at the bottom; record which you deleted and why.

   Re-rank again on what you already know about this program:

   - A payment instrument collected before the qualifying event moves verification up sharply - the strongest gate is already paid for.
   - An existing trust-and-safety function collapses review's effort.
   - A regulated program already runs identity checks, so its top rung costs nothing at the margin.

   Treat the ordering as a default, not a law: it shifts with context and with who executes it.

5. Handle B2B and B2C explicitly. Caps, holds, and eligibility memory work identically for both - say so. B2B diverges on:

   - Domain-overlap checks between referrer and referee: the check that matters, since a work-email check alone is weak because a shell company has a real domain.
   - Pre-payout human review: ROI-positive in B2B, not in B2C.
   - Company-account credit by default: paying an individual employee is a procurement/gift-policy problem before it is a fraud problem.

6. Choose monitoring signals from [references/detection-signals.md](references/detection-signals.md), which carries the full per-axis ranking.

   - efficiency: `payment-reuse == cohort-quality > velocity > email-similarity > graph > fingerprint`

   The two leaders tie because both already sit in billing data, neither degrades with a browser or device change, and each catches exactly what the other misses. Cookie and IP linkage are excluded from the ranking, not demoted: their value is already at the floor, so ordering them would be false precision. Graph signals are what this order starves; see the reference for the condition that promotes them.

7. Design the enforcement ladder from [references/enforcement-and-compliance.md](references/enforcement-and-compliance.md): published rungs, a specific reason string for every denial, and a working appeal path - build the reason string and the appeal path before the detector. Keep legal constraints as design constraints and route the actual legal questions to counsel.
8. Verify every rule is publishable: flag any rule missing from current terms as unenforceable until published, and route the clause drafting to `mbfinotti/partnerships-skills@affiliate-program-terms`.
9. If you can query the program's event data, derive velocity and flag thresholds from the user's own legitimate-referrer distribution (e.g. p95-p99 of weekly referrals); otherwise mark them as illustrative defaults to replace with derived baselines within the first review cycle.
10. Emit the guardrail spec (Output Shape below), one section at a time for user validation; ground it in a matching worked example from [references/worked-examples.md](references/worked-examples.md).
11. Attach the calibration plan from the Pass Threshold below and iterate until it holds.
12. If your harness has persistent memory, memorize the decided thresholds, hold window, and enforcement rungs so a later tuning run starts from them instead of re-interviewing.

## Output Shape

Deliver every engagement as this artifact. Every threshold line carries a provenance tag; every rule line names the legitimate behavior that could trip it.

```
REFERRAL GUARDRAIL SPEC - <program>, <date>
Qualifying event : reward trigger + why it is costly to fake + reversibility note
Caps             : per-referrer (period + lifetime), per-referee, program budget ceiling.
                   Take the values from the existing reward design where one exists and
                   record them as given; this spec enforces caps, it does not size them
Velocity         : referrals/claims per referrer per window + cooldown after a burst
Hold policy      : hold length = refund/chargeback window (+ processing), pending-state display
Eligibility      : new-customer definition, self/household exclusion, cross-referrer cooldown,
                   B2B domain-overlap rule
Verification     : gates by friction rung, escalation condition per rung, what is never gated
Monitoring       : signals watched, expected flag baseline, cohort-quality dashboard
Enforcement      : published ladder rungs, reason strings, appeal path + response SLA
Terms status     : where each rule is published; unpublished rule = not yet enforceable
Calibration      : holdout cell design, review cadence, leakage/friction computation
```

## Pass Threshold

Judge the spec on leakage and friction together - never a catch rate or precision target alone. No referral-specific false-positive benchmark is published anywhere; never substitute an industry number for the user's own holdout.

- Compute both on the same unit: Leakage = (invalid rewards paid) x (reward cost); Friction = (rewards wrongly withheld) x (reward cost + support cost + P(churn) x LTV). The friction term carries an LTV multiplier the leakage term does not, so a 1:1 error-rate trade is almost never break-even - when in doubt, loosen.
- Calibrate with a holdout: run a small cell under looser rules and compare it to the strict rules on all three conditions below. The spec passes only when all three hold:
  1. **Total value, not per-signup**: the strict cell's 90-day cohort value **per 1,000 exposed referrers** is at least the holdout's. This condition is load-bearing and must never be replaced by a per-signup average.
     - Tightening removes marginal signups, so per-signup value is non-decreasing in strictness.
     - A per-signup gate is satisfied most easily by the most over-tight configuration and can never fail for over-tightening, which is the failure this whole section exists to catch.
  2. **Quality**: the referred cohort beats organic on retention, refund rate, and 90-day revenue.
  3. **Net of the formula above**: leakage saved by the strict rules exceeds the friction cost they incur, both computed on the same exposure base.
- If the referred cohort loses to organic even with sane guardrails, the program is buying signups, not acquiring customers - the defect is the reward structure, so route to `mbfinotti/partnerships-skills@referral-incentive-design` rather than tightening further.
- Iterate thresholds until all three conditions hold; if data to calibrate does not exist yet, say so in the deliverable and schedule the holdout as the first post-launch review gate.

## Common Failure Modes

| Defect                                             | Consequence                                                   | Fix                                                                                                                                                                                                                 |
| -------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Guardrails so tight they kill legitimate referrals | Program starves; friction cost exceeds leakage saved          | Apply the leakage/friction formula; loosen until cohort value per 1,000 exposed referrers recovers. A rising per-signup average alongside falling volume is the signature of this defect, never evidence against it |
| Caps without velocity checks                       | Abuser hits the lifetime cap in a weekend, undetected         | Pair every cap with a per-window velocity limit and burst cooldown                                                                                                                                                  |
| Ignoring device and payment-instrument reuse       | Cheap deterministic self-referral catches missed              | Check payment-instrument reuse first; it is the strongest signal already held                                                                                                                                       |
| Silent reward denial                               | Trust damage, support load, legal exposure in several regimes | Specific reason string + published appeal path, built before the detector                                                                                                                                           |
| Retroactive rule tightening                        | Unenforceable against past referrals; regulator attention     | Publish first, enforce after; grandfather already-earned rewards                                                                                                                                                    |
| Hold window shorter than the refund window         | Referee refunds after payout; reward unrecoverable            | Set hold = refund/chargeback window + processing time, per product line                                                                                                                                             |
| Treating an enthusiastic advocate as a ring        | Top referrer banned; worst possible word of mouth             | Require corroboration beyond graph shape: reward-splitting, refunds, cohort collapse                                                                                                                                |
| Manual review cost exceeds reward value            | Every review is a net loss regardless of accuracy             | Reserve review for rewards above the review cost; B2B default, B2C exception                                                                                                                                        |
| Full KYC on a low-value consumer reward            | Sign-up abandonment dwarfs fraud prevented                    | Stop at payment-instrument verification; KYC is for regulated programs                                                                                                                                              |

## KPIs

- Track:
  - invalid-reward rate (leakage)
  - wrongly-withheld rate from appeals upheld (friction)
  - referred-vs-organic cohort deltas on retention, refund rate and 90-day revenue
  - flag rate against the expected multi-accounting baseline
  - hold-to-release time
  - budget ceiling burn
  - support tickets on denied rewards
- Report leakage and friction in currency on the same unit, side by side - one number alone always misleads.
- Escalate the spec itself when:
  - appeals-upheld rate climbs (rules too tight)
  - cohort quality decays while flag rate stays flat (rings under the radar)
  - the qualifying event's refund rate rises (event too cheap)

## Invocation Examples

- "Our meal-kit box gives $25 to both sides and someone just farmed it with 40 plus-addressed email accounts. Write the guardrails before we relaunch."
- "We're launching give-10-get-10 in our fitness app next month - design the caps, hold policy, and verification gates so it doesn't get gamed on day one."
- "Our B2B SaaS pays $500 in account credit per referred workspace that converts to paid; finance suspects an agency is referring its own shell accounts. Set up the abuse guardrails and review process."

## Reference

- Read [references/abuse-patterns.md](references/abuse-patterns.md) when mapping the abuse surface - the consumer-gaming taxonomy with each pattern's observable tell, plus documented incidents.
- Read [references/guardrail-mechanics.md](references/guardrail-mechanics.md) when setting caps, holds, eligibility rules and verification gates - published values with provenance, the friction ladder, B2B specifics.
- Read [references/detection-signals.md](references/detection-signals.md) when choosing monitoring signals - strength ratings, which signals are degrading, calibration baselines.
- Read [references/enforcement-and-compliance.md](references/enforcement-and-compliance.md) when writing the enforcement ladder, reason strings, appeals, and the legal design constraints.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - one B2C and one B2B filled spec, plus one negative example.
- See `mbfinotti/partnerships-skills@referral-incentive-design` for reward structure (sidedness, type, size, payout trigger, tiers) - this skill protects that structure, never redesigns it.
- See `mbfinotti/partnerships-skills@affiliate-fraud-detection` for professional-affiliate traffic and commission fraud.
- See `mbfinotti/partnerships-skills@affiliate-program-terms` for the consumer refer-a-friend terms wording only when the program also has a professional-affiliate tier.
