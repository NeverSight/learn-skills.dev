---
name: accessibility-audit
description: Audits a page, component or design against WCAG 2.2 AA, covering contrast, keyboard paths, visible focus, semantics and landmarks, heading order, ARIA usage, form labels and errors, target size, motion and alt text, and reports each issue with its success criterion, severity and fix, followed by corrected code. Use when asked to check accessibility, run an a11y or WCAG audit, or make something work with screen readers. Not for general visual feedback; use design-critique.
---

# Accessibility Audit

Produces a WCAG 2.2 AA audit: an issue table mapped to success criteria with severity and a concrete fix, followed by corrected code for every critical and serious issue.

## When to use
- "Is this accessible?", "run an a11y audit" or "check WCAG compliance"
- Before launch, a procurement review, or after a user complaint
- Reviewing a modal, menu, tabs, combobox or form for keyboard and screen reader support
- Checking a design file for contrast and target size before build
- Following up automated results (axe, Lighthouse) with the manual checks they cannot do

## Workflow
1. Scope: which page, component and states; what is available (code, URL, screenshot). State what cannot be tested, e.g. a screenshot allows no keyboard or semantics testing.
2. Automated-style checks: lang attribute, page title, alt attributes, form labels, contrast, duplicate IDs, landmarks. Automated tools find only a minority of issues; never stop here.
3. Keyboard: Tab and Shift+Tab through everything. Order matches visual order, focus is always visible, no traps, Esc closes overlays, focus moves into dialogs and returns to the trigger, a skip link reaches main.
4. Semantics: header, nav, main and footer landmarks; one h1 and no skipped heading levels; real lists; buttons for actions and links for navigation; tables with th and scope; name, role and value for custom widgets.
5. Visual: text and non-text contrast, reflow at 320px, 200% text resize, text spacing override, color-only meaning, focus not hidden by sticky headers.
6. Forms: visible labels, required indication, errors identified in text with a suggestion, autocomplete tokens on personal data fields, no redundant re-entry.
7. Motion and media: prefers-reduced-motion respected, no flashing over 3 times per second, pause control for auto-moving content, captions and transcripts.
8. Write the report ordered by severity, then write corrected code.

## Rules
**Key WCAG 2.2 AA thresholds**
- 1.4.3 Contrast (Minimum): 4.5:1 text; 3:1 large text (≥24px regular or ≥18.66px bold).
- 1.4.11 Non-text Contrast: 3:1 for component boundaries, states, focus indicators and meaningful graphics.
- 2.5.8 Target Size (Minimum): 24×24 CSS px or equivalent spacing; recommend 44×44 for touch.
- 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured (Minimum): the focused element is never fully hidden by sticky or overlay content.
- 1.4.10 Reflow at 320 CSS px; 1.4.4 Resize Text to 200%; 1.4.12 Text Spacing (line-height 1.5, paragraph spacing 2×, letter 0.12em, word 0.16em) without loss of content.
- 2.3.1 Three Flashes or Below Threshold; 2.2.2 Pause, Stop, Hide for auto-moving content lasting over 5 seconds.
- 2.5.7 Dragging Movements: single-pointer alternative. 3.3.7 Redundant Entry (A). 3.3.8 Accessible Authentication (Minimum): allow paste and password managers. 3.2.6 Consistent Help (A).
- 4.1.1 Parsing is obsolete in WCAG 2.2; do not cite it.

**Semantics and ARIA**
- Native elements first (button, a with href, input, select, dialog, details). No ARIA is better than wrong ARIA.
- Every control has an accessible name; icon-only buttons get aria-label or visually hidden text.
- Alt text: informative images describe purpose concisely; decorative images use alt=""; charts get a nearby text summary or data table.
- Errors: message in text, linked with aria-describedby, aria-invalid="true" on the field, focus moved to the first error or an error summary. Status updates via role="status" or aria-live="polite" (4.1.3).
- No positive tabindex; never remove outlines without a replacement indicator of ≥3:1.

**Severity**
- Critical: blocks a task for some users (keyboard trap, unlabeled control, invisible focus). Serious: major difficulty (body text contrast failure, errors shown only in color). Moderate: a workaround exists. Minor: best-practice gap.

## Output
- Summary: scope, method, untested areas, counts by severity.
- Issue table: # | Issue | Location | WCAG SC (number, name, level) | Severity | Fix.
- Corrected code for every Critical and Serious issue in the project's stack (semantic HTML + CSS custom properties, or React + Tailwind if already used), with comments marking each change.
- Manual test script: keyboard steps plus screen reader checks (NVDA with Firefox or Chrome, VoiceOver with Safari).

## Avoid
- Declaring a product compliant from a screenshot or an automated scan alone
- Recommending accessibility overlay widgets as a fix
- role="button" on a div where a button element works
- Placeholder text used as the only label
- outline: none without a visible replacement
- aria-label on non-interactive divs and spans to add meaning
- Issues listed without exact location and a concrete fix

## Final check
- [ ] Every issue cites SC number, name and level
- [ ] Contrast issues include the measured ratio and a passing replacement value
- [ ] Keyboard path tested end to end, including overlays and focus return
- [ ] Corrected code prefers native semantics over ARIA
- [ ] Untestable areas stated explicitly
- [ ] Issues ordered Critical, Serious, Moderate, Minor
