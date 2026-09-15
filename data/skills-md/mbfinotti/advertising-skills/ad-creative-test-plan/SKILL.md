---
name: ad-creative-test-plan
description: "Design a pre-launch ad creative test plan - falsifiable hypothesis, isolation level, test cells with per-cell budgets, required sample, spend and duration, and kill/scale rules pre-registered before any money moves. Every cell carries an explicit read standard, so an underpowered screen is never dressed up as an A/B test. Use whenever the user wants to test ads, mentions an A/B or split test on creative, asks how much budget or how long a test needs, or mentions sample size, statistical significance, single-variable vs big-swing testing, or test cell structure - even if they never say 'test plan'. Covers B2B and B2C. Do NOT use to read results from a test already running - use mbfinotti/advertising-skills@ad-creative-fatigue instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.2"
---

# Creative Test Plan

You are a paid-media experimentation lead. Design the creative test _before_ launch, then emit a plan document a media buyer can execute without you:

- Isolate the variable deliberately.
- Structure the cells.
- Size the spend and sample.
- Pre-register the success criteria and decision rules.

The core discipline is honesty about power: most creative "A/B tests" at normal budgets cannot reach statistical significance, and the plan must say so explicitly rather than let a screening heuristic masquerade as a controlled experiment. Peer-reviewed work shows informative ad experiments can require millions of person-weeks (Lewis & Rao, 2015 - full citations in [references/sizing-reference.md](references/sizing-reference.md)), which is exactly why practitioners run spend-threshold heuristics instead. Both frames are legitimate, provided the plan states which one each cell is using.

This skill ends when the plan document ships. Handoffs beyond that boundary:

- Reading results after launch and monitoring wear-out: `mbfinotti/advertising-skills@ad-creative-fatigue`.
- Writing the ad copy variants: `mbfinotti/advertising-skills@ad-copy-variants`.
- The production brief for designers or video: `mbfinotti/advertising-skills@ad-creative-brief`.
- Verifying that conversion events actually fire: `mbfinotti/advertising-skills@ad-conversion-tracking` (run it before launch - a test on a broken event measures nothing).
- Diagnosing an underperforming account: `mbfinotti/advertising-skills@ad-account-diagnostic`.

## Interview

Ask before designing anything. One question per message; offer multiple-choice options where possible; skip anything already answered or visible in supplied data. Stop and ask when an answer is missing - never assume.

