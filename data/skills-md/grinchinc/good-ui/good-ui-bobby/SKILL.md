---
name: good-ui-bobby
description: Apply an opinionated personal UI implementation system on top of good-ui for web apps and product interfaces, including fully authored visual styling, real icon assets, 4px/8px spacing, standardized control sizes, edge clearance, expanded hit areas, complete interaction states, intentional focus behavior, continuity-preserving motion, shadcn-first primitives, production component galleries, temporary dev overlays, Git checkpoints, and optional OpenRouter-backed features. Use for new UI, substantial UI revisions, component-system work, interaction polish, or in-product design exploration.
---

# Good UI Bobby

Use this skill as a personal execution layer on top of `good-ui`. Keep `good-ui`'s product-specific judgment, restraint, accessibility, and existing-system respect. Apply the defaults here when the project does not provide a stronger constraint.

## Precedence

Resolve decisions in this order:

1. Explicit user direction and real project constraints.
2. Functional correctness, accessibility, platform conventions, and existing product language.
3. `good-ui`'s general design guidance.
4. The defaults in this skill.

Break a default when it would harm usability, accessibility, performance, or the product's established language. Do not invent a new visual system merely to satisfy a rule.

## Bobby absolutes

- Own the appearance of every visible UI element. Do not ship unstyled browser controls, library demo defaults, placeholder styling, generic surfaces, or accidental native chrome. Customize the presentation through the project's tokens and visual language while preserving reliable native semantics and behavior.
- Use real icons only. Never use Unicode glyphs, emoji, ASCII art, or text symbols such as `+`, `x`, `->`, or `check` as visual icon substitutes. Use an established icon component, inline SVG, local SVG asset, or platform icon system instead.
- Treat unintended focus as a high-severity defect. Keep visible focus for keyboard and required focus transitions, but do not steal focus, autofocus casually, add `tabindex` to noninteractive wrappers, or show keyboard focus styling for an ordinary pointer interaction when `:focus-visible` can distinguish the input modality.
- Keep content and controls deliberately inset from component boundaries. Do not let text, icons, hit areas, focus rings, or nested surfaces read as flush against an edge unless an explicit edge-to-edge variant calls for it.

## Route the work

Read only the reference needed for the task:

| Task | Reference |
| --- | --- |
| Grid, control sizing, hit areas, states, motion, or shadcn | [Interaction defaults](references/interaction-defaults.md) |
| Tokens, primitives, component APIs, component gallery, or dev overlay | [Component system](references/component-system.md) |
| Git setup, checkpoints, environment variables, or OpenRouter | [Project workflow](references/project-workflow.md) |

For a new product or substantial redesign, read all three references before implementation.

## Working sequence

1. **Orient.** Inspect the existing stack, routes, tokens, components, dependencies, Git state, and real data. Preserve intentional work and avoid unrelated rewrites.
2. **Establish the system.** Define or extend tokens and reusable primitives before composing a broad surface. Use production components, not screenshot-only approximations.
3. **Build the surface.** Implement the primary task first. Give every interactive element a visible box, an adequate hit box, a complete state model, and a meaningful motion path.
4. **Protect the edges.** Check the clearance between every bounded surface and its first visible content on all sides. Treat the inset as component anatomy, not a usage-site patch.
5. **Expose the system.** For substantial work, create a dev-only component review surface that imports the actual production components and shows their variants and states in isolation.
6. **Inspect and correct.** Render representative wide, intermediate, and narrow layouts. Exercise mouse, touch, keyboard, focus recovery, reduced motion, loading, empty, error, and overflow states as relevant. Make at least one correction pass.
7. **Checkpoint.** Keep temporary exploration controls gated or remove them. Commit meaningful milestones when the repository is under active development.

## Completion gate

Before finishing substantial UI work, confirm:

- Spacing follows the 4px base grid and 8px rhythm unless a documented constraint requires otherwise.
- Visual control sizes use the 24/32/40/48/56px scale; effective hit targets are never reduced just to preserve a small visual shape.
- Interactive elements have appropriate hover, focus-visible, pressed, selected, disabled, loading, and error states.
- State changes preserve spatial identity and animate when motion improves comprehension; reduced-motion preferences are respected.
- The component review surface shows real components, not parallel recreations.
- No dev overlay, test data, fake control, or secret is accidentally treated as production behavior.
- Every visible element has authored project-appropriate presentation; no default browser, library-demo, or fake-icon treatment remains.
- Text and icons have deliberate edge clearance; no bounded control, field, menu, card, or nested surface feels cramped against its boundary.
- Focus appears because of a real keyboard or context change, not because of incidental pointer events, mount timing, hover, or focus theft.
- Keyboard order, touch access, focus recovery, content resilience, and responsive behavior have been checked.
