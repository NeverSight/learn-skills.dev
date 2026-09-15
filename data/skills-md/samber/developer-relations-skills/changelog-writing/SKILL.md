---
name: changelog-writing
description: Turns raw commits, pull requests and tickets into release notes developers actually read  -  a scannable record of what shipped, what it means in practice, and what breaks. Use whenever the user mentions a changelog, CHANGELOG.md, release notes, a GitHub release body for a tag, a hosted "what's new" page, app-store release notes, Keep a Changelog, or Common Changelog, or asks what to write for a release they just cut  -  even when the commit history is messy and follows no commit convention. Not for version bumping, tagging or publishing pipelines. Do NOT use for a full breaking-change upgrade guide  -  use samber/developer-relations-skills@version-migration-guide; for a narrative release post use samber/developer-relations-skills@engineering-blog-post.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Changelog Writing

You are a release-communication specialist. Take the raw record of what shipped - commits, merged pull requests, issues, tickets - and produce release notes a developer can scan in fifteen seconds to answer one question: _does this release cost me work?_

A generator produces a list. Produce the editorial layer no generator does: what to keep, what it means for a reader, and what breaks. That layer is why the task is expensive and disliked - drafting one release-note document takes an experienced developer up to 8 hours (Moreno et al., as cited in Daneshyan et al., FSE 2025), and a Microsoft developer advocate summarized the sentiment: "we hate creating release notes when it's our turn to ship" (Jasmine Greenaway, opensource.microsoft.com, 2018).

## Scope check

Confirm the task before starting. Route elsewhere when:

- The user wants versions bumped, tags cut, or artefacts published → release-automation tooling, not this skill.
- The change needs before/after code, a deprecation timeline, and codemods → `samber/developer-relations-skills@version-migration-guide`.
- The release deserves a narrative post with context and screenshots → `samber/developer-relations-skills@engineering-blog-post`.
- The question is which channels announce the release → `samber/developer-relations-skills@devrel-content-calendar`.

Writing the notes and linking out to a migration guide is in scope; writing that guide is not.

## Interview

Ask one at a time, multiple-choice where you can. Stop as soon as you know the surface, the audience and the source range - do not run the whole list mechanically.

1. Which surface is this for: repository `CHANGELOG.md`, a git-host release body, a hosted changelog page, an in-product "what's new", an app-store listing, an enterprise advisory, or several at once?
2. Who reads it: integrators upgrading a dependency, end users of an application, or both?
3. What is the version range - previous tag to `HEAD`, a milestone, a date window?
4. Does the project already follow a changelog specification, or is this the first release?
5. Does the history follow a commit convention, or is it free-form?
6. Does the release contain anything breaking or deprecating, as far as the user knows?
7. Is there a migration guide, upgrade doc, or issue to link breaking entries to?
8. Which of the raw material can you actually read - the repository, an exported log, a ticket list?
9. Will these notes be translated? If yes, into how many locales, and is there a character cap?

Ask 10-12 only when answer 1 names more than one surface, or when the release looks like tier 1 or 2. A single-surface release has no menu to order, and asking anyway is noise.

10. When does this have to be out - a ship date already announced, an embargo, a security window, or whenever it is ready?
11. Is this one release you need out of the door, or are you setting up how every release goes out from now on?
12. What is your ceiling for this release - your own hours only, engineering time for an in-product note, a marketing send, a security or app-store review cycle?

Re-rank the surface order below against 10-12 and say which answer moved which surface:

- Q10 (ship date): a fixed date drops every surface that needs someone else's review cycle.
- Q11 (how every release goes out): promotes the hosted page and a note-fragment workflow, because both pay back per release rather than once.
- Q12 (ceiling): your own hours alone deletes the email and the in-product note from the plan outright.

If your harness has persistent memory, record the answers to questions 1, 2, 4, 5 and 9 as project conventions. They are stable across releases; re-asking them every release is the main reason this task feels tedious.

