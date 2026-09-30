---
name: personal-ui
description: Use when designing, building, restyling or reviewing app and web interfaces, including components, settings, onboarding, installers and motion, or when designing a product README's presentation. Primary design guidance for this owner, taking precedence over frontend-design's aesthetic defaults without replacing it.
---

# Personal UI

Design for the actual task and this owner's taste. Current instructions and the product's established design system take precedence over examples here.

Use this skill as the primary design guidance when it overlaps with `frontend-design`. Keep `frontend-design` installed and use its compatible implementation guidance. Resolve conflicting aesthetic defaults using this skill and the current request. This is an instruction for cooperating skills, not a mechanism that disables or replaces another skill.

## Start with the right reference

Read [preferences.md](references/preferences.md) for the owner's general preferences and the dated, product-specific decisions. For desktop utilities or dense settings, also read [desktop-patterns.md](references/desktop-patterns.md). For another product type, choose relevant images from [repertoire.md](references/repertoire.md). Open those images before taking visual direction from them. For detailed animation decisions, use [motion.md](references/motion.md).

Keep references conditional. A finance workspace, book reader, installer and command launcher need different amounts of space and different hierarchies. Near-black with purple is Cloak's current direction, not a universal template.

For a product README or installation guide, read [readmes.md](references/readmes.md). For installers, read the installer section in [desktop-patterns.md](references/desktop-patterns.md). [validation.md](references/validation.md) records an independent skill test and the limits of its evidence.

## Design and build

Identify the main action, the information needed to choose it, and the secondary controls. Choose the smallest useful composition for realistic content. Keep consistent edge insets and readable text. Let an empty utility shrink instead of reserving a dashboard's worth of space.

Use existing semantic tokens and components when they fit. Shadcn/ui is a useful reference for understated controls, keyboard behavior and dark neutral surfaces. Preserve its behavior if restyling its components. A reusable design system includes geometry, state, motion and copy, not only colors.

Concentrate accent color in selection and the immediate action. Use a consistent icon family. Keep names beside icons when identification matters. Make secondary configuration deliberate to open and easy to leave.

Write direct action labels, useful errors and short explanations only where they help a decision. Use sentence case and plain punctuation. The owner dislikes tiny redundant status text, em dashes, middle-dot separators and uppercase subtitles. Tasteful emojis and expressive motion are welcome when they serve the product.

## Verify the real interface

Review rendered screens after the data and controls are wired. Use empty, populated, long-text, loading and failed states. Check narrow and resized windows, zoom or OS scaling, keyboard focus, dropdown gutters, hover actions and reduced motion. Check native corners separately from renderer layout.

A control is complete when it acts on real state, its outcome is visible, errors keep the user's draft, and it remains understandable without hover or color alone. Capture screens at rest as well as during transitions. Fix the worst composition or interaction defect and inspect again. A build passing does not establish good design.

## Refine from feedback

Record the user's new feedback in the relevant reference. Separate durable preferences from a decision about this product. Replace superseded guidance rather than accumulating contradictory rules. Keep lessons tied to their cause so the next app can use the principle without reproducing the same screen.
