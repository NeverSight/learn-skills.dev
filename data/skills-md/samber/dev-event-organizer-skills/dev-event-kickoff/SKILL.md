---
name: dev-event-kickoff
description: Before answering any event-organizing request that opens a new project or a new session, run this router first - it maps the task onto the 71-skill samber/dev-event-organizer-skills collection, or says plainly that none fits, and bootstraps or resumes the project's shared context so the next session starts warm. This fires on a conversational state, not on a subject - invoke it at every event project start even when the collection's skills are already in daily use on another event, at every recurring check-in on the same project, and whenever routing between siblings is unclear. Covers conference, meetup and hackathon kickoffs, "which event skill do I need", "where do I start organizing this event", event organizer skill routing, and recurring event check-ins. Use this whenever someone describes an event-organizing problem without naming a skill, even if they never say "kickoff", "routing" or "start".
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Dev Event Kickoff

You are the entry point and router for the 71-skill dev-event-organizer-skills collection. Route the current task to exactly one sibling skill, or say plainly that none fits, and make the next session start warm instead of cold. Routing is the reason this skill exists; everything else serves it.

The collection is too large for its own members to see each other. An organizer inside `event-sponsor-pricing` cannot know the number it needs came from `event-budget`, or discover `event-b2b-matchmaking` at all. Solving that discovery problem is the whole job.

Run this skill at every project start, even when the collection is already in daily use on another event: a new event is a new context. On later sessions of the same project, re-run to resummarize and re-route, never to re-interview.

## 1. Detect before asking

Every fact you derive from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold versus warm start from one signal only: does the context artifact `event-context.md` exist in the project? Present → warm start. Absent → cold start. Never ask the user which one it is.
2. If you can read the project's git history, read the recent log to infer stage and pace: what changed last, whether event work stalled, how close the last commit sits to a dated milestone.
3. Inventory existing files - README, agent-instruction files, a budget spreadsheet, a submissions export, a rate card, a schedule grid, a venue contract, a risk register. A committed rate card fixes the sponsorship state; a published grid fixes the format and the date at once.
4. If your harness exposes connectors - a git host, a calendar, a mailing or ticketing source, an analytics source, a document store - detect which exist and let them shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships readable version metadata, note what changed since the last session; otherwise degrade silently. Never block or ask about versions.

## 2. Interview - capped, tappable

On a cold start, ask at most 5-7 questions, one question per message, and offer multiple-choice options whenever possible. Spend questions only where detection came up empty; skip whatever the file inventory or git log already answered.

1. **Which block is this session in?** - (a) the event does not exist yet, or you are deciding whether to run it, (b) decided and being planned, (c) doors open within weeks, or you are on site, (d) it has finished, (e) planning edition N of something that already ran. This is the fork: it selects which routing blocks in § 3 are live, and every later question narrows inside it.
2. **Is the format fixed - shape, track count, delivery mode - and where is that written?** - (a) nothing fixed, (b) shape fixed, the rest open, (c) fully fixed: name the shape, the track count and in-person / virtual / hybrid. Answers (a) and (b) mean the format gate cannot be applied yet.
3. **One-off or edition N, and how many properties does the team run?** - (a) first edition of something new, (b) one-off, not meant to recur, (c) edition 2 or later, (d) more than one property, or weighing whether to add one. Sets the lifecycle gate; (d) also opens the portfolio gate, whatever edition the flagship is on.
4. **Who funds it and who organizes it?** - (a) volunteer community organizers, (b) a company funding and owning its own event, (c) a foundation or non-profit, (d) mixed. Sets the company gate and shapes how much of the budget sponsorship carries.
5. **What is the goal of this session - and is it the same as the project's goal?** Ask on both cold and warm starts; a project goal never substitutes for today's goal.
6. **Is there a date the result has to land by?** - (a) doors open on a fixed date, (b) a CFP, on-sale or announcement deadline, (c) a sponsor budget window that closes, (d) no date. Give the date in cases (a) to (c).
7. **One-off outcome or a standing system - and what is your effort ceiling?** - (a) one-off, hours only, (b) one-off, a week of work is fine, (c) standing, a few hours weekly, (d) standing, with paid staff or a funded budget.

Questions 6 and 7 exist to order the output, not to describe the project: the landing date, the one-off-versus-standing answer, and the effort ceiling re-rank the short-list (§ 4) and the routines (§ 7). Ask them here, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact so the warm start re-ranks without re-asking.

On a warm start, ask only question 5. Everything else - including the gates and the two ranking inputs - comes from the artifact.

## 3. Route the task

Match the stated session goal against the declared scope of each skill below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap.

These tables are deliberately unranked, and must stay that way. Scope is a match test, not a ratio: a task either falls inside a skill's declared scope or it does not, so ordering the rows would invent a preference between skills that never compete. Ranking belongs one step later, in the short-list (§ 4).

