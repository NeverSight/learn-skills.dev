---
name: developer-relations-kickoff
description: Before starting any developer-relations work - and again at the start of each new session on an existing DevRel project - routes the current task to the right skill of the samber/developer-relations-skills collection, or says plainly that none fits, then bootstraps or resumes the project's shared devrel-context.md artifact. Covers documentation, open source, community, events, technical content, program strategy, devtools business strategy, employer brand and measurement; the output is a routing short-list plus an ordered skill chain. Run it at every project start even when the collection's skills are already in daily use elsewhere, at each periodic DevRel check-in, and whenever routing is unclear - a devrel kickoff, a new developer-relations project, "which devrel skill do I need", devrel, docs or open-source skill routing, or a recurring developer-program review - even if the user only describes a devrel problem and never asks which skill to use.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Relations Kickoff

You are the router for the 55-skill developer-relations-skills collection. Route the current DevRel task to exactly one sibling skill - or say plainly that none fits - and leave the next session warm instead of cold. Never perform a sibling's job yourself; everything else in this file serves the routing.

Run this skill at every project start, even when the collection's skills are already in daily use elsewhere - a new project is a new context. On later sessions of the same project, re-run it to resummarize and re-route, never to re-interview.

The collection serves two adoption motions: an individual developer who self-serves, and an organization where the developer is the user but someone else signs. Several sibling skills split their advice on that line, so carry the answer - self-serve, organization-buys, or both - through routing instead of collapsing it to one motion.

## 1. Detect before asking

Every fact derivable from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold vs warm start from one signal only: does `devrel-context.md` exist in the project? Present → warm. Absent → cold. Never ask the user which mode it is.
2. If you can read the repository's git history, infer stage and pace from the recent log: release frequency, whether docs and code move together, whether the project stalled.
3. Inventory what already exists - README, CONTRIBUTING, CODE_OF_CONDUCT, GOVERNANCE, LICENSE, CHANGELOG, `docs/`, `.github/` templates, agent-instruction files, a docs site config, past content plans - so nothing already written gets re-asked. Treat the absence of a file as a routing signal in its own right: a repository with no CONTRIBUTING file makes `samber/developer-relations-skills@oss-contributor-onboarding` a candidate before anyone asks for it.
4. If your harness exposes connectors or integrations, detect which are available - a code host, an analytics source, a docs build, a community platform export, a package registry - and let their presence shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships version metadata you can read, note what changed since the last session. If it doesn't - the common case - degrade silently. Never block, warn, or ask about versions.

## 2. Interview - capped

On a cold start, ask at most 5-7 questions, one per message, multiple-choice whenever possible. Spend questions only where detection came up empty - skip any question the file inventory or git log already answered.

1. "Which surface is today's work on?" - (a) documentation and developer experience, (b) an open-source project, (c) community, (d) events and speaking, (e) content and media, (f) program strategy or measurement, (g) company-level developer business strategy. This fork splits the collection into blocks and steers every later route, so it comes first.
2. "What is the goal of this session - is it the same as the project's goal, and what about it is already decided versus still open?" Ask on both cold and warm starts; a project goal never substitutes for today's goal, and a decided item comes off the short-list entirely rather than being ranked last.
3. "Who adopts, and who pays?" - (a) individual developers self-serving, (b) an organization where the developer evaluates and someone else buys, (c) both, (d) a non-commercial open-source project with no buyer.
4. "Which business driver funds this work?" - (a) developer adoption, (b) sales enablement, (c) developer enablement, (d) product input, (e) ecosystem and partnerships, (f) contributor community, (g) employer branding. The driver decides which pillar the work belongs to and what it will be judged on; a program claiming all seven has no strategy.
5. "What stage is the program at?" - (a) nothing formal yet, (b) one person doing it part-time, (c) a dedicated person or small team, (d) a multi-person team with its own budget.
6. "Any hard constraints right now - and is there a date the result has to land by?" - (a) no budget, (b) maintainer hours only, (c) no engineering support for docs, (d) legal or security review required, (e) no analytics access, (f) none. Give the date when there is one: a release, a conference, a funding review.
7. "Do you want a one-off win or a compounding asset out of this - what is your effort ceiling, and who signs off?" - (a) one-off, maintainer hours only, (b) one-off, a week of work is fine, (c) standing, a few hours every week from here, (d) standing, with engineering time and cross-team sign-off available. Name whoever holds sign-off; that answer fills the artifact's Stakeholders field.

