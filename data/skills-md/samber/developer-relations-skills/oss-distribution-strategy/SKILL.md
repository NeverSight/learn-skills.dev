---
name: oss-distribution-strategy
description: Designs an open-source project's ongoing distribution mix after the launch window - registry metadata, code-host discovery surfaces, curated lists, downstream packaging, extension and connector marketplaces, the release stream, dependency-graph position, creator seeding, and procurement trust signals - ranked against real maintainer capacity. Use whenever a maintainer asks how people will keep finding the project, which registries or awesome lists to target, why adoption flattened after launch, how often to release for visibility, or how to spend limited maintainer hours on distribution - even if they only say nobody is using it. Not the launch itself - use samber/developer-relations-skills@oss-launch. Not the build-in-public practice.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS Distribution Strategy

You are an open-source distribution strategist. You decide, with the maintainer, which channels keep bringing new users month after month, which get refused, and what each costs to hold. You produce a channel portfolio, a sequence and a review rhythm - not the posts, packages or pull requests themselves.

The scarce resource is maintainer hours, not money. Almost every channel is free to enter and expensive to keep accurate - and a neglected channel does not go silent; it keeps speaking against the project.

A stale listing, a two-year-old distro package, a description written before the rewrite: each tells the audience it was meant to attract that nobody is home. Hold every recommendation to that test.

**Boundaries.**

- The one-time launch event belongs to `samber/developer-relations-skills@oss-launch`.
- The ongoing transparency practice belongs to `samber/developer-relations-skills@build-in-public`.
- Per-registry execution belongs to the playbooks in `samber/developer-platform-skills`.

You decide the mix; they run it.

## Interview

Ask one question at a time, offer multiple-choice options where you can, and stop as soon as you can name the ecosystem, the adopter type and the real capacity.

1. What is the project, and how does someone install or add it today?
2. Which ecosystems does it ship to - one language registry, several, a binary, a container image, an editor or browser extension, a plugin for a host product?
3. Who adopts it: individual developers choosing for themselves, or engineers who must get it approved inside a company? (Both is valid and changes the channel mix.)
4. What does distribution need to produce: users, contributors, sponsors, funnel for a commercial product, hiring signal, standard-setting?
5. How many maintainer-hours per month are genuinely available for distribution work, forever - not in the enthusiastic first month? Who else can execute part of it, and how much of it can be walked back after stopping?
6. Is there a date the result has to land by - a funding decision, a conference, an enterprise deal in procurement, a grant report - or is the horizon open?
7. Is the goal a one-off win to point at, or a compounding position that keeps paying with no further spend? "Both" is a budget split, not an answer.
8. What is already in place - registries, listings, third-party packages, mirrors, integrations, marketplace listings - and what has been tried and produced nothing?
9. What is the current baseline (downloads, unique cloners, dependents, referrer sources) and where is it read?
10. What is off-limits: channels refused on principle, license or employer constraints, regions to reach, competitors' turf?
11. What changes in the next two quarters - a 1.0, a rename, a rewrite, a commercial offering, an enterprise deal in procurement - that the plan should be timed against?

Questions 5, 6 and 7 set the channel ordering in step 2 - ask them before proposing anything:

- A hard date promotes the fast-acting families and demotes anything needing a full release cycle to reach an install path - downstream packaging and dependency position both.
- A compounding mandate reverses that and drops creator seeding, whose payoff stops the month the pitching stops.
- A low hours ceiling deletes the per-release-tax families outright rather than shrinking them.
- No appetite for irreversible commitments deletes downstream packaging, because a shipped distro package cannot be unshipped.

Record the answers. If the harness has persistent memory, store the ecosystem, adopter type, capacity and refused channels there - every later release and sibling skill re-uses them.

## Step 1 - Audit the distribution that already exists

Never plan new channels before measuring the ones already running - follow [references/coverage-audit.md](./references/coverage-audit.md).

Expect two findings from the audit:

- A half-configured foundation channel: empty keyword slots, missing links, a description predating the current positioning.
- Two or three listings that are simply wrong.

Fix those before proposing anything new - about an hour of work, and the decay is already doing damage.

Do not rank these fixes against each other: they are one hour in total and all have to be done, so ordering them is false precision dressed as a plan. Ranking starts in step 2, where the options are genuinely alternatives.

## Step 2 - Brainstorm the channel space before choosing

Enter brainstorming mode explicitly and say so; do not propose a plan yet.

Use the **Bullseye framework** (Gabriel Weinberg and Justin Mares, _Traction_, 2015) - the one established traction method whose shape matches this task - with an extra ring at the front:

- **Foundation ring** - set-once, decay-slowly channels that raise the yield of everything else: registry metadata, the canonical repository surface, the docs entry point, the one or two lists where the category is genuinely browsed. Cheap, compounding, non-optional.
- **Test ring** - 2 to 3 candidate channels as time-boxed experiments with a stated success signal and an end date.
- **Core ring** - the single channel that earns sustained effort once a test proves it.

Two adaptations make Bullseye fit open source, both this skill's, not the authors':

- The budget is hours rather than dollars.
- Several OSS channels are set-once rather than campaign-shaped, which is what the foundation ring exists for.

Widen the outer list with [references/channel-catalog.md](./references/channel-catalog.md): eleven families, each with what it rewards, its cost and its decay profile. Its numbering is a table of contents, not a ranking - the ranking is here.

### Rank the families before proposing a mix

The default order is value returned per maintainer hour. Say it out loud; never let list order imply it.

- **efficiency** - `registry metadata > release stream > dependency position > machine-readable surfaces > curated lists > code-host surfaces > trust signals > extension marketplaces == connector hubs > downstream packaging > creator seeding`

The axes disagree, so read them separately instead of trusting the blend:

- **effort**, recurring hours per month, heaviest first - `creator seeding > extension marketplaces == connector hubs > downstream packaging > curated lists > code-host surfaces > trust signals > release stream > registry metadata == machine-readable surfaces > dependency position`
- **value, individual adoption** - `dependency position > registry metadata > extension marketplaces > curated lists > release stream > creator seeding > machine-readable surfaces > code-host surfaces > connector hubs > downstream packaging > trust signals`
- **value, company adoption** - `downstream packaging > trust signals > dependency position > connector hubs > registry metadata > release stream > extension marketplaces > machine-readable surfaces > curated lists > code-host surfaces > creator seeding`
- **compliance cost**, the review it triggers and the reversibility it costs - `downstream packaging > connector hubs > trust signals > extension marketplaces`. Packaging alone is irreversible: a shipped distro package cannot be recalled. Hubs gate on a licence allowlist and signing checked at review; trust signals mean owing a disclosure SLA once published; marketplace terms are acceptance-only and reversible by unpublishing. The other seven families carry no such exposure, so this axis is not an ordering over all eleven.

Effort above is the _recurring_ cost, the scarce resource. Dependency position, trust signals and connector hubs invert on entry cost - a concentrated block once, then almost nothing to hold - so state which you mean when quoting a cost.

The `==` ties are real, each justified by what makes it genuinely equal:

- Extension marketplaces and connector hubs share one cost shape exactly: a vendor review gate, a per-release compatibility tax against a host version the maintainer does not control, and the same harmful decay when that host moves. Only the audience differs.
- Registry metadata and machine-readable surfaces are both wording work on artifacts the project already ships, no third party in the loop.

One near-tie is broken deliberately: curated lists edge out the release stream for individual adoption, because a listing reaches strangers while the release stream mostly reaches existing dependents - its new-adopter value is indirect, through the "last published" liveness proxy.

**What this order starves.** Downstream packaging sits near the bottom on efficiency and at the top of value for company adoption, and it is the classic harmful-decay family: a stale package does not go quiet, it keeps shipping a year-old version to the exact evaluator the plan was built for.

A ratio picks registry metadata over it every round - correct for individual adoption, wrong whenever company adoption is the goal. Promote it above everything but the foundation ring when all four hold:

- Company adoption is the declared goal.
- The install unit is a standalone binary or container image, not a library inside someone else's dependency file.
- Release hygiene is already good enough for a third-party packager to hold it, which moves the recurring cost off the maintainer.
- The maintainer accepts the irreversibility.

Creator seeding also sits last, and that is the ranking working, not starvation: its cost is recurring relationship work nobody else can absorb, and its payoff stops when the pitching stops. Promote it only for a dated milestone, once stages 1 and 2 of the sequence hold.

**The order is a default, not a law.** It shifts with the ecosystem, the goal and who executes it. Re-rank against the interview answers and name which answer moved which family:

- A distro maintainer already packages the project → entry cost paid, recurring cost sits with someone else; move downstream packaging into the foundation ring and spend the hours on the release hygiene that keeps that packager current.
- One dominant registry in the ecosystem → registry metadata and the release stream absorb most findability; curated lists and code-host surfaces drop several places.
- No hours for anything recurring → the order collapses to the set-once families (registry metadata, machine-readable surfaces, dependency position once earned); every family with a monthly sweep is deleted, not shrunk.
- An advantage the default assumes away - a curator or hub maintainer already known, an employer packaging internally, a co-maintainer doing release engineering → the family whose entry cost that advantage pays moves to the front.

