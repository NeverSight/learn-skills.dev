---
name: hackathon-team-formation
description: Decide how participants at a hackathon end up on teams - the published team-size rule including whether solo entry is allowed, the matchmaking mechanic that runs on the day, what happens to someone still unteamed after it, when membership freezes relative to the opening, and any track-conditioned team-composition rule. Use whenever the user mentions hackathon team size, a pitch-and-join or team-matching session, whether solo hackers are permitted, a participant nobody picked, or teams changing mid-event - even if they never say "team formation". Do NOT use to match a stuck team to expertise - use samber/dev-event-organizer-skills@hackathon-mentoring; the rules text is samber/dev-event-organizer-skills@hackathon-brief-design.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Hackathon Team Formation

You decide how people at a hackathon end up building with each other: the team-size rule the brief publishes, the mechanic that runs on the day, what happens to whoever it fails, when membership stops moving, and how all four fit around the opening.

This is the participant-to-participant problem. It is not the participant-to-expert problem, and the two get confused constantly.

## What you own, and what is already decided

You own:

- the team-size number and its solo answer
- the matchmaking mechanic
- the unteamed-participant protocol
- the mid-event change policy
- any track-conditioned composition rule

Four things arrive from, or leave for, siblings - hand them over rather than re-deciding them:

- **The published rules text** belongs to `samber/dev-event-organizer-skills@hackathon-brief-design`. Its interview asks this skill for the team-size rule by name, and its pre-publication threshold counts that rule as one of seven items that must exist. You decide the number and the wording intent; that skill prints it.
- **Matching a stuck team to expertise** belongs to `samber/dev-event-organizer-skills@hackathon-mentoring`. Draw the boundary this way: a participant who cannot find a team is this skill's problem, a team that cannot find help with a technology is that skill's. Never build a mentor request channel here.
- **The run-of-show slot** - where the pitch round or mixer actually sits in the day and what it displaces - belongs to `samber/dev-event-organizer-skills@event-run-of-show`. You supply the duration and the ordering constraint; it schedules against them.
- **Prize eligibility and who may receive a payout** belong to `samber/dev-event-organizer-skills@hackathon-cash-prize`. A team-size cap changes how a non-cash prize divides; say what the roster is, never what it is worth.

Every menu below, with its rungs and its axis orderings, is this skill's own construction: reasoned from mechanism, not measured against event data. Each ranking is a default, not a law. Re-rank every one after the interview against what you already know about this edition:

- last year's registration data
- a returning cohort that arrives in formed teams
- an organizing team who has run a mixer before
- a venue with one room and no second space

## Interview

Ask one question at a time, multiple-choice where possible. Questions 2 to 9 each key a rung, a delete condition or a promotion condition; no default below can be picked without those answers.

1. Is the event themed with organizer-supplied problems, open with participants bringing their own, or both?
2. How long is the hacking window, and do the opening ceremony and the start of hacking sit in the same block or on different days?
3. Of the people registered so far, how many registered as an existing team, and how many registered alone? An estimate is a real answer; "we do not collect it" is the most useful answer of all.
4. What share of the cohort is at their first hackathon, and does registration ask anything about skills, role or what someone wants to work on?
5. Is a demographic or skill-level track required - a beginners track, a first-timers quota, a student-only category - and does anything in it depend on a fraction of the team rather than the individual?
6. How many rooms does the event occupy, and is there a second space available for a facilitated session?
7. Are prizes awarded against a submitted project, and may minors participate?
8. Is this a one-off edition or a recurring one whose mechanic should still work next year, and when must the rules be published?
9. What is the effort ceiling: organizer hours before the event, and how many named people are actually free during the hacking window rather than nominally on the schedule?

Q8 and Q9 each move a named rung. Say which as you re-rank.

- **Q8, near publication date:** promotes the adopted size rule over anything drafted, and demotes pre-event matching, whose whole cost is reading registrations that have not arrived yet.
- **Q8, recurring edition:** promotes the rungs written once and reused, the size rule with its carve-out and a pitch-round script, because their cost amortises where a one-off pays it in full.
- **Q9, effort ceiling in organizer hours:** does not touch the safety net.
- **Q9, effort ceiling in people free during the window:** removes the floor sweep and the escalation outright, because both are somebody's attention and nothing else. Say that rather than pretending a rota exists.

