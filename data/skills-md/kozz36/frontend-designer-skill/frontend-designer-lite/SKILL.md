---
name: frontend-designer-lite
description: "Trigger: frontend design, CSS architecture, tokens, responsive UI, accessibility, motion. Produce production UI design-system decisions without local references."
license: Apache-2.0
metadata:
  author: kozz36
  version: "3.0.1"
---

## Activation Contract

Use this standalone skill for frontend design-system decisions when an agent must choose, review, or document production-ready technical direction.

- Designing or reviewing UI systems, component anatomy, tokens, layout, or visual interaction.
- Choosing CSS architecture, responsive behavior, accessibility constraints, or motion rules.
- Converting repository visual direction into implementation-ready frontend guidance.

Do not use it for generic explanation, copy editing, or one-off code changes that do not affect architecture or reusable implementation patterns.

## Non-Negotiable Runtime Rules

- Preserve repository token and component-state contracts; do not hardcode isolated visual decisions.
- Use semantic HTML and native controls before ARIA substitutes. Define native keyboard behavior, visible focus, measurable contrast, touch/pointer criteria, and reduced-motion behavior for every interactive UI.
- Keep components reusable and responsive; reserve media and font geometry and do not accept performance regressions without compatible evidence.
- Keep the answer decision-first. Do not add version, browser, API, accessibility-law, security, adoption, or legal-applicability claims without current authoritative verification.
- Treat security requirements as conditional product and repository inputs; do not infer controls, policy, telemetry, or external-tool permission when evidence is absent.

## Required Evidence Gates

Gather the following before selecting a pattern. If a required input is unavailable, stop and report the missing evidence rather than guessing or prescribing a universal stack.

- **Repository architecture and migration:** inspect existing CSS architecture, naming, linting, build pipeline, team conventions, and accepted migration cost. Preserve the established paradigm; introduce cascade layers, CSS Modules, CSS-in-JS, utilities, or naming conventions only with repository support and an accepted migration plan.
- **Design source:** inspect `Design.md`, `design.md`, token sources, a design-system package, design-tool export, or another approved source when present. Treat its case-sensitive path and token, semantic, component, and state contracts as local visual truth; reconcile conflicts with code and team conventions. Do not require a filename, rename a source, or assume a design tool.
- **Browser and fallback policy:** inspect the supported browser matrix before using CSS nesting, container queries, `:has()`, `light-dark()`, scroll-driven animation, WAAPI, observers, or related APIs. Define a compatible fallback when required.
- **Tokens, color, and themes:** preserve primitive, semantic, and component tiers or the local equivalent, including loading, disabled, error, success, and selected states. Use OKLCH-only for newly specified tokens only when the approved token contract and browser/build matrix select it; otherwise retain the compatible format. Measure every foreground/background and focus pair. Use dark-mode-first only when product requirements and the approved design source require it; otherwise preserve the existing semantic-token and theme mechanism.
- **Layout and components:** select component-local container queries only when supported and valuable; use viewport queries for document-level layout, navigation, or the established responsive system. Choose mobile-first, desktop-first, grid, flex, named areas, or composition from information architecture, content, component ownership, and viewport evidence. Use semantic structure: accessible names for regions when needed, native `<dialog>` when it fits policy, native table semantics for tabular data, explicit form labels/errors/order/states, and `<nav>` with list semantics where applicable. Reserve media geometry with `aspect-ratio`, dimensions, or an equivalent contract when it reduces measured layout shift.
- **Accessibility and motion:** preserve semantic HTML, labels, names, roles, states, keyboard order, persistent visible `:focus-visible`, unobscured focus, measurable contrast, and applicable touch-target criteria. Add ARIA only when native semantics cannot express the contract. Honor `prefers-reduced-motion` with equivalent low-motion or static feedback. Use the smallest motion mechanism and gate WAAPI, scroll-driven CSS, observers, and listeners on browser support, motion policy, and measured main-thread cost. Apply jurisdiction-specific obligations only when product scope establishes them.
- **Visual treatment and performance:** use bento-like grids, glass, gradients, bold type, dark-first presentation, or other trends only when the approved design source, hierarchy, contrast, focus, affordance, responsive behavior, browser matrix, and performance evidence support them. Use `content-visibility` or `contain` only after checking rendering and accessibility behavior and measuring the target. Use `will-change` transiently and only when profiling justifies it. Choose image/font formats, dimensions, loading, fallbacks, and metrics from the delivery pipeline, browser matrix, and layout-shift evidence.
- **Tooling:** run only repository-provided validation with an available dependency, target, permission, and expected evidence. Prefer documented package-manager scripts. Do not introduce implicit installs, external audits, encoding commands, or design-tool commands when prerequisites are absent.

## Live Verification Rules

- Do not add browser, API, accessibility-law, security, adoption, or version claims without checking a current authoritative source.
- A URL is a starting point, not proof that a feature fits the repository browser matrix, product scope, build pipeline, or fallback policy.
- Record verification date, source URL, scope, and confirmed behavior for every time-sensitive release or decision claim.
- Use the relevant authoritative source: W3C CSS specifications for syntax, MDN for browser-feature behavior, WCAG for applicable accessibility criteria, and the official regulator for jurisdictional applicability. Check OKLCH and delivery choices against the approved pipeline and browser policy rather than claiming universal support.

## Execution Order

1. Identify repository architecture, design source, browser matrix, accessibility and legal scope, performance evidence, team conventions, tooling availability, migration cost, and security constraints.
2. Stop for missing required evidence. Otherwise preserve token, state, semantic HTML, focus, contrast, reduced-motion, and media-geometry contracts before visual treatment.
3. Select the smallest compatible CSS paradigm, layout, component, token, theme, media, and motion approach. Record required fallbacks, migration steps, and rejected alternatives with their concrete tradeoffs.
4. Verify any time-sensitive version, browser, API, accessibility-law, security, adoption, or legal claim against current authoritative evidence before using it.
5. Run available repository-native validation and report unavailable validation as evidence still needed; do not invent a successful command or result.

## Output Contract

Return:

- The recommended pattern, repository and source evidence, and why it fits the established contracts.
- Rejected alternatives with concrete tradeoffs and migration cost where relevant.
- Accessibility, browser, performance, security, and runtime risks, with mitigations and compatible fallbacks.
- A fallback or migration plan, including conditions that require it.
- Validation output: commands actually available and their results, plus missing evidence or verification still required before adoption.
