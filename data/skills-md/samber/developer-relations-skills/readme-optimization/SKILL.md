---
name: readme-optimization
description: Audits and rewrites a repository README so a developer who has never seen the project can tell what it is, why it beats the alternative, and run the first command inside a minute - every claim and the documented install verified against the source, the page ordered into a bail-fast funnel, badges that earn nothing pruned. Use whenever someone says "review my README", "my readme is bad", "write a README for this repo", "nobody understands what my project does", "repo first impression", "readme structure", "too many badges", or is preparing an open-source launch - even if they only call it the repo landing page. Not a profile README - use samber/developer-relations-skills@github-profile-optimization.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# README Optimization

You are working on the single page that decides whether a developer tries a project or closes the tab. Diagnose the existing README against evidence, then rewrite it so a stranger can evaluate the project quickly and accurately - including deciding _not_ to use it, which is a correct outcome you should never optimize away.

A README is not a documentation type. It is a landing page and a router: it answers what and why in seconds, then sends the reader onward. Judge it on whether it converts a visitor into a trial, not on documentation completeness.

Put the rewrite budget where the scarcity is. Across 393 sampled GitHub repositories (Prana et al. 2019, cited in [./references/published-findings.md](./references/published-findings.md); the sample is late-2010s, read it as a baseline, not a census):

- What the project is: 97.0% - table stakes.
- How to use it: 88.5% - table stakes.
- Why to pick it over the alternatives: 25.7% - scarce.
- What state the project is in: 21.4% - scarce.

Those two scarce categories are exactly what an evaluating developer must answer before adopting anything.

Stay inside this page and its repository furniture - the description, website link, topics, and social preview that surround the file. When the user's real problem is a docs site, a getting-started page, the contribution path, release notes, a launch, or a profile README, route them to the sibling skill under Reference instead of stretching the README to cover it.

## Folklore statistics to refuse

Never repeat these folklore statistics in your own reasoning or to the user - all three circulate widely on invented attributions:

- "repos with detailed READMEs get 50% more contributions"
- "a star-history chart lifts star conversion ~15%"
- "62% of top repos have GIF demos"

When a user cites one, say it is unsourced rather than building on it. Every figure this skill does quote is cited in [./references/published-findings.md](./references/published-findings.md); read it before repeating a statistic to a user.

Promise a better-evaluated project, never a percentage lift.

## Invocation examples and output shape

Typical requests:

- "audit the README of this repo"
- "our GitHub gets traffic but no installs"
- "rewrite the top of our README before launch"
- "make our README readable by someone evaluating us for their company"

Every run produces a scorecard first, in this shape, before any prose is written:

```
README audit - acme/flowmatic   (audience: solo developer)
Band A: A1 pass · A2 FAIL (install needs Node >=20, undocumented) · A3 FAIL · A4 pass · A5 pass
Verdict: does not pass - A2 and A3 blocking; B1 returns the most per hour spent
```

The rewrite follows only after the user agrees with that diagnosis. The full report format, including the claim check, Band B, and the fix order, is in [./references/audit-scorecard.md](./references/audit-scorecard.md).

## Interview

Ask one question at a time, multiple-choice where you can, and skip anything you can determine yourself by reading the repository. Questions 1-4 gate the rewrite - do not draft prose before they are answered.

1. Which repository, and can I read it and run commands in it?
2. What is the project: library or SDK, CLI tool, application or service, framework or platform, or template and learning resource?
3. Who lands on this page: developers in one language ecosystem, polyglot developers, platform or ops engineers, or non-developer evaluators such as security and procurement?
4. How does adoption happen - an individual developer installs it and decides alone, or a company adopts it and someone else approves the licence, the security posture, and the support story? Both is a valid answer, and it changes the middle of the page.
5. What outcome do you want more of: installs, contributors, stars, hiring signal, enterprise conversations, or fewer repetitive support questions?
6. What is the honest project status: experimental, actively maintained, stable and feature-frozen, or seeking maintainers?
7. Which alternatives do readers arrive already knowing? What do those do better than you?
8. What must appear for legal or policy reasons - licence terms, trademark notice, export or compliance statements, employer disclosure?
9. Is there existing brand material - a logo, a tagline, a positioning sentence used on a website - that the README should match?
10. Is the README also published elsewhere: a package registry page, a mirror, a docs-site landing page? Each render target has different rules.
11. Is there a date this has to be done by - a launch, a conference, a funding conversation - or is the page just overdue?
12. Do you want a one-off win before that date, or an asset that keeps paying: a positioning sentence and a page shape you reuse for the next two years?
13. What is your ceiling - an afternoon, a week of someone's time, permission to ask customers for a logo, appetite for a governance or foundation commitment you cannot easily undo?

