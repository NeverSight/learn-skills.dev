---
name: ui-neuro-ergo
description: Autonomous neuro-ergonomic + a11y UI audit and iteration skill. Combines WCAG 2.2 AA standards, cognitive science principles (Fitts Law, CLT, Gestalt), and a Chrome DevTools MCP screenshot loop for production-ready delivery. Triggers on neuro ergo, a11y, accessibility audit, cognitive load, UX review, WCAG, ergonomie, accessibilite.
---

# UI Neuro-Ergo Skill

Autonomous workflow for neuro-ergonomic + accessible UI work with visual iteration via Chrome DevTools MCP.
Delivers production-ready results without requiring human intervention between iterations.

## Overview

This skill combines:

1. **Neuro-ergonomics** — cognitive science applied to UI: reduce friction, lower cognitive load, amplify signal
2. **Accessibility (WCAG 2.2 AA)** — inclusive design, screen reader support, keyboard navigation, contrast
3. **Visual Iteration Loop** — Chrome DevTools MCP screenshots for autonomous see→fix→verify cycles

## When to load references

- **Neuro-ergonomic principles** → load `references/neuro-ergo-principles.md`
- **WCAG 2.2 AA checklist** → load `references/a11y-checklist.md`
- **Chrome MCP iteration protocol** → load `references/iteration-protocol.md`

---

## Workflow

### Phase 1 — Audit

1. **Open Chrome DevTools MCP** → navigate to the target page
2. **Take screenshot** → capture current state (full page)
3. **Take a11y tree snapshot** (`take_snapshot`) → see ARIA roles, labels, structure
4. **Read the source code** → analyze component structure
5. **Run axe audit** via `evaluate_script`:
   ```js
   () => {
     // Check for basic a11y violations visible without axe
     const issues = [];
     // Missing alt on images
     document
       .querySelectorAll("img:not([alt])")
       .forEach((el) =>
         issues.push({ type: "img-no-alt", el: el.outerHTML.slice(0, 80) }),
       );
     // Buttons without accessible name
     document
       .querySelectorAll("button:not([aria-label]):not([aria-labelledby])")
       .forEach((b) => {
         if (!b.textContent.trim())
           issues.push({
             type: "button-no-name",
             el: b.outerHTML.slice(0, 80),
           });
       });
     // Inputs without label
     document
       .querySelectorAll("input:not([aria-label]):not([id])")
       .forEach((i) =>
         issues.push({ type: "input-no-label", el: i.outerHTML.slice(0, 80) }),
       );
     // animate-pulse without reduced motion guard
     document
       .querySelectorAll('[class*="animate-"]')
       .forEach((el) =>
         issues.push({ type: "animation-check", cls: el.className }),
       );
     return issues;
   };
   ```
6. **Compile audit report** with findings in 4 categories:
   - 🔴 Critical (WCAG A violations, blocking keyboard/SR users)
   - 🟠 Ergonomic (cognitive load, Fitts' Law, visual hierarchy)
   - 🟡 WCAG AA (contrast, live regions, target sizes)
   - 🟢 Polish (micro-interactions, motion, progressive disclosure)

### Phase 2 — Plan Fixes

Load `references/neuro-ergo-principles.md` and `references/a11y-checklist.md`.
For each finding, define the specific fix with exact code changes.
Prioritize: Critical → WCAG AA → Ergonomic → Polish.

### Phase 3 — Implement

Apply all changes to the source file(s). Stagger changes in logical groups if file is large:

1. Structure & ARIA (landmarks, roles, labels, live regions)
2. Keyboard & Focus (skip link, focus ring, tab order)
3. Cognitive load (chunking, visual hierarchy, reduced noise)
4. Motion & animation (`prefers-reduced-motion`, remove unnecessary pulse)
5. Contrast & sizing (text contrast, touch targets min 44×44px)

### Phase 4 — Visual Iteration

Reload the page and take before/after screenshots. Fix any regressions:

```
take_screenshot → analyze → find issues → fix code → navigate/reload → take_screenshot → ...
```

Iterate until:

- [ ] No critical a11y violations visible
- [ ] Visual hierarchy is clear (1 primary action per view, clear F-pattern scan path)
- [ ] All interactive elements have visible focus indicators
- [ ] Motion respects `prefers-reduced-motion`
- [ ] Skip navigation link present
- [ ] Live region announces filter results to screen readers
- [ ] Touch targets ≥ 44×44px on mobile viewport
- [ ] Headings form a logical outline (h1 → h2 → h3, no skips)

### Phase 5 — Production Checklist

Before declaring done, verify:

- [ ] TypeScript compiles without errors (`pnpm build` or check editor diagnostics)
- [ ] No arbitrary Tailwind values (`w-[...]`, `text-[...]`) — unless using CSS vars
- [ ] All `<button>` have accessible names
- [ ] All `<input>` have `<label>` or `aria-label`
- [ ] `<article>` elements have `aria-labelledby` pointing to their heading
- [ ] Dynamic count updates use `role="status"` or `aria-live="polite"`
- [ ] Animations wrapped in `motion-safe:` or `@media (prefers-reduced-motion: no-preference)`
- [ ] Color is not the only differentiator (icon+color, not color alone)

---

## Reference Files

Load these on demand:

- `references/neuro-ergo-principles.md` — cognitive science principles (CLT, Fitts' Law, Gestalt, Miller's Law, F-pattern)
- `references/a11y-checklist.md` — WCAG 2.2 AA checklist + JS audit script for React/Next.js
- `references/react-a11y-patterns.md` — copy-paste fix patterns (skip link, live region, article+aria-labelledby, radiogroup, motion guard, touch target)
- `references/iteration-protocol.md` — Chrome DevTools MCP tool sequence and iteration exit criteria
