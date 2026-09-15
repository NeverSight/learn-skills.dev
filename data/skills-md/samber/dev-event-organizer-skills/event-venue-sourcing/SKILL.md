---
name: event-venue-sourcing
description: Find and negotiate the venue for a technical event. Covers the written space program built from an attendance estimate and chosen format (main room, breakouts, hallway track, sponsor tables, power and WiFi density, load-in), a sourcing ladder treating free campus, civic and company-hosted space as a real first rung, site visits at the depth the risk warrants, several venues carried against several dates, and the contract traps - attrition, food-and-beverage minimum, cancellation curve, insurance requirement. Use whenever the user mentions finding a venue, room or space for an event, venue requirements, a site visit, or a venue contract - even if they never say "sourcing". Do NOT use for non-venue suppliers - use samber/dev-event-organizer-skills@event-vendor-sourcing instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Venue Sourcing

You are a venue sourcing and negotiation advisor for technical events. Find the space, prove it meets a written requirement sheet, and negotiate terms the organizer can live with - for a conference, a hackathon, or a multi-day event with satellite sites.

You do not decide whether to grow, which date to pick, or what insurance to buy. Those decisions arrive from siblings and you execute against them.

## Two things this skill will not supply

- **Venue prices** - venue rates are quoted per deal, not published: no rate card holds across markets, seasons and venue classes. Never invent a figure to fill that gap. One narrow, sourced exception exists (a UK marketplace's own published listing prices, see `references/contract-traps-and-negotiation.md`); treat it only as a planning-stage sense check, never as a number to bring into a negotiation. A fabricated benchmark anchors the organizer on a number the venue can immediately disprove, and the credibility lost is the leverage the rest of the negotiation runs on. Real quotes from three candidates on one identical requirements sheet are the only benchmark that is true for this city, this year, this size.
- **Hybrid and multi-venue technical specifications** - _choosing_ a hybrid format is settled on the format side. Translating that choice into venue-side requirements (guaranteed upstream bandwidth, rigging points, camera positions, uplink redundancy, control-room space) sits outside this skill. Do not invent an equipment list or a bandwidth figure; put it to the venue as a question it must answer in writing, and route the specification to `samber/dev-event-organizer-skills@event-production` and `samber/dev-event-organizer-skills@event-format-selection`.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability and effort; those defaults cannot be chosen for the user.

1. What is the expected attendance, and where does that number come from - a prior edition's actuals, a demand read, or an estimate? What format has already been chosen (single track, multi-track, workshops, hackathon, overnight, hybrid)?
2. Which candidate date windows are live? (Expect three to five from `samber/dev-event-organizer-skills@event-date-selection`. If exactly one date exists, say now that it costs most of the negotiating position, and ask whether it can move.)
3. Is this a first edition, a repeat in a known venue, or a decided step-up to a bigger one? If a step-up, what financial ceiling did that decision set - deposit tolerance, attrition tolerance, lead time?
4. Free or hosted space, or a paid rental? Which free options genuinely exist - a university, a civic or innovation centre, a company willing to host, a sponsor willing to buy the venue?
5. What is non-negotiable in the space itself: overnight operation, hardware or rigging, livestreaming, a specific accessibility bar, catering that must come from outside?
6. By what date must the venue be signed - a sponsor budget cycle, an announcement already made, a competing booking on the same room? (A near deadline promotes the fast rungs and demotes anything with institutional bureaucracy in it.)
7. Is this a one-off edition or one step in a recurring annual event? (A recurring event should trade a better one-year price for a relationship and a renewal option; a one-off should not.)
8. What is the effort ceiling - organizer hours, whether anyone can visit in person, whether a lawyer will read the contract, and how much irreversibility the team can carry?
9. What already exists that the default ranking assumes away: a standing venue relationship, an organizer employed by a company with space, a campus advocate, a prior edition's marked-up contract, a sponsor already asking to host?

## Donated space vs. contracted venue

Whether money and a cancellation curve are on the table at all changes every menu below.

- **Donated or hosted pole** - free campus, civic or company space. No deposit, no attrition clause, no food-and-beverage minimum. The exposure is relational rather than financial: institutional bureaucracy, an academic or corporate calendar that can shift under you, sponsor-category restrictions the host imposes, infrastructure gaps you patch yourself, and often a booking with no written notice period at all. This is where most community-run technical events start.
- **Contracted commercial pole** - paid rental, hotel, conference centre. Every money mechanic applies in full, contract review becomes unskippable, and the cancellation-fee curve becomes the spine of `samber/dev-event-organizer-skills@event-risk-management`'s decision calendar.

This correlates with the collection's community-run vs. company-run split but is not the same line: a company-run event often sits at the donated pole in its own office, and a volunteer community conference often signs a paid centre. Ask which pole the venue puts them in, not which pole the organization is.

## Workflow

1. Run the interview. Confirm what arrives from upstream instead of re-deciding it: the attendance number and format, the candidate windows, the step-up decision and its financial ceiling, the accessibility criteria, the budget shape. If no attendance number exists yet, stop and route to `samber/dev-event-organizer-skills@event-market-fit` and `samber/dev-event-organizer-skills@event-growth-strategy` - a space program built on a guess sizes the whole contract wrong.
2. Check the prerequisite the venue conversation itself needs before it opens: the organizing entity's legal name, contact details and business or registration number. Some venues require them just to place a hold on a date, so a missing registration number can burn a candidate window while it is found.
3. Translate attendance and format into the **space program**: main room, breakout mix, hallway-track space, sponsor tables, zones for a hackathon, plus the density ratios and every non-space criterion. Write it once, and give every venue the identical sheet - two venues cannot be compared on two different questions.
4. Generate candidates from the sourcing ladder, free rungs first and as rungs rather than fallbacks.
5. Desk-check every candidate against the sheet, then visit only the survivors, at the depth the site-visit menu sets.
6. Fill the **options grid**: candidate venues against candidate windows, with a written quote from every survivor on the identical sheet, before opening a price conversation with any of them. This is what lets availability rank the date windows - the job `samber/dev-event-organizer-skills@event-date-selection` explicitly hands over - and it is the alternative that gives every negotiation tactic its force.
7. Read the contract traps on every offer, including the free ones. A hosted space has restrictions where a paid one has fees; neither is free of terms.
8. Negotiate at the posture the menu sets, in the channel you are actually in. Say out loud which tactics are general vendor-negotiation technique rather than venue-specific practice.
9. Sign, then extract two things verbatim for siblings: the cancellation-fee dates and percentages, and the insurance requirement with its amounts. You report these; you do not decide what they mean.
10. Hand off the pack, and name **one local organizer** as the venue's day-to-day operational contact for layout, tables and A/V detail - an explicit role, not an assumption that whoever signed owns it. Venue work runs through the final weeks; it does not close at signature.

Two cheap artifacts pay for themselves across a multi-year relationship with the same venue, and belong in the handoff pack rather than in any one organizer's head: a short recorded video walkthrough of the venue's own idiosyncratic equipment (a sound desk, a coffee machine, a back-room setup a volunteer will have to operate), filmed once and reused; and a room/space inventory kept by striking through entries no longer available rather than deleting them - availability oscillates year to year, and a deleted line loses the memory of a room worth re-requesting later.

If your harness has persistent memory, record the signed terms and the rejected candidates: the cancellation curve, the insurance requirement, the attrition or minimum commitments, every requirement marked not-met with its workaround, and which venues were ruled out and why. The next edition's negotiation starts from this venue's own history, and a candidate rejected for a fixable reason is worth revisiting.

## Sourcing channel ladder

Every ranking in this skill is a default, not a law - it shifts with context and with who executes it. Re-rank all three menus against the interview:

- A hard signing deadline (Q6) demotes anything with institutional bureaucracy in it.
- A recurring annual event (Q7) promotes relationship-building over a one-year price.
- A low effort ceiling (Q8) demotes the free rungs that need chasing.
- Any asset in Q9 (a standing relationship, an organizer whose employer has space, a campus advocate) promotes its own rung past everything above it.

- effort: `host sponsor buys the venue > educational or civic space == bare commercial rental > coworking or community rental > company-hosted space`
- value (fit to the full space program, at the needed scale, with certainty): `host sponsor buys the venue > bare commercial rental > educational or civic space > coworking or community rental == company-hosted space`
- efficiency: `company-hosted space > educational or civic space > coworking or community rental > host sponsor buys the venue > bare commercial rental`
- compliance cost (review triggered, reversibility lost): `host sponsor buys the venue > bare commercial rental > educational or civic space == company-hosted space > coworking or community rental`

- **Effort tie** - both rungs take months: one spent chasing institutional sign-off and patching the infrastructure the room lacks, the other spent on requesting quotes, reviewing the contract, and sourcing the tables, chairs and security a bare rental omits. Equal in months and coordination; they differ only in who you chase.
- **Value tie** - a coworking rental and a company-hosted office are both someone else's working space. Capacity is whatever it already is, infrastructure comes with it, and neither can be scaled to the sheet. They differ in whether you pay, not in what you get.
- **Compliance tie** - each binds something outside the venue arrangement itself: a campus's own security, fire and event-policy regime, or a host's restriction on who may sponsor. What you lose in both is not money but a later decision.

- **Educational or civic space** - universities, innovation centres, libraries, public facilities. Named first for conference-scale and hackathon-scale events alike, from opposite audience poles. Free, and campus staff already know the booking process. Bring a **campus advocate** - a professor, dean or staff sponsor who can fast-track institutional booking; the hackathon guide publishes ready-made pitch material for administrators and faculty, framing the event in career-fair vocabulary they already value.
- **Company-hosted space** - a company offers its own facility. Best efficiency on the menu when capacity fits: one relationship conversation, good WiFi and power by construction, no rent. Capacity is the usual failure, and it cannot be fixed by layout.
- **Coworking or community rental** - paid, but with the infrastructure already built in. The named fallback when no free rung works, cheaper than a bare rental plus the build-out it forces. It sits above company-hosted space on effort because being paid means it carries a search, a quote and a rental contract that an offered space does not. For a team-based event, a shared-office building can give each team a real closed room instead of a table in a hall - budget roughly one room per team plus a few spares. The known cost is that helpers get lost navigating a building nobody designed for a single event; when the venue will not consolidate the event onto fewer floors, the accepted fallback is a printed floor map plus signage, not another round asking for a room reshuffle.
- **Bare commercial rental** - conference centre or hotel. The only rung that can meet any requirement at any scale, and the only one that carries the whole money mechanic. A paid bare venue also shifts infrastructure onto the organizer that a sponsored space absorbs - internet wiring, tables and chairs, a security team - and hidden and additional charges can double the event's total cost.
- **Host sponsor buys the venue** - the starved option: a sponsor pays for a commercial venue on the organizer's behalf. Highest value on the menu and it loses on efficiency to every free rung, because it needs two negotiations and is gated on a sponsorship sale landing first. Promote it when a sponsor relationship already exists with budget in the right fiscal year _and_ the sheet needs a commercial-grade venue the event cannot fund itself.

**Default rung: the highest-capacity free rung that meets the must-have lines** - educational or civic at conference scale, company-hosted below roughly an office floor. Move down to a paid rung only when no free rung meets the must-haves, or when the free rung's terms cost more than rent would: a sponsor-category restriction that blocks categories already sold, no setup-day access, or an academic calendar that kills every candidate window.

**The unwritten handshake booking is deleted from this menu, not ranked last.** "A friend's company said we can use their space" presents as the cheapest rung and reappears the moment budget gets tight. Parking it at the bottom is unsafe for exactly that reason. An unwritten free booking has no notice period, no setup-day access, no storage commitment and no sponsor-restriction clarity, and the organizer discovers all four in the final week with every alternative gone. A free venue still gets terms in writing; without them it is not a rung.

## Site-visit depth

Cumulative rungs - each contains the one below.

- effort: `technical walkthrough > working walkthrough > single sales-led visit > desk check`
- value (requirements confirmed rather than assumed, while leverage still exists): `technical walkthrough > working walkthrough > single sales-led visit > desk check`
- efficiency: `working walkthrough > desk check > single sales-led visit > technical walkthrough`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all six pairs: the deeper visit confirms more and costs strictly more time, including every pair against the desk check, which loses on value rather than winning anything for free. No third axis is printed. The check catches nothing; the non-obvious ordering below rests on its own argument.

The efficiency order puts the free desk check above two of the three real visits, which is the non-obvious part: the desk check's whole job is elimination, and it does that at near-zero cost. A sales-led walkthrough, by contrast, costs half a day and returns a feeling rather than a marked sheet. Only the working walkthrough beats it, because it is the one rung that returns a marked sheet at all - a jump in value larger than the day it costs, which no other step up this ladder can claim.

- **Desk check** - floor plans, capacity sheets, photos, and reports from past events held at the same venue. Eliminates candidates on capacity, date, and hard must-haves before anyone travels.
- **Single sales-led visit** - one walkthrough with the sales contact. Ranked, not deleted, because it is sometimes all the access a distant venue allows; it just cannot substitute for the rung above.
- **Working walkthrough** - the default: walk the sheet line by line and mark every line met, not met, or needs-an-answer-in-writing. Arrive the way an attendee will, walk the accessible route in parallel, and test the WiFi yourself in the rooms. Count outlets against the density ratio, walk the load-in route, see the actual lockable storage room, and meet the person who will be on site on the day rather than only the one who sells it.
- **Technical walkthrough** - the starved option: the working walkthrough plus the production or A/V lead, plus an accessibility reviewer where the format needs one, timed at the event's own day and hour. Highest value, loses every efficiency round. Promote it for a hybrid or livestreamed format, heavy rigging or hardware, an overnight event, or a first edition at a venue nobody on the team has worked in.

**A site visit scheduled after signature is deleted from this menu, not demoted.** Venues offer it, it feels like diligence, and it is worthless: a visit with no leverage left can only produce a list of things to worry about. The visit's entire value is that its findings can still change the deal.

## Negotiation posture

No compliance-cost axis here, and the reason belongs inline: every posture ends with the same contract going to the same reviewer. What changes is what the contract says, not what reviewing it costs.

- effort: `structured concession bargaining > competitive options > disclosure pass > accept the quote`
- value (terms improved and surprises removed before signature): `competitive options > structured concession bargaining > disclosure pass > accept the quote`
- efficiency: `disclosure pass > competitive options > structured concession bargaining > accept the quote`

Competitive options beat structured bargaining on value because the grid moves the terms that matter most: which date, which venue, whether a mandated caterer is even in play. Bargaining without a real alternative, by contrast, moves a price slightly and a clause not at all. Accepting the quote sits last on efficiency despite costing nothing: a zero numerator is not a cheap win.

- **Accept the quote** - take the terms as offered. A real position in exactly one case: a free institutional room offered on standard terms with nothing on the table to move. Anywhere money is involved it is a decision not to look.
- **Disclosure pass** - send a written question list:
  - Is the quote a guaranteed ceiling?
  - Is catering mandated in-house?
  - Are security, fire marshal or janitorial staff charged separately?
  - What insurance is required of us and of sponsors?
  - What is the shipping address and receiving fee?
  - What is the cancellation schedule?
  - Are there restrictions on who may sponsor?

  An email that removes the whole class of surprise that costs most later, which is why nothing else on the menu returns as much per hour.

- **Competitive options** - the default: run the grid, quote every survivor on the identical sheet, and let availability and _total committed cost_ rank them rather than the headline room rate venues compete on precisely because it is not what you pay.
- **Structured concession bargaining** - the starved option: tactical negotiation techniques (mirroring, labelling, calibrated "How" questions, an accusation audit) applied to the clauses that actually hurt. Pair a decreasing-increment concession sequence with a non-monetary ask: an extra load-in day, waived receiving fees, a later catering headcount deadline, a softer cancellation step. **Scope caveat**: these are general vendor-pricing negotiation techniques rather than venue-specific practice, and their voice and pacing guidance assumes a live conversation. Promote it when the rental is paid, the committed amount is material against the budget, and the channel is a call or a visit. Demote it on an email-only exchange.

**Negotiating one venue on one date is deleted from this menu, not ranked last.** It is the tempting posture - the venue everyone loves, the date already announced - and parked at the bottom it returns as "we'll just push them a bit". Every tactic above derives its force from an alternative that this posture does not have.

**The contract trap list is deliberately not ranked**, and that is an argued refusal rather than an omission. Which trap is expensive is set by the contract in front of you and the format you are running. A food-and-beverage minimum decides everything for a catered conference and nothing for a bring-your-own hackathon, while a fire-code limit on overnight sleeping is decisive only for events that run through the night. Ranking them would be false precision that quietly authorizes skipping the last one; read all of them.

## Failure modes

- **Signing before reading the attrition clause and the food-and-beverage minimum.** These are the core financial exposure of a venue contract: the organizer can owe the shortfall even when attendance comes in below the number committed to. The one published threshold is a hotel room block requiring around 80% of blocked room-nights to be used where the hotel gets no other business - mitigate with a very small starter block that grows as it fills, scoped to the nights actually needed.
- **One venue, one date.** Converts every subsequent conversation from a negotiation into a request, and it is usually self-inflicted: a date announced before the venue was signed, or a favourite venue approached alone.
- **Quoting sponsors before reading the venue's insurance requirement.** Venue-required insurance is a routine contract term, often naming the venue as additional insured, and what the venue requires of the organizer shapes what the organizer must require of sponsors. Read it first, then let `samber/dev-event-organizer-skills@event-sponsor-agreement` pick its rung.
- **Checking accessibility after signing.** The accessible route is either the route everyone takes or it is a finding - and after signature a finding is just something to apologize for. Walk it during the visit, against the criteria `samber/dev-event-organizer-skills@event-accessibility-inclusion` sets.
- **Discovering shipping and load-in on the day.** Ask during sourcing from what date shipments are accepted, to what address, with what receiving fees, what hours the team has access, and whether secure overnight storage covers sponsor equipment as well as the organizer's.
- **Treating a free venue as free of terms.** A hosted space substitutes restrictions for fees - most commonly a limit on which other companies may sponsor or exhibit. Clarify it in writing before selling a single category.
- **Overcommitting headcount, or pre-paying.** Avoid both until forced: adding a few extra plates is always cheaper and easier than having already paid for too many.
- **Asking "can we run overnight?" as one question.** Overnight working is usually permitted where overnight sleeping is against fire code at the same address. Ask both, and get the answer in writing.

## Measurement

The observables below are **self-set** working defaults, not industry standards - say so when you report against them.

- Every must-have line on the requirements sheet is marked met, not met, or answered in writing, before signature.
- At least two venues quoted on the identical sheet, with at least two date windows still live when the quotes arrived.
- Zero contract terms discovered after signature that appear on the trap list.
- The cancellation-fee schedule and the insurance requirement are in `samber/dev-event-organizer-skills@event-risk-management`'s and `samber/dev-event-organizer-skills@event-sponsor-agreement`'s hands before the next sponsor is quoted.
- Nothing about load-in, storage or access hours is learned for the first time on the event day.

Success for this skill's own output: a signed venue with a marked requirements sheet, a filled options grid showing what was rejected and why, the trap list read with each finding recorded, and a handoff pack. A signature with no marked sheet is not a finished job.

## Invocation examples

- "We're expecting 180 people over two days in April or May - help me work out what to ask venues for."
- "The conference centre sent a quote. What do I need to read before signing it?"
- "Our hackathon runs overnight for about 300 students. Which venue options should we chase first?"
- "The university said yes but wants us to carry insurance. What does that mean for our sponsors?"

Expected output: the space program, then the shortlist and grid, then the trap findings, then the negotiation plan - delivered section by section for validation rather than as one finished document.

## References

- [references/space-program-and-requirements.md](references/space-program-and-requirements.md) - the room-by-room space program, the per-attendee WiFi and power ratios, the non-space criteria, the overnight fire-code case, the hybrid and multi-venue gap stated rather than filled, and a filled requirements sheet with a negative counterpart.
- [references/contract-traps-and-negotiation.md](references/contract-traps-and-negotiation.md) - deposit, attrition, lead-time and room-block mechanics, the full trap list, the two terms other skills consume, the negotiation tactics, the price-benchmark refusal in full, and the one sourced sanity-check figure this skill carries.
- [references/site-visits-and-options.md](references/site-visits-and-options.md) - the sourcing channels in detail, the site-visit checklist walked in day order, the options grid, the handoff pack, and a worked shortlist with a negative counterpart.

See also, same collection:

- `samber/dev-event-organizer-skills@event-budget` - models the venue as what it usually is, the largest single cost line. This skill supplies real quotes; that skill supplies the budget shape, and neither invents a price.
- `samber/dev-event-organizer-skills@event-planning-timeline` - turns the signed contract's dates (catering headcount deadline, room-block expiry, cancellation steps, setup access) into the work-back schedule.
- `samber/dev-event-organizer-skills@event-attendee-experience` - designs how an attendee discovers and moves through the signed floor plan, and turns the hallway-track space and quiet room in this skill's space program into a located, signed design.
- `samber/dev-event-organizer-skills@event-schedule-design` - lays the sessions inside the rooms and hours this skill secures. Capture seated capacity and the walking distance between rooms while you are on site: a grid built without them is a seating plan discovered on the day.
- `samber/dev-event-organizer-skills@workshop-program-design` - produces the workshop-specific room, power and network requirements that enter this skill's space program, including the device-count and blocked-protocol questions a venue must answer in writing.
- `samber/dev-event-organizer-skills@event-learning-expedition-design` - takes an audience into an organization that supplies the room _and_ the program, so a withdrawing host deletes the agenda rather than costing a re-bookable room and this skill's several-venues-against-several-dates mechanic does not transfer. It takes the multi-venue extension of this skill's requirements sheet as an input, and note the third name collision on "site visit": there it means showing an audience somebody's working floor, never inspecting a room before signing.
