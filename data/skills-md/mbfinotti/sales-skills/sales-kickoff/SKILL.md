---
name: sales-kickoff
description: Before starting any sales project, and before answering a sales request that spans more than one sales topic or names no skill at all, run this router first. It routes the task to exactly one skill in the sales-skills collection, or says plainly that none fits, and bootstraps or resumes the project's shared sales-context.md artifact, producing a short-list plus an ordered skill chain. Fires on the state of the conversation rather than the subject matter, at a sales project start, at a periodic sales check-in or recurring sales review, on a mid-project re-route, or on any broad or ambiguous sales request such as "which sales skill do I need" or "where do I start with sales". Covers both altitudes, CRO-altitude planning (motion, ICP, market sizing, segmentation, tiering, org structure, quota, coverage, comp) and execution (outbound, cold calling, discovery, objections, MEDDPICC, recaps, call review, hiring, career). Run it even when sibling skills are already in daily use elsewhere.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.10"
---

# Sales Kickoff

You are the entry point and router for the 27-skill sales-skills collection. Route the current sales task to exactly one sibling skill - or say plainly that none fits - and make the next session start warm instead of cold. Routing is the reason this skill exists; everything else here serves it.

The collection spans two altitudes: nine CRO-altitude planning skills that decide the frame - motion, ICP, market size, segments, tiers, org topology, quota, coverage, comp - and eighteen that execute inside whatever those decisions produced. Establish which altitude the session is at before routing; the same words mean different skills at each one.

Run this skill at every project start, even when the collection's skills are already in daily use in another context - a new project is a new context, and daily familiarity with siblings does not replace the kickoff pass. On later sessions of the same project, re-run it to resummarize and re-route, never to re-interview.

The collection covers two selling worlds: B2B SaaS outbound and AE motions, and commission-heavy high-ticket B2C (real estate, insurance, solar, auto). Where B2B and B2C advice differs, the sibling's own scope says so - carry that split into the routing instead of flattening it.

## 1. Detect before asking

Every fact derivable from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold vs warm start from one signal only: does the context artifact `sales-context.md` exist in the project? Present → warm start. Absent → cold start. Never ask the user which one it is.
2. If you can read the repository's git history, read the recent log to infer project stage and pace: commit frequency, what changed last, whether work stalled.
3. Inventory existing files - README, agent-instruction files, ICP or persona docs, playbooks, quota/comp/territory plans, `.github/` - so nothing already written gets re-asked.
4. If your harness exposes connectors or integrations, detect which are available - a CRM export, a sequencer, call recordings, a calendar, meeting notes - and let their presence shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships version metadata you can read, note what changed since the last session. If it doesn't - the common case - degrade silently. Never block, warn, or ask about versions.

## 2. Interview - capped, tappable

On a cold start:

- Ask at most 5-7 questions.
- Ask one question per message.
- Offer multiple-choice options whenever possible.
- Spend questions only where detection came up empty; skip any question the file inventory or git log already answered.

1. "What selling motion are we operating?" - (a) B2B outbound-led (SDR/BDR prospecting), (b) B2B inbound or full-cycle AE, (c) B2C high-ticket / commission-heavy, (d) mixed.
2. "Which seat are you in?" - (a) SDR/BDR, (b) AE, (c) sales manager, enablement, or sales leadership setting the plan (VP Sales / CRO), (d) founder selling, (e) hiring for a sales seat, (f) interviewing for one. Ask this early whenever the request touches interviews, scorecards, or ramp plans - options (e) and (f) settle the hiring-vs-career route in one question, and (c) or (d) is the usual signal that the session is planning-altitude.
3. "What is the goal of this session - and is it the same as the project's goal?" Ask this on both cold and warm starts; a project goal never substitutes for today's goal.
4. "Where does the funnel hurt most right now?" - (a) not getting meetings, (b) meetings go nowhere, (c) deals stall mid-cycle, (d) losing at negotiation or close, (e) team consistency and coaching, (f) the plan above the funnel - motion, ICP, segments, org, quota or comp - rather than any one deal.
5. "Any hard constraints, and is there a date the result has to land by?" - (a) quota deadline or quarter close: give the date, (b) domain or sender reputation problem, (c) regulated outreach (do-not-call, consent, regional email law), (d) no CRM or no call-recording access, (e) none.
6. "Do you want a one-off win out of this session, or a compounding asset - and what is your effort ceiling?" - (a) one-off, hours only, (b) one-off, a week of work is fine, (c) compounding, a few hours every week from here, (d) compounding, and I can commit headcount or manager sign-off.
7. "What is already decided, and what is still open?" - ICP, offer, pricing floor, channels, tooling; one line each. Decided items are off the table for re-litigation.

