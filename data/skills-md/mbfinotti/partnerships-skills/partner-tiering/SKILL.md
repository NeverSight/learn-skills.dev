---
name: partner-tiering
description: Design or redesign the tier structure inside an existing B2B partner program - qualification criteria, benefit bundles, tier count, promotion and demotion rules, review cadence for registered/silver/gold-style ladders, and migration of the current partner base. Also covers the B2C affiliate, creator and loyalty tier contrast. Use whenever the user mentions partner tiers, tier criteria, tier benefits, tier compression, demotion rules, or reseller, MSP and agency tier design, even if they never say tiering. Do NOT use for standing up a partner program from scratch - use mbfinotti/partnerships-skills@partner-channel-program instead. Affiliate commission payout tiers are a separate skill.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.7"
---

# Partner Tiering

Define the criteria and benefits that separate partner tiers inside an existing B2B partner program. No single canonical tier-design methodology exists - say so plainly rather than invent one. What the field actually offers:

- **Forrester's 3-tier norm**: tiering is used by 98% of top IT partner programs, averaging three tiers named "good, better, best" (analyst assertion, not raw survey data).
- **The Alexander Group's three tier mechanics**: volume, engagement, or engagement pathways (points accumulated across multiple dimensions) - the first structural choice a designer makes.
- **Forrester's Channel Partner Segmentation Matrix** (Stephanie Sissler, Feb 2023): a 3x3 current-performance x future-potential grid, explicitly an internal overlay on a public tier ladder, never a replacement for it.
- **Jay McBain's critique** (an attributed practitioner viewpoint, not a framework): revenue is a lagging indicator, and non-transacting partners - tech/ISV, referral, advisory - structurally don't fit a revenue ladder.

## Interview

Ask before designing anything, one question per message. Offer multiple-choice options. Skip whatever the user already answered.

- How many partners, and of which types - reseller, MSP, agency, ISV/tech, referral? Which types actually transact?
- What are the current tiers, their criteria, and the current distribution - how many partners sit in each?
- What is the specific pain: top tier crowded, nobody advancing, benefits ignored, long tail neglected, channel conflict?
- How concentrated is partner-sourced revenue - roughly what share comes from the top 10-20% of partners?
- What does each tier cost to serve today: margin give, deal-registration uplift, MDF, PAM headcount?
- What is the review cadence today, and is demotion actually enforced?
- What is the average sales-cycle length? (Any deal-registration protection window offered as a tier benefit is sized at ≥75% of it, so a window picked from a stock range without this number can be half what the cycle needs.)
- By what date must the new structure be live, and by what date must its results show up in tier movement?
- Is this a one-off fix to a specific pain, or a compounding asset you will re-score every cycle from here on?
- What is the effort ceiling: partner-ops hours, data work available, and the political capital to actually enforce a demotion?
- Is this B2B channel only, or does the program also run B2C-facing affiliate, creator, or loyalty tiers?
- What is immovable: signed partner agreements, fiscal calendar, comp plans?
- Who must sign off: channel chief, CRO, finance, legal?

## Workflow

