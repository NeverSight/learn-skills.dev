---
name: superior-ui
description: Build, redesign, or visually refine product interfaces using project evidence, real content, functional states, and deliberate composition. Use for implementation work on websites, apps, dashboards, landing pages, or component systems. Do not use for read-only audits or logic-only changes.
---

# Superior UI

Produce an interface that belongs to this product. Derive choices from the user's request, existing design evidence, content, and task flow; do not impose a house style or mechanically ban familiar techniques.

## Establish the brief

Before editing, identify:

- the primary user and job this surface supports;
- the content and actions that deserve first attention;
- existing design owners: tokens, typography, components, layouts, brand assets, and documented decisions;
- implementation constraints, affected routes, and states;
- what must remain unchanged.

Inspect the rendered surface when practical. If direction is missing, make the smallest reversible assumption that fits the product and disclose any choice that materially shapes the result.

## Choose a visual thesis

State the direction in one useful sentence, such as “dense operational console with quiet chrome and high-signal status color.” The sentence must constrain actual decisions about hierarchy, density, type, color, shape, or motion. Avoid mood labels that could describe any product.

When the user asks to recreate, match, or closely follow a supplied design, that reference is the visual direction for the requested scope. Do not shortlist alternatives or redesign its visible composition unless the user asks. Read [references/design-recreation.md](references/design-recreation.md) for fidelity, adaptations, and visual verification.

When no governing visual direction exists, shortlist two or three materially different candidates that fit the product and explain each candidate's task fit, defining traits, and principal risk. Select one primary direction before implementation unless the user explicitly requests parallel concepts. A supporting influence may shape a limited detail, but do not blend several named styles into an incoherent trend collage. When a reference's role is ambiguous, preserve its observable characteristics and disclose material assumptions rather than silently redesigning it.

Read [references/visual-system.md](references/visual-system.md) when the task creates a new visual direction, changes several components, needs substantial visual polish, or recreates a design from an image or external reference. Also read [references/style-and-palette-direction.md](references/style-and-palette-direction.md) when selecting among named UI styles, establishing a new palette, or assigning colors to body, component, and typography roles. For focused edits, preserve the local system without loading either reference.

Read [references/reference-source-hygiene.md](references/reference-source-hygiene.md) whenever a screenshot, template, repository, demo, or third-party design materially informs the implementation. Use the reference for source-identity cleanup and for deciding when copied or adapted material requires attribution or license preservation.

Read [references/page-closure-and-footer.md](references/page-closure-and-footer.md) when building or substantially redesigning a landing page, homepage, multi-section marketing page, or footer. Treat the ending as a deliberate part of the page composition without assuming that every site needs a large multi-column footer.

Read [references/semantic-html-and-search-discovery.md](references/semantic-html-and-search-discovery.md) when building or substantially changing a public page whose content must be discoverable, linked, or indexed, including landing pages, homepages, articles, documentation, catalogs, and public detail routes. Keep private dashboards and authenticated tools outside search-oriented requirements unless the product contract says otherwise.

Read [references/expressive-composition-and-component-craft.md](references/expressive-composition-and-component-craft.md) when the direction calls for asymmetric composition, layered depth, editorial tension, or bespoke tactile component details. Use those patterns as candidates justified by content and task—not as mandatory decoration or randomized style selection.

Read [references/motion-and-rendering-performance.md](references/motion-and-rendering-performance.md) when motion is a substantial part of the experience, including animated navigation, overlays, scroll entry, coordinated state transitions, or expressive microinteractions. Keep motion purposeful, accessible, and proportionate to runtime cost.

## Build around the task

- Start with semantic structure and information order; decoration follows.
- Give each region a job. Remove sections that exist only to complete a familiar template when designing freely; for an explicit recreation, preserve the requested reference structure and handle unavailable content honestly.
- Reuse existing primitives when they express the needed hierarchy. Add a variant only when the existing contract cannot.
- Use spacing, type, contrast, alignment, and grouping to create hierarchy before adding containers or effects.
- Let repeated components reflect repeated content. Do not force unlike information into identical cards.
- Keep responsive and accessibility behavior intact. Load the dedicated skills when either concern is a substantial part of the request.

Load `superior-ux` when the primary work is a journey, information architecture, task flow, cross-screen continuity, feedback, or recovery contract. Keep ordinary page hierarchy and visual interaction design here.

## Protect product integrity

Read [references/product-integrity.md](references/product-integrity.md) when the surface includes dashboards, marketing claims, forms, navigation, asynchronous data, or multiple UI states.

At minimum:

- never fabricate metrics, customers, testimonials, activity, compliance, or destinations;
- make controls work, remove them, or label them honestly as unavailable;
- distinguish loading, first-use, filtered-empty, permission-denied, validation, error, and success states when relevant;
- write specific labels and actions using the product's vocabulary;
- preserve user data and existing behavior outside the requested change.

## Critique before delivery

Review the result from three distances:

1. **Page:** Is the primary task obvious, does the composition have intentional rhythm, and does the page end with deliberate visual and informational closure?
2. **Component:** Does each component earn its boundary, emphasis, and interaction?
3. **Detail:** Are labels, icons, states, focus, alignment, and content honest and coherent?

Challenge generic template habits when creating a new direction. In an explicit recreation, the supplied design is evidence for the requested visual choices; do not discard them merely because they resemble a template.

## Verify

Exercise changed interactions and relevant states. Check representative narrow and wide viewports, content extremes, keyboard flow, and the project's normal lint/type/build checks in proportion to the change. For recreation, compare rendered output against the reference at a comparable viewport when practical, iterate on material differences, and report unverified fidelity or necessary deviations. Report concrete results and any unverified risk.

Load `superior-performance` when loading, rendering, responsiveness, bundle cost, or client memory is a primary measured concern. Keep ordinary motion and rendering discipline in this skill when no dedicated performance investigation is needed.
