---
name: impeccable-lite
description: Design, build, redesign, critique, audit, and refine frontend interfaces with strong visual direction and production-ready UX. Use for websites, landing pages, dashboards, application UI, components, forms, onboarding, empty states, responsive behavior, accessibility, typography, color, layout, motion, UX copy, or when an interface feels generic, bland, cluttered, inconsistent, or unfinished. Do not use for backend-only or non-UI tasks.
---

# Impeccable Lite

> Derived and modified from [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus under Apache-2.0.

Create distinctive, coherent, production-ready interfaces without adding process machinery. Apply design judgment directly to the user's request and the existing product.

## Principles

- Let the brief win. Honor explicit aesthetics, constraints, content, brand decisions, and user priorities.
- Preserve product truth. Never invent claims, capabilities, prices, testimonials, metrics, or configuration.
- Distinguish refinement from redesign. Refinement preserves the current identity and behavior. Redesign preserves the product and function but may replace the visual language.
- Treat existing code as evidence. Read the relevant route, component, tokens, styles, and representative neighboring UI before deciding.
- Prefer one committed direction over a mixture of safe ideas.
- Make design serve the surface. Marketing can earn expression; product UI should disappear into the task.
- Reuse the project's components, tokens, icon set, and conventions before introducing anything new.
- Keep verification bounded. Build fully, inspect once, fix findings together, confirm once, and stop.

## Workflow

1. Understand the request and inspect the target plus one representative source of visual truth.
2. Classify the work as creation, redesign, refinement, critique, or technical audit.
3. Identify the surface mode and the visitor's primary success condition.
4. Resolve only decisions that materially change the result. Ask concise questions when audience, content, scope, or visual authority is genuinely unclear.
5. Commit to a coherent direction before editing.
6. Implement the complete requested scope, including meaningful states and responsive behavior.
7. Verify the rendered result and relevant automated checks in no more than two inspection rounds.
8. Report what changed, what was verified, and anything intentionally left out.

For critique or audit requests, inspect and report without editing unless the user also asks for changes.

## Surface modes

Choose by surface, not by company category.

### Persuade

Use for landing pages, campaigns, pricing, and marketing. Help the visitor understand, believe, and act. Give the first viewport a clear thesis, demonstrate the product instead of repeating claims, and make the primary action unmistakable.

### Operate

Use for dashboards, tools, settings, editors, and authenticated application UI. Optimize for task completion, scanability, consistency, familiar affordances, and complete interaction states. Decoration must not compete with the work.

### Read

Use for documentation, articles, guides, help, and changelogs. Optimize structure, wayfinding, typography, and comprehension. Keep prose readable and navigation predictable.

### Experience

Use for portfolios, galleries, showcases, and immersive work. Let the artifact lead while the interface recedes. Use interaction and motion only where they strengthen exploration.

## Establish direction

For an established surface, inherit its visual system unless the user explicitly requests a redesign. A missing design document does not make an existing product greenfield.

For a new surface, determine:

- who is using it and in what situation
- what they need to understand or accomplish
- what content and functionality are real
- what visual world fits the subject and audience
- what should make the result recognizable rather than generic
- what must remain unchanged

Define the direction in one compact statement covering the visual thesis, palette character, typography character, composition, and one memorable interaction or detail. Do not present a large menu of near-identical options when one well-supported direction will do.

## Craft the interface

### Hierarchy and layout

- Make the primary action and information hierarchy obvious within seconds.
- Group related elements tightly and separate distinct sections generously.
- Use spacing rhythm deliberately, with more space above a heading than below it.
- Prefer composition and alignment over wrapping everything in containers.
- Use cards only when grouping benefits from a bounded surface. Never nest cards by reflex.
- Make responsive changes structural: collapse navigation, reorder content, resize grids, and adapt tables instead of merely shrinking type.
- Avoid horizontal overflow at every supported viewport.

### Typography

- Choose type that fits the product rather than defaulting to fashionable sameness.
- Use a clear scale with intentional differences in size, weight, and line height.
- Keep long-form body text near 65 to 75 characters per line.
- Test the real copy. Handle long names, translated text, dynamic values, and user content without clipping.
- Use monospace for code, data, or measurement, not as a costume for technical products.

### Color and depth

- Build a small semantic palette for backgrounds, surfaces, text, borders, actions, and states.
- Maintain at least 4.5:1 contrast for normal text and 3:1 for large text and essential graphical controls.
- Derive secondary text from its surrounding color context instead of placing generic gray on colored surfaces.
- Use accent color to communicate priority or state, not to decorate every section.
- Pick either a border or a shadow as the primary elevation cue. Avoid redundant outlines under diffuse shadows.
- Use gradients, glass, glow, grain, and blur only when the chosen visual world requires them.

### Components and interaction

- Preserve semantic HTML and native platform behavior where possible.
- Use the existing component library before creating replacements.
- Provide visible hover, focus, active, selected, disabled, loading, empty, success, warning, and error states where relevant.
- Keep keyboard navigation and screen-reader relationships intact.
- Make touch targets at least 44 by 44 CSS pixels when practical.
- Keep overlays usable outside clipping containers and within the viewport.
- Prefer inline or progressive interactions over a modal unless interruption or protected focus is necessary.
- Write controls as actions and errors as a problem plus a recovery path.

### Motion

- Use motion to explain state, continuity, hierarchy, or causality.
- Keep content visible by default and honor `prefers-reduced-motion`.
- Favor a small number of authored moments over identical entrance animations on every section.
- Keep product UI transitions quick and avoid making frequent tasks wait for choreography.
- Avoid bounce and elastic easing unless the product's established motion language explicitly calls for it.

### Content and assets

- Use the product's vocabulary and preserve factual copy unless changing it is in scope.
- Prefer real or clearly labeled illustrative content over vague placeholders.
- Use one consistent icon family. Do not substitute emoji or arbitrary Unicode symbols for interface icons.
- Use meaningful imagery at the scale the composition needs. Do not fill missing content with decorative chrome.
- Give every informative image useful alternative text and every decorative image empty alternative text.

## Reject generic defaults

Unless the brief or existing system clearly earns them, avoid:

- repetitive grids of equal cards with an icon, heading, and paragraph
- nested cards and containers inside containers
- generic hero layouts that could belong to any product
- decorative metric cards, progress rings, or charts without information value
- gradient text and purple-blue gradients as automatic emphasis
- a rounded-square icon tile above every heading
- an eyebrow label above every section title
- oversized pills for ordinary containers or controls
- decorative side borders on cards and callouts
- glassmorphism, grid backgrounds, or noise added only to make a surface feel designed
- display fonts in dense application controls
- custom interactions that make standard tasks less familiar
- invented testimonials, numbers, integrations, or product behavior

Do not merely soften a generic pattern. Replace it with a composition grounded in the content, task, and visual direction.

## Production floor

Do not trade away:

- semantic structure and accessible names
- keyboard operation and visible focus
- readable contrast in light and dark themes
- reduced-motion support
- responsive behavior across mobile and desktop
- loading, empty, error, disabled, and success states where applicable
- input validation and safe content rendering
- internationalization and text expansion resilience
- image sizing, lazy loading, and stable layout
- cross-browser behavior for supported browsers
- performance appropriate to the effect's value

Avoid adding a dependency for a minor visual effect. Prefer CSS, native browser capabilities, and installed project tools. Bound expensive animation and rendering work, clean up observers and listeners, and avoid blocking initial content on non-critical assets.

## Verification

For frontend changes:

1. Run the project's relevant lint, type, and test commands.
2. Inspect desktop and mobile together in one batched round using available browser or screenshot tooling.
3. Check hierarchy, overflow, contrast, controls, focus, states, content truth, and consistency with the chosen direction.
4. Fix material findings in one batch.
5. Confirm the fixes once and stop polishing.

For critique or audit work, report skipped or failed browser steps with concrete reasons.
