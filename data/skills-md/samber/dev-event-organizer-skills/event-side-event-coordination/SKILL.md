---
name: event-side-event-coordination
description: Approve and coordinate third-party-run satellite events around a technical event - the vetting gate, calendar deconfliction against the published grid, name and logo usage rules, and the disclaimer stating what the main event does not vouch for. Use whenever a user group, sponsor or attendee wants to run a party, meetup, dinner, workshop or afterparty during the event's dates, when someone is already using the event's name on their own page, or when fringe events collide with the main programme - even if they never say "side event". Approving nothing is often the right answer; routes trademark and liability exposure to counsel. Do NOT use for the organizer's own evening programme - use samber/dev-event-organizer-skills@event-official-social-program instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Side Event Coordination

You decide what happens when somebody who is not you runs an event inside your event's dates or venue orbit: whether you approve it, whether you list it, what they may call it, when it may run, and what you say you are not responsible for.

The default answer is often nothing at all. Most community events never formalise this and are right not to. Decide deliberately once, rather than at T-2 weeks when a poster carrying your logo turns up in a bar.

## What you own, and what is already decided

You own the relationship with an event you do not run. Four questions, and only these four: approval, calendar, name, liability.

- **The evening you run yourself is not yours.** `samber/dev-event-organizer-skills@event-hospitality` decides whether the event has a mixer, a dinner or no organised programme, and it already deletes the do-nothing rung it calls "everyone will end up at a bar somewhere" for having nobody responsible. Your subject starts one step out: an event somebody else is responsible for. That skill's evening is what you provide; yours is what you permit.
- **The policy's reach is not yours.** `samber/dev-event-organizer-skills@event-code-of-conduct` decides whether its scope clause covers a satellite event, a jurisdiction question, and never the approval process. Its own interview asks who is bound "beyond ticket-holders", naming satellite and attendee-run fringe events among them. Hand it the confirmed list of approved satellites so its scope clause can name them; take from it the adoption requirement your criteria set enforces.
- **The peer swap is not yours.** `samber/dev-event-organizer-skills@cross-event-promotion` brokers reciprocal visibility between two independently-run events. Nobody hosts anybody and nobody approves anybody. A counterparty asking you to promote their event, rather than to run something inside your dates, belongs to that skill.
- **The grid is not yours.** `samber/dev-event-organizer-skills@event-schedule-design` owns the published session grid you deconflict against. Never move a session to make room for somebody else's party.
- **The main venue is not yours.** `samber/dev-event-organizer-skills@event-venue-sourcing` secures it. Note the name collision: that skill's "satellite sites" means extra venues for your _own_ event, never a third party's separate one.
- **Selling a side-event slot is not yours.** `samber/dev-event-organizer-skills@event-format-selection` already lists side events among the inventory a sponsor may buy, and `samber/dev-event-organizer-skills@event-sponsor-fulfillment` delivers what was sold. You decide the terms a bought slot runs under, exactly as you decide them for any other satellite.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-8 exist because the menus turn on them and no other question surfaces what they carry.

1. Has anyone actually asked to run something around your event - a party, a user-group meetup, a company dinner, a workshop - or are you designing for a possibility nobody has raised yet?
2. Is any third party already using your event's name, logo, or dates in materials they have published? Answer for materials you have seen, not for what you assume.
3. Does the organizing team hold a legal entity that could be a counterparty to anything, and who actually holds the event's name and marks - the team, a parent body, or nobody in particular?
4. Whose events are these: a sponsor who bought a side-event slot, a local user group, an attendee organising a dinner, or another organizer running a full second event?
5. Which hours of your own published grid must not lose their audience - keynotes, the evening programme, an awards moment - and is that grid published yet?
6. Who on the team would actually say no to a request, and would saying no be personal for them? A volunteer team whose decider drinks with the applicant is a different machine from a staffed one.
7. What is the effort ceiling: hours before the event, whether anybody will maintain a list live through the week, and how reversible a mistake can afford to be?
8. By what date must any of this exist - an application window, a published list, a printed guide - and is this a one-off edition or a recurring event whose rules should still hold next year?
9. What already exists that the default ordering assumes away: last edition's fringe list, a sponsorship agreement that already sold a side-event slot, a code of conduct whose scope clause already names unofficial events, or a parent body that owns the marks?

