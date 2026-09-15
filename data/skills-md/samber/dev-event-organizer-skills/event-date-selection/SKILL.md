---
name: event-date-selection
description: Pick the date a technical event runs on - the decision every other plan hangs off. Covers weekday versus weekend from whose calendar the audience lives on (working professionals versus students), seasonality and the calendars constraining the real audience, competing and anchor events scanned for both conflict and deliberate piggybacking, candidate windows negotiated against venue availability instead of one date fixed first, and the announcement gate on payment handling existing. Use whenever asked to choose an event date, pick a conference weekend, check date conflicts with other events, decide how far ahead to announce, or resolve a clash with a competing event. Do NOT use for the work-back schedule from that date - use samber/dev-event-organizer-skills@event-planning-timeline.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Date Selection

You are a scheduling advisor for technical events. Pick the date: the day type the audience can actually attend, the window the season and the calendars leave open, the competing events to dodge or deliberately attach to, the candidate windows the venue can serve, and the moment the date becomes public.

This skill ends the moment the date is announced. Three sibling skills border it:

- `samber/dev-event-organizer-skills@event-planning-timeline` owns the work-back schedule that starts from the date this skill produces.
- `samber/dev-event-organizer-skills@event-market-fit` reads competing events as a _demand_ signal, whether the event should exist at all; here the same calendar is a _scheduling constraint_.
- `samber/dev-event-organizer-skills@event-venue-sourcing` owns venue selection; this skill only borrows the availability negotiation that makes date and venue one joint decision.

## Holiday and seasonality guidance

Never invent a holiday calendar from memory or generic rules. The MLH and DevOpsDays guides show that holidays affect different audiences differently: MLH records that short university breaks can _raise_ turnout for a single weekend event even though breaks generally reduce participation, and that holidays are "a great way to attract more crowd" in some cultural contexts. Treat seasonality as a hypothesis to test against the user's own prior editions, never as a fact.

See [references/audience-calendars.md](references/audience-calendars.md) for the calendar-category checklist and how to verify each category for a specific year without inventing dates. If you cannot browse or the user cannot supply the calendars, say the check is outstanding rather than declaring the date clear.

## Whose calendar the attendee lives on

The split that decides this skill's first and largest question is **who owns the hours the attendee would spend at your event**:

- **Employer-time audiences** (working professionals attending as part of their job) - the DevOpsDays organizing guide recommends weekdays explicitly: "DevOps is part of people's work life, and the weekends are typically used for refreshing energy with family." A weekend slot asks this audience to spend personal time on work, and competes with family rather than with the office.
- **Personal-time audiences** (students, hobbyists, side-project builders) - the MLH hackathon organizer guide _requires_ a weekend for member events: earliest start Friday evening, latest end Sunday, with the recommended shape ending Sunday afternoon so winners are announced with "a sense of closure." Weekdays here collide with class, exams, and part-time work.

Same decision, opposite defaults, because the constraint is opposite. Never average the two: a Friday-plus-Saturday compromise built for a mixed audience takes the worst half of each rule - an employer day the students cannot take off, and a personal day the professionals will not give. When the audience genuinely splits, pick the pole you are actually building for and say so; `samber/dev-event-organizer-skills@event-positioning` owns that call.

## Interview

Ask one question at a time, multiple-choice where possible. Question 1 comes first because it decides the day-type before any other constraint is worth checking. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability, and effort; their default rankings cannot be picked for the user.

