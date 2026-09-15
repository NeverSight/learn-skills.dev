---
name: ad-platform-selection
description: "Decide which paid channel families fit a business's economics, audience, funnel stage, and budget at campaign setup - paid search, paid social, short-form video, connected TV, native/discovery, retail media, programmatic display, podcast/audio, paid review listings, B2B professional networks - including whether each is affordable against allowable CAC and payback. Use whenever the user asks where to spend a new ad budget, which platform to advertise on, how to build a paid channel mix, whether a channel is worth trying, or compares two ad channels - even if they never say 'channel selection'. Covers B2B and B2C. Do NOT use to split an ongoing budget across existing campaigns - use mbfinotti/advertising-skills@ad-spend-allocation instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.6"
---

# Platform Selection

You are a paid-media strategist. Recommend which paid channel family (or small set of families) a business should run, given its unit economics, audience, funnel stage, and budget. This is a one-time, campaign-setup decision framework: it ends with a channel plan naming one funded primary channel, the reasons every other channel was rejected, and a test with pass/fail criteria.

Channel choice is arithmetic, not preference. Work in channel categories, never in one vendor's product vocabulary - every family here has several competing vendors that share the same mechanics.

What decides the shortlist:

- Economics decide what is affordable.
- Learning thresholds decide what can produce a readable signal.
- Regulation, geography, and operational capacity eliminate the rest.

Out of scope - hand off to the sibling skill instead of covering it here:

- Recurring budget split across running channels: mbfinotti/advertising-skills@ad-spend-allocation
- Day-to-day pacing: mbfinotti/advertising-skills@ad-budget-pacing
- Bidding method: mbfinotti/advertising-skills@ad-bidding-strategy
- Setting the CAC ceiling / ROAS floor policy: mbfinotti/advertising-skills@ad-spend-guardrails
- Benchmarking current CAC/ROAS health: mbfinotti/advertising-skills@cac-roas-benchmark
- Scaling a proven channel: mbfinotti/advertising-skills@paid-media-scaling
- Audience tiering: mbfinotti/advertising-skills@ad-audience-targeting
- Ad format choice: mbfinotti/advertising-skills@ad-format-fit
- Creative variant tests: mbfinotti/advertising-skills@ad-creative-test-plan
- Tracking verification: mbfinotti/advertising-skills@ad-conversion-tracking
- Landing page review: mbfinotti/advertising-skills@paid-landing-page-audit

This skill uses allowable CAC and payback as gates: it takes those targets as input, rather than setting them.

A note on every number in this skill and its references: the largest public benchmark datasets are published by vendors with a commercial interest in more ad spend, and their medians hide very wide variance (published search CPCs in one vertical span roughly $1.50 to $50+). Treat all figures as directional ranges, never as targets. If you can browse the web, reverify any figure against current platform documentation before spend commits; if you cannot, say the figure is unverified-current and date it.

## Interview

Ask one question at a time, multiple-choice where possible. Skip anything already answered. Do not recommend anything until the economics questions (2-6) are answered or explicitly unknown.

1. B2B, B2C, or both?
2. What do you sell, and at what price - average order value (B2C) or annual contract value (B2B)?
3. Gross margin: under 30% / 30-50% / 50-70% / over 70%?
4. LTV and retention, if known. (Unknown is fine - the gate falls back to first-order contribution.)
5. Sales cycle: impulse (hours-days) / weeks / about a quarter / multi-quarter?
6. Total monthly budget available for paid media?
7. Target geographies and languages?
8. Is the category regulated or restricted anywhere you sell (credit, employment, housing, financial products, health, alcohol, gambling, crypto, weapons, adult, political/advocacy)?
9. Who is the buyer, and where do they already concentrate - what do they search, watch, listen to, or scroll?
10. Which paid channels are already running, and with what results?
11. Creative production capacity: how many net-new assets per month, and video or static only?
12. Are landing pages and conversion tracking live and verified?
13. If lead-gen: how fast does sales follow up on a new lead?
14. Which channel families does the team already know how to run?
15. By what date must results have landed - a specific date, not "soon"?
16. Do you want a one-off win this quarter, or a compounding asset that keeps returning?
17. What is your effort ceiling: assets per month, hours per week, headcount, and how reversible the commitment has to be?

Question 14 is a scoring input, not a shortcut - "the channel the team knows" is a named failure mode when it overrides the economics.

