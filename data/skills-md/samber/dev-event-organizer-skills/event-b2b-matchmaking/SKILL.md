---
name: event-b2b-matchmaking
description: Design a technical event's structured 1:1 business meeting program - whether to run one at all, how the two sides are matched (directory, brokering, mutual opt-in, scored ranking), how slots get booked inside the grid, what meeting quota a sponsor package may honestly commit to, how a booked-meeting no-show is absorbed, and what to measure. Use whenever asked to set up scheduled 1:1 meetings at an event, run buyer-seller or founder-investor matchmaking, promise a sponsor a number of meetings, or build a booked-meeting timetable. Matches two populations for business conversations. Do NOT use for hackathon build-team formation - use samber/dev-event-organizer-skills@hackathon-team-formation - or the expo floor - use samber/dev-event-organizer-skills@event-booth-experience.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event B2B Matchmaking

You design the mechanic that turns two populations at one event into scheduled 1:1 business conversations. Own the whole chain: whether the program runs at all, how the two sides are matched, how slots get booked and placed, what meeting number a sponsor package may honestly commit to, how a missed booking is absorbed, and what gets measured afterwards.

Answer no by default. Most community technical events correctly never run this, and "no meeting program at all" is a ranked, often-winning rung below, not a placeholder for organizers who have not got around to it yet. The program earns its place only when a signed package names a meeting number, or when the event has deliberately assembled two populations that will not find each other in a corridor.

## The nearest-sounding neighbour is a different job

`samber/dev-event-organizer-skills@hackathon-team-formation` also calls its menu matchmaking. It is a different mechanic, and conflating the two runs the wrong one:

- It matches hackathon participants **to each other**, one population, onto build teams. Its failure mode is a participant nobody picked.
- You match **two different populations** - attendees and sponsors, founders and investors, buyers and vendors - into a booked pair. Your failure mode is a sponsor whose promised count was not delivered, or an attendee ambushed by a meeting they never agreed to.

Neither mechanic substitutes for the other: a pitch-and-join round delivers no quota, and a booked grid forms no team. Route hackathon-team questions there and stop.

## Principles that hold everywhere

**Don't:**

- State or quote a meeting length, slot count, fill rate or no-show percentage. Every one of those is exactly the number that feels safe to invent here, and an invented number outlives the caveat attached to it.
- Carry a number from a previous edition of a different event. The only numbers this program may use are ones this organizer measured on this program.

Trade-show structure carries over only partly. What survives the move: two declared sides, a stated matching criterion, a bounded block of slots, a confirmation step, and a delivered-versus-promised count. Four things do not:

1. **The buyer/seller frame.** A trade-show attendee arrives expecting to be sold to; a developer attendee arrives to learn and treats an unsolicited vendor meeting as an interruption.
2. **Registration as consent to be contacted.** Large commercial shows often treat a badge as permission to be matched. At community events, sponsors get aggregate demographics, never names (DevOpsDays organizing guide).
3. **The dedicated meeting day.** Show matchmaking owns hours of the timetable outright. At a developer event the meeting block is a guest inside a grid built for sessions, and it loses every conflict.
4. **Vendor benchmark figures.** Fill rates and meeting counts published by matchmaking-platform companies are sales material. Never quote one. Brella, one such vendor, publishes a 1.5% no-show rate for a single high-volume partner against its own stated 20-30% industry average, and a 38-40% platform-wide meeting-acceptance rate. Both are that vendor's own numbers, from its own customer base, published to sell its own product, and never independently verified: a fact about the vendor's marketing, not a number this program may plan against.

Every ranking below is a default, not a law. Re-rank all four menus against what you already know. Each of these overturns a default rung:

- An opt-in profile form the registration flow already collects.
- A sponsor with their own target list.
- A room block already contracted.
- A staffed desk already rostered.
- Last edition's booked-versus-held count.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 9-11 exist because the menus below diverge sharply on effort, reversibility and time-to-effect - those defaults cannot be picked for the user.

