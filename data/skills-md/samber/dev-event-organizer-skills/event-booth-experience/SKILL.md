---
name: event-booth-experience
description: Design a technical event's expo floor once per edition, organizer-side - the layout and traffic pattern carrying attendees past every booth, the tier-to-physical-spec catalog turning "floor presence, Gold" into table size, power, height and signage rules, the master setup and teardown schedule, per-booth power and WiFi distribution, booth staffing and conduct rules, and a floor-wide traffic mechanic such as a passport card. Use whenever asked how to lay out an expo hall or sponsor area, what a sponsor tier's booth physically includes, when sponsors load in and out, or how to pull attendees past low-traffic booths. Do NOT use for per-sponsor day-of execution - use samber/dev-event-organizer-skills@event-sponsor-fulfillment - or for how a company runs its own booth.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Booth Experience

You design the expo floor as a system for every booth, once per edition: the layout and traffic pattern, the tier-to-physical-spec catalog booths are staged against, the master setup and teardown schedule, the staffing and conduct provisioning rules, and the mechanic that pulls attendees across the floor. Hand per-sponsor day-of execution to `samber/dev-event-organizer-skills@event-sponsor-fulfillment`.

Do not write "how to run a great booth". That is the exhibiting company's job: demo loop, booth staffing, lead qualification, and swag policy, all from the sponsor's own side. The reader owns the hall, not a stand in it, so when a user turns out to be a sponsor rather than an organizer, say so and stop.

## Five siblings own the ground next to yours

