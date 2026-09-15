---
name: customer-health-score
description: Design, validate, and govern a composite customer health score - product usage and engagement signals combined into one weighted, normalized, decayed, banded account score that flags both churn risk and expansion readiness, backtested against real churn outcomes and recalibrated. Use whenever the user mentions a customer health score, health scoring model, account health, signal weighting, score bands, at-risk account flagging, churn risk score, expansion risk, or says "green accounts keep churning" - even if they never say "health score". Covers B2B account-level rollup and B2C/PLG continuous scoring. Do NOT use for discovering which indicators actually predict churn - use mbfinotti/revops-skills@customer-churn-signals instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.1"
---

# Customer Health Score

Design, validate, and maintain one composite score that tells a post-sale team which accounts are drifting toward churn and which are ready for an expansion conversation. In ChurnZero's 2025 Customer Revenue Leadership Study (~800 CS and post-sales leaders surveyed), 73% said their current health score does not reliably predict churn.

- **Performative score.** Someone picks ten metrics, weights them by intuition; CS ignores the result because it predicts nothing.
- **Predictive score.** Derives its weights from what churned accounts actually did before churning, then proves itself in backtest.

This skill owns the composition and validation that turns one into the other:

- Normalization
- Weighting
- Decay
- Banding
- Segment calibration
- Override governance
- Wiring every band to a play

Which indicators to feed it, and how predictive each one is, is discovery work owned by `mbfinotti/revops-skills@customer-churn-signals`. Treat signals here at the category level (product usage, relationship/engagement, support, commercial, sentiment) and take the discovered indicator list as input.

Draw on the field's named canon where it genuinely helps:

- **Gainsight's DEAR framework** (Deployment, Engagement, Adoption, ROI): a balanced-scorecard model of 4-6 weighted metric groups summed into bands. Gainsight cautions that weighting "is highly unique to each company".
- **Lincoln Murphy's Success Potential**: ties expansion to achieved health ("No Customer Success... No Expansion Revenue").
- **RFM-style reads**: recency, frequency, and depth of usage.
- **Leading-vs-lagging split**: adoption trend, sponsor engagement, and response-time trend lead; churn, NRR, and renewal rate only confirm afterward. Score the leading ones.

One composite score, or a separate expansion model:

- **One composite, top band gates expansion (default).** Already the score being built and validated; a second model costs a quarter to build and two validation loops to keep. Gating expansion plays on the top band is the dominant practitioner pattern: low bands trigger retention, the top band triggers expansion/advocacy motions.
- **A separate expansion model.** Justified only when expansion-specific inputs are systematically tracked; otherwise it is a second unvalidated score.

Only vendor case studies support the claim that high health causally predicts expansion; no rigorous published study does. Treat health as necessary but not sufficient for expansion: the top band earns an account the conversation, and fit, whitespace, and budget decide it.

B2B and B2C/PLG share most of the mechanics: per-seat normalization, trend-over-level, an action wired to every band, and the backtest loop are identical in both. Say so when asked. What genuinely differs:

- **B2B.** Rolls user-level signals up to account level with extra weight on champion/sponsor continuity: renewals hinge on the buying organization, not one user, and flat aggregate usage can hide a disengaged champion (the "silent churn" pattern). Risk concentrates around a renewal date, so weight renewal proximity inside the score.
- **B2C/PLG.** No CSM and no renewal cliff: scoring is continuous and system-driven, ownership sits with growth/product rather than CS ops, and an involuntary-churn layer (failed payments, dunning) belongs in the score because payment failures correlate with engagement decline.

## Interview

Ask before designing. One question per message; offer multiple-choice answers when possible. Skip anything already answered.

