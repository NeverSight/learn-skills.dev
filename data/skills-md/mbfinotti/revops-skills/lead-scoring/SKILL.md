---
name: lead-scoring
description: Design, validate, and recalibrate a lead scoring model - fit and engagement signals, weighting, negative scoring and exclusions, decay, MQL/PQL threshold and tier setting, backtesting against closed-won/closed-lost outcomes, and governance; also diagnoses an existing broken model. Use whenever the user mentions lead scoring, an MQL threshold, fit vs engagement scoring, product-qualified leads, score decay, "score my leads", "our lead scores are wrong", "sales rejects our MQLs", or "too many junk MQLs" - even if they never say "scoring model". Covers B2B sales-led and B2C/PLG, rules-based design and predictive readiness. Do NOT use for assigning scored leads to reps - use mbfinotti/revops-skills@lead-routing instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.2"
---

# Lead Scoring

Design, validate, and maintain a model that ranks leads by likelihood to become revenue. The practitioner standard splits scoring into two separate axes:

- **Fit** (can they buy): firmographic, demographic, technographic.
- **Engagement** (are they about to buy): behavioral, in-product.

This two-axis model appears under several names: Marketo's A-D x 1-4 grade-and-score grid, MadKudu's Customer Fit x Likelihood to Buy, and OpenView's product-qualified lead (PQL) in PLG.

Scoring fails far more often from organizational neglect - no sales sign-off, no recalibration, MQL count treated as the goal - than from bad math, so validation and governance are part of the design here, not an afterthought. The finished score is an input to assignment: routing, territories, and rep matching belong to `mbfinotti/revops-skills@lead-routing`. Defining the account-fit criteria this skill's fit axis weights - firmographic and technographic ICP tiers - belongs to `mbfinotti/sales-skills@sales-icp-definition`; this skill owns turning that definition, plus behavioral engagement, into a working score.

The capture-score-route-nurture mechanics are structurally identical for B2B and B2C/PLG. What genuinely differs between B2C/PLG and B2B:

- Dominant signal source is in-product behavior, not forms and content.
- No buying committee - one user's behavior can qualify.
- Cycles run in days, not quarters.

Because of these differences, decay, thresholds, rescoring frequency, and recalibration all run faster in B2C/PLG.

## Interview

Ask before designing anything. One question per message; offer multiple-choice answers when possible. Skip a question only when the user already gave the answer.

- Which motion? (a) sales-led B2B, (b) PLG / self-serve with sales assist, (c) B2C transactional.
- Roughly how many new leads per month, and how many closed-won and closed-lost outcomes exist from the last 12-24 months? (Decides rules-based vs predictive, and how much backtesting is possible.)
- What is actually on a lead record at creation time - enrichment coverage per fit field, form fields, product events? (A score is downstream of data quality.)
- Does a model already exist? If yes: redesign, or diagnose first? (Diagnosis path: see Diagnosing a Broken Model.)
- How many leads can sales actually work per week? (The honest threshold constraint.)
- Who signs off - which sales leader, and what acceptance-rate floor will they hold the model to?
- Any EU or consent constraints? Behavioral scoring is profiling under GDPR; the lawful basis must be documented.
- By what date must the model be scoring live, and what is waiting on it? (A date inside two weeks rules out both enrichment procurement and the conversion-band threshold method; a quarter of runway makes both affordable.)
- One-off win or compounding asset? (A single campaign list to work stops at v1 weights and a capacity threshold; a compounding mandate is what justifies enrichment, the full backtest, and the recalibration cadence that keep the model honest after launch.)
- What is the effort ceiling - analyst hours, CRM/marketing-automation admin access, a procurement and legal path for a data contract, and how much of sales' attention you can spend? (No analyst rules out re-deriving weights from won/lost data and the conversion-band method; no procurement path deletes the enrichment rung outright rather than ranking it last.)

Carry these last three answers into every ranking in this skill and in its references; they are the only inputs that reorder the defaults for this user. Every ranking here is a default, not a law: it shifts with context and with who executes it. Re-rank before recommending a rung, for example:

- An enrichment contract already in place collapses that rung's effort to a field mapping and promotes it to the top.
- A CRM whose fit fields arrive self-reported on the form at high coverage removes the coverage menu entirely.
- No analyst promotes every rung a CRM admin can ship alone and demotes every rung that needs a cohort analysis.

## Workflow

