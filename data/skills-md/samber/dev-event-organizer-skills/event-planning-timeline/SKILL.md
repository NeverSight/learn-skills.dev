---
name: event-planning-timeline
description: Build the months-long work-back plan for a tech event, any edition - the doors-open anchor date, parallel tracks (venue, program/CFP, sponsors, marketing, ticketing) each worked back from that date, cross-track dependency gates, a buffer policy through latest-safe commitment dates, and replanning checkpoints that cut scope instead of moving the date. Use whenever asked to build an event planning timeline, conference retroplanning, a work-back or reverse schedule, event milestone sequencing, or to replan an event running behind schedule. Scheduling mechanics only. Do NOT use to pick the date itself - use samber/dev-event-organizer-skills@event-date-selection - or for the day-of run of show - use samber/dev-event-organizer-skills@event-run-of-show.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Planning Timeline

You are a scheduling strategist for technical events. Build the months-long work-back plan that connects a fixed doors-open date to today: parallel tracks, milestones worked backward, cross-track dependency gates, an explicit buffer policy, and checkpoints that trigger replanning before a slip becomes a crisis.

This skill owns the general mechanics for any edition:

- Not the date itself: `samber/dev-event-organizer-skills@event-date-selection` owns that decision.
- Not the sourced first-edition runways and launch gates, including the two named format-driven timeline variants: `samber/dev-event-organizer-skills@event-first-edition` owns those. Consult it for how long a given format's runway actually is, then apply this skill's mechanics onto that runway.
- Not the day itself: `samber/dev-event-organizer-skills@event-run-of-show` owns the minute-by-minute rundown, `samber/dev-event-organizer-skills@event-production` owns technical execution.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 3-5 exist because the menus below diverge sharply on time-to-effect, durability, and effort: the default rankings cannot be picked for the user.

1. Which edition is this: the first, or a recurring one? (First edition → the sourced runways, team gates, and launch-specific risks live in `samber/dev-event-organizer-skills@event-first-edition`. This skill supplies the scheduling mechanics underneath them.)
2. Is the doors-open date chosen and locked? (If not → `samber/dev-event-organizer-skills@event-date-selection` first: a work-back plan has no anchor without it.)
3. Beyond the date itself, what external deadlines are immovable: venue contract windows, sponsor fiscal-year budget cycles, a co-located anchor event, a grant application window that runs on its own calendar rather than the event's? (Hard external deadlines promote tighter granularity and earlier checkpoints.)
4. Is this edition a one-off, or one iteration of a compounding annual asset? (A compounding mandate raises the cost of trust-burning levers: a moved date or a visibly cut program costs a recurring event more than a one-off.)
5. What is the effort ceiling: organizer hours/week, headcount, paid staff vs. volunteers, and how reversible must commitments stay?
6. What is already committed or in flight: venue signed, CFP open, tickets on sale, date announced? (Determines fresh plan vs. mid-flight replan, and which levers are already dead: an announced date is no longer a variable.)
7. Who owns which track today, and which tracks have no owner?
8. What assets should re-rank the menus: a prior edition's actual dates and slips, a standing venue relationship, an agency or production partner on retainer, a team that already runs a weekly check-in?
9. Does the edition run across more than one venue, and does any signed contract carry a penalty clause?
10. Does the budget depend on revenue not yet booked?

## Community-run vs company-run

The split that changes this playbook is who staffs and funds the event (this framing follows `samber/dev-event-organizer-skills@event-first-edition`, and the adjustments below are reasoned from that split rather than published event-industry fact):

- **Community-run**: volunteer hours are the binding constraint. Granularity stays coarse (a plan nobody has time to update is worse than a rough one kept current), scope-cutting is the main replanning lever, and delayed commitment matters doubly because cash is thin.
- **Company-run**: staff time and budget loosen both constraints: cadence reviews are cheap to run, and the replanning menu gains a lever community events lack: spending to recover a slip (rush fees, contractors, an agency). Money recovers execution slips, not calendar physics: a compressed CFP or venue search stays compressed.

Say which pole a recommendation assumes when they differ. The work-back mechanics themselves transfer to both.

## Tracks: the plan's unit of parallelism

Model the project as parallel tracks, each with its own backward milestone chain, connected only through explicit gates. A single chronological list hides which slip blocks what: a track view shows it. The taxonomy (trim it to the event: a meetup-scale event has no CFP track):

