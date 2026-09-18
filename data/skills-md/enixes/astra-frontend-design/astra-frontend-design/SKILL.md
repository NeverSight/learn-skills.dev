---
name: astra-frontend-design
description: Design, implement, or visually refine a web interface when the visible experience is a primary deliverable. Use for greenfield UI, redesigns, reference matching, and visual polish; skip backend-only work and behavior-only frontend changes.
metadata:
  short-description: Astra-native frontend design and visual QA
---

# Astra Frontend Design

Build a coherent, distinctive interface that serves the product, fits the codebase, and survives inspection in a real browser. Carry the requested frontend work through implementation and visual verification unless the user asks only for a plan or critique.

The user's brief and the repository's established product constraints take precedence over this skill. Treat the guidance here as judgment criteria, not a house style. A familiar pattern is acceptable when it is the right choice for the subject and workflow.

## Route the task

Read only the references the current task needs.

| Task | Reference |
| --- | --- |
| Landing page, portfolio, editorial, brand, or expressive site | [art-direction.md](references/art-direction.md) |
| Dashboard, SaaS product, admin surface, form, or operational tool | [product-ui.md](references/product-ui.md) |
| Existing interface redesign or modernization | [redesign.md](references/redesign.md) |
| Screenshot, Figma frame, image, or named site as a reference | [reference-to-code.md](references/reference-to-code.md) |
| Prominent animation, scroll behavior, or interaction choreography | [motion-and-interaction.md](references/motion-and-interaction.md) |
| Review, polish, accessibility audit, or final verification | [quality-gates.md](references/quality-gates.md) |
| A reusable prompt rather than implementation | [prompt-recipes.md](references/prompt-recipes.md) |
| Compare skill quality across models or revisions | [evaluation.md](references/evaluation.md) |

## Establish the design truth

Inspect the target route, nearby components, global styles, assets, and dependency manifest before changing visible UI. Reuse the project's framework, component primitives, tokens, icon family, and interaction conventions unless the task explicitly calls for a new direction.

Infer a compact design read from the available context:

- subject, audience, and the screen's primary job;
- visual character and one memorable idea;
- information density and motion level;
- content, behavior, brand, and accessibility constraints that must survive.

Proceed on reasonable assumptions. Ask one focused question only when different answers would materially change the product, brand, or interaction model. Do not stop after describing what could be built when the request authorizes implementation.

For a multi-screen product or ongoing redesign, preserve durable product facts separately from visual direction. If the repository lacks an equivalent, use [PRODUCT.template.md](assets/PRODUCT.template.md) and [DESIGN.template.md](assets/DESIGN.template.md) as starting points. Do not create process documents for a small one-off change unless they will prevent real drift.

## Shape before styling

Decide hierarchy, content order, responsive behavior, and interaction states before choosing decorative details. Give each surface one clear visual thesis. Spend expressive complexity where it supports that thesis and keep the rest disciplined.

Generated-looking conventions are warning signs only when they are unexamined defaults. Examples include repeated equal cards, decorative gradients, universal pill shapes, an eyebrow above every heading, arbitrary monospace labels, interchangeable copy, and motion on every element. Keep any of them when the brief genuinely calls for them; otherwise choose a more specific solution grounded in the subject.

Use truthful content. Do not invent customer names, testimonials, performance claims, precise metrics, or product capabilities. Clearly mark sample data when realistic data is needed to demonstrate a state.

## Implement the real experience

- Build the useful screen first. Do not substitute a marketing shell when the user asked for an app, tool, game, or dashboard.
- Make expected controls and flows functional. Include relevant loading, empty, error, success, disabled, and overflow states.
- Prefer real project assets or relevant images over decorative placeholders. Create or retrieve assets only when they materially improve the result and the available tools permit it.
- Check the dependency manifest before importing a package. Add a dependency only when it provides needed capability that the current stack does not already offer.
- Keep semantic HTML, keyboard access, visible focus, readable contrast, text reflow, reduced-motion behavior, and responsive layout in the implementation rather than in a detached checklist.

## Finish with a visual loop

Run the smallest relevant build, lint, and behavior checks. Start the app when needed, capture the actual interface at representative desktop and mobile widths, and inspect the pixels rather than trusting the source code. Check hierarchy, framing, content fit, alignment, contrast, interaction feedback, and console errors. Fix visible or functional defects and repeat the affected checks until no material issue remains.

Use the project's existing browser or end-to-end tooling when available. Do not add a large test stack solely to take screenshots. Calibrate verification to the change: a token tweak needs less coverage than a responsive page or animated interaction.

In the handoff, lead with what is now usable. Mention the chosen visual direction and verification evidence briefly; do not narrate every design deliberation unless the user asks.

## If paired with agent orchestration

Keep this skill's design and implementation judgment with the capable frontend implementer. On a bounded, browser-testable build, a smaller coordinator may give one Astra worker the original product brief and references, then test the running result and return screenshots plus concrete defects to the same worker thread. The coordinator should not replace the worker's visual judgment with a prescriptive layout recipe. Use direct Astra or an Astra-led plan when quality is paramount, the work is ambitious, or acceptance is difficult to test. Delegate only if the user and environment permit it; allocate essential checks explicitly.

## Research basis

This skill is an original Astra-oriented synthesis. For provenance and the adaptation decisions, see [research-basis.md](references/research-basis.md).
