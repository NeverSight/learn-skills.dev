---
name: partner-performance
description: Measure and review the performance of individual partners in a B2B partner program - the per-partner scorecard (dimensions, weights, targets, red-flag thresholds, data sources), the review cadence and QBR structure, and the underperformance ladder from trigger through corrective action to de-tier or exit. Also covers the B2C affiliate and creator review contrast. Use whenever the user mentions a partner scorecard, partner reviews, a channel partner QBR, a partner health check, or an underperforming channel partner, even if they never say performance. One partner at a time. Do NOT use for designing the tier ladder itself - use mbfinotti/partnerships-skills@partner-tiering instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.4"
---

# Partner Performance

Define how a B2B partner program measures and reviews individual partners: the per-partner scorecard, the review cadence and partner QBR, and the underperformance ladder. No single canonical partner-performance methodology exists - say so plainly rather than invent one. What the field genuinely offers for per-partner measurement:

- **A five-category engagement taxonomy**: sales performance, partner satisfaction, training/certification completion, marketing/lead generation, partner lifecycle and retention. No numeric weights are published anywhere - set them with the user. Evidence class: vendor blog.
- **A maturity-staged KPI taxonomy**: recruitment → activation → engagement → revenue efficiency, prioritized by program maturity rather than by fixed weights. Evidence class: vendor taxonomy.
- **Continuous leveling**: partner scores recalculated from CRM, LMS and portal data, visible to the partner, with at-risk flags that trigger coaching before de-tiering. Evidence class: vendor product model.
- **A four-step partner attribution journey** - crediting value to partners including non-transacting ones - is about attribution, not a per-partner scorecard. Use it upstream, as an input to the scorecard's revenue dimension. Evidence class: analyst blog.

These four are evidence inputs, not a menu to choose from - the choice the user actually makes is the scorecard approach, ranked under "Designing the system with the user". Each model is named to its originating vendor or analyst in [references/scorecard-design.md](references/scorecard-design.md); the concepts above are what the skill actually applies. Keep it that way - PRM vendors rebrand and restructure often, so a body written around today's product names dates faster than the ideas in it.

## Interview

Ask before designing anything. One question per message; offer multiple-choice options; skip whatever the user already answered.

- How many partners, and of which types - reseller, VAR/MSP, agency, SI, ISV/tech, referral, distributor? Which types actually transact?
- What is measured today, and where does the data live - CRM, PRM, LMS, spreadsheets, nowhere?
- Do partners currently see their own numbers?
- What is the review cadence today, and does it differ by tier?
- What does "underperforming" mean today - and does anything actually happen when a partner hits it?
- Roughly how much partner revenue is sourced vs influenced - and can your systems tell the two apart?
- Review culture today: is a QBR a working session or a status update?
- How many partner managers (PAMs), and what is the coverage ratio - partners per manager?
- Is this B2B channel only, or does the program also include affiliate/creator partners?
- What is immovable: signed partner agreements, fiscal calendar, existing tier commitments?
- Who signs off: channel chief, CRO, finance, legal?
- By what date must the first scored review actually land - inside the current review cycle, next fiscal year, no fixed date? A date inside the current cycle promotes the weighted composite alone and defers everything the program's partner mix does not force.
- Is this a one-off exercise - a board or QBR question you must answer once - or a system meant to run every quarter? A one-off stops at the composite; a compounding system justifies the leading/lagging split and per-type tracks, which only pay back across repeated reviews.
- What is the effort ceiling: partner-ops hours available, whether anyone can export portal, LMS and deal-registration data, and whether the design can still change once partners have seen it? No export capacity deletes the leading/lagging split from this design rather than deferring it; a scorecard partners have already been shown is close to irreversible, so settle the dimension list before socializing it.

Those last three answers re-rank the design options in the next sections - ask them before proposing anything, not while presenting the menu.

## Workflow

