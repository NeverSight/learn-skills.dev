---
name: partner-channel-conflict
description: Write the channel conflict rules that govern contested deals between direct sales and channel partners or between partners - rules of engagement, account segmentation, named-account carve-outs, deal registration as a claim instrument (protection window, tie-break, rejection grounds), compensation neutrality for direct reps, escalation and adjudication ladders, and governance cadence. Also covers consumer brands (D2C vs retail conflict, MAP policy, channel-exclusive assortment). Use whenever the user mentions channel conflict, partner disputes, deal poaching, or two routes to market claiming the same account, even if they never say conflict. Do NOT use for designing the co-sell operating model - use mbfinotti/partnerships-skills@co-selling-strategy instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.9"
---

# Partner Channel Conflict Rules

Write the rules that decide who owns a contested deal when direct sales and channel partners, or two partners, claim the same account, and the governance that enforces them.

The deliverable is a rules-of-engagement (RoE) artifact plus its adjudication machinery:

- Structural boundaries.
- A registration-based claim policy.
- An escalation ladder with a named adjudicator.
- A compensation-neutrality decision.
- A governance cadence.

Diagnosis anchors on two frameworks: the vertical / horizontal / multichannel conflict typology (Stern & El-Ansary, _Marketing Channels_, 1977; current edition Palmatier, Sivadas, Stern & El-Ansary, _Marketing Channel Strategy: An Omni-Channel Approach_, 9th ed., 2019), and the latent → perceived → felt → manifest stage progression. Resolution gets harder at each later stage, which is the whole argument for writing rules before the first manifest dispute. Forrester's _Mitigating Channel Conflict: Rules Of Engagement_ is the on-point analyst artifact for the deliverable's shape.

Boundaries, said out loud:

- `mbfinotti/partnerships-skills@partner-ecosystem` detects and measures conflict zones (account overlap, coverage gaps) and hands off here. This skill starts where detection stops.
- `mbfinotti/partnerships-skills@co-selling-strategy` owns how direct and partners collaborate on shared deals. Deal registration appears here only as a conflict-prevention and claim-adjudication instrument: the protection window, the tie-break, the rejection grounds, and what happens when two parties claim the same deal.

## Interview

Ask before proposing anything: one question per message, multiple-choice when possible, skip anything the user already answered.

- B2B, B2C, or hybrid?
- What does the company sell, and through which motions - direct, resell, referral, co-sell, marketplace-transacted, D2C, retail?
- Sales org shape, and how are direct reps compensated today on a partner-involved deal - neutral, penalized, undefined? (This answer outweighs every other.)
- Which partner types exist, and roughly how many are active?
- What is the average sales-cycle length, in days? (It sizes the registration protection window - the pass threshold requires at least 75% of it, so a window set without this number is a guess.)
- Where does conflict actually show up today, with what evidence - logged disputes, partner complaints, deals lost to infighting, or only anecdote?
- Are registrations visible in the CRM system of record at opportunity creation, or only in a partner portal the direct team never opens?
- What artifacts already exist: rules of engagement, named-account list, registration policy, comp-plan language on partner deals?
- Escalation culture: when disputes escalate today, does direct sales always win?
- Who must sign off: channel chief, CRO, deal desk, legal?
- Geography - any EU presence? EU rules constrain territory, termination, and pricing clauses (flag for counsel).
- By what date must the rules be in force - is a live dispute or a deadline driving this, or is it open-ended? (A hard date promotes the fast-acting rungs - a deal-size threshold, double comp, a QBR agenda item - and demotes named-account lists and a Partner Advisory Council, which only pay off over quarters.)
- A one-off fix for the disputes on the table now, or a compounding governance asset? (Compounding promotes the alignment workshop, the Partner Advisory Council, and named accounts. One-off promotes a threshold, published rules and a neutral adjudicator, and nothing beyond them.)
- Effort ceiling: who maintains this after publication, for how many hours a quarter, and how much political capital do you hold in the direct sales line? (No list owner rules out the named-account axis. No capital in the sales line means comp neutrality will not clear, so the structural axes carry the whole load.)

## Workflow

Hold one discipline throughout: wherever a real choice exists - segmentation axis, protection-window length, tie-break rule, comp-neutrality variant, adjudicator seat - present 2-3 candidates with trade-offs and a recommendation, then wait. Present the deliverable section by section, validating each with the user before drafting the next, with an explicit approval gate before finalizing.

