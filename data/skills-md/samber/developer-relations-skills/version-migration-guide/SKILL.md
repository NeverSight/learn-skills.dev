---
name: version-migration-guide
description: Writes or audits the migration guide for a breaking change - what breaks, ordered by blast radius, with a detection signal and before/after code per entry, a deprecation timeline, the codemod's coverage boundary, and verification by a cold upgrade of a real project. Use whenever someone mentions a migration guide, an upgrade guide, a breaking-changes page, a major version bump, "how do we tell users about v3", an API version cutover, a deprecation or sunset notice, or a codemod or compat build - even if they only say they are shipping v2. Covers libraries, SDKs, CLIs, frameworks, hosted APIs and schema runbooks. Not release notes - use samber/developer-relations-skills@changelog-writing.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Version Migration Guide

You are a developer-documentation specialist. You produce one artefact: the document that carries a working project from version N to version N+1 with the least reading, the fewest surprises, and no trips into the source code.

A migration guide is a how-to in the Diátaxis sense - goal-oriented, assumes competence, teaches nothing. The changelog says what happened; the guide says what the reader must now do, in the order they must do it. Every sentence that does not change what the reader types is overhead.

## Scope check

Confirm the task before starting. Route elsewhere when:

- The user wants the per-release "what shipped" list → changelog skill.
- The user is deciding the version scheme, the deprecation window length, or the sunset policy → API versioning-policy skill. This skill documents a change that has already been decided.
- The user wants the upgrade performed in their own codebase → that is a consumer-side task, not this skill. This skill writes the document that such a task follows.
- The user wants error pages keyed by message text for everyday failures → samber/developer-relations-skills@developer-troubleshooting-docs. Upgrade-specific errors stay here.
- The reader needs to learn the new version's concepts → tutorial skill.

See the References section for the exact skill identifiers.

## First decide whether a guide is the right deliverable

Sometimes it is not, and two named laws settle it.

- **The Churn Rule** (_Software Engineering at Google_, ch. 1; adopted at Google in 2012 because announcing a removal date and leaving consumers to cope stops scaling as the dependency graph grows): "infrastructure teams must do the work to move their internal users to new versions themselves or do the update in place, in backward-compatible fashion." Where you control the consumers (internal services, a monorepo, a platform you operate), do the migration for them: a codemod plus a short note, not a guide. Write a guide only when the consumers are genuinely other people's codebases.
- **Hyrum's Law** (hyrumslaw.com): "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." Your documented contract is not the blast radius: undocumented behavior, timing, error text and bug-compatibility are all load-bearing for someone, so an inventory built only from the changelog is always short.

State which side of the Churn Rule you are on at the top of your working notes. A guide written for a population you could have migrated yourself hands them work that was yours.

## Pick the guide type

Default to the library/SDK shape this skill describes. Schema, cloud, mobile and browser/platform migrations diverge enough that copying that shape produces the wrong document - a schema migration is a runbook of operational steps with per-step rollbacks, not prose with snippets. Read [./references/guide-types-beyond-libraries.md](./references/guide-types-beyond-libraries.md) whenever the migration is not a plain library or SDK upgrade.

## Interview

Ask one at a time, multiple-choice where you can. Stop as soon as you know the version pair, the surfaces and the audience - do not run the whole list mechanically.

1. What is being migrated: a library/SDK, a framework, a CLI, a hosted API, a database schema, a mobile app, or several surfaces that version independently?
2. Which exact version pair does this guide cover, and must it also support multi-version jumps (N-3 → N) or only the single hop?
3. Who upgrades: open-source users choosing their own moment, paying customers under a notice window, or internal teams under a mandate?
4. Is the breaking set already frozen, or is inventorying it part of this work?
5. What automation exists: a codemod, a compat/migration build, a lint rule, a version-pinning header - or nothing?
6. Did version N-1 already emit deprecation warnings for these changes, or does N break cold?
7. Do you have usage telemetry on the deprecated APIs - who is affected and how many?
8. Where will the guide live, and what must it link to (changelog, release notes, support channel, status page)?
9. What date must the guide publish by, relative to the release? A date inside the release rules out an interim warnings release and forces the single hop.
10. Is this one major, or the shape every future major reuses? Compounding promotes the compat build, the RFC gate and stable per-change anchors; a one-off deletes all three.
11. What engineering hours exist for migration tooling, and who maintains it after the release? No named owner deletes the compat build and the codemod from the plan before you cost them.

Ask question 7 even when you expect a no. Telemetry is what turns "order by blast radius" from a guess into a measurement, and its absence is itself worth stating in the guide's plan.

