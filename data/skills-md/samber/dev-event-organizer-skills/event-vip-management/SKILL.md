---
name: event-vip-management
description: Receive named guests who are neither speaking nor sponsoring but whose presence creates escort, protocol, security or discretion obligations the general attendee flow cannot absorb - public officials, dignitaries, major funders, executives with no booth duty. Covers the qualification test (obligation, never status), the identification roster, escort depth, and a visibility posture that meets the obligation without building a status tier attendees can read. Use whenever the user mentions receiving a minister, mayor, funder or visiting executive, VIP badges or reserved seating, escorting a dignitary, or coordinating with a guest's own security detail - even if they never say "VIP". Do NOT use for speakers - use samber/dev-event-organizer-skills@event-speaker-experience instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event VIP Management

You receive a named guest whose visit creates an obligation your general attendee flow cannot absorb, and you do it without building a tier the room can see. Those are two jobs, and the second one is the hard one.

Two illustrative shapes:

- A minister arrives with a protective detail whose requirements you did not write and cannot refuse.
- A funder your event depends on arrives alone and would rather nobody noticed.

Both are yours. Neither is a reason to print a different badge.

The qualifying fact is an **obligation, never a title**. A guest qualifies when their presence imposes something the door, the queue and the help desk cannot handle as they stand: an escort, a protocol requirement, a security constraint, a discretion request. Prominence alone qualifies nobody, and the most common correct outcome of this skill's interview is that nobody is left in scope.

## Four siblings own most of what people call a VIP

Route these out at the interview, before anything else. Some of these boundaries are agreed from both sides, others are written from here only.

- **On the program → not yours.** `samber/dev-event-organizer-skills@event-speaker-experience` takes every speaker from acceptance to thank-you, however senior, and its speaker-care menu already carries a rung that books travel and lodging rather than reimbursing, promoted for the international or visa-dependent traveller. A second owner for one relationship is how a commitment gets dropped between two runbooks.
- **Covered by a signed sponsorship → not yours.** `samber/dev-event-organizer-skills@event-sponsor-fulfillment` delivers every promised perk against the agreement and gates each on payment. A sponsor's executive on the clock at their booth is theirs. You start only where a guest's presence is covered by no agreement at all: a sponsor CEO attending purely as a guest, with no booth duty. That edge is written from this side only; fulfillment never mentions it.
- **Here to file copy → not yours.** `samber/dev-event-organizer-skills@event-press-relations` claims accreditation, embargoes and on-site press handling, and states that boundary from its own side as well. You own only a _guest's own exposure_ to press: declining a photograph on their behalf, keeping a departure time off the schedule.
- **A general attendee → not yours.** `samber/dev-event-organizer-skills@event-attendee-experience` designs the door, the queue and the help path, and names you from its side: "a VIP is a separate protocol track, never the top rung of this journey." You never upgrade an attendee into this skill; you route a guest out of it.

You add only the guest-specific layer on top of the shared floor `samber/dev-event-organizer-skills@event-hospitality` sets. That skill ships and decides:

- The catering service style.
- What a scheduled break contains.
- The alcohol posture.
- Whether an evening programme exists.

It names this boundary from its own side, delivering the floor and never re-deciding "a speakers' dinner, a volunteer meal or a VIP table". A guest's table is therefore yours; the food on it is not. Route the user there when the real question is a hospitality question, and do not restate one of its four decisions here.

All four menus below are this skill's own construction. Their rungs, axis orderings, defaults, promotion conditions, and delete rules are argued here, not drawn from a published standard or measured against event data.

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank all four menus against what you know. Each of these overturns a default rung, and the list is not closed:

- An organizer who already knows the guest personally.
- A venue with a second entrance.
- A team member with government or protocol experience.
- An institutional relationship already years old.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-8 exist because the menus below diverge sharply on visibility, time-to-effect and effort - those defaults cannot be picked for the user.

