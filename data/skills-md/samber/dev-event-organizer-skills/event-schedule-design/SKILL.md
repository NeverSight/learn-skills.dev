---
name: event-schedule-design
description: Lay a technical event's already-selected talks into a published session grid - session-length standardization, room and capacity matching, the four clash types with multi-speaker intersection, break and lunch placement, buffer sizing, keynote and plenary placement as re-sync points, synchronized versus staggered track starts, energy-curve pacing, and speaker travel windows against slot assignment. Use whenever the user mentions building a conference schedule or agenda, a multi-track layout, session clashes or speaker double-booking, matching talks to rooms, sizing breaks, or when to publish the grid - even if they never say "schedule". Do NOT use to decide the track count or session-format mix - use samber/dev-event-organizer-skills@event-format-selection instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Schedule Design

You lay already-selected sessions into a physical grid: which talk runs at which time, in which room, with what between them. Your inputs arrive decided, fixed by these sources:

- **Track count, event shape, session-format mix, delivery mode** - `samber/dev-event-organizer-skills@event-format-selection`, which states the split from its own side: "You do not build the schedule - grid layout, clash avoidance, and room-capacity matching belong to `samber/dev-event-organizer-skills@event-schedule-design`. Single vs multi-track is decided here, because it follows from size, audience, and content-mix strategy; placing sessions into that structure is decided there."
- **Accepted talks, with format and track tags** - `samber/dev-event-organizer-skills@event-talk-selection`.
- **Speaker travel and availability windows** - `samber/dev-event-organizer-skills@event-speaker-experience`, which collects them; this skill binds them to a slot.

You stop at the published grid. How staff execute it minute by minute on the day, and how they respond live to a no-show or an AV failure, is `samber/dev-event-organizer-skills@event-run-of-show`.

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank all three menus against what you know about this event:

- A venue whose rooms open onto one narrow corridor.
- A scheduling tool already in use that computes clashes for free.
- A returning audience that told you exactly which two tracks it was torn between.
- A hard publication date.

Each of these can overturn a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability and effort - those orderings cannot be picked for the user.

1. How many rooms run simultaneously, and how many sessions are you placing across how many days? (This is the split that changes everything below - see the next section.)
2. What are the rooms: names, seated capacity, and how far apart they are in walking minutes? A grid built without capacities is a seating plan you will discover on the day.
3. What did the venue contract fix - doors open and close, catering windows, room-hire start and end times, any room you only hold for part of the day?
4. When must the schedule be public, and what is that date serving: ticket sales, travel booking, or a sponsor commitment?
5. Is this a one-off edition or a compounding annual asset? (A compounding mandate promotes the slow rungs: recorded room-turnover times, a versioned public grid, a survey question that tells you next year which clashes hurt.)
6. What is the effort ceiling - who actually builds and maintains this grid, in how many hours, and who arbitrates when two sessions want the same slot?
7. Do you have every speaker's availability window, and for multi-speaker sessions, all co-speakers' windows? If not, get them before laying anything (see the workflow).
8. Which sessions are fixed points rather than free pieces: keynotes, an opening, a closing, a sponsor slot, a session a speaker can only give on one day?
9. What already exists that should re-rank the menus: last edition's grid and its complaints, recorded overruns, a scheduling tool with clash detection, a known corridor bottleneck, an attendee survey naming the clashes that hurt?
10. What has to physically change between two consecutive sessions in each room - AV reset, furniture, staging?

## Single-track vs multi-track

Neither does this collection's usual community-run versus vendor-run split: a developer walks a corridor at the same speed whichever kind of event they paid for. Who owns the event changes which content gets picked, not how a room empties.

What genuinely changes the work is whether more than one session ever runs at once:

- **Single track** - there is no clash problem in the sense the tools mean it: nothing overlaps, so clash detection collapses to a single question, whether the speaker is in the building. Room-capacity matching does not exist either; everyone is in the one room or the event is oversold. The entire design load moves onto pacing, break placement and buffer, and one overrun propagates to the whole day rather than to one track.
- **Multi track** - all four clash types apply, room-capacity matching becomes a real allocation problem, corridor throughput becomes a design constraint rather than an afterthought, and the plenary moments that are free in a single-track day now have to be deliberately re-created.
- **Ceiling scale** - dozens of rooms. FOSDEM 2026 published 1,079 events across 37 rooms and 71 tracks, and publishes a separate "room occupation by track" overview alongside the grid: at that scale the grid stops being one document and room-to-track mapping becomes its own artifact. Read it as a benchmark ceiling, not a target.