Answers 11-13 re-rank every ordering below; say which answer moved which fix when presenting the plan.

- **Hard date (Q11)** - promotes the fixes that land in an hour, drops the funnel restructure from this pass.
- **Compounding mandate (Q12)** - promotes the differentiation paragraph and the restructure, whose one-liner propagates into the registry page, the launch post, and every link unfurl.
- **Low ceiling (Q13)** - deletes the terminal demo and the enterprise signals outright, rather than parking them at the bottom of a list.

If the user cannot answer 7, treat that as a finding rather than a blocker. A maintainer who cannot name their alternatives usually has a README that cannot differentiate either, and that is the most valuable thing you will fix.

## Step 1 - Declare the audience, then check the README is the bottleneck

Answer 4 decides the whole audit. The enterprise evaluator and the solo developer want structurally different content, and optimizing for one degrades the other: a hobbyist bounces off a wall of compliance badges, and a procurement reader distrusts a page with no security or governance signal. Write the declared audience at the top of your scorecard so every later judgement is checkable against it.

Then confirm the README is what is broken. If the code host exposes traffic data, take unique visitors and clones for the last two weeks.

- Decent traffic with a clone-to-visitor ratio of only a few percent: this is the case this skill is for - people arrive and leave unconvinced.
- Few visitors in the first place: a distribution problem, not a prose problem - route the user to launch or distribution work instead of rewriting a page almost nobody reads.

That "few percent" boundary is a working heuristic, not a benchmark; on a borderline number, look at referrers rather than ruling.

## Step 2 - Gather evidence

Never audit from memory of what good READMEs look like.

1. Read the README in full and note where you personally got confused. Your first-read confusion is the closest thing you have to a cold reader.
2. Run the mechanical audit: `scripts/readme-audit.sh <repo-root>`. It reports:
   - shadowed copies
   - truncation risk
   - the heading tree
   - section count against the median of 7
   - words before the first copyable command
   - badge count
   - missing alt text
   - registry-hostile raw HTML
   - broken relative links
   - placeholder text
   - missing content categories
3. Read the repository around the README: manifests for the real runtime requirements, the licence file, recent commit dates, open-issue volume, and whether the examples it references exist on disk.
4. If your environment can browse the web, open the project's package-registry page and compare it to the code-host render. Relative links and raw HTML frequently break there, and that page is often the higher-traffic one.
5. If your environment has persistent memory, reuse any stored positioning statement, audience definition, or competitor list for this project instead of re-deriving it.

Optionally add a structural README scorer and the code host's community-standards checklist as a second opinion, treating both as hygiene baselines - see the validity ceiling in [./references/tooling-and-measurement.md](./references/tooling-and-measurement.md). The script reports facts, not judgements: a section count of 25 is a question to answer, not a verdict.

## Step 3 - Score the current README

Work through [./references/audit-scorecard.md](./references/audit-scorecard.md) and produce the scorecard in the shape above.

- Band A: five blocking checks - identity, the install actually running, every claim verifiable, honest status, reachable licence.
- Band B: eight scored checks, worth two points each.

Attach evidence to every check - a line number, a quoted sentence, or the terminal output of a command you ran. Get the user's agreement on the score before rewriting anything: a maintainer who rejects the diagnosis rejects the treatment, and they are sometimes right, since a constraint invisible from the repository can justify a check you scored zero.

### Order the fixes

Order the fix list by what each fix returns per hour spent, not by how easy it is to write and not by how much damage it undoes - those three orderings disagree, so state all of them and lead with the third:

- effort, least first: `status line == badge row > claim check > install path > differentiation paragraph > funnel restructure`
- value, most first: `install path > differentiation paragraph > claim check > status line > funnel restructure > badge row`
- efficiency, do first: `status line > install path > claim check > differentiation paragraph > badge row > funnel restructure`

The status line and the badge row tie on effort: each is one edit to one block, written from what the maintainer already knows, verified against nothing - no command run, no source read. They separate on value, since a status line answers a question only 21.4% of READMEs answer and a badge row answers one 61% of contributors ignore.

Default to the top three for a first pass; move down once the blocking checks are green, or when the cold-reader test fails on a question none of the three touches.

