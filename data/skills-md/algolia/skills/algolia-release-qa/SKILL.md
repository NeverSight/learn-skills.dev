---
name: algolia-release-qa
description: >
  Algolia launch, regression, and implementation QA. Use when auditing an Algolia build before release, validating relevance changes, checking search UI behavior, verifying event instrumentation, diagnosing analytics gaps, reviewing secured keys, or creating a smoke test plan for search, browse, autocomplete, indexing, and configuration changes. Do NOT use to make live account changes or inspect live account data; use algolia-mcp or algolia-cli first. Do NOT use as the primary implementation skill when the task is clearly data modeling, events setup, InstantSearch, Autocomplete, NeuralSearch, or Agent Studio; use the focused skill first and this skill for final QA.
license: MIT
metadata:
  author: algolia
  version: "0.5"
---

# Algolia Release QA

Use this skill before launching or after a risky change. Prioritize defects that affect discoverability, conversion, analytics integrity, security, or operational rollback.

## Customer-Facing Standard

- Lead with launch blockers and high-risk findings, not a generic summary.
- State what was tested, what was not tested, and what evidence supports each finding.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Do not say launch-ready without validating data, settings, UI, events, security, and rollback where relevant.
- Build an evidence matrix before assigning a release status: evidence must identify the surface, scenario, source, result, owner, and remaining risk.

## Official Companion Skills

- Use official `algolia-mcp` for live search, analytics, recommendations, index discovery, and evidence gathering.
- Use official `algolia-cli` for settings, rules, synonyms, records, keys, backups, and admin verification.
- Use official `instantsearch` for UI implementation correctness, framework-specific source-of-truth checks, and frontend search QA.
- Use official `algobot-cli` for Agent Studio, conversational, RAG, memory, tool, and deployment QA.
- Use this skill after official tool calls to write severity-led customer findings, owners, fixes, tests run, and residual risk.

## Source-Of-Truth Rules

- Do not mark an implementation launch-ready from screenshots or code alone when data, settings, events, security, or rollback are in scope.
- Use official tools for live evidence and current docs for feature-specific requirements.
- Separate verified findings from untested risks. If evidence is missing, say exactly what could not be inspected.
- For search implementations, use the cross-skill readiness signposts from `algolia-search-implementation` before saying launch-ready, prototype-ready, or ready with documented follow-ups.

## Workflow

1. Read `references/release-qa-checklist.md` for the relevant surface.
2. Read `references/example-output.md` when writing a customer-facing launch or regression report.
3. For any frontend surface, run the Finish Gates below in a real browser or with `scripts/page-smoke.mjs` before writing a single "verified" — and read `references/verified-cdn-urls.md` before trusting any `<script src>`.
4. Capture what changed: data model, settings, UI, events, environment, credentials, or deployment.
5. Test representative happy paths and failure paths.
6. Verify attribution as a chain: search or browse request, queryID, hit identity and position, event payload, debugger/arrival, and downstream usability.
7. For experiments, confirm the hypothesis, isolated change, traffic/data sufficiency, event coverage, confidence state, and rollback decision instead of treating a dashboard metric as self-explanatory.
8. Report findings by severity with concrete reproduction steps, expected behavior, evidence source, and owner.
9. Write the report so a non-specialist customer can decide what to fix now versus later.
10. Include residual risk when production data, analytics windows, credentials, or live tools cannot be inspected.

## QA Areas

- Data and indexing: objectIDs, record counts, freshness, replicas, secured/hidden records, partial updates.
- Relevance: top queries, zero-result queries, filters, facets, synonyms, rules, sort orders, typo tolerance.
- UI: routing, pagination, empty states, loading/errors, mobile filters, accessibility, analytics attribution.
- Events: userToken consistency, queryID propagation, positions, conversion taxonomy, duplicate-event risk.
- Security and operations: API key exposure, secured API keys, environments, settings backup, rollback.
- AI surfaces: NeuralSearch event prerequisites, semantic/evaluation query regressions, Agent Studio tool authority, memory, guardrails, and feedback loops.

## Algolia Search Readiness Signposts

Use these signposts to decide whether the implementation is launch-ready, prototype-ready, or ready with accepted follow-ups:

- Data contract exists.
- Index settings match the UI.
- Records include all display, facet, ranking, merchandising, inventory, and event-attribution fields used by the experience.
- Autocomplete has source and selection contracts when autocomplete is included.
- Search results or browse pages handle query, hits, filters, sort, current refinements, recovery, pagination or infinite loading, empty states, loading, and errors when those surfaces are included.
- Events taxonomy exists.
- Click events are implemented, validated, or explicitly deferred by the user.
- Conversion events are planned, implemented, validated, or explicitly deferred by the user.
- Live index validation queries pass when live data is available.
- Browser QA passes for the relevant UI surfaces when a browser is available.

