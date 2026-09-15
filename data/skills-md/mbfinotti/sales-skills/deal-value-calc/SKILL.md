---
name: deal-value-calc
description: Builds the ROI and business case for one deal - value drivers, full investment, ROI, payback, three cases conservative-first, and a one-page case the champion can forward. The buyer supplies every assumption, each number labeled buyer-supplied, benchmark, or rep-assumed, and none invented. Covers B2B and high-ticket B2C. Use whenever the user mentions ROI, business case, payback period, TCO, cost of doing nothing, "justify the price", or CFO sign-off, even without the word value. Do NOT use for price rebuttals (mbfinotti/sales-skills@sales-objection-handling) or discount trade planning (mbfinotti/sales-skills@negotiation-concession-planner).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.3"
---

# Deal Value Calculator

Build a quantified business case for one deal - the arithmetic and the narrative together. The organising rule: "It's your job to build the math equation. It's their job to give you the assumptions." (Armand Farrokh, 30MPC). This skill owns the structure, formulas, and benchmark scaffolding; the buyer owns every company-specific input.

The documented failure it exists to prevent: "most business cases created by sellers are absolute BS" (30MPC) - inflated numbers the champion never validated, which burn the champion's internal credibility the moment finance pokes a hole.

Second rule: "An ROI model on its own isn't a business case. It's a future maybe, without context. Narratives bring meaning to your numbers." (30MPC). Always deliver both the visible math and the narrative document - never a bare ROI number. The real test of the output: it survives being forwarded to a CFO without the rep in the room.

## Never invent a number

- Refuse to fabricate any input. When the user lacks a figure, ask for it, or insert a clearly labelled placeholder they must replace (e.g. `[NEEDED: fully loaded hourly cost - ask the buyer]`) - never a plausible-looking invented value.
- Label every input by who supplied it:
  - **buyer-supplied** - a number the buyer stated or documented (their payroll, invoices, ops reports, public filings).
  - **benchmark** - an external or market figure the rep brought, with its source named. "Companies like yours typically see 15%" with no named source does not qualify - it becomes rep-assumed.
  - **rep-assumed** - the rep's own estimate, not confirmed by the buyer.
- Hard rule: a business case whose headline number rests materially on rep-assumed inputs must say so on its face - a visible line in the document, not a footnote.
- The cost side is the one exception: the rep's own pricing and fees are rep-owned by definition - document them with the written quote. Every value-side input takes one of the three labels.
- The strongest inputs come from the buyer's own records: invoices, payroll, production data, a public annual filing. Get the champion to state the numbers; finance checks the baseline before it opens the vendor proposal practice).

## Interview

Ask one question per message; offer multiple-choice options wherever possible; skip anything the deal description already answers.

1. B2B, or considered high-ticket B2C (solar, home improvement, real estate, private education, financial advisory)?
2. Deal segment: transactional (single decider, low price), mid-market, or enterprise (buying committee, procurement/security in the path)? This sets the artifact size.
3. What date must the result land by? A hard near date promotes the drivers computable from documents the buyer already holds - retired contracts, the hiring plan - and deletes any driver needing a time study or a cohort analysis.
4. One-off win, or a compounding asset the buyer reuses as a renewal or QBR baseline?
   - Compounding promotes error/rework and downtime avoided, whose measured baselines outlive the deal.
   - One-off keeps the artifact at its lightest rung.
5. Effort ceiling: how many hours can the champion spend, and can they reach finance data at all? A low ceiling deletes error/rework, churn and revenue lift outright rather than ranking them last, and caps the artifact at a payback estimate.
6. Which value drivers are in play? Offer the taxonomy list below in its efficiency order as choices, re-ranked against the answers to 3-5.
7. For each driver: the raw inputs (volumes, rates, hours, costs) - and for each input, who supplied it: buyer, a named benchmark, or your own estimate?
8. The investment side:
   - Subscription/licence price
   - Implementation and integration cost
   - Internal effort (hours and whose)
   - Training
   - Ongoing administration

   Contract length?

