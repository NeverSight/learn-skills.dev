---
name: pwa-user-simulation
description: "Simulate real user journeys through a PWA using browser automation MCPs (Playwright MCP + Chrome DevTools MCP). Combines SXO (Search eXperience Optimization), neuro-ergonomic heuristics, WCAG 2.2 AA checks, and Core Web Vitals analysis via structured accessibility snapshots and visual screenshots. Triggers on: simulate user, user journey, PWA test, SXO audit, UX walkthrough, browser automation, e2e exploration, user simulation, test the app, parcourir comme un utilisateur, tester le flow, vérifier le parcours."
---

# PWA User Simulation Skill

Simulate real user journeys through a web application using Playwright MCP (accessibility tree, structured navigation, assertions) and Chrome DevTools MCP (visual screenshots, DOM inspection, JS evaluation). Produce structured reports with prioritized findings and actionable handoff recommendations.

## When to Load References

- **Persona definitions** → load `references/personas.md`
- **SXO audit checklist** → load `references/sxo-checklist.md`
- **MCP tools usage guide** → load `references/mcp-tools-guide.md`
- **Journey report template** → copy from `assets/journey-report.md`

---

## Simulation Protocol (3 Phases)

### Phase 1 — Bootstrap & Discovery

1. Verify the app is running (`browser_navigate` to `$BASE_URL` or `http://localhost:3000`)
2. Take an initial screenshot (Chrome DevTools `take_screenshot`) + accessibility snapshot (Playwright `browser_snapshot`) to confirm the landing state
3. Load the selected persona from `references/personas.md`
4. List all navigable routes visible from the current page (links, nav items, CTAs)

### Phase 2 — Route-by-Route Exploration

For **each route** in the persona's journey:

1. **Navigate** — use Playwright `browser_navigate` (structured, token-efficient) or Chrome DevTools `navigate_page` (if vision/screenshot needed)
2. **Snapshot** — take an accessibility snapshot (`browser_snapshot`) to read the page structure as an accessibility tree
3. **Screenshot** — take a visual screenshot (`take_screenshot`) to capture visual state. Do this at every significant state change: page load, form interaction, modal open, error state, loading state, hover state
4. **Interact** — simulate user actions: click CTAs (`browser_click`), fill forms (`browser_type`), submit, navigate back, toggle dark mode, resize viewport
5. **Analyze** — for each state, evaluate against the SXO checklist (load `references/sxo-checklist.md`):
   - Cognitive load: too many elements? Clear visual hierarchy?
   - Affordances: are interactive elements obviously clickable?
   - Navigation depth: how many clicks to reach the goal?
   - Error handling: what happens on wrong input or 401/404/500?
   - Loading states: are there skeletons or spinners?
   - Responsiveness: does the layout adapt to mobile viewport?
6. **Log** — record each finding with severity (P0/P1/P2), affected route, screenshot reference, and recommended handoff target

### Phase 3 — Synthesis & Report

1. Compile all findings using the template from `assets/journey-report.md`
2. Group by severity: P0 (blocking UX), P1 (significant friction), P2 (polish)
3. For each finding, specify:
   - The affected component/route
   - A description with screenshot reference
   - Recommended fix approach
   - Handoff target: **UI** (design/component issues), **Backend** (API errors, data problems), **Review** (quality gate, patterns)
4. Provide an overall SXO score (0-100) based on the checklist

---

## MCP Tool Selection Guide

| Task | Playwright MCP | Chrome DevTools MCP |
|------|---------------|-------------------|
| Navigate to URL | `browser_navigate` ✅ | `navigate_page` |
| Read page structure | `browser_snapshot` ✅ (accessibility tree) | `take_snapshot` (DOM) |
| Visual screenshot | `browser_screenshot` (with `--caps=vision`) | `take_screenshot` ✅ |
| Click element | `browser_click` ✅ (by ref from snapshot) | `click` (by selector) |
| Type text | `browser_type` ✅ | `fill` |
| Evaluate JS | — | `evaluate_script` ✅ |
| Check console errors | `browser_console_messages` | `get_console_message` |
| Network monitoring | — | `get_network_request` |
| Run assertions | `browser_snapshot` + logic (with `--caps=testing`) | — |
| Emulate device | `--device` flag | `emulate` |

**Default strategy:** Use Playwright for navigation + interaction (token-efficient, structured). Use Chrome DevTools for screenshots + JS evaluation + network inspection (vision-powered, pixel-level).

---

## Key Principles

1. **Think like a user, not a developer** — navigate via visible UI elements, not code knowledge
2. **Screenshot at every state change** — page load, interaction, error, success, loading
3. **Accessibility-first exploration** — the accessibility tree reveals what screen readers see
4. **Mobile-first** — always test the smallest viewport first (390×844), then desktop (1920×1080)
5. **Feature flags awareness** — check which features are enabled/disabled and test both states
6. **No code editing** — this skill is read-only/browser-only. Findings lead to handoffs, not direct fixes
7. **Structured reporting** — every finding must be actionable with a clear handoff target

---

## Anti-Patterns to Detect

- ❌ Click targets < 44×44px on mobile
- ❌ Missing loading states (content flash, layout shift)
- ❌ Forms without validation feedback
- ❌ Navigation dead-ends (no back button, no breadcrumbs)
- ❌ Inconsistent visual hierarchy (competing CTAs)
- ❌ Missing error handling (white screen on 500, generic "Error")
- ❌ Animations without `prefers-reduced-motion` guard
- ❌ Contrast ratio < 4.5:1 on body text
- ❌ No focus indicators on interactive elements
- ❌ Orphan pages (unreachable from main navigation)
