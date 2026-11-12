---
name: algolia-instantsearch-ui
description: >
  Build and review Algolia InstantSearch experiences in JavaScript, React, Vue, Angular (via InstantSearch.js; Angular InstantSearch is deprecated), or compatible frontend stacks. Use when planning or reviewing search results pages, browse/category pages, routing, widgets, filters, facets, sort-by, pagination, infinite hits, current refinements, insights middleware, SSR, or UI-state synchronization. For net-new search UI builds, start with algolia-discovery-planning, which loads algolia-search-implementation so data contract and event taxonomy decisions are visible before UI is marked ready. Do NOT use for autocomplete/typeahead experiences before the user commits to a results page; use algolia-autocomplete instead. Do NOT use for choosing between Algolia UI libraries; use algolia-ui-libraries. Do NOT use as the source of truth for current framework APIs or code-level implementation details; use the official instantsearch skill and current docs alongside this customer-readiness skill.
license: MIT
metadata:
  author: algolia
  version: "0.4"
---

# Algolia InstantSearch UI

Use this skill for full search or browse interfaces powered by InstantSearch. Keep the implementation faithful to the index contract and user journey.

## Customer-Facing Standard

- Treat a working search box as incomplete until filters, empty states, routing needs, mobile behavior, and events are considered.
- Preserve the customer's existing design system and accessibility patterns.
- Treat Algolia's official `instantsearch` skill from `algolia/skills` as the implementation authority for React InstantSearch, Vue InstantSearch, InstantSearch.js, source-of-truth checks, prop shapes, widgets, hooks, connectors, SSR, middleware, custom widgets, and framework anti-patterns.
- Use this skill as the customer-readiness layer around the official skill: clarify the search journey, data contract, refinements, URL behavior, event attribution, mobile interaction, accessibility, and QA.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Produce implementation notes or code plus a browser-verifiable QA checklist.

## Official Companion Skills

- Use official `instantsearch` from `https://github.com/algolia/skills` for production implementation details, source-of-truth checks, widget/hook/connector behavior, framework-specific anti-patterns, and code-level InstantSearch or Autocomplete work.
- Use official `algolia-mcp` when live index schema, sample hits, facet values, or analytics should shape the UI.
- Use this skill before the official `instantsearch` skill to frame the customer journey and after the official skill to validate UX, routing, event behavior, mobile behavior, and launch readiness.
- Use `algolia-events-insights` alongside this skill when click/conversion attribution, Insights middleware, `queryID`, `objectID`, position, or `userToken` behavior affects the UI.

## Source-Of-Truth Rules

- Use the official `instantsearch` skill for framework-specific widgets, hooks, connectors, SSR, middleware, routing, and source-of-truth checks.
- Follow the official skill's discovery pattern: identify the library (`react-instantsearch`, `vue-instantsearch`, or `instantsearch.js`), inspect existing setup, inspect installed types and docs before writing unfamiliar APIs, and read the matching official reference directory before implementation.
- Inspect the project dependencies and installed types before assuming package names or prop shapes.
- Verify current docs before writing SSR, routing, middleware, or event code that is not already present in the project.
- For net-new implementations, avoid treating UI as isolated from data and events. Confirm that a data contract and event taxonomy exist, or create minimal versions and mark them provisional.

## Workflow

1. Read `references/instantsearch-guide.md` before implementing or reviewing UI code.
2. Confirm the framework and InstantSearch package already used by the project. If code will be written, invoke the official `instantsearch` skill or follow its source-of-truth checks before choosing APIs.
3. Confirm the data contract: index names, replicas, display attributes, facets, ranking fields, secured filters, and event attribution fields.
4. Confirm the event taxonomy: result clicks, conversion path, `userToken`, `queryID`, `objectID`, index, and position handling.
5. Define the result-page job: search results page, category/browse page, federated page, internal lookup, marketplace listing, or support/documentation search.
6. Preserve existing design-system conventions and accessibility patterns.
7. Teach the customer that Autocomplete helps users choose what to search for, while InstantSearch helps users explore, refine, recover, and act on results after the search.
8. Wire routing, filters, sort, active refinement feedback, clear refinements, pagination/infinite hits, loading states, empty states, and events deliberately. A working search box alone is not a complete search experience.
9. Verify the UI in a browser when possible, including empty states, slow/error states, mobile filter behavior, keyboard use, URL restoration, and event readiness.

## Questions To Ask

