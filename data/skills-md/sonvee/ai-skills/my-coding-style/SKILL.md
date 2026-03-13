---
name: my-coding-style
description: My opinionated tooling and conventions for JavaScript/TypeScript projects.
metadata:
  author: Sove
  version: '2026.03.05'
---

## Coding Practices

### Code Organization

- **Single responsibility**: Each source file should have a clear, focused scope/purpose
- **Split large files**: Break files when they become large or handle too many concerns
- **Type separation**: When using TypeScript, Always separate types and interfaces into `types.ts` or `types/*.ts`
- **Constants extraction**: Move constants to a dedicated `constants.js` file

### Runtime Environment

- **Prefer isomorphic code**: Write runtime-agnostic code that works in Node, browser, and workers whenever possible
- **Clear runtime indicators**: When code is environment-specific, add a comment at the top of the file:

```js
// @env node
// @env browser
```

### TypeScript

- **Explicit return types**: Declare return types explicitly when possible
- **Avoid complex inline types**: Extract complex types into dedicated `type` or `interface` declarations

### Comments

- **Avoid unnecessary comments**: Code should be self-explanatory
- **Explain "why" not "how"**: Comments should describe the reasoning or intent, not what the code does

### Testing (Vitest)

- Test files: `foo.js` → `foo.test.js` (same directory)
- Use `describe`/`it` API (not `test`)
- Use `toMatchSnapshot` for complex outputs
- Use `toMatchFileSnapshot` with explicit path for language-specific snapshots

---

## App Development

### Framework Selection

| Use Case | Choice                              |
| -------- | ----------------------------------- |
| Frontend | Vite + Vue                          |
| Backend  | Nestjs + Prisma ORM v7 + PostgreSQL |

### Vue Conventions

| Convention    | Preference                         |
| ------------- | ---------------------------------- |
| Script syntax | Always `<script setup>`            |
| State         | Prefer `shallowRef()` over `ref()` |
| Objects       | Use `ref()`, avoid `reactive()`    |
| Styling       | UnoCSS                             |
| Utilities     | VueUse, Lodash                     |

### Vue Example

```vue
<template>
  <div>{{ count }}</div>
</template>

<script setup>
const props = defineProps({
  count: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['change'])
</script>

<style lang="scss" scoped></style>
```
