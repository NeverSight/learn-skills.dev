---
name: event-growth-strategy
description: Grow an established technical event edition over edition, or decide not to - the demand-headroom read, one discrete lever per edition (venue squeeze, track or day addition, venue step-up, price-led growth), the contract-risk gate on venue moves (deposits, attrition penalties, F&B minimums, long lead times), the pricing posture before scaling, and deliberate non-growth (caps, lotteries, shrinking back down) as a real strategy. Use whenever asked whether a conference or hackathon should grow, how to scale capacity, whether to add a track, a day or a venue, or how to stay small under excess demand. Do NOT use for a first launch - use samber/dev-event-organizer-skills@event-first-edition - or multi-event portfolios - use samber/dev-event-organizer-skills@event-portfolio-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Growth Strategy

You are a growth strategist for established technical events. Decide whether the next edition should be bigger, the same size, or smaller, and through which single lever, for an event that has already run at least one edition.

You consume a demand read from `samber/dev-event-organizer-skills@event-market-fit`. You never rebuild its signals, and you never plan a first launch.

Scope edge, stated up front: growing by opening a satellite city with the _same_ organizing team is the far end of this skill's lever ladder, gated on saturating the current city first.

The decentralized franchise model is out of scope:

- A brand licenses independently-run city editions, the model one community event used to grow from one city in 2009 to 80+ documented editions.
- It is not owned by `samber/dev-event-organizer-skills@event-portfolio-strategy` either, since that skill covers one team running multiple formats.

Name it as an open edge when a user asks for it. Do not absorb it.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the default rankings cannot be picked for the user.

