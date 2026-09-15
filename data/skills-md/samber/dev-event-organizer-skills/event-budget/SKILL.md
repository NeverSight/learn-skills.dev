---
name: event-budget
description: Build the budget and P&L for a technical event - every cost line split into fixed and per-head, the revenue mix against the funding model, a Good/Better/Best scope-tier ladder so break-even has three answers instead of one, a contingency sized as a stacked floor, pad and downgrade ladder, and outflows scheduled against the dates sponsor and ticket money actually lands. Use whenever asked to build an event budget, model conference or hackathon costs, find break-even, size a contingency reserve, plan event cash flow, or decide what to cut when revenue falls short. Consumes prices and real vendor quotes, never sets them. Do NOT use to set ticket or sponsor prices - use samber/dev-event-organizer-skills@event-ticket-pricing or samber/dev-event-organizer-skills@event-sponsor-pricing.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Budget

You model the money for one edition of a technical event. Produce five things:

- The cost lines, and which of them scale with heads.
- The revenue total, and where it comes from.
- The cushion.
- The dates cash moves.
- The cut order when revenue falls short.

Consume prices - ticket, sponsor, venue, vendor - never derive them. Hand back every number as either a dated quote or a labelled placeholder.

Treat every ranking below as a default, not a law. Re-rank against what the interview turns up: a recurring event with last edition's actuals, an organizer with no accounting capacity, a fiscal host already taking a share off the top, a format with no ticket-revenue line at all. Each overturns a default rung.

**No currency amount appears anywhere in this file.** The real figures - published P&Ls, revenue splits, unit costs, fee ranges - live in the references with their event, year, and source, carried across as ratios, never copied as amounts.

## Ticketed or free-by-construction

The axis that changes the budget work is **whether the format has a ticket-revenue line at all**, never who pays for the attendee. The same catering invoice arrives whether the attendee expensed the ticket or paid it themselves, and sponsors are a business buyer in both cases.

- **Ticketed** - a genuine two-line revenue mix. Sponsorship share is a lever the team sets and can miss. Once sponsorship is booked, break-even is an attendee count at a price, and the downgrade ladder exists because the ticket side is uncertain.
- **Free-by-construction** - typically a hackathon, sometimes a conference. Sponsorship is close to the whole funding source, not by target but because the format offers no priced alternative. Break-even collapses to a fundraising target, and the only lever left is total spend per head.

Name which one the model assumes in the first line of the output. Keep the two cost taxonomies apart too: they differ in shape and must never be blended (see [references/cost-taxonomies-and-sourced-benchmarks.md](references/cost-taxonomies-and-sourced-benchmarks.md)).

## What arrives already decided

Take these as inputs. Re-deriving any of them produces a second, competing number nobody reconciles.

| Sibling                                              | Owns                                            | You do                                                                                                     |
| ---------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `event-ticket-pricing`                               | The ticket price ladder                         | Hand it the ticket target and the paid capacity after comps; it returns the actual sold total for variance |
| `event-sponsor-pricing`                              | Tier splits                                     | Own the sponsorship-share target; it splits into tiers                                                     |
| `event-venue-sourcing`                               | Real quotes, terms                              | Hold the line-item slot, fixed/per-head character, deposit timing                                          |
| `event-vendor-sourcing`                              | Every other supplier quote                      | Same split: it quotes, you shape                                                                           |
| `event-production`                                   | The Media line, pre-split by tier               | Take it as handed                                                                                          |
| `event-no-show-management`                           | The expected-show-up number                     | Budget from it, never the registration count; the overbooking buffer is the gap                            |
| `event-team-structure`                               | Which entity holds the money                    | Model what it costs and how fast it releases funds                                                         |
| `event-risk-management`                              | The risk case for a reserve, go/no-go placement | **You pick the contingency number**                                                                        |
| `event-growth-strategy` / `event-portfolio-strategy` | Whether the edition grows, portfolio split      | Re-run this model at whatever scale they set                                                               |

Hand post-edition variance to `event-debrief`, never re-modelling it, and hand a cost line creeping across editions to `event-continuous-improvement`. Plan and track one edition only.

## Interview

Ask one at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge on time-to-effect, durability and effort - their defaults cannot be picked for the user.

