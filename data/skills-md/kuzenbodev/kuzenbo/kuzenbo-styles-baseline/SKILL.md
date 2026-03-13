---
name: kuzenbo-styles-baseline
description: Apply @kuzenbo/styles baseline global CSS with safe ordering and overrides in Kuzenbo apps. Use when tasks mention recommended.css, global focus rings, selection styles, scrollbar behavior, anchor offsets, reduced-motion behavior, or baseline style hardening.
---

# Kuzenbo Styles Baseline

Use this skill for external app code that consumes the stable public package `@kuzenbo/styles@0.0.6`.

## Runtime Setup

1. Install:

```bash
npm install @kuzenbo/styles
```

2. Import styles after theme CSS at app root:

```ts
import "@kuzenbo/theme/prebuilt/kuzenbo.css";
import "@kuzenbo/styles/recommended.css";
```

## Baseline Workflow

1. Keep `recommended.css` as the default global baseline.
2. Apply app-specific overrides by overriding exposed CSS variables, not by editing package files.
3. Set `--kb-anchor-offset` when sticky headers are present.
4. Verify focus-visible behavior and reduced-motion behavior after overrides.

## Guardrails

- Use public entrypoints only: `@kuzenbo/styles/recommended.css` or `@kuzenbo/styles/styles.css`.
- Do not duplicate the entire baseline file into app code.
- Keep semantic token compatibility with `@kuzenbo/theme`.
- If baseline behavior conflicts with app UX, override variables/selectors locally instead of removing the package globally.

## References

- `references/styles-entrypoints-and-behavior.md`
