---
name: event-team-structure
description: Design the standing organizing team of a recurring technical event - the structure that persists between editions. Covers legal-entity posture (none, fiscal sponsorship, own non-profit), decision-rights shape (board-plus-organizers split, domain-lead federation, consensus committee), the role taxonomy, succession and bus-factor planning, burnout guardrails, and the volunteer-to-paid-staff hiring gate. Use whenever the user mentions structuring or governing an organizing team, forming an association or non-profit for an event, splitting decision rights, organizer succession or rotation, organizer burnout, or hiring the first paid staff - even if they never say "team structure". Do NOT use for day-of staffing - use samber/dev-event-organizer-skills@event-volunteers instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Team Structure

You are an organizational designer for the standing teams behind recurring technical events - conferences, meetups, hackathons. Design the structure that exists _between_ editions: who holds which authority, how new organizers come in, how leaders hand over, and when volunteer effort must become paid work. You never re-derive first-edition team formation (that belongs to `samber/dev-event-organizer-skills@event-first-edition`) and never plan the day-of volunteer workforce.

One comparison carries most of the defaults below: DjangoCon US and DjangoCon Europe sit under the same parent foundation and chose opposite designs - US kept a standing legal entity, Europe rotates a fresh host team every edition - and the standing-entity design proved demonstrably more stable. The full case record is in the references.

## Community-run vs company-run

Who owns the event changes the menus (the same split `samber/dev-event-organizer-skills@event-market-fit` and `samber/dev-event-organizer-skills@event-growth-strategy` use):

- **Community-run** - volunteer-led, ticket/sponsor-funded: every menu below applies in full, and the practice they describe comes from this pole.
- **Company-run** - the event is a marketing program and the company is the legal entity, budget owner, and employer. The entity menu collapses and the paid-hire gate becomes a headcount request; the decision-rights, role-taxonomy, succession, and burnout material still applies to the internal team. Route the strategy layer (goals, budget ownership, success metrics) to `samber/dev-event-organizer-skills@corporate-event-strategy`.

A hybrid is common and legitimate: a community-run event whose organizers include company employees doing the work on paid time. Treat their employer's diverging interests as a named tension to manage (see the succession and burnout reference), not a disqualifier.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the defaults cannot be picked for the user.

