---
name: virtual-event-production
description: Run the technical and audience-facing delivery of a fully-remote technical event once the format decision has already chosen virtual - the platform that replaces the venue, remote-speaker connectivity and local backup recordings, live chat and Q&A moderation staffing, and the failure drills an event with no physical room needs. Use whenever the user mentions a virtual event platform, an online or remote-only conference or meetup, preparing remote speakers, staffing chat and Q&A moderation, or what happens when the stream dies - even if they never say "virtual". Do NOT use when a physical room exists - the room's signal path is samber/dev-event-organizer-skills@event-production and two audiences at once is samber/dev-event-organizer-skills@hybrid-event-design.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Virtual Event Production

You run delivery for an event with no room. A software platform is the venue, each attendee's own connection is the uplink, and the crew is a moderator roster plus a remote-speaker pipeline rather than a stage crew. Treat the format as settled: `samber/dev-event-organizer-skills@event-format-selection` already chose fully-virtual. Never re-argue that choice.

## Where the room disappears

This boundary is written from your side only. Confirm it rather than implying an agreed handoff.

`samber/dev-event-organizer-skills@event-production` owns capture-through-published-master for any event with a physical room to instrument, including whatever stream that room also produces. It stops at the recorded or streamed output.

Its whole model has meaning only where a room exists: a mixing board, a camera on the board feed, a crew watching a monitor, a stage manager, the coverage tier named for a smartphone at the back of a room. You start where the room disappears entirely.

- **Capture.** A camera pointing at a physical stage is `samber/dev-event-organizer-skills@event-production`'s signal path, not yours, even when the audience is remote. Own the case with no stage to point at.
- **The remote attendee's day.** `samber/dev-event-organizer-skills@event-attendee-experience` scopes itself to "the general-attendee on-site journey" and keys every mechanic (badge desk, wayfinding, quiet room) to a signed floor plan, so it says nothing about a remote attendee's journey. Cover that mirror here; that skill does not know this one exists.
- **The channel architecture.** `samber/dev-event-organizer-skills@event-comms-channels` owns which channels exist, who is on each, and which class of message routes where, for remote and physical attendees alike. Consume its roster. Add only the live in-session question surface and the staffing that watches it, and reuse its standing-moderation-cost argument rather than deriving a second one.
- **Speaker care.** `samber/dev-event-organizer-skills@event-speaker-experience` owns the speaker relationship end to end, including the recording consent record you may not publish past. Its tech check happens on "the actual stage equipment" and its green room is a physical space, so remote connectivity testing, home-setup guidance and local backup recording fall to you. Hand the results back.
- **The day.** `samber/dev-event-organizer-skills@event-run-of-show` builds a cue sheet keyed to rooms, room leads, and an organizer-only channel. One coordination channel reserved for the organizing team, separate from every attendee-facing one, carries over to a virtual event unchanged. Nothing else about a room-keyed cue sheet does.
- **Accessibility.** `samber/dev-event-organizer-skills@event-accessibility-inclusion` decides whether captions are required and to what standard. Deliver them on the platform and report what the platform can and cannot do. Never set the bar yourself.

Every ranking below is a default, not a law. After the interview, re-rank all four menus against what you already know. Each of these overturns a default rung:

- a community that already lives in a chat space
- an organizer who has streamed before
- a platform an employer or sponsor has already paid for
- a previous edition whose feed died

Each promotion condition below names its interview question inside the condition's own text, and each trigger in an "or" list is keyed separately rather than riding on the first. Never source a condition from the re-ranking list above: that is a standing instruction, not an answer the interview collected. The four **delete** items cite no question on purpose - each is deleted unconditionally, on an argument that holds whatever the user answers.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the menus diverge sharply on time-to-effect, durability and effort, and those orderings cannot be picked for the user.

