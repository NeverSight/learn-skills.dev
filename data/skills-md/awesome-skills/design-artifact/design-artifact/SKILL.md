---
name: design-artifact
description: Design, build, and verify distinctive one-off visual artifacts such as landing pages, interactive prototypes, component explorations, product mockups, dashboards, onboarding flows, and motion studies. Use for high-fidelity HTML design work or design-led implementation; use create-html-deck instead when the primary deliverable is a slide presentation.
---

# Design Artifact

Act as a designer who can ship the artifact, not as a style generator. Start from the user's context, establish a coherent visual system, build a complete local result, and verify it in the real rendering environment.

## Preserve the output contract

- Deliver the working artifact, not only a mood board, style description, or screenshot, unless the user explicitly requested exploration only.
- Treat supplied copy, screenshots, code, tokens, specs, and handoffs as authoritative inputs. Do not re-interview the user for decisions those materials already contain.
- Ask only when a missing decision would materially change scope, brand direction, interaction, or production integration. Otherwise state the assumption and continue.
- Make the primary path usable and the decision-relevant states observable.
- Keep content honest. Mark draft data and unfinished copy instead of presenting them as real product facts.

## Route the request

- Use `create-html-deck` for a complete browser-native slide presentation.
- Use a token-spec skill when the requested deliverable is a persistent `DESIGN.md` or machine-readable token system.
- Implement inside the actual repo when the user asks for production code. Reuse its stack, components, tokens, and conventions.
- Produce a standalone HTML file for one-off visual studies, prototypes, option boards, and demonstrations when no production stack is required.
- Inspect a named brand or reference for principles and constraints. Do not clone a proprietary interface or identity.

## Establish the brief

Determine:

- audience and primary job
- intended output format and viewing environment
- locked content and required interactions
- source material, brand system, and existing implementation
- fidelity target and the decision the artifact should enable

Ask only for missing information that would materially change the result. Skip questions for small continuations and obvious defaults. State consequential assumptions when proceeding without an answer.

Turn the brief into a compact artifact contract before building:

- one primary job
- one target user or audience
- one intended environment and viewport range
- locked content and non-goals
- primary interaction or decision
- concrete completion and verification criteria

## Read context before designing

Prefer evidence in this order:

1. existing product and repo source
2. design tokens, theme files, and UI components
3. supplied screenshots, brand docs, and content
4. prior mockups and reference products
5. newly invented visual language

For repo work, inspect the files that actually define the interface: global styles, tokens, layouts, routing, shared primitives, and representative pages. A file tree is only a map; read the source before reproducing its vocabulary.

## Define the artifact system

Choose a small, explicit system before building:

- type families, scale, weights, and numeric treatment
- neutral, surface, ink, border, accent, and semantic colors
- spacing rhythm and layout grid
- radii, borders, shadows, and elevation posture
- component density and interaction rules
- motion timing, easing, and reduced-motion behavior

Use existing tokens when available. When inventing a system, keep the palette and component vocabulary intentionally small.

## Choose the right form

- Static comparison: show alternatives side by side in one HTML canvas.
- Interaction or workflow: build a clickable prototype with the primary path and key states.
- Product screen: implement the actual layout hierarchy and decision-relevant data.
- Component exploration: expose meaningful variants and states in a compact lab.
- Motion study: make state transitions observable and controllable.

Use plain HTML, CSS, and JavaScript for portable standalone artifacts. Use React only when state, interaction complexity, or the target repo makes it useful. Pin any remote dependency and avoid adding one for decoration alone.

## Build in passes

1. **Structure:** establish the semantic hierarchy, content order, responsive layout, and primary path without decorative polish.
2. **System:** apply the chosen type, color, spacing, border, elevation, and motion vocabulary consistently.
3. **States:** implement the default, interaction, loading, empty, error, and completion states that matter to the brief.
4. **Polish:** refine line breaks, density, alignment, crops, focus treatment, and transitions at the actual target viewports.
5. **Cleanup:** remove filler copy, dead controls, abandoned variants, unused dependencies, and console noise.

