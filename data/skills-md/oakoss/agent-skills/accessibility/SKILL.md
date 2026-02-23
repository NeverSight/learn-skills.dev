---
name: accessibility
description: |
  Build WCAG 2.2 AA compliant interfaces with semantic HTML, ARIA, keyboard navigation, focus management, color contrast, and screen reader support. Covers forms, dialogs, tabs, live regions, skip links, alt text, and data tables.

  Use when implementing accessible UIs, auditing WCAG compliance, fixing screen reader issues, keyboard navigation, focus traps, or troubleshooting "focus outline missing", "aria-label required", "insufficient contrast", "missing alt text", "heading hierarchy".
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Web Accessibility (WCAG 2.2 AA)

Build for everyone — accessibility is a requirement, not a feature.

## Contrast Ratios (WCAG AA)

| Element                            | Minimum Ratio |
| ---------------------------------- | ------------- |
| Normal text (< 18pt)               | 4.5:1         |
| Large text (>= 18pt or 14pt bold)  | 3:1           |
| UI components and focus indicators | 3:1           |

## WCAG 2.2 New AA Criteria

| Criterion                           | Requirement                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| Target Size Minimum (2.5.8)         | Interactive targets at least 24x24 CSS pixels                                        |
| Focus Not Obscured Minimum (2.4.11) | Focused element at least partially visible, not hidden by sticky headers or overlays |
| Focus Appearance (2.4.13)           | Focus indicator has minimum area (2px perimeter) and 3:1 contrast change             |
| Dragging Movements (2.5.7)          | Provide single-pointer alternative for any drag interaction                          |
| Redundant Entry (3.3.7)             | Do not require re-entering previously provided information                           |
| Consistent Help (3.2.6)             | Help mechanisms (chat, phone, FAQ) appear in same relative order across pages        |
| Accessible Authentication (3.3.8)   | No cognitive function test for login (allow paste, autofill, or alternatives)        |

## Essential Keyboard Patterns

| Key             | Action                                |
| --------------- | ------------------------------------- |
| Tab / Shift+Tab | Navigate between focusable elements   |
| Enter / Space   | Activate buttons and links            |
| Arrow keys      | Navigate within widgets (tabs, menus) |
| Escape          | Close dialogs and menus               |
| Home / End      | Jump to first/last item in widget     |

## Element Selection

| Need                   | Element                           |
| ---------------------- | --------------------------------- |
| Navigates to page      | `<a href="...">`                  |
| Submits form           | `<button type="submit">`          |
| Opens dialog           | `<button aria-haspopup="dialog">` |
| Other action           | `<button type="button">`          |
| Self-contained article | `<article>`                       |
| Navigation links       | `<nav>`                           |
| Supplementary info     | `<aside>`                         |

## Common ARIA Attributes

| Attribute              | Purpose                                            |
| ---------------------- | -------------------------------------------------- |
| `aria-label`           | Name when no visible label exists                  |
| `aria-labelledby`      | Reference existing text as label                   |
| `aria-describedby`     | Additional description (hints, errors)             |
| `aria-live`            | Announce dynamic updates (`polite` or `assertive`) |
| `aria-expanded`        | Collapsible/expandable state                       |
| `aria-hidden="true"`   | Hide decorative elements from screen readers       |
| `aria-invalid`         | Mark form fields with errors                       |
| `aria-required="true"` | Mark required fields                               |
| `aria-busy`            | Indicate loading state                             |

## WCAG 2.2 AA Checklist Summary

| Principle      | Key Requirements                                                                                                                             |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Perceivable    | Alt text on images, contrast >= 4.5:1, color not sole indicator, text resizable to 200%, captions on video, `prefers-reduced-motion` support |
| Operable       | Keyboard accessible, visible focus not obscured, focus appearance meets minimum, targets >= 24px, skip links, dragging alternatives          |
| Understandable | `<html lang="en">`, consistent navigation, consistent help placement, form labels, error identification, no redundant entry, accessible auth |
| Robust         | Valid HTML, name/role/value on all UI components, `aria-live` for status messages (SC 4.1.1 Parsing is obsolete in WCAG 2.2)                 |

