---
name: using-reacticx
description: Use when adding Reacticx components to a React Native or Expo project, when asked about "reacticx" or "reactctx" components, or when integrating animated UI primitives via the Reacticx CLI.
---

# Using Reacticx

## Overview

[Reacticx](https://github.com/rit3zh/reacticx) is a copy-paste animated component library for React Native and Expo. Components are added to your project via CLI — there is no npm package to install.

## Quick Reference

| Task | Command |
|------|---------|
| Add a component | `npx reacticx add <cli-key>` |
| Add to specific dir | `npx reacticx add <cli-key> --dir src/components/ui` |
| List all components | `npx reacticx list` |
| List by category | `npx reacticx list -c molecules` |

> Use `bunx`, `npx`, or `pnpm dlx` depending on your package manager.

## Setup

Configure output directory in `component.config.json` at project root:

```json
{
  "outDir": "src/components/ui"
}
```

## Implementation Pattern

1. Check if the component already exists before adding.
2. Run `npx reacticx add <cli-key>`.
3. Install any missing dependencies listed in the component's docs.
4. Import and use the component from your `outDir`.
5. Run type-check and lint before committing.

## Dependency Notes

- Reacticx components depend on common RN animation libraries (Reanimated, Gesture Handler, Skia, etc.).
- `react-native-blur` used by some components is a **GitHub fork**: `sbaiahmed1/react-native-blur` — install with `npm install sbaiahmed1/react-native-blur` (not the npm `react-native-blur`).
- After adding any **native dependency**, rebuild the native target (e.g., `npx expo run:ios`) — a Metro restart alone is not enough.
- `react-native-skia` is published as `@shopify/react-native-skia` on npm.

## Component Catalog

See `references/components.md` for the full catalog of 95+ components organized by category (Base, Micro Interactions, Molecules, Organisms, Templates, Other). Each entry includes the CLI key, description, dependencies, and docs URL.

## Common Mistakes

- Installing `react-native-blur` from npm instead of the required GitHub fork (`sbaiahmed1/react-native-blur`).
- Forgetting to rebuild after adding native dependencies.
- Adding a component that already exists in `outDir`.
- Missing a dependency — always check the component's docs page for the exact install command.