- Which motion? (a) CSM-covered B2B with contract renewal dates, (b) PLG/self-serve continuous subscription, (c) B2C consumer subscription.
- How many accounts, and roughly how many churn events in the last 12-24 months? (Decides statistical weighting vs the rules-based cold-start path.)
- Which data sources are actually connected today - product usage data, engagement/meeting records, support system, billing? Rough coverage of each?
- Has signal discovery been done - is there an evidenced list of indicators that preceded past churn (see `mbfinotti/revops-skills@customer-churn-signals`), or only a gut list?
- Does a health score already exist? If yes: diagnose first or rebuild? (Diagnosis path: see Diagnosing a Broken Score.)
- What segments exist - enterprise vs SMB, onboarding vs mature? (A 70 that is healthy for enterprise is a red flag for an onboarding SMB; segment calibration is mandatory, not optional.)
- How many at-risk accounts can the team actually work per month? (The red band is sized to this, not to statistics.)
- Who owns the scoring logic, who acts on the score day-to-day, and who may override it?
- By what date must the score be live and acted on? (A hard date - a renewal cycle, a board review - promotes the rules-based proxy and the top two signal rungs; a distant date makes statistically fitted weights and a survey category affordable.)
- One-off win or compounding asset - this quarter's at-risk list, or a model that keeps getting better? (A one-off list drops decay, segment calibration, and the standing recalibration cadence; a compounding mandate promotes all three plus fitted weights.)
- What is the effort ceiling - analyst hours, whose data-engineering time, and how much manual logging CS will genuinely do? (Manual logging is what makes stakeholder-continuity signals real; if nobody will log, that category drops to whatever the CRM captures on its own.)

## Build order

Build the score rung by rung, ranked by churn actually prevented per hour of analyst time - not by what is cheapest to wire, and not by what scores best in backtest. Effort here is analyst hours, data the product must already emit, ongoing re-fitting, and how legible the score stays to the people who must act on it: a score CSMs cannot reconstruct is expensive no matter how accurate it is.

- efficiency: usage/adoption > commercial/billing > support > stakeholder continuity > sentiment survey
- value (churn caught): stakeholder continuity > usage/adoption > support == commercial/billing > sentiment survey
- effort:
  - usage/adoption and commercial/billing: near-zero - the product and billing system already emit the events.
  - support: an hour to map tickets to rates and trends.
  - stakeholder continuity: a standing job - humans must log meetings and sponsor changes for the input to stay true.
  - sentiment survey: a week to stand up, plus a standing job to run - low response rates keep it unstable.

Support and commercial tie on value because each catches a blind spot the other cannot - escalation clusters, invoice disputes - and neither substitutes for the other.

Start from the top two rungs plus whatever discovery already evidenced, validate that, then add rungs.

**What this order starves:**

- **Stakeholder continuity.** The highest-value input, the one that catches silent churn, and the worst ratio because it depends on humans logging contact. Promote it to rung one in any B2B book with renewal dates, or the moment one green account churns after a champion left - the continuity rule in step 5 makes it mandatory regardless of its ratio.
- **Statistically fitted weights and a second, dedicated expansion model.** Both lose every round on ratio and are still right eventually. Both need an account base large enough to fit and validate on its own outcomes (tens of churn events per segment), and both buy better signal once it exists.

This ordering is a default, not a law. It shifts with context and with who executes it - re-rank it against everything already known about the user before proposing it:

- A product already emitting rich usage telemetry locks usage at rung one for near-zero effort.
- A customer-success team of one demotes everything that needs manual logging and promotes automated usage and billing signals.
- Fewer than a hundred accounts takes fitted weights off the table entirely (see the cold-start path) and makes monthly CSM interview-validation the strongest check available.

## Workflow

1. Run the Interview; collect every answer before designing.
2. Define the outcome before any signal talk. A score that predicts an undefined event cannot be validated.
   - Churn event: non-renewal, cancellation, or no reactivation within N days for B2C.
   - Entity level: account for B2B, subscriber for B2C.
   - Prediction window: what the score claims to predict, e.g. churn within 90 days.
3. Take the indicator list as input - from the customer-churn-signals discovery work or, failing that, the user's best-evidenced candidates - and group it into the categories in [references/signal-categories.md](references/signal-categories.md). Audit data coverage per category, then build in the Build order ranking above, re-ranked against the user's answers. Never integrate everything at once, and drop any signal that could never trigger a play - if it can't trigger a play, it's a vanity signal.
4. Normalize per [references/signal-categories.md](references/signal-categories.md):
   - Rate-normalize by seats/users (500 logins from 50 users is not 500 logins from 1,000 users).
   - Read support and sentiment as trends, not counts.
   - In B2B, roll user-level signals up to account level with champion/sponsor weighting.
