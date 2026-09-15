---
name: event-official-social-program
description: Decide how many official social occasions a technical event runs and how they sit against each other one occasion, two on separate slots, or a themed multi-activity track - plus the inclusion floor a whole slate must clear rather than each activity separately. Use whenever asked whether to run more than one social activity, whether two social activities can run in the same hours, how to publish a social track, or which activity a caregiver or a non-drinker can be in. Do NOT use for a single occasion's format, food, drink or alcohol posture - use samber/dev-event-organizer-skills@event-hospitality - third-party satellites - use samber/dev-event-organizer-skills@event-side-event-coordination - or invite-only gatherings - use samber/dev-event-organizer-skills@event-vip-social-program.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Official Social Program

You decide one thing: **how many official social occasions the event runs, and how they sit against each other.** One occasion, a second on its own slot, or a themed track of several. That is the whole subject.

`samber/dev-event-organizer-skills@event-hospitality` already decides what any single occasion _is_. None of the following reopens here:

- its format
- its food
- its drink
- its alcohol posture
- who it is for
- where it happens
- what it costs to attend
- when it starts and ends

## What is already decided, and by whom

This skill is narrow because the neighbouring ground is occupied. Read this section before ranking anything. If the answer you need sits below, this is the wrong skill.

- **The format of any one occasion** is `samber/dev-event-organizer-skills@event-hospitality`'s, outright.
  - Its menu decides "whether an evening or social programme exists and in what form", and ranks the formats by efficiency: `venue-based mixer > formal dinner with a programme > no organised programme > offsite excursion or activity`.
  - Never re-rank those rungs, rename them, or derive a competing menu.
  - Take that skill's answer as the shape of every occasion on your slate. Run its menu once per occasion.
- **Choosing zero occasions** is its rung too, not yours. "no organised programme" sits on the menu above, and that skill already tells you to publish the answer either way, because an unannounced absence sends people to an unhosted bar. The floor of _this_ menu is therefore one occasion. If the honest answer is none at all, that skill has already answered you, and this one has nothing to add.
- **The per-occasion brief** is specified in that skill's own reference file:
  - the owner
  - "The whole audience, or a subset."
  - "Where, and whether that place was chosen for access."
  - "What it costs the attendee."
  - "The food and drink"
  - "The start and the end"
  - the access lever it names as "family-inclusive evening programming"
  - Fill it in per occasion from there. Nothing on that list is re-specified here.
- **The alcohol posture** is its decision, set once for the event. A slate does not get a posture per activity.
- **Third-party-run satellites** are `samber/dev-event-organizer-skills@event-side-event-coordination`'s, which states the seam from its own side: the hospitality evening is what you provide, a satellite is what you permit. Your slate is what the event runs itself. Hand that skill your finished slate as the calendar its approvals deconflict against.
- **Invite-only and named-guest hospitality** is `samber/dev-event-organizer-skills@event-vip-social-program`'s. A slate of occasions open to every badge is yours. A dinner somebody has to be invited to is not, even when it sits in the same evening.
- **The published grid** is `samber/dev-event-organizer-skills@event-schedule-design`'s, whose own words are "You stop at the published grid". Hand it a non-overlap requirement. Never place or move a slot yourself.
- **Which access provisions exist at all** is `samber/dev-event-organizer-skills@event-accessibility-inclusion`'s: the "physical, sensory, dietary, economic and digital-access set". Never invent that set. Check a slate against whatever it published.

The ranking below is a default, not a law. It shifts with context and with who executes it. Re-rank it against what you already know, because each of these overturns a default rung:

- an edition whose social track is the reason people come
- a venue that already holds a second room at no extra ask
- a team where one person is quietly the owner of everything

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6 to 8 exist because the rungs diverge sharply on effort, durability and time-to-effect. Nobody can pick that default for the user.

