---
name: startup-pitch-contest
description: Run a startup pitch contest or demo day inside a technical event - the pre-event application and selection funnel, the pitch format and the time it costs, the rubric dimensions an investor judge actually scores, the conflict of interest specific to a judge who may want to invest in the company just ranked, and a prize built from introductions and committed meetings rather than cash. Use whenever the user mentions a pitch competition or demo day, opening applications for startups, picking a slate, briefing an investor jury, pitch time limits, or what the winner gets - even if they never say "pitch contest". Routes securities and contest-law questions to counsel. Do NOT use for projects built during the event - use samber/dev-event-organizer-skills@hackathon-judging instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Startup Pitch Contest

You design and run a pitch contest: a demo day, a startup showcase, a pitch competition, held inside a larger technical event. It covers:

- Who gets on the stage.
- What they do once they are on it.
- Who judges, and on what.
- What a judge may do afterwards with a company they just watched.
- What the winner actually receives.

## No build phase

A hackathon judges an artifact assembled inside the event, in a room the judges can walk into. You judge a company that existed before anyone arrived and will exist after everyone leaves. Three consequences run through every section:

1. **Almost nothing that decides the result is observable in the slot.** `samber/dev-event-organizer-skills@hackathon-judging` tells its reader to "Check the highest-weighted criterion is one a judge can actually observe in the slot." That instruction deletes most of a pitch rubric here. Traction, retention, margin and team history are claims about a world outside the room, so the reviewing problem becomes verification against an application, not observation on the day.
2. **Readiness is a property of the applicant, not of the event.** A hackathon can rescue an unfinished project with more hacking hours. Nothing makes a company more ready between the call closing and the stage, so everything that decides slate quality happens in the funnel.
3. **Nothing here schedules a build, a venue for one, or mentors for one.** There is no build phase, so there is no hand-off to make and no sibling skill owns one.

## What you own, and what is already decided

- **The block is not yours.** `samber/dev-event-organizer-skills@event-format-selection` commits the hours in the shape, and `samber/dev-event-organizer-skills@event-schedule-design` places the block in the published grid. You design _inside_ that block and never move a session.
  - The format-selection demo-structure menu (expo table, stage pitch, video only, two-stage) is written for hackathon teams presenting projects built at the event, and names no startup pitch contest.
  - The pitch format below is claimed here rather than agreed with it. Say that when presenting it.
- **The scoring arithmetic is not yours, and you must not re-derive it.** `samber/dev-event-organizer-skills@hackathon-judging` already solved the judge-time-budget problem in general form: the full-coverage ceiling, the coverage-per-team formula, the three allocation bands, and the feasibility gate all live in its own judge-allocation reference.
  - Open that skill, load that reference, feed it your own numbers, and consume the answer.
  - Only one input changes meaning: the hackathon per-team figure is dominated by setup and swap at a physical handoff, and a serial stage block has none of that. Take the formulas, and re-measure the input.
  - The full adaptation is in [references/pitch-block-and-rubric.md](references/pitch-block-and-rubric.md).
- **Founder-to-investor 1:1 meetings are not yours.** `samber/dev-event-organizer-skills@event-b2b-matchmaking` owns them, and already names the configuration a pitch contest tends to grow into: "a curated founder-and-investor day, not a conference with a meeting corner." A pitch is a broadcast to a jury; a meeting is a booked pair. Route it there and build no booking mechanic here.
- **Cash prize structure almost certainly does not apply.** `samber/dev-event-organizer-skills@hackathon-cash-prize` is named and scoped to hackathons throughout, and its medium menu is built on one hackathon organizer's prize guidance. Do not reach for it by default.
  - Its refusal to state a threshold, a form name or a currency amount transfers and is adopted below.
  - Its routing shape transfers and is adopted below.

Do not state any of the following, in this skill or in anything built from it:

- Pitch length.
- Slate size.
- Judge count.
- Application volume.
- Acceptance rate.
- Prize amount.
- Equity percentage.

Those seven are exactly the quantities that feel safe to invent, and an invented number outlives the caveat attached to it. One published figure is the exception: DevOpsDays' organizing guide states people usually need at least 4-6 weeks to arrange travel or time off before a pitch event.

