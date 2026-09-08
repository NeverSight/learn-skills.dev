---
name: frontend-designer
description: "Trigger: frontend design, CSS architecture, tokens, responsive UI, accessibility, motion. Produce production UI design systems."
license: Apache-2.0
metadata:
  author: kozz36
  version: "3.0.1"
---

## Activation Contract

Use this skill for frontend design-system decisions when an agent must choose, review, or document production-ready technical direction.

- Designing or reviewing UI systems, component anatomy, tokens, layout, or visual interaction.
- Choosing CSS architecture, responsive behavior, accessibility constraints, or motion rules.
- Converting a repository's visual direction into implementation-ready frontend guidance.

Do not use this skill for generic explanation, copy editing, or one-off code changes that do not affect architecture or reusable implementation patterns.

## Hard Rules

- Preserve the repository's token and component-state contracts; do not hardcode isolated visual decisions.
- Use semantic HTML and native controls before ARIA substitutes. Define keyboard behavior, visible focus, measurable contrast, and reduced-motion behavior for interactive UI.
- Keep responsive components reusable, reserve layout space for media and fonts, and avoid performance regressions without evidence that the tradeoff is acceptable.
- Keep the main answer decision-first; move deep rationale to local references instead of long inline prose.
- Verify new version, browser, API, legal, or adoption claims before adding them to changelogs or decision guidance.

## Decision Gates

| Evidence to inspect | Decision |
|---|---|
| Repository-native CSS architecture, naming, linting, build pipeline, and team conventions | Preserve the established paradigm. Introduce layers, CSS Modules, CSS-in-JS, utilities, or a naming convention only when the repository supports it and migration cost is accepted. |
| Existing `Design.md`, `design.md`, design-token source, or approved design tool | Treat it as the source of visual truth when present. Do not require a particular filename, generate a handoff file, or assume an external design tool. |
| Supported browser matrix and fallback policy | Gate container queries, nesting, `:has()`, `light-dark()`, scroll-driven animation, and other platform features on that matrix; define a fallback when required. |
| Approved token contract plus browser/build support | When the contract selects OKLCH, keep newly specified tokens OKLCH-only. Do not force a legacy color-format migration without an approved cost and compatibility plan. |
| Product theme requirements and design source | Use dark-mode-first only when the product and source require it; otherwise preserve the existing theme strategy and semantic token behavior. |
| Component reuse, page topology, content, and viewport requirements | Prefer container queries for reusable components when supported; use viewport media queries, mobile-first, desktop-first, or composition when they fit the repository and product. |
| Accessibility scope and measurable acceptance criteria | Preserve semantic HTML, keyboard access, focus visibility, contrast measurement, touch-target requirements, and reduced-motion behavior. Apply jurisdiction-specific requirements only when the product scope establishes them. |
| Performance evidence, budgets, and delivery path | Use containment, `content-visibility`, image formats, font loading, and animation techniques only when compatible with the browser matrix and supported by measured or stated performance goals. |
| Installed repository tooling and approved execution environment | Run a repository-native validation command when available. Do not prescribe `npx`, a browser audit, encoding, or design-tool command when the dependency, target, permission, or evidence is unavailable. |

## Execution Steps

1. Identify the repository architecture, design source, browser matrix, accessibility scope, performance evidence, team conventions, tooling availability, and migration cost.
2. Define or preserve token, state, semantic HTML, focus, contrast, and reduced-motion contracts before choosing visual novelty.
3. Select the smallest compatible CSS, layout, component, theme, and motion approach; record needed fallbacks and rejected alternatives.
4. Read `references/technical-reference.md` only when detailed decision matrices, examples, safeguards, or command prerequisites are needed.
5. State the chosen pattern, evidence, runtime risks, fallback or migration plan, and validation path. Add changelog claims only when verified.

## Output Contract

Return:

- Recommended decision, repository evidence, and why it fits.
- Alternatives rejected with concrete tradeoffs, including migration cost where relevant.
- Accessibility, browser, performance, and runtime risks with mitigations or fallbacks.
- Validation steps that are available in the repository, or the evidence still needed before adoption.

## References

- `references/technical-reference.md` — curated technical basis and conditional decision guidance for v3.0.1.
- `references/source-index.md` — source pointers and verification rules for version-sensitive claims.