Rows follow the decision sequence an organizer moves through, because that is the order questions arrive in. Question 1's answer selects which blocks are live: (a) opens A-B, (b) opens B-I, (c) opens J-K, (d) opens L, (e) opens M plus whichever of A-K the next edition reopens.

**Gate column.** A gate names the condition under which a row is reachable at all:

- `hackathon`, `virtual`, `hybrid`, `in-room`, `conference`, `workshop` - from the format decision (Q2).
- `first`, `recurring`, `properties` - from the lifecycle answer (Q3); `company` - from the funding answer (Q4).

A blank gate means the row is always reachable. Full matrices, including what to do when Q2 came back unfixed, are in [`references/format-and-lifecycle-gates.md`](./references/format-and-lifecycle-gates.md).

### A. Does this event exist, and what is it?

| Skill                                                        | Route here when the task is…                             | Gate       |
| ------------------------------------------------------------ | -------------------------------------------------------- | ---------- |
| `samber/dev-event-organizer-skills@event-market-fit`         | Whether concept, audience and price meet real demand     |            |
| `samber/dev-event-organizer-skills@event-positioning`        | What it stands for, for whom, against which alternatives |            |
| `samber/dev-event-organizer-skills@event-cultural-identity`  | The register, and its expression at every touchpoint     |            |
| `samber/dev-event-organizer-skills@event-first-edition`      | Scoping and launching edition one from zero              | first      |
| `samber/dev-event-organizer-skills@corporate-event-strategy` | What the company is funding this event to accomplish     | company    |
| `samber/dev-event-organizer-skills@event-portfolio-strategy` | Several properties shaped into a set that feeds itself   | properties |

### B. What shape does it take?

| Skill                                                                | Route here when the task is…                             | Gate     |
| -------------------------------------------------------------------- | -------------------------------------------------------- | -------- |
| `samber/dev-event-organizer-skills@event-format-selection`           | Shape, track count, session mix, delivery mode           |          |
| `samber/dev-event-organizer-skills@business-event-formats`           | Which company-run shape: dinner, summit, roadshow, floor | company  |
| `samber/dev-event-organizer-skills@workshop-program-design`          | How a hands-on session or lab actually runs              | workshop |
| `samber/dev-event-organizer-skills@event-learning-expedition-design` | Taking the audience into a host's own premises           |          |
| `samber/dev-event-organizer-skills@hybrid-event-design`              | Serving a room and a remote audience at once             | hybrid   |
| `samber/dev-event-organizer-skills@virtual-event-production`         | Delivering an event that has no room at all              | virtual  |

### C. When and where

| Skill                                                       | Route here when the task is…                       | Gate    |
| ----------------------------------------------------------- | -------------------------------------------------- | ------- |
| `samber/dev-event-organizer-skills@event-date-selection`    | Picking the date every other plan hangs off        |         |
| `samber/dev-event-organizer-skills@event-planning-timeline` | The work-back plan from doors-open, track by track |         |
| `samber/dev-event-organizer-skills@event-venue-sourcing`    | Finding, visiting and negotiating the room         | in-room |
| `samber/dev-event-organizer-skills@event-vendor-sourcing`   | Suppliers the venue does not include               |         |

### D. Who runs it, under what rules

| Skill                                                          | Route here when the task is…                          | Gate      |
| -------------------------------------------------------------- | ----------------------------------------------------- | --------- |
| `samber/dev-event-organizer-skills@event-code-of-conduct`      | The policy and the enforcement pipeline behind it     |           |
| `samber/dev-event-organizer-skills@event-risk-management`      | Risk register, insurance stack, go/no-go dates        |           |
| `samber/dev-event-organizer-skills@event-volunteers`           | Recruiting, rostering and briefing day-of volunteers  |           |
| `samber/dev-event-organizer-skills@event-volunteer-experience` | Volunteer care off-shift, thanks, the alumni list     |           |
| `samber/dev-event-organizer-skills@event-team-structure`       | The standing team and its governance between editions | recurring |

### E. Money in - budget and tickets

| Skill                                                    | Route here when the task is…                                | Gate |
| -------------------------------------------------------- | ----------------------------------------------------------- | ---- |
| `samber/dev-event-organizer-skills@event-budget`         | Cost lines, revenue mix, break-even, contingency, cash flow |      |
| `samber/dev-event-organizer-skills@event-ticket-pricing` | The ticket ladder, access rungs, refund and transfer policy |      |

### F. Money in - sponsorship

| Skill                                                               | Route here when the task is…                           | Gate |
| ------------------------------------------------------------------- | ------------------------------------------------------ | ---- |
| `samber/dev-event-organizer-skills@event-sponsor-value-proposition` | What each sponsor segment genuinely buys, and why      |      |
| `samber/dev-event-organizer-skills@event-sponsor-pricing`           | The rate card, its tier ladder and its discount policy |      |
| `samber/dev-event-organizer-skills@event-sponsor-prospectus`        | The published packages document sponsors read          |      |
| `samber/dev-event-organizer-skills@event-sponsor-outreach`          | Target list through to a signed yes, and renewals      |      |
| `samber/dev-event-organizer-skills@event-sponsor-agreement`         | The term sheet counsel reviews before signature        |      |
| `samber/dev-event-organizer-skills@event-sponsor-fulfillment`       | Delivering what was signed, then the renewal case      |      |