1. Has `samber/dev-event-organizer-skills@event-hospitality` already decided the occasion format and the alcohol posture? If not, go there first. This skill ranks nothing until that answer exists.
2. How many distinct official social occasions are genuinely on the table? Did somebody ask for a second one, or is it an assumption you arrived with?
3. Which access commitments did the accessibility bar publish, and at what depth? Ask. Never invent the set.
4. Would any two occasions run in the same hours, or does each get its own slot against the published grid?
5. Is there a named owner for each occasion beyond the first? Answer per occasion, never for the slate as a whole.
6. What is the effort ceiling: volunteer hours, a budget line beyond the first occasion, a second room or venue? And what did last edition leave you?
7. One-off edition, or recurring, where the social track is part of why people come back?
8. By what date must each occasion's venue be held and its access statement published? Those dates, not the event date, are what this menu is ranked against.

## Slate depth

How many official social occasions the event runs, and whether any of them overlap. Every rung below assumes each occasion's own format comes from `samber/dev-event-organizer-skills@event-hospitality`'s menu, run once per occasion.

Value here is **coverage**: how many people find something on the slate they can be in and want to be in.

The menu, its four axis lines and every condition attached to them are this skill's own construction, not measured practice. Treat the ordering as a default rather than a law; Q2, Q5 and Q7 re-rank it.

- effort (owners to name, venues or rooms to hold, access routes to confirm, statements to publish): `themed multi-activity track > two occasions on separate slots > a single social occasion`
- value, coverage: `themed multi-activity track > two occasions on separate slots > a single social occasion`
- compliance cost (review triggered, reversibility spent): `themed multi-activity track > two occasions on separate slots == a single social occasion`
- efficiency: `a single social occasion > two occasions on separate slots > themed multi-activity track`

**Dominance check: 3 rungs, 3 pairs, zero strict-dominance relations; clean only by construction, which is never a pass.** The counting rule is every unordered pair of the three named rungs, with no rung excluded. One mechanism blocks all three pairs, and it accounts for every one of them rather than a share.

Each rung is the rung below it plus another occasion. Effort and coverage therefore march in the same order, and no cheaper rung ever outperforms a richer one on the value axis. That leaves no case for the test to catch, and no rung losing on value alone. Check the ordering against Q2's real count and Q5's real owners, not against the ranking.

**"Concentration" is a real property of a slate, and this menu does not rank it.** Concentration is the event having one shared moment everybody was in. It orders the rungs `a single social occasion > two occasions on separate slots > themed multi-activity track`, which is rank-identical to inverse effort.

Ranking it would discriminate nothing the menu does not already carry. Its only mechanical effect would be to make the dominance check look non-vacuous, while collapsing the efficiency line into cheapest-first. It is named here rather than ranked, so a reader who wants the shared moment argues for it directly.

The compliance tie is argued, not used to avoid deciding. A second occasion reusing the first occasion's venue, hours pattern, and alcohol posture triggers the reviews the first already triggered: one venue's access confirmation, one licensing question. Those are repeated rather than added to, and reversible the same way. The track sits genuinely above both, because concurrency across more than one room or building multiplies the access confirmation and the licensing question per place, and because a published track is expensive to withdraw once people have planned around it.

- **A single social occasion**, the default: one occasion, its format taken from `samber/dev-event-organizer-skills@event-hospitality`. It leads efficiency because the coverage a slate buys is front-loaded by construction rather than by any measured proportion. Whatever the audience does socially, it does at the first occasion. Every person a second occasion reaches is by definition somebody the first did not suit: a shrinking remainder, bought at a roughly constant cost per occasion.
  - **Promotion condition, keyed to Q2 and Q5, evaluated separately:** move up one rung only when both hold. Either failing keeps you here.
    - Q2 reports that somebody actually asked for a second occasion, rather than it being an assumption you brought.
    - Q5 names an owner for that second occasion.
