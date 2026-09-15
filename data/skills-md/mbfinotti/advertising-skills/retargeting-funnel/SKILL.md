---
name: retargeting-funnel
description: "Design a multi-stage retargeting sequence from a site's own funnel data - recency windows and behavioural-depth tiers per stage, a message and offer ladder for each stage, mutually exclusive audiences with exclusion logic, and per-stage frequency caps. Use whenever the user mentions retargeting or remarketing, cart or form abandonment, how long a retargeting window should be, frequency caps, a retargeting audience that is too small, or ads still showing to people who already bought - even if they never say 'funnel'. Covers B2B and B2C, and produces a stage-by-stage plan rather than campaigns built inside an ad platform. Do NOT use to design cold prospecting audience tiers - use mbfinotti/advertising-skills@ad-audience-targeting instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.9"
---

# Retargeting Funnel

Design a multi-stage retargeting sequence from the client's own conversion data: stage boundaries, per-stage message intent, exclusion logic, frequency caps, and a measurement plan.

## Scope and handoffs

This skill decides stage boundaries, per-stage message intent, exclusion logic, caps, and the measurement plan. It does not build campaigns inside any ad platform, and it hands off neighbouring work:

- Working event tracking is a hard prerequisite - retargeting audiences cannot be built without it. Verify first via `mbfinotti/advertising-skills@ad-conversion-tracking`.
- The broader targeting plan across interest/lookalike/retargeting layers → `mbfinotti/advertising-skills@ad-audience-targeting`.
- Ongoing creative-decay monitoring after launch → `mbfinotti/advertising-skills@ad-creative-fatigue`.
- Writing the per-stage ads themselves → `mbfinotti/advertising-skills@ad-copy-variants` and `mbfinotti/advertising-skills@ad-creative-brief`.
- Splitting the total budget across campaigns and channels → `mbfinotti/advertising-skills@ad-spend-allocation`.

If you draft any customer-facing copy while illustrating a stage, route it through your preferred humanizer skill before the user ships it - this is not a copywriting skill.

## Interview

Ask these questions one at a time, multiple-choice where possible. Stop asking as soon as you have enough to design; do not batch all of them into one wall of questions.

1. Business model: (a) B2C / e-commerce, (b) B2B, (c) hybrid (e.g. PLG SaaS with self-serve and sales-assisted tiers)?
2. Typical time from first visit to conversion: (a) under 3 days, (b) 3-14 days, (c) 2-8 weeks, (d) 2 months or more, (e) unknown?
3. Monthly site traffic and monthly conversions, roughly? (Order of magnitude is enough.)
4. Which behavioural events are actually tracked today: page views only, product/feature views, pricing views, cart or checkout starts, trial starts, purchases, CRM stages?
5. Which paid channels are in use or planned?
6. Offer type: (a) transactional purchase, (b) free trial, (c) demo request, (d) lead form / gated content?
7. Is a discount ever available as an incentive? (Many B2B businesses: no - that removes a rung of the ladder, not the ladder.)
8. Total monthly paid budget and the current prospecting-vs-retargeting split, if one exists?
9. Does a converter-suppression / exclusion audience already exist on any channel?
10. By what date must this be live and producing, and is that date hard? (The creative ladder in step 5 spans near-zero to a quarter in time-to-effect, so its ordering cannot be picked without this.)
11. Do you want the fastest revenue available this quarter, or durable assets that keep paying - a proof library, an incrementality baseline? (The first favours the cheap rungs, the second the slow ones.)
12. Effort ceiling: who can produce creative and how often, and can you actually obtain customer consent and legal sign-off? (A "no" removes the top rungs of the ladder rather than delaying them.)

Refuse to invent stage boundaries without time-lag data. If the user answered "unknown" to question 2, say explicitly: "I will not guess your windows - either export a time-to-conversion report, or I will use <named proxy> and flag every boundary as provisional." Acceptable proxies - always named as a proxy in the output, never silently substituted for real data:

- Ranked by evidence bought per unit of effort: analytics lag report > CRM sales-cycle export > sector-typical figure for the vertical.
- effort (heaviest first): CRM export (an hour, plus whoever owns the CRM) > analytics export (an hour, self-serve) > sector figure (near-zero, one search).
- The cheapest proxy is also the weakest. The CRM export overtakes the analytics one only when the cycle outruns what the pixel can see (B2B, multi-month).
- This is a default, not a law - re-rank against what the user already holds. A lag report exported last month beats a better one nobody will pull.

