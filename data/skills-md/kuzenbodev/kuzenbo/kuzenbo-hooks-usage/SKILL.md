---
name: kuzenbo-hooks-usage
description: Select and implement stable React hooks from @kuzenbo/hooks for state, browser APIs, storage, timing, viewport, and interaction patterns. Use when tasks mention hook selection, replacing ad-hoc effects/listeners, responsive behavior, clipboard/fullscreen flows, or client-only React behavior.
---

# Kuzenbo Hooks Usage

Use this skill for external app code that consumes the stable public package `@kuzenbo/hooks@0.0.6`.

## Runtime Setup

1. Install:

```bash
npm install @kuzenbo/hooks
```

2. For Next.js/client components that use browser APIs, add:

```tsx
"use client";
```

## Hook Selection Workflow

1. Read `references/hooks-by-category.md` to choose the right hook family.
2. Confirm the hook is in `references/hook-exports.md` before implementation.
3. Prefer dedicated hooks instead of manual event listeners, timers, or storage plumbing.
4. Keep business logic in app code and use hooks for state/effect wiring.

## Guardrails

- Use only exported hooks from `@kuzenbo/hooks`.
- Use `useFullscreenDocument` or `useFullscreenElement` (not `useFullscreen`).
- Browser-only hooks must run in client components.
- If a hook is missing from exports, state the gap and propose the closest exported alternative.

## References

- `references/hooks-by-category.md`
- `references/hook-exports.md`
