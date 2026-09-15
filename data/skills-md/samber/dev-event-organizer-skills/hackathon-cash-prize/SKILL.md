---
name: hackathon-cash-prize
description: Structure what a hackathon actually awards - cash versus non-cash medium including no monetary prize at all, total pool size inside the event budget's prizes line, how that pool splits across places and sponsor tracks, and who may legally receive a payout. Use whenever the user mentions hackathon prize amounts, cash versus hardware or credits, splitting a prize pool across tracks, prize eligibility for minors, sponsor employees or cross-border winners, or how winners actually get paid - even if they never say "prize". Names the contest-law, tax and cross-border exposure categories and routes them to counsel or a fiscal host, never stating a threshold or a form name. Do NOT use to rank the projects - use samber/dev-event-organizer-skills@hackathon-judging instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Hackathon Cash Prize

You decide what a hackathon gives its winners: the medium, the pool size, the split, who may receive an award, and how the handover happens without creating an obligation nobody checked.

Organizers ask about cash first. Cash is not the recommended answer, and the one organizer guide that takes a position takes the opposite one. Read the medium menu before assuming the user needs a number.

## What you own, and what is already decided

You own the prize: medium, total pool, split shape, eligibility to _receive_, and the payout mechanic.

- **The rank is not yours.** `samber/dev-event-organizer-skills@hackathon-judging` produces the ranked outcome per track and hands it to you. Turn a rank into an award. Never re-open a placement, and never let the size of a prize influence who won it.
- **The rules document is not yours.** `samber/dev-event-organizer-skills@hackathon-brief-design` owns the published brief, including eligibility to _compete_: who may enter, at what age, from where, in what employment. You own the narrower question of who may legally _receive_ an award once a rules-eligible team has won. Hand that text to the brief rather than drafting a rules document yourself.
  - Neither skill drew this split before this one existed. State it plainly when you present it, because a reader who has used the brief skill expects eligibility to live there.
- **The ceiling is not yours.** `samber/dev-event-organizer-skills@event-budget` sets the Prizes line inside the overall P&L. Propose a pool and a split that fit inside whatever that line carries.
  - Never invent a pool size independent of it. If that line does not exist yet, say so rather than sizing against nothing.
  - That skill names this one and describes the hand-off the same way, so you consume an agreed boundary rather than assert one.
- **A sponsor-funded prize is sold elsewhere and delivered elsewhere.** `samber/dev-event-organizer-skills@event-sponsor-pricing` prices the add-on that funds it; `samber/dev-event-organizer-skills@event-sponsor-fulfillment` delivers it as a tracked perk. You decide its shape - medium, split, eligibility - once the sponsorship is signed.
  - Neither of those skills names this one, and neither says anything about a competition prize: the fulfillment skill's only prize rung is the booth raffle below.
  - So you assert this boundary into empty space rather than repeat an agreement. Say so.
- **A raffle prize is not a competition prize.** A booth raffle is an attendee incentive open to any attendee, and it belongs to `samber/dev-event-organizer-skills@event-sponsor-fulfillment`. A competition prize is awarded on a judged rank. Both are sponsor-funded and both are called "prize", but the mechanics differ and so do the eligibility questions.

Every ranking below is a default, not a law. After the interview, re-rank each menu against what you know: a sponsor's credits already in hand, an organizer with no legal entity, a hardware event whose participants want components, a returning event whose last edition already published a prize structure.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-9 exist because the menus turn on them and no other question surfaces the facts they carry.

1. What does the Prizes line in the event budget carry, and has it been set at all? (Fixed input - you size inside it, you do not raise it.)
2. What track and place structure did the brief already publish, and did any of it promise a prize? Read the published rules before designing anything; a prize promised in writing is a commitment, not an option.
3. Which sponsors fund a prize, what did they buy, and is the funding cash, product credits, hardware, or an opportunity their own company controls?
4. Could any winner be a minor, and could any winner be outside the organizer's own country? Ask both explicitly - these two facts delete rungs from two menus and no other question surfaces them.
5. Does the organizing team have its own legal entity, or does it run under a school, a company, or a fiscal host? This decides who can even sign a payout, and how long money takes to move.
6. Are organizers, volunteers, mentors, judges or sponsor employees allowed to compete, and if so, may they win? These are two different permissions and most events conflate them.
7. Do you want the prize to buy attention before the event, or to reward the winners after it? A prize sized for marketing and a prize sized for the winners are different decisions with different failure modes.
8. What is the effort ceiling: organizer hours before the event, whether anyone will chase a winner for paperwork afterwards, and how reversible a mistake can afford to be?
9. By what date must the prize structure be published, and is this a one-off edition or a recurring event whose structure should still hold next year?

