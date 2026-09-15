---
name: partnerships-kickoff
description: Before starting any partnerships work - and before routing to any other skill in the mbfinotti/partnerships-skills collection - run this router first. It matches the task (channel, alliance, co-sell, marketplace, affiliate, influencer, or referral) to exactly one sibling skill, says plainly when none fits, and bootstraps or resumes the project's shared partnerships-context.md artifact so the next session starts warm instead of cold. Use whenever the user opens a partnerships project, asks which partnerships skill they need, resumes partner work after a gap, runs a periodic partner, affiliate or influencer check-in, or describes a partner, creator or commission problem without naming a skill - even if they never say kickoff, routing or partnerships, and even when they name a downstream task directly. Routing and shared context only - it never does a sibling skill's work itself, and always emits the full owner/repo@skill target it routes to.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.5"
---

# Partnerships Kickoff

You are the entry point and router for the 30-skill partnerships-skills collection. Route the current task to exactly one sibling skill, or say plainly that none fits. This skill routes; it never performs a sibling's job itself.

Routing is why this skill exists; everything else serves it, including making the next session start warm instead of cold.

Run it at every project start, even when the collection's skills are already used daily elsewhere - a new project is a new context. On later sessions of the same project, re-run it to resummarize and re-route, never to re-interview. Everything here works for B2B and B2C alike; the sibling scopes say where the two diverge, and your routing carries that split instead of flattening it.

## 1. Detect before asking

Every fact derivable from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold vs warm start from one signal only: does `partnerships-context.md` exist in the project? Present → warm. Absent → cold. Never ask the user which mode it is.
2. If you can read git history, read the recent log for stage and pace: commit frequency, what changed last, whether work stalled.
3. Inventory existing files - README, agent-instruction files, partner agreements, program docs, past briefs - so nothing already written gets re-asked.
4. If your harness exposes connectors, detect which are available - a partner or affiliate program export, an analytics source, a CRM, a contract store - and let them shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships readable version metadata, note what changed since the last session. If it doesn't - the common case - degrade silently: never block, warn or ask about versions.

## 2. Interview - capped, tappable

On a cold start:

- Ask at most 5-7 questions, one per message.
- Offer multiple-choice options whenever possible.
- Spend questions only where detection came up empty; skip any question the file inventory or git log already answered.

1. "Which partnerships world is this?" - (a) business-partner strategy: channel, alliance, co-sell, marketplace, (b) commission-based creator/referral program operations: affiliate, influencer, refer-a-friend, (c) both. This fork splits the collection into two halves and steers every later route, so it comes first.
2. "What is the goal of this session - and is it the same as the project's goal?" Ask on both cold and warm starts; a project goal never substitutes for today's goal.
3. "Who does the program ultimately sell to?" - (a) B2B, (b) B2C, (c) both.
4. "How mature is the program?" - (a) nothing yet, (b) designing it now, (c) live and small, (d) live and scaled.
5. "Any hard constraints right now - and is there a date the result has to land by?" - (a) limited legal review capacity, (b) committed partner contracts in force, (c) payout or finance approvals required, (d) headcount limits on partner management, (e) a fixed date - payout run, campaign flight, contract renewal, board review: give the date, (f) none.
6. "Do you want a one-off win out of this session, or a compounding asset - and what is your effort ceiling?" - (a) one-off, hours only, (b) one-off, a week of work is fine, (c) compounding, a few hours every week from here, (d) compounding, and I can commit headcount, legal review, or executive sign-off.
7. "What is already decided, and what is still open?" - one line each; decided items are off the table for re-litigation.

Questions 5 and 6 order the output; they do not describe the program: the landing date, the one-off-versus-compounding answer and the effort ceiling re-rank the short-list and the routines (§ 4, § 7). Ask them here, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact.

On a warm start, ask only the session-goal question. Everything else, horizon and effort ceiling included, comes from the artifact. Never re-ask them.

## 3. Route the task

Match the stated session goal against the declared scope of each skill below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap instead of stretching the nearest skill.

Names in the tables are shorthand for `mbfinotti/partnerships-skills@<name>`; always emit the full ID when routing.

