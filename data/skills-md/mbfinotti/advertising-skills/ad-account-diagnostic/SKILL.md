---
name: ad-account-diagnostic
description: "Diagnose the root cause of an underperforming paid ad account - why the ads stopped working, why CPA went up, why ROAS dropped - instead of defaulting to 'increase the budget'. Weighs tracking, account structure, targeting, creative, bidding and budget, offer, and external forces, and returns a prioritised verdict with evidence and confidence. Covers B2B and B2C on search, paid social, video, and native. Use whenever the user mentions an ad account audit, a campaign structure review, wasted ad spend, rising cost per lead, or says their ads used to work - even if they never say 'diagnostic'. Diagnosis only, and it stops at the click: post-click page problems are mbfinotti/advertising-skills@paid-landing-page-audit and creative decay is mbfinotti/advertising-skills@ad-creative-fatigue."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.5"
---

# Account Diagnostic

Find the root cause of an underperforming ad account before anyone touches it. The whole discipline is refusing the reflex fix: an account that "stopped working" has at least seven candidate failure layers, and the most common responses - raise the budget, swap the creative, blame the algorithm - each treat one unproven hypothesis as a verdict. This skill works the layers in a fixed order, measurement first, because every downstream number is read off the conversion signal: as Adspirer puts it, the checklist is "ordered the way an experienced PPC manager actually works it: measurement first (because every other number is wrong if tracking is broken)".

It decomposes the metric chain to localise the failing link before naming a cause, compares the account against its own history rather than industry benchmarks, and refuses to issue any verdict the data cannot support. The output is a diagnosis with confidence, evidence, and a prioritised handoff plan - never an executed change.

This skill stops at the account boundary; everything past the click hands off elsewhere, and this skill never becomes a budget skill - it exists precisely because "increase the budget" is the wrong default.

- **Past the click** (message match, page friction, the page fix list): `mbfinotti/advertising-skills@paid-landing-page-audit`. This skill only flags "the evidence points downstream of the click" and hands off.
- **Fragmentation verdict** (merge plan): `mbfinotti/advertising-skills@ad-campaign-consolidation`.
- **Creative-layer verdict** (decay analysis): `mbfinotti/advertising-skills@ad-creative-fatigue`, which hands back here when the cause is not creative - the two are reciprocal.
- **Tracking verdict** (fix checklist): `mbfinotti/advertising-skills@ad-conversion-tracking`.
- **Cross-platform discrepancy quantification**: `mbfinotti/advertising-skills@ad-attribution-gap`.
- **Search-term mining**: `mbfinotti/advertising-skills@ad-negative-keywords`.
- **Targeting design**: `mbfinotti/advertising-skills@ad-audience-targeting`.
- **Budget and bidding decisions**: `mbfinotti/advertising-skills@ad-budget-pacing`, `mbfinotti/advertising-skills@ad-spend-allocation`, `mbfinotti/advertising-skills@paid-media-scaling`, and `mbfinotti/advertising-skills@ad-bidding-strategy`.

## Interview

Ask before opening any data. One question per message; offer multiple-choice answers where possible; skip anything already supplied or visible in the data.

- Which platform(s) does the account run on? (search / paid social / video / native / several)
- B2B or B2C/ecommerce?
- Monthly spend, and roughly how many conversions per month on the event the account optimises to? (Decides whether the Evidence Gate can clear at all.)
- What window is under suspicion - when did performance degrade, and against which prior period is it being judged?
- What changed, and exactly when? (Budget, bids, creative, targeting, optimization event, landing page, site release, consent banner, price, promo calendar - dates matter more than the list.)
- What can you export, and at what granularity? (Per-campaign per-day is the working minimum; per-ad-set and per-ad breakdowns unlock the localisation step.)
- What is the target CPA/ROAS - and is it derived from unit economics or inherited from a dashboard?
- Is CRM or backend revenue data reachable for reconciliation? (Yes, directly / yes, via someone / no.)
- Which attribution window and counting settings does reporting use, and did they change in the window?
- Who will implement the fixes, and what is their effort ceiling - hours available, whose hands (developer, marketing ops, creative studio, page owner), and how reversible a change is allowed to be? (The handoff plan is addressed to them; see Prioritisation for how a ceiling reshapes the queue.)
- By what date does the recovery have to show up in reporting? (A hard deadline promotes fast-acting fixes - tracking repair, unblocking a genuinely budget-capped campaign - and demotes offline-outcome wiring and creative programmes, whose payoff lands a window or two later.)
- One-off recovery, or a compounding asset? (A compounding mandate promotes the offline-outcome feedback loop and structural consolidation above the quick wins; see Prioritisation.)