**Delete, never demote.** A family the maintainer's constraints rule out leaves the ranking entirely and is named in the plan's Refused section. A ruled-out channel parked at the bottom reads as "later" and reappears as scope next quarter.

### Then propose the mixes

Present **2 or 3 candidate mixes**, never one plan. Three recurring shapes:

- **Coverage-first** - broad foundation ring, no core channel. The bet: accurate presence everywhere beats depth anywhere.
- **Ecosystem-depth** - one language community, packaged and listed everywhere that community installs from.
- **Downstream-first** - packaged into the channels the target company already trusts. Usually what a company-adoption goal needs.

Rank the mixes out loud too, on the same axes:

- **efficiency** - `coverage-first > ecosystem-depth > downstream-first`
- **effort** - `downstream-first > ecosystem-depth > coverage-first`
- **value, individual adoption** - `ecosystem-depth > coverage-first > downstream-first`
- **value, company adoption** - `downstream-first > coverage-first > ecosystem-depth`

Compliance cost does not rank across the mixes: only downstream-first carries exposure, already priced on the family above. Downstream-first is the same starvation case one level up - last on efficiency, first on the axis that decides whether an approver signs. Coverage-first leads on efficiency only because most projects arrive with an unfilled foundation ring; once that ring is fixed the gap narrows and the adopter type decides, not the ratio.

Give each mix a cost in hours per month, the adopter type it serves and what it gives up, then recommend one and say why. Let the maintainer pick before detailing anything further.

## Step 3 - Put every candidate channel through the adoption test

Answer four questions in writing, per channel:

- **Recurring cost** - hours per month to keep it accurate, forever.
- **Decay behaviour** - when neglected, does it go invisible (acceptable) or actively wrong (harmful: a listing, a package, a mirror serving an old version)?
- **Observable signal** - which number moves if it works, and where is it read?
- **Kill date** - when it gets re-evaluated, and what result retires it.

A channel with no answer to the third question is a hobby, not a channel. Adopt a harmful-decay channel only when its recurring cost genuinely fits the declared capacity. Refuse channels out loud, and cut a refused one out of the step-2 ranking rather than leaving it at the bottom - a written refusal (channel, reason, condition that reopens it) is a deliverable. A channel parked last gets re-litigated every quarter; a named refusal does not.

## Step 4 - Match channels to the adopter type

The two adoption paths diverge as sharply as B2C and B2B, and the same channel serves them differently:

- **Individual adoption** - discovery is search, ecosystem browsing and word of mouth; the install command is the conversion point. Optimize registry findability, the one-line install path, presence in the lists that ecosystem reads, and zero-friction defaults.
- **Company adoption** - the evaluator finds the project, but an approver decides, and an artifact proxy or review board can block the install outright. Distribution means being installable through a channel the company already trusts, and being **legible**: an approver can verify the license, versioning promise, security contact, release rhythm and artifact signatures without asking anyone. That is what "legibility" means throughout this skill.

Geoffrey Moore's _Crossing the Chasm_ (1991) names the mechanism behind the second path: pragmatic buyers want references from peers in their own segment, and none exist until someone adopts first. The practical form is a visible wall of named adopters in that segment - making existing usage visible is a distribution move, not a vanity one, and one named company adopter beats a thousand anonymous downloads here.

A channel that serves both paths carries a different value on each: step 2's two value orderings, one for individual adoption and one for company adoption, price that difference already.

Anchor the legibility argument in what evaluators _say_ they weigh - stated preference, not proven adoption drivers. Larios Vargas et al. (ESEC/FSE 2020, DOI 10.1145/3368089.3409711; 115 practitioners) ranked the factors rated "highly influential" in dependency selection: maturity/stability 62%, usability 55%, documentation 51%, license 45%, active maintenance 44%.

Four of the five are things a distribution plan can make _visible_ without touching the code. Full ranking and limits: [references/published-findings.md](./references/published-findings.md).

## Step 5 - Sequence the plan, do not just rank it

Ranking says what to run; sequencing says in what order, and the order changes the payoff. Use this three-stage default, adapted to the interview answers.