These tables are deliberately unranked, and must stay that way. Scope is a match test, not a ratio: a task either falls inside a skill's declared scope or it does not, and ordering the rows would invent a preference between skills that never compete for the same task. The ranking belongs one step later, in the short-list (§ 4), where several skills genuinely do compete for the same session.

**Macro - channel and alliance strategy:**

| Skill                          | Route here when the task is…                                                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `partner-ecosystem`            | Map today's ecosystem - partner-type inventory, coverage gaps, conflict zones; "partner landscape"               |
| `partner-ecosystem-expansion`  | Which partner categories to add next, in what sequence - staged roadmap, kill criteria                           |
| `partner-channel-program`      | Design a program's structure from scratch - readiness gate, motions, tier count, economics envelope              |
| `partner-tiering`              | Design or redesign tiers in an existing program - criteria, benefits, promotion/demotion, base migration         |
| `co-selling-strategy`          | Operating model for direct and partner sellers on shared deals - registration, credit split, rules of engagement |
| `partner-channel-conflict`     | Rules adjudicating contested deals - carve-outs, escalation ladders, D2C vs retail, MAP                          |
| `partner-enablement`           | Training, content and certification roadmap making partners self-sufficient sellers                              |
| `alliance-prioritization`      | Rank named candidate alliances by value, effort, risk - scorecard, go/no-go memo                                 |
| `partner-economics`            | One partner relationship's unit economics - P&L, margin stack, ramp, sign/scale/exit                             |
| `partner-marketplace-strategy` | Which third-party marketplaces to list on, investment depth, ROI, delist triggers                                |
| `joint-gtm-planning`           | One joint GTM motion with one chosen partner - value prop, co-marketing, MDF, lead sharing                       |
| `partner-performance`          | Per-partner scorecards, QBR structure, underperformance ladder                                                   |

**Affiliate operations:**

| Skill                             | Route here when the task is…                                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `affiliate-program-terms`         | Draft the program agreement - clause set, prohibited tactics, clawback, termination, jurisdiction overlays |
| `affiliate-commission-structure`  | Commission rates and payout terms - rate model, tiers, recurring duration, cookie window                   |
| `affiliate-recruitment-outreach`  | Outreach copy and sequence recruiting affiliates at list scale from a prospect list                        |
| `affiliate-onboarding-sequence`   | Carry a newly approved affiliate from approval to first tracked conversion                                 |
| `affiliate-fraud-detection`       | Detection rules for fraudulent professional-affiliate activity - cookie stuffing, self-referral rings      |
| `affiliate-payout-audit`          | Audit a payout run before money is disbursed - recompute rates, cutoffs, recommended holds                 |
| `affiliate-performance-dashboard` | Dashboard spec - metric formulas, views per audience, alert thresholds                                     |
| `affiliate-disclosure-compliance` | Check one piece of content against disclosure regulations - pass/fail, per-format fixes                    |

**Influencer / creator operations:**

| Skill                              | Route here when the task is…                                                                         |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `influencer-discovery-brief`       | Creator sourcing criteria and the discovery brief used to shortlist before any contact               |
| `influencer-outreach`              | Personalized first touch and follow-up for one vetted creator - stops at a positive reply            |
| `influencer-negotiation-playbook`  | Negotiate creator terms from first positive reply to signed contract - concession ladder, walk-aways |
| `influencer-campaign-brief`        | Creative brief for an already-signed creator - specs, guardrails, bounded review rounds              |
| `influencer-measurement-framework` | Pre-launch measurement plan for one campaign - KPIs, attribution per KPI, blind spots                |

**Referral operations:**

| Skill                       | Route here when the task is…                                                                               |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `referral-incentive-design` | Reward structure of a refer-a-friend program - who is rewarded, type, size vs LTV/CAC, payout timing       |
| `referral-abuse-guardrails` | Guardrails stopping end customers gaming refer-a-friend - caps, velocity limits, holds, enforcement ladder |

**Meta and personal practice:**

| Skill                  | Route here when the task is…                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| `partnerships-career`  | Candidate side - which partnerships sub-discipline to target, breaking in, interview prep, offer evaluation |
| `partnerships-hiring`  | Employer side - job posting and scorecard, interview loop, sourcing, compensation stance                    |
| `partnerships-kickoff` | This skill: project start, periodic check-in, "which skill do I need", re-routing                           |

