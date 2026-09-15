---
name: advertising-kickoff
description: "Before starting any paid advertising work, before each recurring advertising review, and whenever routing is unclear, route the task to the right skill of the advertising-skills collection - or say plainly that none fits - and bootstrap or resume the project's shared context artifact. Use at every advertising project start, on later sessions of the same project to re-route without re-interviewing, and whenever the user mentions a new ad campaign or paid media project, asks which advertising skill they need, or wants a periodic advertising check-in - even if they name no skill at all. Prefer this whenever several skills could apply, since the collection has three colliding clusters - the hirer-vs-candidate pair, the budget cluster, the creative cluster - and it returns a short-list plus an ordered skill chain rather than a single guess. Do NOT use when the task already maps cleanly to one skill, such as a pure account audit - that is mbfinotti/advertising-skills@ad-account-diagnostic."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.7"
---

# Advertising Kickoff

You are the entry point and router for the 31-skill advertising-skills collection. Route the current paid-advertising task to exactly one sibling skill - or say plainly that none fits - and make the next session start warm instead of cold. Routing is the reason this skill exists; everything else here serves it.

Run this skill at every project start, even when the collection's skills are already used daily in another context - a new project is a new context, and daily familiarity with siblings does not replace the kickoff pass. On later sessions of the same project, re-run it to resummarize and re-route, never to re-interview. Everything in this skill works identically for B2B and B2C accounts; only the routing outcomes differ, and the sibling scopes say so where they do.

## 1. Detect before asking

Every fact derivable from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold vs warm start from one signal only: does `advertising-context.md` exist in the project? Present → warm. Absent → cold. Never ask the user which mode it is.
2. If you can read the repository's git history, read the recent log to infer stage and pace: commit frequency, what changed last, whether work stalled.
3. Inventory existing files - README, agent-instruction files, briefs, past campaign docs, media plans - so nothing already written gets re-asked.
4. If your harness exposes connectors or integrations, detect which are available - an ad-account export, an analytics source, a CRM, a creative asset store - and let their presence shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships readable version metadata, note what changed since the last session. If it doesn't - the common case - degrade silently. Never block, warn, or ask about versions.

## 2. Interview - capped, tappable

On a cold start:

- Ask at most 5-7 questions.
- Ask one question per message.
- Offer multiple-choice options whenever possible.
- Spend questions only where detection came up empty - skip any question the file inventory or git log already answered.

1. "What are we selling, and to whom?" - (a) B2B sales-led, (b) B2B self-serve, (c) B2C, (d) both/mixed. B2B and B2C answers steer different siblings later, so this comes first.
2. "What is the goal of this session - and is it the same as the project's goal?" Ask on both cold and warm starts; a project goal never substitutes for today's goal.
3. "Which channels are you buying today, and what's the monthly spend band?" - (a) not spending yet, (b) under $5k, (c) $5k-50k, (d) over $50k; list the channels free-form.
4. "What conversion event counts as success, and where does the source of truth live?" - platform pixel, analytics tool, CRM, or order system.
5. "Any hard constraints, and is there a date the result has to land by?" - (a) committed budgets or an agency contract, (b) a fixed date - seasonal peak, launch, board review: give the date, (c) regulated vertical / compliance review, (d) no creative production capacity, (e) none.
6. "Do you want a one-off win out of this session, or a compounding asset - and what is your effort ceiling?" - (a) one-off, hours only, (b) one-off, a week of work is fine, (c) compounding, a few hours every week from here, (d) compounding, and I can commit headcount or executive sign-off.
7. "What is already decided, and what is still open?" - one line each; decided items are off the table for re-litigation.

Questions 5 and 6 exist to order the output, not to describe the project: the landing date, the one-off-versus-compounding answer and the effort ceiling are what re-rank the short-list and the routines (see § 4 and § 7). Ask them here, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact so the warm start re-ranks without re-asking.

On a warm start, ask only the session-goal question. Everything else comes from the artifact.

## 3. Route the task

Match the stated session goal against the declared scope of each skill below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap instead of stretching the nearest skill.

This table is deliberately unranked, and must stay that way. Scope is a match test, not a ratio: ordering the rows would invent a preference between skills that never compete for the same task. Ranking belongs one step later, in the short-list (§ 4).