9. Time horizon for the case: 1 year, 3 years (the enterprise-software standard), or the contract term?
10. Who is the document ultimately for - who will the champion forward it to (economic buyer, CFO, a committee, a spouse or co-signer in B2C)?
11. Will the buyer's finance function (or lender, in B2C) review it? If yes, the finance-reviewer additions in the workflow apply.

## Right-size the artifact

Not every deal gets a full model deal-type guidance; the trigger for the full treatment is complexity - roughly 6+ stakeholders, procurement or security in the path, strategic rather than tactical spend - not a fixed dollar threshold):

- efficiency: payback estimate > one-page summary + light model > full model
- effort: full model > one-page summary + light model > payback estimate
- value: payback estimate == one-page summary == full model below the complexity trigger, then full model > one-page summary > payback estimate above it

Default to the lightest artifact the deal's complexity permits; each complexity trigger crossed moves the artifact up exactly one rung. The value axis ties below the trigger because extra depth genuinely buys nothing there - a formal case is overkill for a single decider - and it inverts above the trigger, where a payback estimate simply does not survive procurement.

| Segment             | Artifact                                                                                                                                                            | Depth                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Transactional / SMB | A short payback estimate: one or two drivers, the investment, payback in months                                                                                     | No formal document; the payback line is the whole artifact              |
| Mid-market          | One-page value summary plus a light model: input ledger, 3-4 drivers, three scenarios                                                                               | Rep-built; sensitivity on the one or two inputs the result hinges on    |
| Enterprise          | Full model: economic-buyer summary and a separate finance/procurement version with an assumption appendix, documented sources for every input, sensitivity analysis | Engage a value engineer or business-value consultant if the org has one |

## Value drivers and per-driver formulas

Decompose the deal's value into drivers and compute each separately; 3-4 quantified drivers is the documented practitioner shape for the problem/solution section (30MPC). Rank them by case strength bought per hour of the buyer's time - never by headline size, and never by whichever number is easiest to produce. Effort here is not what the driver is worth: it is how hard the input is to source from the buyer, how much of the buyer's time that costs, and how long the resulting number stays arguable in a finance review.

- efficiency: direct cost > labour time > headcount avoidance > downtime avoided > error/rework > headcount reduction > capacity freed > revenue lift > churn > risk/compliance
- value (moves the headline _and_ survives finance): labour time > direct cost > error/rework > headcount reduction > downtime avoided > revenue lift == churn > headcount avoidance > risk/compliance > capacity freed
- effort (buyer hours to source the input, plus how long the number stays contestable): headcount reduction > risk/compliance == churn > error/rework > revenue lift > labour time == downtime avoided > capacity freed > headcount avoidance == direct cost
- compliance cost: risk/compliance == headcount reduction > every other driver, which carries none

Every tie is a real equality, never a dodge:

- revenue lift == churn (value) - same margin arithmetic, and both die on the same attribution objection, so finance discounts them identically.
- risk/compliance == churn (effort) - neither number exists in the buyer's own systems; both cost a week of external or cohort analysis.
- labour time == downtime avoided (effort) - each hinges on one figure the buyer either already tracks (an hour) or has to measure (a week). Same fork, same price.
- headcount avoidance == direct cost (effort) - both read straight off a document the buyer already owns, the hiring plan and the contract list.
- risk/compliance == headcount reduction (compliance cost) - each needs a review outside the deal team before the number can be written down: legal or compliance sign-off on a stated regulatory exposure, HR (in some jurisdictions works-council) consultation on a stated role removal. Both are hard to walk back once in writing.

B2C adds a substantiation duty on top of that, on every driver - see B2B and B2C.

Default: lead with the top two _hard_ drivers on the efficiency line that this deal actually has, since the case must clear the buyer's hurdle on hard value alone, then add soft drivers (headcount avoidance, capacity freed, risk/compliance) to close. Move up the value line when finance is the audience and the hard drivers are thin.

**What this order starves.** Error/rework reduction is the driver finance argues with least, and efficiency pushes it to fifth purely because a baseline cost per error is the one number most teams never track. Promote it to first when the buyer already tracks it, or when quality, compliance or an audit finding is the initiative named in the headline - there it is simultaneously the strongest and the cheapest driver in the case. Headcount reduction starves the same way on political rather than data effort; a stated reduction mandate promotes it.