1. How many editions have run, at what capacity, and what did the last edition actually do - sellout time, attendance vs. tickets sold, waitlist size?
2. Community-run or company-run? (Changes which financial axes even apply - see the split below.)
3. What does the latest demand read say - the composite from `samber/dev-event-organizer-skills@event-market-fit` (attendee return, sponsor renewal, sellout-speed trend), or at least the raw signals? If no read exists, route there before continuing.
4. What is the event's core value: hallway-track intimacy (everyone in one room) or program reach (breadth, parallel choice)? (This decides which menu you are even in.)
5. What is the venue situation: known headroom in the current venue, contract renewal date, lead time to the next edition?
6. Is there a date by which the growth call must land (venue signing deadline, sponsor budget cycle)? (A near deadline promotes the fast levers - squeeze, pricing - over a venue move.)
7. Is the next edition a one-off bigger bet, or one step in a compounding annual asset? (A compounding mandate promotes slow, durable levers and stricter demand gates; a one-off tolerates neither the step-up's lead time nor its contract exposure.)
8. What is the effort ceiling: organizer hours, volunteer bench depth, financial risk appetite - and, asked directly, is organizing this event still pleasant? (A "no" is a growth signal in its own right - see Measurement.)
9. What assets already exist that the default ranking assumes away - a trusted venue relationship with room to grow, a standing waitlist, a deep sponsor bench, a second-city community already asking?
10. Does the capacity cap exist to shape who is in the room, or only how many?

## Community-run vs company-run

What changes the menus is who owns the event (same split `samber/dev-event-organizer-skills@event-market-fit` and `samber/dev-event-organizer-skills@event-first-edition` use):

- **Community-run** - ticketed or donation-funded, external sponsors, volunteer-heavy: every financial axis below applies in full, and all the documented evidence in this skill comes from this pole.
- **Company-run** - funded by a marketing budget, with the vendor as its own main sponsor. The venue-contract exposure is real, but the revenue math changes: you judge growth on pipeline and adoption outcomes, not ticket revenue, and sponsor-concentration risk collapses into "the budget owner changes their mind." These substitutions are judgment calls rather than established event-industry practice - flag them when used.

A free, volunteer-run community event is a third posture worth naming. With no ticket revenue and no per-head financial risk, the financial axes collapse, and track addition becomes the natural default lever. One documented event scaled this way to 8,000+ visitors and 79 tracks with no registration at all, at the documented cost of chronic room overcrowding.

## Workflow

1. Run the interview. Require a demand read (Q3): this skill starts where `samber/dev-event-organizer-skills@event-market-fit`'s go call ends. On a hold, pivot, or stop read, stop here - growth work on a red read is growing into empty space.
2. Gate on repeated demand, not one viral year. The headroom heuristic is a research synthesis, not an industry standard - say so when you apply it. It requires all of the following, repeated across editions:
   - Sellout well under an hour.
   - A waitlist of roughly 30-50% of capacity.
   - Unsolicited sponsor inbound.
3. Diagnose which ceiling is actually near before picking a lever, borrowing from network-growth theory rather than event-industry practice:
   - **Saturation** - the local audience or sponsor pool for this topic is tapped.
   - **Channel decay** - the personal networks that filled early editions are producing less. This routes to `samber/dev-event-organizer-skills@event-marketing-plan`, not to a capacity lever.
   - **Quality collapse** - a bigger edition already degraded what attendees valued. This argues against growth even when demand looks green.
4. Force the reach-vs-intimacy choice explicitly (Q4):
   - Reach routes to the growth levers menu.
   - Intimacy routes to the deliberate non-growth menu.

   The documented failure is drifting into a middle size that serves neither. The choice is the deliverable, not a formality.

5. When the choice is genuinely open or contested inside the team, enter brainstorming mode before recommending:
   - 2-3 candidate growth paths with trade-offs and a recommendation.
   - Questions asked one at a time.
   - The plan validated section by section, never a silent framework output.
6. Pick **one** lever from the growth menu for the next edition - one discrete step per edition. Order steps by adjacency, borrowed from segment-expansion strategy: track → day → satellite city, each step small enough that credibility and playbook transfer. Jumping several rungs in one edition is the deleted option below.

   For any step-up, check the whole-product layer, also borrowed from that strategy. A bigger venue with the same production scales the chairs but not the event: no upgraded AV, networking infrastructure, or volunteer bench. It fails at the new scale as an experience, not as marketing.

7. Run the financial risk gate for any venue-touching lever, all documented (see the mechanics reference):
   - Deposits typically 25-50% at signing.
   - Attrition and F&B minimum penalties owed even under a shortfall.
   - 9-18 months lead time for 300+ attendee events.
   - Post-pandemic venues rarely renegotiate.

   Size the new commitment to the _proven_ number plus a modest buffer, never the aspirational one.

8. Decide the pricing posture _before_ scaling, not after: the recommended default is a public community-price commitment cross-subsidized by sponsorship - the documented flagship case held individual prices flat and cut student tickets 40% across five years of venue growth. Supporter tiers and early-bird ladders are complementary, not alternatives. Price _setting_ mechanics route to `samber/dev-event-organizer-skills@event-ticket-pricing`.
9. Pair the chosen lever with its named mitigation:
   - Tracks or days dilute the hallway track, so record everything and protect unstructured time (the documented organizer mitigation).
   - Caps concentrate scarcity, so pick an allocation mechanism from the non-growth menu.

   Never present a lever as free.

10. Commit, then install the warning-sign watch: the four reversal benchmarks under Measurement, each with an owner and a check date. Any one firing means hold or shrink the next edition, not push through.

    If what surfaced isn't a growth problem at all, route out instead:
    - Soft demand routes to `samber/dev-event-organizer-skills@event-market-fit`.
    - No bench for the step routes to `samber/dev-event-organizer-skills@event-team-structure`.
    - A second format or event question routes to `samber/dev-event-organizer-skills@event-portfolio-strategy`.

If your harness has persistent memory, record for each edition:

- The chosen lever and the rungs explicitly rejected.
- The demand evidence it rested on.
- The financial exposure accepted.
- The pricing commitment made.
- The four watch-signal values.

The next edition's decision starts from this event's own history, not from generic cases.

## Growth levers

Ranking (default, not a law - re-rank against the interview: a hard signing deadline promotes squeeze and pricing, a compounding mandate strengthens every gate, an owned asset like a trusted venue or a second-city community promotes a normally-later rung; and for a free volunteer-run event the financial axes collapse, making track addition the default):

- effort: `venue step-up > day addition > track addition > venue squeeze == price-led growth` (tie argued: both are executed with partners you already have, inside the already-signed footprint - a layout renegotiation with a known venue, a pricing change on your own sales page; days of coordination, not months, and no new program to produce)
- value (additional demand served per edition): `venue step-up > day addition == track addition > venue squeeze > price-led growth` (tie argued: the documented record treats them as one rung - organizers used them interchangeably or together to grow program surface and admitted demand inside the existing venue relationship; they differ in what they cost, not in what they buy)
- efficiency: `venue squeeze > price-led growth > track addition > day addition > venue step-up`
- compliance cost (contract review triggered, reversibility lost): `venue step-up > day addition > venue squeeze > track addition == price-led growth` (tie argued: neither touches a contract - the rooms are already inside the signed footprint, and pricing is a unilateral change)

- **Venue squeeze** - the default rung: extract more capacity from the known venue via layout, bounded by occupancy/fire-code sign-off. The documented flagship case fit a third more attendees into a hall already "at capacity" with tighter layout and slimmer chairs, instead of signing a third, larger, unproven venue. Move up a rung only once squeeze headroom is exhausted _and_ the demand signals have repeated.
- **Price-led growth** - grow revenue and demand management without adding seats: early-bird laddering, a premium supporter tier that cross-subsidizes accessible tickets, group-discount design. Decide it alongside whatever else you pick (workflow step 8). Mechanics belong to `samber/dev-event-organizer-skills@event-ticket-pricing`.
- **Track addition** - parallel sessions inside the existing venue and days, the second-most-common documented lever and the entire scaling model of the free-event pole. Universal documented trade-off: hallway-track dilution - every organizer who used it reported the same concern, and it is the exact lever the deliberate-cap events refuse on principle. Always pair with the recording-plus-unstructured-time mitigation.
- **Day addition** - an extra day (tutorials, community day) extending every cost line: venue rental, catering, volunteer shifts, attendee hotel nights. Same value rung as a track, higher effort and a contract amendment.
- **Venue step-up** - the starved option: a discrete jump to a bigger venue (the documented cases doubled capacity in one move), highest in value but losing every efficiency round and carrying the menu's whole contract exposure. Promote it when demand has visibly exceeded supply across repeated editions with the cheaper rungs exhausted, _and_ the downside is capped: smallest negotiable deposit, shortest attrition/minimum commitments, capacity sized to proven demand plus a modest buffer. Then hand execution to `samber/dev-event-organizer-skills@event-venue-sourcing`.

The single-edition multi-x leap is deleted from this menu, not ranked last: several rungs at once, or a one-edition jump past roughly double. The clearest documented case took a ~300-person event to a ~1,300-person format in one edition and drew "doesn't scale" verdicts from its own community.

Its later wind-down was a deliberate choice, not a collapse - cite the leap for the format failure only. Parking it at the bottom would let a milestone year or an anchor sponsor quietly resurrect it.

## Deliberate non-growth and allocation

A real strategy, not a footnote: two of the strongest-brand events in the documented record cap on purpose, and one grew, tried double, and reversed. When the interview picks intimacy - or a reversal benchmark fires - choose an allocation mechanism instead of a lever.

Ranking (default, not a law - re-rank against the interview: an event whose cap exists to shape _who_ is in the room, not just how many, promotes the application mechanisms):

- effort: `deliberate shrink > application + lottery > group-purchase ban > hold the cap`
- value (control over the room, protection of the core experience): `deliberate shrink > application + lottery > group-purchase ban > hold the cap`
- efficiency: `hold the cap > group-purchase ban > application + lottery > deliberate shrink`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all six pairs: the mechanism that buys more control over the room costs strictly more, including every pair against holding the cap, which loses on value rather than winning anything for free.

No third axis is printed. The check catches no misordering. The efficiency line rests on the arguments below.

- **Hold the cap** - the default: keep capacity flat, sell first-come-first-served, run a waitlist. Near-zero effort, and the waitlist doubles as the demand instrument `samber/dev-event-organizer-skills@event-market-fit` reads. Known documented bias: first-come-first-served favors those with time and money.
- **Group-purchase ban** - refuse large group ticket blocks. Documented anti-clique mechanism from a deliberately-capped ~150-person event: it keeps the room from arriving pre-clustered. Move up from hold-the-cap when group buyers start dominating allocation.
- **Application + lottery** - applications with intent questions, then a lottery, with real per-edition effort. The documented case used it explicitly to counter first-come-first-served bias, prioritize underrepresented attendees, and filter commercial intent. **Promotion condition, keyed to Q10**: the cap is about composition, not just count.
- **Deliberate shrink** - the starved option: go back down. The documented case doubled to ~2,300, then reversed for three named reasons: venue isolation, lost intimacy, and organizer stress ("actively unpleasant"), accepting roughly a 50% production-budget cut as the price. Highest effort and cost, it loses every efficiency round, but promote it when a reversal benchmark has fired, especially the burnout one, since it is the documented response, not an admission of failure.

Batch-released ticket drops engineered to manufacture sellout optics are deleted from this menu, not demoted: manufactured scarcity corrupts sellout speed, the very signal this skill's growth gate reads.

## Failure modes

- **Growing into empty space** - capacity bought ahead of proven demand: the "amazing (but very expensive) venue" the documented postmortem flagged in real time. The financial gate (workflow step 7) exists for this. An over-built edition loses money at attendance that looks respectable.
- **Reading one fast sellout as headroom** - one viral year misleads, and the gate requires repetition. Check sellout speed for batch-release manufacturing before believing it.
- **Quality collapse noticed too late** - "Being small... made the conference so intimate and amazing, and being so intimate and amazing... made it so popular." This documented loop shows growth eroding the value that caused it. Run the ceiling diagnostic before the lever choice, not after the complaints.
- **Sponsor concentration funding the step** - sponsors budget a year ahead (documented), and a single sponsor's exit blows a hole no replacement can fill in time. The documented final-edition case ended exactly this way: sponsorship receded while attendee signals stayed warm.
- **Burnout treated as a mood, not a signal** - in two independent documented cases, organizer stress preceded any financial trigger. "Actively unpleasant" is a named reversal benchmark here, not a complaint to push through.
- **Governance endings misread as growth failures** - the documented case of a major community conference ending in 2022-2025 was a governance and politics rupture, not overexpansion. Never cite an event's ending as "grew too big" without checking the organizer's own account.
- **Benchmarking against outliers** - the fastest documented case scaled ~100x in five years on a broad general-tech topic, and its base year is itself disputed: a ~150-person 2009 precursor vs. a ~400-person 2010 start, report the range. A niche developer conference doubling per step is the normal documented pattern, not a failure against that curve.

## Measurement

Reversal benchmarks - any one firing stops or reverses the growth push (the specific trigger values are self-set and must be declared before the sale opens):

- Sellout speed slows materially year-over-year at flat or higher capacity.
- No-show/attrition rate rises as the event scales.
- A single sponsor exceeds the revenue share you set in advance (self-set - declare the threshold now, not after a sponsor grows into it).
- The organizing team reports the work has become actively unpleasant.

Context to temper expectations: a 2023 industry write-up found independent in-person events running 30-40% below pre-pandemic attendance - a market-wide contraction, not evidence any single event mismanaged growth.

Success for this skill's own output is a growth plan that names all of the following:

- Exactly one lever, or one allocation mechanism.
- The demand evidence it rests on, with each figure marked documented or self-set.
- The financial exposure accepted and its cap.
- The pricing posture.
- The lever's paired mitigation.
- The four watch signals, with owners and check dates.

A plan missing the watch or the mitigation is not done.

## Invocation examples

- "Our 300-person conference sold out in 20 minutes with a 200-person waitlist. Do we sign the 600-seat venue?"
- "We're debating adding a second track next year - what does it cost us besides money?"
- "Demand keeps growing but organizing stopped being fun. Can we just not grow?"

Expected output: the growth (or non-growth) plan described under Measurement, delivered section by section for validation:

- Demand evidence.
- Ceiling diagnostic.
- Reach-vs-intimacy call.
- Chosen lever with rejected rungs.
- Financial gate result.
- Pricing posture.
- Mitigation.
- Watch plan.

## References

- [references/growth-case-studies.md](references/growth-case-studies.md) - the documented case record behind every lever and cap: venue step-ups, the squeeze, track-based free scaling, accessible-pricing scaling, the deliberate caps and the shrink, the overexpansion postmortems, the outlier - including three contested figures that must be reported as ranges.
- [references/venue-and-money-mechanics.md](references/venue-and-money-mechanics.md) - venue contract risk mechanics (deposits, attrition, F&B, lead times), the demand-headroom heuristic and the cases behind it, the three pricing-evolution mechanisms, and the sponsor-concentration and burnout warning patterns.

See also, same collection:

- `samber/dev-event-organizer-skills@event-market-fit` - produces the demand read this skill consumes; a soft read goes back there, never into a lever.
- `samber/dev-event-organizer-skills@event-first-edition` - zero-to-one launch; this skill starts at edition two.
- `samber/dev-event-organizer-skills@event-ticket-pricing` - owns price-setting mechanics; this skill only decides the posture.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - executes the venue search and negotiation once a step-up is decided.
- `samber/dev-event-organizer-skills@event-planning-timeline` - turns a committed lever and its 9-18 month lead into the work-back plan.
- `samber/dev-event-organizer-skills@event-portfolio-strategy` - one team running several events or formats; the franchise edge named above belongs fully to neither skill.
