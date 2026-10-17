---
name: algolia-ui-libraries
description: >
  Living selector and reference workflow for current Algolia UI libraries. Use when choosing, installing, upgrading, implementing, or auditing InstantSearch.js, React InstantSearch, Vue InstantSearch, InstantSearch Android, InstantSearch iOS, Algolia for Flutter, Autocomplete, legacy Angular InstantSearch audits or migrations, DocSearch-style autocomplete, routing, SSR, events, mobile SDKs, framework integrations, UI examples, styling, performance, secured API keys, or frontend search library architecture. Do NOT use as a frozen API reference or package-version source; verify current docs. Do NOT use for full implementation once the library is selected; use algolia-instantsearch-ui, algolia-autocomplete, or the official instantsearch skill.
license: MIT
metadata:
  author: algolia
  version: "0.3"
---

# Algolia UI Libraries

Use this skill to choose the right current Algolia UI library and docs path. Do not treat this skill as a frozen API reference or package-version source.

## Customer-Facing Standard

- Verify current public docs before recommending package names, imports, SSR patterns, routing, or upgrade steps.
- Choose the library from the customer journey and framework, not from generic preference.
- Use public `academy.algolia.com` for learning alignment and public `algolia.com/doc` for current implementation guidance when source-backed context is needed.
- When an Academy metadata reference pack is available, use only its `title`, `url`, `course`, `module`, `learning_objectives`, and `updated_at` fields for structure. If it is stale or no match exists, fall back to live Academy/docs lookup. Do not treat cached metadata as course content or implementation authority.
- Do not require custom Academy/docs access; use customer-provided sources only as optional context.
- When live Algolia data, analytics, index inspection, settings changes, or account actions are needed, use Algolia MCP, the Algolia CLI, or official Algolia skills for the live operation, then apply this skill to interpret results and validate the customer-ready implementation path.
- Route to InstantSearch, Autocomplete, Events, or Release QA when implementation depth is needed.

## Official Companion Skills

- Use official `instantsearch` for production implementation, source-of-truth checks, framework-specific rules, and code-level InstantSearch or Autocomplete work.
- Use this skill before the official implementation step to choose the right current UI path and after implementation to validate routing, SSR, events, and upgrade assumptions.

## Source-Of-Truth Rules

- Check `https://www.algolia.com/doc/llms.txt`, current public docs, installed package metadata, or official skills before giving install commands, imports, APIs, or upgrade instructions.
- Do not freeze package versions in the skill output unless the project already pins them or current docs/package metadata were checked.
- If docs cannot be checked, provide the decision path and mark exact commands as needing verification.

## Workflow

1. Read `references/ui-library-selector.md` before choosing or changing a library.
2. Identify the app platform and framework: vanilla JS, React, Next.js, Vue, Angular, Android, iOS, Flutter, React Native, Laravel/Vue, or documentation search.
3. Choose the UI library by experience shape:
   - Full search or browse results: InstantSearch family.
   - Typeahead, query suggestions, recent searches, or federated suggestions: Autocomplete.
   - Documentation/site search: DocSearch-style Autocomplete only if that matches the product.
   - Native/mobile search: InstantSearch Android, iOS, or Flutter Helper.
4. Verify the current official docs before install, imports, SSR, routing, event, or upgrade changes.
5. Route to the implementation skill:
   - `$algolia-instantsearch-ui` for full results/search/browse UI.
   - `$algolia-autocomplete` for typeahead and suggestion experiences.
   - `$algolia-events-insights` for click/conversion attribution.
   - `$algolia-release-qa` before launch.

## Questions To Ask

- What framework and version does the app use?
- Is the experience a full results page, browse/category page, autocomplete, federated search, mobile UI, or docs search?
- Does the project need SSR, URL routing, backend search, secured API keys, or mobile/native behavior?
- Which index, replicas, facets, filters, and sort options must the UI expose?
- Which events and analytics features are required?
- Is this a fresh implementation, migration, or package upgrade?

## Standards

- Do not copy large Algolia docs into the skill. Link to current docs and summarize decision logic.
- Do not hard-code package versions from memory. Inspect the project and verify current docs/package metadata before changing dependencies.
- Prefer the framework-specific official guide over generic snippets.
- Preserve event attribution: queryID, objectID, index, position, and userToken where needed.
- Include routing, empty/loading/error states, mobile behavior, accessibility, and performance in QA.

## Anti-Patterns

- Choosing a library because it is familiar instead of matching the framework and user journey.
- Mixing Autocomplete and InstantSearch responsibilities without a clear handoff contract.
- Treating mobile/native apps as web InstantSearch ports when native libraries are available.
- Recommending SSR, routing, or secured-key patterns from memory.

## Academy And Customer Education Alignment

When source-backed guidance is needed, search public Academy sources for UI library learning objectives and public Algolia docs for current docs paths, package guidance, framework patterns, and implementation prerequisites. Do not freeze package versions or copy large docs into the answer. Map the request to maturity level and use case before recommending a library or upgrade path.

## Output Contract

Return the selected library, why it fits, official docs to use, install/upgrade assumptions, implementation plan, event/routing/security notes, and QA checklist. Call out any docs that must be verified live before the agent touches code.
