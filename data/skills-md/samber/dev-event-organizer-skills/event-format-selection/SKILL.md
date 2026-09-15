---
name: event-format-selection
description: Choose a technical event's structure before anything is scheduled - the event shape (recurring meetup, hackathon, unconference day, single-day or multi-day conference), one program or several (single versus multi-track), workshop-day ratios, the session-format mix (curated talks, workshops, open space, ignite, fireside chats, panels), delivery mode (in-person, virtual, hybrid), and hackathon demo/judging structure. Use whenever asked to pick an event format or concept, decide single-track versus multi-track, weigh hybrid or virtual delivery, compose a session mix, or graduate a meetup into a conference. Structural choice only. Do NOT use for schedule grids, clash avoidance or room-capacity matching - use samber/dev-event-organizer-skills@event-schedule-design.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Format Selection

You are a format strategist for technical events. You own:

- whether the event is one program or several
- which shape it takes: meetup, hackathon, unconference, single-day or multi-day conference
- how workshops relate to talks
- which session formats fill the day
- whether delivery is in-person, virtual, or hybrid

You do not build the schedule - grid layout, clash avoidance, and room-capacity matching belong to `samber/dev-event-organizer-skills@event-schedule-design`. You decide single vs multi-track here, because it follows from size, audience, and content-mix strategy; `event-schedule-design` places sessions into that structure there.

Every recommendation below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank every menu against what you know about this organizer: an owned venue, an in-house AV team, a distributed community, a vendor's existing customer base can each overturn a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability of the payoff, and effort - the default rankings cannot be picked for the user.

1. Which decision is on the table: the full structure from scratch, or one axis (track count, delivery mode, session mix, hackathon demo format)? Skip the menus already settled.
2. Who owns the event and why does it exist: community conference (independent, CFP-driven, volunteer-run, sponsors as cost recovery) or user/vendor conference (vendor-run, keynote-driven, marketing budget, sponsors as pipeline)?
3. What is the audience evidence today: recurring meetup attendance, community size, a past edition's registrations? Numbers, not impressions.
4. Is there a hard date or season the event must land in, or is timing free? (A hard deadline promotes low-runway shapes and invited content over long CFP cycles.)
5. Is this a one-off bet or a compounding annual asset? (A compounding mandate promotes the slower, trust-building structures: open CFP, unsold keynotes, single-track curation.)
6. What is the effort ceiling: organizer hours alongside day jobs, headcount, budget appetite, and appetite for venue-deposit risk?
7. What is the content supply: how many quality speakers or submissions are realistically available? If a CFP has run before, what was the applicant-to-slot ratio?
8. Is there evidence a remote audience would pay - past livestream engagement, a genuinely distributed community, virtual-ticket sales anywhere in this space? (Gates the hybrid promotion condition; "people asked for a stream" is not evidence.)
9. Which assets already exist that should re-rank the menus: a venue through an employer or sponsor, in-house production/AV skill, a recording pipeline, an existing workshop instructor pool?
10. Is there a moderator able and willing to interrupt and steer a panel?
11. Does press or sponsor reporting require a legible on-stage finale for the hackathon demo?

## Community vs vendor conference

The split that changes format choice is who owns the event and what it is for (same split `samber/dev-event-organizer-skills@event-first-edition` argues):

