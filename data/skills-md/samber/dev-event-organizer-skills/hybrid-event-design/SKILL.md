---
name: hybrid-event-design
description: Design a technical event serving an in-room and a remote audience at once, after the format decision has already chosen hybrid - which sessions the remote audience gets, how far a remote attendee's voice reaches the stage, the cue track the stream needs beside the room's, and the crew split between them. Use whenever the user mentions streaming talks to a remote audience, remote Q&A, staffing the remote side, or running a day for two audiences at once - even if they never say "hybrid". Do NOT use to decide whether to run hybrid at all - use samber/dev-event-organizer-skills@event-format-selection; an event with no room is samber/dev-event-organizer-skills@virtual-event-production.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Hybrid Event Design

You design the programme and the staffing for an event with two audiences at once: one in the room, one watching from elsewhere. The format decision arrives made. Never reopen it.

## This skill is deliberately narrow, and the reason matters

Siblings already own most of what a hybrid event needs. The scope left over is small. Say so rather than expanding into their territory:

- `samber/dev-event-organizer-skills@event-format-selection` decides whether hybrid happens at all and owns the entire cost case against it. Its verdict: "It is the maximum-cost, maximum-risk option, not the middle". Consume that verdict. Never re-derive the cost argument, never re-quote its figures. If the user is still deciding, route them there and stop.
- `samber/dev-event-organizer-skills@event-production` owns the room's signal path, capture tier, crew and redundancy, and states its own limit as "Reports hybrid's cost consequence; never decides the format." Every camera, cable and encoder is its work. You name the sessions that need a feed. It builds the feed.
- `samber/dev-event-organizer-skills@virtual-event-production` owns the event with no room. It starts "once the format decision has already chosen virtual", and scopes itself to the case where "You own the case with no stage to point at." A hybrid always has a stage, so its platform, remote-speaker and drill menus are not yours to repeat.
- `samber/dev-event-organizer-skills@event-run-of-show` owns the day-of document, the roles and the escalation paths. You add one column to its artifact. Never write a second one.
- `samber/dev-event-organizer-skills@event-schedule-design` owns the grid. You mark sessions on it. Never move them.

Four things are genuinely left, covered by three menus and one section:

- Which sessions the remote audience gets.
- How far a remote attendee's voice reaches the stage.
- What cue track the stream needs beside the room's.
- Who staffs the remote side.

That is the whole skill. Its shortness is the correct outcome, not a gap.

Every ranking below is a default, not a law. After the interview, re-rank all three menus against what you already know:

- A room already wired for capture.
- A community that has streamed before.
- A remote audience that has already paid.
- A previous edition where remote questions went unanswered.

Each of these overturns a default rung.

## Why parity matters, and why it fails

Remote audiences at hybrid events report feeling like second-class attendees when they watch but cannot participate. The failure is not equipment; it is attention.

Two documented cases:

- A workshop running late in the room while remote participants are not told.
- Remote check-in lagging because the team is busy in person.

In both, the staff were looking at the room and the remote audience got what was left. A scaled-back hybrid conference confirms the pattern: online participants reported it less engaging than anticipated, and the event closed at a loss.

Every value ordering below is reasoned, not measured. No menu choice here carries a figure tying it to remote attendance, engagement or satisfaction.

Never invent any of these to justify a rung:

- A parity threshold.
- A remote-to-in-room staffing ratio.
- A share of Q&A owed to remote.
- A tolerable stream delay.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the menus diverge sharply on time-to-effect, durability and effort - those orderings cannot be picked for the user.