1. Run the Interview. Collect every current-state fact the design depends on.
2. Confirm scope: refine the tier layer of a program that already exists. Building a program from scratch or fixing individual-partner performance belongs to the sibling skills in the Reference section.
3. Build the baseline: partners, revenue contribution, and cost-to-serve per current tier. Expect a power law - 10-20% of partners driving 70-80% of channel revenue is the commonly cited pattern (PRM-vendor rule of thumb, not an empirical dataset).
4. Decide the tier count (default 3; collapse to 2 below roughly 50 partners) - see [references/distribution-and-cadence.md](references/distribution-and-cadence.md). Then pick the mechanic here, where the choice is actually made:
   - **Volume** - revenue thresholds only. Near-zero to run: the CRM already holds the number. Buys the weakest ranking, because revenue is a lagging indicator and every non-transacting partner scores zero on it.
   - **Engagement** - revenue plus certifications, competencies, or retention. About a quarter to stand up, near-zero per cycle afterwards. Buys criteria a partner cannot dispute at appeal, and a rung non-resellers can climb.
   - **Points pathway** - a published formula scoring several motions at different weights. A standing job: the formula, the per-category minimums, and a recalculation you owe partners every cycle. Buys the finest ranking, and it is the only mechanic that orders a base no single metric ranks correctly.
   - efficiency (best ratio first): `engagement > volume > points pathway`
   - value (ranking power bought): `points pathway > engagement > volume`
   - effort (heaviest first): `points pathway > engagement > volume`
   - Cost gets no line of its own: a mechanic's only cost is the work of running it, so its cost order is its effort order.
   - Default to engagement. Move up to a points pathway when partners transact across several motions - sourced, assisted, managed. No single metric ranks them in an order the channel team will defend.
   - This order starves the points pathway: highest value, highest effort, so it loses every round. Promote it anyway when the program is already losing demotion disputes, or when tier assignments get argued case by case each cycle.
   - Delete volume outright once a material share of the base never transacts. A volume ladder cannot rank those partners at all, and leaving it on the shortlist reinstates the ladder that reads ISV and referral partners as bad partners.
   - Re-rank against the Interview answers:
     - a hard date inside one quarter promotes volume and removes the points pathway from this round
     - a compounding mandate promotes it
     - an effort ceiling with no partner-ops hours removes it
   - Then give non-transacting partner types criteria that fit them, or a separate track.
5. Define qualification and maintenance criteria before touching benefits - criteria decide who lands where; benefits designed first get promised to a population never modelled. See [references/tier-criteria.md](references/tier-criteria.md).
6. Backtest the proposed criteria against the existing partner base:
   - Inspect the resulting distribution against the pass threshold below.
   - Adjust thresholds and rerun.

   This step produces the modelled tier headcount the next one prices against - a bundle costed before the backtest is a guess about a population nobody has counted.

7. Price each tier's benefit bundle and check the exchange balances both ways: the tier's revenue covers its bundle cost, and each step up visibly rewards the partner's climb. See [references/tier-benefits.md](references/tier-benefits.md).
8. Design promotion, demotion, review cadence, measurement window, grace period, grandfathering, and appeals path.
9. Plan migration and socialization: partner advisory council preview, notice period, migration comms, published decision dates.
10. Brainstorm and validate per the next section: candidate structures first, then the spec section by section.
11. Check the pass threshold; iterate criteria, benefits, or tier count until every check holds.
12. Stop at the approval gate - finalize nothing without the user's explicit approval of the full spec.
13. If your harness has persistent memory, memorize the approved structure, thresholds, and first review date; otherwise tell the user to store the spec where partner ops can retrieve it.

If you can browse the web, verify any named vendor structure before citing it - major programs restructured repeatedly across 2022-2026. Otherwise flag vendor examples as possibly stale.

Every ordering in this skill and its reference files - mechanics above, criteria, benefits, cadence and demotion posture in the references - is a default, not a law. It shifts with the program's context and with who executes it.

Re-rank each one against what you already know about this user:

- a live certification registry drops the engagement mechanic's setup to near-zero and it wins outright
- per-motion attribution already built in the warehouse turns the points pathway's standing job into a query
- a channel chief with no political capital for demotions this year changes the cadence order

Say which of the user's facts moved which option, rather than restating the default.

## Brainstorming the structure

Run the design the way channel teams actually run it - a compressed 90-day design sprint, not a single answer:

- Ask one question per message throughout; never batch questions.
- Assemble the data channel professionals bring to the table: partner P&L, sourced-revenue distribution, cost-to-serve, PSAT/NPS, portal-engagement signals. Model with what exists; name what is missing.
- Map the RACI: channel chief accountable, partner ops runs the model, partner marketing owns migration comms, finance validates margin, legal amends agreements, CRO defends the program.
- Segment the base first (partner type x size x economic potential); overlay the Forrester 3x3 grid internally to sanity-check where key partners would land.
- Present 2-3 candidate tier structures built from the ranked mechanics in workflow step 4: lead with the one that ranking recommends for this base, then say what would have to be true for each alternative to beat it.
- Once the user picks a direction, present the spec one section at a time - criteria, then benefits, then cadence, then migration - and validate each before writing the next.
- Recommend socializing the near-final structure through a partner advisory council before any public announcement; a tier change is negotiated and relationship-bound, not shipped.
- Gate finalization on explicit user approval of the assembled spec.

