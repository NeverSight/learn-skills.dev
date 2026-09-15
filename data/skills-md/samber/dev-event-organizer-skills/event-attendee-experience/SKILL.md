---
name: event-attendee-experience
description: Design the general-attendee on-site journey for a technical event  -  check-in desk and badge pickup, the badge's privacy and scanning posture, wayfinding and signage, the quiet room and other facilities, meal and dietary mechanics, the help path, first-time-attendee orientation, and a walkthrough audit of the finished design. Use whenever asked how to run conference check-in, whether to put a QR code on a badge, where the quiet room goes, how to sign a venue so people find rooms, how to hand out dietary-restricted meals, what a help desk should cover, or how a first-timer finds their feet. Starts at the door. Do NOT use for registration or no-show mechanics  -  use samber/dev-event-organizer-skills@event-no-show-management; speakers, sponsors and volunteers have their own journey skills.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Attendee Experience

You design the day a general attendee actually walks through: getting in the door, finding the room, where to go when the day gets loud, eating, asking, and what they remember. Inputs arrive decided - a signed floor plan, a published grid, a register, an accessibility bar - and the output is a design somebody can execute and audit by walking the building.

You add only the attendee-specific layer on top of the population-agnostic fundamentals in `samber/dev-event-organizer-skills@event-hospitality`, which decides only the catering service style, what a scheduled break contains, the alcohol posture, and whether an evening programme exists. It routes signage, wayfinding and facilities back here, and the welcome register and staff warmth to `samber/dev-event-organizer-skills@event-cultural-identity`. Consume its brief; do not restate its decisions here.

## Seven siblings already own part of this day

Each states its own side of the boundary. Consume them; do not re-derive them.