1. **What was the remote audience actually promised, and to whom?** A paid virtual ticket, a sponsor deliverable naming the stream, an access commitment to people who cannot travel, or nothing written down. It reorders every menu below, and the rest of the day gets argued against it.
2. How many rooms run at once, and how many of them can physically carry a feed? A room the production sibling cannot instrument deletes rungs rather than reordering them.
3. Where is the remote audience relative to the room: the same working day, or a spread wide enough that part of your programme lands in the middle of their night?
4. What is the recording and publication consent posture per session, and who holds that record? Does the in-room audience appear on the outgoing feed during Q&A?
5. Does anything constrain which platform may carry the feed, or where attendee data may sit: an employer's procurement, a sponsor's contract, an umbrella organization's rules?
6. Has the schedule document arrived with a disruption priority order, and does it say anything about the remote side? Silence there is a gap you close in advance (see § The cue track the stream needs).
7. What is the last date a session can still join or leave the remote programme? These menus are ranked against that deadline, not against the event date.
8. One-off edition or a recurring event? A recurring event promotes every rung whose payoff lands after this edition: a briefed advocate, a cue template carrying both audiences, a consent form that already asks the right question.
9. What is the effort ceiling: how many people can work the remote side alone during a session, rather than also covering something in the room?
10. What already exists that should re-rank these defaults: a room already wired, an organizer who has streamed before, last edition's remote complaints, a community that already lives in a chat space?

## What actually splits this work

Community-run and vendor-run events diverge at one question, not across the menus. A remote attendee waits the same seconds for an answer whoever funded the room.

That question is Q1. A vendor-run event more often arrives with the remote audience already sold something:

- A virtual ticket.
- A customer commitment.
- A sponsor line naming the stream.

Being sold something promotes rungs rather than reordering them, because a promise is not a preference.

Two things reshape every menu instead:

- Whether the remote audience has a return path at all.
- After that, how many rooms carry a feed.

A single streamed room with a one-way feed is a broadcast attached to a conference, and it needs almost nothing new. Two streamed rooms with live Q&A is a staffing problem before it is a technical one. Say which case a recommendation assumes whenever the two differ.

## Workflow

1. **Confirm the format decision is closed.** If hybrid is still being weighed, route to `samber/dev-event-organizer-skills@event-format-selection` and stop. Re-arguing it here wastes the only pass you get.
2. **Write down what the remote audience was promised**, in one sentence, from Q1. Every later choice is measured against that sentence, not against what is technically possible.
3. **Mark remote eligibility on the published grid** (Menu 1) as a column, not as a separate list. A separate list is a second document, and second documents drift.
4. **Choose the parity depth** (Menu 2). For what each rung looks like minute to minute, read [references/remote-eligibility-and-parity-mechanics.md](references/remote-eligibility-and-parity-mechanics.md).
5. **Hand the eligible-session list to `samber/dev-event-organizer-skills@event-production`** as an input to its own coverage-tier decision, per room. You name the sessions and the return path. It names the equipment. Never specify equipment yourself.
6. **Check the consent record covers what the feed will carry** (Q4). `samber/dev-event-organizer-skills@event-speaker-experience` holds that record, and `samber/dev-event-organizer-skills@event-production` states the constraint a live feed adds: "a speaker's opt-out has to be honoured in the room rather than in an edit". Settle this before the grid is marked, not after.
7. **Staff the remote side** (Menu 3), by name per streamed session rather than by function.
8. **Add the stream's cue track to the run of show** (see below) and hand it to `samber/dev-event-organizer-skills@event-run-of-show` as an addition to its document.
9. **Close the two-audience gap in the disruption priority order** (Q6) before the day, in writing, and say who decided it.
10. **Report the staffing consequence to `samber/dev-event-organizer-skills@event-budget`**, split by what a lean tier can drop. The feed itself survives every tier; the return path and the people watching it are what a lean tier cuts first.

Present the plan section by section for validation, in this order:

1. The promise.
2. Eligibility.
3. Parity.
4. Staffing.
5. The cue track.

Do this before the grid is published. After publication, removing a session from the remote programme is a public retraction rather than a decision.

If your harness has persistent memory, record per edition:

- What the remote audience was promised, and in whose words.
- Which sessions were marked eligible, and which speakers declined.
- How many remote questions actually reached a stage.
- Every moment the remote side was left unattended, and what the room was doing instead.
- What the disruption order turned out to say about remote.

A second edition should start from that record rather than from these defaults.

## Menu 1 - Session remote eligibility