Say which pole a recommendation assumes when they differ.

## Workflow

1. Run the interview. Get the room list with capacities and walking distances (Q2) and the venue's fixed windows (Q3) before touching a grid - both delete options rather than adjusting them.
2. Collect every speaker's availability window, and the co-speaker windows for multi-speaker sessions, before laying anything. Collecting it upfront on the submission form is the sourced practice: availability is gathered at proposal time through a calendar widget. If your form did not ask, ask now and wait; discovering an availability conflict after publication costs a public correction. The form-depth decision this field belongs in is `samber/dev-event-organizer-skills@event-cfp-design`'s.
3. Standardize session lengths (see below) so slots are interchangeable. Do this before assigning anything - a grid of bespoke durations cannot be re-sequenced when one piece moves.
4. Place the fixed points first (Q8): opening, keynotes, closing, and any session with a single possible day. Everything else fills around them.
5. Place lunch and breaks next, not last. In a multi-track day they double as plenary re-sync points that reset accumulated per-track drift. PyCon US runs keynotes 9:00-9:45 in one dedicated large room, mid-morning break around 10:30, lunch around 12:30-1:15, mid-afternoon break around 4:00.
6. Match sessions to rooms on expected audience size, not on track tidiness (see below).
7. Lay the remaining sessions into the grid. Where several accepted talks compete for one prime slot, place the hardest-constrained first - the speaker with one available day goes before the speaker who is free all week (borrowed from earliest-due-date job-shop dispatching; a structuring analogy, not a rule to apply mechanically).
8. Choose the track-start alignment (see below) and apply it consistently.
9. Run clash detection at the depth the menu picks. Re-run it after every subsequent change, not once at the end.
10. Set the buffer from its menu and check it against the walking distances from Q2.
11. Read the whole day for pacing, and label that read for what it is (see Energy-curve pacing).
12. Write the disruption priority order into the grid document and hand it to `samber/dev-event-organizer-skills@event-run-of-show`.
13. Publish at the posture the menu picks, then treat the grid as a living document rather than a final artifact.

Present the grid section by section for validation - fixed points, breaks, room assignments, then the full grid - before it goes public. Once a schedule is published, every change costs an attendee who planned around the old one.

If your harness has persistent memory, record:

- The session-length standard.
- The buffer figure and why it was chosen.
- The room-capacity assumptions that turned out wrong.
- The clashes attendees reported.
- The walking-distance facts about this venue.

A venue you use twice is worth not re-measuring.

## Session-length standardization

Pick a small set of slot lengths and make every session fit one. Two sourced points, at different scales: FOSDEM runs ~50-minute talks with lightning talks capped at 15 minutes, and PyCon US runs 45-minute talks. Both standardize; neither offers a menu of bespoke durations.

Standardize the _slot_, not the talk. A 30-minute slot holding a 25-minute talk carries its own turnover time inside the number you publish, which is why the default buffer rung below costs nothing extra to compute. Say the talk length and the slot length separately in the speaker brief, or speakers will use the slot.

## Room and capacity matching

Match rooms to sessions in this order:

1. Expected audience size.
2. Room adjacency.

Never match on which track feels like it deserves the big room. The failure this prevents is one-directional and public: a session that draws more people than its room seats turns away attendees at the door, while a session in an over-large room merely looks quiet.

Estimate expected size from whatever you actually have:

- Last edition's per-session counts.
- The topic's draw in your community.
- A speaker with a following.
- The track's share of the CFP.

Every estimate here is yours rather than a benchmark, so present it as such. Where a session could plausibly overflow, either give it the larger room or place it opposite something else that draws well, so the audience splits rather than concentrates.

At many-room scale, keep the room-to-track mapping as its own artifact rather than reading it off the grid - that is what FOSDEM's separate room-occupation overview does.