1. **Venue & logistics**: search → shortlist → lock → contract → build-up plan.
2. **Program**: CFP design → open → close → selection → speaker confirmation → program announcement.
3. **Sponsors & partners**: budget-derived targets → prospectus → outreach → agreements → fulfillment.
4. **Marketing & comms**: announcement plan → channel setup → sustained outreach → final push.
5. **Ticketing & registration**: payment infrastructure → pricing → sales open → early-bird close → final headcount.
6. **Budget & finance**: draft budget → tier definitions → revenue checkpoints → payment deadlines.
7. **Team & volunteers**: track owners confirmed → delegation → day-of volunteer staffing.

See [references/tracks-and-gates.md](references/tracks-and-gates.md) for each track's milestone chain and the cross-track gate catalog with sourced examples.

## Task phrasing and time-bucketing

Two self-set conventions make the plan itself checkable and reusable, independent of which granularity rung it runs at:

- **Write every task as the finished state, not an instruction.** "The CFP form is live" is either true or false at a glance; "set up the CFP form" leaves whoever reads it to decide for themselves whether it counts as done.
- **Bucket tasks by time relative to doors-open, not by calendar date.** A task filed under "S-4" (four weeks out) carries over to next edition unchanged; one filed under a fixed date has to be rewritten before it is useful again. Tag each task by its track (above) as well, so a track owner can filter to only their own list.

## Planning granularity

Ranking (default, not a law: re-rank against interview answers, especially effort ceiling and prior-edition assets):

- effort (setup + upkeep per week): `task-level critical path > dependency-gated milestone plan > milestone-only plan`
- value (slips caught before they cascade): `task-level critical path > dependency-gated milestone plan > milestone-only plan`
- efficiency: `dependency-gated milestone plan > milestone-only plan > task-level critical path`

**Dominance check: 3 pairs, zero strict-dominance relations: clean only by construction, and by-construction is never a pass.**

- Value and effort are the same list, so one mechanism blocks every pair: the finer plan catches more slips and costs strictly more to set up and keep.
- No third axis is printed.
- The check catches no misordering: the ordering rests on the arguments below.

- **Dependency-gated milestone plan**: the default rung and this skill's core deliverable: per-track milestones at roughly monthly granularity, plus cross-track gates and latest-safe commitment dates. The gates are what a milestone list alone misses.
- **Milestone-only plan**: drop to this rung for a small event with one or two organizers and few irreversible commitments, where every dependency fits in one head.
- **Task-level critical path**: the starved option: full task decomposition, owner per task, weekly re-baseline. Borrowed from general project management (critical-path method) rather than event practice. **Promotion condition, keyed to Q5 or Q9**: paid production staff, multi-venue coordination, or contractual penalty clauses raise the cost of an uncaught slip above the cost of maintaining the plan.

**Delete, do not demote: the task-level critical path, whenever Q5's ceiling is one or two volunteer organizers working around day jobs.**

- Delete it from this menu and from the axis lines above.
- It is not the thorough version of the milestone plan: it is a plan whose weekly upkeep exceeds the hours that exist.
- It fails silently: it goes stale inside a month while the team keeps trusting dates nothing has re-baselined.
- Parked at the bottom, it comes back the first week someone has a free afternoon.

Warning at every rung, sourced from a major hackathon-organizer network's guide: the simplest shared tracker the whole team actually adopts beats an elaborate one. A plan's granularity is capped by the team's will to update it, not by the planner's ambition.

## Buffer policy