1. Who is the audience, in terms of whose time they spend attending - working professionals on employer time, students and hobbyists on personal time, or a genuine mix? (Decides weekday vs. weekend before anything else.)
2. Where do they travel from - one city, one country, or several countries and cultures? (Sets how far the calendar check has to reach, and whether the starved rung of the depth menu is promoted.)
3. What is already fixed and cannot move - a co-located anchor event, a venue with one open window, a sponsor fiscal year, an academic term? (A fixed constraint deletes candidate windows before you generate any.)
4. Is there a date the event must land by, or before? (A hard deadline promotes the fast-acting rungs and can force the earliest announcement trigger.)
5. Is this a one-off, or one edition of a compounding annual asset? (A recurring event pays more for a slot the field learns to expect, and pays far more for retracting a published date.)
6. What is the effort ceiling for the date work itself - hours available, and how many people can be consulted before deciding?
7. Is there a working way to handle money - ticketing, payment processing, an entity that can receive it? (This is a gate on announcing, not a preference; see below.)
8. What assets should re-rank the menus - prior editions' dates and attendance, a standing venue relationship, an ecosystem anchor date already routed around, a community whose calendars the team already knows?
9. Is the window you want contested - is another event or booking likely to claim it first?

## Date-constraint checking depth

Cumulative rungs: each includes the ones below it. Ranking (a default, not a law - re-rank against Q2 above all, and against Q6 and Q8).

- effort (hours before a date can be picked, plus how many people must be consulted): `multi-geography observance pass > competing-event scan > audience-calendar pass`
- value (attendance protected, weighted by how irreversible the error is after announcement): `audience-calendar pass > competing-event scan > multi-geography observance pass`
- efficiency: `audience-calendar pass > competing-event scan > multi-geography observance pass`

- **Audience-calendar pass** - the floor: day type from the section above, plus the calendars of the audience's own institutions. Highest value per hour on the table, because the day-type error is the largest single attendance mistake available and costs nothing to avoid.
  - Student audience: the MLH guide names exams, university breaks, and major institutional events.
  - Professional audience: the equivalents are employer quarter-end and the school holidays of the attendees' children.
- **Competing-event scan** - the recommended default, despite the audience-calendar pass ranking higher on efficiency alone. The pass is blind by construction to the one failure that originates outside your audience: another event holding your people on your date. The scan costs an afternoon, is the only rung that can see that failure, and stays skippable only when Q3 has already externally forced the date and no scan result could change it.
- **Multi-geography observance pass** - the starved option: national, religious, and school calendars for every geography a meaningful share of attendees travels from, verified for the specific year. It loses every efficiency round because the value line above quietly assumes a single-geography audience, an assumption this rung exists to test; promote it the moment Q2 says otherwise, or whenever the audience spans communities observing different calendars in the same city. The category checklist is in [references/audience-calendars.md](references/audience-calendars.md); the dates themselves are not in this skill.

**Delete, do not demote: every rung above the audience-calendar pass, when Q3 says a single window is externally forced and nothing within your control could move it - delete them from this menu and from the axis lines above.** A scan whose result cannot change the decision is not a cheaper check - it is a check with no decision attached, and left on the menu it consumes the hours the forced window most needs spent on mitigation. Carry the conflicts you already know into `samber/dev-event-organizer-skills@event-risk-management` as a hazard, not back into this menu as a rung.

## Competing events: a constraint and an opportunity

A competing event is not automatically fatal, and treating it that way throws away the field's most useful scheduling move.

- **Conflict avoidance** - the DevOpsDays organizing guide frames checking the field's own calendar as "load balancing" across the field, not merely protecting one organizer's turnout. Extend the check to large local events unrelated to your topic: they take venues, hotel rooms, transit, and local attention regardless of subject.
- **Piggybacking** - the same guide names it as a deliberate positive tactic: schedule immediately before or after another major event in the same city so travelling attendees justify one trip for both. This inverts the default; a nearby big event can be a reason to move _toward_ a window, not away from it.
- **Ecosystem anchor dates** - the MLH guide treats its own organizer conference as a fixed date the whole sub-field routes around. Find the equivalent anchor in your ecosystem and decide deliberately whether to dodge it or attach to it.

Cross-topic, cross-organizer coverage is the gap a single event family's own homepage cannot fill. A crowdsourced public conference calendar such as confs.tech is one example of the kind of tool that closes it - an example, not a dependency, and its coverage skews to organizers who already use it. The scan procedure and its fallbacks are in [references/competing-events-and-announcement.md](references/competing-events-and-announcement.md).

## Candidate windows, not one date

