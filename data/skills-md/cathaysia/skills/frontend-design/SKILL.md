---
name: frontend-design
description: Design, implement, or review production frontend interfaces with a clear visual direction, strong usability, accessible interaction, responsive behavior, and disciplined use of the existing design system. Use whenever the user asks to create, redesign, polish, or review a web page, component, dashboard, form, or application; translate a mockup into code; improve visual hierarchy or styling; or make a frontend feel less generic—even when the request is framed as a component refactor. Do not use for backend-only work or purely mechanical frontend changes with no UI decision.
---

# Frontend Design

Create interfaces that feel intentional, coherent, and ready for real use. Balance visual character with product clarity: a marketing page may be expressive, while an operations dashboard may earn its quality through density, restraint, and speed.

## Choose the Working Mode

Match the response to the user's task:

- **Build or redesign:** inspect the existing code and design language, choose a direction, implement working UI, and verify it.
- **Review:** identify the highest-impact problems first, explain why they matter, and propose concrete replacements.
- **Design guidance:** give a specific layout, hierarchy, component, and interaction recommendation rather than a list of abstract principles.

Do not turn a focused request into an unsolicited full redesign. Ask a question only when a missing constraint would materially change the result; otherwise make a reasonable choice and state it briefly.

## Design Workflow

Follow this order before polishing details:

1. **Understand the job:** identify the audience, primary task, content, primary action, device context, and relevant constraints.
2. **Inspect the local system:** find existing components, tokens, typography, icon libraries, layout patterns, and neighboring screens. Preserve established conventions unless the user explicitly wants a new direction.
3. **Choose one direction:** describe the intended tone in one sentence and make the layout, type, color, imagery, and motion support it.
4. **Establish hierarchy:** decide what users should notice first, what belongs together, and what can remain secondary.
5. **Implement from structure outward:** semantics and content first, then layout, responsive behavior, states, interaction, and visual refinement.
6. **Verify the result:** check functionality, keyboard use, focus, contrast, responsive behavior, overflow, and loading/empty/error states.

## Make the Design Intentional

Commit to a coherent point of view instead of assembling fashionable fragments. Distinctive does not always mean decorative: precision, unusual information architecture, strong typography, or excellent density can provide character.

Avoid generic AI defaults unless the product context genuinely calls for them:

- interchangeable card grids for every section
- purple-on-white gradients, decorative blobs, and glow effects without purpose
- oversized hero text that crowds out the product's actual content
- excessive pills, rounded rectangles, shadows, and glass effects
- random gradients, emoji used as interface icons, or mixed icon styles
- animation scattered across every element rather than focused on meaningful transitions

For a new visual direction, choose a memorable idea appropriate to the product—editorial, industrial, playful, refined, technical, quiet, or another clear tone—and execute it consistently. For an established product, coherence with the existing system usually matters more than novelty.

## Build Hierarchy Before Decoration

Use composition, alignment, spacing, scale, and contrast to communicate structure before adding borders and effects.

- Give the primary task and primary action the strongest emphasis.
- Group related content through proximity and alignment before adding containers.
- Use cards for genuinely self-contained surfaces, not as the default wrapper for every section.
- Avoid nested cards by default. Use spacing, dividers, headings, or a subtle surface change inside a card unless the nested item is independently actionable and semantically distinct.
- Match density to the task. Operational tools can be compact; onboarding and marketing flows usually need more breathing room.
- Keep a stable alignment system. Small arbitrary offsets make an interface feel improvised.

## Use Typography and Copy Deliberately

- Keep headings concise and scannable, but retain supporting copy when it resolves ambiguity, sets expectations, or helps users decide.
- Use the existing type scale and font family in established products.
- In greenfield work, choose typography that reinforces the visual direction while keeping body text highly readable.
- Limit the number of font families, sizes, and weights. Create hierarchy through a small, repeatable scale.
- Avoid placeholder marketing language when real product language can be inferred from the task.

## Reuse the Design System

Before creating a UI primitive, check whether the project already provides it.

- Prefer existing components for dialogs, menus, forms, tables, tooltips, notifications, and other behavior-heavy elements.
- Use library variants, tokens, slots, and theme APIs before custom wrappers or deep CSS overrides.
- Extend an existing component when the new behavior is genuinely shared; keep one-off composition local.
- Avoid `!important`, brittle descendant selectors, and hardcoded internal library selectors. If an override is unavoidable, keep it narrow and document why.
- Do not add a new dependency when the current stack can solve the problem cleanly.