### G. Programme - the talks lane

| Skill                                                           | Route here when the task is…                       | Gate |
| --------------------------------------------------------------- | -------------------------------------------------- | ---- |
| `samber/dev-event-organizer-skills@event-cfp-design`            | Writing and timing the published call for papers   |      |
| `samber/dev-event-organizer-skills@event-talk-selection`        | Reviewing and choosing what the call brought in    |      |
| `samber/dev-event-organizer-skills@event-speaker-sourcing`      | Finding and qualifying speakers outside the call   |      |
| `samber/dev-event-organizer-skills@event-speaker-cold-outreach` | The invitation to a speaker already shortlisted    |      |
| `samber/dev-event-organizer-skills@event-speaker-experience`    | From acceptance through to the post-talk thank-you |      |
| `samber/dev-event-organizer-skills@event-schedule-design`       | Laying selected sessions into a published grid     |      |

### H. Programme - the competition lane

| Skill                                                        | Route here when the task is…                                   | Gate      |
| ------------------------------------------------------------ | -------------------------------------------------------------- | --------- |
| `samber/dev-event-organizer-skills@hackathon-brief-design`   | The challenge document and rules teams build against           | hackathon |
| `samber/dev-event-organizer-skills@hackathon-team-formation` | How participants end up on teams, and when it freezes          | hackathon |
| `samber/dev-event-organizer-skills@hackathon-mentoring`      | Mentor coverage and how a stuck team reaches help              | hackathon |
| `samber/dev-event-organizer-skills@hackathon-judging`        | The rubric, judge allocation and the scoring process           | hackathon |
| `samber/dev-event-organizer-skills@hackathon-cash-prize`     | What is awarded, and who may lawfully receive it               | hackathon |
| `samber/dev-event-organizer-skills@startup-pitch-contest`    | A pitch contest or demo day for companies that already existed |           |

### I. Fill the room

| Skill                                                              | Route here when the task is…                        | Gate       |
| ------------------------------------------------------------------ | --------------------------------------------------- | ---------- |
| `samber/dev-event-organizer-skills@event-marketing-plan`           | Segments, channels, campaign calendar, budget split |            |
| `samber/dev-event-organizer-skills@event-landing-page`             | The public front door and its date-gated CTA states |            |
| `samber/dev-event-organizer-skills@event-social-media`             | The event's own channels, inside the plan's weight  |            |
| `samber/dev-event-organizer-skills@event-attendee-email-sequences` | The dated email arc, its cadence and its copy       |            |
| `samber/dev-event-organizer-skills@event-media-partnerships`       | Barter visibility deals with media and communities  |            |
| `samber/dev-event-organizer-skills@cross-event-promotion`          | Reciprocal swaps with other organizers' events      |            |
| `samber/dev-event-organizer-skills@event-press-relations`          | Earned coverage, accreditation, the press room      | conference |
| `samber/dev-event-organizer-skills@event-no-show-management`       | Overbooking, waitlist, walk-ins, the real headcount |            |

### J. Care on site, by population

| Skill                                                             | Route here when the task is…                                          | Gate       |
| ----------------------------------------------------------------- | --------------------------------------------------------------------- | ---------- |
| `samber/dev-event-organizer-skills@event-attendee-experience`     | Check-in, badges, wayfinding, help, first-timers                      | in-room    |
| `samber/dev-event-organizer-skills@event-accessibility-inclusion` | Which access provisions the event commits to, and how requests arrive |            |
| `samber/dev-event-organizer-skills@event-hospitality`             | Catering, breaks, alcohol posture, whether an evening exists          | in-room    |
| `samber/dev-event-organizer-skills@event-booth-experience`        | Expo floor layout, tier specs, load-in schedule                       | conference |
| `samber/dev-event-organizer-skills@event-b2b-matchmaking`         | Structured 1:1 business meetings inside the grid                      | conference |
| `samber/dev-event-organizer-skills@event-vip-management`          | Named guests creating escort or protocol obligations                  | conference |
| `samber/dev-event-organizer-skills@event-official-social-program` | How many official social slots, and their inclusion floor             | conference |
| `samber/dev-event-organizer-skills@event-vip-social-program`      | The private gathering beside the public programme                     | conference |

### K. The day itself

| Skill                                                             | Route here when the task is…                          | Gate    |
| ----------------------------------------------------------------- | ----------------------------------------------------- | ------- |
| `samber/dev-event-organizer-skills@event-run-of-show`             | The minute-by-minute playbook staff execute from      |         |
| `samber/dev-event-organizer-skills@event-production`              | Capture tier, signal path, AV crew, redundancy        | in-room |
| `samber/dev-event-organizer-skills@event-comms-channels`          | Which attendee channel carries which class of message |         |
| `samber/dev-event-organizer-skills@event-side-event-coordination` | Approving third-party satellites around your dates    |         |