Questions 5 and 6 exist to order the output, not to describe the project: the landing date, the one-off-versus-compounding answer, and the effort ceiling are what re-rank the short-list and the routines (see § 4 and § 7). Ask them here, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact so the warm start re-ranks without re-asking.

On a warm start, ask only the session-goal question. Everything else - including the deadline, the horizon and the effort ceiling that drive both rankings - comes from the artifact.

## 3. Route the task

Match the stated session goal against the declared scope of each skill below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap instead of stretching the nearest skill.

This table is deliberately unranked, and must stay that way. Scope is a match test, not a ratio: a task either falls inside a skill's declared scope or it does not. Ranking belongs one step later, in the short-list (§ 4), where several skills genuinely do compete for the same session.

| Skill                                                     | Route here when the task is…                                                                                                          |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `mbfinotti/sales-skills@sales-outreach-personalization`   | Turn prospect signals into 2-3 ranked personalization angles with proof and recency - never the message                               |
| `mbfinotti/sales-skills@cold-email-subject-line-tester`   | Generate, score, or split-test email subject lines; spam-trigger words inside the subject line only                                   |
| `mbfinotti/sales-skills@cold-email-deliverability`        | A cold email draft plus its sending setup: authentication, reputation, body mechanics, legal compliance; "going to spam"              |
| `mbfinotti/sales-skills@sales-outbound-sequence`          | Touch-by-touch cadence: channels, spacing, stop rules, re-entry, capacity math - explicitly not the copy                              |
| `mbfinotti/sales-skills@cold-call-opener`                 | The first 5-30 seconds of a live cold call: opener pattern, pain hypothesis, single ask, testable variants                            |
| `mbfinotti/sales-skills@sales-discovery-questions`        | A sequenced discovery question set for one deal or persona: pain, root cause, impact, urgency                                         |
| `mbfinotti/sales-skills@sales-objection-handling`         | Diagnose a voiced objection and write spoken rebuttals - price, timing, competitor, authority, status quo                             |
| `mbfinotti/sales-skills@meddpicc-scorecard`               | Score one described deal against the eight MEDDPICC elements on an evidence ladder; "qualify this opportunity"                        |
| `mbfinotti/sales-skills@deal-champion-mapping`            | Evidence-graded stakeholder/power map for one active deal; "who is the real decision maker", single-threading                         |
| `mbfinotti/sales-skills@deal-red-flags`                   | Sweep one deal's free-text notes for qualification red flags with severity grading; "is this deal real" from the notes                |
| `mbfinotti/sales-skills@deal-value-calc`                  | ROI and business-case narrative for one deal; "justify the price", cost of doing nothing                                              |
| `mbfinotti/sales-skills@negotiation-concession-planner`   | Pre-negotiation concession plan: tradeable levers priced, give-get pairs, BATNA-based walk-away                                       |
| `mbfinotti/sales-skills@sales-meeting-recap`              | Raw call notes → structured recap email with owned action items and a mutual action plan                                              |
| `mbfinotti/sales-skills@sales-call-review`                | Grade one call transcript against an anchored four-part rubric; rep self-review and manager tape review                               |
| `mbfinotti/sales-skills@sales-motion`                     | PLANNING: choose the selling motion - PLG, sales-led, hybrid, channel - or sequence a transition between them                         |
| `mbfinotti/sales-skills@sales-icp-definition`             | PLANNING: define or re-derive the ICP itself - firmographic, technographic, behavioral criteria, disqualifiers, a weighted fit rubric |
| `mbfinotti/sales-skills@sales-market-sizing`              | PLANNING: count the market - TAM/SAM/SOM, bottom-up build, triangulation, sanity checks                                               |
| `mbfinotti/sales-skills@sales-account-segmentation`       | PLANNING: design the segment model - fit×readiness scoring, whitespace mapping, per-segment motion map                                |
| `mbfinotti/sales-skills@sales-account-tiering`            | PLANNING: set tier cutoffs, tier names, capacity caps and per-tier coverage levels on top of an existing fit score                    |
| `mbfinotti/sales-skills@sales-org-structure`              | PLANNING: design the topology - pods, verticals, hunter/farmer split, SDR:AE ratio, manager span; seats, not people                   |
| `mbfinotti/sales-skills@sales-quota-setting`              | PLANNING: derive quotas - top-down vs bottom-up reconciliation, ramp relief, over-assignment, territory weighting                     |
| `mbfinotti/sales-skills@sales-pipeline-coverage-modeling` | PLANNING: model how much pipeline a quota needs - coverage ratios, conversion inversion, the gap and its levers                       |
| `mbfinotti/sales-skills@sales-comp-design`                | PLANNING: design the comp plan - base/variable mix, accelerators, draws, spiffs, crediting rules, governance                          |
| `mbfinotti/sales-skills@sales-hiring`                     | EMPLOYER side: scorecard, interview loop, mock-call work sample, 30-60-90 ramp for a sales hire                                       |
| `mbfinotti/sales-skills@sales-career`                     | CANDIDATE side: landing and growing a sales career, interview prep, skill-gap roadmap, offer evaluation                               |
| `mbfinotti/sales-skills@sales-radar`                      | A watch list of sales information sources; what to read or follow, "how to stay current in sales"                                     |
| `mbfinotti/sales-skills@sales-kickoff`                    | This skill: project start, periodic check-in, "which skill do I need", re-routing                                                     |