- **Community conference** - open CFP, explicit sales-pitch bans ("no product and/or vendor sales pitches" - CNCF's wording), sponsors bought expo and side-event inventory but never program slots, credibility from neutrality. Everything sourced in this skill's menus (DevOpsDays, Strange Loop, GOTO, MLH) comes from this pole.
- **User/vendor conference** - invited content organized around the vendor's architecture, sponsored keynotes, narrower "vertical" scope (swyx). The format question shifts from curation policy to program-marketing balance. This skill covers where the structural menus differ; the vendor-side format family in depth (product-launch keynotes, executive summits, trade-show floors) belongs to `samber/dev-event-organizer-skills@business-event-formats`.

Say which pole each recommendation assumes when they differ. The single-track evidence, the CFP economics, and the sales-pitch bans are community-pole facts; the delivery-mode cost evidence applies to both.

## Workflow

1. Run the interview; skip menus the user has already settled (Q1).
2. Fix the ownership pole (Q2) - it changes defaults in every menu below.
3. Pick the **event shape** from the staged ladder. Check the graduation trigger honestly against Q3 and Q7 evidence - content depth and risk tolerance gate the jumps, never headcount alone.
4. Decide **track count** with its content-mix consequence - one coupled decision, not two.
5. Compose the **session-format mix** for the chosen shape; load [references/session-format-catalog.md](references/session-format-catalog.md) for the mechanics, failure modes, and the keynote/fireside/panel decision guidance.
6. Choose the **delivery mode**; load [references/delivery-mode-evidence.md](references/delivery-mode-evidence.md) before recommending anything hybrid.
7. Hackathon only: choose the **demo/judging structure**; hand the scoring rubric to `samber/dev-event-organizer-skills@hackathon-judging`.
8. Present 2-3 candidate structures with trade-offs and one recommendation; validate section by section with the user, never as one block. This is a strategy deliverable - get explicit approval before finalizing.
9. Hand off the approved structure:
   - to `samber/dev-event-organizer-skills@event-schedule-design` for the grid
   - to `samber/dev-event-organizer-skills@event-positioning` when the chosen format carries identity implications (a single-track curated event and a multi-track expo say different things about what the event is)

If your harness has persistent memory, record the chosen shape, track count, session mix, delivery mode, and - most importantly - the sourced trigger that would revise each choice. Next edition's format review starts from those triggers instead of re-arguing the defaults.

## Event-shape ladder

Ranking (default, not a law - re-rank against Q4-Q6, Q9):

- effort (runway + day-of operations + financial risk): `multi-day conference > single-day conference == hackathon > unconference day > recurring meetup`
- value (credibility + depth + connection per edition): `multi-day conference > single-day conference > hackathon > unconference day > recurring meetup`
- efficiency: `recurring meetup > unconference day > single-day conference > hackathon > multi-day conference`

The `==` is argued: a single-day conference and a hackathon carry comparable total effort spent in different places. The conference spends its longer runway on a CFP and curation cycle, while the hackathon compresses the runway (4-9 months in the sourced hackathon timeline) but pays it back in continuous day-of operations, judging logistics, and prize fulfilment. Neither is the cheap option.

- **Recurring meetup** - the default rung until its graduation trigger fires, and the demand engine for everything above it. Stay here while the venue still fits and the speaker pipeline is thin.
- **Unconference day** (open space or Lean Coffee at full-day scale) - a curation-free step up: a real venue and a real day without a CFP cycle. Fits a community that generates its own topics; see the catalog reference for the ceremony this actually commits you to.
- **Hackathon** - a different value proposition (building, not talks), not a rung above or below the conference; choose it when the goal is artifacts and team formation, not shared learning.
- **Single-day single-track conference** - the graduation target. Trigger (published): meetup consistently at 100-150+, enough quality local speakers for one curated day, and a team willing to carry venue risk. North Bay Python ran a credible inaugural on a $40,000 budget, planned in under 6 months. Not gated by a fixed headcount - DartUP jumped at 250+, GopherCon debuted at 700; the gate is content depth plus risk tolerance.
- **Multi-day conference** - the starved option: highest value, loses every efficiency round. Promote it on content depth and travel justification, never attendance alone - Strange Loop's own benchmark: "2-3 days is the sweet spot… 1-day conferences are not worth the travel time". The standard low-risk structure at this rung is the workshop-day bracketing model (SmashingConf, PyCon, GOTO): optional, separately ticketed hands-on days around the talk days - added depth, no dilution of the curated track, and a real revenue lever. Cite the per-event ratios in [references/format-precedents.md](references/format-precedents.md) rather than averaging them into a single industry figure.

If this is a first edition, size and launch it with `samber/dev-event-organizer-skills@event-first-edition` - its single-focus scope tier deliberately cuts from this catalog, and its ladder-jumping gates (team, budget tiers) are stricter than this menu's.

## Track count - and the content-mix rule it enables

Ranking (default, not a law):

- effort (curation + coordination): `multi-track > single track + open-space afternoon > single track`
- value, content capacity + attendee agency: `multi-track > single track + open-space afternoon > single track`
- value, shared experience + curation control: `single track > single track + open-space afternoon > multi-track`
- efficiency: `single track > single track + open-space afternoon > multi-track`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** One mechanism blocks all three: the two value axes are exact reverses, so whichever rung buys more content capacity gives up shared experience, and no rung is at least equal on both.

Effort is never reached in any pair, and no third axis is printed. The check finds nothing; the ordering rests on the argument that follows.

The two value axes genuinely disagree - that disagreement is the decision. Multi-track buys content volume by selling off the shared story arc and the organizer's editorial control.

- **Single track** - the default, on independent convergence: Strange Loop, GOTO, Monktoberfest, Deconstruct, and SmashingConf all chose it deliberately and give overlapping reasons (shared context, curation as editorial responsibility, the hallway track as a design goal, no sold slots, speakers who stay). Quotes and sources in [references/format-precedents.md](references/format-precedents.md). Treat multi-track as a scale decision, never a quality upgrade.
- **Single track + open-space afternoon** - the DevOpsDays architecture: curated 30-minute talks in the morning, an Ignite block, open space all afternoon. Its quiet advantage: the content-mix rule it enables - tool- and vendor-specific talks are steered to open space, keeping the curated track conceptual. Track count and content policy are one coupled decision; a second curated track would need its own balance policy.
- **Multi-track** - the starved option. Promotion condition (published): a CFP pool oversubscribed ~8-10x beyond slots (swyx's benchmark: 8-12 speakers per day per track; 200-1,200 applicants for a JSConf-tier event), so that multi-track reduces rejection of genuinely strong content. Promote it only alongside added plenary moments (opening keynote, shared lunch, closing) that preserve some shared experience.
  - A second, distinct promotion condition, self-set rather than published: two genuinely different audiences who share the same underlying problem stated at different depths - decision-makers wanting the why, practitioners wanting the how - run as two tracks under one banner rather than as two separate events. Where this fires, tag each session with a maturity level so both a beginner-heavy and an expert-heavy track can carry sessions at the depth its own audience actually wants, rather than one flat difficulty band.

Community-pole guardrail regardless of track count: no sponsor ever buys a program slot; sponsor inventory is expo, side events, and the DevOpsDays-style 1-minute inter-talk slot - never the stage.

## Session-format mix

Compose the day from the catalog; mechanics and failure modes per format live in [references/session-format-catalog.md](references/session-format-catalog.md). Ranking for the marginal program hour (default, not a law):

- effort (organizer hours per program hour delivered well): `panel > workshop day > curated talks > fireside chat > ignite block > open space`
- value (learning + connection + durable assets per hour): `curated talks > workshop day > open space > fireside chat > ignite block > panel`
- efficiency: `open space > ignite block > curated talks > fireside chat > workshop day > panel`

- Default backbone: curated ~25-30 minute talks - the sourced balance point for content, and the event's recorded assets.
- Ignite blocks and open space are the efficiency leaders: near-zero content-curation cost, and they solve real program problems (first-time speaker volume; self-selected relevance and a pressure valve for tool-specific content).
- Fireside chat over keynote for a high-profile guest who is not a polished presenter - the sourced substitution.
- **The workshop day is what this order starves**: second on value, second on effort, so it never wins a marginal program hour. Promotion condition: it stops competing for program hours once it moves out of the program - a separately ticketed bracketing day (see the shape ladder), where it also becomes a revenue lever.
- **Panels sit last on every axis, and for a first event they are deleted, not demoted** (the sourced ladder cuts them entirely - hardest format to execute, most-criticized: Fred Wilson, Brad Feld, Scott Berkun, Duncan Green, by name in the catalog reference). **Promotion condition for an established event, keyed to Q10**: a strong, prepared, willing-to-interrupt moderator with pre-briefed provocative questions, and no long self-introductions. Absent that moderator, the option stays off the menu.
- Protect the hallway track as a format choice, not leftover time: long breaks, good food, quiet rooms (Monktoberfest optimized its start time around it).

## Delivery mode

Ranking (default, not a law - Q8 evidence can promote the starved rung):

- effort: `interactive hybrid > fully virtual == in-person with record-and-post`
- value (engagement depth + reach): `interactive hybrid > in-person with record-and-post > fully virtual`
- efficiency: `in-person with record-and-post > fully virtual > interactive hybrid`

The `==` is argued: each single mode is one full production, and the cost centers substitute for each other. CHI's published figures price the hybrid platform "similar… to a physical convention centre rental," and MLH warns "a well run digital hackathon is more than just a Discord."

CHI's other figure - virtual logistics support at double the physical event's - prices the virtual layer of a hybrid run, not a standalone virtual production, so it does not break the tie. Hybrid is not a third production of the same size; it is both at once.

- **In-person with record-and-post** - the default and the pattern that survived the post-2022 shake-out: full room, talks recorded and posted (or streamed one-feed, unmonitored) afterward. The remote audience gets the content asynchronously without a second live production.
- **Fully virtual** - legitimate when the community itself has cost or access reasons to stay all-remote (MLH's digital format is global by design). A deliberate single-mode choice, not a downgrade.
- **Interactive hybrid** - the starved option for conferences, argued on the published record: hybrid roughly doubled AV and logistics cost, virtual fees did not cover virtual costs, CHI 2022 lost $484,886, and free livestreams draw well under 10% of sign-ups (figures and caveats in [references/delivery-mode-evidence.md](references/delivery-mode-evidence.md)). Promotion condition: remote registrations reliably above ~25-30% of paid attendance **and** covering their marginal cost, plus a dedicated production budget sized for roughly double AV/logistics. For **hackathons, hybrid is deleted, not starved**: MLH refuses hybrid outright ("worse for both organizers and hackers") with a named failure-mode list - pick in-person or digital and commit.

## Hackathon demo/judging structure

Structural choice only - rubric, weights, and jury mechanics belong to `samber/dev-event-organizer-skills@hackathon-judging`. Ranking (default, not a law; borrowed from adjacent practice - see the catalog reference):

- effort (judge-hours + staging per team): `two-stage expo-then-finals > stage pitch > expo table > video only`
- value (judge interaction depth + winner-narrative legibility): `two-stage expo-then-finals > stage pitch > expo table > video only`
- efficiency at scale: `video only > expo table > two-stage expo-then-finals > stage pitch`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** Value and effort are the same list, so one mechanism blocks every pair: the structure that buys deeper judge interaction costs strictly more judge-hours and staging.

Nothing else is printed that could block or rescue a pair. The check catches no misordering; what follows is argument, not verification.

- **Expo table** - the default: real judge-demo interaction, parallel so it scales.
- **Two-stage** - the starved option: top of both value axes, top of effort, so efficiency never picks it; **promotion condition, keyed to Q11**: press or sponsor reporting needs a legible on-stage finale.
- **Video only** - the digital-format default and the only structure that scales past what judge-hours allow.

Match format to jury composition: technical judges need to touch the demo; business judges need the narrative slot.

## Failure modes

- **Hybrid chosen as the safe compromise.** It is the maximum-cost, maximum-risk option, not the middle: two simultaneous productions, doubled AV/logistics, and a remote audience that reports feeling second-class. Weigh the sourced cost list; don't split the difference.
- **Multi-track read as a quality upgrade.** Five independent single-track manifestos say otherwise; multi-track is a scale and agency decision with a sourced promotion trigger. Reaching for it below ~8-10x CFP oversubscription buys empty rooms and a fragmented event.
- **Graduating the ladder on headcount alone.** The sourced gates are content depth, venue-risk tolerance, and speaker supply. GopherCon debuting at 700 does not make 700 a threshold; DartUP jumped at 250.
- **Inventing an industry-average workshop percentage.** Cite the named-event ratios and let the spread between them stand; collapsing them into one number invents a norm the events themselves do not share.
- **A panel scheduled to flatter sponsors or fill a slot.** The sourced consensus is brutal; without the prepared-moderator promotion condition, replace it with a fireside chat or one more curated talk.
- **Track count and content policy decided separately.** The single curated track is what makes a "conceptual talks on stage, tool talks in open space" rule enforceable - decide them together or the rule dies in track two.
- **Copying a named event's structure without its constraints.** Monktoberfest's smallness and Strange Loop's curation are worked-backward-from-venue, turn-down-hundreds choices. Import the reasoning, not the surface shape.
- **Selling program slots to cover the format's cost.** Every sourced community event refuses stage inventory to sponsors; funding structure belongs to `samber/dev-event-organizer-skills@event-budget`, not to the program.

## Measurement

Format choices are testable edition over edition. Each measure below is marked published or self-set; adapt the self-set gates per event.

- **Delivery-mode check** (published figures): if a stream or virtual tier ran, compare engaged remote attendance to the sub-10%-of-sign-ups livestream benchmark (indicative only - the figure comes from academic conferencing, not tech; see the reference) and the ~25-30% promotion threshold. Below them, the hybrid spend fails its own test next edition.
- **CFP pressure** (published figures): applicant-to-slot ratio against the ~8-10x multi-track trigger - the only published trigger for adding a track. Read it as the floor where the conversation opens, not as evidence the CFP is broken: swyx's own figures make 8-30x oversubscription normal at a popular single-track event.
- **Workshop sell-through** (self-set): separately ticketed workshop days that don't sell to a threshold you fix in advance (e.g. 60% of capacity) argue for fewer next edition; the bracketing model makes this reversible.
- **Session-mix signals** (self-set): open-space marketplace filling its wall, ignite-slot application volume, room walkouts during panels. Pick 2-3, decide the revision they would trigger, and write both down before the event.
- Sellout speed, attendee retention, and sponsor renewal read on the whole event, not the format - they belong to `samber/dev-event-organizer-skills@event-market-fit`.

## Invocation examples

- "Our Rust meetup pulls 120 people every month. Should we run a conference, and what shape?"
- "We're debating adding a second track next year - the CFP had 90 submissions for 24 slots."
- "The CEO wants our user conference hybrid so remote customers can join live. Talk me through it."
- "Design the day: one day, 200 attendees, community-run, more first-time speakers on stage."

Expected output: a format brief with (1) the chosen shape and the graduation evidence behind it, (2) track count with the content-mix rule it enables, (3) the session-format mix as a day architecture, (4) delivery mode with its promotion/deletion reasoning, (5) for each choice, the sourced trigger that would revise it next edition. Presented section by section for validation, with 2-3 candidate structures and one recommendation up front.

## References

- [references/format-precedents.md](references/format-precedents.md) - graduation trajectories (DartUP, GopherCon, RailsConf/Rails World, North Bay Python), the five single-track manifestos with quotes, the DevOpsDays day architecture, per-event workshop ratios, community-vs-vendor session-selection evidence.
- [references/session-format-catalog.md](references/session-format-catalog.md) - mechanics, costs, and failure modes per session format: curated talks, Ignite, open space, Lean Coffee, keynote/fireside/panel guidance with the named critics, workshop-day model, hackathon judging-format table.
- [references/delivery-mode-evidence.md](references/delivery-mode-evidence.md) - CHI's published hybrid finances, SIGMETRICS retreat, the sub-10% livestream figure, MLH's anti-hybrid failure-mode list, and the benchmarks that would revise the default.

See also, same collection:

- `samber/dev-event-organizer-skills@event-cfp-design` and `samber/dev-event-organizer-skills@event-talk-selection` - the CFP process and talk selection feeding whatever track structure is chosen here.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - venue requirements the chosen structure creates, including hybrid/virtual infrastructure.
- `samber/dev-event-organizer-skills@event-cultural-identity` - turns the shape chosen here into a register, traditions and rituals; a single-track curated day and a multi-track expo carry different cultures and it owns that consequence.
- `samber/dev-event-organizer-skills@workshop-program-design` - runs the workshop day this skill decided to bracket: capacity, facilitator coverage, participant prerequisites and environment setup, and the network posture a room of laptops needs. It never re-argues whether the day exists or how it is ticketed.
- `samber/dev-event-organizer-skills@hackathon-brief-design` - writes the challenge document against the demo and judging structure chosen here. Note the word collision: a _track_ here is a parallel session stream, while a _challenge track_ there is a thematic category a team enters.
