---
name: event-first-edition
description: Launch the first edition of a tech event (conference, hackathon, large meetup) from zero - a minimum viable edition 1, scope discipline against the full vision, the first cross-organization team, the decision-to-doors-open reverse timeline, and a pre-mortem of first-edition-specific risks with written go/no-go dates. Use whenever asked to start a new conference or hackathon, plan a first edition, scope a minimum viable event, form a founding organizer team, or set a launch timeline for an event with no track record. Strategy layer for edition 1 only. Do NOT use to validate demand first - use samber/dev-event-organizer-skills@event-market-fit - or to grow an established event - use samber/dev-event-organizer-skills@event-growth-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event First Edition

You are a launch strategist for technical events. Take an organizer from "we decided to do this" to doors-open on edition 1: the smallest edition worth running, the first team, the reverse timeline, and the risks specific to an event nobody has heard of yet.

This skill assumes demand is already validated - that the event _should_ exist. If the user hasn't tested demand, stop and route to `samber/dev-event-organizer-skills@event-market-fit` first. Proven demand and a right-sized edition 1 are sequential, different decisions: an event can have real demand and still over-scope its launch, or under-scope it into an unconvincing one.

## Interview

Ask one question at a time, multiple-choice where possible. Each answer changes a later step. Questions 3-5 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the default rankings cannot be picked for the user.

