---
name: revops-kickoff
description: Before starting any RevOps or Sales Ops task, and at the start of every session on an ongoing RevOps project, run this first - it routes the task to exactly one skill of the revops-skills collection or says plainly that none fits, and bootstraps or resumes the project's shared, versioned context artifact so the next session starts warm instead of cold, ending in a short-list plus an ordered skill chain. Run it even when the collection's other skills are already used daily - a new project is a new context. Also use whenever the user mentions a revops kickoff, a new RevOps project, a revops project start, revops or crm skill routing, a periodic RevOps check-in, a recurring RevOps review, "which revops skill do I need", or "where do I start with RevOps" - even if they never name a skill, and even if the request looks like it already belongs to one specific skill. Do NOT use for routing quota-carrying sales tasks - use mbfinotti/sales-skills@sales-kickoff instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.4"
---

# RevOps Kickoff

You are the entry point and router for the 20-skill revops-skills collection, which spans two altitudes: macro design skills that decide what the revenue system _is_, and tactical skills that operate inside it. Route the current RevOps task to exactly one sibling skill, or say plainly that none fits, and make the next session start warm instead of cold. Routing is the reason this skill exists; everything else here serves it.

Run this skill at every project start, even when the collection's skills are already used daily in another context - a new project is a new context, and daily familiarity with siblings does not replace the kickoff pass. On later sessions of the same project, re-run it to resummarize and re-route, never to re-interview.

## 1. Detect before asking

Every fact derivable from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold vs warm start from one signal only: does the context artifact `revops-context.md` exist in the project? Present → warm start. Absent → cold start. Never ask the user which one it is.
2. Read the repository's recent git log when the history is readable, and infer project stage and pace from it: commit frequency, what changed last, whether work stalled.
3. Inventory existing files - README, agent-instruction files, data dictionaries, stage documentation, `.github/` - so nothing already written gets re-asked.
4. If the harness exposes connectors or integrations, detect which are available - a CRM export, an analytics source, a ticketing system, meeting notes - and let their presence shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships readable version metadata, note what changed since the last session. If it doesn't - the common case - degrade silently. Never block, warn, or ask about versions.

## 2. Interview - capped, tappable

On a cold start:

- Ask at most 5-7 questions.
- Ask one question per message.
- Offer multiple-choice options whenever possible.
- Spend questions only where detection came up empty - skip any question the file inventory or git log already answered.

1. "What revenue motion are we operating?" - (a) B2B sales-led, (b) B2B PLG / self-serve, (c) B2C / transactional, (d) mixed.
2. "What is the goal of this session - and is it the same as the project's goal?" Ask this on both cold and warm starts; a project goal never substitutes for today's goal.
3. "Who owns the CRM day-to-day, and who signs off on changes to it?" - capture both names/roles; they rarely coincide.
4. "Any hard constraints, and is there a date the result has to land by?" - (a) release/change freeze, (b) quarter close or month-end close: give the date, (c) limited admin capacity, (d) compliance or audit window, (e) none.
5. "Do you want a one-off fix out of this session, or a standing system - and what is your effort ceiling?" - (a) one-off, hours only, (b) one-off, a week of work is fine, (c) standing, a few hours every week from here, (d) standing, and I can get admin access and cross-team sign-off.
6. "What is already decided, and what is still open?" - one line each; decided items are off the table for re-litigation.

Questions 4 and 5 exist to order the output, not to describe the project: the landing date, the one-off-versus-standing answer and the effort ceiling are what re-rank the short-list (§ 4) and the routines (§ 7). Ask them here, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact so the warm start re-ranks without re-asking them.

On a warm start, ask only the session-goal question. Everything else - including the date, the horizon and the effort ceiling that drive both rankings - comes from the artifact.

## 3. Route the task

Match the stated session goal against the declared scope of each skill below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap instead of stretching the nearest skill.

This table is deliberately unranked, and must stay that way. Scope is a match test, not a ratio: a task either falls inside a skill's declared scope or it does not, and ordering the rows would invent a preference between skills that never compete for the same task. Ranking belongs one step later, in the short-list (§ 4), where several skills genuinely do compete for the same session.

