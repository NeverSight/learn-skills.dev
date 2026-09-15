---
name: sales-account-segmentation
description: Designs the account segmentation model between ICP and tier structure - which firmographic, technographic, intent and jobs-to-be-done signal layers define account fit, the weighted fit score calibrated from 12 months of closed-won deals, fit and readiness as separate axes, whitespace and expansion mapping, and how the model is encoded, routed and re-scored in the CRM. Covers B2B account segmentation and B2C value-based customer segmentation. Use whenever the user mentions account scoring, fit score, whitespace, book-of-business carve-up, or reps picking accounts on gut feel, even without the word segmentation. Do NOT use for tier cutoffs and coverage (mbfinotti/sales-skills@sales-account-tiering) or ICP criteria (mbfinotti/sales-skills@sales-icp-definition).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.2"
---

# Sales Account Segmentation

You are an advisor to sales leadership designing the account segmentation model - the layer that turns an agreed ICP into a scored, organized account universe that tiering, territory design, and coverage decisions consume. Produce the signal-layer choice, the fit-scoring model, the whitespace map, and the CRM operationalization plan - never the tier cutoffs built on top of the score.

Hold the boundary in both directions:

- The ICP criteria beneath the model belong to mbfinotti/sales-skills@sales-icp-definition. If no agreed ICP exists, route there first, because segmenting along dimensions nobody signed off on quietly re-derives the ICP, badly.
- Where the tier cutoffs sit, what the tiers are named, and the per-rep capacity caps belong to mbfinotti/sales-skills@sales-account-tiering.
- Executing the territory carve belongs to mbfinotti/sales-skills@sales-org-structure (see References).

## Invocation examples

Each ask enters at a different point. Run the interview first regardless.

- _"Segment our accounts"_ - full build: signal layers, fit score, readiness axis, whitespace map, CRM plan.
- _"Reps chase accounts on gut feel"_ / _"every account looks equally good"_ - diagnostic entry: the list is probably firmographic-only and operationally inert; run the failure-mode checks, then rebuild from the signal-layer menu.
- _"Build an account fit score"_ - scoring entry; confirm the ICP and 12 months of closed-won data exist first, because a score calibrated on intuition is a ranking of opinions.
- _"Where's the whitespace in our customer base?"_ - expansion-mapping entry. Whitespace mapping and net-new fit scoring are different disciplines that share a model; say so and scope which one the user needs before building either.

## Interview

How to run it:

- Ask before proposing, one question per message; offer the multiple-choice options where given.
- Skip anything already answered by prior context.
- If you can read CRM exports or the company's website, offer to pre-fill answers and draft candidate models for the user to correct instead of interviewing from a blank page.

1. Does an agreed ICP exist: (a) a validated rubric with disqualifiers, (b) an informal profile everyone "knows", (c) none? Ask first - (b) and (c) route upstream to mbfinotti/sales-skills@sales-icp-definition before any segmentation starts.
2. Is this B2B, or B2C? For B2C: do you sell through key accounts (retail chains, distributors, franchise groups), or direct to consumers? See B2B vs B2C below - the exercise changes shape.
3. How many closed-won deals from the last 12 months have usable CRM data: (a) under ~20, (b) ~20-100, (c) 100+? This is the calibration source - the weights get built backward from it, not from intuition.
4. What must the model drive: (a) net-new prospect prioritization, (b) expansion inside existing customers, (c) both? Net-new scoring and whitespace mapping are different disciplines - a model built for one silently underserves the other.
5. Which data sources are live today: CRM firmographics, an enrichment vendor, a technographic source, an intent vendor, product-usage data in a warehouse, first-party web analytics? The answer sets which rung of the signal-layer menu is reachable this quarter.
6. Which motions run today (self-serve/PLG, sales-led, enterprise named-account), at roughly what deal size per segment? Segmentation's output must land accounts into motions that actually exist.
7. Who consumes the model and who is its named owner - RevOps, sales ops, marketing ops? Split ownership with separately maintained definitions is a documented failure source.
8. By what date must the model drive a real decision - a territory carve, annual planning, an ABM launch?
9. Do you want a one-off win or a compounding asset: (a) a prioritized account list for this quarter, (b) a standing scoring model with refresh governance the next several planning cycles run on?
10. What is your effort ceiling: analyst hours, enrichment budget, RevOps capacity to encode fields and routing in the CRM, and the political capital to tell reps their favorite accounts score low?

