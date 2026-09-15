---
name: event-run-of-show
description: Write and run the day-of run of show for a technical event once the schedule is published - the minute-by-minute playbook staff execute from, day-of role assignment (MC, speaker introducers, room leads, the organizer on duty), cue sheets at every transition, an organizer-only comm channel kept separate from attendee-facing ones, the escalation path and live incident response, shift rotation with verified handoffs, and closeout. Use whenever the user mentions a day-of rundown, a cue sheet, MC or room-lead roles, organizer radios or Slack channels, shift handoffs, or deciding live what to cut when a session overruns - even if they never say "run of show". Do NOT use to build the grid itself - use samber/dev-event-organizer-skills@event-schedule-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Run of Show

You own the day itself. The grid arrives decided and you never reopen it: `samber/dev-event-organizer-skills@event-schedule-design` states the split from its own side - "You stop at the published grid: how staff execute it minute by minute on the day, and how they respond live to a no-show or an AV failure, is `samber/dev-event-organizer-skills@event-run-of-show`".

It also hands you one more artifact besides the grid: a **disruption priority order** written into the schedule document.

1. Protect the plenary or keynote first.
2. Protect the headline commitment the audience showed up for next.
3. Minimize how many other sessions the fix disturbs.
4. Lock the revised grid for the rest of the block.

Consume that order. Do not re-derive one under pressure.

`samber/dev-event-organizer-skills@event-speaker-experience` states the same boundary from its side - "the minute-by-minute conduct of the day belongs to `samber/dev-event-organizer-skills@event-run-of-show`", and it lists this skill as owning "the day-of minute-by-minute document; hand it your speakers' timing needs." Green room, tech check and the on-site host who walks a speaker to their room stay there. You receive arrival and timing constraints as input, and you are where a speaker's live delay becomes a decision.

Two more boundaries:

- `samber/dev-event-organizer-skills@event-risk-management` authors the standing register and the printed emergency plan: which scenarios, which contacts. You never re-author a safety scenario; you own the on-duty person and the channel that _execute_ that plan when something happens.
- `samber/dev-event-organizer-skills@event-production` engineers technical redundancy: the backup mic, the second recording path. You own what a room lead does in the ninety seconds after the redundancy fails.

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank all three menus against what you already know. Each of these can overturn a default rung:

- Radios the event already owns.
- A venue basement with no signal.
- A volunteer team that has run this day four times.
- A room that started late every hour last edition.
- A hard briefing deadline.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-7 exist because the menus diverge sharply on time-to-effect, durability and effort - those orderings cannot be picked for the user.

1. What is the published grid, and did the schedule document arrive with a disruption priority order? If not, get it before writing anything (see workflow step 1).
2. How many rooms or stages run at once, and what staffed posts exist besides them - registration, production, info desk, a sponsor hall?
3. Who is actually on the day, and in what shifts? Volunteers, organizers, paid crew, venue staff. This is an input from `samber/dev-event-organizer-skills@event-volunteers`, not something you build.
4. Does mobile coverage hold everywhere staff will be, and does the venue run its own comms you have to join rather than talk over?
5. What is the last moment you can still change something - print the cue sheet, add a person to a shift, brief a room lead? That deadline, not the event date, is what the menus are ranked against.
6. One-off edition or a recurring event? A recurring event promotes the rungs whose payoff lands after this day ends: a reusable cue-sheet template, a written handoff format, recorded turnover times.
7. What is the effort ceiling - who writes and maintains this document, in how many hours, and how many people can be on duty rather than doing a job?
8. Does a printed emergency plan already exist, and who is named on it? If not, that is `samber/dev-event-organizer-skills@event-risk-management`'s work and it blocks you.
9. What already exists that should re-rank the menus: last edition's overruns, radios you own, a basement with no signal, a team that has run this before, a room that always starts late?
10. Is the opening recorded or livestreamed, and does any sponsor contract fix wording that must be read verbatim?

## Community-run or vendor-run: tested, and it splits only part of this