| Sibling                         | The line                                                                                                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event-cultural-identity`       | Sets the register you carry; you decide where the desk stands and how the queue moves. Ask which register it set, never redesign it.                       |
| `event-code-of-conduct`         | Borrows your quiet room as an intake space - the room must serve decompression _and_ confidential intake at once (§ Facility provision depth).             |
| `event-accessibility-inclusion` | Decides whether a provision exists, how many, dietary categories, the accessible route; you own where it sits and how someone reaches it.                  |
| `event-run-of-show`             | Staffs and executes what you design. Its named organizer-on-duty is this skill's escalation at check-in.                                                   |
| `event-speaker-experience`      | A separate population with zero overlap: speakers get their own host, tech check, green room.                                                              |
| `event-venue-sourcing`          | Secures the envelope, already naming hallway-track space and a quiet room as requirements. Work inside the signed floor plan; never reopen square footage. |
| `event-schedule-design`         | Owns the grid. Design what happens inside a scheduled gap, never move or lengthen a break.                                                                 |

Five further siblings now ship: `samber/dev-event-organizer-skills@event-hospitality`, `event-booth-experience`, `event-volunteer-experience`, `event-attendee-email-sequences` and `event-no-show-management`. Every boundary against them below is stated from this side only - check theirs before relying on it.

`event-booth-experience` and `event-volunteer-experience` are genuine two-sided design problems: booth traffic runs through the same corridor your wayfinding serves, in the opposite direction, and volunteers use the meal line and quiet room you size without owning their design. `event-attendee-email-sequences` owns cadence and copy; you are the source of truth for what those emails say about the on-site day.

Every ranking below is a default, not a law: it shifts with context and who executes it. Re-rank all four menus after the interview. Each of these overturns a default rung: a venue with one entrance and one corridor, a registration system that exports a sorted list, a signage set you already own from last edition, a volunteer who has run a desk before, a sponsorship agreement that already promised lead capture.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the menus below diverge sharply on time-to-effect, durability and effort - those defaults cannot be picked for the user.

1. How many attendees, across how many days, in how many buildings or floors?
2. Is there a registration gate at all - paid ticket, free-with-registration, open door? Decides whether half this skill applies.
3. What register did the culture work set - warm and chatty, or efficient and quiet?
4. What does the signed floor plan actually give you: rooms, corridors, food, sponsor tables, entrance?
5. What dietary categories and accessible-route bar were set for you? Ask; never invent the list.
6. Does any sponsorship agreement already promise badge scanning or lead capture? If yes, the posture was decided upstream.
7. For each artifact, what's the last date it can still change - badge print, signage print, catering headcount, room allocation?
8. One-off edition, or recurring, where this year's walkthrough becomes next year's starting map?
9. Effort ceiling: volunteer-hours on the desk, print budget, and what you already own (last edition's signage, a floor plan, a list export)?
10. Which distinct ticket categories exist, and do any of them need their own check-in lane?
11. Does a meaningful share of the audience attend with caring responsibilities (children, dependents)?
12. Does the code-of-conduct pipeline already name an on-duty responder for the day?

## Community-run vs vendor-run, and the axis that actually reshapes the menus

What changes the design is who owns the event, not who paid for the ticket:

- **Community-run** - volunteer labour, thin print budget, care bought with attention: pre-sorted badges, a named person at the desk, a room signposted by hand.
- **Vendor or corporate-run** - paid staff, printed signage systems, a lead-capture expectation written into sponsorship contracts. Bigger machinery hides an attendee's confusion more easily, so the walkthrough audit matters more here, not less.

The axis that genuinely reshapes the menus is different: **whether the event has a registration gate at all.** With no gate - a legitimate posture at 8,000+ attendees (FOSDEM), not an omission - there is no badge, no list, no dietary match, no check-in queue, and the whole design collapses onto wayfinding and the help path. Ask Q2 before ranking anything.

## Workflow

1. **Write down what you may not move** - floor plan, grid, register, accessibility bar. Contradictions route to that sibling.
2. **Walk the journey on paper first.** One row per touchpoint from arrival to departure: [references/journey-audit-and-first-timers.md](references/journey-audit-and-first-timers.md). Design against the rows that come back bad.
3. **Design check-in.** Place the desk clear of the sponsor queue, pre-sort badges by last then first name, give walk-ins their own slower lane. Full mechanics: [references/checkin-badges-and-swag.md](references/checkin-badges-and-swag.md).
4. **Set the badge and scanning posture**, then execute it in the artifact itself - where the code is printed and how the lanyard hangs are part of the posture.
5. **Design the wayfinding** from the floor plan's decision points, not the building's rooms: [references/wayfinding-facilities-and-food.md](references/wayfinding-facilities-and-food.md).
6. **Locate the facilities**, designing the quiet room for both purposes in one pass - decompression and confidential intake.
7. **Execute the dietary bar** via one of two fulfilment models this skill deliberately refuses to rank (see reference) - your catering contract picks one.
8. **Build the help path**, and make whoever staffs it visibly identifiable.
9. **Design the first-timer's first twenty minutes** and the one moment worth remembering - both self-set.
10. **Walk the finished design in the actual building before doors open**, using the same rows from step 2, and record what you changed.

Show the user the floor-plan markup, the badge design and the signage list before anything is printed. A printed sign with the wrong room number is the one mistake you cannot fix at 09:00.

If your harness has persistent memory, record per edition:

- The longest check-in queue and the hour it happened.
- Which questions the help point actually received.
- Whether the quiet room was used, and for which of its two purposes.
- How many dietary-restricted meals went unclaimed or went to the wrong person.
- Every sign you added by hand on the day.

The hand-added signs are the wayfinding gaps your design missed.

## Check-in model

How an attendee gets from the door to being inside with the right badge. Ranking (default, not a law - Q1, Q2 and Q9 re-rank it):

- effort: `multi-lane staffed desk > pre-sorted pickup with a walk-in lane > single-table name-check > no registration at all`
- value: `multi-lane staffed desk > pre-sorted pickup with a walk-in lane > single-table name-check > no registration at all`
- compliance cost: `multi-lane staffed desk == pre-sorted pickup with a walk-in lane == single-table name-check > no registration at all`
- efficiency: `pre-sorted pickup with a walk-in lane > single-table name-check > no registration at all > multi-lane staffed desk`

Value and effort tie exactly, so no pair strictly dominates: whichever rung leads on value costs strictly more effort. The three staffed rungs carry equal compliance cost - same attendee list and data, differing only in headcount who holds it; no registration is the only honest zero. Full dominance-check reasoning is in [references/checkin-badges-and-swag.md](references/checkin-badges-and-swag.md).

- **Pre-sorted pickup with a walk-in lane** - the default: badges sorted alphabetically before doors open, a separate slower lane for walk-ins who still complete the full form. Highest value per hour since the sort happens the night before. Move up one rung once the door-open rush exceeds one queue, or a real ticket-category split exists.
- **Single-table name-check** - one volunteer, a printed or searchable list, a mark against each name. Buys a headcount, a name badge and a dietary match for one person's time.
- **Multi-lane staffed desk** - the starved option: tops effort and value together, so efficiency never picks it. **Promotion condition, keyed to Q10**: at scale, for a multi-day badge window, or wherever sponsor and regular tickets differ.
- **No registration at all** - a legitimate posture, not a gap, at 8,000+ attendees (FOSDEM). Removes the queue, the list and the data entirely, and costs you the headcount, badge, dietary match and identification the code of conduct leans on. Choose it deliberately.
- **Deleted, not demoted: one table doing check-in, swag, walk-in registration and questions at once.** It fails at exactly the busiest ten minutes of the day. Split the walk-in lane, move questions to the help point, or accept a queue out the door.

Full desk mechanics, including the ticket-category confusion the sort has to tolerate, are in [references/checkin-badges-and-swag.md](references/checkin-badges-and-swag.md).

## Badge and scanning posture

What is printed on the badge and what a machine can read off it. One rule sits above the menu: attendee contact lists are never given or sold to sponsors. Ranking (default, not a law - Q6 re-ranks it outright):

- effort: `QR on the badge's back with consent, opt-out and sponsor terms > UUID-only code > name badge with no machine-readable code`
- value: `QR on the badge's back with consent, opt-out and sponsor terms > UUID-only code > name badge with no machine-readable code`
- compliance cost: `UUID-only code > QR on the badge's back with consent, opt-out and sponsor terms > name badge with no machine-readable code`
- efficiency: `name badge with no machine-readable code > QR on the badge's back with consent, opt-out and sponsor terms > UUID-only code`

