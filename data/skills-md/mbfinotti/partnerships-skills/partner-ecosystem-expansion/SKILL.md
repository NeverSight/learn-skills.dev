---
name: partner-ecosystem-expansion
description: Decide which partner categories to add next to a partner ecosystem and in what sequence  -  a staged partner-category expansion roadmap with readiness gates, capacity limits, and kill criteria. Covers B2B categories (tech/ISV, reseller/VAR, MSP, SI/GSI, agency, referral/affiliate, marketplace) and consumer-side equivalents (retail/wholesale, creator, licensing, co-branding). Use whenever the user mentions partner ecosystem expansion, partner category planning, a partner mix roadmap, or asks which partner type to launch next, even if they never say expansion. Category-level sequencing only. Do NOT use for ranking named candidate companies  -  use mbfinotti/partnerships-skills@alliance-prioritization instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.1"
---

# Partner Ecosystem Expansion

Plan which categories of partner to add next and in what order, as a staged roadmap with gates.

Be honest about the evidence before anything else:

- No peer-reviewed optimal partner-category sequence exists.
- Most published "frameworks" for this decision are borrowed strategy grids force-fit onto channels.
- Nearly every quoted benchmark comes from a vendor or consultant that profits when the number looks good.

What the evidence genuinely supports:

- **Adner's minimum viable ecosystem (MVE) + staged expansion + value blueprint** (_The Wide Lens_; _Winning the Right Game_) - the one framework designed for exactly this problem: prove the smallest partner configuration that evidences joint value, then add categories in a deliberate order, gated on evidence.
- **The alliance-portfolio-diversity inverted-U** (Jiang, Tao & Santoro 2010, _SMJ_; Lee et al. 2017 meta-analysis) - the field's only independent evidence: partner-type diversity helps firm performance up to a point, then coordination and governance costs dominate. It argues for restraint and sequencing; it prescribes no order.
- **Operational coverage/capacity math and stage-gate pilots** - unbranded, but the actual working method: gate every category on capacity, not enthusiasm.

McBain/Canalys' channel trifurcation supplies the category taxonomy (never a sequence), and Moore's whole product / bowling alley partially transfers. Name and reject the force-fits when a user brings one: Ansoff applied to channels, McKinsey three horizons, BCG growth-share, Iansiti & Levien for category selection. See [references/sequencing-frameworks.md](references/sequencing-frameworks.md).

This skill sequences categories, never named companies. Related decisions live in sibling skills:

- Ranking named candidates: `mbfinotti/partnerships-skills@alliance-prioritization`
- Mapping the current ecosystem: `mbfinotti/partnerships-skills@partner-ecosystem`
- Program structure (tiers, benefits, requirements): `mbfinotti/partnerships-skills@partner-channel-program`

## Interview

Ask before sequencing anything. One question per message; offer multiple-choice options; skip whatever the user already answered.

- B2B, B2C, or hybrid? What do you sell, to whom, at what price band, through which motion?
- Current ecosystem shape: which partner categories are live today, how many partners per category, and what share are actually active? (An ecosystem map from the mapping sibling is the ideal input.)
- Which existing category is proven - repeatable joint wins, not just signings? Any category still a half-built stub?
- Product readiness: API maturity and multi-tenancy, certification/training content, deal registration, margin structure, support model, contracting - which exist today, which are still on the roadmap?
- Internal capacity: partner managers and their current load, enablement content bandwidth, tooling, program budget?
- How does your buyer actually buy - self-serve, sales-led, through implementers, through retail or marketplaces?
- Goal of the expansion: coverage of a segment/geography/journey stage, a whole-product gap, new-logo pipeline, retention/expansion, margin capture?
- Geography and segment coverage today vs target?
- Budget and sign-off: who funds this, who approves, and is there a planning cycle it must land in?
- Time horizon for the roadmap - 12, 24, or 36 months?

Three answers re-rank the category order before any sequencing starts - ask them here, never beside the ranking:

- **By what date must the first result land?** A hard near-term date promotes the fast-acting categories (referral/affiliate, creator, agency) and deletes the standing-job ones from stage 1 - a category whose first revenue arrives after the date cannot be stage 1 whatever its ratio.
- **A one-off win, or a compounding asset?** Compounding promotes tech/ISV and the categories it makes cheap later (marketplace, MSP); one-off promotes referral/affiliate, creator and co-branding, and demotes everything that only pays back across years.
- **What is the effort ceiling** - hours, headcount, political capital, reversibility? A ceiling below one standing job deletes MSP, SI/GSI, reseller, retail and distributor outright; a ceiling that includes an existing services arm promotes SI/GSI to the front.

