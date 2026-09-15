---
name: affiliate-fraud-detection
description: Build the detection rule set an affiliate program manager uses to flag fraudulent affiliate activity, plus the investigation and escalation path behind it  -  cookie stuffing, fake lead and form-fill fraud, self-referral rings, traffic-quality baselines, commission holds and clawbacks, and separating real fraud from legitimate low-incrementality coupon or cashback partners. Covers B2B SaaS lead-gen and B2C ecommerce programs. Use whenever the user mentions affiliate fraud, suspicious affiliate traffic, invalid clicks or leads, bot traffic, or an affiliate whose numbers look too good, even if they never say fraud. Do NOT use for consumer refer-a-friend gaming  -  use mbfinotti/partnerships-skills@referral-abuse-guardrails instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.1"
---

# Affiliate Fraud Detection

Build the rule set a program owner uses to flag fraudulent affiliate activity, then investigate and escalate it. This is a defensive skill: it protects programs from being defrauded, and describes each fraud pattern only to the depth needed to recognize it.

No canonical affiliate-fraud detection framework exists. The only ratified standard is the IAB/MRC invalid-traffic split, an ad-measurement standard the affiliate industry borrows rather than one written for affiliate programs:

- **GIVT** - caught by routine list filtration: known bots, data-center IPs, non-browser user agents.
- **SIVT** - needs advanced analytics and corroboration: hijacked devices, adware, cookie stuffing.

The PMA's Toolbar and Software Industry Standard is a voluntary, non-binding proposal, not a ratified standard. Force-fit no other framework.

The single highest-leverage control is a commission hold/validation window of 30-90 days, not a detection algorithm. The strongest independent evidence agrees: Edelman's research (related to Edelman & Brandi, _JMR_ 2015) found delaying affiliate payments by two to four months could eliminate more than 70% of fraud without decreasing profit.

## Control Leverage

Four controls compete for the hours before the next payout cycle. Rank them before writing a single rule.

- value (most first): `hold window > clawback clause set > detection rule set > new-partner terms`
- effort (most first): `clawback clause set > detection rule set > new-partner terms == hold window`
- compliance cost (most first): `clawback clause set > hold window == new-partner terms > detection rule set`
- efficiency (best first): `hold window > detection rule set > new-partner terms > clawback clause set`

