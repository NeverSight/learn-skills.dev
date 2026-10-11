---
name: frontend-excellence
description: Holistic, framework-agnostic playbook for shipping ultra-fast, accessible, search-friendly, visually distinctive web interfaces. Combines Lighthouse mastery (target 95+ mobile, 99+ desktop, 100 A11y/BP/SEO), UI/UX patterns drawn from Apple HIG and Material Design, design aesthetics that avoid generic AI styling, plus deep guidance on performance, accessibility, SEO, motion, forms, layout, and data visualization. Apply this when building, reviewing, refactoring, or polishing any web UI regardless of framework (vanilla HTML/CSS/JS, React, Vue, Svelte, Astro, Solid, Next.js, Nuxt, SvelteKit, Remix, Qwik, Lit, Web Components). Use to make decisions about typography, color, spacing, motion, contrast, semantic structure, asset loading, render strategy, hydration, third-party scripts, image formats, font loading, JS budgets, CSS architecture, ARIA, keyboard flows, focus management, structured data, meta tags, and Core Web Vitals.
---

# Frontend Excellence

A single, holistic skill for delivering web interfaces that look unforgettable, perform near the top of the Lighthouse curve, and degrade gracefully across devices and assistive technologies. Framework-agnostic by design: every rule is expressed as a principle plus a concrete check, never as a library API.

## When to Use

Apply this skill any time the work changes how an interface **looks, feels, moves, loads, ranks, or is interacted with**. Examples:

- Building or refactoring any page, form, modal, navigation, table, chart, or component
- Choosing typography, color, spacing, motion, or visual style
- Auditing or improving Core Web Vitals (LCP, INP, CLS), bundle size, or hydration cost
- Auditing or improving accessibility (contrast, keyboard, screen reader, focus, dynamic type)
- Auditing or improving on-page SEO (titles, descriptions, headings, structured data, canonicals)
- Reviewing visual polish, hierarchy, contrast, density, dark/light mode parity
- Replacing generic AI-flavored styling with a distinctive aesthetic direction
- Auditing or polishing an existing multi-page site against a reference design or production baseline

Skip this skill for backend logic, infrastructure, data pipelines, or non-visual scripting.

## Loading policy (read before pulling references)

Each file under `references/` averages 400 to 600 lines. Loading more than three at once burns context for content you do not need. Pick the 2 to 3 files that match the current task by reading the Routing tables below (By Task, By Symptom, then Reference Index). If a table does not resolve cleanly, read the YAML frontmatter at the top of candidate files (about 15 lines each, via `head -20`) before loading the rest. Drop a reference when the current task no longer matches its purpose.

## North Star Targets

Every interface should meet these bars before being considered "done". Treat any failure as a blocking defect, not a polish task.

| Category | Mobile target | Desktop target | Source |
|----------|--------------|----------------|--------|
| Lighthouse Performance | >= 95 | >= 99 | Lighthouse |
| Lighthouse Accessibility | 100 | 100 | Lighthouse + axe |
| Lighthouse Best Practices | 100 | 100 | Lighthouse |
| Lighthouse SEO | 100 | 100 | Lighthouse |
| Largest Contentful Paint (LCP) | < 2.5s | < 2.0s | Core Web Vitals |
| Interaction to Next Paint (INP) | < 200ms | < 200ms | Core Web Vitals |
| Cumulative Layout Shift (CLS) | < 0.1 | < 0.05 | Core Web Vitals |
| Time to First Byte (TTFB) | < 800ms | < 600ms | Core Web Vitals |
| First Contentful Paint (FCP) | < 1.8s | < 1.0s | Lighthouse |
| Total Blocking Time (TBT) | < 200ms | < 100ms | Lighthouse |
| Initial JS payload (gzipped) | < 90 KB | < 130 KB | Budget |
| Initial CSS payload (gzipped) | < 25 KB | < 35 KB | Budget |
| Web font payload (per screen) | <= 2 families, <= 4 weights | same | Budget |

These are the universal bar. A given project may consciously relax a budget for a specific surface (e.g., a heavily interactive client-rendered tool that legitimately ships more JS), but the relaxation should be a recorded, justified exception, not a default.

## Priority Stack (read top-down on any review)