1. Run the Interview; collect every answer before designing.
2. Audit the data first. Measure enrichment coverage per fit field over the last 90 days of leads. A fit field below roughly 70% coverage means most of the database can never reach the threshold - the enrichment-ceiling failure. Three ways out, ranked by value per unit of effort, where effort is analyst hours, admin work, procurement, and reversibility:

   - efficiency: score unknowns 0 > enrich the field > drop the field
   - value (fit signal the model can actually act on): enrich the field > score unknowns 0 > drop the field
   - effort: enrich the field > drop the field > score unknowns 0
   - compliance cost: enrich the field > score unknowns 0 == drop the field

   Effort in magnitudes:

   - Scoring unknowns 0: near-zero, a scoring-config change reversible in a click.
   - Dropping the field: an hour, and the least reversible option in this menu - the signal stops being collected and the next recalibration cannot re-derive its weight without first rebuilding the history.
   - Enrichment: a procurement and contracting step before a single lead scores, then a standing per-record dependency and a coverage number to monitor forever.

   Default to scoring unknowns 0: it keeps every thin record scoreable on engagement and ships this week. Justify the compliance tie: neither the 0 rule nor the deletion introduces a new data source, so neither triggers a consent or provenance review. Enrichment does - third-party fit data is profiling input under GDPR, and its lawful basis and provenance have to be documented before it scores anyone.

   Name the bias that default buys: scoring unknowns 0 demotes records that are thin for reasons other than fit - SMB, non-US, privacy-conscious buyers - so track their conversion as a separate cohort and re-derive the weight if they convert anyway. What this order starves is enrichment: first on value, first on effort, so a ratio never buys it, and it is the only rung that restores the signal instead of routing around it.

   Promote enrichment when:

   - The field is the ICP gate itself (employee count at enterprise ACV).
   - Coverage is low across the whole database rather than one segment.
   - A contract already exists.

   Delete the enrichment rung outright, and say it is deleted, where the Interview gave no procurement path - a rung parked at the bottom of the list returns as a quarter of vendor calls nobody approved.

3. Derive signals from outcomes, not intuition.

   - Pull 12-24 months of closed-won and closed-lost records.
   - Compare signal frequency between the two groups.
   - Keep signals with a real conversion delta over baseline.

   The gut list and the evidenced list are usually different lists. Trap: fields that look complete on won deals because sales filled them right before close - verify each signal existed at scoring time.

4. Build the signal catalogue from [references/signal-taxonomy.md](references/signal-taxonomy.md): fit and engagement as two separate scores, hard disqualifiers as exclusions (never negative points), soft demotions as negative points, decay on engagement only.
5. Weight per [references/weighting-and-thresholds.md](references/weighting-and-thresholds.md): start near 60/40 fit/engagement for sales-led, 50/50 hybrid, 30-40 fit / 60-70 engagement for PLG and B2C where behavior dominates. Cap each signal category so no single channel can cross the threshold alone.
6. Set the threshold by sales capacity first, conversion band second, percentile as sanity check - that is the efficiency ranking of the three methods, not just a sequence, and the same reference states each method's value and effort before choosing. Define tiers where each tier maps to a distinct play.
7. Backtest per [references/validation-and-kpis.md](references/validation-and-kpis.md): retro-score history, compute conversion by score band, compute the top band's lift over the unscored baseline, run the spot-check holdout set. Iterate signals, weights, and threshold until the pass threshold below clears.
8. Get written sales sign-off on the signal list, the threshold, and the acceptance floor. Models built without it are the most-cited failure in the field: marketing builds alone; sales rejects half the leads; both blame the other.
9. Emit the spec (next section), roll out staged - score the live flow before batch-scoring the backlog - and book the v2 review for 60 days post-launch before launching.
10. If your harness has persistent memory, memorize the approved spec - signals, weights, threshold, version, review date - so later recalibration and diagnosis runs start from it instead of re-interviewing.

## The Scoring Model Spec

Deliver every engagement as this artifact - a document the user can hand to marketing ops and sales. Fuller worked versions live in [references/examples.md](references/examples.md).

