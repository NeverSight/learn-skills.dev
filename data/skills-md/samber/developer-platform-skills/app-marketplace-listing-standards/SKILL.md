---
name: app-marketplace-listing-standards
description: Write the listing-content rulebook for the operator of a B2B SaaS app marketplace - the standard every third-party listing must meet, covering required fields with objective reject criteria, screenshot and video specs, description quality bars, category taxonomy design, localization posture, badge display rules, and staleness/decay enforcement. Use whenever the user mentions listing standards, a listing rubric or marketplace quality bar, screenshot or media requirements, marketplace categories, rejection criteria, or delisting stale listings - even if they never say "listing standards". Operator side only. Do NOT use for optimizing a vendor's own listing - use samber/developer-platform-skills@integration-listing-optimization instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# App Marketplace Listing Standards

You are a marketplace-content advisor to the platform team that operates a B2B SaaS app marketplace. Write the listing-content rulebook the marketplace enforces against every third-party submission: what a listing must contain, what gets it rejected on content grounds, and what happens to it when it goes stale. The output is a published rulebook a submitter can self-check before submitting and a reviewer can enforce consistently - because across the benchmarked operators, the ones with the fewest review disputes are the ones whose rules are objective enough to fail against before submission.

This skill is the mirror image of submitter-side listing optimization: the rubric a vendor optimizes their listing against is exactly the rubric being written here. Content standards also stay deliberately separate from safety: a blurry screenshot, a keyword-stuffed description, or a trademark-infringing name gets a listing rejected regardless of whether the app is secure and functional - those gates belong to the review process, not this rulebook.

## Interview

Ask these before proposing anything. One question per message, multiple-choice where offered - each answer redirects a menu below.

1. Where is the listing standard today? (a) designing from scratch pre-launch (b) marketplace live, content rules ad-hoc (c) rulebook exists, revising for scale or friction (d) revising after a quality incident - low-quality listings, buyer complaints, stale catalog.
2. How many listings now and in 12 months, and who maintains each one - the vendor self-service, or your team on the vendor's behalf? The maintenance model sets how prescriptive the spec must be.
3. Which curation rung did the marketplace strategy choose - open, hybrid with a certified tier, or hard gate? The content bar enforces that decision; it does not re-make it (see `samber/developer-platform-skills@connector-marketplace-strategy`).
4. Who evaluates a listing before install - an end user installing self-serve, or an admin or committee doing diligence? This moves video length, tone, and description philosophy.
5. Does your platform ship versioned releases or scheduled deprecations on a cadence? This enables the strongest decay-enforcement rung.
6. Which languages and regions must listings serve, now and in 24 months?
7. Does a review, certification, or badge program exist or is one planned? Badge display rules only apply when there is something to display - eligibility lives with the review process.
8. By when must the rulebook be live - a hard date, or open-ended?
9. Is this a one-off win (unblock a launch, satisfy a flagship partner) or a compounding asset (a quality bar that appreciates as the catalog grows)?
10. What is the effort ceiling - reviewer hours per week for content review, engineering time for automated checks (link crawlers, image validators), and appetite for partner friction?

Questions 8-10 exist because the menus below diverge sharply on time-to-effect, durability, and effort:

- A hard deadline promotes rungs that ship as policy text.
- A compounding mandate promotes tooling and curation layers.
- A low effort ceiling rules whole shapes out, rather than demoting them.

## Who evaluates and who maintains

The eight marketplaces benchmarked for this skill span consumer-adjacent browser extensions to enterprise B2B suites, and all eight converge on the same listing skeleton ([references/marketplace-listing-benchmarks.md](references/marketplace-listing-benchmarks.md)):

- A short hook string.
- A benefit-oriented body.
- A fixed-geometry visual gallery.
- A capped optional video.
- A capped category assignment.
- Off-listing trust surfaces (privacy policy, support channel, landing page) that gate approval independently of the marketing copy.

What actually diverges tracks two other variables:

- **Who evaluates the listing.** Marketplaces whose buyers self-serve install tolerate promotional pacing (the loosest benchmarked video ceiling is 2-3 minutes, promotional tone allowed); marketplaces whose listings face an evaluating admin demand terse function proof (the strictest ceiling is 30 seconds, marketing footage banned).
- **Who maintains listings at what volume.** A vendor-self-service catalog needs machine-checkable prescriptive specs; an operator-assisted boutique catalog can run on judgment.

