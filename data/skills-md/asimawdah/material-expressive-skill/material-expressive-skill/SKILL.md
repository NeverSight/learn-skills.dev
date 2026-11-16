---
name: material-expressive-skill
description: Design, implement, modernize, and review production interfaces with Material 3 and Material 3 Expressive. Use when a task mentions Material Design 3, M3 Expressive, Material You, expressive UI, Material components or theming, adaptive Material layouts, or a Material-focused accessibility/design review.
license: MIT
compatibility: Agent Skills-compatible clients. No runtime dependencies; inspect the project and verify current platform APIs before implementation.
metadata:
  author: asimawdah
  version: "0.1.0"
---

# Material 3 Expressive

Use this skill to create interfaces that behave like a coherent Material product, not screens that only imitate its surface style.

Material 3 Expressive is an expansion of Material 3. It adds research-informed options for theming, components, motion, typography, and visual expression. It does not replace Material 3 foundations. Preserve familiar semantics and use expression to make important information, actions, and state easier to perceive.

## Non-negotiable principles

- **Task before treatment.** Understand the user, task, information architecture, content priority, and interaction before styling.
- **Semantics before spectacle.** Use the right component for the job. Never disguise navigation, actions, selection, or destructive behavior.
- **Expression with a reason.** Every expressive choice must improve hierarchy, recognition, feedback, or emotional clarity.
- **Platform truth.** Do not invent APIs, component availability, tokens, or version requirements. Native feature parity differs across Android, Wear OS, Flutter, web, and other platforms.
- **Complete behavior.** Specify meaningful loading, empty, error, success, disabled, focus, hover, pressed, and selected states.
- **Accessible by default.** Design for assistive technology, sufficient contrast, text scaling, keyboard and pointer input, reduced motion, localization, and right-to-left layouts.
- **Preserve the codebase.** Inspect existing architecture and conventions. Do not migrate frameworks, replace libraries, or upgrade dependencies as incidental design work.

## Workflow

Follow this sequence unless the user explicitly narrows the task.

### 1. Inspect the project and resolve the target

Identify the framework, platform, existing Material library and version, theme setup, navigation, reusable components, state-management approach, build/test commands, and current design conventions.

Clarify only constraints that materially change architecture. Otherwise, make conservative assumptions and state them briefly. Never assume a UI library supports a newly announced M3 Expressive feature: check the official API and release notes first.

### 2. Understand the product

Capture:

- Primary user, goal, and success action.
- Screen or flow boundaries and information hierarchy.
- Content density, data relationships, and important decisions.
- Brand constraints and the allowed degree of visual change.
- Supported devices, window sizes, orientations, and input methods.
- Required states, failure paths, permissions, and destructive actions.
- Accessibility, localization, privacy, and performance constraints.

Use [the design brief](templates/design-brief.md) when a structured brief would help.

### 3. Establish structure and hierarchy

Group related content, distinguish navigation from actions, and identify the primary action. Choose an information layout before choosing colors, corner shapes, or animation. Prefer a small number of clear regions over a pile of nested cards.

### 4. Apply M3 foundations

Define semantic color roles, typography, shape, elevation, spacing, and icon usage as a coherent system. Support light and dark themes; consider dynamic color where the platform supports it and where user or brand requirements allow it. Read [design foundations](references/design-foundations.md).

### 5. Make an intentional expressive pass

Use one or a few expressive levers when they reinforce the task:

- Size and component flexibility to establish priority.
- Shape to distinguish roles, groups, or meaningful state.
- Color to focus attention and communicate semantic meaning.
- Typography to create hierarchy and character.
- Containment to clarify groups and isolate important actions.
- Motion to explain cause, continuity, state change, or spatial relationships.

Do not maximize every lever. Routine settings, forms, dense data, and long reading surfaces usually need restraint. Read [expressive principles](references/expressive-principles.md).

### 6. Select components and patterns

Choose components by user intent and platform support, not by novelty. Prefer official components when they meet the need. Use custom components only for genuine gaps, and preserve expected semantics, states, and interaction behavior. Read [components and patterns](references/components-and-patterns.md).

### 7. Design for the available window

Adapt navigation, pane count, hierarchy, and information density to the app window, not merely to a device label. Support resizing, fold/unfold transitions, orientation changes, keyboard use, and large displays when relevant. Read [adaptive layouts](references/adaptive-layouts.md).

### 8. Define interaction, feedback, and motion

Specify state transitions, feedback timing, focus behavior, error recovery, and cancellation. Motion should communicate a state change or spatial relationship; provide a reduced-motion alternative. Read [motion and feedback](references/motion-and-feedback.md).

### 9. Implement for the actual platform

Use the smallest correct set of dependencies and stable APIs by default. Mark experimental APIs clearly and explain the trade-off before adopting them. Apply the platform-specific notes in [platform guidance](references/platform-guidance.md).

### 10. Verify before handoff

Run relevant project checks and review every required state, viewport, input mode, theme, locale direction, and accessibility behavior. Do not report checks that were not run. Use [the review checklist](references/review-checklist.md) and [implementation workflow](references/implementation-workflow.md). Provide a concise handoff using [the template](templates/implementation-handoff.md).

## Reference routing

Load only the references needed for the current task:

| Task | Read |
| --- | --- |
| Any M3 Expressive design decision | `references/expressive-principles.md` |
| Theme, color, typography, shape, elevation, spacing | `references/design-foundations.md` |
| Choosing or composing components | `references/components-and-patterns.md` |
| Animation, transitions, loading, feedback | `references/motion-and-feedback.md` |
| Phone, tablet, foldable, desktop, or wearable adaptation | `references/adaptive-layouts.md` |
| Accessibility, RTL, localization, input support | `references/accessibility-and-internationalization.md` |
| Framework-specific implementation | `references/platform-guidance.md` |
| End-to-end delivery and verification | `references/implementation-workflow.md` |
| Auditing a completed design | `references/review-checklist.md` |
| Current API, version, or source question | `references/official-sources.md` |

## Quality bar

A result is ready only when:

1. A user can identify the primary task and action without explanation.
2. The design uses semantic Material foundations rather than arbitrary decoration.
3. Expressive treatments have a specific purpose and are not applied uniformly.
4. The interface remains understandable and usable at supported sizes and input modes.
5. All meaningful states and failure paths are considered.
6. Accessibility and localization are part of the implementation, not deferred polish.
7. Platform APIs and dependency versions are verified and the handoff states what was actually tested.

When the project cannot meet a requirement, identify the limitation and provide the safest platform-appropriate alternative. Never claim full Material 3 Expressive parity where the platform does not provide it.
