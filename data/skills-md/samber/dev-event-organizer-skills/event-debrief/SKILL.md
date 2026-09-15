---
name: event-debrief
description: Run the organizing team's own internal retrospective on one finished edition of a technical event - the blameless frame, the reconstructed timeline, what went well split from what went poorly, what fired reconciled against the risk register, budget plan and run of show, team-health findings, and dated lessons-learned entries each carrying an owner and a due date. Use whenever asked to run a post-event debrief, a post-mortem or a retrospective after a conference, meetup or hackathon, review an edition against the goals the team set, build a lessons-learned log, or publish a public recap. Do NOT use to collect participant feedback - use samber/dev-event-organizer-skills@event-feedback - or for trends across editions - use samber/dev-event-organizer-skills@event-continuous-improvement.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Debrief

You run the organizing team's retrospective on one finished edition: the meeting, the reconstruction, the findings, and the log that reaches next edition's plan. Internal-facing only - nothing here reaches an attendee, a speaker or a sponsor.

**Run it every edition, unconditionally.** The SRE incident-postmortem lineage this skill borrows from gates a postmortem on a severity threshold (SEV1/SEV2, an outage over fifteen minutes); that gate does not transfer. A quiet edition where nothing broke still gets a debrief - the goal is improving a recurring asset, not containing an incident. "It went fine, let's skip it" is the failure this rule exists to prevent.

Five things arrive already decided. Read them, reconcile against them, never reopen them:

| Sibling                 | Owns                                          | You do                                                                                    |
| ----------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `event-feedback`        | Collecting from attendees, speakers, sponsors | Consume its summary, never survey or write to participants                                |
| `event-risk-management` | Taxonomy, scoring, treatments                 | Check what fired against it, hand back a reconciliation                                   |
| `event-budget`          | P&L, next edition's numbers                   | Compare actual vs. planned, hand back the variance                                        |
| `event-run-of-show`     | Day-of execution                              | Log what broke as raw input, never re-diagnose                                            |
| `event-market-fit`      | Whether the concept still meets demand        | Surface whether this edition hit the goals _this team_ set, as a signal, never a go/no-go |

Upstream boundary: **trends across editions are not yours.** You produce one edition's dated log; `event-continuous-improvement` aggregates editions - comparing this one to the last two duplicates its whole reason to exist.

## What the field actually publishes about this

Published organizer guides give this a line or two at most. The mechanics that follow instead - when to hold the debrief, who attends, how the log reaches the next plan - come from the SRE incident-postmortem lineage, adapted to an asset that runs once a year rather than a service that breaks on a weekday. See [references/field-precedent.md](references/field-precedent.md) for the sourced detail.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6 to 8 exist because the menus below diverge sharply on time-to-effect, durability and effort; the default ordering cannot be picked for the user without them.

1. Which edition just ended, when did doors close, how many days ago? Decides debrief vs. archaeology.
2. What goals did the team set _before_ the event, in its own words? If unwritten, say so - the review becomes reconstructed, not measured.
3. Who held a named role, and who can be in the room? A debrief missing the volunteer lead misses the half of the day only they saw.
4. Which of the four inputs already exist: feedback summary, risk register, planned budget, run of show? Each missing one is a reconciliation you can't run.
5. Volunteer-run or staffed? Changes who can safely say what and who can be given an action item.
6. When does next edition's planning actually start? That date is this skill's deadline.
7. One-off, final, or recurring for years? A closing and a compounding edition want opposite things from the same menus.
8. Effort ceiling: hours left, and what state the team is in - honestly. An exhausted team is the first finding, not a scheduling problem to route around.
9. Is leadership handing over after this edition, and does the event run as one unit or as several cities under a shared brand?
10. How many code-of-conduct reports did this edition receive, how many were resolved, and were any visible enough that the community already knows?
11. Is this event public, or private/NDA-bound?
12. Does the team already run a year-round tracker for something else?

## Who is in the room and what they are paid

