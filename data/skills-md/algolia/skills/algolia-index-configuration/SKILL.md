---
name: algolia-index-configuration
description: >
  Algolia index settings and relevance configuration guidance. Use when configuring searchableAttributes, attributesForFaceting, customRanking, ranking, replicas, virtual replicas, rules, synonyms, typo tolerance, distinct, filters, optional filters, merchandising, browse/category relevance, or A/B-testable relevance changes. Also use when auditing, reviewing, health-checking, or troubleshooting an EXISTING index's settings — "is this configured correctly", inherited implementations, relevance regressions, or a settings review before launch — not only when configuring something new. Do NOT use for live settings writes, backups, copies, or operational account tasks; use algolia-cli or algolia-mcp instead. Do NOT use for record-shape or variant strategy; use algolia-data-modeling instead.
license: MIT
metadata:
  author: algolia
  version: "0.4"
---

# Algolia Index Configuration

Use this skill when changing how Algolia ranks, filters, facets, merchandises, or sorts results. Relevance configuration should reflect the business outcome and the user's decision path.

## Customer-Facing Standard

- Capture the current settings or assumptions before recommending changes.
- Tie every setting change to a business goal and representative query set.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Produce settings, expected tradeoffs, rollback notes, and validation queries.
- Produce a settings decision record that distinguishes deterministic constraints, ranking preferences, and query-specific merchandising.

## Official Companion Skills

- Use official `algolia-cli` for live settings, rules, synonyms, replicas, backups, or configuration changes.
- Use official `algolia-mcp` for live search behavior, analytics, top searches, no-result queries, click positions, and recommendation evidence.
- Use official A/B testing guidance or tools when an experiment is in scope; keep this skill focused on hypothesis, evidence, decision criteria, and rollback.
- Use this skill after the official tool call to explain tradeoffs, test queries, rollback expectations, and customer-facing validation criteria.

## Source-Of-Truth Rules

- Do not change or recommend live settings without first capturing the current settings or stating that the plan is provisional.
- Use official `algolia-cli` for settings, rules, synonyms, replicas, and backups; use this skill to design and explain the change.
- Verify current docs or official skill guidance before relying on feature behavior such as replicas, virtual replicas, rules, optional filters, or A/B testing.

## Workflow

1. Read `references/configuration-guide.md` before editing settings.
2. Capture current settings before modifying an existing index.
3. Ask what good results mean for the use case: exactness, availability, popularity, margin, recency, location, personalization, editorial priority, or diversity.
4. Classify each relevance lever: deterministic filter, textual match priority, tie-breaker, optional preference, query-specific rule, or explicit sort.
5. Make the smallest coherent settings change and describe expected tradeoffs.
6. Validate with representative queries, facet/filter combinations, query rules, sorts, and no-result cases.
7. For material changes, write the hypothesis, baseline, success metric, experiment decision rule, and rollback trigger before launch.

## Questions To Ask

- Which queries or browse pages are most valuable or currently broken?
- Which attributes should match first, and which should only help recall?
- Which business metrics should break textual ties?
- Which filters must be available to users, and which filters are applied silently?
- Do sort orders need replicas, and are those sort orders allowed to weaken relevance?
- Are synonyms and rules global, seasonal, category-specific, or campaign-specific?
- Which constraints are non-negotiable filters, and which are preferences that can rank lower but still return results?
- Which terms need typo protection or exact treatment, such as SKUs, part numbers, acronyms, postal codes, or regulated names?

## Implementation Standards