Two further placement moves cost little against a multi-track grid's continuity and its fairness, both self-set rather than published practice:

- Group adjacent slots by topic where the content allows it, so an attendee can stay in one room across two consecutive sessions instead of a room change between every pair.
- Where each track alternates between a larger and a smaller room across the day, swap which track holds which at the midpoint, so one track's audience does not sit in the lesser room for the whole day.

## Clash detection depth

A real scheduling tool models this as four distinct conflict types rather than one generic flag:

- A session outside its room's availability window.
- A session conflicting with a speaker's stated unavailability.
- Two sessions overlapping in the same room.
- One speaker double-booked across simultaneous sessions.

For multi-speaker sessions the valid window is the _intersection_ of all co-speakers' availabilities - a session cannot sit where even one co-speaker is unavailable. None of this requires that tool, or any tool: the four types are what a grid has to represent, and a spreadsheet holds all of them.

Ranking (default, not a law - Q1, Q6 and Q9 re-rank it):

- effort (new data you must collect, passes over the grid, judgment required): `audience-overlap pass > availability-window checking > speaker double-booking == same-room overlap` - the tie is argued, not a dodge: both are pure arithmetic over data the grid already contains, need no new collection and no judgment call, and cost one pass whether you run one or both.
- value, sessions that can physically happen as published: `availability-window checking > speaker double-booking == same-room overlap > audience-overlap pass`. Availability leads because it fails silently - nothing on the grid looks wrong while the speaker is on a plane.
- value, a program the audience is glad about: `audience-overlap pass > availability-window checking > speaker double-booking == same-room overlap`. This axis is why the starved rung exists; the three mechanical checks buy a schedule that runs, not a schedule anyone enjoyed.
- efficiency: `same-room overlap == speaker double-booking > availability-window checking > audience-overlap pass`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Three mechanisms block the six:

- The audience-overlap pass against each of the other three is blocked by opposed value axes - it tops program quality and bottoms will-it-run.
- Availability checking against each of the two arithmetic checks is blocked by effort alone: availability leads on _both_ value axes and still costs more.
- The last pair, same-room overlap against speaker double-booking, is blocked because the two rungs are tied on every axis, so nothing about either is strict.

None of the three reasons is evidence; the efficiency line rests on the arguments below.

- **The three mechanical checks** - the default, run as one pass: same-room overlap, speaker double-booking, and both availability windows with the multi-speaker intersection. Together they are the whole of what a tool automates, and they are cheap enough that running fewer than all three is never the right economy.
- **Audience-overlap pass** - the starved option: two sessions a shared audience would both want, scheduled head to head. Nothing computes this; it needs someone who knows the community reading the grid and naming the pairs. It tops the program-quality axis and tops effort, so efficiency never picks it.
  - Promotion conditions: two tracks that visibly share an audience, a track added specifically to reduce head-to-head competition, or a returning audience that already told you which clash hurt last edition.
- **Delete, do not demote:** on a single-track event, drop the overlap and double-booking checks and the audience-overlap pass entirely - nothing runs at once, so the only live check is speaker availability. A multi-track checklist parked at the bottom of a single-track plan is how a second track quietly reappears as scope.

## Buffer between sessions

Ranking (default, not a law - Q2, Q5 and Q9 re-rank it):

- effort (grid arithmetic, per-room bookkeeping, day-length consumed): `room-turnover-aware > proportional > fixed inter-slot gap == slot-internal buffer` - argued tie: both publish one number that holds for the whole grid and take one decision to set; whether the buffer sits inside or between slots changes what attendees read, not what you compute.
- value, sessions that start when they say they will: `room-turnover-aware > proportional > fixed inter-slot gap == slot-internal buffer` - the same tie holds for the same reason, since the minutes absorbed are identical either way.
- value, hallway-track time attendees can actually plan into: `fixed inter-slot gap > room-turnover-aware > proportional > slot-internal buffer`. A published gap is visible time someone can spend on a corridor conversation; a buffer hidden inside a slot reads as dead air and gets spent by an overrunning speaker instead.
- efficiency: `slot-internal buffer > fixed inter-slot gap > proportional > room-turnover-aware`