## Workflow

Wherever a real choice exists - candidate pool, sequence order, gate thresholds, where the capacity line falls - present 2-3 candidate approaches with trade-offs and your recommendation, then wait. Never let an assumption harden into the roadmap unstated.

1. Run the Interview. Confirm the input is a current-ecosystem picture (a map, or an honest mix description). No picture at all → route to the ecosystem-mapping sibling first.
2. State the evidence posture up front: the roadmap is a reasoned, gated bet, not a validated formula - and every benchmark used will carry a provenance flag.
3. Define the MVE: the smallest partner configuration that creates enough evidence of value to attract the next category. If the current motion is not yet an MVE with repeatable joint wins, the honest roadmap's stage 1 is finishing it, not adding.
4. Run the ego-system check: draft the value blueprint from the customer's position, not yours. A sequence that presumes your own centrality (Adner's ego-system trap) recruits categories that have no reason to show up.
5. Build the candidate pool from the trifurcation buckets - influence, transact, retain-and-deliver - plus the B2C vocabulary where relevant, and from the whole-product gaps each category would close. See [references/partner-category-economics.md](references/partner-category-economics.md).
6. Fix the capacity numbers before sequencing: partner-manager-to-partner ratios, enablement bandwidth, budget. These cap the roadmap; a sequence without them is a wish list.
7. Score each candidate category's readiness and economics: commercial model, relative time-to-first-revenue, effort to stand up, standing load, compliance exposure, prerequisites met vs missing. See [references/readiness-and-capacity-gates.md](references/readiness-and-capacity-gates.md).
8. Rank the pool by efficiency: value returned per unit of effort, never cheapest-first. Use the ordering and the per-axis lines in [references/partner-category-economics.md](references/partner-category-economics.md), then re-rank it against this user: their three interview answers above, an existing services arm, a product needing no implementation, a partner team of one. Delete every category their constraints rule out, with the reason, instead of parking it at the bottom; it lands in `Not now` with a re-entry trigger. Say the ordering out loud, and say what it starves. Draft 2-3 candidate sequences from the re-ranked pool with trade-offs and your recommendation.
9. Argue the strongest case against your own recommended sequence before presenting it: the inverted-U cost of another category, the conflict it creates, the capacity it steals from the proven motion.
10. Attach a stage gate to every stage: pilot cohort shape, a partner-market-fit threshold (repeatable joint wins), and explicit kill criteria. Gates trigger on evidence, never on a calendar date alone.
11. Pre-check channel conflict for any category that overlaps an existing route (direct, or another partner category). Detect and size it here; writing the rules of engagement belongs to `mbfinotti/partnerships-skills@partner-channel-conflict` - but a launch scheduled before rules exist is a roadmap defect.
12. Cost each stage as a capital request: total loaded cost (headcount, enablement build, incentives, tooling, program spend), never headcount alone, with the funding mechanism named.
13. Run the brainstorming discipline below; present the roadmap section by section, validating each with the user before drafting the next. Require explicit approval of the assembled roadmap before finalizing.
14. Check the Pass Threshold; iterate the sequence, gates, or capacity assumptions until every check holds.
15. Set the review cadence and re-sequencing triggers: a gate result, a category's activation collapsing, a product-readiness slip, a conflict incident, a market shift. The roadmap is a standing hypothesis, dated for its next review.
16. If your harness has persistent memory, memorize the approved roadmap - the sequence, each stage's gates and kill criteria, and the capacity numbers - so a later run (a gate review, a re-sequencing) resumes from them instead of re-interviewing.
17. If you can browse the web, verify time-sensitive facts the plan leans on (marketplace policies, a candidate category's structural economics) before finalizing; otherwise flag them as user-supplied and unverified.

## Brainstorming the sequence

Enter brainstorming mode before drafting any roadmap - never open with a finished sequence. Run it in the profession's own formats, not generic ideation.

The five are ranked by efficiency in [references/expansion-workshops.md](references/expansion-workshops.md) - `map re-read > value blueprint > account mapping > partner persona > business-design workshop` - with their question sets and the axes behind that order. Run from the top, confirm the format with the user, and stop when the candidate pool stops changing; the order shifts with what data already exists.

- One question per message, always; never batch.
- Every real choice gets 2-3 candidate approaches with trade-offs and your recommendation - then wait for the user.
- Name assumptions out loud before they harden: which category the room already wants, which readiness claim nobody verified, which capacity number is a guess.
- Argue against your own recommended sequence before presenting it (workflow step 9) - enthusiasm for a category is the documented way this exercise fools itself.
- Present the deliverable section by section - current base, candidate pool, capacity, sequence, gates, costs - each validated before the next is drafted.
- Gate finalization on the user's explicit approval of the assembled roadmap.

## The Staged Expansion Roadmap

Deliver the engagement as this artifact:

```
PARTNER-CATEGORY EXPANSION ROADMAP  -  <business area>, <date>
Current base    : categories live today, activation per category, MVE status
Evidence posture: what is validated vs asserted; every benchmark used, with provenance flag
Candidate pool  : categories considered, trifurcation bucket, gap each would close
Capacity        : manager ratios, enablement bandwidth, budget  -  the numbers that cap the plan
Sequence        : Stage 1..N  -  category, why now, why this order, prerequisites met/missing
Gates           : per stage  -  pilot shape, partner-market-fit threshold, evidence required, owner
Kill criteria   : per stage  -  activation floor, time-to-first-deal window, the two-quarter rule
Conflict check  : overlap of each new category with existing routes, sized; rules needed pre-launch
Cost and ask    : total loaded cost per stage, funding mechanism, sign-off owner
Not now         : categories deleted from the ranked pool  -  deferred or rejected, each with the
                  constraint that ruled it out and a re-entry trigger
Open questions  : what the evidence could not answer, and what would change the sequence
```

A full worked roadmap and a bad expansion plan annotated line by line live in [references/worked-examples.md](references/worked-examples.md).

## Pass Threshold

Ship nothing until all of these hold; iterate until they do:

1. **One stage opens at a time.** Each stage opens only when the previous stage passed its gate; at most two in parallel, and only when they share enablement infrastructure, stated explicitly.
2. **Evidence-gated, never calendar-gated.** Every gate names the evidence that opens it - repeatable joint wins, activation, sourced pipeline - never a date alone.
3. **Capacity-consistent.** Summed stage loads (manager time, enablement build, budget) fit inside the stated capacity numbers.
4. **Kill criteria on every stage** - at minimum an activation floor, a time-to-first-deal window, and the rule for two consecutive missed quarters.
5. **Every benchmark flagged.** Each quoted number carries its provenance flag (vendor, vendor-commissioned, analyst, consultant, academic); an unflagged number is a defect.
6. **At least one category deferred or rejected**, with a re-entry trigger. A roadmap that adds everything sequenced nothing.
7. **Conflict pre-checked** for every category that overlaps an existing route, with the needed rules named before that category's launch stage.

## KPIs

Judge each added category by cohort against its gate - and the roadmap by whether its gates worked. Instrument in efficiency order - gate decisions settled per unit of measurement effort - and stop when the gate can be read:

- Partner activation rate per new category (signed partners with at least one closed deal in year one), against the gate's floor.
- Time-to-first-deal per category, against the expected window set at the gate.
- Partner-sourced and partner-influenced pipeline (B2B) or incremental attributed revenue (B2C) per category, by cohort.
- Enablement/certification completion inside the onboarding window, per cohort.
- Category share of new revenue over time - starved by that order (a year of cohorts before it says anything), and promoted whenever the review is a funding decision rather than a stage gate.
- Gate survival: share of piloted categories that pass their gate rather than get killed or re-scoped - 100% suggests soft gates, 0% suggests a broken candidate pool.
- The inverted-U watch: coordination cost rising while total sourced revenue flattens as categories accumulate - the signal to stop adding and deepen.

Full indicator definitions and published figures with provenance flags: [references/kpis-and-benchmarks.md](references/kpis-and-benchmarks.md).

## B2B and B2C

Genuinely identical on both sides, so use the same method rather than reinventing it:

- Coverage/incrementality analysis to decide which category fills a gap.
- The MVE and pilot-then-scale discipline.
- Channel conflict and cannibalization as the central governance risk when a new category overlaps an existing route.
- Partner economics as a sequencing gate.
- The inverted-U logic that too many overlapping categories create cost and noise.

A DTC brand ranking creators, marketplace and wholesale by value per unit of effort runs the same category-portfolio logic as a SaaS vendor ranking ISV, agency and MSP. Both efficiency orders live in [references/partner-category-economics.md](references/partner-category-economics.md).

What genuinely changes:

| Dimension                    | B2B tech/SaaS                                                     | B2C/consumer                                                                         |
| ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Category vocabulary          | ISV, VAR, MSP, SI/GSI, agency, referral, distributor, marketplace | Retail/wholesale, distributor, affiliate, creator/influencer, licensing, co-branding |
| Head of the efficiency order | Tech/ISV, then referral/affiliate                                 | Creator/influencer, then affiliate                                                   |
| Sequencing driver            | Product readiness, coverage gaps, buyer route                     | Incrementality (reach buyers before intent) and margin capture                       |
| Attribution                  | Deal registration, account mapping, co-sell                       | Codes, affiliate links, last-click                                                   |
| Dominant risk                | Enablement lag; conflict with direct sales                        | DTC vs retail vs marketplace cannibalization                                         |

## Failure Modes

| Failure                                                                                      | Fix                                                                                                                                                              |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ego-system trap - the sequence presumes partners will orbit you                              | Blueprint from the customer's position; verify each category's reason to join now                                                                                |
| Recruiting ahead of enablement - the field's most-cited failure                              | Capacity gate before recruiting; activation below ~20% means stop recruiting, not recruit harder                                                                 |
| Over-rotation on one category, cutting others (the Nike/Under Armour pattern)                | Treat category subtraction as high-risk as addition; size the conflict and dependency before shrinking a route                                                   |
| Category sprawl, then forced pruning (the HubSpot agency-badge pattern)                      | Kill criteria plus the deferred list; watch the inverted-U signal                                                                                                |
| Premature diversification - category two before category one is proven                       | MVE gate: repeatable joint wins first; the honest stage 1 may be "finish the current motion"                                                                     |
| Cheapest category first, mistaken for the most efficient one                                 | Rank by value per unit of effort: referral is the cheapest rung and buys the least, while an ISV motion costs a quarter and makes three later categories cheaper |
| A ruled-out category parked at the bottom of the ranking                                     | Delete it from the pool with its reason; it belongs in `Not now` with a re-entry trigger, not in a list the loudest sponsor can re-read upward                   |
| Borrowed strategy grid presented as the method (Ansoff, three horizons, BCG, Iansiti-Levien) | Keep it as vocabulary if it helps the room; rebuild the decision on MVE + gates + capacity                                                                       |
| Calendar-gated stages - "SI program launches in Q3" regardless of evidence                   | Gates trigger on evidence; dates are forecasts, not triggers                                                                                                     |
| Vendor benchmarks quoted as proof                                                            | Provenance flag on every number; vendor figures are directional context only                                                                                     |
| Roadmap drifts into ranking named companies                                                  | Categories only; hand named candidates to `mbfinotti/partnerships-skills@alliance-prioritization`                                                                |

## Invocation Examples

- "We have resellers and referral partners. Which category should we add next, and when? Two partner managers, no new headcount."
- "Turn our ecosystem map into a three-year category roadmap with readiness gates and kill criteria."
- "Leadership wants MSPs, SIs and a marketplace motion all this year. Sequence them honestly against our capacity."

## Reference

- [references/partner-category-economics.md](references/partner-category-economics.md) - per-category economics ranked by efficiency (commercial model, what it buys, time-to-first-revenue, effort, standing load, compliance exposure), B2B and B2C vocabularies, the per-axis orderings, what the order starves, and how to re-rank it for this user.
- [references/sequencing-frameworks.md](references/sequencing-frameworks.md) - Adner's MVE/staged expansion/value blueprint and the ego-system trap, the inverted-U, the trifurcation, whole product/bowling alley, and the named force-fits with why each fails.
- [references/readiness-and-capacity-gates.md](references/readiness-and-capacity-gates.md) - readiness prerequisites per category, capacity math, the business-case shape, stage-gate design, kill criteria.
- [references/kpis-and-benchmarks.md](references/kpis-and-benchmarks.md) - leading indicators, published numbers with provenance flags, the vendor-bias warning, the known-unstable statistics.
- [references/expansion-workshops.md](references/expansion-workshops.md) - the five facilitation formats ranked by efficiency, with their question sets.
- [references/worked-examples.md](references/worked-examples.md) - a full worked staged roadmap and a bad expansion plan annotated line by line.

Sibling skills (same collection):

- `mbfinotti/partnerships-skills@partner-enablement` - the enablement build each stage's prerequisites demand.
- `mbfinotti/partnerships-skills@referral-incentive-design` - incentive mechanics for a referral/affiliate stage.
