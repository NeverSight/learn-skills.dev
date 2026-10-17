---
name: algolia-search-implementation
description: >
  Execution checklist for net-new Algolia search, browse, autocomplete, ecommerce search, recommendations, personalization, Dynamic Re-Ranking, or search UI builds. Use during a greenfield build to keep data contract, event taxonomy, index configuration, UI, and release QA visible as explicit checkpoints with completion signposts and suggested artifacts, so agents proceed deliberately and document tradeoffs and deferrals. Do NOT use as the entry point for Algolia work; start with algolia-discovery-planning, which maps the request to the lifecycle and loads this skill for net-new builds.
license: MIT
metadata:
  author: algolia
  version: "0.2"
---

# Algolia Search Implementation

Use this skill as the execution checklist for net-new Algolia search builds, loaded from `algolia-discovery-planning` once the phase plan marks a greenfield implementation in scope. Its job is to make data, events, index configuration, UI, and release QA visible decision points, especially when an agent needs to move quickly or proceed with provisional assumptions.

Use the whole Algolia lens: data and events are not side quests. The data contract determines what search can retrieve, rank, filter, display, merchandise, secure, and attribute. The event foundation determines whether analytics, personalization, Recommend, Dynamic Re-Ranking, NeuralSearch evaluation, and Agent Studio feedback loops can be trusted. Let UI and AI feature decisions inherit from those foundations instead of discovering them late.

## Recommended Workflow

For any net-new Algolia search, browse, autocomplete, ecommerce, recommendations, personalization, or Dynamic Re-Ranking implementation, work through these checkpoints in order when practical:

1. Data contract checkpoint: use `algolia-data-modeling`.
2. Event instrumentation checkpoint: use `algolia-events-insights`.
3. Index configuration checkpoint: use `algolia-index-configuration`.
4. UI implementation checkpoint:
   - Choosing the UI library, framework fit, SSR/routing strategy, or mobile SDKs: use `algolia-ui-libraries`.
   - Autocomplete or typeahead: use `algolia-autocomplete`.
   - Search results page, browse page, filters, facets, routing, sort, pagination, or current refinements: use `algolia-instantsearch-ui`.
   - Current framework APIs and production code details: use the official `instantsearch` skill alongside `algolia-instantsearch-ui` or `algolia-autocomplete`.
5. Release QA checkpoint: use `algolia-release-qa`.

Before UI work, pause long enough to identify the data contract and event taxonomy. If the user asks for a quick prototype or the information is unavailable, proceed with a minimal provisional contract, name the assumptions, and record what must be revisited before launch.

## Foundation Lens

When using the full skills library, orient the work in this order:

1. Data shape: records, variants, objectIDs, searchable/display fields, facets, ranking signals, inventory, permissions, and update ownership.
2. Event shape: userToken strategy, click and conversion taxonomy, queryID/objectID/position preservation, ownership, deduplication, and validation.
3. Relevance and UI: settings, widgets, routing, filters, autocomplete sources, and result interactions that match the data and event contracts.
4. AI readiness: NeuralSearch, Dynamic Re-Ranking, Recommend, personalization, and Agent Studio behavior evaluated against data quality and behavioral signals.
5. QA: evidence that data, events, settings, UI, security, and rollback are understood.

## Completion Signposts

Use these signposts when deciding whether to call the implementation ready, prototype-ready, or ready with documented follow-ups:

- Data contract exists.
- Index settings match the UI.
- Records include all display, facet, ranking, merchandising, inventory, and event-attribution fields used by the experience.
- Autocomplete has source, ordering, selection, routing, and event-handoff contracts when autocomplete is included.
- Search results or browse pages handle query, hits, filters, sort, current refinements, pagination or infinite loading, empty states, recovery, loading, and error states when those surfaces are included.
- Events taxonomy exists.
- Click events are implemented, validated, or explicitly deferred by the user.
- Conversion events are planned, implemented, validated, or explicitly deferred by the user.
- Live index validation queries pass when live data is available.
- Browser QA passes for the relevant UI surfaces when a browser is available.

## Suggested Artifacts

For production-oriented work, create or update:

- `algolia/index-contract.md` or an equivalent index contract artifact.
- `algolia/search-event-taxonomy.md` or an equivalent event taxonomy artifact.
- A release QA note or report covering data, settings, UI, events, security, and rollback where relevant.

For small demos or prototypes, produce the minimal contract:

- One paragraph data contract.
- One table of events.
- Three validation queries.
- Explicit deferred production concerns.

## Decision Behavior

- If sample records, UI fields, objectID strategy, event attribution fields, or userToken strategy are missing, state assumptions and create a provisional artifact instead of silently skipping the decision.
- If the user asks to defer events or conversions, record the deferral explicitly with owner, risk, and follow-up validation.
- If live Algolia inspection or writes are needed, route through Algolia MCP, Algolia CLI, or official Algolia skills first, then return to this guided workflow.
- If a task is only an audit of an existing implementation, start with `algolia-release-qa`, then route findings back to data, events, index configuration, autocomplete, or InstantSearch skills as needed.

## Output Contract

Return a checkpoint-by-checkpoint implementation summary:

- Data contract status.
- Event taxonomy status.
- Index configuration status.
- UI implementation status.
- Release QA status.
- Explicit deferrals and risks.
- Next validation step.