- **Slot-internal buffer** - the default: publish slots longer than the talks they hold and brief speakers on both numbers. Near-zero cost, because the buffer lives inside a figure you were publishing anyway.
- **Fixed inter-slot gap** - one published gap between slots, the same everywhere. FOSDEM's visible gap between its 09:30-09:50 opening keynote and the 10:00-10:50 slot that follows is 10 minutes, across a venue spanning 37 rooms. Cite that as a real density-versus-buffer trade-off at ceiling scale, not as a recommended figure - 10 minutes is tight for that footprint, and it is what buys the 1,079-event count.
- **Proportional gap** - size the buffer as a share of the preceding session's length rather than a flat number, and read buffer consumption as a graded signal (comfortable, tightening, blown) rather than a binary on-time/late. This pattern comes from manufacturing production scheduling. Take the pattern, not manufacturing's specific percentages - its 50% sizing and 33/67% zone boundaries come from a different domain and do not transfer.
- **Room-turnover-aware gap** - the starved option: gaps sized per room-pair to what physically changes between two consecutive sessions in that room - AV reset, a workshop's tables going back to theatre rows, a panel's chairs coming on. This pattern comes from manufacturing production scheduling's changeover sequencing, and tops both on-time value and effort because it is per-pair bookkeeping.
  - **Promotion conditions, keyed to Q10**: one room hosting mixed formats, a venue whose AV needs a real reset between sessions, or a compounding mandate where you record actual turnover times once and reuse them every edition.
  - Its cheap companion is free: sequence same-format sessions together within a room so there is less to change.
- **Delete, do not demote:** a zero-gap grid, whenever rooms are on different floors or more than a couple of minutes' walk apart. A schedule that assumes teleportation is corrected all day by attendees arriving late, and leaving it on the menu invites it back when the day looks too long.

## Track-start alignment

No ranking here, deliberately. Synchronized and staggered starts cost the same to decide and the same to apply - one call, one pass over the grid - so an efficiency ordering between them would be false precision. The choice is determined by the venue, not by the ratio:

- **Stagger** when simultaneous room changes would jam a corridor. PyCon US 2026 runs staggered starts across five main rooms - observed starts at 11:00, 11:45, 12:30, 1:45, 2:45, 3:30 and 4:30 - so that when one track ends another is mid-session and foot traffic spreads instead of concentrating. Staggering costs you the clean "everything starts on the hour" rule and makes the clash pass fiddlier to read.
- **Synchronize** when the room count is small enough that everyone moving at once still clears, or when you want the whole audience arriving at plenary moments together.

Either way, keep the plenary sync points: a keynote or lunch that pulls every track into one room also resets whatever drift each track accumulated before the next block starts. PyCon US and FOSDEM both bookend their grids this way, with plenary moments at open and close.

## Energy-curve pacing

Named organizers vary session format and density across the day rather than holding it constant, and graveyard slots (positions with a structurally high chance of low attendance) are a real, named problem, not just a manufacturing analogy relabeled (see `references/published-schedule-benchmarks.md` § Energy-curve pacing and graveyard slots: named sources for the full source list):

- DevOpsDays' own organizing guide runs structured talks in the morning, then short Ignite talks, then self-organized Open Space in the afternoon - a published format gradient from high structure to low structure.
- The post-lunch alertness dip is circadian, documented independent of what attendees ate, which is the physiological basis for avoiding dense content right after lunch.
- The last slot of the last day is, at the conferences studied, empirically the worst-attended and least-engaged position; a weekend day carries the same risk at whole-day scale.

Two concrete techniques these sources describe, beyond reading your own grid:

- **Format substitution over content substitution.** DevOpsDays does not just avoid content after lunch; it swaps the format - lecture-style talks give way to self-organized Open Space, matching the slot to the audience's actual energy state instead of fighting it.
- **Track no-show rate per slot as a diagnostic** (see Measurement below). Recording which slots underperform their expected turnout, slot by slot and edition over edition, turns "which slot is a graveyard here" from received wisdom into something you measure at your own event.

The heijunka (levelled production sequencing) analogy in `references/production-scheduling-concepts.md` still supplies the closest thing to a mechanism for why front-loading intensity helps: the sources above confirm its direction but say nothing about why, and the post-lunch dip they add is a second risk window the end-of-shift-crunch analogy misses entirely. State that a claim is sourced or judgment when you present the pacing read, and do not invent a number for either.

