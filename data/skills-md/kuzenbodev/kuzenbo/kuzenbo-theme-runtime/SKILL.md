---
name: kuzenbo-theme-runtime
description: Configure @kuzenbo/theme runtime, prebuilt themes, and semantic token usage for Kuzenbo apps. Use when tasks mention ThemeProvider setup, theme bootstrap/hydration, light-dark behavior, token overrides, prebuilt theme selection, z-index/cursor tokens, or color token wiring.
---

# Kuzenbo Theme Runtime

Use this skill for external app code that consumes the stable public package `@kuzenbo/theme@0.0.6`.

## Runtime Setup

1. Install:

```bash
npm install @kuzenbo/theme next-themes
```

2. Load one prebuilt theme stylesheet at app root:

```ts
import "@kuzenbo/theme/prebuilt/kuzenbo.css";
```

3. Add bootstrap + provider in root layout:

```tsx
import { ThemeBootstrapScript, ThemeProvider } from "@kuzenbo/theme";

<ThemeBootstrapScript />
<ThemeProvider>{children}</ThemeProvider>
```

## Theme Workflow

1. Pick a prebuilt theme from `references/prebuilt-themes.md`.
2. Use semantic tokens from `references/theme-token-families.md` instead of hardcoded colors/z-index values.
3. Override tokens in CSS (`:root`, `.dark`, or scoped container) for customization.
4. Use runtime helpers from `references/theme-runtime-api.md` only when custom bootstrap behavior is required.

## Guardrails

- Keep theme CSS import and provider wiring in every Kuzenbo UI runtime.
- Avoid raw palette classes when a semantic token exists.
- Prefer `cursor-clickable` and z-index tokens instead of ad-hoc cursor/z-index literals.
- Keep imports on the public surface (`@kuzenbo/theme`, `@kuzenbo/theme/theme-provider`, `@kuzenbo/theme/prebuilt/*.css`).

## References

- `references/prebuilt-themes.md`
- `references/theme-runtime-api.md`
- `references/theme-token-families.md`