The community-run versus vendor-run split holds for one part of the day and fails for the rest.

**It holds for hosting.** DevOpsDays writes "one or more MCs" - plural, as a legitimate design, not a fallback. That is a real fork:

- **Community pole:** distributes hosting among organizers who already embody the event's norms, against no set playbook. Plan a rotation of organizer-hosts and a separate speaker-introducer per session.
- **Vendor pole:** treats hosting as a named craft with a briefed and rehearsed single host. Practitioner guidance there covers scripting to the culture and rehearsing together beforehand. It also covers the discipline that "the first 90 seconds set the tone for the entire event" (guidance from professional-host services that sell MC work, so read it with that interest in mind). Plan one host, one script, and one rehearsal, and let cue-sheet depth move up a rung on its own.

**It fails for everything else.** A transition takes the same seconds to execute, a radio reaches the same distance, and a handoff drops the same context whoever paid for the venue.

What actually changes the rest of the work is **how many staffed posts run at once and whether anyone on duty is also doing a job**. A single-room meetup where three organizers see each other all day needs no channel architecture at all. A four-room day needs one before it needs anything else.

Say which pole or which scale a recommendation assumes whenever they differ.

## Workflow

1. Take the published grid and the disruption priority order. If the schedule document has no priority order, go get one rather than inventing it - the ordering is a program decision, and improvising it at 14:00 with a hall full of people is how a keynote gets cut to save a sponsor slot.
2. Collect the inputs the day depends on: the shift plan, every speaker's arrival and timing constraint, the venue's own windows and staff, and the printed emergency plan with the names on it.
3. Assign the day-of roles (see below) by name, not by function. "A volunteer" is not an owner.
4. Build the cue sheet at the depth the menu picks, working from the grid outward - a row per segment and per transition, not a row per hour.
5. Set the comm channel architecture and write the two escalation paths onto the cue sheet itself: the routine one (a staffed post hits something above its authority) and the incident one (which triggers into the emergency plan, which you do not rewrite).
6. Build the on-duty rotation and the handoff format. Publish who is on duty for every block on the cue sheet, where a volunteer at a registration desk can read it without asking anyone.
7. Brief everyone against the document, not around it. The briefing is where you find out that two rows assume the same person is in two rooms.
8. Run the day. At each transition, execute the cue: queue position, tech ownership, spoken line (see below).
9. When something breaks, run the live disruption sequence (see below) rather than deciding fresh.
10. At each shift change, complete the handoff before the outgoing person leaves - including the live channel check.
11. Close out: the last segment, the venue handback, and the same-day capture of what the document got wrong.

Present the run of show section by section for validation - roles, then the cue sheet, then comms and escalation, then the rotation - before it is printed and briefed. After printing, every change costs a person who is holding the old version.

If your harness has persistent memory, record:

- Which rows turned out wrong.
- Which transitions ran long.
- Where the comm channel failed.
- Who was actually reachable.
- The venue's own comms and coverage facts.

A venue you use twice is worth not re-learning.

## The day-of roles

Three roles come from published organizer guides. The fourth is one you define yourself, and it is labelled where it appears.

- **MC** (sourced) - kicks off and orchestrates the event. One or more; splitting the duty across people is named practice, not a compromise.
- **Speaker introducer** (sourced) - a _separate_ role from the MC, assigned per session. The MC orchestrates the whole event's flow; somebody else handles the per-session task of introducing whoever is next. Collapsing the two is a named failure mode below.
- **Organizer on duty** (sourced) - the named person who takes last-minute decisions for a block, and the target of the routine escalation path. Sourced explicitly as single-point-of-failure mitigation for crisis decision-making, not as a fairness rota.
- **Room lead** (a role you define yourself) - one person per room who owns that room's clock: holds a start, cuts a Q&A, gets the tech owner, and escalates to the on-duty organizer. Published practice assumes per-room ownership without fixing what that person may decide, so define its authority explicitly in your own document - what it may do alone, and what it must escalate.

## Cue-sheet depth

