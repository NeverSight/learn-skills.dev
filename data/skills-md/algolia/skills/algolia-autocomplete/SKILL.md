---
name: algolia-autocomplete
description: >
  Build and review Algolia Autocomplete and query suggestion experiences. Use when planning or implementing typeahead, query suggestions, recent searches, popular searches, federated autocomplete panels, product/content suggestions, detached mobile mode, plugins, keyboard navigation, insights events, or Autocomplete integration with InstantSearch. For net-new search or ecommerce builds, start with algolia-discovery-planning, which loads algolia-search-implementation so source strategy, data contract, and event taxonomy decisions are visible before autocomplete is marked ready. Do NOT use for full search results pages, browse pages, filters, pagination, or current refinements; use algolia-instantsearch-ui instead. Do NOT use for choosing between Algolia UI libraries; use algolia-ui-libraries. Do NOT use as the source of truth for current Autocomplete package APIs; use the official instantsearch skill and current docs alongside this customer-readiness skill.
license: MIT
metadata:
  author: algolia
  version: "0.7"
---

# Algolia Autocomplete

Use this skill for search-as-you-type experiences where the user has not committed to a full search results page yet. Autocomplete should help users form intent, not just mirror final results.

## Customer-Facing Standard

- Define source strategy and selection behavior before code.
- Validate keyboard, touch, mobile, empty/loading states, routing handoff, and events before launch.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Produce source ordering, selection contract, implementation notes, and QA checklist.
- Assess the finished experience as helpful, clear, focused, device-usable, and accessible; a technically connected panel is not necessarily ready for users.

## Official Companion Skills

- Use official `instantsearch` for current Autocomplete implementation details, framework-specific source-of-truth checks, and code-level patterns.
- Use official `algolia-mcp` when live index schema, query suggestions, facet values, or analytics should shape source selection.
- Use this skill before the official implementation skill to frame the customer journey, and after it to validate source strategy, selection behavior, mobile behavior, and event handoff.

## Source-Of-Truth Rules