1. Does a signed or drafted sponsor package already name a meeting number? If yes, that's an input to deliver, not a decision to take.
2. Are there genuinely two populations invited separately, or is this one audience with sponsors standing in it?
3. How many meeting pairs do you expect: a handful one person could hold in their head, or more?
4. What structured data do you already hold about each side, and from where - registration, an opt-in form, a sponsor's target list, nothing?
5. What did each side actually consent to - being contacted by sponsors, appearing in a directory, neither? From the wording they saw, not what you intended.
6. Where do meetings physically happen and who owns that space?
7. Where in the published grid does the meeting block sit, and is it already fixed?
8. Is anyone staffed at the meeting area during the block, or does it run unattended?
9. By what date must booking open, and by what date must the schedule stop moving?
10. One-off or recurring - do you hold measured numbers from a previous edition of _this_ program?
11. Effort ceiling: organizer hours during booking and on the day, and political capital for telling a paying sponsor their meetings aren't available?

## Workflow

1. **Decide whether this program runs at all** (Q1, Q2). Without a named number or a genuine two-population structure, say so and stop.
2. **Write down what you may not move**: the signed meeting number, published grid, consent wording each side saw, floor plan, room block. Contradictions route to the sibling that owns them.
3. **Pick the matching mechanism**, and write the matching criterion as a sentence before writing any form: [references/matching-and-slot-mechanics.md](references/matching-and-slot-mechanics.md).
4. **Settle consent before collecting anything.** Retrofitting after a directory is live is the one error here that cannot be undone.
5. **Pick the scheduling mechanic** and lay the block inside the grid you were given, never across a session.
6. **Set the quota commitment posture** before the package is sold, if you still can: [references/quota-commitment-and-evidence.md](references/quota-commitment-and-evidence.md).
7. **Choose the no-show handling**, and confirm every pairing with both sides before the schedule is published.
8. **Publish one meeting brief**: matching criterion, block placement, how to book, what happens to a missed slot, one named organizer on duty.
9. **Run the block**, recording what happened per pair: booked, held, empty, replaced.
10. **Hand the outcome downstream** as one generic record. Per-sponsor tracking and renewal reporting belong to `event-sponsor-fulfillment`, never built here.

If your harness has persistent memory, record per edition: the matching criterion used, pairs booked, meetings held, slots left empty, which side cancelled, and every complaint about an unwanted meeting. The held-versus-booked count is the only number this program may ever plan against, and it exists only once you have measured it yourself.

## Matching mechanism

How a pair comes to exist. Five rungs, and the first one is real. Ranking (default, not a law - Q2, Q3 and Q4 re-rank it):

- effort (setup, per-pair organizer hours during the booking window, and whether the job is dated or standing): `organizer brokering > scored ranking > mutual opt-in > open directory > no meeting program`
- value, quota certainty (you can promise a specific number of meetings against stated criteria and deliver it): `scored ranking > mutual opt-in > organizer brokering > open directory > no meeting program`
- value, per-meeting relevance (both sides would take the same meeting again): `organizer brokering > mutual opt-in > scored ranking > open directory > no meeting program`
- compliance cost (the review collecting and sharing this data triggers, and how little of it can be undone): `scored ranking > open directory > organizer brokering > mutual opt-in > no meeting program`
- efficiency: `mutual opt-in > open directory > no meeting program > scored ranking > organizer brokering`

Two of these orderings are argued rather than asserted, and the full pairwise dominance check (10 pairs, zero strict-dominance relations) is in [references/matching-and-slot-mechanics.md](references/matching-and-slot-mechanics.md) § Ranking derivations.

- **No meeting program at all** (default) - correct at most community-run events; the hallway track and expo floor already cover this. Promote to mutual opt-in the moment Q1 names a meeting number or Q2 confirms two populations invited separately.
- **Mutual opt-in** - the efficiency leader once the program runs: both sides state what they want; a pair exists only where both opted in.
- **Open directory** - an opt-in participant list people browse and request against. Cheap, but beaten on value and compliance by the two rungs above - only one side of every pair chose.
- **Scored ranking** - the organizer scores fit from structured profile data and pushes ranked recommendations. Tops quota certainty. Promote when structured, comparable profile data already exists on both sides from something collected anyway.
- **Organizer brokering** - a named person hand-pairs from stated interests. Tops relevance and effort. Promote when the expected pair count is small enough for one person to hold in their head.
- **Deleted, not demoted:** any pairing where only one side opted in - handing a sponsor a list to book against. The mechanic behind every ambushed-meeting complaint.

## Scheduling mechanic

How a pair that exists becomes a slot on a day. Ranking (default, not a law - Q7, Q9 and Q11 re-rank it):

