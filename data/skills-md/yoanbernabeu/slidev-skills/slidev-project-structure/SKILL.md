---
name: slidev-project-structure
description: Understand Slidev project structure and configuration. Use this skill to configure themes, addons, and customize your presentation setup.
---

# Slidev Project Structure

This skill helps you understand the complete structure of a Slidev project, including configuration files, directory conventions, and customization options.

## When to Use This Skill

- Setting up a complex Slidev project
- Adding custom components or layouts
- Configuring themes and addons
- Understanding where to put assets and styles
- Troubleshooting project structure issues

## Standard Project Structure

```
my-presentation/
├── slides.md              # Main presentation file
├── package.json           # Project dependencies
├── components/            # Custom Vue components
│   └── Counter.vue
├── layouts/               # Custom layouts
│   └── my-layout.vue
├── pages/                 # Additional slide files
│   └── intro.md
├── public/                # Static assets
│   ├── images/
│   └── favicon.ico
├── styles/                # Global styles
│   └── index.css
├── setup/                 # Setup scripts
│   ├── main.ts           # Vue app setup
│   ├── monaco.ts         # Monaco editor setup
│   └── shiki.ts          # Shiki highlighter setup
├── snippets/              # External code snippets
│   └── example.ts
├── .slidev/               # Generated files (gitignore)
│   └── drawings/         # Persisted drawings
├── vite.config.ts         # Vite configuration
├── uno.config.ts          # UnoCSS configuration
└── netlify.toml           # Deployment config (optional)
```

## Core Files

### slides.md

The main presentation file containing all slides:

```markdown
---
theme: seriph
title: My Presentation
---

# Slide 1

---

# Slide 2
```

### package.json

Essential scripts and dependencies:

```json
{
  "name": "my-presentation",
  "private": true,
  "scripts": {
    "dev": "slidev --open",
    "build": "slidev build",
    "export": "slidev export"
  },
  "dependencies": {
    "@slidev/cli": "^0.50.0",
    "@slidev/theme-seriph": "^0.25.0"
  }
}
```

## Global Configuration

### Headmatter (First Slide)

The first slide's frontmatter configures the entire presentation:

```yaml
---
# Theme
theme: seriph
addons:
  - slidev-addon-excalidraw

# Metadata
title: My Presentation
titleTemplate: '%s - Slidev'
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

# Appearance
colorSchema: auto
aspectRatio: 16/9
canvasWidth: 980
themeConfig:
  primary: '#5d8392'

# Code
highlighter: shiki
lineNumbers: true
monaco: true

# Features
drawings:
  enabled: true
  persist: true
  presenterOnly: false
  syncAll: true
selectable: true
record: true

# Navigation
transition: slide-left
clicks: auto

# Export
exportFilename: my-presentation
download: true

# Layout
layout: cover
background: /cover.jpg
class: text-center
---
```

## Directory Conventions

### components/

Custom Vue components auto-imported into slides:

```vue
<!-- components/Counter.vue -->
<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div class="flex items-center gap-4">
    <button @click="count--">-</button>
    <span>{{ count }}</span>
    <button @click="count++">+</button>
  </div>
</template>
```

Use in slides:

```markdown
# Interactive Counter

<Counter />
```

### layouts/

Custom layouts extend built-in ones:

```vue
<!-- layouts/my-intro.vue -->
<template>
  <div class="slidev-layout my-intro">
    <div class="header">
      <slot name="header" />
    </div>
    <div class="main">
      <slot />
    </div>
    <div class="footer">
      <slot name="footer">
        <span>My Company</span>
      </slot>
    </div>
  </div>
</template>

<style scoped>
.my-intro {
  display: grid;
  grid-template-rows: auto 1fr auto;
  height: 100%;
  padding: 2rem;
}
</style>
```

Use in slides:

```markdown
---
layout: my-intro
---

::header::
# Welcome

::default::
Main content here

::footer::
Custom footer
```

### public/

Static assets served at root URL:

```
public/
├── images/
│   ├── logo.png        # Use: /images/logo.png
│   └── diagram.svg
├── favicon.ico         # Use: /favicon.ico
└── data.json           # Use: /data.json
```

### styles/

Global styles applied to all slides:

```css
/* styles/index.css */
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

:root {
  --slidev-theme-primary: #3b82f6;
}

.slidev-layout {
  font-family: 'Inter', sans-serif;
}

/* Custom utility classes */
.highlight {
  background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
  padding: 0 0.25em;
}
```

### setup/

Configuration scripts:

```typescript
// setup/main.ts - Vue app configuration
import { defineAppSetup } from '@slidev/types'

export default defineAppSetup(({ app, router }) => {
  // Register global components
  // Configure plugins
})
```

```typescript
// setup/shiki.ts - Code highlighter
import { defineShikiSetup } from '@slidev/types'

export default defineShikiSetup(() => {
  return {
    themes: {
      dark: 'vitesse-dark',
      light: 'vitesse-light',
    },
  }
})
```

```typescript
// setup/monaco.ts - Monaco editor
import { defineMonacoSetup } from '@slidev/types'

export default defineMonacoSetup(() => {
  return {
    editorOptions: {
      fontSize: 14,
      minimap: { enabled: false },
    },
  }
})
```

### pages/

Additional slide files for modular presentations:

```markdown
<!-- pages/intro.md -->
# Introduction Section

---

# About Me

---

# Agenda
```

Import in main file:

```markdown
---
src: ./pages/intro.md
---

---

# Main Content

---

---
src: ./pages/conclusion.md
---
```

## Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  slidev: {
    vue: {
      // Vue plugin options
    },
  },
  // Standard Vite options
  server: {
    port: 3030,
  },
})
```

## UnoCSS Configuration

```typescript
// uno.config.ts
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'bg-main': 'bg-white dark:bg-slate-900',
    'text-main': 'text-slate-900 dark:text-slate-100',
  },
  theme: {
    colors: {
      primary: '#3b82f6',
    },
  },
})
```

## Theme Configuration

### Using a Theme

```yaml
---
theme: seriph
themeConfig:
  primary: '#5d8392'
  secondary: '#8b5cf6'
---
```

### Ejecting a Theme

To customize a theme's source code:

```bash
slidev theme eject
```

This copies the theme to your project for full customization.

## Multi-File Presentations

### Importing Slides

```markdown
---
src: ./pages/section1.md
---

---
src: ./pages/section2.md
---
```

### With Frontmatter Merging

```markdown
---
src: ./pages/intro.md
title: Overridden Title
class: custom-class
---
```

## Generated Files (.slidev/)

The `.slidev/` directory contains:
- `drawings/` - Persisted drawings
- Other generated assets

Add to `.gitignore`:

```gitignore
.slidev
node_modules
dist
```

## Best Practices

1. **Keep slides.md focused**: Use `src` imports for large presentations
2. **Organize assets**: Use `public/images/` for all images
3. **Reuse components**: Create components for repeated patterns
4. **Version control**: Commit all source files except `.slidev/` and `dist/`
5. **Document custom layouts**: Add comments explaining slot usage

## Output Format

When explaining project structure, provide:

```
RECOMMENDED STRUCTURE:
├── slides.md           # Main file
├── components/         # Custom Vue components
├── layouts/           # Custom layouts
├── public/            # Static assets
├── styles/            # Global CSS
└── package.json       # Dependencies

KEY CONFIGURATION:
- Theme: [theme name]
- Addons: [list of addons]
- Custom components: [component names]
- Custom layouts: [layout names]

FILES TO CREATE:
1. [filename] - [purpose]
2. [filename] - [purpose]

GITIGNORE:
.slidev/
node_modules/
dist/
```