1. Which mode: set a posture before an edition, or handle one named guest already confirmed for a date?
2. Who owns the event and which pole is it on - community-run (volunteer, CFP-driven, cost-recovery sponsors) or vendor/corporate-run (marketing-funded)? And does its register say anything about status: flat and explicitly anti-hierarchy, or comfortable recognizing who is in the room? _(This one answer flips Menu B end to end.)_
3. Name each guest and say what makes them a guest rather than something else. Anyone on the program is a speaker; anyone covered by a signed sponsorship is a sponsor; anyone filing copy is press - route each out. For whoever is left: what obligation do they carry, in one sentence, and is there one at all, or only status?
4. Does any guest arrive with obligations you do not control: a protective detail, a protocol or advance officer, a stated institutional security requirement, a fixed arrival or departure window? Has their office actually contacted you, or are you assuming they will?
5. Has the guest or their office said how _visible_ they want to be: introduced, or moving through the day unremarked? Never infer this. Both answers are common, and this is the fact that decides the whole visibility posture.
6. How long until doors, and are the badge print run, the seating plan and the run of show still open? _(A closed print run deletes every badge-marking rung on its own, without any argument about culture.)_
7. Is this a one-off visit, or a relationship that recurs edition after edition?
8. What is the effort ceiling: organizer-hours, how many people can be pulled off another post on the day, and who is willing to own this? Note that reversibility is not symmetric here: a badge colour can be dropped next edition; a stage announcement and a published photograph cannot be unsaid.
9. How many named guests in total, who compiles the list, who else sees it, and on what date is it deleted? Which assets re-rank the defaults: an organizer who already knows the guest, a venue with a second entrance, a team member with protocol experience?

## Community vs vendor pole

Who owns the event, and what it is for, flips a whole menu. Sibling skills in this collection argue the same split.

- **Community pole.** Status is the thing the event is trying not to reproduce. A visible tier is not merely expensive; it contradicts the register `samber/dev-event-organizer-skills@event-cultural-identity` set. The obligation still has to be met - it just has to be met invisibly.
- **Vendor/corporate pole.** Visible recognition is frequently the deliverable. An investor, a parent-company executive or a strategic customer's CIO is often attending _because_ the visit will be acknowledged, and refusing to acknowledge it fails the guest rather than protecting the culture.

Say which pole a recommendation assumes whenever they differ. Menu B is the only one of the four where they genuinely diverge; A, C and D hold their order across both.

## Workflow

1. Run the interview. Route out speakers, sponsor personnel and press first. If nobody remains in scope, say so and stop - that is a correct result, not a failed one.
2. Apply the qualification test to whoever remains: obligation, not status. The test, its four qualifying obligation types, and the worked pass/fail pairs are in [references/guest-qualification-and-roster.md](references/guest-qualification-and-roster.md).
3. Set the identification breadth (Menu D), then build the roster: its fields, its named holder, who else sees it, and its deletion date - decided now, not after the event. Same reference.
4. Set the program posture (Menu A).
5. Set the visibility posture (Menu B) against the pole (Q2) and against what the guest actually said (Q5). Where there is still time, ask rather than decide; a guest who has not been asked is a guess, not a preference.
6. Set the escort depth (Menu C) and write the greeter brief. Template, the what-not-to-say list, and the discretion mechanics for each Menu B rung are in [references/discretion-and-escort-mechanics.md](references/discretion-and-escort-mechanics.md).
7. Where a guest arrives with their own detail or advance team, run the liaison intake in that same reference:
   - Receive their requirements.
   - State in writing what the venue can and cannot do.
   - Name one counterpart.
   - Confirm they are bound by the code of conduct like any other third party in the building.

   `samber/dev-event-organizer-skills@event-code-of-conduct` names contractors and press in its scope clause; somebody else's security staff is the same shape, and the clause wording is theirs, not yours.

