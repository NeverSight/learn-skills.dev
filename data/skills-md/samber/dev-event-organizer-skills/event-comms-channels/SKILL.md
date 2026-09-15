---
name: event-comms-channels
description: Design the attendee-facing communication channel architecture for one edition of a technical event - which channels exist, who is on each, which class of message routes to which channel, how several writers stay consistent executing a register set elsewhere, and how every channel is wound down once the event ends. Use whenever asked whether an event needs a chat space, an app or a status page, where a room change or schedule slip should be announced, how to stop attendees missing announcements, who may post in the event's name, or what to do with the event's channels after it is over. Do NOT use for mailing-list copy and consent - use samber/dev-event-organizer-skills@event-attendee-email-sequences - or social copy - use samber/dev-event-organizer-skills@event-social-media.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Comms Channels

You design the set of channels a technical event talks to its attendees on, for one edition, from the moment attendees exist to the moment the last channel is closed. Your output is an architecture somebody else executes:

- A roster of channels with a stated job each.
- A rule that says where any given message goes.
- A process that keeps several writers sounding like one event.
- A dated wind-down for every channel you opened.

This skill writes no copy. The register, what the event sounds like, arrives fixed from `samber/dev-event-organizer-skills@event-cultural-identity`, which owns "the register (hacker, corporate, design, business) and its consistent expression across every touchpoint" (verbatim from that skill's own description).

Decide how a team of writers _executes_ that register across several channels without drifting. Never originate one.

## Siblings own part of this, and you must not re-derive them

| Sibling                          | The line                                                                                                                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event-run-of-show`              | Owns the organizer-only coordination channel, kept separate from every population-facing one. Never route staff coordination onto an attendee channel.                             |
| `event-code-of-conduct`          | Owns incident reporting entirely, including anonymous paths - exclude it from the roster - and the public-statement rule during an incident (enforced in § Message-class routing). |
| `event-attendee-email-sequences` | Owns the mailing list's copy, cadence, consent, hygiene. Decide only whether email is the right channel for a class of message.                                                    |
| `event-social-media`             | Owns public-broadcast platform choice and social copy. Say "this goes out publicly" if needed; never pick the platform or write the post.                                          |
| `event-marketing-plan`           | Owns acquisition-channel weight before attendees exist. This architecture starts once someone has registered.                                                                      |

Two more boundaries are written from one side only, so say so when relying on them:

- `event-attendee-experience` owns static wayfinding (printed signs). Dynamic on-site announcement (PA call, live schedule-change screen) belongs here.
- `event-community-building` owns the standing community between editions. The same chat space can be this edition's channel and next year's community, handed off at Menu 4's top rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability and effort, so the defaults cannot be picked for the user.

1. Which phase: pre-event, days on site, wind-down after, or all three?
2. Shape: one room/day, several rooms, several days, or an overnight hackathon? Remote, livestreamed, recorded, press-covered? Do attendees need to reach each other?
3. How many people write to attendees, and how many have never written for this event before?
4. Which channels already exist with attendees on them, and does anything signed force a channel (sponsor deliverable, venue system, umbrella platform)?
5. Does a register exist (`event-cultural-identity`)? If not, route there first and label anything here provisional - this skill executes a register, never sets one.
6. Is there a hard live-by date?
7. One-off edition, or compounding series with a next edition intended? (Turns Menu 4 outright; moves Menu 1's app rung too.)
8. Effort ceiling: organizer hours before the event, who can watch a channel during it, who is on duty the week after?
9. What can break in a way an attendee can't see for themselves (livestream, shuttle, single entrance, venue change, catering failure)?
10. What already exists that should re-rank these defaults - a community chat your audience is already in, last edition's member list, an in-house writer, an app already in use?

Every ranking below is a default, not a law. Re-rank all four menus against Q10's answers, and say which answer moved which rung.

## How many things happen at once, and how many people write about them

Every menu below reorders between two scales:

- **One room, one day, one writer.** A list, and nothing else.
- **Three rooms, two days, five volunteer writers.** A routing rule, before another channel.

State which of those two scales a recommendation assumes whenever it holds at one and not the other.

A vendor-run event more often arrives with a channel already forced on it by contract (Q4), which deletes a rung rather than reordering one. Beyond that, funding model reorders nothing: a message takes the same seconds to reach a phone whoever paid for the room.

## Workflow

1. Run the interview. Stop and route to `event-cultural-identity` if Q5 comes back empty.
2. List the **message classes** this edition will actually send, before choosing any channel: [references/message-class-matrix-and-message-bank.md](references/message-class-matrix-and-message-bank.md). A roster picked before the messages are known is picked by fashion.
3. Choose the channel roster (Menu 1). Give every channel one stated job and one named owner - an unstated job is the channel that goes quiet.
4. Choose the routing policy (Menu 2), written where the writers are, not a document they open once.
5. Choose the consistency process (Menu 3); at the message-bank rung or above, write the bank before the event.
6. Point at the channel directory: `event-marketing-plan` owns that page (its "comms hub" rung) as the acquisition-side artifact. Hand it the roster - every channel, its job, its boundary - to publish there rather than standing up a second page.
7. Check digital-space obligations: the code of conduct binds every channel; confirm with that sibling, never write the reporting path yourself.
8. Choose the wind-down (Menu 4) now, before the event, and publish its date on the channels themselves.
9. Present section by section - roster, routing, consistency, wind-down - approved before anyone creates a channel.

If your harness has persistent memory, record:

- The roster, with each channel's stated job and owner.
- The routing rule.
- Which message classes actually got sent and where.
- Every message that had to be repeated on a second channel because the first did not reach.
- The wind-down decision and its date.
- Any channel that went quiet.

The repeats and the quiet channels are next edition's roster changes.

## Menu 1 - Channel roster

An additive ladder: each rung adds a channel to the ones below it. Two value axes, because reach and speed are not the same thing, and no rung tops both.

- value, a routine message reaches everyone who registered: `announcement list > chat space == event app > status page`
- value, a change of plan reaches people fast enough to act on it during the event: `event app == chat space > status page > announcement list`
- effort (setup, plus the standing ops and moderation each one adds for the whole lifecycle): `event app > chat space > status page > announcement list`
- efficiency: `announcement list > chat space > status page > event app`

All four orderings are this skill's own construction, not measured rankings. The menu is clean by care, not by construction: it has genuinely mixed pairs, since chat beats the status page on both value axes but costs more, so neither dominates. See [references/menu-ranking-rationale.md](references/menu-ranking-rationale.md) for why the `==` ties hold.

The channel directory itself is not a rung here: `event-marketing-plan` owns that page (its "comms hub" rung). Extend that page rather than publishing a second one - see Workflow step 6.

- **Announcement list** (default/floor) - already exists from acquisition, reaches every registrant by construction, latency in hours. Move up as soon as a message would arrive too late by email - any message about today.
- **Chat space** - a persistent two-way space. Real cost is moderation for the whole lifecycle plus the code-of-conduct duty inside it: [references/channel-roster-and-platform-notes.md](references/channel-roster-and-platform-notes.md). Promote when Q2 says overnight, multi-day, remote, or attendees need to reach each other.
- **Status page** - one canonical page saying whether the broken thing is still broken. The pattern is adapted from software incident communication, with four things that do not transfer: [references/wind-down-and-status-page.md](references/wind-down-and-status-page.md). Nobody checks it unprompted; it works only with a push on another channel pointing at it. Promote when Q9 names something an attendee can't see for themselves.
- **Event app** (starved rung) - tops effort, ties chat on speed, loses to the list on reach - efficiency never picks it. No ROI figure exists for a community-run event. Promote when Q4 says a signed commitment forces one, Q2 says 3+ concurrent rooms with a grid changing more than once a day, or Q10 says you already own one with sunk content cost.
- **Delete, never demote:** a second chat platform running the same job in parallel - doubles moderation, halves each announcement's audience.
- **Conditional delete:** status page where Q9 comes back empty - a page reporting "everything is fine" trains people not to look.

## Menu 2 - Message-class routing

Which class of message goes on which channel.

Rungs:

- One channel for everything.
- A two-channel split (a broadcast channel nobody replies in, one open channel where people talk).
- Per-audience-segment channels.
- A full message-class matrix with escalation tiers.

Orderings:

- value, a message reaches the person who needs it without being buried: `matrix > per-segment > two-channel split > one channel`
- value, a volunteer writer routes a message correctly on the first try with nobody to ask: `one channel > two-channel split > matrix > per-segment`
- effort (channels to create and watch, plus the coordination to keep the rule current): `matrix > per-segment > two-channel split > one channel`
- efficiency: `two-channel split > matrix > one channel > per-segment`

A routing policy nobody can execute routes nothing. Writer-operability is therefore the pivot this menu turns on, and the efficiency line stands or falls with it: reject the axis and the ordering goes with it. That axis and all four orderings are this skill's own construction, not measured rankings.

One channel is unambiguous by construction. Per-segment channels are the worst of both: segment membership is a fresh judgement call on every message, and the writer resolves it by cross-posting, which rebuilds the noise the segments were meant to remove. See [references/menu-ranking-rationale.md](references/menu-ranking-rationale.md) for why the efficiency line rests on writer-operability rather than a dominance check.

- **Two-channel split** (default) - one channel the event posts on, one where attendees talk back. Answers the only routing question most events have, at the cost of one extra channel. Promote when Q3 says multiple writers and Q2 says multiple rooms or days.
- **Matrix with escalation tiers** (starved rung) - tops reach and effort, loses every efficiency round. One table: message class down the side, channel across the top, plus escalation tiers. Promote with the two conditions above, plus recorded/livestreamed editions where a missed message is missed permanently.
- **One channel for everything** - legitimate at a single-room single-day event with one writer. Ranks third, not last, on efficiency: top operability at no cost.
- **Per-audience-segment channels** - last on efficiency, real cost, the operability floor. Choose only when segments are genuinely disjoint and stable for the whole event.
- **Delete, never demote:** a direct message from an organizer as a routing tier - no record for the next shift, unescalatable, makes the sender the channel.
- **Conditional delete:** matrix and per-segment rungs where Q2 is one room/day and Q3 is one writer - no message class concerns part of that room only.

**One routing rule you inherit, and must not re-derive:** a public statement after an incident has exactly one authorized publisher, and nobody else posts about it on any channel. `samber/dev-event-organizer-skills@event-code-of-conduct` owns that rule outright; restating it here would give a team two copies to disagree with. Make every channel obey it instead: the matrix carries an incident-statement row whose publisher is that named authority, with no local exception for being faster.

## Menu 3 - Multi-writer consistency

How several writers execute one register without drifting. The register itself is fixed elsewhere. Nothing here originates one.

- value, consistency across the messages that actually go out during the event: `editorial sign-off > pre-written message bank > named owner per channel > shared quick-reference > ad hoc`
- value, a time-critical message goes out without waiting for a specific person: `pre-written message bank > ad hoc > shared quick-reference > named owner per channel > editorial sign-off`
- effort (hours before the event plus coordination during it): `editorial sign-off > named owner per channel > pre-written message bank > shared quick-reference > ad hoc`
- efficiency: `shared quick-reference > pre-written message bank > named owner per channel > ad hoc > editorial sign-off`

The first value axis is deliberately scoped to _the messages that actually go out during the event_, mostly the predictable classes. On that quantity a frozen template beats a human who drifts. Widening it to "every message ever written" would reverse the bank and owner rungs, so state which quantity you mean before reordering anything here.

All four orderings, the five rungs and every promotion condition are this skill's own construction, not measured rankings. See [references/menu-ranking-rationale.md](references/menu-ranking-rationale.md) for the dominance relation this scope protects.

- **Shared quick-reference** (default) - one page condensing the register into do/don't lines and worked examples. Near-zero effort since the thinking is done. Move up when Q3 says a writer has never written for this event before.
- **Pre-written message bank** - templates for classes you know are coming (delay, room change, venue change, lost property, last call, closing, cancellation). Freezes the register into exact messages sent under time pressure. For the nudges that repeat every edition on a predictable clock - a venue-closing warning, a meal-ready ping, a "starting in 3 minutes" call - go one step further than a template on standby: write the whole day's script against literal timestamps in advance. Nobody then has to remember to compose and send a message at a specific hour while also running the event.
- **Named owner per channel** - one person accountable per channel's output. Buys consistency the bank doesn't cover, at the cost of a slower message when the owner is away. `event-social-media` owns the public social account.
- **Ad hoc** - no shared reference. Fourth, not last, on efficiency: real speed for no effort, but a poor ratio - its one virtue is bought better by the message bank.
- **Editorial sign-off before publish** (starved rung) - tops consistency and effort, bottoms speed, which hurts most at a live event. Promote when the edition is recorded/livestreamed/press-covered, a sponsor contract fixes verbatim wording, or Q3 says most writers have never seen the register - even then, exempt time-critical classes to the bank.
- **Delete, never demote:** a channel-local register invented by whoever writes that channel. `event-cultural-identity` settles it: identity is fixed, only expression modulates.

## Menu 4 - Wind-down after the event

Q7's one-off/compounding answer decides this menu, so ask it before ranking.

Rungs:

- Leave everything open.
- Read-only archive.
- Export plus scheduled deletion after a stated retention window.
- Hand-off to a persistent community space.

Orderings:

- value, an attendee who returns next edition is still reachable: `hand-off > leave open > read-only archive > export + scheduled deletion`
- value, nothing the event no longer maintains is still speaking in the event's name: `export + scheduled deletion > read-only archive > hand-off > leave open`
- effort (hours at wind-down, coordination, and who has to keep watching afterwards): `hand-off > export + scheduled deletion > read-only archive > leave open`
- compliance cost (the review it triggers and what it costs to reverse): `export + scheduled deletion > leave open > hand-off > read-only archive`
- efficiency: `read-only archive > export + scheduled deletion > hand-off > leave open`

Reachability and non-liability oppose each other on five of the six pairs, so no pair dominates. The efficiency line rests on the ratio argued per rung below and on Q7, not on a dominance check. See [references/menu-ranking-rationale.md](references/menu-ranking-rationale.md) for the full argument.

The five orderings, the four rungs and the compliance-cost axis are this skill's own construction, not measured rankings. That does not make the compliance cost soft. Never compress it:

- **Export-plus-deletion** tops it: the only rung you cannot undo, and the only one that forces a lawful-basis and retention question _before_ you act.
- **Leave-open** sits second for the opposite reason: it triggers no review at all, which is the problem - the code-of-conduct duty on that space stays live with nobody assigned to it.
- **Hand-off** carries a consent question, because moving people into a new space is a new purpose.
- **Read-only archive** is lowest: content stays where it was posted under terms already accepted, and nothing new accrues.

Name no jurisdiction, quote no retention period, and route the actual retention decision to the organizer's own counsel: it turns on jurisdiction, platform terms and year.

Per rung:

- **Read-only archive** - the default: freeze posting, keep content visible, post a notice saying the space is closed and where to go instead. Cheapest rung that ends the standing duty without destroying anything.
- **Export + scheduled deletion** - the default _promotion_ when Q7 says one-off: take the export, publish the deletion date on the channel ahead of it, then delete. A one-off's member list is a liability with no next edition to spend it on.
- **Hand-off to a persistent community space** - the starved rung: tops reachability, tops effort. Promotion condition, both halves required: Q7 says compounding **and** a standing space already exists or a named person has committed to running it. Handing off into a space nobody owns is leave-open with extra steps. Coordinate with `samber/dev-event-organizer-skills@event-community-building`, which owns the receiving side and hands the live member list back when the next edition's build-up opens.
- **Leave everything open** - last on efficiency: near-zero cost at wind-down, and the only rung whose ongoing duty never ends.
- **Delete, do not demote - a silent wind-down.** Closing or emptying a channel without telling the people on it. It destroys the belief that an announcement posted there is real, and next edition's channel starts below zero.
- **Conditional delete - leave everything open, where Q8 says nobody is on duty after the closing date.** An unmoderated space in the event's name is a code-of-conduct obligation with no responder, and the digital-harassment warning applies to it exactly as it did during the event.

## Failure modes

- **A channel with no stated job.** Created because a similar event has one, goes quiet by week two, then carries the one message that mattered. Every channel names its job and owner, or it does not get created.
- **Opening a channel nobody is staffed to write to.** Channel _staffing_, not channel _existence_, is what reaches people - see [references/channel-roster-and-platform-notes.md](references/channel-roster-and-platform-notes.md) for the published hybrid-event failure this comes from.
- **Routing by who is loudest.** Whoever is holding a phone posts wherever they already are. The routing rule lives where the writers are, or it does not exist.
- **Treating the chat space as free.** Setup is an hour. Moderation is a standing job for the whole lifecycle, with a code-of-conduct duty identical to the one in the room.
- **Announcing a disruption only where people already are.** The people who need a venue-change message are not yet in the building and not watching chat. Disruption classes escalate to the channel that pushes, not the one that is convenient.
- **Deciding the wind-down after the event.** By then the people who would have run it have gone home, and leave-open happens by accident rather than by choice.
- **Re-inventing a voice per channel.** Covered by Menu 3's delete rule. It shows up as an event that sounds like four different events.

## Measurement

Every threshold below is self-set, not a measured benchmark. Fix each one before the event, never after the data arrives.

- **Repeat rate** (self-set): the share of messages that had to be re-sent on a second channel because the first did not reach. Every repeat is a routing rule that was wrong or a channel that was unstaffed. Pick a ceiling in advance.
- **Unrouted questions** (self-set): questions that arrived somewhere with no owner - a personal DM, a social reply, a speaker's inbox. Count them and note where they landed. That is your missing channel or your missing directory line.
- **Channel silence** (self-set): any channel with no organizer post for a period fixed in advance. A silent channel is a deletion candidate for next edition, not a moderation problem.
- **Wind-down completion** (binary): every channel opened has a closed state and a date, on the day the wind-down was scheduled. This is the only gate here that passes or fails cleanly.
- Attendee satisfaction and return rate read on the whole event, not on the channels. They belong to `samber/dev-event-organizer-skills@event-feedback` and `samber/dev-event-organizer-skills@event-market-fit`.

## Invocation examples

- "We have 400 registered attendees and a two-track day. Do we need a group chat space, or is email enough?"
- "Three of us will be posting updates during the event and we keep sounding like different people. How do we fix that without a sign-off bottleneck?"
- "Our venue changed two weeks out and half the room did not find out. Where should that have gone?"
- "The conference ended a month ago and the chat is still open with nobody watching it. What do we do with it?"

Expected output: a channel architecture with:

1. The roster, each channel with a stated job, an owner and its opening date.
2. The message-class list and the routing rule at the chosen depth.
3. The escalation tiers where the matrix rung was taken.
4. The consistency process and, at the bank rung or above, the written templates.
5. The roster handed to `event-marketing-plan`'s channel directory rather than a second, competing page.
6. The digital-space code-of-conduct check with its route to the CoC sibling.
7. The wind-down decision per channel with its date, chosen before the event.

Every self-set element labelled as such. Presented section by section for approval.

## References

- [references/channel-roster-and-platform-notes.md](references/channel-roster-and-platform-notes.md) - the published channel roster, its per-channel jobs, what does not transfer from a hackathon to a conference, the digital-space code-of-conduct rule, and platform-category notes.
- [references/message-class-matrix-and-message-bank.md](references/message-class-matrix-and-message-bank.md) - the message-class taxonomy, a worked routing matrix with escalation tiers, a negative example, and eight message-bank templates.
- [references/wind-down-and-status-page.md](references/wind-down-and-status-page.md) - the four per-rung wind-down checklists, the review list to hand to counsel, and the status-page pattern with what does not transfer.

Sibling skills referenced throughout: see § Siblings own part of this, plus `samber/dev-event-organizer-skills@event-cultural-identity` (sets the register every channel expresses; run it first).