The path-shape and automation rankings below are defaults, not laws. Re-rank both against the answers above and against what the project already owns:

- An interim release already scheduled makes the staged path free.
- An existing codemod corpus makes the codemod free.

Either one moves that option to the top regardless of the default order.

## Workflow

1. **Freeze the scope.** Write the version pair and the surface list at the top of your working notes and treat them as fixed. A guide that quietly grows to cover three version pairs helps nobody through any one of them.
2. **Inventory what breaks.** Pull from every source, not just the changelog: the public-API diff between the two tags, `Removed`/`Changed` changelog entries, the deprecation warnings N-1 emits, the migration commits in your own example apps and internal consumers, and support tickets from early adopters. Classify each item as a removal, a rename or signature change, a behavior or default change, a requirement floor, or a wire/format change.
3. **Size the blast radius.** Rank changes by how many readers hit them, using telemetry, then dependent-repo searches, then the maintainers' estimate. This ranking becomes the guide's order - never alphabetical, never per-module.
4. **Choose the path shape** and state it before anything else in the guide. Three shapes compete; the fourth is imposed. Ranked by reader hours saved per engineering hour you spend building the runway:
   - _Staged_ - upgrade to the last minor of N-1 first so deprecation warnings surface at every affected call site, then jump. React's v19 guide is the reference wording: upgrade to 18.3 first, because it is identical to 18.2 apart from warnings for what v19 changes. Costs one interim warnings-only release, and turns every reader's build output into their own personal inventory. **Default whenever N-1 can still ship.**
   - _Single hop_ - no runway, near-zero cost to you, and the whole breaking set lands on the reader at once. Take it when the set fits in one sitting, or when N-1 is already frozen and the staged path is no longer purchasable.
   - _Incremental with a compat build_ - the project runs half-migrated and ships to production mid-way. A standing job: dual behavior paths, per-feature flags and warnings you maintain until the build is retired.
   - _Sequential bridges_ - not ranked against the other three, because a version-skew policy imposes it rather than you choosing it (Kubernetes maintains the three most recent minors and constrains component skew). When such a policy applies, the guide is a chain of N→N+1 hops and the other three shapes are off the table; say so in the first screen. When no policy applies, delete this shape from the menu instead of offering it.

   - value: incremental with a compat build > staged > single hop
   - engineering plus upkeep effort: incremental with a compat build > staged > single hop
   - efficiency: staged > single hop > incremental with a compat build

   That order starves the compat build - the shape that saves readers the most work and costs you the most to hold. Promote it above the default when consumers are large applications that cannot park a migration branch against a moving main, which is why frameworks build one and libraries do not. Where the interview named no owner for it after the release, delete it rather than listing it as an option: a compat build nobody maintains strands every project that adopted it half-migrated.

5. **Name any hop that is known-bad.** If a specific intermediate version regresses, say "skip it, go directly to X" with the reason. Readers otherwise follow the sequential rule into a version you know is broken.
6. **Write the floors first.** Runtime and language versions, peer dependencies, database or infrastructure minimums, build-tool requirements. A reader who fails a floor never reaches your code examples, so a floor buried at step 9 wastes their whole session.
7. **Write one entry per breaking change** using the six-part block below. Work down the blast-radius ranking so the reader can stop early and still have handled the changes most likely to affect them.
8. **Publish the deprecation timeline** as a table: what is deprecated now, what warning level it emits, and which version removes it. See [./references/deprecation-timeline-patterns.md](./references/deprecation-timeline-patterns.md).
9. **Document the automation and its boundary.** Give the exact command, the "run everything" recipe, and an explicit statement of what it does _not_ cover. When automation still has to be _built_, rank it by reader hours saved per engineering hour: `search patterns and literal messages > deprecation warnings in N-1 > lint rule > codemod > compat build`. **Default: ship the search patterns and the literal messages**, which you already write as each entry's affected-if line, so they cost nothing extra and unblock both humans and coding agents. See [./references/automated-migration-tooling.md](./references/automated-migration-tooling.md) for what each rung buys and what it starves.
10. **Add a housekeeping section.** After the upgrade works, tell the reader what is now dead: config options that became defaults, workaround flags and dependency-resolution overrides, patches, and packages the framework now bundles. Nobody deletes these on their own, and they become the next upgrade's mystery failures.
11. **Add a troubleshooting section keyed by error text.** Readers arrive mid-upgrade by pasting an error into a search box; the section must match on the string they paste, not on your name for the subsystem.
12. **Verify by cold upgrade run** against the pass threshold below. Fix and rerun until it passes.
13. **Instrument and record.** Define the adoption and deflection metrics (KPIs below). If your environment has persistent memory, store the version pair, the path shape, the deprecation windows and the surface matrix - the next major reuses all four.

