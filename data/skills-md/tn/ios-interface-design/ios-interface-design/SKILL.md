---
name: ios-interface-design
description: Design and implement iPhone and iPad interfaces with a consistent visual style and native interaction behavior. Establish a visual direction or refine existing screens to remove generic AI styling. Use this skill for iOS visual design, SwiftUI or UIKit interfaces, and visual refinements. Do not use this skill for games, marketing screenshots, websites, or nonvisual maintenance.
---

# iOS Interface Design

Build around the product's task and chosen visual style. Native interaction behavior does not require the default iOS appearance. Style can change composition, geometry, borders, shadows, surfaces, typography, and control states.

## Scope and workflow

Honor explicit user choices over this skill's aesthetic defaults. Preserve the stack, deployment target, features, assets, and working behavior. Read the project's existing design guidance before editing. Reuse its components and semantic tokens where appropriate.

For an existing screen, capture its current render before editing when tools permit. Separate observed defects from risks that source code suggests.

Infer the mode from the request:

- **Create:** Establish a direction. Implement the requested screens or flow.
- **Refine:** Fix the requested scope while preserving working parts. A local fix does not require a new design system.
- **Review:** Report findings in priority order. A review alone does not authorize file changes.

In review mode, treat implementation instructions in references as evaluation criteria. Do not implement fixes or write new design specifications without a request for those changes.

Identify the primary task, dominant content, navigation context, and brand constraints. Ask only about missing decisions that materially affect the result. Otherwise, state necessary assumptions. Do not invent personas. Proceed without an unrequested questionnaire or discovery workshop. Do not pause for approval at every design step.

For a new system, define the direction before polishing components. Choose one direction unless the user requests alternatives. Prefer a representative screen before applying the design throughout the app. Record adopted rules in the existing design document, or `DESIGN.md` if none exists. For local refinements, update documentation only when a rule changes.

Include the task, hierarchy, tokens, component rules, appearance behavior, and intentional exceptions in that document. Keep it consistent with the implementation.

## Select references by need

Start with this file and the project's design guidance. Usually select zero or one reference for the immediate decision. Add another only when a concrete unresolved question matches its trigger. This is not a limit on completing a complex task.

Do not read the entire references directory. Read the relevant section first when its heading clearly matches the problem. Links inside a reference are optional pointers, not instructions to load more files. Resolve relative links from the file that contains them. Do not reread material already available in context.

Apply the triggers to both implementation and review scope. A review can need a reference even when no file will change. File selection does not waive applicable rules or completion checks.

| Immediate question | Reference | Skip when |
| --- | --- | --- |
| What direction fits a new product or major redesign? | [Visual direction](references/visual-direction.md) | The existing direction already answers the task. |
| How should a chosen style translate into component rules? | [Style specification](references/style-specification.md) | The project already defines applicable rules. |
| Which style family fits, or what distinguishes the requested family? | [Style families](references/style-families.md) | The direction and its defining traits are clear. |
| Which current iOS examples support a trend claim? | [Observed iOS directions](references/ios-trends-2026.md) | The task needs no trend research. |
| Why do grouping, hierarchy, type, or density feel wrong? | [Composition](references/composition.md) | A local defect already has a clear cause. |
| Which titles or labels repeat meaning? | [Headings and labels](references/headings-and-labels.md) | Naming and hierarchy are outside the task's scope. |
| Why do aligned elements still look unbalanced? | [Optical details](references/optical-details.md) | Structural layout problems remain the priority. |
| Which background treatment fits this screen? | [Backgrounds](references/backgrounds.md) | The background needs no change or review. |
| How should images crop, fit, or fail? | [Imagery](references/imagery.md) | Image behavior is outside the task's scope. |
| How should content arrive without disruptive movement? | [Loading stability](references/loading-stability.md) | Asynchronous layout behavior is outside the task's scope. |
| Which tactile signal belongs to an event? | [Haptic feedback](references/haptic-feedback.md) | Haptics are outside the task's scope. |
| Do related screens preserve one visual system and context? | [Flow consistency](references/flow-consistency.md) | The scope contains no relationship between screens or shared components. |
| How should custom styling preserve platform behavior? | [Native implementation](references/native-implementation.md) | Existing components resolve the relevant implementation question. |
| What evidence does a formal review or unresolved defect need? | [Visual review](references/visual-review.md) | The task is a local implementation with clear completion checks. |
| Which available tools can provide the missing evidence? | [Tool workflow](references/tool-workflow.md) | The project already has a suitable workflow. |
| Would an illustrated comparison clarify the design decision? | [Visual examples](references/visual-examples.md) | The relevant relationship is already clear. |