**Delete, do not demote.** A driver the buyer cannot feed leaves the case entirely:

- No baseline cost per error deletes error/rework.
- Withheld gross margin deletes revenue lift and churn, rather than tempting a top-line model.
- No written agreement that a role leaves the budget deletes headcount reduction, rather than parking it as soft.

A ruled-out driver left at the bottom of the list comes back later as a number somebody invents.

**Re-rank against the buyer in front of you.** This order is a default, not a law - it shifts with the deal and with who builds the case, since a value engineer can afford a driver a solo rep cannot.

- A buyer who already instruments a metric moves that driver up several places at once.
- A procurement-led evaluation weights direct cost and TCO comparison hardest and gives soft drivers roughly nothing.
- A champion with no reach into finance data can supply no baseline at all, which deletes half the list before ranking even starts.

Formulas and cautions consolidate standard practitioner and finance practice per the source labels shown.

| Driver                               | Formula                                                                                                                      | Buyer input and effort                                                                                                                                        | Caution                                                                                                                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Direct cost / tool consolidation     | Retired licence, infrastructure, and service spend                                                                           | Contract list and renewal amounts - near-zero: already in the buyer's payables, and finance can verify it in one query                                        | Hard; confirm the old contracts actually terminate                                                                                                                       |
| Labour time saved                    | Hours saved per unit x units/year x fully loaded hourly cost                                                                 | Volume and salary band, an hour. Per-unit touch time: an hour if the team tracks it, a week for a time study. Contested on realization, not on the arithmetic | Fully loaded = base wage plus benefits and taxes, typically 125-135% of base (practitioner range). Apply a realization haircut of 60-70% for adoption and learning curve |
| Headcount avoidance                  | Loaded cost of hires not made as volume grows                                                                                | The approved hiring plan - an hour, and the champion usually has it open already                                                                              | Soft (cost avoidance); more palatable to finance than reduction - no layoff required                                                                                     |
| Downtime avoided                     | Downtime hours avoided x cost per hour of downtime                                                                           | Cost per hour of downtime: an hour if incident or SLA work already produced the figure, a quarter to derive one across functions                              | Cost per hour must be buyer-supplied                                                                                                                                     |
| Error / rework reduction             | (Baseline error rate - new rate) x volume x cost per error                                                                   | Baseline rate and cost per error: a week to a quarter, since most teams track the rate and not the cost. Least contested of any driver once supplied          | Needs a documented baseline cost per error, buyer-supplied                                                                                                               |
| Headcount reduction                  | Fully loaded cost of roles removed from budget                                                                               | The arithmetic is free; the effort is political - a standing job to get written agreement that the budget line actually goes                                  | Hard only if the role genuinely leaves the budget                                                                                                                        |
| Capacity freed (soft)                | Hours freed x loaded cost x utilisation factor                                                                               | A utilisation factor and a named redeployment target - an hour to state, and finance discounts it anyway                                                      | Only cash if the freed time is redeployed to additive work                                                                                                               |
| Revenue / win-rate / conversion lift | Incremental revenue x gross margin                                                                                           | Conversion baseline plus gross margin - a week, and margin is often withheld; the attribution argument then reopens at every review                           | Model on margin, never top line; finance discounts attribution heavily                                                                                                   |
| Churn / retention                    | Retained recurring revenue x margin                                                                                          | Cohort retention by segment - a week of analysis the buyer has to run themselves                                                                              | Attribution must be specific, not "stickiness"                                                                                                                           |
| Risk / compliance avoidance          | Expected loss = probability x impact; annualized loss = single-loss cost x annual rate of occurrence standard risk formulas) | A defensible probability and a named loss benchmark - a week to source, and the probability stays arguable forever                                            | Probabilistic - pair with a named loss benchmark, never an unsourced scare number                                                                                        |

Double-counting guard: one person's hours, one revenue stream, one budget line backs at most one driver. Time saved and headcount avoidance drawn from the same team must be split, not both counted in full.

**Hard vs. soft value - keep them separate.**

- Hard (cash-releasing) value hits the P&L or budget.
- Soft value (cost avoidance, capacity, satisfaction, risk comfort) is real but not bankable, and finance is trained to reject it inside an ROI number.

