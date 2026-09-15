---
name: event-ticket-pricing
description: Set attendee ticket prices for a technical event - free, nominal or priced against the funding model, comps subtracted from capacity, a ladder split by who pays (employer-funded, self-funded, student), gating on a date or a ticket count, the need-gated scholarship rung, group and invoicing mechanics, and the refund and transfer policy written before tickets go on sale. Use whenever the user mentions ticket prices, early-bird tiers, free versus paid entry, student, diversity or group rates, invoicing an employer, or a ticket refund policy - even if they never say "pricing". Do NOT use for sponsor tiers - use samber/dev-event-organizer-skills@event-sponsor-pricing; no-shows are samber/dev-event-organizer-skills@event-no-show-management.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Ticket Pricing

You price attendee tickets. This covers:

- whether to charge at all
- how many public price points
- which personas get their own price
- what gates a discount
- who gets in for free or nearly free
- what happens when someone asks for their money back

`samber/dev-event-organizer-skills@event-budget` owns the revenue target this ladder has to hit upstream, and `samber/dev-event-organizer-skills@event-sponsor-pricing` owns the sponsorship share that cross-subsidizes it. You set attendee numbers and policy. You do not:

- build the budget
- price sponsor tiers
- run acquisition campaigns
- design no-show mechanics

Every ranking below is a default, not a law. It shifts with context and with who executes it.

After the interview, re-rank all three menus against signals like these:

- an event that already sells out
- a free-to-attend funding model decided upstream
- a volunteer team with no accounting capacity
- an audience that is overwhelmingly self-funding

Each one overturns a default rung. Axis lines carry no currency amounts.

The real published prices, each with its event and date, live in [references/published-ticket-ladders.md](references/published-ticket-ladders.md). Treat them as ratios to transpose, never as figures to copy across scale, market, or year.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the defaults cannot be picked for the user.

1. Does a budget exist, with a total expense figure and the share it assigns to ticket revenue? If not, stop and run `samber/dev-event-organizer-skills@event-budget` first - a ladder built without a target under-prices tier by tier.
2. Who pays for a ticket in this audience: an employer's training or travel budget, the attendee's own wallet, or a mix? Ask for the rough split. This decides the ladder's shape before any number.
3. What is the room's paid capacity, and how many seats are already committed as comps - sponsor allotments per their signed tiers, speakers, organizers, volunteers? Comps come off capacity before pricing, not after.
4. Is the event free to attend by design, or is charging genuinely open? A free-to-attend funding model is a budget decision, not a pricing one - say which was already made and by whom.
5. Which comparable events' registration pages are in hand - same community, same region, same scale, with the date you read them? Numbers with dates, not memories of numbers.
6. When must ticket revenue land? A hard date promotes date-gated mechanics and a shorter ladder. No deadline pressure leaves room for the slower access rungs.
7. Is this a one-off edition or one year of a recurring event? A recurring event promotes price stability and a published community-price commitment over squeezing this edition.
8. What is the effort ceiling - organizer hours during the sale, anyone who can review applications, an entity that can issue invoices and handle tax? An organizer with no invoicing capacity deletes the invoice rung outright.
9. Who runs the event: an independent community group, or a vendor or company?
10. Is accessibility a stated positioning claim the event has to be able to defend?

## Who pays for the ticket

The axis that changes the pricing work is who pays for the ticket:

- an employer's budget
- the attendee's own money
- an institution's

Every sourced published ladder encodes this split, under different label words: corporate/individual/student at one conference, business/personal/education at another. Ask Q2 and say which mix the ladder assumes.

The community-run versus vendor-run pole this collection branches on elsewhere still bounds the _price band_ - a vendor conference charging against marketing budgets sits an order of magnitude above a community event - but it does not pick the ladder's shape. Community and vendor events alike split by payer.

## Free, nominal, or priced

The posture decision, made against the funding model, before any ladder exists. Ranking (default, not a law - re-rank against Q1, Q4, Q7):

