---
name: event-sponsor-pricing
description: Build the sponsorship rate card for a technical event - the revenue target taken from the budget, an inventory of sellable surfaces, cost-recovery, market-comp and value-based price setting, a 2-4 tier ladder with anchoring and a sane top-to-floor ratio, add-on and exclusivity premiums, in-kind valuation, and the discount and negotiation policy written before the first sponsor call. Use whenever the user mentions sponsorship tier prices, a sponsor rate card, sponsor package pricing, or choosing between a published ladder, quote-gated pricing and no ladder at all - even if they never say "pricing". Do NOT use for attendee ticket prices - use samber/dev-event-organizer-skills@event-ticket-pricing; the deck is samber/dev-event-organizer-skills@event-sponsor-prospectus.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Sponsor Pricing

You price event sponsorship: the rate card - how many tiers, at what ratios, which add-ons, which premiums, which discounts, and what the organizer will and won't negotiate.

Upstream, `samber/dev-event-organizer-skills@event-sponsor-value-proposition` has articulated what each tier's price buys; value claims justify the rate card, never the reverse. `samber/dev-event-organizer-skills@event-budget` owns the revenue target the card must hit. Downstream, `samber/dev-event-organizer-skills@event-sponsor-prospectus` presents the ladder and `samber/dev-event-organizer-skills@event-sponsor-outreach` sells it.

You set numbers and policy. You do not:

- Build the deck
- Run the sale
- Draft the contract
- Price attendee tickets

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank all three menus against what you know about this organizer - any of the following overturns a default rung:

- A sold-out prior edition
- A multi-event portfolio
- A volunteer team with no sales capacity
- A free-to-attend funding model

Menu axis lines carry no currency amounts: ratios and orders of magnitude only. The real dollar ladders live in [references/published-rate-ladders.md](references/published-rate-ladders.md), each next to the event that published it. Treat them as anchors to transpose by ratio, never figures to copy across scale or market.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-payoff, durability, and effort - the defaults cannot be picked for the user.

1. Which pole does the event sit on: community-run (independent, CFP-driven, sponsors as cost recovery) or vendor/foundation-run (marketing budget, purchasable stage time and exclusivity)? This bounds the sellable inventory before anything gets a price.
2. Is this a single event or one edition of a portfolio the same organizer runs? Is the event free-to-attend by design? (A portfolio unlocks bundling; a free event collapses the price-setting sequence - see the method menu.)
3. Does a budget exist - total expenses and the sponsorship share it assigns? If not, stop and run `samber/dev-event-organizer-skills@event-budget` first; a rate card without a target under-prices tier by tier.
4. What capacity constrains the card: venue floor space (booth/table count), attendee count, stage minutes the program policy allows to be sold, and how prior editions' tiers actually filled or sold out?
5. Which comparable events' rate cards are in hand - same community, same region, same scale? Numbers with dates, not memories of numbers.
6. When must sponsorship revenue close? Sponsors sign roughly a fiscal quarter ahead of the event; a near deadline promotes the early-bird rung and a shorter, simpler ladder over segmentation.
7. Is this card a one-off raise or a compounding multi-edition asset? A compounding mandate promotes card integrity - the no-off-card-discount policy and scarcity-based repricing - over closing any single deal.
8. What is the selling-effort ceiling: organizer hours, anyone with sales experience, appetite for per-deal negotiation? A volunteer team with no sales capacity deletes the quote-gated rung outright.

## Published ladder, quote-gated, or no ladder at all

The axis that changes the pricing work is disclosure architecture, and all three patterns are sourced, legitimate, and mutually exclusive:

- **Published ladder** - fixed tiers and prices on a public page or prospectus. The pattern appears at both community and foundation scale.
- **Quote-gated** - reach numbers published, prices per conversation. The clearest case is a network selling annual portfolio access to sophisticated repeat buyers, not a single event.
- **No ladder by design** - a free-to-attend, donation/exhibitor-funded event never depended on tiered sponsorship; a flat stand fee plus donations is its whole card. This is a funding-model choice made at the budget/format level, not a pricing failure.

The community-run vs vendor-run pole this collection usually branches on still bounds _inventory_ - purchasable stage time and category exclusivity exist only at the vendor/foundation pole - but it does not pick the architecture: community and foundation events alike publish ladders. Say which architecture and which pole the card assumes.