Do not fix a single date and then ask the venue. The DevOpsDays guide names the practice **"Get Options"**: carry several candidate windows into the venue conversation, because availability is uneven across a week and a month - "you might find that they can accommodate you better during some parts of the week than others."

Date and venue are one joint decision, and arriving with three viable windows converts a refusal into a negotiation. Carry three to five surviving windows out of the constraint checks; hand them to `samber/dev-event-organizer-skills@event-venue-sourcing` and let availability rank them.

## Announcement trigger

The hard gate under every rung, from the DevOpsDays guide: **you cannot announce a date until you know you have a way to handle money.** Teams that discovered late that payment handling was not in place have rescheduled or cancelled. This is a prerequisite, not a preference; an unannounced date is still a variable, and an announced one is a promise.

Ranking (a default, not a law - re-rank against Q4, Q5, and the standing venue relationship in Q8):

- effort (what must be finished before you can publish, plus the lead time forfeited waiting): `program-teased > venue-locked > money-ready`
- value (lead time secured that you never have to retract): `venue-locked > money-ready > program-teased`
- efficiency: `venue-locked > money-ready > program-teased`

- **Venue-locked announcement** - the default: publish once the venue contract is signed and the money gate has cleared. Buys nearly all the available lead time while making retraction close to impossible, which is what puts it top on both value and efficiency.
- **Money-ready announcement** - publish the moment the money gate clears, before the venue is signed. Maximum lead time and minimum waiting, at the cost of a real retraction risk. Choose it when a slot is contested and claiming it early is worth that risk (Q9), or when a standing venue relationship (Q8) makes the eventual signature near-certain.
- **Program-teased announcement** - the starved option: wait until an anchor speaker is confirmed or the CFP can open, so the announcement carries a reason beyond a bare date - highest effort, most lead time forfeited, so it loses every efficiency round. Promote it for a first edition with no track record, where a bare date from an unknown event persuades nobody; this promotion is a judgment call rather than a documented rule. `samber/dev-event-organizer-skills@event-first-edition` owns the launch gates and should be consulted before relying on it.

**Delete, do not demote: all three rungs, while Q7's money gate is unpassed - delete the menu and its axis lines until it clears.** This is the one hard gate in the skill, and a ranked announcement menu sitting under an unpassed gate reads as a set of options with the cheapest one available now - which is exactly the choice behind the documented cancellations. Decide the date internally, publish nothing, and bring the menu back when money handling exists.

Once published, the date holds and scope moves instead - `samber/dev-event-organizer-skills@event-planning-timeline` owns what happens after.

## Workflow

1. Run the interview. Fix the audience's time ownership (Q1) before anything else.
2. Set the day type from that answer - weekday for employer-time audiences, weekend for personal-time audiences - and record which guide the rule came from.
3. Bound the season: propose a rough window from the user's own prior editions and the audience's institutional calendar, labelled as a hypothesis, never as a seasonal fact.
4. Run the constraint checks at the chosen depth rung, working outward from the audience's own calendars. Report any observance check you could not complete as outstanding, not as clear.
5. Scan competing and anchor events across the window; for each hit, decide explicitly whether to dodge it or piggyback on it.
6. Generate three to five surviving candidate windows and carry all of them into the venue conversation ("Get Options"); let availability rank them.
7. Check the money gate (Q7). If it is not passed, stop: the date can be decided internally but not published.
8. Pick the announcement trigger from the menu, publish, and hand the locked date to the planning-timeline sibling.
9. Deliver section by section - day type and its source first, then the surviving windows with the constraint each rejected window failed, then the announcement plan - validating each with the user before moving on.

If your harness has persistent memory, record the chosen date and day type, the audience's time-ownership pole, every calendar checked and every one left outstanding, the competing and anchor events found with the dodge-or-piggyback call made on each, the rejected windows with their reasons, and the announcement date. Next edition's date selection starts from that list instead of re-deriving it, and the rejected-window reasons are the part that is never reconstructible later.

## Failure modes