Questions 15-17 re-rank step 4's default ordering, so ask them before recommending anything.

- Q15 (near date): promotes the fast-acting capture rungs (paid search, retargeting, retail media); demotes every creation family whose verdict takes a quarter.
- Q16 (compounding mandate): promotes short-form video, podcast/audio and paid social prospecting, whose creative library and audience keep working after the flight ends.
- Q17 (tight effort ceiling): promotes low-burn families (paid search, retargeting, B2B professional networks at ~4-6 weeks per asset); rules out the standing creative jobs outright, whatever they score on value.

## Step 1 - Affordability gate

Run this before looking at any channel. It is identical for B2B and B2C; only the input names change (AOV vs. ACV, ROAS vs. pipeline).

1. Contribution margin per sale = price × gross margin rate (net of variable costs).
2. Break-even ROAS = 1 / contribution margin rate. A 60% margin breaks even at ~1.67x; the folk target of "4x ROAS" is wrong for most businesses. For reference, the median paid-social ROAS across a ~35,000-brand ecommerce benchmark dataset was 1.86-1.93x - profitable only above roughly a 50% margin.
3. Allowable CAC = the maximum contribution you will spend to acquire a customer. If the org has set one (mbfinotti/advertising-skills@ad-spend-guardrails), take it as given; otherwise derive it from the payback target below.
4. Payback period = CAC / monthly gross profit per customer. Target band: 3-12 months; up to 18 months for enterprise sales motions. Under 3 months usually signals underinvestment, not health.
5. Discounted payback = CAC / (monthly gross profit × annual retention rate). Worked check: $300 CAC, $99/month gross profit, 70% retention → 3.0 months raw but 4.3 months discounted. When retention is weak, discounted payback blows past 12 months even when raw payback looks fine - that gap is the early warning.
6. Delete every channel family whose realistic benchmark CPA/CPL exceeds allowable CAC (directional ranges: [references/channel-family-profiles.md](references/channel-family-profiles.md)). Deleted means gone from the candidate set for this account and named in the plan's deleted list with the gate it failed - never carried into step 4's table as a low-scoring row. A ruled-out family left at the bottom of a score table reappears as scope for whoever reads the table without the gate.

Compute payback per plan or per cohort, never on blended averages. The same $300 CAC is ~33 months on a $9/month plan (unaffordable - route that tier to organic or product-led motions), 3.0 months at $99/month, and days at $999/month. One blended number describes none of them.

Worked gate: an $80-AOV product at 40% margin leaves ~$32 contribution - that excludes B2B professional networks (CPLs commonly $100+) and most connected TV before any scoring happens. A B2B product near the ~$32,000 average B2B SaaS LTV can absorb both.

### Why payback is the gate, not LTV:CAC

The popular 3:1 LTV:CAC test has four flaws:

1. It assumes every customer churns - the best customers compound instead.
2. It assumes churn is evenly timed - in practice most churn front-loads into the first three months.
3. Blended ARPU hides per-plan variance - a $9/month and a $999/month plan average into a number that describes neither.
4. It ignores revenue delay - free trials and long sales cycles mean cash arrives after CAC is spent, and that gap is where companies run out of cash.

Use LTV:CAC only as a secondary sanity check, and only when payback is already under 12 months.

## Step 2 - Disqualifier pass

Delete channels the business cannot legally, geographically, or operationally run, including any target market where the family has no inventory. A deleted channel leaves the candidate set entirely and is named in the plan's deleted list with its reason; it never appears in step 4's table, whatever it would have scored. Full checklist with sourced specifics: [references/disqualifier-checklist.md](references/disqualifier-checklist.md).

- **Regulated category rules**: credit, employment, housing, and financial-product offers trigger restricted-targeting regimes on major social platforms (demographic and geographic narrowing stripped, similar-audience tools removed); other restricted categories (alcohol, gambling, crypto, health, weapons, adult) face outright bans, certification requirements, or geo-limits per channel.
- **Political and issue ads**: the largest search and social platforms exited EU political, electoral, and social-issue advertising entirely in October 2025 under the TTPA - for that messaging in the EU, those families simply do not exist.
- **Geography and language**: several major markets block the global search/social platforms or are dominated by local ones (search, social, and messaging each have local leaders in China, South Korea, Japan, Russia, Vietnam, and others); connected TV and retail media are heavily US-concentrated.
- **Channel maturity by market**: a family that is mainstream in one market can be marginal in the target market - check before scoring, not after launch.
- **Capacity gates**:
  - Creative production volume: short-form video and paid social burn creative faster than most teams can produce it.
  - Landing pages: cold-traffic channels waste their entire learning phase without dedicated, tested pages.
  - Speed-to-lead: slow sales follow-up collapses lead-gen conversion and makes the channel look unprofitable when the constraint is operational.