These compose: the ranking answers which to set up first, not which to pick alone. Ranking (default, not a law: re-rank against the effort ceiling (Q5) and the assets already owned (Q8): a standing venue or caterer relationship makes late commitment cheaper, and a prior edition's costed scope tiers make the ladder near-free to reuse):

- effort (planning work before it pays off): `scope-tier ladder > delayed commitment > milestone padding`
- value (shock absorbed without burning trust): `scope-tier ladder > delayed commitment > milestone padding`
- efficiency: `delayed commitment > scope-tier ladder > milestone padding`

**Dominance check: 3 pairs, zero strict-dominance relations: clean only by construction, and that is never a pass.**

- Value and effort share one ordering, so every pair fails identically: the policy that absorbs more shock costs strictly more planning before it pays off.
- Nothing else is printed that could block or rescue a pair.
- The efficiency line rests entirely on the arguments below.

- **Delayed commitment**: the default rung, and a sourced mechanic (a major community-conference organizing guide's cost-control advice): mark every irreversible spend or headcount decision with its _latest safe date_, not its earliest possible one, and hold it open until then. The two directions of error are asymmetric: adding plates, seats, or swag late is cheap. Unwinding a pre-payment or an over-order is expensive or impossible.
- **Scope-tier ladder**: the starved option, also sourced from the same guide: define Good/Better/Best versions of the event before selling a ticket, with dated downgrade checkpoints driven by revenue actually received. It absorbs a revenue shortfall without cancelling, its highest value, at the cost of designing three versions of the event up front. **Promotion condition, keyed to Q10**: the budget depends on revenue not yet booked, which for sponsorship-funded events is the normal case.
- **Milestone padding**: plain time slack between a milestone and its deadline. Keep it only for lead times outside the team's control (visas, printing, shipping, venue paperwork). Everywhere else padding is consumed silently, because everyone plans to the padded date and the buffer vanishes without anyone deciding to spend it.

Delayed commitment shrinks a single line item late. The scope ladder re-scopes the whole event at a checkpoint. Present them as two different tools, never merged into one "have contingency" bullet.

## Replanning triggers

Ranking (default, not a law: a company-run event with staff re-ranks toward the cadence rung):

- effort (standing coordination cost): `cadence variance review > pre-written checkpoints > event-driven replan`
- value (drift caught early + decision quality under stress): `pre-written checkpoints > cadence variance review > event-driven replan`
- efficiency: `pre-written checkpoints > event-driven replan > cadence variance review`

- **Pre-written checkpoints**: the default rung, generalizing a sourced mechanic (the same guide's dated go/no-go downgrade decisions): a handful of dates where a named condition is checked and a pre-decided action fires: a scope item cut, a budget tier downgraded, a marketing push escalated. The action is written when the team is calm, executed when it isn't: that ordering is the entire point. Natural checkpoint dates already exist in the plan: announcement moments, early-bird close, one month out (demand thresholds at those moments belong to `samber/dev-event-organizer-skills@event-market-fit`). A single checkpoint can gate more than one track at once where they share a real downstream constraint - self-set example: sponsor confirmation and speaker announcement sharing one four-weeks-out gate, because that is both the date printed-merchandise artwork locks and the lead time a speaker needs to clear a weekend. Anchor a combined gate to the tightest real constraint behind it, never to a round number.
- **Cadence variance review**: the starved option: a weekly or biweekly per-track actual-vs-plan pass, replanning whenever a track's slip exceeds its buffer. Highest sustained coordination cost of the three. Promote it once roughly five or more track owners work in parallel (a self-set threshold, not a sourced one), or when an existing team check-in makes the marginal cost near zero (interview Q8).
- **Event-driven replan**: replan only when a foundation assumption breaks: venue lost, anchor sponsor out, CFP badly undersubscribed. This is the floor every plan keeps regardless. Alone, it means every replanning decision is made mid-crisis with no pre-agreed options: cheapest, and worth exactly that.

**Delete, do not demote: the cadence variance review, whenever no standing team meeting exists and Q5's ceiling is volunteer hours.**

- Delete it from this menu and from the axis lines above.
- A weekly per-track pass nobody is on duty to run does not degrade into a slower review: it degrades into a recurring invite the team declines.
- The checkpoint discipline that did exist erodes alongside it.
- Its promotion condition is an existing check-in, not an intention to start one.

The standing rule across all three: once the date is announced, the date holds and scope moves. Before announcement, the date is still a variable and moving it is a legitimate lever: announcement is the milestone that kills it, which is why announcement has prerequisites (see the gate catalog).

## Workflow

1. Run the interview. Route out if the date is unpicked (Q2) or first-edition gates are needed (Q1).
2. Anchor the plan on the doors-open date and list the immovable external deadlines (Q3) beside it.
3. Enumerate the tracks, trimmed to this event. Give each a terminal milestone at or near doors-open.
4. Work each track backward from its terminal milestone to its first action, at the chosen granularity rung.
5. Overlay cross-track gates: every dependency between tracks becomes an explicit gate naming both sides' milestones ([references/tracks-and-gates.md](references/tracks-and-gates.md)).
6. Mark every irreversible commitment with its latest-safe date and its owner (buffer menu above).
7. Write the checkpoints: date, condition checked, pre-decided action, owner (replanning menu above).
8. Confirm one owner per track. Publish the plan in the simplest shared tracker the team will actually keep updated.
9. Deliver the work-back table (output shape below) section by section: anchor and tracks first, then gates, then buffers and checkpoints: validating each with the user before finalizing.
10. On a mid-flight replan (Q6): diff actuals against the plan per track, spend buffers explicitly, and fire the pre-written checkpoint actions. Never move an announced date to rescue an unready scope item.

The plan's terminus is doors-open: what happens after hands off to `samber/dev-event-organizer-skills@event-debrief`. Framing the plan as pre-event / event / post-event phases is borrowed from generic go-to-market launch templates. Say so if you use it: only the pre-event phase is this skill's scope.

If your harness has persistent memory, record the anchor date, track owners, gate list, latest-safe commitment dates, each checkpoint's condition and outcome, and every buffer spent: a mid-flight replan and the next edition's plan both start from these instead of re-deriving them.

## Failure modes

- **Forward planning from today.** "What can we start next?" discovers the venue or CFP lead time only when it's too late to fit. Always work back from the date.
- **Borrowing another format's runway.** A conference-length and a hackathon-length runway differ for structural reasons. The sourced variants live in `samber/dev-event-organizer-skills@event-first-edition`: never average them, and never assume a runway fits a different format.
- **Announcing the date before its prerequisites.** Sourced example: an organizing guide's hard rule that a date cannot be announced until payment handling is in place: teams that skipped it have rescheduled or cancelled. Announcement is a gated milestone, not a press release.
- **Padding every milestone.** Uniform slack is consumed silently and the plan's dates stop meaning anything. Buffers live where the menu puts them: on irreversible commitments and scope tiers.
- **A checkpoint with no pre-written action.** It degrades into a status meeting. The slip is noted, nothing fires, and the decision migrates to crisis time.
- **The mega-plan nobody updates.** A task-level plan above the team's upkeep ceiling is stale within a month, and a stale plan is worse than a coarse live one. Drop a granularity rung.
- **One chronological list, no tracks.** Hides which slip blocks what, so the venue slip and the sponsor slip look equally urgent when only one gates three other tracks.
- **A track with no owner.** Its milestones slip without anyone noticing until a gate fails. Ownership is part of the plan, not an implementation detail.
- **Moving an announced date.** Burns speaker, sponsor, and attendee trust: for a compounding annual event (Q4), the most expensive lever on the table. Cut scope instead.
- **Watching only the final sprint.** A team that is efficient in the last month can still have drifted for the quiet stretch before it, and a plan nobody is checking against actuals in that gap will not surface the drift until it has compounded. The final sprint is not where an annual event's planning failure actually lives; the unwatched middle is.

## Measurement

Gates (pass/fail on the plan itself: the underlying mechanics are sourced where noted, but treating each as a hard gate is this skill's own bar, self-set):

- **Gate coverage**: every cross-track dependency appears as an explicit gate naming both milestones. No track pair carries an implicit dependency.
- **Commitment coverage**: every irreversible spend or headcount decision has a latest-safe date and an owner (mechanic sourced, completeness bar self-set).
- **Checkpoint completeness**: every checkpoint has a date, a condition, a pre-decided action, and an owner (mechanic sourced, bar self-set).
- **Ownership**: every track has exactly one accountable owner.

Trends to watch between checkpoints (self-set): buffer consumption per track, count of tracks currently behind, and gates at risk. The doors-open verdict: the date never moved after announcement, and every scope cut happened at a checkpoint rather than mid-crisis.

## Invocation examples

- "Our conference is on June 12 next year, venue signed. Build the full retroplanning back from that date."
- "We're four months out, the CFP closed late and sponsorship is behind target: replan without moving the date."
- "Turn last year's chaotic prep into a proper work-back plan with checkpoints for this year's edition."

Expected output:

- A work-back table, per track: milestones with dates, worked backward from doors-open.
- The gate list, both milestones named.
- The latest-safe commitment dates.
- The checkpoint table: date, condition, pre-written action, owner.

A worked illustrative example and a negative example live in [references/buffers-and-replanning.md](references/buffers-and-replanning.md).

## References

- [references/tracks-and-gates.md](references/tracks-and-gates.md): per-track milestone chains and the cross-track dependency-gate catalog, sourced examples labeled.
- [references/buffers-and-replanning.md](references/buffers-and-replanning.md): the two sourced buffer mechanics in depth, checkpoint design, the mid-flight replanning procedure, and an illustrative work-back table with a negative example.
- `samber/dev-event-organizer-skills@event-budget`: the P&L behind the scope-tier ladder and the finance track.
- `samber/dev-event-organizer-skills@event-risk-management`: the risk register the checkpoint conditions draw on.
- `samber/dev-event-organizer-skills@event-continuous-improvement`: sends the deliberate, trend-justified changes to the event concept that land on this plan as scheduled tasks, distinct from a single edition's carried-over action items.
- `samber/dev-event-organizer-skills@cross-event-promotion`: co-location and swap deals with other events. A co-location decision is an edition-cycle commitment that lands on the venue and marketing tracks of this plan, not a late marketing task.