| Sibling                     | The line                                                                                                                                                                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event-sponsor-fulfillment` | Real overlap, split is **design vs. execution**: you decide layout, tier zones, spec catalog, master schedule, provisioning rules, once per edition; it executes per signed sponsor (FAQ, staging, payment gate, evidence, raffle). |
| `event-sponsor-pricing`     | Prices what is sold; you define what the sold thing physically is - your catalog is the "floor presence" its ladder gates on but never specifies.                                                                                   |
| `event-venue-sourcing`      | Negotiates the room's aggregate capacity as a venue-fit criterion. You take the signed room as given and distribute it; never reopen square footage.                                                                                |
| `event-production`          | Owns the stage and A/V signal path, never the expo floor. Booth power is yours; stage power is its.                                                                                                                                 |
| `event-code-of-conduct`     | Owns adjudication, sanctions, ejection. You own provisioning only: staffing minimums, credentials, attire standard.                                                                                                                 |

Two-sided: `event-attendee-experience` engineers traffic away from booths toward sessions and facilities through the same corridor; you shape the route through them.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 8-10 exist because the menus below diverge on effort, durability and reversibility - those defaults cannot be picked for the user.

1. What is the floor, physically: a dedicated hall, a room, or a corridor around the food? Decides which layout rungs exist at all.
2. How many booths, across how many tiers, and what did each tier's package already promise on floor presence? Route a missing answer to `samber/dev-event-organizer-skills@event-sponsor-pricing`, don't invent the ladder.
3. What does the signed floor plan give you: entrance, food service, hallway-track space, where power and network already reach?
4. What are the venue's access hours, and is there secure overnight storage for sponsors' equipment as well as yours? A "no" removes a whole setup rung rather than demoting it.
5. Does the venue permit rigging - anything suspended from the ceiling or attached to the building - and what sign-off does it require?
6. Who supplies booth power, what does a drop cost, and by when must it be requested?
7. What already exists that you'd otherwise build: last edition's floor plan, a screen and someone to run it, printed signage, a fire sign-off already booked?
8. By what date must the floor plan be signed off and printed? Work back from that, not the event date - a printed plan is the least reversible artifact here.
9. One-off edition, or recurring, where this year's plan becomes next year's starting point?
10. What is the effort ceiling: volunteer hours on the dock, coordination capacity per sponsor, political capital for telling a top-tier sponsor where they sit?
11. Who runs this event: an independent community group, or a vendor or foundation?

## Workflow

1. **Run the interview; write down what you may not move**: signed floor plan, aggregate capacity, tier ladder, conduct policy. A design need that contradicts one of these routes to that sibling, not a decision you take.
2. **Settle venue facts before designing anything** - access hours, shipping window and fees, overnight storage, rigging permission, who supplies power and by when. Question list: [references/setup-teardown-and-staffing.md](references/setup-teardown-and-staffing.md). A schedule built before these arrive gets redrawn after.
3. **Pick the layout and traffic pattern** from the menu below: place booths on the path foot traffic already takes to food and the hangout space, not off to the side.
4. **Write the tier-to-spec catalog**, one row per tier, using the row list and worked example in [references/floor-plan-and-booth-specs.md](references/floor-plan-and-booth-specs.md). Fill the vertical limit and signage rule; the two rows organizers skip and regret.
5. **Distribute power and network per booth** (same reference): count booths that actually need a drop, publish per tier what's included and what must be requested, state the deadline.
6. **Build the master setup and teardown schedule** as offsets from a fixed anchor, not clock times. Shape and worked example in [references/setup-teardown-and-staffing.md](references/setup-teardown-and-staffing.md).
7. **Set staffing and conduct provisioning rules** - coverage obligation, credentials, who to send, attire standard, one named organizer on duty. Provisioning only; a conduct matter leaves this skill.
8. **Choose the traffic-driving mechanic**, designed to serve the booths the layout could not reach rather than the ones already busy.
9. **Get the floor plan reviewed before it is printed**, not before doors open - fire lane, egress, occupancy, plus rigging where the spec allows it.
10. **Walk the floor once built, before doors open**: aisles clear, nothing overhanging, every booth staffed, every promised drop live. Record what you changed for next edition's starting plan.

Publish one **floor brief** - schedule, catalog, provisioning rules, named contact - once per edition, and hand it to `samber/dev-event-organizer-skills@event-sponsor-fulfillment` to execute per signed sponsor. Never build a per-sponsor tracking matrix here.

If your harness has persistent memory, record per edition: the final floor plan with tier zones, which booths were dead spots, what you moved on the day and why, missed request deadlines, and whether the traffic mechanic reached anyone not already engaged. Dead spots and hand-moved tables are the layout errors your next plan starts from.

## Two of these four menus do not diverge, and that is worth naming

- **Layout and setup menus** - value and effort disagree, so an efficiency ratio genuinely resolves the choice.
- **Booth-spec and traffic-mechanic menus** - value and effort rise together across every rung. No dominance relation exists there, so the ordering rests on judgment about where returns flatten.

Re-rank those two hard against Q7 and Q10. Full reasoning: [references/decision-menus.md](references/decision-menus.md).

## Layout and traffic pattern

Where booths sit and how attendees move past them. Ranking (default, not a law - Q1, Q3 and Q7 re-rank it):

- effort (floor-plan iterations, venue coordination, sponsor negotiation, reversibility once printed): `hub-and-spoke around a central draw > zoned by tier > racetrack perimeter loop > grid rows > circulation-path siting`
- value (every booth walked past by people who were not looking for it, not only the well-placed ones): `racetrack perimeter loop > circulation-path siting > hub-and-spoke around a central draw > zoned by tier > grid rows`
- compliance cost (the review it triggers, and what stops being reversible): `hub-and-spoke around a central draw > circulation-path siting > racetrack perimeter loop == zoned by tier > grid rows`
- efficiency: `circulation-path siting > racetrack perimeter loop > grid rows > zoned by tier > hub-and-spoke around a central draw`

- **Circulation-path siting** (default) - site tables on the food or hangout path so foot traffic naturally passes them (DevOpsDays organizing guide). Near-zero effort, wins efficiency outright. Promote to the racetrack once Q1 says the floor is a dedicated hall, or Q2's booth count exceeds what that path holds.
- **Racetrack perimeter loop** - perimeter with one circulating path, no booth off a spur. Tops value: position barely matters, so it is easiest to defend to a sponsor who paid for a good spot.
- **Grid rows** - parallel aisles. Cheap, sign-off close to a formality; aisle interiors starve while the ends do well.
- **Zoned by tier** - premium tiers drawn from a premium zone. Promote when the ladder genuinely sold position and Q10 says you have the political capital to hold the line. Delete when the ladder sold no floor-presence differentiation: one table spec for everyone.
- **Hub-and-spoke around a central draw** - booths radiate from a central attraction. Real value, top effort; efficiency never picks it. Promote only when Q7 turns up a draw that already exists for other reasons (a coffee bar, a demo stage, a hallway-track hub).
- Never leave the floor unmapped for sponsors to pick their own spot on arrival: it rewards whoever arrived earliest, not whoever paid most, and leaves the last sponsor in the dead corner with a legitimate complaint.

Full reasoning behind the compliance tie and each rung: [references/decision-menus.md](references/decision-menus.md).

## Booth tier physical-spec depth

How precisely each tier's booth is specified, and how much of it you build.

Value and effort rise together across every rung here. No dominance relation exists, so the ordering is clean by construction, not by care, and the efficiency line rests on a judgment about where differentiation stops paying.

Ranking (default, not a law - Q2, Q5 and Q7 re-rank it):

- effort/value: `fully bespoke per sponsor > custom structure for the top tier only > standard table spec per tier > shared table row`
- compliance cost (rigging review triggered): `fully bespoke per sponsor > custom structure for the top tier only > standard table spec per tier == shared table row`
- efficiency: `standard table spec per tier > shared table row > custom structure for the top tier only > fully bespoke per sponsor`

- **Standard table spec per tier** (default) - two or three written specs, each carrying the eight rows in [references/floor-plan-and-booth-specs.md](references/floor-plan-and-booth-specs.md). Wins efficiency: it creates the gating axis the ladder needs for a small effort step up from a shared row.
- **Shared table row** - a single shared surface for everyone. Near-zero effort, but collapses the axis a ladder needs to gate on. Legitimate only where the ladder sold no floor differentiation either.
- **Custom structure for the top tier only** - a built stand for the top tier, tables below. Promote only when Q2 says the top tier's price promises floor presence a table cannot deliver, _and_ Q5 says the venue permits rigging: both required.
- **Fully bespoke per sponsor** - every sponsor builds their own stand to a plot spec. Tops value and effort together, so efficiency never picks it. **Promotion condition, keyed to Q11**: a vendor- or foundation-run event where sponsors expect to build.
- Never leave "a table will be provided" with no dimension, no height limit and no signage rule: whoever is standing there at 08:00 fills each blank later, inconsistently.

Full reasoning, the compliance-tie argument, and a worked catalog with negative counterpart: [references/floor-plan-and-booth-specs.md](references/floor-plan-and-booth-specs.md) and [references/decision-menus.md](references/decision-menus.md).

## Setup and teardown window architecture

When sponsors get in, and when they get out. Ranking (default, not a law - Q4, Q6 and Q10 re-rank it):

- effort (dock coordination, messages per sponsor, venue access hours negotiated, supervision): `overnight pre-day build > tiered windows > staggered by zone > single shared window`
- value (every booth ready at doors-open, dock congestion and damage avoided, equipment safe): `tiered windows > overnight pre-day build > staggered by zone > single shared window`
- compliance cost (electrical and labour review triggered, and what cannot be renegotiated): `overnight pre-day build > tiered windows == staggered by zone > single shared window`
- efficiency: `single shared window > staggered by zone > tiered windows > overnight pre-day build`

Tiered windows dominate the overnight build outright: better value _and_ less effort, so any ordering putting overnight above tiered would be a violation. What demotes overnight is a distinction the venue's storage answer does not cover: secure overnight storage means crates in a locked room, while a pre-day build leaves assembled stands out on a floor nobody staffs.

- **Single shared window** (default) - setup an hour before registration on the first day, for everyone; a real published practice (DevOpsDays Des Moines, standing 2019-2025), not a cross-event standard. Promote to staggered once Q2's booth count exceeds what one door absorbs, or Q4's access hours run shorter than the build needs.
- **Staggered by zone** - move-in slots per aisle or zone, spreading arrivals across the same total window. Cheap: the shared window plus a list.
- **Tiered windows** - premium tiers get an earlier or dedicated slot. Promote when the top tier's package sold a dedicated load-in, or one sponsor's build genuinely needs more time than the shared window holds.
- Delete the overnight pre-day build when Q4 says the venue grants no out-of-hours access or no secure storage. It is not a rung the organizer may choose against the venue's answer.
- Never let teardown start before the last session ends: it converts the closing session into packing-tape noise and silently breaks the floor-presence perk the sponsor bought.

Full reasoning behind the dominance case and the compliance tie: [references/decision-menus.md](references/decision-menus.md).

## Traffic-driving mechanic

What pulls attendees to the booths the layout could not reach. The per-booth raffle is deliberately not a rung here: `samber/dev-event-organizer-skills@event-sponsor-fulfillment` already ranks it as a lead-capture posture. On this menu's own question it fails anyway: its pull stays confined to the booth already running it.

Value and effort rise together across all three remaining rungs, as on the booth-spec menu: no dominance relation exists, and the ordering is clean by construction, not by care. Ranking (default, not a law - Q7 and Q10 re-rank it):

- effort/value: `scavenger hunt with a live leaderboard > passport or stamp card > organic traffic only`
- efficiency: `passport or stamp card > organic traffic only > scavenger hunt with a live leaderboard`

No compliance-cost axis: no rung here collects anything beyond one winner's contact detail at claim time. The moment you redesign the passport so each booth _scans_ the attendee, it becomes the lead-capture question `samber/dev-event-organizer-skills@event-sponsor-fulfillment` owns instead, with a consent flow attached.

- **Passport or stamp card** (default) - one card, a stamp per booth, a prize for a completed card. Wins efficiency: the only rung that makes every booth a required stop.
- **Organic traffic only** - the layout does the work and nothing else runs. Beats the hunt on near-zero effort; honest at a small event on a single circulation path.
- **Scavenger hunt with a live leaderboard** - tops value and effort together, so efficiency never picks it. Promote when Q7 says a screen and someone to run it already exist, or the floor is too large for a card alone to route people through it.
- Never require a sponsor's signature or a conversation before the stamp is given: it converts a traffic mechanic into a forced pitch, against the published staffing guidance to send someone who can "tell your story and participate with the community", not process a queue.

Full reasoning: [references/decision-menus.md](references/decision-menus.md).

## Failure modes

- **A spec with blanks in it.** Every unstated dimension, height limit, deadline or signage rule is filled in on the morning by whoever is standing there, under time pressure, inconsistently. Fix: the catalog's eight rows are all mandatory, and the vertical limit and signage rule are the two that get skipped.
- **Quoting a booth-position figure to a sponsor.** No usable data exists; what circulates comes from companies selling booth displays. Fix: describe the position honestly, on the food path or off a spur, and let the sponsor judge.
- **Designing the schedule before the venue answered.** Access hours, shipping fees, storage and rigging are venue facts, and a schedule built without them is redrawn once they arrive. Fix: workflow step 2 comes before step 6, always.
- **A power request with no deadline.** The drop is sold, nobody says by when it must be requested, and it lands on the morning at a venue that needed two weeks. Fix: the deadline is a published row in the schedule, not a sentence in an email.
- **Rebuilding `samber/dev-event-organizer-skills@event-sponsor-fulfillment`'s job.** A per-sponsor tracking matrix, a payment gate, a sponsor's FAQ answered one at a time - all of that is downstream. Fix: you publish one generic floor brief; it is executed per sponsor elsewhere.
- **Adjudicating a booth-conduct incident.** You wrote the standard; you do not enforce it. Fix: route it to the incident pipeline the moment it stops being a provisioning question.
- **A signed and printed floor plan changed late.** It is the least reversible artifact you produce. Fix: work back from Q8's print date, and get the fire review before the print run rather than before the doors.

## Measurement

Everything below is self-set and only becomes meaningful across editions.

- **Dead-booth count** (self-set) - booths that reported being walked past by almost nobody. This is the single number that says whether the layout rung was right. Ask the sponsors; do not infer it.
- **Spec completeness** (gate) - every tier row has all eight fields filled before the brief goes out. No threshold; the number that matters is zero blanks.
- **Floor ready at doors** (gate) - every booth staffed and every promised drop live at the floor walk. A booth still unpacking at doors-open is a setup-menu failure, not a sponsor failure.
- **Tables moved by hand on the day** (self-set) - count and keep them. Each one is a place the plan met the building and lost.
- **Traffic-mechanic completion by the un-engaged** (self-set) - not how many cards came back, but whether any came from attendees who were not already touring booths. That is the only thing the mechanic exists to buy.

## Invocation examples

- "We have 12 sponsors and one hall. Where do the booths go?"
- "What does our Gold tier's booth actually include? The prospectus just says 'floor presence'."
- "When do sponsors load in, and how do we stop the dock jamming at 08:00?"
- "The booths at the back say nobody visits them. What do we change next edition?"
- "A sponsor wants to hang a banner from the ceiling. What do we tell them?"

Expected output: one floor brief assembling:

- a marked-up floor plan with tier zones and the traffic pattern named
- a tier-to-spec catalog with all eight rows filled per tier
- a master setup and teardown schedule written as offsets from a fixed anchor, with request deadlines as rows
- a per-booth power and network allocation with what must be requested and by when
- staffing and conduct provisioning rules
- a chosen traffic mechanic

Label every self-set element as such, and route every venue-specific figure to the venue rather than stating it.

## References

- [references/floor-plan-and-booth-specs.md](references/floor-plan-and-booth-specs.md) - what is published about placement, the eight-row tier catalog with a worked example and its negative counterpart, the constructed power and WiFi distribution process, and the two review categories the plan triggers.
- [references/setup-teardown-and-staffing.md](references/setup-teardown-and-staffing.md) - the published sponsor logistics FAQ, the venue questions that must be answered first, the master schedule shape with a worked example and negative counterpart, and the staffing, credentials and attire provisioning rules.
- [references/decision-menus.md](references/decision-menus.md) - the full reasoning behind each of the four menus' ties, promotions and deleted options, and why two of the four menus carry no dominance relation at all.

Sibling skills referenced throughout: see § Five siblings own the ground next to yours.

The mirror question - how an exhibiting company runs its own booth - is planned as a skill in this owner's developer-relations collection and is not built yet. Until it is, tell a sponsor-side reader plainly that this skill answers the organizer's half only.