### Resolve by altitude first, then by who is asking

Most collisions here are altitude collisions rather than subject collisions: the same vocabulary names a planning decision and a task executed inside it. Route to the planning skill when the model itself is missing or wrong, to the tactical sibling when that model exists and the work happens inside it.

- `sales-motion` picks the motion; `sales-outbound-sequence` runs a cadence inside it.
- `sales-icp-definition`, `sales-account-segmentation` and `sales-account-tiering` all sound like "targeting", but answer who qualifies, how the qualified are scored and grouped, and what service level each group gets, in that order; `sales-market-sizing` counts the market the three of them filter.
- `sales-quota-setting` derives the number; `sales-pipeline-coverage-modeling` sizes pipeline against it. Neither audits a live pipeline.
- `sales-org-structure` defines the seats, `sales-comp-design` prices the behaviour inside them, and `sales-hiring` fills them.

A question about one named deal or one message is never planning-altitude, however strategic it sounds. `references/skill-routing.md` § Boundary pairs carries each of these in full; read it before routing an ambiguous task.

**sales-hiring vs sales-career** - the collection's most confusable pair, mirror images of the same role knowledge. Decide by who is asking, never by topic keywords.

- Someone filling a seat (scorecard, interview loop, work sample, ramp plan) → `mbfinotti/sales-skills@sales-hiring`.
- Someone taking a seat (interview prep, track-record evidence, offer evaluation) → `mbfinotti/sales-skills@sales-career`.

When the phrasing is ambiguous, such as "SDR interview questions" or "30-60-90 plan", ask one question before routing: "are you hiring for this role, or interviewing for it?" Both skills self-detect a wrong audience and point across, but routing right the first time saves the bounce.

Other sibling pairs also collide on keywords. Disambiguate strictly from each skill's declared scope - never from a guess about what a skill "probably" covers; a wrong disambiguation misroutes worse than none. Read `references/skill-routing.md` for the boundary-pair disambiguations, the planning skills' declared scopes and exclusions, the ordered chains, and the named coverage gaps - read it before routing any task that could plausibly match two skills.

