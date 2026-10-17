---
name: algolia-neuralsearch
description: >
  Product-specific Algolia NeuralSearch implementation, validation, and optimization guidance. Use when planning, enabling, configuring, testing, or tuning NeuralSearch, AI relevance, semantic retrieval, adaptive intent, model training, A/B testing, limitations review, query analysis, relevance diagnostics, event readiness, and data preparation for neural or hybrid search experiences. Do NOT use for generic vector database, embeddings, or non-Algolia semantic search architecture. Do NOT use for live settings changes, replica creation, or analytics retrieval; use algolia-cli or algolia-mcp first, then this skill for readiness and rollout guidance.
license: MIT
metadata:
  author: algolia
  version: "0.4"
---

# Algolia NeuralSearch

Use this skill when adding or optimizing NeuralSearch. Neural relevance depends on good records, explicit relevance intent, representative queries, and measurement signals; do not treat it as a switch that fixes poor data. Current public docs state that click and conversion events are not required to activate NeuralSearch, but when present they guide semantic attribute selection and unlock retraining and Adaptive Intent; recheck them before advising on activation.

## Customer-Facing Standard

- Treat NeuralSearch as a rollout decision, not a standalone toggle.
- Require evidence for data readiness, event readiness, query evaluation, filters, permissions, and rollback.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Produce a clear go, limited rollout, fix-first, or do-not-start recommendation.

## Official Companion Skills

- Use official `algolia-mcp` for live query behavior, top searches, no-result searches, click/no-click signals, recommendations, and analytics evidence.
- Use official `algolia-cli` when settings, replicas, rules, synonyms, or index changes are required.
- Use this skill after the official tool call to produce rollout readiness, semantic query sets, measurement plans, and customer-facing launch guidance.

## Source-Of-Truth Rules

- Verify current NeuralSearch docs before stating activation steps, limitations, model training behavior, Adaptive Intent requirements, A/B testing behavior, or replica/sort constraints.
- Current public docs state that click and conversion events are not activation prerequisites: without events NeuralSearch selects semantic attributes from record structure, and with events it selects and weights attributes from real behavior. Adaptive Intent and retraining do depend on engagement data. Recheck the chosen mode's current docs before advising on cold-start, preview, activation, model training, or Adaptive Intent behavior.
- Do not recommend launch without a representative query set and a rollback or staged rollout plan.

## Workflow

1. Read `references/neuralsearch-guide.md` before implementation or review.
2. Read `references/example-output.md` when producing a readiness report or rollout plan.
3. Use `$algolia-discovery-planning` to clarify the search journey, success metrics, and query patterns.
4. Use `$algolia-data-modeling` to ensure semantic fields, titles, descriptions, categories, and attributes are search-ready.
5. Use `$algolia-index-configuration` to preserve the right balance of textual relevance, filters, facets, custom ranking, replicas, and business rules.
6. Use `$algolia-events-insights` and `$algolia-release-qa` for event readiness, A/B testing, analytics, and launch validation.
7. Teach the rollout path: confirm eligibility and readiness, preview with a representative query set, test with a replica or controlled configuration, compare against baseline, tune one semantic variable at a time, then monitor and optimize.

## Questions To Ask

- Which query classes should NeuralSearch improve: vague, conceptual, natural-language, synonym-heavy, long-tail, support/content, or product discovery queries?
- Which queries must remain exact, deterministic, compliance-sensitive, or heavily merchandised?
- Which record fields carry semantic meaning, and which are noisy or internal?
- Is the customer's plan and application eligible for the NeuralSearch mode they want to use?
- Will testing happen in a replica, an A/B test, a staged rollout, or a manual evaluation environment?
- Which semantic behavior should be conservative, broader reach, or append-only relative to keyword relevance?
- Are click, conversion, view, add-to-cart, purchase, or feedback events available to evaluate relevance?
- What is the baseline: current conversion, CTR, zero-result rate, no-click searches, top-query relevance, or manual judgment set?
- Is A/B testing available before broad rollout?
- Which limitations, language/locale constraints, filters, and sort expectations need to be reviewed in current docs?
- Which attributes should carry semantic meaning, in priority order, and which attributes must never influence semantic matching?
- For a surprising result, which evidence will distinguish a data problem, semantic-setting choice, keyword behavior, or merchandising override?

## Implementation Standards

- Audit records before enabling neural relevance. Titles, descriptions, categories, brand, attributes, and content summaries should reflect how users search.
- Keep filters, facets, secured data, and business rules explicit; semantic matching must not leak inaccessible or irrelevant records.
- Build a query evaluation set that includes head, tail, exact, vague, natural-language, branded, typo, category, and no-result queries.
- Use A/B testing or a staged rollout for meaningful relevance changes.
- Do not optimize only by subjective spot checks. Pair human review with analytics and event signals.
- Document limitations and feature constraints from current Algolia docs before promising behavior.
- Use explainability tools or result inspection to diagnose surprising results before changing many settings.
- Treat merchandising rules as compatible with NeuralSearch, but test pinned, buried, suppressed, promoted, and campaign-driven results against semantic behavior.
- Use analytics tags, replica comparisons, or A/B test segmentation so NeuralSearch impact can be isolated from unrelated relevance changes.
- Select a small, meaningful semantic attribute set and justify the priority of each field; do not let IDs, supplier boilerplate, internal notes, or duplicated text dilute semantic meaning.
- Compare hybrid behavior by result origin where current diagnostics expose it: keyword match, semantic match, or both. Use this evidence to diagnose rather than guessing from a result list.
- Change one meaningful variable per evaluation round: semantic fields or priority, blend behavior, business rule, or ranking context. Keep the before/after query set and decision record together.

## Anti-Patterns

- Treating NeuralSearch as a fix for poor record content, missing filters, weak relevance settings, or unclear business rules.
- Evaluating only aggregate conversion or a handful of favorable queries.
- Ignoring exact-match, compliance, permissions, merchandising, or sorted-result regressions.
- Claiming events are required to activate NeuralSearch, or skipping event readiness entirely because activation does not require events; events still gate Adaptive Intent, retraining, and trustworthy measurement.
- Promising Adaptive Intent or model-training behavior without checking current docs and event readiness.
- Treating semantic configuration as a one-time activation choice instead of a testable, reversible relevance decision.
- Diagnosing a surprising result by changing multiple fields, ranking rules, and merchandising settings at once.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for NeuralSearch and AI-readiness learning objectives and public Algolia docs for semantic retrieval, data readiness, events-informed optimization, A/B testing, limitations, and current rollout guidance. Map the request to maturity level and use case, then produce guided prompts such as "Use this skill to design my NeuralSearch rollout" or "Use this skill to validate my data, measurement path, and query set before rolling out NeuralSearch."

## Maturity Behavior

- Beginner implementation: do not start with NeuralSearch if basic data, filters, and search UI are not yet stable.
- Production readiness: require deterministic filters, secured data strategy, rollback plan, and query evaluation set.
- Optimization: compare semantic relevance against baseline relevance with representative query classes and outcome metrics.
- AI readiness: prefer reliable events and feedback loops for measurement and Adaptive Intent readiness, while requiring permission-aware records and a clear go/fix-first/do-not-start recommendation.

## Output Contract

Return a NeuralSearch readiness assessment, semantic attribute rationale, query test set, measurement plan, rollout strategy, explainability/diagnostic plan, and validation report. Call out missing data, missing or weak events, noisy fields, unsupported feature constraints, or business-rule conflicts before recommending launch.
