---
name: event-vip-social-program
description: Run the private gathering alongside a public technical event, once a named-guest programme already exists - how the seat list is assembled when sponsors, speakers and the organizer all put names forward, how invitations and the door work without publishing a tier, and where the gathering sits against the public programme. Use whenever the user mentions a private dinner or reception at a conference, refusing a sponsor's seat request, an invite-only room without a VIP badge, or when to schedule one - even if they never say "VIP". Folding it into the general evening is the default answer. Do NOT use to decide whether a guest qualifies - use samber/dev-event-organizer-skills@event-vip-management; food is samber/dev-event-organizer-skills@event-hospitality.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event VIP Social Program

You run a room that not everyone can walk into, at an event where everyone can walk into everything else. Three decisions, and only three, cover the job:

- How the seat list gets assembled when more than one party is putting names forward.
- How the invitation and the door work without publishing that a tier exists.
- Where the gathering sits against the public programme.

The default answer is that there is no separate room. That is a rung on the first menu, not a refusal to help, and at a community-run event it is the most common correct outcome.

## How little this skill owns, and why that is deliberate

Almost everything a reader means by "VIP social programme" already has an owner. What is left is narrow.

- **Whether a named-guest programme exists at all → not yours.** `samber/dev-event-organizer-skills@event-vip-management` decides it, on a test it states as an **obligation, never a title**, and its own most common correct answer is that nobody is left in scope. It also owns the escort depth, the guest's own visibility, and the obligation roster.
  - Run it first. If it finds nobody, this skill has nothing to do.
- **What is served, and whether an evening exists → not yours.** `samber/dev-event-organizer-skills@event-hospitality` decides the catering style, the alcohol posture, and whether an evening or social programme exists at all. Its reference file already separates the two artifacts you are standing between: `"the evening event" and "an invited dinner" are different artifacts`; it designs only the first.
- **The speakers' dinner → not yours.** `samber/dev-event-organizer-skills@event-speaker-experience` owns it, on its own budget line, and `event-hospitality` says from its own side that it will `never re-decide a speakers' dinner, a volunteer meal or a VIP table`. That budget line describes speakers and nobody else. Never carry it over to the rungs below.
- **A gathering that was sold → not yours to allocate.** `samber/dev-event-organizer-skills@event-sponsor-fulfillment` delivers what a signed agreement promised, gated on payment. Be precise about the split, because it is easy to get backwards:
  - A sponsor _asking_ for seats at your gathering is this skill's allocation problem.
  - A gathering the agreement _sold_ is that skill's deliverable, and you do not get to ration it.
- **Somebody else's party → not yours.** `samber/dev-event-organizer-skills@event-side-event-coordination` approves and deconflicts events run by third parties, and states the seam from its own side: `Where that skill's evening is the thing you provide, yours is the thing you permit.` A sponsor-hosted reception is theirs. Yours is a room you host.
- **The social track everyone can join → not yours.** `samber/dev-event-organizer-skills@event-official-social-program` designs the announced social programme for the whole audience. If the honest answer to "who is this for" is "anyone who wants to come", you are in that skill, not this one.
- **Choosing an invite-only dinner as the whole event → not yours.** `samber/dev-event-organizer-skills@business-event-formats` picks between company-run shapes where the dinner _is_ the event. Here the dinner is a room inside somebody else's conference.

What survives all of that is the private-gathering mechanics, and only those. `event-vip-management` hands them over explicitly and then designs none of them: `A guest's table is therefore yours; the food on it is not.` This skill is that table.

## How to use the menus and defaults

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank all three menus against what you already know. Any of these overturns a default rung:

- A venue with a side room.
- A team member who already owns the relationship with whoever is asking for seats.
- A list that survived from last edition.
- An organizer who already knows every guest personally.

No quantity is prescribed anywhere - no seat count, no cap, no lead time, no headcount - because invented numbers read as benchmarks. Every number that does appear is either quoted from published guidance or a reader's own words about their own room, never a threshold this skill sets.

## The named owner

Designate one contact person who holds the seat list, builds it, sends the invitations, works the door, and answers every refusal. Governance and organizational practice establish the pattern. That same person decides any exception to the list at the door.