Which sessions the remote audience gets. Mark this on the grid `samber/dev-event-organizer-skills@event-schedule-design` published - that skill's own limit is "You stop at the published grid", so the column is yours to add and the placement is never yours to change.

Ranking (default, not a law - Q1, Q2, Q7 and Q10 re-rank it):

- effort (rooms instrumented, crew committed, consent chased, editorial passes over the grid): `every session in every room > per-session speaker opt-in > curated remote programme > one designated streamed room > plenary only`. Opt-in outranks curation on cost, for two reasons worth stating:
  - An opt-in can land in any room, so you instrument every room, which is the top rung's bill.
  - Constrain where speakers may opt in and it stops being an opt-in. A curated set is bounded because you chose it, and you can choose it to sit in rooms already carrying a feed.
- value, breadth (how much of the programme a remote attendee can actually watch): `every session in every room > per-session speaker opt-in == curated remote programme > one designated streamed room > plenary only` - argued tie: neither delivers a predictable share of the programme. How many speakers say yes sets opt-in's breadth; the organizer's own editorial ceiling sets curation's. Which ends up wider is not knowable before the fact.
- value, coherence (a remote attendee gets a day that holds together rather than a scatter of fragments): `curated remote programme > one designated streamed room > plenary only > every session in every room > per-session speaker opt-in`. This axis is why the menu is not a ladder:
  - A curated programme is designed as a remote day. A single streamed room is at least a continuous thread. Plenary-only is short but complete.
  - Streaming everything hands a remote attendee a multi-track grid they can watch only one stream of, with none of the corridor cues that make a room's choice easy.
  - Opt-in ranks worst: it produces holes at times nobody can predict.
- compliance cost (the review it triggers and what stops being reversible): `every session in every room > curated remote programme == per-session speaker opt-in > one designated streamed room > plenary only` - argued tie: both put a mid-sized, organizer-known subset of the programme out. The curated set arrives needing each chosen speaker's consent chased. The opt-in set arrives with the speaker's consent already given and needs the in-room audience's covered instead: the questioners whose voices and faces go out live. Same review, different half of it. What makes this axis real rather than decorative is the sibling constraint quoted above, an opt-out honoured in the room rather than in an edit, and "A published stream cannot be recalled from the people already watching it."
- efficiency: `plenary only > one designated streamed room > curated remote programme > per-session speaker opt-in > every session in every room`

**Dominance check: 5 rungs, 10 pairs, two cost axes and two value axes, and one real strict-dominance relation.**

The curated remote programme strictly dominates per-session speaker opt-in: cheaper on effort, tied on compliance, tied on breadth, strictly better on coherence.

The remaining nine pairs split into two blocks:

- Blocked by breadth alone, where the cheaper rung also wins coherence and loses only on how much a remote attendee can watch (five pairs): plenary-only against opt-in, plenary-only against every-session, one-room against opt-in, one-room against every-session, and curated against every-session.
- Blocked by cost running opposite to both value axes (four pairs): plenary-only against one-room, plenary-only against curated, one-room against curated, and opt-in against every-session.

That accounts for all ten (1 relation + 5 + 4).

- **One designated streamed room** - the default: one room is the remote room, and whatever the grid puts in it is what remote gets. It buys a continuous day for the cost of instrumenting one room, needs no per-session negotiation, and collapses the eligibility question into a room-booking question the schedule already answered. **Move up to the curated programme** whenever Q1 says the remote audience paid or was promised specific content. A room chosen for its cabling is not a programme anyone was promised.
- **Plenary only** - the minimum, and it wins outright more often than it looks. The opening, the keynotes and the closing carry the widest audience, usually sit in the room already best equipped, and make sense to someone who is not in the building. It is the honest choice when Q1's answer is "nothing written down".
- **Curated remote programme** - organizers choose the sessions that serve a remote audience specifically, and mark them. Tops coherence, mid on everything else. It treats the remote audience as an audience rather than as an overflow.
- **Per-session speaker opt-in** - strictly dominated above, and kept on the menu for one reason: a consent posture can hand it to you already decided. Where `samber/dev-event-organizer-skills@event-speaker-experience`'s consent record is per-speaker and opt-out is genuinely offered, the eligible set _is_ whoever said yes. Make the resulting holes legible rather than pretending they are a programme.
- **Every session in every room** - the starved option: tops breadth, tops both cost axes, bottoms coherence, so efficiency never picks it. Promotion conditions:
  - Keyed to Q1: a paid virtual ticket sold as access to the whole programme.
  - Keyed to Q2: a venue where every room is already instrumented, so breadth costs nothing extra to reach.