## Workflow

1. **Collect the raw material.** Run [./scripts/collect-release-material.sh](./scripts/collect-release-material.sh) when you can execute shell commands in the repository. Otherwise take a pasted log, an exported ticket list, or the user's spoken description of what shipped. Never stall because the repository is unreachable - state which mode is in use, because verification strength depends on it.
2. **Reduce to the net diff.** Collapse fixup, revert and follow-up commits into the single surviving outcome. Three commits that add, revert and re-add a flag are one entry or none.
3. **Select.** Keep every change a consumer can observe. Drop what they cannot. See the selection rules below.
4. **Tier the release** to decide how much surface it earns. See Announcement tiering.
5. **Categorize.** Assign each surviving change to a category from the project's specification - read [./references/format-specifications.md](./references/format-specifications.md) when the project has no convention yet or you must map between two.
6. **Write each entry** impact-first, in the project's voice. See Entry anatomy, and [./references/worked-examples.md](./references/worked-examples.md) for full before/after releases.
7. **Handle breaking changes and deprecations** with the three-part form below.
8. **Assemble per surface** using [./references/surface-templates.md](./references/surface-templates.md) for git-hosted surfaces, and [./references/non-git-surfaces.md](./references/non-git-surfaces.md) for app stores, enterprise advisories, hosted APIs and browser extensions - each imposes hard caps and review rules the git surfaces do not.
9. **Run the verification gate.** Do not hand over notes that have not passed it.
10. **Hand off.** Name what still needs a human: unverified performance numbers, a missing migration guide, a security entry needing a CVE reference.

When the project has many contributors and no note-fragment workflow - each entry written as its own small file in the same patch as the code - recommend one, once. Entries written at release time reconstruct impact from memory, weeks after the change.

## Selection rules

Keep changes a consumer can observe, even when they look internal:

- Default values, error message text (people match on it), timeouts, limits.
- Runtime, engine or platform version floors.
- Performance characteristics, when you have a measurement.
- Refactors with a behavioural side effect, and newly documented behaviour.

Drop changes with no consumer surface:

- Development-only dependency bumps, lint and formatter config, CI workflows.
- Test-only changes, internal renames, comment and docs formatting churn.

Never decide from a filename or directory. A change under `docs/` can be release-relevant; a change under `src/` can be pure churn. Read what it does.

When the range is too large to write up in full, rank the surviving changes by consumer impact and set an explicit cut line rather than trimming by feel. Precedent: the SmartNote study (Daneshyan et al., FSE 2025) tuned a significance threshold of 0.10-0.15 to balance verbosity against omission. Transfer the discipline, not the number - state the cut line to the user and list what fell below it.

## Announcement tiering

Tier the release before choosing surfaces. PostHog publishes the clearest public version of this framework, and its lineage as a resource-allocation device goes back to Pragmatic Institute launch tiering.

Set the tier by expected reader impact, never by engineering effort - the one place in this skill where effort is deliberately excluded from the ordering. A quarter of rewriting that nobody can observe is a tier 4; a one-line default change that breaks callers is a tier 2. Ranking the tier by what it cost to build would systematically under-announce exactly the cheap changes that break people.

| Tier | Definition                                               | Surfaces it earns                                            |
| ---- | -------------------------------------------------------- | ------------------------------------------------------------ |
| 1    | New product                                              | Everything, plus a launch plan owned outside this skill      |
| 2    | Noticeable impact on most users, or requires user action | Changelog, release body, hosted page, email, in-product note |
| 3    | Noticeable impact on some users, no action required      | Changelog, release body, hosted page                         |
| 4    | No noticeable impact for most                            | Changelog and release body only                              |

The tier definitions follow PostHog's published handbook; the per-tier surface lists are this skill's adaptation to its own surface set. Pool tier 3 and 4 items into a curated periodic digest - useful without consuming launch resources (reported practitioner guidance). Tier 1 is a launch, not a release; hand it to `samber/developer-relations-skills@devrel-content-calendar` and `samber/developer-relations-skills@engineering-blog-post`.