Questions 6 and 7 exist to order the output, not to describe the project: the landing date, the one-off-versus-compounding answer, and the effort ceiling are what re-rank the short-list (§ 4) and the routines (§ 7). Ask them here, in the interview, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact so a warm start re-ranks both lists without re-asking them.

On a warm start, ask only the session-goal question. Everything else - including the date, the horizon and the effort ceiling that drive both rankings - comes from the artifact.

## 3. Route the task

Match the stated session goal against each skill's declared scope below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap instead of stretching the nearest skill.

These tables are deliberately unranked, and must stay that way - inside a block and between blocks alike. Scope is a match test, not a ratio: a task either falls inside a skill's declared scope or it does not, and ordering the rows would invent a preference between skills that never compete for the same task.

`changelog-writing` is not "better" than `oss-governance`; they are never candidates for the same session. Ranking belongs one step later, in the short-list (§ 4), where several skills genuinely do compete for the same hours.

**Program strategy and measurement:**

| Skill                                                            | Route here when the task is…                                                                                                                                        |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@devrel-strategy`              | Design the program from the top - situational analysis, funded driver, allowed goals, pillar mix, build-vs-buy, staffing sequence, refused list                     |
| `samber/developer-relations-skills@devrel-team-structure`        | Org design - reporting line, team shape, coverage map, interlocks, re-org triggers                                                                                  |
| `samber/developer-relations-skills@devrel-budget-allocation`     | Split the budget across pillars into line items with a return threshold and a cut list                                                                              |
| `samber/developer-relations-skills@devrel-metrics`               | Which KPIs deserve a target - tiered framework, attribution rule, baselines, vanity cuts                                                                            |
| `samber/developer-relations-skills@devrel-analytics`             | The tracking plan that instruments the surfaces - event taxonomy, identity spine, UTM discipline                                                                    |
| `samber/developer-relations-skills@developer-journey-map`        | Map the journey stage by stage - discover, try, adopt, contribute, advocate as a working spine, not a published framework - and locate the single leak worth fixing |
| `samber/developer-relations-skills@developer-segmentation`       | Cut the developer audience into named, sized, ranked segments plus an anti-segment                                                                                  |
| `samber/developer-relations-skills@developer-education-strategy` | Whether and how to invest in structured education - academy, curriculum, labs, certification                                                                        |
| `samber/developer-relations-skills@devrel-competitor-analysis`   | Benchmark a competitor's devrel motion from public signals into a close/ignore/counter plan                                                                         |
| `samber/developer-relations-skills@tech-employer-branding`       | Attract engineers to work here - engineering EVP, verification-surface audit, seniority-matched channel bets, hiring measurement baseline                           |

**Developer business strategy (company level):**

| Skill                                                            | Route here when the task is…                                                                                                                                                |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@devtools-business-model`      | How the tool makes money - nine model archetypes and the GTM each forces                                                                                                    |
| `samber/developer-relations-skills@devtools-pricing-strategy`    | Value metric, free-tier limits, tier ladder, price points, safe price changes                                                                                               |
| `samber/developer-relations-skills@developer-first-gtm`          | The adoption-to-revenue motion - self-serve entry, developer-to-buyer handoff, land and expand                                                                              |
| `samber/developer-relations-skills@open-source-company-strategy` | What the company open-sources and what stays proprietary, asset by asset, with the motive                                                                                   |
| `samber/developer-relations-skills@developer-ecosystem-strategy` | Whether and how far to open the product into a platform others build on                                                                                                     |
| `samber/developer-relations-skills@open-standards-strategy`      | How to engage a named standard or protocol - ignore, consume, certify, extend, contribute upstream, co-found a spec, drive your own - plus venue, patent mode and kill rule |

**Documentation and developer experience:**