| Skill                                                    | Route here when the task is…                                                                                                                           |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `mbfinotti/advertising-skills@ad-account-diagnostic`     | Find the root cause of an underperforming ad account across tracking, structure, targeting, creative, bidding, offer; "why are my ads underperforming" |
| `mbfinotti/advertising-skills@ad-copy-variants`          | Turn one value proposition into distinct static/text copy variants labelled by angle and awareness stage; search headline sets                         |
| `mbfinotti/advertising-skills@ad-format-fit`             | Flag poor-fit or misused ad formats for a stated objective on a chosen platform, pre-launch format QA; format vs creative problem post-launch          |
| `mbfinotti/advertising-skills@ad-swipe-file`             | Collect competitors' currently-running ads into a categorized library and rank creative test hypotheses                                                |
| `mbfinotti/advertising-skills@advertising-career`        | Candidate side: skill-gap roadmap, interview prep, NDA-safe portfolio, agency vs in-house, pay conversations                                           |
| `mbfinotti/advertising-skills@advertising-hiring`        | Hirer side: rung decision, scorecard, interview loop, work sample, 30-60-90 with staged spend authority                                                |
| `mbfinotti/advertising-skills@advertising-radar`         | What to read/follow to stay current: a time-budgeted watch list of paid-advertising sources                                                            |
| `mbfinotti/advertising-skills@ad-attribution-gap`        | Quantify and explain discrepancies between platform reporting, analytics, and the source of truth; "the numbers don't match"                           |
| `mbfinotti/advertising-skills@ad-audience-targeting`     | Turn an ICP and buying signals into a layered targeting plan sized against platform floors, with exclusion rules                                       |
| `mbfinotti/advertising-skills@ad-bidding-strategy`       | Choose the bid policy per platform and goal, set and move the target, evaluation window, rollback trigger; "target CPA or target ROAS"                 |
| `mbfinotti/advertising-skills@ad-budget-pacing`          | Track daily/weekly spend against an already-set budget and flag under/over-pacing; "am I on pace"                                                      |
| `mbfinotti/advertising-skills@ad-buyer-group-mapper`     | Map the buying committee for an offer and give each role a messaging angle plus an ad-targeting proxy                                                  |
| `mbfinotti/advertising-skills@cac-roas-benchmark`        | Compute CAC/ROAS from real data and judge spend health against break-even, own history, external benchmarks; "is my CAC too high"                      |
| `mbfinotti/advertising-skills@ad-campaign-consolidation` | Plan which campaigns/ad sets to merge without resetting learning; "too many ad sets", "stuck in learning"                                              |
| `mbfinotti/advertising-skills@conversational-ad-copy`    | Ad copy for a single response slot inside an AI-assistant reply or answer-engine result                                                                |
| `mbfinotti/advertising-skills@ad-conversion-tracking`    | Pre-launch GO/NO-GO check that conversion events are configured, firing once, deduplicated; "is my tracking working"                                   |
| `mbfinotti/advertising-skills@ad-creative-brief`         | Turn a campaign goal plus an audience insight into a brief a designer, editor, or creator executes                                                     |
| `mbfinotti/advertising-skills@ad-creative-fatigue`       | Verdict on whether a running creative is genuinely worn out or a confounder explains the decline; "should I kill this ad"                              |
| `mbfinotti/advertising-skills@ad-creative-test-plan`     | Design a pre-launch creative test: hypothesis, cells, budgets, sample, pre-registered kill/scale rules                                                 |
| `mbfinotti/advertising-skills@ad-hook-analyzer`          | Score and force-rank the openings of candidate video ads before launch; "which hook should I test"                                                     |
| `mbfinotti/advertising-skills@paid-landing-page-audit`   | Audit a landing page receiving paid traffic and return a prioritised fix list; "clicks but no conversions"                                             |
| `mbfinotti/advertising-skills@lookalike-audience-seeds`  | Select and size the seed customer list behind a lookalike/value-based audience; match rate, platform floor                                             |
| `mbfinotti/advertising-skills@paid-media-scaling`        | Decide when a proven campaign has earned a budget increase, the step size, the ramp, rollback triggers                                                 |
| `mbfinotti/advertising-skills@ad-negative-keywords`      | Build and maintain negative keyword lists from search term reports; exclusion levels, review cadence                                                   |
| `mbfinotti/advertising-skills@ad-platform-selection`     | Choose which paid channel families fit the business's economics, audience, funnel stage, and budget at setup                                           |
| `mbfinotti/advertising-skills@ad-spend-guardrails`       | Write the org's spend policy: max allowable CAC, min ROAS floor, kill switches, ownership, override rights                                             |
| `mbfinotti/advertising-skills@retargeting-funnel`        | Design a staged retargeting sequence: recency windows, depth tiers, message ladder, exclusions, frequency caps                                         |
| `mbfinotti/advertising-skills@ad-spend-allocation`       | Split a fixed total budget across campaigns, platforms, funnel stages, and audiences by expected marginal return                                       |
| `mbfinotti/advertising-skills@thought-leadership-ads`    | Plan a campaign promoting an executive's existing organic posts as paid person-fronted ads                                                             |
| `mbfinotti/advertising-skills@ugc-ad-scripts`            | Write UGC-style short-form video ad scripts a creator can film, with hook variants and delivery notes                                                  |
| `mbfinotti/advertising-skills@advertising-kickoff`       | This skill: project start, periodic check-in, "which skill do I need", re-routing                                                                      |