Value and effort run in the same order, so effort always outpaces value's lead. Compliance re-orders the menu but rescues no pair: UUID-only tops compliance cost despite protecting the badge itself, because a scan log handed to a sponsor re-identifies everyone in it, the exact act the rule above forbids. Full reasoning is in [references/checkin-badges-and-swag.md](references/checkin-badges-and-swag.md).

- **Name badge with no machine-readable code** - the default and the published stance: scannable badges are actively discouraged. The name alone identifies who belongs on site and doubles as an icebreaker. Zero exposure, zero build.
- **QR on the badge's back with consent, opt-out and sponsor terms** - the starved option: tops effort and value together, so efficiency never picks it first. Promote it the moment Q6 confirms a signed sponsorship agreement already promised lead capture.
- **UUID-only code** - an opaque identifier resolved only by the organizer. Protects the badge but moves the entire risk into what you do with the scan log afterwards.
- **Deleted, not demoted: attendee data encoded directly in the QR.** Every scanner in the building reads it, not only an authorized sponsor's - the same rung with the consent removed.

Full badge mechanics, both technical fallbacks and all four required mitigations, are in [references/checkin-badges-and-swag.md](references/checkin-badges-and-swag.md).

## Facility provision depth

How much of the venue you take out of circulation for people rather than programme. No compliance-cost axis: providing a room triggers no review - what it is used for does, and that sits in the code-of-conduct runbook. Ranking (default, not a law - Q1, Q5 and Q9 re-rank it):

- effort: `full wellness catalog > quiet room plus inclusion wayfinding on the map > designated quiet room with stated hours > venue's own facilities only`
- value: `full wellness catalog > quiet room plus inclusion wayfinding on the map > designated quiet room with stated hours > venue's own facilities only`
- efficiency: `designated quiet room with stated hours > quiet room plus inclusion wayfinding on the map > full wellness catalog > venue's own facilities only`

Value and effort are the same list, so every higher-value rung is strictly the costlier one; the ordering is argued, not verified. Full reasoning is in [references/wayfinding-facilities-and-food.md](references/wayfinding-facilities-and-food.md).