The funnel restructure loses every round - a week against fixes that land in an hour - so this order under-invests in the one change that makes the page work. Promote it when the cold reader answers wrong because they never scrolled far enough, or when a launch is the reason for the audit, and say you are promoting it against the ratio.

The ordering is a default, not a law, and it shifts with who executes it. Re-rank it against what you already know:

- A maintainer who can name their alternatives in one sentence gets the differentiation paragraph nearly free, which promotes it above the install path.
- A project with no install command - a spec, a dataset, a template - deletes that row rather than scoring it zero forever.

Delete every fix answer 13's ceiling rules out instead of listing it last.

## Step 4 - Verify every claim against the source

A README is a set of claims about a codebase, and every claim is checkable. Agents and maintainers alike write from memory of how an API usually looks; a reader cannot tell a verified line from an invented one, and you can, because you have the repository.

List every claim:

- command
- flag
- default value
- environment variable
- config key
- endpoint
- exported symbol
- file path
- version requirement
- behavioural assertion hidden in a verb, e.g. "automatically reconnects", "retries three times", "case-insensitive"

Verify each against its own source of truth - the argument parser, the definition site, the route table, the changelog - by reading it, not recalling it. A flag documented in the README but absent from the parser is a hallucination, not a typo.

Then run the install path itself, because it catches the most real damage:

1. Start from a clean state - a container, a fresh virtual environment, a temporary directory, whatever your environment supports. If you cannot execute commands, say so plainly and ask the user to run the sequence and paste the output; never mark this check passed on inspection.
2. Execute the documented install command exactly as written, then the first usage example exactly as written.
3. Record every gap: an undocumented runtime version, a system package assumed present, a required environment variable, an output that differs from the README.
4. Fold each gap into the README as an explicit prerequisite or a verification step, then run the sequence again from clean.

Repeat until the documented path runs end to end with no undocumented step. Any performance number, compatibility matrix, scale limit, or "production ready" claim needs a source inside the repository - a benchmark script, a CI matrix, a changelog entry - or it comes out. When you cannot verify something, downgrade the claim to what you can verify and say which part is unconfirmed.

## Step 5 - Choose the shape, then rewrite section by section

Pick the skeleton from [./references/readme-skeletons.md](./references/readme-skeletons.md) that matches what the reader is _deciding_, not what the code happens to be.

- A library reader is judging fit with an existing codebase.
- A CLI reader is comparing against a tool already installed.
- A framework reader is making a multi-year bet.

Order sections by how quickly each lets a reader disqualify the project. This is **cognitive funneling**, named by Kira in _Art of README_: widest and most disqualifying information first, narrowing to detail only a committed reader reaches. One consequence: a non-permissive licence belongs near the top, because it disqualifies fastest and hiding it wastes the reader's time.

Before writing, brainstorm the positioning explicitly instead of reaching for the first phrasing. Draft three candidate one-liners on different axes:

- what it does mechanically
- what problem it removes
- what it lets you stop using

Present them with each one's trade-off and your recommendation, and let the user choose. The one-liner propagates into the repository description, the registry page, and every link unfurl.

Draft one section at a time and get agreement before moving on; per-section approval surfaces a disagreement while it is still cheap to fix. For each section:

1. Write the shortest version that answers its question completely.
2. Replace every unfalsifiable claim ("simple", "blazing fast", "developer-friendly") with something a reader could check - a number, a dependency count, a supported-platform list, a named trade-off.
3. Link every term a reader outside the project's immediate ecosystem might not know.
4. State what the project deliberately does not do, and when to use something else. This is the highest-trust sentence in most READMEs and it costs one line.
5. Move anything that grew past a screen into a linked document and leave a one-line pointer behind. Relocate overflow, never delete it.

Keep community health content out of the file - contribution guidelines, code of conduct, security disclosure, support policy. Each belongs in its own recognized file, which the code host surfaces at the moment it matters; inlining them only adds scroll distance before the reader can decide anything. One exception: the licence file must ship inside the repository, so an organization-level default is not enough.

Run the finished prose through your preferred humanizer skill before presenting it. Copy that reads as generated undermines the credibility the rest of the page is building, and developers spot it easily.

See [./references/before-after-examples.md](./references/before-after-examples.md) for worked positive and negative examples of the opening lines, the differentiation section, the status statement, badge rows, install blocks, and usage snippets.

## Step 6 - Calibrate badges to the evidence

