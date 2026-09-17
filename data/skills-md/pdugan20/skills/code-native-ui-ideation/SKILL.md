---
name: code-native-ui-ideation
license: MIT
description: Use when a user wants to brainstorm or compare multiple runnable UI, interaction, layout, visual, or motion directions in an existing web or native app before choosing one. Do not use for exact implementation of a selected design, production delivery, audits, or requested static or generated mockups.
---

# Code-Native UI Ideation

## Core principle

Make design decisions comparable in the running product. Hold representative content, data, state, and constraints constant while varying named design choices.

## Stage gate

Determine the current stage before proposing implementation:

- **Choose directions:** The user asks to brainstorm, contribute ideas, or decide what is worth building first. Respond with three to five directions, a short thesis and tradeoff for each, and ask them to select two to four. Stop there. Do not enumerate implementation files, promise to build every idea, or treat your own recommendation as the user's selection.
- **Build variants:** The user explicitly asks to implement alternatives now or has selected the comparison set. Build that small set in the project-native comparison surface.
- **Graduate:** The user has selected a direction and explicitly asks to clean up or productionize it. Follow the graduation boundary below.

A request for an exploration plan, expected handoff, or concrete next steps does not advance the stage. At the choose-directions stage, the concrete plan is to narrow the directions before implementation.

## Choose directions

Use this section only at the choose-directions stage:

1. Inspect only the context needed to understand the decision, including the current interface and design system when available.
2. Propose three to five total comparison directions, including the user's ideas. Make each a named design decision with a short thesis and tradeoff.
3. End with a selection question and wait. Do not load the platform implementation guide, outline files or build phases, or offer to implement all directions.

### Optional design-system distance

When the user wants directions at different relationships to an existing design system, first identify the repository-backed foundations that should remain stable and the component conventions that may vary. Then use the requested range; do not force these postures into unrelated exploration:

- **Faithful:** Reuse established tokens, primitives, interaction patterns, and visual language. Improve the component from inside the existing vocabulary.
- **Stretch:** Preserve the foundations while extending one named pattern, primitive, or rule. State what is new and why it could belong in the system.
- **Divergent:** Preserve the product behavior, content, accessibility, and comparison constraints while intentionally departing from named visual or component conventions. State what changes and what remains protected.

Do not present token swaps, color changes, or arbitrary decoration as meaningful distance. The directions must embody different system relationships while keeping the underlying job comparable.

## Build variants

Use this section only after the user has selected directions or explicitly asked to build alternatives now:

1. Inspect the instructions, interface, design system, data, and existing development surfaces.
2. Define one comparison contract before building:
   - Give each variant a named design decision, not merely a different label or color.
   - Use the same representative content, data snapshot, state, device or viewport, and interaction scenario across variants.
   - When design-system distance is an axis, record the posture, protected foundations, and intentional departures for each variant.
   - Include fixtures that expose meaningful differences and edge cases.
   - Provide one obvious way to switch among or inspect the variants.
3. Load the one relevant platform guide:
   - For SwiftUI or other Apple-native work, read [references/swiftui.md](references/swiftui.md).
   - For React Native work, read [references/react-native.md](references/react-native.md).
   - For browser-based web work, read [references/web.md](references/web.md).
4. Build inside the project. Reuse its Storybook, previews, development routes, fixtures, tokens, assets, and components before adding infrastructure. Keep additions lightweight and reversible.
5. Render on the target platform. Exercise distinguishing interactions and states, capture useful screenshots, and run focused checks proportional to exploration.
6. Report how to compare the variants, what each emphasizes, what was exercised and checked, and a concrete cleanup inventory. Ask the user to choose if they have not.

## Graduation

Exploration ends with a selected direction and a cleanup inventory. Do not turn selection into production work unless asked.

Do not describe exploration variants as production-ready. They are deliberately lightweight evidence for a design decision until the user selects and asks to graduate one.

When asked to graduate a simple experiment, preserve the selection, remove abandoned variants and temporary controls, retain reusable fixtures or previews, and keep development surfaces out of production. Use `feature-delivery` when graduation becomes a substantial production feature.

## Boundaries

- Use synthetic, sanitized, or safely derived fixtures; do not put sensitive production data in stories or previews.
- Do not invoke Product Design image ideation or ImageGen unless the user explicitly requests generated images or image mockups.
- Do not create a detached option-picker application; the live project is the comparison surface.
- Do not require a formal spec, worktree, test-first cycle, commit, or production hardening for lightweight exploration.

## Common mistakes

- Comparing different data or states and attributing the result to the design.
- Adding a new preview framework without checking what the repository already uses.
- Building many superficial variants instead of a few meaningful directions.
- Calling a color or token swap a faithful, stretching, or divergent direction without changing the underlying system relationship.
- Treating a request for a concrete plan as permission to build ideas the user asked to narrow first.
- Calling temporary exploration variants production-ready.
- Leaving temporary switches, stories, fixtures, or styles in a production path after graduation.
