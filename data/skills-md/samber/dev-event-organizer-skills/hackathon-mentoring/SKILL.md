---
name: hackathon-mentoring
description: Design the mentor programme for one hackathon edition - coverage depth sized against the challenge tracks rather than a headcount, recruitment through community and sponsor channels, expertise tagging matched to the brief's tracks and any sponsor API, the request mechanic a stuck team uses to reach a mentor, the mentor briefing including the help-versus-build boundary, and rotation by expertise across shifts. Use whenever the user mentions how many mentors a hackathon needs, recruiting or briefing mentors, how a stuck team reaches help during the hacking window, or what a mentor may touch in a team's repository - even if they never say "mentoring". Do NOT use for generic shift and roster mechanics - use samber/dev-event-organizer-skills@event-volunteers instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Hackathon Mentoring

You design the mentor programme for one hackathon edition: how much coverage the field needs, who supplies it, how a stuck team reaches it, what mentors are told before they start, and how coverage rotates across the hacking window.

Read the published brief before designing anything. Two things in it drive every menu below:

- The challenge tracks, which name the expertise that has to be on the floor.
- The sponsor-integration depth, which measures how hard a promise the event has already made.

`samber/dev-event-organizer-skills@hackathon-brief-design` states the boundary from its own side: it names this skill as the owner of mentor coverage, including for a sponsor's API, and confines itself to stating that mentors exist.

Treat every ranking below as a default, not a law. Re-rank each menu after the interview against what this event already holds: a returning mentor crew, a sponsor whose staff are contractually committed, a hacking space of one room, an organizing team who all know the sponsor's API.

## A mentor is not a volunteer, and not a judge

**Treat a mentor as its own role, never a volunteer subtype.** MLH's documents state the parity outright: its Code of Conduct names "Sponsors, judges, mentors, volunteers, organizers, MLH staff, and anyone else participating in the event" as parallel categories, and its organizer guide gives mentors their own recruitment channel, their own chat channel and their own role marker rather than routing them through a general volunteer sign-up.

That is an identity claim, not a mechanics claim. **Borrow the staffing arithmetic rather than rebuilding it.** The coverage rule in `samber/dev-event-organizer-skills@event-volunteers` - "do not leave your post until you have confirmation of a replacement" - applies to a mentor shift unchanged.

`samber/dev-event-organizer-skills@event-volunteers` owns:

- Bottom-up roster sizing from posts and hours.
- Arrival buffers.
- Sign-up confirmation.
- The no-show and replacement protocol.
- Shift-linked recognition.

This skill owns what that skill has no concept of:

- Expertise tagging.
- Coverage depth by topic.
- The request mechanic.
- The help-versus-build briefing.

**Judges are not mentors**, and `samber/dev-event-organizer-skills@hackathon-judging` already says so from its side, in those words: mentors "help teams build during the hacking window", while "judges evaluate finished projects afterwards". The word "briefing" names two different documents across the two skills: a jury briefing there, a mentor briefing here. Write **mentor briefing** wherever a reader could confuse them.

**Mentor conduct policy and enforcement are not yours.** Mentors sit inside `samber/dev-event-organizer-skills@event-code-of-conduct`'s existing pipeline like every other named role; do not draft a second one. Yours is narrower and lives inside the mentor briefing: the help-versus-build boundary, and the power dynamic between someone who knows the stack and someone who has been awake for twenty hours.

## The mentor-judge conflict, stated from one side

A mentor who materially helped a team, then judges that team, is a conflict **`samber/dev-event-organizer-skills@hackathon-judging` already owns from its own side**. It states that "a mentor who helped a team build cannot score that team neutrally" and routes the case into its existing recusal ladder: "apply the recusal rule to every team that person mentored". That skill owns the rule and the recusal mechanics.

**This skill owns only the input data**: a mentor-team contact log recording which mentor spent meaningful time with which team, available when the judge pool is assembled.