- Use the official `instantsearch` skill or current docs for Autocomplete package APIs, plugins, render hooks, and InstantSearch integration details.
- Do not assume a Query Suggestions index exists; verify it or design a fallback source strategy.
- Do not wire selection behavior until the destination is known: submit query, navigate, refine InstantSearch, apply filter, open record, or run an approved action.
- For net-new implementations, confirm the data contract and event taxonomy, or create minimal provisional versions and name the follow-up decisions.
- Treat mouse, touch, Enter, and keyboard navigation as equivalent routes: each selection must reach the same URL or state with the same query and applicable scope.
- When Autocomplete is the only search input on a results page, the free-text submit path is a hard requirement: typing a query and pressing Enter must refine the results index (via `onSubmit`/`setQuery` or the InstantSearch `autocomplete` widget's search handoff), and it must be verified live by watching the search request after Enter. Suggestion and item selection working proves nothing about typed queries: a polished suggestions panel can sit on top of a search box where Enter does nothing for every shopper who types.

## Workflow

1. Read `references/autocomplete-guide.md` before implementation or review.
2. Confirm whether Autocomplete is standalone, integrated with InstantSearch, or part of a federated search entry point.
3. Confirm the data contract for every direct-result source: index, display fields, URLs, objectIDs, and event attribution fields.
4. Confirm the event taxonomy for every selection type, especially the difference between direct-result clicks and query suggestion submissions.
5. Choose sources intentionally: query suggestions, products, categories, content, recent searches, popular searches, or redirects.
6. Teach the difference between source types: Query Suggestions help users search better; product/content results help users jump directly to a record; recent searches help returning users resume.
7. Write a source contract for each group: trigger, source/index, input value, selection destination, scope carried forward, and attribution method.
8. Select advanced patterns only when they solve a named user need: resumption, discovery, early narrowing, non-product intent, or no-result recovery.
9. Validate suggestion quality before connecting it to the UI.
10. Implement in layers: mount the base input, validate Query Suggestions, add direct results, add focus/empty-query behavior, then validate mobile and events.
11. Use the official `instantsearch` skill and current docs to implement the selected package, plugin, renderer, or InstantSearch integration.
12. Implement keyboard, mouse, touch, empty, loading, and detached mobile behavior.
13. Preserve event attribution from suggestion selection to the resulting search or conversion.

## Questions To Ask

- What should appear while typing: queries, products, categories, content, recent searches, or all of these?
- Should selecting a suggestion navigate, refine InstantSearch state, open a result, or submit a query?
- Is there a query suggestions index, and how is it generated?
- Are the suggestions clear, useful, searchable, and free of internal/test language?
- What should appear before typing: recent searches, popular searches, useful categories, shortcuts, or nothing?
- Are recent searches stored locally, server-side, or disabled?
- What mobile behavior is expected?
- Which selections need click or conversion events?
- If a category is shown with a suggestion, does it narrow the subsequent search, route to a category page, or only provide context?
- What should a user see and be able to do when a source is empty, slow, or unavailable?
- Which user problem justifies each advanced pattern: resuming, discovering, narrowing, reaching non-product content, or recovering from a likely dead end?
- With the mobile keyboard open, which few suggestions or direct results must remain visible, and where does “see all results” lead?

## Implementation Standards

- Use Algolia Autocomplete primitives and plugins instead of hand-rolled typeahead state unless the project has a strong reason.
- Keep source limits tight and ordered by user value.
- Keep Query Suggestions and product/content results visually and behaviorally distinct.
- Review the Query Suggestions index before launch. Tune noisy, incomplete, offensive, stale, or internal suggestions before exposing them.
- Use recent searches and `openOnFocus` style behavior only when the empty-query state helps users resume or discover, not as a promotional dumping ground.
- Debounce or stall UI responsibly; do not make the input feel laggy.
- Respect accessibility defaults and avoid custom markup that breaks keyboard navigation.
- Keep InstantSearch integration explicit: update query/refinements without creating conflicting state loops.
- Use consistent userToken and event metadata when suggestions lead to result interactions.
- Use a URL or selection-state contract that works for pointer and keyboard selection; test it with a category-bearing suggestion where relevant.
- Keep a source empty-state deliberate: hide a failed/empty group, show an approved fallback, or show a clear no-suggestions state. Do not leave blank labeled panels.
- Start with a small source set and add groups only when they pass the helpful, clear, and focused test; do not let a new source displace the best guidance.
- On mobile, preserve a top search input, distinct clear and close actions, tap-friendly rows, visible primary guidance above the keyboard, and a clear path to all results.
- Keep category scope sparse and visually distinct. Use it to narrow a genuinely ambiguous query, not as a duplicate list of category labels.

## Anti-Patterns

- Showing too many source groups or too many hits per group.
- Treating autocomplete as a mini search results page instead of a search guidance experience.
- Connecting Query Suggestions before reviewing whether suggestions are useful, safe, and likely to return results.
- Using the source index name where the Query Suggestions plugin expects the Query Suggestions index name.
- Making every suggestion behave differently without clear visual or routing cues.
- Creating two competing query states between Autocomplete and InstantSearch.
- Making Autocomplete the sole entry point without a working typed-query submit path — or verifying "search works" by clicking a suggestion instead of typing and pressing Enter.
- Breaking keyboard, focus, Escape, Enter, or detached mobile behavior with custom markup.
- Sending direct-result events as search-attributed events when the item did not come from an Algolia search response with queryID.
- Displaying a category label without defining whether it scopes the result, navigates, or is informational only.
- Letting the pointer path and keyboard path produce different query parameters, filters, or destinations.
- Adding popular searches, categories, federated content, or product groups because the panel has space rather than because they solve a named user need.
- Letting product cards crowd out the query guidance, especially when the mobile keyboard is open.
- Combining the clear-input action and the close-overlay action on mobile.

## Completion Checkpoints

Before calling autocomplete ready, or when handing off a prototype with follow-ups, state whether these checkpoints are satisfied, deferred, or unknown:

- Source and ordering contract.
- Selection behavior for every source.
- Referenced data contract or explicit minimal demo data contract for direct-result sources.
- Referenced event taxonomy or explicit user-approved event deferral.
- Clear distinction between query suggestion submissions and direct-result clicks.
- Browser QA for keyboard, pointer, touch, detached mobile mode, empty/loading states, selection behavior, and routing/search-state handoff.
- Source contract and fallback behavior for unavailable, empty, or low-quality suggestions.
- Quality standard verdict: helpful, clear, focused, device-usable, and accessible, with any failed dimension recorded as a follow-up.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for autocomplete and search UX learning objectives and public Algolia docs for autocomplete, query suggestions, UI state, mobile behavior, and event attribution. Use source guidance to shape questions, maturity level, use-case bundle, and validation artifacts; do not turn it into a static docs dump.

## Maturity Behavior

- Beginner implementation: define sources, ordering, and selection behavior before adding advanced plugins.
- Production readiness: build and verify the base input, Query Suggestions, direct results, empty-query behavior, then keyboard, touch, mobile detached mode, routing handoff, accessibility, and event attribution.
- Optimization: review suggestion quality, no-result behavior, source ordering, recent/popular searches, category scope, federated content, latency, and query suggestion analytics.
- AI readiness: preserve selected query/result context, userToken, and downstream event attribution for personalization, NeuralSearch evaluation, or AI assistants.

## Output Contract

Return code or review notes plus:

- Official Skill Usage Note: framework/package choice and official source consulted for implementation details.
- Source Contract: order, trigger, source/index, input value, selection destination, carried scope, fallback, and event treatment for each group.
- Customer UI Plan: empty/focus behavior, mobile mode, result-page handoff, device-specific content budget, and accessibility notes.
- Quality Standard: helpful, clear, focused, device-usable, and accessible verdicts with open issues.
- QA checklist for keyboard navigation, selection behavior, mobile detached mode, routing/search-state sync, no suggestions, latency, and events.
