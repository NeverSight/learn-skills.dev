---
name: event-production
description: Engineer the technical AV production of a technical event once the format and session grid are fixed - capture tiers from a single smartphone to multi-camera vision mixing, signal-path architecture separating room display from recorded output and crew monitor, redundancy against named recorded-audio failure modes, AV crew roles, the written technical spec handed to venue sourcing, the Media budget line, rehearsal, and the publication pipeline. Use whenever the user mentions conference AV, recording or livestreaming talks, cameras, microphones, an AV supplier brief, or a backup plan for a technical failure - even if they never say "production". Do NOT use to decide whether to run hybrid or virtual at all - use samber/dev-event-organizer-skills@event-format-selection instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Production

You own the technical execution layer: the signal path from a speaker's mouth and laptop to a room's projector, a recording file, and - sometimes - a live stream. Everything upstream arrives decided:

- `samber/dev-event-organizer-skills@event-format-selection` decides whether the event is hybrid or streamed at all.
- `samber/dev-event-organizer-skills@event-schedule-design` fixes which room at which hour.
- `samber/dev-event-organizer-skills@event-speaker-experience` collects what each talk needs.

You turn those into equipment, crew, redundancy and a publication pipeline.

Five boundaries, four of them stated by the sibling from its own side.

- **Venue.** `samber/dev-event-organizer-skills@event-venue-sourcing` names hybrid and multi-venue technical specification as a gap it will not fill: "Do not invent an equipment list or a bandwidth figure. Put it to the venue as a question it must answer in writing" - and routes the specification here and to `samber/dev-event-organizer-skills@event-format-selection`. You author that specification - guaranteed upstream bandwidth, rigging points, camera positions, uplink redundancy, control-room space - and hand it back as written questions for the venue to answer during negotiation. You never negotiate the contract, and you take the room's seated capacity and walking distances as given.
- **The day.** `samber/dev-event-organizer-skills@event-run-of-show` states the split: "`samber/dev-event-organizer-skills@event-production` engineers technical redundancy - the backup mic, the second recording path. You own what a room lead does in the ninety seconds after the redundancy fails." Build the backup path before the day starts. Never re-describe live incident escalation here.
- **Speakers.** `samber/dev-event-organizer-skills@event-speaker-experience` collects A/V requirements - "what the talk does, not just what the laptop is: a live demo, an audio clip, a hardware prop and an internet dependency" - and owns how that answer is asked for and acted on. You consume what it collects and you consume its consent record. You never publish a recording the consent record does not cover.
- **Captioning.** `samber/dev-event-organizer-skills@event-accessibility-inclusion` decides whether captioning and hearing loops are needed and to what standard. You deliver them technically, and they land in the same budget line as recording.
- **The supplier.** `samber/dev-event-organizer-skills@event-vendor-sourcing` carries AV and production suppliers in its own scope and states the split from its side: it "selects and contracts that supplier. Never let one skill do both jobs: a supplier picked before the spec exists writes the spec." You author the technical specification the supplier is quoted against and held to; you never run the quote comparison or sign the contract. Hand the brief over before selection starts, not after a quote arrives.

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank all three menus against what you know:

- A venue with a house technician and installed cameras.
- A community that already runs a video crew across editions.
- An event that has never published a video.
- An owned equipment stock.

Each of these overturns a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the menus diverge sharply on time-to-effect, durability and effort - those orderings cannot be picked for the user.

1. **Is anything captured at all, and in what form: nothing, recorded for later, or streamed live?** This is the question that reorders every menu below. Ask it first and get a real answer rather than an aspiration.
2. What did the format decision actually commit to, and to whom? A promised livestream is a commitment; a hoped-for one is not.
3. What is the grid - how many rooms run at once, how long is the shortest changeover between sessions, and which sessions are plenary?
4. What did speaker collection return: live demos, audio playback, hardware props, internet dependencies, non-standard connectors? Which of those has no answer yet?
5. What is the recording and publication consent posture per session format, and where is that record held? You cannot publish past it.
6. What does the venue actually give you - a house technician or not, installed projection and sound or not, rigging points, a control-room space, an internet connection with a guaranteed upstream figure or a shrug?
7. What is the last date the venue or the supplier can still add something? That deadline, not the event date, is what these menus are ranked against.
8. One-off edition or a recurring event? A recurring event promotes every rung whose payoff lands after this edition ends: a trained crew, a written brief, owned equipment, a repeatable pipeline.
9. What is the effort ceiling - who runs this on the day, how many people can be doing only production rather than also doing something else, and does anything have to be reversible after the event?
10. Has accessibility decided on captioning or hearing loops? That decision lands in your budget line and your signal path, and it is not yours to make.
11. What already exists that should re-rank the menus: cameras the community owns, a crew that has done this four times, a venue that streams its own events, last edition's recordings and what went wrong with them?
12. Is the audience genuinely distributed, such that reaching a remote half is the point of the event rather than a bonus?