1. **Crawlability and indexability** (does the page exist in the index, with the right canonical and meta?)
2. **Accessibility correctness** (semantic HTML, contrast, keyboard, focus, screen reader)
3. **Core Web Vitals** (LCP, INP, CLS, TTFB)
4. **Layout and responsive integrity** (no horizontal scroll, no clipped content, safe-area respect)
5. **Visual hierarchy and intentional aesthetic** (typography, color, spacing, motion, density)
6. **Interaction quality** (hover, press, focus, loading, error, empty, success states)
7. **Forms and feedback** (validation, error placement, recovery, autofill, autosave)
8. **Motion and animation** (purposeful, reduced-motion safe, transform-only)
9. **Data and charts** (legible, accessible, responsive)
10. **Polish and craft** (icon discipline, dark/light parity, brand fidelity)

Higher-priority items always block lower-priority items. Never trade contrast for aesthetics. Never trade INP for animation.

### When rules conflict (tie-breakers)

The Priority Stack covers the common case. Use this table when two specific rules push the other way:

| Conflict | Tie-breaker |
|---|---|
| Animation polish vs INP budget | INP wins. An animation that drives INP over 200ms is a defect, not a polish item. |
| Aesthetic preference vs WCAG contrast | Contrast wins. No 3:1 large-text or 4.5:1 body floor is negotiable for visual taste. |
| LCP preload vs initial JS budget | JS budget wins. Find a smaller LCP element or defer the preload; do not blow the budget. |
| SSR for SEO vs INP under hydration cost | Split: SSR the shell for indexability, defer islands to keep INP under 200ms. |
| Motion polish vs `prefers-reduced-motion` | Reduced motion wins. Motion is the enhancement, not the baseline. |
| Brand color vs dark-mode text contrast | Use a lightened accent for text on dark surfaces; brand stays for backgrounds. See `design.md`. |

## Decision: Render Strategy

A page lands in one of five render strategies. Choose by these axes; deep treatment in `performance.md` and `seo.md`.

| If ... | Pick |
|---|---|
| Indexable, mostly static content, low personalisation, traffic spike resilient | **SSG** (static site generation) |
| Indexable, per-request personalisation, dynamic data, server has compute budget | **SSR** (server-side rendering), optionally streamed |
| Index not required, deeply interactive, app-shell experience, INP-sensitive | **CSR** (client-side rendering), with route-level code splitting |
| Indexable, partial personalisation, want SSG for the shell with revalidation | **ISR** (incremental static regeneration) |
| Mostly static + a few interactive widgets, want minimal JS | **Static plus islands** (partial hydration / resumability) |

Decision rule of thumb: indexability first (SSG / SSR / ISR for indexable surfaces); interactivity cost second (split into islands if SSR pages run over the JS budget); fall back to CSR only when index is not required and the app shell is the product.

## Routing: by task

Pick the row that matches what you have been asked to do. Load the named files first; pull others only if those files point you elsewhere.

| You are asked to ... | Load these files |
|---|---|
| Build a new page from scratch | [components.md](references/components.md), [design.md](references/design.md), [responsive.md](references/responsive.md), [performance.md](references/performance.md) |
| Audit an existing site against a reference | [audit-workflow.md](references/audit-workflow.md), [defects.md](references/defects.md), [design.md](references/design.md) |
| Fix a failing Lighthouse audit | [lighthouse.md](references/lighthouse.md), [performance.md](references/performance.md), [debug-recipes.md](references/debug-recipes.md) |
| Polish visual quality on an existing page | [design.md](references/design.md), [ui-ux.md](references/ui-ux.md), [defects.md](references/defects.md) |
| Add a form or sign-in flow | [forms.md](references/forms.md), [auth.md](references/auth.md), [accessibility.md](references/accessibility.md) |
| Set up CI gates and pre-merge checks | [testing.md](references/testing.md), [lighthouse.md](references/lighthouse.md), [observability.md](references/observability.md) |
| Diagnose a production issue | [observability.md](references/observability.md), [debug-recipes.md](references/debug-recipes.md), [defects.md](references/defects.md) |
| Verify a page is done before shipping | [pre-launch.md](references/pre-launch.md), [quick-reference.md](references/quick-reference.md) |
| Internationalise or localise a surface | [i18n.md](references/i18n.md), [responsive.md](references/responsive.md), [accessibility.md](references/accessibility.md) |
| Harden security (CSP, headers, Trusted Types, SRI) | [security.md](references/security.md), [lighthouse.md](references/lighthouse.md), [pre-launch.md](references/pre-launch.md) |
| Add PWA, offline, or installability | [pwa-offline.md](references/pwa-offline.md), [performance.md](references/performance.md) |
| Embed third-party widgets or be embedded | [embed-patterns.md](references/embed-patterns.md), [security.md](references/security.md), [auth.md](references/auth.md) |
| Print stylesheet or transactional email HTML | [print-email.md](references/print-email.md) |
| Add charts, tables, or data display | [data-viz.md](references/data-viz.md), [ui-ux.md](references/ui-ux.md), [accessibility.md](references/accessibility.md) |
| Add or refine motion and animation | [motion.md](references/motion.md), [performance.md](references/performance.md) |
| Review a change against known anti-patterns | [anti-patterns.md](references/anti-patterns.md), [defects.md](references/defects.md) |

