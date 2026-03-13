---
name: web-guidelines
description: Use when designing, reviewing, or implementing web UIs and you need concrete MUST/SHOULD/NEVER rules for accessibility, interaction patterns, forms, layout, animation, performance, content, or visual design decisions. Also use when asked to "review my UI", "check accessibility", or "audit design".
---

# Web Interface Guidelines

Concise rules for building accessible, fast, delightful UIs. Use MUST/SHOULD/NEVER to guide decisions and reviews.

## How to Apply

- Prioritize MUST items first; NEVER items are hard constraints.
- When reviewing, scan each section and confirm every MUST is satisfied.
- If a guideline conflicts with product requirements, surface the conflict explicitly.
- For the latest upstream rules, fetch from: `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`

## Quick Reference

| Area | Top MUST checks |
| --- | --- |
| Keyboard | Full keyboard support per WAI-ARIA APG; visible focus rings; manage focus (trap/move/return) |
| Forms | No paste blocking; loading buttons keep label + spinner; inline errors + focus first error |
| Navigation | URL reflects state; links are links; back/forward restores scroll |
| Motion | Respect prefers-reduced-motion; animate transform/opacity only; animations interruptible |
| Layout | Respect safe areas; avoid unwanted scrollbars; verify mobile/laptop/ultra-wide |
| Content | Accurate labels; skip link + proper headings; resilient to long user content |
| Performance | Measure reliably; batch layout reads/writes; prevent CLS from images |

## Interactions

- Keyboard
  - MUST: Full keyboard support per [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/) patterns
  - MUST: Visible focus rings (`:focus-visible`; group with `:focus-within`)
  - MUST: Manage focus (trap, move, and return) per APG patterns
- Targets & input
  - MUST: Hit target >= 24px (mobile >= 44px). If visual < 24px, expand hit area.
  - MUST: Mobile `<input>` font-size >= 16px or set viewport `maximum-scale=1`
  - NEVER: Disable browser zoom
  - MUST: `touch-action: manipulation` to prevent double-tap zoom
- Inputs & forms
  - MUST: Hydration-safe inputs (no lost focus/value)
  - NEVER: Block paste in `<input>/<textarea>`
  - MUST: Loading buttons show spinner and keep original label
  - MUST: Enter submits text input; Cmd/Ctrl+Enter submits textarea
  - MUST: Errors inline next to fields; on submit, focus first error
  - MUST: `autocomplete` + meaningful `name`; correct `type` and `inputmode`
  - MUST: Warn on unsaved changes before navigation
  - MUST: Compatible with password managers and 2FA
  - MUST: No dead zones on checkboxes/radios
- State & navigation
  - MUST: URL reflects state (deep-link filters/tabs/pagination)
  - MUST: Back/Forward restores scroll
  - MUST: Links are links: `<a>`/`<Link>` for navigation (support Cmd/Ctrl/middle-click)
- Feedback
  - SHOULD: Optimistic UI; reconcile on response
  - MUST: Confirm destructive actions or provide Undo
  - MUST: Use polite `aria-live` for toasts/inline validation
- Touch/drag/scroll
  - MUST: `overscroll-behavior: contain` in modals/drawers
  - MUST: During drag, disable text selection and set `inert`

## Animation

- MUST: Honor `prefers-reduced-motion`
- SHOULD: Prefer CSS > Web Animations API > JS libraries
- MUST: Animate compositor-friendly props (`transform`, `opacity`); avoid layout props
- MUST: Animations are interruptible and input-driven
- MUST: Correct `transform-origin`

## Layout

- SHOULD: Optical alignment; adjust ±1px when perception beats geometry
- MUST: Verify mobile, laptop, ultra-wide
- MUST: Respect safe areas (`env(safe-area-inset-*)`)
- MUST: Avoid unwanted scrollbars

## Content & Accessibility

- MUST: `<title>` matches current context
- MUST: No dead ends; always offer next step/recovery
- MUST: Tabular numbers for comparisons (`tabular-nums`)
- MUST: Redundant status cues (not color-only); icons have text labels
- MUST: `scroll-margin-top` on headings; "Skip to content" link; hierarchical headings
- MUST: Resilient to user-generated content (short/avg/very long)
- MUST: Icon-only buttons have descriptive `aria-label`
- MUST: Prefer native semantics before ARIA

## Performance

- MUST: Batch layout reads/writes; avoid unnecessary reflows
- MUST: Virtualize large lists
- MUST: Preload above-fold images; lazy-load the rest
- MUST: Prevent CLS from images (explicit dimensions)
- SHOULD: Prefer uncontrolled inputs; make controlled loops cheap

## Design

- SHOULD: Layered shadows (ambient + direct)
- SHOULD: Nested radii: child <= parent; concentric
- MUST: Meet contrast (prefer APCA over WCAG 2)
- MUST: Increase contrast on `:hover`/`:active`/`:focus`

## Example: Loading Submit Button

```tsx
export function SubmitButton({ pending, errorId }: { pending: boolean; errorId?: string }) {
  return (
    <button type="submit" aria-describedby={errorId} aria-busy={pending} disabled={pending}>
      {pending ? (
        <span aria-live="polite">
          <span className="spinner" aria-hidden="true" />
          Saving…
        </span>
      ) : "Save"}
    </button>
  );
}
```

## Common Mistakes

- Missing focus management in dialogs (no trap/return)
- Blocking paste in inputs or disabling zoom
- Loading states that replace labels instead of adding spinner
- Links implemented as buttons (breaks Cmd/Ctrl click)
- Animating layout properties instead of `transform`/`opacity`
- Icons without accessible labels