Every ranking below is a default, not a law. After the interview, re-rank all four menus against what you already know. Each of the following overturns a default rung:

- A fund partner already on the organizing team.
- An accelerator relationship that predates the event.
- A slate half-filled by invitation before the call opened.
- A stage block that cannot grow.

## Interview

Ask one question at a time, multiple-choice where possible. The menus below turn on questions 4-6 and 9-10, and nothing else surfaces the facts they carry.

1. Is the contest already committed in the published programme, and what has already been said publicly about how a company gets on that stage? Read it before designing anything - a published route is a promise, not a starting position.
2. Who is the pitching population, described as a stage of company rather than a number: pre-product, first customers, or raising against traction? Who decided that, and is it written down anywhere an applicant can read?
3. Which block of the grid does the contest own, is that block already fixed, and how many companies is it expected to hold?
4. Who judges, named by role - active investors, operators, customers, sponsor representatives, a regional or public-sector representative where the event carries a regional or public mandate? For each investor judge, does their fund invest at the stage these companies are at? And was anyone, judge or audience, invited specifically because of who would be pitching?
5. What does the winner actually receive, item by item - and for each item, which party delivers it, and have they committed to it in writing?
6. Does any award carry capital, a convertible instrument, or equity in any form? If so: is placing that capital the reason the contest exists, or is it a prize attached to a contest that would run anyway?
7. Is any part of the contest sponsored, and does any signed agreement give a sponsor a say in who pitches or who wins?
8. Is the room recorded, streamed, or open to press - and were applicants told that before they applied?
9. One-off edition, or a recurring contest whose rules should still hold next year? By what date must the call and its criteria be published?
10. What is the effort ceiling: organizer hours across the application window, who reads applications, who chases a third party that promised the winner something - and what already exists that would overturn a default, such as named referrers who would nominate companies?

## Workflow

1. Run the interview. Read what was already published (Q1) and the block you were given (Q3) before designing anything.
2. **Decide the prize before the funnel** - the same ordering `samber/dev-event-organizer-skills@hackathon-cash-prize` argues for its own domain. What the winner receives decides who applies, which judges will sit, and whether counsel has to see the structure at all.
3. Pick the funnel from its menu and write the published route down as a sentence before you build any form. Field lists are in [references/application-and-slate-mechanics.md](references/application-and-slate-mechanics.md).
4. Publish the criteria and their weights in the call itself, before applications close. `samber/dev-event-organizer-skills@hackathon-judging` states the reason in one line that transfers without modification: "Undisclosed weights score a competition nobody entered."
5. Pick the pitch format from its menu, then take the arithmetic - not the numbers - from `samber/dev-event-organizer-skills@hackathon-judging`'s allocation math and check the block actually holds the slate.
6. Build the rubric on what a judge can reach, splitting observable dimensions from claimed ones. Both lists and a positive/negative scoring pair are in [references/pitch-block-and-rubric.md](references/pitch-block-and-rubric.md).
7. Set the conflict rule from its menu, and brief every judge on it before they see a single application - not before they score. Full ladder and the sponsor hard case are in [references/investor-conflict-and-prize-policy.md](references/investor-conflict-and-prize-policy.md).
8. Run the three gates below. If any one fires, counsel or the committing party reviews the structure before the award is announced.
9. Run the block. Announce from a prepared list, and state the same contest path `samber/dev-event-organizer-skills@hackathon-judging` prescribes: who receives a challenge, a window that closes before anything of value changes hands, and what can actually change.
10. Record what was delivered against what was announced, per item and per party, and hand nothing downstream - the award is yours to close out.

Present the design section by section for validation - prize, funnel, format, rubric, conflict rule - before the call goes public. A published call is a promise to founders who will rearrange a company's month around it.

If your harness has persistent memory, record the published route and its criteria, the prize items with the party who committed each one, every declared judge interest, and which of those items was actually delivered afterwards.

## Selection funnel

Four rungs:

- **Curated invitation**: the organizer fills the slate from companies it already knows.
- **Open application, single review pass**.
- **Open application with a screening call**, before the slate is fixed.
- **Nomination by named referrers**: funds, accelerators or community leads each put companies forward, and the organizer selects from what arrives.