## Workflow

1. Run the interview. Read last edition's registration data first if one exists; Q3 and Q4 are the answers it settles.
2. **Fix the team-size rule before the mechanic.** The mechanic has to produce teams the rule allows, and a mixer that forms sixes under a cap of four wastes the room. Hand the rule to `samber/dev-event-organizer-skills@hackathon-brief-design` as soon as it is decided.
3. **Pick the matchmaking mechanic** and state its duration and its ordering constraint. Load [references/matchmaking-mechanics-and-run-sheets.md](references/matchmaking-mechanics-and-run-sheets.md).
4. **Decide the unteamed-participant protocol before the day, not during it.** Load [references/unteamed-participant-protocol.md](references/unteamed-participant-protocol.md).
5. **Set the change policy and its cut-off**, and check it against step 4 - a freeze that lands before the safety net runs cancels the safety net.
6. **Stock the project backlog** if the mechanic or the safety net depends on one, and size it against Q1. Load [references/team-size-and-composition-rules.md](references/team-size-and-composition-rules.md).
7. Hand the slot, its duration and its position to `samber/dev-event-organizer-skills@event-run-of-show`, and the rule text to the brief.
8. Publish before registration closes. A team-size rule added after people have already agreed to hack together disqualifies teams that already exist.

Present the decision set section by section for validation - size rule, mechanic, safety net, change policy - never as one block. Get explicit approval before the rule goes into the brief; publication is the point of no return.

If your harness has persistent memory, record:

- the size rule and whether solo entry was allowed
- the mechanic and its measured duration
- how many people were still unteamed when the sweep ran
- what each of them ended up doing

The last one is the only number that tells you whether any of this worked, and no other event's figure substitutes for it.

## Team-size policy

Four rungs: no stated rule, a stated cap only, a stated range that includes solo, and a range plus a track-conditioned composition rule.

- value (disputes prevented at submission, a solo entrant knowing before arriving that they may enter, and a carve-out that is actually enforceable): `range plus composition rule > stated range including solo > stated cap only > no stated rule`
- effort (deciding the number, wording it, and checking it against every track): `range plus composition rule > stated range including solo == stated cap only > no stated rule`
- compliance cost, as the review each rung triggers and the reversibility it costs: `range plus composition rule > no stated rule > stated cap only > stated range including solo`
- efficiency: `stated range including solo > stated cap only > no stated rule > range plus composition rule`

**Dominance structure: 6 pairs, exactly one strict-dominance relation.** The stated range including solo beats the cap alone on value, ties it on effort, and beats it on compliance cost, so it dominates. The efficiency line honours this by ranking the range first.

None of the other three rungs dominates:

- the composition rule (top of every cost axis)
- no stated rule (dominates nothing)
- the cap (dominates nothing)

A wrong ordering here would have failed the check, so this pass carries information.

**The `==` on effort is argued, not a dodge.** A cap and a range are the same sentence: deciding a maximum already forces the question of whether one person counts, so the cap does not save the decision; it just declines to write it down. Both land under an hour, and the cap only looks cheaper because its deferral is invisible until someone registers alone.

- **Stated range including solo** - the default, and the strongest single recommendation this skill makes.
  - Copy-paste text from a published organizer guide: "Teams can be 1-4 people".
  - The same guide's own reason for the cap: "We see hackers have the most success with teams of a maximum size of 4", offered as one organizer network's practitioner observation, with no study cited behind it.
  - Take the shape; decide the number for your own event.