The axis that changes this skill's output is who is in the room and what they are paid - it decides what can be said and who can be handed a task. **Volunteer-run**: no employment relationship buffers the conversation, so candor is cheaper, but no manager absorbs an action item, and a criticised volunteer simply stops volunteering - a loss invisible in the log. **Staffed**: carry-through is structurally better since action items land on someone whose job includes them, but the debrief drifts toward performance review unless the blameless frame is stated and enforced explicitly. **Mixed** (the common case): state the frame most explicitly here - a volunteer and their day-job manager in the same room changes what the volunteer will say about workload.

## Workflow

1. Run the interview. Pick the depth rung before booking anything.
2. **Set the date immediately, hold it soon.** No standard interval exists; propose one and calendar it before the team disperses.
3. **Open with the blameless frame, out loud, in the room** - the question is _what conditions allowed this_, never _who caused this_. Findings describe gaps and systems, never people.
4. **Reconstruct the timeline before any analysis.** Walk the edition chronologically. Reconstruction first, judgment second - a room jumping to opinions relitigates the loudest memory instead of the actual sequence.
5. **Separate well from poorly as two explicit passes.** Run "well" first - a practice that worked and goes unnamed is one quietly dropped next edition.
6. **Reconcile against what exists**: risk register, planned budget, run of show, Q2's goals. Four checks, four outputs, each to its owning sibling. Checklists: [references/reconciliation-and-session-agenda.md](references/reconciliation-and-session-agenda.md).
7. **Surface team-health findings and route them without solving them.** Exhaustion, a role only one person could do, an unsized workload - structural findings for `event-team-structure`, not yours to fix.
8. **Write each finding as a three-part entry**: what happened, what was done in the moment, what changes next edition - deliberately shallow. Format and escalation criteria: [references/lessons-learned-entries.md](references/lessons-learned-entries.md).
9. **Give every open entry an owner and a due date, or close it explicitly.** No orphans - an entry with no owner is a wish, not a lesson. If no action is needed, write "no action, because" rather than manufacturing one.
10. **Decide the publication posture** as a team, in the room, while findings are fresh.
11. **Hand the log to `event-continuous-improvement`** as one dated document, each reconciliation to its owning sibling, and stop.

If your harness has persistent memory, record:

- the dated log itself
- the goals this edition was measured against
- every action item with its owner and due date
- which findings were routed to which sibling

Next edition's debrief then opens with last edition's open items instead of a blank page - and that carry-over list is the single input `samber/dev-event-organizer-skills@event-continuous-improvement` cannot reconstruct later.

Every ranking below is a default, not a law; it shifts with context and with who executes it. Where a constraint deletes a rung, strike it from that menu's axis lines too - a rung surviving in the ordering survives in the reader's head and comes back as scope. Re-rank all three menus against what you already know about this team:

- A team whose members run sprint retrospectives at work buys the deeper depth rungs far more cheaply than the effort axis assumes.
- An event with a published-recap tradition already sits at the publication menu's default.
- A team that already keeps a shared tracker running year-round makes the tracking menu's starved option nearly free, because it is an existing habit rather than a new standing job.
- A team where one person holds three roles has already produced the finding that the depth menu is trying to buy.

## Debrief depth

Ranked menu - findings that actually change next edition, bought per unit of the team's remaining energy. All three orderings are judgment rather than a published standard: organizer guides prescribe no debrief format.

- effort (hours, calendar coordination, facilitation): `multi-track written review > per-track sessions > written pre-read plus one session > one session`
- value (findings surfaced that would otherwise be lost): `multi-track written review > per-track sessions > written pre-read plus one session > one session`
- efficiency: `written pre-read plus one session > one session > per-track sessions > multi-track written review`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all six pairs: whichever rung surfaces more costs strictly more team-hours. No third axis blocks or rescues a pair; the efficiency line rests on the argument that follows.

Efficiency inverts the middle of the list because the two rungs on top of value are also the two on top of effort. Hours are the binding constraint right after an event, and per-track coordination scales worse than the detail it buys.