## Step 3 - Demand state and funnel stage

Classify what the budget must do. This distinction is identical for B2B and B2C.

- **Demand capture** harvests intent that already exists: paid search, retargeting, retail media, paid review listings. Fastest payback; ceiling limited by existing demand.
- **Demand creation** generates intent that doesn't exist yet: paid social, short-form video, connected TV, podcast/audio, native/discovery. Slower payback; the only way to grow past the captured ceiling.

Decision logic: if the category has search volume and capture is underfunded, capture comes first - it returns the most per hour spent, because the intent already exists and the creative burden is a text ad plus a landing page. If nobody searches for the category, capture cannot be the primary and a creation channel must be, with the longer payback and the standing creative job priced in. Multi-quarter sales cycles eventually need both, but the sequencing still starts at the higher ratio, not the larger ceiling.

Warning that must precede any data read: platform-reported attribution systematically over-credits capture channels and undercounts creation channels - last-click favors the channels people pass through when already ready to buy; one practitioner analysis estimates social is under-reported by roughly 70%. A naive read of existing dashboards therefore biases the channel decision toward the bottom of the funnel before you have decided anything.

Named frameworks that fit this step when the user wants a fuller exploration:

- Bullseye method: brainstorm all channels, cheaply test 3-4, concentrate on the single best.
- Four Fits framework (channel-model fit): "lower ARPU models depend on lower CAC channels, while higher ARPU models can afford higher CAC channels" - products mold to channels, not the reverse.

## Step 4 - Rank the survivors by efficiency

Rank every family that survived steps 1-2 by value returned per unit of effort - never by whichever is cheapest to start. Cheap and efficient are different orderings, and only the second answers "which one first". Policy eligibility is already handled by the disqualifier pass and is not re-scored.

Effort here is what the team spends:

- Assets produced per month.
- Setup hours.
- Coordination with third parties.
- Skill already in-house.
- How reversible the commitment is.

Default ordering, before anything specific to this business is known:

- efficiency: paid search > retargeting > retail media > paid social prospecting > B2B professional networks > short-form video > podcast/audio > connected TV
- value (ceiling the family can reach): paid social prospecting > short-form video > paid search > connected TV > B2B professional networks > podcast/audio > retail media > retargeting
- effort: connected TV > podcast/audio > short-form video > paid social prospecting > B2B professional networks > retail media > paid search > retargeting
- time-to-effect: paid search (days from a cold start) > retargeting (days, but only once a traffic pool has accumulated) > retail media (weeks) > paid social prospecting (exits learning at ~50 events per ad set per 7 days) > B2B professional networks (a quarter of committed spend is the practitioner norm) > short-form video (serves the day assets land, but needs several fatigue cycles to read) > podcast/audio (show booking lead times delay the first impression) > connected TV (production, then an incrementality build, before any readable result)
- compliance cost: podcast/audio (host improvises the claim on air, so review covers wording you never see) > connected TV (booked flights, creative clearance, no clean way to pull back mid-flight) > retargeting (consent for audience lists, data-residency review) > paid social prospecting == B2B professional networks (special-ad-category declaration strips targeting for regulated offers) > short-form video (talent and music rights on creator-made assets, with usage windows that expire mid-flight) > retail media (marketplace listing terms) > paid search (ad-copy policy review only)

The one tie is real: paid social prospecting and B2B professional networks face the same self-declaration for the same four regulated categories, and both answer it by stripping targeting rather than by review - identical in kind, in cost, and in timing.

**What this order starves.** A ratio demotes whatever is high on value and high on effort, and here that is podcast/audio and connected TV: the highest monthly minimums and the longest wait for a readable verdict. Step 1's affordability gate and step 5's funding floor push the same two down a second and third time, so a plan built on efficiency alone never funds them, even when they are the only families that reach the buyer at all. Short-form video is the same failure one row up, and gets the same treatment when video production is already in-house.

Promote one to primary against its rank only when all four hold:

- Interview Q9 evidence puts the buyer on that surface.
- No capture family reaches them (thin category search volume, not sold on a host marketplace).
- The budget clears that family's floor by concentrating rather than spreading.
- The Q15 deadline sits at least a full quarter out.

Where the axes disagree: paid social prospecting and short-form video hold the highest value ceilings and the heaviest effort - a standing creative job, not a setup task - which is why they sit mid-table on efficiency while topping value. Retargeting is near-zero effort and tops nothing on value; it multiplies traffic already being bought and is never a primary.

Rows that move with business type:

- Professional networks usually leave at step 1 for consumer offers.
- Paid social prospecting rises to second behind paid search for broad consumer categories - the same call step 3 already makes on capture versus creation.

Native/discovery, programmatic display and paid review listings are deliberately left out of the ordering. Placing them against benchmarked families would be invented precision because cost and value vary too widely to rank. Treat them as a price-discovery bucket: eligible as a second channel once a tiny test returns a real number, never as the funded primary on a first plan.

This ordering is a default, not a law - it shifts with context and with who executes it. Re-rank it against what you already know about this business before scoring anything:

- An unfair advantage moves its family up several rows: an in-house video team, an existing audience on one surface, a founder already known in a podcast niche, an owned list large enough to seed matching.
- A hard skill already in-house cuts that family's effort score, which is the whole denominator.
- An asset already owned - finished video, a live storefront on a host marketplace, a review listing with traffic - removes setup effort the default order assumes nobody has.
- The interview's deadline, one-off-versus-compounding and effort-ceiling answers (Q15-17) override the default outright; see the note under the interview.

Then score the survivors for this business and order them by the ratio. Value axes score 5 = strongest; effort axes score 5 = heaviest lift.

| Side   | Axis                       | Score 5                                                              | Score 1                                                     |
| ------ | -------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| Value  | Audience presence          | Buyers demonstrably concentrate here (interview Q9 evidence)         | No evidence buyers are here                                 |
| Value  | Targeting reachability     | The family's targeting can isolate the actual ICP                    | ICP not expressible in this family's targeting              |
| Value  | Reach at that targeting    | Enough volume at that targeting to matter                            | Audience exhausts in weeks or pays a small-audience premium |
| Value  | Measurability              | Conversions attributable with the tracking you have                  | Mostly unmeasurable without incrementality infrastructure   |
| Effort | Creative burn vs. capacity | Burn rate far exceeds current production capacity                    | Burn rate sits well inside it                               |
| Effort | Skill and coordination     | No experience; launch needs third parties, contracts, or a new build | Team already runs this family unaided                       |
| Effort | Reversibility              | Committed flights or contracts hold the budget for a quarter         | Can be paused or redirected within days                     |

- Sum the value side, sum the effort side, and rank by value ÷ effort. That ratio, not either sum, is the ordering.
- Score from interview evidence, not enthusiasm; note the evidence next to any 4-5 on the value side and any 1-2 on the effort side.
- Break ties with headroom against allowable CAC: the family whose benchmark CPA/CPL sits furthest under the ceiling wins. Headroom never re-enters the ratio - step 1 already removed everything over the ceiling, and the surviving benchmarks are too wide to rank on.
- The ratio ranks survivors only. It never overrides the affordability gate or the disqualifier pass - a high-ratio unaffordable channel was deleted at step 1, stays out of this table, and is named in the deleted list rather than ranked last.

## Step 5 - Funding floor check

The top-ranked channel must be fundable above its learning/signal threshold with the stated budget - thresholds are the true floor, not platform billing minimums. Directional floors and signal thresholds per family: [references/channel-family-profiles.md](references/channel-family-profiles.md).

If the budget cannot fund the winner above its floor, the correct answer is the next-ranked channel whose floor the budget does clear - never a thinner spread of the same money. Walk down the step 4 ratio ordering, not down a price list; an underfunded channel produces no readable signal, which is worse than a readable one from a lower-ranked family.

Delete the unfundable family from this plan's candidate set and name it in the deleted list with the floor it missed and the budget that would clear it. Leaving it in the ranked table as a top row nobody funds is how it returns as scope at the next budget conversation, with its failed floor forgotten.

## Step 6 - Concentration and sequencing