## The Tier Structure Spec

Deliver the engagement as this artifact - a decision record the user hands to partner ops, finance, and legal:

```
TIER STRUCTURE - <program>, <date>
Mechanic         : volume | engagement | points pathway, with the point formula if points
Tier count       : N, and why not N-1 or N+1
Per tier (repeat for each, bottom to top):
  Name           : partner-facing, repeatable (never "Tier 2")
  Qualification  : criteria + thresholds + measurement window + data source
  Maintenance    : what keeps the tier at each review checkpoint
  Benefits       : bundle, each benefit with its modelled unit cost
  Modelled count : partners qualifying today (from the backtest) + % of base
  Cost-to-serve  : modelled annual bundle cost at that headcount
  Revenue        : modelled contribution of that cohort
Program level:
  Review cadence : recalculation moment + rolling vs fixed window
  Grace period   : length before a demotion takes effect
  Appeals        : path + named decision owner + published decision dates
  Grandfathering : who keeps status through migration, until when
  Migration plan : notice period, advisory-council preview, comms milestones
  Validation     : pilot cohort or model checks before full launch
  KPIs           : from the KPI section, with the first review date
```

Rules about the spec itself:

- Attach a measurement window and data source to every threshold - a criterion nobody can compute demotes nobody.
- Carry a reason on every line ("top tier requires 80% gross revenue retention - gates co-sell on retention quality"); a bare number is not reviewable.
- Reject any criterion a partner can self-report or game; use only data the program itself records and can defend in a dispute.
- Treat backtested counts as mandatory: a structure never run against the real partner base is a guess, not a design.

## Pass threshold

Ship nothing until all four hold; iterate the design until they do:

1. **Reachable, not crowded.** The top tier is attainable by roughly >=10% of partners (PRM-vendor heuristic, not an empirical benchmark). If far more qualify, thresholds lag the base - escalate them.
2. **Visible economic differential at every adjacent step.** A ~2% discount bump plus a nicer badge is the documented failure: partners rationally decline to climb.
3. **Every tier self-funding.** Each tier's modelled benefit-bundle cost sits below that tier's modelled revenue contribution.
4. **Nothing gameable.** No criterion is self-reported or manipulable - logo counts and self-reported pipeline are the documented gaming vectors.

## Diagnosing an existing tier structure

When the user arrives with a running structure instead of a blank page, find their symptom in the table - rows are keyed by symptom, not by priority.

When several symptoms are present at once, fix in this order, ranked by efficiency, not severity:

`criteria thresholds > benefit differentiation > cadence, grace and comms > benefit allocation to the middle > tier count`

- Escalating a threshold is a spreadsheet change against data the program already holds, and it lands at the next review.
- Collapsing the tier count is a migration, a comms plan, and an agreement amendment, so it pays last, even when the bloat is what the user came in complaining about.

A crowded top tier and an unexplainable ladder are usually the same disease, and the threshold fix cures both.

The tier count is what that order starves - the highest-value fix on the list, ranked last on effort alone, so a ratio defers it every cycle while thresholds get re-escalated on a ladder nobody could explain in the first place. Promote it when adjacent tiers stop differing on both criteria and benefits, or when a migration is already happening for another reason and the count can ride along at no extra comms cost. Strike any row the program's constraints rule out and say it is struck - signed agreements that fix the current benefit bundle remove the differentiation row this cycle - rather than leaving it at the bottom, where it returns as work nobody scoped.