| Control                                                        | What it buys                                                                                                                     | What it costs                                                                                                                                                                                     |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hold/validation window, 30-90 days                             | Most fraudulent commissions never leave the account - the >70%-of-fraud result above, at no cost to profit                       | An hour: one platform setting, reversible the day it changes. Alters terms a partner already accepted, so it carries a notice obligation                                                          |
| Detection rule set (this skill's deliverable)                  | Names which partner to act on and produces evidence an enforcement action can stand on                                           | A week to derive baselines and write rules, then a standing triage job. Near-zero compliance cost until a rule reads cross-account identity data, which inherits the `[LEGAL REVIEW]` gate        |
| New/high-risk partner terms (net-60/90, stricter filters)      | Narrows exposure to the cohort that produces most first-incident fraud                                                           | An hour, and tied with the hold window on both effort and exposure for a real reason: same settings page, same person, same reversibility, same notice obligation - only the edited field differs |
| Clawback + negative-balance carry-forward + chargeback reserve | The only control that recovers money already paid, and the sole cover for the 120-540 day chargeback tail no hold window reaches | A quarter: legal drafting and partner re-assent, barely reversible once shipped. Clawing back a paid commission without these clauses is itself a breach                                          |

Set the hold window first, then build the rule set; a program missing both has no working control however good its detection gets.

The efficiency order starves the clawback clause set - top of the value axis, bottom of the ratio, so it loses every round. Promote it above everything else when the program sells subscriptions, high-ticket, or delayed-delivery goods, or has already paid out on a chargeback: there, the only control that touches money already gone is the one the ratio ranks last.

## Re-Rank Before Delivering

Every ordering in this skill is a default, not a law. It shifts with the program and with who executes it, so re-rank it against what the Interview told you:

- The platform cannot configure a hold window → delete that rung from the deliverable and say so. A ruled-out control parked at the bottom of a plan comes back as scope. What remains is `rule set > new-partner terms > clawback clause set`, and the clawback clauses stop being optional.
- Nobody has review hours → the 24-48h review under Hold & Investigate never happens. Route the rule set to Watch plus one monthly batch review, and let the hold window carry the program.
- The roster is small enough to read by hand, roughly under 20 partners → 2-SD outlier math and per-event scoring are false precision on that sample. Inspect the partner list and skip the statistical rungs.
- The user already owns something the order assumes away - server-side postbacks, a fraud analyst, a standing chargeback reserve - promote whatever that asset makes cheap.

## Ground Rules

- Recognize, never perpetrate: state the observable tell each pattern leaves in program data; write no evasion or how-to-build detail.
- Label every numeric threshold with its provenance: vendor/agency rule of thumb, academic result, or a baseline the user derives from their own data. Never present a vendor heuristic as an industry constant.
- Warn off headline loss statistics: the famous "17% of affiliate traffic is fake / $3.4B" figure is single-vendor marketing with circular citation.
- Treat low incrementality as a repricing problem, never as fraud. Coupon, cashback, loyalty, extension, retargeting, and brand-search partners are legitimate by default.
- Keep B2B and B2C signals separate. Say explicitly when a rule applies to both.
  - B2C fraud: a stolen-attribution sale, visible in click-timing, cookie-drop, and chargeback signals within hours-to-days.
  - B2B lead-gen fraud: a fake form-fill whose worthlessness surfaces weeks later in downstream rates.
- Never assume the network does the policing: networks earn a share of commission volume, so their compliance is reactive - it acts on evidence-backed complaints, not brand-specific surveillance.
- Expect AI-generated synthetic traffic to degrade behavioral heuristics (session duration, scroll depth); treat recent vendor detection-efficacy claims as unverified and weight server-side and downstream-outcome signals instead.

## Interview

Ask before building anything:

- One question per message.
- Multiple-choice where possible.
- Skip anything already answered.

Ask the first three questions below before any of the rest: the controls diverge by two orders of magnitude in time-to-effect and effort, and the answers decide the order everything downstream is delivered in.

- By when must this rule set be protecting money - the next payout cycle, or a quarter out? A cycle puts the whole load on the hold window and band assignment and rules the clawback clause set out of scope; a quarter puts contract changes back on the table.
- One-off cleanup of a partner you already suspect, or a standing control that compounds? One-off promotes the dossier and enforcement path and skips baseline derivation; standing promotes baselines, monitoring cadence, and the KPI loop.
- Effort ceiling: how many review hours per week, who can amend partner terms, and who signs off on suspending a partner? No review capacity collapses Hold & Investigate into Watch; no contract authority deletes the clawback rung outright.
- Program size: how many active affiliates, and roughly what monthly commission spend?
- B2B lead-gen, B2C ecommerce, or both?
- Which partner types and traffic sources are permitted: coupon, cashback, loyalty, browser extensions, paid search (brand bidding allowed?), email?
- Tracking and attribution: last-click? Cookie window length? Client-side pixel or server-side postback?
- Commission validation/hold window today, if any? Is clawback contractually authorized (negative-balance carry-forward, chargeback reserve)?
- Any historical fraud incidents? What happened, and was any commission recovered?
- Exactly which data can you query: click logs, conversion records, IP/device data, CRM lead outcomes, refund/chargeback records?

## Workflow

1. Run the Interview; collect every answer the rule set depends on.
2. Confirm the scope boundary: this rule set flags illegitimate activity. Payout math, contract clauses, and refer-a-friend gaming belong to sibling skills (see Reference).
3. Rank the four controls against those answers using Control Leverage above, then fix the money mechanics before writing a single rule. A rule set sitting on a 14-day hold window with no clawback authority flags fraud the program cannot act on.
4. Derive baselines from at least 90 days of the user's own per-affiliate data: conversion rate, click-to-conversion time, refund/chargeback rate, and for B2B the lead-to-qualified and lead-to-demo-show rates. Read [references/detection-signals.md](references/detection-signals.md) for the signal catalogue and starting thresholds.
5. Map the program's fraud surface from [references/fraud-taxonomy.md](references/fraud-taxonomy.md): which patterns the permitted partner types and tracking setup actually expose it to.
6. Draft the rule set in the Output Shape below: one row per rule, each carrying signal, threshold with provenance, severity band, and mandated action.
7. Add false-positive protections from [references/false-positives-and-incrementality.md](references/false-positives-and-incrementality.md): exclude legitimate checkout-moment partner behavior from fraud rules and route non-incrementality suspicions to holdout/geo testing instead.
8. Attach the operating procedure from [references/investigation-and-enforcement.md](references/investigation-and-enforcement.md): monitoring cadence, evidence collection, dossier, escalation ladder, appeals, and clawback mechanics.
9. Backtest against the Pass Threshold below; tune thresholds and iterate until both halves hold.
10. Present the rule set section by section for user validation; deliver the full artifact with dossier template and KPI plan. Ground it in a matching worked example from [references/worked-examples.md](references/worked-examples.md).
11. If your harness has persistent memory, memorize the derived baselines, decided thresholds, and permitted-partner decisions so a later run starts from them instead of re-deriving.

## Output Shape

Deliver a rule set where every rule reads: signal → threshold (with provenance tag) → severity band → mandated action. Three bands, listed below in efficiency order rather than severity order:

- value (most first): `Suspend & Escalate > Hold & Investigate > Watch`
- effort (most first): `Suspend & Escalate > Hold & Investigate > Watch`
- compliance cost (most first): `Suspend & Escalate > Hold & Investigate > Watch`
- efficiency (best first): `Hold & Investigate > Watch > Suspend & Escalate`

The first three axes agree, which is exactly why the fourth decides: severity buys more the further up the ladder the response climbs and costs more at the same rate, so the band that stops the money for hours of reversible work wins.

- **Hold & Investigate** (ladder tier 2) - auto-throttle new commissions to zero pending review, open a dossier, cross-functional review within 24-48 hours. Throttling preserves evidence an instant ban destroys. Costs hours per case: the throttle is one switch, the review is two people's attention for a day or two. Withholding a commission is a contractual act but a reversible one - pay it and the partner is whole. Highest ratio of the three, and the source of the evidence the band above needs.
- **Watch** (ladder tier 1) - log the flag, keep paying, review at the weekly triage. For soft anomalies and first offenses of minor rules. Near-zero cost: a log line and a slot in a meeting that already happens, nothing withheld, no relationship damage, nothing to appeal. Protects nothing on its own, and earns its place only by feeding Hold & Investigate.
- **Suspend & Escalate** (ladder tier 3) - suspend the account, reverse violation-period commissions, forward the dossier to network compliance and, where warranted, legal review. Costs a week per case plus the partner relationship outright: dossier completion, sign-off, network filing, appeal handling. Least reversible and most exposed of the three - suspension can breach published terms, and an unfounded fraud allegation is its own liability.

Assign a new rule to Hold & Investigate by default. Move it down to Watch when the signal alone has a plausible legitimate cause; move it up to Suspend & Escalate only on confirmed technical evidence, stolen-card chargebacks, or reoffense after a warning.

The efficiency order starves Suspend & Escalate: a program ranking by ratio alone throttles forever and terminates nobody, and a ring that learns the program never bans simply absorbs the throttles. Promote it whenever confirmed-fraud rate or reversed-commission share climbs quarter over quarter, and whenever a case has to survive network compliance, where a throttle carries no weight.

Every band assignment carries the false-positive caveat inline: name the legitimate behavior that could trip the rule and the check that separates it.

Each investigation opens a dossier with these fields: affiliate ID and network/platform ID; rule(s) triggered with timestamps; baseline vs observed values; evidence artifacts (cookie-drop reproduction steps, redirect-chain capture, timestamped screenshots, server-log excerpts); financial exposure (commissions held, paid, at risk); declared traffic source vs observed referrers; prior warnings and history; recommended action with reviewer name; appeal status and deadline.

## Pass Threshold

Judge the rule set on its detection rate and false-positive rate as a pair - every credible source tracks catch rate and false-positive rate together, never catch rate alone.

- Backtest against historical confirmed incidents and a random sample of flagged and unflagged partners reviewed manually.
- Pass when both hold: at least 80% of known incidents fire at Hold & Investigate or above, and at most 5% of sampled flags are false positives.
- Provenance of the pair: published fraud-ops checklists converge on a >80% catch target with a low-single-digit false-positive ceiling; the academic ceiling for a simple rule is Snyder & Kanich's two-feature timing classifier at ~2-second thresholds - 93.3% accuracy, 1.5% false positive, 5.2% false negative (_Journal of Cybersecurity_ 2016). These are calibration anchors, not industry constants.
- No incident history to backtest against? Say so in the deliverable and schedule the threshold as a first-quarterly-review gate on sampled flags.
- Iterate thresholds until both halves pass; if they cannot, the deliverable states which data or history is missing rather than shipping an untested rule set.

## Common Failure Modes

| Defect                                                                     | Consequence                                                                  | Fix                                                                                       |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Fraud rules fire on legitimate coupon/cashback/loyalty last-click behavior | Terminates real partners; legal and relationship damage                      | Classify partner types; route incrementality doubts to holdout/geo tests, not enforcement |
| Over-blocking on untuned vendor thresholds                                 | Real partners churn; program revenue drops                                   | Derive own baselines from 90 days of data; vendor numbers are starting points only        |
| Validation window shorter than chargeback window                           | Stolen-card commissions paid out are unrecoverable                           | Clawback + negative-balance carry-forward + chargeback reserve in the contract            |
| B2C click-timing rules applied to B2B lead-gen (or vice versa)             | False positives in B2B; missed fake form-fills; missed B2C attribution theft | Split the rule set by motion; B2B leans on downstream rates                               |
| Trusting the network to police the program                                 | Fraud runs until an outsider complains                                       | Own the monitoring; send evidence dossiers to the network, expect nothing unprompted      |
| Treating a vendor benchmark as the program's baseline                      | Thresholds miscalibrated in both directions                                  | Provenance-tag every number; replace with derived baselines                               |
| Instant ban on first flag                                                  | Evidence destroyed; no dossier survives for network/legal escalation         | Auto-throttle to zero pending review; ban only after the dossier is complete              |

## KPIs

- Track: flagged rate, confirmed-fraud rate, false-positive rate from sampled review, reversed-commission share, recovered spend.
- Report to leadership in commission-loss dollars saved and recovered - never vague risk language.
- Escalate the program itself when confirmed-fraud rate or reversed-commission share climbs materially quarter over quarter: revisit hold windows, partner vetting, and tooling.

## Invocation Examples

- "We run a B2B SaaS partner program paying $150 per qualified lead - sales says half the leads from two new affiliates never answer the phone. Build me detection rules."
- "Our ecommerce affiliate program just ate $12K in chargebacks traced to one affiliate's 'sales'. Set up a fraud rule set and an investigation process before we pay the next cycle."
- "Audit our affiliate traffic quality: 60% of commissions go to coupon extensions and I can't tell poaching from fraud."

## Reference

- `mbfinotti/partnerships-skills@affiliate-payout-audit` - accuracy of legitimate-activity payouts; this skill flags illegitimate activity upstream.
- `mbfinotti/partnerships-skills@affiliate-program-terms` - write prohibited-tactics clauses and enforcement ladder into the contract - this skill detects operational violations.
- `mbfinotti/partnerships-skills@affiliate-commission-structure` - reprice non-incremental partners; repricing is that skill's job, not enforcement's.
- `mbfinotti/partnerships-skills@referral-abuse-guardrails` - consumer refer-a-friend gaming - this skill covers professional-affiliate traffic and commission fraud.