Q7 through Q9 move specific rungs. Name which as you re-rank.

- **A near publication date (Q9)** promotes the media that need no procurement lead time: recognition and credits first, cash only where the medium menu's delete conditions do not fire. It demotes gear, which the same menu's backorder warning puts furthest out.
- **An attention-before-the-event intent (Q7)** is the only thing that promotes a flagship pool. A reward-the-winners intent leaves it starved.
- **A one-off edition (Q9)** promotes the sponsor-funded pool, whose fundraising is already being done elsewhere. A recurring mandate promotes what is written once and reused, the standard-form payout text and the published eligibility paragraph, and it is what makes a counsel review worth its cost across editions rather than once.
- **A low effort ceiling (Q8)** deletes the flat-across-many-tracks split, whose entire cost is the per-winner check repeated.

## Workflow

1. Run the interview. Read the budget's Prizes line (Q1) and the published brief (Q2) first.
2. **Answer the medium question before the size question.** The medium decides which legal categories are even live, and half the sizing conversation disappears once the prize is not money. Load [references/prize-medium-catalog.md](references/prize-medium-catalog.md).
3. Size the pool inside the Prizes line, and separate the organizer's own baseline from the sponsor-funded part. They have different ceilings and different owners.
4. Choose the split shape against the track structure the brief already published, not against a blank page.
5. Write the eligibility-to-receive text and hand it to `samber/dev-event-organizer-skills@hackathon-brief-design` for the rules document. Load [references/eligibility-to-receive-text.md](references/eligibility-to-receive-text.md).
6. Pick the payout rigor rung, and name every exposure category the chosen medium and winner pool trigger. Route each one - never answer it. Load [references/payout-exposure-categories.md](references/payout-exposure-categories.md).
7. Publish the prize structure in the brief _before_ submissions close. A prize announced after teams have chosen what to build has already failed at motivating anything.
8. On the day, take the ranked outcome from `samber/dev-event-organizer-skills@hackathon-judging` and award against the published structure. Record what was actually handed over, to whom, and what remains outstanding.

Present the structure section by section for validation - medium, pool, split, eligibility, payout mechanic - before any of it reaches the published brief. Publication is the point of no return, because a published prize is a promise.

If your harness has persistent memory, record:

- the medium and why
- the pool and the ceiling it fit inside
- the split shape
- the eligibility carve-outs
- which exposure categories were routed to whom

## Prize medium

Five rungs:

1. **Cash**
2. **Gear**: hardware, components, tools a participant keeps.
3. **Credits and vouchers**: cloud or SaaS credits, gift cards, makerspace credit.
4. **Opportunity**: a conference ticket, a mentorship slot, an interview or investor introduction.
5. **Recognition only**: a trophy, a title, a public write-up, no transferable value.

The value axis here is counterintuitive. MLH's organizer guide frames the prize decision as behavioural rather than monetary: prizes "say a lot about who you are as a community, why you are there in the first place, and they influence the vibe of your event - big time." MLH states its own position on cash: "While cash prizes are easy for events, we do not recommend them. The perceived value of a cash prize is much lower than traditional prizes."

That claim's direction shifts the default order. It is one organizer's stated position, not a measured comparison of outcomes.

- value (what the winner perceives and what behaviour the prize rewards, per the framing above): `opportunity > gear > credits > cash > recognition only`
- effort (sourcing hours, procurement, coordination with a third party, chasing a winner afterwards): `opportunity > gear > credits > cash > recognition only`
- compliance cost, as the review each rung triggers and the reversibility it costs: `cash > credits > gear > opportunity > recognition only`
- efficiency: `gear > recognition only > credits > cash > opportunity`

