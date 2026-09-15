---
name: event-content-repurposing
description: Turn one edition's already-captured material into derivative published artifacts after the event - which formats get made, on what cadence, under which licence, and what speakers are asked to amplify. Covers publishing latency (dump, batched, drip, evergreen), the rights gate on third-party slide material and attendee photos, and the inventory handed up to the next edition's campaign. Use whenever asked what to do with talk recordings after a conference, how to turn an event into clips, write-ups or transcripts, when to release them, or whether footage can be republished at all. Do NOT use for capturing or editing the master recording - use samber/dev-event-organizer-skills@event-production - or the event's own channels - use samber/dev-event-organizer-skills@event-social-media.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Content Repurposing

You decide what happens to an edition's captured output once a master file already exists.

- **Inputs, every one of them somebody else's output:** a published recording, slides, a transcript, a photo archive, hallway notes.
- **Decisions you own:** which derivative artifacts get made, in what order, on what cadence, under which licence, and what each speaker is asked to do about the piece cut from their own talk.
- **Outputs you produce:** published derivative artifacts, plus a content inventory the next edition's campaign can schedule.

## Where you start, and the six lines you never cross

| Sibling                        | Owns                                                 | The line                                                                                                                    |
| ------------------------------ | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `event-production`             | Master recording, capture through published file     | Take the master as handed over; never re-edit, re-publish, or send a speaker their own link. You begin at the _derivative_. |
| `event-social-media`           | The event's own channels                             | You decide which derivative exists and when it drops; that skill owns platform, hashtag, copy, and posting.                 |
| `event-speaker-experience`     | The consent record, post-event follow-up             | Enforce the consent record; never collect or re-ask it. You decide only whether the speaker amplifies the derivative.       |
| `event-marketing-plan`         | The attendee-acquisition plan and its funnel targets | Repurposed content is inventory you hand up, never a target you set.                                                        |
| `tech-podcast-youtube-channel` | Any standing owned-media property                    | A one-off derivative is yours; a format outliving any single edition is a property and belongs there.                       |
| `event-debrief`                | The organizers' public recap                         | That skill covers how the edition went; yours covers what was _said_ in the sessions. Write one of each.                    |

Which siblings state the same boundary back, and which do not: [references/decision-rationale.md](references/decision-rationale.md).

Every rung, axis ordering, efficiency line, default and promotion condition in the four menus below is this skill's own construction, not a measured benchmark. Each is a default, not a law: it shifts with context and with who executes it. Re-rank all four menus against what you already know:

- A volunteer who edits video for a living.
- An existing subtitling community.
- An audience that finds the event through search.
- A speaker with a large following of their own.
- A consent record that stops at "recording and publication".

Each of these overturns a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability, and effort; those defaults cannot be picked for the user.

1. What exists to work from and in what state (published master, raw files, slides, transcript, photo archive)? Who handed it over, anything still owed?
2. Where is the consent record, what does it cover per session format, does it reach derivative works or stop at recording and publication?
3. What photo opt-out did badges carry, retrievable per photo or only for the room as a whole?
4. One-off edition, or one year of a recurring event? A compounding mandate promotes every rung whose payoff lands after this edition ends.
5. Any date anything must land by (campaign moment, sponsor report, partner calendar)? A hard date promotes rungs shipping in one push.
6. Who owns publishing after the event, how many hours a week, until what date? Decides Menu 1 more than any other answer.
7. Which sessions did people actually ask about - in the room, in feedback, in chat?
8. Does the event already run a standing owned-media property with its own audience?
9. Is search a real route into this event for people who've never heard of it?
10. Has a licence been decided, and by whom? If nobody has, you are deciding it - say so.
11. Is the audience multilingual, and did the accessibility work commit to anything that implies text derivatives?
12. Which speakers, if any, have an audience of their own larger than the event's?
13. Is this the event's first edition, and does the program include a keynote session?

## What actually splits this work

One axis reorders every menu below: **whether anyone owns publishing after the crew disperses**. An owner with a standing weekly slot and an owner with one free afternoon are running two different plans. Every menu below assumes you have asked which one you have.

`samber/dev-event-organizer-skills@event-production` names the same risk in its own failure list: a pipeline with no owner after the event, where files are collected, the crew disperses, and the videos are published very late or never.