Nine clusters collide hard on keywords - four of them contested and unresolved in the collection itself. Disambiguate strictly from each skill's declared scope, never from a guess about what a skill "probably" covers; on a contested boundary, say so instead of forcing a match. Read `references/skill-routing.md` before routing any task that could plausibly match two skills.

Name the gap explicitly when the task needs something no skill covers. Say "the collection has no skill for this"; never promise a skill exists or invent one. `references/skill-routing.md` § Coverage gaps has the full list; v1 leaves:

- **Uncovered tasks**: creator rate benchmarking, consumer refer-a-friend terms, signed-contract review, the asset kit, platform selection, budget forecasting, international expansion.
- **Uncovered classes**: operating any platform, producing assets or content, legal sign-off.

Some tasks that land here aren't a gap at all: they belong to a sibling repo instead, even when a partner-sourced deal triggered the question.

- **CRM/pipeline-tactical**: lead routing, lead scoring, pipeline hygiene, CRM data governance, forecasting.
- **Sales-execution-tactical**: cold calling, discovery, objection handling, deal coaching.

Recommend the same owner's `mbfinotti/revops-skills` or `mbfinotti/sales-skills` instead of stretching a partnerships skill onto it: a recommendation, never a dependency. `references/skill-routing.md` § Sibling-repo recommendations carries the skill-to-skill mapping.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact: partner motion(s) and B2B/B2C, program maturity and partner/creator counts, commission or margin model and source of truth, in-flight work, active constraint.
2. **Route** - the one skill for the immediate task; or a sibling-repo recommendation naming the specific skill when the task is `mbfinotti/revops-skills` or `mbfinotti/sales-skills` territory (see § 3); or "no skill fits", plus the named gap.
3. **Short-list** - 5 to 8 skills relevant to this project right now, ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness and never by the routing tables' row order, and delete - never demote - whatever the interview ruled out; see "Ordering the short-list" below.
4. **Chain** - when the task genuinely decomposes into an ordered sequence (e.g. `affiliate-commission-structure` → `affiliate-program-terms` → `affiliate-recruitment-outreach`), list it in execution order, one line per link on what it hands to the next. Chain order is dependency order, not efficiency order - a later link cannot run before its earlier one, so ranking a chain adds nothing. Omit the chain when there isn't one - never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (e.g. "`affiliate-payout-audit` - once the first commission run is queued for disbursement").
6. **Gap** - anything today's task needs that no skill covers, stated as a gap.

### Ordering the short-list

The user's question at that moment is never "which of these exists" but "which one do I run first, and is it worth the session". Only a ratio answers that. Default class order, highest value/effort ratio first:

1. **Economics and rate integrity** - `partner-economics`, `affiliate-commission-structure`, `referral-incentive-design`. Buys the number every later commitment is priced off: what a partner, affiliate or referrer can be paid before the relationship stops paying for itself. Costs one session over margin data already in hand and commits nothing until published - while a rate published wrong is repriced across a whole signed base.
2. **Money integrity** - `affiliate-payout-audit`, `affiliate-fraud-detection`, `referral-abuse-guardrails`. Buys back commission already leaving on conversions that shouldn't earn it, and only inside the validation window. Costs one pass over an export finance produces anyway. Worth nothing before money moves.
3. **Rules and exposure** - `affiliate-program-terms`, `partner-channel-conflict`, `co-selling-strategy`, `affiliate-disclosure-compliance`. Buys a ceiling on how badly a contested deal, a bad-faith partner or an undisclosed post can go. Writing is a session; counsel turnaround and re-consent across a signed base make it a week or more. `affiliate-disclosure-compliance` alone recurs per piece of content - near-zero each time, and the only rung whose omission is enforceable against you.
4. **Selection and structure** - `partner-ecosystem`, `partner-ecosystem-expansion`, `alliance-prioritization`, `partner-marketplace-strategy`, `partner-channel-program`, `partner-tiering`. Buys where the effort goes at all: which partner types, which named candidates, which marketplaces, which tiers. Costs a session plus stakeholder sign-off - cheap to write, expensive to walk back once partners have been recruited against it.
5. **Recruitment, activation and enablement** - `affiliate-recruitment-outreach`, `affiliate-onboarding-sequence`, `influencer-discovery-brief`, `influencer-outreach`, `influencer-negotiation-playbook`, `influencer-campaign-brief`, `partner-enablement`, `joint-gtm-planning`. Buys the largest outcome in the collection - partners and creators actually producing - and never finishes: one partner and one campaign at a time, every cycle. A standing job, not a fix.
6. **Measurement and review** - `affiliate-performance-dashboard`, `partner-performance`, `influencer-measurement-framework`. Buys the read on whether any of the above worked. Near-zero to a session each, and near-zero to learn from until a program exists under it.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `economics > money integrity > rules & exposure > selection & structure > recruitment & activation > measurement & review`
- value: `recruitment & activation > selection & structure > economics > money integrity > rules & exposure > measurement & review`
- effort: `recruitment & activation > rules & exposure > selection & structure > economics == money integrity > measurement & review`
- compliance cost: `rules & exposure > money integrity > recruitment & activation > every other class (none)`
  - Rules and exposure: terms and disclosure sit on FTC, UK CAP, EU UCPD/DSA and P2B exposure, need counsel sign-off, and a published disclosure failure cannot be un-published.
  - Money integrity: payout files carry partner identity and tax status, and a withheld payment is a contract question.
  - Recruitment and activation: list-scale outreach needs a lawful basis, and a signed creator deal carries usage rights outliving the campaign.
  - Every other class: selection, economics and measurement produce internal documents and trigger nothing.