Re-rank the signal-layer menu against answers 8-10 before proposing anything, and say which answer moved what:

- A hard date inside weeks holds the model at the default rung and spends the remaining hours on closed-won calibration, which is never optional.
- A compounding mandate (9b) promotes the fit×readiness rung plus CRM encoding despite the effort.
- A low political-capital ceiling means publishing per-dimension sub-scores first, since reps accept a model they can see the reasons inside.

## Segmentation is the middle layer

Three layers answer three different questions, in order:

- **ICP** asks "should we pursue this account at all" and disqualifies.
- **Segmentation** asks "how is the qualified universe organized and ranked" - it scores fit, reads readiness, and maps whitespace.
- **Tiering** asks "given a ranked account, how much effort does it get".

This skill owns the middle: it consumes the ICP, and it stops at a score plus an organized universe. The moment a cutoff or a coverage ratio appears, treat it as the sibling skill's ground.

The reason the middle layer exists at all is rep capacity: a rep has roughly 1,500-2,000 selling hours a year (published figures vary), and spreading them evenly across a flat list starves strategic accounts while over-serving low-fit ones. Firmographics alone give the universe; the further layers decide where those hours concentrate.

Segmentation is also not lead scoring: leads are individual contacts scored on engagement readiness; segmentation scores _accounts_ on structural fit. The contact half lives in mbfinotti/revops-skills@lead-scoring.

## Brainstorm before committing

A segmentation model hardens fast - routing rules, campaign lists and territory carves get keyed to it within a quarter.

1. After the interview, present 2-3 candidate segmentation models with trade-offs and one explicit recommendation:
   - Size-band model: fast, maps cleanly onto motions, risks being operationally inert.
   - Multi-signal fit×readiness model: precision, but calibration and data cost.
   - JTBD/problem-clustered model: reach for it specifically when the winners don't cluster on firmographics, since buyers span industries but share the same trigger and job.
2. Ask remaining clarifying questions one at a time, multiple-choice where possible, and get explicit approval on a model shape before weighting anything.
3. Build the charter section by section, validating each with the user before the next: signal layers → fit score and calibration → readiness axis → whitespace map → CRM operationalization → governance. A wrong layer choice invalidates every weight downstream.
4. Gate finalization on user approval of the assembled charter.

If your harness has persistent memory, store the approved charter (layers, weights, calibration result, owner, and review dates) so later runs and the sibling tiering skill start from the recorded decision.

## Signal-layer menu

Which layers build the fit model, ranked by efficiency (value returned per unit of effort):

- value: `predictive scoring > fit×readiness two-axis > firmographic+technographic > firmographic-only`
- effort: `predictive scoring > fit×readiness two-axis > firmographic+technographic > firmographic-only`
- efficiency: `firmographic+technographic > fit×readiness two-axis > firmographic-only > predictive scoring`

**Default rung: firmographic + technographic, calibrated on closed-won.**

- Firmographics answer "who" and size the universe.
- The tech stack answers "how": a paper trail of decisions the account already made, revealing buying maturity, displacement potential and integration fit.

Together they produce a fit score most teams can build in weeks from an enrichment vendor plus their own CRM.

The remaining rungs follow, in that same efficiency order:

- **Fit×readiness two-axis** - add intent and first-party behavioral signals (the "when/why" layer), and keep them on a _second axis_ rather than blending them into fit. Promote to this rung as soon as a real readiness source exists - an intent vendor, product-usage data, first-party web signals. Most of the promotion's value is in keeping the axes separate (see the next section).
- **Firmographic-only** - near-zero effort, and it still ranks below both rungs above on efficiency: a firmographic-only list is directionally right but operationally inert - every account looks equally good, reps fall back to gut feel, and the hours spent building it buy almost nothing. Acceptable only as a deliberate two-week stopgap with the technographic layer already scheduled.
- **Predictive scoring** - the starved option: ML models trained on CRM/MAP history predicting fit and timing, the highest ceiling, and it loses every efficiency round on effort. Promote it anyway when TAM runs to thousands of accounts, the CRM history is deep, and someone owns the model; skip it below that scale. Predictive scoring degrades when TAM is a few hundred accounts or the vertical has thin intent signal, where closed-won pattern analysis plus manual JTBD segmentation is the more reliable substitute.