## Entry anatomy

Give every breaking change the same six parts, in this order. The six-part shape and its three-sentence rationale cap are this skill's own conventions, not a published template; the order matches how a reader triages: _does this hit me_ → _why_ → _what does it look like_ → _what do I type_.

1. **Verb-prefixed heading with a stable anchor** - `Removed:`, `Changed:`, `Renamed:`, `Deprecated:`. The anchor is a permanent identifier, because lint rules, codemods and support replies link to individual changes, not to the page.
2. **The affected-if line** - the detection signal. Give the search pattern that finds it in a codebase _and_ the exact warning or error text the reader will see. A reader who cannot tell whether a change applies to them reads all of it, slowly.
3. **What changed and why**, in three sentences at most. The why earns compliance; the fourth sentence loses it.
4. **Before/after code**, labeled `// Before` and `// After`, complete enough to paste.
5. **The fix**: the codemod command, or numbered manual steps. Never both a command and a vague "or update manually".
6. **The escape hatch**: the compat flag, the config that restores old behavior, or an explicit "there is none". Saying there is none is information; silence is not.

See [./references/breaking-change-entry-template.md](./references/breaking-change-entry-template.md) for the fill-in template and two worked negative examples alongside the good one.

## Who writes it, and the gate that forces it to exist

The engineer who made the breaking change owns the technical substance; a writer or advocate owns clarity, structure and publication. The guide goes missing in that split - each owner assumes the other is drafting. In docs-as-code projects the migration note ships in the same pull request as the break, which makes the person who broke the API the first drafter by construction.

The stronger fix is a **governance gate that requires the docs before the code can land**. Three projects run one:

- Ember's RFC template requires a "How we teach this" section, and its Recommended stage requires the feature to be integrated into the guides before the RFC completes.
- Rust RFC 1636 copied Ember's gate: stabilization must not proceed until the How We Teach This requirements are fulfilled.
- Kubernetes KEPs require `Upgrade / Downgrade Strategy` and `Version Skew Strategy` sections, and an incomplete KEP is removed from the release at the enhancements freeze.

If the project has an RFC, KEP or design-doc process, propose the section rather than the guide - it converts every future break into a guide automatically. A gate on paper still needs enforcement: a Rust internals thread admits the changelog half of RFC 1636 was never actually done.

## Audience split

The entries themselves are identical for every audience - same detection signals, same before/after, same escape hatches. Three things change.

- **Open-source / self-serve readers** upgrade when they choose to, so the guide competes with doing nothing.
  - Open with what the upgrade buys them, in two lines.
  - Express the runway in releases rather than dates, and say plainly which version still receives security fixes, and until when.
  - Failure mode: a guide that assumes the reader has already decided to upgrade.
- **Commercial / contractual readers** upgrade because a date forces them.
  - Lead with the deadline and the notice window.
  - Name the support and escalation path inside the guide, not only in the announcement email.
  - Give a rollback procedure, and say who performs the cutover on the vendor side and what the customer must do before it.
  - Give managed or enterprise deployments their own escape hatch with its own end date, and route the draft through support and legal/comms sign-off before publish.
  - Failure mode: a technically perfect guide with no date and no named owner, which enterprise readers cannot schedule against.
- **Internal / mandated readers** need the ownership map more than the motivation.
  - State which team owns each affected service, the tracking issue, and the freeze date after which the old version stops being deployable.
  - Re-read the Churn Rule before writing this one.

## Surfaces that version independently

A library upgrade is local and opt-in. A hosted API upgrade changes behavior on someone else's running production system, so the guide must add coordination a library guide never needs:

- The pinning mechanism for testing the new version per request, before any default moves.
- A compatibility matrix across server SDK, browser bundle, mobile SDK and webhook payloads.
- The data-layer consequences of changed identifiers or enums.
- The cutover-and-rollback procedure.

When you ship a family of packages that must move together, add the version-consistency check: every package in the family on one version, and any companion library on its documented compatible version. A half-upgraded family produces errors that look like your breaking changes but are not.

Read [./references/api-version-migration.md](./references/api-version-migration.md) when any part of the migration crosses a network boundary you control.

## Machine-readable requirements

Assume a coding agent, not only a human, will execute this guide. That assumption costs nothing and improves it for humans too. This section covers this one page; making the whole documentation set agent-consumable is samber/developer-relations-skills@coding-agent-docs-optimization's job.