- **One session** - a single 60-90 minute meeting, notes captured live into a dated log.
- **Written pre-read plus one session** (default) - every named role submits a well/poorly list beforehand; the session discusses rather than collects. Buys the quiet organizer's findings and stops the first speaker anchoring the room.
- **Per-track sessions** - separate debriefs per workstream, then one consolidation session. Promote when named workstream leads worked genuinely independently - no single room holds everyone who knows what happened.
- **Multi-track written review** (starved rung) - per-track sessions plus a written document per track, consolidated into a full edition report. Tops value and effort, so efficiency never picks it. **Promotion condition, keyed to Q9**: a leadership handover (incoming team inherits a written record) or a franchise/multi-city event whose sibling organizers read each other's reviews.

When the "team" is one or two people, **delete both track-based rungs** rather than demoting them - five track sessions for two people is ceremony.

## The retro table

A single meeting produces minutes; a **standing table kept open across the cycle** produces something a meeting cannot - room for dissent to survive past the moment it was raised. Structure it with five columns - _Who / Observation / Agrees / Disagrees / Comments_ - and let anyone add a row at any time, not only during the scheduled session. Agreement and disagreement are columns, not a comment thread that quietly closes; a row stays open until the team is actually ready to close it, never just until the meeting ends.

Preserve some findings as raw testimony rather than folding every voice into one summary line. Two people describing the same practice in contradictory terms - one calling it too rare, another too frequent - is real signal a synthesized average would erase into "seems fine." Where a topic drew genuinely split reactions, keep both quotes on the table instead of picking the louder one.

**A documented refusal is itself the artifact, not a failure to act.** Writing "no action, because [reason]" directly onto the row is what stops an identical suggestion resurfacing next edition as if it had never been considered - the same no-action discipline step 9 already asks for action items, applied here to the table itself. Do the same for a call that genuinely split the team: record both positions on the row rather than letting one side win by attrition, so the debate stays available to whoever revisits it.

## Publication posture

Ranked menu - community trust and accountability bought per unit of drafting, review and exposure. This is the one menu here carrying real exposure, so it gets a compliance-cost axis.

- effort (drafting, anonymisation, sign-off): `recap plus retrospective plus transparency report > recap plus retrospective > recap only > nothing published`
- value (trust, accountability pressure that makes the fix happen, and a reusable public artifact): `recap plus retrospective plus transparency report > recap plus retrospective > recap only > nothing published`
- efficiency: `recap plus retrospective > recap only > recap plus retrospective plus transparency report > nothing published`
- compliance cost (review triggered, reversibility spent): `recap plus retrospective plus transparency report > recap plus retrospective > recap only`; publishing nothing carries none.

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** Value, effort and compliance cost all run in one order: the rung that buys more trust is strictly worse on both cost axes, including against "nothing published," which loses on value rather than winning anything for free. The check catches nothing; what follows is argument.

Efficiency still favors the retrospective: its findings already exist in three-part form by step 8, so the marginal cost is two paragraphs, not new analysis. Publishing nothing ranks last on efficiency despite costing nothing, because zero over zero never wins a ratio, even where it is the correct choice for other reasons.

The compliance ordering is not a rewrite of the effort ordering:

- **Recap** - exposure is a photo-consent check.
- **Retrospective** - exposure is contractual: a finding naming a venue or a caterer can collide with a non-disparagement clause and will certainly reach a supplier you want next year.
- **Transparency report** - exposure is categorically different again: it needs the code-of-conduct pipeline's own sign-off on anonymisation, and a published incident description cannot be unpublished.

- **Nothing published** - findings stay in the team's log.
- **Recap only** - what happened, numbers, photos, thanks; no findings. DevOpsDays endorses this much: blogging results is "optional, but strongly recommended."
- **Recap plus retrospective** (default) - Write the Docs Prague 2017's shape: recap plus a short section naming what went wrong and what changes next edition.
- **Recap plus retrospective plus transparency report** (starved rung) - full Prague 2017 artifact, adding an anonymised account of code-of-conduct reports and how each was handled. Tops value, effort, and compliance cost, so efficiency never picks it. **Promotion condition, keyed to Q10**: reports were actually resolved and `event-code-of-conduct`'s pipeline signs off on the anonymisation, or an incident was visible enough that silence would read as a cover-up.

