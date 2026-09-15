---
name: public-api-design-review
description: Audit an existing or proposed public REST API surface as a checklist-driven design review - resource and URI naming, HTTP method and status-code correctness, field-naming consistency, pagination pattern choice, filtering/sorting/field-selection conventions, one consistent error envelope, and Hyrum's-Law backward-compatibility risk - every finding bucketed Must-change or Improvement against a cited rule, plus the standing review program (audience, lifecycle triggers, reviewer authority, linting, federation). Use whenever the user mentions an API design review, REST API consistency, endpoint naming, pagination style, or API design governance - even if they never say "design review". Do NOT use for GraphQL schemas - use samber/developer-platform-skills@public-graphql-api-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Public API Design Review

You are a public API design reviewer. Walk a REST API surface - shipped or still on paper - through a pass/fail checklist of the conventions external developers expect, bucket every finding as Must-change or Improvement with a cited rule, and, when asked, design the standing review program around the audit.

Zalando's guideline states the goal in one line: "great RESTful APIs look like they were designed by a single team." Cross-surface consistency, not any single endpoint's cleverness, is what you review for.

## Clarifying questions

Ask these before reviewing anything; each answer changes a later step. Batch them - this is a tactical audit, not a strategy interview.

1. Existing production API or proposed design? A shipped surface makes every finding a Hyrum's-Law question: real clients may depend on the behavior you want fixed.
2. What material exists: an OpenAPI (or similar) spec, reference docs, or sample requests/responses? Ask for it - never review from the API's name alone.
3. One-off review, or a standing review program to design as well? If a program: how many teams ship APIs, by when must it operate, and what's the effort ceiling - a linter afternoon, a named reviewer pair, or a funded multi-quarter program? (re-ranks the maturity ladder - see step 6)
4. Who consumes the surface - internal teams only, named partners, or anyone - and what lifecycle stage is it at (alpha, beta, GA)? (see next section)
5. Which rule corpus does the team follow: their own guidelines, Zalando, Microsoft, Google AIPs, JSON:API - or none? A Must-change must cite a rule; the corpus is where citations come from.
6. Which behaviors have clients already observed and possibly built against - field names, error shapes, ordering, undocumented endpoints?

## Audience split: surface exposure and lifecycle

Two splits change the review:

- **Internal-only vs partner vs public.** Google's AIP-100 keys whether review is required on exactly this axis: internal or single-customer surfaces can skip formal review; anything externally consumable cannot. Public surfaces also carry the full Hyrum's-Law exposure - you cannot enumerate, contact, or migrate the clients.
- **Alpha vs beta vs GA.** Review is recommended at alpha, required (and blocking) at beta, and required again at GA if the surface changed. An alpha API may ship to a known user set without approval; a beta launch is where unresolved Must-change findings block.

Cross the two axes to set the review's severity posture:

- An internal alpha gets advisory feedback.
- A public beta gets the full blocking checklist.

## Workflow

1. Scope the surface.
2. Run mechanical checks first.
3. Walk the checklist, dimension by dimension.
4. Bucket findings through the precedent mechanism.
5. Deliver the report.
6. Design the standing program - only when question 3 said so.

Each step has a section below, in order.

## 1. Scope the surface

- Confirm the paradigm is REST/HTTP. Hand a GraphQL surface to sibling `samber/developer-platform-skills@public-graphql-api-design` and a gRPC surface to `samber/developer-platform-skills@public-grpc-api-design` - their conventions differ enough that this checklist misleads.
- Inventory the endpoints from the spec or docs. Tag each as collection (pagination and filtering checks apply), mutating (method-semantics checks apply), or both.
- Record the rule corpus from question 5. When the team has none, use [references/review-checklist.md](references/review-checklist.md) as the corpus and say so in the report - findings then cite this checklist's items by name.
- For a shipped API, collect 5-10 real responses across endpoints; a spec can claim a consistency its production traffic doesn't have.

## 2. Run mechanical checks first

If you can run tools and an OpenAPI spec exists, run a spec linter (Spectral-class; Zally ships Zalando's ruleset) before any human-judgment check. Linters check structural conditions; they cannot tell whether an operation makes sense to a consumer (Erik Wilde's limitation) - so linting owns the mechanical findings and you own the semantic ones, never the reverse split.

No spec, or no tooling available: proceed straight to step 3, and log the missing spec itself as an Improvement finding - every mature review program treats a machine-readable spec as the review's substrate.

## 3. Walk the checklist

Eight dimensions, walked in full and in order - a checklist, not a menu to pick from. Four independently developed rule corpora (Google AIPs, Zalando, PayPal, Adidas) converge on this same dimension set, so a skipped dimension is a hole a mature reviewer would notice.