Value and effort run in the same order across all five rungs. So no pair exists where one rung has value greater than or equal to another's and every cost less than or equal. Resist the temptation to manufacture a disagreement by calling cash the cheapest rung outright: cash is cheapest to _procure_ and dearest to _hand over_, which is why that cost sits on the compliance axis rather than the effort axis.

The compliance axis is what re-orders this menu, and it is why the default is neither the most valued rung nor the cheapest. Cash moves through a payment rail to a named individual, and that rail pulls in the tax, cross-border and minor-payout categories; a keyboard handed over at a table does not. Credits sit beside cash because a redeemable, resellable code carries monetary value without ever touching a bank.

That payment rail is documented practice, not a hypothesis. Devpost's own prize-claim process requires a cash winner to submit a tax-identification form before funds release, with a separate form for an international individual and another for an organization, and the platform states plainly that working out which one applies is each winner's own responsibility. General tax-compliance practice treats a gift card or voucher the same way it treats cash for reporting purposes, and values physical merchandise through a fair-market-value mechanism instead: the sourced reason credits sit beside cash on this axis rather than beside gear.

The opportunity rung's place on this axis rests on reasoning alone. It stays the menu's least confident cell, so name it as an open question when you present the ordering.

- **Gear - the default.** MLH's own recommended direction, and the one rung that pairs high perceived value with no payment rail. It costs real procurement hours and carries a known constraint: many items will be backordered, so order prizes early to have them in time. It also carries a unit-count consequence the other rungs do not, covered on the split menu.
- **Recognition only.** Neither a fallback nor a demotion. hackathon.guide's author runs events on this rung deliberately: "don't make winners and losers. Just don't. There has never been beer, competitions, or time pressure at my hackathons." That is a civic-tech organizer's own practice, so the rung is genuinely chosen, though it does not necessarily fit a competitive student event.
  - Support from a different angle: MLH, PennApps, Papers We Love and NASA Space Apps all lead their public positioning with learning, building and sharing rather than prize size. An event positioned that way and awarding recognition only reads as consistent, not cheap.
  - Promotion condition, keyed to Q7: the prize rewards the winners rather than buys attention, **or** Q5 says the team has no legal entity and no fiscal host, in which case this is the only rung that needs neither.
  - Favour a form that outlives the ceremony. A trophy passed from cohort to cohort, or a public acknowledgement from someone the winners will recognise, holds value longer than a certificate nobody keeps.
- **Credits and vouchers.** Cheap when a sponsor already holds them (Q3) and near-free to that sponsor, which is why they appear in sponsor-funded tracks more than anywhere else. They carry expiry dates, redemption regions and account requirements a winner can fail to satisfy months later. State the expiry in the published prize structure or you will hear about it.
- **Cash.** Cheapest to procure and top of the compliance axis, which is why efficiency ranks it fourth rather than first. **Delete it, from this menu and from the axis lines above, when Q4 says a winner could be a minor or outside the organizer's country, or Q5 says there is no legal entity and no fiscal host.** The machinery to pay it correctly does not exist yet in those cases, and a cash prize parked at the bottom of a menu quietly becomes the plan at the ceremony.
- **Opportunity - the starved option**: top of value, top of effort, so efficiency never picks it. MLH names this rung in its own catalogues: conference tickets, "Lunch with your hero", a company visit, and an introduction to present to a seed funder in its hardware guide.
  - Its legal treatment is unsettled: an award that functions as a job or investment introduction plausibly intersects employment or securities rules in some jurisdictions. Name that as an open question when you offer it.
  - Promotion condition, keyed to Q3: an external party - a sponsor's hiring team, a conference, an investor - has committed in writing.
  - **Delete it, from this menu and from the axis lines above, when no such commitment exists**: an opportunity the organizer cannot actually deliver is the one prize that fails publicly, after the winner has been announced.

The full medium catalogue, the receipt-and-return practice, and the unit-count arithmetic are in [references/prize-medium-catalog.md](references/prize-medium-catalog.md).

