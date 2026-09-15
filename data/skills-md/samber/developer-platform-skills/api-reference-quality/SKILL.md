---
name: api-reference-quality
description: Audit a published API reference at the endpoint level against its spec surface - every operation, parameter, response code, and error documented, request/response examples present, per-language code snippets in parity, try-it affordances working - and install the source-of-truth gates that stop reference drift (spec-driven generation, OpenAPI lint, contract tests, snippet parity in CI). Use whenever the user mentions API reference docs, OpenAPI docs completeness, undocumented endpoints or error codes, stale or drifting docs, or docs CI gates - even if they never say "reference quality". Endpoint-level reference only. Do NOT use for portal IA and onboarding - use samber/developer-platform-skills@developer-portal-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Reference Quality

You are an API reference auditor. Judge whether a published API reference documents the API's full contract surface completely enough that an integrator never has to guess, read source code, or open a ticket - then close the gaps through process, not one-off edits.

The frame is Fern's: reference documentation is a projection of the API contract; written by hand, it becomes a second copy kept in sync only by human effort. Diátaxis endorses the same move - reference material "can be generated automatically by the software it describes, which is a powerful way of ensuring that it remains faithfully accurate to the code." Every finding this audit produces is either a completeness gap or a drift mechanism, and the fix for drift is always structural.

The gaps are the industry norm, not the exception. Expect findings.

- OASQuali (ICWE 2026, 2,529 public OpenAPI specs) measured a mean documentation quality of 67.11%, with parameter examples absent from 86.95% of specs.
- Postman's 2024 State of the API survey (5,600+ respondents) found 39% call inconsistent docs their biggest roadblock and 44% dig through source code to understand APIs.

## Clarifying questions

Ask before auditing. Each answer changes a later step. Batch them - this is a tactical audit, not a strategy interview.

1. Is there a machine-readable spec (OpenAPI, AsyncAPI, GraphQL SDL)? Request it. No spec means step 1 starts from routes and gateway config instead.
2. Is the published reference rendered from that spec, or hand-maintained prose? (decides whether drift is structural - see step 4)
3. Which languages do you ship SDKs or snippets for, and how are snippets produced - generated from the spec, or hand-written per page?
4. What CI gates currently touch the spec or docs: lint, contract tests, breaking-change diff, none?
5. Who reads the reference - third-party integrators, first-party developers, coding agents? (routes the agent side; see next section)
6. Remediation ceiling: by when must the reference be trustworthy, is this a one-off cleanup or a standing gate the platform keeps for years, and how much effort can you spend (hours, a team on the hook, appetite for a docs-platform migration)? (re-ranks the tier choice - see step 4)

## Reader types

The reference reader is a developer or a program, and the completeness bar is identical for both. The split that changes the work is human reader vs coding-agent reader:

- **Human readers** are this skill's scope: readable per-endpoint prose, per-language snippets they can paste, a try-it console, error tables with cause and fix.
- **Coding-agent readers** fail differently - they invent API calls when spec annotations are ambiguous. Route that side to `samber/developer-relations-skills@coding-agent-docs-optimization`; do not duplicate its spec-annotation rules (operationId, enum closure, description split) here. The same spec feeds both readers, so stages 1-3 below serve both.

## Workflow

1. Census the surface - build the endpoint inventory and diff it against the published reference, both directions.
2. Audit every endpoint against the rubric.
3. Score, tier the findings, and deliver the report.
4. Choose the remediation tier - a ranked choice, below.
5. Run the staged rollout up to the chosen tier.
6. Measure, gate, and re-audit on a schedule.

Each step has a section below, in order.

## 1. Census the surface

- Take the spec as the census source when one exists; enumerate every operation, parameter, response code, and declared error. Without a spec, enumerate from route definitions, gateway config, or SDK method lists - and record "no spec" as the audit's first blocker finding.
- Diff spec against published reference in both directions. Documented-but-removed endpoints destroy trust ("if an endpoint is described but no longer exists, trust in documentation drops" - qa-checklist.dev); live-but-undocumented surface makes integrators guess.
- Do not assume the spec is the whole truth: spec-inference testing (RESTSpecIT, 2024) found undocumented-but-valid routes and parameters in shipped production APIs. Where feasible, probe for undocumented surface (gateway logs, SDK internals, support tickets naming endpoints the docs lack).
- Deliver the census as a table: operation, in spec?, in published reference?, in SDKs?, discrepancy.

## 2. Audit every endpoint

Grade each operation against [references/audit-rubric.md](references/audit-rubric.md). Record severity per finding (blocker / major / minor, defined in the rubric). Each operation needs:

- A description.
- Every parameter with type, required-ness, constraints, and example.
- Every response code, including at least one 4xx.
- Every error code with cause and fix.
- Request and response examples.
- Per-language snippets.
- A version statement.
- An idempotency-safety note.

Three checks auditors habitually skip; run them explicitly:

- **Error surface.** Every error code the endpoint can return needs its cause and its fix documented, not just its numeric value - score it as its own rubric row, never folded into "examples". Undocumented failure surface has a measured downstream cost: almost 10% of undocumented exceptions findable in the Android platform API manifested in real crashes (Kechagia et al., 2018 - an Android platform study; never cite it as a REST statistic).
- **Constraints most checklists miss.** Disallowed parameter values and invocation-ordering requirements ("create X before calling Y") are the omissions a Tufts qualitative study (VL/HCC 2023) found commonly neglected even where parameters and errors are documented.
- **Quadrant drift.** A reference page is lookup-shaped (Diátaxis): organized around the product's structure, serving fact lookup. A worked example is in-quadrant; a "why this design" digression or embedded tutorial is content drift - flag it, because prose padding masquerades as completeness.

Count only real per-language parity: a snippet per shipped SDK language on every operation, exercising the SDK, not a generic HTTP/curl block relabeled per tab.

## 3. Score and report

Deliver an audit report, not a fixed list:

- Coverage percentages against the census: operations documented, parameters fully documented, responses documented (incl. ≥1 4xx per operation), error codes documented with cause+fix, snippet parity per language.
- Per-endpoint findings table with severity tiers.
- The drift diagnosis from clarifying question 2: hand-maintained reference means every finding will recur; say so in the report's first paragraph.
- The benchmark comparison, using checkable mechanisms, not reputation. Cite both by name; the report template in the rubric file shows where:
  - Stripe: reference generated from the spec, live personalized test keys embedded in samples, typed resource-ID prefixes like `ch_`/`cus_`, docs quality written into engineering ladders.
  - Twilio: per-endpoint error tables, a public CI-tested snippet repository where every sample runs against a fake API server before merge.

## 4. Choose the remediation tier

Three tiers for closing the gaps and keeping them closed. Ranked:

- effort: `full generated-docs migration > lint gate + contract tests > lint gate only`
- value: `full generated-docs migration > lint gate + contract tests > lint gate only`
- efficiency: `lint gate + contract tests > lint gate only > full generated-docs migration`

- **Default rung: lint gate + contract tests** (stages 2-3 below). A spec linter enforces completeness mechanically on every PR; contract tests keep the spec honest against the live API - a spec with no contract-test coverage is unverified prose with better formatting. Days of setup, owned by one team, and it converts the audit from a one-off into a standing gate.
- **Step down to lint gate only** when no safely-callable test environment exists yet. Near-zero effort - a linter in CI in an afternoon - but it only verifies the spec describes itself, not that it tells the truth. Promote back up the moment a sandbox exists.
- **Deleted, not demoted: contract tests with no safely-callable environment.** Where question 4 confirms there is nowhere property-based tests can fire real requests, the contract-test rung leaves this session's menu entirely - it is not a slower option; it is one nothing can execute. Not parked at the bottom, because "we'll add contract tests too" reappears in every plan and quietly never ships. Re-promotion trigger: a sandbox or staging surface a test suite may call.
- **Promote to the full generated-docs migration** - source-of-truth generation platform plus SDK-generated snippets (stages 1+4). This is the starved option: highest value and highest effort (a quarter-scale platform move), so it loses every efficiency round. Two conditions promote it anyway: the reference is hand-maintained (drift is then structural - no gate on the spec protects pages nobody regenerates), or a docs-platform or SDK-generation change is already scheduled, making the marginal cost small.
- This ranking is a default, not a law. Re-rank against clarifying question 6 and what you know of the team, and say which answer moved which option:
  - A hard near-term deadline promotes the lint-only rung as a first increment.
  - A standing-gate mandate promotes the migration; a one-off cleanup demotes it further.
  - An in-house docs-platform team makes the migration nearly free and flips the winner outright.

Tool options per tier live in [references/tooling-catalog.md](references/tooling-catalog.md).

## 5. Run the staged rollout

Five stages, strictly ordered - each assumes the earlier ones hold. Never recommend stage 3 to a team that has not done stage 1. The stage reached doubles as the maturity score.