| Skill                                                              | Route here when the task is…                                                                   |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@readme-optimization`            | One repository's README - first impression, bail-fast funnel, badge pruning                    |
| `samber/developer-relations-skills@developer-quickstart-guide`     | Zero to one verified success - minimal path, copy-paste commands, expected output              |
| `samber/developer-relations-skills@developer-tutorial`             | A teaching tutorial - one concept per step, checkpoints, a demonstrable skill at the end       |
| `samber/developer-relations-skills@developer-docs-structure-audit` | The docs set's information architecture - Diátaxis classification, misplacement, coverage gaps |
| `samber/developer-relations-skills@docs-code-sample-standards`     | Sample policy and a corpus audit - runnability, testing, language parity, copy-paste safety    |
| `samber/developer-relations-skills@developer-troubleshooting-docs` | Error-reference and troubleshooting pages built from tickets, issues and telemetry             |
| `samber/developer-relations-skills@changelog-writing`              | Release notes for one release, from commits and pull requests                                  |
| `samber/developer-relations-skills@version-migration-guide`        | The breaking-change migration guide - blast radius, detection signals, before/after, timeline  |
| `samber/developer-relations-skills@coding-agent-docs-optimization` | Make docs machine-readable so a coding agent can integrate unattended                          |

**Search demand for technical content:**

| Skill                                                          | Route here when the task is…                                                                      |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@developer-keyword-research` | What developers actually search - error strings, task queries, integration intents, demand sizing |
| `samber/developer-relations-skills@docs-seo`                   | On-page and technical SEO of a docs site - indexing, canonicals, templates, internal links        |

**Open source:**

| Skill                                                           | Route here when the task is…                                                                                                                         |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@oss-launch`                  | The launch window - readiness gate, positioning, channel sequencing, run of show                                                                     |
| `samber/developer-relations-skills@oss-distribution-strategy`   | Ongoing distribution after launch - registries, curated lists, packaging, release cadence                                                            |
| `samber/developer-relations-skills@build-in-public`             | The recurring transparency practice - disclosure ladder, cadence, platform mix, boundaries                                                           |
| `samber/developer-relations-skills@oss-contributor-onboarding`  | The stranger-to-first-merge path - CONTRIBUTING, good first issues, cold-runnable setup                                                              |
| `samber/developer-relations-skills@oss-issue-triage`            | The triage system - queue measurement, labels, response targets, intake forms, staleness policy                                                      |
| `samber/developer-relations-skills@oss-governance`              | Decision rights, maintainer roles, voting, conflict escalation, succession and bus-factor planning, trademark and asset control, foundation donation |
| `samber/developer-relations-skills@oss-license-strategy`        | License choice plus CLA/DCO, dual licensing, source-available options, relicensing risk                                                              |
| `samber/developer-relations-skills@github-profile-optimization` | A personal or organization profile on a code host - profile README, pins, contribution signals                                                       |
| `samber/developer-relations-skills@oss-sponsors-fundraising`    | Maintainer side - build a sponsorship program, tiers, rewards, the invoice path                                                                      |
| `samber/developer-relations-skills@oss-sponsors-brand-strategy` | Company side - which projects to fund, how much, and how to prove it worked                                                                          |

**Events and speaking:**

| Skill                                                           | Route here when the task is…                                                            |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@conference-cfp-submission`   | Turn a talk idea into a submission for one named event                                  |
| `samber/developer-relations-skills@tech-talk-outline`           | Turn an accepted abstract into a rehearsable outline and slide skeleton                 |
| `samber/developer-relations-skills@developer-live-demo-design`  | Make a demo survive the stage - fidelity tier, checkpoints, fallbacks, runbook          |
| `samber/developer-relations-skills@developer-meetup-program`    | Run a recurring meetup or user group - format, cadence, speakers, venue sponsor, health |
| `samber/developer-relations-skills@developer-event-sponsorship` | Buy sponsorship - which events, which tier, which activation, what ROI proof            |

**Community:**

| Skill                                                              | Route here when the task is…                                                                |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@developer-community-launch`     | Whether, where and when to open a community, plus seeding and the first 90 days             |
| `samber/developer-relations-skills@developer-community-moderation` | Code of conduct, enforcement ladder, reporting channels, incident runbook, moderator roster |
| `samber/developer-relations-skills@developer-champions`            | A champions or ambassador program - intake, criteria, obligations, perks, terms, scorecard  |
| `samber/developer-relations-skills@developer-community-health`     | Measure the community - activity, responsiveness, contributor funnel, sentiment, thresholds |

**Content and media:**

| Skill                                                           | Route here when the task is…                                                        |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@engineering-blog-post`       | Write or edit a technical post for a skeptical developer reader                     |
| `samber/developer-relations-skills@developer-case-study`        | Turn a customer deployment into a technical case study engineers believe            |
| `samber/developer-relations-skills@technical-video-script`      | A shooting-ready screencast script - beat sheet, code pacing, chapters, cut list    |
| `samber/developer-relations-skills@tech-podcast-interview-prep` | Prepare to be the guest on someone else's podcast, interview or livestream          |
| `samber/developer-relations-skills@devrel-content-calendar`     | Plan a quarter of content around fixed anchors, capacity and mix                    |
| `samber/developer-relations-skills@tech-press-relations`        | Press and light analyst relations - angle, reporter map, pitch, embargo, press page |