Ranking (default, not a law - Q5, Q6, Q7 and Q9 re-rank it):

- effort (hours writing, rehearsal, per-segment arithmetic, coordination at the briefing): `word-for-word MC script > per-slot execution budget > scripted transitions > timed grid with named owners`
- value, a day that runs without dead air or a dropped handover: `scripted transitions > per-slot execution budget > timed grid with named owners > word-for-word MC script`
- value, what the audience remembers of the opening and the closing: `word-for-word MC script > scripted transitions > timed grid with named owners == per-slot execution budget` - argued tie: neither an owner column nor a setup-and-swap number changes a single word anybody hears. Both buy a day that runs, not a moment anyone recalls.
- efficiency: `timed grid with named owners > scripted transitions > per-slot execution budget > word-for-word MC script`

- **Timed grid with named owners** - the default: every segment and every transition gets a start time, a named owner and a room. Near-zero, because the grid already exists and you are adding a column. Move up one rung the moment any block hands over faster than the buffer absorbs - lightning talks, demos, back-to-back sponsor slots - or the moment more than one room runs at once.
- **Scripted transitions** - what physically happens at each handover: where the next presenter stands, who owns the tech, and the line that gets said out loud. This is the sourced mechanic, drawn from a rapid-fire format and generalizing to any tight transition; the mechanics and a worked row are in [references/cue-sheet-anatomy.md](references/cue-sheet-anatomy.md).
- **Per-slot execution budget** - budget the setup-and-swap tax inside slots that carry live execution risk, instead of assuming the published slot length covers it. The one sourced worked example budgets ten minutes per team for a live demo: three minutes of demo, one to two of questions, and the remaining five to six for setup and swapping to the next team - more than half the slot spent on neither. Present it as that event's number for that format, never as a constant.
- **Word-for-word MC script** - the starved option: every line written and rehearsed. It tops the memorability axis and tops effort, so efficiency never picks it. **Promotion conditions, keyed to Q10**: a single hired or briefed host rather than distributed organizer-hosting, a recorded or livestreamed opening, sponsor lines that must be said exactly as contracted, or a first edition where nobody has done this before and reading beats improvising.
- **Delete, do not demote:** the attendee-facing published schedule used as the staff document. It names no owner, no transition and no tech, and leaving it on the menu is how a day ends up being run off the public agenda by whoever is holding a phone.

## Comm-channel architecture

The sourced pattern is structural, not a product: one coordination channel reserved for the organizing team, kept separate from every population-facing channel - including the channel attendees use to _reach_ organizers, which is a different, public space that organizers merely monitor. The source implements this on a chat platform because it describes a hackathon; the split carries over to radios, a phone group, or three people who can see each other. Name the medium your event actually has.

Ranking (default, not a law - Q2, Q4 and Q9 re-rank it):

- effort (hardware, setup, discipline to teach people who have never used it, message volume to manage): `radio net with call signs > role-addressed channels > text-plus-live pair > single organizer channel`
- value, a message reaches the right person during a live problem: `radio net with call signs > role-addressed channels == text-plus-live pair > single organizer channel` - argued tie: each buys exactly one split of the same undifferentiated stream, one by function and one by urgency, and which split helps depends on whether your day's confusion runs along roles or along noise. Neither reaches anybody who is out of signal.
- value, a handoff or a post-event review has something to read: `text-plus-live pair > role-addressed channels > single organizer channel > radio net with call signs`. Radio leaves nothing behind, which is exactly why it sits last here and first above.
- compliance cost (the review it triggers, and what is hard to undo): `radio net with call signs > single organizer channel == text-plus-live pair == role-addressed channels` - argued tie: all three sit on a platform the event already accepted terms for when it opened its attendee channels, so none triggers a review that has not already happened. The radio rung is the only one that does - check whether the band is licence-free in your jurisdiction and whether the venue runs a net you must join rather than talk over. A channel plan agreed after the radios arrive is the hard thing to undo.
- efficiency: `single organizer channel > text-plus-live pair > role-addressed channels > radio net with call signs`

