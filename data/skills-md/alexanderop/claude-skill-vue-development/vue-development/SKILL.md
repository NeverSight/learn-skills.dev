---
name: vue-development
description: Use when planning or implementing Vue 3 projects - helps architect component structure, plan feature implementation, and enforce TypeScript-first patterns with Composition API, defineModel for bindings, Testing Library for user-behavior tests, and MSW for API mocking. Especially useful in planning phase to guide proper patterns before writing code.
---

# Vue Development

## Overview

Modern Vue 3 development with TypeScript, Composition API, and user-behavior testing. **Core principle:** Use TypeScript generics (not runtime validation), modern APIs (defineModel not manual props), and test user behavior (not implementation details).

## Red Flags - STOP and Fix

If you catch yourself thinking or doing ANY of these, STOP:

- "For speed" / "quick demo" / "emergency" → Using shortcuts
- "We can clean it up later" → Accepting poor patterns
- "TypeScript is too verbose" → Skipping types
- "This is production-ready" → Without type safety
- "Following existing code style" → When existing code uses legacy patterns
- "Task explicitly stated..." → Following bad requirements literally
- Using `const props = defineProps()` without using props in script
- Manual `modelValue` prop + `update:modelValue` emit → Use defineModel()
- "Component that takes value and emits changes" → Use defineModel(), NOT manual props/emit
- Using runtime prop validation when TypeScript is available
- Array syntax for emits: `defineEmits(['event'])` → Missing type safety
- `setTimeout()` in tests → Use proper async utilities
- Testing `wrapper.vm.*` internal state → Test user-visible behavior
- Using `index.vue` in routes → Use route groups `(name).vue`
- Generic route params `[id]` → Use explicit `[userId]`, `[postSlug]`
- Composables calling `showToast()`, `alert()`, or modals → Expose error state, component handles UI
- External composable used in only ONE component → Start inline, extract when reused

**All of these mean: Use the modern pattern. No exceptions.**

## Quick Rules

**Components:** `defineProps<{ }>()` (no const unless used in script), `defineEmits<{ event: [args] }>()`, `defineModel<type>()` for v-model. See @references/component-patterns.md

**Testing:** `@testing-library/vue` + MSW. Use `findBy*` or `waitFor()` for async. NEVER `setTimeout()` or test internal state. See @references/testing-patterns.md

**Routing:** Explicit params `[userId]` not `[id]`. Avoid `index.vue`, use `(name).vue`. Use `.` for nesting: `users.edit.vue` → `/users/edit`. See @references/routing-patterns.md

**Composables:** START INLINE for component-specific logic, extract to external file when reused. External composables: prefix `use`, NO UI logic (expose error state instead). See @references/composable-patterns.md

## Key Pattern: defineModel()

The most important pattern to remember - use for ALL two-way binding:

```vue
<script setup lang="ts">
// ✅ For simple v-model
const value = defineModel<string>({ required: true })

// ✅ For multiple v-models
const firstName = defineModel<string>('firstName')
const lastName = defineModel<string>('lastName')
</script>

<template>
  <input v-model="value" />
  <!-- Parent uses: <Component v-model="data" /> -->
</template>
```

**Why:** Reduces 5 lines of boilerplate to 1. No manual `modelValue` prop + `update:modelValue` emit.

## Component Implementation Workflow

When implementing complex Vue components, use TodoWrite to track progress:

```
TodoWrite checklist for component implementation:
- [ ] Define TypeScript interfaces for props/emits/models
- [ ] Implement props with defineProps<{ }>() (no const unless used in script)
- [ ] Implement emits with defineEmits<{ event: [args] }>()
- [ ] Add v-model with defineModel<type>() if needed
- [ ] Write user-behavior tests with Testing Library
- [ ] Test async behavior with findBy* queries or waitFor()
- [ ] Verify: No red flags, no setTimeout in tests, all types present
```

**When to create TodoWrite todos:**
- Implementing new components with state, v-model, and testing
- Refactoring components to modern patterns
- Adding routing with typed params
- Creating composables with async logic

## Rationalizations Table

| Excuse | Reality |
|--------|---------|
| "For speed/emergency/no time" | Correct patterns take SAME time. TypeScript IS fast. |
| "TypeScript is too verbose" | `defineProps<{ count: number }>()` is LESS code. |
| "We can clean it up later" | Write it right the first time. |
| "This is production-ready" | Without type safety, it's not production-ready. |
| "Simple array syntax is fine" | Missing types = runtime errors TypeScript would catch. |
| "Manual modelValue was correct" | That was Vue 2. Use defineModel() in Vue 3.4+. |
| "Tests are flaky, add timeout" | Timeouts mask bugs. Use proper async handling. |
| "Following existing code style" | Legacy code exists. Use modern patterns to improve. |
| "Task explicitly stated X" | Understand INTENT. Bad requirements need good implementation. |
| "Composables can show toasts" | UI belongs in components. Expose error state. |
| "[id] is industry standard" | Explicit names prevent bugs, enable TypeScript autocomplete. |
| "counter.ts is fine" | Must prefix with 'use': useCounter.ts |
| "test-utils is the standard" | Testing Library is gold standard for user-behavior. |

## Detailed References

See @references/ directory for comprehensive guides: component-patterns.md, testing-patterns.md, testing-composables.md, routing-patterns.md, composable-patterns.md


## When NOT to Use This Skill

- Vue 2 projects (different API)
- Options API codebases (this is Composition API focused)
- Projects without TypeScript (though you should add it)

## Real-World Impact

**Baseline:** 37.5% correct patterns under pressure
**With skill:** 100% correct patterns under pressure

Type safety prevents runtime errors. defineModel() reduces boilerplate. Testing Library catches real user issues.