- effort (price-setting work plus the per-order handling each posture demands during the sale): `commercial price > community price > nominal fee > free-by-design`
- value (budget covered plus headcount certainty bought against committed venue and catering spend): `commercial price > community price > nominal fee > free-by-design`
- compliance cost (what charging obliges the organizer to register and declare, and how reversible the posture stays once prices are public): `commercial price == community price == nominal fee > free-by-design`
- efficiency: `nominal fee > community price > commercial price`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations.** Clean only by construction, and by-construction is never a pass.

- Value and effort share one blocking mechanism: the posture that covers more budget costs strictly more price-setting and per-order handling.
- That same mechanism blocks the three pairs against free-by-design too, since free-by-design loses on value rather than winning anything for free.
- The compliance axis ties the three priced postures, so it cannot rescue a pair: the effort half is already lost in every one.

The check catches nothing here. The efficiency line rests on the arguments below.

The three priced postures tie on compliance cost because the obligation is triggered by charging at all, not by the amount: any non-zero price pulls in accounting and tax handling, and a cross-border sale can require registering in another jurisdiction. Free-by-design sits at the floor as the only posture raising no tax, invoicing, or refund obligation, and the only one that stays reversible - a published price cannot be withdrawn mid-sale without refunding whoever already paid.

Free-by-design is deliberately absent from the efficiency line: a ratio of revenue to effort is false precision on a posture that raises no ticket revenue by construction. It is chosen upstream on funding-model grounds, not won on efficiency.