- effort (grid construction, conflicts resolved against sessions, messages per participant, reversibility once published): `organizer-assigned grid > hybrid > self-service booking > no booked slots`
- value, delivered quota (the promised number of meetings actually happens, with counterparts meeting the stated criteria): `organizer-assigned grid > hybrid > self-service booking > no booked slots`
- value, attendee autonomy (an attendee keeps control of their own day and never finds a meeting on it they did not choose): `no booked slots > self-service booking > hybrid > organizer-assigned grid`
- efficiency: `self-service booking > no booked slots > hybrid > organizer-assigned grid`

The delivered-quota axis is rank-identical to inverse effort - a warning, not a result. Autonomy is the axis that carries the menu, and the one a sponsor-facing organizer is most likely to forget.

No compliance-cost axis applies here: nothing on this menu collects data or takes on an obligation the matching and quota menus have not already taken on. Full dominance check (6 pairs, zero strict-dominance relations) in [references/matching-and-slot-mechanics.md](references/matching-and-slot-mechanics.md) § Ranking derivations.

- **Self-service booking against published availability** - the default and efficiency leader: each side states when it is free, the counterpart books, and the organizer publishes the block and nothing more. Every meeting on an attendee's day is one they chose. **Promote to hybrid the moment Q1 names a contracted number** - self-service delivers meetings but cannot guarantee a count.
- **No booked slots** - the introduction is made and the calendar is theirs. Tops autonomy at zero effort. Honest wherever the program's purpose is the introduction rather than the meeting, and the only rung that survives a grid with no block in it at all (Q7).
- **Hybrid** - contracted quota slots pre-assigned by the organizer, remaining capacity self-service. The smallest construction that guarantees a number. Its cost: the pre-assigned half is the half an attendee did not choose, so every pre-assigned pair needs an acceptance step before it appears on any schedule.
- **Organizer-assigned grid** - the organizer constructs every pairing and slot, and each side confirms. Tops delivered quota and effort, bottoms autonomy. **Promotion condition, keyed to Q2:** both populations were invited specifically to meet each other and neither has another reason to be in the building.
- **Deleted, not demoted: a meeting placed on someone's schedule without their acceptance.** It is the only way to manufacture quota out of people's time, and it produces the exact failure the quota was meant to prevent: a meeting nobody accepted is a no-show already on the schedule.

## Quota commitment posture

What a sponsor package may honestly promise. You design the commitment's shape; `samber/dev-event-organizer-skills@event-sponsor-agreement` drafts the clause and `samber/dev-event-organizer-skills@event-sponsor-value-proposition` decides whether the benefit is worth selling at all. Ranking (default, not a law - Q1, Q4 and Q11 re-rank it):

- effort (delivery machinery, criteria you must verify, per-pair tracking, and the remedy you must be able to fund): `guaranteed count with criteria > guaranteed count > best-efforts target > no meeting promise`
- value, price the package can carry (what the certainty is worth to the buyer): `guaranteed count with criteria > guaranteed count > best-efforts target > no meeting promise`
- value, renewal survivability (the promise still looks honest to that sponsor after the event, whatever happened on the day): `no meeting promise > best-efforts target > guaranteed count with criteria > guaranteed count`
- compliance cost (the review a written commitment triggers, and how little of it can be undone once countersigned): `guaranteed count with criteria == guaranteed count > best-efforts target > no meeting promise`
- efficiency: `best-efforts target > no meeting promise > guaranteed count with criteria > guaranteed count`

The compliance `==` is argued, not a dodge: both rungs are a countersigned number the organizer must deliver or remedy, so both trigger the same contract review and both are equally hard to walk back once signed. Adding criteria changes what you have to verify on the day, an effort question, not a review the tie would hide.

The price axis is rank-identical to inverse effort, exactly as on the previous menu - renewal survivability is what makes this menu decidable. Full dominance check (6 pairs, zero strict-dominance relations) in [references/quota-commitment-and-evidence.md](references/quota-commitment-and-evidence.md) § Ranking derivations.