- Carries over to a private gathering: the role.
- Does not carry over: a protocol office's own staffing, or its authority over a building.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4, 7 and 8 exist because the menus below diverge sharply on time-to-effect, durability and effort ceiling - those defaults cannot be picked for the user.

1. Has `samber/dev-event-organizer-skills@event-vip-management` already run, and did it find anybody in scope? If not, stop and run it. It decides whether a named-guest programme exists at all, and this skill assumes that answer rather than re-deciding it.
2. Who owns the event and what does its register say about status - flat and explicitly anti-hierarchy, or comfortable recognizing who is in the room?
3. Name each guest the gathering exists for, and say in one sentence what the room does that the general evening cannot. For each: did they, or their office, ask not to be identified, listed or photographed?
4. How long until doors, and are the room booking, the schedule and any printed programme still open? Does any guest have a fixed arrival or departure window, and does any existing slot fit inside it?
5. Who else is asking for seats - sponsors, speakers, board members, your own team - and what did each ask for, in their words? Has anybody already been told yes, and by whom?
6. What does the room seat, and who set that number: the venue, the budget, or the conversation you actually want to have?
7. Who owns this by name - builds the list, sends the invitations, works the door, and answers the party who gets refused? Are they also running the main event that day? Reversibility is not symmetric here: a seat can be added, and an issued invitation cannot be withdrawn without costing more than the seat did.
8. One-off, or does this recur edition after edition? And has anything about it already been published or promised, in what artifact - a prospectus, an agreement, a schedule, an email?
9. Which assets re-rank the defaults: a venue with a usable side room, a team member who already holds the relationship with whoever is asking, a list from last edition?

## Community vs vendor pole

Who owns the event moves one menu, on the same community-versus-vendor split the rest of this collection argues.

- **Community pole.** A room not everyone can enter contradicts the register `samber/dev-event-organizer-skills@event-cultural-identity` sets. Menu A's fold is not a compromise at this pole. It is usually the right answer, and the burden sits on whoever wants the room to name what it does that the general evening cannot.
- **Vendor/corporate pole.** A private room is ordinary and often the reason a guest came. The seats are then scarce for a stated reason, and the defensibility half of Menu A's value carries most of the weight.

Say which pole a recommendation assumes wherever they differ. The pole moves Menu A's default and nothing else. Menus B and C hold their order across both.

## Workflow

1. Run the interview. If Q1 says no named-guest programme exists, stop and route to `samber/dev-event-organizer-skills@event-vip-management`.
2. Answer Q3's second half first: what does the room do that the general evening cannot? If nothing survives that question, Menu A's default is the answer and the rest of this skill does not run.
3. Set the seat-list construction rule (Menu A). Then build the list - its fields, its named owner, its circulation, and its deletion date, decided now - from [references/invitation-and-door-mechanics.md](references/invitation-and-door-mechanics.md).
4. Set the invitation and access mechanics (Menu B). Issue invitations from the same reference: individually, privately, by the person holding the list.
5. Set the placement against the public programme (Menu C), then hand the slot to `samber/dev-event-organizer-skills@event-run-of-show` and the grid clash to `samber/dev-event-organizer-skills@event-schedule-design`. Tell them the slot. Never move a public session to make room for a private one.
6. Write the refusal rule down before the first ask arrives, and cite the same one to every party. The rule is the whole of the defensibility, and it is cheap only in advance.
7. Hand off what is not yours:
   - Catering and drink for the room: `samber/dev-event-organizer-skills@event-hospitality`.
   - Any access need: `samber/dev-event-organizer-skills@event-accessibility-inclusion` - a guest who cannot enter the room is an access question first.
   - Anything a guest's own security detail requires: `samber/dev-event-organizer-skills@event-vip-management`.
   - The code-of-conduct reach over a private room: `samber/dev-event-organizer-skills@event-code-of-conduct`, which decides which spaces its scope clause covers.
8. Present section by section - purpose, list rule, list, invitation and door, placement, refusal rule - and get explicit approval per section before finalizing.

If your harness has persistent memory, record per edition:

- What the room was for.
- Who asked for seats, and what each was told.
- Which rule was cited.
- Whether the list was deleted on its date.
- Whether any attendee mentioned the room afterward.