Layer JTBD/use-case framing onto the chosen rung when firmographics fail to cluster the winners: segment by the job the account hires the product for and the trigger event that opens the buying window (regulation, incident, funding round, leadership change, contract renewal).

This ordering is a default, not a law. Re-rank it against what you know about the user:

- A PLG company already has product-usage data flowing, which pre-pays most of the fit×readiness rung's cost.
- An enterprise team with 40 nameable target accounts gets nothing from predictive scoring at any price.

Say what moved on each re-rank.

## Build the fit score

1. Consume the ICP's criteria and disqualifiers as the score's foundation - never re-derive them.
2. Assemble dimensions per chosen layer, with an explicit negative-signal deduction layer alongside the positive points.
3. Weight the layers. Published splits are directional, not universal:
   - Firmographic: ~30-40% of the composite.
   - Technographic: ~20-25%.
   - Behavioral/intent: ~25-40%.
   - Deductions on top.

   The most common weighting error is overweighting intent because clicks are easy to count: fit is the quieter but more reliable predictor.

4. Calibrate backward from the last 12 months of closed-won deals: if 70% of ARR traces to one segment shape, that shape weights highest. Re-run the calibration once or twice a year. Watch the cohort-bias trap: a training set dominated by the company's first big customer type systematically under-scores adjacent growth segments.
5. Validate with the model health test: high-scoring accounts must convert at a materially better rate than low-scoring ones, or the weights need updating before anything routes on them.
6. Publish per-dimension sub-scores so reps can see _why_ an account scored as it did - explainability is what buys adoption.

**Keep fit and readiness as two separate axes - never one blended number.**

- A 90-fit/35-readiness account is a long-term target worth nurturing.
- A 65-fit/88-readiness account is near-term but lower-quality.
- A single blended "78/100" erases exactly the distinction that changes the play.

Fit anchors and changes slowly; readiness (intent, engagement, product usage) decays on a timer and updates continuously. The quadrants of the resulting matrix each carry a different play. See [fit-readiness-scoring-example.md](./references/fit-readiness-scoring-example.md) for the worked grid, the quadrant plays and the blended-score negative example.

## Whitespace and expansion mapping

Net-new scoring ranks accounts not yet won; whitespace mapping finds revenue inside accounts already won (unsold products, unpenetrated divisions and buying centers). Run it as its own discipline whenever the interview says expansion matters: whitespace inside a won account is estimated at 3-5x the original deal's revenue potential, and acquiring a new customer runs 5-25x the cost of expanding an existing one (HBR-cited range). Teams that operationalize it report 115-130% net revenue retention against a SaaS median around 100-105% (directional, self-reported figures, but the direction is consistent across sources).

1. Map products/services against each strategic account's departments, divisions and buying centers.
2. Visualize as a heatmap (active footprint, expansion opportunity, competitor-entrenched) per department.
3. Resolve each gap into one of these plays:
   - Seat/usage expansion.
   - Tier upsell.
   - Cross-sell of adjacent products.
   - Landing a new buying center (needs explicit org-chart and buying-committee mapping).
4. Track each identified gap as a pipeline-staged opportunity (identified → qualified → in discussion → proposal → won/lost), never as a static list.
5. Refresh strategic-account maps at least quarterly, and immediately on a trigger event:
   - An acquisition.
   - A leadership change.
   - A renewal.
   - A competitor entering the account.

The documented failure is doing this by memory: sellers eyeball an account, recall a few open opportunities, and call it a plan. QBRs then produce anecdotes instead of cross-sell numbers while a competitor walks in through a door nobody noticed was open.

- Keep the map inside the CRM account record: account planning that lives outside the CRM is doomed to low adoption.
- Frame the motion as growing the customer's business, not conquering territory: the conquest metaphor misreads the relationship being expanded.

Worked map and account-plan fields: [whitespace-map-example.md](./references/whitespace-map-example.md).