Q7 and Q8 move specific rungs. Name which answer moved which rung as you re-rank.

- **Nobody to maintain a list through the week** deletes the two rungs on the third menu whose entire value is being current.
- **A recurring mandate** promotes what is written once and reused - a criteria set, a disclaimer sentence, a protected-window statement - over anything re-run live each edition.

## Workflow

1. Run the interview. Q1 first: if nobody has asked and nobody is using your name, the honest recommendation is the first menu's default; say so before proposing machinery.
2. Answer the approval posture from the first menu. This decides everything after it - you cannot set naming rules for a population you have not decided to talk to.
3. If the posture is anything above doing nothing, write the criteria set _before_ the first application arrives. Load [references/application-and-criteria.md](references/application-and-criteria.md). Criteria invented after a request has landed are a judgment about that requester.
4. Set the naming rule from the second menu and write the exact sentence a satellite organizer must carry. One sentence, reusable, in the approval response.
5. Set the deconfliction depth from the third menu, against the published grid's own protected hours (Q5).
6. Write the liability position. It is not ranked, and it routes rather than resolves. Load [references/naming-and-liability-wording.md](references/naming-and-liability-wording.md).
7. Run the two cross-checks the collection already owns before approving anything: the sponsor-exclusivity check and the code-of-conduct adoption requirement, both in the criteria reference.
8. Publish the answer either way. An unpublished posture is read as permission by everyone who wanted permission.
9. After the edition, record what ran, what collided, what used your name without asking, and what you would refuse next time.

Present each decision for validation before publishing it: posture, criteria, naming rule, calendar depth, disclaimer. Publication is the point of no return, because a satellite organizer prints materials against your answer.

If your harness has persistent memory, record the posture and why, the criteria set, the naming sentence, every approval and refusal with its reason, and any unapproved use of the name you found. Next edition starts from a decided rule instead of an argument.

## Approval posture

Four rungs: **no posture** (approve nothing, list nothing, say nothing), **self-registration listing** (an open form, everything submitted gets published, no gate), **vetted application** (published criteria, a named decider, a recorded yes or no), **partnership agreement** (a signed document with a named counterparty and stated terms).

Two value axes, and they genuinely disagree - which is the whole reason this menu is worth running rather than defaulting to the cheapest rung.

- value, calendar coverage - the share of satellite events you actually learn about in time to do anything: `self-registration listing > vetted application > partnership agreement > no posture`
- value, misattribution and liability contained - how much you can refuse, and how defensible the line between you and them is: `partnership agreement > vetted application > no posture > self-registration listing`
- effort (drafting, a decision round per request, chasing organizers, negotiating): `partnership agreement > vetted application > self-registration listing > no posture`
- compliance cost, as the review each rung triggers and the reversibility it costs: `partnership agreement > vetted application > self-registration listing > no posture`
- efficiency: `no posture > vetted application > self-registration listing > partnership agreement`

**Dominance check, re-derived: 4 rungs, 6 pairs, zero strict-dominance relations.** Two mechanisms block all six, and both need naming.

- **Opposed value axes, four pairs**: no posture against the listing, the listing against the vetted application, the listing against the agreement, and the vetted application against the agreement. In each, the rung ahead on coverage is behind on containment.
- **Cost alone, two pairs**: no posture against the vetted application, and no posture against the agreement. Each of those two leads on _both_ value axes and still costs strictly more on effort and on compliance.

That accounts for every pair. The check catches no misordering, but unlike a menu whose axes are one list, the opposed-value mechanism here is a real disagreement rather than an artefact of construction.

The efficiency order is **not** cheapest-first, and the inversion is the point: the vetted application sits above the cheaper self-registration listing. A published list with no gate buys the worse of the two value axes, because it hands you an endorsement you never examined.