Next edition starts from that instead of re-arguing the same asks.

## Menu A - seat-list construction rule

How the list gets assembled when the organizer, sponsors and speakers all have names to put forward. Two value axes run close to opposite, which is why this menu prints two value orderings rather than one.

- effort (organizer-hours, arbitration between asking parties, the conversations a refusal costs, records kept): `open nomination with published criteria and a host veto > host list + capped nominations per asking party > host-nominated only > no separate list`
- value, the room is right (the people the gathering exists for are actually in it): `host-nominated only > host list + capped nominations > open nomination with criteria > no separate list`
- value, the answer is defensible (every party who asked can be told why, and the same rule was applied to each): `open nomination with criteria > host list + capped nominations > no separate list > host-nominated only`
- compliance cost (review triggered, reversibility spent): `open nomination with criteria > host list + capped nominations > host-nominated only == no separate list`
- efficiency: `no separate list > host list + capped nominations > host-nominated only > open nomination with criteria`

**Dominance check: four rungs, six pairs, zero strict dominance relations - and two distinct mechanisms account for all six, not one.**

Four pairs are blocked because the two value axes run opposite, and in each the rung that puts the right people in the room is the rung whose rule is hardest to defend:

- Open nomination against capped nominations.
- Open nomination against host-nominated only.
- Capped nominations against host-nominated only.
- Host-nominated only against the fold.

The remaining two pairs are blocked by cost rather than by opposition, the busier rung winning both value axes and losing on effort:

- Open nomination against the fold.
- Capped nominations against the fold.

This menu is **clean by construction on four pairs and by a cost trade on two, which is not a pass either way**. The efficiency line rests on each rung's own argument below.

The compliance `==` is argued: compliance is the one axis on which the two cheap rungs come out equal, since effort already separates them and this axis deliberately does not.

- **Host-nominated only:** creates a small named-person list carrying one retention decision. A list nobody was told about can still be shortened - it holds an artifact and spends no reversibility.
- **The fold:** holds no artifact at all. Every invitation it issues is verbal, unrecorded and impossible to withdraw cleanly - it spends reversibility and holds nothing.

Equal exposure, opposite halves. The two busier rungs sit above both because capped nominations means holding names a sponsor supplied about somebody else, and published criteria are a commitment you can be held to next edition.

- **No separate list** - the default: there is no private gathering, and the guest is walked into the general evening by a named person. It is also the only rung that cannot produce a tier.
  - It wins the ratio because near-zero effort only pays when what the rung buys is still non-zero, and here it usually is. Most of what a private room buys is a short, nameable set of conversations, and those can be made by walking up to people.
  - Done properly, it has its own mechanics in the reference file: a named companion, the introductions written down in advance, a stated exit time. Done lazily, it is a guest holding a drink at the edge of a room, which is worse than not inviting them.
  - **Promotion condition, keyed to Q3:** move up one rung when Q3 names something the room does that the general evening genuinely cannot - a discretion request a public room breaks, or a conversation that needs a fixed set of people and no others. "It would be nice for them to meet" is not that, and it is the answer this question exists to catch.
- **Host list + capped nominations per asking party** - the organizer builds the list, and each asking party gets the same stated allowance. Second on both value axes and second on effort, it wins the ratio over host-only because the asks arrive whether or not you have a rule for them.
  - The cap is the cheapest artifact that turns every ask into one answer, and it costs one number and one sentence over building the list alone.
  - Published event-planning guidance for exactly this scenario states the same mechanic: agree a funding party's allocation as a number before any money changes hands, since "you have 20 spots" is a different conversation than "who would you like to invite."
  - **Promotion condition, keyed to Q5:** this is the rung whenever Q5 names more than one party already asking for seats.
- **Host-nominated only** - the organizer builds the list and accepts no nominations. Tops the room-is-right axis, because nobody knows the must-have names better than the host and every seat given to a nomination is a seat the host did not allocate.
  - It sits third on efficiency because its saving is real, and the grievance it generates lands precisely on the relationships the room was meant to serve.
  - **Promotion condition, keyed to Q5:** this is the rung when Q5 finds no asking party at all - a cap nobody is asking against is an artifact built for nothing.