- **Stated cap only** - real value for the same minutes, and it leaves the question the source poses explicitly, "Can hackers participate solo?", unanswered until somebody asks at the registration desk.
- **No stated rule** - **delete it, from this menu and from the axis lines above, as soon as a brief is published at all** (Q8). `samber/dev-event-organizer-skills@hackathon-brief-design`'s own pre-publication threshold counts the team-size rule as one of seven items that must exist with zero blanks; shipping without it leaves that check at six. It also ranks second on compliance because it triggers no review beforehand and defers the whole adjudication to the least reversible moment there is - a prize decision, in public, with a team standing there.
- **Range plus composition rule** - the starved option: top of value, top of effort, top of compliance cost.
  - Promotion condition, keyed to Q5 and Q7: a track whose eligibility depends on a fraction of the team rather than on each individual.
  - Published example: "Beginners track where at least half the team must have this be their first hackathon".
  - The same source's procedural rule: "Make sure to state how many of the team members must fit the category in your rules before the event."
  - Treat the fraction as the thing to decide and "half" as one event's number.

**Why the composition rule tops the compliance axis.** A fraction keyed to "first hackathon" is a skill-level proxy and reviews cheaply. A fraction keyed to age, student status, gender or disability is a carve-out on a protected characteristic: it needs review before publication by whoever owns that exposure for the organizing entity, and it cannot be withdrawn mid-event without re-scoring a whole track. Decide which kind yours is before writing it, and route the second kind rather than wording it yourself.

## Matchmaking mechanic

Five rungs: no formal matchmaking at all, a pitch-and-join round, a persistent project board, a facilitated mixer, and pre-event matching from registration data. Two value axes, because they genuinely disagree.

- value, coverage (share of participants who end the mechanic in a team of their choosing): `pre-event matching > facilitated mixer > pitch-and-join round > persistent project board > no formal matchmaking`
- value, project fit (the team that forms has a buildable thing to build and the skills to build it): `pitch-and-join round > pre-event matching > persistent project board > facilitated mixer > no formal matchmaking`
- effort (organizer setup, run-of-show minutes, and coordination during the window): `pre-event matching > facilitated mixer > persistent project board > pitch-and-join round > no formal matchmaking`
- efficiency: `pitch-and-join round > persistent project board > no formal matchmaking > facilitated mixer > pre-event matching`

**Dominance structure: 10 pairs, exactly one strict-dominance relation.** The pitch-and-join round beats the persistent board on coverage, on project fit, and on effort simultaneously, so it dominates. The board reaches only whoever walks past it, carries a project statement with nobody standing next to it to answer questions, and still costs a surface plus somebody maintaining it all day. The efficiency line honours that by ranking the round above the board.

None of the other three rungs dominates:

- pre-event matching (top of the effort axis)
- the mixer (loses project fit to both the round and the board)
- no formal matchmaking (bottom of both value axes)

The other nine pairs each trade one axis against another. The check verifies nothing about them, so their ordering rests on the arguments below.

**Why the two value axes split.** A pitch round forms teams around a project somebody has already articulated and committed to building. A mixer forms social groups that then have to invent a project, which is the slowest possible route to a first commit. Coverage and fit are not the same quantity, and a mechanic that maximises one can starve the other.

- **Pitch-and-join round** - the default, and the only mechanic with a published run sheet behind it.
  - "Hacking begins with project introductions. Participants that bring projects to the event have an opportunity to briefly (1 minute max) explain what they are working on at the very start of the event so that other participants can join that project".
  - The same source names the anti-pattern that ruins it: "Do not allow anyone to pitch an idea that they will not be working on at the event, unless there really are not enough ideas to go around."
  - Groups formed this way are described as "about 2-5 individuals", a range observed at that author's civic-tech events, not a target to enforce; it sits alongside rather than inside the 1-4 cap above.
  - Two aids scale the round past a small room. Both are this skill's own suggestions, not published practice:
    - a marker per pitcher, readable across the space and tied to their spot, so a crowd finds a project without queuing
    - a skill-coded wristband issued at check-in, so the room self-balances by discipline