## Workflow

1. Run the interview; fix the pole, the architecture, and the constraints.
2. **Fix the total first.** Sum the budget's expense lines and multiply by the sponsorship share: 75-80%+ of budget at community-conference scale (organizer guide's own target), effectively 100% for a free hackathon with no ticket line. This is the sum the whole card must raise - never a number to split evenly across tiers.
3. **Inventory the sellable surfaces**:
   - Booth/table slots the floor supports
   - Ticket allotments (a real, subtractable cost component, never free swag)
   - Stage minutes, if the pole allows selling any
   - Branding prominence
   - Named branded surfaces (lanyards, coffee, lunch, transcription, evening event)
   - Track or category exclusivity (vendor/foundation pole only)

   Delete from inventory now whatever the program policy forbids selling.

4. **Choose the price-setting sequence** from the method menu below: cost-recovery fixes the total, market comps band each tier, value-based allocates within the band.
5. **Design the ladder** from the architecture menu below:
   - Tier count and top:floor ratio
   - Feature-gating on the four physical axes: tickets, floor presence, stage time, branding prominence (gated identically across every published ladder)
   - Anchoring: present the top tier first, make the middle tier the visibly best value
   - An optional permanently-free community tier for non-commercial local orgs (a reserved category, not a freemium funnel)
   - The booth price floor: floor presence starts at a hard tier, with no cheap route in beneath it (consistent across sourced prospectuses)
6. **Price add-ons independently of the ladder.** A named branded surface may legitimately out-price a mid tier, at community and foundation scale alike. It cannibalizes only when it re-sells a tier's core gated benefit - floor presence, stage time - for less; price such an add-on above the cheapest tier that includes the benefit, or don't sell it. Keep one or two "contact us" lines for custom or sold-out slots.
7. **Price exclusivity premiums** (vendor/foundation pole only): a track or category lead slot prices above the general ladder - published instances sit multiples above the top general tier, not add-on money - with a hard cap on count. At the community pole, the program policy rules these out: delete the line, don't park it.
8. **Value in-kind sponsorship** with the framework in [references/in-kind-and-negotiation-policy.md](references/in-kind-and-negotiation-policy.md): an in-kind deal is worth the budget line it displaces, never the donor's stated retail value, and buys tier placement at that displaced-cost value.
9. **Write the negotiation and discount policy before the first call**, from the same reference:
   - What is negotiable: payment schedule, equal-value benefit swaps, bundling add-ons into a tier
   - What never is: published tier prices, anything the program policy forbids
   - Who can approve a deviation, and at what floor
   - A log of every deviation granted

   One leaked off-card discount reprices next year's whole ladder.

10. **Set the calendar**: signing deadline about a quarter out to match sponsor fiscal lock-in, an early-bird date if the discount menu picked one, and add-on purchase cutoffs. Validate the card with the user section by section - total, ladder, add-ons, policy - then hand off to `samber/dev-event-organizer-skills@event-sponsor-prospectus`.

If your harness has persistent memory, record: the revenue target and the share math behind it, the final card, each deviation granted and its reason, and every sellout or unsold tier. Next edition's repricing starts from that record instead of a blank sheet.

## Price-setting method

How the numbers get set. Ranking (default, not a law - re-rank against Q2 and Q5-Q8):