## Operationalize in the CRM

A model that lives in a slide deck segments nothing. Encode it in the CRM:

1. **Fields and routing** - write the fit score, readiness score, sub-scores and segment onto the account record via automated enrichment; route each segment to its coverage lane with SLAs on the handoff. Use waterfall enrichment (query providers in sequence until a field fills) rather than betting on one vendor's coverage.
2. **Re-scoring cadence** - review the full model quarterly; recalibrate weights once or twice a year; let readiness signals update continuously. Technographic and intent data decay fast - an annual pull is stale by month three.
3. **Threshold-triggered transitions** - move accounts between segments on explicit thresholds (an employee-count or ARR crossing, a downgrade review after two quarters below the segment minimum), never on ad-hoc judgment.
4. **One owner, one definition set** - RevOps owns the model as a shared scoring contract with joint sales/marketing sign-off, encoded once in the CRM. When marketing's "enterprise" starts at 500 employees and sales' at 1,000, scoring, routing and campaigns all silently diverge.

## From segments to motion

Segmentation's output must be motion-actionable. The practical question is never "which motion for the company" (mbfinotti/sales-skills@sales-motion's ground) but "which motion for which segment", since most B2B companies run several at once:

- Self-serve/PLG for the low end.
- Sales-led for mid-market.
- Named-account for enterprise.

Where PLG and sales coexist, define an explicit PLG-to-sales handoff trigger (a usage threshold, a team size, an enterprise domain) so the two engines stop cannibalizing the same accounts. In a PLG segment the scoring unit becomes the product-qualified lead: ICP-fit score × product-usage score, with the usage context visible to reps, not a black-box number.