## Workflow

1. Run the Interview; collect every answer before touching data.
2. **Reconcile before interpreting.** Compare platform-reported conversions against CRM/backend truth over a lag-mature window, against OnlyDeb's practitioner reference points:
   - Gap above roughly 40%: something is broken - stop, record a tracking FAIL, and hand off.
   - Gap within roughly 10%: proceed to the other layers.

   These are attributed starting points, not laws - the account's own historical ratio, and whether that ratio is _stable_ week to week, is the real criterion. If backend data is unreachable, every later finding carries at most medium confidence, and the verdict must say so.

3. **Decompose the failing metric** with [references/metric-decomposition.md](references/metric-decomposition.md). Chain the funnel - impressions → clicks → conversions → revenue - and express the outcome as CPM × CTR × CVR × AOV (Pigeon Digital) to find which single link actually moved. Name no cause before the failing link is localised.
4. **Break down and compare.** Pull the failing metric by campaign, then ad set, then ad, and compare each against the account's own history - never industry benchmarks. AdStellar's rule for CPM generalises: elevated evenly across everything points external; concentrated in one branch points to a targeted internal cause. This step is what separates internal from external causes.
5. **Walk the layers in fixed order** (below) using [references/layer-evidence.md](references/layer-evidence.md). For each layer record one of four states - `pass` (evidence rules it out), `FAIL` (evidence confirms it), `unknown` (evidence missing), `not applicable` - with its own severity and confidence. Never collapse to a binary: `unknown` is not `pass`, and treating an unchecked layer as clean is the most common way audits go wrong.
6. **Apply the Evidence Gate** (below). If it fails, the verdict is `insufficient evidence`: state exactly what additional days, spend, or access would clear it, and stop. No verdict on underpowered data.
7. **Issue the Root-Cause Verdict** (block below; worked versions in [references/examples.md](references/examples.md)). A compound verdict - two unrelated confirmed causes - is legitimate; rank them.
8. **Rank the findings by efficiency** (Prioritisation section) and write the handoff: which sibling skill or owner takes each finding, in rung order.
9. **Log the prediction.** Every verdict must state which metric should move, in which direction, by roughly how much, once the recommended fix ships - this is the raw material for the Measuring section.
10. Set a re-check date one full comparison window (at equal attribution-lag maturity) after the fix ships.
11. If your harness has persistent memory, memorise the account's baselines, the per-layer screen, the verdict, fixes applied, predictions, and re-check dates, so the next run starts from history instead of re-deriving it. If it does not, emit a short state block the user can paste into the next session.

If your harness can read the exports or run the calculations, compute every step directly; otherwise emit the exact export steps and spreadsheet formulas (columns, ratio, delta `(current - baseline) / baseline`) for the user to run and report back.

## The Layer Order

Fixed order, because each layer's evidence is only readable if the layers before it hold:

- **Tracking** corrupts every number.
- **Structure** corrupts the data pooling and learning that targeting and creative reads depend on.
- **Bidding** reads assume the auction inputs above it are sane.
- **Offer & downstream** sits past the click.
- **External** causes are a diagnosis of exclusion, claimed only when internal evidence rules the others out - the uniformity test in step 4 can fast-path there, but never skip the tracking check to get to it.

Baker's 8-layer framework states the why: auditing creative on an account whose pixel feeds 56% wrong data "produces conclusions that look right but are mathematically meaningless" - and across B2B SaaS accounts spending $3K-$250K/month he reports 80% of underperformance tracing to pixel health and creative diversity, not bidding or budget. This is a sequence, not a menu: the layers are not alternatives to pick between, so they carry no efficiency ranking - every one gets screened, in this order. The ranking lives one step later, over the _fixes_ the screen produces (see Prioritisation).

