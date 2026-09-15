---
name: oss-contributor-onboarding
description: Designs and verifies the path a stranger walks to their first merged contribution on an open-source project - the CONTRIBUTING file, the good-first-issue queue, a clone-to-passing-tests command that works cold, and the first-pull-request review and recognition loop, scored against a blocking-plus-weighted rubric. Use whenever someone says "nobody contributes to my project", "write a CONTRIBUTING.md", "our good first issues get no takers", "first-time contributors disappear", "contributor onboarding", "first pull request experience", or "how do we get more open-source contributors" - even if they only complain about a lonely repo. Not triage-system design - use samber/developer-relations-skills@oss-issue-triage. Not governance or CLA choice.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Contributor Onboarding

You are fixing the path between a stranger who wants to help and a merged pull request with their name on it. Projects lose people at every step of that path:

- land
- find work
- set up
- change
- submit
- survive review
- return

Find the step that leaks, fix it, and prove the fix by walking the path from a clean machine.

Diagnose against a published taxonomy, not intuition. Steinmacher et al.'s systematic review of newcomer barriers (Information and Software Technology 59, 2015, a review over 20 primary studies, not a measurement of any one project) sorts every recorded failure into five categories:

- social interaction
- the newcomer's prior knowledge
- finding a way to start
- documentation
- technical hurdles

Name the category behind each finding: it stops the audit from becoming a list of wording complaints.

Two failures dominate, and both are invisible from inside the project:

- A setup that breaks on a machine the maintainer never tested produces no issue, no message, and no trace.
- Silence on a submitted pull request produces the same nothing.

GitHub's Open Source Guides report that contributors reviewed within 48 hours return at a much higher rate (practitioner guidance, with no published dataset behind the figure), and that "it only takes one negative experience to make someone not want to come back". Optimize for those two failures before touching any wording.

Stay inside the first-contribution path. Seven sibling skills own the neighbouring problems, routed one per line in the Reference section; when the user's real problem is one of them, say so and route them.

## Invocation and output

Typical invocations, and what each one should produce:

| The user says                                                   | You run                      | You return                                                                                                             |
| --------------------------------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| "audit why first-time contributors give up"                     | Steps 1-2, then score        | The audit report in [./references/contributor-path-scorecard.md](./references/contributor-path-scorecard.md) section 5 |
| "write a CONTRIBUTING.md for this repo"                         | Steps 1-3, then 5            | A drafted file, plus the cold-run log that proves each command in it                                                   |
| "our good first issues sit untouched for months"                | Step 1 baseline, then step 4 | A rewritten queue, a claiming convention, an expiry rule                                                               |
| "someone opened their first PR and I do not know what to reply" | Step 6 only                  | A reply drafted from the templates, plus the two-clock rule for the next one                                           |
| "we get stars but no pull requests"                             | Full workflow                | Scorecard first - this phrasing usually means step 3 or step 6, not the wording of any file                            |

Attach evidence to every deliverable:

- a file path and line
- a command output
- a counted number with its date

A recommendation with no evidence attached is an opinion, and a maintainer will discount it correctly.

## Interview

Ask one question at a time, multiple-choice where possible, and skip anything you can answer yourself by reading the repository. Questions 1-7 gate the work - do not draft any file before they are answered.

1. Which repository, and can I read it and run commands inside it?
2. What do you actually want more of: code contributions, documentation and translation help, triage and support help, or co-maintainers who can share the load?
3. Is this a volunteer or solo-maintained project, or is it corporate-backed or foundation-hosted? The answer changes the response target, the legal gate, and the ladder you can promise - the split is tabled in [./references/contributing-file-outline.md](./references/contributing-file-outline.md) §3.
4. How many hours per week can you realistically spend on contributors, review included, in a normal week rather than a good one? An honest small number is more useful than an aspiration, and it is the ceiling every later recommendation is sized against.
5. By what date must this land - a release, a grant milestone, an event, or an open horizon?
6. Do you want one wave of contributions, or a path that keeps producing contributors after you stop pushing it?
7. What is out of scope - the contributions you decline however well written?
8. What happened the last three times an outsider tried to contribute? Merged, stalled, declined, vanished?
9. Is there a legal gate (DCO sign-off, CLA), and does the contributor learn about it before or after opening the pull request?
10. How long does a stranger's setup take today, and when did you last run it from a clean machine?
11. Does anything about your stack make setup unusually hard - a database, a paid API key, a GPU, a proprietary SDK?
12. Who besides you can review a pull request, and what happens to contributors while you are on holiday?