Community-run against vendor-run moves only _who edits_, a volunteer with a laptop or a contracted editor, and nothing else on these menus.

## Workflow

1. **Take delivery rather than re-doing it.** Confirm what `event-production` published and what state the files are in. If the master isn't published yet, stop and wait.
2. **Read the consent record and mark each session usable, restricted, or off-limits** before choosing any format: [references/rights-and-licence-gate.md](references/rights-and-licence-gate.md).
3. **Pick the derivative mix** (Menu 2), driven by Q7's answer, not the running order: [references/derivative-catalog-and-release-plan.md](references/derivative-catalog-and-release-plan.md).
4. **Pick the publishing latency** (Menu 1), pinned to real dates - Q5's deadline and Q6's owner decide this.
5. **Run the rights gate** (Menu 4) on each planned artifact before production, not before publication.
6. **Decide and state the licence.** Write it on the artifact, not in a spreadsheet.
7. **Build the speaker ask** (Menu 3), reusing the shareable kit `event-social-media` already owns.
8. **Hand each scheduled piece to the channel that publishes it**, with date and licence line, and stop.
9. **Hand the inventory list up to `event-marketing-plan`** - what exists, from what date, in what format.
10. **Record what shipped against what was planned**, and where it stalled - the only reliable read on whether the plan was sized correctly.

Present the plan for validation, section by section, before any editing starts:

1. The usable-session list.
2. The format mix.
3. The release dates.
4. The rights findings.
5. The licence and the speaker ask.

Everything is cheap to change up to the moment somebody opens an editor.

If your harness has persistent memory, record per edition:

- Which sessions the consent record covered and which it did not.
- What was made from each.
- What shipped on its planned date and what slipped.
- Which speakers amplified.
- The licence chosen, and who decided it.

The next edition's plan starts from a real record rather than from these defaults.

## Menu 1 - Publishing latency

When the derivatives drop. This is the menu where the axes genuinely disagree, so it carries two value axes rather than one blended rank.

- effort (production against a repeating date, coordination, a standing owner, how long the job stays open): `drip > evergreen re-surfacing > batched release > all-at-once dump`
- value - sustained presence across the gap to the next edition, which is what `samber/dev-event-organizer-skills@event-marketing-plan` can schedule against: `drip > evergreen re-surfacing > batched release > all-at-once dump`
- value - completion, meaning every artifact you planned actually ships: `all-at-once dump > batched release > drip > evergreen re-surfacing`
- efficiency: `batched release > all-at-once dump > evergreen re-surfacing > drip`

**Read the completion axis before the efficiency line.** Most plans omit it, and latency ranked on reach alone picks the rung most likely to die halfway. Three reasons it is not a hedge:

- Post-event energy decays, so the failure named above is not a badly timed release but one that never happens.
- A dump has already finished by the time a drip is on its second piece.
- A drip's later half is exactly what an exhausted volunteer team drops.

**Dominance audit:** vacuous - no strict dominance among the 4 rungs, so the efficiency line rests on the argument above, not on the audit. Full audit: [references/decision-rationale.md](references/decision-rationale.md).

- **All-at-once dump** - everything drops in one push soon after the event. One decision, one afternoon; reaches only people already paying attention.
- **Batched release** - split into a few waves, write-up first. Costs only scheduling on top of a dump; later waves reach people who missed the first.
- **Drip** - one piece per fixed interval over weeks. Needs a piece ready on a date, repeatedly, and an owner until a stated end date.
- **Evergreen re-surfacing** - re-posting an existing artifact months later against a newly relevant moment. No new production, but the watch has no end date and almost nobody keeps it.

- **Default rung:** batched release.
- **Promotion condition:** move to a drip when Q4 says the edition recurs _and_ Q6 names an owner with a standing slot through to a stated end date - both, not either.
- **Demotion condition:** fall back to the dump when Q6 returns no owner past the week after the event, or when Q5's deadline lands before a drip could finish.

**The starved options are the drip and, behind it, evergreen re-surfacing** - both top the sustained-presence axis and both cost real standing attention, so efficiency never picks either.