### CRM/pipeline and channel/partner tasks - recommend the sibling repo, never force-fit

Some sales-adjacent tasks sit outside this collection's boundary by design, not by omission:

- **CRM/pipeline-tactical work** - lead routing, lead scoring, pipeline hygiene sweeps across many deals, CRM data governance, forecast diagnostics, stage or deal-desk process design, customer health/churn scoring, revenue reporting - is `mbfinotti/revops-skills` territory, not sales-skills.
- **Macro channel/partner-strategy work** - partner ecosystem design, channel program structure, co-selling rules, alliance or marketplace strategy - plus affiliate, influencer, and referral program operations - is `mbfinotti/partnerships-skills` territory.

Recommend installing the sibling repo instead of stretching the nearest sales-skills sibling onto such a task - e.g. "this is CRM/pipeline work, not sales execution; `mbfinotti/revops-skills` likely has a skill for it - consider installing that collection." Keep it a recommendation, never a dependency: sales-skills stays fully usable standalone, and the pointer flows only because both collections share the `mbfinotti` owner. See `references/skill-routing.md` § Sibling repository recommendations for the full task-to-skill mapping.

Name the gap explicitly when the task needs something no skill covers - in this collection or the two siblings above. Collection v1 has no dedicated skill for:

Execution side:

- Voicemail scripts
- Full-call talk tracks beyond the opener and discovery block
- Ongoing coaching plans
- Social selling and rep personal branding
- Sales methodology selection
- Prospect list building
- Proposal and contract drafting
- Rep mindset work

Planning side:

- Territory-carve methodology
- Rep capacity and headcount modeling
- Competitive positioning