## Total pool size

Four rungs:

1. **No monetary pool**
2. **Modest pool**: sized to the Prizes line.
3. **Sponsor-funded pool**: the organizer's own baseline is nothing and the pool scales only with signed commitments.
4. **Flagship pool**: deliberately sized to be the event's headline.

- value (submissions drawn and turnout - argued, not measured): `flagship > sponsor-funded > modest > no monetary pool`
- effort (fundraising, budget negotiation, and the procurement or payout volume that follows): `flagship > sponsor-funded > modest > no monetary pool`
- compliance cost: `flagship > sponsor-funded > modest > no monetary pool`
- efficiency: `sponsor-funded > modest > no monetary pool > flagship`

All three axes run in the same order. In every one of the six pairs the higher-value rung is _strictly_ worse on effort and on compliance cost, so no rung wins any axis for free and no pair can satisfy "value greater than or equal, every cost less than or equal". The ordering below rests on the argument, not on the check.

The payout-rigor menu is vacuous too, for its own separate reason, stated there.

Two things argue against the naive value line. Put both to the user rather than resolving either one.

**The value axis rests on an assumption, not a measurement.** "Flagship draws more submissions" is untested. Present it to the user as the assumption it is, because the published material cuts both ways and settles nothing.

- **Against sizing for headline value.** Devpost's own organizer guidance states that a very low prize can suppress participation, that a modest, well-distributed pool performs as well as a much larger one in its own stated experience, and that more prize money is no guarantee of stronger submissions. Participant engagement, technical support, promotion and simple requirements carry equal weight.
- **For it, as a single-edition illustration rather than a controlled measurement.** ETHGlobal Bangkok drew 713 project submissions from roughly 1,950 hackers in the same edition it ran its largest-ever prize pool, a record on both counts. HackYeah's most recent public figures pair nearly 3,000 attendees with over 300 submitted projects against a prize pool the organizers do not break out by placement.

Neither event controls for its own year-over-year growth or publishes a same-edition comparison against a smaller pool. Read both as texture, not as evidence for the axis either way.

**A counterweight points the other way regardless of participation counts.** The four organizations above lead with learn, build and share rather than prize size. Leading with a headline pool therefore competes on ground the credible large events deliberately vacate, and it selects for the participants who came for the money.

- **Sponsor-funded - the default where any sponsor is in play (Q3).** The sponsorship skills already do the fundraising, the pool scales with what actually got signed rather than with hope, and it draws nothing from the organizer's own Prizes line. Its failure mode is a pool announced before the money lands.
- **Modest, sized to the Prizes line - the default where no sponsor funds a prize.** A real ceiling bounds it, which is what makes it safe.
- **No monetary pool.** Near-zero on every axis, and a legitimate structure rather than a failure. It ranks third rather than first only because it forgoes the sponsor inventory a funded prize creates.
- **Flagship - the starved option**: top of every axis, so efficiency never picks it. Promotion condition, keyed to Q1 and Q7: the Prizes line is genuinely large enough that the pool fits inside it without moving another line, **and** the user's stated intent is attention before the event rather than reward after it. **Delete it, from this menu and from the axis lines above, when Q1 says the Prizes line has not been set** - a headline pool sized against no ceiling is a commitment made on behalf of a budget nobody has written.

## Split shape

Four rungs:

1. **Winner take most**: one large award, thin or no runner-up.
2. **Graduated podium**: first, second, third, descending.
3. **Track only**: no overall award; every prize belongs to a challenge track.
4. **Flat across many tracks**: many comparable awards, no headline.

