---
name: good-ui
description: Apply broadly useful visual and interaction design judgment when creating, implementing, reviewing, or substantially revising apps and websites, especially Bash.tv projects. Use for product screens, tools, dashboards, landing pages, prototypes, layout, hierarchy, typography, color systems, components, states, motion, responsiveness, accessibility, polish, and preventing generic agent-generated UI. Preserve the project's brand and tone rather than imposing a fixed aesthetic.
---

# Good UI

## Objective

Produce an interface that feels intentional, competent, and specific to its product. Use this skill as a design-judgment layer, not a fixed style or a heavyweight process. Preserve deliberate brand character and user direction. Establish functional competence before conspicuous art direction.

## Sequence of attention

Use this order for substantial UI work:

1. **Understand the surface.** Identify the recurring task, audience, real content, existing conventions, and whether the surface is operational, content-focused, marketing, or onboarding.
2. **Establish priority.** Decide what deserves first attention, what action is primary, what can remain secondary, and what should be removed or deferred.
3. **Compose before decorating.** Resolve the working surface, grid, shared edges, content widths, density, type hierarchy, and responsive reflow before styling isolated components.
4. **Establish the system.** Extend existing tokens and components where possible. Choose semantic color, type, spacing, shape, surface, and primitive behavior deliberately.
5. **Complete the behavior.** Implement relevant states, validation, feedback, focus, keyboard and touch paths, loading and empty states, overflow, and error recovery.
6. **Inspect and revise.** Render the actual result at representative sizes, exercise it, identify visible weaknesses and generic defaults, and make at least one correction pass.

Scale this sequence to the task. For an isolated change, preserve the surrounding system and focus on the relevant steps; do not turn a small fix into a redesign ceremony.

## Decision priority

When guidance conflicts, prioritize:

1. Explicit user direction and real project constraints
2. Functional correctness, truthful content, and the primary task
3. Hierarchy and comprehension
4. Interaction, accessibility, and responsive integrity
5. Product-specific visual character
6. Decorative detail

A lower-priority goal must not break a higher-priority one.

## Requirements

- Preserve existing functionality and intentional conventions unless the user requests a change.
- Make every visible control real, semantically appropriate, and complete in every state relevant to its behavior.
- Make the working surface primary in recurring-use applications; do not put a promotional composition ahead of the task without a current user need.
- Keep important actions and information usable across mouse, keyboard, touch, narrow screens, zoom, and realistic content.
- Prevent careless layout shift, focus loss, scroll jumps, clipped content, and state changes that erase context.
- Use real content when available. Do not invent factual-looking metadata, metrics, claims, activity, or features to fill a composition.
- Build practical accessibility into semantics, labels, focus, keyboard operation, contrast, and motion. Calibrate exhaustive conformance work to the project's reach and stakes.
- Inspect the rendered interface rather than inferring quality from code, component coverage, or theme coherence.

## Strong defaults

- Prefer hierarchy, alignment, proximity, and typography over cards, borders, dividers, fills, and nested containers.
- Make prominence proportional to utility, frequency, and consequence. Do not use display scale merely to manufacture drama.
- Use a small coherent system of semantic type, spacing, color, surface, and shape roles. Build color relationships in OKLCH and evaluate actual foreground/background pairs with APCA.
- Use readable typography, clearly distinct levels, sensible measures, resilient wrapping, and restrained eyebrow or uppercase treatment.
- Inspect the existing stack before creating primitives. Reuse proven behavior, preserve native semantics, and own the presentation rather than accepting accidental browser chrome or a library's demo aesthetic.
- Keep primary actions visible. Disclose repetitive secondary actions on hover only when they also have focus, selection, and touch paths.
- Use motion to explain change or provide feedback. Keep routine transitions interruptible, name animated properties, and use deliberate easing rather than mechanical linear motion.
- Spend strong color, scale, motion, elevation, and decoration selectively. Let a few decisions carry the character.

## Heuristics and exceptions

- Treat the defaults as context-sensitive judgment, not a mandate for minimal, neutral, spacious, or corporate design. Expressive, dense, playful, and unconventional interfaces can be excellent.
- Keep native platform presentation when it provides materially better behavior for the context, commonly some mobile pickers, or when custom treatment adds little value.
- Calibrate accessibility rigor to audience, permanence, reach, and stakes without permitting severe or easily preventable barriers.
- Break a guideline when the product clearly benefits, not because an implementation shortcut is convenient.
- Do not apply manual optical nudges unless the user explicitly requests pixel-level refinement or identifies a visible imbalance. Fix geometry, assets, typography, and layout first.

## Common failure modes

- Turning an operational tool into a landing page with a persistent hero, manifesto, tagline, or ceremonial first viewport.
- Translating a product category into a literal visual costume: reading as an editorial spread, developer tools as terminal theater, finance as glassy charts, or creative work as floating gradient blobs.
- Reaching reflexively for current agent style bundles: giant serif statements, italic accent words, rust or purple gradients, tiny uppercase metadata, colored punctuation, cultivated emptiness, universal pills, or rounded card grids.
- Using containers, borders, dividers, badges, or shadows as an easy substitute for hierarchy.
- Copying a component library's demo composition or leaving conspicuously default browser controls inside an otherwise authored interface.
- Rebuilding complex controls from generic elements and producing custom appearance with incomplete keyboard, focus, form, overlay, or touch behavior.
- Inventing copy, data, controls, or decorative sections merely to make the page look populated or designed.
- Treating the first coherent screenshot as completion without testing real content, intermediate widths, interaction states, or focus behavior.
- Continuing to decorate after hierarchy, character, and behavior are already clear.

## Reference routing

Read only the references relevant to the task:

| Reference | Read when |
| --- | --- |
| [Composition and visual direction](references/composition.md) | Establishing or revising hierarchy, layout, density, spacing, typography, application composition, or overall visual direction |
| [System and components](references/system-and-components.md) | Defining color, tokens, themes, gradients, surfaces, borders, shadows, radii, component anatomy, or primitive-library use |
| [Interaction and responsiveness](references/interaction-and-responsiveness.md) | Building states, validation, disclosure, overlays, feedback, motion, keyboard/touch behavior, responsive adaptation, or accessibility |
| [Polish and critique](references/polish-and-critique.md) | Handling truncation, layout stability, finishing details, restraint, slop prevention, or reviewing substantial work before delivery |

For a new app or broad redesign, begin with composition and system guidance, consult interaction guidance for the behaviors in scope, and always use the polish and critique reference before delivery. For an isolated change, load only the relevant reference.

## Completion gate

Before finishing substantial UI work:

- Render representative wide, intermediate, and narrow layouts when those sizes are in scope.
- Inspect the first viewport, focal point, shared edges, content width, density, wrapping, and control affordance at normal viewing size.
- Test realistic populated, empty, loading, error, overflow, and disabled states where relevant.
- Exercise every visible control. Verify keyboard order, visible focus, mutation focus recovery, touch access, and overlay dismissal.
- Confirm that changing or asynchronous content does not cause careless layout shift or erase user context.
- Remove fake controls, invented factual content, unjustified decoration, and treatments that could belong to an unrelated product.
- Make at least one correction pass after inspecting the rendered result.

Stop adding visual treatment when the hierarchy is immediately legible, important states are represented, the interface has coherent product-specific character, visible roughness is resolved, and further decoration would not improve comprehension or meaningful expression.