If any item is missing, report it as a launch blocker, accepted deferral, or residual risk depending on severity and the user's explicit decisions.

## Finish Gates

These are gates, not suggestions. Do not claim launch-ready, and do not let a completion summary claim them implicitly, unless each is satisfied or explicitly deferred by the user.

A gate is **executed**, never asserted. Reading your own edit and concluding "no console errors" is not a gate; loading the page in a browser and reading the console is. In testing, agents that had read this section still reported "no console errors ✓" and "events verified ✓" over pages with uncaught exceptions and an Insights loader that 404'd — no browser had been opened. If a browser tool is available, use it. If not, run `scripts/page-smoke.mjs` (Playwright; `node scripts/page-smoke.mjs --dir <folder> --query "<a real product word>" --click --mobile`) and paste its output into the report. If neither is possible, the gate is **untested** and the report must say so — it is never "passed."

- **Page-startup smoke test**: the page loads with zero uncaught errors and zero console errors, every `<script src>` returns 200, at least one request reaches the Algolia search API, and hit cards render **with readable text** (a card whose only content is an `<img>` is a broken template, not a hit). A single uncaught error in an inline script (a missing analytics loader is the classic case) can blank the entire experience while every settings check still passes.
- **CDN URLs verified, not guessed**: every third-party script and stylesheet URL was fetched (`curl -sI`, 200) before it shipped. See `references/verified-cdn-urls.md` — agents have shipped invented search-insights filenames and lost every event silently.
- **Insights client actually loaded**: `window.aa` is the real client, not the loader shim with calls sitting in `aa.queue`. `typeof window.aa === 'function'` proves nothing and neither does the queue length; a callback from `aa('getVersion', cb)` does.
- **Typed query reaches the results**: type a real product word into the search input and press Enter; a search request carrying that query must fire and the results must change. Mandatory when Autocomplete owns the input — selecting a suggestion working does not prove free-text submit works, and a storefront where Enter does nothing is a dead search box for every shopper who types.
- **Mobile-width render check**: at a ~375px viewport, no horizontal overflow, the search input reachable and usable, filters accessible. A desktop-only pass misses layout defects shoppers hit first.
- **Captured event evidence**: any claim that events work is backed by at least one captured outbound Insights payload (network tab, beacon intercept, or the smoke script's `--click`) inspected for `index`, `queryID`, `objectID`, and position — never by reading the source. Count the payloads: duplicates are a finding.
- **Claims audit**: every specific claim in the QA write-up ("X is fixed", "Y verified") was re-checked against live state — settings, live queries, rendered page — before finishing. A polished report with unverified claims is worse than a short honest one. Quote the evidence (console output, request body, smoke-script line) next to each claim.

## Anti-Patterns

- Reporting a checklist as passed without evidence, screenshots, payloads, settings exports, query results, or code references.
- Asserting a Finish Gate from source reading ("the loader is included, so events work"; "I removed the crash, so the page renders") instead of executing it in a browser or with `scripts/page-smoke.mjs`.
- Shipping a CDN `<script src>` whose URL was never fetched.
- Treating a working suggestion click as proof that the search box works when Autocomplete is the only entry point.
- Burying launch blockers under a positive summary.
- Treating event payload presence as success without checking identity, attribution, duplicate risk, and downstream visibility.
- Ignoring rollback, environment separation, API-key scope, or secured data because the UI appears to work.
- Calling an A/B test a win before its data and confidence state support interpretation, or when multiple unrelated changes prevent causal attribution.
- Marking an event as valid only because it reached the debugger without checking queryID, userToken, objectID, position, duplicate ownership, and downstream feature usability.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for launch and QA learning objectives and public Algolia docs for data, relevance, UI, events, analytics, security, and AI-readiness details. Convert source guidance into maturity-aware checks and validation artifacts for the customer team.

## Maturity Behavior

- Beginner implementation: focus on whether the basic data, settings, UI, and event paths work at all.
- Production readiness: lead with launch blockers, evidence matrix, security, rollback, attribution chain, mobile UX, and indexing reliability.
- Optimization: test representative queries, analytics quality, A/B readiness and confidence, merchandising behavior, and regression risk.
- AI readiness: verify NeuralSearch event prerequisites and evaluation queries plus Agent Studio data, permissions, tool authority, guardrails, feedback loops, and readiness gates.

## Output Contract

Lead with findings, not a generic summary. Include:

- Severity and affected surface.
- Evidence or reproduction.
- Recommended fix.
- Owner or role needed to fix it.
- Tests run and tests not run.
- Evidence matrix and residual risk.

If no issues are found, say so clearly and identify the remaining risks.
