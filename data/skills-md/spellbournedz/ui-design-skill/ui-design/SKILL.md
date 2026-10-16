---
name: ui-design
description: Design, build, redesign, polish, or review product UI with a product-specific visual direction and a high craft bar. Use for frontend pages, components, dashboards, forms, responsive web surfaces, design-system work, screenshot or Figma-driven implementation, UI cleanup, interaction and animation decisions, or whenever an interface risks looking generic, templated, or AI-generated. Skip for backend-only work or mechanical frontend changes that do not materially affect the user experience.
---

# UI Design

Act as a product-minded design engineer, not a generic interface generator.

The goal is not to make a screen merely look polished. Make it feel intentional, specific to the product, coherent with the existing system, and complete across states and breakpoints.

For utility UI, default to minimum useful copy, consistent spacing by role, and grouped actions by scope. Keep design reasoning and implementation notes in the work process, not as text on the product screen.

## 1. Establish design authority

Follow applicable project instructions, including `AGENTS.md` and `CLAUDE.md`, throughout. The order below resolves visual decisions; it does not override project requirements.

Before changing UI, use this order of authority:

1. User-provided Figma, screenshots, specifications, or explicit visual instructions.
2. Existing project design system, tokens, components, and visual language.
3. Product patterns already used consistently in the codebase.
4. Project documentation such as `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, component docs, or frontend conventions.
5. This skill's defaults when no stronger direction exists.

Do not replace a provided design with your own taste unless the user explicitly asks for redesign or critique.

If the project defines a fallback design system, use it. If it does not, do not silently introduce a new one just because it is familiar.

## 2. Understand the product before styling

Before material UI work, determine from the brief, code, docs, screenshots, or existing product:

- what the product does in plain language;
- who the primary user is;
- the main task on the current surface;
- the first decision or action the user should understand;
- what success looks like;
- important empty, loading, error, disabled, and recovery states;
- the product temperament: utilitarian, calm, premium, playful, dense, editorial, technical, or another specific direction;
- vocabulary already used by the product;
- components and tokens that should be reused.

Infer these from available context when the answers are clear. Do not turn obvious context into ceremonial discovery questions.

## 3. Choose a visual thesis when direction is missing

If no design direction is already specified, form a compact visual thesis before implementing substantial new UI.

A useful thesis covers:

- visual character;
- dominant hierarchy principle;
- intended density;
- typography behavior;
- surface, border, and elevation behavior;
- motion temperament;
- at most one memorable visual idea.

Example:

`Calm utilitarian finance UI with dense information, strong numeric hierarchy, flat surfaces, restrained borders, and motion used only to explain state changes.`

Do not begin with effects such as gradients, glass, large radii, or shadows. Begin with the product and task.

For a significant **new visual direction**, expressive landing page, onboarding experience, branded surface, or redesign of generic UI, read [references/creative-direction.md](references/creative-direction.md) before committing to that thesis. Privately explore different product-grounded concepts, test them against task clarity, design authority, responsiveness, accessibility, and engineering cost, and choose the simplest meaningful direction. A distinctive concept is optional when familiar utility UI better serves the task.

For faithful Figma implementation, routine components, bug fixes, or UI cleanup that does not call for a new direction, do not run concept exploration. Respect the provided design instead.

## 4. Run the anti-slop gate

Read [references/anti-slop.md](references/anti-slop.md) before accepting a substantial new visual direction or when reviewing UI that feels generic.

A useful test: if a visual decision could move unchanged into several unrelated SaaS products, it may be a template habit rather than a product decision.

Do not mechanically ban popular styles. Cards, gradients, glass, pills, bento layouts, dark themes, serif type, bold radii, and expressive motion can all be correct when the product or design system gives them a reason to exist.

## 5. Structure before decoration

Resolve these in roughly this order:

1. information hierarchy;
2. grouping and proximity;
3. alignment;
4. spacing rhythm;
5. content density;
6. primary and secondary actions;
7. responsive behavior;
8. interaction and system states;
9. accessibility;
10. visual expression.

Do not use decoration to compensate for unclear structure.

### Define a compact layout contract

Before adding markup, reuse or choose the spacing roles, field structure, and action locations for the changed surface. Apply them across sibling components instead of styling each block independently. This is a small implementation decision, not a new design-system project or a user-facing explanation.

Use existing spacing tokens first. If none exist, a compact fallback is `4 / 8 / 16 / 24 / 32` px with this role mapping:

| Relationship | Default |
| --- | --- |
| Label, control, and supporting content within a field | 8 px |
| Adjacent buttons within an action group | 8 px |
| Related rows within a section | 16 px |
| One complete field to the next field | 24 px |
| Panel padding and header-to-body spacing | 24 px |
| Distinct sections | 32 px |

These are fallback values, not overrides of supplied designs. Equal roles get equal tokens; different hierarchy levels can have different distances. Use one panel inset so headings, fields, and action rows share alignment. Responsive density may change the mapping at a breakpoint, but not arbitrarily from one sibling to another.

### Keep fields structurally consistent

- Treat label, optional help, control, counter, validation, and attachment actions as one field group.
- Use the same parent `gap` between complete field groups. Keep each field's internal spacing inside its wrapper; do not tune the next field with one-off margins.
- Include upload previews and remove/replace actions inside the attachment field. Include counters and errors inside their field, rather than as independently spaced rows.
- Keep the same gap from the end of a complete field to the next label whether the control is an input, upload, or textarea. Check rendered spacing, not only token names: line-height, margins, and component padding can add hidden space.

### Give actions a predictable home

- Group actions that operate on the same object or workflow in one compact panel or toolbar when they fit. Do not distribute them among a header, sidebar footer, and canvas footer just to fill space.
- Choose the location by scope: document actions in the document toolbar, view controls beside the view, and field actions inside the field. Consolidation should preserve this relationship.
- Give the current task's primary action clear priority; keep secondary actions alongside it with quieter styling. Separate destructive actions within the group when needed to prevent mistakes.
- When width runs out, reflow the group or use an accessible overflow menu for secondary actions. Preserve ordering, scope, and access to the primary action across breakpoints.

### Allocate screen space to the task

- Give the main task the working area it needs. In an editor, size the preview and editing controls for useful reading and manipulation before allocating space to supporting chrome.
- Size utility headers, toolbars, and side panels to their content and controls. Reconsider a separate strip or panel that holds only one hint or secondary action; merge it into an appropriate existing region when scope allows.
- Check what remains usable after fixed and sticky regions consume space, especially at short viewport heights and narrow widths. Avoid a layout where the task requires scrolling mainly because its chrome occupies the viewport.
- Preserve whitespace that supports focus, grouping, or readability. Do not fill spare room with copy, stretch controls, or shrink accessible targets merely to make the screen look full or compact.

## 6. Build components for real behavior

Prefer established project components over bespoke replacements.

When creating or changing components:

- support realistic content ranges, not only demo data;
- include hover, focus-visible, active, disabled, loading, error, success, and empty states where relevant;
- preserve semantic HTML and keyboard behavior;
- keep touch targets appropriate for the platform;
- express differences through existing tokens and component APIs when possible;
- do not hand-roll mature primitives when an established project dependency already solves the problem;
- do not add a dependency for a trivial behavior that CSS or existing code already handles well.

When several component APIs are plausible, prefer the smallest coherent system.

Use one geometry per component role and size variant: matching buttons share height and padding, matching inputs share control height and internal padding, and icons in the same context share size and alignment. Reuse project size tokens or define the few local values needed alongside the existing spacing contract. Multiline controls, touch variants, and other functional exceptions may differ; express the reason through a shared variant rather than a one-off CSS adjustment.

## 7. Treat typography as structure

- Follow the project's type system when it exists.
- Use one size, weight, and line-height combination per text role. Repeated labels, helper text, and section titles should not acquire local styles without a functional hierarchy change.
- Do not add a typeface merely to make the interface feel designed.
- Prefer sentence case unless the product language says otherwise.
- Create hierarchy through type size, weight, spacing, contrast, and placement before adding extra labels.
- Avoid decorative eyebrow labels and arbitrary monospace metadata.
- Keep long-form text readable.
- For data-heavy products, handle numeric alignment, units, precision, and tabular figures deliberately.

## 8. Use color, surfaces, and elevation semantically

- Use semantic tokens when available.
- Color should communicate hierarchy, state, brand, or meaning.
- Borders should separate or group something, not outline every rectangle by reflex.
- Shadows should communicate elevation or focus, not decorate every container.
- Radius should reflect component role and product language rather than one universal value.
- Do not create a second near-identical neutral palette inside an existing system.
- Keep state colors consistent across surfaces.

## 9. Design responsive behavior, not just smaller screenshots

- Preserve the primary task and important context across breakpoints.
- Do not simply stack every desktop panel vertically and call it mobile.
- Decide what reorders, collapses, becomes sticky, moves into a sheet or menu, or can disappear.
- Avoid controls that are unnecessarily full-width on large screens or unusably compressed on small screens.
- Test realistic long labels, validation messages, empty values, and dense content.

## 10. Use motion as feedback and explanation

Before adding animation, ask:

1. Does the change need animation?
2. What does the motion explain or confirm?
3. How often will the user see it?
4. Can CSS handle it simply?
5. Does it respect reduced-motion preferences?

Prefer immediate feedback for direct manipulation and short, restrained transitions for frequent actions. Reserve expressive motion for rare or meaningful moments.

Avoid:

- `transition: all`;
- animating every card or section on page load;
- repeated fade-and-slide reveals without a product reason;
- slow animation on high-frequency actions;
- motion that delays keyboard workflows;
- scale-from-zero entrances for ordinary UI;
- animation whose only purpose is to make the screen feel more designed.

## 11. Treat copy as part of the interface

Use product vocabulary rather than implementation vocabulary.

For each visible text block, ask: **what decision, action, constraint, or meaningful state would become unclear if this disappeared?** If there is no concrete answer, omit it. Do not replace deleted filler with an icon, tooltip, badge, or another explanatory layer by reflex.

- CTA labels should name the real action.
- Keep the same action name across buttons, results, toasts, and history when possible.
- Empty states should help the user move forward.
- Error messages should explain recovery when possible.
- Avoid marketing language inside utility surfaces unless the product requires it.
- Do not stack an eyebrow, heading, and subtitle when they repeat one context. For example, a selected "Cover" item rarely needs "Card fields / Cover / General details and cover" above its form; retain only the title needed for orientation.
- Do not narrate obvious mechanics with persistent copy such as "Fill in the fields beside the preview" or "Changes appear immediately in the card" when the interaction already makes this clear.
- Show non-obvious instructions where they are needed: a format constraint beside its field, first-use help on demand, or a state message when that state occurs. Use accessible help controls rather than hover-only tooltips for essential guidance.
- Preserve field labels, accessible names, recovery instructions, consequential storage limitations, and warnings needed to prevent mistakes or data loss. If sample-data provenance or a locked design affects a decision, communicate it once at the relevant point, not in repeated boilerplate across panels.
- Do not add filler headings, subtitles, or status rows only to balance a composition. A sparse panel does not need explanatory prose to look finished.

If the project has a dedicated writing skill, use it for longer copy while preserving the product vocabulary established here.

## 12. Keep implementation disciplined

While coding:

- reuse existing tokens and primitives;
- preserve architectural conventions unless they prevent the requested result;
- keep visual constants centralized where the project already centralizes them;
- avoid repeated magic numbers;
- do not refactor unrelated code under the label of UI polish;
- do not replace working interaction behavior merely to simplify styling;
- keep DOM structure semantic and reasonably shallow;
- verify that visual work does not regress forms, loading, errors, keyboard use, or mobile behavior.

## 13. Visually verify material UI changes

Do not stop at a successful build when rendering or browser inspection is available.

For material UI changes:

1. render the changed surface;
2. inspect a primary desktop width;
3. inspect a realistic mobile width;
4. exercise relevant realistic-content scenarios below and compare with source Figma or screenshots when provided;
5. identify the most visible weaknesses and any violations of the layout contract, component geometry, or task-space allocation;
6. fix in-scope issues and reinspect the affected scenarios;
7. run [references/ui-review.md](references/ui-review.md).

Check scenarios relevant to the changed surface using actual product content or representative examples, not only short demo strings:

- **Long content:** a long title, label, URL, or user value; wrapping or truncation preserves meaning, alignment, and access to actions.
- **Empty and invalid content:** blank fields and visible validation errors; field-group spacing stays consistent, guidance remains attached to its field, and recovery controls stay usable.
- **Attachments:** before and after an image upload where supported; preview dimensions, replacement/removal controls, and neighboring fields remain coherent.
- **Constrained space:** the same content at a narrow width and short viewport height; main work remains usable, controls do not collide, and grouped actions stay reachable.

Treat applicable checks as acceptance criteria. For build or polish tasks, correct observed violations within the authorized scope before claiming completion; fixing only three prominent issues does not waive remaining failed checks. For review-only tasks, report failures and concrete corrections without changing the product.

If rendering or browser inspection is unavailable, perform the checks that are possible and state which visual checks remain unverified. Do not claim a visual review from a successful build alone.

Prefer one meaningful correction pass over adding more decoration.

## 14. When existing UI looks AI-generated

Do not repaint it first. Diagnose in this order:

1. hierarchy;
2. excessive containerization;
3. spacing rhythm;
4. typography;
5. primary action clarity;
6. repetitive component geometry;
7. decorative effects;
8. generic copy;
9. purposeless motion.

Fix the earliest structural problem that explains the largest amount of visual noise.

## 15. Final response

For build tasks, summarize meaningful UI decisions and important tradeoffs rather than narrating every CSS edit.

For review tasks, order findings by impact. Each finding should identify:

- what is wrong;
- where it appears;
- why it hurts the experience;
- the concrete correction.