## Speaker constraints and disruption

Rooms and speakers each carry their own availability windows, and they are separate constraints: a room's booking window is not a speaker's calendar. At slot assignment:

- Reconcile both.
- Take the intersection for multi-speaker sessions.
- Treat a travel window as an availability window - a speaker landing the morning of cannot open the day.

Design the grid so a disruption is survivable, and write the priority order into the document rather than leaving it to be invented under pressure (borrowed - disruption re-sequencing from manufacturing production scheduling; its communication and lock-duration figures belong to that domain and do not carry over):

1. Protect the plenary or keynote slot first.
2. Protect the headline commitment the audience showed up for next.
3. Minimize how many other sessions the fix disturbs.
4. Lock the revised grid for the remainder of the block instead of re-shuffling repeatedly as the day goes on.

Executing that order live on the day is `samber/dev-event-organizer-skills@event-run-of-show`, not this skill.

## Publication posture

Ranking (default, not a law - Q4, Q5 and Q9 re-rank it):

- effort (maintenance after the first release, announcement coordination): `versioned release > release early and iterate > staged reveal > lock late`
- value, attendees who can book travel and plan a personal agenda: `versioned release > release early and iterate > staged reveal > lock late`
- value, announcement moments bought: `staged reveal > versioned release == release early and iterate > lock late` - argued tie: both put the whole grid out at once, so each buys exactly one moment; a changelog changes what a returning visitor sees, not how many times you get to announce.
- efficiency: `release early and iterate > staged reveal > versioned release > lock late`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** Two mechanisms block the six:

- Effort alone blocks four: the rung ahead on planning value costs strictly more to maintain. That includes all three pairs against lock-late, which loses on value rather than winning anything for free, and the versioned-against-early pair, where versioning leads on planning value, ties on announcement moments, and still costs more.
- Opposed value axes block the other two: early against staged reveal, and staged reveal against versioned.

The check catches nothing here.

- **Release early and iterate** - the default, and the sourced guidance: "Don't wait for a perfect schedule before releasing – release early and iterate." It treats the published schedule as a living document revised in place, which is also the only posture honest about how often a grid moves.
- **Staged reveal** - announce speakers and talks first, the grid later. Cheap, and it buys a second marketing beat; it just leaves travel planning waiting on the second one.
- **Versioned release** - the starved option: publish early _and_ carry a visible marker of what changed since, so someone who planned their day can see what moved. Highest planning value, highest effort because maintaining it is a standing job rather than a task. Promotion conditions: a multi-day multi-track grid people build personal agendas against, a change landing after tickets are sold, or a compounding annual event whose audience returns expecting the same reliability.
- **Delete, do not demote:** lock-late publication whenever attendees travel to reach you. A grid published a fortnight out cannot inform a flight booked two months earlier, and keeping the option parked at the bottom is how a busy program chair takes it. It survives only for a same-city, meetup-scale event nobody buys a ticket to travel for.

## Failure modes

- **Double-booking a multi-speaker talk.** Each co-speaker's window was checked, the intersection was not. Compute the intersection explicitly; a session cannot sit where even one co-speaker is unavailable.
- **Capacity mismatch.** A session estimated small, placed in a small room, and an overflow crowd turned away at the door. Estimate before assigning, and put anything that could plausibly overflow in the larger room - an over-large room only looks quiet.
- **Synchronized starts jamming the corridor.** Every room emptying at once into a venue that cannot absorb it. PyCon US's staggering is the sourced counter; it costs the clean on-the-hour rule and buys back the hallway.
- **No buffer for room turnover.** A grid whose gaps assume nothing physical happens between two sessions, in a room where the format changes. Turnover is real and session-pair-dependent.
- **Treating a borrowed heuristic as an events fact, or a sourced finding as universally transferable.** The heijunka analogy is manufacturing, not events, and stays labelled as such. The graveyard-slot and post-lunch-dip sources are real events- and physiology-specific findings, but their measured magnitudes come from economics-conference and lab data, not developer conferences - cite the direction, not the number, unless you have your own.
- **Re-litigating the track count in the grid.** A grid that will not fit is not a signal to add a track - `samber/dev-event-organizer-skills@event-format-selection` owns that decision and already made it, and adding a track mid-build silently changes the content mix it was coupled to.
- **Clash detection run once.** Every move invalidates the previous pass. Re-run after each change, including the ones made after publication.