### Which surface to produce first

The tier says which surfaces a release earns. It does not say which to produce first when the budget runs out mid-release, and those are different questions on different axes - the tier is a property of the change, the production order is a property of your hours. Never let the order below leak back into the tiering decision.

- effort, least first: `changelog == release body > hosted page > email > in-product note`
- value, most first: `in-product note > email > hosted page > release body > changelog`
- compliance cost: an app-store note ships inside a review cycle and cannot be corrected without another submission; an enterprise or CVE advisory needs security sign-off and is unretractable once distributed; an email is unretractable once sent; the changelog, release body and hosted page stay editable forever.
- efficiency, do first: `changelog == release body > hosted page > in-product note > email`

The changelog and the release body tie: they are the same text pasted twice, so one edit produces both. They separate no reader, since which one a person finds depends only on whether they arrived from the repository or from the tag.

Default to the top two for any release, and add the hosted page once it renders from the same source rather than being maintained by hand. Add the rest only when the tier earns them and answer 12 says someone can pay for them.

The in-product note and the email are what this order starves: each costs a week and another team's calendar, and each is the only way to reach the users who will never open a repository. Promote both above everything else the moment the release requires user action - a breaking change nobody reads about gets discovered as an outage - and accept that the ratio is the wrong instrument for that case.

This order is a default, not a law, and it shifts with who executes it. Re-rank it against what you know:

- A team whose hosted page already auto-publishes from the changelog gets that rung for free and should take it immediately.
- A project with no email list deletes that row rather than carrying it release after release.

Delete every surface answer 12's ceiling rules out and say which one you removed.

## Entry anatomy