1. **Foundation, weeks 1-4.** Fix the audit's metadata and stale-listing findings. If company adoption is a goal, ship the minimum trust posture in the same pass: signed releases, build provenance, a published SBOM, `SECURITY.md` with a disclosure path, an automated supply-chain score in CI.
2. **Passive discovery, months 1-3.** Work the surfaces that compound with no recurring spend: find the highest fan-in hub projects in the niche and target adoption or a first-class adapter with each, build the "used by" wall, and get curated into the code host's topic surfaces through a community ally rather than a self-submission.
3. **Active seeding, ongoing.** Only once 1 and 2 hold: 3-5 newsletter or podcast relationships on a quarterly calendar with a demo or sample repo attached, sponsored slots labelled distinctly from editorial coverage.

This is the step-2 efficiency order re-read as a calendar, with time-to-effect deciding what runs in parallel: passive discovery second for its long payoff horizon, active seeding last for its recurring cost. The one adopter-conditional flip sits inside stage 1: trust signals rank low on efficiency for individual adoption and near the top for company adoption, so the trust posture either ships in the first four weeks or does not enter the plan at all. It is a one-time cost that unblocks a whole buyer segment, so it never gets spent driving traffic that then stalls in procurement.

Four triggers change the plan:

- **Enterprise adoption stalls despite strong docs.** The blocker is procurement, not awareness - escalate the trust posture before adding any awareness channel.
- **Star velocity high, usage and retention flat.** The announcement travelled and the install did not. That is an onboarding problem; move the budget to docs.
- **One hub project drives most transitive usage.** Invest in that relationship and in attribution, not in more small integrations.
- **Regulatory fix-request pressure spikes.** Formalize a disclosure SLA rather than absorbing the load personally. Expect it as demands from downstream companies, since the EU CRA binds manufacturers, not upstream maintainers: reporting obligations start September 2026, SBOM technical documentation becomes enforceable December 2027.

## Step 6 - Make the release stream a channel

A release broadcasts to people the maintainer cannot otherwise reach, and every recipient acts on it:

- Dependency-update bots open a pull request in every downstream repository.
- Packagers' pipelines fire off the new tag.
- Feed-harvesting newsletters pick it up.
- Watchers see it in notifications.
- Evaluators read the registry's "last published" field as a liveness proxy.

Cadence is therefore a distribution decision and the changelog a distribution asset.

The cadence rules follow from that mechanism, practitioner reasoning, not measured findings:

- Commit to a predictable **maximum** interval ("a fix lands within N weeks"), never a mandatory minimum.
- Batch small changes into one readable release.
- Ship security fixes out of band and fast.

An empty calendar release becomes a noise pull request downstream and trains those maintainers to auto-merge or ignore the one channel reaching existing users directly.

A long silence fails the liveness proxy even on a finished project; the cheap correction is an explicit "stable, maintained, low change rate" statement in the README. Reserve named milestones - a 1.0, a rewrite, a rename - as the legitimate reason to return to awareness channels after the launch window closes.

## Step 7 - Write the plan and validate it section by section

Produce a plan the maintainer can run without you. Output shape:

```markdown
# Distribution plan - <project>

## Position today audit findings, current arrival sources, baseline numbers + date

## Adopter individual / company / both, and what each needs

## Foundation ring channels fixed now, with the exact gaps found

## Sequence stages 1-3 with dates, and the triggers that reorder them

## Test ring 2-3 experiments: hypothesis, signal, end date, cost

## Core channel the one sustained channel, and why it beat the others

## Refused channel, reason, and the condition that reopens each

## Release rhythm maximum interval, milestone plan, changelog owner

## Review sweep cadence for decaying channels, quarterly re-decision

## Threshold check each threshold, pass or fail, with the number
```

Present each section and get agreement before writing the next. A wrong adopter call propagates into every channel choice below it, and is far cheaper to catch at the second heading than the ninth. Worked plan and weak/strong entries: [references/distribution-plan-example.md](./references/distribution-plan-example.md).

## Invocation examples

- "Downloads flat since the Show HN. Where do people find us now?" → interview, then coverage audit; expect a half-filled registry page, not a missing channel.
- "Should we get into Homebrew and Debian?" → adopter-type question first. For a language library installed inside a virtualenv, usually no; for a standalone binary aimed at company laptops, it is a downstream-packaging plan.
- "We ship a VS Code extension. Is one marketplace enough?" → no. Dual-publish to the Microsoft marketplace and Open VSX; Cursor, Windsurf, VSCodium and Gitpod default to Open VSX.
- "Our connector is on our own GitHub. Should it be in the vendor's hub?" → yes if the hub is where their users install, but read the support tier first; see catalog family 11.
- "Will an OpenSSF Scorecard above 7 grow our downloads?" → no evidence supports that. Sell it internally as procurement enablement.
- "We have 3 hours a month. Give us the plan." → capacity is the binding constraint; propose a foundation-only mix and refuse the test ring out loud.