## What actually splits this work

This collection usually replaces the B2B/B2C split with community-run versus vendor-run. Test it here rather than assuming it: it splits the crew and almost nothing else.

It holds for crew, which splits into two poles:

- **Community pole.** Staffs production with volunteers. The sourced training ladder is built exactly for that pole: a full introduction deck "for events without 'experienced' A/V angels," a brief refresher plus hands-on training "for experienced angels" at a recurring event (C3VOC).
- **Vendor pole.** Contracts a supplier. The source addresses it as an external party: "your audiovisual company should be able to provide a camera or cameras" (DevOpsDays).

Those are genuinely different jobs: one is recruiting and training people, the other is writing a brief and holding a supplier to it.

Capture posture is the axis that reorders everything else. Nothing captured, recorded for later, and streamed live are three different events technically, and the difference dwarfs who is paying:

- **Nothing captured.** Needs a working room and no pipeline at all.
- **Recorded for later.** Needs a clean signal, a reliable file and somewhere to put it. Forgives almost every failure that lasts under a minute.
- **Streamed live.** Forgives nothing, needs rehearsal and a dedicated operator (DevOpsDays), carries a takedown risk on published platforms, and consumes an uplink nobody has measured.

State which of the three a recommendation assumes whenever they differ.

When asked to execute a hybrid or streamed format, report what the format costs technically before it is locked, then stop. The format decision belongs upstream; your job is to make sure it is taken with that number visible.

The clearest published finances available say hybrid "AV support" ran "more than double the cost of a physical-only conference," alongside a $484,886 loss in the year that conference ran fully hybrid (ACM SIGCHI, published Nov 2023). It is an academic conference, not a developer one: cite the ratio, never the figure, and never attribute it to a developer conference.

## Workflow

1. **Establish capture posture.** Nothing, recorded, or streamed. Write it down. Everything downstream is a consequence of this line.
2. **Read the inputs rather than re-collecting them:** the grid, the per-speaker A/V needs, the consent record per format, the accessibility decisions, and the venue's own answers.
3. **Pick the coverage tier** (see below) per room, not for the event as a whole. A plenary room and a third breakout room rarely deserve the same tier.
4. **Draw the signal path** before ordering anything: where audio is captured, where it is mixed, where the room's display feed splits from the recorded feed, and where the crew watches what is actually going out. See [references/signal-path-and-redundancy.md](references/signal-path-and-redundancy.md).
5. **Engineer redundancy against named failures**, not against a general fear of failure (see below). The failure list is sourced; use it rather than improvising one.
6. **Assign crew roles and pick training depth** (see below). Name people, not functions.
7. **Write the venue technical specification as questions** and hand it back to venue sourcing to put in front of the venue in writing. Do not state a bandwidth figure you do not have - ask for a guaranteed upstream number and get it in the contract. Template in [references/av-supplier-brief.md](references/av-supplier-brief.md).
8. **Write the supplier brief** and hand it to whoever contracts the supplier. See [references/av-supplier-brief.md](references/av-supplier-brief.md).
9. **Hand the Media cost line to `samber/dev-event-organizer-skills@event-budget`** with its tiering already split (see below). Supply the content; the budget decides the shape.
10. **Rehearse, if anything is live.** Rehearsal is sourced as a requirement for streaming, not a nicety, and it is the step that gets cut first. It is also the only place a signal path gets tested end to end before an audience is in the room.
11. **Run the post-event pipeline:** verify every file exists and is playable before the crew disperses, then edit, check against the consent record, publish, and send each speaker their own link.