1. **Is there an interaction surface at all, or is this a feed people watch?** This reorders every menu below, and it decides whether Menu 3 exists at all.
2. How many sessions run at the same time, and how long is the shortest gap between them?
3. Where are the speakers and where is the audience - one time zone, or a spread wide enough that somebody presents in the middle of their night?
4. What did the format decision promise, and to whom: a paid virtual ticket, a sponsor deliverable naming the stream, an access commitment to people who cannot travel?
5. What is the recording and publication consent posture per session, and where is that record held? Do attendees appear on camera anywhere - a breakout, a networking room, a Q&A?
6. Does anything constrain where attendee data may be held or which platform may be used - an employer's procurement, a sponsor's contract, an umbrella organization's rules?
7. What is the last date a platform choice can still be reversed? That deadline, not the event date, is what these menus are ranked against.
8. One-off edition or a recurring event? A recurring event promotes every rung whose payoff lands after this edition: a rehearsed crew, a warm fallback path, a home-setup note you send again next year.
9. What is the effort ceiling - how many people can be doing only production during a session rather than also doing something else, and who is still available the week after?
10. What already exists that should re-rank these defaults: a chat space your audience is already in, an organizer who has run a stream before, a platform somebody already pays for, last edition's failures?
11. **Which sessions cannot be re-run or rescheduled, which carry a live demo, and which speakers have an unknown connection or have never presented on this platform?** Nothing else above reaches what a session contains or how badly it must not fail, and four rungs below promote on exactly that.

## What actually splits this work

The community-run versus vendor-run pole decides less here than it looks. A packet takes the same milliseconds whoever funded the event. What it does decide is Q6: a vendor-run event arrives more often with a platform already forced on it by procurement, which **deletes** a rung rather than reordering one.

Two answers reshape every menu, in this order: **whether an interaction surface exists**, then **how many sessions run at once**.

- A single feed with comments closed is a broadcast, and needs almost nothing.
- Three simultaneous tracks with open chat is a staffing problem before it is a technical one.

Say which of the two a recommendation assumes whenever they differ.

## Workflow

1. **Fix the interaction posture in one line** - a feed people watch, or an event people are inside. Write it down before anything else; every menu below is a consequence of it.
2. **Read the inputs rather than re-collecting them:** the channel roster, the per-speaker consent record, the accessibility bar, and whatever the format decision promised.
3. **Choose the platform posture** (Menu 1), then put the vendor questions in [references/platform-selection-and-vendor-questions.md](references/platform-selection-and-vendor-questions.md) to whoever can answer them, in writing, before committing.
4. **Choose remote-speaker readiness depth** (Menu 2) and send the home-setup note the same day acceptances go out. Details in [references/remote-speaker-readiness.md](references/remote-speaker-readiness.md).
5. **Staff moderation** (Menu 3) per concurrent session, by name, not by function. Skip this step entirely if step 1 said "a feed people watch".
6. **Pick the failure-drill depth** (Menu 4) and publish the fallback line where the audience will look for it, before the day. Runbook in [references/moderation-and-failure-drills.md](references/moderation-and-failure-drills.md).
7. **Rehearse once, on the platform the event actually runs on.** This is the step that gets cut, and a rehearsal on a different tool tests nothing.
8. **Hand the cost consequence to `samber/dev-event-organizer-skills@event-budget`**, split by what a lean tier drops: the feed itself survives every tier; the interaction surface and its staffing go first.
9. **After the event**, hand captured sessions to `samber/dev-event-organizer-skills@event-content-repurposing` and the recording consent check back to `samber/dev-event-organizer-skills@event-speaker-experience`.

Present the plan section by section for validation - interaction posture, then platform, then speakers, then moderation staffing, then the drill - before any contract is signed. After signature, a platform change costs money rather than a conversation.

If your harness has persistent memory, record per edition:

- which platform posture was chosen and what its vendor answers actually were
- which speakers needed which readiness rung
- how many moderators were genuinely busy versus idle
- every failure and which drill caught it
- what the audience did in the minutes after a feed dropped

A platform used twice is worth not re-learning.

## Menu 1 - Platform posture

The platform is your venue. Rank it like one: what it costs to acquire, what it costs to run, and what it actually buys the person watching.

