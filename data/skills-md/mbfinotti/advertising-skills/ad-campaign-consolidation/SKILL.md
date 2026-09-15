---
name: ad-campaign-consolidation
description: "Evaluate a fragmented paid-ads account and recommend which campaigns and ad sets to merge, which splits to preserve, and how to migrate without resetting learning across the account - it plans the consolidation, it never executes it. Use whenever the user mentions too many campaigns or ad sets, merging or restructuring an ad account, ad sets stuck in learning or learning limited, budget spread too thin, account simplification, or campaigns competing with each other - even if they never say 'consolidation'. Covers B2B and B2C on search, paid social, video, and professional-network platforms. Do NOT use to find out why the account underperforms in the first place - use mbfinotti/advertising-skills@ad-account-diagnostic instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.9"
---

# Campaign Consolidation

Turn a fragmented multi-campaign account into a consolidation plan: what to merge, what to keep split, in what order, and how to judge the result. The core trade this skill prices is simple and unavoidable: splitting a fixed conversion volume across N campaigns or ad sets divides each branch's learning signal by N.

Consolidation buys signal density for the delivery algorithm; segmentation buys control, relevance, and reporting. Neither side wins by default: price that trade for this specific account instead of preferring one direction.

You recommend; you never execute. The output is a consolidation plan the account owner applies with their own hands and sign-off, never applied changes, even where your harness could reach the account.

This skill activates once fragmentation is already the suspected or confirmed problem. The broader "why is this account underperforming" root-cause work belongs to `mbfinotti/advertising-skills@ad-account-diagnostic`, which hands its fragmentation verdict to this skill - run the diagnostic first if nobody has established that fragmentation is the problem.

Consolidation is platform-endorsed, not a fringe opinion:

- **Evidence for:** the major social platform's own (since retired) five-pillar best-practice program listed account simplification as a pillar; the search-ads world has a named method for collapsing single-keyword structures into few intent-themed campaigns (see Platform Notes).
- **Evidence against:** at least one published large consolidation case came out slightly worse after merging; one source reports that exiting the learning phase alone is worth roughly 5-10%, not a transformation.

Treat consolidation as a hypothesis to test, never a guaranteed win. Do not oversell it in the plan.

## Interview

Ask before analysing anything.

- One question per message.
- Offer multiple-choice answers where possible.
- Skip anything already supplied by the user, the data, or a diagnostic handoff.

- Which platform(s)? (search / paid social / short-video / professional-network / several)
- B2B or B2C/ecommerce?
- Monthly spend, and monthly conversion count on the event the account actually optimises to? (This single pair decides most of what follows.)
- Current structure: how many campaigns, ad sets/ad groups, and active ads?
- What can you export, and at what granularity? (Per-branch per-day conversion counts are the working minimum.)
- What is the target CPA or ROAS - and is it derived from unit economics (margin, deal size, close rate) or inherited from a dashboard?
- Which segments exist as separate campaigns/ad sets today, and _why was each one split out_? (The load-bearing question - answers like "for the 2024 launch" or "the previous manager reported that way" versus "different margin per segment" decide the whole plan.)
- Who controls the budget, and is any split externally mandated (client contract, finance, a guaranteed spend per line of business)?
- What reporting does the business need preserved after the merge? (Contractual or operational - not "nice to have".)
- Are any branches currently in the learning phase, and is there an active cost spike or panic driving this request?
- How long is the sales cycle, when is the next peak season, and by what date must the result land? (A hard date promotes the fast, contained moves - `prune`, then `merge` - and rules out anything whose payoff needs a learning cycle plus a sales cycle.)
- Do you want a one-off win on this quarter's numbers, or a structure that keeps paying? (One-off promotes `prune` and `re-parent`; a compounding mandate promotes `merge` and, in low-volume B2B, `up-funnel`.)
- What is the effort ceiling: rebuild hours available, who must sign off, how much political capital the split owners cost you, and how reversible the change must stay? (A low ceiling caps the plan at `prune` and `re-parent`; only a high one funds a multi-phase merge.)