So write the same skeleton whatever the market, and set strictness and tone from questions 2 and 4.

## Workflow

1. Fix the design inputs: curation rung inherited from strategy, listing volume and maintenance model, buyer evaluation mode, platform release cadence, language/region targets.
2. Write the field skeleton and choose the spec-strictness rung (menu 1).
3. Set media specs and the accessibility floor (menu 2).
4. Write the description quality bar and the content-rejection trigger taxonomy.
5. Design the category taxonomy (menu 4).
6. Set the localization posture (menu 5).
7. Write the badge display rules (menu 6).
8. Write the decay-enforcement policy (menu 7).
9. Set measurement, then check the rulebook against the gates in Measurement.

Draft the rulebook section by section in that order, validating each with the user before the next:

- A wrong strictness rung caught at step 2 is cheap.
- The same rung discovered at step 8 rewrites every spec between.

## 1. Field-spec strictness

How prescriptive the rulebook's field requirements are. Four rungs, ranked. Efficiency here means consistent rejections bought per hour of rulebook authoring and maintenance:

- effort, authoring plus tooling (descending): `completion-tracked builder > exact per-field limits > named rejection triggers > principles-only`
- rejection consistency bought: `exact per-field limits > named rejection triggers > completion-tracked builder > principles-only`
- efficiency: `named rejection triggers > exact per-field limits > completion-tracked builder > principles-only`

- **Default rung: named rejection triggers, plus exact limits on the load-bearing fields only** - name, hook string, body, media geometry get numeric caps; everything else gets an enumerated list of violations (misleading or out-of-date metadata, keyword spam defined numerically, unattributed testimonials - the pattern of the most explicitly enumerated benchmarked policy). A trigger a submitter can self-check costs one sentence to write and removes a whole class of review disputes.
- **Promote to exact per-field limits across the board** once listings are vendor-self-maintained at volume - the most granular benchmarked rulebook puts a character or pixel cap on nearly every field precisely because thousands of self-service submitters cannot be reviewed on judgment. Consistency then depends on the spec, not on which reviewer reads it.
- **Starved option: the completion-tracked builder** - a submission console that tracks listing completion percentage and blocks publication below a floor. Highest effort (it is partner-console engineering, not policy text), best submitter completion rates, so it loses every efficiency round. Promote it when a partner console already exists and the rulebook can ship as validation rules inside it - an asset already owned re-ranks this menu.
- **Deleted, not demoted: principles-only rules** ("listings should demonstrate value and trust") once more than one person reviews content. Two reviewers reading the same principles reject different listings, and the gap surfaces as appeal noise. Not parked at the bottom, because "we'll use judgment" silently reappears as scope every time writing a real trigger feels like work.

This ranking is a default, not a law - and so is every menu below. Re-rank each against the interview: question 2 moves this menu, question 4 moves menu 2 and the quality bar, question 5 moves menu 7, question 7 moves menu 6 - and against assets the team already owns (an existing partner console, an existing localization pipeline, an in-house editorial function). Say which answer moved which rung.

## 2. Media specs

The single most important fact from the benchmarks: **there is no industry-standard screenshot geometry**. The eight operators ship 16:9, 8:5, and roughly 3:2 in production, and two skip pixel rules entirely ([references/marketplace-listing-benchmarks.md](references/marketplace-listing-benchmarks.md)). Never borrow one vendor's numbers as an industry constant - pick one geometry for your marketplace, publish it, and hold every submission to it. Three enforcement postures, ranked:

- effort (descending): `ranking-penalized optional assets > fixed-geometry hard spec > content-correctness-first`
- browse-surface quality bought: `fixed-geometry hard spec > ranking-penalized optional assets > content-correctness-first`
- efficiency: `fixed-geometry hard spec > content-correctness-first > ranking-penalized optional assets`

- **Default rung: fixed-geometry hard spec plus content rules** - one published ratio and count per asset type, and content requirements that matter more than pixels: at least one screenshot of the actual app UI, no PII, no pricing or review claims baked into the image, a quality floor (an off-topic, distorted, or wrong-ratio image is a named rejection trigger, stated as directly as the strictest benchmarked policy states it).
- **Content-correctness-first** - live URLs and truthful imagery policed, pixels not - is the right posture only while the operator's team maintains listings itself (question 2); it survives at scale in exactly the benchmarked marketplaces whose review process verifies every URL with a crawler.
- **Starved option: the ranking-penalty lever** - an optional asset that publishes without penalty of rejection but ranks below listings that provide it (one benchmarked operator does this for a promotional tile). It requires ranked search infrastructure to exist, so it loses every efficiency round; promote it when ranking already exists and an asset should be encouraged rather than required - and disclose the penalty in the published policy, as the operator that invented it does.

