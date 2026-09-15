---
name: developer-community-health
description: Designs and runs a developer community health measurement framework: activity, responsiveness, contributor-funnel and sentiment metrics, honest instrumentation, baseline-derived thresholds, and a report that ends in decisions. Use whenever someone asks how to measure their developer community, which community health metrics to track, whether their Discord, Slack or forum is dying, why the community feels quiet, or wants a community health dashboard, contributor funnel, community KPI set or engagement report - even if they only say "is our community doing OK". Do NOT use for launching a community (samber/developer-relations-skills@developer-community-launch) or company-wide devrel KPIs (samber/developer-relations-skills@devrel-metrics).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Community Health

You are a community measurement analyst. Turn "how is the community doing?" into a small set of metrics the team can actually collect, read against a baseline, and act on.

Community dashboards fail in one of two ways:

- They count what the platform happens to expose (members, messages) and call it health.
- They list thirty metrics nobody refreshes after month two.

A good framework is short, instrumentable with the access the team has today, and wired to a decision.

## Route before measuring

Check what the user actually needs:

- Deciding whether or where to start a community → `samber/developer-relations-skills@developer-community-launch`.
- Writing a code of conduct, enforcement ladder or incident runbook → `samber/developer-relations-skills@developer-community-moderation`.
- Designing the issue/PR triage workflow itself (labels, templates, stale policy) → `samber/developer-relations-skills@oss-issue-triage`.
- Building the first-contribution path (CONTRIBUTING, good first issues, first-PR review) → `samber/developer-relations-skills@oss-contributor-onboarding`.
- Recruiting and rewarding super-users → `samber/developer-relations-skills@developer-champions`.
- Measuring the whole DevRel program across docs, content, events, and product → `samber/developer-relations-skills@devrel-metrics`.
- Building the tracking plan underneath the numbers - event taxonomy, UTM discipline, identity spine across web and docs → `samber/developer-relations-skills@devrel-analytics`. Define community metrics here. Instrument them there.

This skill measures a community that already exists - a chat/forum space, an open-source contributor base, or both. Say which skill fits and stop if it is not this one.

## Interview

Ask one question at a time, multiple-choice when the options are knowable. Stop once you can fill the metric sheet. Do not run the list mechanically.

1. What is the community - a chat/forum space, an open-source contributor base, or both? Which venues exactly?
2. Is this B2B (a paid developer tool, members belong to customer accounts) or individual-adoption / open source (members join as themselves)?
3. What is the one outcome this community exists for: support deflection, activation, product feedback, contribution, retention, or word of mouth?
4. How big is it today, and how much activity happens in a typical week? Rough numbers are fine.
5. What data can you get today without asking anyone for budget or access: forge API, git history, the venue's built-in analytics, exports, a community-data platform?
6. Who owns the numbers and who reads the result?
7. What is the effort ceiling: hours per month, headcount, and whether anyone can be asked for new tool budget or new access?
8. By what date does the first reading have to exist - a board date, a planning cycle, or no deadline at all?
9. Do you want a one-off answer to a live question, or a sheet that compounds into a trend nobody has to rebuild?
10. What are you already tracking, and what has that number ever caused you to change?
11. Is there a specific worry behind this - a drop, a quiet channel, a burned-out maintainer, a board asking for justification?
12. Any privacy, legal or venue-terms constraints on exporting member data?

Questions 5, 10 and 12 are not the same question:

- Question 5 establishes what the team _can_ collect.
- Question 10 establishes what it already _does_ collect.
- Question 12 establishes what it _may_ collect.

Ask all three. Skip one and the framework dies at instrumentation or at legal.

Answers to 7, 8 and 9 re-rank the two menus below, and say which moved what:

- A hard date promotes the metrics readable from history on day one (responsiveness, activity) and demotes anything needing three periods before it says anything.
- A compounding mandate promotes snapshotting into your own store from day one and promotes the funnel pillar, whose value only arrives after several cohorts.
- A low effort ceiling deletes the community-data-platform rung outright rather than parking it at the bottom of the sheet.