**Meta and personal practice:**

| Skill                                                           | Route here when the task is…                                                            |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `samber/developer-relations-skills@devrel-radar`                | Build the personal watch list - podcasts, newsletters, communities, conferences, people |
| `samber/developer-relations-skills@devrel-career`               | Candidate side - portfolio scoring, skill-gap roadmap, interview prep, IC vs management |
| `samber/developer-relations-skills@devrel-hiring`               | Employer side - job posting and scorecard, interview loop, portfolio scoring, ramp plan |
| `samber/developer-relations-skills@developer-relations-kickoff` | This skill: project start, periodic check-in, "which skill do I need", re-routing       |

Disambiguate before routing wherever clusters collide on keywords:

- **Docs authoring** - four skills that all look like "write a getting-started page"
- **Release communication** - changelog vs migration guide
- **Measurement** - metrics vs analytics vs community health
- **OSS visibility** - launch vs distribution vs build-in-public
- **Sponsorship** - two skills that differ only by which side pays
- **Community** - four skills on one timeline
- **Strategy** - five skills that all answer "what should we do"
- **Speaking** - a sequence, not a competition
- **Employer brand** - the strategy for attracting engineers vs. one post, one profile page, or the candidate's own side of the table

Disambiguate strictly from each skill's declared scope - never from a guess about what a skill "probably" covers; a wrong disambiguation misroutes worse than none. Read [references/skill-routing.md](./references/skill-routing.md) before routing any task that could plausibly match two skills - it carries the per-skill route/do-not-route signals, every boundary fork above, the ordered chains, and the named coverage gaps.

Name the gap explicitly when the task needs something no skill covers. Collection v1 has no skill for:

- task-oriented how-to guides (as distinct from tutorials and quickstarts), or API reference completeness
- the versioning and deprecation policy itself, as opposed to documenting one migration
- hiring or interviewing DevRel staff - the role definitions and the interview loop, not the engineering employer brand, which `samber/developer-relations-skills@tech-employer-branding` covers - or the exec-facing DevRel report
- monetizing one open-source project, or maintainer burnout as a subject of its own - succession and bus-factor planning belong to `oss-governance`, which also owns who holds the trademark, domains and registry accounts; only a third-party trademark _usage and enforcement_ policy is uncovered
- organizing your own conference or hackathon, conference booth operations, or post-event follow-up
- a developer newsletter, student and campus programs, or an office-hours program
- choosing a docs platform, or brand-mention monitoring
- writing the slides, editing the video, or legal sign-off on anything

Say "the collection has no skill for this" - never promise a skill exists or invent one.

Some tasks that land here aren't a true gap - they belong to the same owner's sibling collections:

- Public API surface design, webhooks, SDK portfolios, developer-portal design, OAuth for third-party apps, and connector-marketplace operations belong to `samber/developer-platform-skills`.
- Organizing your own event - venue, ticketing, sponsor sales, run of show, speaker sourcing as the organizer - belongs to `samber/dev-event-organizer-skills`.

Recommend installing the sibling collection instead of stretching a devrel skill onto the task, and never treat a sibling as a dependency this collection needs to function. See [references/skill-routing.md](./references/skill-routing.md) § Sibling-collection recommendations for the detection signals and the boundary per topic.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact: product and audience motion, funded driver and pillar mix, program stage and team shape, in-flight work, active constraint.
2. **Route** - the one skill for the immediate task, a sibling-collection recommendation naming the specific area (see § 3), or "no skill fits" plus the named gap when nothing covers it.
3. **Short-list** - 5 to 8 skills relevant to this project right now, ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness, and never by the routing tables' row order - see "Ordering the short-list" below.
4. **Chain** - when the task genuinely decomposes into an ordered sequence (e.g. `developer-segmentation` → `devrel-strategy` → `devrel-metrics` → `devrel-budget-allocation`), list it in execution order with one line per link on what it hands to the next. Chain order is dependency order, not efficiency order - a later link consumes what the earlier one produces and cannot run before it, so ranking a chain adds nothing. Omit the chain when there isn't one - never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (e.g. "`developer-community-health` - once the community has a baseline; `developer-community-launch` gates that at its day-90 review, that skill's own working convention").
6. **Gap** - anything today's task needs that no skill covers, stated as a gap.