Record a blank on question 7 as the audit's first finding, not a blocker.

Carry questions 4, 5 and 6 into every ordering in this skill, and say which answer moved what:

- a near deadline (Q5) promotes the fixes that land in an afternoon, the response target, the issue queue, the first reply, over the environment tiers that need a rebuild
- a compounding mandate (Q6) promotes step 3, the only work that keeps paying after you stop
- hours per week under a day (Q4) delete the structured program in step 7 outright, whatever its appeal

## Step 1 - Baseline before changing anything

Measure first, so the work has a before and an after that are not both opinion.

1. Run `scripts/contributor-path-audit.sh <repo-root>`. It reports the community-health files and their display precedence, which of ten contributing topics the current file mentions, the setup surface, how many CI workflows use secrets and therefore cannot run on fork pull requests, and the git contributor history - distinct authors, one-commit-only rate, CHAOSS contributor absence factor, new authors per year.
2. Treat the script's content probe as a vocabulary check, not a coverage check - it greps for keywords, so "review expectations: mentioned" means a word matched, not that the topic is handled. Read the file before repeating any probe result to the maintainer.
3. Collect from the forge's own interface or API what the script cannot see: the funnel-baseline figures listed in the scorecard's report format, plus the current stock of unclaimed beginner-friendly issues and their age. Use a 90-day window for response times and four quarters for contributor counts - both windows are this skill's own defaults, not published standards.
4. Read the last ten pull requests from people who are not maintainers, oldest comment first. Note where each one stalled and what the first maintainer reply said, if there was one.
5. If your environment has persistent memory, load any stored scope statement, response target, or audience definition for this project rather than re-deriving it.

The script reports facts, not judgements. Treat the one-commit-only rate as a baseline, not a defect: it becomes a finding only when it fails to move after the path is fixed.

Score the current path with [./references/contributor-path-scorecard.md](./references/contributor-path-scorecard.md) and show the maintainer the result before proposing changes. A maintainer who disagrees with the diagnosis will reject the treatment, and they are sometimes right - a constraint you cannot see from the repository can justify a check you scored zero.

## Step 2 - Walk the path yourself

Follow the cold-run protocol in [./references/contributor-path-scorecard.md](./references/contributor-path-scorecard.md) §3, both runs - the environment path and the task path - and obey its rule that a setup is never marked working by inspection.

Keep a friction log while you run: a timestamped record of every moment of confusion, with a traffic-light severity per entry. Note, for each entry:

- what you expected
- what happened
- what you had to know that was not written down

Do not fix anything mid-run. Fixing hides the size of the problem.

## Step 3 - Fix the environment before the prose

Documentation describing a broken setup is worse than no documentation, so this step comes before any writing. Pick a reproducibility tier first, then close the gaps the cold run exposed.

Three tiers, ranked by setup failures removed per unit of maintenance the tier then costs you forever. The cold run picks between them: take the highest-efficiency tier that removes the failures it actually found, and stop there.

- efficiency: `bootstrap command > pinned toolchain > container definition`
- value (failures removed): `container definition > pinned toolchain > bootstrap command`
- effort: `container definition > pinned toolchain > bootstrap command`

1. **Bootstrap command** - one `make setup` or `./script/bootstrap` that installs dependencies, prepares fixtures, and ends by running the test suite. An afternoon to write, works everywhere, still trusts the host toolchain.
2. **Pinned toolchain** - a version file the host's tool manager reads, plus a committed lockfile. Removes most "works on my machine" reports for the cost of one file and the upgrades it then forces.
3. **Container definition** - a development-container definition that both a local editor and a cloud workspace can consume. Strongest reproducibility and highest maintenance: a standing job, and the tier that rots fastest when maintainers do not use it themselves.

- What this order starves: the container definition, the only tier that removes a whole class of environment failure. Promote it when the stack needs services or a painful toolchain (interview question 11) - there the cheaper tiers remove nothing, and an ordering is never a reason to ship a fix that does not work.
- Re-rank against what you know: a team already running containers in CI has paid that tier's effort, which moves it to the top of the efficiency line for that project alone.