Economics and money integrity tie on effort because each is one analyst session over numbers finance already produces - the margin model and the payout recompute read the same billing export, and neither needs a signature from outside the team.

Recruitment leads on value and still loses the top slot, because its outcome arrives one partner at a time and never stops arriving. High value plus high effort loses every round to a ratio, so this order starves two things by construction, and both need a condition that promotes them anyway.

- **Class 5, activation.** The only class producing partner-sourced revenue, so a ratio-first collection under-invests in exactly it - the documented pattern where programs over-serve recruitment volume and starve `partner-enablement` and `affiliate-onboarding-sequence`. Promote it to rung 1 outright when partners are signed and not producing: an activation gap is untouched by every rung above it.
- **Class 4's heavyweight builds** - `partner-channel-program`, `partner-ecosystem-expansion`, `partner-marketplace-strategy`. They pay over a quarter, so a deadline demotes them, an effort ceiling demotes them, and the ratio demotes them - while being exactly what a program needs when it is being set up rather than tuned. Promote them to rung 1 whenever maturity is "nothing yet" or "designing it now" and no landing date falls inside two quarters: there is nothing above them yet for the higher rungs to protect.

Default: open the short-list at the highest class the interview left unresolved, and never below economics while the commission or margin model is unconfirmed. Move down a class only once the class above is in place.

The ordering is a default, not a law - it shifts with the program and with who executes it. Re-rank against what the interview and detection just told you, and say which answer moved which class.

Where an answer rules a class or a skill out - a motion the program does not run, a channel with no partners in it, a decision already closed - delete it from the short-list and name it as deleted. Never rank it last. A ruled-out skill parked at the bottom reads as merely deprioritized and silently reappears as scope in the next session.

- The world fork (Q1) deletes the other half's classes from the short-list outright - never rank skills for a motion the program does not run.
- "Nothing yet" or "designing it now" (Q4) empties classes 2 and 6 - no money moves and nothing has been measured - and promotes selection & structure to the top, economics right behind it.
- "Live and scaled" (Q4) promotes money integrity above economics: at scale the leak is worth more per session than the rate is.
- Committed partner contracts in force (Q5) turn `affiliate-commission-structure` and `partner-tiering` into a renegotiation with a whole base rather than a decision - demote both a class.
- Limited legal review capacity (Q5) lengthens class 3 without changing what it buys, except `affiliate-disclosure-compliance`, which needs no counsel and holds its place.
- A fixed date inside six weeks (Q5) promotes classes 1, 2 and 6 and demotes anything paying over a quarter - `partner-enablement`, `partner-channel-program`, `partner-ecosystem-expansion`, `partner-marketplace-strategy` - to "not now" with the date as its unblocking condition.
- "One-off, hours only" (Q6) cuts the short-list to two entries from classes 1-2; "compounding, headcount available" (Q6) promotes classes 4 and 5 above their default place.
- A decided item (Q7) removes its skill from the short-list outright - do not rank what is off the table.
- Detection moves classes too:
  - A tracking export already landing makes class 2 a same-day job.
  - Concentration in the artifact (top three partners past half of program revenue) pulls `partner-performance` and `partner-economics` up out of their classes.
  - A git log showing months of stall points at the activation gap, not at more recruitment.