## Workflow

1. Run the Interview. Collect every answer before touching data.
2. **Inventory the current structure.** Map every campaign → ad set/ad group → ad, with each branch's daily budget, bid strategy, optimisation event, audience definition, and the stated reason it exists. If you can read the account's exports directly, build this yourself; otherwise emit the exact export steps and a table for the user to fill and return. Tag each split as _deliberate_ (someone can state a live business reason) or _archaeological_ (launch leftovers, a departed manager's reporting habit, an old test nobody closed) - a split nobody can justify is the cheapest merge available.
3. **Compute per-branch conversion volume against the platform's learning threshold.** Count conversions per branch over a lag-mature window (exclude days still accumulating attributed conversions), on the event the branch actually optimises for - never a downstream event the platform never sees. Compare against the platform's _documented_ threshold (see Platform Notes; re-verify against the live help page, these numbers drift). Where the platform documents no threshold, say so - do not import another platform's number.
4. **Run the budget feasibility test - it is independent of the volume test.** A branch can be above threshold in theory yet under-budgeted to ever reach it: minimum daily budget ≈ target CPA × exit threshold ÷ threshold period in days. A branch whose budget cannot buy its threshold is fragmented by funding even if its audience is large.
5. **Classify every branch** using the four states below. Never let "couldn't verify" collapse into a verdict.
6. **Test every existing split against the preserve-vs-collapse rules** (section below). A split survives only when a rule protects it; the learning cost of keeping it must be named in the plan either way.
7. **Apply the Evidence Gate** (section below). If it fails, the deliverable is not a merge plan - it is a statement of exactly what extra days, spend, or access would clear it.
8. **Produce the target structure.** Pick each group's move from Consolidation Moves below - the earliest rung its classification allows, not the most ambitious one.
   - For each merged group: the shared objective, offer, optimisation event, bid strategy, and budget level (campaign-level pooling vs per-branch budgets - see Budget Mathematics for when pooling recreates the problem).
   - For each preserved split: the rule that protects it and its budget floor.
   - Cover the segmentation question explicitly: which segments move into creative variants inside the merged structure (section below), and which keep structural separation.
9. **Produce the migration sequence** (Migration Mechanics below): phases, what gets built new vs edited, the control, the no-touch window, and the timing relative to peak season.
10. **Define the measurement plan and the re-check date** (Measuring section below): baseline, judgment window, pass threshold, rollback trigger, and who signs off. If your harness has persistent memory, memorise the inventory, classifications, plan, phase dates, and re-check date so the follow-up run starts from history; otherwise emit a short state block the user can paste into the next session.

## Classification States

Assign every branch (campaign or ad set) exactly one state, each with a one-line justification citing the volume test, the budget test, and the preserve rules:

- **`merge`** - below threshold (or budget-starved) and no preserve rule applies. Name the merge destination.
- **`keep`** - clears volume and budget on its own, or a preserve rule protects it. Name which.
- **`keep but re-parent`** - reporting or control must survive, but the bidding signal should pool. The branch stays separately reported under a shared budget and bid strategy (rung 3 below).
- **`insufficient evidence`** - the data cannot support any of the above. State what would clear it. This is a real state, not a failure to decide.

## Consolidation Moves, Ranked by Efficiency

Five moves chase the same goal - denser learning signal per branch. They are not equivalent, and the owner's real question is which one to spend this month's hours and sign-offs on.

- efficiency (signal recovered per hour and per sign-off spent): `prune` > `merge` > `re-parent` > `up-funnel` > `big-bang`
- value (signal actually recovered): `merge` == `big-bang` > `up-funnel` > `re-parent` > `prune`
- effort (build time, coordination, sign-off, reversibility): `big-bang` > `up-funnel` > `merge` > `re-parent` > `prune`
- compliance cost (the review each move triggers): `big-bang` > `merge` > `up-funnel` > `re-parent` == `prune`

1. **`prune`** - pause the branches nobody can justify and move their budget to the survivors in steps of roughly 20%. Near-zero build, instantly reversible (pausing does not reset learning), no sign-off past the budget owner. Fixes funding starvation, not duplicated audiences - which is why it leads the order without ending the job.
2. **`merge`** - build one merged entity per group, shift budget, then pause the originals. Building takes about an hour plus one learning cycle of patience per phase, and it's the move that genuinely recovers divided signal, though it stays reversible only while the legacy structure remains paused. Start with the archaeological splits, where no one defends the split and the political capital cost is nil.
3. **`re-parent`** - pool budget and bid strategy under a shared parent while each branch keeps reporting separately (the low-risk middle move practitioner Jyll Saskin Gales recommends for roughly-ten-campaign accounts), each with a minimum-spend floor. Same build effort as a merge, far less negotiation because the report survives - but it pools funding, not ad-set-level learning, so the volume test can still fail afterwards.
4. **`up-funnel`** - move the optimisation event to a higher-volume proxy (see B2B and B2C). Needs the tracking and CRM owners, a consent and data review, and a standing job keeping the proxy honest against real outcomes. Slow and compounding, and the only move that works when even the fully merged structure cannot clear the threshold.
5. **`big-bang`** - rebuild the whole account at once. Its theoretical value matches a phased merge; every branch relearns simultaneously, the result attributes to nothing, and any externally mandated split it dissolves needs finance, client, or legal sign-off first. Migration Mechanics rules it out for any live account - it is listed here so a plan can say why it was rejected.

Default: run rung 1 across the account, then rung 2 on the groups the preserve rules leave unprotected. Move up a rung when the one below has run its no-touch window and the volume test still fails.

**What this order starves is `up-funnel`.** It is slow, it costs a second team plus a standing job, and it sits at rung 4, so the escalation rule above reaches it only after three rungs have each burned a no-touch window - which is months. That is exactly backwards for the account that needs it most: where the conversions do not exist, no amount of merging conjures them, and every rung below `up-funnel` spends a learning cycle proving that again.

Promote it straight to first, ahead of `prune`, on one condition: the volume test shows that even the _fully merged_ structure would not clear the platform's threshold (see B2B and B2C). Do not walk the ladder to reach it - the arithmetic is available on day one.

This ordering is a default, not a law - it shifts with the account and with who executes it. Re-rank it against what you already know about this user:

- An account whose splits are all deliberate makes `prune` nearly worthless and `re-parent` the real first move.
- An in-house analyst who can run a holdout makes the bigger moves readable.

Their Interview answers move it directly too - a hard date promotes `prune` and `merge`, a compounding mandate promotes `up-funnel`.

A constraint the user actually stated does something different from re-ranking: it removes the rung. Delete it from the ladder and name it as deleted in the plan, with the constraint that killed it and what would revive it - the way rung 5 is already listed only so the plan can say why it was rejected.

- A tracking implementation nobody may touch deletes `up-funnel`.
- An effort ceiling that funds no multi-phase rebuild deletes `merge` and everything above it, leaving `prune` and `re-parent` as the whole plan.

Say so outright rather than ranking the deleted rung last. A move parked at the bottom of a ladder reads as future scope, and it comes back next quarter as a fresh proposal to whoever forgot the constraint.

## Evidence Gate

Refuse to produce a merge plan on data that cannot support it. All of these must hold before any `merge` classification becomes a plan:

- **Window maturity.** The counting window is lag-mature and long enough to be representative - at minimum one full learning cycle plus typical conversion lag; stretch to 4-6 weeks for long-cycle B2B.
- **Per-branch spend.** Each branch being judged has accumulated roughly 3x its target CPA in spend over the window - below that, zero conversions is plausibly noise, so the state is `insufficient evidence`, not `merge`. (Practitioner starting point: at a true cost-per-conversion equal to target, 3x spend showing zero conversions is about 5% probability. Recalibrate against the account's own variance.)
- **Attribution consistency.** All branches counted under the same attribution window and counting method, with no settings or tracking change mid-window. Never sum conversions across differing windows.
- **A real target.** The target CPA/ROAS feeding the budget math comes from unit economics, or is explicitly flagged as inherited and unverified - a plan built on an inherited dashboard target is built on sand, and must say so.
- **No panic restructuring.** If the account is mid cost-spike or a branch is inside the learning phase, do not restructure as a reflex - a learning reset often costs more than the spike. Diagnose first; delay the plan if needed and say why.

When the gate fails, state the arithmetic of what clears it and offer the clearing moves in this order - efficiency: missing export or access > more days at current volume > concentrating budget into fewer branches to accumulate per-branch spend faster.

- An export clears the gate today for near-zero effort.
- Waiting costs only calendar time, which the deadline answer may not have.
- Concentrating budget is itself a structural change and carries the same sign-off as a merge.

## Preserve or Collapse: Testing Every Split

A split survives only for a business reason, never for comfort or habit. Test each split against this list; anything unprotected is a merge candidate. This list is what keeps the skill honest - a plan that only ever says "merge" is wrong roughly as often as one that never does.

Keep the split when:

- **Unit economics differ materially per segment** - margin, deal size, or LTV. One target CPA cannot serve two segments with different economics; pooling them optimises for the wrong one.
- **Budget control is externally mandated.** A client contract or finance requiring guaranteed spend per line of business needs per-branch budgets; campaign-level pooling will not honour the guarantee. Removing such a guarantee needs explicit finance/client approval, not a footnote.
- **Regulatory, legal, or brand-safety separation is required.** Regulated ad categories (housing, employment, credit, political, pharma, gambling, financial services) can mandate structural separation and restricted targeting.
- **Brand vs non-brand intent would share one bid strategy.** Automation gravitates to the easiest conversions: brand eats the pool, non-brand growth starves, and blended ROAS looks healthy while the account goes blind where it matters. Keep them in separate campaigns with distinct bid strategies, and exclude brand terms from blended/automated campaign types.
- **Geography, language, or currency differ** - especially when an expensive market would pool with cheap ones and be priced out of its own budget.
- **The offers or landing destinations genuinely differ** - one campaign cannot carry two promises. (Reasoned from message-match first principles plus practitioner consensus, not platform documentation.)
- **The platform itself treats the campaign types as structurally distinct** - different documented eligibility floors and conversion mechanics per campaign type imply they were not designed to merge. (An inference from documented per-type thresholds, not an explicit platform statement.)
- **Reporting the business is contractually or operationally obliged to produce** depends on the split - though check first whether `keep but re-parent` preserves the report while pooling the signal.
- **Guaranteed frequency on a named-account list matters** (account-based B2B), or prospecting and retargeting would otherwise share one pool - retargeting reports cheaper, absorbs the budget, and cold acquisition starves while reported ROAS inflates.

The mirror failure is real too: over-consolidation into one undifferentiated pool lets the algorithm park on its easiest slice and never reach the rest - mixed account lists get over-served to the largest companies and stall. Consolidation is not monotonically good; the plan states where merging _stops_.

## Keeping Segmentation Without Keeping the Structure

This is how the plan answers "consolidate without losing audience segmentation control" on algorithmic platforms: move the audience knowledge from the targeting filters into the creative. Merge the ad sets, then run one creative variant per segment inside the merged set - each variant speaks that segment's language - and let delivery match variant to viewer.

The anti-pattern this replaces: generic creative propped up by a stack of narrow filters. Twelve stacked interests, three demographic filters, and a custom audience over a bland ad produces a small audience that all see a bad ad. If segment knowledge exists, spend it on the message, not the filter.

This move applies to B2B and B2C alike - the segments differ (personas and account tiers vs demographics and intent stages) but the mechanic is identical. It does not apply where a preserve rule above forces structural separation (regulation, unit economics, budget mandates): creative variants cannot substitute for a separate budget or a separate bid target. Hand the actual per-segment creative work to `mbfinotti/advertising-skills@ad-creative-test-plan`.

## Budget Mathematics

Two formulas carry the quantitative plan; the derivations are durable even as platform numbers drift.

- **Budget floor per branch:** minimum daily budget ≈ target CPA × exit threshold ÷ threshold period days. Run it with whatever threshold the platform actually documents. Every branch in the target structure must clear its floor, or it is fragmentation rebuilt.
- **The pooling limit:** merging unequal-cost branches into one budget pool recreates starvation one level down. Campaign-level budget optimisation chases the lowest-cost result by design - expect 70-90% of a pooled budget to flow to one or two structurally cheaper winners (brand search is the canonical eater), starving exactly the branches you needed data from. Campaign-level pooling is therefore not automatically the right answer: pool only branches with comparable cost-per-conversion, and where a strategically required branch would starve, keep per-branch budgets or set minimum/maximum spend floors.

Practitioner starting points worth using _with their conditions attached_ - all recalibrate against the account's own data, none are platform law:

- Merge search campaigns that cannot reach roughly 15-30 conversions/month; they cannot feed automated bidding, especially in low-volume B2B.
- On the professional network, one campaign at 35%+ audience penetration beats three at 12%, and branches under roughly 10 results/week are starved.
- Audience overlap above roughly 30% between two active branches is where measurable auction self-competition kicks in.
- An account's ad-count ceiling ≈ (daily budget × 14) ÷ (2 × target CPA), because each ad needs judgeable spend inside the evaluation window - the same logic scales up to ad sets and campaigns.

## Migration Mechanics

The plan is the easy half; migrations get reverted on day three. Sequence it so the account never resets everything at once:

1. **Phase it, never big-bang.** Merge one group per phase, highest-confidence merges first (the archaeological splits). A whole-account reset maximises the dip and destroys any ability to attribute the outcome.
2. **Build new alongside, do not edit in place.** Editing targeting, optimisation event, bid strategy, or budget (beyond roughly 20%) inside a live entity resets its learning; pausing does not. Build the merged entity fresh, shift budget over, then pause - never delete - the old structure. Deletion destroys learning history and reporting; treat any deletion request as a pause-or-archive conversation.
3. **Keep a control where volume allows.** Run the legacy structure at reduced budget alongside the new one, or use the platform's experiment tooling, so the comparison survives the migration.
4. **Time it off-peak.** The relearning dip costs the most exactly when volume and auction prices peak; never restructure mid peak-season.
5. **Pre-commit the no-touch window.** State up front: expect a transient performance dip while the merged entity relearns. No significant edits for at least one full learning cycle: 7 days is the common floor, 14 for a real read, up to 30 (or one full sales cycle) for the verdict. Without this pre-commitment - in writing, with the sign-off owner - the plan gets reverted before it can work.
6. After exit, move budget in steps of roughly 20% or less every 3-5 days; larger single moves are widely treated as learning-resetting edits.

Window lengths stretch with the sales cycle. Whoever owns budget guarantees (finance, the client) signs the plan before phase one, not after.

## B2B and B2C

The method is identical in both: same inventory, same volume-and-budget tests, same preserve rules, same gate, same migration discipline. What diverges is whether the threshold is reachable at all.

- **B2C/ecommerce:** volume usually supports the full arithmetic. The dominant risk is pooling unequal-cost branches (Budget Mathematics) and retargeting eating prospecting.
- **B2B low-volume reality:** when even the _fully merged_ structure cannot clear the platform's threshold on the target event, consolidation alone is not the answer - no amount of merging conjures conversions that do not exist. Say this plainly in the plan, then take (a) before (b):

  - (a) `up-funnel`: move the optimisation event to a higher-volume proxy (qualified visit, form open, MQL) and retarget converters - the platform-advised path when the bottom-funnel event is unreachable - feeding CRM outcomes back so the proxy stays honest.
  - (b) accept manual or volume-independent bidding for that branch and judge it on leading metrics.

  - value: (a) > (b) - only (a) restores an optimisation signal; (b) just stops pretending there is one.
  - effort: (a) > (b) - (a) needs the tracking and CRM owners plus a standing job policing the proxy; (b) is a settings change.

  Take (b) first when there is no tracking owner to coordinate with, or when the effort ceiling from the Interview rules (a) out.

  This is the case the thresholds are hardest for and the one most often botched: a plan that merges a 5-conversions/month account into one campaign and declares victory has changed nothing.

## Measuring Whether the Merge Worked

Judge against the account's own pre-merge history, never industry benchmarks, over a full lag-mature window at equal attribution maturity on both sides. Expect and forecast the transient dip - a plan that does not predict the dip gets reverted inside it.

- **Baseline:** the pre-merge window's blended cost per conversion (or MER/blended CAC where revenue data exists) and the share of spend sitting in learning-limited or under-threshold branches.
- **Pass threshold** (this skill's own working target, not a researched constant), at the re-check date - one full learning cycle plus one sales cycle after the final phase:
  - Every surviving branch clears its volume-and-budget floor, or the plan states why it structurally cannot and what proxy it optimises instead.
  - Blended cost per conversion is at or better than baseline.
  - Iterate until met: if branches still sit under threshold, the next iteration merges further, raises floors, or (B2B) moves the event up-funnel.
  - If two iterations fail to meet it, treat that as evidence consolidation is not this account's fix and route back to `mbfinotti/advertising-skills@ad-account-diagnostic`.
- **Rollback trigger, defined before phase one:** blended cost per conversion worse than roughly 1.5x baseline after the no-touch window matures (starting point - set it from the account's own variance), or a preserved-for-a-reason segment starved below its floor. Rolling back means shifting budget back to the paused legacy structure - which is why it was paused, not deleted.
- **Prefer incrementality over platform-reported ROAS for the verdict.** The most common consolidation failure hands budget to already-converting audiences that report beautifully; reported retargeting ROAS is cited as overstating true incremental ROAS by 40-70%. Three ways to settle it, and the axes disagree:
  - value (evidence strength): geo holdout > platform lift study > platform-reported ROAS
  - effort: geo holdout (design, a market held dark, a quarter of patience) > platform lift study (in-platform setup, one cycle) > platform-reported ROAS (already in the dashboard)
  - efficiency: platform lift study > geo holdout > platform-reported ROAS

  Run the lift study by default. Escalate to a geo holdout when the merge moved a large share of the account's budget, or when the platform grading its own homework is exactly what is in dispute. Isolate confounders - seasonality, creative refreshes, price/promo moves, tracking or consent changes - by segmenting pre/post data, never blending it.

## Failure Modes

| Failure                               | What it looks like                                                                                                           | Fix                                                                                                       |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Pool starvation                       | One cheap branch (brand search, retargeting) eats the shared budget; blended numbers look great, growth branches go blind    | Pool only comparable-cost branches; minimum-spend floors; keep brand and retargeting on their own budgets |
| Retargeting absorbed into prospecting | Reported ROAS jumps, incrementality collapses - budget locked onto users who would have converted anyway                     | Separate funnel stages structurally; verify with a holdout, not the dashboard                             |
| New creative starved                  | Net-new concepts in a pool with proven ads get nothing within 48 hours                                                       | Isolate net-new concepts with a protected test budget                                                     |
| Over-consolidation                    | One undifferentiated pool; the algorithm parks on the easiest slice and never reaches the rest                               | Re-split into homogeneous bands with their own budgets - consolidation has a floor                        |
| Day-3 reversion                       | The predicted relearning dip arrives, nobody pre-committed, the merge is rolled back before it can work                      | Written no-touch window and evaluation date, signed before phase one                                      |
| Big-bang reset                        | Whole account restructured at once; everything relearns simultaneously; the outcome cannot be attributed                     | Phase the migration; keep a control                                                                       |
| Edit-in-place reset                   | "Just retargeting the existing campaign" silently resets its learning                                                        | Build new alongside, shift budget, pause the old                                                          |
| Panic merge                           | Restructuring mid cost-spike or mid learning phase as a reflex                                                               | Evidence Gate: diagnose first; a reset often costs more than the spike                                    |
| Threshold folklore                    | Applying one platform's conversion threshold, or a universal budget-to-CPA ratio, to a platform that documents no such thing | Use each platform's documented number or none; teach the derivation, re-verify live pages                 |
| Merged across economics               | Segments with different margin/LTV pooled under one target                                                                   | Preserve rule one: different unit economics keep their split                                              |

## Invocation Example

> "We run 14 search campaigns and 9 paid-social ad sets on about $9K/month, maybe 40 conversions total. What should we merge?"

Run the Interview, inventory every branch, compute per-branch volume against threshold, test each split against the preserve rules, classify, gate, then deliver the plan. See [./references/worked-invocation-example.md](./references/worked-invocation-example.md) for the full worked walkthrough.

## Platform Notes (optional - vendor-specific)

Skip this section for a tool-agnostic plan; read it when the user names a platform. Documented from each platform's own help pages - re-verify against the live page before quoting, these numbers drift:

- **Meta:**
  - ~50 optimisation events per ad set per rolling 7 days to exit learning.
  - "Learning Limited" has four documented causes: small audience, low budget, low bid, too many ads.
  - Significant edits, targeting, event, bid strategy, creative, or budget beyond ~20%, reset learning.
  - Its retired "Power 5" program listed account simplification as a pillar. Practitioners Ben Heath ("fewer campaigns; each extra campaign is another spinning plate the algorithm can smash") and Taylor Holiday ("8 ad sets × 8 ads on a small budget puts 70-90% of spend in learning") built the consolidation case on it.
- **TikTok:**
  - Volatility declines after ~25 results or 7 days.
  - ~50 conversions is the documented indicator of passing learning.
  - Ad-group budget ≥ 5x target CPA is documented guidance.
- **Google Ads:**
  - Learning runs "up to 3 weeks or 1-2 conversion cycles".
  - Target ROAS documented floors by campaign type: 15 conversions/30 days (Search/Shopping, Display), 30/30 (Video Action), 50/35 (Demand Gen), 50/week (Hotel), 50/7 days (Travel).
  - The Hagakure method is the search-side consolidation framework: collapse single-keyword ad groups into few high-volume intent-themed campaigns.
- **LinkedIn:** documents _no_ learning-phase conversion threshold at all, only $10/day and $100-lifetime minimums. Practitioner AJ Wilcox recommends manual bidding over max-delivery and a practical $3-5K/month floor for usable data.

**Folklore to actively debunk when the user repeats it** (most competing advice presents these as fact):

- "Target CPA requires 15 or 30 conversions in 30 days" - Google's own page says the strategy works with no conversion history; the 30 figure is an evaluation sample, not a gate.
- "50 conversions per week" applied to Google or LinkedIn - documented nowhere for either.
- "Daily budget must be 10x (or 5x) target CPA" as a universal law - a practitioner extrapolation from the 50-event arithmetic, not documentation.

## Reference

- `mbfinotti/advertising-skills@ad-bidding-strategy` - chooses the bidding method the merged structure runs on.
- `mbfinotti/advertising-skills@ad-spend-allocation` - splits the total budget across the resulting campaigns and platforms.
- `mbfinotti/advertising-skills@ad-negative-keywords` - search-term routing so merged search campaigns do not self-compete.
- `mbfinotti/advertising-skills@retargeting-funnel` - stage design when prospecting/retargeting separation is preserved.
- `mbfinotti/advertising-skills@ad-audience-targeting` - designs the targeting inside the consolidated structure.
- `mbfinotti/advertising-skills@ad-budget-pacing` - daily pacing once the new structure is live.