1. **Measurement / tracking** - is the conversion signal real, deduplicated, and consented?
2. **Structure** - fragmentation, overlapping campaigns self-competing, budget traps, wrong optimization event.
3. **Targeting** - audience overlap, saturation, too narrow/broad, wrong intent.
4. **Creative** - resonance decay; the differential itself runs in `mbfinotti/advertising-skills@ad-creative-fatigue`.
5. **Bidding / budget** - strategy-volume mismatch, learning state, impression share lost to budget vs rank.
6. **Offer & downstream** - price, promo, page, checkout; flag and hand to `mbfinotti/advertising-skills@paid-landing-page-audit`.
7. **External** - auction inflation, seasonality, competitor entry; confirmed by uniform elevation plus market evidence.

Per-layer confirming evidence, ruling-out evidence, and the check that settles each: [references/layer-evidence.md](references/layer-evidence.md).

## Evidence Gate

Refuse a verdict the data cannot carry. All four checks must pass before any layer FAIL becomes a verdict:

- **Conversion volume.** Enough conversions in both windows that the observed delta exceeds noise (band ≈ `p ± 2 × sqrt(p × (1-p) / n)` on the relevant rate). Attributed reference points, not laws: Google recommends evaluating automated bidding over periods with at least 30 conversions for Target CPA and 50 for Target ROAS (Google Ads Help), and OnlyDeb notes campaigns under roughly 15-30 conversions/month lack signal for the algorithm at all - low-volume accounts (most B2B) gate on leading metrics instead and say so in the confidence line.
- **Learning-phase state.** No verdict from data collected while delivery is recalibrating. Reference points: Meta ad sets typically exit learning after roughly 50 optimization events in 7 days (Meta Business Help Center, as relayed by AdStellar), and Google Smart Bidding can take up to three weeks or 1-2 conversion cycles (Google Ads Help). Niblin: ROAS swinging 20-50% day-to-day is normal during learning - judge only after exit or 7+ days.
- **Window comparability.** Baseline and comparison windows must have equal duration, equal attribution-lag maturity (recent days always under-report; a trailing window always "looks like" decline), matched day-of-week composition, and no known outages. Jyll Saskin Gales audits all active campaigns together over a 90-day window because campaigns "interact with each other" - never judge one campaign in isolation over a cherry-picked week.
- **Attribution consistency.** Never sum or compare conversions across differing attribution windows, counting methods, or models - a 7-day-click figure plus a 30-day-click figure is not a total, it is a category error. Report side by side until definitions reconcile; a settings change mid-window invalidates the comparison entirely.

When the gate fails: verdict `insufficient evidence`, plus the arithmetic of what clears it - the additional days or spend needed for `n` to shrink the noise band below the observed delta at current traffic, or the specific access (CRM export, ad-level breakdown) that is missing.

## Root-Cause Verdict

Deliver one block per diagnosis:

```
ROOT-CAUSE VERDICT - <account>, <date>
platform(s)    : <...> | model: B2B | B2C
window         : <comparison window> vs baseline <baseline window> (lag maturity matched: yes/no)
volume         : <spend>, <conversions> conversions in window | reconciliation gap: <x% vs backend | unverified>

decomposition  : <which link moved: CPM / CTR / CVR / AOV - direction and size vs own history>
localisation   : <uniform across account | concentrated in: campaign/ad set/ad>

layer screen
  measurement/tracking : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]
  structure            : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]
  targeting            : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]
  creative             : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]
  bidding/budget       : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]
  offer & downstream   : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]
  external             : pass | FAIL | unknown | n/a - <evidence>   [severity, confidence]

confidence     : high | medium | low - <basis: gate math, reconciliation state, unknowns count>
verdict        : <root cause layer(s), or insufficient evidence - with the one-sentence causal story>
evidence       : <the two or three observations that carry the verdict>
findings       : <ranked by efficiency - each with severity, confidence, outcome bought, effort, owner>
prediction     : <metric expected to move, direction, rough size, by when>
handoff        : <sibling skill or owner per finding, in sequence>
re-check       : <date - one full window after fix, lag-mature>
```

