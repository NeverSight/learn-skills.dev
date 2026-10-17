---
name: algolia-events-insights
description: >
  Algolia event instrumentation guidance for Insights, analytics, personalization, Dynamic Re-Ranking, Recommend, and merchandising feedback loops. Use for search, autocomplete, browse, ecommerce, personalization, recommendations, or analytics instrumentation. Makes event decisions explicit before an Algolia UI is considered ready. Use when implementing or auditing clickedObjectIDsAfterSearch, convertedObjectIDsAfterSearch, viewedObjectIDs, addedToCartObjectIDsAfterSearch, purchasedObjectIDsAfterSearch, userToken, queryID, eventName, eventSubtype, or frontend/backend event pipelines. Do NOT use for live analytics retrieval, top-query inspection, or account-aware diagnostics; use algolia-mcp. Do NOT use for framework-specific InstantSearch or Autocomplete APIs; use the official instantsearch skill alongside this planning and validation skill.
license: MIT
metadata:
  author: algolia
  version: "0.6"
---

# Algolia Events Insights

Use this skill whenever user behavior needs to power analytics, personalization, Recommend, dynamic re-ranking, or measurable search quality.

## Customer-Facing Standard

- Start with one validated result-click event and one validated primary conversion before expanding.
- State which owner controls each event: frontend, backend, analytics/tag manager, or data pipeline.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Produce an event taxonomy, payload checklist, duplicate-event rule, and validation plan.
- Distinguish between events that are merely ingestible and events that are usable by analytics, Dynamic Re-Ranking, NeuralSearch, Recommend, personalization, or revenue reporting.
- Choose the implementation path deliberately: InstantSearch/search-insights first when possible, GTM for constrained marketing-managed frontends, Segment/CDP for centralized pipelines, and backend ownership for final server-side conversions.

## Official Companion Skills

- Use official `algolia-mcp` for live analytics signals such as top searches, no-result rates, click positions, no-click searches, and outcome metrics.
- Use official `instantsearch` when event wiring belongs in InstantSearch or Autocomplete implementation code.
- Use this skill after the official tool call to produce the event taxonomy, ownership model, payload checks, and feature-readiness notes.

## Search UI Event Decision Point

If the task includes a search results page, autocomplete, browse page, recommendations, personalization, Dynamic Re-Ranking, or ecommerce search:

- Produce an event taxonomy before or during implementation when practical.
- Plan events for every result interaction that the UI supports.
- If event instrumentation is not implemented now, document the user-approved deferral, owner, risk, and validation follow-up in the completion summary.

Required output:

- `userToken` strategy.
- Event names.
- Event types.
- Source UI surface.
- Required Algolia fields: `index`, `objectID`, `queryID`, and `position` where the event type requires them.
- Implementation location.
- Validation method.

For demos and prototypes, still produce a lightweight event table with planned events, deferred production concerns, and validation steps.

## Source-Of-Truth Rules

- Verify the current event method and required fields in public docs or the official implementation skill before writing code.
- Do not use an `AfterSearch` method unless the interaction is explicitly attributable to an Algolia search or browse response and has a valid `queryID`.
- If a conversion cannot include `queryID`, decide whether Algolia can infer attribution from a prior click. If not, use the non-AfterSearch method and state the analytics or feature limitation.
- A 200 response, network success, or Debugger visibility proves ingestion only. Do not call the event setup ready until the payload is complete, consistent, attributed, and eligible for the intended downstream feature.
- Treat generic views and filter interactions as weak signals unless the selected feature or personalization strategy explicitly needs them. Do not let weak P2 events distract from search-attributed clicks and conversions.

## Workflow