8. Write down the two decisions the day will test, with a name against each: who decides on the spot when a photograph is requested, and who says no on the guest's behalf. Name someone in advance, or whoever is standing there decides both under time pressure.
9. Hand off what is not yours:
   - Seating against the grid, to `samber/dev-event-organizer-skills@event-schedule-design` and `samber/dev-event-organizer-skills@event-run-of-show`.
   - Anything touching the general check-in desk, to `samber/dev-event-organizer-skills@event-attendee-experience`.
   - Any access need, to `samber/dev-event-organizer-skills@event-accessibility-inclusion`, because a guest with an access need is an access question first and a guest question second.
   - Anything that has become a crowd, medical or credible-threat question, to `samber/dev-event-organizer-skills@event-risk-management`.
10. Present section by section - qualification, roster, posture, visibility, escort - and get explicit approval per section before finalizing.

If your harness has persistent memory, record per edition:

- Which guests qualified and on which obligation.
- What each one's office actually asked for.
- What you refused and why.
- Whether the roster was deleted on its date.
- Whether any attendee noticed a difference in treatment.

Next edition starts from that instead of re-deriving a posture for the same guest.

## Menu A - program posture

How much apparatus exists at all, before any specific guest arrives.

- effort (organizer-hours, standing ownership, documentation, briefing): `formal named program with dedicated staff > defined criteria + protocol runbook > ad hoc invisible accommodation > no posture`
- value (every obligation met with no failure at the door): `formal named program > defined criteria + runbook > ad hoc invisible accommodation > no posture`
- compliance cost (review triggered, reversibility spent): `formal named program > defined criteria + runbook == ad hoc invisible accommodation > no posture`
- efficiency: `ad hoc invisible accommodation > defined criteria + runbook > formal named program > no posture`

**Value and effort run in the same order on this menu.** No rung offers more value at less effort, so zero dominance relations exist and the strict-dominance check cannot find anything. This menu is clean **by construction, not by care**, and that is not a pass: the efficiency line rests entirely on each rung's own argument below.

Compliance cost is the one axis that departs from that order, and its `==` is argued. The runbook triggers a data-handling review that ad hoc skips; ad hoc spends the reversibility the runbook keeps, because an undocumented list of names in one organizer's messages has no stated holder, no deletion date, and no way to confirm it is gone. Equal exposure, opposite halves.

- **Ad hoc invisible accommodation** - the default. One organizer quietly handles whatever a specific guest needs; nothing is written, nothing is announced, nothing is repeatable. It wins on ratio because the common case is one or two guests a year and the whole obligation is met by one person paying attention. Move up one rung when Q7 says the relationship recurs _and_ Q9 puts more than a handful of names on the list - past that, the arrangement lives in one person's head and leaves with them.
- **Defined criteria + protocol runbook** - documented qualifying triggers, a named owner, a repeatable sequence, and a roster with a deletion date. The promotion target for a recurring institutional relationship.
- **Formal named program with dedicated staff** - the starved rung: top of value, top of effort, top of compliance cost, so efficiency never picks it. Promotion condition: Q4 says a guest arrives with a protective detail or advance team _and_ Q7 says this recurs - at that point you are the standing counterpart to somebody else's standing process, and improvising against it each edition is the actual risk.
- **No posture** - every guest absorbed into the general, speaker or sponsor flow, unchanged. It sits last on efficiency for the same reason `samber/dev-event-organizer-skills@event-cultural-identity` puts "no deliberate ritual" last: near-zero effort buying nothing on the axis being measured is a ratio of zero, and by the time this skill is running, a qualifying guest already exists.

  **Promote no posture to first outright when Q3 finds status without obligation**: the guest is prominent, arrives alone, brings no detail, states no requirement. Every rung above it then manufactures a tier for nothing. That promotion is not a courtesy, and at the community pole it is the most common right answer.

- **Deleted when Q2 says a flat, explicitly anti-hierarchy register and Q4 finds no external obligation: the formal named program.** Delete it from this menu and from the axis lines above. A standing VIP program at an event whose stated identity refuses status is not an expensive option to defer - it is a contradiction that will be read as one, and parked at the bottom it comes back next planning cycle as a proposal.

## Menu B - visibility and discretion posture

What the handling _shows_. This is the menu carrying the cultural tension, and the only one whose value ordering flips by pole.