## Workflow

### 1. Pull the funnel data

Gather these, in order:

1. Traffic by page type (content / product or feature / pricing / cart or signup)
2. Conversion rate by funnel stage
3. The time-to-conversion lag distribution
4. The main drop-off points
5. The abandonment rate at the deepest pre-conversion step

If your harness can read files, ask the user to export these reports and drop them where you can read them; otherwise ask them to paste the key numbers. If you can browse the web, you may fetch published benchmarks to sanity-check their figures - but the client's own numbers always win over benchmarks.

### 2. Set stage boundaries from converter recency percentiles

This is the core move: derive windows from the client's own converters, not from platform defaults. From the lag distribution, find the recency point by which roughly 80% of converters had converted - that is the edge of the hot window. Then:

- If 80%+ convert inside 7 days, collapse to fewer stages (often just hot / warm / win-back). More stages than the cycle supports produces empty stages.
- If the cycle runs 60-90 days (typical B2B, high-ticket), stretch every window and plan for list-based rather than pixel-based membership at the long end, since browser privacy limits make long cookie windows unreliable.
- Default retention windows on ad platforms are arbitrary relative to any specific business. A default-length window on a 90-day cycle silently drops most of the pipeline; the same default on a 2-day impulse cycle wastes weeks of spend on cold traffic.

### 3. Build the two-axis grid: recency × behavioural depth

Cross the recency windows with the behavioural-depth axis. Claim grid cells deepest first, in this order:

cart, checkout or trial start > pricing page viewer > product or feature page viewer > any visitor / content viewer

Past customer and churned customer sit outside the conversion ladder, as win-back tiers. Assign windows inversely to depth: deep actions get short windows (intent decays fast), shallow actions get long windows (they were never hot, so staleness costs less). Not every grid cell becomes a stage - take the 3-5 deepest cells where the client has volume and a distinct message.

That order is value, not effort: every tier costs the same to build - one audience definition, minutes - so nothing separates them but the intent they capture. Effort splits them only where the event is not tracked yet (question 4): an untracked depth signal costs an engineering ticket and a wait, which can drop it below a shallower tier for this quarter. Re-rank on what the account already owns - a CRM deal stage already synced outranks a pricing-view pixel that needs a sprint.

### 4. Size-check every stage after exclusions

Check each stage against the platform's documented minimum audience size, measured **after** the exclusions from step 6 are applied - a stage that clears the floor before exclusions can fall under it once fresher stages and converters are carved out. Current floors and retention ceilings are in [references/platform-constraints.md](references/platform-constraints.md); verify against official documentation before building, because these values change often.

Collapse rule: if a stage cannot clear its floor after exclusions, repair it in this order:

widen the window > broaden the trigger > merge adjacent stages > collapse to one combined warm pool