### L. After the doors close

| Skill                                                            | Route here when the task is…                        | Gate      |
| ---------------------------------------------------------------- | --------------------------------------------------- | --------- |
| `samber/dev-event-organizer-skills@event-feedback`               | What participants are asked, through what, and when |           |
| `samber/dev-event-organizer-skills@event-debrief`                | The organizing team's own blameless retrospective   |           |
| `samber/dev-event-organizer-skills@event-content-repurposing`    | Turning captured material into published artifacts  |           |
| `samber/dev-event-organizer-skills@event-continuous-improvement` | Trends across several editions' debrief logs        | recurring |

### M. Between editions

| Skill                                                            | Route here when the task is…                           | Gate      |
| ---------------------------------------------------------------- | ------------------------------------------------------ | --------- |
| `samber/dev-event-organizer-skills@event-community-building`     | The event's own audience in the gaps between editions  | recurring |
| `samber/dev-event-organizer-skills@event-growth-strategy`        | Grow edition over edition, or deliberately not         | recurring |
| `samber/dev-event-organizer-skills@tech-podcast-youtube-channel` | A standing show or channel as a cross-edition property | recurring |

### Meta

| Skill                                                 | Route here when the task is…                                                      | Gate |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- | ---- |
| `samber/dev-event-organizer-skills@dev-event-career`  | Candidate side - breaking into event organizing, interview prep, offer evaluation |      |
| `samber/dev-event-organizer-skills@dev-event-hiring`  | Employer side - job posting and scorecard, interview loop, sourcing, compensation |      |
| `samber/dev-event-organizer-skills@dev-event-kickoff` | This skill: project start, check-in, "which skill do I need", re-routing          |      |

**Three rows are deliberately narrow and are leaf routes, never starting points.** `event-learning-expedition-design` defers catering to `event-hospitality` and multi-venue logistics to `event-production`; `event-official-social-program` defers a single occasion's food, drink and format to `event-hospitality`; `event-vip-social-program` defers whether a guest qualifies at all to `event-vip-management`. Route to them only when the task is exactly the sliver they keep; presenting one as load-bearing misleads worse than leaving it out.

**Read the format decision; never re-decide it.** `event-format-selection` owns the shape, the track count and the delivery mode. When Q2 came back (a) or (b), route there and stop: every gated row stays unreachable until it returns. When it came back (c), carry the answer as the gate column and never revisit it. `hybrid-event-design` and `virtual-event-production` sit downstream of that decision and never make it.

Disambiguate strictly from each skill's declared scope - never from a guess about what a skill "probably" covers. Read [`references/skill-routing.md`](./references/skill-routing.md) for the boundary pairs and the ordered chains before routing any task that could plausibly match two skills.

Before naming a gap, check whether the task belongs to a sibling `samber` collection: developer content, docs, open-source strategy or an always-online community recommends `samber/developer-relations-skills`; a public API, SDK, webhook or app-marketplace question recommends `samber/developer-platform-skills`. Frame either as a recommendation, never a dependency - this collection stays usable standalone.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact: event identity and format, the date and where it sits, in-flight work, top open decision, active constraint.
2. **Route** - the one skill for the immediate task (or "no skill fits", plus the named gap).
3. **Short-list** - 5 to 8 skills relevant right now, ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness, never by the routing table's row order.
4. **Chain** - when the task genuinely decomposes, list the sequence in execution order, one line per link on what it hands the next. Chain order is dependency order, not efficiency order. Omit the chain when there is not one; never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (for example, "`event-schedule-design` - after `event-talk-selection` returns an accepted list").
6. **Gap** - anything today's task needs that no skill covers. When the gap is DevRel practice or platform surfaces, recommend the matching sibling repo instead of a bare gap statement.

### Ordering the short-list

The user's question is never "which of these exists" but "which one do I run first, and is it worth the session", and only a ratio answers that. The nine classes below, and the four axis orderings under them, are this skill's own construction, not a published taxonomy. Default class order, highest value per unit of effort first:

1. **Existence check** - `event-market-fit`, `event-positioning`, `corporate-event-strategy`, `event-cultural-identity`, `event-first-edition`. Buys the verdict on whether this event should run and what it is, which can delete every class below it. Costs sessions spent reading signals that already exist; nothing booked, published or signed.
2. **The spine** - `event-format-selection`, `event-date-selection`, `event-planning-timeline`, plus the shape skills downstream of them (`business-event-formats`, `workshop-program-design`, `event-learning-expedition-design`, `hybrid-event-design`, `virtual-event-production`). Buys the three decisions every other class then works inside. Costs a session each plus a calendar scan; an announced date is reversible only at a public cost.
3. **Fill the room** - `event-marketing-plan`, `event-landing-page`, `event-social-media`, `event-attendee-email-sequences`, `event-no-show-management`, `event-press-relations`, `event-media-partnerships`, `cross-event-promotion`. Buys registrations, the input every other class assumes. Costs a campaign from announcement to doors, plus the list consent you then owe.
4. **Money model** - `event-budget`, `event-ticket-pricing`. Buys break-even as a number with a date instead of a hope. Costs a modelling session; a published refund policy binds once tickets sell.
5. **Programme intake** - the talks lane (`event-cfp-design`, `event-talk-selection`, `event-speaker-sourcing`, `event-speaker-cold-outreach`, `event-speaker-experience`, `event-schedule-design`) and the competition lane (`hackathon-brief-design`, `hackathon-team-formation`, `hackathon-mentoring`, `hackathon-judging`, `hackathon-cash-prize`, `startup-pitch-contest`). Buys the content people came for. Costs an incompressible call window, a review committee, per-speaker logistics, and per-person consent.
6. **Place and duty of care** - `event-venue-sourcing`, `event-vendor-sourcing`, `event-code-of-conduct`, `event-risk-management`, `event-accessibility-inclusion`, `event-volunteers`, `event-volunteer-experience`, `event-team-structure`. Buys a room that holds the format, and commitments that survive an incident. Costs site visits, negotiation and a rehearsed response team, each reversible only on someone else's terms.
7. **On-the-day operations** - `event-run-of-show`, `event-production`, `event-comms-channels`, `event-attendee-experience`, `event-hospitality`, `event-side-event-coordination`, `event-booth-experience`, `event-b2b-matchmaking`, `event-vip-management`, `event-vip-social-program`, `event-official-social-program`. Buys the day the promise already sold gets redeemed. Costs crew, rosters and a physical build, compressed into days that cannot slip.
8. **Sponsorship sale** - `event-sponsor-value-proposition`, `event-sponsor-pricing`, `event-sponsor-prospectus`, `event-sponsor-outreach`, `event-sponsor-agreement`, `event-sponsor-fulfillment`. Buys the revenue line tickets rarely cover. Costs the most of any class: a months-long motion on a counterparty's calendar, counsel on the term sheet, and obligations owed until the event is over.
9. **After and between editions** - `event-feedback`, `event-debrief`, `event-content-repurposing`, `event-continuous-improvement`, `event-community-building`, `event-growth-strategy`, `event-portfolio-strategy`, `tech-podcast-youtube-channel`. Buys the next edition's starting position. Cheap per session, but the payoff lands after this cycle's finish line.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `existence check > spine > fill the room > money model > programme intake > place and duty of care > on-the-day > sponsorship sale > after and between`
- value: `programme intake > fill the room > sponsorship sale > spine > place and duty of care > on-the-day > after and between > money model > existence check`
- effort: `sponsorship sale > programme intake > fill the room > on-the-day > place and duty of care > after and between > spine > money model > existence check`
- compliance cost: `sponsorship sale > place and duty of care > programme intake > on-the-day > fill the room > after and between > money model > spine > existence check (none)` - a signed sponsorship carries exclusivity and a delivery obligation counsel reviews; a venue contract and an access commitment bind you on another party's terms; consent, prize eligibility and jury conflicts need deciding upfront; badge scanning and an approved satellite publish a posture you then owe; list consent and barter delivery are promises to third parties; a refund policy binds once tickets sell; an announced date is a public commitment. The existence check publishes, signs and books nothing.

**Cheap and efficient are different orderings, and this menu shows it twice.** Fill-the-room outranks the money model on efficiency while costing more, since a campaign converts hours into the input every class assumes, and a break-even number seats nobody. After-and-between is near the cheapest class and ranks last, since efficiency is scored inside the current cycle and that class pays the next one.

**Dominance audit, at its point of use.** Nine classes yield 36 unordered pairs. Six carry no trade-off - one class is both more valuable and cheaper - and each gets its own mechanism rather than sharing one:

- _Programme intake over sponsorship sale_, and _fill the room over sponsorship sale_ - **prerequisite inversion**: sponsors buy access to an audience and a programme, so both must exist first; the dominance is sequencing, not preference.
- _Spine over place and duty of care_, _spine over on-the-day_, and _spine over after and between_ - **upstream-decision leverage**: shape, date and timeline are inputs to all three, so a changed date restarts the venue search and a changed shape makes the run of show and retrospective describe a different event.
- _Place and duty of care over on-the-day_ - **the room precedes the day**: the venue contract, code of conduct, roster and risk register are what the day executes, so a run of show written before the room is known gets rewritten.

The criterion weighs value against effort only. This last pair inverts on compliance cost - the contracts and published commitments sit on the room's side, not the day's - so a reader bound by sign-off rather than hours picks it the other way round.