- **Two occasions on separate slots**: a second occasion in its own hours, reusing the first's venue and posture, aimed at the people the first does not suit. It buys coverage without buying concurrency, which is what ties its compliance cost to the rung below. Its real cost is a second owner's evenings, which lands on `samber/dev-event-organizer-skills@event-volunteers`' arithmetic.
- **Themed multi-activity track**, the rung the efficiency order starves: it tops coverage and effort together, so efficiency never picks it. A team reaches for it when it wants the social programme to be a feature. Its real property is concurrency, which lets genuinely different activities coexist. A sequence cannot do that when people only have one evening.
  - **Promotion condition, keyed to Q3, Q5 and Q7, evaluated separately:** promote it only when all three hold. Any one failing leaves you below it.
    - Q3's published access set contains commitments no single format can carry at once (a family-inclusive occasion and a quiet, alcohol-free one are not the same room).
    - Q5 names an owner per activity, rather than one owner for the whole track.
    - Q7 says the edition recurs, so the track compounds across editions.
  - Where the track becomes the event's signature moment, route that call to `samber/dev-event-organizer-skills@event-cultural-identity`, which owns signature traditions and whose own published precedent reserves budget for "the fun things that make your event unique".

**Delete condition, keyed to Q5:** when Q5 names no owner beyond the first occasion, delete both rungs above "a single social occasion" from this menu and from the axis lines above. Delete rather than demote. A rung left at the bottom is how a plan gets built on one and then handed to nobody. `samber/dev-event-organizer-skills@event-hospitality` deletes its own upper rungs on the same trigger; there the rule governs formats, here a count of occasions.

**Deleted, not demoted: a slate published as a list of options with no statement of which one clears the access floor.** Delete it from this menu and from the axis lines above.

It looks like the generous rung, more choice for everybody. It is the rung where the choice is fake for exactly the people the floor exists for. A slate is not an access provision because it is long.

## The inclusion floor a slate must clear

**This section is the one thing here that a single-occasion decision cannot already answer.** It is why the skill exists at all. The floor below is this skill's own construction, not a published standard.

`samber/dev-event-organizer-skills@event-hospitality`'s reference already sets the floor for one occasion: whether the place was chosen for access, what it costs the attendee, and the family-inclusive lever. Applied per activity, that check passes on a slate that still leaves somebody with nothing. Every activity was considered individually, and the person who can be in none of them was never the subject of any single check.

The slate-level rule, stated as a floor rather than as a benchmark: **in every hour where the slate offers anything at all, at least one option clears the access set Q3 reported.** "At least one" is the minimum a floor can be, not an observed practice or a recommended number; no count above it is implied.

Each consequence below is a slate property, never an activity property:

- **A slot whose options nobody can clear is a slot the event excluded somebody from**, however well each activity in it was designed. Fix it three ways: add a clearing option to that slot, move one activity out of it, or narrow the slate. Never note the gap and publish anyway.
- **Publish which option clears the floor, beside the slate itself.** A reader decides whether to travel, arrange care, or come at all from the published slate, not from a page they find afterwards. Name which activity is step-free, which is family-inclusive, which is alcohol-free, in the terms Q3's published set uses.
- **Concurrency creates this problem, so Q4 is the question that finds it.** A slate whose occasions never share an hour cannot fail this floor on choice. It can only fail the ordinary per-occasion way, which the hospitality reference already covers.

Hand the finished check back to `samber/dev-event-organizer-skills@event-accessibility-inclusion`, which owns the set and its published depth. You check a slate against its bar. You never set the bar.

## What you hand on

Your output is a slate: a list of occasions, each with its own hospitality brief attached. Hand on what that slate generates:

1. **To `samber/dev-event-organizer-skills@event-schedule-design`**: the non-overlap requirement. Name which occasions must not share hours with each other, and which must not share hours with the main programme. State it as a requirement. That skill places it, and you never move a session or a slot yourself.
2. **To `samber/dev-event-organizer-skills@event-side-event-coordination`**: the confirmed slate, as the calendar third-party satellites are deconflicted against. It cannot protect hours it does not know about.
3. **To `samber/dev-event-organizer-skills@event-accessibility-inclusion`**: the per-slot floor check above, and any slot you could not clear.
4. **To `samber/dev-event-organizer-skills@event-code-of-conduct`**: the count and the places, so the scope clause reaches every occasion rather than the one everybody remembered.

