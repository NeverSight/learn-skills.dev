---
name: lucide-icons
description: Use Lucide icons correctly across any framework or environment. Lucide is a tree-shakeable SVG icon library with 1000+ icons. Use this skill when working with Lucide icons in React, Vue, Svelte, Solid, Preact, Angular, Astro, React Native, Vanilla JS, or static/server-side environments. Triggers include installing lucide icons, importing lucide components, customizing icon appearance, using dynamic icons, or using Lucide lab custom icons.
---

# Lucide Icons

Lucide provides framework-specific packages—each icon is an individually importable component/element that renders an inline SVG. All packages are fully tree-shakeable.

## Icon Naming

- Package exports use **PascalCase**: `Camera`, `ArrowRight`, `CircleAlert`
- CSS/HTML data attributes and icon font classes use **kebab-case**: `data-lucide="circle-alert"`, `icon-circle-alert`
- Find icon names at [lucide.dev/icons](https://lucide.dev/icons)

## Universal Props

All framework packages share the same core props:

| prop                  | type      | default      |
| --------------------- | --------- | ------------ |
| `size`                | number    | 24           |
| `color`               | string    | currentColor |
| `strokeWidth`         | number    | 2            |
| `absoluteStrokeWidth` | boolean   | false        |

All packages also accept any SVG presentation attribute as a prop (e.g. `fill`, `stroke-linejoin`).

## Best Practices

- **Always tree-shake**: Import only the icons you use. Never import `* as icons` in production bundles.
- **Direct icon imports** (e.g. `from 'lucide-react/icons/camera'`) improve build performance by bypassing the package barrel.
- **Dynamic by name**: Use `DynamicIcon` (React) or a generic wrapper only when icon names come from dynamic data (e.g. a CMS).
- **Accessibility**: Icons default to `aria-hidden="true"`. Add `aria-label` when the icon conveys meaning.

## Framework Reference Files

Read the relevant reference file for the framework in use:

| Framework / Environment         | Package               | Reference file                                                             |
| ------------------------------- | --------------------- | -------------------------------------------------------------------------- |
| React                           | `lucide-react`        | [references/lucide-react.md](references/lucide-react.md)                  |
| Vue 3                           | `lucide-vue-next`     | [references/lucide-vue-next.md](references/lucide-vue-next.md)            |
| Svelte 5 (or 4)                 | `@lucide/svelte`      | [references/lucide-svelte.md](references/lucide-svelte.md)                |
| SolidJS                         | `lucide-solid`        | [references/lucide-solid.md](references/lucide-solid.md)                  |
| Preact                          | `lucide-preact`       | [references/lucide-preact.md](references/lucide-preact.md)                |
| Angular                         | `lucide-angular`      | [references/lucide-angular.md](references/lucide-angular.md)              |
| Astro                           | `@lucide/astro`       | [references/lucide-astro.md](references/lucide-astro.md)                  |
| React Native                    | `lucide-react-native` | [references/lucide-react-native.md](references/lucide-react-native.md)    |
| Vanilla JS / HTML               | `lucide`              | [references/lucide.md](references/lucide.md)                              |
| Static / No-framework / Node.js | `lucide-static`       | [references/lucide-static.md](references/lucide-static.md)                |

## Lucide Lab (Custom / Unofficial Icons)

[Lucide lab](https://github.com/lucide-icons/lucide-lab) provides additional icons not in the main library. All packages support lab icons via their `Icon` component:

```jsx
// React example — same pattern works across React, Preact, Solid, Astro, Svelte, Vue
import { Icon } from 'lucide-react';
import { coconut } from '@lucide/lab';

<Icon iconNode={coconut} color="red" size={32} />
```