Adopt the container definition before adopting any hosted workspace vendor: the `.devcontainer/` format is portable across editors, cloud workspaces and self-hosted runners, while the hosting choice is not. Vendor-published time savings for these tools are marketing figures with no peer-reviewed measurement behind them; read [./references/published-findings.md](./references/published-findings.md) §6 for that caveat and the three constraints (who pays for compute, portability before hosting, drift) to raise before recommending one.

Then close the gaps, in this order:

- Make every gate CI enforces runnable locally with one documented command. A contributor who cannot reproduce a red check locally is stuck by definition.
- Split the pipeline into a credential-free lane that always runs on fork pull requests and a privileged lane a maintainer triggers. Jobs needing secrets cannot run on a fork, and they show red to exactly the people who need reassurance. Where an approval gate holds fork runs entirely, say in the file who approves it and how fast.
- Turn on maintainer edits to contributor branches, and say in the file that you do it, so a stalled pull request can be finished rather than closed.
- State the merge style (squash, rebase, merge commit), because it changes how contributors structure their commits.

Re-run the cold run from clean after each fix. The step is done when nothing new is discovered.

## Step 4 - Stock the first-issue queue

A beginner label is a promise of mentoring, not a difficulty rating. Kubernetes says so explicitly: their `good first issue` means members have committed to providing extra assistance, while `help wanted` is the broader "we would take a patch". GitHub also surfaces the label algorithmically and publishes no criteria for it, so the label pulls in strangers from outside the project entirely - an empty one-line issue behind it converts that attention into a bad first impression.

1. Stop fixing easy bugs yourself; each one is a recruiting opportunity spent on twenty minutes of your own time. Kent C. Dodds, whose 2015 post created the `first-timers-only` convention, states the trade: "Could I have finished it quicker and moved on my way if I'd just done it myself? Of course. But that's not what it's all about as an open source contributor." His diagnosis is the one this skill is built on - "the hard part of getting into open source for the first time isn't the implementation of a feature, but figuring out how to actually contribute code".
2. Write each candidate issue with the seven parts: observed behaviour, expected behaviour, the file and its test, the skills or APIs required, a suggested approach or an explicit "design not settled - discuss first", the exact verification command, and a named mentor. One 74-participant study (Steinmacher et al., arXiv:2103.12653) found newcomers picked issues labelled with the _technical domain required_ over issues labelled by architecture area - the question they ask is "can I already do this?", not "is this easy?".
3. Size each issue at roughly one evening for someone who has never seen the codebase, setup included - this skill's own sizing default. A one-word typo fix teaches nothing and produces a contributor who never returns.
4. Reserve non-code entry points explicitly - documentation, tests, triage, translation, examples. They are the widest door and the first thing an all-code queue loses.
5. Publish the claiming convention and a stale-claim expiry, then apply it. A queue that looks full but is entirely claimed by absent people is worse than an empty one.
6. Keep a standing stock of at least three valid unclaimed issues - a self-set floor. Someone who finds zero does not come back later to check.

See [./references/first-issue-and-review-examples.md](./references/first-issue-and-review-examples.md) for a weak and a strong issue body side by side.

## Step 5 - Write the CONTRIBUTING file

Draft section by section against [./references/contributing-file-outline.md](./references/contributing-file-outline.md), and get the maintainer's agreement on each section before moving to the next. A file rewritten in one pass gets rejected in one pass.

Hold four rules while drafting:

- Write only what is now true. Every command in the file must be one you ran in step 2 or 3.
- Publish the response target you can actually hold, from interview question 4. A stated seven days that is met beats a stated 48 hours that is missed.
- Put the legal gate before the reader writes code, never at the gate itself. Where the project still has the choice, a sign-off line (`git commit -s`) costs a contributor nothing, while a signing workflow stops a typo fix - which is why the CNCF encourages projects to use a DCO "as it's easier to setup and use". The choice itself belongs to samber/developer-relations-skills@oss-license-strategy; only its placement in the file is yours.
- Write for the agent reading it too: state conventions literally and near the top, write the commands out rather than only the wrapper, and keep every mandatory step inside the file rather than behind a link. The outline's §6 reads GitHub's own repo-contribution skill as the spec these three rules come from.

Place the file where the forge surfaces it and keep exactly one copy (outline §1), and link the neighbouring files instead of absorbing them (§4).

Run the finished prose through your preferred humanizer skill. A contributing guide that reads as generated undermines the welcome it extends, and this audience spots it immediately.

## Step 6 - Design the review and recognition loop