- Promote the drip for the compounding mandate above.
- Promote evergreen re-surfacing on its own separate condition: a talk whose subject becomes newly relevant, where the marginal cost is one scheduled post against an artifact that already exists.

**Delete, do not demote: publishing with no dated plan at all** - "we will get to it". Delete it from this menu and from the axis lines above.

It reads as the cheapest rung and it is not a rung. It is the failure named above, where the crew disperses and the files are never published. A dump with a date is the floor.

## Menu 2 - Which derivative to make

Five artifacts, chosen individually rather than as a bundle, because a team rarely has capacity for all of them and the question is which one first.

- effort (production hours, editing craft, repetition per talk, review): `transcript-derived text page > short clips > audio cut > written write-up > social thread`
- value - new reach, meaning people who did not attend and were not already following: `short clips > written write-up > transcript-derived text page > audio cut == social thread`
- value - durability, meaning how long it keeps returning value and whether it survives as inventory for the next edition: `transcript-derived text page > written write-up > short clips > audio cut > social thread`
- efficiency: `written write-up > short clips > social thread > transcript-derived text page > audio cut`

The `==` on new reach is argued rather than a dodge: neither an audio cut nor a thread travels on its own - each reaches only the fraction of an audience the event already has who passes it on. They differ in shelf life, which is why the durability axis separates them and this one does not.

**Dominance audit:** one strict relation among the 5 rungs - the written write-up dominates the audio cut on both value axes and effort, and ranks above it. The other nine pairs are trades. Full audit: [references/decision-rationale.md](references/decision-rationale.md).

- **Written write-up** - one piece covering what the sessions actually said, audience-facing rather than organizer-facing. Reusable as the link that answers "what is this event", which is why it leads on efficiency despite leading on neither value axis outright.
- **Short clips** - a cut from the master carrying one moment worth watching without deciding to. Tops new reach because a clip travels through other people's feeds. Finding the moment is the work, not the cut.
- **Social thread from the archive** - photos, quotes and links assembled from what already exists. Near-zero effort, near-zero durability, reaches only people who were already there.
- **Transcript-derived text page** - the talk as searchable, quotable, translatable text. Tops durability because search keeps finding it long after a feed has moved on. Tops effort too: a correction pass per talk across a programme is a standing job.
- **Audio cut** - the talk as audio. Dominated by the write-up and last on efficiency: a one-off audio file with no property behind it has nowhere to land. Stops being dominated once Q8 says a standing audio property already exists - building one is `samber/dev-event-organizer-skills@tech-podcast-youtube-channel`'s job.

- **Default rung:** the written write-up, plus short clips for the sessions Q7 named.
- **Promotion condition:** add the transcript-derived page when Q4 says the edition recurs _and_ Q9 says search is a real route in - one without the other does not repay a per-talk correction pass. Add the audio cut only on Q8's yes.

**The starved option is the transcript-derived text page** - tops durability, tops effort, so efficiency never picks it.

- **Promotion conditions, keyed to Q11**: a multilingual audience, where text is the only derivative that translates at all; or an accessibility commitment made upstream that already implies it.

**Delete, do not demote: re-uploading the full session as a "derivative".** Delete it from this menu and from the axis lines above. Re-posting the whole talk to a second destination is not a derivative; it is the master again, and `samber/dev-event-organizer-skills@event-production` owns that file and its publication. A second copy under different terms is how a consent record quietly stops matching what is published.

## Menu 3 - The speaker amplification ask

Scoped narrowly on purpose:

- **Already owned elsewhere.** `samber/dev-event-organizer-skills@event-social-media` runs its own amplification-ask menu, covering speakers, sponsors and partners for the campaign _before_ the event, and it owns the shareable kit.
- **Covered here.** Only the post-event ask about the derivative made from that speaker's own talk.
- **Reuse, never rebuild.** Take that kit as it stands and never restate its contents here. The double ownership is on the mechanism, not on the moment.