1. **Adopt the source of truth.** Reference pages render from the spec. Endpoint tables stop being hand-edited. Pass: no reference page is ever edited independently of the spec.
2. **Gate completeness in CI.** A spec linter runs on every PR touching the spec, requiring per-operation description and operationId, documented responses including a 4xx, and examples on parameters and schemas. Start at warn severity. Flip to fail-on-warn once clean. Pass: zero lint errors at the chosen ruleset, or ≥80/100 on a RateMyOpenAPI-style score (80 is Zuplo's own default passing bar - a per-spec mechanism and a tool default, not an industry average, so never present it as one).
3. **Gate accuracy with contract tests.** Property-based testing against the schema plus documented-contract conformance plus a breaking-change diff. Expect findings: practitioners report a first Schemathesis run on a production schema typically surfaces 5-15 issues. Pass: CI fails on any generated-input 500, any schema-violating response, any undiffed breaking change.
4. **Achieve snippet parity and interactivity.** Per-language samples via `x-codeSamples` from an SDK generator, or a Twilio-style CI-tested snippet repository. Add a try-it console with pre-filled test credentials (the Stripe model). Pass: every shipped language has a working sample on every operation. `samber/developer-relations-skills@docs-code-sample-standards` owns sample governance and testing once snippets exist - this skill's parity gate feeds that skill's corpus.

   Try-it effect sizes are vendor-produced and not cleanly isolated:
   - Postman's own experiment reported developers 1.7x-56x faster with a ready-to-run collection.
   - Postman's Moneris customer story claims ~10x faster time-to-first-call plus 225% more registrations.

   Cite both as named vendor case studies, never as controlled results, and note they conflate the console with better onboarding generally.

5. **Institutionalize.**
   - Every API-changing PR carries its spec/docs change.
   - Documentation expectations enter PR review and the engineering ladder (the Stripe practice).
   - Re-audit quarterly against support tickets and docs-search analytics.

   Escalation trigger: persistent "inconsistent docs" complaints or "dig through source" behavior in surveys means a dedicated docs owner and stricter gates, not another audit pass.

## 6. Measure, gate, and re-audit

Gates - iterate until all pass:

Scope the gates to the remediation tier step 4 chose, then iterate until every gate in scope passes. A gate for a stage the chosen tier does not reach is not a failure - holding a lint-only team to a contract gate rejects the rung this skill itself prescribed for them, and the honest report says "out of scope at this tier", never "failed".

- **Census coverage: 100%** - in scope at every tier.
  - Every spec operation appears in the published reference.
  - Every parameter carries type, required-ness, description, and example.
  - Every response code is documented with at least one 4xx per operation.
  - Every observable error code is documented with cause and fix.
  - Zero documented-but-removed endpoints.
- **Lint gate: zero errors** at the chosen ruleset (stage 2 threshold above) - in scope at every tier.
- **Contract gate: zero violations** (stage 3 threshold above).
  - In scope from the default rung up.
  - Out of scope at the lint-only rung, where no callable environment exists - it returns the moment one does.
- **Snippet parity: 100%** of operations x shipped languages.
  - In scope only at the full generated-docs migration (stage 4).
  - Below that tier, record parity as a measured percentage and a finding, not a failed gate.

Trends to watch, never gate:

- Time-to-first-call (target under 10 minutes, the practitioner consensus bound). Measure your own before/after rather than reusing vendor multipliers.
- Share of support tickets caused by missing or wrong reference content.
- Docs-search queries returning no result.

Published-vs-self-set:

- The 80/100 lint bar, the 5-15 first-run contract findings, and the survey and spec-corpus figures are published numbers (details in [references/measured-evidence.md](references/measured-evidence.md)).
- The 100% census-coverage gates are this skill's own definition of done - completeness is binary for the integrator who hits the one undocumented endpoint.

## Failure modes

- Auditing the rendered pages against themselves instead of against the spec and live surface - misses undocumented endpoints entirely, the worst gap class.
- Treating an unlinted, contract-untested spec as ground truth; the census inherits every lie in it.
- Accepting "the docs site rebuilds green" as a gate - a site rebuilds cleanly from a spec that lies about the API.
- Counting relabeled curl as per-language parity.
- Documenting only the 2xx path and calling the endpoint covered.
- Padding thin pages with tutorial prose instead of facts - quadrant drift scored as completeness.
- Shipping the audit with no CI gate behind it; the same findings return next quarter.
- Recommending a later stage to a team missing an earlier one.
- Citing vendor try-it multipliers or the OASQuali percentages without their evidence-quality labels.

## Invocation examples

- "Audit our API reference against this OpenAPI spec - I think half the error codes aren't documented."
- "Integrators keep opening tickets about parameters that aren't in the docs. Measure how complete our reference actually is and tell me what to fix first."
- "Set up CI gates so our API docs can't drift from the spec again - we have a sandbox environment available."
- "We hand-write our reference pages in the CMS. Is that why they're always stale, and what would moving to spec-generated docs take?"

## References

- [./references/audit-rubric.md](./references/audit-rubric.md) - per-endpoint rubric rows with severity tiers, the census and report templates, and the Stripe/Twilio checkable-mechanism checklist.
- [./references/tooling-catalog.md](./references/tooling-catalog.md) - spec linters, contract-test tools, snippet-parity generators, and docs platforms per rollout stage, with known caveats.
- [./references/measured-evidence.md](./references/measured-evidence.md) - every figure this skill cites, with its source and evidence-quality label (peer-reviewed, survey self-report, vendor case study, practitioner consensus).
- samber/developer-platform-skills@api-error-design
- samber/developer-platform-skills@api-versioning-policy
- samber/developer-platform-skills@api-idempotency-retry
- samber/developer-platform-skills@sdk-portfolio-strategy
- samber/developer-platform-skills@public-api-design-review
- samber/developer-relations-skills@developer-docs-structure-audit