- effort (coordination, rehearsal, print deadlines, run-of-show reopened): `public marker + recognition moment > visible marker > staff-only signal > invisible handling`
- value at the **community pole** (obligation met without contradicting a flat-status register): `staff-only signal > invisible handling > visible marker > public marker + recognition moment`
- value at the **vendor/corporate pole** (the acknowledgement is itself what the guest came for): `public marker + recognition moment > visible marker > staff-only signal > invisible handling`
- efficiency, community pole: `staff-only signal > invisible handling > visible marker > public marker + recognition moment`
- efficiency, vendor/corporate pole: `visible marker > staff-only signal > public marker + recognition moment > invisible handling`

**Dominance check, community pole - clean by care.** Value and effort run opposite, so five dominance relations exist and each one could have been violated:

- Staff-only signal over visible marker and over public recognition (more value, less effort in both pairs).
- Invisible handling over visible marker and over public recognition (same shape).
- Visible marker over public recognition.

The community-pole efficiency line honours all five. Only staff-only signal against invisible handling is unconstrained - value favours the first, effort the second - and it is decided by ratio below, not by dominance.

**Dominance check, vendor/corporate pole - clean by construction.** At this pole value and effort run in the same order, so there are no dominance relations at all and the check finds nothing. The pole flip converts this menu from checkable to unfalsifiable, and the vendor-pole efficiency line rests on its own argument alone.

No compliance-cost axis is printed here, and the skip is argued: rung for rung it would reproduce the effort ordering exactly, adding a line and no information. What it would have carried is the reversibility asymmetry, and that belongs in the rungs themselves: a badge colour can be swapped between sessions, and a stage announcement and a published photograph cannot be unsaid.

- **Invisible handling** - the guest carries the same badge, uses the same door, is not seated apart, and the arrangements are known to the one organizer handling them. Nothing about them is legible to any attendee, at near-zero effort. At the community pole it sits second only because it cannot brief anybody: the door lead who does not know a guest is coming cannot act when they arrive. At the vendor pole it sits last on efficiency - near-zero effort delivering nothing the guest came for is the same ratio of zero.
- **Staff-only signal** - the community-pole default, and the whole recommendation for most events this skill will ever run for. Identical public surface to invisible handling: no marker, no reserved row, no announcement. What it adds is internal - the door lead, the room leads and the code-of-conduct responders know who is in the room and what was agreed. The marginal cost over invisible handling is one briefing and one message; it buys the entire obligation. That is why it leads its pole despite costing more.
- **Visible marker** - a badge colour, ribbon, lanyard or reserved row that attendees can read as a tier. It leads the vendor-pole efficiency line, on one argument and no more: a reserved seat next to the person the guest came to meet costs an afternoon and delivers most of what a stage moment delivers. Promotion condition at the community pole: Q5 says the guest's office explicitly asked to be identifiable, _and_ Q6 confirms the print run is still open. Nothing else promotes it - not seniority, not the size of a cheque.
- **Public marker + recognition moment** - announced arrival, acknowledgement from the stage, a photograph. The starved rung on both poles: top of effort everywhere, top of value only at the vendor pole, and it still loses that pole's ratio round to the visible marker. Promotion condition: Q2 says vendor pole _and_ Q5 says the guest's office asked for it in as many words. A recognition moment nobody requested is a risk dressed as a courtesy - some guests' security posture forbids advance publication of their movements, and consent to a photograph is not implied by attendance.
- **Deleted when Q6 says the badge print run and the seating plan are closed: both marker rungs.** Delete them from this menu and from the axis lines above. A hand-written addition to a printed badge is more legible as a tier than a designed one, not less.

**Interaction with Menu D, and it runs one way:** widening the identification list pushes this menu toward its costlier, more visible rungs. Four obligation-carrying guests can be held in one organizer's head and briefed by one message. Forty cannot, so they need a marker somebody can read at a glance, which is a visible tier arrived at by logistics rather than by decision. If this menu's outcome is a visible marker and nobody ever chose one, check Menu D first.

