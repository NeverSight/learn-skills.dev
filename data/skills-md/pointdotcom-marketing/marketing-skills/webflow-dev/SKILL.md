---
name: webflow-dev
description: Build or revise Webflow pages from supplied designs by reusing the site's existing classes, components, assets, responsive patterns, and interactions. Use for design-to-Webflow implementation, section rebuilds, responsive parity work, or Webflow cleanup where the existing site is the implementation system and the design is the visual source of truth.
---

# Webflow Development

Treat the existing Webflow site as the implementation system and the supplied design as the visual source of truth. Match the design using existing classes, components, assets, responsive patterns, and interactions.

## Scope and access

Establish the exact site, page, branch, and source frame before editing. Keep work on the current branch and unpublished unless the user authorizes another target or publishing. Protect shared components and global styles unless the requested change includes their wider effects.

Use the available source-native integration for Figma or Paper. If it cannot access the design, use an available authorized export or explain the missing dependency. Desktop MCP is not required when another native integration provides the necessary design information.

## Implementation constraints

Inspect the target and comparable site sections before adding new structures. Reuse the site's utilities for typography, color, containers, spacing, buttons, and layout. Read the actual source design for copy, order, dimensions, assets, crops, and responsive intent.

Create a class only when existing patterns cannot express a required structure, interaction, or responsive adjustment. Use semantic names and shared classes across repeated elements. Keep typography and color on existing utilities. Every new class must be attached to an active element and have a defensible purpose.

Reuse matching site assets. Export missing artwork from the design at an appropriate resolution and import it once. Preserve source SVG artwork when available and match specific design icons. Supply useful alt text.

Sliders, tabs, accordions, forms, and filters are functional requirements. Prefer existing native components and scope custom code to the relevant section. For testimonial sliders, use [interaction-checks.md](references/interaction-checks.md).

## Tool and cleanup checks

Inspect partial-success messages and dropped-style warnings. Verify applied global classes, ambiguous combo-class computed styles, custom-code contents, and managed image references when tool results leave uncertainty. Resolve warnings that affect the requested result.

Remove only superseded elements, code, and styles created during this task. Before deleting a style, establish that no active element uses it. Leave no abandoned duplicate sections, placeholders, or unused task-created classes.

## Acceptance and handoff

Compare all in-scope sections against the source design at the site's configured breakpoints. Verify copy, hierarchy, spacing, colors, assets and crops, stacking, and interactions, including keyboard access. For a localized change, focus verification on the changed section and affected shared behavior.

Report the completed changes, any new classes with their purpose, verification performed, material limitations, and publication status. A per-section progress ledger or full inventory of reused utilities is unnecessary unless requested.