`samber/dev-event-organizer-skills@event-attendee-email-sequences` records the honest version of such a list, a night-by-night set of unofficial gatherings framed as "please support them" rather than as programming (devopsdays Chicago 2023 pre-event email, recorded in that skill's reference file). That framing is what keeps an unvetted list from reading as a vetted one. A list published without it is worse than no list.

- **No posture - the default, and often the right final answer.** Near-zero on every axis. It wins the ratio outright whenever Q1 says nobody has asked, and it is what most community events do. Publish the absence rather than leaving it silent: `samber/dev-event-organizer-skills@event-hospitality` makes the same argument about an unannounced evening, that silence is not neutrality but a decision to let something happen where nobody is responsible. **Delete it, from this menu and from the axis lines above, when Q2 says a third party is already using your event's name in published materials.** At that point doing nothing is not a posture, it is an unexamined licence.
- **Vetted application - the promotion, one step up.** Promotion conditions, keyed to Q2 and Q4: a third party is already using the name, or a sponsor bought a side-event slot whose terms somebody has to set. It costs a criteria set written once plus a decision round per request, and it is the only rung that buys coverage and containment together. A real version runs at conference scale: the UN Ocean Conference vets side-event proposals against how closely each relates to its own theme and gives priority to partnership submissions over single-organizer ones (full shape in [references/application-and-criteria.md](references/application-and-criteria.md)).
- **Self-registration listing.** Below the vetted rung on efficiency despite costing less, for the containment reason above. Promote it above the vetted rung when Q6 says nobody on the team can refuse a request without it being personal. An open list carrying a non-endorsement line is more honest than a gate that never says no, and it at least surfaces the calendar.
- **Partnership agreement - the starved rung.** Tops containment and tops both cost axes, and loses on coverage: only a committed few will sign anything, so most satellites never reach you. Efficiency never picks it. Promotion condition, keyed to Q3 and Q4: a legal entity exists on both sides _and_ the counterparty is running a full second event whose association with yours is material to both. **Delete it, from this menu and from the axis lines above, when Q3 says no entity could be a counterparty** - an agreement nobody can sign is a document that reappears as scope while the vetted rung goes unbuilt.

## Naming and branding rule

Four rungs: **no use of the event's name** (factual dates and city only), **factual reference only** (the name may appear in a plain factual sentence, no marks, no lockup), **mandatory unofficial-disclaimer wording** (the name may appear and a stated non-affiliation line must appear with it), **licensed co-branding** (a named, limited, purpose-bound licence to use the name and logo).

- value, attendee discoverability - a satellite event your audience can find and connect to your dates: `licensed co-branding == mandatory unofficial-disclaimer wording > factual reference only > no use of the event's name`
- value, misattribution avoided - a reader, a sponsor or a journalist reaches the correct conclusion about who is responsible: `no use of the event's name > mandatory unofficial-disclaimer wording > licensed co-branding > factual reference only`
- effort (drafting, per-request review, noticing when somebody ignores it): `licensed co-branding > mandatory unofficial-disclaimer wording > factual reference only > no use of the event's name`
- compliance cost, as the review each rung triggers and the reversibility it costs: `licensed co-branding > mandatory unofficial-disclaimer wording > no use of the event's name == factual reference only`
- efficiency: `mandatory unofficial-disclaimer wording > factual reference only > no use of the event's name > licensed co-branding`

The discoverability tie is argued, not a dodge: both rungs put your event's name in the satellite's own materials, which is the entire mechanism by which anyone finds it. The tie assumes a disclaimer line changes what a reader concludes about who runs the thing without changing whether they encounter it, and that assumption is weaker than it looks.

Trademark-specific disclaimer research finds disclaimers unreliable at curing the confusion they are meant to cure. A broader review of advertising disclaimers found them ineffective or actively harmful to the reader's judgment across most of the controlled studies it covers (both in [references/naming-and-liability-wording.md](references/naming-and-liability-wording.md)). Treat the misattribution axis, and the one dominance relation it produces below, as resting on a contested premise rather than a settled one.

Factual-reference-only sits _last_ on misattribution, below even co-branding, and the reason is worth stating because it is counter-intuitive. Misattribution is a reader reaching a wrong conclusion. Under a licence the reader concludes the event is connected to yours and is right. Under a bare factual reference the reader concludes the same thing and is wrong, with nothing on the page to correct them. Cheapness is what makes that rung dangerous rather than safe.

The compliance `==` is real: neither of the bottom two rungs grants anything, so neither creates an instrument to review or revoke. They differ in what a satellite organizer may say, which is a rule rather than a review.

**Dominance check, re-derived: 4 rungs, 6 pairs, exactly one strict-dominance relation - the mandatory disclaimer dominates licensed co-branding**, tying it on discoverability, beating it on misattribution, and costing strictly less on both effort and compliance. The efficiency line honours it by ranking the disclaimer first and co-branding last. The remaining five pairs split two ways.

- **Opposed value axes, three pairs**: no use of the name against each of the other three rungs in turn, since it tops misattribution avoidance and bottoms discoverability.
- **Cost alone, two pairs**: factual reference against the disclaimer, and factual reference against co-branding. In each, the rung ahead leads on both value axes and costs strictly more on both cost axes.

Every pair is accounted for, and this menu's check carries real information rather than being clean by construction. That one dominance relation is only as solid as the misattribution axis it derives from. Treat "the mandatory disclaimer dominates licensed co-branding" as the conclusion the current axis produces, not as independently verified.

- **Mandatory unofficial-disclaimer wording - the default.** One sentence, written once, carried in every approval response and required on the satellite's own page. The exact wording and its five components are in [references/naming-and-liability-wording.md](references/naming-and-liability-wording.md).
- **Factual reference only.** Cheap and real. `samber/dev-event-organizer-skills@cross-event-promotion` describes this same floor case from the other side, a smaller event referencing a bigger one's dates with no deal at all, and closes with the instruction that matters here: "check before borrowing a trademark" (that skill's own rule, drawn from co-marketing practice rather than from an events-industry finding). You are the party being checked with, and answering the check is this menu.
- **No use of the event's name.** Tops misattribution avoidance and costs nothing, and it is the honest answer where you are unwilling to review anybody's materials. Its cost is that nobody finds the satellite. Two named conferences run this rung as enforced policy rather than as a fallback: SXSW bans third-party use of its marks for unofficial events outright and hands organizers a substitute name to use instead, and CES enforces the same rule under the name "outboarding," with real penalties attached (both in [references/naming-and-liability-wording.md](references/naming-and-liability-wording.md)).
- **Licensed co-branding - dominated, not merely starved.** Because it is dominated, its promotion condition has to break the tie that produces the dominance rather than merely outweigh a cost. Promote it only where you _want_ the event read as connected, so that discoverability stops being a tie and the licence stops being misattribution: a sponsor's bought side-event slot (Q4), or a partner-run track you would name in your own programme. **Delete it, from this menu and from the axis lines above, when Q3 says nobody clearly holds the marks** - granting a licence you do not hold is a worse problem than the one it solves. Where a parent body holds them, the grant is theirs to make, not yours.