**Delete condition, keyed to Q11**: for a private event, or findings that are personnel-sensitive or under confidentiality, delete every public rung rather than demoting them.

## Action-item tracking rigour

Ranked menu - lessons that actually reach next edition, per unit of standing overhead. Ownership discipline matters: every action item needs a named owner and a date, or it vanishes.

This does not assume a ticketing system exists; all rungs work with whatever the team has. The rungs are judgment.

- effort (setup, calendar, maintenance): `standing tracker with a review cadence > plan carry-over == mid-cycle check-in > owner and date on the entry`
- value (share of findings that change something): `standing tracker with a review cadence > plan carry-over > mid-cycle check-in > owner and date on the entry`
- efficiency: `owner and date on the entry > plan carry-over > mid-cycle check-in > standing tracker with a review cadence`

The effort tie is argued, not indecision: both the check-in and the carry-over cost one calendar entry and under half an hour, with nothing to build or maintain between the debrief and that date - unlike the standing tracker, which is a job rather than an appointment. They are not equal on value: the carry-over lands items in the document the team actually works from, so with effort tied, it wins the ratio.

- **Owner and date on the entry** - every entry carries a named person and a date, or an explicit "no action, because". Near-zero marginal effort. Stops orphaning, nothing more.
- **Mid-cycle check-in** - one dated check a few weeks out, confirming short-fuse items happened (vendor conversation, refund, apology, deposit chased).
- **Plan carry-over** - every open item written into next edition's work-back plan as a real task, handed to `event-planning-timeline`.
- **Standing tracker with a review cadence** (starved rung) - a persistent tracker reviewed on a recurring cadence between editions. Tops value and effort, so efficiency never picks it. **Promotion condition, keyed to Q12**: a year-round tracker already exists for something else, or findings routed structural work to `event-team-structure` (which happens between editions by definition).

**Default: owner and date on every entry, plus plan carry-over.** Add the mid-cycle check-in when items have a fuse shorter than the planning cycle. Move to the standing tracker when findings must resolve before planning starts (a legal-entity change, a succession gap).

For a final or one-off edition, **delete the carry-over and the standing tracker** rather than demoting them, keeping only the owner-and-date rule.

## Re-ranking against the interview answers

Say which answer moved which option, per menu, rather than silently reordering.

