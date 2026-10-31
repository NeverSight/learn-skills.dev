---
name: figma-design-tool-workflows
description: "Figma mastery and design-to-code: Auto Layout, component architecture, variable modes, Dev Mode handoff, Figma MCP server integration, Code Connect, and token pipelines. Use when working in Figma, converting designs to code, or setting up a design-to-code flywheel."
---

# Figma Design Tool Workflows — From Canvas to Production Code

## Figma as the Design System of Record

Figma is not a drawing tool. It is the single source of truth for design intent, component architecture, token definitions, interaction specifications, and handoff documentation. When used properly, a Figma file becomes a living specification that machines can read, humans can interpret, and CI/CD pipelines can validate against.

The shift in thinking is fundamental: every layer name, every component property, every variable definition in Figma is data. That data flows downstream into code generation, token pipelines, accessibility audits, and visual regression testing. A sloppy Figma file produces sloppy code. A well-architected Figma file produces components that are correct on the first pass.

This skill covers the full Figma workflow from component architecture through AI-assisted code generation and automated validation.

## Component Architecture in Figma

### Variants and Properties

Figma components support four property types that map directly to code component APIs:

- **Boolean properties** control visibility of child layers. A button's `showIcon` boolean maps to a React `showIcon?: boolean` prop. The icon layer is present or absent based on this toggle, which means the generated code conditionally renders the icon.
- **Text properties** expose editable text content. A button's `label` text property maps to a `children: string` or `label: string` prop. The designer controls the default, the developer overrides at the call site.
- **Instance swap properties** define composition slots. A button's `icon` instance swap maps to an `icon?: ReactNode` prop. The slot accepts any icon component from the icon library, and the generated code renders the passed component.
- **Preferred values** constrain instance swap choices to a curated set. Rather than showing every component in the file, preferred values limit the swap picker to relevant options (icon library components only, for example).

### Variant Architecture

Use **variants** when a component has visually distinct states that change multiple properties simultaneously. A Button component might have variants across two axes: `variant` (primary, secondary, ghost, danger) and `size` (small, medium, large). Each combination is a distinct visual design within the same component set.

Use **component properties** (booleans, text, instance swaps) when a single property toggles independently. Whether a button shows an icon is independent of its variant and size. Making this a boolean property rather than doubling the variant count keeps the component manageable.

Use **separate components** when two patterns share no structural DNA. A Button and a Card are separate components, not variants of each other.

### Nested Components and Slot Patterns

Production-grade Figma components use nested sub-components to create composition points. A Card component contains a `CardHeader` sub-component, a `CardBody` sub-component, and a `CardFooter` sub-component. Each sub-component is a separate Figma component that the Card references via instance swap slots. This mirrors the compound component pattern in React (`<Card><Card.Header /><Card.Body /><Card.Footer /></Card>`).

### Naming Conventions

Follow a `Category/Type/State` naming hierarchy:

- `Button/Primary/Default`
- `Button/Primary/Hover`
- `Button/Secondary/Disabled`
- `Input/Text/Default`
- `Input/Text/Error`
- `Card/Elevated/Default`

This naming convention creates automatic grouping in the Figma assets panel and maps cleanly to code organization: the `Button` directory contains `Primary` and `Secondary` variant files, each handling their own states.

## Variable Modes

Figma variables replace static styles with dynamic, mode-switchable tokens. Variables organize into collections with multiple modes.

### Token Layer Architecture

Structure variable collections in three tiers:

1. **Primitive collection** — raw values: `blue-500: #3b82f6`, `spacing-4: 16`, `radius-md: 8`. A single mode; these values never change.
2. **Semantic collection** — contextual meaning with modes for light/dark/high-contrast: `color-bg-primary` resolves to `white` in light mode and `neutral-900` in dark mode. `color-text-primary` resolves to `neutral-900` in light mode and `neutral-50` in dark mode.
3. **Component collection** — component-specific bindings: `button-primary-bg` references `color-action-primary`, which references `blue-500` in the primitive layer. Modes here handle density (compact/default/comfortable) or brand switching (brand-a/brand-b).

### Mode Switching

Variable modes enable designers to preview every combination without duplicating frames. A single button component, bound to semantic variables, previews as light primary, dark primary, high-contrast primary, light compact, dark comfortable, and every other permutation — all by switching the mode on the enclosing frame.

This is the design equivalent of CSS custom property theming. The structure must match: Figma variable names should correspond directly to CSS custom property names or token identifiers in the codebase.

## Auto Layout

Auto Layout is the mechanism that makes Figma components developer-friendly. A component without Auto Layout is a static drawing. A component with proper Auto Layout is a responsive specification that communicates padding, spacing, alignment, and resize behavior to developers.

Key principles:

- **Every component uses Auto Layout.** No exceptions. If a component cannot be built with Auto Layout, the design needs to be reconsidered.
- **Padding and spacing use variables.** Bind Auto Layout padding and item spacing to spacing variables so that density modes work automatically.
- **Fill container for responsive elements.** Text blocks and content areas use "Fill container" width so they stretch to available space, matching CSS `flex: 1` behavior.
- **Hug contents for intrinsic sizing.** Icons, badges, and labels use "Hug contents" so they size to their content, matching CSS `width: auto` behavior.
- **Absolute positioning sparingly.** Badges positioned on avatar corners and floating action buttons use absolute positioning within Auto Layout. This maps to CSS `position: absolute` within a `position: relative` container.

## Dev Mode

Figma Dev Mode is the bridge between design and development. When a developer inspects a component in Dev Mode, they see:

- **Component properties** mapped to code props
- **CSS values** for every selected layer (spacing, colors, typography)
- **Variable references** showing the token name rather than the raw value
- **Annotations** added by designers explaining behavior, interaction rules, and edge cases
- **Code snippets** generated from component configuration
- **Measurements** between elements (spacing, alignment guides)

Dev Mode effectiveness depends entirely on how well the designer structured the component. Proper naming, variable binding, and Auto Layout produce clean Dev Mode output. Poor structure produces noise.

## Figma MCP — The AI-Assisted Game Changer

The Figma Model Context Protocol (MCP) server allows AI assistants like Claude to read Figma design files programmatically. This is the single most impactful development in design-to-code workflow since component libraries.

With Figma MCP, Claude can:

- Read the complete structure of a design file (pages, frames, components)
- Extract component properties, variants, and their values
- Read variable definitions and mode configurations
- Understand Auto Layout specifications (padding, spacing, alignment, sizing)
- Extract color, typography, and effect styles
- Read prototype flows and interaction definitions

This means a designer can build a component in Figma, and Claude can read that component's specification, generate production-quality code (React, SwiftUI, CSS), and produce accompanying tests — all without a human translating the design spec into a ticket.

## The Design-to-Code Flywheel

The flywheel operates in six steps:

1. **Design** — Designer builds a component in Figma with proper architecture: Auto Layout, variables, component properties, correct naming.
2. **Read** — Claude reads the component specification via Figma MCP: layout structure, token bindings, property API, responsive behavior.
3. **Generate** — Claude produces code: React component with TypeScript types, CSS Module with token references, Storybook story with all variants, unit test covering props and accessibility.
4. **Validate** — Visual regression testing (Chromatic, Percy) compares the rendered component against the Figma source. Accessibility testing (axe-core) validates WCAG compliance.
5. **Iterate** — Designer updates the component in Figma. The MCP read detects changes. Claude generates an incremental code update. Visual regression catches any drift.
6. **Ship** — CI/CD pipeline deploys validated components. Token pipeline syncs updated variables. Consuming applications pull the latest version.

Each cycle gets faster. The first pass through the flywheel for a new component might save 50% of development time compared to manual implementation. Subsequent iterations on existing components save 70-80% because the structure, tests, and stories already exist and only need updating.

## Routing

For **working in Figma** — Auto Layout in depth, component architecture,
variable modes, prototyping, Dev Mode and handoff, library management, naming
and file organization, the plugin essentials, and the shortcuts that actually
save time: read `references/figma-mastery-workflows.md`.

For **getting Figma into production code** — pipeline architecture, Style
Dictionary configuration, token transformation examples, CI/CD integration,
visual regression testing, component naming conventions, Storybook integration,
multi-brand and white-label architecture, and accessibility in the pipeline:
read `references/design-to-code-pipeline.md`.

For **the MCP flywheel** specifically: read `references/figma-mcp-ai-flywheel.md`.

## Cross-References

- **Component code output and patterns** — reference `component-patterns-code` for React, SwiftUI, and CSS component architecture, compound components, render props, and polymorphic patterns that Figma MCP-generated code should follow.
- **Design system governance** — reference `design-systems-architecture` for token hierarchy (primitive, semantic, component), versioning strategy, contribution models, and change management processes that govern the Figma library.
- **Visual design tokens** — reference `ui-visual-design-system` for color theory, typography scale, spacing system, and elevation definitions that underpin Figma variable collections.
- **Accessibility in Figma** — reference `accessibility-inclusive-design` for Figma accessibility plugins (Stark, A11y Annotation Kit), color contrast checking, focus order annotation, and screen reader text specification within design files.
- **Interaction and motion** — reference `interaction-motion-design` for Figma prototyping best practices, smart animate specifications, and motion token definitions that map to CSS transitions and animations.

## Key Sources

- Figma official documentation: Components, Variables, Auto Layout, Dev Mode, Code Connect
- Figma MCP server documentation and API reference
- Style Dictionary documentation for multi-platform token transformation
- Tokens Studio (Figma plugin) documentation for token management
- Chromatic documentation for visual regression testing with Storybook
- W3C Design Tokens Community Group specification for token format