- **Single organizer channel** - the default: one coordination space for the organizing team, structurally separate from every attendee-facing channel. Move up one rung as soon as anyone on duty will be away from a screen, or as soon as shifts change hands and the incoming person needs to read what happened.
- **Text-plus-live pair** - a written channel that leaves a log and a live one for real-time coordination. The sourced setup recommends exactly this pair, and it costs one extra channel.
- **Role-addressed channels** - separate channels per function (rooms, registration, production) alongside the org channel. Buys precision, costs everyone deciding where each message goes and someone watching four windows.
- **Radio net with call signs** - the starved option: tops reach and tops effort, and its discipline is yours to write - call signs, channel assignment by role, push-to-talk etiquette, and what happens when a channel is jammed. Promotion conditions: a venue where mobile coverage fails, a multi-floor or multi-building footprint, staff whose hands are full, a message volume where a text channel scrolls faster than anyone reads, or a venue that already runs a net you have to join.
- **Delete, do not demote:** the attendee-facing channel used for organizer traffic. It broadcasts who is panicking about what to the people it is about, and it buries the one message the on-duty person needed under everyone else's. Parking it at the bottom is how it comes back at 09:00 when the org channel has not been created yet.

## On-duty rotation and handoffs

The rotation follows published organizer practice; everything below about _how_ a shift changes hands is borrowed from on-call engineering practice - carry the structure, never its tooling or its figures. Full mapping in [references/shift-handoff-protocol.md](references/shift-handoff-protocol.md).

Ranking (default, not a law - Q3, Q6 and Q7 re-rank it):