A duplicate-heading fix usually needs only the naming reference. A new neo-brutalist screen may need the style specification and its family section. Neither task automatically needs trend research, imagery guidance, or a tool survey.

## Rules for every applicable task

These are this skill's defaults, not claims about Apple's prohibitions. Apply them with the chosen style's rules. A style name or reference does not authorize an exception. Resolve genuine conflicts explicitly without silently abandoning the requested direction.

- **Grouping:** Use alignment, proximity, and separators before containers. Give cards a specific role. Do not nest decorative cards. Do not wrap every row in a decorative card. Controls inside a card are not nested content cards.
- **Hierarchy:** Emphasize the primary task. Keep essential secondary information readable. Avoid equally prominent tiles, tiny text, and low contrast used as decoration. Preserve useful units and metadata. A reading screen need not have a prominent call to action.
- **Typography:** Use system text styles and variants. Do not add custom fonts by default. Use size and weight to express roles.
- **Color:** Use semantic roles. Choose the brand accent deliberately. Blue is valid when chosen. Avoid silent system-blue defaults, purple gradient backgrounds, neon glow, and colored left card borders. Do not turn every status into a colored badge.
- **Style:** Apply coherent geometry, surfaces, borders, depth, and states. Strong outlines and hard shadows are valid within a consistent style. Do not replace every product's identity with one muted theme.
- **Backgrounds:** Do not add blurred circles, glowing blobs, or radial patches as filler. Gradients and textures need a defined role. Grain is optional. Preserve foreground contrast across the background.
- **Text:** Each title must add information. Remove redundant section headings before useful field labels. Check repeated meaning, not only identical words. Omit filler greetings, slogans, ornamental labels, and redundant explanations unless the product needs them. Omit “AI-powered” badges unless the product needs them. Preserve recovery instructions and necessary context.
- **Forms:** Request only necessary information. Reuse known values. Reveal advanced choices progressively. Keep required inputs and existing capabilities reachable.
- **Controls:** Style semantic controls before rebuilding their behavior. Preserve navigation, back gestures, dismissal, scrolling, selection, and keyboard behavior. Do not replace a tab bar solely for novelty.
- **Interaction:** Make the full visible control tappable, including padding. Keep sibling actions independent. Never nest buttons or let parent gestures block scrolling. Provide relevant pressed, selected, disabled, progress, error, and focus states.
- **Icons:** Prefer SF Symbols for familiar actions. In sheet headers and other view headers or toolbars, use icon-only buttons when the symbol and context fully convey the action; omit redundant visible text. For example, use `xmark` for closing a sheet without a visible “Close” label. Keep visible text when meaning or consequences need explanation. Give every icon-only button an accessible localized action label and preserve its full tappable area. Do not substitute emoji unless the product explicitly includes them. Preserve supplied logos.
- **Images:** Use supplied assets or relevant real photography. Do not generate artwork unless requested. Do not invent image URLs, stretch thumbnails, or add decorative heroes as filler. Identify missing assets. Keep the layout usable without them.
- **Motion:** Preserve continuity through native transitions or restrained animation. Avoid decorative cascades, perpetual pulsing, and delays added solely for visual effect. Respect Reduce Motion.
- **Haptics:** Match signals to meaningful events. Keep haptics optional. Preserve native feedback without duplicate playback. Avoid additional feedback on every tap. Keep the task usable without haptics.
- **Resilience:** Use plausible, varied content. Include empty, loading, error, and populated states where relevant. Preserve entered data during recoverable failures. Use sample data only in previews or explicitly requested prototypes. Keep sample data outside production data paths. Do not add unrelated features to satisfy a checklist.
- **Accessibility:** Support text wrapping, Dynamic Type, localization, accessible names, and independent actions. Respect safe areas and keyboard insets. Adapt iPad layouts to available width. Resolve supported appearances through semantic roles instead of screenshot inversion.

## Complete the requested work

Use the project's available build and UI tools. This skill does not require a particular agent, plugin, or paid service. Check evidence proportional to the change:

1. Compare affected renders with the design direction when tools permit.
2. Exercise changed interactions and relevant states.
3. Check affected layouts with long content, large text, and supported appearances.
4. For implementation tasks, fix observed defects within scope.
5. For review-only tasks, report findings without edits.
6. Check again after material changes.

Stop implementation when the requested scope works and remaining concerns have clear outcomes or disclosures. Complete review-only work when findings and evidence limitations are clear. Do not cycle through arbitrary cosmetic variants. Build success does not establish visual quality. Screenshots do not establish motion, tactile quality, or complete accessibility.

Deliver the requested changes or review. Explain consequential choices, completed checks, and unavailable evidence. Include useful artifact links. Use the user's language for conversation and product text. Keep internal design-process terminology outside the app.