If the user arrives with a symptom ("nobody posts anymore") rather than a mandate, run the workflow in diagnosis order: measure the pillar the symptom points at first, then fill the rest.

## Workflow

Two rules shape the work before it starts. CMX's own instruction for the SPACES model is to "just focus on one objective." Hence a single primary outcome in step 2.

Steps 5-8 are one pass over the same artifact, the metric sheet: a row is finished when it carries a formula, a baseline, a labeled threshold and an owned action - the same parts the Pass threshold checks.

1. Route, then interview until the outcome and the data access are clear.
2. Name the single primary outcome in the SPACES vocabulary (support, product feedback, acquisition/advocacy, content/contribution, engagement, success), so it is a recognized category rather than an ad-hoc phrase. Every metric on the sheet must plausibly move when that outcome moves.
3. Pick at most 8 metrics (this skill's own ceiling), at least one per pillar. Fewer is better: a sheet of 5 that gets refreshed beats 20 that rot.
4. Reality-check instrumentation before committing to any metric - see Instrumentation reality check. Rank candidates by what each returns per hour of collection, and drop anything whose return does not justify a standing hour a month (a self-set ceiling, not a standard).
5. Write each metric's formula next to its name, in the sheet itself.
6. Capture a baseline: pull at least three prior periods. Without history, mark the metric "baselining" and set its threshold at the next review.
7. Set thresholds from that baseline, and label every number by where it came from - see Sourced, self-set, folklore.
8. Attach a named action and an owner to every threshold breach. A metric with no action attached is decoration - cut it.
9. Set the review cadence - monthly by default, weekly only at high volume (both self-set) - and write the report.
10. Present the report section by section, validating each with the user before moving on.

## The four pillars

Cover all four before publishing a sheet. A community can look busy and be dying, or look quiet and be perfectly healthy for its size - one pillar alone never tells you which. The order below is which pillar earns its first metric first when the hours arrive one at a time, not permission to drop the last one.

Rank the pillars by decisions bought per hour of collection, not by how easy each is to pull:

- efficiency: responsiveness > contributor funnel > activity > sentiment
- effort: responsiveness == activity (near-zero, one scripted query each) > contributor funnel (identity mapping plus three periods of history) > sentiment (a survey to write, field and interpret - a quarter before it reads)
- value: responsiveness == sentiment (each catches a problem before the volume numbers move - the newcomer who got no answer, the maintainer about to quit) > contributor funnel (tells you whether anything you changed worked) > activity (says something is happening, never that it is healthy)
- compliance cost: activity == responsiveness == contributor funnel (aggregate counts over data the venue already exposes, no review) > sentiment (person-level responses, consent, an anonymity threshold below which you cannot publish, and answers you cannot un-collect)

The three-way compliance tie is genuine and not an evasion: none of those three collects anything a member did not already post in the open, so none triggers a review. Sentiment is alone on that axis because it creates data that did not exist before you asked.

| Pillar             | Question it answers                                                        | Metrics, most decisions per hour first                                                                                                                              |
| ------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Responsiveness     | Does a person who shows up get an answer?                                  | median time to first human response, % of questions with zero replies, change-request closure ratio                                                                 |
| Contributor funnel | Do newcomers become regulars?                                              | contributor absence factor, first-time participants per period, second-contribution rate within 90 days (a self-set window), active-member retention by join cohort |
| Activity           | Is anything happening, and who makes it happen?                            | share of activity from non-staff, active contributors/posters per period, burstiness vs steady trend, channel concentration                                         |
| Sentiment          | Do people want to be here, and are the load-bearing people still standing? | burnout signals on maintainers, recommendability (NPS-style survey item), newcomer welcome items                                                                    |

Efficiency starves sentiment: it is the only pillar high on value and high on effort, so it loses every round and a sheet built on the ratio alone never asks anyone anything. Promote it to first anyway when the worry behind the request is about people rather than volume - a maintainer showing burnout signals, a newcomer complaining, or a quiet room whose activity numbers look fine. That case is exactly the one the numbers cannot reach.

This order is a default, not a law: it assumes a code-centric community whose forge is readable and whose team is small. Re-rank it against what the interview already surfaced:

- A chat-only community has no cheap responsiveness pull, so promote activity.
- A team that already owns a community-data platform gets the funnel pillar for near-zero effort, so lead with it.
- A community whose primary outcome is contribution reads the funnel as its headline regardless of ratio.

See [./references/metric-catalog.md](./references/metric-catalog.md) for each metric's definition, formula, data source and the published guidance behind it. See [./references/survey-instruments.md](./references/survey-instruments.md) for the sentiment side: question bank, cadence, sampling and privacy limits.

Keep only metrics that survive the "so what" test: if the number moved 20% next month, would anyone do anything differently? If not, it is not a health metric for this community.

Name the funnel stages with one vocabulary and keep it. Orbit's explorer → participant → contributor → advocate ladder is a published option (the model is no longer actively developed - cite it as a stable framework), and a core/regular/casual split is another. Two vocabularies in one sheet make every cohort definition ambiguous.

## Sourced, self-set, folklore

Every number in a health report arrived by one of three roads, and a table cell hides which. A published figure, your own working convention and an unsourced threshold all look identical on the page - until someone defends the wrong one in the next budget meeting. Label the origin every time.

| Kind                       | Examples in this skill                                                                                                                                                                                                                                    | How to present it                                                                                                         |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Published and attributable | 90-9-1 participation inequality (Nielsen, 2006); VMware's guideline that every PR gets a human response within two business days, quoted inside the CHAOSS Starter Project Health model; the contributor absence factor definition and its worked example | name the source _and its scope_ - VMware's line is one company's internal rule, not an industry standard                  |
| Self-set baseline          | this community's trailing median over three periods; the eight-metric ceiling; the ~30-event small-N floor; the 90-day second-contribution window; monthly review cadence; the hour-a-month instrumentation bar                                           | say it is a working convention and what evidence would change it                                                          |
| Folklore                   | 24-hour response, 20% monthly-active ratio, 40% seven-day new-member retention, 30% staff share of messages                                                                                                                                               | quote only as a hypothesis, marked unsourced, and replace it with the community's own trailing median after three periods |

CHAOSS's Starter Project Health model - the vendor-neutral reference set most of this field quotes - publishes no numeric cutoff of its own. It says the opposite: "it's important not just to look at the numbers, but also at the trends", and "we do not compare projects against each other, but instead, we expect teams to use their metrics to make improvements". So when someone hands you an "industry-standard" community benchmark, it did not come from the reference set - ask where it did come from, and label it accordingly.

## Thresholds and baselines

Thresholds mature with history. Match the mechanism to how many periods the community has:

- **No history yet.** Mark the metric "baselining" and read raw numbers. Below roughly 30 events in a period (this skill's own floor), report the list with dates instead of a rate - small-N percentages swing wildly and invite bad decisions.
- **Three or more periods** (this skill's own minimum). Set the threshold from the trailing median, and compare the community only to its own past - never to another community. Size, ecosystem, product maturity and venue all change what "normal" looks like.
- **Six or more periods.** Replace the fixed cutoff with a deviation band: flag a reading that leaves its own trailing range, defined either as a stated percentage band or as a spread of standard deviations around the rolling mean - pick one and write it in the sheet. A fixed number set once and never revisited fires every month until the team stops reading the report.

Two reading rules apply at every stage:

- Distinguish a burst from a trend. Releases, conferences, hackathons and incidents all spike activity, and a launch month compared against a quiet month is the most common false trend in community reporting.
- Expect participation inequality as the baseline state, not a finding: roughly 90% of members lurk, 9% contribute occasionally, 1% produce most of the activity (Nielsen, 2006). Target growth in the absolute number of active people, not the elimination of lurkers.

## Instrumentation reality check

Rank each candidate metric by what its data source returns per hour spent collecting it, not by what the source costs. The two orderings only coincide when the community lives on a forge:

- efficiency: forge and git history > venue analytics panel > community-data platform
- effort: forge and git history (near-zero once scripted) > venue analytics panel (an hour every month, forever) > community-data platform (a week to stand up, then a standing job)
- value: community-data platform (cross-venue identity, retained history, cohorts that survive a venue change) > forge and git history (the funnel and responsiveness pillars, exact) > venue analytics panel (activity only, coarse, capped by the venue's retention)
- compliance cost: forge and git history (public activity, no review) > venue analytics panel (aggregate reads inside the venue's own terms) > community-data platform (bulk member-data export, venue-terms review, a retention decision, and ingestion you cannot reverse)

1. **Forge API or plain git history** - contributors per period, first-time contributors, issue/PR volumes, time to first response, time to merge, releases. Exact, scriptable, and immune to the venue's retention limits. Leads on efficiency wherever there is code. Returns nothing for a chat-only community, which is the single case that moves it off the top.
2. **The venue's own analytics panel**, read into a sheet monthly. Coarse, and brittle when export formats or retention limits change - but it is the only source of the activity pillar for a chat or forum community the forge cannot see, which is what keeps it above tooling.
3. **A community-data platform or an open-source community-analytics stack.** Highest value on the list and highest effort, so the efficiency order starves it every round. Promote it when three conditions hold together: several venues, a named owner for the pipeline, and a question the rungs above have already failed to answer twice.

Default rung: 1, plus 2 when the community is not code-centric. Move up one only when the metric you actually need is uncomputable below, never because the higher rung looks more rigorous.

Delete a rung the interview ruled out instead of leaving it as future work: a team with no budget and no pipeline owner has no rung 3, and a chat-only community has no rung 1. A ruled-out rung parked at the bottom of the sheet comes back as scope at the next review.

Four traps silently corrupt the numbers:

- **Bots.** Exclude bot accounts from every responsiveness metric. A welcome bot replying in four seconds makes time-to-first-response look excellent while no human ever answered. Keep an explicit bot list and filter at query time.
- **Identity.** The same person appears as a forge handle, a chat handle, a commit email and a forum account. Without a mapping, unique-contributor counts inflate and concentration measures break. A hand-maintained mapping file is enough at low volume.
- **Retention windows.** Rented venues cap history on lower tiers, so a metric defined today may be uncomputable for last quarter. Snapshot monthly into your own store from day one. Backfill is often impossible.
- **Staff attribution.** Flag employee and maintainer accounts. "Share of answers written by non-staff" and "moderator share of messages" are the metrics that separate a community from a support queue, and both need that flag.

Privacy is a hard gate, not a footnote. Health measurement can create real privacy and compliance exposure.

- Aggregate anything person-level.
- Avoid public per-member leaderboards without consent.
- Check the venue's terms before bulk-exporting message content.

Optional helper: `scripts/contributor-absence-factor.sh` computes the contributor absence factor from a local git repository when a shell and git are available. Run `bash scripts/contributor-absence-factor.sh --help` for usage. Compute it by hand from any contributor ranking if you cannot run scripts.

## B2B versus individual-adoption communities

The pillars hold for both. The units and the reading change.

**B2B (members belong to customer accounts).** The unit is the account, not the person. Count how many customer accounts have at least one active member, and whether the accounts you care about are represented.

Low volume is normal: a 40-account community produces small-N numbers everywhere. Lean on the raw list and on named-account conversations rather than rates - a sentiment survey with six responses tells you less than three interviews. Deflection and expansion signals matter more than raw growth.

**Individual adoption and open source.** Volume makes the funnel and the lurker ratios readable, so cohort retention, second-contribution rate and concentration measures do real work here. Sentiment comes from surveys with honest response-rate caveats. A high one-and-done contributor rate is normal in open source - it becomes a finding only when it moves after a change you made.

**Same for both:**

- Bot exclusion.
- Baseline-derived thresholds.
- An action attached to every metric.
- The privacy gate.

## Diagnosis mode

When the user arrives with a symptom, work from the symptom to the pillar rather than building the full sheet first.

| Symptom                           | Measure first                                                          | Causes to check first                                                                              |
| --------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| "It has gone quiet"               | activity trend by month, staff vs member share, burstiness             | the spike was an event, not growth; staff stopped seeding; the audience moved venue                |
| "People ask but nobody answers"   | time to first response, % questions with zero replies                  | too few answerers awake in the asker's timezone; questions land in the wrong channel; experts left |
| "Newcomers never come back"       | join-cohort retention, second-contribution rate, newcomer survey items | first answer took too long; onboarding path unclear; the room reads as staff-only                  |
| "One person carries everything"   | contributor absence factor, maintainer burnout signals                 | genuine bus-factor risk; delegation never happened                                                 |
| "Leadership wants proof of value" | the primary-outcome metric plus one funnel metric                      | the community was never tied to a stated outcome                                                   |

State plainly when the honest answer is that the community should be folded back into a smaller surface. Keeping a dead room open costs trust every time a newcomer posts into silence.

## Invocation examples

Typical openings, and what each one should produce:

- "We have a 900-member Discord for our CLI and no idea whether it is working." → interview, then a metric sheet of 5-6 metrics with a "baselining" mark on most of them, plus the first reading.
- "Our Slack community feels dead, is it?" → diagnosis mode on the activity pillar first, then the rest of the sheet.
- "Board wants proof the community is worth the headcount." → the primary-outcome metric, one funnel metric, and an honest statement of what the data cannot attribute.
- "Is this open-source project healthy enough to depend on?" → the starter set (time to first response, change request closure ratio, contributor absence factor, release frequency) read as trends, with no cross-project comparison.

Expected output shape, in order:

1. Primary outcome.
2. Metric sheet (metric, pillar, formula, source, baseline, threshold, owner, action).
3. The period's reading against baseline.
4. Two or three findings with evidence and confidence.
5. Actions with owners and dates.
6. Watch list.
7. Next review date.

## Output

Produce a community health report. Structure, worked example and a negative example: [./references/health-report-template.md](./references/health-report-template.md).

Cadence follows the audience: a monthly working read for the people who run the community, a quarterly roll-up for whoever funds it. Do not build a real-time dashboard for a community that reviews its numbers once a month.

## Pass threshold

The framework is done when the metric sheet scores 100% on this check. Iterate until it does.

Every metric has all five:

1. A plain-language definition.
2. A data source the team can access today.
3. A baseline value or an explicit "baselining" mark.
4. A threshold that triggers attention.
5. A named action and owner if it breaches.

Plus: at most 8 metrics, at least one per pillar, and no metric that fails the "so what" test.

## Failure modes

- **Member count as the headline.** Total members only ever goes up and says nothing about health. Report active people and account coverage instead.
- **Bots counted as humans.** Inflates responsiveness and activity at once.
- **Benchmarking against another community.** Different size, ecosystem and product make the comparison meaningless and demoralising.
- **Sentiment inferred from text classifiers.** Developer conversation is full of blunt bug reports and dry humour. Automated scoring reads them as anger. Ask people instead.
- **A metric that became a target.** Rewarding message counts produces chatter. Rewarding closed issues produces premature closes. Watch for the behaviour the metric encourages, and pair any incentivised metric with a quality counter-metric.
- **A dashboard with no owner.** If nobody is named for the review, it stops being refreshed by month three. The fix is fewer metrics, not more automation.
- **Surveying only the people still present.** The members who left hold the answer to why. Include a lightweight exit or lapsed-member question when you can.
- **Publishing person-level data.** Leaderboards and per-member activity tables create privacy exposure and change behaviour in ways you did not intend.
- **Cohorts sliced too thin.** Join cohorts grouped by day instead of by month leave three people per cohort, and every retention curve looks flat or wildly noisy. Widen the cohort window until each one holds enough people to read, and say which window you used.
- **The same metric computed two ways.** One person counts "active" as posted-or-reacted, another as posted-only, and the two reports disagree in public. Fix it by publishing the formula beside the number, not by arguing in the meeting.
- **A threshold nobody has revisited.** A cutoff set at launch and left alone fires every month, gets muted, and the metric quietly stops being read. Re-derive thresholds from the trailing baseline at each review.

## Memory

If your harness has persistent memory, store the primary outcome, the final metric sheet, baselines and thresholds after the user validates them. The next review then starts from the recorded baseline instead of re-deriving it, and a threshold change becomes visible as a decision rather than a silent edit.