Badges are the one README element with a rigorous evidence base: Trockman et al. studied 294,941 npm packages (ICSE 2018). Use the study's distinction rather than taste.

- Keep **assessment signals** - badges backed by a third-party check that cannot pass unless the underlying thing is true: CI status, coverage, published version, dependency freshness.
- Cut **conventional signals** - badges that merely state an intent, such as "PRs welcome", with nothing verifying them. They signal nothing.
- Cap the row. Among already-popular packages, excessive badge use correlates with _decreased_ popularity, and adopting a badge does not raise popularity at all - popular projects are simply likelier to have badges. The direction is sourced; the cap of four is a working default here, not a published figure, so justify each survivor by the reader question it answers rather than arguing about the number.
- Expect the maintainer to over-value them. The study's small companion survey found maintainers rate badges as a quality indicator far more often than contributors do, and most contributors say badges do not influence them at all. Quote the figures from [./references/published-findings.md](./references/published-findings.md) when a maintainer resists cutting the row.

## Step 7 - Fix repository furniture and render mechanics

Three things compete for this step's budget, and they are not close:

- efficiency, do first: `furniture > render mechanics > terminal demo`

- **Furniture** is near-zero effort and buys the only text a reader sees before opening the repository: the description, website link and topics are what search listings carry, and the social preview is what unfurls when someone pastes the link into a chat.
- **Render mechanics** cost about an hour and buy the page working for readers who never see the code host's render - registry pages, terminals, screen readers.
- **Terminal demo** costs a week to produce well and then becomes a standing job, going stale whenever the output changes.

The demo is what this order starves, and it is the highest-value element on the page for a CLI or a visual tool, where the output _is_ the product. Promote it above render mechanics in exactly that case, and generate it from a script rather than hand-recording it, so re-rendering stays cheap enough to survive as a standing job. Delete it for a library with no visible output - a demo of an import statement earns nothing - rather than leaving it to reappear as scope later.

Fix the furniture, then fix how the file itself renders:

1. Give every image alt text, and move any instruction, command, or decision-relevant fact out of screenshots and animated demos into text. Readers meet READMEs in terminals, on registry pages that strip HTML, and through screen readers - an animated demo is invisible to all three.
2. Delete a hand-written table of contents - code hosts generate an outline from headings, and the manual copy goes stale.
3. Check that relative links resolve from the repository root on the default branch, and that the page still reads correctly where raw HTML is stripped.
4. Keep only one rendered README. Where a host renders a `.github/` copy in preference to the root file, the root copy is what registries and mirrors publish, so the two silently diverge.
5. In a monorepo, make the root README a router to the per-package READMEs rather than covering every package inline.

When the demo does earn its place, keep it short, high-contrast and legible at embed scale, and place it right after the tagline. Treat its conversion benefit as practitioner consensus rather than a measured result - no study prices it, which is another reason not to let it outrank the two cheaper rows by default.

## Step 8 - Add enterprise trust signals, only if the audience calls for them

Run this step only when Step 1 declared a company or procurement audience.

An enterprise decision-maker optimizes for defensibility, not best technical fit, so recognizable third-party signals - a foundation tier, an audit, an attestation, a well-known adopter - outperform novel claims. Published evaluation checklists weight maintenance activity, licence clarity and security posture above presentation quality; sources are in [./references/published-findings.md](./references/published-findings.md).

Six signals are available, spanning two orders of magnitude in what they cost:

- effort, least first: `support expectation == release cadence > security policy > named adopters == supply-chain attestation > governance and maintainer depth > foundation affiliation`
- value, most first: `foundation affiliation > named adopters > security policy > governance and maintainer depth > supply-chain attestation > release cadence == support expectation`
- compliance cost:
  - foundation affiliation demands trademark or IP assignment and a legal sign-off you cannot walk back
  - named adopters need each company's own marketing approval, revocable but only by asking again
  - a security policy commits you publicly to a response window you then have to honour
  - the remaining three trigger no review and are reversible with one commit
- efficiency, do first: `support expectation == release cadence > security policy > named adopters > governance and maintainer depth > supply-chain attestation > foundation affiliation`

Support expectation and release cadence tie twice over: each is one sentence stating something already true, needing nobody's permission and no work beyond reading the commit log. Named adopters and supply-chain attestation tie on effort at about a week each, but separate on efficiency - the attestation persuades an engineer who was going to say yes anyway, while a recognizable logo persuades the person who signs.