- effort (production per speaker, other people's calendars, coordination): `dated joint push > ready-made post-event asset > one-line ask on the existing follow-up > no ask`
- value - the speaker actually posts: `ready-made post-event asset > dated joint push > one-line ask on the existing follow-up > no ask`
- value - reach when they do: `dated joint push > ready-made post-event asset > one-line ask on the existing follow-up > no ask`
- efficiency: `one-line ask on the existing follow-up > ready-made post-event asset > dated joint push > no ask`

The first value axis rests on one assumption, stated plainly so you can reject it: what decides whether a speaker amplifies is their own effort, not their willingness. If your record of past editions contradicts it, re-rank.

**Dominance audit:** vacuous - value rises monotonically with effort across the 4 rungs, with one exception (the ready-made asset beats the dated joint push on cost and take-up, blocked only on reach). Full audit: [references/decision-rationale.md](references/decision-rationale.md).

- **No ask** - publish, say nothing beyond what `samber/dev-event-organizer-skills@event-speaker-experience` already sends. Last on efficiency, but the right answer when the consent record does not cover a speaker-facing derivative.
- **One-line ask on the existing follow-up** - one sentence riding on the message that sibling is already sending. Coordinate the wording rather than sending your own message.
- **Ready-made post-event asset** - the clip plus a drafted caption and link, handed over so the speaker's own effort is near zero. Only the asset is new; the kit's shape is the sibling's.
- **Dated joint push** - event and speaker post the same day, cross-tagged. Concentrates both audiences on one moment, and needs someone else's calendar.

- **Default rung:** the one-line ask.
- **Promotion condition:** move to the ready-made asset for the speakers Q7 named - the sessions people asked about are where amplification returns most - and to the dated joint push only when Q12 names a speaker with an audience larger than the event's and that speaker has already agreed to a date.

**The starved option is the dated joint push** - tops reach, tops effort, so efficiency never picks it.

- **Promotion conditions, keyed to Q13**: a keynote session; or a first edition whose own audience is too small for anything else to matter.

**Delete, do not demote: asking a speaker to amplify a derivative they have not seen.** Delete it from this menu and from the axis lines above. It is not the cheap version of an ask; it hands a speaker a public commitment to a cut they have never watched, and the one thing you cannot undo is their name on it.

## Menu 4 - Rights and consent review depth

**Ranked by compliance cost only**, never by value or effort and never in money: these rungs are descriptions of how much unreviewed surface a given artifact republishes, not competing ways to buy the same outcome. A blended ratio here would read as a recommendation to take the cheap one, exactly the wrong reading.

- compliance cost (the review it triggers, and what stops being reversible): `a derivative containing identifiable attendees > a derivative carrying third-party material > a cleared-only derivative`

- **Cleared-only derivative** - built solely from material the consent record already covers, with no third-party content and no identifiable attendee. One check, already done upstream.
- **A derivative carrying third-party material** - someone else's logo or chart on a slide, music under a demo, another company's interface on screen. Triggers a clearance question nobody in this collection owns (see below); reversible - a complaint or platform action removes the file, and the piece can be re-cut without those frames.
- **A derivative containing identifiable attendees** - a room shot, a hallway photo, a face in the background of a clip. Tops this axis because permission cannot be reconstructed afterwards: the badge opt-out is a signal collected in a moment that has passed. Check it before production, not before publication.

Enforce, never define. Speaker consent is `samber/dev-event-organizer-skills@event-speaker-experience`'s; do not infer it from the absence of an objection. Attendee photos run through the badge-based opt-out mechanism owned by `samber/dev-event-organizer-skills@event-accessibility-inclusion`; read that signal, do not invent a second one.

Two gaps this skill names rather than closes:

- **Third-party material in slides.** Nobody owns clearance for it. This skill runs a minimal checklist gate before a clip is cut, and that checklist is its own construction, not a clearance procedure.
- **Derivative-works scope in the release itself.** Most releases stop at publication and say nothing about a later re-cut. Route that gap to `samber/dev-event-organizer-skills@event-speaker-experience` rather than reading a permission into silence.

Checklist, quotes, wording and the escalation path: [references/rights-and-licence-gate.md](references/rights-and-licence-gate.md).

## The licence decision

No sibling claims the licence, and developer conferences follow no shared convention. The call is yours by default, so make it explicitly rather than by drifting.

This section bounds the choice instead of naming a licence, because there is no convention to name. Decide three things, and record who decided:

- Whether published derivatives carry an open licence at all.
- Which licence.
- Whether it differs between a recording, a transcript and a photo.

One large-conference precedent sits outside the domain: TED licenses its talks under Creative Commons BY-NC-ND 4.0 (attribution required, no commercial use, no derivative works). TED is not a developer conference, so treat its choice as one event's own, never as a convention to match.

Write the licence line onto each artifact where a re-user will actually see it.

Two constraints bound the choice. Both are this skill's own reading of the rights position, not legal advice, and neither is optional:

- **You cannot grant more than the consent record gave you.** An open licence over a talk whose release covers publication only is a grant you never held.
- **A licence attached to a derivative containing third-party material licenses somebody else's work along with yours.**

Where either bites, publish without an open licence and say so.

## Failure modes

- **Re-publishing the master under a new name.** A full-session re-upload is `samber/dev-event-organizer-skills@event-production`'s file, not a derivative. It splits the archive, and the second copy is the one whose terms nobody checks.
- **Sending the speaker their video link.** Two siblings already claim it: `event-production` in its post-event pipeline, and `event-speaker-experience` in its post-event follow-up. Your message is about the derivative and nothing else.
- **Inferring derivative rights from a publication grant.** A release covering "recording and publication" did not license a re-cut. Route the gap upstream; do not close it by assumption.
- **Using an attendee photo because nobody objected.** The opt-out was a signal given at the badge table and it does not renew. Silence at publishing time is not permission.
- **Attributing a photo norm to the code of conduct.** Its text names harassing photography only. Reading a consent mechanism into it invents a policy the event never adopted.
- **Planning a drip nobody owns.** The rung needs a person and an end date. Without both it is a dump that ships half of itself.
- **Quoting a turnaround as an industry norm.** A release grants a permission, not a publication date. Publish your own date as your own promise.
- **Writing a recap that competes with the debrief's.** Two documents about the same edition, one about the sessions and one about the organizing, are fine. One document trying to be both serves neither reader.
- **Setting a view target.** A number nobody measured becomes the thing the plan is judged on.

## Measurement

This skill sets **no numeric threshold** on views, retention or engagement for conference-talk derivatives, and refuses to invent one. A target imported from a video platform's marketing material would read as domain evidence and be defended as such.

Two completeness gates carry the weight instead. Both are self-set, and both are checkable without a threshold to argue about:

- **Every published derivative traces to a session the consent record covers**, and every session outside it is marked unusable rather than left ambiguous.
- **Every planned artifact has a date and an owner**, and both existed before production started.

Beyond those, everything is self-set. Pick two, write down before publishing what each would change next edition:

- **Shipped against planned, by date** (self-set): the single most honest read on whether the latency rung was sized for the team you actually have.
- **Where the pipeline stalled** (self-set): at editing, at the rights check, at scheduling, or at the channel. The category recurs; the individual delay does not.
- **Amplification take-up** (self-set): speakers who posted, over speakers asked. A low rate diagnoses the ask, not the speakers - usually an ask that arrived without the asset attached.
- **Inventory available to the next campaign** (self-set): what `samber/dev-event-organizer-skills@event-marketing-plan` could actually schedule when it asked. An edition that produced nothing repurposable has nothing to promote the next one with.

## Invocation examples

- "The videos are up. What do we make from them, and in what order?"
- "Should we drop everything at once or release one talk a week?"
- "A clip we want to cut has a Spotify player visible in the demo. Can we publish it?"
- "What do we ask speakers to do once their clip is live?"
- "Do we put a Creative Commons licence on our talk recordings, and which one?"

Expected output: the usable-session list with each session marked against the consent record, the derivative mix with the reason each format was chosen, a dated release plan with its owner, the rights findings per planned artifact, the licence decision with who made it, the speaker ask with its asset, and the inventory list handed up to the marketing plan.

## References

- [references/derivative-catalog-and-release-plan.md](references/derivative-catalog-and-release-plan.md) - each derivative format with what it is made from and what it actually costs, a worked release plan with its negative counterpart, the handover list to the channel sibling, and the inventory format handed up to the marketing plan.
- [references/rights-and-licence-gate.md](references/rights-and-licence-gate.md) - the per-session consent check, the derivative-works question and where to route it, the third-party-material checklist as a claimed gap, the attendee-photo check, and the licence decision with its two binding constraints.
