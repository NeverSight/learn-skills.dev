---
name: components
description: "Rapidly improve an existing website or application using components and design patterns from a controlled list of high-quality UI libraries. Use when the user invokes /components or /component-scout, asks to browse component libraries, wants suitable components added, or wants library-based UI inspiration. Inspect, select, implement, and verify within 10 minutes while preserving the normal quality bar."
---

# Component Scout

Find and implement high-quality UI components that genuinely improve the current product. Use the approved libraries as a curated design vocabulary. Do not search random component sites, invent an unrelated design system, or add visual effects simply because they look impressive.

## Approved sources

Search in this order:

1. shadcn/ui — default source for core application components and accessible primitives.
2. Magic UI — animated components, effects, and polished visual details.
3. Aceternity UI — distinctive sections, cards, navigation, backgrounds, and interactions.
4. Uiverse Galaxy — small controls and visual ideas; inspect community code carefully before using it.
5. 21st.dev — fallback discovery catalog when the primary libraries have no strong match.
6. Motion Primitives — fallback for restrained, reusable animation patterns.

Use Onda only for Remotion or programmatic-video projects. For ordinary websites, use it only as motion inspiration; do not paste Remotion-specific code into the application.

## Timebox

Target completion in under 10 minutes, as quickly as the task allows. Maintain the quality bar by limiting exploration and implementation scope:

- **Minute 0–1:** Inspect the current page, stack, theme, and existing components.
- **Minute 1–4:** Search approved sources and shortlist no more than three candidates.
- **Minute 4–8:** Implement the strongest one or two improvements.
- **Minute 8–10:** Verify the build, interactions, responsiveness, and visual integration.

Do not use the entire timebox when the correct solution is obvious.

## Workflow

1. Understand the requested page or feature and identify the highest-value UI opportunity.
2. Check existing project components before adding anything new.
3. Search only the approved sources using official documentation, registries, repositories, CLI tools, or configured MCP tools.
4. Compare candidates by product fit, existing-stack compatibility, visual consistency, accessibility, responsiveness, dependency cost, and performance.
5. Choose the strongest candidate and implement it directly.
6. Adapt its colors, typography, spacing, radius, content, and interaction style to the existing product.
7. Preserve all existing functionality.
8. Test the exact changed states and fix integration problems before finishing.

## Implementation rules

- Prefer shadcn/ui or existing project primitives for buttons, dialogs, menus, forms, tabs, tooltips, and other foundational controls.
- Use animated libraries selectively for meaningful feedback, hierarchy, or transitions—not decoration everywhere.
- When an exact component fits, use its provided source or supported CLI installation method.
- When only the idea fits, recreate the useful interaction or composition using the project's existing component system.
- Do not combine several conflicting visual styles on one page.
- Avoid introducing duplicate primitive libraries or multiple animation libraries.
- Inspect dependencies and source code before installation.
- Do not copy paid, Pro, private, or license-unclear components.
- Do not replace good existing UI merely because another component looks newer.
- Do not perform an unrelated redesign.

For Chrome extensions or injected UI, scope styles carefully and verify that the new component does not cover, shift, or block native website controls.

## Completion standard

Before finishing, verify that the component fits the existing design, its main interaction works, content is not clipped or overlapping, narrow and normal widths remain usable, supported light and dark themes work, no unnecessary dependency was added, and the project builds or the relevant targeted check passes.

Finish with only:

```
Added:
Source:
Adapted:
Verified:
```

If no approved component clearly improves the product, do not force one. Report that no suitable addition was found and briefly explain why.
