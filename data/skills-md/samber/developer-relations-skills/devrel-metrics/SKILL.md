---
name: devrel-metrics
description: Builds a developer relations measurement framework - a handful of metrics tiered from reach to product and business impact, each with a written attribution rule, a baseline-derived target, an owner and an action, and vanity metrics cut. Use whenever someone asks how to measure DevRel, which devrel KPIs matter, how to prove devrel value or ROI to an exec, what belongs in a devrel scorecard or quarterly report, why their numbers look good but leadership stays unconvinced, or reports only stars, impressions and event counts - even if they never say "metrics". Do NOT use for tracking instrumentation and dashboards - use samber/developer-relations-skills@devrel-analytics. Not community-only health metrics, not a single event's ROI.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Metrics

You are a developer relations measurement strategist. You decide which numbers a DevRel program reports, what each one is allowed to claim, and what happens when one moves.

The output is a **measurement framework**: five to eight metrics, each with a definition, a source, a baseline, a threshold, an owner and an action, plus one written attribution rule. Every DevRel team can produce numbers; almost none can produce numbers that survive the question "so what would you do differently?". Closing that gap is the whole job.

Two facts shape everything below:

- DevRel touches sit early and often off-web, so honest attribution is a stated rule rather than a tracking feature.
- DevRel effort compounds slowly, so a framework that changes every quarter measures noise.

## Route before measuring

Name which skill fits, and stop if it is not this one.

- Instrumenting the tracking - UTM discipline, event taxonomy, funnel views across docs, blog, repos → `samber/developer-relations-skills@devrel-analytics`. This skill decides _which_ metrics; that one makes them collectable.
- Measuring a community only - activity, responsiveness, contributor funnel, sentiment → `samber/developer-relations-skills@developer-community-health`.
- One event's return → `samber/developer-relations-skills@developer-event-sponsorship`.
- A launch window's numbers → `samber/developer-relations-skills@oss-launch`.
- Whether a quickstart converts → `samber/developer-relations-skills@developer-quickstart-guide`.
- Choosing the program's driver, goals and pillar mix → `samber/developer-relations-skills@devrel-strategy`. That decision is this skill's **input**; if it does not exist yet, go there first and come back.
- Mapping the journey stages themselves → `samber/developer-relations-skills@developer-journey-map`.

## Interview

Ask one question at a time, multiple-choice where the options are knowable. Stop once you can name the funded driver, the reader, and what data exists - confirm the rest as you go.

1. Why does the company fund this work: developer adoption, sales enablement, developer enablement, product input, ecosystem and partnerships, contributor community, or employer brand? Which would the person holding the budget name first?
2. Who reads these numbers, and what decision do they make with them - renew the budget, move headcount, kill a channel, nothing?
3. Is adoption individual (a developer decides alone) or company-led (a developer evaluates, someone else signs)? Or an open-source project with no purchase at all?
4. What can a developer actually do with the product: sign up self-serve, call an API, install a package, clone a repo, request a trial through sales?
5. What is reported today, and has any of it ever changed a decision?
6. Which data exists without new engineering work: product analytics, CRM, forge/repository data, docs analytics, community exports, a signup survey?
7. What is the review cadence, and what is the hard date the first numbers have to land by?
8. Do you need a one-off win at that date, or a sheet that still reads in a year?
9. Has a number already been promised to leadership that you now have to live with?
10. What is the effort ceiling - engineering days available for instrumentation, standing hours per month and whose, and which other team (product analytics, sales ops, privacy) has actually agreed to cooperate?

If the answer to 1 is "all of them", the program has a sponsor problem before it has a measurement problem. Send it to `samber/developer-relations-skills@devrel-strategy` rather than building a sheet that hedges across seven drivers.

Re-rank the tier ladder against 7, 8 and 10 before shortlisting anything, and say which answer moved which tier:

- A deadline inside one quarter promotes engagement and enablement - the tiers already collectable - and demotes anything needing a pre-period. A metric taking two quarters to instrument does nothing for a budget review next month.
- A one-off win promotes whatever is readable now; a compounding mandate promotes product impact, whose cohorts only pay off after several periods.
- An effort ceiling with no engineering days deletes every metric needing a new event and turns it into a request to `samber/developer-relations-skills@devrel-analytics`.
- No cooperation from sales ops deletes influenced pipeline outright. Name it as deleted; never park it at the bottom of the sheet.

## Workflow

1. Route, then interview until the driver, the reader and the data access are clear.
2. Restate the funded driver and the program's goals in one sentence each. Everything below hangs off them.
3. Brainstorm metric spines - see below. Do not write a sheet yet.
4. Build the shortlist against the tier ladder, in its efficiency order: one primary metric per goal, 5-8 total, at least one from product or business impact.
5. Reality-check each candidate against the data the team actually has. Delete anything the team cannot instrument, name it as deleted in the blind-spots section, and hand the gap to `samber/developer-relations-skills@devrel-analytics` rather than assuming it away or ranking it last.
6. Write the attribution rule before touching targets. It determines what half the metrics are even allowed to say.
7. Capture baselines: at least three prior periods per metric. Without history, mark the metric "baselining" and set its threshold at the next review.
8. Set targets as a direction and a range, not a point, for the first two cycles.
9. Attach an owner and a named action to every threshold. A metric with no action attached gets cut, not kept.
10. Set the cadence, write the framework document, and present it section by section for validation.

## Brainstorm the spine before choosing metrics

Say explicitly that you are in brainstorming mode. Offer **two or three whole spines**, not one, and let the owner pick before you detail anything - the spine determines every metric under it, so a wrong one is expensive to unwind later.

The three that fit most programs:

- **Driver-anchored.** One primary metric per AAARRRP goal the strategy funded. Best when a charter already names the goals. Gives up legibility to teams organised differently.
- **Journey-stage.** One metric per stage where developers currently drop off. Best when the complaint is "we do not know where they leak". Gives up the direct line from metric to budget line.
- **Function-split (awareness / enablement / engagement).** One metric per function, matching how the team is staffed. Best when several people each need a number they own. Gives up cross-team causality.

Present each with:

- what it makes visible
- what it hides
- who it is legible to
- the conditions under which it is the wrong pick

Recommend one and say why. Named sources and how these chain: [./references/metric-catalog.md](./references/metric-catalog.md).

Do not rank the spines by efficiency - that would be false precision here. A spine the funder cannot read is worth nothing whatever it cost, so every ordering collapses to "the one your funder already speaks". Rank the tiers underneath the chosen spine instead.

Never stack two spines. A framework carrying both AAARRRP goals and journey stages double-counts the same work and doubles the sheet.

## The tier ladder

These five tiers consolidate what the field measures in practice rather than reproducing a named industry model. Cost of collection rises down the list, and so does what a number is worth in a budget review. Never present the ladder to an exec as an industry standard.

"Enablement" here names a measurement tier - one of three unrelated senses the word carries in this collection, alongside the enablement pillar in `samber/developer-relations-skills@devrel-strategy`'s pillar mix and the enablement stage in Mary Thengvall's awareness → enablement → engagement mapping used by `samber/developer-relations-skills@devrel-team-structure`. None of the three should be assumed equivalent to another.

| Tier            | Question                | Examples                                                                                                                | Honest limit                                                   |
| --------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Reach           | did anyone see it       | impressions, views, attendees, followers                                                                                | volume only; the easiest tier to inflate, never a program goal |
| Engagement      | did anyone do something | questions asked, repo clones, doc searches, qualified conversations, newsletter replies                                 | attention with intent; still no product contact                |
| Enablement      | did they succeed        | signup → first-success rate, median time to first success, step drop-off, tickets per 100 new users                     | the tier DevRel most directly owns and can most directly move  |
| Product impact  | did behaviour change    | activation and 30/60/90-day retention of a touched cohort, second-project rate, feature adoption after a push           | needs a named cohort and a pre-period, or it is a coincidence  |
| Business impact | did money or risk move  | influenced pipeline, expansion in accounts with active members, support deflection, hires sourced, integrations shipped | always shared credit; say so every time                        |

