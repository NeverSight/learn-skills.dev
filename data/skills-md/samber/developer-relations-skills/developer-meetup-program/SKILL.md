---
name: developer-meetup-program
description: Designs and runs a recurring developer meetup or user group - purpose and host model, format menu, cadence, a standing speaker pipeline, in-kind venue and food sponsors with their conduct limits, no-show planning, the attendee-to-co-organizer ladder, and a health scorecard. Use whenever someone mentions starting a developer meetup or user group, dying meetup attendance, finding meetup speakers, getting a venue or pizza sponsor, how often to meet, RSVPs who never show, or handing the meetup over - even if they only say "we want to do local events". Covers independent, vendor-backed and company-staffed groups. Not for speaking at a conference - use samber/developer-relations-skills@conference-cfp-submission.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Meetup Program

You are an experienced user-group organizer. The user wants a developer meetup that still happens in eighteen months, with a room that keeps coming back - not a single great evening.

A meetup is a subscription, not an event. Optimize everything for the twentieth edition, not the first: a cadence the team can hold when tired, a speaker pipeline that fills itself, a cost base that survives a lost sponsor, and enough shared ownership that the founder can miss a month.

Scope is the recurring program. These sibling skills cover adjacent tasks:

- Submitting a talk to someone else's event: samber/developer-relations-skills@conference-cfp-submission
- Structuring a talk: samber/developer-relations-skills@tech-talk-outline
- De-risking a demo: samber/developer-relations-skills@developer-live-demo-design
- Buying a sponsor slot at another organizer's event: samber/developer-relations-skills@developer-event-sponsorship
- An online community space: samber/developer-relations-skills@developer-community-launch
- Full-scale conference production, once the program outgrows an evening: samber/dev-event-organizer-skills

Typical invocations:

- "we want to start a Rust meetup in Lyon"
- "attendance dropped from 40 to 12, what do we do"
- "I need a format that doesn't need two speakers every month"
- "write the sponsor ask for a venue"
- "I'm burning out, how do I bring in co-organizers"

## How to read the numbers

Every figure in this skill is one of two kinds:

- **Sourced** - published by a named organizer program, marked inline with its source (CNCF Community Groups, DevOpsDays, the Orbit Model, Nielsen).
- **Baseline** - set by this skill, marked "baseline".

Say which kind a number is whenever you quote one: a baseline presented as an industry standard costs the user's trust in the whole plan. Replace each baseline with the group's own trailing median after three editions. Where every figure comes from: [./references/evidence-and-benchmarks.md](./references/evidence-and-benchmarks.md).

## Interview

Ask one question at a time, multiple-choice where possible, and skip whatever the user has already answered. Questions 1-7 gate the design: do not propose a format before they are answered.

1. Is this a new group or an existing one? If existing: how many editions so far, and what is the attendance trend?
2. Who is the room - technology, seniority, and whether they attend on work time or their own time?
3. Who hosts: an independent community group, a vendor-backed chapter, or a company running the series itself?
4. What does success look like in a year - a live local ecosystem, hiring, product feedback, adoption, your own reputation? Name the first one.
5. By what date must the next edition happen - a fixed date you are already committed to, or an open horizon?
6. Do you want one good evening, or a program still running in two years?
7. How many organizers are there today, and what is the standing effort ceiling - hours a month each can hold on a tired month, not in the launch burst?
8. City, expected headcount for edition one, and do you already have access to a room?
9. What budget exists, if any, and who signs for it?
10. Which channels already reach these developers - an existing Slack/Discord, a company list, a neighboring meetup, a university?
11. Do you have two speakers you could ask today? Names, not categories.
12. Anything fixed you must design around - a language, a sponsor commitment, a venue's closing time, a company mandate?

If the answer to 7 is "just me", say so plainly: a solo group is one job change from dead.

- CNCF Community Groups: minimum two organizers, divided responsibilities.
- DevOpsDays: at least three organizers, from different organizations.

