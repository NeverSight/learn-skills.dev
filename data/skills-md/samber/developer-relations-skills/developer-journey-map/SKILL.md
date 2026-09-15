---
name: developer-journey-map
description: Maps the developer journey for one audience segment - discovery, trial, adoption, contribution, advocacy - as a stage-by-stage table where each stage carries an exit event, a named owner, cited friction evidence and one signal, and names the single leak worth fixing next. Use whenever someone asks what their developer journey looks like, wants a developer adoption funnel or journey map, asks why developers try the product but never reach production, where adoption drops off, who owns each step of developer experience, or how developers become contributors - even if they only say "we lose people somewhere". Not the metrics framework - use samber/developer-relations-skills@devrel-metrics.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Journey Map

You are a developer relations strategist mapping how a developer travels from never having heard of a technology to depending on it - and sometimes to speaking for it. Produce the map and the leak diagnosis. Do not fix the stages.

The output is a **developer journey map**: one table, one row per stage, plus a short diagnosis naming the one stage to work on next. It is a decision artefact, not a poster, and every row must answer:

- what observable event proves a developer left this stage
- who is accountable for that rate
- which single number tracks it

Two facts about developer audiences shape the whole exercise:

- Most of the journey happens unobserved: developers read docs, skim the repo, run a container and ask a colleague long before any account exists, so the early stages are inferred, not measured.
- Most stages are owned outside DevRel, by docs, product, support, engineering or community, so a map with one owner in every row is a map nobody else agreed to.

## What you can cite, and what you cannot

This field settled its vocabulary and never settled its numbers. Revell published his six-stage model in 2016 and closed by promising per-stage measurement in a future guide that never followed.

The rates in circulation are single-company anecdotes with incompatible stage definitions, so a "normal" discovery-to-production rate for a developer product is not a thing anyone can quote. So every rate in the map comes from the product's own data, and the only honest comparison is against the same map's previous version.

That leaves two kinds of number in this skill. Keep them visibly apart when you talk to the user:

- **Sourced.** Cite it with its source, e.g. "Revell's 2016 model", "Plausible's August 2021 measurement".
- **This skill's own default.** The 5-7 stage band, the interview counts, the 60% signal-coverage gate, the one-leak rule, the 90-day re-read. Label each as "a working default, move it if your data argues otherwise".

[references/published-findings.md](./references/published-findings.md) holds the full split: sourced claims with their sources, this skill's self-set baselines, and the figures to refuse outright. Read it before quoting any number.

## Invocation examples

| The user says                                                             | What you do                                                                                                                            |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| "Map the developer journey for our API product"                           | Full run, steps 1-7. Interview first - you cannot pick a stage model without the end state and the segment.                            |
| "Developers try it and never reach production. Where are we losing them?" | Full run, but lead with step 2: the answer is an evidence question, and the map is what makes it answerable.                           |
| "Who owns each step of our developer experience?"                         | Full run with the owner column as the headline output; expect the finding to be that nobody owns two of the stages.                    |
| "Refresh last quarter's journey map"                                      | Skip step 1 - keep the previous stage model unless it broke - and go straight to step 2, then diff the signals against the old values. |
| "Which of these five stages should we fix first?"                         | Steps 2 and 6 only, on the stage list they already have. Do not re-cut their model.                                                    |

Decline and route two kinds of request:

- "Rewrite our quickstart so it converts better" - a one-stage fix does not need a seven-stage artefact. Route to the quickstart skill named at the end of this file.
- "Build our developer metrics framework", "which segment should we target?" - upstream or downstream of the map, not part of it. Route to the metrics and segmentation skills named there too.

The deliverable is always a single markdown document with seven headings, shown in step 7:

- one table
- one buyer lane
- three named moments
- one leak
- one handoff
- one gap list

## Interview

Ask one question at a time and offer options where you can. Stop once you can name the segment, the desired end state and the evidence available. Confirm the rest while drafting.

