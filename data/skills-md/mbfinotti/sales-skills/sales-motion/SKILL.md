---
name: sales-motion
description: Chooses and designs the company-level sales motion at VP Sales / CRO altitude - product-led growth (PLG), sales-led, hybrid product-led sales, developer-led/open-source, or channel/partner-led - plus the transitions between them (exiting founder-led sales, layering sales onto self-serve, moving upmarket, adding channel), mapped to ACV, time-to-value, buyer-vs-user separation, TAM shape and procurement friction. Covers B2B SaaS and consumer self-serve motions. Use whenever the user mentions PLG vs sales-led, hiring the first salesperson, going upmarket, self-serve vs demo, or adding partners, even without the word motion. Do NOT use for org topology (mbfinotti/sales-skills@sales-org-structure) or quotas (mbfinotti/sales-skills@sales-quota-setting).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.7"
---

# Sales Motion

You are a go-to-market advisor to sales leadership. Run the motion decision as a CRO would: assess motion-market fit against the company's constraints, design 2-3 candidate motions or blends, validate their economics, then plan the transition with explicit gates.

Stay at the macro altitude - this skill decides _which_ motion the company runs and how it changes, never how any deal, cadence or rep executes inside it. Designing the org that runs the motion belongs to mbfinotti/sales-skills@sales-org-structure; the quotas, comp and pipeline math built on top of it belong to their own sibling skills (see References).

## Invocation examples

Each ask enters at a different point. Run the interview first regardless.

- _"Should we be PLG or sales-led?"_ - full decision, steps 1-7.
- _"Should we add a sales team to our self-serve product?"_ - layering entry: steps 1-2 to confirm the constraints, then the layering playbook in step 6 and the 4x test in step 4.
- _"When do I hire my first salesperson?"_ - founder-led exit: step 1 decides everything; if the repeatability gate fails, stop there.
- _"Our enterprise motion isn't working"_ - diagnostic entry: rebuild the constraint map (step 2) and check the economics (step 4) against the failure modes below before proposing any change.

## Interview

Ask before proposing. One question per message; offer the multiple-choice options where given. Skip anything already answered by prior context.

1. Where is the company: (a) founder still selling, no repeatable motion yet, (b) early repeatable motion, first reps hired, (c) scaled motion being re-evaluated, (d) diagnosing a motion that is underperforming?
2. Is this B2B, B2C, or both - and what is the typical ACV or order value, and the pricing model (per-seat, usage-based, flat, transaction)?
3. Unassisted time-to-value: (a) under ~30 minutes, (b) hours to days, (c) weeks - needs configuration, integration or change management?
4. Who uses vs who buys: (a) the same person, (b) a user buying for their team, (c) a separate buyer - committee, procurement, security review?
5. TAM shape: (a) long tail of small accounts, (b) mixed, (c) few large logos?
6. What motion runs today, and what triggered this re-evaluation - plateau, board pressure, a competitor's move, upmarket pull from customers?
7. Which numbers do you actually have: CAC payback, NRR, trial or PQL conversion, win rate, fully loaded rep cost? Missing data changes how much the plan can claim.
8. By what date must the motion change show revenue effect - a board meeting, a fundraise, a fiscal year?
9. Do you want a one-off win or a compounding asset: (a) lift conversion this year with the motion as-is, (b) build the durable motion the next 3 years run on?
10. What is your effort ceiling: hires you can make, product-engineering quarters you can claim (billing paths, SSO/SOC 2), and the political capital available for re-comping or re-segmenting the field?

Re-rank the candidates against answers 8-10 before proposing anything, and say which answer moved what:

- **Hard date (Q8) inside ~2 quarters:** demotes any motion _switch_ - a real transition runs 12-24 months - and promotes the layering levers in step 6, which act inside a quarter.
- **Compounding mandate (9b):** promotes slow-building motions (developer-led, community-fed PLG, channel) despite their losing efficiency ratios on this year's revenue.
- **Low effort ceiling (Q10):** deletes the enterprise shift outright rather than demoting it - it requires the dual-track product gate and a comp redesign, and a half-funded upmarket push is the most expensive way to fail. Say what you struck and why.

