---
name: event-community-building
description: Animate one recurring technical event's own audience in the gaps between editions - the cadence posture for the standing space, the conversion of attendees into returning participants and contributors, keeping a local cohort of the same event's fans warm, and handing the community asset over when organizers change. Use whenever asked how to keep an event's community alive between editions, what to post in the quiet months, whether a between-editions space should stay dormant or be programmed, how to make attendees come back next year, or who takes over the community platform when an organizer leaves. Do NOT use to decide whether that space belongs in the team's property set at all - use samber/dev-event-organizer-skills@event-portfolio-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Community Building

You animate one recurring technical event's own audience during the months when no edition is imminent. Your object is an **edition cycle**, not a product and not a standing meetup series. One outcome pays you: "this person comes back next edition, and some of them bring work with them".

Inherit the space, never choose it. `samber/dev-event-organizer-skills@event-portfolio-strategy` decides whether a continuity surface belongs in the team's property set; decide how to run it once that answer is yes. Never recommend adding or retiring the surface as a property, and route that recommendation back there.

Produce three things:

- A cadence posture for the gap, with a named owner.
- A mechanism that converts attendees into returning participants.
- A written handoff of the community asset that survives an organizer leaving.

## Where the line is

Seven boundaries, mirrored rather than re-derived. Read [references/sibling-boundaries.md](references/sibling-boundaries.md) for each sibling's own statement of the line.