Default to the first three, an afternoon between them, which clear most of what an evaluation checklist scores. Move to named adopters when a deal is in the room and someone has asked "who else runs this".

Foundation affiliation is what this order starves: strongest signal on the page, a quarter or more of work, so it never wins on ratio and a README-driven plan never reaches it. Promote it when the project is being adopted as infrastructure rather than as a dependency, or when a foundation tier is the objection you keep losing to - then hand that decision to the user, because its reversibility cost is not a documentation cost.

Delete every signal answer 13 rules out instead of listing it as future work: no legal appetite means no foundation row, and a solo maintainer writes an honest support expectation rather than an empty governance heading.

## Step 9 - Re-score and test with a cold reader

Re-run the scorecard. The README passes when all five blocking checks pass and the scored checks total at least 14 of 16 - a working default here rather than a published bar, so let the user move it for a stated reason you record in the report.

Then run the cold-reader test defined in the scorecard - five questions, 60 seconds, five correct answers to pass - using a person if the user can find one, otherwise a fresh agent session with no repository context. Each wrong answer maps to a specific check, so a failure tells you exactly what to fix.

If your environment has persistent memory, store the agreed one-liner, audience definition, competitor list, and final score. Sibling work - launch posts, docs landing pages, conference abstracts - should start from that positioning rather than inventing a new one.

## What to track afterwards

Attribution on a README is weak. Record the ship date, compare a full period before against a full period after, and annotate confounders instead of claiming the delta. Re-measure four to six weeks out; shorter windows are noise.

- efficiency, track first: `support load > conversion rate > contributor conversion`

- **Support load** costs nothing to track and moves within weeks: count the "how do I install this" and "what does this do" issues per month and watch them fall.
- **Conversion rate** - clones or downloads divided by unique visitors - takes an hour to assemble from the host's traffic data and is the truest single number available, but says nothing until a full period has passed either side.
- **Contributor conversion** is slowest and most confounded; read it a quarter out.

Drop stars from the tracking plan entirely, even when answer 5 named stars as the goal: they only ever go up, so the metric cannot show a regression and reports success for a change that made the page worse. Offer the conversion rate instead.

If clones rise but contributor count does not, the contribution path is broken, not the README. Measurement surfaces and their caveats: [./references/tooling-and-measurement.md](./references/tooling-and-measurement.md).

## Common failure modes

**Rewriting before diagnosing.** A rewrite that fixes the prose and preserves the broken install has fixed nothing. In review mode, do not rewrite at all unless asked.

**Padding to look serious.** Half of all READMEs sit between 5 and 12 sections, median 7. A four-section README for a single-purpose project is complete; adding architecture and roadmap sections to a 200-line utility makes it look abandoned, not mature.

**Marketing voice.** Superlatives without evidence read as noise to this audience and actively lower trust. Every claim should be checkable or cut.

**Auditing only one render target.** The registry page frequently has more traffic and different rules. A README that only works on one host is broken for a large share of its readers.

**Fabricated status.** Never write "production ready", "battle-tested", or a user count you did not get from the user. An overstated claim is disproved by one glance at the commit history and costs more trust than an honest "early beta".

**Leading with the cheapest fix.** The badge row is the fastest thing on the list and nearly the least valuable. Present the order from Order the fixes, not the order you could finish first.

## Reference

- [./references/audit-scorecard.md](./references/audit-scorecard.md) - Rubric, thresholds, cold-reader test, and report format.
- [./references/published-findings.md](./references/published-findings.md) - Every sourced figure and the folklore list.
- [./references/readme-skeletons.md](./references/readme-skeletons.md) - Section orderings per project type.
- [./references/before-after-examples.md](./references/before-after-examples.md) - Worked positive and negative examples.
- [./references/tooling-and-measurement.md](./references/tooling-and-measurement.md) - Scoring, linting and attribution tools.
- [./scripts/readme-audit.sh](./scripts/readme-audit.sh) - Mechanical facts the scorecard depends on.
- samber/developer-relations-skills@developer-quickstart-guide - Dedicated getting-started page.
- samber/developer-relations-skills@developer-docs-structure-audit - Documentation site structure.
- samber/developer-relations-skills@oss-contributor-onboarding - CONTRIBUTING.md and first-contribution path.
- samber/developer-relations-skills@changelog-writing - Release notes and changelog structure.
- samber/developer-relations-skills@oss-launch - Launch planning and execution.
- samber/developer-relations-skills@oss-distribution-strategy - Which channels point readers at this repository surface.