Ranking (default, not a law - Q1, Q6, Q7 and Q10 re-rank it):

- ops effort (setup hours, people on the day, skill required): `assembled stack > managed virtual-venue platform > broadcast tool with a built-in question queue > one-way feed plus the existing chat space > single one-way feed`
- procurement cost (lead time to acquire, commitment signed, how reversible up to the date): `managed virtual-venue platform > broadcast tool with a built-in question queue > assembled stack == one-way feed plus the existing chat space > single one-way feed` - argued tie: both are assembled from things you can start and abandon in the same week, with nothing signed. The assembled stack's real price is paid in hours, and those already sit on the effort line above; the existing chat space was procured for another reason and this decision does not commit it further.
- value, reach (a watchable, audible talk arrives at a person on their own home connection): `single one-way feed == one-way feed plus the existing chat space > broadcast tool with a built-in question queue > managed virtual-venue platform == assembled stack` - argued tie at the top: the chat space sits beside the feed rather than inside it, so it adds nothing the video path has to carry. Argued tie at the bottom: both put the viewer behind a login and a bespoke player instead of a public video platform's delivery, and both add moving parts between the speaker and the viewer.
- value, interaction (attendees reach the speaker and each other, live): `managed virtual-venue platform > assembled stack > one-way feed plus the existing chat space == broadcast tool with a built-in question queue > single one-way feed` - argued tie: one buys attendee-to-attendee conversation with no question discipline, the other buys a disciplined question queue with no peer space. Neither buys both, and which one is worth more depends on Q1's answer, not on this ordering.
- compliance cost (the review it triggers and what stops being reversible): `managed virtual-venue platform > assembled stack > broadcast tool with a built-in question queue == one-way feed plus the existing chat space > single one-way feed` - argued tie: both hold attendee identity inside one vendor's chat or question record and nothing more; neither creates a directory a third party can export. The top rung is different in kind: an attendee directory and sponsor-facing lead capture trigger a data-handling review before signature, and a list a sponsor has already exported cannot be recalled. The assembled stack sits second because you chose each component's jurisdiction yourself, which is a review you own rather than one a vendor's terms performed for you.
- efficiency: `single one-way feed > one-way feed plus the existing chat space > managed virtual-venue platform > assembled stack > broadcast tool with a built-in question queue`

**Dominance check: 5 rungs, 10 pairs, four cost-and-value axes plus compliance, one real strict-dominance relation.**

- The one-way feed plus the existing chat space strictly dominates the broadcast tool with a built-in question queue: cheaper on ops effort, cheaper on procurement, **tied on compliance**, better on reach, tied on interaction. Dominance asks for no-worse on every axis and strictly-better on at least one; the two ties count as part of the relation, not as gaps in it, since this pair is strictly better on three axes.
- Eight of the remaining nine pairs are blocked by the interaction axis running opposite to effort: the rungs that buy conversation cost strictly more to acquire and to run. One of those eight, the broadcast tool against the assembled stack, is blocked twice over, since procurement also runs opposite to ops effort there.
- The last pair, the managed platform against the assembled stack, is blocked by procurement and compliance running opposite to ops effort and interaction: the managed platform is the lighter one to run and the heavier one to commit to.
- That accounts for all ten pairs (1 relation + 8 + 1).

**One warning about the reach axis.** Taken alone it is close to rank-identical to inverse effort, and would collapse this menu into cheapest-first, the ordering the ranking discipline exists to prevent. It earns its place only because the interaction axis runs the opposite direction, which is what gives this menu a real dominance relation rather than a vacuous check.

- **One-way feed plus the existing chat space** - the default. The feed goes to a public video platform; the conversation happens in the space `samber/dev-event-organizer-skills@event-comms-channels` already designed, with no second login and no second roster.

  **Drop to the single one-way feed** whenever Q9 says nobody can watch a chat during sessions: an open space in the event's name with nobody on duty is a code-of-conduct obligation with no responder. The published digital-harassment warning applies to it exactly as it does during a staffed session.