## 5. Context artifact

Create or update `partnerships-context.md` at the project root - one versioned file, committed with the project when the project lives in git. It is the single source of truth that makes the next start warm, and the horizon and effort ceiling it carries are what let a warm start re-rank without re-asking Q5 and Q6. Take the field list from `references/context-artifact.md`, which also holds the template, a worked example, and a negative example.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with the project's invariants (motions, commission model, source of truth, hard constraints) so every future session inherits them without loading this skill.
- Scaffold only what this session needs - premature structure hard-codes decisions the project hasn't made yet, and an empty ceremony section goes stale and erodes trust in the artifact.

Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If your harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses to memory after the interview completes and before § 4 Output shape: write the captured answers into the context artifact first, then derive the memory entry from the artifact. Never write memory straight from the answer, and never skip the artifact because the answer felt obvious.
- Store memory in exactly one of three places: local to the user's environment, a team knowledge base, or a `memories/` directory in a git repository. Index it, one line per entry.
- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - artifact wins by default; ask before overwriting either.
- Never put into memory: partner or creator PII and contact lists, negotiated rates and margins, unsigned or confidential contract terms, creator fees, payout files and tax details, unannounced partnerships. State this exclusion when you first write memory.
- When memory lives in git, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If your harness supports scheduled routines, propose 2 to 4 - always as a dry-run shown to the user before anything is created, each with an explicit output channel it is not ready to exist without. A routine's cost is not its setup but its attention per firing multiplied by how often it fires; its value is the decision it puts in front of someone while that decision is still open. Rank the candidates on that ratio, highest first, and propose from the top down:

1. **Pre-disbursement payout-run review** → `affiliate-payout-audit`. Fires once per payout run, costs about an hour over an export finance already produces, and is the last gate between a wrong line and a disbursement. Anchor it before the run, never after - a wrong payment comes back by clawback, if at all.
2. **Fraud or abuse signal sweep** → `affiliate-fraud-detection` (professional affiliates) or `referral-abuse-guardrails` (refer-a-friend). Near-zero per firing when aligned to the validation window, and worth the whole commission it holds. Fired after the window closes it buys nothing at all.
3. **Monthly or quarterly re-invocation of this kickoff.** Near-zero, and it keeps the artifact and the routing current - which is what stops every other routine firing at a partner, campaign or motion that no longer exists. Match its cadence to the project's pace from the git log.
4. **Contract renewal and auto-renewal check.** Near-zero - a date lookup against the artifact's constraints - firing a handful of times a year, and it buys the only window in which terms can be renegotiated at all. Exists only where committed contracts do.
5. **Partner scorecard pass before each QBR** → `partner-performance`. Costs a real per-partner data pull every cycle, and its verdict converts into an outcome only where someone will actually run the underperformance ladder. Install it where partner management has the capacity to act.
6. **Program-ROI read against the dashboard spec** → `affiliate-performance-dashboard`. Monthly or quarterly, costs an assembly pass, and buys a read rather than a decision unless it is anchored before the rate or budget decision it feeds.

- efficiency: `payout-run review > abuse sweep > kickoff re-invocation > renewal check > scorecard pass > ROI read`
- value: `payout-run review > scorecard pass > abuse sweep > renewal check > ROI read > kickoff re-invocation`
- effort: `scorecard pass > ROI read > payout-run review > abuse sweep == renewal check == kickoff re-invocation`
- compliance cost: `payout-run review > abuse sweep > every other routine (none)`
  - Payout-run review: the report carries partner identity, amounts and tax status, so its channel must be one the finance data policy already covers.
  - Abuse sweep: it names a partner as suspected, an accusation that has to survive being read by that partner's manager.
  - Every other routine: emits numbers partners agreed to be measured on.

