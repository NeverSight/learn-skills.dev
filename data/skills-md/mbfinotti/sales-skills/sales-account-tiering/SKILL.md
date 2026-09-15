---
name: sales-account-tiering
description: Designs the tier layer downstream of an existing account fit score - where the cutoffs sit, tier names, rep-to-account capacity caps, the coverage model per tier (touch cadence, channel mix, QBR frequency, executive involvement), coverage-ratio health metrics, and the recalibration cadence. Covers B2B account tiering and B2C key-account tiering through retail/distribution channels. Use whenever the user mentions tiers, strategic/key/growth/long-tail accounts, accounts-per-rep ratios, 1:1 or 1:few or 1:many ABM coverage, or "everything drifted into Tier 1", even without the word tiering. Takes the fit score as input. Do NOT use for building that score (mbfinotti/sales-skills@sales-account-segmentation).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.1"
---

# Sales Account Tiering

You are an advisor to sales leadership designing the tiering layer of account coverage - everything downstream of an account fit score. Decide:

- Where the cutoffs sit.
- What the tiers are called.
- How many accounts a rep can hold in each tier.
- What coverage each tier actually receives.
- The governance cadence that keeps tier membership honest.

Produce a tiering charter, never a re-derivation of the fit criteria.

Treat the fit score as a given input:

- Which dimensions and signals build that score belongs to mbfinotti/sales-skills@sales-account-segmentation.
- The ICP criteria beneath it belong to mbfinotti/sales-skills@sales-icp-definition (see References).

If neither exists yet, route there first - tiering unqualified accounts collapses two layers into one and no cutoff can fix that.

## Invocation examples

Each ask enters at a different point. Run the interview first regardless.

- _"Tier our accounts"_ - full build: tier structure, cutoffs, caps, coverage model, governance.
- _"Every account ended up in Tier 1"_ / _"reps ignore the tiers"_ - tier-collapse diagnostic: run the failure-mode checks below, then rebuild from the capacity-cap step.
- _"How many accounts should each rep carry?"_ - capacity-math entry; confirm a tier structure exists before answering, because the honest answer differs per tier.
- _"Design our 1:1 / 1:few / 1:many ABM coverage"_ - same exercise in marketing vocabulary; the ITSMA Strategic/Lite/Programmatic bands map onto Tier 1/2/3.

## Interview

Ask before proposing. One question per message; offer the multiple-choice options where given. Skip anything already answered by prior context.

1. Does a per-account fit score exist: (a) a maintained composite score (0-100 or letter grades), (b) an agreed ICP but no score, (c) neither? Ask first - (b) and (c) route upstream to the sibling skills before tiering starts.
2. Is this B2B, or B2C? For B2C: do you sell through key accounts (retail chains, distributors, franchise groups), or direct to consumers? Direct-to-consumer changes the exercise - see B2B vs B2C below.
3. What is the typical ACV / annual account value: (a) under $10K, (b) $10-50K, (c) $50-500K, (d) $500K+? This drives the capacity math more than any per-tier convention does.
4. How many quota-carrying reps hold books, and does the tiered list cover prospects, customers, or both? A book that mixes the two needs the split made explicit before any cap means anything.
5. Current state: (a) no tiering, (b) informal per-rep judgment, (c) a formal system that broke - usually by everyone's accounts drifting into Tier 1.
6. Beyond revenue potential, what makes an account strategic here - reference-logo value, expansion whitespace, partnership leverage? These are the inputs the fit score does not carry and tiering must add.
7. By what date must tiers drive real assignment - a territory carve, annual planning, a new-segment launch?
8. Do you want a one-off win or a compounding asset: (a) a triage of this quarter's book, (b) a standing tiering system with caps, SLAs and governance the next several planning cycles run on?
9. What is your effort ceiling: RevOps capacity to encode SLAs in the CRM, executive willingness to formally sponsor accounts, and the political capital to demote accounts out of Tier 1?

Re-rank both menus below against answers 7-9 before proposing anything, and say which answer moved what:

- A hard date promotes the caps-plus-cutoffs core and defers the coverage build-out.
- A compounding mandate (8b) promotes SLA encoding and governance despite the effort.
- A low political-capital ceiling means the first proposal must show reps _why_ each account landed where it did: explainability is what buys demotions.

## Tiering is the third layer

Three layers answer three different questions, in order:

- Scoring (ICP/fit) asks "should we pursue this account at all" and disqualifies.
- Segmentation asks "how do we organize the market" into size bands, verticals and geos.
- Tiering asks "given a qualified account inside a segment, how much effort does it get and how many can a rep hold".

Tiering is a resourcing decision, not a qualification gate: it ranks survivors, it never rescues misfits.