- **Designated quiet room with stated hours** - the default: one named room, located on the map, with published hours. Wins efficiency by a wide margin: it is the only rung the incident runbook depends on, serving as both decompression space and the private space a responder needs. Design it for both at once - a door rather than a curtain, findable without crossing the main thoroughfare, signed so ordinary use never looks like an incident.
- **Quiet room plus inclusion wayfinding on the map** - add colour-coded gender-neutral restrooms and mapped first-aid points. Cheap once the map is being drawn anyway.
- **Full wellness catalog** - the starved option: quiet room, nursing/wellness suite placed near registration, multiple mapped first-aid stations. Tops value and effort together, so efficiency never picks it first. **Promotion condition, keyed to Q11**: a multi-day event, an audience with caregivers, or when the accessibility bar already requires it.
- **Venue's own facilities only** - the floor: toilets and whatever hangout space remains. Not free: the code-of-conduct pipeline then has nowhere private to take a report.
- **Deleted, not demoted: a curtained corner of a hallway called the quiet room.** Satisfies neither purpose - no decompression, since it sits in the noise it exists to escape, and no confidential intake, since it has no door.

## Help path

Who answers "where is room B", "I lost my laptop bag", and "did the 14:00 talk move". Ranking (default, not a law - Q1 and Q9 re-rank it):

- effort: `split help desk plus on-call organizer > one desk absorbing everything > visibly identifiable staff with no desk > no named help point`
- value: `split help desk plus on-call organizer > one desk absorbing everything > visibly identifiable staff with no desk > no named help point`
- efficiency: `one desk absorbing everything > visibly identifiable staff with no desk > split help desk plus on-call organizer > no named help point`

Value and effort run in one order, so the rung ahead on value always costs more. No compliance axis applies: none of these rungs collect anything the registration list did not already hold. Give lost property a named owner and a stated end-of-event disposal, whichever rung you pick. Full reasoning is in [references/wayfinding-facilities-and-food.md](references/wayfinding-facilities-and-food.md).

- **One desk absorbing everything** - the default: a single infodesk covering room locations, scheduled-talk questions, practicalities and lost-and-found. Works at scale by centralizing rather than specializing. Move up one rung when the venue spans buildings, or the desk starts queueing behind lost property.
- **Visibly identifiable staff with no desk** - staff recognizable on sight, e.g. a bright t-shirt marked "Staff". Near-zero cost, works in a single-room venue. Fails once a question has an answer only one person knows.
- **Split help desk plus on-call organizer** - the starved option: a desk scoped to directions, lost-and-found and scheduling, a named organizer on duty for anything else, and someone owning proactive channel updates with buffer for follow-up questions. Tops effort and value together. **Promotion condition, keyed to Q12**: the code-of-conduct pipeline already requires a named on-duty responder.
- **No named help point** - questions still arrive, at whoever looks least busy. Last on efficiency, not first.
- **Deleted, not demoted: a chat channel as the only help path at a physical event.** Excludes everyone not in the channel and routes an in-person question through a device.

## First-time attendees

- **Make orientation opt-out, not opt-in.** Only the people who were already going to ask use an "ask us if you're new" sign. A line on the badge back, or a different lanyard colour offered rather than assigned, reaches the ones who would not. A first-timer ribbon picked up voluntarily at registration is published practice at professional conferences - ICMA's own attendee guide tells newcomers to pick one up at Registration - offered, never assigned, the same distinction this skill draws.
- **Answer the three questions nobody asks aloud**: where do I sit, is it acceptable to leave a talk partway, and what actually happens in the hallway track. Print them - they cost one side of one card.
- **Give the first twenty minutes a destination.** A first-timer's worst moment is the gap between badge and first talk, standing alone. Name a place to go, with a person in it.
- **A standalone welcome session and a one-to-one buddy pairing are two published shapes for that destination.** PyCon US runs a named Newcomer Orientation, a short workshop hosted by community organizers before the opening reception that covers how to get involved. Several professional-association conferences (NAPFA, the Electrochemical Society) instead pair each newcomer with a returning attendee one-to-one before the event. A single scheduled session suits a venue with one entrance and one corridor; a standing pairing programme scales past the room size a single session can hold.
- **Never build it as a separate track.** Anything that visibly segregates first-timers converts the awkwardness into a label they wear all day.

## Failure modes

