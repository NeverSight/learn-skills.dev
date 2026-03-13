---
name: korean-ime-handler
description: Use when generating text input components in Quasar (Vue) or NiceGUI that handle Korean or CJK IME composition - prevents double-enter bugs, lagging v-model binding, and isComposing issues
---

# Korean IME Input Optimization Guide

When generating components for Quasar (Vue) or NiceGUI that involve text input, strictly follow these patterns to prevent "double-enter" bugs and "lagging binding" issues common with Korean characters.

## 1. Quasar (Vue) Strategy

Native `v-model` in Vue 3/Quasar does not update during IME composition. Use explicit event binding instead.

### Recommended Implementation

- **Avoid:** `v-model="text"`
- **Use:** `:model-value` with `@input` or `@update:model-value` for real-time sync.
- **Prevent Double Enter:** Always check `event.isComposing` on Enter key events.

```vue
<template>
  <q-input
    :model-value="text"
    @input="val => { text = val }"
    @keydown.enter="handleEnter"
    label="한글 입력"
  />
</template>

<script setup>
const text = ref('');

const handleEnter = (e) => {
  // Prevent duplicate execution during IME composition
  if (e.isComposing) return;
  console.log('Submitted:', text.value);
};
</script>
```

## 2. NiceGUI (Python) Strategy

NiceGUI's `ui.input` defaults to `on_change`, which triggers late for Korean text. Use client-side JavaScript events for instant updates.

### Recommended Implementation

```python
from nicegui import ui

# Use 'on' with 'input' event for real-time IME tracking
input_ui = ui.input(label='한글 입력')
input_ui.on('input', f'() => {{ {input_ui.id}.value = event.target.value }}')

# Handle Enter without double-firing
input_ui.on('keydown.enter', '''
    (e) => {
        if (e.isComposing) return;
        // Trigger server-side logic here
    }
''')
```

## 3. Core Principles

- **Real-time:** IME composition must reflect in the state immediately without waiting for the block to finish.
- **Composition Awareness:** The `isComposing` flag is mandatory for any `keydown.enter` logic to avoid processing the same input twice.