1. Read `references/events-guide.md` before adding or changing event code.
2. Read `references/example-output.md` when producing an event taxonomy or customer-facing event setup plan.
3. Read `references/search-event-taxonomy.md` when producing a search, browse, autocomplete, recommendations, or ecommerce event taxonomy.
4. Separate the business path from the technical path. Business users define what to track, why it matters, KPIs, surfaces, and success criteria. Technical users implement schema, queryID propagation, identity consistency, validation, and monitoring.
5. Start with the simple event plan: search result click, result view when needed, primary conversion, and add-to-cart or purchase when relevant.
6. Prioritize with P0/P1/P2. P0 is search-attributed clicks plus the primary conversion. P1 adds important outcomes such as add-to-cart, purchase, lead, save, support resolution, or recommendation interactions. P2 adds optional or context-specific signals such as generic views or filter interactions.
7. Identify which downstream features need events: analytics only, A/B testing, personalization, Recommend, dynamic re-ranking, merchandising, NeuralSearch evaluation, or Agent Studio feedback.
8. Confirm the user identity strategy before implementation. Anonymous and authenticated user tokens must be consistent enough to join behavior.
9. Preserve search attribution. Events after search must include `queryID`, `objectIDs`, `positions` when required, `index`, and the same user token used for the search.
10. Select the implementation path and document connector risks: InstantSearch/search-insights, custom frontend, GTM, Segment/CDP, backend, or hybrid.
11. Validate in a non-production environment before launch using arrival, usability, and attribution checks.
12. Add a regression check after releases that touch UI structure, routing, identity, checkout, backend workflows, or analytics connectors.

## Simple Implementation Recipe

Use this order unless the app has unusual constraints:

1. Turn on queryID retrieval for searches that produce clickable results.
2. Set one durable anonymous `userToken`, then decide how it maps after login.
3. Send click events from result cards using the hit's `objectID`, `index`, `queryID`, and displayed position.
4. Send the primary conversion event from the place the conversion actually happens.
5. Add cart, purchase, lead, save, or support-deflection events only when they map to a real business outcome.
6. Test the network payload, Events Health, Debugger, user timeline where available, and destination or feature eligibility before calling the setup complete.

Prefer a minimum viable event setup over a large taxonomy. For most customers, the first useful milestone is one validated result-click event and one validated primary conversion event with the same `userToken`, correct `objectID`, correct `index`, and `queryID` when search attribution applies.

## InstantSearch Auto-Events And The Loader

Two failure modes appear repeatedly in real implementations. Both pass demos and settings checks; both corrupt or kill the event pipeline.

- **The middleware already clicks.** When the InstantSearch insights middleware (`insights: true`) is enabled, it auto-sends a click event for clicks inside a hit. Sending a manual `clickedObjectIDsAfterSearch` on the same click double-counts every CTR datapoint. A manual conversion (`convertedObjectIDsAfterSearch` / `addedToCartObjectIDsAfterSearch`) does NOT suppress the automatic click either — an add-to-cart button inside a hit produces one auto click plus your conversion, which is correct; a manual click handler on top of that is not. Expected totals per add-to-cart interaction: exactly one click event and one conversion event. Use the hit template's `sendEvent` for custom click semantics rather than a parallel manual pipeline, and never hardcode the `index` field — read the live index name (sort replicas change it), and treat `data-index="undefined"` in a payload as a failed implementation even if the call returns 200.
- **The loader defines `window.aa`; a plain script tag does not.** Loading `search-insights` via a bare `<script src>` and then calling `aa('init', ...)` throws `ReferenceError: aa is not defined` — and because that aborts the entire surrounding inline script, the typical result is a completely blank search page, not a missing event. Always use Algolia's documented async queue snippet (or bind explicitly on script load), and smoke-test page startup: the page must render and queue events with the insights script throttled or blocked.

Validation for both: capture the actual outbound payloads to the Insights endpoint (network tab, `sendBeacon`/`fetch` intercept) and count and inspect them. Reading the source is not verification — both of these failure modes look correct in source.

## Questions To Ask

- Which conversions matter: view, click, add to cart, purchase, lead, signup, content save, support deflection?
- Which Algolia-powered surfaces need events: search page, category/browse page, autocomplete, product detail page reached from search, recommendations, content search, support search, or agent experiences?
- Which events are P0, P1, and P2 for this business goal?
- Are events sent from the browser, backend, or both?
- Which implementation path fits this stack: InstantSearch/search-insights, custom frontend, GTM, Segment/CDP, backend, or hybrid?
- How is `userToken` assigned before and after login?
- Can the UI access the `queryID` and hit position from the search response?
- Are purchases or other conversions available only server-side?
- Which indices and objectIDs should events reference when the same item appears in multiple indices or replicas?
- What should prevent duplicate events when frontend tags, backend conversions, GTM, or Segment all observe the same action?
- What validation surface will prove the event is not only received, but usable by the intended feature?

## Implementation Standards