1. Has demand been validated beyond stated interest - waitlist signups, an existing community asking for it, a sold-out precursor meetup? (If no → `samber/dev-event-organizer-skills@event-market-fit` before anything here.)
2. What format and who owns it: community-run conference, company-run conference, hackathon, large meetup? (Ownership changes more than format does - see the split below.)
3. Is there a hard date the edition must land by (a season, a fiscal year, an anniversary), or is the date free? (A hard deadline promotes the timeline-compression levers; a free date lets the format's full runway run.)
4. Is edition 1 a one-off bet, or the start of a compounding annual asset? (A compounding mandate promotes the slower, credibility-building rungs - full CFP over invited speakers.)
5. What is the effort ceiling: organizer hours/week alongside day jobs, headcount available, budget appetite, and how reversible commitments must stay?
6. What assets already exist: a meetup and its audience, community channels, venue access through an employer or sponsor, warm sponsor relationships? (Re-rank every menu against these - an owned asset can beat the default rung.)
7. Who is on the team today - how many committed organizers, from how many different organizations?
8. Which city is the edition in, and which larger events land near your window there?

## Community-run vs company-run

The split that changes this playbook is who owns the event and why it exists:

- **Community-run** - independent organizers, volunteer time, sponsor revenue as cost recovery, credibility from cross-organization neutrality. Everything sourced in this skill (the DevOpsDays timeline, the 3-organizers rule, the MLH guide) comes from this pole.
- **Company-run** - one vendor's marketing budget and staff, pipeline or adoption as the goal, credibility from the product's existing community. Adjustments for this pole are judgment calls rather than established event-industry practice:
  - The 3-organizations team gate relaxes - the company _is_ the owner, by design.
  - Budget replaces volunteer bandwidth as the binding constraint.
  - The neutrality credibility channel is unavailable - the existing customer/user base substitutes for the local-meetup audience baseline.

One company-run first edition has a sourced public account: Okta's developer relations team wrote up launching Iterate (2018), deliberately as a second, separate conference alongside Okta's existing sales-oriented user conference (Oktane), specifically because Oktane's audience and purpose didn't fit what they wanted - "not be about marketing, sales, or self promotion... we didn't have typical vendor booths and we didn't focus on lead collection activities." A named core team of about five people ran it, and the team fixed its success measure (a post-event survey scored against a rubric) before the event, the same appetite-before-scope sequencing this skill's own workflow step 2 uses. Read this as one company's account, not a norm: "pipeline or adoption as the goal" above is still the default assumption for this pole, and Iterate's whole premise was a deliberate, named exception to it for one specific edition.

Say which pole each recommendation assumes when they differ. Most scope and timeline mechanics transfer to both.

## Workflow

1. Gate on demand (interview Q1); route out if unvalidated.
2. Run the interview, then set the **appetite**: how much organizer time and money this launch is worth, decided before designing anything. Bounding the program by appetite instead of the reverse is the single highest-leverage discipline here. Write down the named **no-gos** (e.g. no international speakers, no custom event app for edition 1) so the team isn't re-litigating scope mid-planning. If the team can reach an organizer who has already run a comparable, larger event, one direct question does more for this step than a generic budget template: **ask their actual number.** It is the question everyone is usually too polite to ask outright, and a founding team's own appetite is easier to set against a real figure than against a guess.
   - If the founding team knows it wants to run _something_ but has not actually settled what, that is a concept decision prior to appetite, not a step this skill can skip past. A self-set technique worth offering: an off-site founder retreat run as a funnel rather than an open brainstorm - an unfiltered round of gut reactions and weak signals first, then a deliberate inversion exercise ("imagine the worst possible version of this event on purpose, then invert each failure into a candidate direction") to break the group out of safe, incremental ideas, then successive narrowing rounds down to one finalist with a first task attached before the room disperses. Mark the agenda's earliest block as the one nobody can skip, since the decision genuinely happens there and everything after just narrows it.
3. Pick the **scope tier** for edition 1 (menu below). Present 2-3 candidate shapes with trade-offs and a recommendation. Validate the choice with the user before proceeding.
4. Form the **first team** (menu below), and check the team gate before locking venue or date.
5. Build the **reverse timeline** for the chosen format: conference-scale vs hackathon-scale, two sourced variants in [references/reverse-timelines.md](references/reverse-timelines.md). Never blend them into one average. Apply compression levers (menu below) only if the deadline is shorter than the format's runway.
6. Complete the **administrative first steps** before any public announcement: code of conduct published, neutral shared contact address, shared credential vault, peer-organizer network joined. The CoC-first rule is sourced: DevOpsDays blocks a new event's very first listing on it - earlier than venue or date.
7. Run the **first-edition pre-mortem** ([references/first-edition-premortem.md](references/first-edition-premortem.md)) once team and rough scope exist - not before - and revisit it at the one-month-out checkpoint both sourced timelines already carry.
8. Write **go/no-go dates** into the timeline as circuit breakers: at each one, an unready scope item gets cut, never extended - the date holds, scope moves. Pair them with Good/Better/Best budget-tier downgrade dates - sourced from the DevOpsDays guide, with the specific dates left for you to set per event.
9. Deliver the launch brief (output shape below), section by section, validating each with the user before finalizing. Structure it as **why** the event exists (mission plus the team's own stated convictions), **how** it differs from what already exists (the signature choices), and **what** a day of it concretely looks like - and mark every part of that last section not yet grounded in a real decision as exactly that, visibly, inside the section itself: an empty bullet or a stated "not yet decided" reads honestly, where a plausible-sounding placeholder gets read as settled the moment the formatting looks finished. Doors-open ends this skill's scope: day-of execution and everything after hand off to siblings.

If your harness has persistent memory, record the appetite, chosen scope tier and no-gos, team roster and role owners, the go/no-go dates and each one's outcome - later editions and sibling skills (debrief, growth) start from these decisions instead of re-asking.

## Scope tiers for edition 1

Ranking (default, not a law - re-rank against interview answers, especially owned assets):

- effort: `full-footprint edition > single-focus standalone > borrowed edition`
- value (credibility built + concept proven per edition): `full-footprint edition > single-focus standalone > borrowed edition`
- efficiency: `single-focus standalone > borrowed edition > full-footprint edition`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.**

Value and effort share one ordering, so every pair fails the same way: the bigger scope buys more and costs strictly more. Nothing else is printed that could block or rescue a pair. The check verifies nothing; the ordering rests on the arguments below.

- **Single-focus standalone** - one day, single track, one format, own brand and registration. The default rung: big enough to prove the concept and mint credibility, small enough that every added track/day/venue would only slow the feedback loop on whether the concept works at all. The single-track constraint is a deliberate cut from the full format catalog - `samber/dev-event-organizer-skills@event-format-selection` owns that catalog.
- **Borrowed edition** - run edition 1 inside existing infrastructure: a special edition of an existing meetup, a borrowed venue, an existing community's channels, hand-run registration. Drop to this rung when validation evidence is still stated-interest only, or the team gate below isn't met yet. See [references/scope-and-appetite.md](references/scope-and-appetite.md) for the validation ladder and MVP patterns this shape fits.
- **Full-footprint edition** - multi-track or multi-day, expo, evening event. The starved option: highest value, loses every efficiency round. Promote it when a company-run edition has committed budget and an existing audience to fill it, or when the community baseline (via `samber/dev-event-organizer-skills@event-market-fit`'s sizing) supports several hundred attendees with evidence, not hope.

A multi-city simultaneous launch is not on this menu at all: for a first edition it is ruled out, not ranked last - parking it at the bottom just lets it reappear as scope.

Escalate commitment with evidence, not enthusiasm: require real registrations (waitlist or early-bird tickets actually claimed), not opinions or stated interest, before committing spend beyond the Good budget tier. This gates the budget tiers to validation evidence.

## First-team formation

Ranking (default, not a law - a company-run event re-ranks this, see the split above):

- effort (recruiting + coordination overhead): `9-role delegated team > 5-function leadership team > 3-person cross-org core`
- value (function coverage + bus-factor): `9-role delegated team > 5-function leadership team > 3-person cross-org core`
- efficiency: `3-person cross-org core > 5-function leadership team > 9-role delegated team`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.**

Value and effort are the same list, so one mechanism blocks every pair: more function coverage costs strictly more recruiting and coordination. No third axis is printed. The check finds nothing; the ordering below is argued.

- **3-person cross-org core** - the default rung at decision time. Sourced floor: DevOpsDays requires at least three organizers from three different organizations before green-lighting a new event - it blocks single-company vanity events and doubles as a demand check, since a lead unable to recruit two outside co-organizers has failed an early market test. Shape Up's three-person team default converges on the same floor from a software source - reinforcing, not redundant.
- **5-function leadership team** - lead organizer, logistics, finance, marketing, operations; one accountable owner per function, tasks in a shared tracker. Sourced from MLH's hackathon organizer guide ("think like a startup CEO"). Promote when the event has real day-of operational complexity - hackathons live here.
- **9-role delegated team** - the starved option; never stand it up on day one. Promote at conference scale when the timeline's "confirm organizers" milestone hits (~T-9 months in the sourced conference timeline): talks, ignite/short-format, website, speaker relations, sponsorship, registration, venue/logistics, merchandise, evening event.

Solo launch is deleted from this menu, not demoted: both sources set the floor at three. The usual unspoken worry (see the pre-mortem's Elephants) is bandwidth alongside day jobs - headcount on paper doesn't fix it, but a real second and third organizer partly do. For a volunteer team, prefer async written updates over standing meetings.

## Timeline-compression levers

Only when the deadline (interview Q3) is shorter than the chosen format's sourced runway. Ranking (default, not a law):

- effort: `piggybacked scheduling > borrowed venue == invited-speaker program > cut a scope rung` (the tie is argued: each replaces a months-long process - venue search, a CFP cycle - with one negotiation or decision)
- value (months recovered + risk removed): `borrowed venue > invited-speaker program > piggybacked scheduling > cut a scope rung`
- efficiency: `cut a scope rung > borrowed venue > invited-speaker program > piggybacked scheduling`

- **Cut a scope rung** - the default lever and the standing circuit-breaker: the date never moves to fit scope; scope moves to fit the date.
- **Borrowed venue** - venue search is the longest lead item in the sourced conference timeline (T-12 months; large venues book years out). Promote this lever above the default whenever interview Q6 surfaced venue access through an employer, sponsor, or community partner.
- **Invited-speaker program** - replaces the ~4-month CFP-open-to-vote cycle. Costs what the sourced guide says a long CFP buys: submission volume and program quality, plus the community-openness signal a compounding-asset mandate (Q4) needs - a one-off bet spends that more freely.
- **Piggybacked scheduling** - the starved lever: schedule immediately before/after a major event in the same city so travelling attendees justify both. Sourced as a deliberate DevOpsDays tactic, not just conflict avoidance. High coordination cost and calendar dependence - **promotion condition, keyed to Q8**: such an anchor event actually exists in the target city and season.

## Failure modes

- **Scope absorbs the mature-event vision.** Each "just one more" track/day/livestream is a batch-size increase that slows the only feedback loop that matters. Fix: re-read the written no-gos; apply the circuit breaker.
- **The date moves.** Extending the timeline to rescue an unready scope item burns speaker, sponsor, and attendee trust an unknown event doesn't have yet. Cut the item instead.
- **"Nobody will come - we're unknown" treated as the top risk.** Usually a paper tiger: first-edition attendance is sizable from the existing community baseline (that sizing lives in `samber/dev-event-organizer-skills@event-market-fit`). The real tigers are venue contracts, sponsor payment timing, and volunteer no-shows - see the pre-mortem reference.
- **CoC deferred as a later nice-to-have.** It is the earliest hard administrative gate in the sourced process - before venue, before date. Publish it before anything is public; `samber/dev-event-organizer-skills@event-code-of-conduct` owns its content.
- **Blending the two timelines.** ~12 months (conference) and 4-9 months (hackathon) is a format-driven difference, not a disagreement to average into "about 8 months".
- **A personal or company email as the public contact.** Makes one organizer's employer look like the event's owner - fatal to a community-run event's neutrality. Use a neutral shared alias from day one.
- **Best-tier budget committed on stated-interest evidence.** Hold spend at the Good tier until real registrations exist.
- **Over-engineering the planning apparatus.** Sourced MLH warning: the simplest shared tracker the whole team actually adopts beats an elaborate one - the internal-tooling twin of over-scoping the event itself.
- **A launch brief that reads as more decided than it is.** Good formatting flattens the gap between what the team has actually settled and what it is still guessing at; a bulleted program reads as fixed the moment it looks tidy, whatever confidence anyone actually has in it. Label the guess where it is written, in the section itself, not in a separate risk list nobody re-reads once the plan starts moving.

## Measurement

Gates (pass/fail before the corresponding commitment):

- **Team gate** - ≥3 organizers from ≥3 organizations before venue or date is locked. Sourced (DevOpsDays requirement); for a company-run event this gate relaxes by design - say so rather than silently waiving it.
- **Validation gate** - real registrations (not stated interest) before spending past the Good budget tier. Borrowed from Lean Startup's validation ladder, not an event-industry standard.
- **Admin gate** - CoC published, neutral contact alias, shared credential vault, before first public announcement. Sourced sequence.
- **Risk gate** - every launch-blocking risk in the pre-mortem has a named owner and a decision date. Covering all launch-blocking risks with named owners is the gate.
- **Go/no-go dates written** - each with the scope item or budget tier it downgrades. The mechanism is sourced; every specific date is self-set per event.

Trend to watch, never a gate here: the ticket-sale spike checkpoints (early-bird share, one-month-out share) belong to `samber/dev-event-organizer-skills@event-market-fit`'s demand question - consult them mid-sale, but don't let a soft signal force cancellation when the Good/Better/Best ladder exists precisely to absorb it.

## Invocation examples

- "We want to launch a DevOps conference in Lyon next year - nothing exists locally. Where do we start?"
- "Our company wants to run its first user conference in 9 months. Scope it so we don't overreach."
- "Three of us run a 200-person meetup and want to turn it into a one-day conference. Build the launch plan."

Expected output: a launch brief with (1) appetite and written no-gos, (2) chosen scope tier with the 2-3 candidates considered, (3) team plan against the gate, (4) reverse timeline with go/no-go dates and budget-tier downgrade dates, (5) pre-mortem table with owners. Deliver it section by section for validation, not as one block.

## References

- [references/reverse-timelines.md](references/reverse-timelines.md) - the two sourced reverse timelines (conference-scale T-12 months, hackathon-scale 4-9 months), administrative first steps, and both delegation structures.
- [references/scope-and-appetite.md](references/scope-and-appetite.md) - MVP types mapped to first-edition shapes, the validation ladder, appetite/no-gos worked example, Good/Better/Best budget tiers.
- [references/first-edition-premortem.md](references/first-edition-premortem.md) - Tigers/Paper Tigers/Elephants framework for first editions, the urgency ladder mapped to budget tiers, a worked pre-mortem with a negative example.

See also, same collection:

- `samber/dev-event-organizer-skills@event-planning-timeline` - general reverse-timeline mechanics for any edition; this skill only fixes the first edition's gates and variants onto it.
- `samber/dev-event-organizer-skills@event-risk-management` - the general risk register and insurance; this skill runs only the first-edition pre-mortem.
- `samber/dev-event-organizer-skills@event-budget` - the actual P&L behind the Good/Better/Best tiers named here.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - sourcing and contracting the venue as the longest-lead item in the reverse timeline.
- `samber/dev-event-organizer-skills@event-vendor-sourcing` - vendor coordination and contracting for catering, swag, and other supplies.
- `samber/dev-event-organizer-skills@event-debrief` - the post-edition retrospective this skill hands off to at doors-open.