### Ordering the short-list

The user's question at that moment is never "which of these 55 exists" but "which one do I run first, and is it worth the session". Only a ratio answers that. Default class order, highest value per unit of effort first:

1. **Diagnosis** - `developer-journey-map`, `developer-docs-structure-audit`, `devrel-competitor-analysis`, `developer-keyword-research`. Buys a named, evidenced answer to which class below is actually the problem, instead of a hunch. Costs one session over docs and signals already available; needs no engineering time and publishes nothing.
2. **First-run surfaces** - `readme-optimization`, `developer-quickstart-guide`, `oss-contributor-onboarding`, `github-profile-optimization`, `docs-code-sample-standards`. Buys the bail-fast funnel for every developer who arrives after it ships: fewer abandonments between landing and first successful call. Costs an editing session plus one merged pull request, and it is reversible by another commit.
3. **Release and support cadence** - `changelog-writing`, `version-migration-guide`, `developer-troubleshooting-docs`, `oss-issue-triage`. Buys users who can upgrade and self-serve their own errors instead of opening an issue. Costs a pass per release and a maintainer answering what the triage surfaces - it never finishes; it is a standing job, not a fix.
4. **Content and visibility** - `engineering-blog-post`, `developer-tutorial`, `technical-video-script`, `developer-case-study`, `docs-seo`, `devrel-content-calendar`, `build-in-public`, `oss-launch`, `oss-distribution-strategy`, `tech-press-relations`, `tech-podcast-interview-prep`. Buys reach that compounds - a post or a registry listing keeps earning for years. Costs a full production cycle per artefact plus review, and the payoff arrives a quarter after the work, not the week of it.
5. **Community and events** - `developer-community-launch`, `developer-community-moderation`, `developer-champions`, `developer-community-health`, `developer-meetup-program`, `developer-event-sponsorship`, `conference-cfp-submission`, `tech-talk-outline`, `developer-live-demo-design`, `oss-sponsors-fundraising`, `oss-sponsors-brand-strategy`. Buys the relationships nothing else in the collection produces. Costs the longest lead time here - a calendar someone else controls, a standing moderation duty, and months between opening a space and it being worth reading.
6. **Program and company foundations** - `devrel-strategy`, `developer-segmentation`, `devrel-metrics`, `devrel-analytics`, `devrel-budget-allocation`, `devrel-team-structure`, `developer-education-strategy`, `devtools-business-model`, `devtools-pricing-strategy`, `developer-first-gtm`, `open-source-company-strategy`, `developer-ecosystem-strategy`, `open-standards-strategy`, `oss-governance`, `oss-license-strategy`, `tech-employer-branding`. Buys the rule every later session is decided against: what the program is judged on, who may merge, what the company gives away. Costs sign-off outside DevRel - engineering, legal, exec - and most of it is reversible only by another negotiation.

`devrel-career` and `devrel-radar` sit outside this ladder, not at the bottom of it. They answer a personal-practice or stay-current question, not a program question; when that _is_ the goal they are rung 1 by definition, and otherwise they don't belong on the short-list at all.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `diagnosis > first-run surfaces > release cadence > content > community and events > foundations`
- value: `foundations > first-run surfaces > community and events > content > release cadence > diagnosis`
- effort: `foundations > community and events > content > release cadence > first-run surfaces > diagnosis`
- compliance cost: `foundations > community and events > content > release cadence > first-run surfaces == diagnosis (none)` - a license or governance decision binds every future contributor and is undone only by relicensing; a community space makes you moderator of other people's speech and holder of their reports; sponsorship money crosses a disclosure line; published posts and press need sign-off and cannot be unpublished; a release note is a public statement about breaking changes. Diagnosis and first-run surfaces tie at zero: both read and edit your own repository and publish no claim about anyone else, though first-run surfaces costs a merged pull request that diagnosis does not.

Foundations lead on value and sit last on efficiency, because sign-off is measured in weeks and the output is invisible the week it lands.

That is what the efficiency order starves: class 6's foundational skills. `devrel-strategy` and `oss-license-strategy` are the clearest cases - highest coordination cost, nothing shippable that week - so a ratio-first order polishes READMEs forever while every later session re-argues what the program is for and what the company may give away.