- Is this a search page, category browse page, federated experience, or internal tool?
- Which index and replicas power each view?
- Which refinements are user-visible versus applied silently?
- Which filters are actually useful to the user for this record type, and are those attributes facetable in the index?
- How will users see and clear active refinements?
- Should URL routing preserve query and filters?
- Should the first page load with an empty query, category filter, route-derived query, or user-entered query?
- Is pagination, infinite loading, or "load more" the best continuation pattern for the context?
- Is click/conversion attribution required for analytics or personalization?
- What is the expected mobile filter/sort interaction?
- Does this route need SSR, server components, static generation, or client-only rendering constraints?

## Implementation Standards

- Use InstantSearch widgets/hooks/connectors appropriate to the local framework.
- When code is required, use the official `instantsearch` skill for the exact framework API and then apply this skill's readiness checks to the result.
- Keep `searchClient`, index name, routing, and environment configuration out of hard-coded UI leaf components when the project has config patterns.
- Use `configure` for query parameters and default filters that belong to the search state.
- Include enough visible structure for users to understand, refine, recover, and continue: results, filters, active refinements, clear refinements, sort when needed, pagination or infinite loading, and empty/no-results recovery.
- Make silent filters legible in the product design or documented in the implementation handoff. Users should not be confused by invisible constraints.
- Match continuation pattern to intent: pagination for comparison and return-to-position, infinite hits for discovery, and load-more when users need both control and flow.
- Treat mobile filters as a first-class interaction, not a compressed desktop sidebar.
- Render accessible hit cards with stable objectID-aware interactions.
- Enable Insights middleware or event helpers when events are in scope.
- Do not mutate Algolia hits in ways that break objectID, queryID, position, or event attribution.
- For SSR/routing work, verify hydration, URL state restoration, and back/forward behavior using the official skill's SSR and routing guidance.

## Anti-Patterns

- Treating a search input plus hits as a complete experience while ignoring filters, empty states, routing, mobile behavior, and events.
- Re-implementing official InstantSearch API guidance from memory instead of using the official `instantsearch` skill and installed types.
- Adding filters without active refinement feedback or a clear-all path.
- Choosing facets because they exist in the data instead of because users need them to narrow results.
- Showing facets with confusing labels, empty values, unstable ordering, or no count/range context.
- Hard-coding index names, app IDs, or environment-specific values inside reusable UI leaf components.
- Client-side sorting or filtering Algolia hits in ways that desynchronize facets, positions, pagination, or analytics.
- Styling InstantSearch markup without checking generated class names or accessibility behavior.
- Shipping a UI that cannot be verified in a browser with realistic records.
- Shipping desktop-only filter behavior and assuming mobile users can recover.
- Enabling URL routing without validating reload, sharing, and back/forward behavior.

## Completion Checkpoints

Before calling the UI ready, or when handing off a prototype with follow-ups, state whether these checkpoints are satisfied, deferred, or unknown:

- Referenced data contract or explicit minimal demo data contract.
- Referenced event taxonomy or explicit user-approved event deferral.
- Official `instantsearch` skill or current docs/types used for framework-specific API choices.
- Hit components preserve `objectID`, `index`, `queryID`, position, and `userToken` for event wiring.
- Facets and filters exist in the index contract.
- Browser QA covers query, filters, active refinements, clear refinements, sort, pagination or infinite loading, empty states, loading/error states, routing when enabled, mobile behavior, keyboard behavior, and event readiness.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for UI learning objectives and public Algolia docs for InstantSearch, routing, widgets, filters, facets, UI state, SSR, and event attribution. Use source guidance to choose maturity level, use-case bundle, guided prompts, and QA artifacts. Keep the skill procedural and source-aligned rather than embedding stale API documentation.

## Maturity Behavior

- Beginner implementation: build the smallest complete search or browse experience with query, hits, filters, loading, empty state, and clear index configuration.
- Production readiness: validate routing, mobile filters, accessibility, API-key boundaries, event attribution, error states, and environment configuration.
- Optimization: review query analytics, facet usage, performance, UI friction, A/B testing, and relevance handoff to index configuration.
- AI readiness: confirm the UI preserves user context, objectID, index, queryID, position, and conversion paths needed by AI and personalization features.

## Output Contract

Return implemented code or a review with file references, plus an Official Skill Usage Note, Customer UI Plan, Data/Event Readiness Notes, and concise QA checklist covering query, filters, active refinements, sort, pagination/infinite loading, empty states, routing, mobile behavior, accessibility, and events.