- effort (data gathering + analysis to run it): `value-based > market-comp > cost-recovery`
- value (how much of sponsors' willingness-to-pay the number captures): `value-based > market-comp > cost-recovery`
- efficiency: `cost-recovery > market-comp > value-based`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks every pair: the method that captures more willingness-to-pay costs strictly more to run.

No third axis is printed to block or rescue a pair. The check catches nothing; the ordering rests on the argument below.

These are sequenced, not exclusive - organizer practice runs the first for the sum and the last for the allocation:

- **Cost-recovery** - the default first move: budget total × sponsorship share fixes what the card must raise. Near-zero effort when the budget exists (Q3). It sets the floor and the total, never each tier's price - a target split evenly across tiers ignores what each tier delivers.
- **Market-comp** - move up once the total is fixed: comparable events' published cards band each tier. This is the practical substitute for willingness-to-pay survey research, which needs a respondent pool no single event's sponsor market has. Comps transpose as ratios, not dollars.
- **Value-based** - the starved option: tops the value axis and the effort axis, so efficiency never leads with it. It allocates within the total - a tier's price tracks audience size and quality and the value categories the upstream proposition actually claims. Promotion condition: premium inventory no comparable publishes a price for (a track exclusivity, a novel activation), or a sold-out prior edition proving the comp band sits below real demand.

For a free-to-attend event (Q2), the sequence collapses to cost-recovery: the total is a fundraising target divided across tiers, and value-based work decides which sponsor gets which tier, not where prices sit.

## Ladder architecture

Tier count, ratio, and disclosure. Ranking (default, not a law - re-rank against Q2, Q6, Q8):

- effort (building the card + per-deal selling it demands): `quote-gated > 4-tier > 3-tier > 2-tier > no-ladder-by-design`
- value (revenue captured + sponsor self-selection): `quote-gated > 3-tier == 4-tier > 2-tier > no-ladder-by-design`
- efficiency: `3-tier > 2-tier > 4-tier > no-ladder-by-design > quote-gated`

The `==` is argued. A fourth tier adds a real segment: published ladders' startup and community tiers are persona tiers with lighter benefits, not just a lower price. But a fourth tier re-introduces the decision paralysis three tiers exist to avoid, and the sourced community ladders split between three and four with three modal.

The segmentation gain and the choice cost roughly cancel.

- **Published 3-tier** - the default. Top:floor ratio runs 3-5:1: the modal ratio across seven independent community ladders is 2:1 to 7.5:1, most near 4-5:1, and the best-tier rule says 2-3x. Community sponsorship runs hotter than that best-tier rule because the floor tier is near-zero marginal cost to the organizer - report the range, not one number. Move up to 4 tiers only when a genuinely distinct sponsor persona exists, never to fill a price gap.
- **Published 2-tier** - a minimal card (a persona tier plus one full tier); fits a near deadline (Q6) and a small team, at the cost of segmentation.
- **Quote-gated** - the starved option: tops value (per-deal price discrimination) and tops effort (every sponsor is a negotiation). Promotion condition: portfolio/network scale - selling annual reach across many events to sophisticated repeat buyers, which is the only sourced case. For a single event sold by a volunteer team (Q8), delete this rung - don't demote it: at that scale "contact us for pricing" stalls every deal behind organizer availability and reads as having something to hide.
- **No-ladder-by-design** - an argued legitimate rung, not a fallback: right exactly when the funding model is donations plus flat exhibitor fees for a free event. It is chosen with `samber/dev-event-organizer-skills@event-budget`, not at pricing time.

## Discount mechanics

What may reduce a published price. Ranking (default, not a law - re-rank against Q2, Q6, Q7):

- effort (contract mechanics + portfolio coordination): `multi-event bundling > negotiated case-by-case > early-bird deadline`
- value (commitments locked or pulled forward): `multi-event bundling > early-bird deadline > negotiated case-by-case`
- efficiency: `early-bird deadline > multi-event bundling > negotiated case-by-case`

- **Early-bird deadline** - the default: one calendar-deadline price on the top tier only, dated to catch sponsors' fiscal lock-in about a quarter out (the one published community-scale early-bird works exactly this way: a date, not a percentage-off banner). A date on the card that pulls the largest deals forward for near-zero effort.
- **Multi-event bundling** - the starved option. It tops value: it locks a multi-event commitment at a small fixed published rate, the closest published structured discount mechanic being a 3/5/8% step for one, two, three-plus events at foundation scale. It also tops effort: it requires a real portfolio and the contract mechanics to honor it. Promotion condition: the organizer actually runs two or more events under one banner (Q2).
- **Negotiated case-by-case** - allowed only inside the written policy of workflow step 9, logged per deal. Without the policy, delete the rung.
- **Year-over-year returning-sponsor discount** - deleted, not ranked: it stays off the card at community and foundation scale alike. The renewal lever is the post-event ROI report and the relationship - that work belongs to `samber/dev-event-organizer-skills@event-sponsor-fulfillment`, not to a rate cut that compounds into a permanently discounted anchor sponsor.

## Failure modes

- **Building tiers before fixing the total.** Each tier looks reasonable next to a comp while the ladder sums below the budget target. Total first, allocation second.
- **Splitting the target evenly across tiers.** Cost-recovery sets the sum, not the shape; allocation is value work.
- **Copying a vendor-scale ladder - or its dollar figures - at community scale.** A foundation card's booth floor can sit above a community event's entire target. Transpose ratios (top:floor, add-on:mid-tier), never prices; the reference file keeps each dollar figure next to the event it came from.
- **Add-ons cannibalizing mid tiers.** A branded surface legitimately out-pricing a mid tier is published practice and fine; an add-on re-selling floor presence or stage time below the tier that gates it hollows the ladder out.
- **Unpriced in-kind.** A donation accepted without a written displaced-cost value distorts the budget and hands out tier placement for free - and retail-value framing inflates the donor's tier by the donor's own margin.
- **Discounting without a written policy.** The first exception becomes the market price; sponsors talk to each other.
- **Passes treated as free swag.** A tier's ticket allotment is a subtractable cost component (published prospectuses value each pass individually); ignoring it under-prices exactly the tiers that carry the most passes.
- **Ladder creep past four tiers.** A fifth tier is a price gap wearing a persona costume.
- **Deleting a sold-out surface from the public card.** The published pattern strikes it through and leaves it visible - live scarcity plus social proof - and a sellout is next edition's repricing signal, not a cleanup task.

## Measurement

Rate-card design cannot be measured against an industry pass rate, so never invent one. What is observable is self-set - pick 2-3 and write down, before outreach starts, the repricing each would trigger:

- **Target coverage by lock-in date**: share of the revenue target signed by roughly a quarter out. Behind pace reads as a price, ladder, or pipeline problem - split it with `samber/dev-event-organizer-skills@event-sponsor-outreach` before touching the card.
- **Tier fill pattern**: the top tier selling out first and fast means it was under-priced - raise it next edition. The floor filling while the middle sits empty means the middle step-up buys no visible value.
- **Add-on sellouts**: each one is a signal to price that surface higher next edition, never lower.
- **Deviation log frequency**: every off-card concession recorded per workflow step 9; a rising rate means the card is mispriced or the policy is too loose - decide which before the next deal, not after.

## Invocation examples

- "Our 300-person community DevOps conference needs sponsor pricing - budget is done, value prop is written, give me the rate card."
- "Should our hackathon publish sponsorship prices or make sponsors ask? We're three volunteers."
- "A sponsor wants to pay half in cloud credits and half in cash - what's that worth against our Gold tier?"
- "Our top tier sold out in two weeks and the middle tier hasn't moved. Fix the ladder for next year."

Expected output: a rate card, presented section by section for validation, every number labeled by the method that set it.

- Revenue target with its share math
- Tier ladder with per-tier gated benefits and ratios
- Add-on and exclusivity price list
- In-kind valuation terms
- Discount and negotiation policy with deadlines

## References

- [references/published-rate-ladders.md](references/published-rate-ladders.md) - the real dollar ladders, each kept next to the event it came from: seven community-conference city ladders with ratios, foundation-scale tier and exclusivity prices, add-on prices at both scales, the bundling percentages, and the quote-gated and no-ladder contrast cases, plus how to transpose them by ratio.
- [references/ladder-design-mechanics.md](references/ladder-design-mechanics.md) - tier-count and ratio guidance with the community-vs-SaaS caveat, anchoring and decoy placement, the feature-gating map from software levers to physical scarcity, persona tiers, the booth price floor, custom-pricing triggers, scarcity mechanics, deadline structure, and what from SaaS pricing does not transpose.
- [references/in-kind-and-negotiation-policy.md](references/in-kind-and-negotiation-policy.md) - the in-kind valuation framework and the negotiation/discount policy worksheet, both self-set.

See also, same collection:

- `samber/dev-event-organizer-skills@event-sponsor-value-proposition` - articulates what each tier's price buys; run it first, since its claims justify this card.
- `samber/dev-event-organizer-skills@event-sponsor-prospectus` - presents this ladder as a document; it inherits the card, never edits it.
- `samber/dev-event-organizer-skills@event-sponsor-outreach` - sells the card and feeds objections and deviation requests back into the log.
- `samber/dev-event-organizer-skills@event-ticket-pricing` - the attendee side of the revenue mix; the two targets must reconcile in the budget.
- `samber/dev-event-organizer-skills@event-budget` - owns the expense total and revenue mix the card's target comes from.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - owns the renewal lever this skill's deleted discount rung defers to.
