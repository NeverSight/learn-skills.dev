---
name: design-tokens
description: Design system foundation. Colors, typography, spacing. Single source of truth. No raw values.
---

# Design Tokens Skill

**One config. Consistent design. Zero guessing.**

## Purpose

Foundation layer for all UI. Every visual property comes from here.

## Output

```yaml
tokens_generated: true
tailwind_config: "tailwind.config.mjs"
css_variables: "src/styles/tokens.css"
design_token_verdict: PASS | WARN | FAIL
```

## Single Source of Truth

> **This skill is the ONLY source for visual tokens.**
> All UI skills consume from here. No local overrides.

Cross-references:
- `section-skeleton` → uses spacing/colors
- `astro-components` → uses all tokens
- `frontend-design` → uses all tokens

## Token Categories

| Type | Tokens | Usage |
|------|--------|-------|
| Semantic | `primary-*`, `accent`, `neutral-*` | Use in components |
| Utility | `spacing.*`, `font-*`, `shadow-*` | Internal mapping only |

**Rule:** Components use semantic tokens. Utility for internal only.

## Token Usage Scope

| Token | Allowed | Forbidden |
|-------|---------|-----------|
| `accent` | CTAs, links, highlights | Body text, backgrounds |
| `primary-900` | Headlines, body text | Buttons |
| `primary-100` | Section backgrounds | Text |
| `neutral-200` | Borders, dividers | CTAs |

**Wrong scope = WARN.**

## Forbidden Raw Values

| Type | Forbidden | Use Instead |
|------|-----------|-------------|
| Colors | `#FF6B35`, `rgb()` | `bg-accent`, `text-primary-900` |
| Spacing | `mt-[23px]` | `mt-6` |
| Font sizes | `text-[18px]` | `text-lg` |
| Shadows | `shadow-[...]` | `shadow-card` |
| Radius | `rounded-[12px]` | `rounded-lg` |

**Any raw value in component = FAIL.**

## A11y Contrast Requirements

| Combination | Min Ratio | Standard |
|-------------|-----------|----------|
| Body text on white | 4.5:1 | AA |
| Body text on primary-100 | 4.5:1 | AA |
| Large text (≥18px) | 3:1 | AA |
| CTA text on accent | 4.5:1 | AA |
| UI components | 3:1 | AA |

**Contrast fail = FAIL.**

## Color System

### Required

| Color | Tokens | Purpose |
|-------|--------|---------|
| Primary | 50-950 scale | Brand, text, backgrounds |
| Accent | DEFAULT, hover, light | CTAs, links |
| Neutral | 50-900 scale | Borders, backgrounds |
| Semantic | success, error, warning | Feedback |

### Usage

| Token | Use For |
|-------|---------|
| `primary-900` | Headlines, body |
| `primary-700` | Secondary text |
| `primary-100` | Light section bg |
| `accent` | CTAs, links |
| `accent-hover` | Button hover |

## Typography (Fluid Scale)

| Token | Range | Use |
|-------|-------|-----|
| `text-base` | 16-18px | Body |
| `text-lg` | 18-20px | Lead |
| `text-2xl` | 24-32px | H3 |
| `text-3xl` | 30-40px | H2 |
| `text-4xl/5xl` | 36-64px | H1 |

Font: `Inter` → `system-ui` → `sans-serif`

## Spacing (8px Grid)

| Token | Value | Use |
|-------|-------|-----|
| `py-12 md:py-20` | 48/80px | Section padding Y |
| `px-4 md:px-8` | 16/32px | Section padding X |
| `gap-6 md:gap-8` | 24/32px | Component gap |
| `p-4 md:p-6` | 16/24px | Card padding |

## Design Token Verdict

```yaml
design_token_verdict: PASS | WARN | FAIL
issues: []
```

| Condition | Verdict |
|-----------|---------|
| Raw value in component | FAIL |
| Contrast fail | FAIL |
| Missing required token | FAIL |
| Wrong token scope | WARN |
| Missing shade in scale | WARN |
| All rules pass | PASS |

## FAIL States

| Condition |
|-----------|
| Hardcoded hex in component |
| Arbitrary spacing `[Xpx]` |
| Contrast ratio below AA |
| Missing primary scale |
| Missing accent colors |

## WARN States

| Condition |
|-----------|
| Token used in wrong scope |
| Missing optional shades |
| Non-standard font loaded |

## Brand Intake

```yaml
brand_intake:
  primary_color: "#XXXXXX"
  accent_color: "#XXXXXX"
  font: Inter | Poppins | System
  style: Modern | Classic | Playful
  industry: removals | cleaning | trades | legal
```

## References

- [tailwind-config.md](references/tailwind-config.md) — Full config
- [color-generator.md](references/color-generator.md) — Shade generation
- [tokens-css.md](references/tokens-css.md) — CSS variables

## Definition of Done

- [ ] `tailwind.config.mjs` generated
- [ ] `tokens.css` with CSS variables
- [ ] Primary has full scale (50-950)
- [ ] Accent has hover + light
- [ ] Contrast passes AA
- [ ] No raw values in components
- [ ] design_token_verdict = PASS