| Interview answer                         | Depth                                                                                                                                      | Publication                                                                                                                                                                                        | Tracking                                                                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Q6 - planning starts within weeks        | Promotes both single-session rungs, demotes both track-based rungs (they need cross-lead calendar coordination the deadline doesn't allow) | Barely moves, and say so - a recap isn't on the planning critical path, so let it slip rather than cutting the debrief short                                                                       | Promotes the plan carry-over hard - the document opens now and items can go in the same week                           |
| Q7 - final or one-off edition            | Demotes the written review unless a successor organisation will read it                                                                    | Promotes the retrospective and the transparency report - a closing edition's public account is the only record the community gets, which is why the JSConf EU and !!Con statements are still cited | Deletes the carry-over and the standing tracker                                                                        |
| Q7 - compounding, recurring edition      | -                                                                                                                                          | -                                                                                                                                                                                                  | Promotes the carry-over and the standing tracker                                                                       |
| Q8 - low effort ceiling / exhausted team | Deletes both track-based rungs outright                                                                                                    | Demotes the transparency report, since anonymisation is where its hours go, and keeps the recap                                                                                                    | Demotes the standing tracker and leaves the default untouched - the point of a default costing one field and one paste |

## Failure modes

- **Blame in the room.** One "you dropped this" reframes the session as a performance review, and the next finding never gets said; on a volunteer team the person simply does not come back, and that loss is invisible in the log. State the frame at the top and hold it out loud the first time it slips.
- **Skipping the debrief because the edition went fine.** Severity-gating is the one mechanic that explicitly does not transfer from the incident-postmortem lineage. A quiet edition still has practices worth naming before they are dropped.
- **Orphan action items.** An entry with an owner of "we" and a due date of "next time" is not tracked by anything. Assign a person and a date, or close it explicitly as no-action.
- **Manufacturing action items to look thorough.** The inverse failure, named directly in incident-postmortem practice: if a finding needs no action, say so.
- **5-Whys on every entry.** Five causal layers on a lunch mixup is over-engineering, and it crowds out the one finding that genuinely warranted it. The published precedent runs three shallow parts per finding with no root-cause treatment at all.
- **Re-diagnosing the day.** Rewriting the cue sheet, re-scoring the risk register or re-modelling the budget inside the debrief takes work from the sibling that owns it and produces a version nobody else will adopt. Hand back a finding, not a redesign.
- **Treating burnout as a personal failing.** "They took on too much" is not a finding; "one person held three roles with no backup" is. The first ends the conversation, the second routes to a structural fix.
- **Deferring the debrief until nobody remembers.** Six weeks out, the timeline is reconstructed from the loudest three memories and the quiet failures are gone. If the date has already slipped that far, say so and downgrade the claim the log makes rather than pretending the reconstruction is complete.
- **Trending across editions.** Comparing this edition's numbers to the last two is `samber/dev-event-organizer-skills@event-continuous-improvement`'s job. Produce one dated log; let the aggregation happen where it belongs.

## Measurement

Published guidance settles when, who, and what artifact a debrief produces, but leaves open how many of its lessons get acted on - see [references/field-precedent.md](references/field-precedent.md) for the sourced detail. This skill sets **exactly one pass threshold**, on the only thing fully inside the team's control:

- **Zero orphan entries** (binary). Every entry in the log has a named owner and a dated deadline, or an explicit "no action, because"; iterate until it holds by re-reading the log line by line and either assigning or closing each one. A log failing this is not a lessons-learned log, it is meeting notes.

The rest are signals to record, not targets to hit:

- **Days from doors closing to the debrief**. Record yours so the team can see the trend across editions.
- **Named-role coverage**: how many people who held a named role were in the room or submitted written input, out of the total. A low share explains a thin log better than any other number.
- **Carry-through rate** (only measurable from edition two onward): how many of last edition's action items were actually done. Record it as an input; the trend belongs to `samber/dev-event-organizer-skills@event-continuous-improvement`.

## Invocation examples

- "Our conference wrapped on Sunday. How do we run the post-mortem, and who should be in the room?"
- "We've got the attendee survey results back - how do we turn those plus our own notes into something the next edition actually uses?"
- "Should we publish what went wrong publicly, or keep it internal?"
- "Last year's debrief produced a list of fifteen lessons and we did none of them. What went wrong with the process?"
- "One of our organizers said in the debrief that they're completely burnt out. What do we do with that?"
- "Nothing really broke this year. Is a debrief still worth an evening?"

Expected output:

- a dated lessons-learned log of three-part entries, each with a named owner and a due date or an explicit no-action
- four reconciliations handed to the siblings that own the risk register, the budget, the run of show and the demand verdict
- a routed list of team-health findings
- a publication decision with its reason
- a stated handover to `samber/dev-event-organizer-skills@event-continuous-improvement`

## References

- [references/lessons-learned-entries.md](references/lessons-learned-entries.md) - the three-part entry format with both sourced worked examples and a negative counterpart, the "why it slipped through" categories, and the narrow criteria for escalating a single entry to a 5-Whys.
- [references/reconciliation-and-session-agenda.md](references/reconciliation-and-session-agenda.md) - the session agenda with a blameless opening script, the timeline reconstruction method, the four reconciliation checklists with their handback formats, two published team-health examples, and the handover packet to event-continuous-improvement.
- [references/field-precedent.md](references/field-precedent.md) - what published organizer guides say about post-event review, and why this skill's session mechanics come from the SRE incident-postmortem lineage instead.