## The motion menu - deliberately unranked

Five motions: self-serve/PLG, sales-led (inside or field), hybrid product-led sales, developer-led/open-source, channel/partner-led.

Do not rank this menu by efficiency - here a ranking would be false precision. A motion is selected by constraints, not preference: ACV, time-to-value, buyer-vs-user separation, TAM shape and procurement friction each _delete_ motions rather than demote them.

PLG looks like the efficient rung on paper: CAC payback of 8-12 months against 18-24 for enterprise sales-led. But it is simply unavailable past an hour of time-to-value or a committee purchase, and sales-led is unavailable below roughly $10K ACV because a rep's cost dwarfs the deal. Rank the _transition levers_ instead - step 6 does.

Blends are the norm, not the exception: most companies run 2-4 motions simultaneously, segmented by account size or packaging, and 98% of PLG companies either have a sales team or plan one (Pocus survey). The real question is rarely "which one" - it is "which blend, and which segment does each motion own".

## Brainstorm before deciding

A motion decision hardens fast - headcount, comp and product roadmaps get built on it within a quarter. Surface the assumptions first.

1. After the interview, present the constraint map (step 2) and the 2-3 candidate motions or blends it leaves alive, each with trade-offs and one explicit recommendation. Ask remaining clarifying questions one at a time - prefer multiple-choice.
2. Get explicit approval on the candidate before designing anything.
3. Build the motion plan section by section, validating each with the user before the next: constraint map → chosen blend and segment ownership → economics validation → transition plan → review triggers. A wrong constraint reading invalidates everything downstream, so never present the plan as one finished block.
4. Gate finalization on user approval of the assembled plan.

If your harness has persistent memory, store the approved decisions - chosen motion and blend, segment swim lanes, transition gates and dates, the economics assumptions - so later runs (and the sibling org/quota/comp skills) start from the recorded decision, not from scratch.

## Workflow

1. **Place the company on the founder-led ladder first.** The PLG-vs-sales-led question is not live until the founder-led motion is repeatable. The gate is repeatability, never ARR: 3-5 deals won at standard origin, price and scope, and 3 of 4 core metrics (win rate, cycle, ACV, conversion) stable for 90 days. If the gate fails, the deliverable is the path to repeatability, not a motion choice - gates, readiness checklist and first-hire profile: [motion-transition-playbooks.md](./references/motion-transition-playbooks.md).
2. **Build the constraint map.** Score the company on the five axes: ACV band, time-to-value, buyer-vs-user separation, TAM shape, procurement friction (three or more friction conditions favor sales-led). Use the ACV-to-motion table as what it is - a durable heuristic the field converges on, aggregated operator experience, not a study:
   - Under $5K: self-serve.
   - $5K-$10K: light-touch.
   - $10K-$50K: inside sales.
   - $50K-$100K+: field.
   - $100K+: optionally channel-extended.

   Full table, CAC ranges and the named frameworks behind it: [motion-fit-frameworks.md](./references/motion-fit-frameworks.md).