- **Putting a scannable code on a badge against the published stance, with none of the mitigations.** The organizer usually discovers the exposure when a sponsor asks for the export. Decide the posture before the badges are designed, not after they are printed.
- **Collecting dietary restrictions and then not separating them at distribution.** A restricted meal sitting in the general line is taken by the wrong person, and the person it was for goes without. The collection is the easy half - the separate table with a printed name checklist is the half that fails.
- **Designing the quiet room for one of its two purposes.** A decompression space with no door cannot take a report - an incident room with a stigmatizing sign is not used for decompression. Both fail quietly, and neither skill finds out until the day.
- **Assuming wayfinding because the venue is "small".** Small venues generate the same number of decision points as large ones - they just hide them behind identical doors. Count the decision points on the floor plan, not the square metres.
- **Leaving first-timers to self-orient.** Assuming an informal community welcome covers the first twenty minutes is how that window stays uncovered. Design it, or accept that it is nobody's.
- **Designing the day from the room list instead of walking it.** The design that reads well on a floor plan is not the one that survives 400 people arriving in eleven minutes.
- **Absorbing a sibling's job because it is physically adjacent.** Staffing the desk, moving a break, renegotiating a room, writing the pre-event email, or building a VIP tier are each somebody else's skill - a VIP is a separate protocol track, never the top rung of this journey.

## Measurement

Everything below is self-set except the three completeness gates, and only becomes meaningful across editions.

- **Dietary fulfilment** (gate) - every attendee who declared a restriction received the meal that was ordered for them. No threshold - the number that matters is zero misses.
- **Consent-record completeness** (gate) - if any badge carries a machine-readable code, every scan-capable badge has a recorded consent and a working opt-out. The exception is the one that surfaces publicly.
- **Quiet-room dual-purpose check** (gate) - the room has a door, is findable without crossing the main thoroughfare, and is signed in a way that makes ordinary use unremarkable. Fail any one and it serves one purpose, not two.
- **Longest check-in queue, and the hour it happened** (self-set) - the single number that tells you whether the model in § Check-in model was the right rung.
- **Signs added by hand on the day** (self-set) - count them and keep them. Each one is a decision point your wayfinding design missed.
- **Peak moments** (self-set) - organizers systematically believe they deliver a memorable "peak moment" more often than attendees report having had one. Ask attendees whether they had one rather than assuming you provided it - see [references/journey-audit-and-first-timers.md](references/journey-audit-and-first-timers.md) for the full caveat against over-reading the correlation this is drawn from.

Pick two, write down what each would change next edition, and record both before the doors open.

## Invocation examples

- "600 people, one entrance, doors at 08:30. How do we run check-in without a queue down the street?"
- "A sponsor wants to scan attendee badges. What do we put on the badge, and what do we have to tell attendees?"
- "Where should the quiet room go, and does it need to be staffed?"
- "We collected dietary restrictions at registration. How do the meals actually get to the right people?"
- "It's a two-floor venue and people keep asking where things are. What signage do we need?"
- "Half our attendees have never been to a conference before. What do we do for them on the day?"

Expected output:

- A marked-up floor plan naming the check-in desk, the quiet room, the help point, the meal tables and the hallway-track space.
- A check-in model with its lane split and sorting rule.
- A badge design with a stated scanning posture and, where relevant, its consent and opt-out mechanics.
- A signage list keyed to decision points.
- A dietary distribution choreography.
- A first-timer orientation plan.
- A walkthrough audit table with the rows that came back bad.

Label every self-set element as such rather than presenting it as established practice.

## References

- [references/checkin-badges-and-swag.md](references/checkin-badges-and-swag.md) - the check-in desk's full mechanics with its ticket-category edge case, the badge privacy stance with both technical fallbacks and all four mitigations, and inclusive swag sizing and pickup.
- [references/wayfinding-facilities-and-food.md](references/wayfinding-facilities-and-food.md) - wayfinding and networking-space design as labelled self-set guidance, the facility catalog with the quiet room's dual-purpose spec, and the two published dietary fulfilment models with the ranking opt-out argued.
- [references/journey-audit-and-first-timers.md](references/journey-audit-and-first-timers.md) - the touchpoint row structure, the stage list, a worked walkthrough with a negative counterpart, and memorable-moment design as a self-set pattern.

Sibling skills referenced throughout: see § Seven siblings already own part of this day, plus `samber/dev-event-organizer-skills@event-hospitality` (the population-agnostic fundamentals this skill layers on rather than restates).