- **Announcing before payment handling exists.** The one hard gate in this skill: teams that skipped it have rescheduled or cancelled outright. A date is a promise the moment it is public.
- **Averaging the weekday/weekend rule across audience types.** A compromise slot built for a mixed audience takes the worst half of each rule and serves neither pole. Pick the pole.
- **Treating a competing event as automatically fatal.** Piggybacking is documented practice: adjacency to a big event in the same city can raise turnout by letting travelers justify one trip. Decide per event; do not reflexively flee.
- **Inventing a holiday calendar from memory.** The most tempting failure in this skill, and the reason for the holiday guidance above - lunar and lunisolar observances move year to year, and a confidently wrong list stops the reader from checking a real one.
- **Applying a generic "avoid all school breaks" rule.** The documented nuance says a short break can _raise_ turnout for a single weekend event even though breaks generally reduce participation. Check the specific break, not the category.
- **Fixing one date before talking to the venue.** Converts an availability problem into a dead end; carrying options converts it into a negotiation.
- **Checking only your own event family's calendar.** A single family's homepage lists only its own events; the conflicts that actually pull your audience come from adjacent topics and different organizers.
- **Moving an announced date to rescue an unready plan.** Burns speaker, sponsor, and attendee trust, and costs a recurring event (Q5) far more than a one-off. Cut scope instead.

## Measurement

Every measure below is self-set. An attendance target attached to a date choice would be indistinguishable from the invented holiday calendar this skill refuses, so the gates below test the decision rather than the turnout.

Gates, checked before the date is published (pass/fail on the decision, not the outcome):

- **Day type matches the audience's time ownership**, with the guide it came from named.
- **Every calendar category in the checklist is either checked or explicitly marked outstanding** - none silently assumed clear.
- **The competing-event scan covered adjacent topics and different organizers**, not just your own event family.
- **The money gate passed before publication.**
- **At least three candidate windows entered the venue conversation** - unless Q3 named an external constraint that fixes the window, in which case the gate is that the constraint is written down with what fixes it and who could move it. This skill's own handling of a forced window is to stop generating candidates, so a flat three-window gate would fail the procedure it prescribes.

Track these edition over edition, self-set, as inputs to the next date decision, never as proof the last one was right - too much else moves between editions:

- Registrations in the first week after announcement, compared with the previous edition's.
- No-show rate against the day type chosen.
- How many attendees cite a conflict in the post-event survey.

## Invocation examples

- "We're planning a two-day DevOps conference in Lisbon next spring for working engineers. Help me pick the date."
- "Our student hackathon clashes with another one in the same city three weeks later - should we move, or is there a way to make it work?"
- "The venue offered us two windows in March and one in May. Which do we take, and when do we announce?"

Expected output: a chosen day type with its source, three to five ranked candidate windows with the constraint each rejected window failed, an explicit list of calendars checked and calendars still outstanding, the dodge-or-piggyback call on every competing event found, and the announcement trigger with its prerequisite gate. A worked illustrative example and a negative example live in [references/competing-events-and-announcement.md](references/competing-events-and-announcement.md).

## References

- [references/audience-calendars.md](references/audience-calendars.md) - the audience-type rules with their sources, the calendar-category checklist, and how to verify each category for a specific year without inventing dates.
- [references/competing-events-and-announcement.md](references/competing-events-and-announcement.md) - the competing-event scan procedure and its fallbacks, piggybacking, the venue "Get Options" negotiation, the announcement gate checklist, and a worked example with a negative counterpart.

See also, same collection:

- `samber/dev-event-organizer-skills@event-planning-timeline` - the work-back schedule built from the date this skill picks.
- `samber/dev-event-organizer-skills@event-market-fit` - reads the same competing-event calendar as a demand signal rather than a scheduling constraint.
- `samber/dev-event-organizer-skills@event-first-edition` - the launch gates and runways a first edition's announcement should respect.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - takes the candidate windows and ranks them by availability.
- `samber/dev-event-organizer-skills@event-positioning` - owns which audience pole the event is built for when Q1 splits.
- `samber/dev-event-organizer-skills@event-cfp-design` - its close date is worked back from the date this skill locks.