## Anti-Patterns

| Anti-Pattern                          | Fix                                               |
| ------------------------------------- | ------------------------------------------------- |
| `<div onClick>` instead of `<button>` | Use semantic HTML elements                        |
| `outline: none` without replacement   | Use `:focus-visible` with visible outline         |
| Placeholder as label                  | Use `<label>` element                             |
| `tabindex` > 0                        | Use DOM order or `tabindex="0"` / `tabindex="-1"` |
| Color-only state indicators           | Add icon and text label                           |
| Skipped heading levels                | Use sequential h1-h6, style with CSS              |
| `role="button"` on `<button>`         | Remove redundant ARIA                             |
| `aria-hidden` on interactive elements | Never hide interactive content                    |
| Fixed font sizes (px)                 | Use `rem` units                                   |
| No focus trap in modal dialogs        | Trap focus, close on Escape                       |

## Common Mistakes

| Mistake                                                        | Correct Pattern                                                                                      |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Adding `aria-label` to elements that already have visible text | Use `aria-labelledby` to reference existing visible text instead                                     |
| Using `aria-live="assertive"` for non-urgent updates           | Use `aria-live="polite"` for most dynamic content; reserve `assertive` for errors and alerts         |
| Setting `alt=""` on informative images                         | Provide descriptive alt text; only use empty alt on purely decorative images                         |
| Adding keyboard handlers to non-focusable elements             | Use native interactive elements or add `tabindex="0"` plus `role` and key handlers                   |
| Testing only with automated tools like axe                     | Automated scans catch ~30% of issues; always supplement with keyboard-only and screen reader testing |

## Screen Reader and Browser Pairings

| Screen Reader | Browser | Platform           |
| ------------- | ------- | ------------------ |
| JAWS          | Chrome  | Windows            |
| NVDA          | Chrome  | Windows (free)     |
| NVDA          | Firefox | Windows (free)     |
| VoiceOver     | Safari  | macOS / iOS        |
| TalkBack      | Chrome  | Android            |
| Narrator      | Edge    | Windows (built-in) |

## Testing Quick Guide

| Method         | Tool                                    | Effort  |
| -------------- | --------------------------------------- | ------- |
| Keyboard-only  | Hide mouse, Tab through page            | 5 min   |
| Screen reader  | JAWS + Chrome or NVDA + Chrome/Firefox  | 10 min  |
| Screen reader  | VoiceOver + Safari (macOS)              | 10 min  |
| Automated scan | axe DevTools browser extension          | 2 min   |
| Lighthouse     | Chrome F12 > Lighthouse > Accessibility | 2 min   |
| Unit tests     | jest-axe (Jest) or vitest-axe (Vitest)  | Ongoing |

## Delegation

When working on accessibility, delegate to:

- `design-system` — Color tokens and contrast verification
- `react-patterns` — Component patterns and hooks
- `testing` — jest-axe integration and test patterns

## Resources

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM](https://webaim.org/)
- [The A11y Project](https://www.a11yproject.com/)

## References

- [Semantic HTML and Structure](references/semantic-html.md) — Document landmarks, heading hierarchy, element selection, skip links
- [Focus Management](references/focus-management.md) — Focus indicators, focus not obscured, dialog focus traps, SPA route focus, focus-visible patterns
- [ARIA Patterns](references/aria-patterns.md) — Accessible tabs, live regions, data tables with ARIA attributes
- [Forms and Validation](references/forms-validation.md) — Label association, error announcement, redundant entry, accessible authentication
- [Color and Media](references/color-and-media.md) — Contrast requirements, reduced motion, dragging alternatives, video captions, alt text
- [Testing](references/testing.md) — Keyboard testing, screen reader pairings, axe DevTools, jest-axe and vitest-axe unit tests