Three clusters collide hard on keywords and demand disambiguation before routing:

- the hirer-vs-candidate mirror pair
- the six-skill budget cluster
- the six-skill creative cluster

Disambiguate strictly from each skill's declared scope, never from a guess about what a skill "probably" covers: a wrong disambiguation misroutes worse than none. Read `references/skill-routing.md` for the per-skill route/do-not-route signals, all boundary-pair disambiguations, the ordered chains, and the named coverage gaps, before routing any task that could plausibly match two skills.

Name the gap explicitly when the task needs something no skill covers. Collection v1 has no skill for:

- positive keyword research
- in-platform execution of any kind
- creative production itself
- incrementality testing or media mix modeling
- cross-channel budgeting beyond paid ads
- post-signup activation
- ad policy appeals and suspension recovery
- product feed management

Say "the collection has no skill for this" - never promise a skill exists or invent one.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact: business model and channels, spend band, conversion source of truth, in-flight work, active constraint.
2. **Route** - the one skill for the immediate task (or "no skill fits", plus the named gap).
3. **Short-list** - 5 to 8 skills relevant to this project right now, ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness and never by the routing table's row order - see "Ordering the short-list" below.
4. **Chain** - when the task genuinely decomposes into an ordered sequence (e.g. `mbfinotti/advertising-skills@ad-platform-selection` → `mbfinotti/advertising-skills@ad-format-fit` → `mbfinotti/advertising-skills@ad-conversion-tracking` → `mbfinotti/advertising-skills@ad-creative-test-plan`), list it in execution order with one line per link on what it hands to the next. Chain order is dependency order, not efficiency order - a later link cannot run before its earlier one, so ranking a chain adds nothing. Omit the chain when there isn't one - never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (e.g. "`mbfinotti/advertising-skills@paid-media-scaling` - after `mbfinotti/advertising-skills@cac-roas-benchmark` returns a healthy verdict").
6. **Gap** - anything today's task needs that no skill covers, stated as a gap.

### Ordering the short-list

The user's question at that moment is never "which of these exists" but "which one do I run first, and is it worth the session". Only a ratio answers that. Default class order, highest value/effort ratio first:

1. **Measurement integrity** - `mbfinotti/advertising-skills@ad-conversion-tracking`, `mbfinotti/advertising-skills@ad-attribution-gap`. Buys back the readability of every number in the account, so every later session is measured through it. Costs hours to a day, mostly one engineer's, and it is done.
2. **Diagnosis** - `mbfinotti/advertising-skills@ad-account-diagnostic`, `mbfinotti/advertising-skills@cac-roas-benchmark`. Buys a named failing layer instead of a guess. Costs one session on data already in hand and implements nothing, which is what stops a week going into the wrong layer.
3. **Policy and structure** - `mbfinotti/advertising-skills@ad-spend-guardrails`, `mbfinotti/advertising-skills@ad-platform-selection`, `mbfinotti/advertising-skills@ad-spend-allocation`, `mbfinotti/advertising-skills@ad-campaign-consolidation`. Buys a ceiling on how wrong a month can go, and volume for starved units. Costs a session plus stakeholder sign-off; cheap to write, expensive to un-merge in the account.
4. **Creative, audience and post-click** - `mbfinotti/advertising-skills@ad-creative-brief`, `mbfinotti/advertising-skills@ugc-ad-scripts`, `mbfinotti/advertising-skills@ad-copy-variants`, `mbfinotti/advertising-skills@ad-hook-analyzer`, `mbfinotti/advertising-skills@ad-swipe-file`, `mbfinotti/advertising-skills@ad-creative-test-plan`, `mbfinotti/advertising-skills@ad-audience-targeting`, `mbfinotti/advertising-skills@lookalike-audience-seeds`, `mbfinotti/advertising-skills@retargeting-funnel`, `mbfinotti/advertising-skills@ad-buyer-group-mapper`, `mbfinotti/advertising-skills@thought-leadership-ads`, `mbfinotti/advertising-skills@conversational-ad-copy`, `mbfinotti/advertising-skills@ad-format-fit`, `mbfinotti/advertising-skills@paid-landing-page-audit`. Buys the largest outcome in the collection, and never finishes: a production cycle every time, a standing job rather than a fix. `mbfinotti/advertising-skills@paid-landing-page-audit` is the one entry whose effort sits outside the account - whoever owns the page sets its pace, not you.
5. **Tuning and scaling** - `mbfinotti/advertising-skills@ad-bidding-strategy`, `mbfinotti/advertising-skills@ad-budget-pacing`, `mbfinotti/advertising-skills@ad-negative-keywords`, `mbfinotti/advertising-skills@paid-media-scaling`, `mbfinotti/advertising-skills@ad-creative-fatigue`. Near-zero effort each, and buys close to nothing until the rungs above pass - while a bid or budget edit spends a learning window on the way.

`mbfinotti/advertising-skills@advertising-career`, `mbfinotti/advertising-skills@advertising-hiring` and `mbfinotti/advertising-skills@advertising-radar` sit outside this ladder rather than at the bottom of it. They answer a people or a stay-current question, not an account question; when that _is_ the session goal they are rung 1 by definition, and otherwise they do not belong on the short-list at all.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `measurement integrity > diagnosis > policy & structure > creative & audience > tuning & scaling`
- value: `creative & audience > policy & structure > measurement integrity > diagnosis > tuning & scaling`
- effort: `creative & audience > policy & structure > measurement integrity == diagnosis > tuning & scaling`
- compliance cost: `measurement integrity > creative & audience > every other class (none)` - a consent-mode change or a server-side conversion upload triggers a data-processing and consent-basis review and cannot be un-sent; uploading a customer seed list needs a lawful basis, and a person-fronted ad needs the featured person's written permission. Diagnosis, policy and tuning read data that already exists and trigger nothing.

What this order starves is the creative and audience class: first on value and first on effort at once, so a ratio ranks it below measurement and diagnosis every session however large the outcome it buys, and its production cycle never finishes paying. Promote it past the ratio, rather than waiting for it to win a round it structurally cannot, when the interview answered compounding with headcount or sign-off (Q6), when diagnosis has already named creative as the failing layer, or when the account's creative has not been refreshed in a full flight. Say which condition promoted it.

Tuning is last on effort and last on efficiency at once: near-zero effort buying near-zero outcome is a rounding error with a learning reset attached, not a cheap win.

Default: open the short-list at the highest class the interview left unresolved, and never below measurement integrity while the conversion source of truth is unconfirmed. Move down a class only once the class above is in place.

This ordering is a default, not a law - it shifts with the account and with who executes it. Re-rank it against what the interview and the detection pass just told you, and say out loud which answer moved which class:

- "Not spending yet" (Q3) empties classes 1, 2 and 5 - there is nothing to measure, diagnose or tune - and promotes `mbfinotti/advertising-skills@ad-platform-selection` and `mbfinotti/advertising-skills@ad-conversion-tracking` to the top.
- A platform pixel named as the only source of truth (Q4) pins measurement integrity to rung 1 whatever else the session wanted.
- A fixed landing date inside six weeks (Q5) promotes fast-acting classes and demotes anything that pays over a quarter - guardrail re-baselining, consolidation, hiring - to "not now" with the date as its unblocking condition.
- No creative production capacity (Q5) moves class 4 off the short-list into "Not now" with capacity as its unblocking condition, rather than ranking it under class 5 - except `mbfinotti/advertising-skills@ad-swipe-file` and `mbfinotti/advertising-skills@ad-copy-variants`, which need none.
- A regulated vertical (Q5) adds a legal review to class 1 and to seed-list work, which lengthens both without changing what they buy.
- "One-off, hours only" (Q6) cuts the short-list to two entries from classes 1-2; "compounding, headcount available" (Q6) promotes class 3 and class 4 above their default place.
- A decided item (Q7) removes its skill from the short-list outright, and so does anything the constraints rule out permanently: a channel the vertical cannot advertise on, an account an agency contract forbids restructuring, a class no budget will ever fund. Delete those entries and name each one as deleted with the constraint that killed it - never rank them last. An option parked at the bottom of a short-list is read as a later rung and comes back as scope next session; a named deletion does not.
- Detection findings move classes too: an in-house engineer makes class 1 a same-day job; an agency holding the account makes class 3 a negotiation rather than a decision; a git log showing months of stall means diagnosis before anything else.