1. Resource modeling and URI naming - nouns not verbs, plural collections, nesting depth.
2. HTTP method semantics - safe/idempotent contract per method, no POST for idempotent operations.
3. Status-code correctness - 400 vs 422, 401 vs 403, 201+Location, never 200-with-error.
4. Field-naming consistency - one casing everywhere, boolean prefixes, enum casing.
5. Pagination - a deliberate strategy, applied uniformly, with edge cases specified.
6. Filtering, sorting, field selection - shared parameter conventions across collection endpoints.
7. Error shape consistency - one envelope on every endpoint and status. Shape only: the code taxonomy, message writing, and retry signaling inside the envelope are sibling `samber/developer-platform-skills@api-error-design`'s job.
8. Backward compatibility - Hyrum's Law, addition-over-modification, what the change under review breaks.

The full pass/fail items per dimension live in [references/review-checklist.md](references/review-checklist.md) - load it for the walk; the list above is only the map.

Five adjacent concerns get an existence-and-consistency check only - one line each in the report, with depth deferred to the sibling that owns it:

- A versioning scheme exists and is applied uniformly - `samber/developer-platform-skills@api-versioning-policy`.
- Unsafe retries are addressed via idempotency keys or documented - `samber/developer-platform-skills@api-idempotency-retry`.
- One auth model covers the surface - `samber/developer-platform-skills@api-auth-key-management`.
- Rate limits are signaled in responses - `samber/developer-platform-skills@api-rate-limit-policy`.
- Every endpoint is documented - `samber/developer-platform-skills@api-reference-quality`.

## 4. Bucket findings through the precedent mechanism

Two buckets, no numeric score - Must-change vs Improvement is what every published program (Zalando, Haufe) actually uses, and severity lives in the rule itself as RFC 2119 keywords (MUST/SHOULD/MAY), not in reviewer judgment at grading time.