- **Single one-way feed** - the minimum viable posture, and it wins outright more often than it looks. Comments closed, no accounts, nothing to moderate, the lowest compliance exposure on the page, and the most robust delivery to a person on a phone.

  It is the honest choice for an event whose remote audience wants the talks and not the company. It is not "not running a virtual event" - that decision belongs to `samber/dev-event-organizer-skills@event-format-selection`.

- **Broadcast tool with a built-in question queue** - strictly dominated above, and kept on the menu for one reason only: Q6 can arrive with it already chosen and paid for. When it is what you have, run it and spend the saved decision on Menu 3.
- **Assembled stack** - separate streaming software, a separate chat platform, a separate schedule page, glued together by you. Cheap to start and reversible, and its whole cost is organizer hours and the seams between components.

  Major League Hacking's warning applies here in full: a well-run digital event is far more than a chat server. That is a hackathon organizer's warning about a hackathon's stack, so read it as a caution about under-estimating the work, not as a verdict on the components.

- **Managed virtual-venue platform** - the starved option: tops interaction, tops ops effort, tops procurement and tops compliance, so efficiency never picks it. Promotion conditions, each keyed separately:
  - several sessions running at once with attendees moving between them, keyed to **Q2** ("How many sessions run at the same time")
  - a sponsor deliverable that names a virtual booth, or an attendee directory sold as a ticket benefit, both keyed to **Q4** ("a paid virtual ticket, a sponsor deliverable naming the stream")
  - a procurement constraint that leaves no alternative, keyed to **Q6** ("which platform may be used - an employer's procurement, a sponsor's contract")
- **Delete, do not demote: a second live platform carrying the same sessions in parallel.** Delete it from this menu and from the axis lines above. It halves the audience of every question a speaker answers and doubles the moderation, and the failure shows up only as the half of the audience that never got an answer.

## Menu 2 - Remote-speaker readiness

A remote speaker's uplink is a domestic internet connection you do not control and cannot inspect. Every rung below either reduces the chance it fails or makes the failure survivable.

Ranking (default, not a law - Q3, Q4, Q8, Q10 and Q11 re-rank it):