- **Persistent project board** - the rung the dominance check rules out, kept on the page because it is what an organizer reaches for when the pitch round runs late and gets cut. Naming it is how you notice that happened.
- **No formal matchmaking at all** - a real rung, and correct at an event where the cohort registers as formed teams: its coverage equals any other mechanic's for zero cost, because everyone already has a team. **Delete it, from this menu and from the axis lines above, as soon as Q3 shows anyone registering without a team.** From that moment silence is not a light-touch choice; it is a decision to leave those people to the room.
- **Facilitated mixer** - a starved option: second on coverage, second on effort, and fourth on project fit. Promotion condition, keyed to Q4 and Q6: a cohort mostly at its first hackathon, where too few people brought projects for a pitch round to absorb the room, **and** a second space exists to run it in. Never promote it on the first condition alone - a mixer in the hacking room displaces the hacking.
- **Pre-event matching from registration data** - the other starved option: top of coverage, top of effort, and the only rung that works before anyone is in the building.
  - Published as a practice rather than a mechanic: the same guide's registration form asks "What kind of hacker are they?" with the examples "Developer. Designer. Data Scientist. Domain Expert. Government Staff. Communicator. Project Manager. Advocate."
  - It also instructs the organizer to "Literally try to imagine how each registered participant will keep occupied at the event based on whatever information you know about them."
  - Promotion condition, keyed to Q3 and Q4: registrations are majority solo **and** registration already collects a role or interest field.
  - Without that field the rung is not expensive but impossible: adding the field after registration opens reaches nobody who already signed up.

Every rung above is a mechanic, not a product; a spreadsheet, a wall and a chat channel each implement several of them, and naming a platform dates the skill without settling anything.

## The unteamed participant

Four rungs: solo normalized only, plus a pre-stocked project backlog, plus a floor sweep by a named person, plus a time-boxed escalation.