Recruit the second organizer within the first three editions, not "later".

Carry questions 5, 6 and 7 into the Step 3 ranking, and say which answer moved which format:

- A fixed near date (Q5) promotes the formats needing no confirmed speaker - study group, open space - because sourcing is the one lead time you cannot compress.
- A two-year mandate (Q6) promotes anchor + lightning, the only format that manufactures the speakers later editions run on.
- A low standing ceiling (Q7) deletes the hands-on workshop outright, and rules out the two-talk classic until the pipeline board holds two editions ahead, whichever the room would prefer.

## Step 1 - Write the charter before booking anything

Write a one-page charter. It settles the arguments that otherwise resurface every edition:

- Who the room is for.
- What happens in a typical evening.
- How often it happens.
- Who decides the program.
- What the group refuses to do.

Name exactly one primary outcome, not a list. For a company-hosted program, use CMX's SPACES model as the vocabulary: support, product feedback, acquisition and advocacy, content and contribution, engagement, or customer success, following its own instruction to "just focus on one objective" when starting out.

That single named outcome is also what gets the program funded internally. For an independent group, apply the same discipline without the business framing: one reason the evening exists, agreed by the organizers.

Present the charter in sections and get each validated before moving on. See [./references/program-charter-template.md](./references/program-charter-template.md) for the exact shape and a filled example.

If your environment has persistent memory, store the charter, the venue and sponsor contacts, and the running edition log. Start the next edition from that file, not from the organizer's memory of what worked.

## Step 2 - Host model and audience

Two axes change almost every downstream decision. Name both out loud rather than leaving them implicit.

**Name who runs the room.** Three models exist, and they are traditions rather than rungs of a ladder: vendor-affiliated user groups (SHARE, 1955) predate the independent volunteer model by two decades.

No efficiency ranking applies across the three. The model is settled by who is asking, at interview question 3, before any effort or value gets weighed: an independent group cannot decide to be vendor-backed, and a vendor cannot decide to be neutral, so ranking a choice nobody makes would be false precision.

Pick the one that already describes you; each is a different contract with the room:

- _Independent, vendor-neutral group_ - sponsors buy logistics, never airtime; competitors are welcome on stage. CNCF caps organizer teams at 50% from any one company to protect exactly this.
- _Vendor-backed volunteer chapter_ - local volunteers run the room; the vendor supplies branding, platform and speaker access but does not staff it (HashiCorp User Groups: 50,000 members across 184 groups - HashiCorp's own figures).
- _Company-staffed series_ - company staff run every stop, no local volunteer organizer (CMX's Circuit Tour). This buys consistency and loses the local ownership that makes volunteers stay.

One real choice sits inside this, and only for a company that has already decided to fund a series: back local volunteers, or staff every stop itself. Effort here is the standing hours company staff must hold for every edition in every city, and how reversible the model is once the room depends on it.

- efficiency: `vendor-backed volunteer chapter > company-staffed series`
- effort: `company-staffed series > vendor-backed volunteer chapter`
- compliance cost: `company-staffed series > vendor-backed volunteer chapter`

- The chapter costs a quarter of recruiting local organizers, then near-zero standing hours; the series is a standing job for staff at every stop, forever, and it stops the month the budget does. Local ownership is also the thing that makes volunteers stay, and a staffed series buys that out without getting it back.
- What this order starves: the company-staffed series - the only model that delivers a consistent evening in a city with no volunteers to recruit. Promote it when the date is fixed and no local organizer exists yet, then convert to a chapter later; a staffed series can hand over to volunteers, but a chapter cannot be un-handed.
- Read the compliance line as the review each triggers: a staffed series runs on company systems, so attendee data, the code of conduct and anything said from the stage carry company legal and brand sign-off; a chapter inherits the vendor's neutrality rules - CNCF's 50%-per-company organizer cap and its escalation path - and the organizers apply them themselves.

Whichever model applies, keep at least one slot per edition for a speaker with no stake in the host's product, or accept that attendance decays to customers only. The full comparison table, per-model risks, and CNCF's escalation path for neutrality violations: [./references/host-model-variants.md](./references/host-model-variants.md).

**Name the audience.**

- B2B/enterprise room: attendance is a work decision. Schedule inside or adjacent to work hours, expect employer-provided venues, and make the topic defensible on a timesheet.
- Individual-adoption audience (hobbyists, students, indie developers): evenings and weekends work, travel budget is zero, food matters more, and the hook is the technology itself.

Format mechanics, speaker sourcing, no-show handling and the participation ladder work identically for both.

A sharper cut applies when a company hosts:

- Developer-first (B2D) business: the attendee is frequently the buyer, so product-adjacent topics carry no tension.
- Developer-plus business: the attendee is one segment of a much larger buying org, so justify the program as brand and ecosystem investment, not pipeline.

The operational mechanics per side are not documented in any source found for this skill - derive them with the user rather than asserting a standard.

## Step 3 - Format and rhythm

Offer the top two or three of the ranking below with their trade-offs and a recommendation, then let the user choose. The right pick is the one the team can repeat when tired, not the most ambitious one. The ordering is this skill's judgement, not a sourced finding.

- **Effort** - what recurs every edition: speakers to source and confirm, and organizer preparation hours. Never the cash cost, which is pizza in every format.
- **Value** - a room that comes back, plus the speakers a format creates for later editions.

- efficiency: `anchor + lightning > study group > two-talk classic > open space > hands-on workshop`
- value: `anchor + lightning > two-talk classic > hands-on workshop > study group > open space`
- effort: `two-talk classic > hands-on workshop > anchor + lightning > study group == open space`

- **Anchor + lightning** - one 25-minute speaker plus 5-minute slots. Leads both lines: one confirmed speaker per edition instead of two, and every lightning slot is a candidate anchor speaker for a later edition, so the format pays back into Step 4's pipeline. Effort: one confirmed speaker, plus an hour recruiting and reassuring first-timers.
- **Study group** - the group works through a book, course or spec together (CNCF lists study groups as a valid meetup style). Ranks second on efficiency purely on its denominator: near-zero recurring effort, and it holds a small room together while the group grows. Caps out - it will not grow a room past the people already committed.
- **Two-talk classic** - 20-30 minutes each. Highest-drawing format for a general audience, and the only one that puts two speakers' networks behind one announcement. Effort: two confirmed speakers every edition, forever - a standing sourcing job, and the single most common way a cadence collapses.
- **Open space / unconference** - attendees propose the agenda on the night. Near-zero preparation, but it needs a room already used to each other, so its value is close to zero until then.
- **Hands-on workshop** - 60-90 minutes, laptops required. Deepest engagement of the five and the best format for tool adoption, but it costs a week of preparation and a facilitator per edition, which is why the ratio puts it last.

- Justify the effort tie: a study group and an open space both need no speaker confirmed in advance and no material the organizers prepare - each costs the room booking and the announcement, nothing more. They differ sharply on value, not on effort.
- Default to anchor + lightning for a new or rebuilding group.
- What this order starves: the two-talk classic, the strongest draw of the five, which the ratio never picks because its sourcing load recurs every edition. Promote it once the pipeline board holds two editions ahead (Step 4) - that is the moment its worst axis collapses, not a matter of taste.
- Delete rather than demote, and say which you deleted: the open space for edition one and for any group whose room has not met before, and the hands-on workshop wherever the answer to interview question 7 was under a day a month per organizer.
- No compliance-cost line: none of the five changes what the group owes anyone. Code of conduct, sponsor stage-time caps and the attendee-list rule apply identically to every format and are handled in Step 5.
- Treat this ordering as a default, not a law: it shifts with the room and with who runs it. Re-rank against what you already know - a room that already knows each other promotes the open space to first, a group with a standing internal speaker bench cancels the two-talk classic's only weakness, and a facilitator who teaches for a living makes the workshop cheap.

Then fix the rhythm. A recurring, predictable slot ("second Tuesday, 19:00") beats date-shopping each month: it becomes a habit and removes one decision per edition. Tuesday-to-Thursday evenings after work is CNCF's stated default for working developers, adjusted to local culture.

Set cadence on CNCF's published thresholds:

- Ideal cadence: monthly.
- Inactivity: **more than 90 days between events marks a chapter inactive**.
- Minimum meetings: technical groups must meet **at least six times a calendar year**.
- Active status: a quarterly event with **more than 10 attendees - attendees, not registrations**.

Below quarterly, a group has occasional events rather than a program. Do not commit to monthly with two organizers and no speaker pipeline - a missed edition costs more trust than a slower cadence.

See [./references/format-catalog.md](./references/format-catalog.md) for the full format menu, per-format time budgets, and a minute-by-minute run of the evening.

## Step 4 - Build a speaker pipeline, not a monthly panic

The recurring failure of meetups is sourcing a speaker three weeks out, every month, forever. Build a pipeline that runs two editions ahead (baseline).

1. Open a **standing call for proposals** - a permanent form linked from every event page and announcement, not a monthly plea (CNCF best practice).
2. **Harvest conferences**: someone who gave a talk at a regional conference can repeat it locally with zero new preparation. Ask them the week of the conference, while it is fresh.
3. **Manufacture speakers from the room**: lightning slots, then a full talk.
4. **Trade with neighboring groups**: their speakers, your speakers, cross-promoted audiences.
5. **Vet the content, not the person.** Ask for the title, the takeaway and the slides in advance - CNCF names slide pre-review as the defense against a talk that turns out to be a pitch. A deck arriving the night of the event is how a group discovers on stage that the talk was a product demo.

Keep a visible pipeline board with confirmed, provisional and prospect speakers per date.

See [./references/speaker-pipeline.md](./references/speaker-pipeline.md) for sourcing channels, an invitation message with a weak and a strong version, first-time-speaker support, and the pitch filter.

## Step 5 - Venue, food and sponsors

At meetup scale sponsorship is usually in kind, not cash: a company lends a room after work and pays for food. Keep the cost base low enough that losing a sponsor costs an edition's pizza, not the group.

Offer the sponsor:

- Recognition on the listing.
- A thank-you from the stage.
- A small table, if they want to talk to people who approach them.
- **At most 15 minutes of stage time** (CNCF best practice).

DevOpsDays is stricter at its own scale: "a short elevator pitch … generally in the order of a minute or two". Pick a cap, publish it, and hold it.

Two limits are absolute, whatever the model:

- **Never a speaking slot in exchange for money.** DevOpsDays states it flatly: "no speaker spots can be bought by sponsors: not ever - period."
- **Never the attendee list.** DevOpsDays: "devopsdays does not ever distribute attendee contact information." People opt in to a badge scan if the sponsor offers something, and not by default.

On food: provide vegan and vegetarian options and label allergens (CNCF).

Rotate venue hosts where possible. A single host that also employs half the organizers turns the group into that company's user group whether or not anyone intended it.

See [./references/sponsor-and-venue-playbook.md](./references/sponsor-and-venue-playbook.md) for the venue requirements checklist, the in-kind ask template, cost lines, and the conduct rules to state up front.

## Step 6 - Promotion and the no-show plan

Free RSVPs are cheap, so a share of them will not turn up. Plan on roughly **30% no-shows** - CNCF's published planning figure, and the only no-show number with a named organization behind it; the 40-50% often repeated for free evening events is folklore. Calibrate on your own door count after three editions rather than trusting any benchmark, including CNCF's.

- **Overbook** to the no-show ratio and run a waitlist that auto-promotes.
- **Remind** two days and two hours before, and explicitly ask people who cannot make it to release their spot. Frame it as freeing a seat for someone else, not as guilt.
- **Count heads at the door.** Attendance, not registrations, goes in the log - every threshold and trend in this skill depends on the real number, and CNCF's own activity bar is written in attendees for the same reason.
- **Promote the speaker and the topic**, not the venue or the food (CNCF marketing guidance). The talk is the reason people come; the pizza is the reason they stay.
- **Announce early**, across the group listing, adjacent meetups, community channels, local newsletters, and the speaker's own network - a speaker who shares their slot brings their audience.

See [./references/promotion-and-no-show-plan.md](./references/promotion-and-no-show-plan.md) for the reminder schedule, the overbooking arithmetic worked through, and a weak-versus-strong announcement pair.

## Step 7 - Retention, the ladder, and succession

Attendance retention is not a marketing problem. People come back to a room where they know someone and where there is a path upward.

Move people up this ladder: **attendee → regular → lightning speaker → volunteer → co-organizer**, each rung recruited from the one below. The ladder is this skill's mapping of the Orbit Model's four community levels - Explorers → Participants → Contributors → Advocates, with gravity defined as love × reach. Orbit was published in 2019 and is no longer actively developed; cite it as a stable framework, not a live product.

- Make first-timers visible and welcomed - a raised hand at the start, an organizer who introduces them to one person, name tags.
- Ask regulars directly. "Would you do five minutes on what you built?" converts far better than an open call, which only reaches people who already consider themselves speakers.
- Give volunteers real ownership (food, A/V, emcee, socials), one or two areas each.
- Recruit co-organizers publicly and on a low bar. CNCF does this through a public issue - nomination or self-nomination, approved when at least 50% of current organizers comment in favor - and handles departures the same way, which is what stops silent exits leaving ghost owners on accounts.

Calibrate expectations with Nielsen's participation inequality (90-9-1, published 2006): about 90% of any community lurks, 9% contribute occasionally, 1% produce most of the activity. A room where only a handful of people ever step up is normal, not a failure of your program; the lever is lowering the barrier to the next rung, not "converting the lurkers".

Design succession from day one, not as an emergency response:

- Shared ownership of the listing, mailing list, socials and any payment account.
- A written run-of-show anyone can follow.
- A public, unembarrassing exit path so a departing organizer says so instead of quietly going silent.

Between editions, keep one channel alive and run a 15-minute co-organizer debrief after every event, feeding the next edition's plan.

## Deliverable

Produce, in this order:

1. **Program charter** - one page, the template in [./references/program-charter-template.md](./references/program-charter-template.md).
2. **Edition plan, three editions deep** - a table with date, format, speaker status, venue, sponsor status, promotion dates.
3. **Speaker pipeline board** - confirmed, provisional and prospect per date; the board shape is in [./references/speaker-pipeline.md](./references/speaker-pipeline.md).
4. **Edition log skeleton** - the empty table the organizer fills the night of each event; columns and filled rows in [./references/program-charter-template.md](./references/program-charter-template.md).
5. **Scorecard baseline** - the Measurement table below with the group's current values or "not measured yet"; a healthy and a failing example, read line by line, are in [./references/program-charter-template.md](./references/program-charter-template.md).

Mark anything beyond edition three as provisional - say so rather than inventing a year of programming nobody has committed to.

## Measurement

Track these per edition in one running log. The trend across editions is the signal; a single edition tells you about the weather.

| Signal                              | Target                              | Basis                                                                |
| ----------------------------------- | ----------------------------------- | -------------------------------------------------------------------- |
| Attendance at the door              | Stable or rising over 3 editions    | Baseline (this skill); CNCF counts attendees, not registrations      |
| Show-up rate (attended ÷ RSVP)      | ≈ 70%                               | Arithmetic on CNCF's ~30% no-show figure, not an independent finding |
| Repeat attendance                   | ≥ 40% of attendees have been before | Baseline (this skill)                                                |
| New faces per edition               | > 0, every edition                  | Baseline (this skill)                                                |
| Speakers sourced from the room      | ≥ 1 in 3                            | Baseline (this skill) - ambitious against Nielsen's 90-9-1           |
| Editions confirmed ahead            | ≥ 2                                 | Baseline (this skill)                                                |
| Organizer count and employer spread | ≥ 2 people, ≥ 2 employers           | CNCF (min 2, ≤50% one company); DevOpsDays (≥3, different orgs)      |
| Gap since last edition              | ≤ 90 days                           | CNCF inactivity threshold                                            |
| Attendees per edition               | > 10                                | CNCF active-chapter bar                                              |

## Pass threshold

A program is healthy when all six hold. Fix the failing line before adding scale, a bigger venue, or a second format.

1. No gap longer than 90 days, and at least six editions planned or held per year (both CNCF).
2. At least two editions have confirmed speakers (baseline).
3. Door attendance is stable or rising across the last three editions, and above 10 per edition (CNCF bar).
4. Repeat attendance is at least 40%, with new faces every edition (baseline).
5. At least two organizers, from at least two different employers, with shared account access (CNCF).
6. No edition where a sponsor exceeded the published stage-time cap or the room got a pitch it did not sign up for (CNCF/DevOpsDays).

See [./references/program-charter-template.md](./references/program-charter-template.md) for a filled scorecard, including a failing one read line by line.

## Failure modes

| Failure                | What it looks like                                                                                 | Fix                                                                                |
| ---------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Founder-shaped group   | One person owns the listing, the room and every decision                                           | Recruit a co-organizer from the regulars in the first three editions               |
| Monthly speaker panic  | Sourcing starts three weeks out, every time                                                        | Standing CFP plus a two-edition pipeline board                                     |
| Vendor capture         | Host company fills every slot; competitors stop coming                                             | One non-host speaker per edition, minimum                                          |
| Pizza-first promotion  | Announcements lead with food and venue                                                             | Lead with speaker and topic; food is a footnote                                    |
| RSVP theater           | Planning on registrations, ordering food for 60, feeding 25                                        | Plan on ~30% no-shows, then use your own measured rate                             |
| Format overreach       | A workshop every month with two organizers                                                         | Downgrade to a repeatable format; ambition costs cadence                           |
| Room full of strangers | High attendance, no repeat, nobody talks                                                           | Structured welcome, name tags, deliberate introductions, protected networking time |
| Cadence collapse       | "We'll do the next one when we find a speaker"                                                     | Fix the slot, book the room, then fill the program                                 |
| Silent decline         | Attendance halves and nobody names it                                                              | Log the door count every edition and read the trend out loud at the debrief        |
| Quiet handover failure | Departing organizer stops answering; accounts locked                                               | Shared ownership from day one, plus a stated exit path                             |
| Borrowed benchmark     | An organizer quotes this skill's 40% repeat-attendance baseline to a sponsor as an industry figure | Quote only sourced numbers externally; call every baseline "our target"            |

## References

- See [./references/format-catalog.md](./references/format-catalog.md) for formats, time budgets and the run of the evening.
- See [./references/speaker-pipeline.md](./references/speaker-pipeline.md) for sourcing, invitation examples and the pitch filter.
- See [./references/sponsor-and-venue-playbook.md](./references/sponsor-and-venue-playbook.md) for venue requirements, in-kind asks and sponsor conduct rules.
- See [./references/promotion-and-no-show-plan.md](./references/promotion-and-no-show-plan.md) for reminders, overbooking arithmetic and announcement examples.
- See [./references/host-model-variants.md](./references/host-model-variants.md) for the three host models, the B2D/developer-plus split and listing-platform considerations.
- See [./references/program-charter-template.md](./references/program-charter-template.md) for the charter, the edition log and a worked scorecard.
- See [./references/evidence-and-benchmarks.md](./references/evidence-and-benchmarks.md) for every figure in this skill with its source or its baseline label.