- **Video ceiling** (set deliberately from question 4): 30-second function-proof with marketing footage banned at the diligence end, 2-3 minutes with promotional tone allowed at the self-serve end, captions required either way.
- **Accessibility floor** (adopt voluntarily): descriptive alt text on informative images, captioned video, contrast and legibility minimums per WCAG 2.2 AA.

Only one of the eight benchmarked operators mandates listing-content accessibility, which makes it a cheap differentiator while adoption stays rare, and future-proofing against tightening accessibility law ([references/decay-and-badge-programs.md](references/decay-and-badge-programs.md)).

## 3. Description quality bar and rejection triggers

Two independent benchmarked operators - a commerce platform and a dev-tools platform - arrived at the same description rule separately, which is strong enough evidence to adopt as the default: **lead with the customer outcome, not the feature's technical mechanism**, and connect each feature claim to a measurable result. The worked accept/reject pair lives in [references/marketplace-listing-benchmarks.md](references/marketplace-listing-benchmarks.md).

Write the rejection triggers so a submitter can self-assess every one:

- **Keyword spam, defined numerically** - unnatural repetition of a term past a stated count, or lists of brands/regions with no added value; never just "don't stuff keywords".
- **Unattributed or anonymous testimonials**, and unsubstantiated outcome guarantees.
- **Trademark naming order** - "Task Tracker for {YourPlatform}" is the accepted shape; "{YourPlatform} Task Tracker" is rejected. Three benchmarked operators enforce this independently with near-identical worked examples; adopt the rule and publish your own pair.
- **Misrepresentation** - the listing must describe what the app actually does; undisclosed third-party account dependencies and their cost are a content violation.
- **Off-listing trust surfaces as hard gates**: a publicly accessible landing page (a PDF or code repository is explicitly not one), a support channel with a stated response commitment, and a privacy policy meeting a minimum-coverage checklist - approval-gating regardless of how good the marketing copy is.

## 4. Category taxonomy

Every benchmarked taxonomy that works has some cap or curation mechanism; the design question is which. Three shapes, ranked. Efficiency here means discoverability bought per unit of standing operator effort:

- standing operator effort (descending): `operator-curated layers > category plus structured tags > fixed capped list`
- discovery value bought: `operator-curated layers > category plus structured tags > fixed capped list`
- efficiency: `fixed capped list > category plus structured tags > operator-curated layers`

- **Default rung: a small fixed cross-functional category list with a hard per-listing cap** of one or two (the benchmarked spectrum runs from one category plus two industries to two of ten), enforced by a **staleness downgrade rather than delisting**: a listing whose categorization drifts from the app gets marked uncategorized and drops off every browse surface - soft, self-correcting, automatable.
- **Promote to structured tags on top of categories** (per-category feature tags plus a handful of search terms, each capped and one-idea-per-term) once search overtakes browsing as the discovery path - the tag caps are what keep search results meaningful.
- **Starved option: operator-curated layers** - editorial collections, "works with" labels, persona groupings assigned by the operator and never purchasable. Highest discovery value and a standing editorial cost every cycle, so it loses every efficiency round; promote it on a compounding mandate (question 9) once the catalog outgrows browsing, and keep placement unpurchasable - the moment curation is sellable it stops being a discovery signal and becomes inventory, which is the launch-marketing skill's territory.
- **Deleted, not demoted: uncapped self-selection.** An uncapped multi-select taxonomy degenerates into every listing claiming every plausible tag until categories stop meaning anything. Not parked at the bottom, because "let vendors pick more categories later" silently reappears every time a partner asks for broader placement.

## 5. Localization posture

Rank by market reach bought per unit of combined operator-plus-vendor effort:

- effort, setup plus per-listing (descending): `all-or-nothing declaration > auto-translate with override > region-locked > opt-in per market`
- reach bought: `auto-translate with override > region-locked > opt-in per market > all-or-nothing declaration`
- trust of the language claim: `all-or-nothing declaration > region-locked > opt-in per market > auto-translate with override`
- efficiency: `opt-in per market > auto-translate with override > region-locked > all-or-nothing declaration`