## 5. Context artifact

Create or update `advertising-context.md` at the project root, one versioned file committed with the project when the project lives in git. It is the single source of truth that makes the next start warm. Its fields:

- business model
- offer and price point
- channels and spend band
- conversion event and source of truth
- CAC/ROAS position and guardrail status
- in-flight work
- decided vs open
- constraints
- stakeholders with decision role
- a session log

See `references/context-artifact.md` for the template, a worked example, and a negative example.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with the project's invariants (business model, source of truth, guardrail policy, hard constraints) so every future session inherits them without loading this skill.
- Do not scaffold a working tree the project hasn't earned. Scaffold only what this session needs - premature structure hard-codes decisions the project hasn't made yet.
- Keep a decision log only when the project actually accumulates contested decisions; otherwise the "decided vs open" field is enough. An empty ceremony log goes stale and erodes trust in the artifact.

Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If your harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses to memory after the interview completes and before § 4 Output shape: write the captured answers into the context artifact first, then derive the memory entry from the artifact. Never write memory straight from the answer, and never skip the artifact because the answer felt obvious.
- Store memory in exactly one of three places: local to the user's environment, a team knowledge base, or a `memories/` directory in a git repository. Index it with an index file listing each entry with a one-line hook.
- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - artifact wins by default; ask before overwriting either.
- Never put into memory: customer PII or the contents of uploaded customer lists, ad account IDs and credentials, negotiated media rates and agency fees, unreleased campaign or pricing plans. State this exclusion when you first write memory.
- When memory lives in a git repository, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If your harness supports scheduled routines, propose 2 to 4, always as a dry-run shown to the user before anything is created, each with an explicit output channel. A routine without an output channel is noise the user silences within a week.

A routine's cost is not its setup but its attention per firing multiplied by how often it fires; its value is the decision it puts in front of someone while that decision is still open. Rank the candidates on that ratio, highest first, and propose from the top down:

1. **Monthly spend health check** → `mbfinotti/advertising-skills@cac-roas-benchmark`. Fires twelve times a year, costs about an hour of assembling inputs you assemble anyway, and is the only routine whose output can stop a losing month. Anchor it before the allocation decision it feeds, never after.
2. **Weekly pacing check** → `mbfinotti/advertising-skills@ad-budget-pacing`. Near-zero per firing, and it catches an over- or under-spend inside the period where it can still be corrected. Its firing rate is its whole cost - drop it to monthly once spend is stable.
3. **Monthly or quarterly re-invocation of this kickoff.** Near-zero, and it keeps the artifact and the routing current, which is what stops every other routine from firing at work that no longer exists. Match its cadence to the project's pace from the git log.
4. **Monthly search term mining** → `mbfinotti/advertising-skills@ad-negative-keywords`. Costs a search-term export plus a review pass each month, and compounds: every negative added keeps paying. Worth nothing on an account with no search spend - skip it there rather than shrinking it.
5. **Weekly or biweekly creative wear-out check** → `mbfinotti/advertising-skills@ad-creative-fatigue`. The most expensive per firing - a genuine read of per-creative delivery - and its verdict is worthless without production capacity to act on it. Install it only where creative can actually be replaced.
6. **Quarterly source refresh** → `mbfinotti/advertising-skills@advertising-radar`. Four near-zero firings a year buying currency rather than an outcome.