- effort (organizer hours across the window, review passes, and the promotion an open call has to sustain): `open plus screening call > open single pass > nomination > curated invitation`
- value, slate quality (pitches a judge and an audience would stay in the room for): `open plus screening call > nomination > curated invitation > open single pass`
- value, pipeline breadth (companies you would never have found on your own): `open plus screening call == open single pass > nomination > curated invitation`
- compliance cost, as the review it triggers and the reversibility it costs: `open plus screening call > open single pass > nomination > curated invitation`
- efficiency: `open single pass > nomination > curated invitation > open plus screening call`

The breadth `==` is argued rather than used to avoid a decision: breadth is fixed by _who is allowed to apply_, and both open rungs are open to exactly the same population. A second pass cuts the slate; it never widens the pool. The two rungs are genuinely equal on that axis and differ on every other one.

The compliance axis is real here and is easy to miss. Every applicant hands over material about a private company. The wider the call and the more people who read it, the more custody you take on and the less of it you can withdraw: a deck circulated to a reviewer cannot be un-circulated. The screening call tops the axis because it is the rung where a founder says more than the form asked for, with no record of what was said.

**Dominance check, re-derived: 6 pairs, zero strict-dominance relations, and the reason accounts for all six in two groups.**

- Four pairs, the screening rung against each of the other three, and nomination against curated invitation, are blocked the ordinary way: the rung ahead on value costs strictly more on effort _and_ on compliance.
- The other two pairs are blocked because the two value axes genuinely disagree: **open single pass against nomination, and open single pass against curated invitation**. There, the open rung tops breadth and trails on slate quality, so neither rung can be at least equal on both.

Clean only by construction. The check catches nothing, and the efficiency line rests on the arguments below.

- **Open application, single review pass - the default.** It buys the whole reason to run a contest instead of booking the companies you already like, at one review pass. Its weakness is stated rather than hidden: paper review of strangers is the weakest available predictor of how a founder holds a stage, which is why it sits last on slate quality.
- **Nomination by named referrers.** A referrer's own standing rides on the company they put forward, and the pool is wider than the organizer's address book.
  - **Promotion condition, keyed to Q10:** named referrers who would actually nominate already exist.
  - Built for one edition from nothing, the rung stops paying: its recruiting and briefing cost lands before a single application arrives.
- **Curated invitation.** Cheapest on every axis, and it ranks third rather than first for a specific reason: the slate is one the organizer could have produced with no contest at all, so the mechanic earns nothing its own name promises.
  - **Delete it, from this menu and from the axis lines above, when Q1 says a public route onto the stage has already been announced.** Running a call and then filling the slate from your own contacts is the single most contestable thing in this skill.
- **Open application plus a screening call - the starved option.** Top of slate quality, top of effort, top of compliance cost, so efficiency never picks it. It is also the only rung that tests what the form cannot show: whether the founder can hold a room. Two promotion conditions, each traced separately:
  - **Keyed to Q3:** the block is fixed and short relative to the slate it must hold, so one weak pitch costs a share of the block you cannot get back.
  - **Keyed to Q4:** a judge or an audience was invited specifically because of who would be pitching. The slate was the offer, and the offer has to survive contact.

The open rungs' timeline carries over from the call `samber/dev-event-organizer-skills@event-cfp-design` designs: open early, close well before the event, review inside the gap. So does its one hard floor, the published lead time an accepted party needs to arrange travel. Below that floor the open rungs stop working and the slate goes to invitation. The anchors, the published figure and the limit on carrying it across are in [references/application-and-slate-mechanics.md](references/application-and-slate-mechanics.md).

## Pitch format

Four rungs:

- **Stage pitch only**: a fixed slot, no questions.
- **Stage pitch plus judge questions**.
- **Stage pitch plus questions plus a closed-door deep dive** with the finalists.
- **Written or recorded submission scored before the day**, with a stage pitch for finalists only.

- effort (block minutes consumed, judge hours, and rounds to run): `deep dive > pre-scored plus finalist stage > pitch plus questions > pitch only`
- value, evidence a judge actually holds when scoring: `deep dive > pre-scored plus finalist stage > pitch plus questions > pitch only`
- value, what the room gets (the audience the event sold this block to): `pitch plus questions > pitch only > pre-scored plus finalist stage > deep dive`
- compliance cost, as the review it triggers and the reversibility it costs: `deep dive > pre-scored plus finalist stage > pitch only == pitch plus questions`
- efficiency: `pitch plus questions > pitch only > pre-scored plus finalist stage > deep dive`

