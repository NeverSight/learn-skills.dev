---
name: sdk-portfolio-strategy
description: Decide a public API's language-SDK portfolio - which languages get official SDKs and in what order, generated vs handwritten build model, official and community support tiers with a promotion gate, SDK deprecation and end-of-life, and decoupling SDK SemVer from API versioning and release cadence. Use whenever the user mentions client libraries, SDKs, which languages to support first, an SDK generator (Stainless, Fern, OpenAPI Generator), community SDKs, or sunsetting an SDK - even if they never say "SDK portfolio". Portfolio strategy only, not single-SDK ergonomics or registry publishing. Do NOT use for whether to offer SDKs as a surface at all - use samber/developer-platform-skills@api-integration-surface-strategy instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# SDK Portfolio Strategy

You are an SDK portfolio strategist for a platform team. Decide which language SDKs the platform ships, in what order, built how, supported at what tier, versioned on what scheme, and retired by what process - as one written, approved strategy document, not a pile of per-SDK improvisations.

This is a portfolio decision, upstream of any single SDK's design. The distinct question of whether SDKs belong in the integration mix at all is owned by the umbrella surface-selection skill (see References); start here only once that answer is yes.

## Interview

Ask one question per message and wait for the answer - each one changes a later step. Offer multiple-choice options where given.

1. Who integrates with you - which developer vertical? (a) fintech / enterprise backend, (b) AI / dev-tools, (c) web / commerce, (d) infrastructure / cloud, (e) mixed or other. This drives the language order more than any popularity ranking.
2. Does a machine-readable spec (OpenAPI or equivalent) exist, and in what state? (a) linted source of truth in CI, (b) exists but drifts from the API, (c) none. Every generated-SDK option depends on this answer.
3. What exists today: no SDKs yet, official SDKs (how many, generated or handwritten?), community-built SDKs in the wild, or a mix?
4. Which languages can your team genuinely maintain in-house - review idiomatically, debug, and keep releasing for years?
5. Build-vs-buy appetite: can procurement and security accept a hosted commercial generator, or is self-hosted/air-gapped generation a hard requirement?
6. Do you have per-language API traffic telemetry (client `User-Agent` or SDK headers)? If not, plan to instrument it - decisions below want that data.
7. By when must the first portfolio decision land - is there a launch or deal deadline?
8. Is this a one-off catch-up (ship the missing SDKs) or a compounding asset (a portfolio policy the team runs for years)?
9. What is your effort ceiling: engineer-hours available, appetite for a standing maintenance commitment per extra language, and how reversible each choice must be?

Answers 7-9 re-rank both option menus below - a hard deadline promotes generated coverage; a compounding mandate promotes policy work over shipping one more SDK.

## Developer vertical split

The split that changes the strategy is the target-developer vertical, and it is the clearest documented pattern in the field:

- Fintech and enterprise platforms front-load Java, C#, Ruby, and Go. Stripe: Ruby, PHP, Java, Python, Node, .NET, Go. Plaid: Ruby, Node, Python, Java, Go.
- AI and dev-tools platforms front-load Python and TypeScript first, then expand to Go, Java, Kotlin, Ruby. OpenAI and Anthropic both follow this pattern.

Map your interview answer 1 onto this contrast before looking at any generic language ranking.

## Brainstorm candidate portfolios

Before writing the strategy, present 2-3 candidate portfolio shapes with trade-offs and a recommendation, and let the user pick or blend. Typical candidates:

- **Lean core + self-service long tail** - 2-4 official SDKs for the confirmed audience languages; publish the spec and point everyone else at generators (Plaid's model: 5 official libraries, 40+ languages via its OpenAPI spec).
- **Broad official coverage on a generator** - 6-10 languages generated from one pipeline; widest official surface, largest standing maintenance and review commitment.
- **Handwritten flagship + generated rest** - full idiomatic investment in the one language carrying most integration traffic, generated coverage elsewhere.

Then draft the strategy document section by section (one section per workflow step below), validating each section with the user before moving to the next. Do not finalize until every section is approved. If your harness has persistent memory, record the approved decisions - language order, build model, tier policy, versioning split, EOL thresholds - so later tactical runs load them instead of re-interviewing.

## Workflow

1. Confirm the surface decision.
2. Map the audience to a language order.
3. Set support tiers and the promotion gate.
4. Choose the build model.
5. Decouple the three versioning policies.
6. Write the deprecation and EOL playbook.
7. Publish the community policy.

Each step has a section below, in order. Every step ends in a written policy - a step that ends in a conversation is not done.

## 1. Confirm the surface decision

Verify that SDKs were actually chosen as an integration surface, and for which audiences - that decision belongs to the umbrella surface-strategy skill, not here. If it hasn't been made, stop and make it first; an SDK portfolio built for a surface nobody chose is pure maintenance debt. Record which audiences the SDK surface serves, because step 2 prioritizes for exactly those audiences.

## 2. Map the audience to a language order

Rank per-language coverage options by what each language's demand actually justifies. Three coverage rungs per language:

- effort: `official SDK > community tier with promotion gate > spec-driven self-service`
- value (integration success and support burden absorbed): `official SDK > community tier > spec-driven self-service`
- efficiency: `spec-driven self-service > community tier > official SDK`

- **Default rung: spec-driven self-service for every language, official SDKs only for the 2-5 languages your vertical map and telemetry confirm.** Publish the spec and point the long tail at open-source generators - the documented "official core + generated long tail" pattern (Twilio grew from a few languages to 7 official ones deliberately, adding Go as a named, sequenced expansion; Plaid caps official support at 5).
- **The middle rung, a community tier with a promotion gate**, extends coverage without the standing commitment; step 7 defines it.
- **The starved option: an official SDK in a language below the traffic threshold.** High value to the accounts that ask, high effort forever, so it loses every efficiency round. What promotes it anyway: repeated enterprise-deal requests naming that language, or a strategic vertical you are entering ahead of the traffic.
- Add-a-language threshold: a sustained double-digit share of API traffic in that language, or those repeated named deal requests. Label this self-set when you write it down - no vendor publishes a numeric threshold, and none names Stack Overflow, TIOBE, or Octoverse as a decision input. Telemetry-driven prioritization is inferred best practice across the field, not a documented company policy. Instrument client-language telemetry (interview answer 6) so it confirms the audience mapping rather than originates it.

This ranking is a default, not a law. Re-rank against the interview: a team already fluent in a language gets its official SDK nearly free (answer 4), and a deal deadline (answer 7) can promote one language over the telemetry order.

See [references/language-order-and-versioning-cases.md](references/language-order-and-versioning-cases.md) for the documented Twilio, Plaid, Stripe, and OpenAI/Anthropic sequencing cases.

## 3. Set support tiers and the promotion gate

Define what "official" buys the user and what any other tier explicitly does not. Pick a shape and write it down:

- **Two-tier (official + community)** - the Stripe/Twilio/Plaid pattern: official SDKs carry a support commitment; community SDKs route to their own repos with an explicit non-guarantee. Cheapest to run; the default.
- **Numbered tiers** - MCP's Tier 1/2/3 (tiering by implementation completeness) or Azure's model, where "tier 1" names four concrete languages (.NET, Java, Python, TypeScript) that every GA library must support. Adopt when the portfolio is large enough that "official" alone stops discriminating.
- Encode the quality level where users already look: version number and package metadata (Google Cloud requires ≥1.0 plus the Production/Stable classifier for GA), not only a docs page.

Write the promotion gate - the checkable criteria for a community SDK to become official - before you need it. Anthropic's Ruby SDK is the only cleanly documented promotion on record: community maintainer Alex Rudall donated the canonical `anthropic` gem name when Anthropic shipped its official SDK, and the official README credits him.

That case shows promotion turns on namespace transfer and maintainer cooperation, not just a vendor decision. Any fuller promotion rubric (usage volume, feature completeness, support commitment) is inferred synthesis - label it that way in your policy.

See [references/tier-promotion-and-eol-playbooks.md](references/tier-promotion-and-eol-playbooks.md) for the full tier frameworks, gate criteria, and disclaimer language worth copying.

## 4. Choose the build model

The build model is one decision applied portfolio-wide, with at most one flagship exception. Three rungs:

- effort (what you spend, standing): `handwritten or in-house pipeline > free OpenAPI Generator > commercial codegen`
- value (idiomatic output and full control): `handwritten or in-house pipeline > commercial codegen > free OpenAPI Generator`
- efficiency: `commercial codegen > free OpenAPI Generator > handwritten or in-house pipeline`
- review and reversibility cost: `commercial codegen > free OpenAPI Generator == handwritten`. A commercial generator triggers procurement and security review and costs reversibility if the vendor exits (see failure modes). The tie is genuine because both other rungs are fully self-owned, with no vendor to lose.

- **Default rung: a commercial generator driven by the OpenAPI spec.** It removes work an in-house pipeline would only relocate, and multi-language idiomatic output is exactly what it sells. Condition on the spec being a real source of truth (interview answer 2). Fix the spec first if it drifts.
- **Step down to the free OpenAPI Generator** when procurement rules out vendors, air-gapped generation is required, or the language set is small and the team accepts the maintenance load - its output is widely described as technically correct but non-idiomatic, so budget curation effort. It is fully official-grade: Plaid generates its five official SDKs with it (documented in `plaid/plaid-openapi`) - "official" is a support commitment, not a build method.
- **The starved option: the handwritten flagship** (or an in-house pipeline, Stripe's path). Highest value, highest standing effort - vendor-order-of-magnitude estimates put hand-maintaining many languages at multiple engineer-years - so it loses every efficiency round. What promotes it: the API is the core product and one language carries the bulk of revenue traffic. Handwrite that one, generate the rest.
- Guardrails at every rung: keep the OpenAPI spec - not a vendor DSL - the single source of truth, prefer generators that can run self-hosted, and write the exit plan (who regenerates the SDKs if this vendor disappears?) into the decision record before signing.

This ranking is a default, not a law: re-rank against interview answers 4, 5, and 9. A hard self-host requirement deletes the hosted rung outright rather than demoting it.

See [references/build-model-vendor-landscape.md](references/build-model-vendor-landscape.md) for the vendor table, the 2026 consolidation case studies, and the in-house-beats-vendor criteria.

## 5. Decouple the three versioning policies

Stripe states the split directly: SDKs use SemVer; the API is versioned by release date. Write three separate policies and refuse to merge them:

1. **SDK package version** - SemVer per package. Major bump only when the SDK's own surface breaks (renamed method, changed constructor), never merely because the API released a new version.
2. **API version** - owned by the sibling versioning-policy skill (see References); this strategy only records which scheme it is and pins the boundary.
3. **Language-runtime support window** - which host-language versions each SDK supports (Stripe: last 4 Go versions, Node LTS 18+; AWS runs this as an explicitly separate policy from SDK lifecycle). Tie it mechanically to upstream language lifecycles plus a stated grace window.

Publish a mapping table from SDK major version to supported API version(s) - Stripe and AWS both maintain this artifact, and it is what lets the two schemes stay decoupled without confusing integrators. Then set release cadence:

- Fixed monthly train (Azure's model), with Azure's own warning not to publish releases just to keep the cadence.
- Continuous release-on-change (AWS, Google Cloud).

Cadence is a predictability promise to integrators, not a productivity metric.

See [references/language-order-and-versioning-cases.md](references/language-order-and-versioning-cases.md) for the Stripe mechanics and cadence norms.

## 6. Write the deprecation and EOL playbook

Retiring a whole language SDK is a distinct, heavier process than deprecating one API inside it. Adopt the evidence-gated shape of Sentry's published playbook (develop.sentry.dev, the most rigorous public one):

1. **Build the case before announcing anything.** Platform health, registry download trends, usage counts - and the decisive number: revenue at risk, isolating accounts that use this SDK _exclusively_, since customers who also use your other SDKs would barely notice. No EOL announcement without this evidence.
2. **Execute in order: final release → announcement → archive.** Pinned deprecation issue naming the why, the successor, and the timeline; registry deprecation markers; README and docs banners; support/GTM notified. Sentry's real executions each named a specific successor SDK, not just a goodbye.
3. **Clean up 6-12 months after archival** - keep retired docs reachable but de-indexed, redirect to the successor.

Set the timeline numbers from published floors, and cite them honestly.

- AWS commits to ≥24 months of GA support and a ≥6-month maintenance announcement, but its own policies disagree on maintenance duration: 12 months in the core SDKs-and-Tools policy, 6 months in the Powertools docs. Never quote "AWS's policy" as one number without naming which document.
- Azure floors deprecated-library fixes at 12 months (3 years with breaking changes).
- The observed announcement-to-archive range across vendors is 6-24 months. A synthesized 6-step sunset sequence is in the reference file, labeled inferred.

See [references/tier-promotion-and-eol-playbooks.md](references/tier-promotion-and-eol-playbooks.md) for the full AWS phases, Sentry playbook detail, and worked timeline examples.

## 7. Publish the community policy

Decide, in writing, how community SDKs are treated: welcomed and listed with an explicit non-guarantee (Twilio: "not supported by Twilio, and we can't speak to their accuracy/completeness"), ignored, or discouraged. Listing them with a disclaimer is the documented norm and the cheapest coverage extension - it staffs your long tail for free and feeds the step-3 promotion gate. State where support requests route (their repo, not your tickets), and revisit the list when a community SDK's language crosses the step-2 threshold: that is the moment to invoke the promotion gate rather than building a competitor from scratch.

## Failure modes

- **Lock-in through an acquired vendor.** The 2026 consolidation is the cautionary tale to cite by name.
  - Postman acquired Fern (January 8, 2026).
  - Anthropic acquired Stainless (announced May 18, 2026, reported at more than $300M) and wound down its hosted generator. Customers kept their generated code but lost the pipeline that kept SDKs in sync with API changes, while OpenAI, Google, and Cloudflare all depended on it.
  - The fix is step 4's guardrails: spec as source of truth, self-host option, written exit plan.
- **The official-equals-handwritten myth.** Teams over-invest in handwriting because they assume generated SDKs can't be "official". Plaid's five official SDKs are generated with the free OpenAPI Generator. Official is the support commitment in step 3, not the build method in step 4.
- **EOL by gut feeling.** Killing a low-download SDK without Sentry's exclusive-usage revenue check mistakes "small" for "safe to drop" - the few users left may have no other path to your product.
- **Language order from a popularity chart.** Generic rankings put Python first for a fintech platform whose integrators live in Java and Go. No vendor documents deciding from a named ranking. Every documented case maps the buyer's stack first.
- **One version number ruling everything.** Coupling SDK majors to API versions forces breaking releases on integrators whose code didn't break, and vice versa. Three policies, step 5.

## Measurement

- Decision coverage gate: all seven workflow steps end in a written, user-approved policy - 7 of 7, or the strategy is incomplete. Iterate until it passes.
- Language coverage gate: zero languages above your recorded add-threshold without an explicit build-or-decline decision on file.
- Trends to watch after adoption (not pass thresholds): per-language traffic share from client telemetry, per-SDK adoption vs. the direct-HTTP share in each language, and exclusive-usage account counts per SDK - refresh that last one before any EOL conversation, it is the step-6 evidence base.

## Invocation examples

- "We're launching our public API next quarter - which language SDKs should we build first, and should we generate them?"
- "We have handwritten Python and Ruby SDKs and community ones for Go and PHP - define support tiers and a promotion policy."
- "Our PHP SDK has almost no downloads. Build me the case for retiring it - or for keeping it."
- "Should our SDK versions track our API versions? Design the versioning and release-cadence policy."

## References

- [references/build-model-vendor-landscape.md](references/build-model-vendor-landscape.md) - generator vendor table, the 2026 Fern/Stainless consolidation case studies, in-house-pipeline criteria, snippet-parity mechanics.
- [references/tier-promotion-and-eol-playbooks.md](references/tier-promotion-and-eol-playbooks.md) - MCP/Azure/Google tier frameworks, two-tier disclaimer language, the Anthropic-Ruby promotion case, AWS's five phases, Sentry's three-phase EOL playbook, worked timelines.
- [references/language-order-and-versioning-cases.md](references/language-order-and-versioning-cases.md) - documented language-order cases by vertical, Stripe's three decoupled versioning policies, release-cadence norms, the SDK-to-API mapping table artifact.

Registry-specific publishing mechanics (package discoverability, readme codes, download-trust signals) sit outside this skill's scope: it decides which SDKs exist, not how each package is published. The third-party `sdk-dx` skill on skills.sh covers single-SDK ergonomics and polish - this skill decides the portfolio, not any one SDK's developer experience.

See also, same owner:

- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella surface-selection decision that step 1 assumes already answered yes for SDKs; run it first if that hasn't been decided.
- `samber/developer-platform-skills@api-versioning-policy` - owns the API-side versioning and deprecation policy that step 5 deliberately decouples SDK versioning from.
- `samber/developer-platform-skills@api-reference-quality` - audits per-language code-snippet parity in the reference docs, which the SDK portfolio feeds.
- `samber/developer-platform-skills@public-api-design-review` - reviews the API surface consistency every generated SDK inherits and projects into its language.
- `samber/developer-relations-skills@coding-agent-docs-optimization` - structuring SDK source and docstrings so coding agents integrate them unattended; the agent-consumption angle of the SDKs this portfolio ships.