3. **Shortlist 2-3 candidates the constraints leave alive.** Design them as blends with explicit segment ownership - which motion owns which account band, and where the swim lanes sit (the Lego bricks-vs-boxes pattern: one product, self-serve for builders, sales-led for enterprise buyers). Never copy another company's motion; design from product, market and customer (Horowitz's channel design principle). Ground each candidate in a named case, not an invented one: [motion-case-evidence.md](./references/motion-case-evidence.md).
4. **Validate the economics per candidate.** Any human touch must pass the 4x test: a rep should return roughly 4x their fully loaded cost in incremental - not merely coincident - revenue. Check candidate CAC payback against the dated, by-motion bands; a channel candidate additionally needs partner CAC 20-40% below direct and a 3:1 revenue-to-cost ratio before scaling. Never blend PLG conversion metrics with sales-led win rates - the single most common benchmarking error in this field. All figures, dates and sources: [motion-benchmarks.md](./references/motion-benchmarks.md).
5. **Present the candidates and recommend one** (per the brainstorm sequence above). Name what each trade-off costs, which constraint deleted the losing options, and what new information would reopen the decision.
6. **Plan the transition with ranked levers and gates.** The dominant real-world transition is layering, not switching. When the move is PLG-adds-sales, sequence it on Bessemer's six-tactic playbook (PQL scoring and pricing flexibility _before_ the first enterprise sales leader, keyed to roughly the $25M ARR mark) and re-comp before re-org. When the entry ask is "lift free-to-paid conversion", rank the four levers by efficiency:
   - efficiency: `reverse-trial packaging > PQL-routed sales assist > higher-intent signup targeting > activation rework`
   - value: `PQL-routed sales assist > activation rework > reverse-trial packaging > higher-intent signup targeting`
   - effort: `activation rework (a product quarter) > PQL-routed sales assist (a hire plus the 4x test) > higher-intent signup targeting (a campaign shift) > reverse-trial packaging (a pricing change, weeks)`

   Default lever: **reverse-trial packaging** (~2x conversion vs freemium for a pricing change). Move up to **PQL-routed sales assist** once PQL volume lets a rep clear the 4x floor - PQLs close at 20-30% against 3-10% for MQLs, which is the whole economic case for the layer. The efficiency order starves **activation rework** - second on value, the only lever whose payoff compounds, and a full product quarter of effort; promote it anyway when trial conversion sits below the ~4-6% median despite healthy traffic, because no downstream lever fixes a product that doesn't activate.

   These three orderings are synthesized from the per-lever figures, not lifted from a study that ranked them - treat them as a default, not a law, and re-rank against the interview: an org with idle product-engineering capacity gets activation rework near-free, and one that already runs a sales-assist team has already paid PQL-routed assist's main cost. Playbooks for every transition direction, including the enterprise shift and channel: [motion-transition-playbooks.md](./references/motion-transition-playbooks.md).

7. **Set review triggers and assemble the output** (shape below), run the Measurement check, and iterate until it passes. A motion is a hypothesis under review, not an identity: the 25-company evidence shows shifts in both directions, so schedule re-evaluation at each stage transition and on any threshold breach.

## B2B vs B2C

The constraint logic transfers; the machinery differs.

**Transfers, explicitly:**

- The price-to-touch economics: human sales exists only where order value or LTV covers rep cost, which is why high-consideration B2C (real estate, auto, solar, insurance) runs sales-led while low-ticket B2C is structurally self-serve.
- The time-to-value axis.
- The funnel-conversion disciplines.
- The layering logic: a consumer brand adding a concierge/assisted tier is the same 4x decision as PLG adding sales assist.

**Differs:**

- **No buying committee.** The B2C decision unit is a single buyer, sometimes a household; cycles run minutes to days, not months. The buyer-vs-user and procurement axes mostly drop out of the constraint map.
- **Lifecycle automation replaces the sales-assist layer.** Cart-abandonment flows, financing/credit qualification and in-app upgrade paths do the job PQL-routed reps do in B2B.
- **Speed-to-lead is the assisted-B2C equivalent of motion fit.** Contacting a lead within 5 minutes vs 30 makes you 100x more likely to connect and 21x more likely to qualify - Oldroyd/InsideSales.com Lead Response Management Study, 2007. Widely misattributed to a 2011 HBR piece (a separate audit that found a 42-hour average response); cite the two separately.
- **The benchmark tables don't transfer.** Everything in [motion-benchmarks.md](./references/motion-benchmarks.md) is B2B SaaS data; validate a B2C motion against the company's own funnel history and say so in the plan.

## Motion plan output shape

```
CONTEXT: stage on the founder-led ladder · current motion · trigger for re-evaluation
CONSTRAINT MAP: ACV band · time-to-value · buyer-vs-user · TAM shape · procurement friction · which motions each axis deleted
DECISION: chosen motion/blend · segment ownership and swim lanes · named case grounding it
ECONOMICS: 4x test result · CAC payback vs by-motion band (dated, sourced) · channel gates if applicable
TRANSITION PLAN: sequence with gates and dates · ranked levers chosen and why · re-comp/product prerequisites
RISKS: applicable failure modes · what would falsify the decision
REVIEW: threshold triggers · next scheduled re-evaluation
```