All four cost minutes in the audience builder, so effort does not separate them. The ordering is value: what each step spends is message distinctness (widening keeps the stage's job intact, merging fuses two jobs into one, the single pool gives up sequencing entirely).

Never ship a stage that will not deliver - an under-floor stage either serves nothing or serves at punitive CPMs while the learning phase never exits. Thin-traffic sites often end with two stages, or one (see the Ben Heath position below); that is a correct output, not a failure.

### 5. Assign message intent and offer per stage

Each stage gets a distinct job, not a louder version of the previous ad. Re-showing the identical offer harder is the weakest stage design - if they saw it and did not act, either the offer or the angle was wrong, so change one of the two.

One menu of rungs, in build order: what each buys per unit of effort to produce it. Build top-down and fill the stages with whatever is ready.

Slot is separate information: where a built rung sits in the funnel sequence, not when to make it.

- B2C slot order: reminder, social proof, objection, incentive.
- B2B slot order: proof, objection, ROI, ask. B2B has no discount rung. Its incentive equivalent is a lower-friction ask, such as an assessment, an audit, or a tailored demo.

| Rung (build order)                                                                    | Slot                      | What it buys                                                        | Effort to produce                                                                     | Compliance cost                                                                        |
| ------------------------------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Objection handling - shipping, returns, guarantee; security, integrations, comparison | B2C 3rd / B2B 2nd         | Removes the stated blocker; the only rung that answers a known "no" | An hour - the policy facts already exist in writing                                   | A claims check against the published policy; fully reversible                          |
| Reminder / dynamic item ad                                                            | B2C 1st                   | Re-presents the exact item; converts the almost-decided             | Near-zero - the catalogue writes it                                                   | Catalogue accuracy, on the consent basis the pixel already needs                       |
| Direct ask - demo, trial, assessment, audit                                           | B2B 4th                   | Converts intent already present; buys no new belief                 | Near-zero                                                                             | None beyond standard ad review                                                         |
| ROI or comparison content                                                             | B2B 3rd                   | Arms the internal champion for a committee decision                 | A week - data pull, sometimes customer interviews                                     | Claim substantiation, and legal review where naming a competitor is restricted         |
| Social proof - reviews, UGC                                                           | B2C 2nd                   | Borrowed credibility at scale; strongest on unfamiliar brands       | A week - sourcing reviews or creators                                                 | Creator usage rights, testimonial and paid-partnership disclosure                      |
| Named-customer proof - case study, named results                                      | B2B 1st                   | The strongest evidence available; unlocks committee trust           | A quarter - customer consent, legal sign-off, political capital with the account team | Written approval per use and logo rights, revocable by the customer                    |
| Discount + urgency                                                                    | B2C 4th, final stage only | Buys the last conversion, and only the last                         | Near-zero to make; spends margin every time it runs                                   | Promotion terms, price-display rules in some markets, urgency claims that must be true |

- efficiency (build first) = the row order above.
- value (strongest first): named-customer proof > social proof > ROI content > objection handling > discount > reminder > direct ask - near enough the reverse of effort at the top of the table, which is why the axes are split instead of blended.
- compliance cost (heaviest first): named-customer proof > social proof > discount > ROI content > objection handling > reminder == direct ask. That last tie is a real equality at the floor of the axis: both run on material the advertiser already publishes, neither makes a new claim nor uses anyone else's likeness, so neither needs more than the standard ad review every rung gets.

The discount is the one rung whose real cost is not production:

- It spends margin every time it runs.
- It trains deliberate abandonment: people park carts to farm the coupon.
- It is the hardest thing here to withdraw once the market has learned it.

That is why it ranks last despite costing nothing to make, and why it runs on the final stage only. If no discount exists (question 7), the final rung is the hardest direct ask instead.

The order is a default for a team starting from nothing. It moves with context and with who executes it.

Re-rank against questions 10-12, and name which answer moved which rung:

- A hard near-term date promotes objection handling and the reminder.
- A durable-asset mandate promotes named-customer proof and social proof.
- No route to legal sign-off deletes the proof rungs outright, rather than delaying them.

Re-rank again on what the user already owns:

- A stocked review corpus drops social proof to near-zero effort and pulls it forward.
- An approved case study makes proof the cheapest strong rung there is.
- An in-house video team collapses UGC to a day.

Ship each stage on the best rung available now, and upgrade it later - a stage running an hour-old objection ad beats a stage waiting a quarter for a case study.

What this efficiency order starves is the belief-building end of the ladder. Named-customer proof, social proof and ROI content top the value axis and sit at the bottom of the build order. A sequence built on the ratio alone ships reminders and objection ads, then reaches for the discount when those stop converting - near-zero to make, margin spent every time it runs, and the hardest rung here to withdraw.

Promote a proof rung against the ratio when any of these holds:

- The objection rung has already run and the stage still does not convert, so the blocker is belief rather than friction.
- Question 11 was answered "durable assets".
- The sequence is B2B and the decision needs an internal champion to carry it through a committee.
- The final-stage discount is what is doing the converting, which means nothing above it built belief.

Start the quarter-long rung the week you notice, and run the hour-long rung in that stage meanwhile.

Delete, don't demote, every rung the answers rule out, and name each deletion in the stage table:

- No route to customer consent or legal sign-off deletes named-customer proof.
- No discount policy (question 7) deletes the discount rung.
- No budget for creator usage rights deletes UGC-based social proof.

A deleted rung is not the bottom of the build order - write the ladder without it, or a stage ends up planned around a rung nobody can produce.

Per stage, plan at least 3 distinct creative concepts - small retargeting pools burn through creative fast, and rotation is part of the frequency cap (step 7). Hand the actual production to `mbfinotti/advertising-skills@ad-creative-brief` and `mbfinotti/advertising-skills@ad-copy-variants`.

### 6. Write the exclusion logic

Every stage excludes all deeper and fresher stages, and every stage excludes converters (the burn/exclusion-audience pattern). Without this, one user occupies several stages at once and the account's own ad sets bid against each other in the same auction - self-competition that inflates CPM with zero incremental reach.

Make the exclusions auditable with a naming convention, e.g. `RTG_<depth>_<window>` for inclusion audiences and `EXCL_<what>_<window>` for exclusions, so anyone can read a stage's definition as "include X minus Y minus converters" without opening each audience. Also set an explicit converter-exclusion window, and write it down:

- Too short: re-ads recent buyers.
- Too long: silently suppresses prospecting reach as the buyer pool accumulates (see failure modes).

### 7. Set the frequency cap per stage

Retargeting tolerates higher frequency than prospecting - the audience already knows the brand - but tolerance is not immunity. Check whether your platform exposes an impression-cap field on the objective in use; many only expose it on awareness-type objectives. Where no cap field exists, audience size and creative rotation are the real cap: a small pool with one creative is an uncapped frequency machine regardless of settings.

Define per stage either a hard cap (where the platform allows) or a cap-proxy: the frequency reading at which you intervene.

Detection signals that a cap is being breached in effect, measured against a 7-day rolling baseline:

- Click-through rate falling 15-20%+.
- CPM rising 10%+ with unchanged targeting.
- Rising negative feedback (hides, "see less of this").

Vendor-specific cap mechanics and practitioner frequency bands per platform and stage are in [references/platform-constraints.md](references/platform-constraints.md). Ongoing monitoring after launch belongs to `mbfinotti/advertising-skills@ad-creative-fatigue`.

### 8. Set the prospecting-vs-retargeting budget split

Common practice splits roughly 70/30 prospecting-to-retargeting, moving toward 50/50 only when traffic is high and conversion is the bottleneck. But the binding constraint runs the other way: retargeting spend is bounded by pool size × frequency ceiling, not by ambition.

Compute the ceiling as reachable pool × capped weekly impressions × expected CPM, and cap retargeting budget there, whatever split was wanted. A small pool caps retargeting spend regardless of strategy. Excess budget forced into it just buys frequency past the cap.

Route the account-wide allocation through `mbfinotti/advertising-skills@ad-spend-allocation`.

### 9. Write the measurement plan

Track these metrics per stage:

- Spend
- Reach
- Frequency
- CTR
- CPM
- Platform-reported conversions and CPA
- New-vs-returning conversion share

At account level, track a blended-efficiency sanity metric: total revenue (or pipeline) divided by total marketing spend, which drops the attribution layer entirely.

Then schedule at least one incrementality test, because platform-reported conversions overstate incremental lift, and not by a little.

- Across 15 large-scale RCTs, Gordon, Zettelmeyer et al. (2019) found observational methods overestimated experimentally measured lift by factors of roughly 7 to 9.5, depending on funnel position.
- Blake, Nosko and Tadelis (2015) showed brand-keyword ads at eBay largely cannibalised traffic that would have arrived anyway.

Retargeting is the highest-risk case: it targets exactly the people most likely to convert on their own. Acceptable designs, ranked by evidence bought per unit of effort:

- efficiency, run first: ghost-ad style lift test (where the platform offers one) > audience holdout (withhold a random 10-20% slice of each stage) > geo/matched-market holdout.
- evidence (strongest first): ghost ads > geo/matched-market holdout > audience holdout.
- effort (heaviest first): geo/matched-market (a quarter - market pairing, spend coordination across regions, and a whole region's revenue riding on the design) > audience holdout (an hour of audience setup, then wait) > ghost ads (near-zero where the platform exposes them, impossible where it does not).
- Ghost ads lead because they top both axes where they exist. The audience holdout leads everywhere else, since the geo design buys somewhat cleaner evidence for an order of magnitude more coordination.

That default moves with the account: re-rank the geo design upward if the user already runs matched-market tests for other channels, because the coordination cost is already paid and only the analysis is new. If your harness can browse the web, verify the platform's current lift-test availability; if not, default to a 10-20% audience holdout, which needs no platform feature.

## Design gate

The plan must pass every item before handoff - 100%, not most:

- [ ] Tracking verified for every event a stage depends on (`mbfinotti/advertising-skills@ad-conversion-tracking`).
- [ ] Stage boundaries derived from the client's lag data, or the proxy used is named in the output.
- [ ] Every stage clears its platform delivery floor **after** exclusions.
- [ ] No user can occupy two stages at once (exclusion map is complete and mutually exclusive).
- [ ] Converters excluded on every stage, with an explicit, written exclusion window.
- [ ] Discount, if any exists, appears only on the final stage.
- [ ] A frequency cap or cap-proxy with detection signals is defined per stage.
- [ ] At least 3 distinct creative concepts staged per stage.
- [ ] An incrementality test is scheduled with a named design and date.

Running threshold after launch: cut or restructure any stage whose holdout-measured incremental lift is indistinguishable from zero - no matter how good its platform-reported ROAS looks. High platform ROAS with zero incremental lift is the signature of paying to intercept conversions that were coming anyway.

## B2B vs B2C

These mechanics are identical for both:

- Two-axis grid construction.
- Mutual exclusion and converter suppression.
- The after-exclusion size check.
- The discount-last rule (where a discount exists at all).
- The measurement plan.

State this to the user, so they do not assume the B2B plan is a softened B2C plan.

What genuinely differs:

| Dimension                       | B2C / e-commerce                         | B2B                                                                                      |
| ------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| Windows                         | Short; hot window often 1-7 days         | Long; 90/180/365 days to match multi-month cycles                                        |
| Pool size                       | Usually clears floors easily             | Chronically small; expect stage merges                                                   |
| Offer ladder                    | Reminder → proof → objection → incentive | Content ladder: proof → objection → ROI → demo ask; no discount rung                     |
| Audience source at long windows | Pixel-based mostly works                 | Shift to CRM-list/first-party audiences; browser privacy limits kill long cookie windows |
| Unit of targeting               | The person                               | Increasingly the account/buying committee - multiple stakeholders see different stages   |
| Deep-intent trigger             | Cart or checkout start                   | Pricing page, trial start, or CRM deal stage                                             |

For B2B, also consider sequencing by CRM deal stage (evaluation / proposal / negotiation) rather than web recency alone - the CRM knows more about depth than the pixel does.

## Failure modes

Rows run in fix order - waste removed per unit of effort first, with the effort in the last column. Suppression fixes lead because they are audience-definition edits that take minutes and stop the bleeding on contact. The incrementality test comes last because it repairs nothing by itself, it only names the stage to cut.

Re-rank against the account in front of you: a single-stage account has no overlap to fix, and an account already suppressing converters starts at the windows.

| Failure                                       | What it looks like                                          | Fix                                                                                                             | Effort                                        |
| --------------------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| Retargeting past converters                   | Buyers keep seeing "buy it" ads; complaints, wasted spend   | Converter exclusion on every stage; audit it exists on each channel                                             | Minutes per channel                           |
| Over-long converter exclusion                 | Prospecting reach quietly shrinks quarter over quarter      | Set an explicit exclusion window sized to the repurchase cycle; review when platforms extend retention defaults | Minutes, plus a diary note                    |
| Overlapping stages self-competing             | CPMs inflate; same user reported in several ad sets         | Mutually exclusive windows + exclusion map (step 6)                                                             | An hour to map, minutes to apply              |
| Dynamic ads showing bought/out-of-stock items | Post-purchase ads for the purchased item                    | Purchase-event suppression + catalogue exclusions                                                               | An hour, plus catalogue feed access           |
| Stale default windows                         | Window length matches platform default, not the sales cycle | Re-derive from lag data (step 2)                                                                                | An hour, once the lag export exists           |
| Too-small pools                               | Delivery stalls or CPM spikes; learning phase never exits   | Collapse rule (step 4): widen, broaden, merge, or pool                                                          | Minutes, but only after the windows are right |
| Creative fatigue / stalking backlash          | CTR sags, negative feedback climbs at high frequency        | Caps + 3+ rotating concepts; hand monitoring to `mbfinotti/advertising-skills@ad-creative-fatigue`              | A standing job - rotation never finishes      |
| Discount-trained abandonment                  | Abandonment rate rises after coupon retargeting starts      | Discount only on final stage; vary the offer; exclude repeat abandoners from incentives                         | Minutes to change, a quarter to un-train      |
| Cannibalisation                               | Great platform ROAS, flat blended revenue                   | Incrementality test (step 9); cut stages with zero measured lift                                                | Weeks of elapsed test time before it answers  |

## Positions worth knowing

Present these honestly as a live disagreement, not a settled prescription.

- **Burn/exclusion audience** - popularised by Ryan Deiss and DigitalMarketer: fire a suppression event on conversion so every stage stops targeting buyers immediately. This is baseline practice. Step 6 assumes it.
- **Effective frequency** - contested, with three positions on how many exposures actually work: Herbert E. Krugman's three-exposure theory (1972) underlies most "cap at ~3" advice. Colin McDonald's single-source work and John Philip Jones argued one well-timed exposure near purchase carries most of the effect. Modern digital studies have found effects growing past 10+ exposures. No single frequency number is evidence-based across contexts - treat published bands as starting points and steer by the decay signals in step 7.
- **Reach over frequency** - Byron Sharp and the Ehrenberg-Bass school object to heavy retargeting altogether: growth comes from reaching light and non-buyers, not from re-hitting a warm pool. Take it as a ceiling argument for the retargeting share of budget (step 8).
- **Anti-stratification** - Ben Heath argues (verified, heathmedia.co.uk) for a single broad warm pool combining site visitors, engagers, video viewers, and lists at maximum windows, instead of fine-grained tiers. Combining every warm signal, in his words, gives the platform "the data it needs to optimize your ad delivery".

  Ranked by return per unit of setup effort, that posture leads:

  one combined warm pool > stratified stages, until every stage clears its floor with room to spare

  The pool costs one audience and no exclusion map. Stratification costs a map, a cap sheet and per-stage creative, and repays that only once each stage has enough people to learn on.

  Default to the single pool below the floor, and move up one rung when step 4's size check passes comfortably - or immediately, where a maintained exclusion map and creative pipeline already exist and make the stratified version nearly free. The step 4 collapse rule converges toward Heath's design as traffic shrinks.

## Output shape

Deliver four artifacts (full worked examples in [references/worked-sequences.md](references/worked-sequences.md), including a required negative example):

1. **Stage table** - one row per stage: name, inclusion rule (depth event + window), message intent, offer rung, creative-concept count, expected pool size after exclusions.
2. **Exclusion map** - per stage: what it excludes (deeper stages, fresher windows, converters), with audience names following the naming convention.
3. **Cap sheet** - per stage: hard cap or cap-proxy, detection signals, review cadence.
4. **Measurement plan** - per-stage KPIs, the blended-efficiency metric, and the scheduled incrementality test (design, holdout share, start date, decision rule).

Integration note: platform-specific floors, retention ceilings, cap mechanics, and frequency bands for Meta, Google, LinkedIn, TikTok, Microsoft, Reddit and DV360 live in [references/platform-constraints.md](references/platform-constraints.md) - read it when mapping this plan onto concrete channels, and verify its values against current official documentation.

## Memory

If your harness has persistent memory, record the chosen stage boundaries, windows, caps, exclusion windows, and the reasoning (which percentile, which proxy, which collapse decisions) - so later sessions tune the design against results instead of re-deriving it. If not, put the same rationale block at the top of the delivered plan.

## References

- [references/platform-constraints.md](references/platform-constraints.md) - per-platform minimum audience sizes, retention ceilings, cap-field availability, practitioner frequency bands. Load when translating the plan to specific channels.
- [references/worked-sequences.md](references/worked-sequences.md) - one worked B2C sequence, one worked B2B sequence, one broken sequence with the diagnosis. Load when producing the deliverable or when the user wants an example.
- `mbfinotti/advertising-skills@thought-leadership-ads` - person-fronted amplification campaigns that feed engagers into this sequence's warm stages; that skill routes the downstream funnel design here rather than duplicating it.