The other 30 pairs each split at least one axis against efficiency, so the ordering does work on them. The efficiency line is also not rank-identical to inverse effort, which would read `existence check > money model > spine > after and between > place and duty of care > on-the-day > fill the room > programme intake > sponsorship sale`, agreeing only at the first position. Matching lines would have collapsed the ranking into cheapest-first.

**What this order starves: the sponsorship sale.** Third on value, eighth on efficiency, the widest gap in the set, because its cost is set by a counterparty's calendar. Left unpromoted, a ratio-first order fills a room for an event whose budget never closes.

Promotion conditions: Q7 (c) or (d), standing weekly hours or funded staff, promotes it to rung 2, since only a standing team can pay a months-long motion; Q6 (c), a closing sponsor budget window, promotes it to rung 1 regardless, since that window does not reopen this cycle.

Delete a ruled-out class; never demote it to last place, because one parked at the bottom silently reappears as scope. A class with an unblocking condition moves to "not now" carrying it; one with none goes unmentioned.

The ordering is a default, not a law. Re-rank against what the interview and detection just told you, and say out loud which answer moved which class:

- Q1a (does not exist yet) promotes the existence check to rung 1 and deletes sponsorship sale and on-the-day - nothing to sponsor, no day to run.
- Q1c (doors within weeks, or on site) promotes on-the-day to rung 1 and deletes the existence check and after-and-between; Q1d (finished) inverts that, reducing the short-list to after-and-between alone. Deleted, not demoted, in both cases.
- Q2a or Q2b (format not fixed) collapses the session to one route - `event-format-selection` - and suspends every gated row.
- Q3a (first edition) promotes `event-first-edition` to rung 1 and deletes after-and-between's cross-edition entries - no prior edition to read.
- Q3d (more than one property) promotes `event-portfolio-strategy` out of after-and-between to rung 2 - a collision between properties is decided before either one's own plan.
- Q4a (volunteer organizers) deletes `corporate-event-strategy` and `business-event-formats`, and promotes the sponsorship sale, since ticket revenue rarely closes the budget alone.
- Q4b (a company funds and owns it) promotes `corporate-event-strategy` to rung 1 and demotes the sponsorship sale.
- Q6a (doors on a fixed date this cycle) promotes fill-the-room, programme intake and on-the-day, and moves after-and-between to "not now".
- Q6b (a CFP or on-sale deadline) promotes whichever of programme intake or the money model owns that deadline, above fill-the-room.
- Q7a (one-off, hours only) cuts the short-list to the existence check and the spine, and deletes sponsorship sale and on-the-day.
- Q7d (standing, with staff or budget) promotes the sponsorship sale and place-and-duty-of-care above their default places.
- Detection moves classes too: a committed budget makes the money model near-free; a published grid deletes `event-schedule-design`; a signed venue contract deletes `event-venue-sourcing` and promotes `event-risk-management`.

## 5. Context artifact

Create or update `event-context.md` at the project root - one versioned file, committed with the project when it lives in git. It is the single source of truth that makes the next start warm, and where a warm start reads its gates.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with its invariants - format, date, funding model - so future sessions inherit them without loading this skill.
- Do not scaffold a working tree the project has not earned; premature structure hard-codes decisions it has not made.
- Keep a decision log only when the project accumulates contested decisions; otherwise the decided-versus-open field is enough.
- Archive the previous edition's artifact before starting edition N; never overwrite it. The debrief and the trend read both need what the last edition decided.

Fields, a worked example and a negative example are in [`references/context-artifact.md`](./references/context-artifact.md). Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If your harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses after the interview completes and before the § 4 output: write the answers into the context artifact first, then derive the memory entry from it. Never write memory straight from an answer, however obvious the answer felt.

Memory lives in exactly one of three places, and all three need the same index file listing each entry with a one-line hook. Pick from this order, highest value per unit of setup effort first:

1. **A `memories/` directory in the project's git repository.** Setup is a directory and an index file, co-organizers read it where they already read the plan, and every change arrives as a reviewable diff.
2. **A team knowledge base.** Reaches volunteers, sponsor contacts and venue staff who never open a repository. Costs an access setup outside the organizing team, and it drifts because nothing ties a page to a commit.
3. **Local to the user's environment.** Near-zero setup, and nobody else can read it. Use it only when one person organizes alone - a per-user store forks the project state the moment a second organizer joins, and organizer turnover is the failure this collection returns to most.

- efficiency: `git repository > team knowledge base > local environment`
- reach: `team knowledge base > git repository > local environment`
- setup effort: `team knowledge base > git repository > local environment`

Default to the git repository whenever the project already lives in one; choose the knowledge base when the people who need the memory do not work in it.

- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - the artifact wins by default; ask before overwriting either.
- Never put into memory: attendee or speaker personal data of any kind, accommodation requests and the conditions behind them, code-of-conduct reports and the identities in them, negotiated sponsor and venue rates, and any contract term still under negotiation. State this exclusion when you first write memory.
- When memory lives in a git repository, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If your harness supports scheduled routines, propose 2 to 4, each shown to the user as a dry-run first and each with an explicit output channel - a routine without one is noise the user silences within a week. A routine's cost is not its setup but its attention per firing times how often it fires; its value is the decision it puts in front of someone while that decision is still open. Rank on that ratio, highest first, and propose from the top down.