- **Open nomination with published criteria and a host veto** - the starved rung: top of effort, top of compliance cost, top of the defensibility axis, and efficiency never picks it. It also loses the room-is-right axis to every rung above the fold, because it selects on who applied rather than on who had to be there.
  - **Promotion condition, keyed to Q8:** promote it when Q8 says the gathering was already published or sold in an artifact people can read. Once something is promised in a document, an unpublished rule is the shape a complaint takes, and criteria stop being optional.
  - Seniority never promotes this rung, and neither does the size of a cheque.
- **Deleted when Q6 says the seat count was set by the venue or the budget rather than by the conversation: the open-nomination rung.** Delete it from this menu and from the axis lines above. Publishing criteria against a number you do not control is a promise you cannot keep, and it converts a capacity limit into a broken commitment.
- **Deleted when Q2 says a flat, explicitly anti-hierarchy register and Q3 names no obligation the general evening breaks: every rung except the fold.** Delete them from this menu and from the axis lines above.
  - Evaluate both halves separately: Q2 alone leaves a discretion obligation unmet, and Q3 alone at the vendor pole deletes nothing.
  - Where both hold, a private room at an event whose identity refuses tiers is the tier with a door on it - parked at the bottom of a menu, it returns next planning cycle as a proposal.

## Menu B - invitation and access mechanics

How the invitation goes out and how the door is worked. This menu decides whether _the gathering_ is legible; `samber/dev-event-organizer-skills@event-vip-management`'s visibility menu decides whether _the guest_ is.

Do not re-rank that one here, but decide the two together, because a published room makes a guest list a public tier even when every badge is identical.

- effort (production and print deadlines, distribution, the questions it generates, a person on a door): `shared credential > published listing with an invited-guests label > named door list > verbal invitation only`
- value, the door works (the right people get in and nobody else does): `named door list > shared credential > published listing > verbal invitation only`
- value, it does not read as a tier: `verbal invitation only > named door list > shared credential > published listing`
- efficiency: `named door list > verbal invitation only > shared credential > published listing`

**Dominance check: four rungs, six pairs, two genuine strict dominance relations - this menu is clean by care, and it is the only one of the three that could have failed.**

The named door list beats the shared credential on both value axes at lower effort, and beats the published listing the same way. The efficiency line honours both.

Of the remaining four pairs, three are blocked because the value axes run opposite:

- Shared credential against verbal invitation only.
- Published listing against verbal invitation only.
- Named door list against verbal invitation only.

One pair, shared credential against published listing, is blocked by cost instead: the credential wins both value axes while costing more.

In the named-list-against-verbal pair, the named list owns the door and verbal owns discretion, so only the efficiency ratio orders them.

No compliance-cost axis is printed, and the skip is argued: rung for rung it would reproduce the does-not-read-as-a-tier ordering exactly, adding a line and no information. What it would have carried is the asymmetry, and that belongs in the rungs themselves - a credential can be dropped next edition, and a room printed in the programme cannot be unpublished.

- **Named door list** - the default. One person holds one page of names at the door. The invitation went out individually and privately from that same person.
  - Publicly there is a closed door and somebody standing at it, and nothing else is legible.
  - It wins its menu outright: it is the only rung where the door actually works, and it is second on discretion behind doing nothing.
  - A professional association's own exhibitor policy states the same discipline as a rule rather than a preference: hospitality-suite access is invitation only from the event holder, and the organizer's own attendee list may never be used to promote the room.
  - Costs one person for the length of the gathering and one printed page. The page, the what-to-say lines, and what happens to a name that is not on it are in the reference file.
- **Verbal invitation only** - no list, no door, no artifact. Tops the discretion axis and sits second on efficiency: near-zero effort, and nothing exists that could leak. Its cost is that the door, if there is one, is worked on recognition, which is the worst possible admission rule - the one that turns away exactly the person nobody on your team happens to know.
  - **Promotion condition, keyed to Q5:** it holds whenever Q5 finds no asking party. With no competing asks, there is nobody a list has to be defensible against.