## Calendar deconfliction depth

Four rungs: **none** (satellites post independently), **published protected windows** (state which of your own hours nothing should run against, and let organizers self-serve), **shared public calendar** (one page listing every known satellite with its time, maintained by you), **actively deconflicted fringe guide** (you place satellite slots against your grid's own gaps and distribute a curated guide).

- value, your own programme's audience protected: `actively deconflicted fringe guide > published protected windows > shared public calendar > none`
- value, an attendee can see what is on and choose: `actively deconflicted fringe guide > shared public calendar > none == published protected windows`
- effort (drafting, per-item collection, maintenance through the week): `actively deconflicted fringe guide > shared public calendar > published protected windows > none`
- compliance cost, as the review each rung triggers and the reversibility it costs: `actively deconflicted fringe guide > shared public calendar > published protected windows == none`
- efficiency: `published protected windows > none > shared public calendar > actively deconflicted fringe guide`

A window statement beats a calendar on the first value axis and loses to it on the second, and both facts have the same cause: a statement _prevents_ a collision, a calendar merely _records_ one. The planning-axis tie between none and protected windows is real at zero. Neither publishes any satellite's time, so an attendee learns nothing from either; a window statement addresses organizers.

The compliance `==` is also real at zero: neither bottom rung publishes a third party's event at all, so neither sends the endorsement signal the two upper rungs send. A curated guide handed out at check-in is the strongest such signal available, every listing in it is a per-item check you own, and a printed guide cannot be retracted after distribution.

**Dominance check, re-derived: 4 rungs, 6 pairs, zero strict-dominance relations.** Two mechanisms cover all six.

- **Cost alone, five pairs**: none against protected windows, none against the calendar, none against the guide, protected windows against the guide, and the calendar against the guide. In each, the rung ahead on value costs strictly more. In the first of those five the extra cost is effort only, since the two rungs tie at zero on compliance.
- **Opposed value axes, one pair**: protected windows against the shared calendar, for the reason argued above.

That accounts for every pair. The ordering rests on the argument, not on the check.

- **Published protected windows - the default.** Near-zero effort, no third party published, and it protects the thing the grid was built for. **Delete it, from this menu and from the axis lines above, when Q5 says the grid is not published yet** - you cannot protect windows nobody can read, and a protected-window statement issued against an unpublished grid is a promise you will break when the grid moves. Fall back to no posture until the grid ships. A real trade-show version of this rung protects the whole show rather than named hours: RE+ Events restricts exhibitors from hosting or participating in competing or conflicting events during official show hours, enforced by booth cancellation and exclusion from future shows, and extends the same requirement to hospitality suites and hotel-room activity in proximity to the event, which must be disclosed and consented to in advance (RE+ Events Terms & Conditions, "Suitcasing/Outboarding").
- **None.** Ranked second, and genuinely correct where Q1 found nobody running anything. It beats the shared calendar because the calendar's entire payoff depends on being current, and a stale calendar sends people to a cancelled event - a worse outcome than never having claimed to know.
- **Shared public calendar.** Promotion conditions, keyed to Q1 and Q7: more than a couple of satellites are running _and_ somebody is named to maintain the page live through the week. Both, not either. **Delete it, from this menu and from the axis lines above, when Q7 finds nobody to maintain it** - its whole payoff is being current, so an unmaintained calendar is not a cheaper version of this rung, it is the stale-calendar failure the rung above it is deleted for.
- **Actively deconflicted fringe guide - the starved rung.** Tops both value axes and tops both cost axes, so efficiency never picks it. Promotion conditions, keyed to Q8 and Q9: the edition recurs _and_ last edition's list exists to start from, which is what turns a build into an update. **Delete it, from this menu and from the axis lines above, when Q7 finds nobody to maintain it.** A half-maintained guide with your name on it is the listing failure with a print run.

## Liability, and where ranking is refused

The disclaimer is **deliberately not ranked**, and the refusal is not a gap to fill later. What you must disclaim follows from what you actually did - whether you approved, whether you listed, whether you licensed the name, whether it happened in your venue - and from the jurisdiction the event sits in. A value-per-effort ratio has no vote on any of that, and ranking it would quietly authorise skipping the bottom rung.

**This skill states no legal threshold, no jurisdiction, no form or instrument name, and no monetary figure - ever.** That is a standing policy, and the same one `samber/dev-event-organizer-skills@hackathon-cash-prize` holds for prize law. A plausible-sounding rule in a document telling an organizer what they are liable for is worse than no guidance at all.

Name the exposure categories and route each one. The full list, the routing ladder, and the disclaimer's components are in [references/naming-and-liability-wording.md](references/naming-and-liability-wording.md).

- Use of your name and marks by somebody you do not control.
- Apparent endorsement created by listing or promoting an event you did not run.
- Whatever happens to a person at a third party's venue.
- Alcohol served by somebody else.
- Personal data collected by a satellite organizer from people who found them through you.

Route each to counsel, to the parent body that holds the marks, or to whoever holds the organization's privacy obligations. `samber/dev-event-organizer-skills@event-risk-management` carries whichever of these you decide to keep as a scored row; the routing stays here.

Two mechanics from elsewhere in the collection belong in whatever you write.

- Keep a withdrawal right separate from any breach. `samber/dev-event-organizer-skills@event-sponsor-agreement` records a reputational termination right letting an organizer stop where "it reasonably determines that it would be detrimental to the reputation and goodwill" of the organization (PyCon US 2020 sponsorship contract, recorded in that skill's clause library). An approval you cannot withdraw is a permission you gave for every future edition.
- Make any name licence expire on its own rather than continuing silently, exactly as that same sibling's drafting rule requires for sponsor marks.

## Failure modes

- **Designing the machine before anyone asks.** An application form, a criteria set and a calendar for a population of zero. Q1 exists to stop this; the first menu's default is the answer more often than not.
- **Publishing a list without the framing.** An unvetted list read as a vetted one, because nothing on the page says otherwise. The framing that works is a request to support these events, not an announcement of programming.
- **Inventing criteria after the request arrives.** Criteria written in response to one application are a judgment about that applicant, and the applicant will read them that way. Write them first or run no gate at all.
- **Approving a satellite that breaks a paid sponsor's exclusivity.** A competitor's party during your dates, listed on your page, is inventory somebody else bought. The check and its owner are in the criteria reference; `samber/dev-event-organizer-skills@cross-event-promotion` names the same trap for comped booth space.
- **Assuming your code of conduct reaches an approved satellite.** It reaches exactly as far as its scope clause says, and that clause belongs to `samber/dev-event-organizer-skills@event-code-of-conduct`. Adoption is a condition you impose at approval, not a fact you inherit.
- **Confusing a peer swap with a hosting request.** Somebody proposing to promote each other is a `samber/dev-event-organizer-skills@cross-event-promotion` conversation and needs none of this machinery.
- **Moving your own grid to accommodate somebody else's party.** The grid belongs to `samber/dev-event-organizer-skills@event-schedule-design` and was laid against constraints this decision does not outrank.
- **Answering a liability question.** It feels small every time, and the correct answer is a routing every time.

## Measurement

Every threshold here is one you set rather than a benchmark to hit. Say so when you present them.

**Pass threshold (structural, one only): before the first satellite is approved or listed, all five of these exist in writing with zero blanks.** Iterate until the count is five.

1. The posture with its reason.
2. The criteria set, or an explicit decision to run no gate.
3. The naming sentence.
4. The calendar depth with its protected windows.
5. The exposure categories with the person each was routed to.

Signals worth recording afterwards (self-set). Pick two or three and write down the revision each would trigger.

- Satellites that ran without ever reaching you.
- Collisions against your own protected windows.
- Uses of your name you did not approve.
- Refusals, and whether any was contested.
- Whether anyone attributed a third party's event to you afterwards.

## Invocation examples

- "A local user group wants to run a meetup the night before our conference and call it a pre-conference event. Can they?"
- "Someone is selling tickets to a party using our logo. What do we do, and what should we have done?"
- "We have six fringe events during our week and half of them clash with our keynotes."
- "Our platinum sponsor bought a side event. What terms does it run under?"
- "Should we publish a list of the unofficial parties happening during our conference?"

Expected output: a coordination plan carrying six elements, each one you set yourself labelled as such, presented section by section for validation before anything is published.

1. The approval posture and why, including the case for doing nothing.
2. The criteria set, or an explicit decision to run no gate.
3. The naming rule, with the exact sentence a satellite organizer must carry.
4. The deconfliction depth, with the protected windows named.
5. The liability position, with each exposure category and who it was routed to.
6. The two cross-checks run: sponsor exclusivity and code-of-conduct adoption.

## References

- [references/application-and-criteria.md](references/application-and-criteria.md) - the application fields, the published criteria set, the decision record and the withdrawal mechanic, the sponsor-exclusivity and code-of-conduct cross-checks, and a positive and negative pair of refusal wordings.
- [references/naming-and-liability-wording.md](references/naming-and-liability-wording.md) - the four naming rungs as usable wording, the disclaimer's five components, the sourced trademark-licence shape, the exposure categories in full with their routing ladder, and the standing no-legal-detail policy restated with its reasoning.

See also, same collection:

- `samber/dev-event-organizer-skills@event-code-of-conduct` - decides whether its policy's jurisdiction reaches an approved satellite; this skill supplies the confirmed list and imposes adoption as an approval condition.
- `samber/dev-event-organizer-skills@cross-event-promotion` - reciprocal marketing between two independently-run events, with no hosting and no approval; it also holds the satellite organizer's own side of the trademark question.
- `samber/dev-event-organizer-skills@event-schedule-design` - owns the published grid whose protected hours this skill deconflicts against.
- `samber/dev-event-organizer-skills@event-hospitality` - owns the event's own evening and social provision; this skill owns other people's.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - delivers a side-event slot a sponsor bought, and holds the exclusivity clauses the criteria set checks against.
- `samber/dev-event-organizer-skills@event-sponsor-agreement` - holds the trademark-licence and reputational-withdrawal clause shapes this skill borrows.