1. Run the Interview; collect every current-state fact the design depends on.
2. Confirm scope: measuring and reviewing individual partners in a running program. Tier design, program design, single-partner economics, and building the joint GTM plan belong to sibling skills (see Reference) - this skill reviews performance against a joint plan, it never builds one.
3. Inventory the data: mark each candidate metric computable today, computable with work, or unmeasurable. Never score on estimates.
4. Pick the scorecard approach from the ranked rungs in "Designing the system with the user", then design it: dimensions with weights, per-KPI target and red-flag floor, measurement window, data source and owner - with a track per partner type, including non-transacting ones. See [references/scorecard-design.md](references/scorecard-design.md).
5. Set recalculation cadence and partner visibility - what the partner sees, and when.
6. Design the review cadence by tier and the partner QBR. See [references/review-cadence-and-qbr.md](references/review-cadence-and-qbr.md).
7. Design the underperformance ladder: triggers → intervention → corrective action → de-tier/exit. Route anything that can de-tier or terminate through legal. See [references/underperformance-ladder.md](references/underperformance-ladder.md).
8. Validate per that same section: present the spec one section at a time and gate each before writing the next.
9. Dry-run the draft scorecard against real partners; inspect the score distribution and the PAM workload it implies; adjust.
10. Check the pass threshold; iterate until every check holds.
11. Stop at the approval gate - finalize nothing without the user's explicit approval of the full spec.
12. If your harness has persistent memory, memorize the approved scorecard, thresholds, and first review date; otherwise tell the user to store the spec where partner ops can retrieve it.

- If you can browse the web, verify any vendor model before citing it by name to the user; the attributions and their dates are in [references/scorecard-design.md](references/scorecard-design.md).
- Otherwise, flag vendor examples as possibly stale.

## Designing the system with the user

Run the design the way channel teams actually work - through partner ops modeling and stakeholder review, not as a solo spreadsheet exercise:

- Ask one question per message throughout; never batch questions.
- Assemble the data channel teams bring: sourced vs influenced revenue split, deal-registration records, certification/LMS completion, portal engagement, PSAT/NPS, MDF utilization. Model with what exists; name what is missing.
- Map who must be involved: channel chief accountable, partner ops builds the model, finance validates the numbers, PAMs must be able to run it, legal reviews anything that can trigger de-tiering or termination.
- Present the three candidate scorecard approaches below in the ranked order given, with your recommendation and its reason. They are rungs, not rivals - each layers onto the one before.
- Once the user picks a rung, present the spec one section at a time - scorecard, then cadence and QBR, then ladder - and validate each before writing the next.
- Socialize the near-final design with a partner advisory council or a pilot cohort before rollout; a measurement system partners never saw breeds disputes, not performance.
- Gate finalization on explicit user approval of the assembled spec.

### Ranking the scorecard approaches

Rank by what each approach settles per hour of partner-ops build time. This is pass threshold 5 - "a PAM can prepare a scorecard in the time they actually have" - applied to the design work as well as the review prep.

- efficiency: weighted composite > leading/lagging split > per-partner-type tracks
- value: weighted composite > per-partner-type tracks > leading/lagging split
- effort: per-partner-type tracks > leading/lagging split > weighted composite

1. **Weighted composite** - 4-6 dimensions, one number per partner. Settles the triage decision: which partners get the PAM's hours this quarter. Costs about a week of partner-ops work to define and near-zero per review afterwards, and it runs on CRM/PRM data most programs already hold. Fully reversible until partners see it.
2. **Leading/lagging split** - a results score beside an early-indicator score. Settles the timing decision: intervene now, or wait a quarter. Near-zero effort when the composite already carries pipeline, engagement or certification dimensions - tag each one and subtotal. A quarter of plumbing when portal, LMS or deal-registration data cannot be exported yet, and that case is what drops it below the composite.
3. **Per-partner-type tracks** - one dimension set per partner type. Settles the coverage decision: whether a non-transacting partner earns its investment, a question a single composite answers with a blank. Costs a week per type to define, each with its own data sources and negotiated targets, then becomes a standing job as partner types multiply.

Per-partner-type tracks are what this efficiency order starves: second on value, first on effort, last on the ratio. A program that only computes efficiency scores its transacting resellers well and leaves its ISVs, referral and advisory partners on a composite that reads as a blank. Promote rung 3 above rung 2 the moment the program holds a non-transacting partner type - pass threshold 3 requires a real score for it, and no amount of composite tuning produces one.

Defaults, and what moves them:

- Start every program at rung 1; add rung 2 as soon as the leading data exports cleanly.
- A program with one partner type deletes rung 3 from the design, and the spec names it as deleted with that reason - a track listed as "later" reappears as a build nobody scoped.
- A program that cannot export portal, LMS or deal-registration data, and has no capacity to build that plumbing, deletes rung 2 the same way - revisit it only once the export exists.