- **Default rung: opt-in per market** - listings launch in one language; a vendor may add per-market listings through a documented path. Cheapest real localization, and the honest floor while question 6 names one primary market.
- **Promote to auto-translate with vendor override** when the operator has machine-translation infrastructure to amortize: every listing gains every supported language by default, and a vendor can replace any one translation - the benchmarked default-on model. The trust cost is real: machine output carries the operator's name.
- **Region-locked** is the posture forced when distribution-region selection controls visibility: each selected region's language must be present or users there cannot find the listing at all. Adopt it only together with region gating, never alone.
- **Starved option: all-or-nothing capability declaration** - declaring a language commits the vendor to the full runtime experience in that language, not just a translated listing page. Highest vendor effort and the least listing reach, so it loses every efficiency round; promote it when buyers treat language support as a purchase-blocking capability claim (enterprise multi-region rollouts), because it is the only rung where the listing's language claim is guaranteed true in the product.

## 6. Badge display

- **Eligibility** (what earns certification) belongs to the review process (`samber/developer-platform-skills@app-marketplace-review`).
- **Display** (where an earned badge renders and how its currency is enforced) is what this rulebook owns.

First check question 7: **running no badge program at all is a legitimate architecture, not an oversight** - one of the eight benchmarked operators does exactly that, and its listing UX is still cited as best-in-class, which shows listing quality and certification are independent axes. If badges exist, four display mechanisms, ranked:

- effort (descending): `renewal-linked display currency > off-marketplace promotional badge with brand rulebook > dedicated trust surface > inline badge chip`
- buyer trust bought: `renewal-linked display currency > dedicated trust surface > inline badge chip > off-marketplace promotional badge`
- efficiency: `dedicated trust surface > inline badge chip > renewal-linked display currency > off-marketplace promotional badge`

- **Default rung: a dedicated trust surface** - a listing tab or section physically separate from the marketing copy, stating data-storage location, displaying earned badges, and listing compliance certifications (the benchmarked trust-tab pattern). Pair it with a written currency rule: a lapsed badge comes down, with a stated grace period.
- **The inline chip** (a badge next to the listing name in search results) is the cheap complement, not a substitute - it asserts trust without the substantiating detail a diligence buyer needs.
- **Starved option: renewal-linked display currency automation** - badge display wired to the review program's eligibility data so a badge that lapses (a failed recertification, a threshold no longer met) disappears without human intervention. Highest effort, and the only mechanism where displayed badges are guaranteed current; promote it once badges carry quantitative, lapsable thresholds - the benchmarked certification that works this way runs on a rolling renewal cycle.
- **The off-marketplace promotional badge** (vendors embed "available on X" on their own sites) is marketing reach, not listing trust; if offered, ship it with a brand-usage rulebook - use as provided, minimum clear space, size parity with competing badges, mandatory link back - because the most detailed benchmarked badge spec is exactly that rulebook.

One hard rule whatever the rung: **never claim or imply an external listing-quality certification.** Targeted research found no ISO-, IAB-, or equivalent external body certifying marketplace listing quality anywhere in the industry - every real program is operator-proprietary. The honest positioning is compositional, named as yours ([references/decay-and-badge-programs.md](references/decay-and-badge-programs.md)):

- WCAG for accessibility.
- Recognized security attestations for security.
- Your own published rubric for content.

## 7. Decay enforcement

Listing content expires on its own whenever the app changes and the listing doesn't. Every benchmarked operator handles this differently and none publishes a hard numeric cadence - the only explicit "update every N months or be removed" rules live in adjacent ecosystems ([references/decay-and-badge-programs.md](references/decay-and-badge-programs.md)). Five mechanisms, ranked:

- operator effort (descending): `version-currency enforcement > calendar cadence with auto-removal > policy-as-violation > staleness downgrade > discretionary monitoring`
- freshness bought: `version-currency enforcement > calendar cadence with auto-removal > policy-as-violation == staleness downgrade > discretionary monitoring`
- efficiency: `staleness downgrade > policy-as-violation > calendar cadence with auto-removal > version-currency enforcement > discretionary monitoring`

The `==` holds because both mechanisms catch drift only when a review touchpoint notices it - they differ in consequence (removal risk versus a browse downgrade), not in detection, and detection is what limits the freshness either one buys.