| Symptom                                             | Check first                                                                | Design variable at fault                                |
| --------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------- |
| Tiers nobody can explain (5+, overlapping criteria) | Whether adjacent tiers differ on both criteria and benefits                | Tier count - collapse                                   |
| Top tier crowded (compression)                      | When thresholds were last raised vs base growth                            | Criteria thresholds - escalate                          |
| Nobody advances; partners stall at entry            | Threshold curve: too easy at bottom, too hard at top; cliffs between steps | Threshold spacing                                       |
| Partners ignore the ladder, won't invest            | Economic differential per step: discount, deal-reg uplift, rebate          | Benefit differentiation                                 |
| Benefits allocated but unused (MDF unclaimed)       | Claim friction and partner marketing bandwidth                             | Benefit design, not criteria                            |
| Tier metrics look great, results don't              | Which criteria are self-reported (pipeline, logos)                         | Criteria gameability                                    |
| Long tail dormant                                   | Investment share reaching mid and low tiers                                | Benefit allocation - fix the middle before adding tiers |
| Deal fights between partners or with direct sales   | Consistency of deal-registration enforcement                               | Benefit enforcement, not structure                      |
| Churn spikes after review dates                     | Demotion surprise: notice, grace period, appeals                           | Cadence, grace, and comms                               |

## KPIs

Judge the tier structure itself, not individual partners (individual scorecards belong to `mbfinotti/partnerships-skills@partner-performance`):

- Tier distribution shape across successive review periods - drift toward compression or an empty middle.
- Share of partners advancing per review period.
- Revenue per tier vs cost-to-serve per tier.
- Benefit utilization rate, especially MDF claim rate: 40-60% commonly goes unclaimed (recurring industry figure sourced).
- Partner satisfaction (PSAT/NPS) by tier.
- Post-demotion churn vs baseline partner churn.

## B2B vs B2C

Identical in both worlds: the power-law concentration, the threshold-gated qualify → status → perks → requalify loop, the tier-count rule above (3 by default, collapsing to 2 below roughly 50 partners), and the failure modes above.

Different - design for the difference:

- **Currency of progression**: B2B channel = revenue + certifications + CSAT/retention; affiliate/creator = sales or GMV on a rolling window; consumer loyalty = annual qualifying spend, nights, or miles.
- **Reset cadence**: B2B = rolling or annual with grace; affiliate = rolling; consumer loyalty = a hard annual status clock.
- **Human touch**: B2B = PAM coverage and QBRs; B2C = self-serve automation end to end.
- **Testability**: an affiliate or consumer ladder can be A/B tested across a large base; a B2B tier change is negotiated, relationship-bound, and socialized through a partner advisory council - model and pilot it instead.

See [references/worked-examples.md](references/worked-examples.md) for the full contrast with real vendor examples.

## Invocation Examples

- "Everyone gets a flat 20% discount and our top partners are asking what more they get. Design the tier ladder - 160 partners."
- "Our top tier is overcrowded and demotion has never been enforced. Fix the criteria and plan the migration."
- "We have 25 non-transacting ISV partners who cannot qualify for any tier. Give them criteria that fit."

## Reference

- See [references/tier-criteria.md](references/tier-criteria.md) for the criteria menu, points-model weighting, measurement windows, gameability checks, and criteria for non-transacting partner types.
- See [references/tier-benefits.md](references/tier-benefits.md) for the benefit menu with real costs, bundle pricing, and a negative example of a non-differentiated ladder.
- See [references/distribution-and-cadence.md](references/distribution-and-cadence.md) for tier count, backtesting, target distribution, cadence, promotion/demotion, grace, grandfathering, appeals, and tier-inflation control.
- See [references/worked-examples.md](references/worked-examples.md) for real 2023-2026 vendor structures decomposed, one fully worked tier structure, and the B2C contrast.
- See `mbfinotti/partnerships-skills@partner-channel-program` to design a whole partner program from scratch - this skill only refines the tier layer inside one.
- See `mbfinotti/partnerships-skills@partner-performance` for individual partner scorecards, QBR structure, and underperformance triggers.
- See `mbfinotti/partnerships-skills@affiliate-commission-structure` for commission payout tiers aimed at professional affiliates - a different discipline from channel tiering.
