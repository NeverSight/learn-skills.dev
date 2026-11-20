---
name: design-handoff
description: Prepares designs for engineering with token-based specs, every state and edge case, responsive behavior per breakpoint, interaction and motion specs, accessibility annotations, asset exports, acceptance criteria per screen, and a QA checklist, delivered as a Markdown handoff document. Use when asked to prepare a dev handoff, write specs for developers, annotate designs, or define acceptance criteria. Not for component usage docs, which is design-system-docs.
---

# Design Handoff

Produces a handoff document engineers can build from without guessing: every screen specified with tokens, states, breakpoints, interactions, accessibility, assets, and testable acceptance criteria.

## When to use
- "Prepare this for dev handoff" or "write specs for the engineers."
- A feature is designed, but only the happy path at one screen size exists.
- Engineers keep asking the same questions, or builds drift from the design.
- Defining acceptance criteria and QA steps for a design ticket.
- Exporting icons and images in the right formats and densities.

## Workflow
1. Gather inputs: design files or screenshots, the token source, target platforms (web, iOS, Android), breakpoints, and the component library in use. Ask only if the platform is unknown; otherwise assume responsive web and say so.
2. List the screens and flows (from user-flows if available) and map each element to an existing component or mark it as new.
3. Write specs with tokens: spacing, size, color, type, radius, elevation. Use raw values only where no token exists, and flag them as token candidates.
4. Specify every state and edge case per screen and component (see ui-states).
5. Define responsive behavior per breakpoint: what reflows, stacks, hides, truncates, or swaps component (see responsive-design).
6. Specify interactions and motion: trigger, property, duration, easing, and the reduced-motion alternative (see motion-design).
7. Annotate accessibility: focus order, accessible names, roles, landmarks, heading levels, announcements, and keyboard support.
8. Prepare assets, then write acceptance criteria and the QA checklist.

## Rules
**Specs**
- Reference tokens by name (`space.4`, `color.text.secondary`), never "16px grey". Flag one-off values instead of hiding them.
- State sizing behavior for each element: fixed, hug content, or fill container, with min and max widths.
- Specify text behavior: maximum lines, truncate or wrap, and how the full text is revealed.

**States and edge cases**
- Cover default, hover, focus-visible, active, disabled, loading, empty, error, success, and partial data.
- Test extremes: very long names, translations about 30% longer, 0/1/many items, large numbers, missing images, slow network, permission denied.

**Responsive**
- Use the project's breakpoints; if none exist, propose a mobile-first set (for example 360, 768, 1024, 1440) and label it an assumption.
- Touch targets at least 44×44 pt (iOS) or 48×48 dp (Android); WCAG 2.2 AA requires at least 24×24 CSS px.

**Motion**
- Write each spec as trigger, property, duration, easing, delay: "Menu open: opacity 0 to 1, translateY 8px to 0, 200ms, ease-out." Keep most UI transitions around 150–300ms, with exits shorter than entrances.
- Provide a `prefers-reduced-motion` alternative (fade or instant) for anything that moves or zooms.

**Accessibility**
- Number the focus order on each screen; it follows the visual reading order.
- Every icon-only button has an accessible name, every input has a visible label, and errors are announced (live region or focus move) and linked to their fields.
- Contrast 4.5:1 for text and 3:1 for large text, UI components, and meaningful graphics (WCAG 2.2 AA).

**Assets**
- Icons and logos as optimized SVG with `viewBox` kept and color via `currentColor` where recoloring is needed. UI images with transparency as PNG; web photos as WebP or AVIF with a fallback if required, plus `srcset` widths.
- Mobile rasters: @1x/@2x/@3x for iOS; mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi (1×, 1.5×, 2×, 3×, 4×) for Android, or vector drawables. Names lowercase and hyphenated: `icon-arrow-left.svg`, `hero-onboarding@2x.png`.

## Output
A Markdown handoff document:
```
# [Feature] handoff
Links (design, flow, ticket) · Platforms · Breakpoints · Owner · Version and date
## Overview and scope          in scope / out of scope
## Screens                     per screen: purpose, components, spec table, states, responsive notes
## Interactions and motion     table: Element | Trigger | Property | Duration | Easing | Reduced motion
## Accessibility               focus order, names and roles, announcements, keyboard
## Assets                      table: Name | Format | Sizes or densities | Usage
## Acceptance criteria         per screen, Given / When / Then
## QA checklist
## Open questions              with owners
```

## Avoid
- Handing off only the happy path at a single breakpoint.
- Raw hex and pixel values where tokens exist.
- "Make it feel smooth" instead of duration and easing.
- Redlining every pixel instead of stating the system (tokens, grid, behavior).
- Leaving accessibility for engineering to work out later.
- Acceptance criteria that cannot be tested ("looks good", "feels fast").

## Final check
- [ ] Every screen has states, edge cases, and responsive behavior.
- [ ] Specs use tokens, and one-off values are flagged.
- [ ] Motion specs include trigger, duration, easing, and reduced-motion behavior.
- [ ] Focus order, labels, and roles are annotated.
- [ ] Assets are listed with formats, densities, and file names.
- [ ] Each screen has testable acceptance criteria, and the QA checklist is included.
- [ ] Open questions have owners.