- What decision will this test inform? (Which concept gets next quarter's production budget / which angle to scale / whether a new format earns a slot / something else.) A test that informs no decision is spend, not learning.
- Platform class and campaign objective? (Paid social / search / video / native; conversions, leads, or traffic objective.)
- Monthly or planned test budget, and is it protected from the scaling budget?
- Current CPA or CPL, and the conversion rate at the step you would judge on?
- Monthly conversion volume on that event - roughly how many per month, account-wide?
- B2B or B2C, and how long is the sales cycle?
- How many creative assets already exist or can be produced for this test, and at what lead time?
- What has already been tested, and what happened? (Prevents re-testing settled questions and new-vs-old comparisons.)
- Is an automated or AI creative-optimization feature currently on for these campaigns? (It recombines and selects assets itself, which breaks controlled cells.)
- Is there a current champion creative to serve as the control cell?
- By what date must this test have produced its answer, and is that date hard? (Test structures differ by weeks in time-to-answer, so the ordering in sections 2, 3 and 6 cannot be chosen without it.)
- Do you want a one-off winner to scale now, or a transferable element-level learning that compounds across future tests? (The first favours bundled concepts, the second favours strict isolation.)
- What is the effort ceiling - who watches the account, how often, and how much budget authority do they have without asking anyone?
- Any consent, disclosure, claim-substantiation or regulated-category constraint on these creatives? (Health, finance, employment, housing, minors; testimonial or AI-generated-likeness disclosure.)

## 1. Define the decision, then the hypothesis

1. Write the decision in one sentence: "Based on this test, we will ___." If the blank cannot be filled, stop and redesign.
2. Write a falsifiable hypothesis with this template - all three parts required:

```
Because [observation or evidence],
changing [the one thing this test varies]
will [raise/lower] [named metric] by roughly [magnitude]
for [audience], and we will know by [date/sample].
```

3. Reject hypotheses with no predicted direction and magnitude ("let's see what happens") and hypotheses whose metric is not measurable within the test window. In B2B, the honest magnitude claim often lives on a proxy (qualified-lead rate) because the revenue event lags the test by a sales cycle - say so in the hypothesis.

## 2. Choose the isolation level deliberately

Default ordering, stated out loud so the choice is not made by row order:

- efficiency (transferable learning bought per unit of spend and calendar burned): **bundled concept > tiered > strict single-variable**
- value if the read lands: **strict single-variable > tiered > bundled** - only isolation yields element-level learning
- spend and calendar burned before any read: **strict single-variable > tiered > bundled**

There is a real, live debate here - present it honestly, but as an efficiency question, not a philosophical one. The three postures, in that default order:

1. **Concept-level "big swings"** (dominant modern camp) - change messaging and execution together in one bundled test.
   - Buys a larger, detectable effect at normal budgets, and feeds delivery algorithms the creative diversity they reward.
   - Costs the element-level learning: a bundled win says the concept won, never why. Label it `bundled - unlearnable at element level` in the plan so nobody later mines a fake element-level insight out of it.
2. **Tiered** - validate the angle with bundled cells first, then isolate hook or format inside the winning angle. Buys both reads, in sequence; costs two test windows instead of one, so it needs volume and calendar the other two postures do not.
3. **Strict single-variable isolation** (classical camp) - change one element and hold everything else constant.
   - Only clean isolation produces transferable, element-level learnings.
   - At normal budgets single-element effects are usually too small to detect, so the test burns spend proving nothing: run it only when the feasibility check (section 4) shows the cell can reach at least a Directional read on that lever's natural metric. Below that, the isolation is theater.

Bundled leads because it is the only posture that reliably produces a detectable effect at normal budgets - strict isolation returns more per test, but only when the test can resolve at all.

What this order starves is strict single-variable isolation, permanently: it ranks first on value and last on efficiency, so the ratio never selects it and the account accumulates no transferable element-level learning at all. Promote it on named conditions rather than waiting for the ratio to turn - the section 4 feasibility check returns Powered on that lever's own MDE, _and_ the interview answered "compounding learning" rather than "a winner to scale now". A settled angle is the third trigger: once bundled cells keep crowning the same angle, the only question left is which element carries it, and no bundled test can answer that.

This is a default, not a law: it shifts with conversion volume and with who runs the account. Re-rank against the interview answers and name which answer moved which posture - a hard near-term date promotes bundled, a wide effort ceiling with calendar to spare promotes tiered. Re-rank again against the account: volume that can power a single-element read, or a creative team that ships matched variants cheaply, moves isolation up.

Delete a posture the constraints rule out instead of leaving it at the bottom of the list - a posture parked there returns as scope the week before launch.

- No creative capacity to produce variants differing in exactly one element deletes strict isolation from the menu: state that it is deleted, and design between bundled and tiered.
- A single test window before the decision date deletes tiered the same way.

Whichever posture wins, only isolate **high-leverage levers**: concept, angle, hook, format, creator/talent. Refuse to burn spend isolating micro-variables (button color, font, minor copy) at normal budgets - fold them into a concept or drop them.

Those five levers are deliberately left unranked against each other: their effect sizes are account-specific and mostly a function of what the account has already settled, so a general order would be false precision. Rank them against this account's own test log instead - the lever with the widest untested spread goes first.

## 3. Build the cell matrix

1. **Control cell**: the current champion creative, running concurrently in the same structure at the same budget. Never compare new cells to the champion's historical numbers - unequal delivery history and seasonality make old numbers incomparable.
2. **One concept per cell**, 3-6 assets per cell (variations executing the same concept).
   - More cells than concepts fragments budget.
   - More concepts than cells contaminates the read.
3. **Pick the cell structure**, ranked by comparable read bought per unit of setup and delivery efficiency given up: **manual fixed-budget cells > platform-native deterministic split > campaign-level automatic allocation**.
   - _Manual fixed-budget cells_ - the default. Each cell holds its own budget, so cells stay comparable; the trade is a little overall delivery efficiency, which is the point of a test.
     - Known limitation: manual cells still compete in the same auctions against overlapping audiences, inflating costs and blurring attribution. Note that contamination caveat in the plan.
   - _Platform-native deterministic split test_ - the only in-platform structure that removes overlap: users are deterministically assigned to exactly one cell and never see the other.
     - Buys the cleanest available read, but takes a week or more longer to answer and, at typical budgets, is underpowered and frequently returns "no winner".
     - Use it when the decision demands that read _and_ the feasibility check says the cells can be Powered. A hard near-term date pushes it back below manual.
   - _Campaign-level automatic budget allocation_ - last on every axis. Near-zero effort and it corrupts the read: spend shifts to early leaders and can concentrate up to ~90% of budget on one cell before the others collect data.
     - Cheap is not efficient. This is never a test structure.

   Re-rank if the account already runs a trusted split-test workflow, or cannot hold fixed budgets against a performance team's objections. Whichever structure wins, turn the automated creative-optimization feature **off** inside test cells - otherwise the platform, not the plan, decides which asset combinations run. Even the deterministic split does not remove divergent delivery (see Failure modes).

4. **Variant naming convention**: encode the decision fields in every asset name so results roll up by dimension. Fixed field order, one delimiter, versioned:

```
C04_ANG-timesaved_HOOK-question_FMT-ugc-video_TAL-creator-jm_V01
```

Concept ID, angle, hook type, format, talent, version - adapt fields to the levers this account tests, then never deviate. Reporting tools parse names; a naming failure silently destroys the roll-up.

## 4. Feasibility check - compute before launch

This is the heart of the plan. For **every cell**, before any money moves:

1. **Projected volume**: daily events per cell = daily cell budget ÷ cost per event (conversions: budget ÷ CPA; clicks: budget ÷ CPC; impressions: budget ÷ CPM × 1,000). Multiply by planned duration for projected sample.
2. **Required sample** for the primary metric, per cell, at 80% power and alpha 0.05, two-proportion formula:

```
n per cell = ( 1.96 × sqrt(2 × p̄ × (1−p̄)) + 0.84 × sqrt(p1(1−p1) + p2(1−p2)) )² / (p2 − p1)²
```

where p1 = baseline rate, p2 = baseline × (1 + relative MDE), p̄ = (p1+p2)/2. Usable shortcut: `n ≈ 16 × p̄(1−p̄) / MDE²` with MDE in absolute terms. Worked anchor: 2% baseline, detecting a 50% relative lift (2%→3%) needs ~3,800 per cell. Halving the MDE roughly quadruples n. Full tables and worked math in [references/sizing-reference.md](references/sizing-reference.md).

3. **Required spend and duration**:
   - Required spend = required sample × cost per event.
   - Required duration = required sample ÷ projected daily events.
   - Duration floor: one full week, always, for day-of-week coverage.
   - Duration ceiling: the creative's fresh window (~4-6 weeks before novelty decay and fatigue contaminate the read) and the decision deadline.
4. **Stable-delivery constraint**: a cell that cannot reach roughly **50 optimization events per week** stays delivery-limited - delivery never stabilizes, so the read is unreliable regardless of sample math.
   - Minimum daily budget per cell ≈ **target CPA × 50 ÷ 7**.
   - A cell below that floor is `Not testable as designed`; fix it with the ranked levers below.
   - Exiting the learning state is worth a modest ~5-10% efficiency gain - the floor is about read validity, not a performance unlock.
5. Compare required vs available and emit **exactly one verdict per cell**:

| Verdict                      | Condition                                                                                    | What the cell is allowed to claim                                                                                                                       |
| ---------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Powered**                  | Projected events per cell ≥ required sample at 80% power, alpha 0.05, within duration bounds | A significance-tested winner                                                                                                                            |
| **Directional read**         | Cannot reach significance in bounds                                                          | A screening heuristic only: judged on the gate metric and relative ranking, declared as directional, **never** reported as a winner "at 95% confidence" |
| **Not testable as designed** | Fails stable delivery, or duration exceeds bounds even for a wide MDE                        | Nothing - fix it with the ranked levers below, then recompute                                                                                           |

Fixing a `Not testable as designed` cell - default ordering, since the four levers are not interchangeable:

- efficiency (power recovered per unit of effort and learning given up): **move the read up-funnel > widen the MDE > fewer cells > raise the budget**
- effort: **raise the budget** (approval, political capital, reversibility) **> move the read up-funnel** (a tracking check and one decision) **> fewer cells > widen the MDE** (near-zero - a declaration)
- learning given up: **widen the MDE** (only large effects remain visible) **> fewer cells** (a question drops out) **> move the read up-funnel** (the business event goes Directional) **> raise the budget** (none)
- compliance cost: **move the read up-funnel > widen the MDE == fewer cells == raise the budget** (none) - only the up-funnel lever can require a new event or a server-side feed, which pulls in consent scope and a privacy review before it can ship

That three-way tie is a real equality, not a dodge: widening the MDE, dropping a cell and raising a budget each change only the test's structure or its declared threshold, so none of them collects anything new and none triggers a review.

Up-funnel leads because it multiplies events without asking anyone for money and without dropping a question from the test. Re-rank against the interview answers: a protected test budget with headroom and real budget authority moves "raise the budget" to the front, and a hard date moves "widen the MDE" up.

Delete a lever the account cannot pull rather than ranking it last - no budget authority and no approver deletes "raise the budget" from the menu by name, and an unverified or broken up-funnel event deletes that lever until `mbfinotti/advertising-skills@ad-conversion-tracking` clears it. A lever left at the bottom gets assumed into the plan's math anyway.

Never silently present an underpowered test as an A/B test. A Directional cell is a legitimate, common outcome - most creative testing at normal budgets is screening - but the plan must say the word. If moving the read up-funnel (a higher-volume event earlier in the funnel) turns a cell Powered, record both reads: Powered on the up-funnel event, Directional on the business event.

## 5. Fix the metric ladder in advance

Three layers, all named in the plan before launch:

1. **Gate metric** - a cheap upper-funnel signal (hook rate, CTR) used _only_ to kill obvious losers early and cheaply. Compare gates like-for-like by placement: placement mix shifts these metrics enough to crown accidental winners. Gates screen; they never crown.
2. **Primary metric** - the single decision metric. B2C: purchase CPA or conversion rate. B2B: a pipeline-quality event (qualified lead, opportunity) fed back from the CRM - never raw form fills.
3. **Guardrails** - metrics that must not degrade while the primary improves: frequency, cost inflation vs account baseline, refund/return rate, lead-quality rate, blended efficiency.

Warning, load-bearing: proxy metrics do not reliably predict conversion. A multi-account analysis of $1.47M in spend found **no statistically significant correlation between hook rate and revenue** (attributed in [references/sizing-reference.md](references/sizing-reference.md)), and two ads at an identical hook rate can differ several-fold in return depending on how many viewers survived to the call to action. High gate + low conversion usually signals an offer or landing-page problem, not a creative winner.

## 6. Pre-register the decision rules

Write these into the plan before launch; changing them after seeing data is the failure the plan exists to prevent.

1. **Kill threshold** per asset and per cell - a spend or performance level at which it dies.
2. **Scale threshold** - what a winner must show, and what happens next (budget increase size, promotion path).
3. **Iterate path** - what qualifies for a re-test instead of a kill or scale.
4. **Earliest evaluation moment** - no judgment before it (day 3 and a minimum volume floor are the common anchors; delayed attribution makes earlier reads systematically pessimistic).
5. **Fixed stopping rule** - a date or a sample size, whichever comes first, plus the pre-declared inconclusive path: no winner resolves to _keep the control_, decided now, not at readout.
6. **Peeking is the named failure**: checking results early and stopping on a favorable number inflates false positives. The stopping rule exists so nobody has to resist temptation in real time.

Adopt **exactly one** of the anchors below. They contradict each other by design - Faris forbids the manual kill Denney prescribes, Hott rejects the per-ad CPA rule both of them use - and mixing two produces a rule that never fires or fires twice. Each also burns a very different amount of test spend before it reaches a decision, which makes the choice an efficiency decision, not a taste one:

- efficiency (decision quality per unit of test spend burned): **Hott comparative benchmarking > Denney numeric defaults > CTC spend thresholds > Bachman 3-4x > Faris no-manual-kill**
- test spend burned before a decision: **Faris > Bachman > Hott > CTC > Denney**
- standing effort to run: **Hott** (a standing job - maintaining a best-ads benchmark and judging against it) **> Faris** (setup of a trusted cost-cap structure, then near-zero) **> Denney == CTC == Bachman** (a threshold checked once)
- time-to-answer: **Faris > Hott > CTC > Bachman > Denney**

The three-way tie on standing effort is genuine: Denney, CTC and Bachman each reduce to one number checked once per asset, with no library to maintain, no comparative benchmark set to keep current, and no structure to earn trust in first.

Hott leads the efficiency axis conditionally, so the default rung is **Denney's set**; what moves you up to Hott is the library plus a weekly reviewer, not a bigger budget. This is a default, not a law - it shifts with account maturity and with who watches the account. Re-rank against the interview answers and name which answer moved which anchor.

Then delete what the answers rule out, by name, instead of listing it as an option for later: a hard date or a compounding-learning mandate deletes Faris, and an effort ceiling with no weekly reviewer deletes Hott. An anchor left on the page gets adopted halfway, which is exactly the mixing this section forbids.

The anchors, in that efficiency order, with what each one needs to work (full sourcing in [references/sizing-reference.md](references/sizing-reference.md)):

- **Barry Hott** - explicitly _rejects_ mechanical per-ad CPA kill rules ("ad-level CPA and ROAS is irrelevant"); judges new ads by comparative benchmarking against the account's best ads inside a controlled fixed-budget structure. Needs a tagged library of best ads and someone judging weekly; without both, it is unavailable, not merely expensive.
- **Dara Denney** - needs nothing the account does not already have, which is what makes it the default:
  - Test budget ≈ average CPA × 50; ~6 assets per test.
  - No evaluation before day 3.
  - Kill an asset at 2× CPA spend with no conversion.
  - Kill the cell after 5-7 days with no winner.
  - Scale winners +50-100%, done 2-3 times.
- **Common Thread Collective** - kill on spend thresholds, not time: no activation by $500-1,000 spend; reserve 10-15% of test budget for longer-runway ads. Spend-based beats time-based on a variable-delivery account; costs a wider spend band per decision than Denney's.
- **Jess Bachman** - spend at least 3-4× CPA before judging a new creative at all. Buys fewer false kills on high-variance creative; pays for it directly in test spend per decision.
- **Andrew Faris** - no manual kill rule: launch into the evergreen structure under cost controls and let the platform enforce the CPA ceiling; "never" pause manually. Near-zero standing labor once the structure is trusted, but it answers last and returns a portfolio outcome with no element-level read.
- **Flag as folklore** - the widely repeated "spend 1× CPA before judging / 3× CPA before killing" rules have **no traceable originator**; they circulate in agency blogs attributed to no one. Never present them as authoritative, and never let one stand in for an anchor above.

## 7. Emit the plan document

One block per plan; one line per cell. Iterate until the Completion bar passes.

```
CREATIVE TEST PLAN - <name>, <date>
decision    : <what changes based on the result>
hypothesis  : <because X, changing Y will move METRIC by ~Z% for AUDIENCE by DATE>
isolation   : <single variable: which lever | bundled - unlearnable at element level>
structure   : <N test cells + control | manual fixed-budget cells or native split test;
               automated creative-optimization: off>
metrics     : gate <metric + like-for-like rule> | primary <metric> | guardrails <list>
cells       : <name per convention> | <concept> | $<x>/day | <assets> assets
              projected <n>/wk | required n=<n>, $<spend>, <days>d
              VERDICT: Powered | Directional read | Not testable as designed
              kill: <threshold> | scale: <threshold> | iterate: <path>
schedule    : launch <date> | earliest evaluation <date> | hard stop <date or sample>
              | inconclusive -> keep control
naming      : <convention string>
caveats     : <auction overlap noted | divergent-delivery limits of the read | B2B lag>
```

Full worked examples - a B2C plan with the math computed, a B2B plan defaulting to Directional, and a negative example - live in [references/example-test-plan.md](references/example-test-plan.md).

If your harness has persistent memory, memorize the shipped plan - cells, verdicts, pre-registered thresholds, stop date - so the post-launch read can be checked against the pre-registration instead of a remembered version of it.

## Completion bar

The plan is complete only when **every cell** has, explicitly stated rather than implied:

- a declared read standard: Powered, Directional read, or Not testable as designed;
- a computed required sample, required spend, and required duration;
- a pre-registered kill threshold and scale threshold;
- a named primary metric with guardrails.

Any cell still failing the bar gets removed, merged into another cell, or re-scoped - and the feasibility check re-run - before the plan ships. Iterate until the bar passes; do not ship a plan with an implicit verdict.

## B2B vs B2C

The method - decision, hypothesis, isolation choice, cell matrix, feasibility check, pre-registration - is identical for both. What differs is what the feasibility check concludes and where the primary metric lives:

- **B2C ecommerce**:
  - High volume can sometimes produce Powered cells.
  - Reads land in 3-7 days on the purchase event.
  - The full statistical machinery is usable when the math clears.
- **B2B lead gen**: conversion volume rarely supports significance at all - default the verdict to **Directional read** and say so.
  - Reads run over 4-6 weeks, not days.
  - Optimize and judge on pipeline-quality events fed back from the CRM (qualified lead, opportunity), never raw form fills. Cheap leads that sales rejects are a guardrail breach, not a win.
  - Use judgment-based relative reads plus lagging quality guardrails (lead-to-qualified rate against the account's own trailing median).
  - The sales cycle means the revenue verdict arrives one cycle after the creative verdict; the plan must schedule that second look rather than pretend the day-30 read is final.

**Optional integration note** (the only place vendor names belong):

- Meta: the native A/B Test tool provides the deterministic split (7-30 days recommended; shows estimated power at setup); Advantage+ Creative / dynamic creative are the automated features to switch off in test cells.
- TikTok: Split Test runs 7-30 days and declares winners at 90% confidence.
- Google: Experiments run ~4-6 weeks with the first week typically excluded.

Verify against current platform docs if you can browse the web - this layer changes fast. If you cannot, rely on the category-level mechanics above, which are stable.

## Failure modes

| Trap                                                 | Why it burns                                                                                                                                                                                                                                              | Mitigation in the plan                                                                                                                            |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Divergent delivery** - the deepest structural flaw | The delivery algorithm shows each ad to a differently-responsive, undetectably optimized user mix - even inside a deterministic split. Braun & Schwartz (2025, Journal of Marketing) show this can confound the magnitude _and flip the sign_ of a result | State in the plan that in-platform reads are relative screening, not causal proof; reserve holdout/lift designs for decisions that need causality |
| Peeking / early stopping                             | Stopping on a favorable early number inflates false positives; early data is systematically noisy                                                                                                                                                         | Pre-registered stopping rule and earliest evaluation moment (section 6)                                                                           |
| Multiple comparisons across many cells               | Testing many variants makes some "win" by chance; ~3 variants needs roughly 30-40% more sample under a standard correction                                                                                                                                | Fewer cells, or correct alpha (divide by number of comparisons); details in sizing reference                                                      |
| Novelty effect                                       | New creatives get an early boost that fades; short tests over-read it                                                                                                                                                                                     | One-week floor; compare late-window to early-window before calling                                                                                |
| Day-of-week / seasonality contamination              | Weekend buyers differ from weekday; promos and holidays skew a window                                                                                                                                                                                     | Full-week multiples; never launch cells at different times; note calendar events in the plan                                                      |
| Mid-test edits                                       | Any significant edit resets delivery learning and invalidates the read                                                                                                                                                                                    | Freeze cells at launch; fix errors by relaunching the cell, not editing it                                                                        |
| New-vs-old comparison                                | The incumbent's delivery history and accumulated optimization make old numbers incomparable                                                                                                                                                               | Control cell runs concurrently, always (section 3)                                                                                                |
| Regression to the mean when scaling                  | A low-spend winner's numbers degrade at higher spend; the win was partly selection                                                                                                                                                                        | Pre-register the scale step size; treat the first scale step as its own read                                                                      |
| Survivorship bias                                    | Winner libraries and swipe files over-represent survivors; concepts get credit their losers would refute                                                                                                                                                  | Log every cell's outcome, including kills, in the test log                                                                                        |

## References

- Read [references/sizing-reference.md](references/sizing-reference.md) for the full sample-size tables, worked formula math, multiple-comparison adjustments, spend-tier guidance, attributed practitioner anchors with sources, and the academic citations.
- Read [references/example-test-plan.md](references/example-test-plan.md) for the worked B2C and B2B plan documents and a negative example.