Present the slate for approval before holding any second venue. A slate published and then shortened reads as a cancellation.

If your harness has persistent memory, record per edition:

- how many occasions ran
- which hours they occupied
- which one each population actually attended
- which slot failed the floor, if any did

Next edition ranks against that record instead of this default.

## Failure modes

- **Re-deciding a format this skill does not own.** The occasion menu is `samber/dev-event-organizer-skills@event-hospitality`'s. A second, differently-worded ranking of the same rungs is not a slate decision. It is a duplicate that makes the reader choose between two orderings of one menu.
- **Counting a satellite as part of your slate.** An event somebody else runs is permitted, not provided. It belongs on the deconfliction calendar, never on the slate you are accountable for.
- **Adding an occasion because there is room in the evening.** The trigger is Q2's actual request plus Q5's actual owner, not an empty hour.
- **Checking access activity by activity and calling the slate checked.** This is the failure the floor above exists for, and it passes every individual review on the way through.
- **Publishing the slate before the access statement.** People plan around the slate the moment it appears. A statement arriving later reaches only whoever is still deciding, which is not the population it was written for.
- **Letting one owner hold a track.** A track with a single owner is a sequence with optimism attached. Q5 is worded per occasion to catch exactly this.

## Measurement

This skill supplies no attendance figure, no activity count and no ratio of its own. The activity count and the weekday in § Invocation examples sit inside a user's own question, and are not quantities to reuse. Everything below is self-set except the gate, and only becomes meaningful across editions.

- **Slot floor coverage** (gate): every hour the slate occupied offered at least one option clearing the published access set. No threshold applies; the number is zero uncovered slots.
- **Occasions run against occasions owned** (self-set): an occasion that ran without the owner Q5 named is the failure this menu's delete condition exists to prevent.
- **Who attended which occasion, by population** (self-set): the only read on whether a second occasion reached anybody the first did not, and so on whether the promotion condition was right.

Pick one. Write down before the event what it would change next edition, then record it.

## Invocation examples

- "We already decided on an evening mixer. Should we also run a morning run and a board-game table, or is one thing enough?"
- "Three social activities, all at the same time on Thursday evening. Is that a problem?"
- "How do I publish a social track so people know which activity they can actually attend?"
- "Somebody wants a second social event on day two. What has to be true before I say yes?"

Expected output:

- a slate naming each occasion with its own hospitality brief attached
- the per-slot access floor check, with any uncovered slot named
- the non-overlap requirement written for the schedule
- the promotion or delete condition that produced the slate's depth

Label every element of that output as taken from a sibling skill or as set here.

## References

This skill has no reference files. Its only decision is the menu above, and the per-occasion detail a reference would carry already exists in `samber/dev-event-organizer-skills@event-hospitality`'s own reference file. Duplicating it here would create the competing second copy this skill exists to avoid.

See also, same collection:

- `samber/dev-event-organizer-skills@event-hospitality`: decides whether a social occasion exists and in what form, sets the alcohol posture, and specifies the per-occasion brief. Run its menu once per occasion on your slate; never re-rank it.
- `samber/dev-event-organizer-skills@event-side-event-coordination`: approves and deconflicts events somebody else runs; receives your slate as the calendar it protects.
- `samber/dev-event-organizer-skills@event-vip-social-program`: invite-only and named-guest gatherings, which never sit on this open slate.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion`: owns the access set the slate floor is checked against, and its published depth.
- `samber/dev-event-organizer-skills@event-schedule-design`: places the slate's hours in the published grid; receives the non-overlap requirement.
- `samber/dev-event-organizer-skills@event-code-of-conduct`: owns the scope clause that must reach every occasion on the slate.