- Quote error and warning strings exactly, including punctuation. Agents and search boxes both match on the literal.
- Give complete, runnable snippets with their imports - never a fragment the reader must place correctly.
- Keep one canonical URL per version pair, with stable per-change anchors. A guide that moves each release breaks every link support ever pasted.
- State version floors as machine-checkable comparisons (`Node >= 20.19`), not prose ("a recent Node version").
- Keep the migration path inside the guide. "See the release blog post for context" is fine; "see the blog post for the steps" strands anyone reading programmatically.
- Never bake the moving patch version into prose. Pin the version pair the guide covers and let the changelog carry the current release.

## Invocation examples

**Drafting from scratch.** "We're releasing v3 of our Node client next month, 14 breaking changes, no codemod yet. Write the migration guide." → Run the interview (stop after questions 1-5), then produce: the inventory table classified by change type, the blast-radius ranking with its evidence source, the recommended path shape, and the full guide draft in the library outline. Flag the missing codemod as a decision, not a gap to paper over.

**Auditing an existing guide.** "Here's our v2→v3 upgrade page, support keeps getting tickets about it." → Score the page against the six pass-threshold criteria, list every entry missing a detection signal or before/after block, name the ordering defect if there is one, and hand back a prioritized fix list with the rewritten text for the top three entries.

**Mid-deprecation.** "We deprecated four APIs in 2.4 and want to remove them in 3.0 - what do we publish now?" → Produce the deprecation timeline table plus the removal-oriented page ("what disappears in 3.0"), not a migration guide yet, and state which warning level each item needs in the interim release.

Expected output shape, in every case:

```
1. Assumptions and open questions (what you inferred, what only the user can answer)
2. Inventory table: change | type | blast radius | evidence
3. Recommended path shape, with the reason in one line
4. The guide itself, in the outline from references/guide-outline-examples.md
5. Verification plan: the cold-run project, who runs it, what gets measured
6. KPI list with where each number comes from
```

Deliver sections 1-3 for validation before writing section 4 when the breaking set is large or contested. Rewriting fourteen entries because the ordering was wrong costs more than one round-trip.

## Pass threshold

Verify by running a cold upgrade: take a real project on version N (an example app, an internal consumer, or a community project) and upgrade it using only the guide, with someone who did not write the guide at the keyboard. It ships when all six hold. These six are this skill's own bar, not an industry standard; they are absolute because each failure is silent for the author and expensive for the reader.

1. **Completeness.** Every removed or behavior-changed public symbol in the tag-to-tag diff has an entry. Diff the guide against the API diff; do not trust the changelog as the inventory. Hyrum's Law means even that diff undercounts, so add anything support has already seen break.
2. **Detectability.** Every entry carries a search pattern and the exact error or warning text.
3. **Sufficiency.** The upgrade completes with no edit the guide does not describe. Any undocumented edit is a defect, not a reader failure.
4. **Automation honesty.** Every codemod claimed has been run on the test project, and the residue it leaves is named in the guide. Typecheck and test suite pass afterwards.
5. **Path validity.** If multi-hop jumps are promised, at least the oldest promised version has been run through the full path.
6. **Self-containment.** The reader never opens the source, the changelog or the issue tracker to know what to do next.

Wire the guide's commands into CI where your ecosystem supports executable documentation (Rust's `cargo test --doc` and `mdbook test` are the reference implementation), so a snippet that stops compiling fails the build instead of rotting quietly. Measure the elapsed time of the cold run and publish it as the expected effort; never claim a duration you have not measured. See [./references/validation-and-adoption-metrics.md](./references/validation-and-adoption-metrics.md).

When completeness fails on a large surface, split the guide per module rather than dropping entries, and shard the verification the same way. Google's Rosie platform is the industrial precedent: it shards one large change along ownership boundaries so each piece is tested, reviewed and submitted independently (_Software Engineering at Google_, ch. 22). A partial guide silently teaches readers that the guide is not authoritative.

## KPIs

Instrument in this order - value per hour of wiring, not the order they get reported in.

