---
name: taste-accessibility
description: |
  Accessibility built into generation, not bolted on after: WCAG 2.2 AA compliance checks (contrast, keyboard, focus, labels, semantics, target size, reduced motion, autocomplete, error handling), baked into every page or component the agent builds. Run before calling any UI done. Stack on the design-taste core skill.
triggers:
  - "accessibility"
  - "a11y"
  - "wcag"
  - "screen reader"
  - "keyboard navigation"
  - "contrast check"
---

# taste-accessibility

> AI-generated UI is inaccessible by default. This skill makes accessible the default. Every rule below is applied during generation — not as a fix-up pass.

## 1. SEMANTIC STRUCTURE (The Code Skeleton)

- One `<h1>` per page; heading levels never skip (h1 → h3 without h2 = failure); headings carry the page outline — test by reading only headings.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, plus `<aside>`/`<section>` with accessible names where meaningful.
- Lists for lists (`<ul>` for nav, features), `<table>` only for tabular data with `<th scope>` headers.
- Buttons are `<button>`; links are `<a href>`; both have visible text. Icon-only controls get `aria-label` matching their visible tooltip.
- Decorative images: `alt=""` (empty). Informative images: alt describing meaning, not appearance ("Chart: conversion fell from 18% to 9% in May" — not "a blue line chart").
- `aria-hidden="true"` + `tabindex="-1"` on decorative SVG/decor; never `aria-hidden` on focusable elements.

## 2. KEYBOARD COMPLETE (Nothing Requires a Mouse or Touch)

- Everything reachable: tab order follows visual order; no element focusable that isn't interactive (`tabindex="0"` only on purpose).
- Focus visible everywhere: 2px ring, 3:1 contrast vs adjacent, `outline-offset` ≥ 2px. Never `outline: none` without a replacement.
- Standard interactions: Enter activates buttons/links; Space toggles; Esc closes dialogs and menus.
- Dialogs/popovers: focus moves into the dialog on open, traps within (or the platform's native pattern), returns to the trigger on close; overlay has `role="dialog"` + `aria-modal="true"` + labeled.
- Skip link: first focusable element on every marketing page ("Skip to content"), visible on focus.
- Custom components (menu, tabs, combobox, slider): implement ARIA patterns correctly (e.g., `role="tablist"` with `aria-selected`, arrow-key navigation) or use the platform element instead — a native `<select>` beats a broken custom one.

## 3. CONTRAST & TARGETS (Exact Numbers, WCAG 2.2)

| Rule | Requirement |
|---|---|
| Normal text | ≥ 4.5:1 |
| Large text (≥24px / ≥18.66px bold) | ≥ 3:1 |
| UI components & focus | ≥ 3:1 vs adjacent |
| Pointer target size | ≥ 24×24px (AA 2.2), ≥ 44×44px recommended & for touch |
| Spacing exception | 24px targets with ≥ 24px gaps to neighbors pass |

- Placeholder-only labels fail (4.1.2): every input needs a programmatically associated label (`<label for>` or `aria-labelledby`).
- Error states: never color-only — text message + icon; errors announced (`aria-live="assertive"` region); error messages identify the field and give the fix, not "invalid".
- Focus indicators on dark and light surfaces both; check focused state against ITS background, not page background.

## 4. FORMS (Generation Checklist)

- Correct `type` per input (`email`, `tel`, `password`, `number`, `search`) + correct `autocomplete` tokens (`email`, `name`, `credit-card-number`, etc.).
- `required` + `aria-required`; validation on `:user-invalid` styling (not just :invalid — don't punish pre-submit), with visible messages.
- One column layout for anything ≥ 4 fields; labels above inputs; hint text associated (`aria-describedby`) not detached.
- Multi-step wizards: progress announced, errors summarize at top, back/next keyboard-safe.

## 5. MOTION & COGNITION

- Everything under `prefers-reduced-motion` (see taste-motion §7): no parallax, no carousel autoplay, no marquees.
- No auto-playing media with sound; carousels pause on hover/focus; content doesn't move faster than the eye can read it.
- Timeouts (sessions, auto-advance): ≥ 20s warning or user control (WCAG 2.2.1).
- Plain language; expand abbreviations at first use; no emoji-only communication.

## 6. TESTING (Run These Checks Before Done)

1. Keyboard walk: Tab through the entire page — focus visible at every stop, order sane, nothing trapped.
2. Read with a screen reader (VoiceOver/NVDA): page title, heading outline, every control labeled, regions announced.
3. Contrast: sample every text/background pair used (at least: headings, body, muted, button text, placeholder, borders of inputs).
4. Resize: at 200% zoom (up to 1280px wide), no horizontal scroll, no text clipping.
5. Check `aria-label`s don't duplicate visible text unnecessarily; check no empty buttons/links exist.
6. Dark/light variants both pass (never assume one does).

## 7. CHECKLIST (Fail the Page If…)

- [ ] Any heading level skipped.
- [ ] Any input without an associated label.
- [ ] Any interactive element unreachable by keyboard.
- [ ] Any focus indicator invisible or `outline: none` without replacement.
- [ ] Any text pair below 4.5:1 (3:1 for large) that isn't a deliberate, documented exception.
- [ ] Any error communicated by color alone.
- [ ] No `prefers-reduced-motion` handling.
- [ ] Touch targets under 24px with less than 24px spacing.

*Accessibility is not a feature. It is the interface working. Ship nothing that fails this checklist.*