- value (a participant who wanted a team and did not get one is reached before they leave): `time-boxed escalation > floor sweep > pre-stocked backlog > solo normalized only`
- effort (pre-event stocking, and a named person's attention during the window): `time-boxed escalation > pre-stocked backlog > floor sweep > solo normalized only`
- compliance cost, as the review each rung triggers and the reversibility it costs: `time-boxed escalation > floor sweep > pre-stocked backlog == solo normalized only`
- efficiency: `floor sweep > pre-stocked backlog > solo normalized only > time-boxed escalation`

**Dominance structure: 6 pairs, zero strict-dominance relations.** Two mechanisms block all six pairs:

- **The ordinary block (5 pairs):** the higher-value rung of the pair costs strictly more effort, more review, or both.
- **The near-miss (1 pair):** the floor sweep genuinely beats the backlog on both value and effort, since one person already walking the room can add a question to a round they were already making, while stocking a backlog is pre-event writing. Only the compliance axis stops it dominating: approaching and identifying an isolated participant costs more review than writing project ideas does.

The check finds nothing here, though one pair came within a single axis of a relation. The efficiency line therefore rests on the arguments below rather than on any verification.

**Why compliance is a real axis here and not decoration.** A sweep singles out a named person on the basis of an observation about their social situation, and an escalation records it and routes them. Where minors participate (Q7) that is a safeguarding interaction, not a hospitality one, and it needs the same posture `samber/dev-event-organizer-skills@event-accessibility-inclusion` sets for accommodation data: who may hold it, for how long, and what is never written down. The lower two rungs touch nobody's data at all, which is the argued `==`.

- **Floor sweep by a named person** - the default, and it comes from a published guide: "Have someone managing the hacking room... See if anyone needs anything or can't find something to work on". Its cadence, its owner and what the sweeper offers are yours. Note the coupling before choosing this alone: a sweep's value is capped by where it can route someone, which is either a stocked backlog or a team known to be short-handed.
- **Pre-stocked project backlog** - also published, and the mitigation that reduces how often anyone is unteamed at all: "have ideas for new projects that are especially easy for participants to get started with if they can't join an existing project. Having project ideas ready is especially important if you do not expect many participants to bring projects!" The same source sets the test of whether a project is genuinely joinable rather than merely listed - "ready-to-go tasks for newcomers with a variety of skills and at a variety of skill levels", with a build environment that "can be spun up in less than 20 minutes".
- **Solo normalized only** - published and genuinely valuable. "A project of one, meaning someone working alone, is okay too!" is the plainest statement that solo work is a legitimate outcome rather than a failure, and it should be said out loud at the opening whatever else you do.
  - **Delete it as the whole answer, from this menu and from the axis lines above, as soon as any matchmaking mechanic above "no formal matchmaking" is published.**
  - Announcing a mechanic creates an expectation of being teamed. Answering the person it failed with "solo is fine" answers a question they did not ask.
- **Time-boxed escalation** - the starved option, top of all three axes, and this skill's own construction rather than reported practice: nothing published describes an escalation for an unteamed participant. It is a named owner, a moment at which still-looking stops being the participant's problem, and a stated ask. Promotion condition, keyed to Q4 and Q7: a cohort mostly at its first hackathon, or minors participating, where being alone all day is not plausibly a preference.

**Do not invent the duration.** Nothing published anywhere gives a number of minutes after which an unteamed participant should be escalated, and a plausible-sounding figure here would be fabrication wearing a benchmark's clothes.

Anchor the time-box to a clock the run of show already contains instead, for example:

- the end of the pitch round
- the first meal service
- the first workshop break

Record what it actually took at your event, so the next edition has one real number where the field has none. The protocol, the sweeper's script and what the escalation may and may not offer are in [references/unteamed-participant-protocol.md](references/unteamed-participant-protocol.md).

## Mid-event team changes

Four rungs: no stated policy, membership frozen at a published moment, open until a published cut-off then frozen, and open throughout with an attribution rule. Nothing standard governs a team changing after it forms. Every rung, every axis line and both dominance relations below are this skill's own construction, reasoned from mechanism and never observed at an event.

- value (a team that gains or loses someone can still submit, and authorship is not disputed at judging): `open until a cut-off > open throughout with an attribution rule > frozen at a published moment > no stated policy`
- effort (publishing the rule, and reconciling the roster at submission): `open throughout with an attribution rule > open until a cut-off > frozen at a published moment == no stated policy`
- compliance cost, as the review each rung triggers and the reversibility it costs: `no stated policy > open throughout with an attribution rule > open until a cut-off > frozen at a published moment`
- efficiency: `frozen at a published moment > open until a cut-off > open throughout with an attribution rule > no stated policy`

**Dominance structure: 6 pairs, two strict-dominance relations.** Two pairs carry information here, which is the most any menu in this skill gets:

- freezing at a published moment beats the no-stated-policy rung on value, ties it on effort, and beats it on compliance, so it dominates
- open-until-a-cut-off beats open-throughout on all three axes, so it dominates too

The efficiency line honours both. Neither the cut-off nor open-throughout dominates the freeze, since each buys its value with strictly more effort, and the no-stated-policy rung dominates nothing.

**The `==` on effort is argued.** Both rungs cost roughly one sentence and roughly nothing at the submission desk. The difference is not size but timing: the freeze spends its hour before the event; the no-stated-policy rung spends the same hour at the desk, under deadline, with no rule to apply. That is why the two rungs separate on the compliance axis rather than this one.

- **Frozen at a published moment** - the efficiency leader and, deliberately, **not the recommended default.**
  - Promotion condition, keyed to Q3 and to your own step-4 decision: as soon as you adopt any safety-net rung above "solo normalized only", move up to the cut-off.
  - A freeze set at the pitch round makes the sweep unable to place anybody, because the team with room for them is no longer allowed to take them.
  - This is the one place in this skill where the ratio is knowingly overruled, by a decision the skill itself made two menus earlier rather than by taste.
- **Open until a published cut-off, then frozen** - the recommended default for that reason. It keeps the roster movable through the hours the safety net actually operates in and fixes it before judging starts, so the list handed to `samber/dev-event-organizer-skills@hackathon-judging` and to `samber/dev-event-organizer-skills@hackathon-cash-prize` is the list that gets scored and paid.
- **Open throughout with an attribution rule** - the starved option, and the rung the check rules out. Promotion condition, keyed to Q2: a multi-day or week-long window, where a team losing a member on day three otherwise cannot submit at all and a freeze is the harsher rule.
- **No stated policy** - **delete it, from this menu and from the axis lines above, as soon as prizes are awarded against a submission** (Q7). Without a rule, the question of who is on the team is settled at the moment it is worth the most money and can be reversed the least.

**Where a composition rule and a change policy collide.** If a track-conditioned fraction was published on the first menu, say what happens to a team that stops satisfying it after someone leaves.

- Deciding it in advance costs a clause.
- Deciding it at judging costs a track.

## Timing against the opening

Three pieces of timing are published:

- **Placement, and it is worth copying.** The pitch round runs immediately after the welcoming session, not as a separate slot later. The same guide's day-of agenda puts the welcome first - organizers, sponsors, history, code of conduct, logistics - and then: "Anyone who has brought a project to work on should then introduce the project to everyone."
- **The mechanic that keeps the round inside its budget.** "Project leaders tend to talk for as long as they can, so you may need to cut them off after one minute". It is framed for the pitcher as "not as recruiting but as boasting how awesome their day is going to be".
- **A scale marker, easy to misread.** "In a small event (up to about 30 people), you can have all of the participants introduce themselves". That threshold governs _everyone introducing themselves_, not the pitch round, which happens either way.

Everything else about timing is this skill's own construction. Nothing published says:

- how long before hacking a size rule should be announced
- whether pre-event matching should run at registration or a week out
- how a two-day event's second morning handles arrivals

Derive those from the ordering constraint instead:

- the size rule is published with the brief
- the mechanic runs before the first line of code
- the change cut-off lands before judging opens
- the safety net operates in the gap between the mechanic and the cut-off

Hand the durations to `samber/dev-event-organizer-skills@event-run-of-show` and let it place them.

## Role coverage instead of headcount

When a team asks what it is missing, answer in functions rather than in people. One published role model exists, from a hardware-hackathon guide, naming four core roles for a "strong" multidisciplinary team:

- programmer
- fabricator
- designer
- visionary, named explicitly as project management

Plus one duty tied to no headcount: "Someone on the team should also be focused on quality assurance and debugging". The full scope of each role is in the sizing reference.

A software-only event has no fabricator, and the roles listed are that build's physical dependencies. The structure carries over, the list does not: name three or four functions a team needs covered, keep them separate from headcount so a four-person cap and a five-function list stay compatible, and let the mechanic surface who fills which. That carry-over is this skill's own reasoning, not a published software-event role model.

The same source's recruiting rationale is the part most often skipped: it asks organizers to invite people who "may not self-identify as 'hackers'", because a coder-only applicant pool makes skill balance impossible at matchmaking time whatever mechanic you picked. Your equivalent function split is yours to write; the guide supplies the shape, not the list.

One published figure covers project supply. At themed hackathons: "ensure that there is at least one subject matter expert + workable project for about every four non-expert participants".

Carry all four of its bounds on every use:

- it is **themed** events only, where projects are confined to one problem domain
- it counts **non-expert participants**, not teams and not registrations
- its expert is a **domain expert embedded in one project**, not a floating mentor
- it is a **project-supply** target, whose purpose is to stop the room splitting off a third group of "participants struggling to find something relevant to work on" rather than to staff anything

`samber/dev-event-organizer-skills@hackathon-mentoring` carries the fuller scoping and the standing warning never to convert it into mentors per participant. Read it there before reusing the number anywhere else.

## Failure modes

- **Freezing membership before the safety net has run.** The ordering mistake this skill exists to prevent: the mechanic identifies someone unteamed, a short-handed team wants them, and the published rule forbids it. Fix: set the change cut-off after the sweep, not at the pitch round.
- **Answering the unpicked participant with "solo is fine".** It is the right thing to say at the opening and the wrong thing to say to the one person it failed. Fix: route to a short-handed team or a stocked project first, and offer solo as a choice rather than as the outcome.
- **A mixer with nothing stocked behind it.** Social groups form, then discover they have no project and no leader, and dissolve by lunch. Fix: never run a people-first mechanic without a backlog.
- **A pitch from someone who will not build it.** It consumes the round's minutes and leaves joiners attached to a project with no author. Fix: state the rule before the round opens and enforce the cut-off.
- **A team-size cap that contradicts the prize.** A non-cash prize counted per person against a cap of four is a different promise from cash divided arbitrarily. Fix: check the roster rule against `samber/dev-event-organizer-skills@hackathon-cash-prize` before publishing either.
- **A composition fraction adjudicated after teams form.** A first-timer quota discovered at submission excludes teams that already exist and had no way to know. Fix: publish the fraction with the brief.
- **Treating a matchmaking format as universally accessible.** A room-wide pitch round and a facilitated mixer both assume comfort with speaking to strangers at volume, which is an access question independent of the unteamed-outcome one. Fix: offer a non-verbal route to the same mechanic and take the design question to `samber/dev-event-organizer-skills@event-accessibility-inclusion`.
- **Collecting registration signals nobody uses.** A skills field on the form buys nothing unless a named person reads it before the day. Fix: only add the field if pre-event matching is actually the chosen rung.

## Measurement

Every gate below is self-set rather than an industry standard; say so when presenting it. Teams-formed rate, solo-entry share, time-to-team and unteamed count are not comparable across events, so do not borrow another event's figure as a target.

**Pass threshold (structural, one only):** before the brief is published, all five of these exist in writing with zero blanks:

- the team-size rule with its solo answer
- the composition fraction, if any track needs one
- the named mechanic with its duration
- the named owner of the safety net
- the change cut-off expressed as a wall-clock time

Iterate until the count is five.

**Coverage gate (on the day):** after the mechanic ends, the number of participants not yet on a team is a known number, not an impression. If nobody can state it, the sweep has no target and the escalation has no trigger.

Signals to record for next edition (self-set):

- how many registered alone versus as a team
- how many were still unteamed when the sweep ran
- what each of them did next
- how long the pitch round actually took against its budget
- how many teams changed membership after the cut-off would have fallen

The field publishes none of these, so your own second edition is the only comparison you will ever have.

## Invocation examples

- "What team size should our 200-person hackathon allow, and do we let people compete solo?"
- "How do we run team formation on the day? Most of our registrations are individuals."
- "Somebody didn't get picked by any team and doesn't want to work alone. What do we actually do?"
- "Can a team add a member on Saturday afternoon? Where do we draw the line?"
- "Our beginners track needs half the team to be first-timers - how do we word and enforce that?"

Expected output: a team-formation decision set with:

1. the team-size rule with its solo answer and any composition fraction, handed to the brief
2. the chosen mechanic at a named rung with its duration and its ordering constraint, handed to the run of show
3. the unteamed-participant protocol with a named owner and a time-box anchored to the day's own clock
4. the change policy with its cut-off as a wall-clock time
5. the signals to record

Presented section by section for validation before anything reaches the brief.

## References

- [references/team-size-and-composition-rules.md](references/team-size-and-composition-rules.md) - the adoptable size-rule wording, the composition-rule mechanics and the protected-characteristic split, role coverage written out, project-backlog sizing, and the registration fields each mechanic needs.
- [references/matchmaking-mechanics-and-run-sheets.md](references/matchmaking-mechanics-and-run-sheets.md) - the five mechanics as run sheets, the pitch-round script and cut-off enforcement, board and mixer design, pre-event matching from registration data, and a positive and negative worked pair.
- [references/unteamed-participant-protocol.md](references/unteamed-participant-protocol.md) - the sweep and the escalation written out with what each may offer, the accessibility and safeguarding overlays, and what never gets written down.

See also, same collection:

- `samber/dev-event-organizer-skills@hackathon-brief-design` - publishes the team-size rule and any composition fraction as brief text; its interview names this skill as the owner of the number.
- `samber/dev-event-organizer-skills@hackathon-mentoring` - matches teams to expertise; this skill matches participants to each other, and that skill carries the full scoping of the themed-event expert ratio.
- `samber/dev-event-organizer-skills@event-run-of-show` - places the mechanic in the day against the durations and ordering constraint this skill supplies.
- `samber/dev-event-organizer-skills@hackathon-judging` - receives the frozen roster; a membership change after its window opens re-opens a scored result.
- `samber/dev-event-organizer-skills@hackathon-cash-prize` - decides what the roster is worth per person, which is why a size cap has to be settled before a non-cash medium is chosen.
- `samber/dev-event-organizer-skills@event-volunteers` - supplies and rosters the named person the sweep and the escalation depend on.