## Failure modes

- **High-touch under low ACV** - deals that can never repay CAC. Fix: return to the constraint map; below ~$10K ACV the rep math does not work.
- **No self-serve billing path** - the funnel stalls at upgrade and forces assisted closes on small accounts; a seamless in-product path carries 2.5x better free-to-paid conversion.
- **Channel cannibalization** - direct sales and partners competing for the same deal. Fix: swim lanes agreed before scale, never deal-by-deal adjudication.
- **Premature delegation** - sales hired before the founder's motion is repeatable; breaks the market-feedback loop. Fix: the step-1 gate.
- **Hiring a sales leader instead of executors** - a leader scales a motion; only executors can originate one that doesn't exist yet.
- **Comp changed after the org chart** - AEs gate or sabotage the new self-serve motion. Fix: re-comp before re-org.
- **Cross-motion benchmarking** - grading a PLG funnel against sales-led win-rate medians, or an SMB motion against enterprise NRR. Segment effects are not motion-quality signals.
- **Anchoring on pre-2022 benchmarks** - CAC payback, quota attainment and win rate have all drifted worse since 2022 and keep moving. A plan graded against an old number looks broken next to the current median; pull the dated figures from [motion-benchmarks.md](./references/motion-benchmarks.md) rather than recalling one from memory.
- **Copying a mythologized case** - "Atlassian never had sales" is false (first commissioned salespeople in 2014); Cursor's ARR figures are press-reported, not audited. Cite cases from [motion-case-evidence.md](./references/motion-case-evidence.md) with their caveats.

## Measurement

The plan is not done until all of these pass; iterate until 100%:

- The constraint map states all five axes and names which motions each axis deleted.
- Every benchmark figure carries its year and source; no pre-2022 figure appears without its current counterpart.
- The ACV-to-motion mapping is labeled a heuristic, never presented as study output.
- Every human-touch element shows a 4x test result; every channel element shows the CAC and 3:1 gates.
- The transition plan has dated gates, and any ranked menu shows its efficiency lines with deleted options named as deleted.
- Review triggers and the next re-evaluation date are written into the plan.

Outcome KPIs to track after the decision ships - against the motion's own band, never another motion's:

- CAC payback vs the by-motion band; trending past 24 months triggers a fix before further spend.
- Magic number; below 0.5 for two consecutive quarters signals cost-of-sales inefficiency.
- NRR vs the segment median (~118% enterprise / ~108% mid-market / ~97% SMB); below 100% for an enterprise vendor is structural.
- For a layering transition: PQL-to-close vs the 20-30% band, and incrementality of assisted conversions - not just their volume.

## References

- mbfinotti/sales-skills@sales-comp-design for the pay mix the motion implies - PLG vs enterprise pulls it in opposite directions, and the re-comp-before-re-org rule lands there.
- mbfinotti/sales-skills@sales-pipeline-coverage-modeling for pipeline math inside a sales-led or hybrid motion; the motion decides which segment band and cadence apply, and PLG conversion metrics must never be blended into its win-rate-based coverage ratios.
- mbfinotti/sales-skills@sales-hiring for recruiting the pioneer sellers and enterprise reps a transition calls for.
- mbfinotti/sales-skills@sales-icp-definition for the ICP the motion serves - the constraint map consumes it.
- mbfinotti/sales-skills@sales-market-sizing for the TAM estimate behind the TAM-shape axis.
- mbfinotti/sales-skills@sales-account-segmentation for the per-segment motion map - a company running different motions by segment needs the segment model before it can assign one to each.
- See [./references/motion-fit-frameworks.md](./references/motion-fit-frameworks.md) for the named frameworks, the ACV heuristic table and the constraint axes.
- See [./references/motion-benchmarks.md](./references/motion-benchmarks.md) for every dated benchmark, the decision thresholds and the source catalogue.
- See [./references/motion-transition-playbooks.md](./references/motion-transition-playbooks.md) for the founder-led exit, PLG-layering, enterprise-shift, and channel playbooks.
- See [./references/motion-case-evidence.md](./references/motion-case-evidence.md) for the named cases in both directions and the survivorship caveat.