- **Efficiency leader, and the always-on floor under whatever else runs: the staleness downgrade** (menu 4's uncategorized penalty) - automatable, self-correcting, no delisting fight. Its consequence is a browse downgrade rather than removal risk, so it stacks under a policy instead of replacing one.
- **Default rung: that downgrade plus policy-as-violation backed by a calendar sweep.** Name "out-of-date listing content" an explicit, rejectable violation in the published policy (two benchmarked operators do), then run a self-set operator-side review cadence - align it to your own release cycle, and treat the adjacent-ecosystem 12-month auto-removal benchmark as the internal worst-case freshness SLA even though nothing external forces it.
- **Starved option: version-currency enforcement** - new listings rejected outright on unsupported platform versions, existing listings required current at recertification, with a stated migration window. The most systematic mechanism in the whole benchmark set and the highest effort, because it presupposes versioned platform releases and deprecation discipline; promote it the moment question 5 says yes, since the release cadence then does the freshness-detection work for free.
- **Discretionary monitoring** - continuous compliance watching with no published trigger - is the floor, not a choice: it is what an operator does when it has not written a policy.
- **Deleted, not demoted: fees as a freshness mechanism.** One benchmarked operator charges an annual listing fee, and it renews the listing's billing relationship, not its content - a fee gates nothing a stale screenshot violates. Listing fees are revenue design and belong to the monetization model; keeping "the fee handles staleness" on this menu would let the rulebook believe decay is covered when nothing checks content at all.

Whatever the rung: every new content requirement applied to already-listed apps needs a notice runway before it takes effect - retroactive rule changes without runway burn the partner trust the standard exists to build.

## Failure modes

- **Borrowing a vendor's pixel numbers as an industry standard.** There is none - three geometries coexist in production. Fix: pick and publish your own, one per asset type.
- **Uncapped taxonomy.** Every listing claims every tag; browse surfaces stop discriminating. Fix: a hard cap or an operator-curated layer, chosen in menu 4.
- **Claiming an external listing-quality certification.** No certifying body exists; the claim is unverifiable at best. Fix: the compositional positioning in menu 6.
- **Review-once-and-forget.** A listing approved once with no decay mechanism drifts from the app until buyers notice before you do. Fix: menu 7's default rung at minimum.
- **Principles-only rules with multiple reviewers.** Inconsistent rejections, then appeal noise, then submitters learning the reviewer instead of the rulebook. Fix: menu 1's deletion argument.
- **Scope creep into security review.** The rulebook starts encoding permission audits and re-review triggers that belong to the review process; the two drift apart and contradict. Fix: content triggers fire independently of safety - keep the boundary and cross-reference.
- **Undisclosed ranking penalties.** Quietly down-ranking listings that skip an optional asset reads as arbitrary when discovered. Fix: if you rank-penalize, publish it, as the benchmarked operator does.

## Measurement

Rulebook gates first - self-set, and flagged as such: no industry pass-standard for a listing rulebook exists, and no external certification body to borrow one from. Iterate until all five pass:

1. Every required field carries an objective reject criterion a submitter can self-check before submitting.
2. Exactly one published geometry per visual asset type.
3. The taxonomy carries a hard per-listing cap, an operator-curated layer, or both.
4. Every listing has a decay trigger with an owner and a stated consequence.
5. Every displayable badge has a display location and a currency rule.

Operating KPIs once live:

- First-pass content-approval rate.
- Listing completion rate.
- Share of the catalog stale beyond the freshness SLA.
- Rejection-reason distribution (a rising "unclear content" share signals spec ambiguity, not submitter failure).
- Review turnaround against listing completeness - one benchmarked operator states outright that clear listing content shortens its review, so the correlation is worth instrumenting.

Listing-to-install conversion benchmarks exist only as vendor-reported marketing figures - usable as direction, never as a promised target ([references/decay-and-badge-programs.md](references/decay-and-badge-programs.md)).

If your harness has persistent memory, record:

- The chosen spec-strictness rung.
- The published media geometry.
- The taxonomy cap.
- The freshness SLA.
- Each menu's rung, with its promotion condition.

Review, onboarding, and launch-marketing runs should inherit these decisions instead of re-asking.

## Invocation examples

- "We're opening our app marketplace to third-party vendors next quarter - write the listing requirements page."
- "Half our marketplace listings have outdated screenshots and dead support links. Design a staleness policy that fixes this without delisting half the catalog."
- "Partners keep disputing listing rejections. Turn our ad-hoc content review into an objective rubric they can self-check against."