Present them as two distinct sections: the hard section closes logically, the soft section closes emotionally - deliberately in that order (30MPC). Test: the case must stand on hard value alone; if it only works with soft value included, rebuild it practitioner rule).

## Core metrics and conventions

State every convention in the document; finance rejects math it cannot audit.

- **Total annual gross value** = sum of hard driver values (soft totalled separately, outside the headline).
- **Total investment (TCO)** = licence/subscription + implementation + integration + internal effort (hours x loaded cost) + training + ongoing administration. Licence-only investment understates true cost badly as a documented finance objection).
- **Annual net value** = total annual gross value - annual recurring cost.
- **ROI %** = (total benefits - total costs) / total costs x 100, over the stated horizon. This is the net-benefit convention; a gross convention (benefits / costs) also exists - always say which one the document uses that both conventions circulate).
- **Payback (months)** = 12 x total Year-1 investment / total annual gross value (hard only). If annual gross value minus recurring cost is zero or negative, payback is undefined: write "does not pay back within the horizon" - never hide a division by zero or a negative result.
- **Multi-year view**: when the contract or horizon is multi-year, show each year's value and cost, then the cumulative net. For a finance review, add NPV = sum of (net cash flow_t / (1+r)^t) - initial investment, with r the buyer's own hurdle rate or cost of capital - ask finance for it rather than assuming (a 10% default exists in one commercial methodology).
- Payback expectations are segment-dependent and come from practitioner and vendor content, not peer-reviewed research:
  - Cheap SMB tools: 3-6 months
  - Cloud software: 12-18 months
  - Larger on-premise: 18-30 months
  - Complex data/AI purchases: 12-24+ months

  Never present any threshold as a universal rule - the buyer's own hurdle is a question to ask finance, and a benefit stream that lands conveniently on a clean 12-month payback reads as manufactured finance objection.

## Three cases, not one point estimate

Produce conservative / expected / optimistic scenarios by varying the genuinely uncertain inputs across defensible ranges - a convention repeated independently across financial-modeling practice as a cross-source convention).

- presentation order: conservative > expected > optimistic. Effort is identical across the three - the same model run at three input settings - so one ordering covers it.
- **Lead with the conservative case.** It is the one the champion defends; if it still clears the buyer's hurdle, the investment does not require perfect adoption to be worth it practitioner consensus).
- The conservative case haircuts rep-assumed and benchmark inputs hardest; buyer-supplied baselines stay fixed unless the buyer offered a range.
- For mid-market and up, add one-at-a-time sensitivity: identify the two or three inputs the result is most sensitive to and show the swing as recognized sensitivity practice).
- Do not rank the three by likelihood. Never attach a probability or a weight to a case: the ranges are defensibility bands, not a distribution, and a "70% likely" label is false precision that finance prices as a guess.

## The narrative

The five-part one-page structure (30MPC):

1. **Priority-driven headline** - tie to an internal priority or initiative the buying executives already recognize.
2. **Problem statement** - the affected parties and the quantified cost of the problem, in the buyer's own numbers, with urgency drivers.
3. **Recommended approach** - the shift in practice enabled, not a feature list.
4. **Target outcomes** - before/after with measurable metrics tied to executive-level KPIs.
5. **Required investment** - commitments of money, people, and time from both sides, with a timeline.

Rules that make it credible:

- Point the whole narrative at the economic buyer's three concerns: costs, time to value, and confidence in the initiative (MEDDICC) - and the cost of doing nothing, in the buyer's own units.
- Strip vendor branding and sales polish; plain formatting or the buyer's own template, so it reads as the buyer's internal analysis, not sales collateral).
- "You're not writing to your champion. You're writing through them (to who they'll forward it to)." (30MPC). Buying groups spend only a small fraction of the purchase with any one supplier; the document does most of its selling in rooms the rep never enters.
- Timing: start the case right after the first discovery call and iterate with the buying team - never produce it late-stage as a leave-behind (30MPC). Invite buyer edits; every correction converts a rep-assumed input into a buyer-supplied one. (The claim that win rates triple after three rounds of buyer edits is unreplicated - count edit rounds, do not promise the lift.)
- Get the champion, and ideally finance, to agree the assumptions in writing before the case is presented, so the number is the buyer's, not the vendor's practice).

