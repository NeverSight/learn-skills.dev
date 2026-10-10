---
name: m3-web-vue
description: Implement Material Design 3 in Vue.js using Vuetify 3 with M3-aligned theming, dynamic color, and component library. Covers theme setup, components, dark mode, and design tokens. Use this when building M3-styled Vue.js applications.
license: Apache-2.0
---

# Material Design 3 — Vue / Vuetify 3

## Overview

Vuetify 3 is the leading Material Design library for Vue.js with strong M3 support. Dynamic color theming, M3-aligned components, design tokens, and accessibility are built in.

**Keywords**: Material Design 3, M3, Vue, Vuetify, Vuetify 3, Vue.js, dynamic color, theming

## When to Use

- Vue.js projects
- Enterprise-ready M3 with excellent documentation
- When you need a large, well-maintained component library for Vue

## Install

```bash
npm install vuetify
```

## Theme Setup

```js
// plugins/vuetify.js
import { createVuetify } from 'vuetify';
import 'vuetify/styles';

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#6750A4',
          secondary: '#625B71',
          'surface-variant': '#E7E0EC',
          error: '#B3261E',
          background: '#FEF7FF',
          surface: '#FEF7FF',
        },
      },
      dark: {
        colors: {
          primary: '#D0BCFF',
          secondary: '#CCC2DC',
          background: '#141218',
          surface: '#141218',
        },
      },
    },
  },
});
```

## Component Examples

### Buttons

```vue
<template>
  <v-btn color="primary">Filled</v-btn>
  <v-btn variant="outlined">Outlined</v-btn>
  <v-btn variant="text">Text</v-btn>
  <v-btn variant="tonal">Tonal</v-btn>
  <v-btn variant="elevated">Elevated</v-btn>
</template>
```

### Cards

```vue
<template>
  <v-card elevation="1" rounded="lg">
    <v-card-title>Card Title</v-card-title>
    <v-card-text>Card content following M3 specs</v-card-text>
    <v-card-actions>
      <v-btn variant="text">Action</v-btn>
    </v-card-actions>
  </v-card>
</template>
```

### Text Fields

```vue
<template>
  <v-text-field label="Email" variant="outlined" />
  <v-text-field label="Name" variant="filled" />
</template>
```

### Navigation

```vue
<template>
  <v-bottom-navigation v-model="value">
    <v-btn value="home">
      <v-icon>mdi-home</v-icon>
      Home
    </v-btn>
    <v-btn value="search">
      <v-icon>mdi-magnify</v-icon>
      Search
    </v-btn>
  </v-bottom-navigation>

  <v-navigation-drawer>
    <v-list>
      <v-list-item title="Home" prepend-icon="mdi-home" />
      <v-list-item title="Settings" prepend-icon="mdi-cog" />
    </v-list>
  </v-navigation-drawer>
</template>
```

### Dialogs

```vue
<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-card>
      <v-card-title>Dialog Title</v-card-title>
      <v-card-text>Dialog content</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="dialog = false">Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
```

## Checklist

- [ ] Vuetify plugin configured with M3 color tokens
- [ ] Both light and dark themes defined
- [ ] Components use Vuetify's `color`, `variant`, and `rounded` props
- [ ] Typography inherits from Vuetify's type system
- [ ] Navigation components use proper M3 patterns

## Resources

- Vuetify: https://vuetifyjs.com/
- Vuetify Theming: https://vuetifyjs.com/en/features/theme/
- M3 adaptation: https://store.vuetifyjs.com/blogs/vuetify-blog/material-design-3-how-to-adapt-to-the-next-generation-of-interfaces