1. What is the format, and does it charge for attendance at all?
2. What is the expected show-up number, who produced it, and is it a show-up figure or a registration count?
3. Which cost lines already have a real dated quote? Which are still guesses?
4. Which entity holds the money, and what comes off the top (fiscal-host share, processing fees, parent contribution)?
5. What is already contractually committed, and on what date does each commitment stop being recoverable?
6. By what date must sponsor and ticket money be **in the account**, not invoiced? A hard date promotes postures that book early.
7. One-off edition, or one year of a recurring event? A recurring event reuses last edition's costed tiers, making the ladder near-free the second time.
8. Effort ceiling: who holds a standing tracking job through the sale window, and is there accounting capacity at all?
9. Who approves spend, and does any expenditure need a second approver who isn't the spender?
10. Does the audience typically attend on employer training budgets, and does the program already clear those budgets?
11. Does any counterparty - venue, vendor - offer a genuine discount for paying early?

## Workflow

1. Run the interview. Fix the format, scale, and which funding-model decisions are already made elsewhere.
2. **List cost lines from the format's own taxonomy** - conference and hackathon differ in shape, never blend them: [references/cost-taxonomies-and-sourced-benchmarks.md](references/cost-taxonomies-and-sourced-benchmarks.md).
3. **Cut every line into fixed and per-head, naming each per-head driver.** Both the split and the assignment of each named line to a side are this skill's own construction, carried over from general financial modelling rather than measured against event data. Take the head count from Q2's expected-show-up figure, never the registration count: budgeting off registrations is the single most common way an event over-orders. Keep the resulting cost per head on hand; it answers a "too expensive" pricing complaint with arithmetic instead of an opinion.
4. **Fill each line with a real dated quote or an explicit placeholder.** Never invent a price to balance the model - write "no quote yet" and carry it as a range.
5. **Deduct what comes off the top first**: fiscal-host share, processing fees on both rails, required parent contribution. Fee ranges: [references/cash-flow-fiscal-hosting-and-tax.md](references/cash-flow-fiscal-hosting-and-tax.md).
6. **Set the revenue mix** (menu below), then hand the targets out: the sponsorship target to `event-sponsor-pricing`; the ticket target (expenses minus sponsorship share) plus paid capacity after comps to `event-ticket-pricing`. Count comps from agreements actually held, never from a ratio.
7. **Cost the Good/Better/Best scope-tier ladder** - three fully-costed versions (Good runs at all, Better adds expected niceties, Best has real headroom), break-even computed per tier. On free-by-construction, each tier is a fundraising target instead.
8. **Size the contingency** using the three-tool stack below.
9. **Build the cash-flow schedule**: every outflow on the date it leaves, every inflow on the date it lands, then read the lowest cash point. Hand checkpoint dates to `event-planning-timeline` and `event-risk-management`.
10. **Write the tax and jurisdiction question rather than answering it.** Route it to the fiscal host, a local accountant, or counsel, then record the answer as a budget line.
11. **Track live against the plan**, validating with the user section by section.

If your harness has persistent memory, record:

- The line taxonomy, with each line's fixed/per-head character.
- The quotes, with their dates.
- The three costed tiers.
- The contingency figure, and how it was reached.
- The cash-flow schedule, with its lowest point.
- After the edition, actual against planned, per line.

The next edition starts from that record instead of a blank spreadsheet. When rewriting a recurring per-head consumable line from what was actually used, record its calibration basis too: the headcount and staff/volunteer/speaker composition it was priced against. A later edition scaling that line then knows what baseline it is adjusting, not just the raw number.

## Revenue-mix posture

Which shape the funding takes. This posture is largely inherited rather than chosen here: the format and the upstream funding-model decision usually fix it. Name which one arrived, and what it implies for the model. Ranking (default, not a law - re-rank against Q1, Q6, Q7):

- effort (modelling work plus the standing revenue management each posture demands): `registration-led > sponsor-led > sponsorship-by-construction`
- value (budget covered without the decision to run hanging on money that arrives late): `sponsor-led > sponsorship-by-construction > registration-led`
- efficiency: `sponsor-led > registration-led`