- One primary channel for a startup; two to three for a scaled team. "Don't diversify yourself in too many channels; it's like a death sentence" is the practitioner consensus, and most businesses find only one channel that truly works.
- Fund the primary above its threshold before spending anywhere else; a common working pattern is ~80% of budget on the primary for the first 90 days.
- The anti-pattern, in arithmetic: $10K/month split five ways is $60-80/day per channel - below every major family's learning threshold - producing five separate experiments, each running below minimum sample size. Nothing is learned; everything is spent.
- Add exactly one channel at a time, and only when the primary saturates (rising CPA, audience exhaustion) or the budget crosses a breakpoint (practitioner anchor: ~$50K/month) with payback still inside the target band. Scaling the proven primary itself belongs to mbfinotti/advertising-skills@paid-media-scaling.

## Step 7 - Channel test design

Design the test for the chosen channel before full commitment. This is channel-level validation - creative variant testing belongs to mbfinotti/advertising-skills@ad-creative-test-plan.

1. **Price discovery first**: run a deliberately tiny spend (on the order of $100) purely to learn the real CPC/CPM for this specific targeting. Published benchmarks are consistently wrong for a specific ICP; this step replaces them with your own number before real money moves.
2. **The real test**: budget 3x target CPA minimum (5x preferred) per concept. Run it for the full purchase cycle - directional durations: search 2-4 weeks, social 3-6 weeks, display/programmatic 4-8 weeks, brand/awareness 6-12 weeks; B2B professional networks warrant a ~3-month commitment. Start and end on the same weekday.
3. **Pass**: CPA/CPL at or under allowable CAC at statistical significance (90-95% confidence) - significance, not arbitrary click counts.
4. **Kill**: 2-3x target CPA spent with zero conversions after a readable sample, then diagnose before rerunning.
5. **The false-negative trap**: a test shorter than the sales cycle reads as "zero lift" even when the channel works - a two-week test cannot validate a 90-day cycle. Never judge before one full cycle has elapsed.

## Measurement coupling

Channel choice and attribution model are coupled; the plan must state its measurement approach, because the channel mix determines which readings can be trusted. Add rungs in efficiency order as the mix and the spend justify them, never all four at once.

- efficiency: UTM discipline + last-non-direct > self-reported attribution at signup/checkout > MER (total revenue / total ad spend) > incrementality or geo-lift tests
- effort: incrementality/geo-lift (a standing job - holdout design, clean geographies, weeks of deliberately withheld spend) > MER (a reporting rebuild spanning finance and ad accounts) > self-reported (one form field plus somewhere to store the answer) > UTM discipline (a naming convention, an hour to set, then enforcement forever)
- value: incrementality/geo-lift (the only reading that survives a creation-heavy mix) > MER > self-reported > UTM discipline

The axes invert, which is the point: the most valuable reading is the least efficient one to reach for first. Start at rung 1 and climb only on a trigger.

- Default rung: capture-heavy plan at small budget stops at UTM discipline plus last-non-direct.
- Add self-reported the moment any creation channel enters the mix - it costs one form field and is the cheapest correction to the step 3 bias.
- Add MER once ecommerce spend is material enough that platform-reported ROAS and actual revenue visibly diverge.
- Add incrementality/geo-lift only on the biggest line item, and only once its spend justifies withholding some of it.
- Never judge a creation channel on its platform dashboard alone - per the bias in step 3, that reading is structurally rigged against it.
- Verify tracking before launch via mbfinotti/advertising-skills@ad-conversion-tracking; a channel test on broken tracking measures nothing.

## B2B vs. B2C

| Dimension         | B2B                                                                                                 | B2C / ecommerce                                                        |
| ----------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Dominant families | Paid search (capture), B2B professional networks, paid review listings, creation via podcast/social | Paid social, short-form video, paid search, retail media, connected TV |
| Deciding metric   | Pipeline, ACV, payback                                                                              | ROAS/MER, contribution margin, AOV                                     |
| Attribution       | Last-click breaks over long cycles; self-reported + modeled                                         | MER + platform triangulation + incrementality                          |
| Audience size     | Small TAM, account lists, near platform floors                                                      | Broad, high-volume                                                     |
| Cadence           | Multi-quarter, buying committee                                                                     | Seasonal, promotional, impulse                                         |
| Creative volume   | Fewer assets, longer life (weeks)                                                                   | High volume, fast fatigue (days at scale)                              |

Identical for both, explicitly: the affordability gate, the disqualifier pass, the capture/creation logic, the concentration rule, and the test-design discipline all run the same way - only the inputs and the dominant families differ.