- Keep the log whenever a confirmed mentor is also on the judge list (Q5).
- State the rule declaratively: a mentor who materially helped a team recuses from judging that team.
- Route the mechanics to that skill rather than deriving a competing ladder here.

**One half of the handshake is still missing on that side:** the recusal rule reaches for "every team that person mentored" without naming where that list comes from. This log is it, and it should be named there when that skill next revises.

## Quantities to refuse, and the one published ratio

Never invent quantities for:

- Mentor-to-participant ratios.
- Evidence linking mentor availability to completion or satisfaction.
- Unblock latency targets.
- Mentor-to-shift staffing formulas.

These numbers feel safe to invent precisely because nothing on the day contradicts them. Argue from the mechanism instead: a blocked team with no route to help abandons the build.

One published ratio exists. Joshua Tauberer's `hackathon.guide` states (under _At Themed Hackathons_) "ensure that there is at least one subject matter expert + workable project for about every four non-expert participants". Its purpose is project supply, not mentor staffing.

The ratio scopes narrowly:

- **Themed** hackathons only (one problem domain).
- Counts **non-expert participants**, not teams.
- Describes **domain experts inside projects**, not floating mentors.

Use it as evidence that expertise, not headcount, is the scarce quantity. Never convert it into a mentors-per-participant formula.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 1-4 and 6-9 exist because the menus turn on them: no default can be picked for the user without those answers.

1. Is the event in person, digital or hybrid; how many rooms does the hacking space occupy; and does the hacking window run through the night?
2. Which challenge tracks does the published brief name, and at what sponsor-integration depth - named funder only, optional bonus challenge, required for one track, or the sponsor's technology as sole substrate?
3. Is the event themed, with organizer-supplied problems, or open, with participants bringing their own?
4. Who is already committed to mentor: community members and alumni, a sponsor's technical staff, or both - and is any sponsor staffing commitment already written into a signed agreement?
5. Is any confirmed mentor also on the judge list?
6. Do prizes carry cash value, and does any sponsor fund one?
7. Have these mentors mentored before, and is this a one-off edition or a recurring event?
8. What is the effort ceiling: organizer hours before the event, whether anyone will coordinate mentors live during the window, and whether a shift grid already exists from the volunteer plan.
9. By what date must the roster close and the request mechanic reach participants? Channels have lead times and the mechanic has to be published before the window opens, so this date constrains both rather than expressing a preference.
10. What already exists that the default ordering assumes away: last edition's mentor list, a university department or user group that would send several people, a sponsor whose staff are already on site for a booth, an organizing team who has built against this API before.

Name which answer moved which rung as you re-rank:

- A close roster date (Q9) promotes community and alumni only, since a warm list answers in days while a sponsor staffing negotiation runs weeks. It demotes the expertise-matched roster, whose tagging and alignment pass are the last work to finish.
- A recurring event (Q7) promotes the boundary-plus-scenario-walkthrough briefing, written once and reused across editions rather than paid for again.
- A low effort ceiling (Q8) demotes the request channel with organizer routing, whose cost is a standing job for the whole window rather than a one-off setup.

## Workflow

1. **Run the interview**, after reading the published brief.
2. **Set coverage depth** against the tracks, not against a headcount. A sole-substrate sponsor integration raises that track's bar from "a mentor is available" to "a mentor is guaranteed on the floor whenever that track is being worked": the brief's own fallback sentence assumes the platform actually gets support.
3. **Pick the recruitment channels** and open them with the lead time the roster deadline demands. Load [references/coverage-and-recruitment.md](references/coverage-and-recruitment.md).
4. **Tag every confirmed mentor with what they actually know**, in the brief's own vocabulary: one tag per challenge track, plus the sponsor technology by name. A tag nobody can match to a track does no routing work.
5. **Hand the roster to the shift machinery you do not own.** Sizing, buffers, confirmation and the replacement protocol belong to `samber/dev-event-organizer-skills@event-volunteers`. You supply the constraint it schedules against: which expertise must be present in which hours.
6. **Choose the request mechanic** and publish it in the same place teams read the brief, before the hacking window opens.
7. **Brief the mentors.** Load [references/mentor-briefing-and-request-mechanic.md](references/mentor-briefing-and-request-mechanic.md).
8. **Record contacts during the window**, meaning which mentor spent meaningful time with which team, whenever a mentor is also judging (Q5). Hand that log to `samber/dev-event-organizer-skills@hackathon-judging`.
9. **Close out.** Record which tracks ran short of coverage and at which hours, then hand the mentor list to whoever recruits next edition.