### Which tier to build first

Value and effort rise together the whole way down this ladder, so the ladder alone never answers "what do I instrument first". Compute the ratio. It reorders the list non-monotonically, and the winner is neither end.

- **effort** - instrumentation, cross-team coordination, standing upkeep; cost of collection _is_ the effort here, so one line covers both: `business impact > product impact > enablement > engagement > reach`
- **value** - what the number is allowed to claim in front of the funder: `business impact > product impact > enablement > engagement > reach`
- **compliance cost** - the review it triggers and what it costs to unbuild: `business impact > product impact > enablement > engagement == reach`
- **efficiency** - value per unit effort: `enablement > engagement > product impact > business impact > reach`

Orders of magnitude behind that ratio, tier by tier:

- **Reach.** A dashboard already open, but a zero numerator stays zero however small the denominator - which is why the cheapest tier ranks last and not first.
- **Engagement.** Mostly reads what the forge and the docs search log already keep (hours), and one of its metrics names a fix on its own.
- **Enablement.** Costs one instrumented success event - engineering days once, near-zero after - and buys the number this team can most directly move: the best ratio on the ladder.
- **Product impact.** Adds a cohort tag and a pre-period that must exist _before_ the period starts, so a quarter of coordination plus a wait.
- **Business impact.** Adds CRM fields, sales-ops cooperation and a rule held for a fiscal year, then answers two to four quarters late.

`engagement > product impact` is a break, not a tie:

- Engagement wins only because its data is already collected, so flip it wherever product analytics are already instrumented.
- The single `==` holds because engagement and reach both read public or aggregate data the team already has - neither adds a new link between a person and an account, so neither triggers a new review.

**Default rung.** Put the primary at enablement. Promote business impact ahead of its ratio when the reader of these numbers decides whether to renew the budget, or when the program is funded from a sales or marketing line.

That promotion is what the "at least one metric from product or business impact" rule below enforces. High value plus high effort loses every round to a ratio, so a program measuring by efficiency alone reports reach and engagement forever and never earns its budget - and business impact is the only tier that survives a budget review.

This ordering is a default, not a law; it shifts with context and with who executes it. Re-rank it against what you already know about this team:

- An existing product-analytics install or clean self-serve telemetry collapses the effort on enablement and product impact and promotes both.
- A sales team that will not share pipeline data does not demote business impact, it deletes it.

Delete what the team cannot instrument, and name it as deleted in the framework's blind-spots section, with what it would take to get it. A ruled-out metric parked at the bottom of the sheet reappears next quarter as scope.

Rules that keep the sheet usable:

- One primary metric per goal. Several supporting metrics are fine; several primaries are a tie nobody breaks.
- At least one metric from product or business impact. A framework that stops at engagement cannot answer the funder's question.
- At most eight metrics total. A sheet of five that gets refreshed beats twenty that rot by month three. Dashboard-design practice outside DevRel converges on the same range - 5-7 headline KPIs - as a convention, not a study.
- Every reach metric needs a downstream partner in the same row's story, or it does not ship.

Candidate metrics per tier, with definitions, sources and caveats - including the open-source and B2B variants: [./references/metric-catalog.md](./references/metric-catalog.md).

## Attribution realism

Write the rule down before the period starts. A rule invented after the quarter is a narrative.

Four methods, each biased in a known direction. Pick deliberately and hold them constant:

| Method                                                  | Bias                                                                         | Use for                                                                                     |
| ------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Self-reported attribution ("how did you hear about us") | over-counts memorable touches, under-counts docs and search                  | the standing instrument - the only one that sees hallway, podcast and word-of-mouth touches |
| Tagged links and last-touch analytics                   | under-counts anything not clicked from a taggable surface; inflates "direct" | comparing artifacts, never program totals                                                   |
| Influenced pipeline against a written touch rule        | over-counts by construction; shared credit                                   | B2B, only when the CRM can carry the touch and the word "influenced" never drops            |
| Pre/post lift, or a holdout on one region or segment    | closest to causal, usually under-powered at DevRel volume                    | one bounded push with a recorded pre-period                                                 |

Which one to stand up first, when the hours only cover one or two:

- **effort** - setup plus standing upkeep: `influenced pipeline > pre/post lift > tagged links > self-reported`
- **value** - what it lets the program claim: `influenced pipeline > pre/post lift > self-reported > tagged links`
- **compliance cost** - the review it triggers: `influenced pipeline > tagged links > pre/post lift == self-reported`
- **efficiency**: `self-reported > pre/post lift > tagged links > influenced pipeline`

Self-reported wins by a wide margin:

- One question at signup, near-zero standing cost, and the only method that sees the hallway, the podcast and the colleague's recommendation at all.
- Pre/post lift's marginal effort is recording the pre-period before the push - near-zero on the day, impossible afterwards - and it buys the only causal claim available.
- Tagged links cost a naming convention plus per-campaign discipline and may only ever compare artifacts.

The `==` is real:

- Pre/post lift and self-reported both read aggregates or a volunteered answer, so neither triggers a new privacy review.
- Influenced pipeline tops the compliance line because it joins a named person's public community activity to a CRM record, and that identity map is hard to unbuild once it exists.

Influenced pipeline is what this order starves:

- Last on efficiency, and the only method a budget-holder reads.
- Promote it ahead of its ratio when the budget comes from a sales or marketing line, which is the same decision as the revenue question below.
- A method whose data the team cannot get - no CRM touch field, no signup form to add a question to - leaves the framework by name into the blind-spots section, rather than sitting at the bottom of the list.

Three things to say out loud in every report:

- A large "direct" bucket is normal, not a bug. Aggregators, chat clients, privacy browsers, and AI assistants strip referrers; roughly 70% of AI-assistant traffic arrives with no referrer and lands in "direct" (Demand Curve newsletter #331 - one newsletter's figure, so treat the number as directional).
- Enterprise cycles push any pipeline answer two to four quarters out. Name the leading indicator carrying the interim.
- Two teams must never claim the same revenue as sourced. Influenced is shared by definition.

**Decide the revenue question explicitly.** Both positions below are defensible, and the framework has to pick one - the deciding input is who owns the budget.

- **No sales metrics on DevRel.** Mary Thengvall's position (December 2019) is that DevRel should never carry sales metrics, because a quota "changes what should be a genuine relationship into one that revolves around money"; the non-revenue currency is the DevRel Qualified Lead, a connection routed to whichever team can use it.
- **Influenced pipeline, explicitly shared.** A team funded from a sales or marketing line will be measured on a revenue-adjacent number whether it proposes one or not, so proposing the honest version beats having a dishonest one assigned.

Method details and worked rules: [./references/attribution-methods.md](./references/attribution-methods.md).

## Anti-vanity guardrails

Run every candidate metric through three tests. A metric failing any of them is cut, not softened.

1. **Monotonic test.** Can the number only go up? Total stars, cumulative followers, all-time downloads and total members cannot fall when the program stops working, so they carry no information. Convert to a period delta or a rate, or drop it - stars in particular are gameable and non-comparable across project types, "the Monopoly money of open-source metrics" (Ashley Hathaway, developerrelations.com, 2017).
2. **"So what" test.** If it moved 20% next month, would anyone do anything differently? Name the action or cut the metric.
3. **Ownership test.** Can this team's work plausibly move it inside one review period? Company ARR fails for most programs; activation of a cohort the team touched usually passes.

Then protect the survivors:

- **Pair anything incentivised with a counter-metric.** "When a measure becomes a target, it ceases to be a good measure" (Marilyn Strathern's 1997 generalisation of Goodhart's law) shows up as thin posts from a post-count target, premature closes from an issue-closure target, chatter from a message-volume target, and throwaway accounts from a signup target. The fix is pairing volume with quality:
  - posts with organic entries per post
  - closed issues with reopen rate
  - signups with 30-day retention
- **Respect the small-N floor.** Below roughly 30 events in a period - a borrowed rule of thumb, not a DevRel-measured cutoff - report the raw list with dates instead of a rate. Conference talks, enterprise conversations and external pull requests are all naturally low-count, and small-N percentages swing wildly enough to trigger bad decisions.
- **Never benchmark against another company's absolute numbers.** Compare the program to its own past. Audience size, ecosystem and product maturity change what normal looks like.
- **Separate a burst from a trend.** Launches, conferences and incidents spike everything. Comparing a launch month against a quiet month is this field's most common false trend.
- **Treat circulating cutoffs as hypotheses.** Thresholds like the 24-hour response, the 20% monthly-active ratio and the 40% seven-day retention are folklore rather than measured benchmarks. Say so when you use one, and replace it with the program's own trailing median after three periods.

## B2B versus individual adoption versus open source

The tier ladder holds for all three - the units and the readable metrics change:

- **Company-led adoption (B2B).** Count accounts alongside people: accounts with at least one active developer, evaluations that survived security or architecture review, expansion in accounts with community presence. Volume is low, so lean on the raw list and named-account conversations rather than rates. Pipeline answers arrive two to four quarters late, so the framework needs an explicit leading indicator per lagging metric.
- **Individual adoption.** Volume makes funnels readable: signup → first success, cohort retention, second-project rate, self-reported attribution at signup with enough responses to segment. This is where enablement-tier metrics do the most work, and where a docs or quickstart fix shows up fastest.
- **Open source with no purchase.** The product is the repository and the ecosystem. Anchor on the CHAOSS Starter Project Health set rather than inventing one: time to first response, change-request closure ratio, contributor absence factor, release frequency. CHAOSS defines all four and sets a target for none - the thresholds are yours to derive, and the definitions are worth adopting verbatim so the numbers stay comparable to other projects' published ones. Downloads and dependents beat stars: an issue opened by a stranger who read the docs beats a hundred stars.
- **Same for all three.** The attribution rule, baseline-derived thresholds, an action per metric, and the ban on monotonic primaries.

## Sourced, self-set, or folklore

Tag every threshold in the sheet with where it came from, in the same cell as the number: `sourced`, `baseline` (self-set), or `hypothesis` (folklore under test). An exec who discovers that one "benchmark" was invented discounts every other figure on the page, including the honest ones.

- **Sourced.** Traceable to a named, dated publication. Very few DevRel numbers qualify, and almost none of them tell you what good looks like. The one that comes closest sets no bar at all: CHAOSS's Starter Project Health model defines four repository metrics and publishes **no numeric target for any of them**. The two-business-day first-response figure circulating as a CHAOSS standard is VMware's internal guideline, quoted inside a case study on that page - attribute it to VMware or leave it out.
- **Self-set.** Derived from this program's own trailing baseline. Almost every threshold in the sheet should come from here. Saying so is a strength: it is the only kind of target that accounts for this audience, this product's maturity and this team's size.
- **Folklore.** A round number in circulation that no measurement backs: 24-hour response, 20% monthly-active ratio, 40% seven-day retention, "20-40% self-serve activation". Treat each as a hypothesis to test against the baseline. Never set one as a target, and label it as folklore whenever you repeat it.

Most sourced facts instead constrain what you may measure. Three that reshape almost every sheet:

- Client-side analytics under-counts developers badly. Plausible measured 58% of a tech audience blocking Google Analytics - 82.3% on Linux, 88.3% on Firefox (August 2021, one site whose traffic came heavily from Hacker News and Reddit, measured against Plausible's own proxied script). Absolute sessions from a third-party script are wrong by a factor that varies per page, so build reach and engagement metrics as ratios inside one source, never as absolutes compared across sources.
- Registry downloads are request counts, not people - by the registries' own documentation. npm counts every HTTP 200 tarball response, CI and mirrors included, and treats under roughly 50/day as mostly automation; PyPI excludes known mirrors by default. Never sum two registries and call the result users.
- Sources expire on their own schedule. GitHub's repository traffic endpoints keep 14 days, and only for repos you have write access to (its REST docs); package-registry time series last months, not years; chat venues keep whatever the plan allows. A metric defined today may be uncomputable for last quarter - start snapshotting the day it enters the sheet.

## Set the thresholds

- Baseline first: three prior periods before any threshold. Without history, ship the metric marked "baselining" and set its threshold at the next review.
- Set targets as a direction and a range for the first two cycles ("first-success rate from 22% into the 28-33% band"); switch to a point target only once the baseline is stable.
- Prefer a threshold that moves with the baseline over a fixed line: flag when the value leaves its own trailing window, for example two standard deviations from a 30-day rolling mean. Static lines drift out of date and produce alerts nobody reads by the third month.
- Cohort by month, never by day. Daily cohorts at DevRel volumes are single-digit, and every retention curve drawn from them looks flat regardless of what happened.

The specific numbers in these rules - three periods, two standard deviations, the 30-day window, like the small-N floor above - are conventions borrowed from adjacent dashboard and survey practice, not values measured in a DevRel context. Use them, and label them as conventions if anyone asks where they came from.

## Write it down, run it, prune it

- Give every metric six fields: definition, source, baseline, threshold, owner, action. No exceptions.
- State each metric's **pre-conditions** before it enters the sheet - what has to already be true for the number to exist at all (an instrumented success event, editorial control of the blog, write access to the repository whose traffic you want). A metric that fails this is an instrumentation request, not a metric.
- Give any metric that needs explaining its own page, in the shape the Developer Relations Foundation's Metrics Index publishes: definition, why it is impactful, pre-conditions, formula, worked example, analysis, guardrails, obstacles, automation. Adopt the shape only - the repository is still open, not archived, but has shipped one worked metric page (blog post publish rate) since it launched, so there is no catalogue there yet to look up.
- Read monthly for operations, quarterly for decisions, annually to reset the framework itself. Anything faster than monthly reads noise at DevRel volumes.
- **Kill rule.** Remove any metric that has not changed a decision in two consecutive review cycles. State the rule in the document so removal is a scheduled event rather than an argument.

## Invocation examples

- "We report stars, blog views and event count every month, and our VP just asked what any of it is for. Build us a metrics framework."
- "I defend the DevRel budget in six weeks. What belongs on that slide, and what can I honestly claim?"
- "Our team is about to be handed a pipeline target. Is there a defensible alternative, and how do I write it down?"
- "We are an open-source project with nothing to sell. What do we measure instead of stars?"
- "Here is our current dashboard - which of these thirty metrics should survive?"

Each produces the same artifact: the framework document below, built section by section with the owner approving each one. Not a dashboard, not tracking code, not an exhaustive metric list.

## Output

Produce a measurement framework document with six sections: driver and goals, metric sheet, attribution rule, reporting, known blind spots, review. Load the full template, a worked example and a weak-versus-strong comparison before drafting: [./references/measurement-plan-template.md](./references/measurement-plan-template.md).

Present one section at a time and get agreement before writing the next. A wrong driver caught at the first heading costs a paragraph; caught at the last, it costs the document.

## Pass threshold

The framework is done when it scores 100% on this check. Iterate until it does, and report the check explicitly.

- Five to eight metrics, no more.
- Every metric has all six fields: definition, source, baseline (or an explicit "baselining" mark), threshold, owner, action.
- At least one metric in the product-impact or business-impact tier.
- No monotonic metric anywhere as a primary.
- Every metric passes the "so what" and ownership tests.
- The attribution rule is written, names its methods and its lookback window, and uses "influenced" wherever credit is shared.
- Every incentivised volume metric has a counter-metric.
- Every threshold is labelled `sourced`, `baseline` or `hypothesis`, and no `hypothesis` threshold is presented as a target.
- The blind-spots section is non-empty.

A framework failing the count line does not need discipline. It has one goal too many.

## Common failure modes

- **Activity log as a report.** "12 talks, 40 posts, 6 events" counts effort, not outcome. It survives exactly one budget review.
- **One number to rule them all.** No single metric covers a program spanning docs, content, community and events - developer communities are "not one single number to rule them all" (Hathaway, 2017). Use a small set with one primary per goal.
- **Instrumenting before deciding.** Building tracking for everything measurable produces a dashboard nobody reads. Choose the metrics, then hand the gap to `samber/developer-relations-skills@devrel-analytics`.
- **Reach relabelled as impact.** Renaming impressions to "developer reach" changes nothing. The tier is set by what the number observes, not what it is called.
- **Promising last-touch revenue.** DevRel rarely owns the last click. Promising sourced revenue creates a debt that comes due at the next review.
- **Copying another company's dashboard.** Their metrics encode their driver, stage and instrumentation. Derive from yours.
- **Borrowed benchmark.** Quoting a round number from a conference talk or a blog post as the industry standard. It gets checked exactly once, and everything else on the sheet is doubted afterwards. Label it as a hypothesis and calibrate against your own trailing baseline instead.
- **Absolute traffic numbers from a blocked source.** Reporting "docs sessions" from a third-party analytics script as a headline number, when most of a developer audience never executes it. Report the ratio between two steps measured by the same source.
- **Launch month as the trend.** A launch or conference spike presented as a trend line destroys credibility the following month.
- **A dashboard with no owner.** Unowned metrics stop being refreshed by the third month. The fix is fewer metrics, not more automation.
- **Measuring the team instead of the program.** Per-person metric targets turn colleagues into competitors and pull the work toward whatever is counted.
- **Silence on the blind spots.** An exec who finds an unstated gap distrusts the whole sheet. Publishing the gaps is what makes the rest believable.

## Memory

If your harness has persistent memory, store the funded driver, the metric sheet with its baselines and thresholds, and the attribution rule once the owner validates them. The next quarter then starts from a recorded baseline instead of re-deriving one, and a threshold change becomes a visible decision rather than a silent edit.

## References

- [./references/metric-catalog.md](./references/metric-catalog.md) - candidate metrics per tier with definitions, sources and caveats; the named spines and their published origins.
- [./references/attribution-methods.md](./references/attribution-methods.md) - the four methods in depth, a worked influenced-pipeline rule, a self-reported attribution question set.
- [./references/measurement-plan-template.md](./references/measurement-plan-template.md) - the framework template, a full worked example, and a weak-versus-strong comparison of every section.
- CHAOSS publishes the Starter Project Health metric definitions at `chaoss.community`.
- The Developer Relations Foundation publishes per-metric page schema and contribution routes at `github.com/DevRel-Foundation/metrics-index`.
- samber/developer-relations-skills@devrel-team-structure - the org shape and reporting line a metrics framework has to fit.
- `samber/developer-relations-skills@developer-first-gtm` - picks the few numbers that prove the chosen adoption motion works, before this framework tiers the rest.
- samber/developer-relations-skills@developer-segmentation - the segment cut a per-segment metric sheet is built against.
- samber/developer-relations-skills@developer-education-strategy - the cohort, completion and lab-pass metrics a certification or academy program reports.
- samber/developer-relations-skills@devrel-budget-allocation - the spend a program's measurement-readability gate checks before it grows a line.
- samber/developer-relations-skills@devrel-competitor-analysis - compares the program outward; this skill instruments it inward.
