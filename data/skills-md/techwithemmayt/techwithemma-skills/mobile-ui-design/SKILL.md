---
name: mobile-ui-design
description: Turn a mobile app idea, plan, codebase, or visual references into a complete screen inventory, coherent visual direction, board-ready prompt, optional generated concept, and portable mobile-design.md handoff. Use for product design before implementation; do not implement application screens.
---

# Mobile UI Design

## Preserve the user's product

Extract the user's required screens, flows, content, visual choices, references, exclusions, and output request before proposing anything. Treat explicitly named decisions as locked. A supplied screen list or implementation plan overrides this skill's defaults. Never replace the requested product with a generic template.

Inspect the brief, codebase, existing routes, plan, screenshots, assets, fonts, tokens, and design documents. Reuse reliable decisions and do not ask the user to repeat available information. Tell them concisely what will be inspected or produced. Do not edit application code.

When useful references are available, study 3–5 strong screens for the same category and screen type. Extract repeated layout, hierarchy, CTA placement, background, navigation, and motion patterns—not one app's pixels, copy, branding, or exact composition. Use fewer references when the user's supplied direction is already decisive.

## Build the screen inventory

List every screen implied by the actual product and group screens into flows. Include loading, empty, error, success, permission, active-task, or other states as separate designs only when their composition materially differs.

Do not add onboarding, authentication, subscriptions, or other categories unless requested or required by the product. For welcome screens or onboarding, read [references/onboarding-paywall-design.md](references/onboarding-paywall-design.md); when the journey is undefined, use its product-personalized default. Show the recommended inventory and assumptions once before locking it.

## Define one visual direction

Create one coherent, product-specific direction unless alternatives are requested:

- personality, emotional tone, platform expectations, and primary visual focus;
- semantic colour roles, contrast, light/dark treatment, and background choice;
- typography hierarchy and numeric treatment;
- spacing, radii, borders, elevation, icons, imagery, and component language;
- motion character, content choreography, accessibility, and platform considerations;
- the visual qualities borrowed from supplied references without copying branding.

Choose a plain surface, image-led background, or restrained gradient from the product, user request, existing system, and reference direction. A gradient is optional, not a requirement for onboarding, plans, paywalls, or premium design. When chosen, treat it as screen/flow atmosphere first and keep controls solid unless a gradient control is explicitly intended.

If custom illustration, mascot, hero, or animated artwork materially improves the concept and no suitable asset exists, read [references/illustration-assets.md](references/illustration-assets.md). Define replaceable image/video slots plus ready-to-use generation and motion prompts. Never substitute complex JSX artwork. Generate assets only when the user explicitly requests or approves it.

## Make the product feel complete

Populate data-dependent surfaces with believable representative names, messages, charts, progress, plans, plan amounts, trial lengths, due dates, renewal terms, offers, ratings, recommendations, and results. The user must see a complete design; never leave an important surface blank because its backend, catalog, or formula is unfinished. Never place `sample`, `demo`, `mock`, `placeholder`, or `Lorem ipsum` inside the UI.

Representative content is not permission to publish false claims. Record what must later connect to real APIs, formulas, catalog prices, eligibility, analytics, verified ratings/testimonials, legal content, and production data. In the final chat, list those replacements and ask whether the user wants the implementation connected to real backend/store data next.

## Keep one design deliverable

When a project filesystem is available, create or update `docs/design/mobile-design.md`; for one feature use `docs/design/<feature>-design.md`. Keep one file from `Status: Draft` through `Status: Approved`; do not create separate temporary/final copies or automatically edit `AGENTS.md`.

Target 1,000–2,000 words for the complete design document. This is a compression target, not permission to omit screens or design decisions. Preserve exact visual values, locked requirements, important states, asset prompts, representative content, and replacement notes. Save space by defining shared rules once, keeping ordinary screens to compact inventory entries, expanding only visually or behaviorally distinct screens, and removing rationale, history, rejected alternatives, and repeated prose. Exceed the range only when the user requests more detail or a materially larger product cannot remain complete within it.

Read [references/design-deliverable.md](references/design-deliverable.md) for the compact handoff and board-prompt format. If filesystem access is unavailable, maintain the draft in conversation and provide copy-ready Markdown with its intended path.

Before refinement, read the current design document, preserve locked decisions, and change only the requested parts. Show a concise change summary; repeat the complete prompt only when requested.

## Prepare or generate boards

Write a complete board-ready prompt that covers the approved inventory before offering generation. If the user explicitly asked to generate a board, that request is approval—do not ask again after showing the direction. Otherwise offer: refine the prompt, generate a 3–5-screen concept board, or generate a selected numbered full-app board.

Use one row for 1–4 portrait screens and a balanced grid of at most four columns by two rows for 5–8. Split larger inventories into numbered flow-based boards. Generate only the requested board, not every board automatically.

After generation, compare the board with the current design document for required screens/content, hierarchy, typography, colours, spacing, components, representative data, and consistency. Record the real asset path and mismatches. Never claim generation or visual approval without evidence.

## Create the implementation handoff

After user approval, tighten the same document and change its status to `Approved`. Preserve the product summary, screen inventory, locked visual system, interaction and content-motion intent, asset specifications, approved prompt/board paths, representative-data replacements, and unresolved decisions.

Keep the handoff implementation-neutral so Expo/React Native, SwiftUI, Compose, Flutter, or another design workflow can consume it. Design owns what the experience should be; the implementation agent owns code structure, packages, navigation configuration, and runtime verification.

## Quality check

Confirm the inventory matches the user's product; every ask changes something later; the visual direction can be reproduced; screens contain believable content and relevant states; accessibility and platform needs are recorded; boards stay readable; generated assets actually exist; locked decisions survive refinement; and the approved handoff is concise and self-contained.

Run a mechanical anti-template check: normally one accent family, one neutral family, one approved radius scale, zero unexplained gradients/glass/glow, zero emoji used as interface icons, and one consistent label for each repeated action. Every exception needs a product or brand reason.

## Design the complete onboarding payoff

Whenever the scope includes a pledge, generated plan, result, or connected paywall, read [references/onboarding-paywall-design.md](references/onboarding-paywall-design.md), even when the journey is already specified. Design the interaction states, clean result, and visual continuity into purchase before writing image prompts. This skill supplies a complete platform-neutral design without requiring Expo Native Builder; any implementation agent can consume it. For separately generated screen images, use the per-screen prompt guidance in [references/design-deliverable.md](references/design-deliverable.md).