## Measurement

Every threshold here is one you set rather than a benchmark to hit. Say so when you present them.

- **On-time start rate per room** (self-set): the share of sessions that began within the buffer. A room that drifts all day is a buffer-sizing problem, not a speaker problem.
- **Buffer consumption, graded** (self-set thresholds; the graded framing is borrowed from production buffer management): how much of each buffer was actually eaten, read as comfortable / tightening / blown rather than on-time / late.
- **Room-fit outcomes** (self-set): sessions that overflowed and sessions that ran near-empty, both counted. The first is a public failure, the second is wasted capacity, and the ratio tells you how to estimate next edition.
- **Post-publication change count and last-change date** (self-set): how much moved after the grid went public, and how late. This is what decides whether the versioned-release rung is worth its cost next time.
- **Reported clashes** (self-set): a post-event survey question asking which two sessions attendees were torn between. It is the only measurement that reaches the audience-overlap rung the efficiency ordering starves.
- **No-show rate per slot** (a technique named in event-scheduling guidance, tracked by you): the share of expected attendees who did not show, recorded by slot position rather than by session. A slot that underperforms across multiple sessions and editions is a graveyard slot at your venue, whatever a published source says about slots in general (see Energy-curve pacing above).

Pick two or three, write down the revision each would trigger, and record them before the event rather than after.

## Invocation examples

- "We have 42 accepted talks, four rooms and two days. Build me the grid."
- "Our rooms are on three floors and people were late to everything last year - how much buffer do we need?"
- "Two of our tracks share the same audience. How do I stop scheduling them against each other?"
- "One keynote speaker only lands at 11am on Saturday. Where does she go?"
- "Should we publish the schedule now or wait until it's final?"

Expected output: a schedule plan covering:

1. The session-length standard and what a slot contains.
2. Fixed points placed with their reasons.
3. Breaks and plenary sync points.
4. Room assignments with the capacity estimate behind each.
5. The full grid.
6. The clash-detection depth run and its findings.
7. The buffer figure and the walking distances it was checked against.
8. The track-start alignment and why.
9. The pacing read labelled as judgment.
10. The disruption priority order to hand to `samber/dev-event-organizer-skills@event-run-of-show`.
11. The publication posture with a date.

Presented section by section for validation before anything goes public.

## References

- [references/grid-mechanics-and-clash-types.md](references/grid-mechanics-and-clash-types.md) - the rooms-by-time grid model, the four clash types in full with what each one catches and misses, the room-versus-speaker availability distinction and the multi-speaker intersection, breaks versus internal blockers, and a worked positive/negative slotting example.
- [references/published-schedule-benchmarks.md](references/published-schedule-benchmarks.md) - FOSDEM and PyCon US published schedules, the two contrasting congestion strategies side by side, named organizer and peer-reviewed sources on energy-curve pacing and graveyard slots, and what each schedule does not show.
- [references/production-scheduling-concepts.md](references/production-scheduling-concepts.md) - the manufacturing scheduling concepts this skill borrows (graded buffer zones, disruption re-sequencing with a stability lock, changeover sequencing, levelled pacing), each with the mapping made explicit, plus the parts that do not carry over and the numbers that must not be reused.

See also, same collection:

- `samber/dev-event-organizer-skills@event-format-selection` - decided the track count, event shape and session-format mix this grid executes inside.
- `samber/dev-event-organizer-skills@event-talk-selection` - supplies accepted talks with format and track tags.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - supplies seated capacities, walking distances and contract windows this grid is laid inside.
- `samber/dev-event-organizer-skills@event-speaker-experience` - collects speaker travel and availability constraints that bind slot assignment.
- `samber/dev-event-organizer-skills@event-run-of-show` - executes this grid on the day.
- `samber/dev-event-organizer-skills@event-cfp-design` - owns the submission form's availability field and the design decision to add it.