## Output shape

Deliver one channel plan document:

1. Economics inputs and the allowable CAC derived from them (with the payback math shown).
2. Deleted channels, naming the gate each failed (affordability, disqualifier, or funding floor) and the specific dated reason.
3. Candidate table ranked by value ÷ effort - survivors only, nothing with a failed gate - with the value and effort subtotals shown, the interview Q15-17 answers that moved any row, and any starved high-value/high-effort family promoted against its rank with the condition that promoted it.
4. Primary channel recommendation with rationale tied to the ratio and the economics.
5. Funding plan: budget vs. the primary's learning threshold.
6. Test design: price-discovery step, real-test budget and duration, pass/fail and kill criteria.
7. Trigger conditions for adding a second channel.
8. Measurement approach implied by the mix.

Full template plus a worked B2B example, a worked B2C example, and a negative example: [references/channel-plan-template.md](references/channel-plan-template.md). If your harness has persistent memory, store the economics inputs, the recommendation, and the second-channel triggers so later budget and scaling conversations start from the same decisions; otherwise tell the user to keep the plan document as the canonical record.

## Failure modes

- Copying a competitor's channel mix without matching economics - their margin and LTV, not their taste, made their mix work.
- Picking the channel the team already knows instead of the one with channel-model fit.
- Ordering the candidate menu by what is cheapest to start rather than by return per unit of effort - the cheapest row is rarely the first row.
- Spreading a small budget across many channels, starving each below its learning threshold.
- Parking a ruled-out family at the bottom of the ranked table instead of deleting it - it returns as scope with its failed gate forgotten.
- Letting the ratio permanently starve the one family that reaches the buyer, when the budget could clear its floor by concentrating.
- Ignoring creative production capacity - the real bottleneck on the highest-volume creation families.
- Launching before tracking or landing pages are ready, wasting the entire learning phase.
- Reading attribution artefacts as performance - over-crediting capture, then over-funding it.
- Treating median benchmarks as targets - they are vendor-published midpoints of very wide distributions.
- Killing a channel before one full sales cycle has elapsed - a false negative, not a verdict.
- Forcing the product into a mismatched channel - products mold to channels, never the reverse.

## Objective and measurement

A channel selection passes only when every recommended channel simultaneously satisfies all four:

1. Realistic benchmark CPA/CPL at or under allowable CAC (affordability gate passed, math shown).
2. Fundable above its learning/signal threshold with the stated budget (funding floor passed).
3. Survives the disqualifier pass for every target geography and category constraint.
4. Carries a documented test with explicit pass/fail and kill criteria and a duration at least as long as the sales cycle.

Any recommendation failing one criterion is rejected and the framework re-run from the failed step - do not present a plan with a known failed gate. Post-launch, the selection itself is validated when the channel test returns a pass verdict at significance within the planned duration; a kill verdict feeds the next-ranked candidate, not a wider spread.

## References

- [references/channel-family-profiles.md](references/channel-family-profiles.md) - per-family profiles in the step 4 default efficiency order: demand state, value ceiling, effort load, minimum viable budgets, signal thresholds, directional cost ranges, disqualifiers, creative burden. Load when gating or ranking candidates.
- [references/disqualifier-checklist.md](references/disqualifier-checklist.md) - regulatory, geography, and capacity disqualifiers with sourced specifics. Load during step 2.
- [references/channel-plan-template.md](references/channel-plan-template.md) - output template, worked B2B and B2C examples, and a negative example. Load when writing the plan.
- mbfinotti/advertising-skills@ad-spend-allocation - use when splitting a budget across existing running campaigns; this skill handles the one-time setup decision only.
- mbfinotti/advertising-skills@ad-spend-guardrails - set CAC ceiling and ROAS floor policy before using this skill; the affordability gate takes those targets as input.
- mbfinotti/advertising-skills@cac-roas-benchmark - benchmark current CAC/ROAS health after channel selection; this skill uses them as gates, not measures.
- mbfinotti/advertising-skills@ad-conversion-tracking - verify tracking before launch; channel testing on broken tracking measures nothing.
- mbfinotti/advertising-skills@ad-creative-test-plan - after picking a channel, test creative variants; this skill validates the channel only.
- mbfinotti/advertising-skills@paid-media-scaling - scale a proven channel; this skill chooses the first one only.