State what changed, then why a reader cares - one to three sentences (this skill's working budget, not a published rule). Lead with the observable effect; put the mechanism after it, or drop it.

Rewrite internal vocabulary - ticket IDs, service codenames, module names outsiders never see - into product terms.

```
Bad:  Implemented Redis caching layer for dashboard API endpoints (PROJ-4471)
Good: Dashboards load noticeably faster on accounts with large workspaces.

Bad:  Revolutionary new streaming experience, completely rebuilt from the ground up!
Good: Add `stream()` to the client for token-by-token responses.
```

The second pair is the trap specific to developer audiences: marketing adjectives make a technical reader stop reading the file. Stay flat and specific. More pairs, including full releases written badly and then correctly, are in [./references/worked-examples.md](./references/worked-examples.md).

Order within a category by consumer impact, breaking items first. A reader who stops after two bullets should have read the two that could break their build.

Match the project's mood and keep it consistent: imperative present ("Add `stream()`") if the project uses a specification that requires it, past tense ("Added streaming") otherwise. Never mix the two inside one release.

### Voice

Two schools disagree, both with credible practitioners behind them (sources in [./references/published-findings.md](./references/published-findings.md)):

- **Editorial school.** Anna Pickard built Slack's release notes on the premise that the store text box is "just a little space in which we can be human", with the voice distilled as _clear, concise, human_, clarity ranked first.
- **Technical-writing school.** Sarah Maddox frames the function narrowly: tell customers something changed, especially when it changes how they use the product. Anne Edwards argues that funny, friendly notes run long, obscure the message, and cost non-native readers extra work.

Settle it with three questions, not taste:

1. Is the reader integrating against this change, or receiving it?
2. Will the text be translated?
3. Does the brand already carry that register elsewhere?

- efficiency, default: `technical-writing school > editorial school`

Default to the technical-writing school: it is faster to write, survives translation unchanged, and answers the reader's actual question. Afford the editorial register only when all three conditions hold together, since any one alone is not enough:

- a consumer surface
- one locale, or a translation budget
- a product whose voice already exists

Under localization, whimsy is not a taste choice: it multiplies translation cost and defect rate across every locale.

## Breaking changes and deprecations

Give every breaking entry three parts:

1. **What breaks** - the observable behaviour, not the internal cause.
2. **Who it hits** - the affected subset (one SDK, one config flag, callers of one endpoint). "Everyone" is rarely true. Overusing it teaches readers to skip the marker.
3. **What to do** - one line of action, plus a link when the fix is longer than a rename.

```
**Breaking:** `client.send()` now rejects payloads over 1 MB instead of truncating
them. Affects callers that relied on silent truncation  -  chunk the payload or catch
`PayloadTooLarge`. See the v3 migration guide.
```

Keep the version number honest:

- Major means breaking.
- Minor means additive.
- Patch means fixes.

A "Removed" entry inside a minor release is a defect in either the notes or the version - say so rather than shipping it, because readers who trust version ranges get broken silently.

Announce a deprecation in a release that removes nothing, naming the replacement and the earliest version that removes it. Reference that announcement again in the release that performs the removal.

## Messy history

Most real repositories have no commit convention - roughly 90% of projects in the SmartNote sample enforce none, and only 54% of 900 open-source projects surveyed by Jiang et al. generate notes from pull requests at all. Assume the log is squash merges, `wip`, and `fix tests` until you see otherwise.

- Work from the diff and the pull-request titles and bodies, not the commit subjects.
- Group changed files into features by reading the code, then confirm each grouping with the user before writing entries for it.
- Ask the user to confirm anything you cannot see: a change gated behind a feature flag, an infrastructure change with a user-visible effect.
- Propose a commit convention only if the user asks. Fixing the pipeline is a different job from writing this release's notes.

## Audience variants

The entry craft is identical for developer tools and consumer products: observable effect first, no internal vocabulary, honest scope. What differs is around it.

- **Integrator / B2B audience.** Precision and references win. Link every entry to its pull request. State deprecation windows in versions, not dates, and keep them long. Enterprise readers may be several versions behind, often arrive months later searching for a symptom or a CVE, and need the breaking set complete and pinned at the top.
- **End-user / B2C audience.** Benefit-led and short - this skill budgets 3-5 items, a working default, not a published standard. Ship it as an in-product note, email or store listing, and link back to the full entry for anyone who wants it.

When one release serves both, write the integrator version first and derive the user-facing one from it - [./references/surface-templates.md](./references/surface-templates.md) gives the derive order.

## Verification gate

Generated notes fail in two directions: entries with no source, and shipped changes with no entry. Check all four before handing over, and iterate until they hold.

1. **Traceability - 100%.** Every entry maps to at least one commit or pull request in the range, and the claim is checkable in that diff. Not negotiable as a principle: GitHub's own release-notes documentation makes "confirm the notes contain all and only the intended information" a numbered step. The 100% figure itself is a self-set bar rather than a published standard.
2. **Coverage.** Every consumer-observable change has an entry or an explicit exclusion - show the exclusion list, never drop things silently. The 100% target is a self-set baseline, deliberately stricter than observed practice: human-written notes covered 31% of commits in the SmartNote evaluation, and Abebe, Ali and Hassan found well-formed release notes list only 6-26% of the issues a release addressed. Those numbers describe writers trading coverage for concision, not a standard to match. If "consumer-observable" is genuinely contested on a large release, negotiate the line with the user and record where you drew it.
3. **No unsourced numbers.** Every quantitative claim ("40% faster") comes from a measurement in the source material. Delete the number rather than estimate it.
4. **Breaking completeness.** Every breaking entry carries all three parts and, where one exists, a migration link.

The durable rule under all four: **the reviewable unit is the claim-to-diff mapping.** Tone, ordering and grouping are cheap to fix after publication; a sentence describing a change the code did not make is the defect that damages trust irreversibly, and the one a model is most likely to introduce. Any review step that does not put the diff next to the sentence is theatre.

For the summary paragraph and any user-facing variant, run a light pass with your preferred humanizer skill. Leave the specification-conformant bullets alone - they are meant to read as terse and mechanical.

## Invocation examples and expected output

Typical requests: _"write the changelog for v2.4.0"_, _"turn these 40 commits into release notes"_, _"what do I put in the GitHub release body for this tag?"_, _"draft the What's New for the App Store update"_, _"our changelog reads like a git log, fix it"_.

Collect the raw material for a range:

```bash
./scripts/collect-release-material.sh --from v2.3.0 --to HEAD
```

Deliver, in this order:

1. **The notes**, one block per requested surface, in fenced Markdown ready to paste.
2. **A traceability table** - one row per entry, with the commit or pull request it maps to.
3. **The exclusion list** - every change you saw and deliberately left out, with the reason.
4. **Open items for a human** - unmeasured performance claims, a missing migration link, a security entry needing a CVE, anything you had to ask the user to confirm and could not.

[./references/surface-templates.md](./references/surface-templates.md) shows the four parts assembled on a sample release.

## Failure modes

| Symptom                                | Cause                                      | Fix                                                                |
| -------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| Notes read as a commit log             | Wrote per commit instead of per outcome    | Re-reduce to the net diff, merge fixups                            |
| Every release says "various bug fixes" | No source material read, only tag names    | Go back to the diff; an empty release is better than a vague one   |
| Breaking change buried mid-list        | Category order applied before impact order | Move breaking items first inside each category                     |
| Reader asks "does this affect me?"     | Entry states mechanism, not effect         | Rewrite impact-first, add the affected subset                      |
| Entry contradicts the code             | Trusted a pull-request title               | Re-check against the diff; titles overstate                        |
| Two releases use different tense       | No recorded convention                     | Fix the current release, record the convention in memory           |
| Reviewer approved a wrong entry        | Review read the prose, not the diff        | Review each sentence against its diff                              |
| Translated notes rejected or truncated | Wrote to the largest surface first         | Write to the tightest cap first, then expand; see non-git surfaces |
| Every change gets a launch             | No tiering step                            | Tier first, then allocate surfaces                                 |

## Measurement

Track per release, if the surfaces are instrumented:

- efficiency, track first: `support volume > breaking-entry click-through > release-page views > time-to-upgrade == review-comment count`

- **Support and issue volume tagged to the release.** Costs nothing beyond triage you already do, and moves within days - a spike right after ship usually means an under-communicated behaviour change, not a bad release.
- **Click-through from a breaking entry to its migration guide.** An hour to tag the link, and the only number that says whether the entry did its job.
- **Release-page views against downloads or installs of that version.** An hour to assemble where the surfaces are instrumented, but views and installs answer different questions and the ratio between them is noisy.
- **Time-to-upgrade** - version distribution in use 7, 30 and 90 days after release - and **review-comment count per release**, if notes go through review, tie at the bottom: each takes a quarter before it says anything and each needs a pipeline you may not have (telemetry for one, a standing review step for the other). Tom Johnson's public account of running an agent on this task records 15-20 comments per release falling to 3-5 after roughly a dozen iterations - a convergence curve, not a target to hit immediately.

Time-to-upgrade is what this order starves: it is the only measure of whether the notes moved anyone, and it costs a quarter plus telemetry, so it never wins on ratio. Promote it above everything when the release is breaking and you need to know who is still on the old version before you remove it.

Never claim adoption, retention or revenue impact from a changelog. The only published outcome evidence is correlational: longer Google Play release notes correlate with higher average ratings across 69,851 releases of 2,232 apps (Yang et al., _Empirical Software Engineering_ 27:55, 2022), confounded by release frequency and app maturity.

Linear's widely cited returns from changelog discipline (recruiting, investor confidence, early-adopter trust) are first-party and unquantified. Cite either as documented practice, never as proof of ROI - overstating attribution costs credibility with exactly this audience.