- **Sponsor-led** (default for a community conference) - sponsorship carries the bulk, registrations cover per-attendee cost. Decouples "will we run at all" from the ticket curve, which makes the downgrade ladder workable.
- **Registration-led** - registration carries the bulk, sponsorship marginal. Tops effort - a sales pace managed across the whole window, money lands latest. **Promotion condition, keyed to Q10**: the audience attends on employer training budgets and the program already clears those budgets.
- **Sponsorship-by-construction** - free-to-attend, no ticket line, share near-total by format not target. Deliberately absent from the efficiency line: the format chooses this posture, not this skill. Cost is concentration - one revenue source, no second lever.

**What this order starves:** registration-led, the only posture whose revenue scales with what the audience pays rather than with sponsor budgets. Follow the default long enough and the sponsor pool becomes the event's ceiling. A community that outgrows that pool has no second lever, and this order gives no warning until the pool is exhausted. Promote registration-led on the condition above.

**Delete, do not demote: sponsor-led and registration-led, on a free-to-attend event** - from this menu and the axis lines. Ranking postures that assume a ticket line invites a ticket price to reappear later as the fix for a shortfall - a funding-model reversal dressed as a budget adjustment.

Three published actuals disagree almost completely - see [references/cost-taxonomies-and-sourced-benchmarks.md](references/cost-taxonomies-and-sourced-benchmarks.md) for the range. Read them as postures that exist, never a norm to hit.

## Contingency provision: a stack, not a ranking

**This section deliberately does not rank its options.**

The three tools compose: a real budget runs all three at once. Ranking them would imply picking one, the opposite of how the stack holds together.

Even if they were competing, a ranking would rest on nothing:

- Value and effort run in the _same_ order across all three - floor lowest on both, ladder highest on both.
- Every pair therefore splits the two axes: each option wins one and loses the other.
- No dominance relation exists anywhere in the menu for an efficiency line to honour.

An unfalsifiable ranking is not a passed check.

- **A floor** - an absolute minimum cash reserve held regardless of budget size, covering the small certain surprises that always arrive (figure and source in [references/cost-taxonomies-and-sourced-benchmarks.md](references/cost-taxonomies-and-sourced-benchmarks.md)). Cheapest of the three: one number, decided once.
- **A pad on the estimates** - a percentage added to expense estimates before summing, protecting against line-item underestimation rather than revenue shortfall. The one figure available for it is a convention carried over from startup financial modelling, not measured against event data. Label it that way every time it is quoted.
- **A downgrade ladder** - the Good/Better/Best tiers with dated checkpoints, driven by revenue actually received. The only one of the three that absorbs a _whole-event_ shortfall rather than a line-item miss, and the most expensive: three fully-priced versions plus checkpoint dates threaded into the plan. On a recurring event (Q7) the tiers are reusable, cutting cost sharply from the second edition on.

**Neither the flat floor nor the borrowed pad is an event-industry convention, and this skill will not present either as one.** Say that to the user rather than producing a percentage that sounds authoritative.

### The cut order lives inside the ladder

The cut order _is_ the ladder's content - the tiers are this sequence, pre-priced and pre-decided. Not a second menu: presenting it separately would ship the same decision twice. Not ranked either: both readings of it (damage avoided per cut, how late the cut can be made) produce the identical order, so a ranking line would only restate it.

Each rung rests on a sourced mechanic: the scope-tier ladder behind the tiers, the attrition exposure behind the fixed lines. The order they sit in is this skill's own construction, not an observed convention.

1. **Discretionary extras first** - the evening event, swag upgrades, sponsored add-ons. This is the Best tier's own content, and cutting it protects the core experience entirely.
2. **Per-head variable quantities second** - catering covers, badge and lanyard counts - only where the guarantee hasn't locked yet. Past the lock date this rung is gone, which is why the cut order must be decided against the cash-flow schedule, not in the abstract.
3. **Fixed structural lines last** - the venue tier, the core Media line. These commit earliest and can cost more to cut than to keep. Attrition thresholds and food-and-beverage minimums are owed on what was committed, not on what turned up, so a downgrade can produce a penalty larger than the saving.

## Outflow commitment posture

How the budget commits money against revenue not yet banked - the liquidity question, distinct from `samber/dev-event-organizer-skills@event-planning-timeline`'s choice of buffer mechanic. That skill owns the calendar; this one decides how far the discipline goes and hands the dates back. Ranking (default, not a law - re-rank against Q5, Q6, Q8):