- effort (people committed, minutes of two people's attention per change, roster complexity): `paired on duty > timed overlap with live verification > written handoff checklist > named on-duty person per block` - the overlap outranks the checklist because it contains it: the window is spent writing _and_ talking, and it needs both people standing in the same place at the boundary, which a checklist written and left behind does not.
- value, the incoming person knows what they inherited: `paired on duty > timed overlap with live verification > written handoff checklist > named on-duty person per block`
- value, no single person is the point of failure for a crisis decision: `paired on duty > named on-duty person per block > timed overlap with live verification == written handoff checklist` - argued tie: neither changes how many people can make the call, only how well the next one is briefed. The named rotation outranks both because that is precisely the mechanic the source names for this failure.
- efficiency: `named on-duty person per block > written handoff checklist > timed overlap with live verification > paired on duty`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations.** Clean only by construction, and by-construction is never a pass. Two mechanisms block the six:

- **Four fail on effort:** the rung ahead on briefing quality costs strictly more, including the overlap-against-checklist pair, where the overlap leads on briefing, ties on single-point-of-failure, and still costs more.
- **The other two** (overlap against the named rotation, and checklist against the named rotation) are blocked by opposed value axes, since the rotation is the only cheap rung that addresses who can make the call.

Neither reason is evidence. The ordering below is argued.

- **Named on-duty person per block** - the default and the sourced practice: publish who is on duty for every block, on the cue sheet, where a volunteer at a post can read it without asking. Move up one rung wherever a change of hands can land during a live problem, or wherever the outgoing person leaves the building at the boundary.
- **Written handoff checklist** - a fixed set of sections with a mandatory-entry rule: nothing is complete until every section has an entry or an explicit "none". The explicit "none" is the load-bearing part - it separates "nothing to report" from "nobody checked", which is exactly what a rushed handoff hides.
- **Timed overlap with live verification** - a short overlap window rather than an instant switch, ending with a live check that the incoming person can actually reach the channel, not a verbal assurance. Where the outgoing person has already gone, fall back to a written quick handoff plus a short recorded walkthrough.
- **Paired on duty** - the starved option: two people on every block, staggered so the two never change at once. Tops both continuity axes, tops effort, and at community scale the extra headcount _is_ the organizing team. Promotion conditions: an overnight event, a first edition where nobody knows the failure modes yet, an on-duty person who is also the MC or a speaker, or an event large enough that two things break at once.
- **Delete, do not demote:** no named on-duty person, on the theory that whoever is nearest decides. That is the single point of failure the sourced practice exists to prevent, wearing flexibility as a costume - in practice one person decides everything and cannot leave the building.

## Running a transition

Three mechanics carry a transition, and none of them is the timing (drawn from a rapid-fire demo format and generalized to any tight handover):

- **Queue position** - where the next person physically stands, next to the stage rather than in the audience.
- **Tech ownership** - one machine and one operator, with material collected in advance, so the handover is a file switch and not a laptop swap.
- **The spoken line** - a live verbal reminder of the format's constraints, given on the day even though everyone was told in advance.

The source is explicit that the reminder is worth repeating at the point of use rather than assumed from an earlier briefing.

Two segments carry disproportionate weight and deserve the cue sheet's deepest rows:

- **The opening** - it sets the day.
- **The closing** - people remember the beginning and the end.

The sourced opening content checklist and closing mechanics are in [references/cue-sheet-anatomy.md](references/cue-sheet-anatomy.md).

## Handling a disruption live

Do not decide fresh. Run the sequence:

1. **Name it at the room.** The room lead calls what has happened and starts the clock - a no-show, a failed feed, a session forty minutes into a thirty-minute slot.
2. **Route it.** Anything the post can resolve alone, it resolves. Anything above its authority goes to the organizer on duty on the org channel - the routine path. Anything that is a safety, medical or security incident goes straight into the printed emergency plan's contacts, which `samber/dev-event-organizer-skills@event-risk-management` authored and you execute rather than rewrite.
3. **Decide against the published disruption order,** not against the room. Protect the plenary or keynote first, the headline commitment next, then minimize how many other sessions the fix disturbs.
4. **Lock the revised grid** for the rest of the block rather than reshuffling repeatedly as the day goes on.
5. **Say it out loud, in the room and on the channel.** A change nobody announced is a change that gets undone by the next person acting on the printed sheet.
6. **Write the row that was wrong** while it is still happening, on the text channel. That is what the next shift and the next edition inherit.

Who holds which authority at step 3 is yours to define. Decide it in advance, write it into your document, and say who decided rather than presenting it as standard practice. [references/comms-and-escalation.md](references/comms-and-escalation.md) has cross-industry conventions for the shape this ladder can take, if you want a starting model rather than a blank page.

## Closeout

At closeout:

- Hand the venue back against whatever the contract requires.
- Release staff explicitly, rather than by attrition.
- Capture the document's failures the same day: which rows were wrong, which transitions ran long, and which escalations never reached anyone.

Cold retrospectives recover the decisions and lose the timings.

## Failure modes

- **One person is the single point of failure for every crisis decision.** No named rotation, so the same organizer takes every call and cannot leave the building. The sourced fix is the on-duty rotation, published per block.
- **The MC also introduces every speaker.** Two sourced roles collapsed into one, so the person orchestrating the day's flow is also the person who must be at a specific lectern every forty minutes. Split them; the introducer role can rotate freely.
- **Organizer traffic on an attendee-facing channel.** The problem gets discussed in front of the people it concerns, and the message that mattered is buried under everyone else's. Create the separate channel before the day, not during it.
- **Transitions with no cue.** The grid says a session ends at 11:20 and says nothing about who speaks, where the next person stands, or whose machine has the slides. The result is dead air that eats the buffer the schedule was designed around.
- **Room reconfiguration assumed to happen invisibly.** A reset between two uses of the same space has no named owner and no timed row, so it either eats into the next segment or gets skipped. Give it the same row treatment as any other transition, started while the current segment is still running rather than after it ends.
- **A handoff with no live verification.** The incoming person says they have the channel and discovers at the first escalation that they do not. Check it live before the outgoing person walks away.
- **Improvising a disruption order.** The schedule already published one and it exists precisely so this call is not made under pressure by whoever is nearest to the broken thing.
- **Presenting your own conventions as industry practice.** Radio discipline, the room lead's authority and the shift-change mechanics are conventions you set, the last borrowed from on-call engineering practice. The live authority ladder's shape now draws on published stage-management and production convention, but its exact roster is still yours to name. Presenting your own specifics as an established standard spends the credibility the sourced parts need.

## Measurement

Two completeness gates, checkable before doors open, and no threshold to argue about:

- Every staffed post can name the organizer on duty for their block without asking anyone.
- Every segment on the cue sheet has a named owner, and every shift boundary has a handoff record with an entry or an explicit "none" in each section.

Every metric below is one you set rather than a benchmark to hit. Say so when you present them.

- **Transition dead air** (self-set): seconds between one segment ending and the next starting, counted separately at transitions the cue sheet scripted and transitions it did not. That comparison is what justifies the depth rung next edition.
- **Escalations that reached the on-duty person** (self-set): counted, and never minimized - zero usually means staff could not reach anyone, not that nothing happened.
- **Live changes made against the published disruption order** versus improvised ones (self-set): the second number is the one to drive down.
- **Cue-sheet drift** (self-set): rows that turned out wrong - an owner who was elsewhere, tech that was not where it said, a segment that did not exist. This is what a recurring event's template inherits.

Pick two or three, write down the revision each would trigger, and record them before the day rather than after.

## Invocation examples

- "We have the schedule locked for a two-day, three-room conference. Write me the run of show."
- "Who should be on radios on the day, and what channels do we need?"
- "Our keynote speaker is stuck in traffic and starts in twenty minutes. What do we do?"
- "How do we hand off between the morning and afternoon organizer on duty?"
- "Write the cue sheet for our closing ceremony with eight team demos."

Expected output: a run of show with:

1. The named role assignments, including who is on duty per block.
2. The cue sheet at the chosen depth, with a row per segment and per transition.
3. The comm-channel architecture and the medium it runs on.
4. Both escalation paths written onto the sheet itself.
5. The handoff format and where the changes fall.
6. The live disruption sequence, with the schedule's priority order quoted into it.
7. The closeout steps.
8. The two completeness gates plus the metrics chosen.

Presented section by section for validation before it is printed and briefed.

## References

- [references/cue-sheet-anatomy.md](references/cue-sheet-anatomy.md) - the cue sheet as an artifact: what each row carries, the sourced transition mechanics in full, the opening-ceremony content checklist and closing-ceremony mechanics, the live-demo timing breakdown with the event and format it came from, and a positive/negative pair of cue-sheet rows.
- [references/comms-and-escalation.md](references/comms-and-escalation.md) - the channel-separation pattern and how to map it onto radios, chat or a phone group, the two escalation paths side by side with what distinguishes them, a role-to-channel worked assignment, the sourced cross-industry conventions for the live authority ladder, and the radio discipline you still set yourself.
- [references/shift-handoff-protocol.md](references/shift-handoff-protocol.md) - the on-call handoff structure borrowed here (overlap window, mandatory-entry checklist, a separate mid-incident template, live verification, async fallback) with the mapping made explicit, plus what does not carry over and the figures that must not be reused.

- `samber/dev-event-organizer-skills@event-schedule-design` - builds the grid this document executes and hands over the disruption priority order; it is never reopened here.
- `samber/dev-event-organizer-skills@event-speaker-experience` - owns green room, tech check and the on-site host, and hands over each speaker's arrival and timing constraints as input.
- `samber/dev-event-organizer-skills@event-risk-management` - authors the standing register and the printed emergency plan whose scenarios and contacts this skill's incident path triggers into, never rewrites.
- `samber/dev-event-organizer-skills@event-production` - engineers the AV, stage and recording redundancy; this skill owns what a room lead does once that redundancy fails.
- `samber/dev-event-organizer-skills@event-volunteers` - recruits, sizes and briefs the people whose shift plan is an input here; this skill scripts what those staffed roles do once the day starts.
- `samber/dev-event-organizer-skills@event-social-media` - plans the day's live coverage; the named poster and the photo rules belong on this document, never on a separate page nobody opens on the day.