Do not spend the polish pass compensating for a weak hierarchy. Fix structure first.

## Explore and consolidate

When the visual direction is genuinely open, present three meaningfully different options:

1. conservative: closest to existing patterns
2. strong-fit: the best interpretation of the brief
3. divergent: a useful challenge to the assumed direction

Vary composition, hierarchy, density, type, interaction, or motion—not merely color. Once the user chooses, consolidate into a single coherent result rather than leaving a gallery of unfinished options.

## Build complete states

Implement the states needed to understand the experience:

- default and focus/hover
- loading when waiting is part of the flow
- empty when absence changes the interface
- error and recovery when failure matters
- success or completion when the flow ends

Make the primary path operable. Use semantic HTML, visible focus states, at least 44px touch targets, and responsive behavior. Respect `prefers-reduced-motion` for non-trivial animation.

For optional in-page design controls, use a small `Tweaks` panel for meaningful dimensions such as density, theme, type scale, layout, or motion. Hide it cleanly and persist settings only when continuity helps.

## Keep content honest

Every element must earn its place. Do not add:

- invented metrics, testimonials, or product claims
- generic feature grids used as filler
- dashboards full of arbitrary data
- icons that do not improve scanning
- placeholder sections that change the user's strategy

Mark unfinished copy as draft. Ask before adding major sections or capabilities not present in the brief.

## Avoid design sludge

Do not default to:

- aggressive gradients or glassmorphism
- rainbow palettes
- oversized rounded cards as the only hierarchy
- stock-photo heroes
- decorative charts and SVG illustrations with no informational role
- emoji outside an established brand language
- vague labels such as “Insights,” “Growth,” or “Optimize” without precise content
- endless equal-sized card grids

Minimal is not automatically refined, and dense is not automatically cluttered. Use typography, rhythm, alignment, contrast, and interruption intentionally.

## Design by medium

### Typography

Use hierarchy before boxes and decoration. Choose type to fit the artifact: editorial, product, technical, luxury, or data-heavy. Keep families and weights limited, preserve readable line lengths, and avoid tiny text that only works in a design screenshot.

### Color

Prioritize contrast and semantic consistency. Use one primary accent unless the source system requires more. Reserve danger and success colors for actual states.

### Layout

Optimize product interfaces for comprehension and action. Let marketing artifacts land one central idea per section. Show only data that helps the viewer decide.

### Motion

Use motion to clarify continuity, state change, and loading. Do not delay the user, loop without purpose, or use animation to hide weak hierarchy.

### Images and references

Use supplied imagery when possible. If real assets are unavailable, prefer strong type and layout over elaborate fake illustrations. Transform reference principles instead of reproducing distinctive proprietary screens.

## Verify in the real environment

Before delivery:

1. Confirm the expected files exist and open from their final paths.
2. For a standalone HTML artifact, run the bundled structural check:

   ```bash
   python3 <skill-dir>/scripts/check_artifact.py /absolute/path/to/artifact.html
   ```

   For repo work, run the project's syntax, type, build, test, and lint checks that cover the changed surface.
3. Open the artifact in a browser and check console and page errors.
4. Exercise the primary interaction and key states.
5. Inspect screenshots at the intended viewport and at least one narrower viewport.
6. Check local assets, focus visibility, overflow, text wrapping, and responsive behavior.
7. Verify theme, variation, or reduced-motion modes when provided.
8. Distinguish structural success from visual success. Record both instead of treating a passing build as visual approval.

A passing build does not prove visual quality. Inspect the rendered composition. Never claim browser verification unless it actually happened.

## Deliver

Report the exact artifact path, what it contains, the checks and viewports actually used, and any remaining caveat or remote dependency. Keep the handoff brief and lead with the result.

## Attribution

Adapted from `claude-design` by BadTechBandit under the MIT License. This variant uses a neutral name, removes hosted-product plumbing, and routes slide-deck work to `create-html-deck`.