- Prefer ordered `searchableAttributes` that reflect the user's mental model.
- Put numeric or boolean business signals in `customRanking`, not in frontend sort hacks.
- Declare only needed `attributesForFaceting`; use searchable facets where users search inside facets.
- Searchable facets are a three-part contract, not a settings flag: declare `searchable(attribute)` in `attributesForFaceting`, enable search-within-facet in the UI widget (e.g. `searchable: true` on a refinement list), and verify with a live facet-value search. For facets users know by name — brand, merchant, designer — default to searchable even at moderate value counts: it costs nothing and real catalogs grow. A plain facet on a 30+-value attribute is a defect, not a default; below that, skipping it is a documented judgment call, not a silent omission.
- Know the facet-stats trap: numeric `filters` work WITHOUT any `attributesForFaceting` declaration — that success is misleading. Range widgets (sliders, min/max bounds, `connectRange`) need the attribute declared as a full facet to return facet statistics, and `filterOnly()` does NOT produce stats. Verify by requesting `facets: ["<attr>"]` and checking the response's `facets` object is non-empty — never by checking that filtering works.
- Restrict what public responses carry: business-internal ranking signals (popularity, sales velocity, margin, review counts used for ranking) belong in `customRanking`, not in the payload. Set `attributesToRetrieve` to the fields the UI displays (plus event-attribution needs) and verify with a live query using the public search key that internal fields are absent.
- Treat hierarchy as a deterministic call, not a preference: when records carry hierarchical category data (`hierarchicalCategories.lvl0/lvl1` or equivalent) and the index or UI filters on a flat mixed-level list, that is a defect to fix — declare the level facets and use a hierarchical widget. Flat mixed-level lists break drill-down and facet counts.
- Treat synonyms and rules as governed relevance assets. Name, scope, and test them.
- Use replicas for explicit sort-by experiences and virtual replicas where relevant sorting fits the use case.
- Avoid irreversible production changes without a settings backup or repeatable configuration file.
- Keep deterministic constraints in filters or secured filters. Use optional filters only when a result may still be relevant without the preference.
- Treat facet configuration as a user decision contract: declare only attributes users need to refine, choose searchable facets only when users search within values, and test counts after common refinements.
- Use synonyms for genuine language equivalence. Use rules for bounded intent, promotions, redirects, or merchandising with a condition, owner, and review/expiry date.
- Protect identifiers and exact-sensitive terms with current documented typo settings rather than weakening all search behavior.
- Treat every sort choice as a relevance decision. Document the replica type, displayed sort label, expected loss of relevance, and whether filters/facets remain consistent.
- Change one meaningful relevance variable per experiment. Do not infer causality when ranking, rules, data, and UI changed together.

## Settings Audit Checklist

When reviewing an existing index, do not stop at "nothing is erroring." The costliest configuration defects are symptom-free: the store works, queries return, and the settings are still wrong. Check each of these against the live settings, not the code:

- `searchableAttributes`: a real ordered array (no comma-joined strings), name/brand-class attributes above descriptive text, deliberate `unordered()` choices.
- `customRanking`: does a near-unique numeric lead the chain (raw popularity, raw sales)? If so, later tie-breakers are inert — bucket the leading signal and require a complete ordered chain. Adding one availability flag is necessary but not sufficient.
- Facet completeness: every attribute the UI filters, sorts bounds, or drills into is declared with the right mode — `searchable()` for name-known or high-cardinality pickers (default it on for brand-like facets; document the decision if skipped), full facet (never `filterOnly`) for range widgets, hierarchical levels when hierarchical data exists.
- Retrieval hygiene: query the index with the public search key and read the hit payload — internal ranking fields present is a finding.
- Replica parity: fetch each replica's settings and diff against the primary — replicas inherit at creation only, and drifted replicas (or replicas missing their sort criterion entirely) sort wrong while looking configured.
- Key scope: prefer a secured or index-restricted search key in production over the app-wide search key; if the plain key ships, document why.

## Anti-Patterns

- Concluding a numeric attribute doesn't need faceting because raw `filters` still work — range widgets need declared facets for stats, and `filterOnly()` does not produce them.
- Declaring a settings review complete without querying the live index as the public key would (retrieval payload, facet stats, replica sort order).
- Tuning relevance with one anecdotal query instead of a representative query set.
- Using synonyms to compensate for missing data or unrelated concepts.
- Pinning or burying results globally when the intent is category, campaign, locale, or segment-specific.
- Adding every possible facet, which slows decision-making and creates noisy filters.
- Letting custom ranking overpower exact-match or permission-sensitive behavior without testing.
- Using optional filters to enforce availability, permission, region, or compliance constraints that must never be violated.
- Using synonyms where a scoped rule, data correction, or typo exception is the real solution.
- Interpreting an A/B test before sufficient event-backed data and confidence exist, or stopping and restarting a test as if it were continuous.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for relevance learning objectives and public Algolia docs for searchable attributes, ranking, facets, synonyms, rules, replicas, merchandising, and A/B testing. Map the work to maturity level and use case, then turn source guidance into questions, test queries, and validation criteria rather than copied reference text.

## Maturity Behavior

- Beginner implementation: define the first coherent searchable attributes, facets, and ranking signals from the customer journey.
- Production readiness: capture settings backup, deterministic-versus-optional filter decisions, representative query set, rollback notes, secured filters, and launch-impact checks.
- Optimization: require baseline queries, analytics signals, one-variable A/B-test plan, merchandising scope, confidence interpretation, and expected before/after behavior.
- AI readiness: preserve deterministic filters, secured data, business rules, and measurement while validating NeuralSearch or Agent Studio dependencies.

## Output Contract

Return settings changes as code or JSON, a settings decision record, relevance intent, test queries, and assumptions requiring business review. Include before/after expectations for top queries, hard/optional constraint behavior, experiment criteria, and rollback triggers when relevance changes are material.
