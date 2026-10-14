---
name: wcag-2.2-aa
description: Use when auditing, remediating, or building any user-facing UI to meet WCAG 2.2 Level A/AA - accessibility review, a11y audit, "is this accessible", contrast/keyboard/focus/ARIA/alt-text/target-size/screen-reader issues, VPAT or ACR prep, or before shipping HTML/CSS, WordPress, React/Tailwind, or Hugo front-end to a client. Covers the six A/AA criteria new in WCAG 2.2.
---

# WCAG 2.2 AA Accessibility

## Overview

WCAG 2.2 is a W3C Recommendation (12 December 2024). Conformance is measured against 86 success criteria organized under four principles - **Perceivable, Operable, Understandable, Robust (POUR)** - at three levels (A, AA, AAA). The 84EM baseline is **Level A + AA** (55 criteria: 31 A + 24 AA). AAA is aspirational, not required.

Core principle: **a11y is a build requirement verified with tooling, never a self-assessed claim.** Automated scanners catch roughly a third of AA failures. A green axe run is necessary, not sufficient. Every compliance claim needs an automated scan **plus** a manual keyboard-only pass.

The full normative text of every criterion (with definitions, exceptions, and notes) is in `references/wcag-2.2-full.md` - the verbatim W3C spec. Quote it; do not paraphrase normative wording into a client deliverable.

## When to Use

- Auditing a page/component/theme/plugin UI for accessibility
- Remediating reported a11y defects (contrast, focus, keyboard trap, missing labels)
- Building new user-facing UI that must ship WCAG 2.2 AA (the 84EM default)
- Preparing a VPAT / Accessibility Conformance Report
- Any time the request says "accessible", "a11y", "WCAG", "screen reader", "508", "ADA"