Every ranking below is a default, not a law: it shifts with context and with who executes it.

Re-rank against the Interview answers and against what you already know about this company:

- A CRM that already carries the segmentation field makes that axis nearly free.
- An account-list owner already in post removes the standing cost of named accounts.
- An existing deal desk absorbs the adjudicator seat.

Say which fact moved which option when presenting the order. Strike the options the answers rule out where each menu is presented, rather than carrying them to the bottom of the list.

1. Run the Interview.
2. Classify each reported conflict with the typology: vertical (direct vs partner), horizontal (partner vs partner), multichannel (route vs route; D2C vs retail for consumer brands). Locate it on the latent → perceived → felt → manifest progression:
   - Latent conflict gets structural rules.
   - Manifest conflict needs an adjudicated case and visible remediation before any new rule will be believed.
3. Audit the economics before writing any rule.

   Compensation neutrality: the direct rep paid, or quota retired, at the same rate whether or not a partner is involved. It is the most-cited real control in this field. A program with elaborate rules of engagement but non-neutral comp is structurally conflicted no matter how good the document is.

   Specific trap: reps paid on the discounted price the partner pays, rather than the customer price, predicts persistent vertical conflict.

   Honest caveat: the direction is practitioner consensus, the magnitude figures are single-sourced and vendor-interested.

   Variants ranked by efficiency, with the axes on which cost and behavior change disagree: [references/compensation-and-incentives.md](references/compensation-and-incentives.md).

4. Set the structural boundaries. Pick the segmentation axis on conflict prevented per unit of ongoing effort, not on precision - precision is what makes named accounts look like the obvious first move:
   - efficiency: deal-size threshold > motion carve-out > geography > product line > named accounts
   - value: named accounts > deal-size threshold > geography > motion carve-out > product line
   - effort: named accounts (a standing job - owner, refresh cadence, edge-case rules) > geography (a week to map, plus counsel where territories are exclusive) > motion carve-out == product line (an hour to write, then a recurring edge-case ruling on renewals or bundles) > deal-size threshold (an hour, then nothing)
   - compliance cost: geography (EU territory exclusivity and active/passive-sales limits - counsel before publication) > every other axis (near-zero)

   Motion carve-out and product line tie on effort for a reason, not to duck the call: each is one sentence in the RoE, and neither carries an owner or a refresh cadence. Both buy the same recurring bill of edge-case rulings: a renewal on a carved-out motion, a bundle spanning two product lines.

   They part company on value, and the motion carve-out wins that axis outright.

   What this order starves is named accounts: first on value, first on effort, dead last on efficiency, so a ratio demotes it every single round. Yet it is the only axis that resolves disputes on the accounts a company actually argues about.

   Promote it when disputes cluster on a handful of strategic accounts _and_ a list owner already exists. It is the one axis that becomes a conflict source of its own when it goes stale.

   Where no owner exists, delete it from this menu and say in the RoE that the program has no named-account axis. An axis parked at the bottom "for later" returns as a list nobody maintains, which is the failure mode below.

   Same rule for the axes the Interview already rules out: a single-product portfolio deletes product line, a single-region footprint deletes geography, and both get named as deleted rather than listed as future phases.

   Default: a deal-size threshold plus one motion carve-out - most programs need exactly two axes. Where named accounts survive the test above, define the house/named lists with that owner and a refresh cadence, and keep the list and the conflict rules in an RoE exhibit rather than the signed contract, so they update without re-papering every partner. See [references/rules-of-engagement-artifact.md](references/rules-of-engagement-artifact.md).

5. Define the claim instrument:
   - Registration eligibility.
   - Required data.
   - Protection window (30-180 days observed, 90 most common, at least ~75% of average sales-cycle length).
   - Approval SLA.
   - Extension and expiry.
   - Standard rejection grounds.
   - Tie-break: first-to-register, with a substantial-work test, vendor discretion as fallback.

   See [references/deal-registration-and-claims.md](references/deal-registration-and-claims.md).

6. Design the escalation and adjudication ladder:
   - Tiers with triggers, adjudicator, SLA.
   - A written evidence standard: registration timestamp, first-engagement timeline, activity logs, never seniority.

   Name a neutral adjudicator who is not the direct sales leader, and define remediation for whichever side loses. See [references/escalation-and-adjudication.md](references/escalation-and-adjudication.md).