Say "the collection has no skill for this" - never promise a skill exists or invent one.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact: motion, seat and team shape, in-flight work, top open decision, active constraint.
2. **Route** - the one skill for the immediate task (or "no skill fits", plus the named gap).
3. **Short-list** - 5 to 8 skills relevant to this project right now, drawn from one ladder only (execution or planning, per the session's altitude) and ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness and never by the routing table's row order - see "Ordering the short-list" below.
4. **Chain** - when the task genuinely decomposes into an ordered sequence (e.g. `sales-outreach-personalization` → `cold-email-subject-line-tester` → `cold-email-deliverability` → `sales-outbound-sequence`), list it in execution order with one line per link on what it hands to the next. Chain order is dependency order, not efficiency order - a later link cannot run before its earlier one, so ranking a chain adds nothing. Omit the chain when there isn't one - never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (e.g. "`sales-call-review` - once a first recorded call exists to grade").
6. **Gap** - anything today's task needs that no skill covers, stated as a gap.

### Ordering the short-list

The user's question at that moment is never "which of these exists" but "which one do I run first, and is it worth the session". Only a ratio answers that. Pick the ladder matching the session's altitude before ranking anything: the execution ladder below, or the planning ladder after it. Never blend the two into one list - a quarter-long decision and an afternoon's task compared on the same ratio hands every top slot to the afternoon.

Execution ladder - default class order, highest value/effort ratio first:

1. **Channel integrity** - `cold-email-deliverability`. Buys back whether anything sent arrives at all, so every outbound number after it means something. Costs hours of authentication and sender-reputation work, mostly once and then done - but the DNS records live with whoever owns the domain, not with the rep.
2. **Deal triage** - `deal-red-flags`, `meddpicc-scorecard`, `deal-champion-mapping`. Buys a named reason a deal is or is not real, instead of a feeling. Costs one session over notes and contact data already in hand, and changes nothing in the deal - which is exactly what stops a quarter going into a corpse.
3. **Reusable structure** - `sales-outbound-sequence`, `sales-discovery-questions`, `negotiation-concession-planner`, `deal-value-calc`. Buys the shape every later conversation runs inside: which touch on which day, what gets asked, what may be traded, what the deal is worth. A session each, then reused across every prospect or deal of the same persona.
4. **Message and live-call assets** - `sales-outreach-personalization`, `cold-email-subject-line-tester`, `cold-call-opener`, `sales-objection-handling`, `sales-meeting-recap`. Buys the largest outcome in the collection - meetings booked and deals moved - and never finishes: one prospect batch, one call, one meeting at a time. A standing job, not a fix.
5. **Review** - `sales-call-review`. Buys the read on whether any of the above landed, quoted off the tape. Costs a genuine transcript read plus the coaching conversation after it, and buys nothing until recorded calls exist and someone owns acting on the verdict.

`sales-hiring`, `sales-career` and `sales-radar` sit outside this ladder rather than at the bottom of it. They answer a people or a stay-current question, not a pipeline question; when that _is_ the session goal they are rung 1 by definition, and otherwise they do not belong on the short-list at all.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `channel integrity > deal triage > reusable structure > message & call assets > review`
- value: `message & call assets > reusable structure > deal triage > channel integrity > review`
- effort: `message & call assets > reusable structure > channel integrity > deal triage > review`
- compliance cost: `message & call assets > channel integrity > review > reusable structure > deal triage (none)` - list-scale outreach needs a lawful basis and an opt-out and a B2C call needs a do-not-call scrub, and neither a sent email nor a placed call can be recalled; the sending setup carries the region's identification and unsubscribe requirements, and a burnt domain takes weeks to rehabilitate; a graded call needs recording consent and holds a customer's own words; a conceded term needs the approval level that owns it. Deal triage reads notes already held and triggers nothing.

Channel integrity outranks deal triage on effort even though it is the smaller job: the DNS records sit outside the sales team, so it costs an approval and a wait, while triage reads what the rep already has.

Message and call assets lead on value and still lose the top slot, because that outcome arrives one prospect at a time and never stops arriving. That is also what the efficiency order starves: class 4 is the only class that books a meeting or moves a deal, so a ratio-first collection re-audits sending setups while nobody rewrites the opener that is actually failing. Promote class 4 to rung 1 outright when the bottleneck answer (Q4) is "not getting meetings" or "meetings go nowhere".

Default: open the short-list at the highest class the interview left unresolved, and never below channel integrity while a deliverability symptom is on the table. Move down a class only once the class above is in place.

Delete a ruled-out class from the short-list; never demote it to last place, because a ruled-out skill parked at the bottom silently reappears as scope.

- With a stated unblocking condition: move it to the "Not now" list, carrying that condition.
- With no unblocking condition: don't mention it at all.

The ordering is a default, not a law - it shifts with the motion and with who executes it. Re-rank against what the interview and the detection pass just revealed, and say out loud which answer moved which class:

- A motion running no cold outbound (Q1b, inbound or full-cycle AE) deletes class 1 and the cold-outreach half of class 4 - `sales-outreach-personalization`, `cold-email-subject-line-tester`, `cold-call-opener` - from the short-list outright.
- "Hiring for a sales seat" or "interviewing for one" (Q2e/f) makes `sales-hiring` or `sales-career` rung 1 and deletes every pipeline class from this session's short-list.
- "Deals stall mid-cycle" or "losing at negotiation or close" (Q4) pins class 2 to rung 1 and pulls `negotiation-concession-planner` and `deal-value-calc` up out of class 3.
- A quota deadline or quarter close inside two weeks (Q5a) promotes classes 2 and 4, which act inside that window, and demotes anything paying over a quarter to "not now" with the date as its unblocking condition.
- A domain or sender reputation problem (Q5b) pins class 1 to rung 1 whatever else the session wanted.
- Regulated outreach (Q5c) adds a consent and do-not-call review to classes 1 and 4, which lengthens both without changing what they buy.
- No CRM or call-recording access (Q5d) moves `sales-call-review` to "not now", unblocked by a first recorded call, and turns deal triage into a manual notes pass.
- "One-off, hours only" (Q6) cuts the short-list to two entries from classes 1-2; "compounding, headcount available" (Q6) promotes classes 3 and 4 above their default place.
- A decided item (Q7) removes its skill from the short-list outright - do not rank what is off the table.
- Detection moves classes too: a git log showing months of stall points at deal triage; call recordings already in the inventory make class 5 a same-day job; a written ICP and a live cadence on disk delete their class-3 entries.
- A planning-altitude session goal (Q3, "the plan above the funnel" at Q4f, or a leadership seat at Q2c/d) replaces this ladder with the planning one below - never merges the two.

### Ordering a planning-altitude short-list

Planning skills decide the frame the execution ladder runs inside, so they rank against each other on their own ratio. Default class order, highest value/effort ratio first:

1. **Frame** - `sales-icp-definition`, `sales-motion`. Buys who is sold to and how, which every number below inherits. A workshop each - and wrong here makes every downstream model precise and wrong.
2. **Market shape** - `sales-account-segmentation`, `sales-account-tiering`, `sales-market-sizing`. Buys a scored, grouped, ranked account universe with a coverage level per group. Days each, over data mostly already held.
3. **The number** - `sales-quota-setting`, `sales-pipeline-coverage-modeling`. Buys a target the field can be held to and the pipeline it implies. A planning cycle, and worth nothing until the frame is settled.
4. **People and pay** - `sales-org-structure`, `sales-comp-design`. Buys the topology and the incentives that execute all of it. Costs a reorg or a re-comp, and is the hardest thing here to unwind.

- efficiency: `frame > market shape > the number > people and pay`
- value: `people and pay > the number > frame > market shape`
- effort: `people and pay > the number > market shape > frame`
- compliance cost: `people and pay > every other planning class (none)` - a topology change moves reporting lines and, where employee representation applies, needs consultation before announcement; a comp change means re-signed agreements with HR and legal in the loop, and a mid-cycle one is a governance exception. The other three produce internal documents nobody signs.

The efficiency order starves **people and pay** - top on value, top on effort, least reversible - so a ratio-first planner keeps re-deriving the ICP while the comp plan pays for the wrong behaviour. Promote it when reps hit quota on out-of-profile accounts, or right after the motion or segment model changes; re-comp before re-org when both move.

Default: open at the highest class the interview left unsettled, never below the frame while the ICP or motion is contested. Same deletion rule as the execution ladder. Re-rank against the answers and say what moved:

- A hard date inside weeks demotes classes 3 and 4, which need a planning cycle.
- "Compounding, headcount available" (Q6d) promotes class 4.
- No closed-deal history deletes the quota and coverage entries until a first quarter of data exists.

## 5. Context artifact

Create or update `sales-context.md` at the project root - one versioned file, committed with the project when the project lives in git. It is the single source of truth that makes the next start warm. Its fields:

- Selling motion
- Seat and team shape
- ICP and offer facts
- Active funnel bottleneck
- In-flight work
- Decided vs open
- Constraints, including the date the result must land by
- The one-off-versus-compounding horizon and the effort ceiling
- Stakeholders with their decision role
- A session log

The last three fields (constraints, horizon/effort ceiling, stakeholders) are what let a warm start re-rank the short-list and the routines without re-asking questions 5 and 6. See `references/context-artifact.md` for the template, a worked example, and a negative example.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with the project's invariants (motion, ICP, pricing floor, hard constraints) so every future session inherits them without loading this skill.
- Do not scaffold a working tree the project hasn't earned. Scaffold only what this session needs - premature structure hard-codes decisions the project hasn't made yet.
- Keep a decision log only when the project actually accumulates contested decisions; otherwise the "decided vs open" field is enough. An empty ceremony log goes stale and erodes trust in the artifact.

Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If your harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses to memory after the interview completes and before § 4 Output shape: write the captured answers into the context artifact first, then derive the memory entry from the artifact. Never write memory straight from the answer, and never skip the artifact because the answer felt obvious.
- Store memory in exactly one of three places: local to the user's environment, a team knowledge base, or a `memories/` directory in a git repository. Index it with an index file listing each entry with a one-line hook.
- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - artifact wins by default; ask before overwriting either.
- Never put into memory: named individuals' personal data, prospect or customer PII from CRM records, call recordings or transcript contents, contract pricing, discount floors, quota and commission figures. State this exclusion on first writing memory.
- When memory lives in a git repository, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If your harness supports scheduled routines, propose 2 to 4, always as a dry-run shown to the user before anything is created, each with an explicit output channel. A routine without an output channel is noise the user silences within a week.

- Cost: not the setup, but the attention spent per firing, multiplied by how often it fires.
- Value: the decision it puts in front of someone while that decision is still open.

Rank the candidates on that ratio, highest first, and propose from the top down:

1. **Pre-forecast deal inspection** → `mbfinotti/sales-skills@deal-red-flags`. Costs one pass over the commit list the rep assembles for that call anyway, and it is the only routine whose output can pull a fake deal out of a number before the number is committed. Anchor it the day before the forecast call, never after.
2. **Sequence checkpoint at the committed touch count** → `mbfinotti/sales-skills@sales-outbound-sequence`. Near-zero per firing, and it forces the stop-or-continue decision inside the window where the cadence can still change. Fires once per sequence, not on a clock.
3. **Monthly or quarterly re-invocation of this kickoff.** Near-zero, and it keeps the artifact and the routing current, which is what stops every other routine firing at work that no longer exists. Match its cadence to the project's pace from the git log.
4. **Monthly sending-setup check** → `mbfinotti/sales-skills@cold-email-deliverability`. Costs a read of authentication and reputation signals each month; buys nothing while the setup is healthy and buys the whole quarter on the month it is not. Anchor it before a planned volume increase rather than to the calendar.
5. **Weekly tape review of one recorded call** → `mbfinotti/sales-skills@sales-call-review`. The most expensive per firing - a genuine transcript read plus the coaching conversation after it - and its verdict is worthless without a manager or peer who acts on it. Install it only where calls are recorded and someone owns coaching.
6. **Quarterly source refresh** → `mbfinotti/sales-skills@sales-radar`. Four near-zero firings a year buying currency rather than an outcome.

- efficiency: `deal inspection > sequence checkpoint > kickoff re-invocation > sending-setup check > tape review > source refresh`
- value: `deal inspection > tape review > sending-setup check > sequence checkpoint > kickoff re-invocation > source refresh`
- effort: `tape review > deal inspection > sending-setup check > sequence checkpoint == kickoff re-invocation == source refresh`
- compliance cost: `tape review > every other routine (none)` - a transcript holds a customer's own words under whatever recording consent the call was made on, so its output channel has to be one that consent basis and the team's data policy already cover; the others emit internal deal and setup summaries.

The three-way effort tie is genuine: each is a single near-zero read, fires rarely, and needs nobody outside the person reading it.

The source refresh is the cheapest candidate and the last one to install - the clearest proof that cheap and efficient are different orderings. The tape review is second on value and fifth on efficiency: it costs a weekly read plus a conversation, and buys a behaviour change that only shows up on later calls.

Default: rungs 1-3, which is three routines. Add rung 4 once outbound email volume is meaningful, rung 5 only where calls are recorded and coaching has an owner. Never exceed 4 - the cap is what protects the routines that matter from the ones that fire into the void.

The ranking is a default, not a law; it shifts with the motion and with who executes it. Re-rank it against the interview, and say which answer moved what:

- "Not getting meetings" (Q4) promotes the sequence checkpoint and the sending-setup check above the deal inspection.
- A quota deadline inside two weeks (Q5a) means install the deal inspection and nothing else until the quarter closes.
- A sender reputation problem (Q5b) tightens the sending-setup check to weekly until it clears.
- Regulated outreach (Q5c) blocks the tape review until its output channel clears the recording-consent basis.
- No CRM or call-recording access (Q5d) removes the tape review entirely.
- "One-off, hours only" (Q6) means install one routine, the kickoff re-invocation, not four.
- A manager already running a weekly tape review makes rung 5 a duplicate, so demote it rather than grade the same call twice.

Anchor triggers to the sales calendar - the weekly pipeline or forecast call, month end, quarter close, the team's cadence-review day - rather than arbitrary dates whenever it fits. List and clean up obsolete routines left over from a previous quarter before adding new ones.

If the harness has no scheduled routines, fall back to one recurring calendar reminder ("Sales check-in - re-run the sales kickoff") and stop there. See `references/routines.md` for the dry-run format, trigger anchoring, event-trigger preference, and cleanup checklist.

## 8. Invocation examples

- "Start a new outbound project for our SaaS."
- "Which sales skill do I need? My deals keep stalling after the demo."
- "Run my sales check-in."
- "Where do I start? I'm the founder and I've never done cold outreach."

## 9. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it doesn't cover wastes a session and hides the gap. Say "none fits" and name it.
- **Force-fitting a CRM/pipeline or channel/partner task.** Lead routing, lead scoring, pipeline hygiene, CRM data governance and forecasting are `mbfinotti/revops-skills` territory; partner/channel strategy and affiliate/influencer/referral ops are `mbfinotti/partnerships-skills`. Recommend the sibling repo instead.
- **Routing across altitudes.** "Our quota is wrong", "we're targeting the wrong accounts" and "this deal is stuck" sound alike and are three different altitudes. Settle the altitude before matching keywords, and never blend planning and execution skills into one ranked short-list.
- **Routing hiring/career by keyword.** "Interview questions" and "30-60-90" appear on both sides of the table. Route by who is asking; ask the one disambiguating question when unsure.
- **Re-interviewing on a warm start.** The artifact exists precisely so questions aren't repeated. Ask only the session goal.
- **Routing from a guessed scope.** Route only from the declared scopes in `references/skill-routing.md`; a plausible-sounding guess misroutes confidently.
- **Uncapped interview.** Past 7 questions the kickoff becomes a form the user abandons. Detection, not questions, fills the gaps.
- **Routines with no output channel.** They fire into the void and get silenced, burying the one routine that mattered.
- **A flat short-list.** Equal-looking options get picked by taste or by whichever sits first. Order by value per unit of effort and name both sides on every line.
- **Leading with the cheapest option.** Cheap and efficient are different orderings, and only the second one answers "what first". A near-zero routine or a near-zero skill that buys near-zero is a rounding error, not a quick win.
- **Demoting a ruled-out skill instead of deleting it.** A skill the interview took off the table, parked at the bottom of the short-list, reappears as scope two sessions later. Delete it, or move it to "not now" with its unblocking condition.
- **Memory committed silently.** Teammates can't review what they can't see land. Diff and approval, always.
- **Stale routing table.** Update this skill - table, `references/skill-routing.md`, boundary pairs, chains, gap list - whenever the collection changes: a skill added, renamed, removed or re-scoped. A stale router sends users to skills that no longer exist.

## 10. Pass bar

Before ending the session, check every item. If any fails, fix it and re-check - do not close the session on a failing bar.

1. Every recommended skill's declared scope matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the 27 skills in the table above.
3. Any hiring-vs-career route was decided by who is asking, not by topic keywords.
4. Interview stayed within its cap: at most 7 questions on cold start, only the session-goal question on warm start.
5. `sales-context.md` was written or updated, including a session-log line, before the session ended.
6. Every proposed routine was shown as a dry-run and has an explicit output channel.
7. A CRM/pipeline or channel/partner task got a `mbfinotti/revops-skills` or `mbfinotti/partnerships-skills` recommendation, not a forced route or a flat "no skill fits".
8. The short-list and the routine set are both ordered by value per unit of effort, each entry naming the bottleneck it attacks and what it costs - and every re-rank an interview answer forced was stated out loud.
9. Every class the interview ruled out left the short-list entirely, rather than sitting at the bottom of it.
10. The short-list was built on exactly one ladder - execution or planning - chosen from the session's altitude, with no skill from the other ladder ranked inside it.

## References

- `references/skill-routing.md` - boundary-pair disambiguations across both altitudes, planning-skill scopes and exclusions, ordered chains, coverage gaps, sibling repository recommendations. Read before routing any ambiguous task.
- `references/context-artifact.md` - the artifact template, one worked example, one negative example.
- `references/routines.md` - dry-run format, sales-calendar trigger anchoring, event triggers, cleanup checklist.