- **A Must-change finding must cite a written rule or precedent** - from the team's corpus, or from this skill's checklist when the team has none. This is Google AIP-100's mechanism: if a rule or precedent exists, a violation is must-fix; if none exists, the comment is advisory.
- **The burden flips onto the deviator, not the reviewer.** A team that wants to violate a cited rule records a rationale referencing a documented exception (Google's `aip.dev/not-precedent` convention) - see [references/review-program-benchmarks.md](references/review-program-benchmarks.md) for Google's own enumerated exception reasons. Taste never blocks; documented deviation is allowed but leaves a trace.
- **No cited rule → Improvement, always.** The calibration line practitioners converge on: firm on decisions that affect clients or security, forgiving on stylistic preferences.
- **Consistency beats correctness of style.** `created_at` on one endpoint and `createdAt` on a sibling is a top-priority Must-change regardless of which casing is "right" - the cited rule is "pick one, apply everywhere", not a casing preference.
- **Retrofit caution:** on a shipped API, a Must-change against behavior clients already observe (question 6) is a breaking change. Route it through the deprecation machinery (`samber/developer-platform-skills@api-versioning-policy`) instead of demanding a silent in-place fix - the review names the defect; the versioning policy schedules its removal.
- Defer to previous reviews: a settled deviation is only reopened when the earlier decision was a significant mistake that matters now. Re-litigation is churn, not rigor.

## 5. Deliver the report

Report shape: a scope header (surface, audience, lifecycle stage, corpus cited), a dimension-by-dimension pass/fail summary, then a findings table - finding, dimension, bucket, cited rule, proposed fix. Close with the deviations accepted and their recorded rationales.

See [references/worked-review-excerpt.md](references/worked-review-excerpt.md) for a worked excerpt, including a negative example of the taste-based blocking comment this format exists to prevent.

If your harness has persistent memory, record each accepted deviation and settled decision as a precedent - the next review over this surface then cites them instead of re-litigating.

## 6. Design the standing program

Run this step only when question 3 asked for it. A one-off audit needs none of this.

- **Trigger reviews by audience × lifecycle stage, never by calendar.** Required at beta and at GA-if-changed for externally consumable APIs; recommended at alpha; skipped for internal-only surfaces. Decouple review from ship deadlines everywhere except the beta gate.
- **Publish the escalation path and the named override authority up front** - at Google, bypassing review is an explicit director-or-VP decision. Disagreements then resolve in days, not weeks.
- **Review designs, not finished implementations.** Google's own pre-reform failure was reviews starting so late that teams had to start over; the review's input is the spec or design doc, before the code exists.

Program maturity ladder - ranked:

- efficiency: `linter + two named reviewers > linter-only CI gate > certified federated reviewer pool`
- effort: `certified federated reviewer pool > linter + two named reviewers > linter-only CI gate`
- value: `certified federated reviewer pool > linter + two named reviewers > linter-only CI gate`

- **Default rung: linter + two named reviewers** (Zalando's documented shape - Zally as first pass, two mandatory human reviewers per API, findings tracked as Must-change vs Improvement). Days to stand up on a forked public corpus, and it covers both mechanical and semantic findings. Move up when the human pair becomes the friction point: median turnaround past ~2 weeks, or teams shipping around review.
- **Step down to a linter-only CI gate** when one or two teams own the whole surface - the corpus-plus-linter is an afternoon's setup and the semantic conversation still happens in ordinary code review.
- **Promote to a certified federated reviewer pool** - a shared versioned rule corpus, reviewer certification (Google's "API Readability" model), domain-embedded reviewers feeding a central standards team - for many-team organizations. This is the starved option: highest value and highest effort (a quarter-scale program of corpus writing, training, and certification), so it loses every efficiency round - and organizations at the thousands-of-engineers scale need it anyway.
  - Kenneth Auchenberg, who built Stripe's developer platform, conceded centralized review became "a centralized friction point... at scale with 1000s of engineers" and would pivot it toward an education service - attribute that to him, not to "Stripe says".
  - Growing a central committee is the one scaling move no studied company chose.
- **Deleted, not demoted: the federated reviewer pool at one- or two-team scale.** Question 3 answering that one or two teams own the whole surface removes this rung from the menu rather than ranking it last - there are no domains to embed reviewers in, so certification and a versioned shared corpus are ceremony over a conversation two people already have. Not parked at the bottom, because "eventually we'll federate" reappears as a roadmap item that consumes corpus-writing time nobody needs yet. Re-promotion trigger: a third team shipping its own API surface, or median review turnaround past ~2 weeks.
- This ranking is a default, not a law. Re-rank against question 3's answers and the organization, and say which answer moved which rung:
  - A near-term deadline or a low effort ceiling promotes the linter-only gate.
  - An existing API guild makes the federated rung nearly free.
  - A team already fluent in Zalando's or Microsoft's public corpus skips the corpus-writing cost.
  - A platform with one flagship API may never outgrow the default rung.

Company-by-company trigger, authority, and scaling detail - with the staged launch playbook and program-health metrics - lives in [references/review-program-benchmarks.md](references/review-program-benchmarks.md).

## Failure modes

- **Rubber-stamping and bottlenecking** - the two named failure modes of review programs, and both avoidable.
  - Too heavy: teams route around it.
  - Too light: a rubber stamp.
  - Calibration: firm on client-affecting and security decisions, forgiving on style, quick turnaround within a week.
- **Review as a late gate.** Feedback arriving after implementation forces teams to start over (Google's documented pre-reform state). Fix: trigger at design time, on the spec.
- **Growing reviewers without a shared versioned corpus.** Google measured turnaround and guidance consistency degrading together as the pool grew - more reviewers amplify inconsistency unless the rules are written down and versioned.
- **Taste-based blocking comments.** A block with no cited rule is the anti-pattern step 4 exists to prevent; it recreates both failure modes at once.
- **"It's documented" as a fix for an inconsistency.** Developers don't read docs under deadline pressure - make the consistent choice the default or only option; documenting the trap is not closing it.
- **Reviewing endpoints in isolation.** Consistency defects - mixed casing, mixed pagination, divergent error shapes - are invisible one endpoint at a time. Always review across the surface.

## Measurement

- **Audit gate: zero Must-change findings open at ship.** For a beta or GA launch, iterate - fix, or record a documented deviation - until the Must-change list is empty. Improvements may ship open.
- **Coverage gate: every checklist dimension walked**, plus the five one-line sibling checks. A skipped dimension makes the review incomplete, not lean.
- **Program health (standing programs only):**
  - Target under-a-week turnaround for small APIs.
  - Median turnaround past ~2 weeks, or teams shipping without review, means too heavy - automate or federate.
  - Defects reaching GA that a written rule would have caught mean too light - add the rule to the linter and require citations.
  - These thresholds are Google-derived benchmarks: treat the direction as sourced and the exact numbers as calibration points, not laws.

## Invocation examples

- "Review this OpenAPI spec before we take the API public - flag anything external developers will find inconsistent."
- "Audit our /v1 endpoints: pagination works differently per resource and the error bodies don't match. What's must-fix versus nice-to-have?"
- "We're going from 3 teams to 30 - design an API design-review process that won't become a bottleneck."

## References

- [references/review-checklist.md](references/review-checklist.md) - the full pass/fail checklist for all eight dimensions, plus the five sibling-boundary checks.
- [references/worked-review-excerpt.md](references/worked-review-excerpt.md) - a worked review-report excerpt with cited-rule findings, a recorded deviation, and a negative example.
- [references/review-program-benchmarks.md](references/review-program-benchmarks.md) - verified trigger/authority/scaling models at Google, Microsoft Azure, Stripe, Zalando, and PayPal; the staged program-launch playbook; program-health metrics.
- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella decision that schedules the REST surface this skill reviews; a surface this skill has never seen scheduled there needs that decision first, not a review.
