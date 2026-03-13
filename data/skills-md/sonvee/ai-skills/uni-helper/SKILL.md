---
name: uni-helper
description: Comprehensive skill reference for uni-helper ecosystem - AI-powered development tools for uni-app
metadata:
  author: FlippeDround
  version: "2026.1.30"
  source: Generated from https://github.com/uni-helper/website, skills located at https://github.com/uni-helper/ai-tools
---

> The skill is based on uni-helper documentation, generated at 2026-01-30.

uni-helper is an ecosystem of AI-powered development tools for uni-app, providing Vite plugins, utility libraries, TypeScript support, and development tools to enhance the uni-app development experience.

## Vite Plugins

| Topic | Description | Reference |
|-------|-------------|-----------|
| vite-plugin-uni-pages | File-based routing system for uni-app with auto page discovery | [plugin-pages](references/plugin-pages.md) |
| vite-plugin-uni-layouts | Nuxt-like layouts system for uni-app | [plugin-layouts](references/plugin-layouts.md) |
| vite-plugin-uni-components | On-demand automatic component imports | [plugin-components](references/plugin-components.md) |
| vite-plugin-uni-manifest | Write manifest.json in TypeScript | [plugin-manifest](references/plugin-manifest.md) |
| vite-plugin-uni-platform | File-based platform compilation (*.h5|mp-weixin|app.*) | [plugin-platform](references/plugin-platform.md) |
| vite-plugin-uni-platform-modifier | Platform modifiers for attributes/directives | [plugin-platform-modifier](references/plugin-platform-modifier.md) |
| vite-plugin-uni-middleware | Middleware support for uni-app routing | [plugin-middleware](references/plugin-middleware.md) |

## Libraries

| Topic | Description | Reference |
|-------|-------------|-----------|
| uni-use | VueUse-style composable utilities for uni-app | [lib-uni-use](references/lib-uni-use.md) |
| uni-network | Promise-based HTTP client for uni-app | [lib-uni-network](references/lib-uni-network.md) |
| uni-promises | Promise wrappers for uni-app APIs | [lib-uni-promises](references/lib-uni-promises.md) |
| uni-typed | TypeScript type definitions for uni-app templates | [lib-uni-typed](references/lib-uni-typed.md) |

## Utilities

| Topic | Description | Reference |
|-------|-------------|-----------|
| uni-env | Environment detection utilities for uni-app | [util-uni-env](references/util-uni-env.md) |
| unocss-preset-uni | UnoCSS preset for uni-app | [util-unocss-preset](references/util-unocss-preset.md) |

## Project Starters

| Topic | Description | Reference |
|-------|-------------|-----------|
| create-uni | CLI scaffolding tool for uni-app projects | [starter-create-uni](references/starter-create-uni.md) |
| vitesse-uni-app | Vite-powered uni-app starter template | [starter-vitesse](references/starter-vitesse.md) |

## Plugin Order Best Practices

When using multiple uni-helper Vite plugins, the recommended order is:

```ts
// vite.config.ts
export default defineConfig({
  plugins: [
    UniComponents(),  // 1. Component auto-import
    UniPages(),       // 2. File-based routing
    UniLayouts(),     // 3. Layout system
    UniManifest(),    // 4. Manifest generation
    UniPlatform(),    // 5. Platform-specific files
    UniPlatformModifier(), // 6. Platform modifiers
    UniMiddleware(),  // 7. Route middleware
    Uni(),            // 8. Official uni-app plugin (always last)
  ],
})
```

## Quick Start

Create a new uni-app project with create-uni:

```bash
# npm 7+, extra double-dash is needed
npm create uni@latest

# pnpm
pnpm create uni

# yarn
yarn create uni
```

## Official Resources

- Website: https://uni-helper.js.org
- GitHub: https://github.com/uni-helper
- NPM Scope: @uni-helper