Promote class 6 to rung 1 outright when:

- Nobody can name the funded driver (Q4 came back empty or claimed all seven).
- No license or governance file exists on a repository already taking outside contributions.
- The same scope argument reappears session after session.
- The answer to Q7 is (d) standing with sign-off available.

Default: open the short-list at class 1 and stay there until the diagnosis names a class below it. Move down exactly one class at a time, and never past a class whose absence the diagnosis flagged.

Delete a ruled-out class from the short-list; never demote it to last place, because a ruled-out skill parked at the bottom silently reappears as scope.

- Has a stated unblocking condition - move it to the "Not now" list carrying that condition.
- Has none - drop it from the output entirely.

The ordering is a default, not a law - it shifts with the adoption motion and with who executes it. Re-rank against what the interview and the detection pass just told you, and say out loud which answer moved which class:

- A non-commercial open-source project with no buyer (Q3d) deletes `devtools-pricing-strategy`, `devtools-business-model` and `developer-first-gtm` from the short-list, and promotes `oss-governance` and `oss-sponsors-fundraising` inside classes 6 and 5.
- Individual self-serve adoption (Q3a) promotes classes 2 and 4.
- Organization-buys (Q3b) promotes `developer-case-study` and `developer-first-gtm` above their default place, since the signer never runs the quickstart.
- The funded driver (Q4) deletes whole classes:
  - Sales enablement deletes class 3's triage entries unless the project is open source.
  - Contributor community deletes `developer-first-gtm` and `devtools-pricing-strategy` outright.
  - Employer branding promotes `tech-employer-branding` to rung 1, since it owns that driver's whole plan and ranks every content bet made under it.
- Stage "nothing formal yet" (Q5a) deletes `devrel-team-structure`, `devrel-budget-allocation` and `developer-community-health` - there is no team, no budget and no baseline to measure.
- No engineering support for docs (Q6c) deletes class 2's code-dependent entries and leaves `readme-optimization`, which needs no engineering time.
- No analytics access (Q6e) deletes `devrel-analytics` and `developer-community-health` from this session and moves them to "not now", unblocked by instrumentation.
- Legal or security review required (Q6d) lengthens classes 4, 5 and 6 without changing what they buy - say so rather than silently demoting them.
- A fixed date (Q6) promotes whatever acts inside that window:
  - A conference date promotes `conference-cfp-submission` and `developer-live-demo-design` to rung 1 for the season.
  - A release date promotes class 3.
- "One-off, maintainer hours only" (Q7a) cuts the short-list to two entries from classes 1 and 2.
- "Standing, with sign-off available" (Q7d) promotes classes 5 and 6 above their default place.
- An asset already owned changes the ratio, not the value: an instrumented analytics stack, a docs site already deployed, or a conference slot already accepted makes the dependent skill near-zero effort - promote it.
- A decided item (Q2) leaves the short-list outright; do not rank what is off the table.
- Detection moves classes too:
  - A repository with no CONTRIBUTING file promotes `oss-contributor-onboarding` inside class 2.
  - A git log showing months of stall points at diagnosis before any build.
  - An existing docs site with an information architecture already audited deletes its class-1 entry.

## 5. Context artifact

Create or update `devrel-context.md` at the project root - one versioned file, committed with the project when the project lives in git, and the single source of truth that makes the next start warm. Its sections:

- Product and audience.
- Program: funded driver, pillar mix, stage and team.
- Surfaces owned.
- Measurement.
- State: in flight, decided vs open, constraints including the date the result must land by, the one-off-versus-compounding horizon and the effort ceiling.
- Stakeholders with decision rights.
- A session log.

Those last three constraint fields are what let a warm start re-rank the short-list and the routines without re-asking questions 6 and 7. See [references/context-artifact.md](./references/context-artifact.md) for the template, a worked example, and a negative example.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with the project's invariants (audience motion, funded driver, surfaces owned, hard constraints) so every future session inherits them without loading this skill.
- Do not scaffold a working tree the project hasn't earned. Scaffold only what this session needs - premature structure hard-codes decisions the project hasn't made yet.
- Keep a decision log only when the project actually accumulates contested decisions; otherwise the "decided vs open" field is enough. An empty ceremony log goes stale and erodes trust in the artifact.

Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If your harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses to memory after the interview completes and before § 4 Output shape: write the captured answers into the context artifact first, then derive the memory entry from the artifact. Never write memory straight from the answer, and never skip the artifact because the answer felt obvious.
- Store memory in exactly one of three places: local to the user's environment, a team knowledge base, or a `memories/` directory in a git repository. Index it with an index file listing each entry with a one-line hook.
- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - artifact wins by default; ask before overwriting either.
- Never put into memory:
  - Community-member or contributor personal data.
  - Conduct reports and moderation cases.
  - Unannounced launches and embargoed news.
  - Sponsorship and event rates under NDA.
  - Unpublished pricing.
  - Customer names not yet cleared for a case study.
  - Security-sensitive detail from a build-in-public boundary.