The room axis is what makes this menu decidable, and it runs against the other three. Questions are the only part of a pitch block where the founder is not reciting, which is why they top it. Pre-scoring and the deep dive each shrink or hide the part the audience came for, and the deep dive hides the decisive part entirely: the room watches a pitch and then hears a result decided somewhere it could not see.

The compliance `==` is argued: both stage rungs put the same material in front of the same public room, and a question answered on a public stage transfers no custody to the organizer that a statement made on it did not. The exposure is set by the room being public, not by whether anyone asked anything.

- Pre-scoring ranks above both stage rungs because the organizer takes and holds written material, and must say who reads it and what happens to it afterwards.
- The deep dive tops the axis because it is the one rung that puts confidential material in a room with no audience and no record.

**Dominance check, re-derived: 6 pairs, zero strict-dominance relations, in two groups.**

- Five pairs, every pair containing the deep dive or the pre-scored rung, are blocked by the two value axes disagreeing: each of those rungs leads on evidence and trails on what the room gets, so neither can be at least equal on both.
- The sixth pair is the informative one, blocked by effort alone: **stage pitch plus questions beats stage pitch only on both value axes at identical compliance cost**, and only the extra block minutes stop it dominating outright.

That finding is why the default sits where it does rather than on the cheaper rung beneath it.

- **Stage pitch plus judge questions - the default**, for the reason the dominance check just gave.
- **Stage pitch only.** Cheapest, and honest where the award is a title and a stage moment.
  - **Delete it, from this menu and from the axis lines above, when Q5 says the award commits a third party to anything**: an introduction, a meeting, a place, capital. A committed outsider is being asked to act on a judgment reached without one unscripted answer.
- **Pre-scored submission with a finalist stage.** Moves part of the judging out of the live block, which is the same lever `samber/dev-event-organizer-skills@hackathon-judging` reaches for when its arithmetic says the window cannot hold the field. Correct when that arithmetic says so; a poor trade when it does not, because it spends the audience's block on fewer companies.
- **Closed-door deep dive with finalists - the starved option.** Top of evidence, top of effort, top of compliance cost, bottom of what the room gets, so efficiency never picks it. Promote it and you publish that it exists, and who is in the room, before applications close. Two promotion conditions, traced separately:
  - **Keyed to Q6:** the award carries capital, in which case a public pitch does not reach the facts the award has to be justified on.
  - **Keyed to Q2:** the pitching population is described as raising against traction, so the judges are being asked to score claims - revenue, retention, cost of acquisition - that no stage slot can show.

## Investor conflict of interest

This is where the hackathon model breaks, and reusing its shape unchanged is the mistake this section exists to stop. Practitioner guidance on judging pitch competitions converges on the same starting instinct: a judge should not score their own portfolio company, employer's team, or anyone they have previously advised. It stops at recusal, and names none of the three structural differences below.

`samber/dev-event-organizer-skills@hackathon-judging`'s ladder covers team closeness, employer and competing-organization ties, and sponsor ties. Every one is an interest in _the outcome_, which recusal from scoring removes because it removes the vote. Only that ladder's upper rungs and its hard case are keyed to sponsors specifically.

An investor judge's interest is structurally different in three ways, and none of them is fixed by recusal:

1. **The interest is in access, not in the result.** A judge gains the same early look at a company whether or not they score it. Recusal removes the vote and leaves the advantage intact.
2. **The interest can run backwards.** A judge holding a position in a company that competes with an applicant has an interest in that applicant _not_ winning, and in it looking ordinary while the judge is standing next to it.
3. **The judge has obligations of their own.** An investor sitting on a panel is frequently subject to their own institution's disclosure and allocation rules. Those obligations are not yours to interpret and not yours to satisfy - they are a reason to ask, in writing, whether the judge is permitted to be there at all.

Four rungs:

- **No stated rule**.
- **Scoring recusal only**: the hackathon shape, imported.
- **Recusal plus disclosure to the pitching companies**, before they pitch.
- **Recusal plus disclosure plus a stated contact protocol**: a stand-off window before any judge approaches a company off this stage, and a route through the organizer when they do.

- value, credibility of the result to the companies and to the room: `contact protocol > disclosure > recusal only > no stated rule`
- effort (collecting interests, judge briefing, tracking on the day, and enforcing anything afterwards): `contact protocol > disclosure > recusal only > no stated rule`
- compliance cost, as the review it triggers and the reversibility it costs: `contact protocol > no stated rule > disclosure > recusal only`
- efficiency: `disclosure > recusal only > no stated rule > contact protocol`

The compliance axis is deliberately non-monotone, and the argument is specific to this domain rather than borrowed.

- **No stated rule** triggers no review before the event and defers the entire review to the least reversible moment there is: after a judge has approached a company off a ranking they helped produce. That cannot be un-approached, and the company will read it backwards through everything that happened on stage.
- **Recusal only** is the cheapest real rung: one line in the judge brief, and a missed tie is quietly fixable by moving a scorer while no result exists.
- **Disclosure** ranks above it because a statement made to the pitching companies cannot be unmade.
- **The contact protocol** is hardest to unwind, because it commits the organizer to police what independent professionals do with their own deal flow, and withdrawing it next edition reads as a retreat.

**Dominance check, re-derived: 6 pairs, zero strict-dominance relations, in two groups.**

- Four pairs, the contact protocol against each of the other three, and disclosure against recusal only, are blocked the ordinary way: the higher-value rung costs strictly more on effort and on compliance.
- The other two pairs are the informative ones, blocked by effort alone: **disclosure beats no stated rule, and recusal only beats no stated rule, each on value and on compliance simultaneously**. In both cases, only the effort of writing the rule down stops the relation.

Read that as the menu's actual finding. The bottom rung is not a cheap version of a rule; it is worse on a cost axis as well as on value, which is why it is deleted rather than ranked.

- **Recusal plus disclosure to the pitching companies - the default.** Recusal alone is imported from a domain where the interest is the vote; here the interest is created by watching, so recusal buys much less than it does at a hackathon. Disclosure costs one more line in the brief and one slide before the block, and it is the first rung that addresses the interest that actually exists.
- **Scoring recusal only.** Honest where the panel is operators and customers rather than investors. Say plainly what it does not cover.
- **No stated rule.** **Delete it, from this menu and from the axis lines above, as soon as Q4 turns up a single active investor on the panel.** That deletes it at most pitch contests; it stays on the page because a contest judged entirely by operators and customers is a real configuration, not a hypothetical.
- **Contact protocol - the starved option.** Top of value, effort and compliance cost. Two promotion conditions, traced separately:
  - **Keyed to Q6:** the award carries capital or an instrument, so a judge's own institution is already a party to the outcome, and the informal path was never available to them.
  - **Keyed to Q9:** a recurring contest whose published rules already promise a process. `samber/dev-event-organizer-skills@hackathon-judging` uses the same reasoning to promote its own registry rung, and the mechanism is identical once a rule has been published.

## Prize and opportunity structure

Four rungs:

- **Recognition only**: a title, the stage moment, a write-up.
- **Committed introductions**: named warm introductions the organizer or a judge will actually make.
- **A committed slot with a named third party**: a partner meeting, a program place, a block of office hours.
- **Capital as the prize**: an investment, a convertible instrument, or any award carrying equity.

- value, what the winner can actually use: `capital > committed slot > committed introductions > recognition only`
- value, deliverability (the winner receives what was announced, and receives it): `recognition only > committed introductions > committed slot > capital`
- effort (securing the commitment in writing, coordinating a third party, chasing delivery after everyone has gone home): `capital > committed slot > committed introductions > recognition only`
- compliance cost, as the review it triggers and the reversibility it costs: `capital > committed slot > committed introductions > recognition only`
- efficiency: `committed introductions > recognition only > committed slot > capital`

The deliverability axis is the one a pitch-contest organizer forgets, because the party promising the award is enthusiastic in the room and absent three months later.