| Skill                                                      | Route here when the task is…                                                                                                                                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mbfinotti/revops-skills@revenue-funnel`                   | Design the funnel model itself: which stages exist, what unit moves through them, the plan's conversion assumptions, who owns each handoff - no agreed stage set yet, or the model is wrong rather than the wording |
| `mbfinotti/revops-skills@lead-scoring`                     | Design, validate, or fix a lead scoring model; MQL/PQL thresholds; "sales rejects our MQLs"                                                                                                                         |
| `mbfinotti/revops-skills@lead-routing`                     | Assign inbound leads to reps: rule precedence, round-robin, territory assignment rules, routing SLAs - the score already exists                                                                                     |
| `mbfinotti/revops-skills@pipeline-stage-definition-audit`  | Audit stage definitions against buyer-verifiable exit criteria; stages named after rep activity                                                                                                                     |
| `mbfinotti/revops-skills@sales-pipeline-hygiene`           | Periodic audit of an active pipeline snapshot: stale deals, close-date pushes, missing fields                                                                                                                       |
| `mbfinotti/revops-skills@sales-forecast-diagnostic`        | Diagnose why an existing forecast misses: stage inflation, sandbagging, roll-up overrides                                                                                                                           |
| `mbfinotti/revops-skills@revenue-leakage`                  | Trace where records silently exit one specific funnel and size the recoverable loss                                                                                                                                 |
| `mbfinotti/revops-skills@revenue-data-governance-strategy` | Org-wide data authority: which system is source of truth per object class, cross-team data contracts, where metric definitions live, who arbitrates "we have two ARR numbers"                                       |
| `mbfinotti/revops-skills@crm-data-governance`              | Field ownership, system of record per field, freshness SLAs, field lifecycle and enforcement rules                                                                                                                  |
| `mbfinotti/revops-skills@deal-desk-approval`               | Discount/concession approval matrix and exception handling for non-standard deals                                                                                                                                   |
| `mbfinotti/revops-skills@customer-churn-signals`           | Discover, validate, and rank leading churn indicators into a signal register                                                                                                                                        |
| `mbfinotti/revops-skills@customer-health-score`            | Combine existing signals into one composite, weighted, banded account health score                                                                                                                                  |
| `mbfinotti/revops-skills@sales-to-cs-handoff`              | Design the sales-to-CS post-close handoff process, packet, and acceptance step                                                                                                                                      |
| `mbfinotti/revops-skills@revenue-kpi-framework`            | Design the org-wide metric tree: which metrics each level owns, how they reconcile upward, which guardrail counter-metric rides alongside each owned number                                                         |
| `mbfinotti/revops-skills@revenue-reporting`                | Metric spine and narrative for a board/exec revenue report, QBR section, or investor update                                                                                                                         |
| `mbfinotti/revops-skills@revops-stack-rationalization`     | Periodic portfolio review of the whole GTM tool stack: keep, consolidate, replace, or cut, tool by tool, timed to renewals                                                                                          |
| `mbfinotti/revops-skills@revops-hiring`                    | Hiring-manager side: scorecard, interview loop, work sample, 30-60-90 for a RevOps hire                                                                                                                             |
| `mbfinotti/revops-skills@revops-career`                    | Candidate side: RevOps career ladder, interview prep, evidence of invisible ops work                                                                                                                                |
| `mbfinotti/revops-skills@revops-radar`                     | Staying current: a watch list of RevOps sources, newsletters, communities, people to follow                                                                                                                         |
| `mbfinotti/revops-skills@revops-kickoff`                   | This skill: project start, periodic check-in, "which skill do I need", re-routing                                                                                                                                   |

Several sibling pairs genuinely collide on keywords. Four of them collide on altitude rather than on subject:

- `revenue-funnel` designs the stage model `pipeline-stage-definition-audit` audits.
- `revenue-data-governance-strategy` designates which system wins per object class while `crm-data-governance` governs the fields inside the winner.
- `revenue-kpi-framework` designs the metric tree `revenue-reporting` narrates.
- `revops-stack-rationalization` rules on which tools exist at all.

Route to the macro skill when the model, the authority map, or the metric set is what is missing or wrong; route to the tactical sibling when that model exists and the work happens inside it. Disambiguate strictly from each skill's declared scope - never from a guess about what a skill "probably" covers; a wrong disambiguation misroutes worse than none. Read `references/skill-routing.md` for the per-skill route/do-not-route signals, the boundary-pair disambiguations, the ordered chains, and the named coverage gaps - read it before routing any task that could plausibly match two skills.

Name the gap explicitly when the task needs something no skill covers. Collection v1 has no dedicated skill for:

- Record deduplication.
- Attribution modeling.
- Territory design.
- Single-tool pre-purchase evaluation.
- BI dashboard building.

Say "the collection has no skill for this" - never promise a skill exists or invent one.

Before naming a gap, check whether the task actually belongs to a sibling `mbfinotti` collection instead of this one:

- **Sales-execution-tactical** (cold calling, discovery calls, objection handling, negotiation concessions, deal-specific call coaching) or **sales-leadership planning** (quota setting, compensation plan design, sales org structure, ICP definition, market sizing, coverage modeling) → recommend installing `mbfinotti/sales-skills`.
- **Macro channel/partner strategy** (partner programs, co-selling, alliances, affiliate/influencer/referral operations) → recommend installing `mbfinotti/partnerships-skills`.

Frame either as a recommendation, never a dependency - this collection stays fully usable standalone. See `references/skill-routing.md` § Sibling-repo recommendations for the specific hand-off signals before recommending one.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact: motion, system of record, in-flight work, top open decision, active constraint.
2. **Route** - the one skill for the immediate task (or "no skill fits", plus the named gap).
3. **Short-list** - 5 to 8 skills relevant to this project right now, ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness and never by the routing table's row order - see "Ordering the short-list" below.
4. **Chain** - when the task genuinely decomposes into an ordered sequence (e.g. `pipeline-stage-definition-audit` → `sales-pipeline-hygiene` → `sales-forecast-diagnostic`), list it in execution order with one line per link on what it hands to the next. Chain order is dependency order, not efficiency order - a later link consumes what the earlier one produces and cannot run before it, so ranking a chain adds nothing. Omit the chain when there isn't one - never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (e.g. "`customer-health-score` - after `customer-churn-signals` delivers a validated register").
6. **Gap** - anything today's task needs that no skill covers, stated as a gap. When the gap is actually sales-execution-tactical or macro channel/partner-strategy work, recommend the matching sibling repo (`mbfinotti/sales-skills` or `mbfinotti/partnerships-skills`) instead of a bare gap statement - see § 3.

### Ordering the short-list

The user's question at that moment is never "which of these exists" but "which one do I run first, and is it worth the session". Only a ratio answers that. Default class order, highest value per unit of effort first:

1. **Diagnosis** - `revenue-leakage`, `sales-forecast-diagnostic`, `pipeline-stage-definition-audit`. Buys a named, evidenced answer to which of the classes below is actually the problem, instead of a hunch. Costs one session over records already exported; needs no admin access, no sign-off, and changes nothing that has to be rolled back.
2. **Funnel plumbing** - `lead-scoring`, `lead-routing`. Buys speed-to-lead and stops qualified leads sitting unworked in a queue. Costs a design session plus a CRM configuration change by whoever holds admin, and a staged rollout with a rollback path - and it only ever applies to leads arriving after it ships.
3. **Standing rules** - `crm-data-governance`, `deal-desk-approval`, `sales-to-cs-handoff`. Buys the rule every later sweep and every later exception is decided against: who owns a field, who may approve a concession, what the CS team must receive. Costs a drafting session plus cross-team sign-off outside RevOps, and a rule is reversible only by another negotiation.
4. **Stack rationalization** - `revops-stack-rationalization`. Buys back duplicate spend and one decided verdict per tool, out of a contract list finance already keeps. Costs an inventory pass across finance, procurement, SSO and expense records plus a tool owner per verdict - and the renewal calendar is the whole ratio: a verdict landing after the auto-renewal date buys nothing for another contract year.
5. **Recurring sweeps** - `sales-pipeline-hygiene`. Buys a pipeline whose numbers hold this quarter rather than only at close. Costs a session per sweep plus a rep chasing each disposition, and it never finishes - a standing job, not a fix.
6. **Account health** - `customer-churn-signals`, `customer-health-score`. Buys ranked, validated reasons an account is at risk while there is still time to act. Costs the longest lead time among the tactical classes: enough renewal history to backtest against, a validation window before anyone may trust the output, then recalibration.
7. **Reporting** - `revenue-reporting`. Buys a number an exec or a board acts on, and the sign-off that it is real. Costs the definition-locking negotiation across finance and sales, and buys little while the metrics feeding it are the ones the classes above have not fixed yet.
8. **Macro design** - `revenue-funnel`, `revenue-data-governance-strategy`, `revenue-kpi-framework`. Buys the model every class above operates inside: the stage set the plan is built on, the system that wins per object class, the metric tree each org level owns. Costs the most in the collection - cross-functional negotiation with finance, marketing and CS, a decision the whole company then reads from, and a payoff arriving a planning cycle after the work. Nothing here is reversible by RevOps alone.

`revops-hiring`, `revops-career`, and `revops-radar` sit outside this ladder rather than at the bottom of it. They answer a people or a stay-current question, not a revenue-system question; when that _is_ the session goal they are rung 1 by definition, and otherwise they do not belong on the short-list at all.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `diagnosis > funnel plumbing > standing rules > stack rationalization > recurring sweeps > account health > reporting > macro design`
- value: `macro design > funnel plumbing > account health > standing rules > stack rationalization > recurring sweeps > reporting > diagnosis`
- effort: `macro design > account health > stack rationalization > standing rules > funnel plumbing > recurring sweeps == reporting > diagnosis`
- compliance cost: `macro design > stack rationalization > reporting > standing rules > account health > funnel plumbing > diagnosis == recurring sweeps (none)`, in that order:
  - A source-of-truth designation and a signed metric taxonomy set org-wide retention, residency and read-access terms that finance and legal both own.
  - Cutting a tool triggers a contract termination notice and a data-deletion or export obligation that lapses on the vendor's clock.
  - A board or investor number carries a finance sign-off and cannot be unsaid once issued.
  - Field-ownership and discount-authority rules encode who may read customer data and who may approve a concession, so both need the data-protection and delegation-of-authority review that owns them.
  - A churn model profiles named accounts on behavioral history whose retention basis someone must own.
  - Routing rules move customer records between owners and regions, which crosses data-residency lines in a multi-region CRM.

Recurring sweeps and reporting tie on effort genuinely: each is a recurring session over records and definitions already held, with nothing to configure, no admin access and nothing to roll back - one runs each sweep, the other each reporting cycle. Diagnosis and recurring sweeps tie at zero compliance cost for the same reason: both read records already held under an existing lawful basis and publish nothing outside the team.

Macro design leads on value and sits last on efficiency - the widest gap between two axes in the collection, because its payoff arrives a planning cycle after the work. Account health shows the same shape one notch down: it leads the tactical classes on value in any renewal-heavy business and still sits sixth on efficiency, because its output cannot be acted on until a validation window has passed.

That gap is exactly what the efficiency order starves: the foundational work. Macro design loses every round on a ratio - highest value, highest effort, slowest payoff - and `crm-data-governance` one rung up shows the same shape at smaller scale, with the highest coordination cost of the tactical classes and no visible output the week it lands. Left unpromoted, a ratio-first order re-runs cheap diagnostics forever while every sweep below re-litigates the same exceptions against a model nobody ever agreed.

Promote macro design to rung 1 outright, and standing rules with it, when the program is being designed rather than tuned:

- Finance and sales quote two different ARR numbers, or nobody can say which system wins per object class → `revenue-data-governance-strategy`.
- No agreed stage set, several motions share one stage list, or a stage audit leaves fewer than two usable anchors → `revenue-funnel`.
- Each org level tracks its own unreconciled numbers, or a planning cycle or board reset is opening → `revenue-kpi-framework`.
- Nobody can name who owns a field or which system wins (Q3 came back empty), the same exception reappears sweep after sweep, or a compliance or audit window (Q4d) is open → standing rules.

Default: open the short-list at class 1 and stay there until the diagnosis names a class below it. Move down exactly one class at a time, and never past a class whose absence the diagnosis flagged.

Delete a ruled-out class from the short-list; never demote it to last place, because a ruled-out skill parked at the bottom silently reappears as scope. When it has a stated unblocking condition it moves to the "Not now" list carrying that condition; when it has none, it is not mentioned at all.

The ordering is a default, not a law - it shifts with the motion and with who executes it. Re-rank against what the interview and the detection pass just established, and say out loud which answer moved which class:

- B2B PLG / self-serve (Q1b) pulls `lead-scoring` up inside funnel plumbing as product-qualified scoring, rewrites `deal-desk-approval` as promo and discount policy rather than a rep-facing approval matrix, and makes `revenue-funnel`'s unit-of-analysis decision - lead, buying group, or workspace - the first thing macro design has to settle.
- B2C / transactional (Q1c) deletes `sales-to-cs-handoff` and `deal-desk-approval` from the short-list unless a named account-management motion exists to hand off to.
- Nobody can name the day-to-day CRM owner or the sign-off (Q3) promotes standing rules to rung 1, whatever the session wanted - and `revenue-data-governance-strategy` with it when the ambiguity spans systems rather than fields. Every class below writes into a system with no agreed owner.
- A change freeze or limited admin capacity (Q4a/c) deletes funnel plumbing from this session's short-list; it moves to "not now", unblocked by admin capacity, and diagnosis absorbs the session. Macro design is untouched by either - it changes no configuration.
- A close date inside two weeks (Q4b) promotes `sales-forecast-diagnostic` and recurring sweeps, which both act inside that window, and demotes anything paying out over a quarter - account health, a governance rewrite, all of macro design - to "not now" with the close date as its unblocking condition.
- A renewal cluster or budget cycle inside the quarter promotes stack rationalization to rung 1; with every renewal more than two quarters out it drops below recurring sweeps, since no verdict can be acted on before then.
- A compliance or audit window (Q4d) promotes standing rules, reporting and `revenue-data-governance-strategy`, and lengthens account health without changing what it buys.
- "One-off, hours only" (Q5a) cuts the short-list to two entries from diagnosis and deletes macro design outright; "standing, admin and sign-off available" (Q5d) promotes standing rules, account health and macro design above their default place.
- A decided item (Q6) removes its skill from the short-list outright - do not rank what is off the table.
- Detection moves classes too: a git log showing months of stall points at diagnosis before any build; a data dictionary or written stage definitions already on disk delete their diagnosis and standing-rules entries and lower `revenue-funnel`'s urgency; no readable CRM export deletes diagnosis's data-dependent entries and leaves `pipeline-stage-definition-audit`, which reads definitions rather than records; a contract inventory or expense export already on disk removes most of stack rationalization's cost.

## 5. Context artifact

Create or update `revops-context.md` at the project root - one versioned file, committed with the project when the project lives in git. It is the single source of truth that makes the next start warm.

Its fields:

- Revenue motion.
- CRM and system-of-record facts.
- Stage set.
- In-flight work.
- Decided vs open.
- Constraints, including the date the result must land by.
- The one-off-versus-standing horizon and the effort ceiling.
- Stakeholders with their decision role.
- A session log.

The last three fields are what let a warm start re-rank the short-list and the routines without re-asking questions 4 and 5. See `references/context-artifact.md` for the template, a worked example, and a negative example.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with the project's invariants (motion, system of record, hard constraints) so every future session inherits them without loading this skill.
- Do not scaffold a working tree the project hasn't earned. Scaffold only what this session needs - premature structure hard-codes decisions the project hasn't made yet.
- Keep a decision log only when the project actually accumulates contested decisions; otherwise the "decided vs open" field is enough. An empty ceremony log goes stale and erodes trust in the artifact.

Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If the harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses to memory after the interview completes and before § 4 Output shape: write the captured answers into the context artifact first, then derive the memory entry from the artifact. Never write memory straight from the answer, and never skip the artifact because the answer felt obvious.

Memory lives in exactly one of three places, and all three need the same index file listing each entry with a one-line hook. They are not equivalent otherwise - pick from this order, highest value per unit of setup effort first:

1. **A `memories/` directory in the project's git repository.** Setup is a directory and an index file, teammates read it wherever they already read the project, and every change arrives as a reviewable diff. Costs the commit-approval step below, and what lands there is durable in history - removing a mistake means rewriting it.
2. **A team knowledge base.** Reaches the people who never open the repository and survives any single machine. Costs an access-and-permissions setup outside RevOps, and it drifts away from the artifact because nothing ties a page to a commit.
3. **Local to the user's environment.** Near-zero setup, and nobody else can read it. Use it only for a solo project, or for notes that must not leave the machine - a per-user store forks the project state the moment a second person joins.

- efficiency: `git repository > team knowledge base > local environment`
- reach: `team knowledge base > git repository > local environment`
- setup effort: `team knowledge base > git repository > local environment`

Default to the git repository whenever the project already lives in one; choose the knowledge base when the people who need the memory do not work in the repository.

- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - artifact wins by default; ask before overwriting either.
- Never put into memory: named individuals' personal data, customer names or PII from CRM records, contract pricing and discount floors, compensation figures. State this exclusion at the first memory write.
- When memory lives in a git repository, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If the harness supports scheduled routines, propose 2 to 4 - always as a dry-run shown to the user before anything is created, each with an explicit output channel. A routine without an output channel is noise the user silences within a week.

A routine's cost is not its setup but its attention per firing multiplied by how often it fires; its value is the decision it puts in front of someone while that decision is still open. Rank the candidates on that ratio, highest first, and propose from the top down:

1. **Pre-close forecast diagnostic** → `mbfinotti/revops-skills@sales-forecast-diagnostic`. Fires a handful of times a year, over the commit list the team assembles for that call anyway, and it is the only routine whose output can correct a number before it is committed upward. Anchor it the week before close, never after.
2. **Monthly or quarterly re-invocation of this kickoff.** Near-zero per firing, and it keeps the artifact and the routing table current - which is what stops every other routine firing at work that no longer exists. Match its cadence to the project's pace from the git log.
3. **Renewal-window stack review** → `mbfinotti/revops-skills@revops-stack-rationalization`. Fires a few times a year against the next renewal cluster, over a contract list finance keeps anyway, and it is the only routine whose output has to land before a date the vendor sets rather than one the team picks. Anchor it a full notice period ahead of each cluster, never at the renewal itself.
4. **Weekly pipeline hygiene pass** → `mbfinotti/revops-skills@sales-pipeline-hygiene`. Buys numbers that hold every week instead of only at close, and carries the highest standing cost in the set: the sweep is a session and each disposition needs a rep to act on it. Install it only where someone owns chasing the exception list.
5. **Monthly CRM field-governance review** → `mbfinotti/revops-skills@crm-data-governance`. Costs a monthly pass over field requests and freshness violations with the field owners present. Buys nothing in a month with no schema churn, and buys back the quarter in the month someone adds nine fields nobody owns.
6. **Quarterly source refresh** → `mbfinotti/revops-skills@revops-radar`. Four near-zero firings a year buying currency rather than an outcome.

- efficiency: `forecast diagnostic > kickoff re-invocation > renewal stack review > hygiene pass > governance review > source refresh`
- value: `hygiene pass > forecast diagnostic > renewal stack review > governance review > kickoff re-invocation > source refresh`
- effort: `hygiene pass > renewal stack review > governance review > forecast diagnostic > kickoff re-invocation == source refresh`
- compliance cost: `renewal stack review > governance review > hygiene pass == forecast diagnostic > kickoff re-invocation == source refresh (none)`, in that order:
  - A cut tool triggers a contract termination notice and a data-deletion or export obligation, both signed off outside RevOps and irreversible once the contract lapses.
  - A governance decision changes who may read and write customer fields, so it needs the data-protection owner's sign-off and is reversible only by another decision.
  - The hygiene and forecast outputs are both deal-level exception lists naming customers and amounts, so both need an output channel the team's data policy already covers, and neither triggers an approval.

The kickoff re-invocation and the source refresh tie on both axes for the same reason: each is one near-zero read, firing monthly or quarterly, needing nobody outside the person reading it, and each emits internal state or public sources naming no customer.

The source refresh is the cheapest candidate and the last one to install - the clearest proof that cheap and efficient are different orderings. The hygiene pass leads on value and sits third on efficiency, because what it costs is a weekly session plus a rep chasing every disposition it produces.

Default: rungs 1-2, which is two routines. Add the renewal stack review once a contract inventory exists, the hygiene pass once someone owns the exception follow-through, the governance review once schema churn is real. Never exceed 4 - the cap is what protects the routines that matter from the ones that fire into the void.

The ranking is a default, not a law; it shifts with the motion and with who executes it. Re-rank it against the interview:

- A close date inside two weeks (Q4b) means install the forecast diagnostic and nothing else until the quarter closes.
- A renewal cluster or budget cycle inside the quarter promotes the renewal stack review to rung 1, and a stack whose renewals all sit two quarters out demotes it below the hygiene pass.
- Limited admin capacity (Q4c) drops the governance review to quarterly.
- An unnamed CRM owner or sign-off (Q3) promotes the governance review above the hygiene pass, since the sweep has no rules to sweep against.
- A compliance or audit window (Q4d) promotes the governance review to rung 1.
- "One-off, hours only" (Q5a) means install one routine - the kickoff re-invocation - not four.
- A team already running a weekly pipeline review makes the hygiene pass a duplicate, so demote it rather than sweep the same deals twice.

Anchor triggers to the revenue calendar - quarter close, month end, board meeting date - rather than arbitrary dates whenever it fits. List and clean up obsolete routines left over from a previous quarter before adding new ones.

If the harness has no scheduled routines, fall back to one recurring calendar reminder ("RevOps check-in - re-run the revops kickoff") and stop there. See `references/routines.md` for the dry-run format, trigger anchoring, event-trigger preference, and cleanup checklist.

## 8. Invocation examples

- "Start a new RevOps project for our sales team."
- "Which revops skill do I need to fix our MQL handoff?"
- "Run my RevOps check-in."
- "Where do I start with RevOps here? The CRM is a mess."

## 9. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it doesn't cover wastes a session and hides the gap. Say "none fits" and name the gap - or point at `mbfinotti/sales-skills`/`mbfinotti/partnerships-skills` when the task actually belongs to one of them (see § 3).
- **Re-interviewing on a warm start.** The artifact exists precisely so questions aren't repeated. Ask only the session goal.
- **Routing from a guessed scope.** Route only from the declared scopes in `references/skill-routing.md`; a plausible-sounding guess misroutes confidently.
- **Routing an altitude, not a subject.** The four macro skills share subject keywords with a tactical sibling each. Sending "our stages are meaningless" to `revenue-funnel`, or "we have two ARR numbers" to `crm-data-governance`, hands the user a session at the wrong altitude - the answer arrives correct and useless.
- **Uncapped interview.** Past 7 questions the kickoff becomes a form the user abandons. Detection, not questions, fills the gaps.
- **Routines with no output channel.** They fire into the void and get silenced, burying the one routine that mattered.
- **A flat short-list.** Six equal-looking options get picked by taste or by whichever sits first. Order by value per unit of effort and name both sides on every line, or the user cannot choose.
- **Leading with the cheapest option.** Cheap and efficient are different orderings, and only the second one answers "what first". A near-zero routine that buys near-zero is a rounding error, not a quick win.
- **Ranking the routing table or the chain.** Scope is a match test and a chain is a dependency order; imposing a ratio on either invents a preference that does not exist.
- **Demoting a ruled-out skill instead of deleting it.** A skill the interview took off the table, parked at the bottom of the short-list, reappears as scope two sessions later. Delete it, or move it to "not now" with its unblocking condition.
- **Memory committed silently.** Teammates can't review what they can't see land. Diff and approval, always.
- **Stale routing table.** Update this skill - table, `references/skill-routing.md`, boundary pairs, chains, gap list - whenever the collection changes: a skill added, renamed, removed, or re-scoped. A stale router sends users to skills that no longer exist, which is worse than no router at all.

## 10. Pass bar

Before ending the session, check every item. If any fails, fix it and re-check - do not close the session on a failing bar.

1. Every recommended skill's declared scope actually matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the 20 skills in the table above.
3. Interview stayed within its cap: at most 7 questions on cold start, only the session-goal question on warm start.
4. `revops-context.md` was written or updated, including a session-log line, before the session ended.
5. Every proposed routine was shown as a dry-run and has an explicit output channel.
6. The short-list and the routine set are both ordered by value per unit of effort, each entry naming the bottleneck it attacks and what it costs - and the re-rank was stated out loud whenever an interview answer moved something off its default place.
7. Every class the interview ruled out left the short-list entirely, rather than sitting at the bottom of it.
8. The routing table and any proposed chain were left unranked - match test and dependency order respectively.

## References

- `references/skill-routing.md` - per-skill route/do-not-route signals, boundary-pair disambiguations, ordered chains, coverage gaps, and sibling-repo (`mbfinotti/sales-skills`, `mbfinotti/partnerships-skills`) hand-off signals. Read before routing any ambiguous task.
- `references/context-artifact.md` - the artifact template, one worked example, one negative example.
- `references/routines.md` - dry-run format, revenue-calendar trigger anchoring, event triggers, cleanup checklist.
