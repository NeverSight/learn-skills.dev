---
name: colorffy
description: Complete guide for Colorffy UI and CSS frameworks. Colorffy UI is a modern Vue 3 / Nuxt 3 component library with 70+ unstyled, headless components (buttons, cards, forms, dialogs, navigation, etc.) with TypeScript support. Colorffy CSS is an expressive SCSS framework with tonal color system, utility classes, and layout systems (grid, flexbox). Use when working with Colorffy packages, setting up Vue/Nuxt projects with Colorffy, choosing components, applying styles, using utility classes, implementing layouts, or integrating Colorffy UI with Colorffy CSS or custom styles.
---

# Colorffy

Complete framework for building Vue 3 and Nuxt 3 applications with Colorffy UI (component library) and Colorffy CSS (utility framework).

## Quick Reference Index

| Category | Guide | Description |
|----------|-------|-------------|
| **Getting Started** | **[Installation & Setup](references/installation.md)** | Install packages, configure Vue 3/Nuxt 3 |
| | **[Component Selection Guide](references/component-guide.md)** | Choose the right components for your needs |
| | **[Styling Guide](references/styling-guide.md)** | Colorffy CSS integration, custom styling approaches |
| **Theming** | **[Theming System](references/theming.md)** | Customize colors, typography, spacing, dark mode |
| **Reference** | **[Components API](references/components.md)** | Full reference for 70+ components |
| | **[CSS Utilities](references/utilities.md)** | Complete utility class reference |
| | **[Layout Systems](references/layout.md)** | Grid and Flexbox layout utilities |
| **Patterns** | **[Best Practices](references/best-practices.md)** | Common patterns, workflows, tips |

## Framework Overview

**Colorffy UI** (@colorffy/ui)
- 70+ Vue 3 components (buttons, forms, cards, dialogs, navigation, tables, etc.)
- Unstyled/headless by default - full control over styling
- TypeScript support, tree-shakeable
- Works with any styling approach

**Colorffy CSS** (@colorffy/css)
- Expressive SCSS framework with tonal color system
- Complete utility class library
- Flexible grid and flexbox layouts
- Dark mode support, customizable via SCSS variables

**Key Insight:** Colorffy UI components are unstyled by default. Style with Colorffy CSS, custom CSS, or any CSS framework.

## Quick Start

### Vue 3

```bash
npm install @colorffy/ui @colorffy/css
npm install @vueuse/components floating-vue
```

```typescript
// main.ts
import { createApp } from 'vue'
import ColorffyUI from '@colorffy/ui'
import '@colorffy/css'

const app = createApp(App)
app.use(ColorffyUI)
app.mount('#app')
```

### Nuxt 3

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  css: ['@colorffy/css']
})

// plugins/colorffy-ui.ts
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(ColorffyUI)
})
```

**[See complete installation guide →](references/installation.md)**

## Usage Example

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { UiButton, UiCard, UiInputText, UiModal } from '@colorffy/ui'

const isOpen = ref(false)
const name = ref('')
</script>

<template>
  <!-- Components with Colorffy CSS styling -->
  <UiCard class="shadow-lg rounded-lg">
    <template #body>
      <h2 class="text-primary fw-bold mb-3">Welcome</h2>
      <UiInputText 
        v-model="name" 
        label="Name"
        placeholder="Enter your name"
        class="mb-3"
      />
      <UiButton 
        variant="filled" 
        color="primary"
        text="Open Modal"
        @click="isOpen = true"
      />
    </template>
  </UiCard>

  <UiModal v-model="isOpen" title="Hello">
    <template #body>
      <p>Hello, {{ name }}!</p>
    </template>
  </UiModal>
</template>
```

## When to Read Each Guide

**[Installation & Setup](references/installation.md)** - When you need to:
- Install Colorffy in Vue 3 or Nuxt 3
- Configure SCSS customization
- Setup auto-imports
- Troubleshoot installation issues

**[Component Selection Guide](references/component-guide.md)** - When you need to:
- Choose the right component for a UI pattern
- Understand when to use one component vs another
- Find components by use case (forms, navigation, feedback, etc.)
- See component decision trees

**[Styling Guide](references/styling-guide.md)** - When you need to:
- Understand styling approaches (Colorffy CSS, custom, hybrid)
- Style components with Colorffy CSS utilities
- Write custom CSS for components
- Integrate with Tailwind, UnoCSS, or other frameworks

**[Theming System](references/theming.md)** - When you need to:
- Customize colors, typography, spacing
- Setup dark mode
- Override SCSS variables
- Configure design tokens

**[Components API](references/components.md)** - When you need to:
- Complete component API reference
- Specific props, slots, events documentation
- Component-specific features and options

**[CSS Utilities](references/utilities.md)** - When you need to:
- Specific utility class names
- Class patterns for spacing, colors, typography
- Responsive utility variants

**[Layout Systems](references/layout.md)** - When you need to:
- Build responsive layouts with grid or flexbox
- Understand column configurations
- Create complex layouts with alignment and gap utilities

**[Best Practices](references/best-practices.md)** - When you need to:
- Common patterns (forms, modals, tables, toasts)
- Code examples for typical use cases
- Performance tips and anti-patterns to avoid

## Component Categories Quick Reference

**Layout:** UiHeaderContent, UiPaneContent, UiCard
**Navigation:** UiTabs, UiNavigationBar, UiDrawerLink, UiSegmentedControls
**Buttons:** UiButton, UiButtonMenu, UiButtonToggleGroup, UiButtonTooltip
**Forms:** UiInputText, UiInputTextarea, UiInputSelect, UiInputCheck, UiInputRadio, UiInputRange, UiInputFile
**Dialogs:** UiModal, UiConfirmModal
**Feedback:** UiAlert, UiAlertToast, UiLoading, UiEmpty
**Data:** UiDatatable, UiListGroup, UiAccordion
**Media:** UiAvatar, UiIconMaterial

**[See complete component list →](references/components.md)**

## Utility Class Categories Quick Reference

**Spacing:** `m-*`, `p-*`, `gap-*` (0-5, responsive)
**Colors:** `text-*`, `bg-*`, `border-*` (primary, success, danger, etc.)
**Typography:** `fs-*` (100-600), `fw-*` (400-800), `text-{align}`
**Layout:** `d-flex`, `d-grid`, `justify-content-*`, `align-items-*`
**Borders:** `border`, `rounded-{size}`
**Effects:** `shadow-*`, `opacity-*`, `filter-*`

**[See complete utilities reference →](references/utilities.md)**

## Support

- **Issues:** [GitHub Issues](https://github.com/giancarlosgza/colorffy-workspace/issues)
- **Discussions:** [GitHub Discussions](https://github.com/giancarlosgza/colorffy-workspace/discussions)