- Recognition is delivered on stage by you alone.
- An introduction is one message you control.
- A committed slot depends on somebody else's calendar.
- Capital depends on a process: diligence, documents, a decision the announcer may not personally hold. It is the one award that can be announced and then simply not happen.

This is `samber/dev-event-organizer-skills@hackathon-cash-prize`'s own warning about its opportunity rung, extended into a full axis. Its catalogue does not transfer wholesale, and it is not empty here either: its opportunity rung already names an investor introduction and a seed-funding pitch, so the introductions rung below is shared ground. Capital itself is the part it has no rung for.

**Dominance check, re-derived: 6 pairs, zero strict-dominance relations, one mechanism covering all six.**

- The two value axes are exact reverses of one another, so in every pair the rung ahead on usable value is behind on deliverability, and no rung can be at least equal on both.
- The cost axes are never reached in any pair, worth stating rather than leaving implied.
- Distrust that mechanism rather than reading it as a pass: deliverability is rank-identical to inverse effort _and_ to inverse compliance, so it discriminates nothing the cost axes do not already say, and makes the check vacuous twice over. It stays because it names a real risk, not because it decides anything.

The ordering rests on the arguments below.

- **Committed introductions - the default.** The one rung whose value is specific to this population and whose delivery you control end to end: a list of named people who already agreed, and one message each, sent by a date you publish alongside the award. Consent runs both ways: the person on the receiving end has to agree to the introduction as well.
- **Recognition only.** Near-zero on every axis and a legitimate structure rather than a failure, exactly as the cash-prize sibling argues for its own recognition rung. Correct wherever the contest's purpose is the stage rather than the award.
- **A committed slot with a named third party.** Real value, and its whole cost is that somebody who is not you has to do something months later. Get the commitment in writing before it is announced, with a named person and a date, or you have announced somebody else's intention.
- **Capital as the prize - the starved option.** Top of usable value, bottom of deliverability, top of effort and top of compliance cost, so efficiency never picks it.
  - **Delete it, from this menu and from the axis lines above, when Q5 says no party has committed it in writing**: an award that fails is bad, and an award of capital that fails is a company that made decisions on it.
  - **Promotion condition, keyed to Q6:** placing that capital is the reason the contest exists rather than a prize attached to a contest that would run anyway. When that is the answer, the award is the point and efficiency has no vote on it, but the first gate below fires regardless.

## Three gates

The efficiency ranking gets no vote on these. Each gate is an obligation rather than a preference, so it decides the response instead of being weighed against effort. Efficiency then orders only what is left.

All three share a shape. Each fires on a single interview answer, and each has to be settled before the moment it protects: the announcement for Q6, the close of applications for Q7, the block itself for Q8.

- **Q6 - any award carrying capital, a convertible instrument or equity.** Route it to counsel before the award is announced.
  - **This skill states no securities threshold, no investment-law classification, no exemption name and no currency amount, ever.** This is the standing policy `samber/dev-event-organizer-skills@hackathon-cash-prize` sets for its own domain, adopted here for the same reason: a plausible-sounding threshold in a document telling an organizer how to structure an investment is worse than no guidance at all.
  - That sibling reached the same edge from the other side and stopped in the same place, finding that such an award "plausibly intersects employment or securities rules in some jurisdictions."
  - Contest-law classification is the second live category and routes the same way: whether the competition counts as a skill-based contest, or as something else, in the place it runs.
- **Q7 - a sponsor with a contractual say in who pitches or who wins.** This is not a rung on the conflict menu but the hard case. Handle it the way `samber/dev-event-organizer-skills@hackathon-judging` handles a sponsor judging its own track: confine the say to what was bought, and pair it with neutral judges. Check whether the result survives dropping those scores, and disclose the composition before applications close.
  - One line is not negotiable: "no speaker spots can be bought by sponsors: not ever - period" (DevOpsDays organizing guide).
  - A stage slot in front of investors is a speaking slot, and it is not for sale.
- **Q8 - recording, streaming or press in the room that applicants were not told about.** You cannot retrofit this: either the room is not recorded, or every applicant is told and re-consents before the block. On a pitch stage a founder says things whose distribution they control exactly once.

## Failure modes