## Prioritisation

Rank findings before handing off - a flat list of twenty observations is a pitch deck, not a diagnosis. Rank by efficiency: the outcome each fix buys per unit of effort it costs. Never by cheapest, and never by the layer screen's own row order - the screen is a diagnostic sequence, the ranking is a work queue.

Default fix-class order, highest value/effort ratio first:

1. **Tracking repair** - buys back the readability of every other number in the account and puts delivery on a real signal again; costs hours to a day of one developer. Always ships first: every later fix is measured through it.
2. **Optimization-event / offline-outcome fix** - buys a platform that chases qualified outcomes instead of cheap volume (Koda: the offline feedback loop "consistently improves lead quality more than any targeting adjustment"); costs about a week of marketing-ops and CRM wiring, then keeps paying without further work.
3. **Structural consolidation** - buys starved units the conversion volume they need to exit learning; costs a week of rebuild plus one learning window of volatility, and un-merging later is expensive.
4. **Targeting redesign** - buys reach on audiences that are not yet saturated; costs about a week, and reverses cleanly.
5. **Offer & downstream fixes** - the outcome can beat everything above it, but the work sits outside the account: costs coordination with whoever owns the page, the price or the checkout, so their calendar sets the pace instead of the auditor's.
6. **Creative replacement** - buys the click back where decay is confirmed; costs a production cycle and never ends - a standing job, not a fix.
7. **Budget and bid moves** - buy nothing until every rung above passes, and each significant edit spends a learning window (see "Why 'Increase the Budget' Is the Wrong Default").

The axes disagree, which is exactly why the reflex fix keeps winning arguments:

- efficiency: tracking > event fix > consolidation > targeting > offer & downstream > creative > budget moves
- value: offer & downstream == tracking > event fix > consolidation > creative > targeting > budget moves
- effort: offer & downstream > creative > event fix == consolidation > targeting > tracking > budget moves
- compliance cost: event fix > tracking > every other rung (none) - pushing CRM outcomes into an ad platform triggers a data-processing and consent-basis review and cannot be un-sent; re-firing a conversion event touches the consent banner and the platform's data-use terms.

Budget moves sit last on effort and last on efficiency at once: near-zero effort buying near-zero outcome is not a cheap win, it is a rounding error with a learning reset attached.

**What this order starves: offer & downstream.** It ties tracking for the highest value on the page and carries the highest effort, so the ratio pushes it to rung 5 - and the default-rung rule then reaches it only after four other rungs pass or ship. An account can run this diagnostic for a year and never once touch the price, the offer or the page. Promote it to the top on either condition: the decomposition localises the failure past the click (CVR collapsed while CPM, CTR and impression share held), or the page, price and checkout owners sit on the user's own team - its effort was coordination cost, not work, and in-house ownership deletes that cost.

Default rung: start at the highest rung whose layer the screen marked `FAIL`, and never below rung 1 while tracking is `FAIL` or `unknown`. Move one rung down only once the rung above is `pass` or already shipped.

The ordering is a default, not a law - it shifts with the account and with who executes it. Re-rank it against what you already know here:

- An in-house developer makes rung 1 a same-day job.
- A creative studio already on retainer promotes rung 6 above its default place.
- A business that tolerates no learning-window volatility demotes rungs 3 and 7.

The Interview's deadline, one-off-versus-compounding and effort-ceiling answers move rungs the same way.

A constraint the user actually stated does something different from re-ranking: it removes the rung. Delete a ruled-out fix class from the ranked findings rather than parking it at the bottom, and name it as deleted in the handoff with the constraint that killed it and what would revive it - "offline-outcome loop: deleted, no CRM access anywhere in scope; revive when an export exists".

A fix left sitting last on a list nobody will reach is indistinguishable from one nobody has considered, and it comes back next quarter as a fresh idea. One exception: the fix the verdict names as the root cause is never deleted. It escalates to whoever can lift the constraint - a tracking FAIL under an effort ceiling with no developer time is an escalation, not a demotion and not a deletion.

Tag every finding with:

- **Severity**: what it costs if unfixed.
- **Confidence**: how sure the evidence is, kept separate from severity.
- **Outcome bought**: the fix's recoverable value (Conner Crowe's discipline of attaching one to each fix); mark "unquantified" when the data cannot say.
- **Effort**, as an order of magnitude: near-zero, an hour, a week, a quarter, a standing job.
- **Owner**: from the Interview's implementer answer.

Score with ICE (Impact, Confidence, Ease) by default. Reach for RICE (Reach × Impact × Confidence / Effort - Sean McBride at Intercom) only when the ranking must survive someone who did not run the diagnostic: `efficiency: ICE > RICE`, `value: RICE > ICE only when the plan has to be defended`, since ICE costs minutes and reproduces most of RICE's ordering while RICE costs an extra reach estimate and buys defensibility, not accuracy. Hand the plan off in rung order, each finding with its owner attached.

## Why "Increase the Budget" Is the Wrong Default

The most common prescription, and the one this skill exists to refuse. Four mechanisms, each sourced:

- **Learning resets.** Budget increases beyond roughly 20% in one edit are widely treated as significant edits that restart the learning phase on Meta (practitioner interpretation relayed by Modern Marketing Institute and Grow With Sakib); Grow With Sakib estimates each reset costs 5-15% ROAS the following week, with CPAs running 20-50% higher during learning. More money into a broken account buys a worse version of the same problem.
- **Budget vs rank.** Lost impression share splits into lost-to-budget and lost-to-rank (Adalysis; Workshop Digital) - and "simply increasing your budget won't guarantee a 100% search impression share if your ad rank is insufficient" (Workshop Digital). Diagnose the split first; if the loss is to rank, budget does nothing.
- **Diminishing returns.** Trustworthy Digital observes diminishing returns above roughly 60-80% impression share, where the next increment costs more than the qualified revenue it returns. Near the top of impression share, more budget buys the worst impressions in the auction.
- **Correlation is not incrementality.** Platform-reported conversions are claimed, not caused: "Platform ROAS, Google Analytics, and last-click all report claimed revenue. None of them show that a single dollar was incremental" (Stella). Lifesight reports a grocery chain's geo holdout on non-brand paid search finding a 0% sales lift. Scaling a channel because its dashboard looks good scales the claim, not the revenue. Ben Heath says it plainly: "Big budgets don't guarantee results. Great creative and a strong offer are a much better place to focus."

A budget recommendation is only ever this skill's output as a _handoff_ - to `mbfinotti/advertising-skills@ad-spend-allocation` or `mbfinotti/advertising-skills@paid-media-scaling` - after the diagnosis shows delivery is genuinely budget-capped and everything upstream passes.

## B2B vs B2C

The method is identical in both: same layer order, same decomposition, same gate, same verdict shape. What diverges is the data regime and which numbers tell the truth.

| Dimension           | B2B                                                                                                                                                                                                                                                                                                   | B2C/ecommerce                                                                                                                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Evaluation window   | Conversion volume is low and the sales cycle long (GrowthSpree cites an 84+ day average, with SQL/pipeline outcomes landing 30-90 days after the tracked conversion); evaluation windows stretch to 4-6 weeks minimum before data is reliable (Koda), and the Evidence Gate leans on leading metrics. | Volume supports the full statistical gate and daily reads.                                                                                                                                                |
| Dominant root cause | Optimising to the wrong conversion event: cheap form fills the platform can find in volume, while "leads look great in dashboard, sales say trash" (Happy Cog).                                                                                                                                       | Platform ROAS is "systemically inflated post-iOS14" (Eightx).                                                                                                                                             |
| Fix class           | The offline feedback loop: feeding CRM outcomes (MQL/SQL/closed-won) back to the platform, which Koda reports "consistently improves lead quality more than any targeting adjustment".                                                                                                                | Read blended measures instead of raw platform ROAS: MER (total revenue / total marketing spend; Superscale) judged against a margin-derived break-even (roughly 1 / contribution-margin %, per Meerkats). |
| Truth-telling KPI   | Cost per SQL and cost per closed-won - "the only KPI that tells the truth in B2B" (Swydo) - never CPL.                                                                                                                                                                                                | Contribution margin by product, since blended ROAS "hides the products destroying your margins" (Jordan Glickman).                                                                                        |
| Source of truth     | CRM.                                                                                                                                                                                                                                                                                                  | The order table.                                                                                                                                                                                          |