## Treat Color as a System

- Use semantic tokens for background, surface, text, border, accent, success, warning, and danger roles.
- Reserve brand or accent color for meaningful emphasis instead of distributing it evenly across the page.
- Do not rely on color alone to convey state.
- Check text and control contrast, including disabled and muted content.
- If dark mode exists, verify every custom surface, border, shadow, chart, and state color in both themes.
- Prefer extending the token system over scattering hardcoded color values.

## Choose Actions and Status Indicators by Clarity

Icons save space only when users can recognize them reliably.

- Use icon-only buttons for familiar, repeated actions such as close, search, refresh, or overflow when context makes the meaning clear.
- Use visible text for primary actions, uncommon actions, and consequential actions whose meaning should not be guessed.
- Give every icon-only control an accessible name such as `aria-label`; a `title` attribute alone is not sufficient. Add a tooltip when it improves discoverability.
- Keep touch targets comfortably large even when the visible icon is small.
- For destructive or irreversible actions, provide clear wording and confirmation when recovery is difficult.

Status must remain understandable without color:

- Prefer icon plus concise text when the status may be ambiguous or important.
- In a dense, repetitive table, an icon-only status can work when it has an accessible name and tooltip and the icon mapping is consistent.
- Use progress indicators for active work, not a static “pending” icon that implies progress.
- Keep status vocabulary and icon mapping consistent across the product.

## Design Every State

For each asynchronous data surface, define the loading, empty, error, and populated states. Also consider disabled, partial, stale, and success states when the workflow needs them.

- **Loading:** preserve layout where possible. Use a skeleton when the content shape is predictable and a spinner for short, localized work.
- **Empty:** explain why nothing is shown and offer the next useful action when one exists. Search with no results and a brand-new account often need different empty states.
- **Error:** use human-readable language, preserve user input, and provide retry or recovery when possible.
- **Success:** confirm completed actions without interrupting the next task.

Choose feedback based on persistence and actionability:

| Situation | Preferred pattern |
|---|---|
| Brief action confirmation | Toast or transient message |
| Field-specific validation | Inline message next to the field |
| Recoverable section failure | Inline error state with retry |
| Persistent page-level issue | Banner or alert |
| Destructive action requiring a choice | Dialog or confirmation flow |

Do not place important recovery instructions only in an auto-dismissed toast.

## Make Interaction Accessible and Responsive

- Use semantic HTML before adding ARIA. Preserve labels, names, roles, and relationships.
- Ensure all interactive elements work with a keyboard and have visible focus states.
- Keep logical focus order; manage focus when dialogs, drawers, and menus open or close.
- Do not hide essential information exclusively behind hover.
- Respect reduced-motion preferences and animate properties that are inexpensive to render.
- Use motion to explain change, continuity, or feedback—not as ambient decoration everywhere.
- Design small screens as a deliberate composition. Reflow, prioritize, collapse, or move secondary content instead of merely shrinking the desktop layout.
- Test long text, localization expansion, zoom, narrow widths, and overflow-prone content such as tables and code.

## Keep the Interface Real

When implementing UI, build functioning interactions rather than a static impression of them.

- Wire primary controls, validation, menus, dialogs, and state transitions.
- Do not leave nonfunctional buttons or fake links unless the user explicitly asked for a visual prototype; label prototype limitations clearly.
- Use realistic content shapes and edge cases so the layout is tested, not flattered by ideal placeholder data.
- Preserve the project's architecture and state-management conventions unless changing them is part of the request.

## Review and Response Pattern

For a design or code review, report findings in this order:

1. usability or accessibility blockers
2. hierarchy and task-flow problems
3. responsive, overflow, and missing-state problems
4. inconsistency with the design system
5. visual polish opportunities

Tie each finding to a specific element or code location when available. Explain the user impact and give a concrete correction; avoid vague feedback such as “make it cleaner.”

For an implementation, briefly state the chosen direction, complete the requested UI, and report the relevant verification. Let the finished interface carry the design argument rather than preceding it with a long essay.

## Final Check

Before handing off, confirm:

- the primary task and action are immediately clear
- the interface has one coherent visual direction
- hierarchy works without excessive containers or decoration
- components, tokens, and icons match the local system
- actions and statuses are understandable without guessing or relying on color alone
- loading, empty, error, and success behavior fit the workflow
- keyboard, focus, contrast, reduced motion, and touch targets are covered
- narrow screens, long content, and overflow have been considered
- implemented controls actually work