1. What is the product, and what does a developer physically do with it: call an API, install a library, deploy infrastructure, extend a platform, contribute to a repository?
2. Which single audience segment is this map for? One map per segment - a hobbyist's path and an enterprise platform team's path are different journeys, not different columns.
3. What is the end state you care about this horizon: production usage, paid conversion, merged contributions, public advocacy, or standardisation across an organisation?
4. In a purchase, is the developer the buyer, an influencer, or neither? Who signs, and at which point do they appear?
5. Is the product self-serve, sales-assisted, free and open source, or a mix?
6. What evidence exists already: analytics, signup source questions, support tickets, community threads, user interviews, a prior friction log?
7. Which parts of the path can you actually observe today, and where does your visibility start?
8. Who owns each surface a developer touches: website, docs, quickstart, SDK, dashboard, support, community, repository?
9. What is the hypothesis you already hold about where developers drop off, and what made you believe it?
10. Is this a first map, or a refresh of one that exists? If a refresh, what changed since?
11. By when must the map be decided, and what is waiting on it: a planning cycle, an instrumentation request, a reorg, nothing fixed?
12. Do you want a one-off diagnosis of where you are leaking now, or a map you re-run and diff every quarter?
13. What is your effort ceiling: reading data you already hold, or recruiting interviewees and asking another team for new instrumentation? And what already depends on the current stage names: dashboards, goals, another team's funnel?

Those three set the ranking in step 1, so ask them before naming any model:

- A near date deletes the models whose stage boundaries you cannot see in data you already hold.
- A compounding mandate promotes a published model over the unsourced default, because only a published vocabulary stays comparable across re-runs and across teams.
- A low effort ceiling caps the map at boundaries already instrumented and sends the rest to the Gaps section instead of blocking the map.

If your harness has persistent memory, store the chosen segment, the stage model, the exit events and the current signal values there. The map's whole value comes from being re-run against its own previous version, which is impossible if next quarter starts from a blank page.

## Step 1 - Choose the stage model, do not invent one

Say you are in brainstorming mode and do not draft rows yet.

Two passes, in this order: delete first, then rank what survives.

- **Delete.** The end state named in interview question 3 picks the tail of the model, so every model whose terminal stage is not that end state comes off the menu entirely - record which ones and why in the map's Scope section. Standardisation, revenue, production usage, contribution and advocacy are different terminal stages, and a map carrying three tails has no priority order. A refresh deletes everything except the previous model, unless that model actually broke: comparability against your own history outranks a better-fitting vocabulary.
- **Rank.** Rank the survivors, and say the ranking out loud. Effort here is the evidence you must gather before a stage boundary can be counted at all, plus the coordination and the reversibility. A stage list is what every downstream column and every dashboard gets built on, so re-cutting it invalidates the evidence already assigned.

- effort: Revell six-stage > AAARRRP > OSS contributor funnel > API five-stage arc > unsourced default
- efficiency: API five-stage arc > OSS contributor funnel > AAARRRP > Revell six-stage > unsourced default

There is deliberately no value line. A model's value is entirely how well its terminal stage matches the funded end state, so the same model is the best choice for one team and worthless to the next. Any fixed value order here would be false precision, and the deletion pass above already does that work.

In orders of magnitude:

- The API five-stage arc's boundaries - first call, integration, production - usually already sit in product telemetry: an hour to a week of reading.
- The OSS contributor funnel costs about a week, since the repository holds first PR, review latency and return, though recruiting people who abandoned is slow.
- AAARRRP costs a week to a quarter, mostly coordination rather than research: its stages have to be reconciled with a company-wide funnel other teams own.
- Revell six-stage costs a quarter, because the standardisation boundary needs account rollup and buyer-side interviews almost nobody already has.

Note where the cheapest option lands: the unsourced default costs near-zero and still ranks last on efficiency, because it buys no comparability with the field's vocabulary or with any other team's funnel - cheap and efficient are not the same ordering.

The efficiency order starves Revell six-stage, the only model with an explicit standardisation stage. Promote it anyway when the funded question _is_ why teams adopt but the organisation never standardises, or when a renewal depends on becoming an org-wide default - then the account rollup it forces is the point, not the cost.

Treat both lines as a default, not a law; they move with what a given team already instruments. Re-rank against that:

- an existing company-wide AARRR funnel collapses AAARRRP's coordination cost and promotes it to first
- account rollup already built for sales removes most of Revell's cost
- a product with no telemetry before signup demotes the API arc, since its early boundaries are exactly the unobservable ones