- **Delete, do not demote: publishing the recordings afterwards and calling that the remote programme.** Strike it from this menu and from the axis lines above. It reads as the cheapest hybrid and it is not a hybrid at all. A remote audience that watches next week is the in-person-with-record-and-post delivery mode, which `samber/dev-event-organizer-skills@event-format-selection` names separately and which this event has already decided against. Leaving it parked at the bottom is how a hybrid quietly becomes a recorded event with a broken promise attached. Post-event publication is real work, and it belongs to `samber/dev-event-organizer-skills@event-content-repurposing`.

## Menu 2 - Parity depth

How far a remote attendee's voice reaches the stage. This is the menu the second-class finding is about, and the one where doing very little is a legitimate answer.

Ranking (default, not a law - Q1, Q3, Q9 and Q10 re-rank it):

- effort (equipment in the room, a person's attention during the session, briefing, rehearsal, a return path into the room's audio): `remote participants appear in the room > reserved floor time for remote questions > live relay by a named person > an asynchronous written return path > feed only`
- value, the remote voice reaches the stage (a remote attendee's question is actually answered by the speaker, live): `remote participants appear in the room > reserved floor time for remote questions > live relay by a named person > an asynchronous written return path > feed only`
- value, the room's own session is undamaged (the speaker and the in-room audience get a session that is not slowed, interrupted or reshaped by the remote layer): `feed only > an asynchronous written return path > live relay by a named person > reserved floor time for remote questions > remote participants appear in the room`. **This axis is rank-identical to inverse effort, which is the pathology the ranking discipline warns about.** On its own it would collapse this menu into cheapest-first. It stays because it discriminates nothing about the ordering and everything about the _incidence_: it names who pays for each rung, and that payer is the in-room audience rather than the organizer. Read it as a statement of who bears the cost, never as an independent reason to pick a rung.
- compliance cost (the review it triggers and what stops being reversible): `remote participants appear in the room > reserved floor time == live relay by a named person == an asynchronous written return path > feed only` - argued tie for the middle three: each collects text a remote attendee typed into a channel the event already opened. That is the same record under the same terms whether it is read aloud, read on a rule, or answered next week, and none of the three puts a new person's likeness anywhere. Feed-only is lowest because no return channel means no remote-side record to hold. The top rung differs in kind: it puts an identifiable person into the room's own captured output, so it needs that person's consent _and_ it lands inside the in-room recording's envelope, where "A camera in the room is not agreement" and a published stream cannot be recalled.
- efficiency: `feed only > live relay by a named person > an asynchronous written return path > reserved floor time for remote questions > remote participants appear in the room`

**Dominance check: 5 rungs, 10 pairs, two cost axes and two value axes, zero strict-dominance relations.**

One mechanism accounts for all ten, and it is the only one operating. The reaching-the-stage axis runs strictly opposite to effort and strictly opposite to the room's own session. On every pair the cheaper rung wins the room and loses the stage, so no rung is at least equal on everything.

Compliance runs the same way but does not carry the block on its own: the three middle rungs tie on it by the argued tie above, so on three of the ten pairs compliance separates nothing.

The check catches no misordering. What follows is argument, not verification, and this menu is clean only by construction.

- **Live relay by a named person** - the default: remote questions arrive in a channel, and one named person in the room reads them aloud during Q&A. It is the cheapest rung on which a remote attendee's question is answered by the speaker, out loud, while they are watching. Sitting one rung above the efficiency leader is deliberate. An event that passed the format decision's gate did so because a remote audience mattered enough to pay for. Buying the most expensive delivery mode while delivering the cheapest parity is the failure this whole skill exists to name.
- **Feed only** - the minimum, and genuinely often the right answer. Remote watches and that is all. **Drop to it whenever Menu 3 cannot name a person for a session.** An open question channel nobody reads during the session is worse than no channel: it invites a question in the moment and drops it in the moment, in front of the person who asked. That is the second-class experience in its purest form.
- **An asynchronous written return path** - questions collected with a _stated_ promise: answered in writing, by whom, by when. It costs no attention during the session, and it is honest, which is what separates it from the deleted rung below. It buys a real answer and never a live one.
- **Reserved floor time for remote questions** - the moderator holds part of Q&A for remote by rule rather than by goodwill. The rule is the point: goodwill loses to a room full of raised hands every time, because the in-room audience has a default channel and the remote one does not. It costs the moderator a brief, and the discipline to hold the rule under time pressure.
- **Remote participants appear in the room** - the starved option: tops the voice axis, tops effort, tops compliance, so efficiency never picks it. It is the only rung where the speaker answers a person rather than reading a line. The return audio path itself is `samber/dev-event-organizer-skills@event-production`'s to build: specify the requirement, never the equipment. Promotion conditions:
  - Keyed to Q1: a paid virtual ticket sold on participation rather than viewing.
  - Keyed to Q1: a sponsor deliverable that names remote interaction.
  - Keyed to Q3: a remote audience concentrated enough that the people awake are the people who matter.
- **Delete, do not demote: an open remote question channel with nobody reading it.** Strike it from this menu and from the axis lines above. It reads as parity's free version, and it is the one rung worse than the floor: it makes a promise inside the session and breaks it inside the same session. It also carries a conduct duty with no responder, which `samber/dev-event-organizer-skills@event-comms-channels` already argues as a standing cost rather than a setup cost. The asynchronous rung above is a different artifact: it states what will happen, and someone is answerable for it.

## Menu 3 - The crew split and the remote advocate

Who is looking after the remote side, and where they are standing. Define the remote advocate's authority explicitly in your document, as you would for any role that is not an industry standard.

Ranking (default, not a law - Q2, Q8, Q9 and Q10 re-rank it):

- effort (people committed per streamed session-hour, briefing depth, roster complexity): `a host on the feed as well > a watcher off the floor and an advocate in each room > an advocate inside each streamed room > one watcher off the floor, event-wide > no split`. The advocate outranks the watcher on cost for two compounding reasons:
  - It scales with streamed rooms. One watcher covers however many rooms exist, so the gap widens with every room added.
  - It needs a session-by-session briefing on the programme and the questions. The watcher needs only the output.
- value, the remote audience is served inside a session (a question is relayed, remote is acknowledged, the speaker knows they are there): `a host on the feed as well == a watcher off the floor and an advocate in each room > an advocate inside each streamed room > one watcher off the floor, event-wide > no split` - argued tie: the host works the gaps between sessions, so it adds nothing inside one. The two rungs put the same person doing the same relay in the same room.
- value, a remote failure is noticed and named (a dead, silent or frozen feed is caught and the remote audience is told): `a host on the feed as well > a watcher off the floor and an advocate in each room > one watcher off the floor, event-wide > an advocate inside each streamed room > no split`. **The crossing here is the finding**: the lone watcher beats the in-room advocate on this axis while costing less, because the watcher sees what the audience receives and the advocate sees the room. An advocate standing beside the stage is the last person who will notice the stream died.
- efficiency: `an advocate inside each streamed room > one watcher off the floor, event-wide > a watcher off the floor and an advocate in each room > a host on the feed as well > no split`

No compliance-cost axis is printed, because nothing here varies on one. Every rung's exposure is whatever Menu 1's eligibility and Menu 2's parity depth already fixed. Adding a person changes who notices a failure, not what is captured or published.

**Dominance check: 5 rungs, 10 pairs, one cost axis and two value axes, zero strict-dominance relations.**

Three mechanisms account for all ten, and none covers another's pairs:

- Blocked by the plain mechanism, cost running opposite to both value axes at once (eight pairs): no-split against each of the four staffed rungs, the lone watcher against the both-rung and against the host rung, and the advocate against those same two.
- Blocked by the two value axes genuinely crossing (one pair): the lone watcher against the in-room advocate, where the watcher is cheaper and catches failures better, and only in-session service saves the advocate.
- Blocked because in-session service ties and only the failure axis separates them (one pair): the both-rung against the host rung.

Zero relations means the check caught no misordering.

- **An advocate inside each streamed room** - the default: one named person per streamed session whose job is the remote audience. They relay questions, they say out loud that remote is watching so the speaker addresses them, and they are the person Menu 2's default rung requires. It scales with streamed rooms rather than with remote headcount, so it needs no per-attendee ratio. None has been published. **Move up to the both-rung** as soon as Q2 says more than one room carries a feed at once, since nobody standing in one room can see another room's output.
- **One watcher off the floor, event-wide** - a person in no room at all, watching the outgoing feed as a remote attendee receives it. The watcher sees what the room's crew structurally cannot: whether the feed is live, audible, or frozen. It beats the default whenever Menu 2 landed on feed-only, where there is nothing to relay and everything to watch.
- **A watcher off the floor and an advocate in each room** - both postures at once, and the first rung that covers both value axes properly rather than trading one for the other.
- **A host on the feed as well** - the starved option: ties the top of in-session service, tops the failure axis, tops effort, so efficiency never picks it. It is the only rung where somebody speaks to the remote audience during the gaps a room fills with corridor conversation, the stretch where a remote attendee has nothing at all and no way to tell a break from a failure. Promotion conditions:
  - Keyed to Q1: a paid virtual ticket.
  - Keyed to Q1: a sponsor deliverable naming the stream.
  - Keyed to Q8: a recurring event where the same person can hold the role again and the briefing is written once.
- **Delete, do not demote: the room lead doubling as the remote advocate.** Strike it from this menu and from the axis lines above. `samber/dev-event-organizer-skills@event-run-of-show` defines that role as "one person per room who owns that room's clock: holds a start, cuts a Q&A, gets the tech owner, and escalates to the on-duty organizer". That is precisely the job competing with relaying a remote question, at precisely the moment both come due. It reads as the free version of the default, and it guarantees which of the two gets dropped.

## The cue track the stream needs

This is a delta on an existing artifact, not a menu. Forcing a ranked ladder onto one added column would be padding, so it stays a section.

`samber/dev-event-organizer-skills@event-run-of-show` owns the day-of document. A hybrid needs no second one. It needs a second **column** on the same rows, because two documents drift and the drift is invisible until the day.

- Hand that column to that skill as an addition.
- Never author a parallel document.

What the column carries, per row:

- What the stream is showing at that moment: the stage, the slides, or a holding card.
- Who owns that decision.
- What the remote audience is being told.

The synchronization rule: the room's transition and the stream's transition are the same row. A cue that exists in only one column is exactly where the two audiences diverge, and it is the row to re-read at the briefing.

Two row types deserve the most attention, and neither is a session:

- Every gap. The room fills a break with corridor conversation and the stream fills it with nothing, so a remote attendee cannot distinguish a scheduled break from a failure.
- Any moment the room is told something out loud that was never typed anywhere: a room change, a delay, a swapped speaker.

The second type is the documented failure this skill exists around: a workshop running late, remote participants never told, the staff busy in the room.

**A gap this order does not close.** `samber/dev-event-organizer-skills@event-schedule-design` writes a disruption priority order into the grid document and hands it over. `samber/dev-event-organizer-skills@event-run-of-show` restates it in its own words as "protect the plenary or keynote first, protect the headline commitment the audience showed up for next, minimize how many other sessions the fix disturbs, then lock the revised grid for the rest of the block", and executes it.

Read the audience in that sentence. It is singular, and a hybrid has two.

Hybrid conferences and AV crews document a default for most of what that raises:

- Keep the room going and fix a dead feed in parallel, rather than pausing on reflex.
- Put the authority to give up on a feed inside the technical chain, escalated to a senior organizer, never a volunteer left alone with the call.
- Give the remote side a named live-chat contact rather than an intermittently checked inbox.

Two questions have no documented answer:

- Who wins when the remote-side person and the room lead need the same technician at once.
- Whether a session moved to fix an in-room problem takes the remote programme with it.

Decide both in advance. Write them into the document beside the documented defaults, say who decided them, and never present either as inherited practice, because neither is. For each default and where it comes from, read [references/dual-audience-cue-track.md](references/dual-audience-cue-track.md).

## Failure modes

- **Re-deciding the format.** The cost case against hybrid is owned upstream, and it is strong. Rehearsing it means you are in the wrong skill: the user needs the format decision, not this one.
- **Attention, not equipment.** Both documented failures are about where the staff were looking: remote attendees not told a schedule slipped, and remote check-in lagging because the team was checking in the room. Buying more equipment fixes neither.
- **Parity by goodwill.** "We'll take remote questions too" loses to a room of raised hands every time, because the in-room audience has a default channel and remote does not. Either a person owns it or a rule reserves it.
- **A question channel nobody reads.** The one rung worse than giving remote nothing: it invites a question and drops it in front of the person who asked.
- **The gaps.** Between sessions the room has a corridor and the remote audience has silence, indistinguishable from a dead feed. Say something on the stream, or publish in advance what the silence means.
- **Marking eligibility after publication.** A session removed from the remote programme after the grid is public is a retraction, not a decision. Settle consent and instrumentation first.
- **Specifying equipment.** Cameras, encoders, uplinks and return audio belong to the production sibling. State the requirement. Let it state the kit.
- **Assuming the remote audience is small enough not to matter.** Academic conferencing data on remote turnout exists but transfers poorly to technology events. The contexts are too different. Do not invent a planning number here.

## Measurement

Three completeness gates, checkable before the first session and free of any threshold to argue about:

- Every remote-eligible session has a named person for the remote side, or its return path is closed. Not a function - a name.
- Every row of the cue sheet that changes what the room sees also says what the stream shows.
- The disruption priority order says, in writing, what happens when a remote-side failure and an in-room one compete.

Everything below is a metric you set rather than an industry standard. Say so when you present it.

- **Remote questions that reached a stage**, against remote questions asked (self-set). This is the number Menu 2 actually moves, and the one that tells you whether the parity rung was real or nominal.
- **Announcements made in the room that never reached the remote channel** (self-set). Counted, never minimized - this is the documented failure, measured directly.
- **Time from a feed problem starting to the remote audience being told something** (self-set). This is what Menu 3's watcher rung buys.
- **Remote-eligible sessions delivered without an audience-visible failure**, over remote-eligible sessions scheduled (self-set).

Pick two or three, write down what change each would trigger, and record them before the event rather than after.

## Invocation examples

- "We're streaming our conference this year as well as running the room. Which talks should remote actually get?"
- "How do we make sure remote attendees get real Q&A and not just a video feed?"
- "Who do we need on the day for the remote side, on top of the AV crew?"
- "Write the run of show for a day with both an in-room and an online audience."
- "Our remote attendees said they felt like second-class attendees last year. What do we change?"

Expected output: a hybrid design with:

1. What the remote audience was promised, in one sentence.
2. The eligibility column marked on the published grid, with the rung chosen.
3. The parity depth and what it looks like inside a session.
4. The remote-side staffing assigned by name per streamed session.
5. The stream's cue column handed to the run of show.
6. The two-audience disruption rule, with the person who decided it.
7. The staffing consequence split for the budget.

Presented section by section for validation before the grid is published.

## References

- [references/remote-eligibility-and-parity-mechanics.md](references/remote-eligibility-and-parity-mechanics.md) - read while choosing the parity depth: what each rung looks like minute to minute, the relay mechanic, and the consent questions a live feed adds.
- [references/dual-audience-cue-track.md](references/dual-audience-cue-track.md) - read while writing the cue column: worked rows, the gap rows, and where each disruption default comes from.