- effort (tracking work, counterparty conversations, standing attention through the sale window): `staged against a tracked signal > latest safe date > earliest date allowed`
- value (money still in hand when a revenue line misses, and quantities committed against a real number): `staged against a tracked signal == latest safe date > earliest date allowed`
- compliance cost (the review each posture triggers and the reversibility it costs at the moment of payment): `earliest date allowed > latest safe date > staged against a tracked signal`
- efficiency: `latest safe date > staged against a tracked signal > earliest date allowed`

**Dominance check: 3 pairs, zero strict-dominance relations.** Two mechanisms block it:

- The two pairs against earliest-date-allowed fail on effort: keeping more money in hand costs strictly more tracking and counterparty attention, even though it is cheaper on reversibility.
- Staged against latest-safe ties on value, each cheaper on a different cost axis (staged spends less reversibility, latest-safe less attention), so neither is at least equal on both.

Staged and latest-safe tie on value: both leave the same money uncommitted on the same date. They differ only in whether commitment arrives as one decision or several, which changes _when you learn_, not how much you keep. Learning is a demand read `samber/dev-event-organizer-skills@event-market-fit` already owns, so it is not counted twice here.

Compliance cost is real here, expressed as reversibility, never money. Paying before a stated cancellation date spends recoverability you were under no obligation to spend, and it does not come back.

A room block or catering guarantee committed at full size carries a usage threshold owed regardless of turnout. A small block grown in steps keeps exposure proportional to what is confirmed - see [references/cash-flow-fiscal-hosting-and-tax.md](references/cash-flow-fiscal-hosting-and-tax.md) for the staging tactic in practice.

- **Latest safe date** - the default and the efficiency winner: identify, per commitment, the last date it can be made without losing the thing, and hold until then. The asymmetry is the whole argument - adding capacity late is cheap and fast, unwinding a committed order is expensive or impossible.
- **Staged against a tracked signal** - the starved option: ties top on value, tops effort, so efficiency never leads with it. Promotion condition (Q5 + Q8): the commitment carries a threshold owed regardless of turnout **and** someone can hold a standing tracking job through the sale window. Both required; staging without a tracker is just a smaller order.
- **Earliest date allowed** - the do-nothing baseline, kept in the menu only so the reader can see what it costs. It tops compliance cost and buys nothing back.

**Delete, do not demote: earliest date allowed, whenever Q11 says no counterparty offers a genuine early-payment discount** - from this menu and the axis lines. With nothing on the other side of the reversibility it spends, it is a pure loss that, parked at the bottom, reappears as "we may as well pay it, it's budgeted."

## What this skill will never state

- **A tax rate, threshold, form name, or registration requirement, as though it were general.** Ticket and sponsorship revenue follow different, jurisdiction-specific rules - see [references/cash-flow-fiscal-hosting-and-tax.md](references/cash-flow-fiscal-hosting-and-tax.md) for contrasting jurisdiction examples. The answer comes from the fiscal host, a local accountant, or counsel.
- **A contingency percentage presented as an industry convention.** Size it from the three tools in the stack above and label the result self-set.
- **A venue or vendor price benchmark.** No published benchmark exists for either; three real quotes on one identical requirements sheet is the substitute, owned by `samber/dev-event-organizer-skills@event-venue-sourcing` and `samber/dev-event-organizer-skills@event-vendor-sourcing`.
- **A named accounting platform, ticketing platform or fiscal host as a recommendation.** Fee structures appear in the references as published facts about a market, not as picks.

## Failure modes