7. Set the governance cadence and metrics. Rank the forums on conflict prevented per unit of standing effort:
   - efficiency: QBR standing agenda item > channel alignment workshop > joint account planning > Partner Advisory Council
   - value: channel alignment workshop (grounds the rules in where conflict actually lives) > Partner Advisory Council (rule changes partners accept before publication) > joint account planning (per-account ownership agreed before a dispute exists) > QBR item (drift stays visible)
   - effort: Partner Advisory Council (a standing job) > channel alignment workshop (a week, once, at drafting or rewrite) > joint account planning (a day per named account per cycle) > QBR item (near-zero - one line on a meeting that already happens)

   The starved forum here is the Partner Advisory Council: second on value, first on effort, last on efficiency, so it never survives a ratio. Yet it is the only forum that gets partners to accept a rule change before it is published, rather than dispute it afterwards.

   Promote it when a rewrite touches money partners already earn (margin, protection window, registration eligibility), where publishing unilaterally costs more trust than the council costs hours.

   Where nobody can staff a standing job, delete it from the governance plan and say so. A council listed as a future forum reads as consultation partners never actually get.

   Default: the QBR item plus one alignment workshop at drafting. Add joint account planning once named accounts exist, and delete it outright where the named-account axis was struck in step 4, since there are no accounts to plan against.

   Run design sessions in these formats: this profession has its own, so never substitute generic brainstorming. Start the metrics on the registration rejection-reason mix. The full ranking is in [references/governance-cadence-and-metrics.md](references/governance-cadence-and-metrics.md).

8. Publish and enforce:
   - Rules live where partners actually read them (the partner portal, not an internal drive).
   - Registrations write to the CRM system of record so overlap is visible at opportunity creation.
   - Executive backing is named inside the document: it is part of the artifact, not a nicety.

   An unenforced rule destroys partner trust faster than no rule.

9. Validate against the Pass Threshold. Iterate until every criterion holds.
10. If your harness has persistent memory, memorize the approved rules of engagement, the named-account carve-outs, and the adjudication precedents so a later run starts from them instead of re-interviewing.

## Pass Threshold

The rules are done when all of these hold. Iterate until they do:

- **Comp neutrality decided** - and the decision written into both the partner agreement and the direct comp plan, not just one.
- **Registration visible in the CRM at opportunity creation**, not only at booking or inside a disconnected portal.
- **Protection window ≥ ~75% of average sales-cycle length.**
- **Adjudication SLA defined per escalation tier** - 48-hour decision at the working-level and neutral-adjudicator tiers, up to 5 business days at the executive tier for precedent-setting disputes and appeals. Do not apply the 48-hour figure to the executive rung: both numbers are this field's convention. Keep this separate from the registration _approval_ SLA, which is 24-48h and is a different clock.
- **A named adjudicator who is not the direct sales leader.**
- **A documented tie-break** for two claims on the same deal.
- **Remediation defined for the losing side** of every adjudication.
- **Every quoted benchmark carries a provenance flag** - this field's numbers are mostly vendor-published marketing. Label primary, trade, and vendor claims apart.
- **Rules published where partners can actually read them.**

## The Rules of Engagement Artifact

Deliver the approved rules as this artifact - full section anatomy in [references/rules-of-engagement-artifact.md](references/rules-of-engagement-artifact.md):

```
RULES OF ENGAGEMENT: <company>, <version>, <date>, <named executive sponsor>
Segmentation   : which accounts are direct-only, partner-only, shared: and the axis that decides
Account lists  : house/named accounts, list owner, refresh cadence, edge-case rules (kept as an
                 exhibit, updatable without re-papering)
Registration   : eligibility, required data, protection window, approval SLA, extension/expiry,
                 rejection grounds, tie-break
Compensation   : the neutrality statement, mirrored in the direct comp plan
Escalation     : ladder (tier, trigger, adjudicator, SLA), evidence standard, remediation, appeal
Exceptions     : how requested, who grants, where logged
Governance     : review cadence, off-cycle rewrite triggers, where published, amendment procedure
```

## B2B and B2C

Identical on both sides:

- The vertical/horizontal/multichannel taxonomy.
- Misaligned economics (not personality) as the root cause.
- A single system of record.
- Segmentation as the first structural control.
- Pricing consistency across routes.
- The governance cadence.

Genuinely different:

| Dimension         | B2B                                                                         | B2C                                                                                                                |
| ----------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Claim instrument  | Deal registration with a protection window                                  | None - the route-to-market map is the governing artifact                                                           |
| Economic control  | Comp neutrality; margin routing on co-sell and marketplace-transacted deals | MAP as a strictly unilateral policy (antitrust - never negotiated)                                                 |
| Structural lever  | Named accounts, deal-size and motion carve-outs                             | Channel-exclusive assortment / SKU differentiation                                                                 |
| Enforcement       | Contract and comp - the vendor controls both                                | Marketplaces refuse to enforce brand policy; grey-market enforcement via trademark material-difference doctrine    |
| Canonical failure | Direct sales overrides approved registrations                               | Assuming MSRP price parity solves D2C conflict - the conflict is attention, traffic, and trust (the Nike reversal) |

Full contrast, the Nike case with dates and figures, and the US/EU legal boundaries: [references/b2b-b2c-and-legal.md](references/b2b-b2c-and-legal.md).

## Failure Modes

| Failure                                                           | Fix                                                                                                                                                                                                      |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Policy as theatre - rules exist but are not enforced              | Enforce or delete; an unenforced rule destroys partner trust faster than no rule                                                                                                                         |
| Direct sales always wins escalations                              | Neutral adjudicator outside the sales line + comp neutrality; the fix is structural, not behavioral                                                                                                      |
| Registration squatting - partners hoard deals they aren't working | Default expiry plus an activity-based extension test                                                                                                                                                     |
| Portal and CRM disconnected - conflict surfaces at booking        | Registrations write to the CRM at submission; auto-check the account against active pipeline                                                                                                             |
| Stale named-account list becomes a conflict source itself         | Named list owner, refresh cadence, and edge-case rules in the RoE exhibit                                                                                                                                |
| Flat registration incentive regardless of deal size               | Differentiate the uplift; a flat bump fails to surface the large strategic deals you most need visibility into                                                                                           |
| A new process invented per edge case                              | One consistent process; allow multiple roles on one opportunity, split credit by documented contribution                                                                                                 |
| Over-regulating an early-stage program                            | Minimum viable set: registration with conflict detection, published rules, aligned comp, territory boundaries                                                                                            |
| Rules rewritten at every channel-leader turnover                  | Average channel-chief tenure is 4.2 years, 2-3 outside the largest companies (Jay McBain, analysis of 337 channel chiefs) - anchor rules to an executive sponsor and amendment procedure, not one person |
| MSRP price parity assumed to solve D2C conflict                   | The conflict is over attention, traffic, and trust; the structural lever is assortment differentiation, not price alone                                                                                  |

## Invocation Examples

- "Direct reps and two resellers keep claiming the same accounts. Write the rules of engagement - 120-day average cycle, comp currently penalizes partner deals."
- "We need a deal-registration claim policy with a tie-break our partners will accept. Registrations live in a portal our AEs never open."
- "Our D2C store is undercutting our retail partners. Write the route-to-market rules and flag what needs counsel."

## Reference

- [references/rules-of-engagement-artifact.md](references/rules-of-engagement-artifact.md) - RoE anatomy, segmentation axes, account-list staleness and edge cases, document layering, published real examples.
- [references/deal-registration-and-claims.md](references/deal-registration-and-claims.md) - registration as a claim instrument: window sizing, SLA, rejection grounds, tie-break, failure modes, and the honest evidence caveat.
- [references/compensation-and-incentives.md](references/compensation-and-incentives.md) - comp neutrality variants with cost ordering, the partner-price trap, stackable margins, the genuine dissent, provenance flags.
- [references/escalation-and-adjudication.md](references/escalation-and-adjudication.md) - the tiered ladder, evidence standard, neutral-adjudicator seat, remediation, RACI.
- [references/governance-cadence-and-metrics.md](references/governance-cadence-and-metrics.md) - Partner Advisory Council, channel alignment workshop, conflict metrics, review triggers.
- [references/b2b-b2c-and-legal.md](references/b2b-b2c-and-legal.md) - D2C vs retail, MAP and the Colgate doctrine, the Nike case, US/EU legal boundaries (flag for counsel, never legal advice).

Sibling skills (same collection):

- `mbfinotti/partnerships-skills@partner-channel-program` - overall program structure the rules live inside.
- `mbfinotti/partnerships-skills@partner-tiering` - tier criteria and benefits (tiers may earn longer protection windows: the criteria live there).
- `mbfinotti/partnerships-skills@partner-economics` - per-partner unit economics behind the comp decisions.
- `mbfinotti/partnerships-skills@partner-performance` - partner scorecards and QBR structure the conflict metrics feed into.