- **Best-efforts target** - the default: a stated number framed as an intention, no remedy attached, criteria written down anyway. It survives a miss because it never claimed to be a guarantee. **Promote to a guaranteed count with criteria when Q1 names a contracted meeting number and Q4 says you hold data good enough to verify the criteria.**
- **No meeting promise** - the sponsor gets access and the program runs on its merits. Tops renewal survivability: a promise never made cannot be broken. Correct wherever the matching menu landed on its own default rung.
- **Guaranteed count with criteria** - a number of meetings with counterparts meeting stated criteria, plus a defined make-good. Tops price and effort together. Promote under the condition above. Its make-good must be something you can actually deliver after the event has ended - the constraint organizers discover too late.
- **Guaranteed count** - a bare number with a make-good and no criteria. Last on efficiency, and the easiest rung to satisfy dishonestly: fill it with whoever is free; the sponsor gets the number and the wrong people; their post-event judgment is worse than if you had promised nothing.
- **Deleted, not demoted: a meeting number printed in a prospectus with no criteria and no stated make-good.** A number with nothing behind it is the same commitment with the remedy left to be improvised in front of an unhappy sponsor. One boundary holds regardless of rung: sponsorship buys placement and access, never program influence - "No sponsor should be able to buy their way into the program" (DevOpsDays organizing guide, carried in this collection by `samber/dev-event-organizer-skills@event-sponsor-value-proposition`). A meeting quota is access; it never becomes a speaking slot, a judging outcome, or a share of the agenda.

## No-show handling for booked meetings

What happens when a confirmed slot goes unfilled. Ranking (default, not a law - Q8 and Q10 re-rank it):

- effort (messages sent, desk staffing during the block, and a rate you must have measured yourself): `slot overbooking > standby refill > reconfirm-and-remind > nothing`
- value, quota protected (booked meetings that actually happen, against the number promised): `slot overbooking > standby refill > reconfirm-and-remind > nothing`
- value, counterpart experience (nobody sits at an empty table, and nobody who booked correctly is turned away): `standby refill > reconfirm-and-remind > nothing > slot overbooking`
- efficiency: `reconfirm-and-remind > standby refill > nothing > slot overbooking`

Quota protected is again rank-identical to inverse effort. Counterpart experience does the work, and its one surprise is that doing nothing outranks overbooking: an empty table disappoints one person who turned up, while a collision turns away someone who did everything asked of them. Full dominance check (6 pairs, zero strict-dominance relations) in [references/quota-commitment-and-evidence.md](references/quota-commitment-and-evidence.md) § Ranking derivations.

- **Reconfirm-and-remind** - the default: an explicit acceptance at booking time, and a reminder before the block. The only rung that reduces the no-show rather than absorbing it, at the cost of two messages.
- **Standby refill** - a per-counterpart standby queue, drained on the day into an emptied slot. Beats the default on both value axes; only effort blocks it. **Promotion condition, keyed to Q8:** someone is already staffed at the meeting area during the block - the queue is worthless unattended.
- **Nothing** - a missed meeting is a missed meeting. Honest wherever the quota menu landed on no promise and Q8 says the block runs unattended.
- **Slot overbooking** - more meetings booked than slots, against an expected show-up rate. Tops protected quota and effort, and is the only rung that creates a new failure mode instead of absorbing an old one. **Conditional delete, keyed to Q10:** when you hold no measured booked-versus-held count from a previous edition of this same program, delete it - the first-edition case and most other cases. The event-level show-up bands in `samber/dev-event-organizer-skills@event-no-show-management` are a different unit; borrowing them here is the specific mistake this rule exists to stop.
- **Deleted, not demoted: a deposit, a forfeited benefit, or any penalty on the attendee side of a missed meeting.** `samber/dev-event-organizer-skills@event-no-show-management` already argues against deposits; a meeting slot changes nothing, and here it additionally puts a price on a conversation you invited the attendee to have.

## Failure modes

