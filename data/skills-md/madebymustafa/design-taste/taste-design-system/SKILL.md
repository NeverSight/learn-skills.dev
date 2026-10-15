---
name: taste-design-system
description: |
  Builds and audits design systems for agentic workflows: three-tier design tokens (primitive → semantic → component), W3C DTCG token format, spacing and type scales, color ramps, component anatomy, documentation, governance, and adoption metrics. Use when creating tokens, scaffolding a component library, or auditing an existing system for consistency. Stack on the design-taste core skill.
triggers:
  - "design system"
  - "design tokens"
  - "token architecture"
  - "component library"
  - "design system audit"
  - "design tokens file"
---

# taste-design-system

> A design system is a decision inventory. This skill tells the agent how to take that inventory, structure it, and keep it honest.

## 1. TOKEN ARCHITECTURE (Three Tiers, Never Two)

1. **Primitive tokens** — raw values: `--color-ink-900`, `--space-4`, `--radius-md`. No meaning beyond the value.
2. **Semantic tokens** — meaning, not value: `--color-surface`, `--color-text-muted`, `--color-border`, `--space-inset-lg`. Products consume semantic tokens ONLY.
3. **Component tokens** — per-component aliases: `--button-bg-primary`, `--button-radius`, `--input-border-width`. Components never reference primitives directly.

Rule: components → semantic → primitive → value. If any layer is skipped, the system will fork.

## 2. TOKEN FORMAT (DTCG, Not Freeform)

Write tokens as a flat key map (or W3C DTCG JSON if the stack supports it):

```css
--color-ink-900: #101014;
--color-ink-700: #3B3B40;
--color-accent: #E8540B;
--space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px;
--radius-sm: 2px; --radius-md: 6px; --radius-lg: 12px;
--font-display: 'Archivo', sans-serif; --font-body: 'Inter', sans-serif; --font-mono: 'JetBrains Mono', monospace;
```

Naming conventions: kebab-case, noun-first, scale-last (`--space-4`, `--color-ink-900`, `--radius-md`). Never encode intent in names ("fancy-purple"), never use hex colors directly in components.

## 3. THE INVENTORY (Audit Before You Build)

Run the inventory before building anything:

1. **Colors** — list every hex in the codebase. Flag any value not in the token set (>15 unique out-of-scheme colors = system is broken).
2. **Spacing** — flag any margin/padding not on the 4px (or 8px) scale.
3. **Type** — count distinct font sizes/weights in use. >5 sizes on one page = no hierarchy.
4. **Radius / elevation / borders** — collect every value; cluster into 2–4 tokens.
5. **Components** — list every component; flag components with >3 variants doing the same job, and any component styling itself from raw values.

Output: a token map, a violation list with counts, and the fix order (primitives first, then semantic mapping, then component cleanup). Never refactor a system in the same pass as auditing it — audit, report, then change.

## 4. SCALES (Fixed Reference)

- **Spacing:** 4/8/12/16/24/32/48/64/96. Gaps below 4px only for hairline borders. Never 5, 7, 10, 14px — unless a deliberate optical override is documented.
- **Type scale (fluid):** 12/14/16/18/24/32/48/64 rendered with `clamp()` where responsive.
- **Color ramps:** 9–11 steps from 50→950 in OKLCH (perceptually even), neutrals and at least one accent family. Dark mode = semantic mapping change, not new colors.
- **Elevation:** 3 levels max: flat (no shadow), raised (subtle, blur ≥ 16px, opacity ≤ 0.15), floating (blur ≥ 40px, opacity ≤ 0.2). Everything else is a bug.

## 5. COMPONENT ANATOMY (Every Component Ships With)

1. One job, one name. If a component has an "and" in its description, split it.
2. Full state matrix: default, hover, active/pressed, focus-visible, disabled, loading, error. If a state is impossible, document why.
3. Size variants only where real (sm/md/lg), never color variants pretending to be states.
4. Responsive behavior and the breakpoint where it changes.
5. Token references in code — zero raw values inside component styles.

## 6. DOCUMENTATION & GOVERNANCE

- One page per component: purpose, anatomy diagram (as code comment), state matrix, usage rules, do/don't examples, accessibility notes.
- Change process: token changes are additive (new token → deprecate old → remove after one release cycle). Never mutate a token value silently.
- Ownership: one person (or one skill) holds the token file. Component decisions route through it.
- **Adoption metrics (measure quarterly):** % of screens consuming semantic tokens, # of raw-color violations, # of off-scale spacing values, % of components with documented states. The number that matters: violation count trending down.

## 7. CHECKLIST (Fail the System If…)

- [ ] Any component references a primitive directly.
- [ ] Any UI uses a hex not present in the token set.
- [ ] Any spacing value off the scale without a documented override.
- [ ] Any component missing a disabled or focus-visible state.
- [ ] More than 3 elevation levels in use.
- [ ] Token names encode meaning AND value ("dark-purple" instead of semantic).
- [ ] Two components exist that do the same job with different APIs.

*Tokens are the memory of a design system. If the system can't remember, it repeats itself — and so do your pages.*