The order is a default, not a law: it shifts with context and with who executes it. Re-rank it against what the Interview already told you:

- A PRM that already reports leading indicators makes rung 2 near-free and promotes it above further composite tuning.
- A partner manager with no analyst support should ship rung 1 rather than a three-track design nobody can recompute next quarter.
- A hard date inside the current review cycle promotes whatever is computable today over whatever is better.

## The Partner Performance System

Deliver the engagement as this artifact - a decision record the user hands to partner ops, PAMs, and legal:

```
PARTNER PERFORMANCE SYSTEM , <program>, <date>
Scorecard:
  Dimensions       : each with a weight; weights sum to 100%
  Per KPI          : definition + target + red-flag floor + measurement window
                     + data source + owner
  Tracks           : one per partner type, incl. non-transacting
                     (ISV/tech, referral, advisory/SI)
  Recalculation    : continuous | monthly | quarterly, and who recomputes
  Partner visibility: what each partner sees, and when
Review:
  Cadence by tier  : which partners get a full QBR, which get lighter
                     check-ins; duration and attendees (user's design decision)
  QBR agenda       : sections, opening with last quarter's action check,
                     closing with a joint action plan
  Action tracking  : where owned, dated actions live between reviews
Underperformance ladder:
  Triggers         : trigger → intervention → timeline table
  Escalation chain : named roles per step
  Corrective plan  : shape, duration, checkpoints, stated consequence
  De-tier / exit   : criteria, gated on documented corrective action having
                     failed; legal-reviewed
System KPIs        : how the measurement system itself is judged,
                     with the first review date
```

Rules about the spec itself:

- Attach a data source and a named owner to every KPI - a metric nobody computes reviews nobody.
- Pair every target with a red-flag floor; a lone target hides decay until it becomes a crisis.
- Reject any metric a partner can self-report or game; use only data the program itself records.
- Present durations, attendee lists, thresholds, and timelines as the user's design decisions, they are self-set, not industry norms.

## Pass threshold

Ship nothing until all five hold; iterate the design until they do:

1. **Every KPI is fully specified**: target, red-flag floor, measurement window, named data source, named owner.
2. **Nothing is self-reported or gameable** - every scorecard input comes from data the program records and can defend in a dispute.
3. **Every non-transacting partner type is scorable** without resold revenue - an ISV, referral, or advisory partner gets a real score, not a blank.
4. **Every review ends with owned, dated actions** - and the next review opens by checking them.
5. **A PAM can prepare a scorecard in the time they actually have** - test the prep workload against the coverage ratio from the Interview.

## Diagnosing an existing review system

When the user arrives with a running system instead of a blank page, work the table top-down. The rows are ordered by reviews repaired per hour of change, not by severity:

- efficiency: action-tracking loop > QBR pre-read and agenda > cadence tiering > partner visibility > leading-indicator mix > per-type tracks > ladder enforcement
- effort: ladder enforcement > per-type tracks > leading-indicator mix > partner visibility > cadence tiering > QBR pre-read and agenda == action-tracking loop
- compliance cost: ladder enforcement - contract review of the demotion and termination terms, and a decision the partner can contest - > every other fix here, which carries none

The QBR pre-read and the action-tracking loop tie on effort because each is a change to a meeting that already happens - one line added to an agenda template, one shared document where actions live - with no new data source, no new system and nobody's sign-off. They part on value, and the action loop wins, since a review whose actions nobody tracks repeats itself.

The top two rows cost near-zero and change every review that follows. What that ordering starves is ladder enforcement: it is the only fix on the list that changes what happens to a partner who never improves, and it lands last because legal review gates it and a wrong demotion is expensive to reverse.

Promote it when partners have already sat through repaired reviews and still miss their numbers - at that point the review process is not the fault, and every further agenda fix is motion.

Re-rank against the program in front of you, and strike what does not apply:

- A program whose partners already see live scorecards has no visibility row.
- A program with a single partner type has no tracks row.

Delete both from the plan rather than leaving them as pending work.