## Routing: by symptom

Use observable problem signals to jump straight to the relevant file and section.

| Symptom | Likely root, file and section to load |
|---|---|
| LCP > 2.5s, LCP regression | preload / fetchpriority / hydration cost: [performance.md: Core Web Vitals](references/performance.md#core-web-vitals) |
| INP > 200ms, slow interaction | long task / handler / hydration: [performance.md: Core Web Vitals](references/performance.md#core-web-vitals), [debug-recipes.md: INP regression](references/debug-recipes.md#inp-regression) |
| CLS > 0.1, layout jump | async element not reserved: [performance.md: Core Web Vitals](references/performance.md#core-web-vitals), [defects.md: Defect Lookup Table](references/defects.md#defect-lookup-table) |
| font swap CLS | missing size-adjust / metrics-override on the fallback: [debug-recipes.md: Font-swap CLS](references/debug-recipes.md#font-swap-cls), [performance.md: Font Strategy](references/performance.md#font-strategy) |
| Lighthouse SEO < 100 | noindex on a graded page, missing canonical: [lighthouse.md: Failing Audit to Fix Map](references/lighthouse.md#failing-audit-to-fix-map), [seo.md: Indexability](references/seo.md#indexability) |
| Lighthouse Best Practices < 100 | CSP violation, console errors, deprecation: [lighthouse.md: Failing Audit to Fix Map](references/lighthouse.md#failing-audit-to-fix-map), [security.md: CSP at Depth](references/security.md#csp-at-depth) |
| errors-in-console, stale SRI beacon | third-party beacon CORS / stale pinned hash, or a client-blocker false positive: [debug-recipes.md: Lighthouse flake triage](references/debug-recipes.md#lighthouse-flake-triage) |
| phantom dev failure (low score only on the dev server) | scoring the dev server, not a production build: [lighthouse.md: Run Lighthouse Properly](references/lighthouse.md#run-lighthouse-properly) |
| image too small on retina (image-size-responsive) | largest srcset candidate below CSS width times DPR: [responsive.md: Responsive Images](references/responsive.md#responsive-images), [lighthouse.md: Failing Audit to Fix Map](references/lighthouse.md#failing-audit-to-fix-map) |
| contrast fail, especially after a build change | low ratio, or a CSS-delivery change that reordered the cascade: [accessibility.md: Color and Contrast](references/accessibility.md#color-and-contrast), [lighthouse.md: Failing Audit to Fix Map](references/lighthouse.md#failing-audit-to-fix-map) |
| duplicate id | reused component with a hardcoded id: [components.md: Drift Detection](references/components.md#drift-detection) |
| scroll lock side shift | modal missing scrollbar-width compensation: [ui-ux.md: Modals and Overlays](references/ui-ux.md#modals-and-overlays), [defects.md: Defect Lookup Table](references/defects.md#defect-lookup-table) |
| hydration mismatch | server vs client divergence: [debug-recipes.md: Hydration mismatch](references/debug-recipes.md#hydration-mismatch), [performance.md: JavaScript Strategy](references/performance.md#javascript-strategy) |
| viewport overflow, horizontal scroll | bleed in a child element: [responsive.md: Horizontal Scroll: Forbidden](references/responsive.md#horizontal-scroll-forbidden), [defects.md: Defect Lookup Table](references/defects.md#defect-lookup-table) |
| focus trap leak, focus not visible | overlay focus management: [debug-recipes.md: Focus trap leak](references/debug-recipes.md#focus-trap-leak), [accessibility.md: Keyboard](references/accessibility.md#keyboard) |
| third-party script slow, analytics blocking | third-party-script discipline / async-defer matrix: [performance.md: Third-Party Strategy](references/performance.md#third-party-strategy), [build-hygiene.md: Dependency-Cost Discipline](references/build-hygiene.md#dependency-cost-discipline) |
| broken on Firefox / Safari only | feature-support assumption, missing fallback: [responsive.md: Media Preferences](references/responsive.md#media-preferences), [motion.md: Reduced Motion](references/motion.md#reduced-motion) |
| consent banner CLS, bounding box jumps | overlay not reserved: [ui-ux.md: Modals and Overlays](references/ui-ux.md#modals-and-overlays), [seo.md: Indexability](references/seo.md#indexability) |
| aria-hidden background still announced, inert leak | overlay applied to the wrong ancestor: [accessibility.md: Modal and Dialog](references/accessibility.md#modal-and-dialog), [ui-ux.md: Modals and Overlays](references/ui-ux.md#modals-and-overlays) |
| hero animation regresses LCP or TBT | above-the-fold motion not gated against a budget: [motion.md: Hero Animations](references/motion.md#hero-animations) |

## Reference Index

Detailed guidance lives in `references/`. Each row gives a one-line purpose plus the keywords that should pull the file.

| File | Use when (keywords) |
|------|---------|
| [lighthouse.md](references/lighthouse.md) | Lighthouse, audit, score, CI gate, csp-xss, duplicate-id, is-crawlable, score variance, user-flow |
| [performance.md](references/performance.md) | LCP, INP, CLS, TTFB, performance, hydration, bundle, BFCache, Speculation Rules, Early Hints, fetchpriority, render strategy, SSR, SSG, CSR, third-party script, list virtualization |
| [accessibility.md](references/accessibility.md) | a11y, WCAG, ARIA, screen reader, keyboard, focus, contrast, forced colors, reduced motion, dynamic type |
| [seo.md](references/seo.md) | SEO, canonical, sitemap, robots, structured data, JSON-LD, AEO, GEO, llms.txt, hreflang, Open Graph |
| [ui-ux.md](references/ui-ux.md) | UI, UX, modal, popover, dialog, drawer, menu, tooltip, breadcrumb, touch target, hit target, popover API, inert |
| [design.md](references/design.md) | design, typography, color, OKLCH, P3, dark mode, brand, variable font, @layer |
| [responsive.md](references/responsive.md) | responsive, breakpoint, container query, viewport, safe area, dvh, srcset, subgrid, scrollbar-gutter |
| [motion.md](references/motion.md) | motion, animation, transition, easing, View Transitions, scroll-driven, WAAPI, @starting-style |
| [forms.md](references/forms.md) | form, validation, input, autofill, autocomplete, constraintValidation |
| [data-viz.md](references/data-viz.md) | chart, data viz, axis, legend, Canvas, SVG, WebGL, timezone |
| [pre-launch.md](references/pre-launch.md) | pre-launch, checklist, ship, gate, verification, evidence |
| [audit-workflow.md](references/audit-workflow.md) | audit, route, sweep, baseline, capture, polish, multi-page |
| [components.md](references/components.md) | component, contract, extraction, slots, composition, tokens, Storybook |
| [defects.md](references/defects.md) | defect, geometry, sweep, threshold, regression, lookup |
| [security.md](references/security.md) | CSP, COOP, COEP, CORP, cross-origin isolation, Trusted Types, SRI, Permissions-Policy, Referrer-Policy, supply chain |
| [observability.md](references/observability.md) | RUM, observability, monitoring, source maps, error capture, INP attribution, Reporting API, CrUX, LoAF |
| [testing.md](references/testing.md) | testing, visual regression, axe-core, pa11y, size-limit, bundlesize, lighthouse-ci, contract test |
| [auth.md](references/auth.md) | auth, login, passkey, WebAuthn, OAuth, magic link, session, account recovery, CAPTCHA, Storage Access API |
| [debug-recipes.md](references/debug-recipes.md) | debug, recipe, hydration mismatch, layout overflow, focus trap, font-swap CLS, Lighthouse-flake |
| [anti-patterns.md](references/anti-patterns.md) | anti-pattern, what to avoid, mistake |
| [i18n.md](references/i18n.md) | i18n, l10n, locale, translation, Intl, plural rules, bidi, RTL, mirroring, hreflang |
| [pwa-offline.md](references/pwa-offline.md) | PWA, offline, service worker, install prompt, push, background sync, manifest |
| [build-hygiene.md](references/build-hygiene.md) | build, tree-shaking, sideEffects, lockfile, dead code, code splitting, dependency cost |
| [embed-patterns.md](references/embed-patterns.md) | embed, iframe, sandbox, postMessage, host, guest, third-party widget |
| [print-email.md](references/print-email.md) | print, email, @page, page-break, transactional email, Outlook |
| [quick-reference.md](references/quick-reference.md) | rule, quick reference, highest leverage |

## Workflow

### 1. Frame the work

Before writing code, capture: audience and intent; indexability (search-indexed surface vs auth wall); aesthetic direction (one bold lane; refuse "Inter on white with a purple gradient"); constraints (render strategy from the table above, hydration model, browser support floor, locale, writing direction).

The rendered browser is the source of truth at every phase. Do not judge visual quality from code alone; capture screenshots, compare against the reference, fix, and re-capture. When the work is auditing or polishing an existing multi-page site rather than building new, switch to the Multi-Page Polish Loop below.

### 2. Plan the structure

One H1 per page; sequential headings. Land the LCP element in the first viewport (a real, served asset with declared dimensions, not lazy-loaded, not behind hydration). Reserve space for every async element (`aspect-ratio`, fixed height, skeleton). Decide which sections are server-rendered, which are streamed, which are deferred, which are client-only; justify every client-only choice.

### 3. Build with budgets

Declare and verify per surface: JS payload (initial route, gzipped); CSS payload (initial route, gzipped); image payload (above the fold); font budget (families, weights, subsets, byte total); third-party script budget (count, total ms of main-thread time). Reject any addition that breaks a budget without an explicit, recorded waiver.

### 4. Verify

Run the full Lighthouse + axe + visual + responsive + dark-mode + reduced-motion + keyboard + screen-reader pass before declaring the work complete. See [pre-launch.md](references/pre-launch.md).

## Multi-Page Polish Loop

When the work is auditing or polishing an existing multi-page site, **read [audit-workflow.md](references/audit-workflow.md) first** for the full procedure (operating rules, capture script, per-phase detail, final acceptance gate). The 19 phases index:

1. Discover context. 2. Inventory routes. 3. Inventory repeated widgets. 4. Capture baseline. 5. Capture reference. 6. Audit each route. 7. Prioritise fixes. 8. Patch with component discipline. 9. Patch with design discipline. 10. Verify after every fix group. 11. Programmatic geometry checks (and content-and-markup sweep). 12. Component drift checks. 13. Interaction QA. 14. Accessibility validation. 15. Lighthouse and performance polish. 16. Reference-level design heuristics. 17. Common defects and fixes. 18. Deliverables. 19. Final acceptance gate.

Component extraction discipline lives in [components.md](references/components.md); defect lookup and the geometry sweep in [defects.md](references/defects.md).

## Quick Reference

The highest-leverage rules across performance, accessibility, SEO, UI/UX, design, and multi-page consistency live in [references/quick-reference.md](references/quick-reference.md). Open that file when you want a single condensed view to scan against a change.

## Skill freshness

This skill encodes web-platform behaviour at a point in time. Before applying an old rule, double-check it is still current when:

- The rule cites a Lighthouse audit ID, weight, or category cutoff (Lighthouse rebalances categories every few releases).
- The rule cites a browser-support floor (Baseline status moves; check caniuse.com or the MDN Baseline widget).
- The rule cites a specific Core Web Vitals threshold or metric name (INP replaced FID in 2024; thresholds are revisited).
- The rule names a CSS or JS API ([`@layer`, View Transitions, Anchor Positioning, Popover, `:has()`] all changed support between 2023 and 2026).

See [CHANGELOG.md](CHANGELOG.md) for the dated history of additions and refinements.

## Self-Improvement

After applying this skill, before declaring work complete:

- Did Lighthouse run on real production builds (not dev mode) with throttled mobile and desktop presets?
- Did axe (or equivalent) run with zero violations on every changed page?
- Did the page render correctly at 320px, 375px, 768px, 1024px, 1280px, and 1920px?
- Did the page render correctly in light and dark mode independently (not by CSS-inverting one)?
- Did the page render correctly with `prefers-reduced-motion: reduce`?
- Did the page work end-to-end with keyboard only?
- Did the page survive a screen reader pass (VoiceOver or NVDA) for the primary task?
- Did the LCP element ship with `fetchpriority="high"`, declared dimensions, and a real served asset?
- Did all custom fonts load with `font-display` set, and is the count <= 2 families / 4 weights?
- Did every async section reserve space?
- Did every interactive element have visible focus and meet contrast?
- Did the page expose unique title, description, canonical, OG, Twitter, and (where applicable) JSON-LD?
- Did you verify the SHIPPED build output (copied headers, static files, generated images), not just the source config?

For multi-page audit and polish work, also confirm:

- Was a widget inventory built for every shared family (header, hero, section, CTA, card, media, list, interactive, empty, legal, 404)?
- Were baseline screenshots captured at `1440x900` and `375x812` before any edits?
- Were after screenshots captured at `1440x900` and `375x812` for every changed route?
- Did the geometry sweep return zero issues on every audited route at both viewports?
- Did you run BOTH programmatic sweeps (geometry, and content-and-markup) on every route?
- Did the drift collector return no unexplained differences for any shared widget family?
- Was a per-route audit table (issues found, fixes applied, before, after) delivered with the change?

If any answer is "no" or "not checked", the work is not done.