## Workflow

1. Run the interview; skip answered questions.
2. Right-size the artifact: start at the lightest rung and move up one per complexity trigger crossed.
3. Select drivers off the efficiency order, re-ranked against the interview's date, compounding and effort-ceiling answers; delete the ones the buyer cannot feed rather than demoting them.
4. Build the input ledger: every input with its value, unit, source, and provenance label (buyer-supplied / benchmark with named source / rep-assumed). Missing input: ask, or insert a labelled placeholder - never invent.
5. Compute each driver's annual gross value; keep hard and soft in separate totals; run the double-counting guard.
6. Compute total investment (full TCO, not licence-only).
7. Compute net value, ROI (state the convention), payback (guard the undefined case), and the multi-year view when applicable.
8. Build the three scenarios; check the conservative case against the buyer's hurdle; add sensitivity for mid-market and up.
9. Test the case on hard value alone; if it fails, tell the user before writing any narrative.
10. Write the narrative with the five-part structure using [references/business-case-template.md](references/business-case-template.md); strip vendor branding; aim it at costs, time to value, and confidence.
11. Run the forward test and the Quality gate; iterate until the gate passes.
12. Deliver, with next steps: champion edit rounds, written assumption sign-off from finance, and the ask - "if I write a short summary of what we've built, are you willing to forward it?" (30MPC phrasing).
13. If your harness has persistent memory, store the input ledger, provenance labels, and scenario assumptions so later runs update instead of rebuilding; otherwise end with a recap the user can paste into their deal record.

If you can browse the web, verify any benchmark the user cites (source and figure) before labelling it **benchmark**; otherwise keep it rep-assumed until a source is named.

## Invocation and expected output

- "Build the business case for my deal: invoice-automation purchase, 8-person AP team, buyer gave me their volumes and error rate."
- "What's the ROI on this deal? $30K/year subscription, they say it saves each rep 4 hours a week."
- "The CFO wants to see the math before Thursday - help me make this defensible."

Deliver two blocks (fill-in templates in [references/business-case-template.md](references/business-case-template.md)):

```
THE MATH     : input ledger (value, unit, source, provenance label),
               per-driver arithmetic shown in full, hard vs soft totals,
               TCO, ROI + convention, payback, three-scenario table
               (conservative first), sensitivity notes,
               rep-assumed disclosure line if applicable
THE NARRATIVE: the five-part one-page business case, unbranded,
               aimed at costs / time to value / confidence,
               plus next steps (edit rounds, assumption sign-off)
```

## B2B and B2C

- Identical in both, explicitly:
  - The arithmetic and formulas
  - The input ledger and provenance discipline
  - The never-invent-a-number rule
  - Hard/soft separation
  - Three scenarios led by the conservative case
  - The forward test
  - The Quality gate
- The practitioner frameworks above are B2B-native; no reachable practitioner source applies them to consumer sales as an absence. Every framework mapping below is therefore structural analogy - label it as such in any B2C output.
- B2C mapping (structural analogy):
  - Economic buyer -> whoever controls the household money or whose financing approval gates the purchase
  - Champion -> the enthusiastic household member selling the skeptical one
  - Drivers -> utility-bill savings, avoided repairs and maintenance, resale value, financing cost vs. current spend
  - The artifact -> usually a one-pager comparing monthly payment against current monthly cost, with a payback range
- B2C regulatory constraint - this is where B2C is genuinely stricter, not just analogous: consumer savings claims must be truthful and substantiated under consumer-protection law. In the US:
  - FTC Act Section 5
  - The R-Value Rule for insulation and window energy claims - with multiple enforcement actions against exaggerated percentage-savings claims
  - Lending-disclosure law for financing
  - Cooling-off rights for door-to-door sales
  - State solar-disclosure statutes

  An unsubstantiated "save 40-70%" claim is a legal exposure, not just weak selling. Present ranges with disclosed assumptions, never headline averages; disclose total cost and financing terms.