| Symptom                                               | Check first                                                                                                   | Design variable at fault              |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Actions from last quarter never got done              | Whether the QBR opens with the prior action check, and where actions are stored between reviews               | Action-tracking loop                  |
| QBRs are one-way status updates                       | Whether a data pre-read goes out, and what share of the agenda is forward-looking                             | QBR agenda and pre-read discipline    |
| Every partner gets the same review regardless of size | Whether cadence and depth vary by tier                                                                        | Cadence tiering                       |
| Partner disputes the numbers                          | Whether the partner sees the same data before the meeting, and which system is the source of truth            | Data source and partner visibility    |
| Scorecard says green but the partner has gone quiet   | Whether any leading indicator (portal logins, deal registrations, certification activity) is on the scorecard | Dimension mix - lagging-only          |
| Only transacting partners have a score                | Whether per-type tracks exist for ISV/referral/advisory partners                                              | Scorecard tracks                      |
| Nobody is ever de-tiered                              | Whether ladder triggers have owners and timelines, and what legal blocks exist                                | Ladder enforcement, not the scorecard |

## KPIs

Judge the measurement system, not the partners - individual partner numbers are the system's input, not its score:

Instrument them in this order when nobody has analyst support - the first three are counts the program already records, the last two need a year of ladder history or a partner survey:

- efficiency: review completion rate > action-item completion rate > share with a current scorecard > dispute rate > ladder timeliness > ladder outcomes > review-process PSAT

1. Review completion rate against the planned cadence, by tier.
2. Action-item completion rate between reviews.
3. Share of partners with a computable, current scorecard.
4. Dispute rate on scorecard numbers raised by partners.
5. Share of red-flagged partners entering the ladder within its stated timeline.
6. Ladder outcomes: share recovering after corrective action vs de-tiered or exited.
7. Partner satisfaction (PSAT/NPS) with the review process itself.

That order starves ladder outcomes: it is the only number that says whether the underperformance ladder does anything, and it needs a year of ladder history before it reads at all, so a ratio buries it every quarter behind counts the program already holds. Promote it whenever the review in front of you is about whether to keep the ladder, or whenever de-tiering is being contested. Where the program has no ladder history and no survey capacity, delete rows 6 and 7 from the instrumentation plan and name them as deleted - carried as pending metrics, they let a later reader assume the ladder was evaluated.

## B2B vs B2C

Identical in both worlds:

- Every metric carries a target and a red-flag floor.
- The metric mix blends leading and lagging indicators.
- Nothing is self-reported.
- Every review produces owned actions.

Different:

- **B2B channel**: human-reviewed, relationship-bound - per-partner scorecards, PAM-run QBRs, a staged human ladder.
- **B2C affiliate/creator**: automated dashboards, cohort-level review, automated re-engagement - per-partner review only for the head of the distribution.

See [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md) for the full contrast with its evidence caveats.

## Invocation Examples

- "Design the per-partner scorecard for our channel program - 80 partners, mix of transacting resellers and non-transacting ISVs."
- "Three Gold partners have not sold in two quarters. Write the underperformance ladder from trigger to de-tier."
- "Our partner QBRs are status theater. Restructure the agenda and tell me what data both sides need before the meeting."

## Reference

- [references/scorecard-design.md](references/scorecard-design.md) - the dimension menu with metric definitions, weighting guidance, target/red-flag pattern, windows, gameability checks, non-transacting tracks, and a negative example.
- [references/review-cadence-and-qbr.md](references/review-cadence-and-qbr.md) - cadence tiering, the 10-section partner QBR agenda, preparation rules, and failure modes.
- [references/underperformance-ladder.md](references/underperformance-ladder.md) - trigger table, escalation chain, corrective-action-plan shape, and exit criteria.
- [references/worked-examples.md](references/worked-examples.md) - a worked transacting scorecard, a worked non-transacting ISV scorecard, and a worked underperformance sequence.
- [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md) - the full B2B/B2C review contrast.

Sibling skills (same collection):

- `mbfinotti/partnerships-skills@partner-economics` - single-partner P&L and unit-economics modeling.
- `mbfinotti/partnerships-skills@partner-ecosystem` - ecosystem-level health metrics; it hands per-partner scorecards and review cadences to this skill.
- `mbfinotti/partnerships-skills@partner-enablement` - measuring whether the enablement program worked, at program level.
- `mbfinotti/partnerships-skills@joint-gtm-planning` - builds the joint GTM/business plan with a partner; this skill reviews performance against that plan, never builds it.
- `mbfinotti/partnerships-skills@partner-channel-program` - designing a whole partner program from scratch.
- `mbfinotti/partnerships-skills@affiliate-performance-dashboard` - affiliate program metrics, a different discipline.