The reason effort must be rationed at all is scarcity on both sides:

- Gartner's buying-journey research puts the B2B buying group at 6-10 decision-makers who spend only ~17% of their buying time with any supplier.
- Forrester's 2018 time-study found reps spend only ~27% of a 50-hour week engaging customers.

Both sides' scarce hours are what the tiers allocate.

Tiering is also not lead scoring:

- Leads are contacts scored on engagement readiness.
- Tiers are accounts ranked for coverage investment.

The contact half lives in mbfinotti/revops-skills@lead-scoring.

## Brainstorm before committing

Tier assignments harden fast - books, territories and comp expectations get keyed to them within a planning cycle.

1. After the interview, present 2-3 candidate tier structures from the menu below - e.g. a lean two-tier cut vs. the three-tier default vs. three-tier with a Tier-0 must-win overlay - each with trade-offs (coverage precision vs. governance overhead vs. time to stand up) and one explicit recommendation.
2. Ask remaining clarifying questions one at a time, multiple-choice where possible, and get explicit approval on a structure before setting any cutoff.
3. Build the charter section by section, validating each with the user before the next: tier structure → cutoffs and gates → capacity caps → coverage model → health metrics → governance calendar. A wrong tier structure invalidates everything downstream.
4. Gate finalization on user approval of the assembled charter.

If your harness has persistent memory, store the approved charter - tier names, cutoffs, caps, coverage SLAs, owner, and review dates - so later runs and the sibling segmentation skill start from the recorded decision.

## Tier-count menu

Ranked by efficiency - value returned per unit of effort:

- value: `five-type ABM > three-tier + Tier 0/watchlist > three-tier > two-tier`
- effort: `five-type ABM > three-tier + Tier 0/watchlist > three-tier > two-tier`
- efficiency: `three-tier > two-tier > three-tier + Tier 0/watchlist > five-type ABM`