| Sibling                      | The line                                                                                                                                                                                           |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event-comms-channels`       | Owns one edition's channel lifecycle. You own the gap after wind-down decides a channel persists; hand back a live member list at next build-up. Never redesign its roster, routing, or wind-down. |
| `event-volunteer-experience` | Owns the volunteer alumni loop (list, thank-you, candidate flag). Your audience is every non-volunteer member; run its alumni channel as a segment inside your surface, never a second space.      |
| `event-portfolio-strategy`   | Gates whether the surface exists at all. A touchpoint that comes to need a venue, schedule, or speaker roster routes there.                                                                        |
| `cross-event-promotion`      | Faces outward; you face inward. A partner event in your space is content you deliver, not a deal you broker.                                                                                       |
| `event-cultural-identity`    | Sets the register; you execute it - never invent a quieter off-season voice.                                                                                                                       |
| `event-growth-strategy`      | Owns whether the event scales. A healthy carry rate is evidence you hand to `event-market-fit`, never a growth recommendation you make.                                                            |
| `event-code-of-conduct`      | Binds your space exactly as it binds the room. Name the owner, route policy and reporting there.                                                                                                   |

## A handover moves three artifacts, only one is yours

1. **Team and decision rights** - `event-team-structure` (charter, backup admins).
2. **The operational learning log** - `event-continuous-improvement` (bus-factor mitigation).
3. **The community asset** - platform, member list, archive, invite links, retention decision. Menu 3 below; nothing else claims it.

Splitting the handover three ways is this skill's own construction, made so none of the three is assumed covered by whoever handles the loudest one.

`event-team-structure`'s 6-12-month window covers the lead role, not a platform account. Set the asset's own timeframe as the team's call.

## Four generic mechanics live in `samber/developer-relations-skills`

That collection owns generic online-community craft for a product or standing meetup series. Recommend and reuse, never re-derive:

| Need                                                    | Skill                            |
| ------------------------------------------------------- | -------------------------------- |
| Platform/venue choice, seeding, go/no-go, shutdown      | `developer-community-launch`     |
| Health metrics, contributor funnel, dashboards          | `developer-community-health`     |
| Moderation policy, enforcement ladder, moderator roster | `developer-community-moderation` |
| Unpaid champion/ambassador design, intake, perks        | `developer-champions`            |

That collection's `developer-meetup-program` draws its own line back here once "the program outgrows an evening". Its attendee-to-co-organizer ladder is built for a standing meetup; Menu 2 re-scopes that shape to one edition cycle.

## Interview

Ask one question at a time, multiple-choice where possible. Ask 7 to 9 before any menu: the menus diverge sharply on time-to-effect, durability and effort, so nobody can pick their defaults for the user.

1. Does the event run annually or more often, and how many editions have happened?
2. Does a standing space already exist, on what platform, and did it come from the last edition's channels or open separately? (No decided surface → route to `event-portfolio-strategy` first.)
3. Who owns it today - named person, rotating role, or nobody? Whose account is the platform registered to?
4. Does a register exist (`event-cultural-identity`)? If not, route there first and label anything provisional.
5. Is your audience one city, one region, or traveling? If multi-city, are any local groups run by people you do **not** organize with?
6. What already carries the audience across the gap - an announcement list, archive, podcast, nothing?
7. Is there a hard live-by date - next-edition announcement, a departing organizer's last month, a platform migration?
8. Effort ceiling **in the quiet months specifically**: who has recurring hours when nothing is being produced, and is anyone funded to moderate?
9. One-off or compounding: is a next edition already intended, and does the team expect to turn over before then?
10. What assets exist that the defaults assume away - an existing chat space, a member list with live consent, an in-house writer, a reopenable archive?
11. Does a legal entity stand behind the event, and does it have to be able to show who holds which access?

Every ranking below is a default, not a law. Re-rank all three menus against Q10 and say which answer moved which rung.

## Who is available in the quiet months

One answer reshapes every menu below: who is available when nothing is being produced (Q8). A vendor-run event has someone whose job includes the quiet season. A volunteer team has the same people who just finished an edition and are recovering.

Say which pole a recommendation assumes whenever the two differ. This split is this skill's own working model, not an industry standard.

## Workflow

1. Run the interview. Stop and route out on Q2 (no surface decided) or Q4 (no register).
2. Read what the edition already decided: which channels `event-comms-channels` wound down, which persisted, on what terms. Start where its wind-down ended.
3. Take the register as given. Write only its between-editions _expression_, so the off-season voice stays auditable against it instead of blurring into a new one.
4. Choose the cadence posture (Menu 1), naming the quiet-months owner. No named owner is undecided dormancy.
5. Choose the conversion mechanism (Menu 2), scoped to non-volunteer members; route volunteer-shaped work to `event-volunteer-experience`.
6. Separate engagement from governance before touching anything local (§ Local cohorts). This is the easiest line here to cross without noticing.
7. Write the Menu 3 handoff now, not when someone leaves. Include the member list's owner and retention decision, restated.
8. Publish what the space is for and isn't. An unstated job drifts into a support channel, a job board, or silence.
9. Hand the live member list back to the next edition's channel design at build-up: who joined, on what consent basis, who is reachable.
10. Present the plan section by section - cadence, conversion, local posture, handoff - and get each approved before changing anything a member can see.

If your harness has persistent memory, record per gap:

- The cadence posture and its owner.
- What was actually posted versus planned, and every month the owner missed.
- The conversion mechanism and who moved along it.
- The member count at each edition's open and close, with its consent basis.
- The handoff document, with its date.
- Every rung you rejected.

The missed months are next gap's cadence decision. The rejected rungs are what stops the next organizer re-litigating all of this from zero.

## Menu 1 - Between-editions cadence posture

How much programming the space gets while no edition is imminent. Two value axes, because "the audience is still there" and "the space still reads as alive" are different quantities and no rung tops both. Rungs, axes and orderings are this skill's own construction.

- value, warmth (members who arrive at the next announcement ready to act - buy early, answer a call, carry word of mouth): `continuous heavy > continuous light > occasional pulse > dormant-but-open`
- value, robustness (the space never reads as abandoned, because it never promised more than it delivers): `dormant-but-open > occasional pulse > continuous light > continuous heavy`
- effort (recurring hours in the quiet months, moderation load, and the burnout it lands on people who just finished an edition): `continuous heavy > continuous light > occasional pulse > dormant-but-open`
- compliance cost (the review it triggers and the reversibility it costs): `continuous heavy > continuous light > occasional pulse > dormant-but-open`
- efficiency: `dormant-but-open > occasional pulse > continuous light > continuous heavy`

No rung dominates another, and that holds by construction rather than because a check found none. Robustness runs exactly backwards to warmth: a rung buys warmth by promising more, and robustness is exposure to the promise the team stops keeping.

Compliance cost is real. A standing space carries a live conduct duty, and a member list that outlives the edition it was collected for.

Dormant is the floor, not zero. A retained list still needs a named owner and a retention decision; route that decision to counsel, and name no jurisdiction or period. Read [references/cadence-and-content-shapes.md](references/cadence-and-content-shapes.md) for each rung as a concrete artifact.

- **Dormant-but-open** (default) - freeze programming, keep the archive and the member list intact, post one dated notice that the space is quiet until next build-up. Near-zero effort, and it cannot fail publicly. Notice template and pulse plan sit in the reference. Where the last edition ran per-team or per-project sub-channels alongside the general space, keep those too rather than folding them into the general archive. A returning member reopens the channel scoped to their own project to check its progress, and the general channel does not replace that.
- **Occasional pulse** - a digest or spotlight on a rhythm the owner can actually hold, nothing else. Promote when Q1 is annual-or-less and Q8 names someone with recurring gap-months hours; without both, it lapses by month three.
- **Continuous light** - standing prompts and threads, no live sessions or sub-channels. Promote when Q6 says nothing carries the audience and Q9 says compounding.
- **Continuous heavy** (starved rung) - recurring live sessions, sub-channels, near-standing moderation load. Promote only when all hold: Q10 says the space is already the audience's primary home, Q8 names a funded moderator roster, Q9 says compounding. One step further and it is a standing meetup series (`developer-meetup-program`'s object, not yours).
- **Delete, never demote:** closing the space each edition and reopening fresh. Looks like cheap dormancy; discards the member list and archive instead. `event-comms-channels` promotes export-plus-deletion only when the edition is a one-off, with no next edition to spend the list on.
- **Conditional delete:** continuous heavy where Q8 says nobody is on duty - an unmoderated standing space is a conduct obligation with no responder.

Christopher Allen's community-size thresholds bound the two continuous rungs, never a dormant archive or a member list, which is a stock rather than a group. See [references/cadence-and-content-shapes.md](references/cadence-and-content-shapes.md) § Sizing thresholds for the figures and their limits.

## Menu 2 - Converting attendees into returning participants

Non-volunteer members only. Two value axes: breadth is who comes back at all, depth is who arrives with work in their hands. Rungs, axes and orderings are this skill's own construction.

- value, breadth (share of last edition's attendees who register for the next one): `single re-engagement touchpoint > fed local cohort > structured participation ladder > no mechanism`
- value, depth (members who produce something the next edition uses - a talk, a review, a host, sustained word of mouth): `structured participation ladder > fed local cohort > single re-engagement touchpoint > no mechanism`
- effort (coordination, standing ownership, reversibility): `fed local cohort > structured participation ladder > single re-engagement touchpoint > no mechanism`
- efficiency: `single re-engagement touchpoint > structured participation ladder > fed local cohort > no mechanism`

No rung dominates another here either, and again the axes make that true rather than a check confirming it. Breadth and depth run opposite each other across the three real rungs, and "no mechanism" sits bottom on both value axes while costing least.

No compliance-cost axis. Every rung reaches people through the attendee list, whose consent `event-attendee-email-sequences` already owns end to end, so inherit that duty rather than writing a second one. One exposure survives: a public status marker names a person, so ask consent before naming anyone, exactly as `event-volunteer-experience` gates its own thank-you.

- **Single re-engagement touchpoint** (default) - one deliberate contact to last edition's attendees, timed to next edition's opening. Reaches the whole list for an afternoon. Its first place rests on an argued premise, not a measurement: breadth is what the next edition is usually short of. Move up when Q9 is compounding and Q6 says something already carries the audience.
- **Structured participation ladder** - named steps attendee → regular → contributor, each with a stated way in and a stated reward (`developer-meetup-program`'s ladder, re-scoped). What doesn't transfer: a meetup runs on monthly contact, so a rung can take three meetings; an annual event gives one live touch a year, so every rung above the first must be climbable asynchronously or it never gets climbed. For a long-running event, inviting past winners or standout contributors back as participants at an anniversary edition is a concrete top rung. It reuses the alumni base as both a returning-attendee mechanism and the edition's own concept hook, rather than treating alumni only as a mailing list to reach.
- **Fed local cohort** (starved rung) - a group of the event's own audience in one city, kept warm between visits. Tops effort (needs a standing local owner who isn't you). Promote when Q5 is genuinely multi-city and Q10 names a willing local person. Read § Local cohorts first.
- **No mechanism** - whoever remembers comes back. Near-zero effort, near-zero return; the rung a team lands on by not deciding. A first edition with no list yet is a defensible case.
- **Delete, never demote:** auto-enrolling every registrant as a member. Manufactures the membership number and spends a ticketing consent basis on a purpose it never granted.
- **Conditional delete:** fed local cohort where Q5 is one city that doesn't travel - that "cohort" is just your audience, and animating it is Menu 1's job.

## Local cohorts: the engagement half only

`event-portfolio-strategy` names the brand-licensing half a genuine gap: "recruiting, vetting and enforcing standards on teams you do not run", which no skill in this collection covers. `event-growth-strategy` puts the decentralized franchise model outside its own scope as well.

Own the engagement half only: keep a local group of your own event's audience warm between visits, in your register, on your surface. The moment the question turns to who may use the brand, or how an independently-run team is vetted, you are standing in that gap. Say so and stop.

The test, this skill's own construction: **does anyone outside your organizing team run an event under your name as a result of this?** Yes means governance, not yours. A chat sub-space, local thread or list segment your team still owns means engagement, yours.

Published chapter models bundle the two halves, so expect to separate them by hand. Read [references/returning-participant-ladder.md](references/returning-participant-ladder.md) for the worked split.

## Menu 3 - Handoff of the community asset

The platform, the member list, the archive, the invite links, and the retention decision attached to them. Not the team (`samber/dev-event-organizer-skills@event-team-structure`) and not the learning log (`samber/dev-event-organizer-skills@event-continuous-improvement`) - see § A handover moves three artifacts, only one is yours.

Rungs, axes and orderings are this skill's own construction. The handoff shape itself is carried over from adjacent organizational practice, not measured against event data.

- value, recoverability (credentials, ownership of record, the member list and its retention decision all end up in the hands of a named living person who is still involved): `fully proceduralized transition > documented ownership and access transfer > named successor with an overlap period > informal handoff`
- value, continuity of animation (the space keeps its voice and its regulars through the change): `fully proceduralized transition > named successor with an overlap period > documented ownership and access transfer > informal handoff`
- effort (hours, standing process, political capital spent asking someone to hand over something they built): `fully proceduralized transition > named successor with an overlap period > documented ownership and access transfer > informal handoff`
- compliance cost (the review it triggers and the reversibility it costs): `fully proceduralized transition > named successor with an overlap period > documented ownership and access transfer > informal handoff`
- efficiency: `documented ownership and access transfer > named successor with an overlap period > fully proceduralized transition > informal handoff`

No rung dominates another here either. The axis lines carry three separate reasons why, and none of them is a check the menu passed:

1. The two middle rungs swap places between recoverability and continuity of animation.
2. The proceduralized rung tops both value axes and effort at once.
3. Both middle rungs beat informal on both value axes, and fail only on cost.

Splitting "continuity" into recoverability and continuity of animation breaks the apparent tie. An overlap period inherits the voice and can still leave a platform registered to someone who left. A documented access transfer buys exactly that recoverability.

Compliance cost here is not Menu 1's. A handoff is the moment a credential changes hands and the member-list retention decision must be restated rather than silently inherited. Informal sits lowest for the wrong reason: it triggers no review, so the conduct duty stays live with nobody assigned.

- **Documented ownership and access transfer** (default) - one written page: every account, admin role, invite link, domain, list; who holds each today and after; the member list's owner and retention decision. An afternoon, and it fixes the one failure that actually orphans a space.
- **Named successor with an overlap period** - named before departure, running alongside the outgoing owner. Promote when Q7 names a departing organizer's last month and Q9 is compounding. Set the overlap length yourself - do not borrow `event-team-structure`'s lead-role window, a different artifact.
- **Fully proceduralized transition** (starved rung) - a written playbook, access checklist, moderation-role transfer, retention decision signed off. **Promotion condition, keyed to Q9 or Q11**: planned rotation, or the event sits under a legal entity that must show who holds what.
- **Informal handoff** - whoever is around briefs the new organizer. Near-zero effort, near-zero recoverability - the default by inaction.
- **Delete, never demote:** adding the successor as a second admin while the departing organizer's personal account stays owner of record. Looks like the cheapest default rung; is precisely its failure mode - unrecoverable the day that account closes.

## Failure modes

- **A cadence with no named owner** reads as continuous in the plan, abandoned by month three. Fix: Q8 names the person before Menu 1, or the posture is dormant by decision.
- **Inventing an off-season voice** ("in the quiet months it's basically just us"). `event-cultural-identity` settles it: identity is fixed, only expression modulates.
- **Absorbing the franchise question** ("should we start chapters") - a governance question two siblings disclaim. Fix: run the one-question test in § Local cohorts and stop.
- **Re-running the volunteer alumni loop** because past volunteers are in the space. Not yours; that skill owns the list, thanks, and flag.
- **Designing a relay mini-event.** The moment a touchpoint needs a venue, schedule, or speaker, it's an event property for `event-portfolio-strategy`.
- **Treating the member list as inherited, not decided.** It outlives its edition. Fix: owner and retention decision on day one, restated at every handoff.
- **Measuring the space instead of the edition.** A noisier space isn't a returning audience. Fix: carry rate is the only number that answers this skill's question.
- **Programming into a gap nobody has capacity for.** Choose the posture against Q8's honest answer, not the team's intentions the week after the event.

## Measurement

Every threshold here is self-set rather than an industry benchmark. Fix each one before the gap starts, never after the data arrives.

- **Carry rate** (self-set): the share of one edition's attendees who register for the next one - the skill's own outcome number, handed to `event-market-fit`. Industry-blended context (Freeman's Ken Holsinger, _Trade Show Executive_, 2025): "our industry's blended retention rate is barely above 30%" - blends every event type, none a technical conference. Read as evidence return rates run lower than assumed, never as a target.
- **Cadence kept** (gate, binary): posts planned versus posts made in the gap, on the posture chosen. This is the honest read on whether the rung was affordable, and it is the input to next gap's choice - two missed cycles is a demotion signal, not a discipline problem.
- **List integrity** (gate): the member list has a named owner and a written retention decision, on the day the gap starts. Failing this is failing the compliance axis, whatever the engagement looks like.
- **Handoff readiness** (gate): the access document exists, is dated, and names a living holder for every account. Check it on a schedule, not when someone resigns.
- **Ladder movement** (self-set, only where Menu 2's ladder rung is in use): how many members moved a step. Small numbers are the expected shape; report the count, not a rate, since the denominator is meaningless at these sizes.

Pass threshold, iterated until met: all three gates. Each one checks against the list and the document you built, which is what makes them usable with no external benchmark to compare against.

## Invocation examples

- "Our conference sells out every year and the Discord is a graveyard for eleven months. What should we be posting?"
- "Half our attendees are new every edition. How do we get last year's people to come back?"
- "Our founder is stepping down and she owns the community Slack on her personal account. What has to happen?"
- "People in three other cities keep asking to run a local version. Is that ours to say yes to?"

Expected output: a between-editions plan with:

1. The cadence posture, its named owner and the rungs rejected.
2. The between-editions expression of the register, written as a delta against it.
3. The conversion mechanism scoped to non-volunteer members.
4. The local posture with the engagement/governance line drawn explicitly.
5. The member list's owner and retention decision.
6. The dated handoff document.
7. The self-set thresholds and three gates.

Label every self-set threshold as such, and present the whole plan section by section for approval.

## References

- [references/sibling-boundaries.md](references/sibling-boundaries.md) - each sibling's own statement of the line, and the fuller mirrored reasoning behind it.
- [references/cadence-and-content-shapes.md](references/cadence-and-content-shapes.md) - what each cadence rung looks like as an artifact, the dormancy notice, a worked pulse plan and a negative example, the between-editions register delta, the two-sided seam table against the within-edition channel architecture, and the sizing thresholds.
- [references/returning-participant-ladder.md](references/returning-participant-ladder.md) - worked shapes for the re-engagement touchpoint and the participation ladder re-scoped to an edition cycle, the local-cohort engagement/governance separation with a worked split, and a negative example for each.
- [references/community-asset-handoff.md](references/community-asset-handoff.md) - the asset inventory, the three-way artifact split, the member-list retention decision, the dated handoff checklist, and the personal-account negative example.

Sibling skills referenced throughout: see § Where the line is.