- **Shared credential** - a wristband, token or badge marker that admits its holder. A starved rung, strictly dominated by the named list: more effort, a worse door once one is lent or copied, and a visible object that attendees read as a rank while it is worn through the general event.
  - **Promotion condition, keyed to Q7:** promote it only when Q7 says nobody from your team will be on that door, because the gathering runs in a space somebody else staffs. A list they cannot read is not a door. A credential is the only thing a venue's own staff can check.
- **Published listing with an invited-guests label** - the room appears in the schedule, marked as invitation-only. The other starved rung, dominated by the named list and last on efficiency: it announces the room to everybody, controls nobody, and generates a stream of requests you then have to refuse.
  - **Promotion condition, keyed to Q8:** promote it when Q8 says the room is already published in an artifact people can read. At that point the listing is not a choice you are making - it is a description of what already happened, and the remaining work is the wording rather than the decision.
- **Deleted when Q3 names any guest who asked not to be identified, listed or photographed: the shared credential and the published listing.** Delete both from this menu and from the axis lines above. A credential worn through the public event and a room named in the programme each publish exactly what that guest asked you not to publish, and no wording fixes either.

## Menu C - placement against the public programme

When and where the room sits. Three rungs, because the fold is Menu A's decision and does not reappear here.

- effort (a second venue, transport, a headcount fixed before anyone travels, a room booking, an owner's evening): `a separate evening at a separate venue > after the last session, in a room at the main venue > inside an existing break or meal slot, in a side room`
- value, the conversation actually happens (people arrive, stay, and talk without a clock running): `a separate evening at a separate venue > after the last session > inside an existing break`
- efficiency: `inside an existing break > after the last session > a separate evening at a separate venue`

**Dominance check: three rungs, three pairs, zero strict dominance relations - and one mechanism, a cost trade, accounts for all three.** The value axis runs rank-identical to effort - more effort buys a deeper conversation - so every pair resolves the same way: the busier rung wins on conversation depth and loses on effort. That is the "blocked by cost rather than by opposition" category Menu A uses for its two cost-trade pairs, not two independent goods in tension.

Whether the guest's absence goes unnoticed is not a second, independent axis here. It runs exactly rank-identical to inverse effort. Printed beside conversation depth, it would make the zero-dominance result read as two goods disagreeing when it is one axis and its own mirror image, forcing the efficiency line to cheapest-first for a reason that looks like evidence and is not.

The conversation-depth axis stays printed because it carries each rung's actual argument, even though it does no dominance work on its own: it agrees with effort by construction. The efficiency line rests on the arguments below.

No compliance-cost axis, and the skip is argued: where the room sits triggers no review that where it sits changes. The reviews this subject does trigger attach to the list and to the door, and they are on Menu A and in the reference file.

- **Inside an existing break or meal slot, in a side room** - the default. It wins the ratio the way Menu A's fold does: near-zero incremental effort only pays when the conversation depth bought is still non-zero, and a short slot still buys a real one because the room and the people are already there. Its real limit is depth: a break ends whether the conversation did or not.
  - **Promotion condition, keyed to Q3:** move up one rung when Q3 says the room's purpose is a conversation among a named set of people rather than a greeting - a break holds a greeting and does not hold a conversation.
- **After the last session, in a room at the main venue** - second on the value axis and second on effort, so it never wins the ratio outright, and it is the rung most events that need a real room should land on. It buys a conversation with no clock while keeping everybody in one building. It has one specific failure, and it is the one to watch: scheduled against the general evening it turns that evening into the consolation room, which is the tier arrived at by calendar.
  - Real event-production practice runs the same logic at the level of the whole evening calendar, not just this one room: a named event producer sequences a multi-evening conference by audience rather than by venue - a first-timers night, an executive/VIP night and a general-admission night, each on its own evening rather than competing for the same one.
- **A separate evening at a separate venue** - the starved rung: top of effort, top of the conversation axis, and efficiency never picks it. Two promotion conditions apply, each evaluated on its own rather than as one trigger.
  - **Keyed to Q4:** promote when Q4 names a guest window that no slot inside the event's own day fits - at that point the choice is this rung or nothing.
  - **Keyed to Q9:** promote when Q9 says the venue has no side room that is not read as a room. This is an absent asset, not a preference, and the one case where offsite is the only place a private gathering can physically be.
  - Before committing to any offsite option, document its hard operating constraints - fixed capacity, an off-peak-only availability window, a surcharge for something the venue does not normally do - rather than stopping at "vendor contacted." A dealbreaker found after the invitation went out costs far more than the same finding at comparison time.
- **Deleted when Q7 says the named owner is also running the main event that day: the separate evening at a separate venue.** Delete it from this menu and from the axis lines above. A second venue with transport and a fixed headcount is a job, and a job with no free owner becomes the organizer's on the day, on top of running the event - which is the failure that takes the main event down with it.

## Failure modes

- **The private room scheduled opposite the general evening.** Everybody can see which room the interesting people went to, and the general evening becomes the consolation prize. If both exist, they do not overlap. A documented conference reception lost much of its expected crowd for the mirror-image reason: the session before it ended an hour before the reception opened, and attendees left the building rather than wait out the gap. The mechanism draining the room is the scheduling seam itself, not something specific to a private gathering.
- **Building a list for a room nobody could say the purpose of.** Q3's second half exists for this, and the honest answer is usually the fold.
- **Rationing seats that were sold.** A gathering promised in a signed agreement is a deliverable, and applying your allocation rule to it is a breach dressed as fairness. Route it to `samber/dev-event-organizer-skills@event-sponsor-fulfillment` and take it off the list.
- **Letting the seat count pick the list.** Capacity is a constraint, never a criterion. When the room is smaller than the purpose, shrink the purpose deliberately rather than letting the venue decide who mattered.
- **The invitation issued by somebody who does not hold the list.** The most common way a room gets over-promised, and the most expensive to fix, because an accepted invitation cannot be quietly withdrawn.
- **The credential that walks out into the general event.** A wristband worn for the rest of the day is a visible tier you did not decide to build, and it is legible to every attendee who did not get one.
- **Re-deciding whether the guest qualifies.** That test belongs to `samber/dev-event-organizer-skills@event-vip-management`, it is stated as an obligation rather than a title, and re-running it here produces two owners for one judgment.
- **The list that outlives the event.** A seat list carrying dietary answers and quoted requirements is a named-person record. The deletion date is set when the list is created, by name, in the same pass.
- **Refusing without a rule.** A refusal with nothing behind it reads as a judgment about the person nominated, which is the version that damages a relationship over a seat nobody would have remembered.
- **The gathering read as a sponsor-arranged meeting.** A speaker-and-partner dinner meant as informal networking is one small step from looking like a transaction the moment attendees suspect seats were sold for access. State the distinction in writing to whoever is invited and whoever asked for seats: this room is a relationship, not a meeting arranged on a sponsor's behalf.

## Measurement

No industry standard exists to calibrate these four signals against. Set your own targets before the event, and never adjust them after the data arrives.

- **Every asking party got an answer, and the same rule was cited to each (binary).** Check the list's nomination field against the parties Q5 named. A party with no recorded answer is the finding.
- **Discretion held (binary).** Zero guests who asked not to be identified were identifiable to a general attendee as having been in the room. Any published photograph, listing or credential bearing on one of them fails this outright.
- **Seats promised versus seats that existed (binary).** Zero invitations issued beyond what the room held. A single over-promise means the invitation went out from somebody who was not holding the list.
- **List deletion (binary).** The seat list is gone by its stated date, confirmed by the named owner.

## Invocation examples

- "Two sponsors and a keynote speaker have each asked us to add someone to the founders' lunch. How do we decide, and how do we say no to the others?"
- "We want a small room where our grant officer can actually talk to three people. When do we put it, and do we tell anyone it exists?"
- "Marketing wants an invite-only reception listed in the programme. Our conference is explicitly flat. What do I do?"
- "Someone on my team already told a sponsor yes and the room seats fewer than we've now invited."

Expected output: a gathering brief containing:

1. What the room does that the general evening cannot, or the finding that nothing survives that question.
2. The seat-list construction rule with its cap or criteria.
3. The list itself, with its fields, named owner, circulation and deletion date.
4. The invitation and access mechanics with the door page.
5. The placement, with the slot handed to the run of show.
6. The refusal rule, written before the first ask.
7. The handoffs.

Presented section by section for approval. Where Menu A lands on the fold, the output is that finding plus the fold's own mechanics, and nothing else.
