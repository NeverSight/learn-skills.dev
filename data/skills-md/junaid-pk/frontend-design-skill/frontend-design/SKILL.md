---
name: frontend-design
description: Design, build, review, or refine production frontend interfaces for SaaS products, web apps, dashboards, onboarding flows, and landing pages. Use for frontend design work where Codex must turn requirements into clear, restrained, consistent, trustworthy UI; remove AI-generated visual clutter; improve hierarchy, states, copy, navigation, responsiveness, or usability; or polish an existing interface so users can complete their main job without confusion.
---

# Frontend Design

Design the shortest clear path from arrival to a useful result. Treat visual polish as the consequence of strong interface decisions, not added decoration. Make the product feel calm, competent, and intentional.

## Start with the user's job

Before choosing cards, colors, or navigation, identify:

1. Who is using this screen?
2. What did they arrive to accomplish?
3. What is the one primary action or piece of information?
4. What must they know to act with confidence?
5. What can be removed without blocking the job?

Make each screen answer one primary question. Add secondary features only when a real secondary intent exists, never to fill space. Assume the creator knows the product too well; guide a new user more explicitly than feels necessary.

If requirements are incomplete, infer a sensible primary job from the product context and state the assumption briefly. When reference screenshots or an established design system exist, inspect and follow them instead of inventing an unrelated visual direction.

## Establish rules before composing screens

Define a compact system and reuse it everywhere:

- a restrained neutral base and one main accent;
- semantic colors for status, charts, warnings, and destructive actions;
- one type family or a deliberate, minimal pairing with a small hierarchy;
- a consistent spacing scale, control heights, icon sizes, border weights, and radius scale;
- a stable vocabulary for actions and objects;
- clear primary, secondary, tertiary, and destructive action treatments.

Prefer near-white or quiet neutral surfaces, thin borders, and subtle separation. Use shadows only when they explain elevation, focus, or an important starting point. Avoid glow effects, clashing gradients, arbitrary glassmorphism, and multiple competing accents unless the brand or brief specifically requires them.

Use one coherent icon family such as Lucide, Phosphor, or the project's existing set. Do not use emoji as interface icons or decoration unless emoji are part of the product's content or brand language. Pair unfamiliar icon-only controls with labels or tooltips.

Keep controls geometrically consistent. Check text centering, icon alignment, padding, radii, and baseline alignment rather than accepting framework defaults blindly.

## Create hierarchy, not volume

Treat every screen like a sentence with one subject. Make the most important element obvious through size, weight, contrast, placement, or space, then turn down everything around it.

Reserve strong color for meaning or action. Let product data, statuses, and the primary action carry color while navigation and chrome stay quiet. Do not give every chip, button, KPI, or category a different color.

Choose components according to the information and task:

- use tables and compact lists for dense, comparable records;
- use cards when grouping is meaningful, not as the default container for everything;
- move infrequent row actions into a clear overflow menu;
- prioritize the number or field that matters and demote metadata;
- use a centered modal for a short, focused form instead of an empty side panel;
- vary space according to content importance rather than repeating identical card grids;
- prefer explicit pagination or “Load more” when it gives users control and a stopping point.

Audit every element with one question: does this help the user understand, decide, or complete the job? Remove it if it only makes the screen look populated.

## Write interface copy as navigation

Use plain, specific, outcome-oriented language from the user's side of the screen. Name controls by what happens: “Save changes,” “Send email,” or “Delete project,” not vague labels such as “Submit” or “Continue” when a more precise verb is available.

Use the same word for the same action throughout the product. If the button says “Publish,” the completion message says “Published.” Do not alternate among “delete,” “remove,” and “trash” for one operation.

Keep labels, helper text, and messages to one job each. Explain errors with a recovery path. Make empty states direct users toward a meaningful first action. Shift marketing copy from implementation or feature inventory toward the result the buyer wants.

## Design the whole state model

Do not design only the ideal screenshot. Test realistic and hostile content: long names, missing values, zero results, many rows, narrow screens, slow requests, failed requests, and limited permissions. Define wrapping, truncation, overflow, and responsive behavior according to the content rather than using one arbitrary character limit.

For every asynchronous or consequential flow, include the states that apply:

- initial and empty;
- loading or progress;
- partial or disabled;
- error with recovery;
- success or completion;
- undo where practical.

Show immediate evidence that work is happening. Use skeletons for content-shaped loads, a familiar progress indicator for short waits, and explicit progress or reassuring status text for long jobs. Never leave a user staring at an unexplained blank surface.

Add ethical friction to destructive, expensive, or irreversible actions. State the consequence, require confirmation proportional to the risk, use typed confirmation only for genuinely severe actions, and show a clear completion state. Offer undo for recoverable destructive actions when possible.

## Guide onboarding progressively

Avoid forced tours that users must dismiss before doing useful work. Make the first valuable action impossible to miss, reveal the next step after completion, and show a short progress path when setup has multiple steps.

Celebrate meaningful progress with restrained feedback. Confetti or playful motion may suit a first success or major milestone, but not routine actions. For B2B products, surface credible outcome metrics such as time saved, work completed, or revenue influenced when the data genuinely supports them.

## Make motion earn its place

Use motion to communicate state, continuity, progress, hierarchy, or cause and effect. Keep it precise and brief. Avoid scroll-jacking, decorative entrance choreography, constant ambient movement, and parallax that does not teach the user anything. Respect reduced-motion preferences.

Ask: “What does this motion tell the user?” If the answer is nothing, remove it.

## Design SaaS landing pages around proof

Make the hero state the product, audience or problem, promised outcome, and primary next step without requiring interpretation. Keep identical destinations labeled identically across the page.

Prefer actual product evidence over generic stock imagery. Show a focused crop or small product demonstration that proves the section's claim; do not make visitors inspect a full dashboard screenshot to find the relevant detail. Avoid repeating the same alternating text-image section or identical four-card row down the page. Give important proof more space and let the page breathe.

Use only the sections needed to answer: What is this? How does it help? How does it work? Can I trust it? What does it cost? What do I do next? Add logos, testimonials, badges, a mega menu, illustration, or animation only when real content and product depth justify them.

## Build, inspect, and simplify

Before implementation, write a compact design contract covering the screen's primary job, hierarchy, palette, type scale, spacing, radii, action hierarchy, icon family, and vocabulary. Reuse the project's tokens and components where they already solve the problem.

Then:

1. Build the primary path and responsive structure.
2. Add realistic content and the full state model.
3. Inspect the rendered UI at desktop and mobile sizes.
4. Check alignment, density, contrast, focus, keyboard use, and reduced motion.
5. Remove visual material before adding more.
6. Verify that a new user can identify the main action and current system state quickly.

Prefer a smaller, coherent interface over a larger showcase. Distinctiveness may come from the product's real content, brand, copy, or one justified signature detail, but never at the expense of clarity, trust, or task completion.

## Final audit

Confirm all of the following before handoff:

- Every screen has one clear primary intent and visual subject.
- Primary, secondary, and destructive actions are unmistakable.
- Color communicates meaning instead of decorating the interface.
- Typography, spacing, radii, icons, and action verbs are consistent.
- Repeated components are compressed and scannable.
- Empty, loading, error, success, and destructive states are handled.
- Realistic data and narrow layouts do not break the design.
- Motion communicates something and reduced motion is respected.
- Landing-page claims are supported by focused product proof.
- Every remaining element helps the user understand, decide, or finish.