- value (teams with something reachable to aim at, sponsor-track completion, a beginner's chance of placing): `flat across many tracks > graduated podium > track only > winner take most`
- effort (award count, per-winner eligibility check repeated, and per-unit procurement): `flat across many tracks > track only > graduated podium > winner take most`
- compliance cost, as the number of times an exposure category has to be re-checked against a different recipient: `flat across many tracks > track only > graduated podium > winner take most`
- efficiency: `graduated podium > winner take most > track only > flat across many tracks`

The efficiency line ranks graduated podium above track only because graduated podium has higher value than track only, lower effort, and lower compliance cost.

Devpost's own organizer guidance backs the value axis directly: splitting a pool into many chances to win is, in the platform's stated experience, the most effective structure, because participants want a reasonable chance of placing before they commit the hours to build.

Dominance check:

- Flat never dominates (top of every cost axis).
- Winner take most never dominates (bottom of value).
- Track only dominates nothing.

Track only sits below graduated podium on value for a specific reason. With no overall award, a team that used no sponsor's product has nothing at all to aim at, and those are frequently the teams the event most wants to keep.

One mechanic makes this menu concrete and is routinely missed: **a non-cash prize is counted in units per person, and cash is not.** MLH raises it as one of the rules an organizer must decide - "Can the teams be as large as they want, and you might just have only 4 prizes?"

MLH gives the matching practice on the procurement side: "Save the receipts for any prizes. If a winning team has 3 members instead of 4 you can return the prize to add to the next year's budget." So plan a gear or credits split in whole units against the team-size cap, with a stated rule for the leftover unit. A cash split divides arbitrarily instead, which is why the medium comes first.

- **Graduated podium - the default.** One extra award and one extra eligibility check beyond the cheapest rung, and it buys a second and third team something real to finish for. One published shape: PennApps split its top-three pool 50/30/20 across grand prize, second and third, so grand prize ran two and a half times third place and second ran one and a half times.
- **Winner take most.** Cheapest on every axis, and it motivates only the teams who already think they can win. **Delete it, from this menu and from the axis lines above, as soon as any sponsor funds a track** (Q3): that sponsor bought a named award and this shape has nowhere to put it.
- **Track only.** Correct when the brief published tracks and no overall category, which is a decision made in the brief, not here. Where an overall category exists in the published brief, this rung contradicts it.
- **Flat across many tracks - the starved option**: top of every cost axis, and every extra award repeats the whole eligibility and payout check against a new recipient. Promotion condition, keyed to Q2 and Q3: several sponsor tracks are already published **and** the medium is non-cash, so the repeated per-winner check is a handover rather than a payment.

  A flat structure commonly layers distinct award types rather than repeating one shape:

  - a ranked podium
  - an audience-choice award decided by attendee vote rather than by judges
  - one horizontal prize per sponsor technology or approach, so each sponsor owns a named award without diluting the podium
  - where a parallel non-judged activity runs alongside the main competition, its own small prize, kept clearly apart from anything judged

  Each layer is still one award on this menu's own terms. Repeat the eligibility and payout check for every one.

## Eligibility to receive, and payout rigor

Eligibility to receive is not eligibility to compete, and there is published practice for the distinction. MLH's copy-paste rule set states: "This event is limited to students. No volunteers, organizers, or mentors are eligible to win any prizes, though they can work on projects for their portfolio if they wish."

That sentence permits the same people to build and forbids them to win, which is exactly the split. The same source flags age range as a field the copy-paste set deliberately leaves blank for the organizer to fill.

`samber/dev-event-organizer-skills@event-volunteer-experience` reaches the same place from the volunteering side, deleting any volunteer reward with real cash value on the grounds that a reward reading as wages stops being volunteering. Treat both as one principle: anyone working the event is out of the receiving pool, whatever they are allowed to build.

Four rungs for the payout mechanic itself:

1. **Informal handover**: the prize changes hands on the spot, nothing recorded.
2. **Standard-form payout**: published eligibility-to-receive text, a claim step, and identity or status collection appropriate to the medium.
3. **Administered payout**: the fiscal host or the funding sponsor runs the payout under its own process and the organizer only facilitates.
4. **Counsel-reviewed payout**: a legal review before any prize is announced.

- value (defensibility if an award is challenged, and exposure actually avoided): `counsel-reviewed > administered > standard-form > informal handover`
- effort (hours, coordination with a host or sponsor, and the cost of engaging counsel): `counsel-reviewed > administered > standard-form > informal handover`
- compliance cost, as the review each rung triggers and the reversibility it costs: `counsel-reviewed > informal handover > administered > standard-form`
- efficiency: `standard-form > administered > informal handover > counsel-reviewed`

Value and effort run in the same order, exactly as on the pool-size menu. The compliance axis creates no dominance pair either: the rung it re-orders, informal handover, is also the cheapest on effort, so no pair clears every axis at once. The ordering rests on the argument below.

The compliance axis is deliberately non-monotone, and the argument is specific to payouts rather than borrowed from `samber/dev-event-organizer-skills@hackathon-judging`'s conflict menu. Informal handover triggers no review before the event. It defers the whole review to the least reversible moment there is, after money or goods have reached a stranger.

A misjudged rank can be re-announced. A payment cannot be un-made, and a prize handed to the wrong recipient comes back only by asking them to give it back. That asymmetry is why the default is not the cheapest rung.

- **Standard-form payout - the default.** One published paragraph and one claim step, both written before the event while they are still cheap. It is the lowest rung on the compliance axis because the review it triggers happens at the only moment a mistake is free.
- **Administered payout.** Promotion condition, keyed to Q3 and Q5: a fiscal host holds the money, or the funding sponsor prefers to pay its own track winner directly. Get the division of responsibility in writing before announcing, because "the sponsor is handling it" is not a payout plan.
- **Informal handover.** **Delete it, from this menu and from the axis lines above, when the prize is cash or a cash equivalent, or when Q4 says any winner could be a minor or outside the organizer's country.** It survives only for a handover of goods to an adult recipient at the venue.
- **Counsel-reviewed - the starved option**: top of value, effort and compliance cost. Promotion condition, keyed to Q1: a pool large enough that a losing team would ask who decided and on what basis. Promote it by routing to actual counsel or to the fiscal host, never by writing legal-sounding sentences yourself.

**Three of Q4-Q6's answers are gates, not menu choices, and the ratio gets no vote on them.** A minor in the winner pool, a winner outside the organizer's country, and a sponsor's own employee eligible to win that sponsor's own track each carry a legal obligation. An obligation determines the response instead of being weighed against effort.

When any of the three is live, counsel or the fiscal host reviews the payout before the prize is announced, whatever rung the efficiency line landed on. Efficiency then orders only what is left: how the surviving mechanic is administered, never whether the review happens.

One published mechanic belongs in whatever rung you pick. A prize can be conditional on something the winner must keep doing, and MLH's published rules make prize eligibility depend on the submitted code and video staying public afterwards: "If your repo and video are not public, new winners may be selected." Where you adopt a continuing condition, state in the published structure when the award becomes final, because until then it is revocable and everyone should know it.

The publishable eligibility text, the carve-out list, and the wording to hand to the brief are in [references/eligibility-to-receive-text.md](references/eligibility-to-receive-text.md).

## What this skill will never state

Contest-law classification, tax withholding and reporting, cross-border payment and the treatment of minors are jurisdiction-specific, and they change. **This skill states no numeric threshold, no tax-form name, and no currency amount. Ever.** A plausible-sounding threshold in a document telling an organizer how to hand money to a stranger is worse than no guidance at all.

Name the exposure category instead, say every time that the specific threshold or form is jurisdiction-specific, and route it.

- **Contest-law classification** - whether a prize competition counts as a skill-based contest or a game of chance in a given jurisdiction, which changes the regulatory regime that applies to it. This is why `samber/dev-event-organizer-skills@hackathon-judging` avoids a coin flip as a tie-break: the tie-break method is one of the few organizer decisions that could move an event across that line.
- **Payer-side tax reporting and withholding** on an award with monetary value, which typically attaches to the organizer rather than the winner.
- **Cross-border payment** - the payment rail itself, plus whatever local rules and treaty questions apply to a winner in another country.
- **Minors receiving an award**, where a guardian may need to receive or countersign it. This is a different question from the one MLH's checklist covers, which is a waiver for a minor to stay at a venue overnight.
- **Sponsor employees receiving that sponsor's own track prize** - a live conflict, and a different one from the judging conflict of interest `samber/dev-event-organizer-skills@hackathon-judging` already handles for the rank.
- **Organizers, volunteers, mentors and judges receiving anything**, the one category with published practice (see above).

Route each live category to counsel, to the fiscal host, or to the funding sponsor's own legal team.

MLH's organizer guide gives the routing shape rather than the answers, as a pre-flight checklist:

- nonprofit status
- insurance
- who holds signing authority and how long their review takes
- where funds are held and how quickly they can actually be spent
- in the source's own words: "Are there any tax requirements we should be aware of? Do we need to keep our receipts?"

For an organizer with no legal entity of its own, the same source names fiscal sponsorship as the standard route, listing Hack Club and Hack+ as hackathon-specific fiscal sponsors. The categories and the routing ladder are set out in [references/payout-exposure-categories.md](references/payout-exposure-categories.md).

## Failure modes

- **Deciding the size before the medium.** Half the sizing conversation concerns money a non-cash prize never involves. Medium first, always.
- **Sizing a pool against no ceiling.** A prize announced before the budget's Prizes line exists commits someone else's money on their behalf.
- **Announcing a sponsor-funded prize before the money lands.** The award is published, the sponsorship falls through, and the organizer owns the gap personally.
- **Splitting gear as if it divided like cash.** A four-unit prize meeting a three-person winning team is a decision you make in advance or improvise at the podium.
- **Letting the prize influence the rank.** `samber/dev-event-organizer-skills@hackathon-judging` hands you a ranked outcome. Reshaping the split so a favoured team lands better is re-judging with extra steps.
- **Treating eligibility to compete as eligibility to receive.** A volunteer who may build a project for their portfolio is not thereby someone who may take home the award.
- **Answering a tax question.** The question feels small every time, and the correct answer is a routing every time.
- **Assuming a sponsor's in-kind prize is worth its retail price.** `samber/dev-event-organizer-skills@event-sponsor-pricing` values in-kind at the budget line it displaces. Check that the method transfers before applying it to a prize, because a prize displaces a Prizes-line spend the organizer might never have made.
- **Assuming the podium order matches perceived value for in-kind prizes.** Credit or product prizes from different sponsors carry different real utility, so a third-place in-kind prize can be worth more to its winner than a first-place one from a less useful sponsor. Check what each item is actually worth to a recipient before setting tier expectations with the sponsor providing it.

## Measurement

Everything below is a self-set gate rather than an industry standard; say so when presenting it. Pool sizes and splits are not comparable across events, so do not borrow another event's number as a target.

**Pass threshold (structural, one only): before the brief is published, all six of these exist in writing with zero blanks.**

- The medium.
- The total pool with the budget line it fits inside.
- The split with an award count.
- The eligibility-to-receive text.
- The payout mechanic naming who hands over what.
- The list of exposure categories with the person each was routed to.

Iterate until the count is six.

Signals worth recording afterwards (self-set):

- awards actually handed over versus announced
- winners who never claimed
- prize units left over against the team-size rule
- any eligibility question that came up on the day and had no published answer

Pick two or three and write down the revision each would trigger.

## Invocation examples

- "We have three sponsor tracks and a general prize. How should we split the pool?"
- "Should we give cash or hardware? The budget is fixed either way."
- "One winner is a minor and another is in a different country. What do we need to sort out?"
- "Our sponsor wants to fund a prize for their own API track. Can their engineers win it?"
- "Write the prize section for our published rules."

Expected output: a prize structure with:

1. The medium with its reasoning and its compliance consequences.
2. The total pool and the budget line it fits inside, separating the organizer's baseline from sponsor-funded amounts.
3. The split shape with an award count and a leftover-unit rule where the medium is counted in units.
4. The eligibility-to-receive text ready to hand to the brief.
5. The payout mechanic with who does what.
6. The exposure categories that are live and who each was routed to.

Presented section by section for validation before publication.

## References

- [references/prize-medium-catalog.md](references/prize-medium-catalog.md)
- [references/eligibility-to-receive-text.md](references/eligibility-to-receive-text.md)
- [references/payout-exposure-categories.md](references/payout-exposure-categories.md)

See also, same collection:

- `samber/dev-event-organizer-skills@event-vendor-sourcing` - procures the physical goods a gear prize needs, on the lead times the medium menu warns about.