Offer **two or three candidate stage models** drawn from [references/stage-models.md](./references/stage-models.md), in efficiency order, each with what it makes visible, what it hides, and what its boundaries will cost you to observe. Recommend one and say why. Let the user choose before any row gets written.

Guidance that decides the rest:

- Prefer five to seven stages - this skill's default band, not a standard. Fewer hides the leak inside a stage; more produces stages nobody can name an exit event for.
- Split a stage only when it has two distinct exit events with different owners - "evaluation" splits cleanly when reading docs and running a local trial are owned by different teams.
- Keep the model's published stage names when you use a published model, so the map stays comparable with the field's vocabulary and with the program strategy that pins goals to it.

## Step 2 - Collect evidence before filling any row

A map assembled from opinion documents the team's beliefs, not the developer's path. Gather evidence first, cheapest source first, and tag each finding with the stage it belongs to.

1. **Walk the path yourself** and keep a friction log (Google's DevRel practice; protocol in the reference below): one realistic scenario, a running record of what you searched, clicked, pasted and felt, with green/yellow/red marks. It is the only source that catches drop-offs nobody ever reports.
2. **Mine what developers already wrote** - support tickets, issues, community questions, docs searches that returned nothing. Cluster them by stage; the biggest cluster is a friction candidate, not yet a conclusion.
3. **Interview five to eight developers who completed the journey**, and - harder to recruit, worth more - three who abandoned it. Both counts are this skill's defaults; the 5-8 matches common usability-panel sizes, not a journey-mapping standard.
4. **Read the funnel data that already exists** before asking for new instrumentation.

Check what each surface can physically report before promising a signal. Three corrections move a developer map's numbers more than anything else:

- **Analytics blocking.** Plausible measured 58% of a tech audience blocking a third-party analytics script (82.3% on Linux, 88.3% on Firefox), in an August 2021 measurement on one site carrying Hacker News and Reddit traffic, read against Plausible's own proxied script. That makes it a single-site measurement by an interested vendor, but the only public one. Absolute traffic numbers on developer surfaces are therefore wrong by a factor that varies page by page; only ratios inside one source survive.
- **Retention windows.** Repository traffic endpoints keep 14 days, npm downloads 18 months, PyPI series 180 days (GitHub REST Metrics/Traffic and pypistats docs). Snapshot any signal drawn from them from the day it is defined; expired data cannot be backfilled.
- **Referrer loss.** Aggregators, chat clients, privacy browsers, and AI assistants strip referrers - roughly 70% of AI-assistant traffic arrives with none, a newsletter estimate (Demand Curve #331), not a study. A large "direct" bucket is the normal case, not an instrumentation bug.

[references/evidence-and-signals.md](./references/evidence-and-signals.md) lists what to look for per stage, the candidate signals, which team usually owns each surface, the friction-log and exit-interview protocols, and the full per-surface instrumentation reality.

## Step 3 - Fill one row per stage

Each row carries eight fields. The three in bold are what separate this from a generic journey map; a row missing any of them is not finished.

| Field             | What goes in it                                                                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage             | the name from the chosen model                                                                                                               |
| Developer's job   | what the person is trying to accomplish, in their words, not the vendor's funnel language                                                    |
| Entry trigger     | the observable event that starts the stage                                                                                                   |
| **Exit event**    | the single observable event proving they moved on - first successful API call, first deploy to production, first merged PR, first talk given |
| Touchpoints       | the surfaces involved: docs page, repo, CLI output, dashboard, community thread, support ticket                                              |
| **Owner**         | one person or team accountable for this stage's exit rate                                                                                    |
| Friction evidence | a cited observation with its source, never a hypothesis; write "no evidence yet" when there is none                                          |
| **Signal**        | one metric with its data source and its current value, or `not instrumented`                                                                 |

Keep out two columns generic journey maps carry:

- Emotion scores get invented at developer volumes and crowd out the accountable columns.
- Opportunity lists written in the same pass turn the map into a backlog before anyone knows which stage leaks.

Mark every stage whose numbers are inferred rather than measured - with the blocking and referrer loss from step 2, the early stages almost always are. An honest `inferred` label protects the map's later conclusions; a confident fake number destroys them.

## Step 4 - Add the buyer lane, or say there isn't one

- **B2B, developer is not the buyer.** Add a second, shorter lane for the economic buyer - security review, legal and licensing, procurement, budget approval - joining at commitment or standardisation. It gets its own exit events (security questionnaire cleared, contract signed) and its own owner, usually outside DevRel entirely. The developer's lane continues in parallel: a champion who cannot arm an approver stalls at a stage the developer lane cannot show.
- **Roll usage up to accounts before reading this lane.** The developer lane counts people; the buyer lane counts organisations. Group signups by email domain, workspace or licence first - forty signups from one company look like forty leads until you do.
- **Read three signal families, in increasing order of buying intent:**
  - **Depth** - production use, sustained volume, wired into CI.
  - **Spread** - a second and third developer in the same account.
  - **Boundary contact** - someone opened an SSO or RBAC page, asked a compliance question, hit a seat limit, requested a security questionnaire.

  Boundary contact is rarest, strongest, and the cleanest exit event the lane can have - instrument it first.

- **Individual adoption or B2C-style self-serve.** The two lanes collapse; the developer decides and pays, or nothing is paid at all. State this explicitly on the map rather than leaving an empty buyer lane, so a later reader knows it was decided, not forgotten.
- **Open source with no purchase.** There is no buyer lane, but there is often an adoption-approval step inside the user's own company (license compatibility, dependency policy). Model it as friction in the adoption stage, not as a lane.

Everything else in the map works the same for both - the stage model, evidence gathering, exit events and leak diagnosis do not change with the business model.

## Step 5 - Name the three critical moments

Pull these out of the rows and state them separately; they are what the map gets read for.

- **First success** - the moment the developer gets a real result from the product. Name it concretely and note how long it takes today.
- **Moment of truth** - the point where they commit or walk: the decision to put it in a real project, to recommend it, to open a PR.
- **Abandonment point** - where the evidence says most people actually stop, which is often earlier and duller than the team assumes.

## Step 6 - Diagnose the leak

- Compute stage-to-stage conversion only where both exit events are counted. Leave the rest labelled `inferred`.
- Pick **one** stage to work on: the earliest stage that both converts poorly and has an owner able to change it. Earliest wins because every downstream fix is diluted by the losses above it; owned wins because an unowned recommendation is a wish. Rank the candidates by developers recovered per unit of fix effort - a docs fix and a re-architected onboarding do not cost the same week - and only then apply earliest-and-owned as the tiebreak.
- Say what that ordering starves. A late stage with a huge payoff and a heavy fix - standardisation, advocacy, contribution - never wins a round against an early cheap one, so a team re-running this map every quarter can spend years never touching it. Promote it when the earliest leaking stage is unowned, when its fix is already in flight, or when the end state from the interview _is_ that late stage.
- Below roughly 30 events in a period, publish the raw list with dates instead of a rate - a statistical convention, not a DevRel finding, and later journey stages hit that floor constantly.
- Compare only against this map's own previous version. Another company's published funnel has a different audience, product maturity and definition of every stage.
- If most rows name DevRel as owner, report that as a finding about the organisation. It means the surfaces have no accountable owner, which is a bigger problem than the leak.

Only after the stage is chosen, say _why_ it leaks, using BJ Fogg's behaviour model (**B = MAP**: a behaviour happens when motivation, ability and a prompt converge). B=MAP explains one stage; it cannot rank stages against each other.

Reach for it before choosing and you will write a fluent motivation story about a stage that was never the binding constraint. A leaking stage is a behaviour that is not happening, and the model splits the cause three ways, each landing on a different owner:

- **Ability too low** - the step is too long, needs an undeclared prerequisite, or asks for an unfamiliar routine. Fixed by docs, developer experience or product. This is the default answer for a developer audience, and Fogg's own directional advice applies: raise ability rather than pump motivation, because, in his words, "motivation is unreliable. Luckily, ability is not."
- **Motivation too low** - nothing at this stage showed a reason worth the effort. Fixed by positioning and product marketing. A motivation-first fix on a developer stage usually means the team preferred writing copy to removing steps.
- **Prompt missing** - they could and would have continued, and nothing told them to. Fixed by in-app guidance, lifecycle content or community.

## Step 7 - Write the map and validate it section by section

```markdown
# Developer journey map - <segment>, <date>

## Scope segment, end state, stage model used and why

## Journey the stage table (one row per stage, eight fields)

## Buyer lane the buyer's stages, or an explicit "none - self-serve"

## Moments first success, moment of truth, abandonment point

## Leak the chosen stage, its evidence, why it beat the others

## Handoff who owns the fix, the signal to watch, the re-read date

## Gaps stages marked inferred, and what would make them measurable
```

Present one section at a time and get agreement before writing the next. A wrong stage model caught at the first heading costs a paragraph; caught at the leak diagnosis it costs the whole document.

A worked map with weak and strong versions of the same rows is in [references/journey-map-example.md](./references/journey-map-example.md).

## Quality gate

Hold the map to this threshold and iterate until it passes, then report the check explicitly. These are this skill's own baselines, not an industry standard. Say so if a user asks where a number comes from, and let them move one when their situation argues for it.

- Every stage has exactly one exit event, phrased as an observable event rather than a state of mind.
- Every stage names one owner, and at least one owner sits outside the DevRel team.
- At least 60% of stages carry a signal with a real current value; the rest say `not instrumented` and appear in the Gaps section.
- Every friction claim cites its source; no row mixes evidence with hypothesis.
- Exactly one leak is nominated, with a named owner and a re-read date.
- Inferred stages are labelled as inferred, everywhere they appear.
- The map fits on one page at readable size - if it does not, the stage list is too long or the cells are carrying prose.

A map failing the signal line is not blocked. Ship it with the gaps named; an honest map with holes beats a complete map with invented numbers, and the gaps become the instrumentation request.

## Common failure modes

- **Mapping the funnel the company wishes for.** Stage names taken from the sales pipeline describe internal process, not developer behaviour. Test each stage name against "would a developer recognise this as something they did?".
- **One map for all developers.** A hobbyist, a platform engineer and an enterprise architect share almost no friction. Pick a segment or produce nothing.
- **Exit events that are not events.** "Understands the value proposition" cannot be observed, counted or owned. "Ran the quickstart to completion" can.
- **Filling the whole map from analytics.** Analytics starts after signup, which is already mid-journey. Everything before it needs qualitative evidence or an honest `inferred`.
- **Assuming silence means satisfaction.** Developers who fail at setup rarely file anything; they leave. Absence of complaints about a stage is not evidence the stage works.
- **Nominating three leaks.** Three priorities is none. Rank them and fix the earliest owned one.
- **Skipping the buyer lane in B2B.** The map then shows a healthy developer journey next to a stalled pipeline and explains neither.
- **Treating the map as permanent.** Re-read it when a launch, a pricing change, a docs rewrite or a new SDK moves a surface. A map older than two quarters describes a product that no longer exists.
- **Borrowing another company's conversion rates.** The numbers in circulation are single-company anecdotes with incompatible stage definitions. Quoting one gives the map false confidence and hides the only comparison that means anything - against its own last version.
- **Writing absolute traffic numbers into early stages.** The blocking rates from step 2 make any session count a fraction that varies page by page. Keep ratios inside one source, and label the stage inferred.

## References

- [references/stage-models.md](./references/stage-models.md) - the published stage models, their sources, and how to pick one.
- [references/evidence-and-signals.md](./references/evidence-and-signals.md) - evidence sources, candidate signals and typical owner per stage, the buyer-lane signal families, the per-surface instrumentation reality, and the friction-log and exit-interview protocols.
- [references/published-findings.md](./references/published-findings.md) - which claims are sourced, which numbers are this skill's own baselines, and the figures to refuse.
- [references/journey-map-example.md](./references/journey-map-example.md) - a full worked map with weak vs strong rows.
- samber/developer-relations-skills@developer-segmentation - chooses the segment a map is drawn for.
- samber/developer-relations-skills@devrel-metrics - turns the per-stage signals into a full measurement framework.
- samber/developer-relations-skills@devrel-analytics - instruments per-stage signals.
- samber/developer-relations-skills@devrel-strategy - pins program goals to the journey this map produces.
- samber/developer-relations-skills@developer-quickstart-guide - stage-level fix for first success.
- samber/developer-relations-skills@developer-docs-structure-audit - stage-level fix for evaluation and adoption friction.