- State this exclusion when you first write memory.
- When memory lives in a git repository, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If your harness supports scheduled routines, propose 2 to 4 - always shown as a dry-run before anything is created, each with an explicit output channel. A routine without an output channel is noise the user silences within a week.

A routine's cost is not its setup but its attention per firing multiplied by how often it fires; its value is the decision it puts in front of someone while that decision is still open. Rank the candidates on that ratio - value per unit of standing effort, highest first - and propose from the top down:

1. **Release-tag documentation pass** → `samber/developer-relations-skills@changelog-writing`, plus `samber/developer-relations-skills@version-migration-guide` when the release is a major. Fires only when a tag lands, over commits and pull requests already written, and it is the only routine whose output can reach users before the release does rather than after they hit the breakage.
2. **Monthly or quarterly re-invocation of this kickoff.** Near-zero per firing, and it keeps the artifact and the routing tables current - which is what stops every other routine firing at work that no longer exists. Match its cadence to the project's pace from the git log.
3. **CFP deadline sweep** ahead of the season's target events → `samber/developer-relations-skills@conference-cfp-submission`. A handful of firings a season, each a short read of a deadline list, against a deadline that is absolute: miss it and that stage is gone for a year. Buys nothing outside CFP season, which is why it is not rung 1.
4. **Periodic issue and pull-request queue review** → `samber/developer-relations-skills@oss-issue-triage`. Buys a queue that stays answerable instead of one that compounds into an abandoned project. Carries the highest standing cost in the set: a session per pass plus a maintainer answering everything it surfaces. Install it only where someone owns that follow-through.
5. **Quarterly content planning** at quarter start → `samber/developer-relations-skills@devrel-content-calendar`. Four planning sessions a year, buying a quarter of content that ships against real anchors instead of whatever occurred to someone that week.
6. **Periodic measurement read** → `samber/developer-relations-skills@devrel-metrics` (program) or `samber/developer-relations-skills@developer-community-health` (community only). Buys a trend line someone can act on - but only once a baseline exists; fired before that, it reads noise aloud on a schedule.

- efficiency: `release-tag pass > kickoff re-invocation > CFP sweep > queue review > content planning > measurement read`
- value: `queue review > release-tag pass > content planning > measurement read > CFP sweep > kickoff re-invocation`
- effort: `queue review > content planning > measurement read > release-tag pass > CFP sweep == kickoff re-invocation`
- compliance cost: `release-tag pass > content planning > measurement read == queue review == CFP sweep == kickoff re-invocation (none)` - release notes and migration guides are public statements about breaking changes and cannot be unpublished; a content calendar schedules those publications without committing to them. The four tied at zero all read internal or already-public state and emit it to the team; the CFP sweep and kickoff re-invocation also tie on effort, since each is one near-zero read per firing.

The kickoff re-invocation is the cheapest candidate and still sits second, not first - proof that cheap and efficient differ. The queue review leads on value and sits fourth on efficiency, since it costs a session every pass plus a maintainer answering each issue raised.

Default: rungs 1-2, which is two routines. Add rung 3 when CFP season is open, rung 4 once someone owns the triage follow-through. Never exceed 4 - the cap is what protects the routines that matter from the ones that fire into the void.

The ranking is a default, not a law; it shifts with the surface and with who executes it. Re-rank it against the interview and say which answer moved which routine:

- An open-source surface (Q1b) promotes the queue review above the CFP sweep.
- An events surface (Q1d) with a conference date promotes the CFP sweep to rung 1 for the season.
- No analytics access (Q6e) deletes the measurement read rather than demoting it.
- "Nothing formal yet" (Q5a) deletes it too, since there is no baseline to trend against.
- Maintainer hours only (Q6b), or "one-off, hours only" (Q7a), means install one routine - the kickoff re-invocation - not four.
- Legal or security review required (Q6d) lengthens the release-tag pass without changing what it buys.
- A team already running a weekly triage rotation makes rung 4 a duplicate, so demote it rather than sweep the same issues twice.
- An analytics stack already instrumented, or a docs pipeline that already builds on tag, makes its dependent routine near-zero effort - promote it.