1. **Acknowledge on a separate clock from reviewing** - the two-clock rule. A same-day "thanks, I have seen this, review by Thursday" preserves the relationship when the real review is a week out. Silence is the expensive failure, not slowness.
2. **Answer scope in the first comment.** Discovering a pull request is out of scope after three review rounds is the worst outcome in the funnel for both people.
3. **Review in a fixed order:** scope, then correctness and tests, then design with the reasoning attached, then style - and only the style the formatter missed. Anything a machine can fix must never appear as a human review comment.
4. **Label blocking versus optional** on every comment. An unlabelled mix reads as a wall of failures.
5. **Decline fast and kindly** when you must: thank them, name the scope rule, link where it was published, offer an alternative issue, close. A quick no beats a pull request rotting for six months.
6. **Credit at merge**: preserve the contributor as author, name them in the release notes, and record non-code contributions somewhere the commit graph cannot - docs, triage, and design work are otherwise invisible.
7. **Invite the second contribution explicitly**, with a named next issue. This is the moment a drive-by becomes a contributor, and it almost never happens on its own.
8. **Write down what happens when a pull request stalls**, from both sides, and offer to finish it yourself rather than letting a bot close it.

Review against the written scope rule and that fixed order, never against an impression of the person - it is the cheapest available control on reviewer bias. Terrell et al. (PeerJ CS 3:e111, 2017) analysed 3,064,667 pull requests and found that on _outside_ contributions - exactly the population this path serves - women's merge rate was 58% against men's 61% where gender was identifiable, while gender-neutral profiles scored highest of all. Gender was inferred and only 35.3% of users were linkable, so treat the direction as robust and the exact percentages as not; caveats in [./references/published-findings.md](./references/published-findings.md) §5.

Turn items 1-8 into a short written playbook the maintainers actually share, and mirror the response target into the CONTRIBUTING file so contributors and maintainers read the same number. Reply templates for each situation are in [./references/first-issue-and-review-examples.md](./references/first-issue-and-review-examples.md).

## Step 7 - Decide against the shortcuts before spending on them

Maintainers reach for a mentorship program, an onboarding event or a bot when the real problem is one of the six steps above. Each is a legitimate accelerator on a working path and a waste on a broken one, so make the call explicitly rather than by enthusiasm.

Rank them only after steps 3-6 hold: on a broken path every one scores zero whatever the ordering says. Effort means maintainer hours committed and how hard the thing is to stop once announced. Value means contributors who return.

- efficiency: `bot > structured program > onboarding event`
- value: `structured program > bot > onboarding event`
- effort: `structured program > onboarding event > bot`
- compliance cost: `structured program > onboarding event > bot`

- **A bot** may absorb mechanical work, never a human moment. Leads the efficiency line on its denominator alone - an hour to install, near-zero afterwards, and reversible in one commit. Keep the first reply, the decline and the stall check-in human (step 6), and treat any wait-state a bot or approval gate introduces as a step 3 gap to document.
- **A structured program** (Google Summer of Code, Outreachy, LFX Mentorship, MLH, Season of Docs) supplies the stipend and the cohort; you supply mentor hours - a standing job for a whole season, and the only item here you cannot abandon halfway without someone's summer attached to it. Host one only once steps 3 to 6 hold, because an under-mentored intern costs more than no intern. Do not promise it fixes retention: the two most-cited studies disagree, and the Mozilla analysis (Labuschagne & Holmes, MSR 2015) found contributors who started on a good-first-bug or mentored bug were _less_ likely to become long-term contributors. Figures and caveats are in [./references/published-findings.md](./references/published-findings.md) §3-4.
- **An onboarding event or sprint** teaches mechanics well and converts nobody on its own. Last on efficiency because it costs a week of preparation plus the follow-up and buys the least measured return of the three. Kubernetes ran the field's most resourced workshop and retired it because "running the session during the summit never led to any people who weren't already contributing to the project becoming dedicated contributors". Budget the follow-up - a named next issue, an assigned mentor, a second-contribution nudge - or skip the event.

