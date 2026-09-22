---
name: requirements
description: "Turn a brief or existing feature into testable behavior, quality constraints, and explicit data and permission contracts. Use when stakeholder notes, a brief, or a vibe-coded concept needs FR/NFR requirements before design or implementation."
---

# Requirements

Write requirements about outcomes and observable behavior. Keep explicit user choices; do not replace their product with a preferred solution.

## Work

- Extract the user goal, initiating event, allowed actor, inputs, result, and failure behavior from the brief or running product.
- Give requirements stable IDs only when traceability helps. Prefer “An editor can rename a project; a viewer cannot” to legalistic filler.
- For each write, identify server authorization, validation, persistence, duplicate submission behavior, and what happens if the result is unknown after a timeout.
- Specify applicable quality constraints with conditions: target devices, input methods, content size, latency measurement, supported languages, privacy, and availability. Mark proposed targets as proposals.
- Name dependencies, unresolved contract questions, and excluded scope. Do not invent APIs or imply they exist.
- When revisiting implementation, report which requirements are met, changed, missing, or unverified, with evidence.

## Deliver

Use **requirement → acceptance example → dependency/unknown**. Add only enough examples to distinguish correct behavior from a plausible implementation.

Write each requirement as:

FR-01: [actor + behavior] — Accept: [observable example] — Depends/unknown: [...]
NFR-01: [constraint + condition] — Verify: [scoped check]
Close with out-of-scope, assumptions, open questions, and next step.

Example: Given a viewer sends a rename request directly, the server rejects it and the stored name remains unchanged. Hiding the edit button alone does not satisfy this requirement.

Include a failure or boundary case for consequential behavior. “Accessible,” “fast,” and “secure” need scoped verification criteria. Use `$flow` when branch order is the open question; `$component` when a reusable interaction needs a contract.

## Worked example

FR-01: The system shows the last 30 days of activity when a user opens the dashboard — Accept: recent work is reviewable without navigation — Depends: activity API exists, rate limits undocumented.
FR-02: The system preserves the date-range filter in the URL — Accept: the view can be shared and bookmarked — Depends: none.
NFR-01: Dashboard load reaches LCP under 2.5s on 4G mobile — Verify: measure on a mid-tier device; mark the target as a proposal.
NFR-02: All dashboard controls are keyboard-reachable with WCAG 2.2 AA contrast — Verify: keyboard pass plus contrast check.
Out of scope: custom report builder, CSV scheduling, mobile push notifications.
Assumptions: activity data is server-side and queryable by date range.
Open questions: past 30 days — paginate or show a summary?
Next: `$sitemap` for the app shell and dashboard routes.

## Gotchas

- Do not treat a hidden button as access control; require server rejection with unchanged data.
- Do not invent endpoints or imply they exist; list undocumented contracts as unknowns.
- Do not write "fast," "secure," or "accessible" without scoped verification criteria.
- Do not specify UI solutions; define observable behavior and defer interaction to flow or component.
- Do not present proposed latency or quality targets as committed guarantees.

## Boundaries

- Do not use when the idea is still vague — run `$intent` first.
- Do not use when requirements exist and the open question is navigation — use `$sitemap` instead.
- Do not specify UI solutions; define comparable behavior and let `$component` or `$flow` resolve the interaction.