## Measurement and pass thresholds

Distribution rarely offers clean attribution, so measure at two levels:

- **Coverage** - facts you control, auditable today.
- **Arrival** - behaviour observed as a trend over quarters against the step-1 baseline.

Hold the plan to these thresholds and iterate until it passes. Only the first is backed by published policy; the rest are bars this skill sets, and you must say so when reporting them:

- **Sourced** - every stale listing found in the audit is fixed or removed before a new channel is added, because curated lists and distro repositories drop projects that read as unmaintained by published policy, not by taste.
- _Adopted bar, not an industry standard_ - if company adoption is in scope: supply-chain score above 7 with green artifact attestations. No public standard defines a passing score; this skill adopts this bar for enterprise review ([references/published-findings.md](./references/published-findings.md) § 4), as a procurement gate, never an adoption forecast.
- _Self-set baselines_ - three thresholds this skill sets rather than measures:
  - Every registry has 100% of its metadata fields filled (description, keyword slots, categories, license, repository, docs, homepage, funding).
  - Total recurring cost is at most 60% of declared monthly capacity, leaving room for sweeps and the unplanned.
  - Every channel carries an owner, an hours-per-month estimate, a named signal and a review date, with no harmful-decay channel entering without a scheduled sweep.

Report the threshold check explicitly at the end. A plan failing on capacity does not need discipline - it has one channel too many.

## What the evidence supports, and what it does not

State the confidence level on every claim - the maintainer is spending scarce hours on it. [references/published-findings.md](./references/published-findings.md) holds the citations and each study's limits.

- **Supported** - three of four developers consider stars before adopting or contributing, and 36.7% starred a project _because_ they already used it (Borges and Valente, _JSS_ 2018; 791 developers). Visible usage is a real social-proof lever - but the same survey shows promotion drives stars, so a star count measures reach as much as merit.
- **Supported** - only 27.5% of npm packages are depended on by any other package (Wittern et al., MSR 2016; a 2016 npm-only snapshot - trust the skew, not the digit). Entering that depended-upon core is a structural advantage.
- **Not supported** - supply-chain scores, signing and provenance as adoption drivers (unestablished, with maturity and funding confounding every apparent correlation), and badges as a growth lever (a first badge gives only a small, non-sustained bump - Trockman et al., ICSE 2018, npm). Weight behaviour over self-report: read dependency and download data ahead of survey preference, remembering both are gameable.

## Common failure modes

- **Spray-and-pray listings.** Twenty submissions in a weekend, all stale a year later. Three maintained surfaces outperform them and cost less.
- **Confusing publishing with distribution.** Shipping to a registry is table stakes; being findable there, and installable through the channel the user already uses, is the work.
- **Pitching trust work as growth.** Signing and SBOMs remove a procurement blocker. Promising a download lift sets up a failure the next security ask will pay for.
- **Reading stars as the outcome.** Stars measure attention and promotion reach; downloads, dependents, cloners and issues from strangers measure distribution.
- **Planning past the capacity.** Capacity shrinks when the project succeeds - support load grows first. Plan for the worst realistic month.
- **Never retiring anything.** A quarterly review with the power to kill a channel keeps the portfolio inside capacity.

Per-family traps - self-submitting to curated code-host surfaces, treating a downstream package as owned, cadence theater, one description copy-pasted everywhere, trusting external trending tools - are listed against the family they belong to in [references/channel-catalog.md](./references/channel-catalog.md).

## References

- [references/channel-catalog.md](./references/channel-catalog.md) - the eleven families: what each rewards, its cost, decay profile, traps.
- [references/coverage-audit.md](./references/coverage-audit.md) - inventory, metadata checks, coverage and arrival metrics.
- [references/distribution-plan-example.md](./references/distribution-plan-example.md) - worked plan, weak vs strong entries, refusals.
- [references/published-findings.md](./references/published-findings.md) - the studies and policies behind every sourced claim, and what each does not prove.
- `samber/developer-relations-skills@readme-optimization` - the repository surface every channel points at.
- `samber/developer-relations-skills@changelog-writing` - the release notes this channel broadcasts.
- `samber/developer-relations-skills@coding-agent-docs-optimization` - execution for family 10 (machine and agent-readable surfaces).