- **Per-head costs budgeted off the registration count.** The registration count is who was accepted; the expected-show-up number is who eats. Catering ordered against the first is over-ordered by construction.
- **A budget that is profitable and still fails.** Deposits leave before sponsor invoices are paid - see [references/budget-failure-case-studies.md](references/budget-failure-case-studies.md) for two cases of exactly this shape. Read the lowest cash point, not the bottom line.
- **Announcing a date before there is a working way to process money.** Settle who holds the money, and how long it takes to get back out, before the date goes public - an organizing guide states this failure directly in [references/cost-taxonomies-and-sourced-benchmarks.md](references/cost-taxonomies-and-sourced-benchmarks.md).
- **One budget instead of three tiers.** A single budget has one break-even and no move except cancelling. The ladder exists so a revenue miss has a response that is not a cancellation.
- **Treating the money-handling share as a rounding error.** A fiscal host's cut and processing fees come off everything passing through, on both rails, before any line is funded.
- **Cutting a fixed structural line first.** Attrition thresholds and food-and-beverage minimums are owed on the commitment, so the penalty can exceed the saving. Follow the cut order.
- **Quoting a contingency percentage, or a tax rule, as a standard.** Neither has an event-industry standard behind it. Saying so costs nothing; inventing either gets discovered by an auditor or a tax authority.
- **Reading one published event's revenue split as a norm.** The three published actuals disagree almost completely. They bound the space of real postures; none of them is a target.
- **Re-deriving a ticket or sponsor price to make the model balance.** That produces a second number competing with the prices `event-ticket-pricing` and `event-sponsor-pricing` already set. Change the target and hand it back instead.

## Measurement

This skill sets one binary gate for itself, plus the self-set observables below. Pick two or three of them, and write down before the first commitment what each would change.

**Gate (binary, checkable):** at the first go/no-go date, every cost line carries either a dated quote or an explicit "no quote yet" label, and the cash-flow schedule has a computed lowest point. A budget with silent placeholders has not been built yet, whatever its total says. Iterate until this passes.

- **Variance per line, planned against actual** (self-set): the number `samber/dev-event-organizer-skills@event-debrief` will ask for. Per line, never as one total - a total nets an underestimate against an overestimate and teaches nothing.
- **Lowest projected cash point against the lowest actual cash point** (self-set): if the actual trough is far below the projection, the inflow dates were optimistic, which is a different fix from the costs being wrong.
- **Contingency drawn against contingency held** (self-set): drawing none for several editions is evidence the floor is oversized; drawing all of it is evidence the pad is undersized.
- **Which tier the event actually ran at, against which was planned** (self-set): a ladder that never downgrades and never upgrades is not being used as a ladder.

## Invocation examples

- "We are planning a 250-person community conference and have a venue quote and nothing else. Build me the budget."
- "Sponsorship is at 60% of target with eight weeks to go - what do we cut, and in what order?"
- "Our hackathon is free to attend. How do I work out what we need to raise, and how much cushion?"
- "The venue wants a deposit in March but sponsor invoices are not due until June. Are we going to run out of money?"

Expected output: a budget model containing:

- The format and revenue posture, named in the first line.
- The cost taxonomy, split into fixed and per-head, with each per-head line's driver.
- Every line, labelled with a dated quote or an explicit placeholder.
- The top-of-budget deductions.
- The sponsorship and ticket targets, with their arithmetic.
- Three costed tiers, with a break-even each.
- The contingency figure, with the three tools stated separately.
- A dated cash-flow schedule, with its lowest point marked.
- The open tax question, written as a question.

Deliver it section by section for validation, with every number labelled published or self-set.

## References

- [references/cost-taxonomies-and-sourced-benchmarks.md](references/cost-taxonomies-and-sourced-benchmarks.md) - the two cost taxonomies with their fixed/per-head cut, the published itemized P&Ls and revenue splits with their events, years and sources, the per-person unit benchmarks, the comp and scholarship allocation figures with their caveats, and how to carry any of it across by ratio.
- [references/cash-flow-fiscal-hosting-and-tax.md](references/cash-flow-fiscal-hosting-and-tax.md) - deposit and attrition mechanics, sponsorship payment schedules, fiscal-host fee structures with their dates and one recent structural change, fund-access timing, and the jurisdictional tax contrasts as examples routed to counsel.
- [references/budget-failure-case-studies.md](references/budget-failure-case-studies.md) - five real events read for their financial mechanism rather than their headline cause, and what each one implies for a line in this model.

See also, same collection:

- `samber/dev-event-organizer-skills@event-first-edition` - sequences when the three tiers get chosen for a first edition.
- `samber/dev-event-organizer-skills@corporate-event-strategy` - at the company-run pole, decides who owns the funding line and what it is funded to accomplish; this skill models the money that ownership already settled and never picks the owner.
- `samber/dev-event-organizer-skills@event-format-selection` - decides whether program inventory may be sold as a funding source at all.
- `samber/dev-event-organizer-skills@hackathon-cash-prize` - sizes a prize pool inside the Prizes line this skill sets.