- **Running the program because the mechanic is interesting.** No signed number, no second population, and now the corridor competes with a booking form. Fix: workflow step 1 is a real gate, and its answer is usually no.
- **Collecting the data first and deciding the sharing rule afterwards.** Consent scope is fixed at the moment someone submits a form, not at the moment you decide what to do with it. Fix: Q5 before any collection, and read the wording they actually saw.
- **Quoting a fill rate or a no-show percentage.** Companies selling matchmaking software publish the figures in circulation, against their own definitions. Fix: describe the mechanic honestly and report your own counts afterwards.
- **Letting the meeting block move a session.** The grid belongs to `samber/dev-event-organizer-skills@event-schedule-design`, and a meeting block is a guest inside it. Fix: take the block's placement as given, or route the request there rather than resolving it yourself.
- **Delivering a number with the wrong people in it.** The bare-count rung makes this easy and the sponsor will notice afterwards, not during. Fix: write the criteria down even on a best-efforts target, where they cost nothing and still shape who gets matched.
- **Rebuilding `samber/dev-event-organizer-skills@event-sponsor-fulfillment`'s job.** A per-sponsor tracking matrix, a payment gate, a renewal report. Fix: you publish one meeting brief and one outcome record; they are executed and reported per sponsor elsewhere.
- **Treating a booked-meeting no-show as an event no-show.** Different unit, different population, different remedy, and the sibling's figures do not transfer. Fix: measure your own.

## Measurement

Everything below is self-set and only becomes meaningful across editions of your own program.

- **Held against booked** (self-set) - the single number this program plans against next time. Nothing else may be used as its substitute.
- **Booked against promised** (self-set, per sponsor) - the only number that says whether a quota commitment was met. Report it per sponsor, never as an average across sponsors.
- **Mutual-acceptance rate** (self-set) - requests where both sides accepted, as the closest available proxy for relevance. It is a proxy; say so when you report it.
- **Empty-slot count** (self-set) - slots that were booked and then held nobody. Each one is a place the no-show menu's rung was too light.
- **Unwanted-meeting complaints** (gate) - the target is zero, and any non-zero count means a pairing reached someone's schedule without their acceptance. Treat it as a defect in the matching or scheduling rung, not as attendee behaviour.
- **Confirmation completeness** (gate) - every pair on the published schedule was accepted by both sides before publication. No threshold; the number that matters is zero unconfirmed.

## Invocation examples

- "A sponsor wants us to guarantee them 15 meetings with engineering leaders. Can we?"
- "We're inviting 20 startups and 10 investors to the same day. How do the meetings get arranged?"
- "Should our community conference run a 1:1 meeting program at all?"
- "Half the booked meetings didn't happen. What do we change next edition?"
- "How do we match attendees to sponsors without handing over an attendee list?"

Expected output:

- A stated yes/no on running the program at all.
- A named matching mechanism with its matching criterion written as a sentence and its consent wording.
- A scheduling mechanic with the meeting block placed inside the grid you were given.
- A quota commitment posture with criteria and, where committed, a make-good you can fund.
- A no-show handling rung.
- One meeting brief plus one outcome record.

Every self-set element is labelled as such, and no meeting length, slot count, fill rate or no-show percentage is stated anywhere.

## References

- [references/matching-and-slot-mechanics.md](references/matching-and-slot-mechanics.md) - the matching criterion as a written sentence, the profile field list and what each field is for, the consent wording checklist, the four matching-rule shapes as run sheets, slot-block construction against a grid you do not own, and a positive and negative worked pair.
- [references/quota-commitment-and-evidence.md](references/quota-commitment-and-evidence.md) - the four commitment shapes as language you can hand to `samber/dev-event-organizer-skills@event-sponsor-agreement`, the make-good catalog with what each one costs you after the event, the qualification-criteria worksheet, the meeting brief and the outcome record, and the measurement definitions with their counting rules.

See also, same collection:

- `samber/dev-event-organizer-skills@event-sponsor-agreement` - drafts the meeting-quota clause and its remedy; this skill decides the commitment's shape, never its wording.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - executes and reports per signed sponsor, and owns lead-capture posture; a booked meeting never substitutes for one.
- `samber/dev-event-organizer-skills@event-booth-experience` - owns the expo floor and organic booth traffic; a different mechanic from booked-and-confirmed meetings.
- `samber/dev-event-organizer-skills@event-schedule-design` - owns the published grid the meeting block sits inside; this skill places slots within it, never moves a session.
- `samber/dev-event-organizer-skills@event-attendee-experience` - owns the general attendee journey and the deliberately unscheduled hallway track; a booked meeting program is the opposite posture.
- `samber/dev-event-organizer-skills@event-sponsor-prospectus` - assembles the document a signed meeting number would be printed in; no guarantee clause of any type appears in any sourced real prospectus, the same finding behind this skill's "deleted, not demoted" rung for a bare meeting number with no criteria or make-good.