5. Weight per [references/weighting-and-bands.md](references/weighting-and-bands.md): derive weights from correlation with the defined outcome in the churned-vs-retained cohort, never from intuition. Cap every category so no single input can move an account across a band alone, and require at least one stakeholder-continuity input so no combination of usage signals can hold an account green after a champion departs.
6. Add decay: every engagement-type signal drifts toward neutral as it ages, so silence reads as uncertainty instead of accumulated green. Score the trend and the level - a falling 75 is a worse account than a stable 60.
7. Band: three bands, no more - more bands sound precise and add confusion. Size the red band to intervention capacity first, then improve the score until the same capacity catches more of the churn. Set segment-specific thresholds and weight overrides.
8. Validate per [references/validation-and-kpis.md](references/validation-and-kpis.md): retro-score the historical cohort, use precision/recall (never raw accuracy - churn is class-imbalanced), and run the retro check on what churned accounts scored 60-90 days pre-churn. Iterate weights, decay, and thresholds until the pass floor in the spec section clears. Too few churn events → take the cold-start path in the same reference.
9. Wire every band to a play with an owner and an SLA - a band change that triggers nothing is a report, not a health score. Define the override policy: any CSM may override with a mandatory reason code; overrides feed recalibration as labeled disagreements.
10. Emit the spec (next section), pilot with a small group before full rollout, review score distribution and misses monthly for the first 90 days, then move to the standing recalibration cadence.
11. If your harness has persistent memory, memorize the approved spec - categories, weights, bands, segment overrides, validation results, review date - so later recalibration and diagnosis runs start from it instead of re-interviewing.

## The Health Score Spec

Deliver every engagement as this artifact - a document the user can hand to CS ops, RevOps, and the CSM team. Fully worked versions live in [references/worked-examples.md](references/worked-examples.md).

```
HEALTH SCORE SPEC - <company/product>, <date>, v<n>
Outcome      : churn event definition | entity level | prediction window
Segments     : list + per-segment weight/threshold overrides
Signals      : category -> weight | inputs (from discovery) | normalization | evidence (outcome correlation)
Decay        : per-category drift-to-neutral rule and window
Rollup (B2B) : user->account aggregation method, champion/sponsor weighting
Bands        : 3 bands -> score ranges -> wired play, owner, SLA per band
Expansion    : top-band gate + the non-health conditions (fit, whitespace, contract timing)
Overrides    : who may override, reason codes, how overrides feed recalibration
Validation   : backtest window | red-band churn multiple vs base rate | % churned accounts
               below green at 60-90 days pre-churn | precision/recall at the red threshold
Triggers     : band-change alert -> task/workflow; renewal-proximity weighting (B2B)
Governance   : logic owner | acting owner | data owner | review cadence | change log location
```

Three rules about the spec itself:

- **Every weight carries its evidence.** "Adoption-depth trend 35%: churned accounts declined here in 7 of 9 pre-churn quarters analyzed" is reviewable. A bare percentage is folklore. If a weight has no outcome evidence yet, label it a provisional hypothesis with a validation date.
- **The spec has a pass threshold.** No standards body publishes a numeric ship-it bar for health scores; these floors are this skill's convention, set because a model that clears less will not survive live noise or earn CSM trust.
  - In backtest, the red band must churn at **at least 3x the portfolio base rate**.
  - **At least two-thirds** of accounts that actually churned must have sat below green 60-90 days before churning.
  - No more than **~80%** of the book may sit green (a documented practitioner red flag if crossed), independent of backtest results.

  Iterate until all three hold. Refuse to ship a score that reads as decoration.

- **The score is versioned and owned.** Diffuse ownership produces a score that changes meaning per reader: CS wants adoption, RevOps wants CRM activity, product wants feature usage, and everyone gets a field.
  - One owner for the logic (CS ops/RevOps).
  - CSMs act and override.
  - One data owner.
  - Every change logged and announced.

## Diagnosing a Broken Score

When the user arrives with a running score ("green accounts keep churning", "the team ignores it"), diagnose every symptom, then fix in the order below - not in the order the symptoms were reported, and not worst-fault-first. The ratio is churn actually prevented per hour, and the deadliest fault is rarely the one that pays back first.