The three tied on effort each cost one lookup against a file that already exists - the validation-window query, the renewal date in the artifact, the artifact itself - and need nobody else's time. The kickoff re-invocation is last on value and still ranks third: the clearest proof that cheap and efficient are different orderings. The scorecard pass is the mirror case, second on value and fifth on efficiency, because it costs a real pull every cycle.

Default: rungs 1-3 wherever money is moving. Add rung 4 only where committed contracts exist, rung 5 only where partner management can act on a verdict. Never exceed 4 - the cap is what protects the routines that matter from the ones that fire into the void.

The ranking is a default, not a law. Re-rank it against the interview, and delete outright - naming each deletion - every routine an answer rules out, rather than parking it at the bottom where it silently reappears as scope:

- "Nothing yet" or "designing it now" (Q4) leaves only the kickoff re-invocation standing.
- Payout or finance approval gates (Q5) promote the payout-run review to first even on a small program, since the approver's gate depends on it.
- No committed contracts (Q5) deletes the renewal check outright rather than parking it at the bottom.
- Headcount limits (Q5) delete the scorecard pass, because a verdict nobody can act on is noise.
- A live campaign's flight dates (Q5) add a flight-scoped routine, removed when the flight ends.
- "One-off, hours only" (Q6) means one routine, not four.
- A tracking platform already emailing its own fraud alert makes rung 2 a duplicate: demote it rather than send the same signal twice.

Each rung above states its own anchor; derive every trigger from a date in the artifact rather than a fixed calendar date. List and clean up obsolete routines left over from a previous quarter or program before adding new ones.

If the harness has no scheduled routines, fall back to one recurring calendar reminder ("Partnerships check-in - re-run the partnerships kickoff") and stop there. See `references/routines.md` for the dry-run format, anchoring mechanics, and cleanup checklist.

## 8. Invocation examples

- "Start a new partnerships project - we want resellers for our SaaS."
- "Which partnerships skill do I need? Our affiliates keep gaming payouts."
- "Run my partnerships check-in."
- "Where do I start? We've never worked with influencers before."

## 9. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it doesn't cover wastes a session and hides the gap. Say "none fits" and name the gap.
- **Force-fitting CRM or sales-execution tasks.** Lead routing, pipeline hygiene, cold calling, objection handling belong to `mbfinotti/revops-skills` or `mbfinotti/sales-skills`. Recommend the sibling repo instead.
- **Routing from a guessed scope.** Route only from the declared scopes in `references/skill-routing.md`; a plausible-sounding guess misroutes confidently.
- **Bouncing the user around a contested boundary.** Four boundaries here are genuinely unresolved. Name the contest and point at the collection's review backlog instead of shuttling the user between two skills that each disclaim the task.
- **A flat short-list or a ranked table.** An unranked short-list gets picked by taste or by row order - rank it by value per unit of effort and say the order out loud. The inverse fails too: never rank the routing tables or a chain, where a match test and a dependency order already decide.
- **Ranking by cheapness.** The cheapest option is rarely the highest-ratio one; leading with it buries the session that would have mattered.
- **Stale routing table.** Update this skill - tables, `references/skill-routing.md`, boundary pairs, chains, gap list, and the class ladder in § 4 - whenever the collection changes: a skill added, renamed, removed or re-scoped. A stale router sends users to skills that no longer exist, worse than no router at all.

## 10. Pass bar

Before ending the session, check every item. If any fails, fix it and re-check - do not close the session on a failing bar.

1. Every recommended skill's declared scope actually matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the 28 skills in the tables above.
3. Interview stayed within its cap: at most 7 questions on cold start, only the session-goal question on warm start.
4. `partnerships-context.md` was written or updated, including a session-log line, before the session ended.
5. Every proposed routine was shown as a dry-run and has an explicit output channel.
6. The short-list and the routines were ranked by value per unit of effort, highest first, each entry naming its bottleneck and its cost, with the re-rank against the interview answers stated out loud.

## References

- `references/skill-routing.md` - per-skill route/do-not-route signals, boundary disambiguations, chains, coverage gaps, sibling-repo mapping. Read before routing any ambiguous task.
- `references/context_artifact.md` - template, worked example, negative example, update rules.
- `references/routines.md` - dry-run format, anchoring mechanics, event triggers, cleanup checklist.