Present the production plan section by section for validation, before anything is ordered:

1. Capture posture and coverage tier.
2. Signal path and redundancy.
3. Crew and training.
4. Venue spec and supplier brief.
5. Budget and pipeline.

After the order goes in, changes cost money rather than a conversation.

If your harness has persistent memory, record per edition:

- The venue's real answers on bandwidth, rigging and house equipment.
- Which coverage tier each room actually got.
- Every failure that happened and which redundancy caught it.
- How long the pipeline took from event to published video.
- What the supplier actually delivered against the brief.

A venue and a supplier used twice are worth not re-learning.

## Coverage tier

Recording is the floor and streaming is the layer above it: that ordering is sourced, not a preference. Published guidance states it plainly - "whether or not you're able to livestream, it's important to record all the talks" (DevOpsDays) - and the same guide's own tiered-budget mechanic makes streaming the first thing a lean tier drops while recording survives.

Ranking (default, not a law - Q1, Q7, Q8 and Q11 re-rank it):

- effort (equipment, people on the day, rehearsal, coordination with the venue's network): `live stream on top of two cameras > two cameras with vision mixing > single operated camera > fixed camera on the board feed > smartphone floor > no capture`
- value (a talk that outlives the day, and a speaker with something to show for it): `live stream on top of two cameras > two cameras with vision mixing == single operated camera > fixed camera on the board feed > smartphone floor > no capture` - argued tie: both put a watchable, audible talk in the archive, which is the whole of the value for an audience watching later. The second camera buys slide detail and reaction shots, and the operator buys framing; neither buys a talk that did not otherwise exist.
- compliance cost (the review it triggers, and what stops being reversible): `live stream on top of two cameras > two cameras with vision mixing == single operated camera == fixed camera on the board feed == smartphone floor > no capture` - argued tie: every recorded rung needs the same thing, a consent record covering that session's format before anything is published, and none of them is harder to obtain than the others. Streaming is the rung that changes the review, because a live feed is published before anyone can check it. A speaker's opt-out has to be honoured in the room rather than in an edit, and background music in a demo can take the stream down on the platform's own initiative (DevOpsDays). A published stream cannot be recalled from the people already watching it.
- efficiency: `fixed camera on the board feed > smartphone floor > single operated camera > two cameras with vision mixing > live stream on top of two cameras > no capture`

- **Fixed camera on the board feed** - the default and the sourced recommendation: a camera and a recording computer taking audio off the mixing board rather than the camera's own microphone. Near-zero on the day once set, and the board feed is what makes the result listenable. Move up one rung when slides carry the talk and a wide shot cannot read them, or when a plenary is the recording anyone will actually watch.
- **Smartphone floor** - the sourced absolute minimum: "if you have no budget for recording talks, a smartphone is better than nothing." It sits second on efficiency rather than first because a phone on a tripod at the back of a room captures room audio, and a talk you cannot hear is not an archive. Use it for a room you were going to leave uncovered, never as the plan for the room that matters.
- **Single operated camera** - a person framing the shot, following the speaker, and holding on the slides when the slides are the point. Buys watchability; costs one trained person per room per session.
- **Two cameras with vision mixing** - a second angle plus somebody switching between feeds. The camera operator and the vision mixer are two separate named roles in sourced practice, not one person with more work.
- **Live stream on top of two cameras** - the starved option: tops value and tops effort, so efficiency never picks it. It also needs the two things the source names explicitly and every organizer under-provisions: rehearsal ahead of time, and at least one person whose only job during the event is running it. **Promotion conditions, keyed to Q2, Q2, Q12 and Q6/Q11**: an audience that genuinely cannot travel and was promised access, a sponsor commitment that names streaming, a distributed community whose remote half is the point of the event, or a venue that already streams its own events and hands you the uplink.
- **Delete, do not demote: streaming with no rehearsal and no dedicated operator.** It reads as the cheap version of streaming and it is not a rung on this ladder - it is the same cost with the failure built in, discovered live, in front of the exact audience the stream existed to serve. Parked at the bottom of a menu it reappears as "we'll just point the laptop at it."

## Redundancy depth

Redundancy here means a backup path engineered before the day, not a person improvising during it. The sourced failure list is what it protects against, and the load-bearing lesson is that a backup system has its own failure modes.

At one large conference (C3VOC, 34C3), the backup existed and was still unusable:

- 128 recorded audio tracks with no labels.
- A recorder with no clock sync.
- Drives a person had to physically carry to an unloading station and back.
- A bulk copy that spiked the network on a predictable cadence.
- Multi-gigabyte files nobody could seek through afterwards.

The redesign written to replace it writes chunked, named files synced continuously to a storage server. Full detail in [references/signal-path-and-redundancy.md](references/signal-path-and-redundancy.md).

Ranking (default, not a law - Q1, Q6, Q8 and Q9 re-rank it):

- effort (hardware, wiring time, setup per room, someone who understands it): `duplicate encode path > continuous chunked sync to storage > three-destination signal split > independent second audio recording > spare mic and spare cable`
- value (a usable file exists after a failure nobody noticed at the time): `continuous chunked sync to storage > independent second audio recording > duplicate encode path > three-destination signal split > spare mic and spare cable`
- value (the session in the room keeps running): `spare mic and spare cable > three-destination signal split > duplicate encode path == independent second audio recording == continuous chunked sync to storage` - argued tie: all three sit downstream of the split that feeds the room, so none of them is audible or visible to the audience. They protect the archive and the stream, and the room never knows either way.
- efficiency: `spare mic and spare cable > independent second audio recording > three-destination signal split > continuous chunked sync to storage > duplicate encode path`

- **Spare mic and spare cable** - the default: a second microphone within reach, spare batteries, a spare cable for every run, and a spare adapter for every connector the speaker collection surfaced. Near-zero, and it is the only rung that saves the session happening right now. Move up one rung the moment any session is not repeatable - a keynote, a launch announcement, a speaker who flew in for one talk.
- **Independent second audio recording** - a recorder that is not in the live mix, capturing the same source. The point is independence: a failure in the mixing or encoding chain does not reach it. Audio-only, because audio is what makes a recording usable and video without it is not.
- **Three-destination signal split** - the sourced architecture pattern: one input, split to the room's projector with minimal delay, to the encoder that produces the recorded or streamed output, and to a monitor the crew watches. Those are three destinations, not three copies of one pipeline, and a failure in the encode path does not have to take down what the room sees or what the crew is watching. Its second payoff is diagnostic: without the crew's own monitor, nobody finds out the recording has been black for forty minutes.
- **Continuous chunked sync to storage** - the starved option: recordings written as short, named, clock-synced chunks and synced continuously to a server rather than collected in bulk afterwards. It tops the archive-value axis, because every failure mode it fixes is one where the recording nominally succeeded and was useless anyway, and it tops effort, needing infrastructure and someone who maintains it. Promotion conditions: a multi-room event where files are collected from several rooms at once, a recurring event that will amortise the setup, an archive somebody has committed to publishing on a deadline, or a previous edition where a recording was lost or unusable.
- **Duplicate encode path** - a full second encoding chain in parallel. Real redundancy, real cost, and it protects the layer that is already the least likely to fail silently.
- **Delete, do not demote: an unlabelled backup nobody has tried to open.** A drive full of unnamed tracks with no time sync is not a backup, and the moment it is needed is the wrong moment to discover that. Every backup rung above owes a labelling convention and one test playback before the event.

## Crew and training

Sourced practice names six distinct crew roles, not one "AV person" (C3VOC):

- Stage manager.
- Audio operator.
- Camera operator.
- Video/vision-mixing operator - a different person from the camera operator.
- AV-technical lead, above the operator roles.
- General crew.

Which of them exist on your event is the staffing decision below. What each one does minute to minute is yours to define; see [references/crew-roles-and-training.md](references/crew-roles-and-training.md) for the role split and the training ladder.

Ranking (default, not a law - Q1, Q8, Q9 and Q11 re-rank it):

- effort (people recruited, hours trained, coordination on the day, money): `full role split per room > contracted supplier plus a named counterpart > audio and video split > one named production owner`
- value (the technical failure that does happen gets caught by somebody whose job it was): `full role split per room > contracted supplier plus a named counterpart > audio and video split > one named production owner`
- efficiency: `one named production owner > audio and video split > contracted supplier plus a named counterpart > full role split per room`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations.** Clean only by construction, and by-construction is never a pass. Value and effort are the same list, so one mechanism blocks all six pairs: the staffing that catches more failures costs strictly more people, hours, and money.

No third axis is printed to block or rescue a pair. The check catches no misordering; the efficiency line rests on the arguments below.

- **One named production owner** - the default: a single person who owns the signal path, has walked it, and is not also MCing, speaking or running registration. Near-zero cost, and it converts "the AV" from a hope into somebody's job. Move up one rung as soon as more than one room runs at once, or as soon as anything is live.
- **Audio and video split** - two people, because the failures are unrelated and they happen simultaneously. Audio is where the archive is won or lost; video is where the room's attention is.
- **Contracted supplier plus a named counterpart** - the vendor pole. The supplier brings the crew; you still name one organizer who owns the brief, checks delivery against it, and is reachable on the day. A supplier with no counterpart delivers what it usually delivers, not what you asked for.
- **Full role split per room** - the starved option: stage manager, audio, camera, vision mixing and a technical lead, per room. Tops value and tops effort together, so efficiency never picks it, and at community scale the headcount it needs _is_ the whole organizing team. Promotion conditions: multi-camera coverage in any room, a live stream, a recurring event with a returning crew that already knows the roles, or a room where a failure is unrecoverable.
- **Delete, do not demote: the venue's house technician as the whole plan.** It is not a cheap rung, it is an unowned one - a house technician runs the house system, and nobody in that arrangement owns your recording, your consent record or your files. Keep the technician; add an owner.

**Training depth** follows a sourced two-tier ladder rather than a single onboarding.

- Run the **full introduction** when the host community has no experienced crew: a first edition, a new team, a venue nobody has worked.
- Run the **brief refresher plus hands-on for newcomers** when a returning crew already knows the drill. This is the recurring-event case, and the reason a trained crew is one of the highest-return investments a repeating event makes.

Both are named practice. The hands-on tier splits into per-topic self-training decks - basics, camera, video mixer, talk timeline - and the operating detail behind each role (camera framing rules, mixer console moves, the phase-by-phase talk timeline) is in [references/crew-roles-and-training.md](references/crew-roles-and-training.md).

## Media budget line

Hand `samber/dev-event-organizer-skills@event-budget` a Media line, not a lump sum, and hand it already split by what survives a lean tier. The sourced taxonomy bundles **live streaming, recording and captioning** into one Media category, with **Signage** and **Internet** as separate categories you neither own nor absorb - attendee internet provisioning is a different line from the production pipeline's own uplink.

Split the line three ways so the budget can cut it without asking you:

- **Recording** - survives every tier down to the smartphone floor.
- **Captioning** - its necessity is an accessibility decision you deliver rather than decide.
- **Live streaming** - the first item a lean tier drops, and the one that takes rehearsal and a dedicated operator down with it.

Give each part equipment, crew and supplier quote separately. A single Media number gets cut whole.

## On-site podcast setups

Treat an on-site podcast as talk recording at smaller scale, with three differences that actually matter:

- It needs a genuinely quiet room rather than a quiet corner.
- It needs one microphone per participant rather than one shared.
- Its consent question differs from a talk's: a conversational recording captures people who never agreed to be on stage.

Get consent per participant, in writing, before the first session, not from the schedule. Everything else is the same signal path and the same redundancy ladder above.

## Failure modes

- **Streaming with no rehearsal and no dedicated operator.** Published streaming guidance names both as requirements. An unrehearsed stream run by whoever is free fails live, in front of the audience it existed for.
- **Recording off the camera's own microphone.** The sourced chain takes audio off the mixing board. Room audio from a camera at the back produces a file nobody finishes watching, and it is discovered weeks later during editing.
- **A backup with no labels and no clock sync.** Sourced, at scale: recordings that existed and could not be used. Name files, sync clocks, and open one before the event.
- **Bulk-copying files over the event network.** A backup process that saturates the network on a predictable cadence has become an incident of its own. Sync continuously in chunks, or copy when nothing else needs the network.
- **Deciding the format instead of reporting its cost.** Hybrid roughly doubles AV cost in the clearest published finances available. Report that before the decision, then execute whatever was decided.
- **Publishing past the consent record.** A camera in the room is not agreement. The consent record names the session format and the opt-out answer; anything not covered stays unpublished, including a stream where the opt-out has to be honoured in the room rather than in an edit.
- **Background music in a recorded demo.** A concrete, sourced platform risk: a stream carrying incidental music can be taken down by the platform. Warn speakers before the day rather than filing an appeal after it.
- **Specifying a bandwidth figure you invented.** Ask the venue for a guaranteed upstream figure in writing and put it in the contract instead of naming a number yourself.
- **A pipeline with no owner after the event.** Files are collected, the crew disperses, and the videos are published five months later or never. Name the owner and the date before the event, and verify every file plays before anyone leaves the building.

## Measurement

Three completeness gates, checkable before doors open and free of any threshold to argue about:

- Every room's signal path has been walked end to end, with one test recording played back - not checked as a level meter, played back.
- Every published-recording plan has a consent record covering that session's format, and every session outside it is marked unpublishable.
- Every camera, recorder and encoder has a named owner for every block, and the livestream has a person whose only job it is.

Everything below is a metric you set rather than a benchmark to hit. Say so when you present it.

- **Capture completeness** (self-set): sessions with a usable recording, over sessions scheduled. Count "recorded but unusable" as a failure, since that is the failure the sourced case study is about.
- **Failures caught by a redundancy** versus failures that reached the audience (self-set). The ratio is what justifies the redundancy rung next edition.
- **Time from event end to published video** (self-set), plus the point in the pipeline where it stalled. This is the number that decides whether a recurring event needs a pipeline or a volunteer.
- **Supplier delivery against the brief** (self-set): line items delivered as specified, over line items in the brief. It only exists if the brief exists.

Pick two or three, write down the change each would trigger, and record them before the event rather than after.

## Invocation examples

- "We're recording all the talks at a two-room conference. What do we actually need?"
- "A sponsor wants us to livestream the keynote. What does that add?"
- "Write the AV brief we send to suppliers for quotes."
- "The venue asked what our technical requirements are. What do we send them?"
- "What's our backup plan if the mic dies during the keynote?"
- "How many people do we need on the video crew, and what does each of them do?"

Expected output: a production plan presented section by section for validation, before anything is ordered.

1. The capture posture stated in one line.
2. The coverage tier per room with its reasoning.
3. The signal path drawn end to end.
4. The redundancy rung chosen and the named failure each part protects against.
5. Crew roles assigned by name plus the training depth.
6. The venue technical specification written as questions for venue sourcing to put in writing.
7. The supplier brief.
8. The Media budget line split three ways.
9. The rehearsal plan.
10. The post-event pipeline with its owner and date.

## References

- [references/signal-path-and-redundancy.md](references/signal-path-and-redundancy.md) - the three-destination split in full, the documented failure-mode list and the redesign that answered it, what carries over to a smaller event and what does not, and a positive/negative pair of redundancy plans.
- [references/av-supplier-brief.md](references/av-supplier-brief.md) - the constructed supplier-brief template and the venue technical specification as written questions, with the bandwidth figure left for the venue to state in writing.
- [references/crew-roles-and-training.md](references/crew-roles-and-training.md) - the six sourced role names and what each covers, the two-tier training ladder with the promotion condition, the one-camera and two-camera coverage difference, and the rehearsal walkthrough.
- `samber/dev-event-organizer-skills@event-format-selection` - decides whether the event is hybrid or streamed; this skill reports what that costs technically and then executes it.
- `samber/dev-event-organizer-skills@event-speaker-experience` - collects per-speaker A/V needs and the recording consent record, both of which are inputs here and neither of which is re-collected.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - gathers the venue-side capacity answers this skill builds against; it routes the technical specification here and this skill hands it back as written questions.
- `samber/dev-event-organizer-skills@event-budget` - receives the Media cost line already split into recording, captioning and streaming, and decides how it fits the overall shape.
- `samber/dev-event-organizer-skills@event-vendor-sourcing` - selects and contracts the AV supplier against the technical specification authored here; never let one skill do both jobs.
- `samber/dev-event-organizer-skills@event-schedule-design` - fixes the grid the crew works inside; a room unfit for a format is reported upstream, never solved by dropping a session.