**Default rung: three tiers** - the ITSMA-descended Strategic (1:1) / Targeted (1:few) / Programmatic (1:many) shape that nearly every practitioner model (Prospeo, TOPO's A/B/C pyramid, the ABM platforms) resolves to. It is the coarsest structure that still distinguishes named ownership from cluster campaigns from automation, which is where most of tiering's value lives.

- **Two-tier (focus / everything else)** - near-zero effort; take it when the team is under roughly five reps or founder-led, where a third tier would govern coverage nobody has capacity to differentiate anyway. Promote to three tiers once a mid-touch motion (SDR-supported cluster campaigns) genuinely exists.
- **Three-tier + Tier 0 and/or watchlist** - add a Tier 0 only for a handful of company-defining must-win logos with a committed executive sponsor each; add a watchlist tier only once signal/intent data actually feeds a promotion path. Either overlay without its precondition is governance theater.
- **Five-type ABM (Bev Burgess: Strategic, Scenario, Segment, Programmatic, Pursuit)** - the starved option: highest coverage precision, and it loses every efficiency round on effort. Promote it anyway when a dedicated ABM marketing function owns account-level marketing - that team pays the extra cost and harvests the extra precision; a sales org alone will not.

This ordering is a default, not a law - re-rank it against what you know about the user: an org already running intent tooling has pre-paid most of the watchlist's cost, and an enterprise motion with three top-ACV-band logos has effectively already built Tier 0 whether it names it or not. Say what moved when re-ranking.

## The score-to-tier bridge

The mechanical procedure, consistent across sources - the fit score arrives from upstream at step 1:

1. Take the stable **fit score** as given, whatever dimensions upstream built it from. It anchors tiers and changes slowly.
2. Layer the dynamic **signal score** upstream maintains - engagement, intent, buying-group coverage - where that data exists; it moves accounts between tiers, decaying on a timer while fit points persist.
3. Combine into one composite 0-100, or multiply fit × intent when accounts strong on both must dominate accounts extreme on one.
4. Apply published cutoffs - 80+/50-79/<50 is the most commonly cited banding; treat it as a starting convention, then calibrate the top cutoff so Tier 1 lands at or under the capacity cap, not at a round number.
5. Gate with firmographic must-haves: an account cannot reach Tier 1 on intent alone if it fails size or industry gates, and Tier-1 gates are tighter than Tier 2's.
6. Fold in the strategic inputs the score does not carry (question 6: reference value, whitespace, partnership leverage) as a limited, logged manual override - bounded in count, decided by sales leadership, reviewed at each tier review.
7. Publish per-dimension sub-scores so reps can see _why_ an account landed in its tier. Explainability drives adoption, and adoption is what separates a tiering system from a spreadsheet.
8. Automate routing against the tiers (assignment speed, sequence type, nurture) and recalculate on the governance schedule below.

Worked bridge on a 600-account list, including the calibration step and the negative example, in [score-to-tier-bridge-example.md](./references/score-to-tier-bridge-example.md).

## Capacity caps

A tier without a hard cap silently inflates - always Tier 1, because that is where everyone wants their accounts. Set the cap before the cutoff, then fit the cutoff to it.

Anchor caps to ACV, not to a flat per-tier convention - Winning by Design's capacity math (reps have roughly 1,500 selling hours a year; load scales inversely with deal size):

| ACV band   | Accounts per rep | Motion    |
| ---------- | ---------------- | --------- |
| $1M+       | 2-6              | 1:1 named |
| $500K-$1M  | 6-20             | 1:1 named |
| $50K-$500K | 20-50            | 1:few     |
| $10K-$50K  | 50-150           | 1:many    |

Cross-source practitioner bands (directional, not audited):

- Tier 1: roughly 5-25 accounts per rep.
- Tier 2: roughly 25-60 accounts per rep.
- Tier 3: automation-bounded rather than per-rep capped.
- Customer-success books: roughly 1:5-15 enterprise, 1:20-75 mid-market, 1:100+ SMB pooled.

The widely repeated "20-50 named accounts per enterprise AE" traces to vendor glossaries rather than to a published study - use it as convention, never as evidence. The authoritative per-segment numbers (ZS Associates, Alexander Group, Bridge Group) sit behind paid reports.

Enforce the top-tier cap hard - a genuine 10-20 account ceiling for a true Tier 1 book. Naming 500 accounts "Tier 1" is the single most common failure of the whole exercise.

Full capacity worked example - book construction, the prospects/customers split, and the segment-level coverage-ratio math - in [tier-capacity-math-example.md](./references/tier-capacity-math-example.md).

## Coverage-lever menu

Differentiated coverage is what makes a tier real; before it, tiering is labeling. Build the levers in efficiency order:

- value: `SLA-encoded coverage differentiation == capacity caps > dedicated account pods > executive sponsorship > QBR-cadence differentiation`
- effort: `dedicated account pods > executive sponsorship > SLA-encoded coverage differentiation > QBR-cadence differentiation > capacity caps`
- efficiency: `capacity caps > SLA-encoded coverage differentiation > QBR-cadence differentiation > executive sponsorship > dedicated account pods`

The `==` tie is real co-dependence, not indecision:

- Caps without differentiated coverage produce tiers that change nothing about how accounts are worked.
- Differentiation without caps produces a top tier that inflates until its coverage promise is unkeepable.

Ship them together as the default rung.

- **Capacity caps** - near-zero effort once the structure exists; the section above.
- **SLA-encoded coverage differentiation** - encode per-tier touch cadence, channel mix, personalization depth and response SLAs into the CRM and marketing-automation platform, not a slide. Moderate RevOps effort; this is the lever that converts tier membership into observable rep behavior.
- **QBR-cadence differentiation** - quarterly business reviews for the top tier, semi-annual or automated value summaries below. Low effort, honest value: a Tier-1 QBR costs roughly 3-6 hours of preparation, so running true QBRs for every account produces shallow QBRs for everyone.
- **Executive sponsorship** - a formal program pairing top-tier accounts with named executives (a public reference point: GitLab caps sponsors at 4 accounts each, with annual selection and a one-year commitment). High effort - executive hours and governance. Promote it once the Tier-1 book is at or under its cap and executives commit for a full year; without both, it is a logo slide.
- **Dedicated account pods (AE + SDR + SE per account or cluster)** - the starved option: highest-touch coverage and the highest effort, an org-design change rather than a coverage setting, so it loses every efficiency round. Promote it when the account value sits in the top ACV bands of the capacity table - the 1:1 named range, where one account is worth a whole team - and design it with mbfinotti/sales-skills@sales-org-structure, because pod design is that skill's ground.

Same warning as above: the ordering is a default. A company whose executives already run customer relationships has pre-paid most of the sponsorship cost; re-rank and say what moved.

The full per-tier coverage matrix - personalization, human involvement, channels, review cadence, marketing motion, with a confidence flag on every figure - is in [coverage-model-matrix.md](./references/coverage-model-matrix.md).

## The charter

Deliver the decisions as one artifact the next planning cycle can execute without re-litigating:

```
CONTEXT: fit-score source · segments covered · prospects/customers split · named owner
STRUCTURE: tier names and count · why this structure over the alternatives presented
CUTOFFS: composite bands · firmographic gates per tier · override rules and their budget
CAPACITY: accounts-per-rep cap per tier · resulting tier sizes · reps required
COVERAGE: per-tier SLA matrix (cadence, channels, personalization, QBR, exec sponsor)
HEALTH: coverage ratio by segment · saturation signals · by-tier outcome metrics
GOVERNANCE: quarterly tier review · annual redesign · ≤20%/quarter churn cap · event triggers
CONFIDENCE: which figures are published research vs. directional convention
```

## Health metrics and recalibration

Measure whether the tiers are working, by tier and by segment - never blended:

- **Pipeline coverage ratio by segment** - compute required coverage as 1 ÷ that segment's historical win rate, never a flat 3x: an SMB motion winning ~60% needs ~1.7-2x while an enterprise motion at 15-25% needs 4-7x, and a healthy blended number can hide a starved segment. Modeling coverage in depth is mbfinotti/sales-skills@sales-pipeline-coverage-modeling's job; here it is a tier-health dial.
- **Accounts-per-rep saturation** - whether any tier is over its cap; for customer books, warning signs include QBR coverage under 80% and accounts silent 14+ days.
- **By-tier outcome validation** - pipeline created, win rate, ACV and retention per tier, not engagement clicks. If Tier-1 lift fails to exceed Tier 2/3 within two quarters, the system is not earning its overhead: redesign it, don't re-run it.

Governance:

- RevOps owns the model, the data and the calendar.
- Sales leadership owns tier-change decisions.

That split is what keeps tiers from drifting or becoming political.

Run on a fixed cadence:

- Quarterly tier reviews (promote/demote).
- An annual full redesign.
- Event-triggered realignments.

Cap list churn at roughly 20% per quarter so an account experiences its new coverage level before being re-scored.

Triggers that force a redesign rather than a review:

- A material win-rate shift (recompute the coverage ratios).
- Quota attainment in a segment falling below ~40% (books are oversized - shrink them rather than pushing reps harder).
- Productivity tooling measurably reclaiming 40-60% of rep time (raise caps 30-50% and re-cut).

## B2B vs B2C

**B2B** is the default framing above: accounts, buying committees, firmographic gates.

**B2C through key accounts** - a manufacturer or brand selling through retail chains, distributors or franchise groups - is account tiering nearly unchanged:

- A handful of national chains form Tier 1, with named key-account managers and joint business planning (the retail-channel equivalent of the QBR).
- Regional chains form Tier 2.
- Independents route through distributors or telesales as Tier 3.

The capacity caps, the score-to-tier bridge, the coverage-lever ordering and the governance cadence all transfer. What changes are the fit score's inputs - store count, shelf and category position, geography instead of firmographics/technographics - and those inputs are upstream, in the segmentation sibling's territory.

**Direct-to-consumer** has no accounts to tier. The structural analog is customer-value segmentation - spend or lifetime-value bands driving differentiated service levels - which is a different exercise with different math; say so rather than forcing the account machinery onto it.

## Failure modes

Run the finished charter against each of these before it ships:

- **Tier collapse** - hundreds of accounts named Tier 1 and treated identically, erasing the point of tiering. Check: is the top tier at or under its hard cap, and did any account get in without passing the gates?
- **Layer collapse** - tiering a list that was never qualified, so Tier 3 is full of accounts that should have been disqualified. Check: did every tiered account clear the upstream fit bar?
- **Labeling without differentiation** - "one cadence for whales and minnows": tiers exist in the CRM but coverage is identical. Check: does each tier have at least one SLA-encoded difference a rep would notice?
- **Blended health metrics** - one company-wide coverage ratio hiding a starved segment. Check: is every health metric computed per segment and per tier?
- **Static tiers** - set once, never reviewed; or the opposite, whipsawed monthly so no coverage level ever gets time to work. Check: quarterly review scheduled, churn capped at ~20%/quarter.
- **Vendor-stat confidence** - asserting figures like "2.3x more likely to hit targets" as fact. Check: every number in the charter carries its confidence grade; vendor claims are attributed, never adopted.

## Measurement

The charter is not done until all of these pass; iterate until 100%:

- Every tier has a published cutoff, firmographic gate, hard capacity cap, and at least one SLA-encoded coverage difference from its neighbors.
- The top tier's size is at or under cap, and the override budget is bounded and logged.
- Health metrics are defined per segment and per tier, with the 1 ÷ win-rate coverage formula, and the two-quarter Tier-1 lift test is scheduled.
- Governance names the RevOps/sales-leadership ownership split, the quarterly/annual cadence, the ~20% churn cap, and the redesign triggers.
- Every figure carries a confidence grade (published research / directional convention / vendor claim), and the B2B or B2C scope is stated explicitly.

After shipping, the live KPIs are the by-tier outcome metrics above - with the two-quarter lift test as the standing verdict on whether tiering earns its overhead.