## Menu C - escort depth

How much of an organizer's day a guest gets, and at which moments.

- effort (organizer-hours, a person pulled off another post, briefing, coordination): `escort + protocol/security liaison > dedicated escort for the visit > named greeter for arrival only > printed contact card`
- value (obligation met, needs anticipated, no incident): `escort + liaison > dedicated escort > named greeter > printed contact card`
- efficiency: `named greeter for arrival only > printed contact card > dedicated escort for the visit > escort + liaison`

**Value and effort run in the same order here too: zero dominance relations, clean by construction, not a pass.** The efficiency line rests on each rung's argument.

No compliance-cost axis, and the skip is argued: exactly one rung carries a review - the liaison rung - and that review is not yours to run. It belongs to the guest's own institution, which arrives with it already done. A four-rung axis with one non-zero entry is not an ordering.

- **Named greeter for arrival only** - the default. One person meets the guest at the door, walks them in, points at the room and the coffee, and hands over a way to reach them. Arrival is where the entire failure lives: a guest who gets past the door knowing where they are and who to ask has had their obligation met, and the rest of the day is a conference. Costs one person for twenty minutes. Move up one rung when Q4 names a fixed departure window or a route the guest cannot navigate alone.
- **Printed contact card** - a named contact and a number, nothing else. Second on efficiency: near-zero effort, and it buys the one thing that matters when something goes wrong. It is the honest floor for most guests this skill will ever see, and it stays the fallback whenever nobody can be spared on the day.
- **Dedicated escort for the visit** - one person assigned to the guest for the duration. Buys anticipation rather than reaction. Costs a whole person for a whole day, which at most community events means a post left unstaffed elsewhere.
- **Escort + protocol/security liaison** - the starved rung: top of value, top of effort, and efficiency never picks it. Promotion condition: Q4 says the guest arrives with a protective detail, a protocol officer or an advance team. At that point you are not choosing an escort depth at all - you are the counterpart to somebody else's plan, and the liaison exists to _receive_ their requirements, not to confer status. Seniority never promotes this rung, at any level.
- **Deleted when Q5 says the guest asked to move through the day unremarked and Q2 says a flat register: the dedicated full-visit escort.** Delete it from this menu and from the axis lines above. A person visibly shadowing one attendee all day is a status marker regardless of what the badges say - it is the Menu B decision made by accident, in the one direction that menu was built to avoid.

## Menu D - identification breadth

Who goes on the list at all.

- effort (screening, triage, maintenance, and the arguments about who qualifies): `broad notability list > obligation + relationship list > obligation-only list > no defined list`
- value (real obligations caught before doors; nobody arrives unrecognized): `broad notability list > obligation + relationship list > obligation-only list > no defined list`
- compliance cost (review triggered, reversibility spent): `broad notability list > obligation + relationship list > obligation-only list == no defined list`
- efficiency: `obligation-only list > obligation + relationship list > no defined list > broad notability list`

**Value and effort run in the same order again: zero dominance relations, clean by construction, not a pass.** Three of this skill's four menus are in that position; only Menu B's community pole is genuinely checkable. Say so to the user if they ask why the orderings look mechanical: they are not derived, they are argued.

The compliance axis is the one that differentiates, and its `==` is argued. No defined list creates no artifact to review, and it leaves an organizer improvising at the door about which named individuals get different treatment, with no criteria and no record of why. An unreviewable decision is not a low-exposure one; it is an unauditable one.

The obligation-only list creates a small named-person record that triggers exactly one retention decision and is defensible line by line, because every entry is there for a reason the guest's own institution stated. Equal exposure, opposite shapes.