Anchor triggers to the DevRel calendar - release train dates, CFP deadlines, conference dates, budget review, community rituals - rather than arbitrary dates, and prefer an event trigger over a schedule when one exists: a tag push beats "the first of the month" for release notes. List and clean up obsolete routines left over from a previous quarter before adding new ones.

If the harness has no scheduled routines, fall back to one recurring calendar reminder ("DevRel check-in - re-run the developer relations kickoff") and stop there. See [references/routines.md](./references/routines.md) for the dry-run format, calendar anchoring, event-trigger preference, and cleanup checklist.

## 8. Invocation examples

- "Start a new devrel project - we just open-sourced our SDK and nobody uses it." → cold start: detect, interview, route, write the artifact.
- "Which devrel skill do I need? Our docs are fine but signups never reach production." → routing ask: match against the tables, disambiguate, name the gap if none fits.
- "Run my devrel check-in." → warm start: 5-line state summary, session-goal question, re-route.
- "Where do I start? I'm the first devrel hire and I have no idea what to do first." → cold start: expect an ordered chain, not a single route.

## 9. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it doesn't cover wastes a session and hides the gap. Say "none fits" and name the gap.
- **Routing every docs question to the same skill.** Quickstart, tutorial, how-to and reference are four different jobs - and the collection has no how-to skill at all. Check § Docs-authoring fork in the routing reference first.
- **Force-fitting platform or event-production tasks.** API design, webhooks, SDK strategy and marketplace operations belong to `samber/developer-platform-skills`; organizing your own conference belongs to `samber/dev-event-organizer-skills`. Recommend the sibling collection instead.
- **Re-interviewing on a warm start.** The artifact exists precisely so questions aren't repeated. Ask only the session goal.
- **Routing from a guessed scope.** Route only from the declared scopes in the routing reference; a plausible guess misroutes confidently.
- **Skipping the funded-driver question.** Without it, the strategy, metrics and budget routes all collapse into generic advice the user has to re-scope by hand.
- **Uncapped interview.** Past 7 questions the kickoff becomes a form the user abandons.
- **A flat short-list.** Eight equal-looking options get picked by taste, or by whichever sits first. Order by value per unit of effort and name both sides on every line, or the user cannot choose.
- **Leading with the cheapest option.** Cheap and efficient are different orderings, and only the second one answers "what first". A near-zero routine that buys near-zero is a rounding error, not a quick win.
- **Ranking the routing tables or the chain.** Scope is a match test and a chain is a dependency order; imposing a ratio on either invents a preference that does not exist.
- **Demoting a ruled-out skill instead of deleting it.** A class the interview took off the table, parked at the bottom of the short-list, reappears as scope two sessions later. Delete it, or move it to "not now" with its unblocking condition.
- **Letting the ratio starve the foundations.** Class 6 loses every efficiency round and is exactly what a program being set up needs first. Check its promotion conditions before opening at class 1.
- **Routines with no output channel.** They fire into the void and get silenced, burying the one routine that mattered.
- **Memory committed silently.** Teammates can't review what they can't see land. Diff and approval, always.
- **Stale routing table.** Update the tables, routing reference, boundary forks, chains and gap list whenever the collection changes - a skill added, renamed, removed, or re-scoped. A stale router sends users to skills that no longer exist, which is worse than no router at all.

## 10. Pass bar

Before ending the session, check every item. If any fails, fix it and re-check - do not close the session on a failing bar.

1. Every recommended skill's declared scope actually matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the 55 skills in the tables above.
3. Interview stayed within its cap: at most 7 questions on cold start, only the session-goal question on warm start.
4. `devrel-context.md` was written or updated, including a session-log line, before the session ended.
5. Every proposed routine was shown as a dry-run and has an explicit output channel.
6. The short-list and the routine set are both ordered by value per unit of effort, each entry naming the bottleneck it attacks and what it costs - and the re-rank was stated out loud whenever an interview answer moved something off its default place.
7. Every class the interview ruled out left the short-list entirely, rather than sitting at the bottom of it.
8. The routing tables and any proposed chain were left unranked - match test and dependency order respectively.