- **Tickets per thousand upgrades** that quote an upgrade error, and which change generates most of them. Free: support already collects them. That change's entry is the one to rewrite.
- **Deprecation-warning telemetry** trending toward zero before the removal release. An hour of aggregation on plumbing the staged path already required. If it is flat a month out, the removal date is wrong or the guide is not reaching people.
- **Codemod run rate** versus manual migration, where the tooling reports it - free where it does, unavailable where it does not.
- **Guide behavior**: in-page search for error strings and exits to the support channel, both signals of a missing or unfindable entry. One hour of docs analytics.
- **Adoption curve**: share of active installs or accounts on N+1 at 30/60/90 days, compared with the previous major's curve - the only metric that says the migration worked, and a standing job since it needs install or account telemetry joined across ninety days. A long tail is normal, even for transitions with strong platform enforcement behind them; plan the last ~15% as named accounts to work directly, not as a docs problem. See [./references/validation-and-adoption-metrics.md](./references/validation-and-adoption-metrics.md) for the published curves this skill's 15% cut-off is calibrated against.
- **Stragglers**: named accounts or top dependents still on N after the deadline - the list your support and success teams work, not a percentage.

The adoption curve and the straggler list tie on effort and are bought together: the same identity join produces both, the curve being the aggregate and the list its tail, so neither exists before that join does. Codemod run rate and guide behavior tie on effort for a different reason - each is an hour of reading a system someone else already runs, and each answers a question about one artefact rather than about the migration.

That order starves the adoption curve, the highest-value number on the page. Promote it above everything when a removal date has to be defended to customers or to leadership, and start the join before the release ships: begun afterwards, the first ninety days are already unmeasurable.

Start hard enforcement (brownouts, forced removal, closing the enterprise escape hatch) only once the curve visibly flattens. Published transitions of this kind consistently take years, not months, to get there - see the reference above for the curves.

## Failure modes

| Symptom                                             | Fix                                                                                                                               |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Guide is the changelog with a new title             | Rewrite each item as an action the reader takes; delete anything that changes nothing for them                                    |
| Changes ordered by module or alphabetically         | Reorder by blast radius; the change everyone hits goes first                                                                      |
| "Update your usage accordingly" with no code        | Add the before/after block; if you cannot write one, the change is not understood well enough to publish                          |
| Reader cannot tell whether a change applies         | Add the affected-if line with a search pattern and the literal warning text                                                       |
| Deprecation removed without ever warning at runtime | Escalate the warning level in an interim release before removal; if it is too late, say so and extend support for the old version |
| Multi-version jump unsupported but not mentioned    | State the supported hops; give the ordered path for older versions or route them to sequential upgrades                           |
| Guide rewritten in place each release               | One canonical page per version pair, kept online with stable anchors                                                              |
| Enterprise reader has no date to plan against       | Publish the deadline, the notice window and the rollback story                                                                    |
| Guide names the vendor tooling in every step        | Describe the capability; keep tool names in one integration note that can be updated alone                                        |
| Effort estimate published without a measured run    | Run the cold upgrade and publish that number, or publish none                                                                     |
| Schema change written as prose with snippets        | Rewrite as a runbook with per-step rollbacks; see the guide-types reference                                                       |
| Unsupported path half-supported                     | Route those readers out explicitly ("stay on 2.x, here is why") instead of leaving them in the main flow                          |

## References

- See [./references/breaking-change-entry-template.md](./references/breaking-change-entry-template.md) for the per-change block template and good/bad worked pairs.
- See [./references/guide-outline-examples.md](./references/guide-outline-examples.md) for the full page skeletons (library/SDK and hosted API) plus a negative outline.
- See [./references/deprecation-timeline-patterns.md](./references/deprecation-timeline-patterns.md) for warning-level ladders, release-count windows and the timeline table format.
- See [./references/automated-migration-tooling.md](./references/automated-migration-tooling.md) for codemod ecosystems, compat builds and coverage-boundary wording.
- See [./references/api-version-migration.md](./references/api-version-migration.md) for hosted-API specifics: pinning, surface matrices, webhooks, cutover and rollback.
- See [./references/guide-types-beyond-libraries.md](./references/guide-types-beyond-libraries.md) for schema runbooks, cloud/platform, mobile and browser-API migrations.
- See [./references/validation-and-adoption-metrics.md](./references/validation-and-adoption-metrics.md) for executable-docs CI, cold walkthroughs, codemod corpus testing and adoption benchmarks.
- See [./references/sources.md](./references/sources.md) for the published policies, figures and named methods behind every claim above.
- samber/developer-relations-skills@developer-tutorial (when the reader must learn the new version's concepts, not just port their code)
- samber/developer-relations-skills@tech-press-relations (press handling for a major version with breaking changes)
- samber/developer-relations-skills@developer-docs-structure-audit (where the guide belongs in the docs site)
- samber/developer-platform-skills@api-versioning-policy (choosing the version scheme, deprecation windows and sunset timelines)
