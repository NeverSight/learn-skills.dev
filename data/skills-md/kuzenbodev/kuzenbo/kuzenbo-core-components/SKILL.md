---
name: kuzenbo-core-components
description: Build and refactor React interfaces with @kuzenbo/core and @kuzenbo/theme. Use when tasks mention Kuzenbo components, subpath imports (@kuzenbo/core/ui/*), component selection, composition patterns, size tokens, accessibility behavior, or migration from custom UI to Kuzenbo primitives.
---

# Kuzenbo Core Components

Use this skill for external app code that consumes the stable public package `@kuzenbo/core@0.0.6`.

## Runtime Setup

1. Install runtime dependencies:

```bash
npm install @kuzenbo/core @kuzenbo/theme
```

2. Load one theme stylesheet once at app root:

```ts
import "@kuzenbo/theme/prebuilt/kuzenbo.css";
```

3. Add theme runtime wiring:

```tsx
import { ThemeBootstrapScript, ThemeProvider } from "@kuzenbo/theme";

<ThemeBootstrapScript />
<ThemeProvider>{children}</ThemeProvider>
```

4. Add `KuzenboProvider` only when global component defaults or env flags are needed.

## Canonical Imports

- Components: `@kuzenbo/core/ui/<component>`
- Provider/runtime helpers: `@kuzenbo/core/provider`
- Size helpers: `@kuzenbo/core/size`

## Implementation Workflow

1. Read `references/component-exports.md` and choose the smallest public component that satisfies the request.
2. Start with default component behavior and customize through `className` before introducing new variants.
3. Keep size values canonical: `xs | sm | md | lg | xl`.
4. Prefer compositional primitives (`Dialog`, `Popover`, `DropdownMenu`, `Sidebar`, `Tabs`) before custom wrappers.

## Guardrails

- Stay on the public stable surface listed in `references/component-exports.md`.
- Never import from package internals (`src/*`, `dist/*`, deep private files).
- Keep `@kuzenbo/theme` paired with `@kuzenbo/core` at runtime.
- If a requested component is not exported, state that clearly and compose from existing primitives.

## References

- `references/component-exports.md`
- `references/provider-and-size.md`