- efficiency: wire band->play > normalize per seat > add decay > cap categories + continuity input > noise guard == ticket-read fix > segment calibration > re-derive weights from the cohort > qualify the expansion gate
- value: re-derive weights == wire band->play > cap categories + continuity input > normalize per seat == add decay > segment calibration > noise guard == ticket-read fix > qualify the expansion gate
- effort:
  - decay and the noise guard: near-zero.
  - normalization, caps, the ticket read, and the expansion gate: an hour each.
  - segment calibration and the cross-team coordination that wires plays to owners and SLAs: a week.
  - cohort re-derivation: a standing job, which also needs churned-account history the book may not have.

Ties justified:

- An unacted score and a wrongly-weighted one both prevent zero churn - they tie on value and split on effort.
- Normalization and decay tie because each removes one systematic misread of the same book.
- The noise guard and the ticket read are the same trailing-trend machinery applied twice, each buying back a different flavor of CSM distrust.

The table is ordered to match.

| Symptom                                             | Likely fault                                                                                     | Fix                                                                                              |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| CSMs ignore or silently distrust the score          | No wired plays; no gated override; unexplainable weights                                         | Wire band->play; allow overrides with reason codes; publish the weight evidence                  |
| Large accounts always look sick (or always healthy) | Raw counts instead of rates                                                                      | Normalize per seat/user; benchmark against similar-size accounts                                 |
| Score rarely moves; most of book green              | No decay - old positive signals accumulate forever                                               | Decay engagement signals toward neutral; recheck distribution monthly (>80% green = broken)      |
| Champion left; account stayed green for weeks       | Single-category dominance - usage alone can hold green                                           | Cap category shares; require a stakeholder-continuity input that can pull the band down alone    |
| Score flaps band-to-band weekly                     | Single-point noise treated as signal                                                             | Score trailing-window trends; require two consecutive readings before a band change fires        |
| High-touch accounts flagged red on ticket volume    | Ticket count read as risk                                                                        | Rate-normalize tickets, read the trend; treat zero tickets as possible disengagement, not health |
| Same score means different things across accounts   | One global model over unlike segments                                                            | Segment-specific weights and thresholds (enterprise vs SMB, onboarding vs mature)                |
| Green accounts keep churning                        | Performative weights - intuition, not outcome correlation; missing relationship/sentiment inputs | Re-derive weights from the churned-vs-retained cohort; add a stakeholder-continuity input        |
| Top-band accounts never expand                      | Health treated as sufficient for expansion                                                       | Gate expansion plays on top band, but qualify on fit, whitespace, and contract timing separately |

Re-rank this too: a book with no churned-account history has no cohort to re-derive from, so that rung leaves the list rather than sitting last (see the cold-start path).

## Reference

- See [references/signal-categories.md](references/signal-categories.md) for how each signal category behaves inside a composite: normalization, trend windows, rollup, and per-category traps. Category mechanics only; indicator discovery lives in `mbfinotti/revops-skills@customer-churn-signals`.
- See [references/weighting-and-bands.md](references/weighting-and-bands.md) for deriving weights from outcomes, caps, decay mechanics, banding, segment overrides, and the one-score-vs-two decision in full.
- See [references/validation-and-kpis.md](references/validation-and-kpis.md) for the backtest procedure, precision/recall framing, pass floors, the cold-start path, KPIs, recalibration cadence, and override governance.
- See [references/worked-examples.md](references/worked-examples.md) for a CSM-covered B2B spec and a PLG/B2C spec worked in full, plus a plausible-looking broken score decomposed.
- See `mbfinotti/revops-skills@lead-scoring` for pre-sale scoring - lead scoring predicts who will buy; this skill predicts who will stay and grow. Different outcome, different model.
- See `mbfinotti/revops-skills@sales-to-cs-handoff` for the sales-to-CS transition where the first health baseline gets set.
- See `mbfinotti/revops-skills@revenue-kpi-framework` for the org-wide metric tree this score reports into - the composite can serve as a leading input under the retention branch, and that skill sets which level owns it and what guardrail rides alongside it.