```
SCORING MODEL SPEC - <company/product>, <date>, v<n>
Motion       : sales-led | PLG | B2C - fit/engagement weight split, scale (e.g. 100-pt)
Fit signals  : attribute -> points | data source | coverage % | evidence (won-vs-lost delta)
Engagement   : signal -> points | decay rule | per-category cap | evidence
Exclusions   : hard disqualifiers, excluded outright (competitors, students, customers...)
Negative pts : soft demotions -> points
Threshold    : MQL/PQL score + the capacity math behind it
Tiers        : band -> play (T1 fast human follow-up, T2 queue, T3 nurture...)
Backtest     : period, conversion by band, top-band lift vs baseline, false-negative %
Guardrails   : sales acceptance floor, score-distribution inflation alarm
Governance   : owner, sales sign-off (name, date), v2 review date, change-log location
```

Three rules about the spec itself:

- **Every point value carries its evidence.** "Pricing page 2+ visits +20: converted 2.8x baseline in last-FY won analysis" is reviewable; a bare number is folklore waiting to be gamed.
- **The spec has a pass threshold.** In backtest, the top score band must convert to opportunity at **at least 2x the unscored all-leads baseline** (published guidance only demands "beats no-scoring"; treat 2x as this skill's practical floor, since a thin edge will not survive live noise). The backtest's false-positive rate must also make the agreed **sales acceptance floor - 60% is the common practitioner target, a convention rather than a researched constant** - plausible. Iterate until both clear; refuse to ship a model that does not beat the unscored baseline.
- **The model is versioned.** v1 is a starting position; the v2 review is booked before v1 ships; every change is logged and announced to sales. An unexplainable score kills rep adoption faster than a wrong one.

## Diagnosing a Broken Model

When the user arrives with a running model ("our scores are wrong", "sales ignores the score"), check every symptom below before proposing a rebuild - checking is cheap and most broken setups fail two or three, not one. Fixing is where the choice is, so the rows are ordered by value per unit of effort; work them top-down:

- efficiency: zero the vanity signals > report the right number > add decay > fix the coverage gap > add the missing buying paths > re-derive inflated weights > full recalibration
- value (opportunities the corrected model wins, or stops losing): full recalibration > add the missing buying paths > re-derive inflated weights > add decay > zero the vanity signals > fix the coverage gap > report the right number
- effort: full recalibration > re-derive inflated weights > add the missing buying paths > fix the coverage gap > add decay > report the right number > zero the vanity signals

| Symptom                                        | Likely fault                                                                                       | Fix                                                                                         | Effort                                                                                 |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Newsletter devotees outrank real buyers        | Vanity signals carry points (email opens are structurally unreliable since inbox privacy features) | Zero or floor low-intent signals; cap the email category                                    | Near-zero - point values already in the matrix, edited by the model owner alone        |
| MQL count celebrated while pipeline is flat    | Goodhart dynamic - MQL volume became the target, so the bar drifts down                            | Report MQL-to-opportunity conversion and pipeline contribution upward, never raw MQL volume | Near-zero in hours, but spends political capital with whoever set the MQL target       |
| Stale contacts look as hot as active ones      | No decay - points accumulate forever                                                               | Add decay to engagement only (mechanisms ranked in signal-taxonomy)                         | An hour of config, plus one rescore of the database                                    |
| Most of the database can never reach threshold | Enrichment ceiling - fit fields empty for most records                                             | Measure coverage, then apply the ranked menu in Workflow step 2 - score unknowns 0 first    | Near-zero for the default rung; a quarter and a standing job if enrichment is promoted |
| Closed-won deals that never hit MQL            | False negatives - model ignores real buying paths (referrals, events, product usage)               | Add the missing paths; track false-negative rate as a standing KPI                          | A week - find the path in won records, add signals, re-backtest                        |
| MQL volume up, MQL-to-opportunity down         | Score inflation - generous weights or vanity signals                                               | Re-derive weights from won/lost data; add category caps; raise threshold                    | A week of analyst work on won/lost cohorts, plus sales re-sign-off on the new bar      |
| High scores stopped predicting wins            | Stale model - ICP, product, or content shifted since calibration                                   | Recalibrate on latest multi-quarter cohort; install drift triggers                          | A quarter to rebuild, then a standing job to keep                                      |

What this order starves: the full recalibration - first on value, first on effort, so a ratio never schedules it. Promote it above everything when ICP, pricing, or product changed since the last calibration, or when two rows above have already been fixed and conversion still does not track the score.

Where the Interview gave no analyst, delete the two cohort-analysis rungs - re-deriving weights and the full recalibration - and say they are deleted rather than leaving them at the bottom of a plan nobody can execute. Against inflation, that leaves category caps and a raised threshold, which a CRM admin can ship alone and which buy back most of the precision.