- Use search-attributed event methods for actions caused by search results.
- Do not invent a new `userToken` per event or page load.
- Use stable, descriptive `eventName` values that business teams can read in reports.
- Include price, quantity, currency, and object data where the selected event type supports it and the business needs revenue analysis.
- Avoid double counting by deciding whether frontend, backend, or a deduped pipeline owns each event.
- Treat a 200 response or visible Debugger event as ingestion proof, not usefulness proof. A valid event can still be unusable for downstream features if it has stale queryID, mismatched objectID, inconsistent userToken, missing position, weak signal type, or duplicate ownership.
- Preserve the exact record identity from the search result. If the user clicked or converted on a variant, do not send a parent product ID unless the original search result used that same parent objectID.
- Explain deduplication risk in customer language: repeated events from the same user on the same record may not all count toward downstream models, and a hardcoded shared userToken can make many users look like one user.
- Positions are one-based. If positions are computed manually from an array index, add 1 and validate against the rendered result order.
- Validate the full journey, not isolated events: search or browse request, click, add-to-cart or primary conversion, purchase or final outcome.
- For Segment/CDP or GTM paths, validate both the source payload and the transformed Algolia payload because mappings may rename, flatten, drop, duplicate, or mis-shape fields.

## Anti-Patterns

- Stacking a manual `clickedObjectIDsAfterSearch` on top of the InstantSearch insights middleware's automatic click event — every click counts twice.
- Loading `search-insights` with a plain script tag and calling `aa()` without the documented async queue snippet — the resulting ReferenceError can blank the entire page.
- Hardcoding the `index` field in event payloads instead of reading the live index name (sort replicas change it), or shipping events whose payload was never actually captured and inspected.
- Building a large taxonomy before one click and one primary conversion are validated.
- Over-investing in P2 events such as broad view or filter interactions before P0 search-attributed clicks and conversions are healthy.
- Sending events from a tag manager that cannot access the actual `objectID`, `queryID`, position, index, or stable userToken.
- Mixing frontend and backend purchase events without a deduplication rule.
- Reusing stale queryIDs long after the search context is gone.
- Treating events as optional for analytics quality, personalization, Recommend, dynamic re-ranking, Agent Studio feedback, or rollout measurement.
- Calling filter clicks or broad view events AI-ready signals while P0 result clicks or conversions are missing.
- Validating only one system in a connector path, such as Segment Debugger but not Algolia Debugger, or browser Network but not Events Health.
- Sending SKUs, parent IDs, or external IDs when Algolia expects the exact `objectID` returned in the hit.

## Completion Checkpoints

Before calling an implementation ready, or when handing off a prototype with follow-ups, state whether these checkpoints are satisfied, deferred, or unknown:

- `userToken` strategy status.
- Hit click attribution status for `queryID`, `objectID`, `index`, and displayed position.
- Autocomplete direct-result click versus query suggestion selection status.
- Conversion event status: planned, implemented, validated, deferred, or unknown.
- Event ownership and duplicate-event rule status.
- Validation step status.
- Implementation path selected and connector-specific risks documented.
- Usability status: arrived, payload complete, attribution intact, feature destination or eligibility checked.
- Regression plan for future UI, route, identity, checkout, or connector changes.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for Insights, analytics, and AI-readiness learning objectives and public Algolia docs for queryID, userToken, event methods, personalization, Recommend, and dynamic re-ranking details. Use source guidance to build a customer-appropriate event taxonomy, maturity plan, and validation path.

## Maturity Behavior

- Beginner implementation: implement one result-click event and one primary conversion event with a durable `userToken`.
- Production readiness: validate payloads, ownership, duplicate prevention, backend conversions, and downstream visibility.
- Optimization: connect events to analytics, A/B testing, personalization, Recommend, merchandising, and dynamic re-ranking decisions.
- AI readiness: prove the event setup can support NeuralSearch evaluation, Agent Studio feedback, AI assistant quality measurement, and conversion attribution.

## Output Contract

Return a prioritized Event Plan, Connector Recommendation, Developer Handoff Sheet, code changes or owner handoff steps, and a validation plan. For audits, report missing attribution, identity inconsistencies, duplicate-event risks, weak-signal overinvestment, connector mapping risks, and downstream feature blockers first. Make the first recommendation small enough that a team can implement it in one sprint.