Present the design section by section for validation before the window opens: coverage depth, recruitment channels, expertise tags, request mechanic, briefing. A request mechanic changed mid-event is a mechanic half the field never learns.

If your harness has persistent memory, record the expertise tags against the tracks they covered, which hours ran short, the request mechanic used and how it failed, and the mentors who would come back.

## Mentor coverage depth

Four rungs: no mentor programme, on-call from organizers, rostered mentor shifts, and a roster matched to the brief's tracks by expertise.

- value (teams unblocked, the sponsor's technology actually reachable, every track covered): `expertise-matched roster > rostered shifts > on-call from organizers > no mentor programme`
- effort before the event (recruiting, scheduling, expertise tagging): `expertise-matched roster > rostered shifts > on-call from organizers > no mentor programme`
- organizer attention consumed during the window: `on-call from organizers > no mentor programme > rostered shifts > expertise-matched roster`
- efficiency: `rostered shifts > expertise-matched roster > on-call from organizers > no mentor programme`

**Dominance check: clean only by construction, and by-construction is never a pass.** Value and pre-event effort are rank-identical, so **one mechanism blocks all six pairs, not some of them**: whichever rung of a pair is higher on value is strictly higher on pre-event effort too, and fails the test before the third axis is consulted.

The third axis diverges genuinely and still rescues nothing. A pair needs value ≥ _and_ both costs ≤, and the effort half is already lost in every pair. Zero strict-dominance relations exist, the check catches no misordering here, and the efficiency line rests entirely on the arguments below.

**Carry the organizer-attention axis anyway, because it is not rank-identical to inverse effort.** Inverse pre-event effort would order these `no mentor programme > on-call > rostered > expertise-matched`; organizer attention orders them `on-call > no mentor programme > rostered > expertise-matched`. The top two swap, and that swap is the finding: on-call is the second cheapest rung to set up and the single most expensive one to live through.

The same swap is why the cheap rung is not the safe one. On-call looks free because nobody is recruited. What it does is route every technical question to the people also running the schedule, at the hour the schedule is hardest to run.

MLH's guide points the other way, asking volunteers to "stay alert on Discord to look for hackers who need help and push them to the above-mentioned mentorship channel", routing questions away from generic staff toward a named mentor pool.

- **Rostered mentor shifts** - the default. Recruiting and a shift grid cost a one-off before the event, and the grid is machinery `samber/dev-event-organizer-skills@event-volunteers` already provides, so the marginal work is a mentor list rather than a scheduling system. It buys the one thing on-call cannot: a named person who is there because that is what they came to do.
- **Expertise-matched roster** - the starved option: top of value and top of pre-event effort, so efficiency never picks it first. The added work is a tag per mentor and an alignment pass against the track hours. Promotion condition, keyed to Q2 and Q3: the brief commits a sponsor technology at **required for one track or deeper**, or the event is themed and its problems come from one domain. Below that, general technical coverage is what teams actually consume.
- **On-call from organizers** - legitimate where the organizing team genuinely holds the field's expertise and is small enough to answer without dropping the run of show. Its cost lands during the window, the moment with no slack in it.
- **No mentor programme** - a real, rankable rung rather than a strawman: an open-theme event where participants bring their own projects and no sponsor technology is named may need none, and Tauberer's guide describes exactly that shape of event. **Delete it, from this menu and from the axis lines above, as soon as the brief names any sponsor technology at required-for-one-track depth or deeper** (Q2). At that point the brief has promised support the event has not staffed, and parking the option at the bottom quietly leaves that promise unfunded.

Coverage arithmetic, expertise-tag vocabulary and the escalation path when no mentor covers a needed skill are in [references/coverage-and-recruitment.md](references/coverage-and-recruitment.md).

## Recruitment source

Four rungs: community members and alumni only, a sponsor's technical staff only, a mixed pool, and a mixed pool plus a written engagement rule telling sponsor staff not to pitch or recruit while mentoring.

- value, expertise coverage across the brief's tracks: `mixed pool with a written rule == mixed pool > sponsor staff only > community and alumni only`
- value, participant trust that the person helping is not selling: `mixed pool with a written rule > community and alumni only > mixed pool > sponsor staff only`
- effort (two recruiting channels, negotiating a sponsor commitment, writing the rule): `mixed pool with a written rule == mixed pool > sponsor staff only > community and alumni only`
- compliance cost, as the review each rung triggers and the reversibility it costs: `sponsor staff only > mixed pool > mixed pool with a written rule > community and alumni only`
- efficiency: `community and alumni only > mixed pool with a written rule > mixed pool > sponsor staff only`

**Dominance check: clean by care.** Exactly one strict-dominance relation exists. The mixed pool with a written rule has equal expertise value, strictly higher trust value, equal effort and strictly lower compliance cost than the bare mixed pool, and the efficiency line honours it by ranking the rule above it.

Community-only never dominates, at the bottom of expertise value; sponsor-only never dominates, at the bottom of trust value and the top of compliance cost. A wrong ordering here would have failed the check, so this pass carries information the other three menus' passes do not.

**Both `==` are argued, not dodges.**

- **Expertise.** The written rule changes what a sponsor representative may _say_, never what they _know_, so the pool's coverage of the brief's tracks is unchanged by it.
- **Effort.** The rule is one paragraph inside a mentor briefing the next menu's default already produces, plus one line handed to `samber/dev-event-organizer-skills@event-sponsor-agreement`: the same order of magnitude as the mixed pool without it, which is minutes against a channel negotiation measured in weeks.

**Why compliance cost re-orders the menu.** A sponsor representative who uses mentor access to pitch a product or recruit a participant creates a disclosure problem. Undisclosed, it surfaces after the event, when the only remedies left are an apology and a sponsorship conversation.

Writing the rule triggers a review before the event that costs a paragraph and reverses next edition. Community-only carries no such exposure at all, which is the other half of why it leads the ratio.

- **Community and alumni only** - the efficiency leader. Publish it as a warm-list ask rather than an open call: reach "existing tutors or teaching assistants to mentor because they already find the value out of mentoring", then "alumni from your school, industry professionals, and your professors". The setting is what fails to transfer. That channel assumes a university hackathon with a department behind it, so a corporate or community event substitutes a user group, a past-participant list or a partner company.
- **Mixed pool with a written engagement rule** - the starved option, and the one to promote deliberately: it tops both value axes and the effort axis, so the cheaper community channel wins the ratio at any event with nothing sponsor-specific to support. Promotion condition, keyed to Q2 and Q4: the brief names any sponsor technology, at any depth, because a community mentor cannot be assumed to know it and the sponsor's own staff are the only people who reliably do.
- **Mixed pool without the rule** - the rung the dominance check rules out, kept on the page because it is what happens by default when nobody writes the paragraph. Naming it is how you notice it happened.
- **Sponsor staff only** - **delete it, from this menu and from the axis lines above, as soon as the brief carries a general track alongside the sponsor track** (Q2) - which is `samber/dev-event-organizer-skills@hackathon-brief-design`'s own default structure. A pool that only knows one platform leaves every general-track team with nobody, and every participant reading a mentor's employer badge as a sales conversation.

Where a sponsor supplies its own staff, that channel is no volunteer sign-up. It is a sponsorship deliverable, negotiated in `samber/dev-event-organizer-skills@event-sponsor-agreement` and delivered against a commitment. Treat a missing sponsor mentor as a fulfilment failure, never as a no-show.

## The request mechanic

How a stuck team reaches a mentor. Five rungs: find someone informally; identifiable mentors and nothing else; a staffed mentor area teams walk up to; a request channel with an organizer routing each request; scheduled office hours.

- value, unblock latency (how soon a team that just got stuck is talking to somebody): `request channel with routing > staffed mentor area > identifiable mentors > find someone informally > scheduled office hours`
- value, expertise match (the person who arrives actually knows the thing): `request channel with routing > scheduled office hours > staffed mentor area > identifiable mentors == find someone informally`
- effort (setup, standing coordination during the window, mentor hours consumed): `request channel with routing > staffed mentor area > scheduled office hours > identifiable mentors == find someone informally`
- efficiency: `identifiable mentors > staffed mentor area > request channel with routing > scheduled office hours > find someone informally`

**Dominance check: clean by care, on one relation out of ten pairs.** The two value axes genuinely disagree, since scheduled office hours are the worst rung for latency and the second best for match, and that disagreement is why this menu is no ladder. Exactly one strict-dominance relation survives it: identifiable mentors have strictly better latency than finding someone informally, equal expertise match and equal effort, so they dominate. The efficiency line honours it.

The other nine pairs each trade one axis against another, so the check verifies nothing about them and their ordering rests on the arguments below.

**Both `==` are argued.**

- **Expertise match.** A visible marker tells a participant who is a mentor and nothing about what that mentor knows, so it buys exactly zero match over asking a stranger.
- **Effort.** Both rungs are near-zero and within the same order of magnitude: one is a stationery decision and a role assignment, the other is nothing at all.

The five rungs, in the efficiency order above:

- **Identifiable mentors** - the default, and the cheapest real intervention on this page. Give mentors a marker a participant can spot across a room and a name in the event's channels; MLH does both, with an "@mentor role" so "hackers can easily differentiate mentors". `samber/dev-event-organizer-skills@event-volunteers` documents the same mechanic working as wayfinding for a different population, which is why the marker survives a budget cut a perk would not. The relation that puts it above informal collapses at exactly one kind of event: one small enough that every participant already knows every mentor by face. Treat that as the re-rank hook, never as an exception to write into the plan.
- **Staffed mentor area** - "a dedicated mentor area that hackers can walk up to with questions". Promotion condition, keyed to Q1: the hacking space runs to more than one room, or the mentor crew is larger than the organizing team, at which point "find one" stops being a reliable instruction.
- **Request channel with organizer routing** - the starved option: it tops both value axes and the effort axis, because the routing is a standing job somebody works for the whole window. The published shape is a channel where "mentors know where to look for requests", with organizers "active on chat" connecting hackers to mentors. Promotion condition, keyed to Q1 and Q2: the event is digital or hybrid, so there is no floor to walk; or the hacking space spans several rooms; or a sponsor track's questions have to reach one named person.
- **Scheduled office hours** - published as a supplement rather than a mechanic: "mentorship office hours: A peer group type of experience where people can ask questions during the assigned time". Excellent expertise match, worst possible latency. **Delete it as the sole route, from this menu and from the axis lines above, when the hacking window runs through hours the office-hour blocks do not cover** (Q1). A blocker at three in the morning does not wait for a ten o'clock slot.
- **Find someone informally** - last on efficiency because the dominance check ruled it out, not because a constraint did. It is what an event with no mentor programme actually does.

**Deleted outright: routing every request through one named organizer's direct messages.** Delete it from this menu and from the axis lines above. It looks like the cheapest possible queue, and it is a single point of failure that fails at the exact hour a hackathon needs it, because that person is asleep.

## Mentor briefing depth

Four rungs: no briefing; logistics only; logistics plus the help-versus-build boundary stated explicitly; boundary plus a scenario walkthrough with rehearsed responses.

- value (teams learn rather than get carried, and the submission stays defensible at prize time): `boundary plus scenario walkthrough > boundary stated > logistics only > none`
- effort (preparation, briefing length, written material): `boundary plus scenario walkthrough > boundary stated > logistics only > none`
- compliance cost, as the review each rung triggers and the reversibility it costs: `boundary plus scenario walkthrough > none > logistics only > boundary stated`
- efficiency: `boundary stated > logistics only > none > boundary plus scenario walkthrough`

**Dominance check: clean only by construction, and by-construction is never a pass.** Value and effort are rank-identical here too, so again **one mechanism blocks all six pairs**: the higher-value rung of every pair is strictly more effort, and no pair survives to be tested against compliance at all.

The compliance axis is non-monotonic and genuinely re-orders the efficiency line. Re-ordering and rescuing are different jobs, and it does only the first. Zero dominance relations exist, the check verifies nothing, and the ordering rests on the argument below.

**The compliance axis is authorship contamination, and it mirrors `samber/dev-event-organizer-skills@hackathon-judging`'s conflict-of-interest pattern deliberately.** A mentor who writes code into a team's repository with no stated boundary creates a contestable-authorship problem. It surfaces at the ceremony, with prizes on the table and nothing published to point at: the least reversible moment there is.

That is why **"none" is cheapest on effort and second-highest on compliance cost**, and why the default is not the cheapest rung. The exposure is real rather than theoretical: `samber/dev-event-organizer-skills@hackathon-brief-design` cites a published requirement that submitted code be public and stay public to remain prize-eligible, so the commits are readable and so is whose they are.

The walkthrough tops the same axis for the opposite reason. It is a written standard the event can then be held to, so it triggers a review before it ships and is the hardest rung to withdraw once mentors have been briefed on it. That is the same shape as `samber/dev-event-organizer-skills@hackathon-judging`'s disclosure-registry rung, which tops its own compliance axis for exactly that reason.

- **Boundary stated explicitly** - the default, and the lowest compliance cost of the four. Decide the line once, before the event, while it costs a sentence and a mid-window reminder can still correct it. The boundary is a line you set rather than a standard to cite, and its wording, with the worked positive and negative pair, is in [references/mentor-briefing-and-request-mechanic.md](references/mentor-briefing-and-request-mechanic.md).
- **Logistics only** - where to be, when, which channel, who to escalate to. Necessary and never sufficient: it leaves the one question mentors actually face unanswered. MLH's guide sits close to this rung, asking for a mentor guide covering "questions to ask hackers, how to troubleshoot with the hacker, and useful beginner tools/resources" and for "a set of guidelines for mentors on what to do during mentorship, giving them a process", while leaving the help-versus-build line to the organizer.
- **None** - **delete it, from this menu and from the axis lines above, as soon as any prize carries cash value or any sponsor funds one** (Q6). This mirrors `samber/dev-event-organizer-skills@hackathon-brief-design`'s deletion of its own minimal rules rung on the same trigger and for the same reason: a prize with value turns a disagreement into a claim, and an unbriefed mentor's commit becomes an eligibility question nobody can answer.
- **Boundary plus scenario walkthrough** - the starved option: top of value, effort and compliance cost. Promotion condition, keyed to Q7 and Q4: most mentors have never mentored before, **or** sponsor staff are mentoring on a codebase their employer has a commercial interest in, **or** the event recurs and the walkthrough is written once and reused across editions.

The briefing's non-negotiable content regardless of rung, the power-dynamics guidance, and the escalation pointer into the code-of-conduct pipeline are in [references/mentor-briefing-and-request-mechanic.md](references/mentor-briefing-and-request-mechanic.md).

## Rotation by expertise

Shift length, arrival buffers, sign-up confirmation and no-show backfill are `samber/dev-event-organizer-skills@event-volunteers`' arithmetic; re-derive none of it here. Your contribution to the grid is one constraint: **the expertise the schedule needs present, hour by hour.** That means the sponsor-API specialist rostered onto the hours that track is actually being worked, not merely somebody rostered onto the floor.

**Take the slot from the mentor at sign-up.** Two published mechanics support this: "a form to get the interested people to register, asking them to pick a timeslot", and "give slots to each mentor so that they know their timings better, though encouraging them to be present throughout the hackathon". The source leaves a tension there, assigned slots alongside an ask to be around anyway. Resolve it in the grid rather than in the briefing: a slot is a commitment, presence beyond it is a courtesy, and only one of the two can be scheduled against.

**Stagger specialty coverage against when teams need each one, rather than rostering every specialty for the same uniform hours.** A track that opens with problem-definition work needs its early-stage mentors soonest. A track that only becomes buildable once a team has a direction needs its technical mentors later. Read the brief's own sequencing wherever the grid allows it, never a flat everyone-from-open-to-close roster.

Opportunity Hack's mentor guide publishes the same staggering against build progress: validation mentors early, debugging mentors mid-event, completion mentors once a team "should already be writing code," and presentation mentors in the final stretch. It staffs each stage with a named specialization (Product, GitHub, cloud deployment, Software Engineering) rather than one undifferentiated pool.

**Give each assigned mentor a checkable visit cadence for their own slice of the roster, not just a presence window.** A minimum check-in frequency per assigned team, a number this event sets for itself, turns "be available" into something a mentor can satisfy and an organizer can verify. Stop scheduled visits ahead of the final stretch, so teams get an uninterrupted run-in rather than a last-minute redirect competing with their own finishing work.

Two decisions the grid leaves to you:

- **The overnight hours.** A hackathon window can run through the night where a conference day does not, so a rotation built on daytime assumptions leaves the hours with the most blocked teams uncovered. Decide deliberately whether those hours are staffed, thinly staffed, or published as unstaffed, and publish whichever it is.
- **The uncovered skill.** When no mentor on the roster covers a needed skill, the escalation is a published route rather than an improvisation. Name in advance who is asked, and what a team is told when the answer is nobody.

## Interruption discipline

Push coverage means mentors roaming rather than waiting for a request, and it is the coverage teams consistently prefer: nobody has to notice they are stuck before getting help. Left uncoordinated, it delivers the opposite of what it promises: a team re-pitching its project to every mentor who wanders past, minutes lost each time, and a mentor pool with no record of who already visited whom.

Keep push coverage rather than replacing it with the request mechanic above, since the two solve different problems. Rate-limit the push instead:

- A per-visit time cap, with a timer the team can see, relaxed only for genuinely hands-on work that cannot be boxed.
- A "do not disturb" signal the team controls itself, visible from across the room.
- A published list of what each present mentor actually knows, so a team using the request mechanic above reaches the right person by name.
- A shared, live view of which teams are currently blocked and on what, so an idle mentor finds the team that needs them next instead of re-visiting one that does not.

The failure signature to watch for: several mentors with overlapping expertise visiting the same team inside one short window while another team goes untouched for hours. That is a coordination gap rather than a coverage-depth gap. The coverage-depth menu above cannot fix it, and only a shared view of who has been where can.

## Failure modes

- **Turning the themed-event expert ratio into a mentor-staffing formula.** The one figure that exists counts domain experts embedded in projects at themed events, per non-expert participant, and it is a project-supply target rather than a staffing one. It counts neither mentors nor teams, and it transfers to no open-theme or sponsor-track event. Fix: size coverage against the brief's tracks and the hours they are worked.
- **A sponsor track promised in the brief and unstaffed on the floor.** The brief's fallback sentence assumes the platform gets support; a sole-substrate integration with an available-if-you-find-them mentor is the promise breaking quietly. Fix: read the integration depth (Q2) before setting coverage depth.
- **Mentors nobody can identify.** The cheapest failure on this page: mentors present, participants unable to tell who they are, and a room that concludes there is no help. Fix: a marker and a named role, before anything more elaborate.
- **A mentor who takes the keyboard.** It resolves the bug and it contaminates the authorship of a submission that will be judged and possibly paid. Fix: state the boundary in the briefing, and say what a mentor does instead.
- **Rebuilding the shift grid here.** Sizing, buffers and backfill already exist next door and are better derived there. Fix: hand over the expertise constraint and let that skill schedule against it.
- **Briefing a mentor as if they were a judge.** Two documents, two audiences, one word. Fix: say "mentor briefing" every time.
- **A mentor who judges a team they carried.** Fix: keep the contact log whenever a mentor is also judging, and hand it over before the judge pool is fixed.
- **Office hours as the whole mechanic on an overnight event.** Fix: office hours supplement a latency mechanic; they never replace one.
- **Roaming mentors with no shared record of who visited whom.** Coverage exists and nobody can tell which teams still need it, so mentors cluster on whichever team pitched loudest last while another goes untouched for hours. Fix: rate-limit the visits and share a blocked-team view, not just recruit more mentors.

## Measurement

Every threshold below is self-set rather than an industry standard. Say so when presenting it, and compare it only against this event's own previous edition.

**Pass threshold (structural, one only): before the hacking window opens, all five exist in writing with zero blanks.** Iterate until the count is five.

- The expertise tags mapped onto the brief's tracks.
- The coverage commitment per track.
- The request mechanic as teams will read it.
- The mentor briefing including the boundary sentence.
- The escalation route for a skill no mentor covers.

Signals worth recording during the window (self-set):

- Requests that waited longest and which track they came from.
- Hours where a track had no tagged mentor present.
- Requests that found nobody at all.
- If any mentor judges, the contact log itself.

Pick two or three, write down the revision each would trigger, and record them live rather than reconstructing them afterwards.

## Invocation examples

- "We have 200 hackers and a sponsor API track. How many mentors, and who?"
- "How does a stuck team actually get hold of a mentor at 2am?"
- "Write the mentor briefing - what are they allowed to do to someone's repo?"
- "Our sponsor wants to send four engineers as mentors. What do we agree in writing?"
- "One of our mentors is also judging. Is that a problem?"

Expected output: a mentor plan with:

1. Coverage depth per challenge track with its rung named.
2. The recruitment channels and their lead times.
3. The expertise tags mapped onto the brief's tracks.
4. The expertise constraint handed to the shift plan.
5. The request mechanic as participants will read it.
6. The mentor briefing including the boundary and the escalation pointer.
7. The contact log decision.
8. The interruption rate-limit mechanics, where coverage is push-based.

Present it section by section for validation before the window opens.

## References

- [references/coverage-and-recruitment.md](references/coverage-and-recruitment.md) - coverage sizing against tracks rather than headcount, the themed-event ratio with its full scoping, expertise-tag vocabulary, the recruitment channels with their lead times and the sponsor-deliverable framing, and the escalation route when no mentor covers a skill.
- [references/mentor-briefing-and-request-mechanic.md](references/mentor-briefing-and-request-mechanic.md) - the mentor briefing contents with the help-versus-build boundary written out, a positive and negative worked pair, power-dynamics guidance, the sponsor-rep engagement rule, and the request mechanic published as participants read it.

See also, same collection:

- `samber/dev-event-organizer-skills@hackathon-brief-design` - names the challenge tracks and the sponsor-integration depth this skill sizes coverage against; it states that the brief only says mentors exist.
- `samber/dev-event-organizer-skills@hackathon-judging` - owns the mentor-judge recusal rule and its mechanics, and already states it from its own side; this skill supplies only the mentor-team contact log that rule reaches for.
- `samber/dev-event-organizer-skills@event-volunteers` - owns roster sizing, shift grids, arrival buffers, sign-up confirmation and the no-show replacement protocol this skill borrows unchanged rather than rebuilding.
- `samber/dev-event-organizer-skills@event-code-of-conduct` - owns conduct policy, reporting and enforcement for mentors as for every other named role; this skill briefs, it does not police.
- `samber/dev-event-organizer-skills@event-sponsor-agreement` - where a sponsor's commitment to supply mentors, and the engagement rule binding them, are negotiated before either reaches this plan.
- `samber/dev-event-organizer-skills@event-run-of-show` - schedules the hacking window whose hours the expertise rotation is aligned to.