**When NOT to use:** back-end-only work with no rendered UI; deciding to *exceed* AA (that's a scope conversation with the client, not this skill).

## Method (audit + remediate)

Run all four passes. No single pass is sufficient.

1. **Automated scan.** axe-core (axe DevTools, `@axe-core/cli`, Playwright `@axe-core/playwright`), Lighthouse, or WAVE. Records the machine-detectable third. Zero violations here is the floor, not the ceiling. If the project has no scanner installed, do not add one as a dependency - inject axe-core into the running page instead. Runnable snippets for a single page, a whole-sitemap run, and validating the harness before trusting its output: `references/running-axe.md`.
2. **Keyboard-only pass.** Unplug the mouse. Tab through the entire flow: every interactive element reachable, visible focus ring at each stop, logical order, no trap, Esc closes overlays, focus not hidden behind sticky headers (2.4.11). Skip link works (2.4.1).
3. **Contrast + zoom.** Text 4.5:1 (large text/UI 3:1) - 1.4.3 / 1.4.11. Reflow at 320px / 400% zoom with no horizontal scroll (1.4.10). Text-spacing overrides don't clip content (1.4.12).
4. **Screen-reader / semantics pass.** VoiceOver, NVDA, or Orca. Correct headings, landmarks, list/button/link semantics; every image has meaningful or empty alt; every control has a programmatic label; dynamic changes announce via live regions (4.1.3). Semantic HTML first - ARIA only to fill gaps native elements cannot.

Report findings as `criterion number + name → failing element → fix`. Cite the criterion, link `references/wcag-2.2-full.md`.

## New in WCAG 2.2 (commonly missed - check these first)

WCAG 2.2 added six A/AA criteria over 2.1 and **removed 4.1.1 Parsing** (now always satisfied - do not report it). The additions are the most-often-overlooked failures:

| # | Name | Level | Check |
|---|------|-------|-------|
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Focused element not fully hidden by sticky header/footer/overlay |
| 2.5.7 | Dragging Movements | AA | Any drag action has a single-pointer alternative (tap/click) |
| 2.5.8 | Target Size (Minimum) | AA | Pointer targets ≥ 24×24 CSS px, or adequately spaced |
| 3.2.6 | Consistent Help | A | Help mechanisms appear in the same relative order across pages |
| 3.3.7 | Redundant Entry | A | Don't force re-entering info already given in the same process |
| 3.3.8 | Accessible Authentication (Minimum) | AA | No cognitive-function test (transcription, memorization, puzzle) as the only auth path |

## Level A / AA criteria checklist (55)

Full text in `references/wcag-2.2-full.md`. This is the scan list - every item must pass for AA.

**1. Perceivable** - 1.1.1 Non-text Content · 1.2.1 Audio/Video-only (Prerecorded) · 1.2.2 Captions (Prerecorded) · 1.2.3 Audio Description or Media Alternative · 1.2.4 Captions (Live) · 1.2.5 Audio Description (Prerecorded) · 1.3.1 Info & Relationships · 1.3.2 Meaningful Sequence · 1.3.3 Sensory Characteristics · 1.3.4 Orientation · 1.3.5 Identify Input Purpose · 1.4.1 Use of Color · 1.4.2 Audio Control · 1.4.3 Contrast (Minimum) · 1.4.4 Resize Text · 1.4.5 Images of Text · 1.4.10 Reflow · 1.4.11 Non-text Contrast · 1.4.12 Text Spacing · 1.4.13 Content on Hover or Focus

**2. Operable** - 2.1.1 Keyboard · 2.1.2 No Keyboard Trap · 2.1.4 Character Key Shortcuts · 2.2.1 Timing Adjustable · 2.2.2 Pause, Stop, Hide · 2.3.1 Three Flashes or Below Threshold · 2.4.1 Bypass Blocks · 2.4.2 Page Titled · 2.4.3 Focus Order · 2.4.4 Link Purpose (In Context) · 2.4.5 Multiple Ways · 2.4.6 Headings & Labels · 2.4.7 Focus Visible · 2.4.11 Focus Not Obscured (Minimum) · 2.5.1 Pointer Gestures · 2.5.2 Pointer Cancellation · 2.5.3 Label in Name · 2.5.4 Motion Actuation · 2.5.7 Dragging Movements · 2.5.8 Target Size (Minimum)

**3. Understandable** - 3.1.1 Language of Page · 3.1.2 Language of Parts · 3.2.1 On Focus · 3.2.2 On Input · 3.2.3 Consistent Navigation · 3.2.4 Consistent Identification · 3.2.6 Consistent Help · 3.3.1 Error Identification · 3.3.2 Labels or Instructions · 3.3.3 Error Suggestion · 3.3.4 Error Prevention (Legal, Financial, Data) · 3.3.7 Redundant Entry · 3.3.8 Accessible Authentication (Minimum)

**4. Robust** - 4.1.2 Name, Role, Value · 4.1.3 Status Messages

## Per-stack remediation notes

**Generic HTML/CSS.** Semantic elements before ARIA (`<button>` not `<div role=button>`, `<nav>`/`<main>`/`<header>` landmarks, real headings in order). `:focus-visible` styling meeting 3:1 against adjacent colors. `prefers-reduced-motion` guards on animation. Decorative images `alt=""`; informative images described. Labels via `<label for>` or `aria-label`, never placeholder-as-label.

**WordPress (block themes).** Contrast lives in `theme.json` color palette - validate every text/background preset pair, don't inline-style. Patterns use block markup (`<!-- wp:group -->`), so semantics come from block choice: use Heading blocks in order, Button blocks (not styled paragraphs), Navigation block for menus. Check the active theme's skip-link and focus styles; many themes ship weak focus rings. Plugin admin UIs need the same four passes - form labels, `aria-describedby` on errors, nonce-guarded but still labeled controls.

**React / Tailwind.** Manage focus on route change and modal open/close (trap inside, return on close, Esc to dismiss). shadcn/Radix primitives are accessible by default - don't strip their ARIA. Tailwind `focus-visible:` utilities must hit 3:1; the default `outline-none` without a replacement is a 2.4.7 failure. Announce async state with a polite live region. Icon-only buttons need `aria-label`. Verify target size (2.5.8) - `h-6 w-6` (24px) is the floor.

**Hugo.** Accessibility is authored in templates/partials, not content - but content vs template separation still holds: alt text comes from front matter or page resources, never hardcoded in the partial. Ensure the base template sets `<html lang>`, one `<h1>` per page, a skip link partial, and that shortcodes producing media require an `alt` param. Check generated markup with axe against the built site, not the source.

## Common mistakes

| Mistake | Reality |
|---|---|
| "axe passed, so it's AA." | axe covers ~a third of AA. Manual keyboard + SR passes are required. |
| "I loaded the page, looks fine." | Passive load misses keyboard traps, focus order, SR announcements, state changes. Exercise the flow. |
| Reporting 4.1.1 Parsing | Removed in WCAG 2.2. Never cite it. |
| Color alone signals state | 1.4.1 fails. Add text/icon/pattern. |
| Placeholder used as the label | Vanishes on input, fails 3.3.2 Labels or Instructions. Use `<label>`. |
| `role="button"` on a `<div>` | Loses keyboard + focus for free. Use `<button>`. |
| Paraphrasing criterion text into a deliverable | Quote `references/wcag-2.2-full.md` verbatim; paraphrase invents normative meaning. |
| "Focus ring removed for design" | `outline:none` with no replacement fails 2.4.7. Provide a visible `:focus-visible` style. |

## Do not claim compliance without evidence

Never state "meets WCAG 2.2 AA" until an automated scan **and** a manual keyboard-only pass have both run and their output is in hand. Report what was tested, at which level, with which tool. A hedged "not yet verified" beats a confident wrong conformance claim in a client-facing ACR.