- **Importing the hackathon conflict rule unchanged.** Recusal answers a sponsor's interest in the outcome. It does not answer a judge's interest in the access, and access is what an investor judge came for.
- **Designing the funnel before the prize.** What is on offer decides who applies. Funnel-first designs a pipeline for an award nobody has agreed to fund.
- **Weighting a criterion no judge can reach.** Traction, retention and margin are claims, verified in the application or not at all. A rubric weighting them with nothing to check them against scores a pitch's confidence.
- **Announcing an award a third party has not committed in writing.** Enthusiasm in the room is real and is not a commitment. The failure is public, it lands on the winner, and it lands after everyone has gone home.
- **Letting a sponsor buy a pitching slot.** The same transaction as buying a speaking slot, which the published line above forbids without qualification.
- **Re-deriving the judge-coverage arithmetic.** It already exists, worked through. A second copy is a second thing to keep correct and a chance to get it wrong.
- **Building a meeting-booking mechanic.** Once the design grows slots, confirmations and a quota, it is another skill's job. Route it.
- **Treating a demo day as a hackathon with better slides.** No build phase means no window to rescue anything, and nothing at the event improves what is judged.
- **Letting an unpublished technical preference decide the result.** An organizer or judge's private enthusiasm for one technical approach - deeper engineering over a thin wrapper, say - shapes who wins even when it never became a published criterion. A company that optimized against the published list then loses to one nobody could have known to match.

## Measurement

**Pass threshold (structural, one only): before the call goes public, all six of these exist in writing with zero blanks.**

- The published route onto the stage.
- The criteria with their weights.
- The pitch format with the block it fits inside.
- The conflict rule with what it does and does not cover.
- The award list with the party who committed each item.
- The answers to all three gates.

Iterate until the count is six.

Signals worth recording afterwards, all self-set:

- Award items delivered against award items announced, per party.
- Declared judge interests against interests that surfaced later.
- Applications from companies nobody on the team already knew, as the only read on whether the funnel did anything an invitation list would not have.
- Any question a founder asked on the day that the call should have answered.

Pick two or three and write down the revision each would trigger.

One warning carries over from the call this funnel is modelled on: widening the pool is an outreach job, not a review job. The DevOpsDays organizing guide states that "under-represented people in tech are much less likely to respond to your CFP", and an open call alone will not fix a slate outreach never reached.

## Invocation examples

- "We're adding a startup pitch contest to our conference. How do companies get on the stage?"
- "Three of our judges are VCs and one wants to invest in a company that pitched. What should we have written down?"
- "A sponsor wants to fund the prize and pick two of the pitching companies. Can they?"
- "The winner gets a meeting with a partner at the fund sponsoring us. What has to be agreed before we announce that?"
- "How long should each pitch be, and how many companies fit in our block?"

Expected output: a contest design with:

1. The award list with each item's committing party and written status.
2. The funnel with its published route written as a sentence, plus criteria and weights.
3. The pitch format with the block arithmetic consumed from `samber/dev-event-organizer-skills@hackathon-judging` and its inputs re-measured for a stage.
4. The rubric split into observed and claimed.
5. The conflict rule with what it covers and what it does not.
6. The three gates answered and routed.
7. The announcement and contest path.

Presented section by section for validation before the call goes public, every borrowed or self-set element flagged as such, and none of the seven banned quantities stated anywhere.

## References

- [references/application-and-slate-mechanics.md](references/application-and-slate-mechanics.md) - the published route as a sentence, the application field list with each field's purpose and which are custody-bearing, the criteria-in-the-call template, the screening call and its limits, the timeline anchors, and a published-route pair.
- [references/pitch-block-and-rubric.md](references/pitch-block-and-rubric.md) - the observable-versus-claimed split, a worked rubric naming each dimension's verification source, how to consume `samber/dev-event-organizer-skills@hackathon-judging`'s allocation formulas without re-deriving them, the tie-break ladder, and a scoring pair.
- [references/investor-conflict-and-prize-policy.md](references/investor-conflict-and-prize-policy.md) - the conflict ladder in detail with the judge brief wording, the sponsor hard case, the contact protocol as publishable text, the award-commitment checklist, the routing ladder for the three gates, and the full gap list.

See also, same collection:

- `samber/dev-event-organizer-skills@event-run-of-show` - runs the block on the day against the format fixed here.
