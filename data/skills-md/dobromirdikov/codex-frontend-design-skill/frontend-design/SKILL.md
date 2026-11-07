---
name: frontend-design
description: "Use when Codex needs to design, build, polish, or substantially redesign frontend UI: landing pages, websites, dashboards, web apps, components, prototypes, games, or visual QA for local interfaces where distinctive production-grade design matters."
---

# Frontend Design

Derived from Anthropic's `frontend-design` skill in `anthropics/claude-plugins-official`, licensed under Apache License 2.0. Modified for Codex with broader trigger wording, landing page rules, UI anti-patterns, asset guidance, and browser-based visual QA.

Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics. Implement real working code with strong attention to visual direction, layout, typography, assets, interaction design, responsiveness, and verification.

The user may ask for a component, page, application, or interface. They may include context about purpose, audience, brand, framework, or technical constraints.

## Workflow

1. Read the request and existing codebase conventions before choosing a direction.
2. Commit to a concrete visual concept that fits the product, audience, and domain. Examples: editorial finance terminal, Swiss industrial SaaS, luxury hospitality, playful learning lab, cinematic game HUD.
3. Implement the actual usable screen or flow first; do not substitute a marketing shell for an app, tool, or game.
4. Use real, generated, or domain-relevant visual assets when imagery would materially improve the result.
5. Make the interface responsive, accessible, and durable against text overflow, loading states, hover states, and narrow viewports.
6. Run the app locally when needed, inspect desktop and mobile layouts in a browser, fix visible defects, and check console errors before calling the work done.

## Design Thinking

Before coding, understand the context and commit to a clear aesthetic direction:

- **Purpose**: Identify the problem the interface solves and who uses it.
- **Tone**: Pick a concrete direction such as brutally minimal, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, soft, industrial, or another style that fits the request.
- **Constraints**: Respect framework, performance, accessibility, responsive behavior, and existing project conventions.
- **Differentiation**: Decide what should make the interface memorable.

Choose a specific concept and execute it with precision. Bold maximalism and refined minimalism can both work; intentionality matters more than intensity.

Then implement working code that is:

- Production-grade and functional.
- Visually striking and memorable.
- Cohesive with a clear point of view.
- Refined in typography, spacing, color, motion, and interaction states.

## Landing Page Rules

- Make the brand, product, venue, person, or offer obvious in the first viewport.
- Use the H1 for the literal product, brand, person, place, offer, or category. Put value propositions in supporting copy.
- Avoid the default split hero with text on one side and a decorative card or mockup on the other unless it is clearly the strongest domain-specific choice.
- Use a relevant image, generated bitmap, product screenshot, immersive scene, or real media when the page benefits from visual proof.
- Let the first viewport hint at the next section on desktop and mobile instead of making the hero feel like a sealed poster.
- Write concrete, domain-specific copy. Avoid empty SaaS phrases like "transform your workflow", "unlock your potential", and "seamless experience".

## UI Type Fit

- For apps, dashboards, editors, CRMs, and operational tools, prioritize dense scanning, predictable controls, and repeated-use ergonomics over marketing composition.
- For games, creative tools, portfolios, venues, and consumer products, allow stronger art direction, motion, atmosphere, and custom interaction.
- For redesigns inside an existing product, preserve useful conventions and improve the weakest visible surfaces first.

## Frontend Aesthetics Guidelines

- **Typography**: Choose fonts that feel deliberate and domain-appropriate. Avoid defaulting to Arial, Inter, Roboto, or system fonts unless the existing product already depends on them. Pair a distinctive display font with a refined body font when appropriate.
- **Color and theme**: Commit to a cohesive palette. Use CSS variables for consistency. Prefer clear dominant colors with sharp accents over timid, evenly distributed palettes.
- **Motion**: Use animation for meaningful effects and micro-interactions. Prefer CSS-only motion for static HTML. Use a motion library in React only when already available or clearly warranted. One well-orchestrated reveal often beats scattered effects.
- **Spatial composition**: Use layout deliberately: asymmetry, overlap, diagonal flow, grid-breaking elements, generous negative space, or controlled density when they match the concept.
- **Assets and imagery**: Prefer images, video, generated bitmap visuals, product screenshots, maps, textures, or domain-specific graphics when they reveal the thing being sold, used, played, or inspected. Avoid decorative SVG filler when a real or generated image would carry the design better.
- **Background and details**: Create atmosphere and depth without relying on generic decoration. Use textures, patterns, layered transparency, shadows, borders, cursors, or grain only when they support the chosen style.
- **Controls and affordances**: Use familiar controls and icons for actions. Buttons, tabs, toggles, sliders, menus, toolbars, and cards should match the task density and domain instead of defaulting to oversized SaaS blocks.
- **Responsive polish**: Define stable dimensions for fixed-format elements, prevent text overlap, verify mobile layouts, and avoid viewport-scaled font sizes that break composition.

Avoid generic AI-generated aesthetics: overused font choices, purple gradients on white, predictable card grids, cookie-cutter SaaS sections, and design choices that do not connect to the domain.

Vary designs across tasks. Do not repeatedly converge on the same typefaces, palettes, layout structures, or effects.

## Design Anti-Patterns

Avoid these unless the user explicitly asks for them or the existing product requires them:

- Purple-blue gradients on white, decorative blobs, bokeh, floating orbs, and generic mesh backgrounds.
- Centered SaaS hero, three-card feature grid, logo cloud, testimonial blocks, and FAQ sections used without domain-specific content.
- Inter-only typography, oversized rounded cards, low-contrast gray text, and button labels that wrap awkwardly.
- Fake dashboard screenshots with meaningless charts, placeholder names, or numbers that do not fit the product.
- In-app text that explains the UI's features, visual style, or keyboard shortcuts instead of making the interface self-evident.

## Implementation Standard

Match complexity to the aesthetic vision. Maximalist designs may need more elaborate effects and layered composition. Minimal or refined designs need restraint, precise spacing, careful type scale, and subtle states.

When working in an existing codebase, preserve established architecture and component patterns unless the request is specifically to redesign them. Keep accessibility, responsiveness, performance, and maintainability in scope.

## Visual QA Checklist

Before finishing substantial frontend work, verify the rendered result in a browser:

- Check desktop around 1440px wide, tablet around 768px, and mobile around 390px when the app can run locally.
- Fix console errors, blank renders, clipped text, overlapping UI, broken assets, unreadable contrast, awkward first-viewport composition, and broken mobile navigation.
- Confirm primary imagery loads, is framed intentionally, and reveals the real product, place, state, gameplay, or subject.
- Confirm all important text fits its container and remains readable across the tested widths.
- Confirm hover, focus, active, empty, loading, and error states for controls touched by the work.