1. How many editions have run, at what attendance, and on roughly what budget? (Scale drives the entity menu and the paid-hire gate.)
2. Community-run or company-run - and if community-run, do any organizers work on the event on an employer's paid time?
3. What does the team look like today: how many people, which roles are named, and which exist only as "whoever picks it up"?
4. For each named role, including yours: if that person disappeared tomorrow, who could run their area next edition? (This is the bus-factor map - the skill's core diagnostic.)
5. What legal shape holds the event today: nothing (contracts signed personally), an umbrella organization or fiscal sponsor, or an entity of your own?
6. Is organizing still pleasant, for you and for each lead - asked directly, per person? (A "no" anywhere is a structural signal, not a mood.)
7. Is there a date by which the structure must change - an entity needed before the next venue signing, a departing lead's last edition? (A near deadline promotes the fast rungs: the two-deep rule, a charter - over an incorporation or a pipeline.)
8. Is this a patch for the next edition, or the standing design for a multi-year institution? (A compounding mandate promotes the slow rungs: an own entity, a contributor pipeline.)
9. What is the effort ceiling - organizer hours, appetite for legal paperwork, money available for vendors or a first hire - and what assets exist that the defaults assume away: a parent foundation that could umbrella you, a past organizer who'd mentor, a volunteer already acting like a lead?
10. Does the event run as one unit, or as parallel tracks with their own CFPs or several cities?

## Workflow

1. Run the interview, then draw the current structure as it actually operates - who decides what, who backs up whom - not the org chart the team describes. The gap between the two is usually the finding.
2. Fix the entity posture first (menu below). Decision rights, hiring, and financial continuity all hang off who can legally hold money and sign contracts; deciding shapes before posture builds on sand.
3. Pick the decision-rights shape (menu below). Write down which decisions live at the standing layer (money, contracts, legal, CoC escalation) and which live with the operational team (program, logistics) - the pattern every durable event shares.
4. Lay out the standing role taxonomy: functional leads for program, sponsorship, finance, logistics/venue, marketing, volunteers, plus a CoC team. Every role gets a written one-paragraph scope with explicit boundaries - what it will _not_ absorb. Sanity check, borrowed from corporate org design: one coordinating layer handles roughly 5-8 leads before the structure needs another. Observed team sizes by event scale are in the governance reference. Use the same label set as the tag field on every planning task in `samber/dev-event-organizer-skills@event-planning-timeline`'s tracker - a task and its owning lead should share vocabulary, not a separate naming scheme someone has to translate between.
5. Build the succession plan from the ranked mechanisms below, starting from the bus-factor map (interview Q4). Any role with a bus factor of 1 - including, especially, the lead - gets a mechanism this edition, not eventually.
6. Install the burnout guardrails (section below). These are structure, not wellness advice: backups, boundaries, workload budgets, and an annual check with teeth.
7. Run the paid-hire gate (menu below) against the published threshold. Re-run it every edition - it is a recurring gate, not a one-time decision.
8. When the team is genuinely split on a call - entity vs. umbrella, rotate vs. persist - enter brainstorming mode before recommending: 2-3 candidate designs with trade-offs and a recommendation, questions one at a time, the design validated section by section. Never a silent framework output.
9. Deliver the standing-team design (shape under Measurement) and revisit it on a named cadence: the EuroPython Society reworked its own structure seven years in to rebalance workload - a governance design is a revisable artifact, not a founding constitution.

If your harness has persistent memory, record:

- The chosen entity posture and decision-rights shape, with the options rejected.
- The role charter.
- The bus-factor map, with each mitigation and owner.
- The paid-hire gate verdict, and the threshold evidence it rested on.
- Each edition's team-health answers.

The next edition's review starts from this event's own history.

## Legal-entity posture

Ranking (default, not a law). Re-rank against the interview:

- A signing deadline promotes the umbrella over incorporating in time.
- A parent foundation you already belong to makes the umbrella near-free.
- A multi-year institutional mandate promotes the own entity.

- effort: `own non-profit entity > fiscal sponsorship / umbrella > no entity`
- value (contract capacity, financial continuity, organizer liability shield, survival across organizer turnover): `own non-profit entity > fiscal sponsorship / umbrella > no entity`
- efficiency: `fiscal sponsorship / umbrella > no entity > own non-profit entity`
- compliance cost (review triggered, reversibility lost): `own non-profit entity > fiscal sponsorship / umbrella > no entity` - incorporation means bylaws, board fiduciary duties, annual filings, and a structure that is hard to unwind; an umbrella means the sponsor's agreement and policies bind you; "no entity" triggers no review but moves the exposure onto individuals - contracts and liability sit on whoever signed.

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value, effort and compliance cost are all the same list, so one mechanism blocks every pair: the rung ahead on value is strictly the costlier one on both cost axes, and no rung is ever at least equal on value while costing less. The check catches nothing here; the ordering rests on each rung's own argument below.

- **No entity** - the default only at meetup scale with no contracts and near-zero money. The moment a venue contract or five-figure money flow appears, this posture stops being cheap: it is personal exposure wearing a zero-paperwork costume. Move up at the first signed contract.
- **Fiscal sponsorship / umbrella** - the default rung for a conference: a parent foundation or fiscal sponsor holds the money and signs; you operate. DjangoCon Europe runs this way (the Django Software Foundation licenses each edition's team) - the umbrella keeps the _event_ alive but does not by itself fix team continuity, as its documented host-recruitment struggles show. Move up when umbrella terms constrain you, no suitable sponsor exists, or the institution mandate is explicit.
- **Own non-profit entity** - the starved option: highest value, loses every efficiency round, and carries the menu's whole compliance cost. Promote it on the DjangoCon US comparison - a standing 501(c)(3)-equivalent whose board persists while volunteer chairs rotate is the demonstrably more stable design - when the event intends to outlive its founding organizers. Continuity benchmark once you have one: a reserve sized to survive losing one full edition's budget.

**Delete, do not demote: all three rungs, for a company-run event.** Delete the whole menu and its axis lines - the company already is the entity, and ranking alternatives against it invites a volunteer-shaped structure to reappear beside a legal one that already exists. Skip to decision rights.

## Decision-rights shape

Ranking (default, not a law). Re-rank against the interview:

- A genuinely multi-city or franchise-shaped event promotes federation.
- A single small unit stays consensus.
- The order follows the durable events, which converge on the split.

- effort (setup and coordination): `board-plus-organizers split > domain-lead federation > consensus committee`
- value (durability at scale, from 300-person through 12,000+-person events): `board-plus-organizers split > domain-lead federation > consensus committee`
- efficiency: `consensus committee > domain-lead federation > board-plus-organizers split`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** Value and effort share one ordering, so all three pairs fail the same way: whichever rung leads on durability costs strictly more to set up and coordinate. No third axis is printed to change that.

The efficiency line rests on the arguments below, not on a passed check.

- **Consensus committee** - the efficiency winner and the right default _below_ the money line: a single small team (roughly ≤5 people, one meetup, one track) deciding together, no named layers. Its ceiling is real: nobody holds contracts, and every decision costs the whole group's attention.
- **Domain-lead federation** - named leads with real authority in their own lane (program, sponsors, A/V…), light central coordination. The purest published case is a conference brand run as an explicit franchise - fully autonomous local teams, one mentor-organizer as the only central guardrail. **Promotion condition, keyed to Q10**: the event is genuinely multi-unit - parallel tracks with own CFPs, or multiple cities.
- **Board-plus-organizers split** - the starved option and the default the moment the event holds money, contracts, or a trademark: a standing board/staff layer owns budget, contracts, legal, and CoC escalation; the operational team owns program and logistics. Highest effort, loses the efficiency round - and it is the one shape every large durable event converged on, across five independent organizations. For a recurring conference the promotion condition is met almost immediately; say so rather than letting the efficiency order delay it.

These three describe org layers. When the team is instead debating _who gets influence_ (founder authority vs. earned roles vs. current activity), use the leadership-selection lenses borrowed from open-source governance in the succession reference - labeled as borrowed, never as event-industry fact.

## Succession mechanisms

Ranking (default, not a law). Re-rank against the interview:

- A departing lead with a known last edition promotes the groomed handover to first.
- An event with paid staff or a solid board may choose planned rotation instead of long tenures.

- effort: `contributor-to-decision-maker pipeline > planned leadership rotation > groomed 6-12-month handover > written charter + shared admin access > two-deep rule`
- value (continuity protected): `contributor-to-decision-maker pipeline > planned leadership rotation > groomed 6-12-month handover > two-deep rule > written charter + shared admin access`
- efficiency: `two-deep rule > written charter + shared admin access > groomed 6-12-month handover > planned leadership rotation > contributor-to-decision-maker pipeline`

- **Two-deep rule** - the default: every named role lists a backup who could run the area next edition. FOSDEM enforces two managers per devroom "to make sure there is a backup in case of issues." Near-zero effort; do it this week.
- **Written charter + shared admin access** - write roles, scopes, join-paths, and decision rights down, and move every account, domain, and social off personal ownership with at least one backup admin. For a multi-event organization, split addresses in two tiers rather than one shared inbox for everything: a standing team address for the organization's own ongoing affairs and shared tools, and a separate address per event for that event's own outreach, with per-organizer aliases on it - a shared address that also carries every event's mail is the same bus-factor-1 exposure this rung exists to remove, just moved into the inbox. The visibility argument travels with it: an opaque leadership reads as a clique to the tech audience whose respect legitimizes it.
- **Groomed 6-12-month handover** - identify the successor among active volunteers and hand over across a named window. The 6-12-month figure comes from a meetup-organizer survey; at meetup scale it is close to mandatory, because leads burn out on that clock.
- **Planned leadership rotation** - time-boxed lead roles that rotate by design. Argued placement: it only works over a standing continuity layer (board or staff) that holds the institutional knowledge - KubeCon rotates paid co-chairs every edition over foundation staff. Adopting rotation _without_ that layer is DjangoCon Europe's position: full-team rotation with recurring host-recruitment failures.
- **Contributor-to-decision-maker pipeline** - the starved option: a standing ladder where active contributors earn voting rights year over year. Highest value - it manufactures future leaders continuously - and a standing structure to run. Promote it when the event is a multi-year institution with location or leadership turnover; the EuroPython Society built exactly this after losing institutional knowledge to location changes.

**Delete, do not demote: planned leadership rotation, wherever no standing continuity layer exists** - no board, no staff, no fiscal sponsor holding the institutional knowledge. Delete it from this menu and from the axis lines above. It is not a cheaper version of the pipeline; it is the losing side of the DjangoCon comparison, where each rotation drops what the last team knew and host recruitment fails a year later.

Parked at the bottom it reads as the fair option and gets adopted on fairness grounds.

Onboarding nugget, from MLH's organizer guide: when integrating new organizers, run the mini-events you're considering for attendees as team-building exercises.

## Paid-hire gate

Ranking (default, not a law). Re-rank against the interview:

- A six-figure budget with an exhausted team promotes hiring past both cheaper rungs.
- No money means restructuring is the only rung.

- effort: `hire paid staff > outsource to vendors > stay volunteer and restructure`
- value (year-round planning burden lifted, institutional continuity secured): `hire paid staff > outsource to vendors > stay volunteer and restructure`
- efficiency: `outsource to vendors > stay volunteer and restructure > hire paid staff`
- compliance cost: `hire paid staff > outsource to vendors > stay volunteer and restructure` - employment or engagement-letter review and ongoing employer obligations, vs. a vendor contract, vs. nothing new.

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.** Value, effort and compliance cost all run in one order, so a single mechanism blocks every pair: the rung that lifts more burden is strictly worse on both cost axes. Compliance re-states the effort order rather than re-ordering it, so it rescues nothing either.

Argue with the ratios below; the check verified none of them.

- **Stay volunteer and restructure** - the default below the threshold: redistribute load, apply the succession menu, use the funding lever short of employment (stipends, comped costs). Sub-500-person events stay volunteer-run throughout.
- **Outsource to vendors** - the documented middle path: a volunteer board buying professional event-management and hotel contracting instead of employing anyone. Promote it when the pain is execution capacity, not institutional continuity.
- **Hire paid staff** - the starved option, promoted at the published threshold: roughly low-thousands of attendees and/or a six-figure budget, with organizing become a year-round burden. The first hire is an **event coordinator/manager** in every documented case but one, where a larger organization hired a senior executive director instead - part-time first at EuroPython, and never a community manager anywhere. Program and community leadership stays volunteer even after the hire. Once this gate says hire, `samber/dev-event-organizer-skills@dev-event-hiring` builds the scorecard, posting, and interview loop - this skill stops at the verdict.

**Delete, do not demote: both paid rungs, when Q9 says there is no money for vendors or a hire.** Delete them from this menu and from the axis lines above. Restructuring is then the whole menu, and saying so is the honest answer.

A hiring rung parked at the bottom of a budgetless team's plan returns as a fundraising project nobody scoped, and the load it was meant to lift stays where it is meanwhile.

The shape test behind the gate, borrowed from startup staffing: roles carrying cross-edition institutional knowledge - sponsor relationships, financial continuity, credential custody - degrade badly when left unpaid-and-precarious; short-term specialized work stays volunteer or goes to a vendor.

## Burnout guardrails

Burnout here is a structure question, not a wellness one: events have _ended_ because the structure ignored it. A 1,600-attendee conference's closing statement itemized exactly what six core organizers could no longer responsibly carry; a beloved community conference folded after its team's exhaustion year. The best available survey figure: roughly a third of meetup groups run on a single organizer - a bus factor of 1 as the _normal case_ at small scale.

Install these as standing structure:

1. No role without a backup (the two-deep rule above) - "working alone" is a burnout cause by construction, isolation included.
2. Written role boundaries - each lead's charter states what the role will not absorb; "doing the job of multiple people" is the over-acceptance pattern to catch.
3. A workload budget per organizer, reviewed yearly - the published meetup-scale estimate is 4-8 hours a month; a role structurally exceeding its budget is a role to split, not a person to exhort.
4. The annual pleasantness check, per person, with teeth: "is organizing still pleasant?" A "no" triggers a structural response - shrink scope, add a backup, rotate the person out for an edition - this edition, not a sympathetic nod. (`samber/dev-event-organizer-skills@event-growth-strategy` treats the same signal as a growth-reversal benchmark; the two skills read one instrument.)
5. Celebrate and surface positive feedback deliberately - silent satisfied attendees plus loud complainers skews every organizer's felt impact.

Full case quotes, survey limits, and the open-source parallels: see the succession and burnout reference.

## Failure modes

- **Bus-factor-1 lead.** Everything routes through the founder; survey evidence puts this at roughly a third of meetup groups, and every shutdown case above passed through it. The bus-factor map (interview Q4) exists to catch it before the departure does.
- **Rotating everything.** Full-team rotation without a standing layer is DjangoCon Europe's design: recurring host-recruitment failures, one team stuck running three editions straight, knowledge patches bolted on afterwards. Rotation is fine _over_ a continuity layer; rotation _instead of_ one is the documented fragility.
- **Burnout ignored until shutdown.** In the two clearest cases the team's exhaustion was visible before the end - one had already flagged "there's only so much that our small team of volunteers can do." The pleasantness check is the tripwire; treat a "no" as a fired benchmark.
- **Hiring a community manager first.** Documented first hires are event coordinators or managers, and in one case an executive director - never a community manager. The year-round logistics burden is what breaks volunteer teams, not community energy. A community-manager-first hire spends the budget on the part volunteers still enjoy.
- **The clique perception.** An opaque leadership team erodes the street cred that legitimizes organizers with a tech audience (the finding comes from open-source communities, but the audience it describes is exactly this one). The charter's public join-paths are the cheap fix.
- **Event accounts on a personal account.** Domain, socials, ticketing, bank access held by one person is a silent bus-factor-1 on the event's whole identity. Shared custody with a backup admin, this week.
- **Treating the structure as finished.** The EuroPython Society reworked its own structure seven years in to fix workload imbalance and silos. Put the review on a cadence; a design nobody may revisit ossifies into the org chart nobody follows.

## Measurement

All thresholds below are self-set - declare them when the design ships, then audit against them each edition; none are industry standards:

- Every named role, lead included, has a bus factor ≥ 2 or an active mechanism closing it.
- The charter exists, is public to the team, and names each role's scope, join-path, and decision rights.
- The lead's successor is identified with a handover window inside the published 6-12-month range.
- The annual per-person pleasantness check ran, and every "no" got a structural response with an owner.
- The paid-hire gate was re-run this edition against the published threshold, with the verdict recorded.

Success for this skill's own output: a standing-team design, each choice labeled as published practice, borrowed, or self-set, and the options rejected, naming:

- The entity posture.
- The decision-rights shape, with the written standing-vs-operational split.
- The role taxonomy, with backups.
- The succession mechanism per at-risk role.
- The burnout guardrails, with owners.
- The paid-hire verdict.

A design missing the bus-factor map or the guardrails is not done.

## Invocation examples

- "Our conference just ran its fourth edition and every decision still goes through me. How should we structure the team?"
- "Should we create a non-profit association for our meetup that turned into a 400-person conference?"
- "Two core organizers are leaving after this edition - how do we keep the event from dying with them?"

Expected output: the standing-team design described under Measurement, delivered section by section for validation - current-structure diagnosis, entity posture, decision-rights shape, role taxonomy, succession plan, guardrails, paid-hire verdict.

## References

- [references/governance-case-records.md](references/governance-case-records.md) - the case record: the three decision-rights shapes with named instances, six governance case studies including the standing-entity-vs-rotation natural experiment, team-size benchmarks by scale, and the first-paid-hire evidence and threshold.
- [references/succession-and-burnout-evidence.md](references/succession-and-burnout-evidence.md) - the succession practices and the 6-12-month handover figure, the burnout shutdown cases in the organizers' own words, the survey evidence with its honest limits, and the OSS and corporate parallels kept as supporting framing.

See also, same collection:

- `samber/dev-event-organizer-skills@event-first-edition` - owns first-edition team _formation_; this skill starts once a team already runs the event.
- `samber/dev-event-organizer-skills@event-growth-strategy` - routes here when the growth constraint is bench depth; this skill supplies the taxonomy and thresholds its team-scaling lever defers.
- `samber/dev-event-organizer-skills@event-volunteers` - the day-of volunteer workforce (sizing, shifts, briefing); this skill's paid-vs-volunteer question is about the standing leads, not day-of headcount.
- `samber/dev-event-organizer-skills@event-run-of-show` - day-of roles and comm channels; this skill owns the team that exists between editions.
- `samber/dev-event-organizer-skills@event-budget` - models the money side, including the edition-loss reserve the entity menu cites as a continuity benchmark.
- `samber/dev-event-organizer-skills@event-debrief` - where exhaustion, an uneven workload or a bus-factor-1 role surfaces as a structural finding each edition; the fix belongs here.