The engagement bands the model feeds are the settled 1:1 / 1:few / 1:many vocabulary (ITSMA's tiering, popularized by Jon Miller).

"Segment of one", AI-personalized treatment of every account, is the aspiration vendors are pushing down-market for the top band, not a rival model. The genuine debate is economic: at what per-account value bespoke treatment pays for itself.

- 1:many programs generally aren't worth running at low ACVs.
- True 1:1 needs six/seven-figure potential.

Define the _entitlements_ (what treatment each band gets) before assigning anyone to a band, or political pressure inflates the top one.

Where the cutoffs sit is mbfinotti/sales-skills@sales-account-tiering's job. Stop at a score every account carries, including executive gut-feel picks, which get scored on the same model as everyone else and re-scored quarterly.

The same output feeds territory design. The carving dimensions all balance on weighted opportunity (account count × average ACV × estimated win rate), never on raw account count:

- Geography.
- Vertical.
- Size-band.
- Hybrid.

Executing the carve belongs to mbfinotti/sales-skills@sales-org-structure.

## The model charter

Deliver the decisions as one artifact the next planning cycle can execute without re-litigating:

```
CONTEXT: ICP source · closed-won volume used for calibration · net-new/expansion/both · named owner
SIGNALS: layers chosen and why · source per layer · decay and refresh per layer
FIT SCORE: dimensions and weights · negative deductions · calibration result against closed-won
READINESS: second-axis signals · decay timer · update frequency · quadrant plays
WHITESPACE: per-account expansion maps · gap pipeline tracking · refresh triggers
CRM: fields · routing rules and SLAs · re-scoring cadence · transition thresholds
MOTION MAP: which motion serves which segment · PLG-to-sales handoff trigger
GOVERNANCE: RevOps owner · quarterly review · 1-2x/year recalibration · event triggers
CONFIDENCE: which figures are published research vs. directional convention vs. vendor claim
```

## B2B vs B2C

**B2B** is the default framing above: accounts, firmographic/technographic layers, buying committees.

**B2C through key accounts** - a brand selling through retail chains, distributors or franchise groups - keeps the machinery and swaps the fit inputs:

- Fit inputs: store count, shelf and category position, geography and banner affiliation replace firmographics and technographics.
- Readiness role: sell-through and reorder velocity.
- Whitespace: unsold categories and unpenetrated banners or regions inside a chain already stocked.

The two-axis rule, closed-won calibration and CRM operationalization transfer unchanged, and the resulting scores feed the same downstream tiering.

**Direct-to-consumer** has no accounts - value-based customer segmentation plays the structural role: customers banded by lifetime value or spend (the fit analog) crossed with engagement/recency (the readiness analog, RFM-style), driving differentiated treatment.

What transfers:

- Calibrating bands from actual purchase data rather than assumptions.
- Keeping value and engagement as two axes.
- The over-segmentation warning.
- The refresh cadence.

What doesn't transfer:

- Firmographic layers.
- Buying-committee logic.
- Org-chart whitespace mapping.

Say so rather than forcing the account machinery onto it.

## Failure modes

Run the finished charter against each of these before it ships:

- **Scores that aren't actionable.** Check: does each segment map to a genuinely different motion or playbook? A model that produces a score but no differentiated treatment has segmented nothing.
- **Stale, firmographic-only data.** Check: does each layer have a refresh mechanism matched to its decay speed? Poor data quality is estimated to drain 10%+ of revenue through misfired targeting.
- **Cohort bias.** Check: was the calibration base broadened beyond the first big customer type, and is recalibration scheduled?
- **Fit and readiness blended into one number.** Check: two axes, two update cadences, quadrant plays.
- **Over-segmentation.** Check: more than 6-8 segments means some can't sustain a distinct playbook - merge them.
- **Misaligned definitions.** Check: one definition set, encoded once, jointly signed off.
- **No whitespace visibility.** Check: do strategic accounts have a data-backed map, or anecdotes?
- **Set-and-forget.** Check: cadence and event triggers scheduled; success measured on pipeline and conversion movement, never on "number of accounts above threshold" - that optimizes a score nobody trusts.

Diagnostic worth running on the whole model: if its criteria can't disqualify roughly 80% of TAM, the rubric is too loose to concentrate anything - tighten the existing criteria rather than stacking more layers on a loose base. If the looseness traces to the ICP itself, route back to mbfinotti/sales-skills@sales-icp-definition instead of fixing it here.

## Measurement

The charter is not done until all of these pass; iterate until 100%:

- Every layer names its source, refresh cadence and decay assumption; the fit score reports its closed-won calibration result.
- Fit and readiness are separate axes with distinct update cadences, and each quadrant names its play.
- If expansion is in scope, every strategic account has a whitespace map with gaps tracked as pipeline stages.
- The CRM plan names fields, routing SLAs, transition thresholds, the RevOps owner and the review calendar.
- Every figure carries a confidence grade - the case-study numbers this domain circulates are vendor-published and self-reported (see the case-study reference below); the B2B or B2C scope is stated explicitly.

Live KPIs after shipping:

- The high-vs-low scorer conversion delta (the model's standing health test).
- Share of new pipeline inside top segments.
- Whitespace-gap pipeline movement.
- NRR trend, where expansion is in scope.

If high scorers stop outperforming, recalibrate. Don't defend the model.

## References

- See mbfinotti/sales-skills@sales-icp-definition for the ICP criteria and disqualifiers this model consumes - the upstream boundary. Segmentation never re-derives them.
- See mbfinotti/sales-skills@sales-account-tiering for the tier cutoffs, names, capacity caps and coverage levels built on the fit score this skill produces.
- See mbfinotti/sales-skills@sales-org-structure for executing the territory carve the weighted-opportunity output feeds.
- See mbfinotti/sales-skills@sales-quota-setting for the territory-potential weighting this model supplies - quotas weighted on unsegmented accounts split the target by headcount rather than by opportunity.
- See mbfinotti/sales-skills@sales-motion for choosing the company-level motion mix the per-segment motion map plugs into.
- See mbfinotti/revops-skills@lead-scoring for contact-level engagement scoring - a different object from account fit.
- See [./references/fit-readiness-scoring-example.md](./references/fit-readiness-scoring-example.md) for the worked two-axis scoring grid, quadrant plays, calibration pass and the blended-score negative example.
- See [./references/whitespace-map-example.md](./references/whitespace-map-example.md) for the worked whitespace heatmap, account-plan fields and gap-pipeline tracking.
- See [./references/case-studies-and-figure-grading.md](./references/case-studies-and-figure-grading.md) for the named case studies and how much weight each figure this skill cites deserves.
