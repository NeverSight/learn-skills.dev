---
name: stitch-to-code
description: Use when implementing Google Stitch screens with a coding agent. Preserve Stitch's exact visual choices, reconcile inconsistencies across screens, avoid inventing product behavior from mockup content, reuse existing UI patterns, and validate the real implementation.
---

# Stitch to Code

Turn a set of Stitch screens into **one coherent app**, not a collection of independently copied mockups.

The core rule is:

> Preserve deliberate Stitch decisions exactly. Reconcile accidental inconsistencies. Ground behavior in the actual product.

## Use Lite by default

Lite needs no Stitch to Code project state.

Use the current Stitch references, the Stitch-generated `.stitch/DESIGN.md` when available, and the existing repository. Do not create metadata or registries just to use this skill.

Use **Strict** only when the project genuinely benefits from explicit screen history, shared-pattern tracking, or QA/provenance records. Read `references/STRICT_MODE.md` in that case.

## 1. Understand the product before coding

Inspect the repository and resolve what actually exists:

- routes and navigation;
- real entities/data;
- supported actions;
- roles/permissions when relevant;
- existing components and tokens;
- product docs, schemas, API clients/contracts when they exist;
- important loading, empty, error, denied, pending, and success states.

Do not infer a real feature simply because it appears in a mockup.

If a visible mockup control has no supported product action, remove/recast it rather than shipping a fake or inert control.

## 2. Read the relevant Stitch material together

Use stable Stitch project/screen IDs when available.

If Stitch MCP or specialized Stitch skills are available, use them to retrieve the current project, screens, `DESIGN.md`, and relevant assets. Fetch only what is needed for the current work.

Before implementing, compare the relevant screens together and identify:

- the shared shell, navigation, headers, panels, lists, forms, and actions;
- typography, iconography, colors, spacing, radii, assets, and density;
- declared breakpoints and responsive behavior;
- differences that appear intentional;
- differences that look like isolated drift.

Do not assume every local difference in a generated screen is a new canonical pattern.

## 3. Keep explicit Stitch choices exact

When Stitch defines a visual primitive, do not silently substitute a similar one.

Preserve as applicable:

- font family and declared weights/metrics;
- icon family;
- exact glyph;
- icon style/variant/state such as outlined/filled and relevant axes;
- colors and semantic tokens;
- spacing and radii;
- supplied logos/assets;
- explicit responsive thresholds;
- established component language.

If the exact dependency/resource is technically unavailable, make the fallback explicit rather than quietly replacing it.

`DESIGN.md` belongs to the Stitch design workflow. Preserve it. Add a rule only when a real project decision is missing and has been confirmed; do not turn `DESIGN.md` into a product-status or QA database.

## 4. Reconcile screens instead of copying contradictions

When screens disagree, decide whether the difference is:

- intentional and should stay;
- an isolated Stitch inconsistency that should be normalized;
- required by the real product;
- illustrative content that should disappear.

Prefer an already established shared pattern over creating another nearly identical header, card, button, search control, pagination, modal, or navigation family.

Do not over-normalize real feature-specific differences.

## 5. Implement real behavior

- Reuse existing components before creating new families.
- Wire only supported actions.
- Do not invent metrics, identities, balances, notifications, routes, filters, or mutations.
- Do not leave visible interactive-looking elements inert.
- Preserve exact/sensitive values when relevant.
- Keep desktop and compact views backed by the same underlying product data.
- Use Stitch/project breakpoints rather than familiar framework defaults when they are explicitly defined.
- Keep desktop dialogs content-driven; do not create large empty modal regions just to fill a viewport.

## 6. Check accessibility in the implementation

Accessibility is part of the coded product, not something a Stitch screenshot can prove.

Check the implementation itself for keyboard operation, visible focus, semantic structure, labels and accessible names, contrast, dialog/drawer behavior, and responsive/zoom behavior where relevant.

## 7. Validate the real app

For web work, run the application and inspect it in a real browser/browser automation environment.

Check the things most likely to drift:

- actual font loading, not only CSS declarations;
- icon family, glyph, and variant/state;
- key colors/tokens, spacing, radii, and assets;
- navigation and important actions;
- every visible control that appears interactive;
- responsive behavior around actual design breakpoints;
- horizontal overflow and critical truncation;
- modal/drawer sizing, scroll, close behavior, focus trapping/restoration;
- keyboard operation and visible focus;
- labels, headings, landmarks, and accessible names;
- runtime/console errors;
- loading/empty/error/permission states where relevant.

Run the repository's normal type/lint/test/build checks where appropriate.

Read `references/QA.md` when you need the fuller checklist.

## Done means coherent and working

Do not mark a surface complete merely because it resembles a Stitch screenshot.

Before finishing, make sure:

- the relevant Stitch references were considered together;
- explicit Stitch visual choices were preserved or deviations were stated;
- accidental cross-screen inconsistencies were reconciled without erasing intentional variants;
- unsupported mockup behavior was not invented;
- required interactions actually work;
- there are no misleading dead controls;
- the important responsive and accessibility behavior was checked in the rendered app;
- no unexplained runtime errors remain.