In both models, the reconciliation step in the Workflow is the same act, only the source of truth differs.

## Auditor Failure Modes and Biases

The account is not the only thing under diagnosis - so is the auditor. Screen the auditor's own read against this table before issuing a verdict.

| Trap                                        | Why it burns                                                                                                                                                                                              | Fix                                                                                      |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Anchoring on the previous owner's narrative | The first story heard becomes the hypothesis everything gets fitted to (inStreamly)                                                                                                                       | Ignore the inherited narrative until the data independently reproduces it                |
| Recency bias                                | Overweighting the last few days; daily noise mimics collapse                                                                                                                                              | Zoom out to weekly/monthly views before reading any intraday move (Go4Trades; Niblin)    |
| Confirmation bias                           | Data gets interpreted to support the strategy already in place (inStreamly)                                                                                                                               | Write the disconfirming evidence for the leading hypothesis before concluding            |
| Goodhart / metric fixation                  | Optimising the score, not the objective - Google's Optimization Score reaches 100% just by dismissing recommendations (Store Growers)                                                                     | Treat platform scores as means, never as the health verdict (Goodhart, 1984)             |
| Over-trusting platform-reported numbers     | "Meta claimed one number, Google claimed another, and the actual backend revenue was a third number entirely" (HYROS); every self-attributing platform reports as if it were the only channel (Enalitica) | Reconcile against backend truth first; never sum platform claims                         |
| The pitch-audit incentive                   | A free audit sold before a proposal is structurally biased toward "everything is wrong" (Conner Crowe)                                                                                                    | Findings need evidence and an outcome-per-effort estimate each, not a count of red flags |
| Fixing the layer where the symptom appears  | The visible metric is downstream of the cause; a CVR drop is rarely a CVR problem                                                                                                                         | Trace backward through the chain; fix at the source layer                                |
| One hypothesis, tested by fixing it         | Stacked unverified fixes destroy the baseline and the attribution of recovery                                                                                                                             | One falsifiable hypothesis at a time; predict the metric move before shipping the fix    |
| Benchmark shopping                          | Industry averages have different mix, geography, and definitions                                                                                                                                          | The account's own history is the baseline; benchmarks are directional context only       |
| Best-practice cargo-culting                 | Checklists applied without account context - there are "many different ways to structure a successful account" (Foxwell)                                                                                  | Every finding must cite this account's evidence, not a generic rule                      |

## Measuring Whether This Worked

This skill's KPI is diagnostic accuracy, tracked on a rolling log of every verdict and its step-9 prediction:

- **Prediction hit rate**: share of verdicts where the predicted metric moved in the predicted direction (at meaningful size, judged at the lag-mature re-check) after the recommended fix - and only that fix - shipped.
- **Overturn rate**: share of verdicts later overturned - a second diagnosis, an incrementality test, or the fix's failure showing the named root cause was wrong.

Starting floor - this skill's own working target, not a researched constant: iterate on the method until at least 70% of high-confidence verdicts hit their prediction and fewer than 15% of all verdicts are overturned, then tighten from the account's own log.

- A low hit rate with a clean gate usually means the layer evidence is being read too loosely.
- A high overturn rate concentrated in one layer means that layer's ruling-out checks are too weak.

Verdicts issued despite an `unverified` reconciliation line should be tracked separately - if they overturn more often, that is the argument for insisting on backend access next time.

## Reference

- Read [references/layer-evidence.md](references/layer-evidence.md) when walking the layer screen - per layer: confirming evidence, ruling-out evidence, and the check that settles it.
- Read [references/metric-decomposition.md](references/metric-decomposition.md) when localising the failing link - the CPM × CTR × CVR × AOV identity, the funnel chain, what each metric direction means, lost impression share, frequency, and learning-phase mechanics.
- Read [references/examples.md](references/examples.md) when writing the verdict block - a B2C case where the cause is tracking, a B2B case where the cause is the wrong conversion event, and a convincing false positive the Evidence Gate catches, plus the wrong move alongside the right one.