- Delete **a reward with no quality gate** rather than ranking it last, and say you deleted it: it buys volume you cannot review, which is a cost, not a small benefit. Hacktoberfest's 2020 spam wave forced opt-in repositories, a longer grace period and the removal of the T-shirt entirely.
- What this order starves: the structured program - highest value of the three, and the only one that brings people who were never going to find the project alone. Promote it when a second reviewer exists (interview question 12) and the maintainer hours in question 4 clear a mentor's weekly commitment for a full season.
- Read the compliance line as the obligations each signs you up to:
  - a structured program: a third party's participation agreement, mentor commitments, stipend administration, and its code of conduct for a season
  - an event: a code of conduct and a venue
  - a bot: neither

  The deleted reward carries published prize rules - what Hacktoberfest had to rewrite mid-event.

- Treat this ordering as a default, not a law: it shifts with the project and with who maintains it. Re-rank against what you know - an employer already funding mentor time, a co-maintainer who has run a cohort, an existing event to attach a sprint to - each moves an item up before the default applies.

## Step 8 - Re-score, then hold the target

Re-run the scorecard and iterate until it clears its threshold - all four blocking checks, plus 12 of 16 scored points. That mark is this skill's own baseline, not a published one; §4 of the scorecard has the wording to give a maintainer who asks where it comes from.

Then hold it, because the path decays - a new dependency breaks the bootstrap, the beginner queue empties, the response target slips. Re-run the audit script and one cold run every quarter - this skill's own cadence - and after any change to the build or the test command. Where your environment supports scheduled routines, install that re-check as a recurring task; where it does not, leave the maintainer a dated calendar reminder and a one-line command to re-run.

If your environment has persistent memory, store the agreed scope statement, the published response target, the beginner-issue definition, and the score with its date, so the next run measures a delta instead of starting over.

## What to track afterwards

At low volume these signals are anecdotes with dates attached, not a dashboard. Four external pull requests a quarter cannot produce a trend, and a conference talk or a front-page mention moves every number below more than a documentation change does. Record the date you shipped each change, annotate the confounders, and only then read deltas.

Track the scorecard's funnel baseline, reading each number this way:

- **New external contributors per quarter** - the headline number, and the noisiest.
- **Second-contribution rate within 90 days** - the retention number the whole path exists to move; the window is this skill's own default.
- **Median time to first human response**, bots excluded, against the 48-hour reference point.
- **External first-pull-request merge rate and median time to merge**, tracked separately from maintainers' own pull requests, which are always faster and hide the number that matters.
- **Contributor absence factor** - it should rise slowly; it is the only one of these that measures whether the project got less fragile.
- **Setup support load** - issues and chat messages that are really "I could not build it". A fixed path drives this to near zero, and it is the fastest-visible win.

## Common failure modes

- **Labelling old bugs as beginner-friendly.** Small for someone who knows the codebase is not small for a stranger. If it has no location, no verification command, and no mentor, it is not a first issue.
- **Optimizing recruitment while review is the bottleneck.** More contributors arriving at an unstaffed review queue produces more abandoned pull requests and more resentment on both sides. Fix step 6 before promoting the project.
- **Quoting an outcome number as if it transfers.** "80% of interns keep contributing" is a self-reported figure from one program's alum survey with a 37% response rate. Measure the project's own funnel, time to first response, second-contribution rate, instead of importing someone else's result.
- **Copying a large project's process.** A ten-person project running Kubernetes' ladder, sponsors and rota spends its whole budget on process for contributors it does not have yet. Take the shape, not the scale.

## Reference

- [./references/contributor-path-scorecard.md](./references/contributor-path-scorecard.md) - rubric, cold-run protocol, pass threshold, and report format
- [./references/contributing-file-outline.md](./references/contributing-file-outline.md) - section-by-section outline, volunteer-versus-corporate split, agent legibility, compact skeleton
- [./references/first-issue-and-review-examples.md](./references/first-issue-and-review-examples.md) - weak and strong issue bodies, first reply, review comments, decline, merge message, stall check-in
- [./references/published-findings.md](./references/published-findings.md) - sources and caveats for every figure cited, plus self-set baselines
- [./scripts/contributor-path-audit.sh](./scripts/contributor-path-audit.sh) - mechanical facts the scorecard depends on
- samber/developer-relations-skills@readme-optimization - repository landing page
- samber/developer-relations-skills@developer-quickstart-guide - user's first success with product (not contributor path)
- samber/developer-relations-skills@oss-governance - decision rights and maintainer selection
- samber/developer-relations-skills@developer-community-moderation - code of conduct and enforcement
- samber/developer-relations-skills@oss-launch - attracting an audience
- samber/developer-relations-skills@developer-journey-map - the stage this contributor path feeds