- efficiency: `spend health > pacing > kickoff re-invocation > search term mining > wear-out check > source refresh`
- value: `spend health > wear-out check > search term mining > pacing > kickoff re-invocation > source refresh`
- effort: `wear-out check > search term mining > spend health > pacing == kickoff re-invocation == source refresh`
- compliance cost: `search term mining > every other routine (none)` - search term reports carry user-typed text that can identify a person, so its output channel has to be one the account's data-handling policy already covers; the others emit aggregates.

The source refresh is the cheapest candidate and the last one to install - the clearest proof that cheap and efficient are different orderings. The wear-out check is second on value and fifth on efficiency, because what it costs is a weekly read and what it buys is a verdict that only converts into an outcome downstream.

Default: rungs 1-3, which is three routines. Add rung 4 when search is a meaningful share of spend, rung 5 only when creative production capacity exists. Never exceed 4 - the cap is what protects the routines that matter from the ones that fire into the void.

The ranking is a default, not a law: it shifts with the account and with who executes it. Re-rank it against the interview:

- "not spending yet" (Q3) leaves only the kickoff re-invocation standing
- a fixed date inside six weeks (Q5) promotes pacing above spend health for the flight's duration and tightens it to daily in the final week
- a regulated vertical (Q5) blocks search term mining until its channel clears compliance review
- no creative capacity (Q5) removes the wear-out check entirely
- "one-off, hours only" (Q6) means install one routine, not four
- an agency already delivering a weekly pacing report makes rung 2 a duplicate: demote it rather than send the user the same number twice

Anchor triggers to the media calendar - month-end budget reset, campaign flight dates, seasonal peaks - rather than arbitrary dates whenever it fits. List and clean up obsolete routines left over from a previous flight or quarter before adding new ones.

If the harness has no scheduled routines, fall back to one recurring calendar reminder ("Advertising check-in - re-run the advertising kickoff") and stop there. See `references/routines.md` for the dry-run format, media-calendar trigger anchoring, event-trigger preference, and cleanup checklist.

## 8. Invocation examples

- "Start a new paid advertising project for our product launch."
- "Which advertising skill do I need? Our ROAS dropped last week."
- "Run my advertising check-in."
- "Where do I start? We've never bought ads before."

## 9. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it doesn't cover wastes a session and hides the gap. Say "none fits" and name the gap.
- **Re-interviewing on a warm start.** The artifact exists precisely so questions aren't repeated. Ask only the session goal.
- **Routing from a guessed scope.** Route only from the declared scopes in `references/skill-routing.md`; a plausible-sounding guess misroutes confidently.
- **Uncapped interview.** Past 7 questions the kickoff becomes a form the user abandons. Detection, not questions, fills the gaps.
- **Routines with no output channel.** They fire into the void and get silenced, burying the one routine that mattered.
- **A flat short-list.** Five equal-looking options get picked by taste or by whichever sits first. Order by value per unit of effort and name both sides on every line, or the user cannot choose.
- **Leading with the cheapest option.** A near-zero skill or routine that buys near-zero is a rounding error, not a quick win.
- **Memory committed silently.** Teammates can't review what they can't see land. Diff and approval, always.
- **Stale routing table.** Update this skill - table, `references/skill-routing.md`, boundary pairs, chains, gap list - whenever the collection changes: a skill added, renamed, removed, or re-scoped. A stale router sends users to skills that no longer exist, which is worse than no router at all.

## 10. Pass bar

Before ending the session, check every item. If any fails, fix it and re-check - do not close the session on a failing bar.

1. Every recommended skill's declared scope actually matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the 31 skills in the table above.
3. Interview stayed within its cap: at most 7 questions on cold start, only the session-goal question on warm start.
4. `advertising-context.md` was written or updated, including a session-log line, before the session ended.
5. Every proposed routine was shown as a dry-run and has an explicit output channel.
6. The short-list and the routine set are both ordered by value per unit of effort, each entry naming the bottleneck it attacks and what it costs:
   - the re-rank was stated out loud whenever an interview answer moved something off its default place
   - anything the constraints ruled out appears as deleted by name, not ranked last
   - the starved high-value/high-effort entry is named with the condition that would promote it

## References

- `references/skill-routing.md` - per-skill route/do-not-route signals, boundary-pair disambiguations, ordered chains, coverage gaps. Read before routing any ambiguous task.
- `references/context-artifact.md` - the artifact template, one worked example, one negative example.
- `references/routines.md` - dry-run format, media-calendar trigger anchoring, event triggers, cleanup checklist.