- **Nominal fee** - the efficiency default: a token price, roughly a tenth to a fifth of what a commercial tech conference in the same region charges (one organizer guide's own published rule). Its job is not funding but risk-spreading: a paid registration converts an unpaid RSVP into a headcount you can commit catering and venue capacity against. It buys most of that certainty for a fraction of the pricing work, which is what puts it first on efficiency - but it carries the full compliance cost of any priced posture, so it is never the free option it looks like.
- **Community price** - the default once ticket revenue has a real job in the budget: priced to cover per-attendee cost with sponsorship carrying the bulk of the budget (the published community-conference target is 75-80%+ from sponsorship). Pairs with an explicit, publicly stated community-price commitment on a recurring event (one large conference held individual and corporate prices flat across venue step-ups while cutting its student price by more than 40% over five years, funded by sponsorship cross-subsidy).
- **Commercial price** - the starved option: tops value and tops effort, so efficiency never leads with it. It requires a program, a brand, and an audience buying on an employer's budget, plus the sales and refund machinery that comes with real money. **Promotion condition, keyed to Q9**: a vendor or company-run event priced against marketing budgets, or a community event that sold out fast at the community price with demand visibly unmet - a read owned by `samber/dev-event-organizer-skills@event-market-fit`, not re-derived here.
- **Free-by-design** - an argued legitimate posture, not a failure to price: a full multi-track conference can be free to attend with no registration at all, funded entirely by sponsorship and merchandise (one such conference states plainly that there is no ticket and no registration step). Once this is the funding model, every rung in the next menu collapses to nothing. Free tickets also carry a consequence this skill does not solve - the no-show rate on a seat nobody paid for. Hand it to `samber/dev-event-organizer-skills@event-no-show-management` rather than answering it with a price.

If the format has no ticket-revenue line at all - a free hackathon, where sponsorship is close to 100% of funding by construction rather than by target, delete the priced postures rather than ranking them, and return to `samber/dev-event-organizer-skills@event-budget`.

## Access architecture

Three disclosure rungs appear on real registration pages, and they are complementary, not competing - real events combine two or three. Ranking (default, not a law - re-rank against Q2, Q6, Q8):

- effort (setup, plus the standing work each demands during the sale): `discretionary scholarship > published persona tier > date-or-volume gate`
- value (revenue captured plus attendees reached who otherwise could not come): `published persona tier > discretionary scholarship > date-or-volume gate`
- efficiency: `published persona tier > date-or-volume gate > discretionary scholarship`

- **Published persona tier** - the default and the largest single lever: a fixed price per payer type, listed publicly, bought self-service with no application. Published top-to-floor ratios run roughly 1.7:1 to 6.5:1 across the two events with full ladders - report the range, never one number, and transpose the ratio rather than the amount. The only gate is self-identification, sometimes an institutional email check.
- **Date-or-volume gate** - near-zero effort, configured once: either a calendar date that moves the price, or a first-N-tickets allocation. Three mechanics are all real - a date that ends an early price, a date that adds a late surcharge on top of the regular price, and a volume-gated early-bird capped at a ticket count. Its second payoff is a forecasting checkpoint the sale can be read against, which belongs to `samber/dev-event-organizer-skills@event-market-fit`; react to that read here, do not re-derive it.
- **Discretionary scholarship** - the starved option: tops effort (every application is read and answered by a human) and carries real access value that no fixed category definition reaches - the unemployed, career-changers, and anyone in hardship who is not a student. Practice gates it behind an email or a form, reviewed by organizers, and frequently leaves the price unpublished; the most developed version runs a scored reviewer panel against a stated eligibility list and an application window. **Promotion condition, keyed to Q8 or Q10**: the organizer can staff the review, or accessibility is a stated positioning claim the event has to be able to defend. Never present it as free - it is organizer labor a published tier does not cost.

On a free-by-design event, delete all three rather than ranking them. Design details, application copy, and worked examples for each rung are in [references/access-rungs-and-group-mechanics.md](references/access-rungs-and-group-mechanics.md).

## Bulk and cross-subsidy mechanics

What sits on top of the ladder once its shape is fixed. Ranking (default, not a law - re-rank against Q2, Q8):

- effort (setup plus per-order handling during the sale): `supporter tier > pay-by-invoice rail > flat group discount`
- value (orders unlocked or enlarged, and programs funded): `pay-by-invoice rail > flat group discount > supporter tier`
- efficiency: `flat group discount > pay-by-invoice rail > supporter tier`

- **Flat group discount** - the default: one published percentage off for a minimum head count in a single order, self-service, no approval step (one community event gives 15% off for five or more in one order; a larger conference steps 5% for five to nine and 10% for ten or more, and applies it only to its standard tier, never stacked on the early or late tiers). Copy that exclusion: a group discount stacked on an early-bird price discounts the same seat twice.
- **Pay-by-invoice rail** - highest value, because it unlocks orders that otherwise never happen: a company that cannot pay via a card checkout buys nothing at all. It is not a discount and must never be described as one (published practice offers invoicing on request for bulk corporate orders at full price). It costs real per-order handling and requires an entity that can invoice. Delete this rung outright when the organizer has no such capacity - an event that cannot process money in the required form has a payment-handling problem, not a pricing one, and that belongs upstream.
- **Supporter tier** - the starved option: a voluntary pay-more ticket whose premium visibly funds accessibility for others (one conference priced a supporter ticket at a premium explicitly to fund its scholars program). Uptake is small, so the cash value is modest against the effort of running the program it funds. Promotion condition: a named scholarship or aid program already exists for the tier to point at, which makes it a positioning asset as much as a revenue line.

Sponsorship cross-subsidy is the other real way accessibility gets funded, but it is set in `samber/dev-event-organizer-skills@event-sponsor-pricing`, not here - this skill only spends what that ladder raised.

## Workflow

1. Run the interview. Fix the payer mix, the posture, the capacity, and the constraints.
2. **Take the revenue target from the budget, never from the ladder.** Total expenses minus the sponsorship share is what tickets must raise. If that number does not exist yet, stop and run `samber/dev-event-organizer-skills@event-budget`.
3. **Subtract comps from capacity before pricing.** Count the actual committed seats - sponsor allotments from their signed tiers, speakers, organizers, volunteers - and price against the paid seats that remain (published checkpoint math is expressed as expected sales _minus_ those comps). No budgeting rule sets comps as a percentage of capacity; count them from the agreements you hold and say so, rather than adopting a fabricated ratio.
4. **Pick the posture** from the free/nominal/priced menu. Say which funding model it assumes and which upstream decision fixed it.
5. **Design the persona ladder**: pick the payer types from Q2 and set the ratios, carrying across the published ranges from the reference rather than copying prices. Keep the public price points to two per persona at most, since no published event runs more than two public price points in its time ladder.
6. **Set the date or volume gate**: one announced step, dated on the calendar and published from the day tickets go on sale. Decide explicitly whether the step is a discount that expires or a surcharge that lands, since the sourced events do both, and never announce a price increase the buyer could not have seen coming.
7. **Add the access rungs** the architecture menu selected - a published student or education price, a discretionary scholarship route, or both. Write the application mechanic and the reviewer before publishing the route, not after the first request arrives.
8. **Layer the bulk mechanics**: the group threshold and percentage, which tiers it may stack on, and whether invoicing is offered.
9. **Write the refund and transfer policy before the first ticket sells.** Fix a refund deadline, whether an administrative fee is retained and whether it is waived for hardship categories, and whether tickets transfer to another person, to another company, or not at all. Four events' policies are sourced in [references/refund-and-transfer-policy.md](references/refund-and-transfer-policy.md) - treat that reference as four worked examples plus a decision checklist, never as an industry norm beyond the one point they share (a single dated cutoff, not a graduated schedule), and make the organizer decide every other line rather than inheriting a default nobody chose.
10. **Publish the whole structure at once**: every price, every date, every gate. Validate it with the user, section by section:
    - target
    - ladder
    - gates
    - access rungs
    - bulk mechanics
    - refund policy

    Then hand acquisition to `samber/dev-event-organizer-skills@event-marketing-plan`.

If your harness has persistent memory, record:

- the revenue target and the arithmetic behind it
- the final ladder with its ratios
- the gate dates
- the refund policy as published
- how each tier actually sold, after the event

Next edition's pricing starts from that record instead of a blank page.

## What not to invent

Say these out loud when the question comes up rather than inventing an answer:

- **Refund, transfer, and cancellation norms** have no industry standard for community technical events beyond a single dated cutoff, which all four sourced events share. Present the four worked policies in the reference as examples, not as a standard, on every other term (fee, hardship handling, transferability).
- **Regional and currency price parity** for a format run in several countries has no established method. Say so and let the organizer decide.
- **Comp allocation as a percentage of capacity** has no budgeting rule behind it. Count committed comps from the agreements instead.
- **Deposit-hold tickets** - charging a refundable deposit returned on attendance - remain untested as a developer-event pricing lever specifically. One cross-industry data point exists (Eventtia's 2024 managed-conference data: a $3 refundable deposit cut a previously-free event's no-show rate from 38% to 14%), general-conference rather than developer-event evidence. If the organizer raises them, treat it as an idea with adjacent-industry support and route the underlying no-show concern to `samber/dev-event-organizer-skills@event-no-show-management`.

## Failure modes

- **Building the ladder before the budget target exists.** Each price looks reasonable against a comp while the ladder sums below what the event needs. Target first, allocation second.
- **More than two public price points per persona.** A third phase only works as a late surcharge, never as a third discount step. Extra steps read as pressure tactics and make every buyer wait for the next one.
- **Publishing the scholarship as a priced tier.** A need-gated ticket is application-reviewed and often unpriced on purpose; listing it as a cheap public tier turns a reviewed decision into a self-service checkbox and invites exactly the buyers it was not for.
- **Inventing a refund policy instead of deciding one.** A policy inherited from a template nobody read is discovered by the first person who asks for their money back, in public. Decide the deadline, the fee, the hardship waiver, and the transfer rule explicitly.
- **Copying a vendor-conference price at community scale.** A commercial conference's ticket can exceed a community event's entire ticket-revenue target. Transpose ratios - top-to-floor, group percentages - never amounts.
- **Free tickets bought and not used.** Pricing does not fix no-shows; a nominal fee reduces the exposure but does not solve it. Route to `samber/dev-event-organizer-skills@event-no-show-management`.
- **Calling the invoice rail a discount.** It changes the payment method, not the price. Discounting it too hands corporate buyers - the segment paying the top price - a second reduction for a problem that was never about money.
- **Stacking the group discount on an early-bird price.** Standard practice excludes the early and late tiers from group discounts precisely to stop the same seat being discounted twice.
- **Reading a slow sale as a pricing failure by default.** Slow sales can be demand, marketing execution, or price. `samber/dev-event-organizer-skills@event-market-fit` separates the three; act on the pricing side only once it has.

## Measurement

Ticket-ladder design has no industry benchmark to score against, so everything observable here is self-set - pick two or three, and write down before tickets go on sale what each would change:

- **Paid share of the revenue target by the gate date** (self-set): what portion of the ticket target is banked when the early price ends. Behind pace is a price, demand, or marketing question - split it with `samber/dev-event-organizer-skills@event-market-fit` before touching a price.
- **Persona mix against plan** (self-set): if the employer-funded tier sells far below its expected share, either the ladder guessed the payer mix wrong (Q2) or the corporate price is above what those budgets approve without a sign-off.
- **Discount and rung uptake** (self-set): group orders, scholarship applications received versus granted, supporter tickets sold. A scholarship route drawing far more applications than it can fund is a budget conversation for next edition, not a reason to quietly stop answering.
- **Refund and transfer request volume against the deadline** (self-set): a spike right before the deadline says the deadline is doing its job; a steady stream after it says the policy is being litigated case by case and needs rewriting, not enforcing.

## Invocation examples

- "Our 300-person community DevOps conference charges nothing today and we are eating the catering risk - what should tickets cost?"
- "Give me the tier ladder for a two-day Python conference: corporate, individual, and student, with an early-bird date."
- "Someone asked for a refund three weeks before our event and we never wrote a policy. What should it say, and what do we do now?"
- "We want to offer free tickets to people who cannot afford one without turning it into a public discount code."

Expected output: a ticket structure, presented section by section for validation, every number labeled sourced or self-set:

- the revenue target with the arithmetic behind it
- paid capacity after comps
- the posture and why
- the persona ladder with its ratios and the gate dates
- the access rungs with their application mechanic
- the bulk mechanics with their stacking rule
- the refund and transfer policy in publishable words

## References

- [references/published-ticket-ladders.md](references/published-ticket-ladders.md) - the real published prices with their events, dates, and sources: two full persona ladders with computed ratios, the three gating mechanics, the group-discount percentages and thresholds, the supporter tier, the free-by-design case, and how to transpose any of them by ratio.
- [references/access-rungs-and-group-mechanics.md](references/access-rungs-and-group-mechanics.md) - the three-rung disclosure architecture in detail: published persona tiers versus discretionary need-gated tickets, the sourced application mechanics from an email request to a scored reviewer panel, eligibility framing, and the group-order and invoicing mechanics with their exclusions.
- [references/refund-and-transfer-policy.md](references/refund-and-transfer-policy.md): four real refund and transfer policies in full, and a decision checklist for writing one, labeled throughout as four examples rather than a norm.

See also, same collection:

- `samber/dev-event-organizer-skills@event-budget` - owns the revenue target this ladder must hit and the free-versus-paid funding decision; run it first.
- `samber/dev-event-organizer-skills@event-sponsor-pricing` - the sponsorship rate card, including the share that cross-subsidizes attendee prices; the mirror of this skill on the sponsor side.
- `samber/dev-event-organizer-skills@event-market-fit` - owns sellout speed, the sales curve, and whether slow sales are demand, marketing, or price; react to its read here, never re-derive it.
- `samber/dev-event-organizer-skills@event-marketing-plan` - runs the campaigns that sell the tickets this skill priced.
- `samber/dev-event-organizer-skills@event-no-show-management` - owns what happens to seats that were bought cheap or free and never used.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - mirrors the need-gated rung this skill owns and covers what attending costs _beyond_ the ticket (childcare, travel and registration grants). It defers the application mechanic and the reviewer to this skill rather than building a second one.