The six candidates below are this skill's own construction, not a standard routine set:

1. **Ticket-pace check** → `samber/dev-event-organizer-skills@event-market-fit`. Reads a number the ticketing system produces anyway, against a checkpoint the project already published. Only this routine can trigger a hold, pivot or stop while the money is still refundable.
2. **Work-back checkpoint** → `samber/dev-event-organizer-skills@event-planning-timeline`. Fires at each replanning checkpoint on the plan's own calendar. Its output cuts scope while that is still cheaper than moving the date.
3. **Kickoff re-invocation** → this skill. Costs near-zero per firing. Keeps the artifact and the routing current, which stops every other routine firing at work that no longer exists.
4. **Go/no-go review** → `samber/dev-event-organizer-skills@event-risk-management`. Anchored a step ahead of each rung of the venue's cancellation-fee curve, never at the rung. Carries the highest compliance exposure in the set: the decision is contractual and cannot be unsaid.
5. **Post-edition trend read** → `samber/dev-event-organizer-skills@event-continuous-improvement`. Fires once a debrief lands, reading several editions together. Cannot fire before two exist.
6. **Sponsor pipeline and renewal sweep** → `samber/dev-event-organizer-skills@event-sponsor-outreach`. Fires against the budget windows the pipeline already records. Carries the highest standing cost: every account it names needs a person to chase it.

- efficiency: `ticket-pace check > work-back checkpoint > kickoff re-invocation > go/no-go review > trend read > sponsor sweep`
- value: `go/no-go review > ticket-pace check > sponsor sweep > work-back checkpoint > trend read > kickoff re-invocation`
- effort: `sponsor sweep > go/no-go review > work-back checkpoint > trend read > ticket-pace check > kickoff re-invocation`
- compliance cost: `go/no-go review > sponsor sweep > ticket-pace check == work-back checkpoint == trend read == kickoff re-invocation (none)` - cancelling or postponing fires the venue's cancellation curve and an insurance claim, a decision counsel and a broker are both party to; the sweep's output names accounts and negotiated terms, so its channel must sit inside the project's data posture. The last four tie at zero because each reads an internal artifact - a sales figure, a timeline, a debrief log, a context file - publishes nothing outside the team, and needs no sign-off.

**Dominance audit, at its point of use.** Six routines yield 15 unordered pairs. Four carry no trade-off, each with its own mechanism:

- _Go/no-go review over sponsor sweep_ - **committed money beats uncommitted money**: the review protects spend already made on a contract-fixed date; the sweep chases revenue not yet promised, at a cost proportional to list length.
- _Ticket-pace check over sponsor sweep_ - **a read is not a job**: the pace check queries figures recorded regardless; the sweep produces the outreach itself and needs a human to send it.
- _Ticket-pace check over work-back checkpoint_ - **the instrument already exists**: pace is a query, a checkpoint requires the team to reassemble and re-cut scope, and pace fires earlier, inside the still-refundable window.
- _Ticket-pace check over trend read_ - **within-cycle beats across-cycle**: the pace check changes this edition; the trend read changes the next one and cannot fire until one has finished.

Same caveat as § 4: the criterion is value against effort, and the first of the four inverts on compliance cost - the go/no-go review is the only routine whose output is contractual. The other 11 pairs split at least one axis. The efficiency line is not rank-identical to inverse effort either: inverse effort would lead with the kickoff re-invocation, which sits third here.

**What this order starves: the sponsor sweep.** Third on value, last on efficiency, because its cost scales with the pipeline rather than with the firing.

Promotion conditions, keyed to Q6: answer (c), a closing sponsor budget window, installs it first; keyed to Q7: answer (d), funded staff, makes it affordable at its default place.

Default: rungs 1-3, which is three routines. Never exceed 4 - the cap protects the routines that matter from the ones that fire into the void.

Re-rank against the interview, and say which answer moved which routine:

- Q6a (a fixed doors date) installs the work-back checkpoint first; Q3a or Q3b (a first or one-off edition) deletes the trend read rather than demoting it, since there is no next edition to change, and Q3c or Q3d restores it.
- Q1a (the event does not exist yet) installs one routine only, the kickoff re-invocation; Q7a (one-off, hours only) does the same.
- A signed venue contract on disk promotes the go/no-go review to rung 1, since the cancellation curve is now real; no ticketing source detected deletes the ticket-pace check outright, because there is nothing to query.

Anchor every trigger to a date the event already has - the CFP close, the on-sale date, the venue's cancellation rungs, doors-open, the debrief - never to an arbitrary schedule, and give each routine a stop condition:

- Retire the previous edition's routines before adding new ones.
- If the harness has no scheduled routines, fall back to one recurring calendar reminder ("Event check-in - re-run the event organizer kickoff") and stop there. See [`references/routines.md`](./references/routines.md) for the dry-run format, calendar anchors and cleanup rules.

## 8. Coverage gaps

No skill in the collection covers these. Name the gap; never promise or invent a skill:

- **Registration and ticketing system operation** - platform choice, checkout, on-site box office, refund processing, tax treatment of revenue. `event-ticket-pricing` sets prices and writes the refund policy; `event-landing-page` wires the CTA to whatever system exists.
- **Conference proceedings and a paper track** - peer review ending in a published paper rather than a stage slot. `event-talk-selection` reviews talk proposals only.
- **A community awards programme** - nominations, a jury, an awards ceremony as a segment. `startup-pitch-contest` and `hackathon-judging` each judge one competition against its own entry rules; neither is an awards programme.
- **Running the programme in two languages** - translated tracks, a bilingual host, per-language labelling. `event-accessibility-inclusion` covers interpretation and captioning as access provisions on request, not a second language as a design choice.
- **Attendee travel and accommodation as a programme** - a negotiated hotel block, travel booking, visa invitation letters at attendee scale. `event-venue-sourcing` reads room-block terms inside the venue contract; `event-speaker-sourcing` flags visa lead time for one invited speaker only.

Out of scope by design, not gaps: attending an event rather than running one, sponsoring someone else's, exhibiting on a floor you do not own, and speaking at one.

## 9. Invocation examples

- "Start a new event project - we want to run our first hackathon next spring."
- "Which event skill do I need? Sponsors keep asking what they actually get."
- "Run my event check-in."
- "Where do I start? We have a date and a venue and nothing else."
- "The conference finished last week. What now?"

## 10. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it does not cover wastes a session and hides the gap. Say "none fits" and name the gap - or point at `samber/developer-relations-skills` or `samber/developer-platform-skills` when the task belongs to one of them.
- **Re-deciding the format.** The gates read `event-format-selection`'s answer; they never produce one. Routing "should we go hybrid" to `hybrid-event-design` hands the user a session that assumes the decision it was asked to make.
- **Applying a gate to an unfixed format.** When Q2 came back (a) or (b), every gated row is unreachable. Route to `event-format-selection` and stop, rather than guessing a shape to unlock rows with.
- **Promoting a leaf route.** The three deliberately narrow rows named in § 3 defer most of their subject to a sibling. Presenting one as load-bearing sends the user into a sliver when the sibling holds the decision.
- **Re-interviewing on a warm start, or exceeding the cap on a cold one.** The artifact exists so questions are not repeated; past seven questions the kickoff becomes a form the user abandons. Detection fills the gaps - a committed budget or a published grid answers more than any question does.
- **Routing from a guessed scope.** Route only from declared scopes; a plausible guess misroutes confidently.
- **Routing a lane, not a subject.** One lane splits on what is judged: work built during the event (`hackathon-judging`) versus companies that existed before it (`startup-pitch-contest`). Two split on which side of a boundary the user sits: your satellite programme versus another organizer's event (`event-side-event-coordination` versus `cross-event-promotion`), and your own channels versus another outlet's (`event-social-media` versus `event-media-partnerships`).
- **Routines with no output channel, or none that ever retires.** They fire into the void and get silenced, burying the one routine that mattered; an event has a finish line, so almost every routine needs a stop condition.
- **A flat short-list, or one led by the cheapest option.** Equal-looking options get picked by taste or by whichever sits first, and cheap is a different ordering from efficient.
- **Ranking the routing table or the chain.** Scope is a match test and a chain is a dependency order; imposing a ratio on either invents a preference that does not exist.
- **Demoting a ruled-out class instead of deleting it.** Parked at the bottom of the short-list, it reappears as scope two sessions later.
- **Memory committed silently, or carrying a person.** Co-organizers cannot review what they never see land, and attendee data, accommodation requests and conduct reports must never reach memory at all.
- **Stale routing table.** Update this skill - the tables, the gates, the reference files, the gap list - whenever the collection changes: a skill added, renamed, removed, or re-scoped. A stale router sends users to skills that no longer exist, which is worse than no router at all.

## 11. Pass bar

Before ending the session, check every item. Fix and re-check any that fails; never close on a failing bar.

1. Every recommended skill's declared scope matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the tables in § 3.
3. Every gate applied was read from an answer or an artifact, never inferred from the event's name or the user's tone.
4. The interview stayed within its cap: at most seven questions cold, only the session goal warm.
5. `event-context.md` was written or updated, with a session-log line, before the session ended.
6. Every proposed routine was shown as a dry-run and has an output channel and a stop condition.
7. The short-list and the routine set are both ordered by value per unit of effort, each entry naming the bottleneck it attacks and what it costs, with the re-rank stated out loud whenever an answer moved something off its default place.
8. Every ruled-out class left the short-list entirely, and the routing tables and any chain were left unranked.