- **Obligation-only list** - the default: anyone arriving with a protective detail, a protocol or advance officer, an institutional security requirement, or an explicit discretion request. Nobody qualifies on title. It is the shortest list that catches every case this skill exists for, and it is the only rung where each name's justification came from outside your own judgment.
- **Obligation + relationship list** - adds major funders, board members and executives of organizations the event depends on. Promotion condition: Q7 says the relationship recurs across editions _and_ Q3 names someone whose visit is itself a deliverable to that relationship. Not "we should probably be nice to them."
- **No defined list** - decide case by case as each guest surfaces. Third on efficiency, above the broad list: it costs nothing and it does not manufacture a tier, but it makes every judgment at the door under time pressure.
- **Broad notability list** - the starved rung, and starved for a reason worth stating: it tops effort _and_ compliance cost, its extra names are judgments about people who never asked to be assessed, and it is the rung that generates the visible tier Menu B exists to avoid. Promotion condition: essentially none at a technical conference. If a user wants it, ask which specific obligation each additional name carries, and watch the list collapse back to the obligation-only rung.
- **Deleted when Q2 says a flat, explicitly anti-hierarchy register: the broad notability list.** Delete it from this menu and from the axis lines above. A written roster of "notable" attendees at an event whose identity refuses hierarchy is the tier, in document form, before anyone reaches the door.

## Failure modes

These eight are this skill's own construction, not an incident record.

- **Building the tier the guest never asked for.** The most common failure, and it usually comes from courtesy rather than vanity. Fix: Q5, asked of the guest's own office, before any marker is designed.
- **Reading a title as an obligation.** A senior person who arrives alone, unescorted, with no stated requirement is an attendee with an impressive job. Fix: the qualification test in the reference - name the obligation in one sentence or route them to the general flow.
- **Making the escort the marker.** One route to a tier nobody decided on: invisible handling on Menu B plus a dedicated full-visit escort on Menu C produces a visible tier anyway. The two menus are decided together.
- **Re-owning a speaker.** A prominent speaker's care already has an owner and a promoted rung there. Two runbooks over one relationship drop commitments in the seam.
- **Running press instead of the guest's exposure to it.** Accreditation, embargoes and the press room are somebody else's. Yours is whether this guest is photographed, and who says no on their behalf.
- **The roster that outlives the event.** A list of named individuals with a reason attached to each, sitting in a shared drive with no deletion date, is the artifact hardest to justify and easiest to forget. Fix: the date is set when the roster is created, by name, in the same pass.
- **Treating a guest's own detail as outside the code of conduct.** They are a third party in your venue like a contractor or a photographer, and the scope clause is where that gets stated.
- **Choosing a visible marker because it is the cheapest way to brief a large door team.** The second route to that same tier, arriving through Menu D's breadth rather than through escort depth. Shorten the list instead of marking it.

## Measurement

All four signals are this skill's own construction; none is a benchmark, and no published figure exists to calibrate any of them against. Fix each target before the event, never after the data arrives.

- **Obligation met, per guest (binary).** Every requirement the guest's office stated was either met, or refused in writing in advance. Pass threshold: zero requirements first discovered at the door.
- **Tier visibility (self-set).** After the event, ask two attendees who were near the guest whether they noticed anyone being treated differently. At a flat-register event, any "yes" is a finding worth acting on, not a rounding error.
- **Image consent (binary).** Zero published images the guest did not agree to. This one is checkable and there is no excuse for failing it.
- **Roster deletion (binary).** The roster is gone by its stated date, confirmed by the named holder.

## Invocation examples

- "The deputy mayor is opening our community conference and her office just emailed about her security team. What do we actually have to do?"
- "Our biggest funder is coming as a normal attendee. Do we give her a different badge? She hasn't asked for anything."
- "We're a vendor running our user conference and three customer CIOs are attending. Marketing wants them recognized from the stage."
- "Someone proposed a VIP lounge for next edition. Our whole identity is that we don't do tiers. Talk me out of it or into it."

Expected output: a guest brief containing:

1. The qualification result per named person, including everyone routed out and to which skill.
2. The identification breadth with the roster's fields, holder, viewers and deletion date.
3. The program posture.
4. The visibility posture with the pole it assumes and what the guest actually said.
5. The escort depth and the greeter brief.
6. The two named day-of decisions.
7. The handoffs.

Presented section by section for approval. Where nobody qualifies, the output is that finding and nothing else.