- effort (organizer hours, scheduling, coordination per speaker): `individual tech check plus an instructed local backup recording > a pre-recorded talk played to schedule > one shared group tech-check window > a written home-setup note > slides and a join link`
- value, insurance (a usable talk exists whatever the speaker's connection does): `a pre-recorded talk played to schedule > individual tech check plus an instructed local backup recording > one shared group tech-check window > a written home-setup note > slides and a join link`
- value, liveness (the session feels live - the speaker is present, reacting, taking a question mid-talk): `individual tech check plus an instructed local backup recording > one shared group tech-check window == a written home-setup note > slides and a join link > a pre-recorded talk played to schedule` - argued tie: both leave the speaker rehearsed enough not to spend the opening minutes discovering the interface, and neither buys the confidence of having presented on it once with somebody watching.
- compliance cost (the review it triggers and what stops being reversible): `a pre-recorded talk played to schedule > individual tech check plus an instructed local backup recording > one shared group tech-check window == a written home-setup note == slides and a join link` - argued tie: none of the three creates a file, so none adds anything to the consent record beyond what the event's own capture posture already required. The two rungs above do create one, and a recording that exists is a recording somebody will later ask to publish; get that covered in `samber/dev-event-organizer-skills@event-speaker-experience`'s consent record before the file exists, not after.
- efficiency: `a written home-setup note > one shared group tech-check window > individual tech check plus an instructed local backup recording > a pre-recorded talk played to schedule > slides and a join link`

**Dominance check: 5 rungs, 10 pairs, two cost axes and two value axes, zero strict-dominance relations.**

- Two mechanisms account for all ten pairs, and neither covers the other's pairs.
- Six pairs are blocked because preparation costs strictly more coordination and buys more of both value axes at once: every comparison inside the live-delivery group, plus each of them against the do-nothing rung. Five of the six are strictly better on both value axes; the sixth, the group window against the home-setup note, is strictly more insurance while tying on liveness. That tie still blocks it, because the cheaper rung gains no value axis at all.
- The other four pairs are blocked by the pre-recording trade specifically: it buys certainty by spending presence, so it wins insurance and loses liveness against every rung it meets, including the pair where it is also the cheaper option.
- Zero relations means this check caught no misordering; what follows is argument, not verification.

- **A written home-setup note** - the default: sent with the join link, asynchronous, reusable next edition, and costing the speaker minutes. It moves the most common failures - a shared connection, a background sync eating the uplink, a laptop camera pointed at a ceiling - before anyone schedules a call.

  Contents in [references/remote-speaker-readiness.md](references/remote-speaker-readiness.md). Move up one rung as soon as any speaker has never presented on this platform - keyed to **Q11** ("which speakers have an unknown connection or have never presented on this platform").

- **One shared group tech-check window** - everyone joins the real platform at the same time, far enough before the day that a failed check can still be fixed. It costs one organizer block rather than one per speaker, and it surfaces platform-wide problems once instead of repeatedly.
- **Individual tech check plus an instructed local backup recording** - a scheduled slot per speaker, on the real platform, ending with the speaker set up to record locally on the day. The local recording is the point: a dropped feed then costs the live session and not the talk. Promotion conditions, all three keyed to **Q11**, which is the only question that reaches them:
  - an unrepeatable session ("Which sessions cannot be re-run or rescheduled")
  - a speaker whose connection is unknown or known-bad ("which speakers have an unknown connection")
  - a talk carrying a live demo ("which carry a live demo")
- **A pre-recorded talk played to schedule, with the speaker live in chat** - the starved option: tops insurance, near-tops effort, bottoms liveness, so efficiency never picks it. Its precedent is ACM SIGCHI, which dropped remote attendance entirely and offered authors who cannot travel a pre-recorded video played to the in-person audience. **What does not transfer** is the setting: that is a physical event's accommodation for an absent author, not a virtual event's default. Promotion conditions, each keyed separately:
  - a session landing in the middle of the speaker's night, keyed to **Q3** ("a spread wide enough that somebody presents in the middle of their night")
  - a demo that has already failed live once, keyed to **Q11** ("which carry a live demo") together with **Q10** ("last edition's failures")
  - a speaker who cannot hold a live slot at all, keyed to **Q11** ("which speakers have an unknown connection")

  ACM's own governing-board minutes record no-shows for remote presentations at one of its conferences: a speaker who does not appear is the failure this rung exists to remove.

- **Delete, do not demote: a tech check run on a different tool than the one the event runs on.** Delete it from this menu and from the axis lines above. It reads as a check and tests nothing that matters: not the platform's screen-share path, not its audio device handling, not what the speaker's browser does under it. `samber/dev-event-organizer-skills@event-speaker-experience` makes the same demand from its own side for a physical stage - a check on the actual equipment - and the reasoning is identical here.

## Menu 3 - Live moderation staffing

**Skip this menu entirely if Menu 1 landed on the single one-way feed.** With no interaction surface there is nothing to moderate, no rung above the floor exists, and the staffing question does not arise. Everything below assumes a surface is open.

The standing cost of an open space is already argued by `samber/dev-event-organizer-skills@event-comms-channels`: setup is an hour, moderation is a standing job for the whole time the space is open, and the code-of-conduct duty inside it is identical to the one in a room. Do not re-derive it. This menu adds only the _live, in-session_ layer that skill does not own: who relays a question to a speaker who cannot see chat, and who notices the feed died.

Ranking (default, not a law - Q1, Q2, Q9, Q10 and Q11 re-rank it):

- effort (people on duty per session-hour): `moderator, technical watcher and a host on the feed > moderator plus a technical watcher > one moderator per concurrent session > one moderator across the whole event > no moderation staffing`
- value, the space is held (questions reach the speaker, and conduct is enforced where it happens): `moderator, technical watcher and a host on the feed > one moderator per concurrent session == moderator plus a technical watcher > one moderator across the whole event > no moderation staffing` - argued tie: the technical watcher does not read chat. Moderation capacity is identical across those two rungs; the second person exists entirely for the other value axis.
- value, silence gets broken (a failure is noticed and named to the audience in the minute it happens): `moderator, technical watcher and a host on the feed > moderator plus a technical watcher > one moderator per concurrent session > one moderator across the whole event == no moderation staffing` - argued tie: one person cannot watch several streams' health at once, so at more than one concurrent session the event-wide moderator notices a dead feed no sooner than nobody does.
- compliance cost (the review it triggers and what stops being reversible): `no moderation staffing > one moderator across the whole event > one moderator per concurrent session == moderator plus a technical watcher == moderator, technical watcher and a host on the feed` - argued tie: all three put a named responder in every open space during every session, which is the whole of what the duty asks; people added beyond that change who notices a failure, not who is answerable for conduct. **This axis runs backwards to every other menu here, and that is the finding**: the cheapest rung carries the highest compliance cost, because an open space with nobody watching is an obligation with no responder, and harm inside it cannot be taken back. The Major League Hacking organizer guide is explicit that a digital space raises the risk rather than lowering it. Read the inversion as an argument about who is answerable, never as a legal reading: duty, platform terms and retention differ by country, and belong with the organizer's own counsel.
- efficiency: `one moderator per concurrent session > one moderator across the whole event > moderator plus a technical watcher > moderator, technical watcher and a host on the feed > no moderation staffing`

**Dominance check: 5 rungs, 10 pairs, two cost axes and two value axes, zero strict-dominance relations.**

- Three mechanisms account for all ten pairs.
- Eight pairs are blocked by the plain one: staffing costs strictly more people and buys strictly more of everything, including the discharge of the duty.
- One pair, the do-nothing rung against the event-wide moderator, needs its own account, because the silence axis ties there and "buys more of everything" stops being true. What blocks it is effort against the space-held axis alone: the moderator costs a person and buys the one value axis that still moves. The compliance inversion is not the blocker here, and naming it as one would be wrong; it runs the other way, which is why the moderator is the right call rather than why neither rung dominates.
- The last pair, one moderator per session against moderator-plus-watcher, is blocked because their moderation capacity is genuinely identical and only the failure-watching axis separates them.
- Zero relations means the check caught no misordering here.

- **One moderator per concurrent session** - the default: one named person per stream that is live at the same time, reading chat, selecting and relaying questions, and holding conduct. It scales with tracks rather than with attendance, which is why it needs no attendee ratio at all.
- **One moderator across the whole event** - sufficient and correct for a single-track day, and it is the same rung as the default when Q2 says one session runs at a time. It fails the moment two things happen at once.
- **Moderator plus a technical watcher** - a second person per session whose only job is whether the feed is up, audible and in sync. The pattern behind it is a physical event's livestream needing "at least one person to run it during the event" (DevOpsDays organizing guide). What does not carry across is the equipment: there is no board to run, so this person watches the output as an audience member sees it, from outside the production path. Promotion conditions, keyed separately:
  - anything live that cannot be re-run, keyed to **Q11** ("Which sessions cannot be re-run or rescheduled")
  - a previous edition where a dead feed went unnoticed, keyed to **Q10** ("last edition's failures")
- **Moderator, technical watcher and a host on the feed** - the starved option: tops both value axes and tops effort, so efficiency never picks it. It is the only rung where somebody actually _says_ something to the audience when a talk fails - an empty stream with a chat full of "is it just me?" is the failure mode the two rungs below leave open. Promotion conditions, each keyed separately:
  - a paid virtual ticket, or a sponsor deliverable naming the stream, both keyed to **Q4** ("a paid virtual ticket, a sponsor deliverable naming the stream")
  - a multi-hour continuous programme with gaps to fill, keyed to **Q2** ("how long is the shortest gap between them")
  - an audience that has no other way to find out what is happening, keyed to **Q1** ("Is there an interaction surface at all, or is this a feed people watch")
- **Delete, do not demote: the speaker moderating their own chat while presenting.** Delete it from this menu and from the axis lines above. It reads as the free version of moderation and it is not a rung: a presenting speaker is doing two jobs badly, and no speaker can enforce a code of conduct against a person in their own audience while talking to them. The floor rung above is honest about being unstaffed; this one is not.

## Menu 4 - Failure-drill depth

A physical room fails in front of people who can see each other. A virtual event fails as silence, and every attendee's first hypothesis is that the problem is on their end.

Ranking (default, not a law - Q4, Q8, Q10 and Q11 re-rank it):

- effort (preparation hours, coordination, infrastructure kept warm): `a full outage drill on a second platform > a standing fallback destination kept warm > a rehearsed handoff for the single likeliest failure > a written fallback line published before the day > no drill`
- value, the audience is held (people know what happened and stay): `a full outage drill on a second platform == a rehearsed handoff for the single likeliest failure > a standing fallback destination kept warm > a written fallback line published before the day > no drill` - argued tie: both rehearse the words somebody says the moment it breaks, and that is the whole of what holds an audience. The full drill adds infrastructure, not composure.
- value, the content survives (the session itself resumes rather than being lost): `a full outage drill on a second platform > a standing fallback destination kept warm > a rehearsed handoff for the single likeliest failure > a written fallback line published before the day == no drill` - argued tie: neither resumes anything. A published line tells people where to look; it does not put a talk back on air.
- efficiency: `a written fallback line published before the day > a rehearsed handoff for the single likeliest failure > a standing fallback destination kept warm > a full outage drill on a second platform > no drill`

**Dominance check: 5 rungs, 10 pairs, one cost axis and two value axes, zero strict-dominance relations.**

- No compliance axis is printed, because nothing here varies on one: every rung's exposure is whatever the platform and consent decisions already fixed.
- Three mechanisms account for all ten pairs.
- Eight pairs are blocked by depth costing preparation and buying both value axes at once. Seven of them are strictly better on both; the eighth, the do-nothing rung against the published line, is strictly more audience held while tying on content, which blocks it just as firmly.
- One pair, the rehearsed handoff against the warm fallback destination, is blocked by the two value axes genuinely crossing: rehearsing words is cheaper _and_ holds the audience better, and only infrastructure resumes the content.
- The last pair, the rehearsed handoff against the full drill, is blocked because the audience-held axis ties there and only the content-survives axis separates them.
- Zero relations means the check caught no misordering.

- **A written fallback line published before the day** - the default, and near-zero: one sentence, published where the audience will already be looking, naming exactly where to go when the feed dies. It costs a sentence and it removes the worst minute of a virtual outage, the one where nobody knows whether the problem is theirs. Move up one rung the moment a moderator exists at all, because then somebody is there to say it live.
- **A rehearsed handoff for the single likeliest failure** - a dry run of one scenario, the speaker's connection dropping mid-talk, with the moderator's exact opening words agreed in advance. It is the highest-value hour on this menu and it buys composure rather than infrastructure.
- **A standing fallback destination kept warm** - a second stream target already live and silent, with the published line pointing at it. This is the first rung that puts a session back on air rather than explaining its absence.
- **A full outage drill on a second platform** - the starved option: tops the content axis, ties the top of the audience axis, and tops effort, so efficiency never picks it. Promotion conditions, each keyed separately:
  - a paid virtual ticket you could be asked to refund, or a sponsor contract naming the stream, both keyed to **Q4** ("a paid virtual ticket, a sponsor deliverable naming the stream")
  - a session that genuinely cannot be rescheduled, keyed to **Q11** ("Which sessions cannot be re-run or rescheduled")
  - a previous edition whose feed died, keyed to **Q10** ("last edition's failures") and **Q8** (a recurring edition, which is what makes last edition's failures predictive)
- **Delete, do not demote: a contingency document nobody has read aloud.** Delete it from this menu and from the axis lines above. It reads as a drill and is not one - the moment it is needed, nobody can find it and nobody knows their line. The floor rung above is one published sentence the audience can see, which is a different artifact entirely.

## Failure modes

- **Treating a chat space as free.** Setup is an hour; watching it is a standing job for as long as it is open, and the conduct duty inside it is identical to a room's. The published warning is that a digital space raises the harassment risk rather than lowering it.
- **Failing as silence.** The feed dies and nothing anywhere says so, so every attendee spends minutes debugging their own connection. Publish the fallback line before the day and say something on it the moment it happens.
- **Rehearsing on a different tool.** A check that does not use the platform the event runs on tests nothing about the screen-share path, the audio devices, or what the speaker's browser does under it.
- **Background music in a demo.** A named platform risk: incidental music in a stream can get it taken down by the platform itself, mid-session, with no appeal that lands in time. Warn speakers before the day.
- **Publishing past the consent record.** A recording that exists is one somebody will ask to publish. `samber/dev-event-organizer-skills@event-speaker-experience` holds the consent record; a locally recorded backup, a breakout where attendees appeared on camera, and a Q&A carrying attendee faces are each outside whatever a talk's consent covered unless it was collected that way.
- **Buying interaction nobody uses.** Breakout rooms, booths and directories cost procurement, ops and a data-handling review whether or not anyone opens them. Published remote-turnout evidence points the same way, and it comes from outside technology - treat it as direction, not as a number.
- **Assuming the physical event's numbers.** The published cost evidence prices a _hybrid_ run's virtual layer, not a standalone virtual production. Never carry it across as if it sized your event.
- **Assuming attendance falls.** Total headcount across a conference's own editions moves either way once it goes virtual: PyCon US counted about 22% fewer people in 2021 (virtual, ~2,650) than in 2019 (in-person, 3,393 checked in), while KubeCon+CloudNativeCon North America's registrations nearly doubled the same way (11,891 in 2019, in-person, to 22,816+ in 2020, virtual). Removing travel cost and geography can grow the number as easily as losing the room shrinks it. Plan capacity from this event's own signals, not from either direction as a default.
- **Scheduling for your own time zone.** A programme built where the organizers live puts some speakers and some of the audience in the middle of their night. That is Q3, and it promotes the pre-recorded rung for exactly those slots.

## Measurement

Three completeness gates, checkable before the first session and free of any threshold to argue about:

- Every concurrent session has a named moderator, or the interaction surface for it is closed. Not a function - a name.
- Every speaker has joined the platform the event actually runs on, at least once, before the day.
- The fallback line is published, and the person who will say it out loud knows the sentence.

Everything below is a metric you set rather than an industry standard; say so when you present it.

- **Sessions delivered without an audience-visible failure**, over sessions scheduled (self-set). Count a session that ran with no audio as a failure, since that is the failure the drills exist for.
- **Time from a feed dropping to the audience being told something** (self-set). This is the number the drill menu actually moves.
- **Questions relayed to a speaker**, against questions asked (self-set). It measures whether the moderation staffing was real or nominal.
- **Speakers who joined a check before the day**, over speakers scheduled (self-set). The one leading indicator available before anything goes wrong.

Pick two or three, write down what change each would trigger, and record them before the event rather than after.

## Invocation examples

- "We're running our conference fully online this year. What platform do we actually need?"
- "How do I get remote speakers ready so a dropped connection doesn't kill a talk?"
- "How many moderators do we need for three parallel virtual tracks?"
- "What's our plan if the stream dies during the keynote?"
- "Our speakers are spread across too many time zones. What do we do about the ones whose slot lands in the middle of their night?"

Expected output: a delivery plan with:

1. the interaction posture in one line
2. the platform posture chosen with its vendor questions still open in writing
3. the speaker-readiness rung with the note or check schedule
4. moderation staffing assigned by name per concurrent session
5. the failure drill and the published fallback line
6. the rehearsal date on the real platform
7. the cost consequence split for the budget

Presented section by section for validation before anything is signed.

## References

See also, same collection:

- `samber/dev-event-organizer-skills@hybrid-event-design` - owns the event serving a room and a remote audience at once. The dividing line is the stage: a hybrid always has one, so every menu here stops applying to it.