- In B2C the conservative case matters even more: the buyer's "finance function" is the household budget and often a lender, and a case that only works in the optimistic scenario is exactly what regulators act against.

## Quality gate

Score the drafted case against all ten checks. Pass threshold: 10/10. Iterate - fix and re-check - until nothing fails.

1. Every value-side input appears in the ledger with value, unit, source, and one of the three provenance labels; cost-side inputs cite the written quote; no unlabelled number anywhere in the math.
2. No input was invented: every non-buyer figure is either a named-source benchmark or explicitly rep-assumed / a labelled placeholder.
3. If the headline changes materially when rep-assumed inputs are stripped, the document says so on its face.
4. Hard and soft value are totalled separately, the headline uses hard only, and the hard-only case was tested.
5. No headcount, hours, revenue stream, or budget line is counted under two drivers.
6. Every output figure is traceable: the arithmetic from inputs to headline is shown, sums check, and no undefined payback or division by zero is hidden.
7. ROI convention, time horizon, and full TCO (including internal effort) are stated.
8. Three scenarios present, conservative first; the conservative case clears the buyer's hurdle or the document says plainly that it does not.
9. The narrative has all five parts and contains no feature list. It is aimed at costs / time to value / confidence and the cost of inaction. It passes the forward test: unbranded, self-explanatory to a reader who never met the rep, nothing in it the buyer has not validated or been explicitly asked to validate.
10. Every carried claim keeps its provenance label; no vendor-data figure is presented as an expected result; no payback threshold is stated as universal.

## KPIs and measurement

- **The buyer corrected an input** - proof they engaged with the math, and each correction upgrades an input's provenance.
- **Edit rounds completed** - the case was co-built, not delivered; track the count itself, not a promised win-rate lift (the tripling claim is unreplicated).
- **Written assumption sign-off from finance or the champion** before presentation is recommended practice; using it as the KPI is a structural choice.
- **The champion forwarded the document unedited**, and it reached an economic-buyer conversation.
- Across deals: compare no-decision losses on deals with a co-built case vs. without. Baseline for how much room there is: 40-60% of qualified B2B deals end in no decision (Dixon and McKenna, HBR 2022 / The JOLT Effect).

## Common failure modes

| Failure                                                       | Fix                                                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Inflated vendor math the champion repeats and gets burned on  | Buyer's numbers, conservative case first; the champion's credibility is the asset being protected |
| Invented or "plausible" inputs                                | Refuse; ask or use a labelled placeholder the user must replace                                   |
| Bare ROI number, no narrative                                 | "A future maybe, without context" - always deliver both blocks                                    |
| Soft savings blended into the headline ROI                    | Separate sections; test the case on hard value alone                                              |
| Single point estimate                                         | Three scenarios, conservative leading                                                             |
| Licence-only investment                                       | Full TCO: implementation, integration, internal effort, training, administration                  |
| Same headcount counted under two drivers                      | One resource backs one driver; split or drop                                                      |
| Round numbers and benefits landing exactly on a clean payback | Keep the raw arithmetic visible; convenient numbers read as manufactured                          |
| Business case produced late-stage as a leave-behind           | Start after the first discovery call; iterate with the buying team                                |
| Written to the champion instead of through them               | Run the forward test before delivery                                                              |
| Unsourced "companies like you see X%" benchmark               | Name the source or relabel it rep-assumed                                                         |
| B2C savings claim without substantiation                      | Ranges with disclosed assumptions; total cost and financing terms disclosed                       |

## Reference

- [references/business-case-template.md](references/business-case-template.md) - fill-in input ledger, arithmetic block, scenario table, five-part one-page narrative, and the finance-reviewer appendix checklist.
- [references/worked-examples.md](references/worked-examples.md) - a full worked B2B mid-market case, a high-ticket B2C case (framework mapping labeled as structural analogy), and a short negative example.
- mbfinotti/sales-skills@sales-discovery-questions - elicits the raw impact figures; they arrive here as inputs.
- mbfinotti/sales-skills@meddpicc-scorecard - grades whether evidence exists; this skill builds the number its Metrics element checks, and never re-qualifies the deal.
- mbfinotti/sales-skills@deal-champion-mapping - identifies the champion; this skill writes through them.
